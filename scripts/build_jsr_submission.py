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
import pathlib
import re
import shutil
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
ES = ROOT / "paper" / "manuscrito_revision_sistematica.md"
EN = ROOT / "paper" / "manuscript_systematic_review_en.md"
BIB = ROOT / "Bibliography_base.bib"
DESTINO_POR_DEFECTO = pathlib.Path.home() / "Desktop" / "Envio_JSR_Fagoterapia_Pseudomonas"

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


def limpia_tex(s):
    """Quita los envoltorios de LaTeX que el .bib usa para proteger mayúsculas."""
    s = re.sub(r"\{\\'\{?([aeiouAEIOU])\}?\}", lambda m: {
        "a": "á", "e": "é", "i": "í", "o": "ó", "u": "ú",
        "A": "Á", "E": "É", "I": "Í", "O": "Ó", "U": "Ú"}[m.group(1)], s)
    s = re.sub(r"\{\\o\}", "ø", s)
    s = re.sub(r"\{\\\"\{?([aouAOU])\}?\}", r"\1", s)
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
    a = autores_vancouver(limpia_tex(e.get("author", "")))
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

    meta = {
        "titulo_es": "Fagoterapia en infecciones por Pseudomonas aeruginosa "
                     "multirresistente: revisión sistemática de la estructura y "
                     "la verificabilidad del cuerpo de evidencia clínica",
        "titulo_en": "Phage therapy for multidrug-resistant Pseudomonas aeruginosa "
                     "infections: a systematic review of the structure and "
                     "verifiability of the clinical evidence base",
        "autores": "Danny Valdiviezo¹*  ·  Nataly Trelles²",
        "correo": "dvchiqui@gmail.com",
        "notas_autor": [
            "1* Danny Valdiviezo. ‹‹GRADO ACADÉMICO — COMPLETAR››, Facultad de "
            "Medicina, Universidad Católica de Cuenca. Azuay, Cuenca, Ecuador. "
            "dvchiqui@gmail.com: ‹‹ORCID — COMPLETAR››",
            "2 Nataly Trelles. ‹‹GRADO ACADÉMICO — COMPLETAR››, Facultad de "
            "Medicina, Universidad Católica de Cuenca. Azuay, Cuenca, Ecuador. "
            "‹‹CORREO — COMPLETAR››: ‹‹ORCID — COMPLETAR››",
            "‹‹RESOLVER ANTES DE ENVIAR: la autoría de N. Trelles conforme a "
            "ICMJE. Cumple el criterio de contribución sustancial (extrajo 98 de "
            "los 124 estudios de forma independiente) pero no ha aprobado esta "
            "versión ni puede responder por ella, al haberse retirado el 22 de "
            "agosto de 2026. Ver LEEME_ANTES_DE_ENVIAR.md››",
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

    docx_out = destino / "manuscrito_JSR.docx"
    escribe_docx(docx_out, bloques, meta, refs, tablas, figuras)
    print("  %-42s %d bloques, %d refs, %d tablas, %d figuras"
          % (docx_out.name, len(bloques), len(refs), len(tablas), len(figuras)))

    # Figuras y tablas, tal como salen del canal
    for sub, patrones in (("figuras", ("*.png", "*.pdf")), ("tablas", ("*.csv",))):
        dst = destino / sub
        dst.mkdir(exist_ok=True)
        n = 0
        for pat in patrones:
            for f in (ROOT / "paper" / sub).glob(pat):
                shutil.copy2(f, dst / f.name)
                n += 1
        print("  %-42s %d ficheros" % (sub + "/", n))

    print("\nescrito en %s" % destino)
    return 0


if __name__ == "__main__":
    sys.exit(main())
