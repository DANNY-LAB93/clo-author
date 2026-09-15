"""Arma el envío a Journal of Science and Research con el formato de la revista.

POR QUE EXISTE

El manuscrito autoritativo está escrito para una revista con estructura IMRaD y
citas autor-año. JSR (E-ISSN 2528-8083, Universidad Técnica de Babahoyo) usa
otra: RESUMEN / ABSTRACT / INTRODUCCIÓN / DESARROLLO / METODOLOGÍA / RESULTADOS
/ DISCUSIÓN Y CONCLUSIONES / REFERENCIAS BIBLIOGRÁFICAS, Times New Roman 12,
carta, y referencias Vancouver numeradas por orden de aparición.

QUE HACE Y QUE NO

Reordena y renumera. NO reescribe ni una cifra: el texto sale del manuscrito
autoritativo, que a su vez toma cada número de `synthesis_scalars.json`. Si un
dato cambia en el canal, se vuelve a correr esto y el envío queda al día.

Las declaraciones de honestidad —cribado por modelo de lenguaje como revisor
único, extracción por duplicado sin reconciliar, revisión no registrada— viajan
enteras. Son la parte del trabajo que más fácil se cae al cambiar de plantilla y
la que no puede caerse.

Uso:
    python scripts/build_jsr_submission.py [carpeta_destino]
"""
import csv
import datetime
import json
import pathlib
import re
import shutil
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
ES = ROOT / "paper" / "manuscrito_revision_sistematica.md"
EN = ROOT / "paper" / "manuscript_systematic_review_en.md"
BIB = ROOT / "Bibliography_base.bib"
DESTINO_POR_DEFECTO = pathlib.Path.home() / "Desktop" / "Envio_JSR_Fagoterapia_Pseudomonas"
SUPLEMENTOS = ROOT / "verificables revisión sistemática"

# Lista blanca de anexos: todo fichero cuyo nombre empiece por S<digito>_ o por 00_.
# Se elige inclusion por patron y no exclusion por lista para que un anexo nuevo
# entre solo en el paquete. Quedan fuera por construccion los cuatro renderizados
# del manuscrito y la subcarpeta «figuras y tablas», que no son suplementos y que
# ya viajan por su propio camino.
PATRON_ANEXO = re.compile(r"^(S\d{1,2}_|00_)")

# La pagina de envios de la revista: de ahi salen sus normas de formato y
# los dos formularios obligatorios. Leida el 2026-09-14.
PORTAL = "https://revistas.utb.edu.ec/index.php/sr/about/submissions"

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass


# --------------------------------------------------------------------------
# Bibliografía
# --------------------------------------------------------------------------
def lee_bib(ruta):
    """{clave: {campo: valor}}. Parser mínimo, suficiente para este .bib.

    No se usa `bibtexparser` porque no está instalado y traerlo por seis campos
    añadiría una dependencia al envío. Este .bib lo genera el propio proyecto y
    tiene una forma estable.
    """
    txt = ruta.read_text(encoding="utf-8")
    fuera = {}
    for m in re.finditer(r"@\w+\{([^,]+),(.*?)\n\}", txt, re.S):
        clave, cuerpo = m.group(1).strip(), m.group(2)
        campos = {}
        for c in re.finditer(r"(\w+)\s*=\s*\{(.*?)\}\s*,?\s*\n", cuerpo, re.S):
            campos[c.group(1).lower()] = " ".join(c.group(2).split())
        fuera[clave] = campos
    return fuera


# Los acentos que este .bib usa de verdad, contados sobre el fichero. La
# version anterior solo conocia el agudo sobre vocal, la o barrada y la
# dieresis, y dejaba pasar cinco mas: «Savovi{\'c}» salia como «Savovi\'c» en
# la lista de referencias, con la barra invertida a la vista.
ACENTOS = {
    "'": {"a": "á", "e": "é", "i": "í", "o": "ó", "u": "ú", "c": "ć", "n": "ń",
          "s": "ś", "z": "ź", "y": "ý",
          "A": "Á", "E": "É", "I": "Í", "O": "Ó", "U": "Ú", "C": "Ć"},
    "`": {"a": "à", "e": "è", "i": "ì", "o": "ò", "u": "ù",
          "A": "À", "E": "È", "I": "Ì", "O": "Ò", "U": "Ù"},
    '"': {"a": "ä", "e": "ë", "i": "ï", "o": "ö", "u": "ü",
          "A": "Ä", "E": "Ë", "I": "Ï", "O": "Ö", "U": "Ü"},
    "~": {"a": "ã", "n": "ñ", "o": "õ", "A": "Ã", "N": "Ñ", "O": "Õ"},
    "^": {"a": "â", "e": "ê", "i": "î", "o": "ô", "u": "û"},
    "c": {"c": "ç", "C": "Ç", "s": "ş", "S": "Ş"},      # cedilla: {\c c}
    "v": {"c": "č", "s": "š", "z": "ž", "C": "Č", "S": "Š", "Z": "Ž"},  # caron
}
SUELTOS = {"o": "ø", "O": "Ø", "ae": "æ", "AE": "Æ", "ss": "ß",
           "aa": "å", "AA": "Å", "l": "ł", "L": "Ł"}


def limpia_tex(s):
    """Quita los envoltorios de LaTeX que el .bib usa para proteger mayúsculas."""
    def acento(m):
        marca, letra = m.group(1), m.group(2)
        return ACENTOS.get(marca, {}).get(letra, letra)
    # El .bib escribe el mismo acento de tres formas: {\'o}, {\c{c}} y, sin
    # llave ninguna, Gr\'egory. Las tres tienen que caer, y la ultima se
    # escapaba: salia «Gr\'egory» con la barra a la vista en la referencia.
    s = re.sub(r"\{\\(['`\"~^cv])\s*\{?([A-Za-z])\}?\}", acento, s)
    s = re.sub(r"\\(['`\"~^])\s*\{?([A-Za-z])\}?", acento, s)
    s = re.sub(r"\\([cv])\s+\{?([A-Za-z])\}?", acento, s)
    s = re.sub(r"\{\\([a-zA-Z]{1,2})\}",
               lambda m: SUELTOS.get(m.group(1), m.group(1)), s)
    # Cursivas del titulo: los nombres de especie van en \textit{} y, al quitar
    # solo las llaves, quedaba «\textitPseudomonas» pegado. Se pasa a la marca
    # que el escritor de Word entiende.
    s = re.sub(r"\\(?:textit|emph)\{([^{}]*)\}", r"*\1*", s)
    s = re.sub(r"\\textbf\{([^{}]*)\}", r"**\1**", s)
    # Comillas de TeX: ``asi'' -> "asi".
    s = s.replace("``", "“").replace("''", "”")
    s = s.replace("\\&", "&").replace("\\_", "_").replace("\\#", "#")
    return s.replace("{", "").replace("}", "").replace("\\%", "%")


def autores_vancouver(campo):
    """«Apellido, Nombre and ...» -> «Apellido NN, Apellido NN, et al.»"""
    if not campo:
        return ""
    partes = [a.strip() for a in re.split(r"\s+and\s+", campo)]
    # BibTeX escribe «and others» donde la fuente pone «et al.». Tratarlo como
    # un apellido imprime un autor llamado «others», que no existe.
    abrevia = any(a.lower() in ("others", "et al.", "et al") for a in partes)
    partes = [a for a in partes if a.lower() not in ("others", "et al.", "et al")]
    fuera = []
    for a in partes:
        # AUTOR CORPORATIVO. El .bib lo protege con llaves --{{World Health
        # Organization}}-- justamente para que no se parta como un nombre de
        # persona. Sin esto salia "Organization WH", que es un autor que no
        # existe, en la referencia de la lista OMS 2024.
        if a.startswith("{") and a.endswith("}"):
            fuera.append(a[1:-1].strip())
            continue
        if "," in a:
            ape, nom = a.split(",", 1)
        else:
            trozos = a.split()
            ape, nom = trozos[-1], " ".join(trozos[:-1])
        ini = "".join(p[0] for p in nom.replace(".", " ").split() if p[:1].isalpha())
        fuera.append(("%s %s" % (ape.strip(), ini)).strip())
    if abrevia or len(fuera) > 6:
        return ", ".join(fuera[:6]) + ", et al."
    return ", ".join(fuera)


def referencia(e):
    """Una entrada en Vancouver, como las imprime la revista."""
    trozos = []
    # El orden importa: `limpia_tex` borra las llaves, y son justo lo que
    # distingue a un autor corporativo de una persona. Se limpia DESPUES de
    # formatear, no antes.
    a = limpia_tex(autores_vancouver(e.get("author", "")))
    if a:
        # «... et al.» ya trae su punto; anadir otro deja «et al..»
        trozos.append(a if a.endswith(".") else a + ".")
    if e.get("title"):
        trozos.append(limpia_tex(e["title"]).rstrip(".") + ".")
    rev = limpia_tex(e.get("journal") or e.get("publisher") or e.get("howpublished") or "")
    if rev:
        trozos.append(rev + ".")
    bit = e.get("year", "")
    if e.get("volume"):
        bit += ";%s" % e["volume"]
    if e.get("number"):
        bit += "(%s)" % e["number"]
    if e.get("pages"):
        bit += ":%s" % e["pages"].replace("--", "–")
    if bit:
        trozos.append(bit + ".")
    if e.get("doi"):
        trozos.append("https://doi.org/%s" % e["doi"])
    elif e.get("url"):
        trozos.append(e["url"])
    return " ".join(trozos)


# --------------------------------------------------------------------------
# Manuscrito -> estructura de la revista
# --------------------------------------------------------------------------
def secciones(texto):
    """{titulo: cuerpo} respetando el orden del documento."""
    fuera, actual, buf = {}, None, []
    for ln in texto.split("\n"):
        m = re.match(r"^(#{2,3})\s+(.*)$", ln)
        if m:
            if actual:
                fuera[actual] = "\n".join(buf).strip()
            actual, buf = m.group(2).strip(), []
        else:
            buf.append(ln)
    if actual:
        fuera[actual] = "\n".join(buf).strip()
    return fuera


def numera_citas(texto, orden):
    """[@a; @b] -> (1,2), asignando el número en el primer uso."""
    def rep(m):
        claves = [c.strip().lstrip("@") for c in m.group(1).split(";")]
        nums = []
        for c in claves:
            if c not in orden:
                orden[c] = len(orden) + 1
            nums.append(orden[c])
        return "(%s)" % ",".join(str(n) for n in sorted(nums))
    return re.sub(r"\[@([^\]]+)\]", rep, texto)


def a_parrafos(md):
    """Markdown a párrafos con marcas de negrita/cursiva resueltas para Word."""
    md = re.sub(r"^\s*[-*]\s+", "• ", md, flags=re.M)
    return [p.strip() for p in re.split(r"\n\s*\n", md) if p.strip()]


# --------------------------------------------------------------------------
# Word
# --------------------------------------------------------------------------
def escribe_docx(destino, bloques, meta, refs, tablas, figuras):
    import docx
    from docx.enum.text import WD_ALIGN_PARAGRAPH
    from docx.shared import Pt, Inches, RGBColor

    d = docx.Document()
    s = d.sections[0]
    s.page_width, s.page_height = Inches(8.5), Inches(11)
    for lado in ("left_margin", "right_margin", "top_margin", "bottom_margin"):
        setattr(s, lado, Inches(1))

    normal = d.styles["Normal"]
    normal.font.name = "Times New Roman"
    normal.font.size = Pt(12)
    normal.paragraph_format.space_after = Pt(10)
    normal.paragraph_format.line_spacing = 1.5

    cab = s.header.paragraphs[0]
    cab.text = "JOURNAL OF SCIENCE AND RESEARCH E-ISSN: 2528-8083"
    cab.runs[0].font.size = Pt(10)
    cab.runs[0].font.name = "Times New Roman"

    def parrafo(txt, negrita=False, centro=False, size=12, espacio=10,
                cursiva=False, sangria=None):
        p = d.add_paragraph()
        p.paragraph_format.space_after = Pt(espacio)
        if centro:
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        else:
            p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        if sangria is not None:
            p.paragraph_format.left_indent = Inches(0.5)
            p.paragraph_format.first_line_indent = Inches(-0.5)
        # **negrita** y *cursiva* dentro del texto
        for trozo in re.split(r"(\*\*[^*]+\*\*|\*[^*]+\*)", txt):
            if not trozo:
                continue
            r = p.add_run(trozo.strip("*") if trozo.startswith("*") else trozo)
            r.font.name = "Times New Roman"
            r.font.size = Pt(size)
            r.bold = negrita or trozo.startswith("**")
            r.italic = cursiva or (trozo.startswith("*") and not trozo.startswith("**"))
        return p

    parrafo(meta["titulo_es"], negrita=True, centro=True, espacio=6)
    parrafo(meta["titulo_en"], centro=True, cursiva=True, espacio=14)
    parrafo("AUTORES: " + meta["autores"], negrita=True, espacio=6)
    parrafo("DIRECCIÓN PARA CORRESPONDENCIA: " + meta["correo"], espacio=6)
    parrafo("Fecha de recepción:  /  /  ", espacio=2)
    parrafo("Fecha de aceptación:  /  /  ", espacio=14)
    # Notas de autor con el patron de la revista. Los huecos van marcados y
    # visibles a proposito: el ORCID y las credenciales no se inventan, y un
    # hueco que se ve se rellena, mientras que uno omitido se envia vacio.
    for nota in meta["notas_autor"]:
        parrafo(nota, size=10, espacio=4)
    parrafo("", espacio=12)

    for titulo, cuerpo in bloques:
        parrafo(titulo, negrita=True, espacio=8)
        for p in a_parrafos(cuerpo):
            parrafo(p)

    parrafo("REFERENCIAS BIBLIOGRÁFICAS", negrita=True, espacio=8)
    for i, r in enumerate(refs, 1):
        parrafo("%d. %s" % (i, r), size=11, espacio=6, sangria=True)

    # Tablas y figuras van al final, que es como se manda un original a
    # revision. La revista las coloca luego donde le convenga al maquetar.
    if tablas or figuras:
        d.add_page_break()
        parrafo("TABLAS Y FIGURAS", negrita=True, espacio=10)

    for titulo, cabecera, filas, nota in tablas:
        parrafo(titulo, negrita=True, espacio=6, size=11)
        tb = d.add_table(rows=1, cols=len(cabecera))
        tb.style = "Table Grid"
        for j, c in enumerate(cabecera):
            cel = tb.rows[0].cells[j]
            cel.text = ""
            r = cel.paragraphs[0].add_run(str(c))
            r.bold, r.font.size, r.font.name = True, Pt(9), "Times New Roman"
        for fila in filas:
            cs = tb.add_row().cells
            for j, v in enumerate(fila[:len(cabecera)]):
                cs[j].text = ""
                r = cs[j].paragraphs[0].add_run(str(v).replace("**", ""))
                r.font.size, r.font.name = Pt(9), "Times New Roman"
        if nota:
            parrafo(nota, size=9, espacio=14, cursiva=True)

    for titulo, ruta, nota in figuras:
        parrafo(titulo, negrita=True, espacio=6, size=11)
        try:
            d.add_picture(str(ruta), width=Inches(6.0))
            d.paragraphs[-1].alignment = WD_ALIGN_PARAGRAPH.CENTER
        except Exception as err:
            parrafo("[no se pudo incrustar %s: %s]" % (ruta.name, err), size=9)
        if nota:
            parrafo(nota, size=9, espacio=14, cursiva=True)

    d.save(destino)


# --------------------------------------------------------------------------



def mil(n):
    """Separador de millar fino, el mismo que el manuscrito: 23 057, no 23,057."""
    return "{:,}".format(n).replace(",", "\u202f")

def escribe_carta(destino, S, meta, n_anexos):
    """Carta al Comite Editorial, con las cifras del canal.

    Se genera por lo mismo que el resto: la version escrita a mano decia «sin
    restriccion de fecha» cuando hay ventana declarada, y daba por retirada a
    la segunda revisora tres dias despues de que volviera.
    """
    import docx
    from docx.enum.text import WD_ALIGN_PARAGRAPH
    from docx.shared import Pt, Inches

    d = docx.Document()
    s = d.sections[0]
    s.page_width, s.page_height = Inches(8.5), Inches(11)
    for lado in ("left_margin", "right_margin", "top_margin", "bottom_margin"):
        setattr(s, lado, Inches(1))
    n = d.styles["Normal"]
    n.font.name = "Times New Roman"
    n.font.size = Pt(12)
    n.paragraph_format.space_after = Pt(10)
    n.paragraph_format.line_spacing = 1.15

    def par(txt, alin=None):
        # Un solo add_paragraph(txt) pone TODO en redonda, y el binomio va en
        # cursiva. La carta es el primer documento que lee el Comite y llevaba
        # «Pseudomonas aeruginosa» sin cursivar, empezando por el titulo. Se
        # parte el texto en runs por los asteriscos, como en el manuscrito.
        pr = d.add_paragraph()
        for i, trozo in enumerate(re.split(r"\*([^*]+)\*", txt)):
            if not trozo:
                continue
            r = pr.add_run(trozo)
            r.italic = bool(i % 2)
        if alin is not None:
            pr.alignment = alin
        return pr

    par("Cuenca, Ecuador", WD_ALIGN_PARAGRAPH.RIGHT)
    for ln in ("Se\u00f1ores", "Comit\u00e9 Editorial", "Journal of Science and Research",
               "Universidad T\u00e9cnica de Babahoyo"):
        pr = d.add_paragraph(ln)
        pr.paragraph_format.space_after = Pt(0)
    d.add_paragraph("")
    par("Estimado Comit\u00e9 Editorial:")

    par("Someto a su consideraci\u00f3n el manuscrito \u00ab%s\u00bb, como art\u00edculo original de "
        "revisi\u00f3n sistem\u00e1tica." % meta["titulo_es"], WD_ALIGN_PARAGRAPH.JUSTIFY)

    par("El trabajo delimita de forma reproducible la literatura cl\u00ednica sobre "
        "fagoterapia en %s resistente y examina una pregunta que las s\u00edntesis "
        "publicadas han dado por resuelta sin comprobarla: si este cuerpo de "
        # El \u00abocho\u00bb estaba tecleado y el otro numero salia de `fuentes_n`, que
        # cuenta brazos y no fuentes. Ahora los dos vienen del canal, y la
        # frase dice lo que de verdad paso: nueve consultas porque Scopus se
        # interrogo dos veces.
        "evidencia admite una s\u00edntesis cuantitativa de eficacia. Se interrogaron %d "
        "bases de datos y registros con %d consultas \u2014Scopus en dos brazos\u2014, "
        "incluidos BVS y SciELO, que las revisiones previas han cubierto de "
        "forma desigual, con una ventana de publicaci\u00f3n de %d a %d aplicada en las "
        "que la admiten. De %s registros quedaron %s informes \u00fanicos, %d estudios y "
        "%d con publicaci\u00f3n recuperable."
        % ("*Pseudomonas aeruginosa*", S["fuentes_distintas_n"], S["fuentes_brazos_n"],
           S["anio_min"], S["anio_max"],
           mil(S["registros_identificados"]), mil(S["informes_unicos"]),
           S["estudios"], S["estudios_extraibles"]), WD_ALIGN_PARAGRAPH.JUSTIFY)

    par("La conclusi\u00f3n es que el cuerpo de evidencia es amplio y a la vez "
        "estructuralmente inadecuado para agregarse en proporciones globales de "
        "\u00e9xito, que es precisamente lo que la literatura reciente viene haciendo.",
        WD_ALIGN_PARAGRAPH.JUSTIFY)

    # El titulo dice \u00abcompletitud del reporte\u00bb, y ese genero suele significar
    # puntuar adherencia a una guia. Aqui no se puntuo ninguna, asi que la
    # aclaracion va por delante en vez de esperar a que la pregunten.
    par("Una precisi\u00f3n sobre el t\u00edtulo. La completitud de reporte que este trabajo "
        "mide no es adherencia a una gu\u00eda de publicaci\u00f3n: no se puntu\u00f3 CONSORT, ni "
        "CARE, ni STROBE. Se cont\u00f3 la presencia o la ausencia de las variables que "
        "una estimaci\u00f3n agrupada necesita \u2014clase de resistencia, \u00e1mbito, numerador, "
        "denominador y definici\u00f3n operativa del desenlace\u2014 sobre lo que cada informe "
        "publica.", WD_ALIGN_PARAGRAPH.JUSTIFY)

    # Lo que el comite va a preguntar, dicho antes de que lo pregunte. Cada
    # cifra sale de los escalares: si el canal cambia, la carta cambia con el.
    par("Declaro lo siguiente, por si el Comit\u00e9 lo considera al evaluar el trabajo. "
        "La revisi\u00f3n no est\u00e1 registrada en PROSPERO ni en ning\u00fan otro registro "
        "prospectivo, y as\u00ed se declara en el manuscrito. El cribado de t\u00edtulos y "
        "res\u00famenes lo emiti\u00f3 un modelo de lenguaje aplicando criterios y un "
        "vocabulario cerrado que los autores fijamos de antemano, como revisor \u00fanico "
        "y sin duplicaci\u00f3n independiente; los %d informes que lo superaron los "
        "revisamos uno a uno, y una submuestra de %d registros excluidos se recribó "
        "a ciegas en Rayyan sin encontrar ning\u00fan falso negativo. La extracci\u00f3n de "
        "datos se hizo por duplicado y de forma independiente sobre %d de los %d "
        "estudios, pero la adjudicaci\u00f3n por consenso de los desacuerdos no ha "
        "concluido: %d de %d siguen sin firmar. Por eso ninguna cifra del art\u00edculo "
        "procede de esos cuadernos; todas salen del cribado y de la pre-extracci\u00f3n "
        "desde res\u00famenes. Todo ello consta en M\u00e9todos y en Limitaciones, con la "
        "concordancia medida. Preferimos declararlo antes que omitirlo."
        % (S["informes_agrupados"], S["validacion_muestra"],
           S["extraccion_estudios_ambos"], S["extraccion_estudios_r1"],
           S["extraccion_conflictos_sin_firmar"], S["extraccion_desacuerdos"]),
        WD_ALIGN_PARAGRAPH.JUSTIFY)

    par("El manuscrito es original, no ha sido publicado ni est\u00e1 sometido a "
        "consideraci\u00f3n en otra revista. El canal de b\u00fasqueda, cribado y c\u00e1lculo est\u00e1 "
        "escrito en c\u00f3digo versionado y es reejecutable; queda a disposici\u00f3n de los "
        "revisores, junto con los %d anexos del material suplementario."
        % n_anexos, WD_ALIGN_PARAGRAPH.JUSTIFY)

    par("Agradezco de antemano su consideraci\u00f3n.", WD_ALIGN_PARAGRAPH.JUSTIFY)
    d.add_paragraph("")
    for ln in ("Atentamente,", "", "Danny Valdiviezo",
               "Facultad de Medicina, Universidad Cat\u00f3lica de Cuenca",
               "Cuenca, Ecuador \u00b7 %s" % meta["correo"]):
        pr = d.add_paragraph(ln)
        pr.paragraph_format.space_after = Pt(0)

    ruta = destino / "carta_de_presentacion.docx"
    d.save(ruta)
    return ruta

def poda(dst, escritos, etiqueta):
    """Retira del sobre lo que esta ejecucion no ha escrito.

    El bucle de copia solo anadia. Un anexo que cambia de nombre al cambiar la
    cifra que lleva --`S5_listado_184_estudios` paso a 162, a 158, a 157 y a
    155-- dejaba la version vieja en la carpeta de envio, y el script no la
    tocaba nunca mas. El 10 de septiembre viajaban cinco listados del corpus con
    cinco recuentos distintos, cuatro de ellos superados por el que el
    manuscrito publica. El sobre tiene que ser el reflejo de la ejecucion, no su
    sedimento.
    """
    sobra = [f for f in sorted(dst.iterdir())
             if f.is_file() and f.name not in escritos]
    for f in sobra:
        f.unlink()
    if sobra:
        print("  %-42s %d retirado(s) de ejecuciones anteriores: %s"
              % (etiqueta, len(sobra),
                 ", ".join(f.name for f in sobra[:4])
                 + (" ..." if len(sobra) > 4 else "")))
    return len(sobra)


def escribe_leeme(destino, S, anexos):
    """La hoja de instrucciones del envio, con las cifras del canal.

    Se genera y no se escribe a mano por lo de siempre: la version manual del
    23 de agosto seguia diciendo 724 desacuerdos y dando por retirada a la
    segunda revisora tres dias despues de que volviera.
    """
    pendientes = [
        "**ORCID de los dos autores.** La revista los pone en la nota al pie de "
        "cada autor, junto a las credenciales. En el articulo modelo se ve el "
        "formato: grado academico, filiacion, ciudad, pais, correo y ORCID.",
        "**La nota al pie de credenciales de cada autor**, con el mismo patron "
        "del modelo.",
        "**La autoria de N. Trelles conforme a ICMJE.** Cubre el criterio de "
        "contribucion sustancial: extrajo %d de los %d estudios de forma "
        "independiente, el %s %% del corpus, y sigue en el proyecto. Faltan los "
        "otros tres criterios, que son actos suyos y nadie puede firmar por "
        "ella: aprobar la version final, revisarla criticamente y aceptar "
        "responder por el trabajo. Recabadlo por escrito. Esto no deja rastro "
        "en el documento: no hay marcador que quitar, y el articulo se puede "
        "enviar sin que nada avise de que falta."
        % (S["extraccion_estudios_ambos"], S["extraccion_estudios_r1"],
           S["extraccion_doble_pct"]),
        "**El DOI del deposito**, solo si decidis depositar los datos y el "
        "codigo. Tampoco hay marcador: la declaracion de disponibilidad dice "
        "hoy que el codigo «se facilita a peticion», que es cierto tal como "
        "esta. Si depositais, hay que reescribir esa frase, no rellenar un "
        "hueco.",
        "**Fechas de recepcion y aceptacion.** Van en blanco a proposito: las "
        "pone la revista.",
        # Decia «exportar a PDF si lo piden, que aqui no hay conversor». Las
        # dos mitades eran falsas: la revista NO acepta PDF como fichero de
        # envio, y ya hay un PDF maquetado para leer.
        "**El PDF no se envia.** La lista de comprobacion de la revista dice "
        "que el fichero de envio va en «OpenOffice, Microsoft Word, RTF o "
        "WordPerfect»: lo que se sube es el `.docx`. Hay un PDF maquetado en "
        "`paper/pdf/manuscrito_JSR_final.pdf`, pero es para leer e imprimir. "
        "No esta convertido del `.docx` --en esta maquina no hay conversor-- "
        "sino maquetado aparte, asi que sus saltos de pagina pueden no "
        "coincidir con los de Word.",
    ]

    md = []
    md.append("# Envio a *Journal of Science and Research* \u2014 que hay aqui y que falta")
    # Si Word tenia el .docx abierto, el constructor escribio el bueno al lado
    # con el sufijo _NUEVO y el viejo sigue en la carpeta con el contenido de
    # la ejecucion anterior. El aviso va aqui, en la hoja que se lee antes de
    # enviar, porque el de la consola se lo lleva el primer scroll.
    nuevo = destino / "manuscrito_JSR_final_NUEVO.docx"
    if nuevo.exists():
        md.append("")
        md.append("> ## PARA. HAY DOS MANUSCRITOS EN ESTA CARPETA")
        md.append(">")
        md.append("> Word tenia `manuscrito_JSR_final.docx` abierto cuando se genero "
                  "este envio, asi que no se pudo sobrescribir. **El bueno es "
                  "`manuscrito_JSR_final_NUEVO.docx`**; el otro es de una ejecucion "
                  "anterior y su contenido esta desfasado.")
        md.append(">")
        md.append("> Cierra Word y vuelve a ejecutar `python scripts/build_jsr_submission.py`: "
                  "el bueno pasa a llamarse `manuscrito_JSR_final.docx`, el `_NUEVO` "
                  "desaparece y este aviso con el. **No mandes nada mientras este "
                  "parrafo siga aqui.**")
    md.append("")
    md.append("**Revista destino:** Journal of Science and Research, E-ISSN 2528-8083  ")
    md.append("(Universidad Tecnica de Babahoyo, Ecuador)  ")
    md.append("**Formato tomado de:** el articulo de Torres Vinueza y Prieto Fuenmayor, "
              "Vol. 9 N.\u00ba 2, abril\u2013junio 2024.  ")
    md.append("**Generado:** %s por `scripts/build_jsr_submission.py`. No lo edites a "
              "mano: se reescribe entero en cada ejecucion."
              % datetime.date.today().isoformat())
    md.append("")
    md.append("## Por que este envio existe")
    md.append("")
    md.append("Es una desviacion deliberada. El manuscrito estaba preparado para "
              "*Clinical Microbiology and Infection*, y ahi no cabe: **%s palabras de "
              "texto principal contra un limite de 3 500**, y el exceso son justamente "
              "las declaraciones de honestidad, que no se recortan. En JSR el problema "
              "desaparece: el articulo que sirvio de modelo ocupa 19 paginas. El "
              "manuscrito de CMI sigue vivo en el repositorio; esto no lo sustituye."
              % mil(S["palabras_cuerpo_es"]))
    # Ni el numero de anexos ni el de tablas se teclean: el primero sale de lo
    # que se acaba de copiar y el segundo del propio manuscrito. Escritos a mano
    # envejecian en silencio --el LEEME anunciaba 14 anexos «S0 a S13» cuando ya
    # eran 17, y una lista de comprobacion mandaba mirar 4 tablas de las 6 que
    # el articulo lleva--.
    numeros = sorted({int(m.group(1)) for m in
                      (re.match(r"^S(\d{1,2})_", n) for n in anexos) if m})
    jsr = ROOT / "paper" / "manuscrito_JSR_final.md"
    cuerpo = jsr.read_text(encoding="utf-8") if jsr.exists() else ""
    n_tablas = len(re.findall(r"^\*\*Tabla \d+\.", cuerpo, re.M))
    n_figuras = len(re.findall(r"^\*\*Figura \d+\.", cuerpo, re.M))

    md.append("")
    md.append("## Que hay en la carpeta")
    md.append("")
    md.append("| Fichero | Que es |")
    md.append("|---|---|")
    md.append("| `manuscrito_JSR_final.docx` | **EL FICHERO QUE SE SUBE.** Times New "
              "Roman 12, A4, interlineado 1,5. RESUMEN / ABSTRACT / INTRODUCCION / "
              "DESARROLLO / METODOLOGIA / RESULTADOS / DISCUSION Y CONCLUSIONES / "
              "DECLARACIONES / REFERENCIAS. Citas Vancouver numeradas. Las %d tablas y "
              "las %d figuras van donde el texto las cita, no en un anexo al final |"
              % (n_tablas, n_figuras))
    # El .pdf va al lado del .docx y con el mismo nombre: en el portal la unica
    # diferencia a la vista es la extension. Se declara aqui, en la fila de
    # despues, para que quien mire la tabla no tenga que deducirlo.
    pdf = destino / "manuscrito_JSR_final.pdf"
    if pdf.exists():
        md.append("| `manuscrito_JSR_final.pdf` | **El mismo articulo, para LEER. NO se "
                  "sube.** La revista pide Word, RTF u OpenOffice. Ojo: se llama igual "
                  "que el `.docx` y esta a su lado; en el portal la unica diferencia a "
                  "la vista es la extension. Ademas no esta convertido del `.docx` sino "
                  "maquetado aparte, asi que sus saltos de pagina pueden no coincidir |")
    md.append("| `carta_de_presentacion.docx` | Carta al Comite Editorial. Declara por "
              "adelantado lo que un revisor va a preguntar |")
    md.append("| `suplementos/` | Los %d anexos (S%d a S%d), el indice y la guia, en %d "
              "ficheros: los de datos van en `.xlsx` y en `.csv`. Empieza por "
              "`00_GUIA_DEL_MATERIAL_SUPLEMENTARIO.pdf`, que dice que pregunta contesta "
              "cada uno |" % (len(numeros), min(numeros), max(numeros), len(anexos)))
    md.append("| `figuras/`, `tablas/` | Las mismas figuras y tablas sueltas, por si las "
              "piden aparte |")
    leer = destino / "para_leer"
    if leer.is_dir() and any(leer.iterdir()):
        md.append("| `para_leer/` | **Nada de esto se sube.** El informe extendido "
                  "--la version larga, con la metodologia que el articulo condensa--, "
                  "las cuatro versiones del resumen con cual se envia marcada, y la "
                  "hoja con lo que va en cada hueco de la carta de cesion de la "
                  "revista. Estan en carpeta aparte para que no se suban por error: "
                  "el informe extendido tiene aspecto de manuscrito y no lo es |")
    # Lo escribe `build_criteria_table.py` en esta misma carpeta. El LEEME no lo
    # nombraba, y un fichero en el sobre que la hoja de instrucciones ignora
    # parece un resto de algo.
    suelto = destino / "tabla_criterios_inclusion_exclusion.docx"
    if suelto.exists():
        md.append("| `%s` | La Tabla 1 en un documento aparte, ya maquetada. Va tambien "
                  "dentro del articulo, donde el texto la cita; esta copia es por si el "
                  "portal pide los cuadros por separado. La escribe "
                  "`scripts/build_criteria_table.py` |" % suelto.name)
    md.append("")
    # LO QUE NO ESTA EN LA CARPETA Y TIENE QUE ESTAR. El LEEME no nombraba los
    # dos formularios de la revista, y sin ellos el envio ni siquiera entra en
    # revision. Se leyeron sus normas el 2026-09-14 --antes solo se decia
    # «confirmalo en el portal»-- y la lista de comprobacion es taxativa.
    md.append("")
    md.append("## Lo que NO esta aqui y sin lo cual no arranca la revision")
    md.append("")
    md.append("La revista provee dos formularios propios y hay que descargarlos de "
              "su seccion **Archivos y formatos descargables**, en "
              "<%s>. Su lista de comprobacion dice, literalmente: «No se iniciara "
              "el proceso de revision del articulo si antes no se encuentran en la "
              "plataforma (o en el correo de la revista) ademas del articulo, la "
              "carta de cesion de derechos y la informacion del(los) autor(es), en "
              "los formatos adecuados, los mismos que se encuentran en la seccion "
              "Archivos Suplementarios de la revista»." % PORTAL)
    md.append("")
    md.append("| Falta | Que es |")
    md.append("|---|---|")
    md.append("| **Carta de originalidad y cesion de derechos** | Formulario de la "
              "revista. Ocho puntos y la firma de los dos autores, con nombre, "
              "documento de identidad, correo, ORCID y filiacion. Lo que va en cada "
              "hueco esta en `para_leer/datos_carta_cesion.docx`, en este mismo sobre |")
    md.append("| **Formato de informacion de articulo y autores** | Otro formulario "
              "suyo, mas la hoja de calculo de informacion de autores |")
    md.append("")
    md.append("**No sirve una carta propia.** El envio se devuelve si no llega en el "
              "formato de ellos.")
    md.append("")
    md.append("Sus normas de formato, leidas el mismo dia, el manuscrito **las cumple "
              "todas**: A4, margenes de 3 cm, Times New Roman 12, interlineado 1,5, "
              "parrafos justificados y sin espacio entre consecutivos, titulo en "
              "mayuscula sostenida a 18 pt y por debajo de 20 palabras, resalte en "
              "cursiva y no en negrita, palabras clave en orden alfabetico y en "
              "negrita y cursiva, resumen de 250 palabras en el maximo de 250, y el "
              "cuerpo en 23 paginas contra un limite de 25 que en los articulos de "
              "revision no cuenta las referencias.")
    md.append("")
    md.append("Los anexos de datos viajan por partida doble: el `.xlsx` trae una hoja "
              "\u00abLeeme\u00bb y las columnas en castellano, y el `.csv` es la copia con los "
              "nombres internos que permite reejecutar el canal. Los `.csv` de esta "
              "carpeta van en UTF-8 **con BOM**, para que Excel respete las tildes al "
              "abrirlos con doble clic; si los lees desde codigo, abrelos como "
              "`utf-8-sig`.")
    md.append("")
    md.append("## Lo que TIENES que rellenar antes de mandarlo")
    md.append("")
    # Decia «Estan marcados en el .docx» y de los cuatro solo uno lo estaba,
    # despues de anadirlo: no habia ningun ORCID ni ningun hueco de autoria en
    # el documento. Mandar quitar un marcador que no existe hace creer que lo
    # que no se ve ya esta hecho.
    md.append("Son datos que no puedo inventar. **Solo el primero deja marca en el "
              "`.docx`**: un parrafo en negrita bajo el autor de correspondencia que "
              "empieza por COMPLETAR ANTES DE ENVIAR, y que hay que borrar entero al "
              "rellenarlo. Los demas no dejan rastro en el documento; se vigilan desde "
              "aqui.")
    md.append("")
    for i, t in enumerate(pendientes, start=1):
        md.append("%d. %s" % (i, t))
        md.append("")
    md.append("## Lo que NO hay que tocar")
    md.append("")
    md.append("Las declaraciones. Viajaron enteras desde el manuscrito autoritativo:")
    md.append("")
    md.append("- la revision **no esta registrada** en PROSPERO ni en ningun registro "
              "prospectivo;")
    md.append("- el cribado de titulos y resumenes lo emitio **un modelo de lenguaje "
              "como revisor unico**, con criterios y vocabulario cerrado fijados de "
              "antemano por los autores;")
    md.append("- la extraccion por duplicado **esta completa** (%d de %d estudios) pero "
              "**la adjudicacion no**: %d de los %d desacuerdos siguen sin firmar;"
              % (S["extraccion_estudios_ambos"], S["extraccion_estudios_r1"],
                 S["extraccion_conflictos_sin_firmar"], S["extraccion_desacuerdos"]))
    md.append("- **ninguna cifra del articulo procede de los cuadernos de extraccion**: "
              "todas salen del cribado y de la pre-extraccion desde resumenes.")
    md.append("")
    md.append("Quitar cualquiera de estas frases para que el articulo \u00abpase mejor\u00bb "
              "convierte un trabajo honesto en uno que no lo es. Si un revisor objeta "
              "alguna, se le contesta con los datos, que estan todos en `suplementos/`.")
    md.append("")
    md.append("## Como se regenera")
    md.append("")
    md.append("Desde `clo-author/`:")
    md.append("")
    md.append("```bash")
    md.append("python scripts/build_jsr_submission.py")
    md.append("```")
    md.append("")
    md.append("Reescribe el manuscrito, las figuras, las tablas, los suplementos y este "
              "fichero. Si tocas el manuscrito autoritativo "
              "(`paper/manuscrito_revision_sistematica.md`) o cualquier anexo, vuelve a "
              "correrlo. No edites el `.docx` a mano salvo para los datos de autor.")
    md.append("")
    md.append("## Antes de darle a enviar")
    md.append("")
    # Lo que BLOQUEA va primero. Antes la lista abria con los ORCID y cerraba
    # con «confirmalo en el portal»; los dos formularios sin los cuales la
    # revista ni empieza no estaban.
    for t in ("**Descargada, rellenada y FIRMADA la carta de cesion de derechos "
              "de la revista**, con los dos autores. Sin ella no arranca la "
              "revision",
              "**Descargado y rellenado el formato de informacion de articulo y "
              "autores**. Tampoco arranca sin el",
              "Subido el `.docx`, NO el PDF: la revista no acepta PDF como "
              "fichero de envio",
              "ORCID y credenciales de los dos autores",
              "Autoria de N. Trelles resuelta, marcador eliminado",
              "DOI del deposito, o marcador retirado si no hay deposito",
              "Leido entero una vez en Word, buscando saltos de formato",
              "Comprobado que las %d tablas y las %d figuras se ven bien"
              % (n_tablas, n_figuras)):
        md.append("- [ ] %s" % t)
    md.append("")

    ruta = destino / "LEEME_ANTES_DE_ENVIAR.md"
    ruta.write_text("\n".join(md), encoding="utf-8")
    return ruta

def main():
    destino = pathlib.Path(sys.argv[1]) if len(sys.argv) > 1 else DESTINO_POR_DEFECTO
    destino.mkdir(parents=True, exist_ok=True)

    bib = lee_bib(BIB)
    sec_es = secciones(ES.read_text(encoding="utf-8"))
    sec_en = secciones(EN.read_text(encoding="utf-8"))
    orden = {}

    def toma(d, *nombres):
        for n in nombres:
            for k in d:
                if k.lower().startswith(n.lower()):
                    return d[k]
        return ""

    resumen_es = toma(sec_es, "Resumen")
    resumen_en = toma(sec_en, "Abstract")
    intro = toma(sec_es, "1. Introducción")

    # La revista separa INTRODUCCIÓN (el problema) de DESARROLLO (el estado de
    # la cuestión). El manuscrito los lleva juntos en la introducción: se parte
    # por el punto donde deja de describir el problema y empieza a examinar lo
    # que las sintesis previas dan por supuesto.
    corte = intro.find("Pese a ello, las síntesis publicadas")
    if corte > 0:
        intro_txt, desarrollo = intro[:corte].strip(), intro[corte:].strip()
    else:
        intro_txt, desarrollo = intro, ""

    metodos = "\n\n".join(
        ("**%s**\n\n%s" % (k.split(" ", 1)[1], v)) if re.match(r"^2\.\d", k) else v
        for k, v in sec_es.items() if k.startswith("2.") or k == "2. Métodos")
    resultados = "\n\n".join(
        ("**%s**\n\n%s" % (k.split(" ", 1)[1], v)) if re.match(r"^3\.\d", k) else v
        for k, v in sec_es.items() if k.startswith("3.") or k == "3. Resultados")
    discusion = "\n\n".join(
        ("**%s**\n\n%s" % (k.split(" ", 1)[1], v)) if re.match(r"^4\.\d", k) else v
        for k, v in sec_es.items() if k.startswith("4.") or k == "4. Discusión")
    conclusiones = toma(sec_es, "5. Conclusiones")
    declaraciones = toma(sec_es, "Declaraciones")

    # Palabras clave: van fuera del cuerpo del resumen en esta revista
    mkw = re.search(r"\*\*Palabras clave:\*\*\s*(.+)", resumen_es)
    kw_es = mkw.group(1).strip() if mkw else ""
    resumen_es = re.sub(r"\*\*Palabras clave:\*\*.*", "", resumen_es).strip()
    mkw = re.search(r"\*\*Keywords:\*\*\s*(.+)", resumen_en)
    kw_en = mkw.group(1).strip() if mkw else ""
    resumen_en = re.sub(r"\*\*Keywords:\*\*.*", "", resumen_en).strip()

    bloques = [
        ("RESUMEN", resumen_es),
        ("Palabras clave: " + kw_es, ""),
        ("ABSTRACT", resumen_en),
        ("Keywords: " + kw_en, ""),
        ("INTRODUCCIÓN", intro_txt),
        ("DESARROLLO", desarrollo),
        ("METODOLOGÍA", metodos),
        ("RESULTADOS", resultados),
        ("DISCUSIÓN Y CONCLUSIONES", discusion + "\n\n" + conclusiones),
        ("DECLARACIONES", declaraciones),
    ]
    bloques = [(t, numera_citas(c, orden)) for t, c in bloques if c or t.startswith(("Palabras", "Keywords"))]

    faltan = [c for c in orden if c not in bib]
    if faltan:
        print("AVISO: %d citas sin entrada en el .bib: %s" % (len(faltan), ", ".join(faltan)))
    refs = [referencia(bib[c]) for c, _ in sorted(orden.items(), key=lambda x: x[1])
            if c in bib]

    S = json.loads((ROOT / "quality_reports" / "synthesis_scalars.json")
                   .read_text(encoding="utf-8"))
    meta = {
        "titulo_es": "Fagoterapia en infecciones por *Pseudomonas aeruginosa* "
                     "multirresistente: revisión sistemática de la literatura "
                     "clínica y la completitud de su reporte",
        "titulo_en": "Phage therapy for multidrug-resistant *Pseudomonas aeruginosa* "
                     "infections: a systematic review of the clinical "
                     "literature and its reporting completeness",
        "autores": "Danny Valdiviezo¹*  ·  Nataly Trelles²",
        "correo": "dvchiqui@gmail.com",
        "notas_autor": [
            "1* Danny Valdiviezo. ‹‹GRADO ACADÉMICO — COMPLETAR››, Facultad de "
            "Medicina, Universidad Católica de Cuenca. Azuay, Cuenca, Ecuador. "
            "dvchiqui@gmail.com: ‹‹ORCID — COMPLETAR››",
            "2 Nataly Trelles. ‹‹GRADO ACADÉMICO — COMPLETAR››, Facultad de "
            "Medicina, Universidad Católica de Cuenca. Azuay, Cuenca, Ecuador. "
            "‹‹CORREO — COMPLETAR››: ‹‹ORCID — COMPLETAR››",
            # N. Trelles se retiro el 22 de agosto y volvio el 26 con su
            # extraccion terminada. El marcador anterior decia que no podia
            # responder por el trabajo: dejo de ser cierto. Lo que sigue
            # abierto es distinto y mas pequeno, y son actos que solo ella
            # puede realizar. Las cifras salen de los escalares.
            "‹‹RESOLVER ANTES DE ENVIAR: la autoría de N. Trelles conforme a "
            "ICMJE. Cubre el criterio de contribución sustancial —extrajo %d de "
            "los %d estudios de forma independiente, el %s %% del corpus— y sigue "
            "en el proyecto. Faltan los otros tres criterios, que son actos "
            "suyos: aprobar esta versión final, revisarla críticamente y aceptar "
            "responder por el trabajo. Recabadlo por escrito antes de enviar y "
            "quitad este marcador. Ver LEEME_ANTES_DE_ENVIAR.md››"
            % (S["extraccion_estudios_ambos"], S["extraccion_estudios_r1"],
               S["extraccion_doble_pct"]),
        ],
    }

    # Las tablas salen del canal, no se reteclean. La primera fila del CSV es
    # la cabecera; el titulo y la nota viven en el .md hermano.
    tablas = []
    for csvf in sorted((ROOT / "paper" / "tablas").glob("*.csv")):
        with open(csvf, encoding="utf-8-sig", newline="") as fh:
            filas = list(csv.reader(fh))
        if not filas:
            continue
        md = csvf.with_suffix(".md")
        titulo, nota = csvf.stem.replace("_", " "), ""
        if md.exists():
            t_md = md.read_text(encoding="utf-8")
            mt = re.search(r"^\*\*(.+?)\*\*", t_md, re.M)
            mn = re.search(r"^\*Nota\.\*\s*(.+)$", t_md, re.M | re.S)
            if mt:
                titulo = mt.group(1).strip()
            if mn:
                nota = "Nota. " + " ".join(mn.group(1).split())
        tablas.append((titulo, filas[0], filas[1:], numera_citas(nota, orden)))

    figuras = [
        ("Figura 1. Diagrama de flujo PRISMA 2020.",
         ROOT / "paper" / "figuras" / "figura_1_prisma.png",
         "Nota. Corrientes separadas para bases bibliográficas y registros de "
         "ensayos. La unidad de inclusión es el estudio, no el informe."),
        ("Figura 2. Composición del cuerpo de evidencia recuperable.",
         ROOT / "paper" / "figuras" / "figura_2_composicion.png",
         "Nota. Sobre los estudios con publicación recuperable."),
    ]
    figuras = [(t_, r, n) for t_, r, n in figuras if r.exists()]

    # EL MANUSCRITO LO ESCRIBE UN SOLO GUION. Este construia el suyo desde el
    # maestro (`manuscrito_JSR.docx`) mientras `build_jsr_docx.py` construia el
    # de la revista (`manuscrito_JSR_final.docx`) en la misma carpeta: dos
    # ficheros llamandose los dos "el articulo", con 2 500 palabras de
    # diferencia, y este LEEME apuntando al que no era. Se delega.
    sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
    import build_jsr_docx
    build_jsr_docx.main()
    docx_out = destino / "manuscrito_JSR_final.docx"
    viejo = destino / "manuscrito_JSR.docx"
    if viejo.exists():
        viejo.unlink()
        print("  %-42s retirado: lo sustituye %s" % (viejo.name, docx_out.name))

    # EL PDF VIAJA EN EL SOBRE, por decision de D.V. el 2026-09-14. Va con el
    # mismo nombre que el .docx y a su lado, asi que la unica diferencia a la
    # vista en el portal es la extension: el LEEME lo declara como «para leer,
    # NO se sube» y la lista de comprobacion lo repite. La revista pide Word,
    # RTF u OpenOffice.
    pdf_origen = ROOT / "paper" / "pdf" / "manuscrito_JSR_final.pdf"
    if pdf_origen.exists():
        shutil.copy2(pdf_origen, destino / pdf_origen.name)
        print("  %-42s para leer; NO es el fichero de envio" % pdf_origen.name)
    else:
        print("  AVISO: no hay %s; correr antes scripts/build_jsr_pdf.py"
              % pdf_origen.name)

    # PARA_LEER: lo que acompana al envio sin ser parte de el. No va en la raiz
    # a proposito. Ahi ya hay dos ficheros que se llaman igual y solo se
    # distinguen por la extension; el informe extendido son 9 200 palabras con
    # aspecto de un tercer manuscrito, y en un portal OJS eso se sube por error.
    # Ademas el LEEME citaba `paper/docx/datos_carta_cesion.docx`, una ruta del
    # repositorio que no existe para quien solo tiene el sobre: ahora la hoja
    # viaja y la referencia deja de colgar.
    LECTURA = (
        ("informe_extendido.docx",
         "el informe extendido, con la metodologia que el articulo condensa"),
        ("resumen_estructurado.docx",
         "las cuatro versiones del resumen, con cual se envia marcada"),
        ("datos_carta_cesion.docx",
         "lo que va en cada hueco de la carta de cesion de la revista"),
    )
    leer_dst = destino / "para_leer"
    leer_dst.mkdir(exist_ok=True)
    puestos = set()
    for nombre, _ in LECTURA:
        f = ROOT / "paper" / "docx" / nombre
        if f.exists():
            shutil.copy2(f, leer_dst / nombre)
            puestos.add(nombre)
        else:
            print("  AVISO: falta paper/docx/%s" % nombre)
    print("  %-42s %d ficheros; ninguno se sube" % ("para_leer/", len(puestos)))
    poda(leer_dst, puestos, "para_leer/")

    # Figuras y tablas, tal como salen del canal
    for sub, patrones in (("figuras", ("*.png", "*.pdf")), ("tablas", ("*.csv",))):
        dst = destino / sub
        dst.mkdir(exist_ok=True)
        puestos = set()
        for pat in patrones:
            for f in (ROOT / "paper" / sub).glob(pat):
                shutil.copy2(f, dst / f.name)
                puestos.add(f.name)
        print("  %-42s %d ficheros" % (sub + "/", len(puestos)))
        poda(dst, puestos, sub + "/")

    # Material suplementario. Este paso no existia: el script escribia manuscrito,
    # figuras y tablas, y nada mas. Los tres anexos que aparecian en la carpeta de
    # envio habian entrado por una copia a mano, asi que el manuscrito citaba
    # catorce anexos y viajaban tres. Reejecutar el script no lo arreglaba: se
    # limitaba a rehacer lo que ya estaba.
    n_anexos = 0
    if not SUPLEMENTOS.is_dir():
        print("  AVISO: no existe %s; el paquete sale sin anexos" % SUPLEMENTOS.name)
    else:
        dst = destino / "suplementos"
        dst.mkdir(exist_ok=True)
        copiados = []
        # LOS .csv SALEN CON BOM, y solo aqui. En la carpeta del repositorio
        # dos de los diez lo llevan y ocho no, y cuatro de esos ocho tienen
        # tildes: Excel, al abrir un UTF-8 sin BOM, los lee como cp1252 y
        # ensena «MÃºltiple». Un revisor que abra S5 bien y S9 roto pensara que
        # los datos estan corruptos. No se normalizan las del repositorio
        # porque varios guiones las leen con `utf-8` a secas y el BOM les
        # metería ﻿ en el nombre de la primera columna; la copia del sobre
        # no la lee ningun guion.
        con_bom = 0
        for f in sorted(SUPLEMENTOS.iterdir()):
            if not (f.is_file() and PATRON_ANEXO.match(f.name)):
                continue
            if f.suffix.lower() == ".csv":
                b = f.read_bytes()
                if not b.startswith(b"\xef\xbb\xbf"):
                    b = b"\xef\xbb\xbf" + b
                    con_bom += 1
                (dst / f.name).write_bytes(b)
            else:
                shutil.copy2(f, dst / f.name)
            copiados.append(f.name)
        print("  %-42s %d ficheros%s"
              % ("suplementos/", len(copiados),
                 " (%d .csv marcados con BOM para Excel)" % con_bom if con_bom else ""))
        poda(dst, set(copiados), "suplementos/")

        # Cobertura: cada anexo que el manuscrito cita tiene que viajar. Se
        # contrasta contra el texto autoritativo y no contra una lista fija, para
        # que la comprobacion siga valiendo si el manuscrito cambia de anexos.
        citados = set(re.findall(r"\bS(\d{1,2})\b", ES.read_text(encoding="utf-8")))
        presentes = {m.group(1) for m in
                     (re.match(r"^S(\d{1,2})_", n) for n in copiados) if m}
        faltan = sorted(citados - presentes, key=int)
        if faltan:
            print("  AVISO: el manuscrito cita anexos que no se copiaron: %s"
                  % ", ".join("S" + s for s in faltan))
        else:
            print("  cobertura: viajan los %d anexos que el manuscrito cita"
                  % len(citados))

        n_anexos = len(presentes)
        leeme = escribe_leeme(destino, S, copiados)
        print("  %-42s instrucciones del envio" % leeme.name)

    carta = escribe_carta(destino, S, meta, n_anexos)
    print("  %-42s carta al comite" % carta.name)

    # El marcador de autor viaja dentro del .docx a proposito: sin el, un ORCID
    # que falta no se distingue de un ORCID que nadie pidio. El aviso suena en
    # cada ejecucion hasta que se rellena, para que nadie lo descubra en el
    # portal de la revista.
    jsr = ROOT / "paper" / "manuscrito_JSR_final.md"
    if jsr.exists() and "COMPLETAR ANTES DE ENVIAR" in jsr.read_text(encoding="utf-8"):
        print("\n  AVISO: el manuscrito sigue llevando el parrafo COMPLETAR ANTES DE "
              "ENVIAR.\n         Faltan los dos ORCID, las credenciales y el correo "
              "de N. Trelles.\n         Se rellena en paper/manuscrito_JSR_final.md y "
              "se vuelve a correr esto.")

    print("\nescrito en %s" % destino)
    return 0


if __name__ == "__main__":
    sys.exit(main())
