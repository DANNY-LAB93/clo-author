"""Arma el envío a Journal of Science and Research con el formato de la revista.

POR QUE EXISTE

El manuscrito autoritativo está escrito para una revista con estructura IMRaD y
citas autor-año. JSR (E-ISSN 2528-8083, Universidad Técnica de Babahoyo) usa
otra: RESUMEN / ABSTRACT / INTRODUCCIÓN / DESARROLLO / METODOLOGÍA / RESULTADOS
/ DISCUSIÓN Y CONCLUSIONES / REFERENCIAS BIBLIOGRÁFICAS, Times New Roman 12,
carta, y referencias Vancouver numeradas por orden de aparición.

QUE HACE Y QUE NO

Arma el sobre: manuscrito, carta, LEEME, tablas, figuras y suplementos. NO
reescribe ni una cifra. El `.docx` que se sube lo escribe `build_jsr_docx.py`
desde `paper/manuscrito_JSR_final.md`, y las cifras de la carta y del LEEME
salen de `synthesis_scalars.json`. Si un dato cambia en el canal, se vuelve a
correr esto y el envío queda al día.

Este docstring decía que el texto «sale del manuscrito autoritativo» y que las
declaraciones de honestidad «viajan enteras». No era así: el manuscrito de la
revista es un fichero aparte que se edita por su lado, y el 2026-10-08 el
maestro llevaba la declaración de uso de IA mientras el de la revista no la
llevaba, con el LEEME afirmando que «viajaron enteras». Ahora esa declaración
se comprueba de verdad: `exige_declaracion_ia` se niega a construir el sobre si
el párrafo «Uso de inteligencia artificial» del manuscrito de la revista no es,
letra por letra, el del maestro con las sustituciones de `SUSTITUCIONES_IA` y
ninguna más. Es la parte del trabajo que más fácil se cae al cambiar de
plantilla y la que no puede caerse.

Desde el 2026-10-13 la carta y el LEEME tampoco pueden afirmar lo que el
manuscrito de la revista no dice: lo que la carta declara y no sale de una
cifra se comprueba contra ese manuscrito (`CARTA_EN_REVISTA`), y lo que no
recoge pasa a la lista de lo que bloquea el envío. El LEEME abre, además, con
lo que dice el protocolo de la fase definitiva sobre el destino del piloto.

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
import unicodedata

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

# EL MANUSCRITO QUE SE SUBE. Es un fichero aparte del maestro, no una vista de
# el: lo que cambie en el maestro no llega aqui solo.
JSR_MD = ROOT / "paper" / "manuscrito_JSR_final.md"
JSR_PDF = ROOT / "paper" / "pdf" / "manuscrito_JSR_final.pdf"

# EL PROTOCOLO DE LA FASE DEFINITIVA (borrador para OSF). Dice que el informe
# piloto «no se enviará como tal», y este sobre es ese informe preparado para
# enviarse. El LEEME lo pone en cabeza mientras la frase siga ahí: se lee del
# protocolo y no se teclea.
PROTOCOLO = ROOT / "revision_sistematica" / "protocolo" / "protocolo_revision_sistematica.md"

# EL PARRAFO DE USO DE IA VIAJA LITERAL, Y SE COMPRUEBA. La declaracion
# canonica es la del maestro; el manuscrito de la revista la copia letra por
# letra. La unica diferencia admitida es la remision a las secciones del
# maestro, que el de la revista no numera. Cualquier otra diferencia --una
# frase de menos, una palabra cambiada-- hace que el sobre no se construya.
CABEZA_IA = "**Uso de inteligencia artificial.**"
SUSTITUCIONES_IA = (("(secciones 2.6 y 2.7)", "(véase Métodos)"),)
# Las que `exige_declaracion_ia` aplicó de verdad en esta ejecución. Desde el
# 2026-10-13 una sustitución cuya remisión el maestro ya no lleva se salta (si
# no queda ninguna remisión numerada), y el LEEME no puede decir que se aplicó.
IA_SUSTITUIDAS = None
# Una remisión a secciones numeradas, que el manuscrito de la revista no tiene.
REMISION_NUMERADA = re.compile(r"secci[oó]n(?:es)?\s+\d+\.\d")

# LAS NORMAS DE FORMATO QUE SE MIDEN, leidas en el portal el 2026-09-14. Son
# topes de la revista, no datos del trabajo: lo que se mide contra ellos sale
# del manuscrito y del PDF en cada ejecucion (`medidas_formato`).
TOPE_RESUMEN = 250        # palabras, contadas como las cuenta Word
TOPE_TITULO = 20          # palabras
TOPE_PAGINAS = 25         # paginas A4 a 1,5; en revisiones no cuentan las referencias
TOPE_CLAVES = (3, 5)      # palabras clave, minimo y maximo

# Las normas que aplica `build_jsr_docx.py` al construir el .docx y que aqui no
# se miden. Las que dependen del texto --titulo, resumen, palabras clave y
# extension-- se miden en cada ejecucion (`normas_formato`). La hoja de cesion
# usa la misma funcion con su propia lista, para que las dos no se contradigan.
NORMAS_APLICADAS = ("A4", "márgenes de 3 cm", "Times New Roman 12", "interlineado 1,5",
                    "párrafos justificados y sin espacio entre consecutivos",
                    "título en mayúscula sostenida y negrita a 18 pt",
                    "resalte en cursiva y no en negrita",
                    "palabras clave en negrita y cursiva")

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass


# --------------------------------------------------------------------------
# Guardas: lo que tiene que ser cierto antes de construir el sobre
# --------------------------------------------------------------------------
def sustituciones_txt(pares=None):
    """Las sustituciones, en texto. Por defecto, las aplicadas en esta ejecución
    si ya corrió la guarda, y si no las previstas."""
    if pares is None:
        pares = IA_SUSTITUIDAS if IA_SUSTITUIDAS is not None else SUSTITUCIONES_IA
    if not pares:
        return "ninguna sustitución"
    return "; ".join("«%s» por «%s»" % par for par in pares)


def parrafo_ia(ruta):
    """(párrafo, índice de línea, líneas) del párrafo de uso de IA de un manuscrito.

    El párrafo es una sola línea del markdown. Si no está, el párrafo es None.
    Si está dos veces no se elige uno: se para, porque cualquiera de los dos
    podría ser el que llega a la revista.
    """
    lineas = ruta.read_text(encoding="utf-8").split("\n")
    hallados = [i for i, l in enumerate(lineas) if l.startswith(CABEZA_IA)]
    if len(hallados) > 1:
        raise SystemExit("NO SE CONSTRUYE EL SOBRE: %s lleva %d párrafos «Uso de "
                         "inteligencia artificial» (líneas %s)."
                         % (ruta.name, len(hallados),
                            ", ".join(str(i + 1) for i in hallados)))
    if not hallados:
        return None, None, lineas
    return lineas[hallados[0]].rstrip(), hallados[0], lineas


def exige_declaracion_ia():
    """Se niega a construir el sobre si la declaración de uso de IA no viaja literal.

    Devuelve el párrafo tal como debe llevarlo el manuscrito de la revista. La
    comprobación es de igualdad exacta, no de parecido: la declaración no se
    resume ni se reescribe con otras palabras en ningún documento.
    """
    maestro, _, _ = parrafo_ia(ES)
    revista, n, lineas = parrafo_ia(JSR_MD)
    if maestro is None:
        raise SystemExit("NO SE CONSTRUYE EL SOBRE: el maestro (%s) no lleva el "
                         "párrafo «Uso de inteligencia artificial», que es la "
                         "declaración canónica." % ES.name)
    if revista is None:
        raise SystemExit("NO SE CONSTRUYE EL SOBRE: %s no lleva el párrafo «Uso de "
                         "inteligencia artificial». Se copia literal del maestro "
                         "(%s), en DECLARACIONES, con estas sustituciones y ninguna "
                         "más: %s." % (JSR_MD.name, ES.name, sustituciones_txt()))
    # Tiene que estar en DECLARACIONES: un parrafo literal colgado de otra
    # seccion, o detras de las referencias, no es la declaracion del articulo.
    titulos = [l[3:].strip() for l in lineas[:n] if l.startswith("## ")]
    if not titulos or titulos[-1].upper() != "DECLARACIONES":
        raise SystemExit("NO SE CONSTRUYE EL SOBRE: en %s el párrafo «Uso de "
                         "inteligencia artificial» (línea %d) está bajo «%s», no en "
                         "DECLARACIONES." % (JSR_MD.name, n + 1,
                                             titulos[-1] if titulos else "ninguna sección"))
    global IA_SUSTITUIDAS
    esperado, hechas = maestro, []
    for viejo, nuevo in SUSTITUCIONES_IA:
        veces = esperado.count(viejo)
        if veces == 0 and not REMISION_NUMERADA.search(esperado):
            # El maestro ya no remite a secciones numeradas: no hay nada que
            # sustituir y los dos parrafos tienen que ser iguales sin mas. Se
            # anadio el 2026-10-13, cuando el parrafo se reescribio a la vez en
            # los dos manuscritos; una remision numerada distinta sigue parando.
            continue
        if veces != 1:
            # El maestro cambio su remision. No se adivina la nueva: se para y
            # se corrige aqui, a la vista, y en el manuscrito de la revista.
            raise SystemExit("NO SE CONSTRUYE EL SOBRE: la declaración del maestro "
                             "lleva «%s» %d veces y la sustitución pide exactamente "
                             "una. Si el maestro cambió esa remisión, cambiad "
                             "SUSTITUCIONES_IA en este guion y volved a copiar el "
                             "párrafo en %s." % (viejo, veces, JSR_MD.name))
        esperado = esperado.replace(viejo, nuevo)
        hechas.append((viejo, nuevo))
    # Lo que quede numerado colgaria en la revista, que no numera secciones:
    # paso con «(sección 2.7)» en el bloque de riesgo de sesgo. En la
    # declaracion se para aqui en vez de viajar.
    m = REMISION_NUMERADA.search(esperado)
    if m:
        raise SystemExit("NO SE CONSTRUYE EL SOBRE: la declaración de uso de IA del "
                         "maestro remite a «%s», y el manuscrito de la revista no "
                         "numera secciones. Añadid esa remisión a SUSTITUCIONES_IA "
                         "en este guion y copiad el párrafo a %s con ella sustituida."
                         % (esperado[max(0, m.start() - 10):m.end() + 10], JSR_MD.name))
    IA_SUSTITUIDAS = hechas
    if revista != esperado:
        i = next((k for k, (a, b) in enumerate(zip(esperado, revista)) if a != b),
                 min(len(esperado), len(revista)))
        raise SystemExit(
            "NO SE CONSTRUYE EL SOBRE: el párrafo «Uso de inteligencia artificial» "
            "de %s (línea %d) no es el del maestro con %s.\nDifieren desde el "
            "carácter %d:\n  maestro, ya sustituido: …%s…\n  revista:                …%s…\n"
            "Se copia del maestro; no se edita aparte."
            % (JSR_MD.name, n + 1, sustituciones_txt(), i,
               esperado[max(0, i - 60):i + 60], revista[max(0, i - 60):i + 60]))
    return esperado


def exige_ia_en_docx(ruta, parrafo):
    """Y que el .docx que se sube la lleve entera.

    `build_jsr_docx.escribe` quita los asteriscos y pasa la negrita a cursiva;
    el texto del parrafo tiene que quedar igual, letra por letra.
    """
    import docx
    plano = parrafo.replace("*", "")
    if plano not in (p.text.strip() for p in docx.Document(str(ruta)).paragraphs):
        raise SystemExit("NO SE CONSTRUYE EL SOBRE: %s no lleva entero el párrafo "
                         "«Uso de inteligencia artificial» que sí está en %s. "
                         "No lo subáis: el .docx de la carpeta es el que acaba de "
                         "escribir build_jsr_docx.py." % (ruta.name, JSR_MD.name))


def pdf_al_dia(pdf, parrafo):
    """(si el PDF para leer puede viajar en el sobre, y si no, por qué).

    El PDF no se sube, pero viaja al lado del .docx, y lo maqueta aparte
    `build_jsr_pdf.py`. El 2026-10-08 el PDF era de las 22:23 y el manuscrito
    de la revista de las 23:05: el que habría viajado no llevaba la
    declaración de uso de IA que sí lleva el .docx. Un PDF anterior al
    manuscrito, o que no lleve el párrafo entero, no viaja.
    """
    if not pdf.exists():
        return False, "no hay PDF maquetado"
    if pdf.stat().st_mtime < JSR_MD.stat().st_mtime:
        return False, "el PDF maquetado es anterior a esta versión del manuscrito"
    try:
        import pymupdf
    except ImportError:
        try:
            import fitz as pymupdf
        except ImportError:
            return False, ("falta pymupdf para comprobar que el PDF lleva la "
                           "declaración de uso de IA")
    # Sin la cabecera ni el folio de cada página: un párrafo que cruza un
    # salto de página llevaba en medio «30 JOURNAL OF SCIENCE AND RESEARCH
    # E-ISSN…», y la comprobación daba por ausente un párrafo que estaba.
    def sin_cabecera(t):
        return "\n".join(
            l for l in t.split("\n")
            if not re.fullmatch(r"\s*\d*\s*(JOURNAL OF SCIENCE AND RESEARCH.*)?\s*", l))
    with pymupdf.open(str(pdf)) as doc:
        texto = "".join(sin_cabecera(p.get_text()) for p in doc)
    # El maquetador parte lineas, puede cortar palabras con guion y usar
    # ligaduras: se compara sin espacios ni guiones y en forma NFKC.
    def plano(t):
        return re.sub(r"[\s\-­‐‑]", "",
                      unicodedata.normalize("NFKC", t))
    if plano(parrafo.replace("*", "")) not in plano(texto):
        return False, ("el PDF maquetado no lleva entero el párrafo «Uso de "
                       "inteligencia artificial»")
    return True, ""


def casillas_abiertas():
    """(cuántas casillas quedan abiertas, si son justo las cerradas por regla).

    El LEEME decia «Las %d casillas sin acuerdo salen vacias» con el escalar
    `extraccion_conflictos_sin_firmar`, que cuenta DESACUERDOS sin firmar (0),
    no casillas abiertas: salia «Las 0 casillas» mientras S14 y S15 llevan 2
    ABIERTO. Las abiertas las cuenta `extraccion_adjudicada.json`. Que sean
    las cerradas por regla mecanica sin firma conjunta se comprueba casilla a
    casilla, no porque coincida el numero.
    """
    j = json.loads((ROOT / "quality_reports" / "extraccion_adjudicada.json")
                   .read_text(encoding="utf-8"))
    n = j["abiertas"]
    carpeta = ROOT / "revision_sistematica" / "extraccion"
    abiertas, por_regla = set(), set()
    with open(carpeta / "extraccion_adjudicada_procedencia.csv",
              encoding="utf-8-sig", newline="") as fh:
        for r in csv.DictReader(fh):
            for campo, origen in r.items():
                if origen == "ABIERTO":
                    abiertas.add((r["study_id"], r["arm_id"], campo))
    # La misma marca con la que `build_adjudicated_dataset.py` las deja abiertas.
    with open(carpeta / "extraction_conflicts.csv",
              encoding="utf-8-sig", newline="") as fh:
        for r in csv.DictReader(fh):
            if "SIN firma conjunta" in (r.get("resuelto_por") or ""):
                por_regla.add((r["study_id"], r["arm_id"], r["campo"]))
    return n, bool(n) and len(abiertas) == n and abiertas == por_regla


def marcadores(cuerpo):
    """Los huecos que el manuscrito de la revista lleva a la vista, por párrafo.

    [(etiqueta del párrafo, [marcadores])]. El LEEME decía que solo un párrafo
    dejaba marca en el .docx y que ni la autoría de N. Trelles ni el depósito
    tenían marcador; las dos cosas dejaron de ser ciertas sin que nada lo
    dijera. Ahora se leen del propio manuscrito.
    """
    fuera = []
    for l in cuerpo.split("\n"):
        ms = re.findall(r"\[DATO FALTANTE[^\]]*\]|‹‹[^›]*››", l)
        if ms:
            m = re.match(r"^\*\*([^*]+?)\*\*", l)
            fuera.append(((m.group(1) if m else l[:40]).strip().rstrip(".:"), ms))
    return fuera


def recoge(cuerpo, *alternativas):
    """Si algún párrafo del manuscrito lleva todos los trozos de alguna alternativa.

    Cada alternativa es una tupla de trozos que tienen que estar en el MISMO
    párrafo; no se distinguen mayúsculas ni el marcado de negrita y cursiva.
    """
    parrafos = [p.replace("*", "").lower() for p in re.split(r"\n\s*\n", cuerpo)]
    return any(all(t.lower() in p for t in alt)
               for alt in alternativas for p in parrafos)


# LO QUE LA CARTA AFIRMA Y TIENE QUE ESTAR EN EL MANUSCRITO DE LA REVISTA. La
# carta remata «Todo ello consta en Métodos y en Limitaciones», y el LEEME
# resume las declaraciones «el texto que vale es el del manuscrito». El
# 2026-10-13 la carta decia cosas que el manuscrito de la revista no traia
# --Rayyan, la fecha de cierre de la adjudicacion, el numero de anexos, que los
# 65 del corpus estaban entre los de doble extraccion-- y el LEEME, las 2
# casillas abiertas. Lo que no estaba se quito o paso a «dato del sobre». Lo que
# queda en la carta y no sale de una cifra del canal se comprueba aqui contra el
# manuscrito de la revista: (que dice la carta, alternativas de trozos que un
# mismo parrafo del manuscrito tiene que llevar). Si falta, el LEEME lo pone
# entre lo que bloquea el envio.
#
# Ajustado el 2026-10-14: la alternativa («endolisinas», «modelo») de las dos
# reglas pasaba con un parrafo que nombra las endolisinas y, en otra frase, una
# propuesta del modelo sobre la unidad de inclusion --no decia que el modelo
# metiera las reglas en sus guiones--; y («adjudica», «14 de septiembre») podia
# pasar con el parrafo de NOORG, firmado ese mismo dia. Se exige lo que la
# carta dice, no dos palabras sueltas.
CARTA_EN_REVISTA = (
    ("que el recribado de la muestra se hizo en Rayyan", (("Rayyan",),)),
    ("que la adjudicación de los desacuerdos se cerró el 14 de septiembre de 2026",
     (("adjudicación", "cerr", "14 de septiembre de 2026"),)),
    # DECIA «que el modelo propuso las dos reglas [...]» y «las propuestas de
    # criterios que decidieron los autores». Las dos reglas del 4-ago las añadió
    # el modelo sin decisión registrada, y de las propuestas solo NOORG consta
    # firmada por los dos (hoja de hechos, correcciones del 15-oct). Se exige
    # ahora quién decidió cada cosa, como lo dice la declaración.
    ("que el modelo añadió a mitad de lote, en sus guiones de cribado, las dos "
     "reglas del primer día sin que conste una decisión de los autores",
     (("dos reglas", "guiones de cribado",
       "sin que conste una decisión de los autores"),)),
    ("que el modelo redactó las propuestas de criterios que se adoptaron, y quién "
     "decidió cada una (D.V., por orden de D.V., o los dos autores)",
     (("propuestas de criterios que se adoptaron", "que decidió D.V.",
       "por orden de D.V.", "que firmaron los dos autores"),)),
    ("que el modelo redactó las ecuaciones de búsqueda y que, según declara D.V., "
     "D.V. las ejecutó", (("redactó las ecuaciones", "según declara D.V.",
                          "ejecutó D.V."),)),
    ("quién firmó las exclusiones a texto completo: los dos autores, D.V. solo, "
     "o la orden de D.V. sin que conste la firma de N.T.",
     (("exclusiones a texto completo", "las firmaron los dos autores",
       "las firmó D.V. solo", "sin que conste la firma de N.T."),)),
    ("que las reglas de desenlace las decidieron los dos autores según declara "
     "D.V., y que el registro las dejó como propuesta sin ratificar",
     (("reglas de desenlace", "según declara", "sin ratificar"),)),
    ("que el modelo propuso, con su cita, las exclusiones que se apoyan en lo que "
     "leyó", (("exclusiones que se apoyan",),)),
    ("que la concordancia del cribado sobre lo que el modelo admitió no se midió",
     (("concordancia", "no se midió", "admitió"),)),
    ("que el modelo redactó los registros de decisión",
     (("redactó", "registros de decisión"),)),
    ("que ProQuest se interrogó y lo que devolvió no se exportó",
     (("ProQuest", "no se exportaron"), ("ProQuest", "no se exportó"))),
)


def carta_sin_respaldo(cuerpo):
    """Lo que la carta afirma y el manuscrito de la revista no recoge."""
    return [que for que, alts in CARTA_EN_REVISTA if not recoge(cuerpo, *alts)]


def firmas_exclusiones(S):
    """Quién firmó las exclusiones a texto completo, desde los escalares
    `exclusiones_*` (2026-10-15). Hasta ese día 27 figuraban a nombre de los
    dos autores y solo consta la orden de D.V.; la carta, el LEEME y la hoja de
    cesión lo dicen con esta misma frase. Si N.T. ratifica por escrito alguna,
    el escalar baja y la frase cambia sola; con 0, la cláusula desaparece."""
    partes = ["%d las firmaron los dos autores" % S["exclusiones_firmadas_los_dos"]]
    if S["exclusiones_firmadas_solo_dv"]:
        partes.append("%d las firmó D.V. solo" % S["exclusiones_firmadas_solo_dv"])
    if S["exclusiones_orden_dv_sin_firma_nt"]:
        partes.append("%d se registraron por orden de D.V. sin que conste la firma "
                      "de N.T." % S["exclusiones_orden_dv_sin_firma_nt"])
    # Sin punto final: lo pone quien la usa. Si acaba en «N.T.», ya lo lleva.
    return ("De las %d exclusiones a texto completo, %s"
            % (S["estudios_excluidos_tras_texto_completo"], y_lista(partes)))


def con_punto(t):
    """La frase con su punto final, sin duplicarlo tras «N.T.»."""
    return t if t.endswith(".") else t + "."


def nombrados_sin_viajar(copiados):
    """Lo que el índice y la guía de `suplementos/` nombran y no viaja en el
    sobre, como {fichero de índice o guía: [nombres]}.

    Los dos se generan para el paquete entero del repositorio y se copian tal
    cual (consejo del 2026-10-15): nombraban S18b, «figuras y tablas» y los
    manuscritos de referencia, que `PATRON_ANEXO` deja fuera. Lo correcto es
    generarlos para el sobre en `build_editorial_report.py` y
    `build_package_guide.py`; mientras no se haga, el LEEME lo dice. Se busca
    sin espacios ni saltos de línea, porque el PDF parte los nombres largos."""
    ausentes = [p for p in SUPLEMENTOS.iterdir() if p.name not in copiados]
    if not ausentes:
        return {}
    plano = lambda t: re.sub(r"\s+", "", t).lower()
    textos = {}
    indice = SUPLEMENTOS / "00_INDICE.docx"
    if indice.exists():
        import docx
        dd = docx.Document(str(indice))
        trozos = [p.text for p in dd.paragraphs]
        trozos += [c.text for t in dd.tables for r in t.rows for c in r.cells]
        textos[indice.name] = plano("\n".join(trozos))
    guia = SUPLEMENTOS / "00_GUIA_DEL_MATERIAL_SUPLEMENTARIO.pdf"
    if guia.exists():
        try:
            import pymupdf
        except ImportError:
            try:
                import fitz as pymupdf
            except ImportError:
                pymupdf = None
        if pymupdf:
            with pymupdf.open(str(guia)) as doc:
                textos[guia.name] = plano("".join(pg.get_text() for pg in doc))
    # Un anexo se busca por su raíz («S18b_…», que el índice da como
    # «.xlsx + .csv»); lo demás, por el nombre entero, para no tomar por el
    # PDF de un manuscrito una mención de su `.md`.
    clave = lambda p: p.stem if (p.is_file() and re.match(r"S\d", p.name)) else p.name
    salida = {}
    for nombre, texto in textos.items():
        vistos = sorted({clave(p) for p in ausentes if plano(clave(p)) in texto})
        if vistos:
            salida[nombre] = vistos
    return salida


def leeme_sin_viajar(copiados):
    """Lo que la hoja «Léeme» de cada .xlsx de `suplementos/` nombra y no viaja,
    como {fichero: [raíces]}. La verificación de exactitud (2026-10-20) vio que
    la Léeme de S18 remite a S18b, que no va en el sobre, y el LEEME solo
    avisaba de lo que nombran el índice y la guía."""
    ausentes = [p for p in SUPLEMENTOS.iterdir() if p.name not in copiados]
    if not ausentes:
        return {}
    import openpyxl
    plano = lambda t: re.sub(r"\s+", "", t).lower()
    clave = lambda p: p.stem if (p.is_file() and re.match(r"S\d", p.name)) else p.name
    salida = {}
    for x in sorted(SUPLEMENTOS.glob("*.xlsx")):
        if x.name not in copiados:
            continue
        wb = openpyxl.load_workbook(str(x), read_only=True)
        if "Léeme" not in wb.sheetnames:
            wb.close()
            continue
        crudo = " ".join(str(c) for fila in wb["Léeme"].iter_rows(values_only=True)
                         for c in fila if c is not None)
        texto = plano(crudo)
        wb.close()
        # Las Léeme citan los anexos por su código («están en S18b»), no por el
        # nombre del fichero: se busca también el código como palabra suelta
        # («S18» no casa dentro de «S18b»). Su propia raíz no cuenta.
        def codigo(p):
            m = re.match(r"(S\d+[a-z]?)_", p.name)
            return m.group(1) if m else None
        vistos = sorted({clave(p) for p in ausentes
                         if not x.stem.startswith(clave(p)) and (
                             plano(clave(p)) in texto or (
                                 codigo(p) and codigo(p) != codigo(x) and re.search(
                                     r"(?<![\w])%s(?![\w])" % codigo(p), crudo)))})
        if vistos:
            salida[x.name] = vistos
    return salida


def y_lista(cosas):
    """«a, b y c»."""
    cosas = list(cosas)
    return (", ".join(cosas[:-1]) + " y " + cosas[-1]) if len(cosas) > 1 else \
        "".join(cosas)


def ojo_indice_guia(copiados):
    """El aviso del LEEME sobre lo que el índice y la guía nombran y no viaja
    (consejo del 2026-10-15): se dice, no se calla. Vacío si no nombran nada."""
    por_lista = {}
    for doc, ns in nombrados_sin_viajar(copiados).items():
        por_lista.setdefault(tuple(ns), []).append(doc)
    return "".join(
        ". **Ojo**: %s %s el paquete entero del repositorio y %s también %s, que "
        "no van en este sobre" % (y_lista("`%s`" % d for d in docs),
                                  "describen" if len(docs) > 1 else "describe",
                                  "nombran" if len(docs) > 1 else "nombra",
                                  y_lista("`%s`" % n for n in ns))
        for ns, docs in por_lista.items()) + "".join(
        ". La hoja Léeme de `%s` remite también a %s, que no %s en este sobre"
        % (x, y_lista("`%s`" % n for n in ns), "van" if len(ns) > 1 else "va")
        for x, ns in leeme_sin_viajar(copiados).items())


def pendiente_de_nt(S):
    """Lo que N.T. tiene que saber o ratificar antes de aprobar la versión
    final, como (título, texto). Lo comparten el LEEME («Lo que deciden los
    autores antes de enviar») y la hoja de cesión (`build_cesion_datos.py`):
    firmar la cesión es aprobar el contenido. Sale del registro de decisión
    del 2026-10-15 (`2026-10-15_firmas-de-n-trelles-sin-respaldo.md`); las
    cifras, de los escalares, y cada punto desaparece cuando su escalar llega a
    0. El del mensaje del 1-sep no lo cierra ningún dato: lo cierra que N.T. lo
    sepa antes de aprobar."""
    nota = "revision_sistematica/extraccion/firma_nataly/NOTA_2026-10-15.md"
    registro = "quality_reports/decisions/2026-10-15_firmas-de-n-trelles-sin-respaldo.md"
    puntos = []
    if S["exclusiones_orden_dv_sin_firma_nt"]:
        puntos.append((
            "Las %d exclusiones registradas por orden de D.V. sin firma de N.T."
            % S["exclusiones_orden_dv_sin_firma_nt"],
            "Se registraron el 1 y el 2 de septiembre de 2026 por orden de D.V.; "
            "figuraban a nombre de los dos autores sin cuaderno firmado detrás, y "
            "desde el 15 de octubre `exclusiones_tras_texto_completo.csv` dice que "
            "no consta la firma de N.T. Si N.T. está de acuerdo, las ratifica por "
            "escrito en un cuaderno de firma como los demás, que entra por un "
            "guion `ingest_*`, nunca escrito a mano en el CSV. Mientras no lo haga, "
            "los documentos dicen que no consta su firma (ver `%s`)." % registro))
    puntos.append((
        "El mensaje del 1 de septiembre de 2026 con el que se pidió a N.T. firmar "
        "las correcciones de modalidad lo redactó el modelo",
        "Lo redactó el modelo en primera persona de D.V., y presentaba como lectura "
        "de D.V. la que había hecho el modelo; N.T. firmó con ese texto delante. "
        "N.T. tiene que saberlo antes de aprobar la versión final (ver `%s`)."
        % nota))
    if S["pares_solapamiento_sin_firma"]:
        puntos.append((
            "Los %d descartes de solapamiento del modelo sin firma"
            % S["pares_solapamiento_sin_firma"],
            "De los %d pares de estudios que podían compartir pacientes, %d "
            "veredictos llevan la firma de los dos autores; los otros %d los "
            "descartó la lectura del modelo del 22 de septiembre de 2026, y no "
            "consta la firma de ninguno de los dos autores. Los autores deciden si "
            "los firman, por escrito (ver `%s`)."
            % (S["pares_solapamiento_examinados"], S["pares_solapamiento_firmados"],
               S["pares_solapamiento_sin_firma"], registro)))
    return puntos


def frase_piloto():
    """La frase del protocolo de la fase definitiva que dice que el informe
    piloto no se enviará, literal; o None si el protocolo ya no la lleva."""
    if not PROTOCOLO.exists():
        return None
    m = re.search(r"[^.\n›]*no se enviar[áa][^.\n]*\.",
                  PROTOCOLO.read_text(encoding="utf-8"))
    return m.group(0).strip() if m else None


def responsabilidad_ajena(cuerpo):
    """La frase del manuscrito que hace responder por el trabajo a los dos
    autores, o None. N.T. no ha aceptado responder por él (criterio 4 del
    ICMJE): mientras no conste por escrito, la frase solo puede hablar por D.V.
    El 2026-10-13 la declaración de IA decía «Los autores asumen la
    responsabilidad», y el LEEME, a la vez, que N.T. no lo había aceptado."""
    m = re.search(r"(?:Los|Ambos|Los dos) autores asumen la responsabilidad[^.]*\.",
                  cuerpo)
    return m.group(0) if m else None


def responsabilidad_pendiente(cuerpo):
    """La frase del manuscrito que deja pendiente la responsabilidad de N.T., o
    None. Desde el 2026-10-13 la declaración de uso de IA dice «D.V. asume la
    responsabilidad [...]; la de N.T. queda pendiente de su aprobación escrita».
    Depende del mismo escrito que el marcador del CRediT de N.T.: cuando conste,
    la frase cambia en el maestro y se copia igual a la revista, o el
    manuscrito seguiría diciendo «pendiente» de algo ya hecho."""
    m = re.search(r"(?:D\.\s?V\.|D\. Valdiviezo) asume la responsabilidad"
                  r"[^\n]*?pendiente de su aprobación escrita\.", cuerpo)
    return m.group(0) if m else None


def resumen_sin_modelo(cuerpo):
    """(el RESUMEN no nombra el modelo, el ABSTRACT tampoco)."""
    r = re.search(r"^## RESUMEN\s*\n(.*?)^## ", cuerpo, re.M | re.S)
    a = re.search(r"^## ABSTRACT\s*\n(.*?)^(?:## |---)", cuerpo, re.M | re.S)
    return (bool(r) and "modelo" not in r.group(1).lower(),
            bool(a) and "model" not in a.group(1).lower())


def palabras_word(t):
    """Como cuenta Word, igual que `build_structured_abstract.palabras`: todo
    token separado por espacios, sin el marcado de negrita y cursiva."""
    return len(t.replace("**", "").replace("*", "").split())


def paginas_cuerpo_pdf(pdf):
    """Páginas del PDF maquetado antes de las referencias, o None si no se puede.

    Si la página de las referencias lleva texto del cuerpo antes del título,
    cuenta como cuerpo; si el título la abre, no. La cabecera de la revista y
    el número de página no son texto del cuerpo.
    """
    try:
        import pymupdf
    except ImportError:
        try:
            import fitz as pymupdf
        except ImportError:
            return None
    with pymupdf.open(str(pdf)) as doc:
        for i, pagina in enumerate(doc, start=1):
            lineas = [l.strip() for l in pagina.get_text().split("\n") if l.strip()]
            if "REFERENCIAS" not in lineas:
                continue
            antes = [l for l in lineas[:lineas.index("REFERENCIAS")]
                     if not re.fullmatch(r"\d+", l)
                     and not l.startswith("JOURNAL OF SCIENCE AND RESEARCH")]
            return i if antes else i - 1
    return None


def medidas_formato():
    """Lo que el LEEME y la hoja de cesión dicen del formato, medido y no tecleado.

    El LEEME decía «resumen de 250 palabras» y «el cuerpo en 23 páginas contra
    un límite de 25», tecleados el 14 de septiembre. Desde entonces el
    manuscrito creció, y el PDF maquetado del 8 de octubre ya ponía las
    referencias en la página 28: el «23» no se sostenía y el «las cumple
    todas» tampoco. Las páginas solo se dan si el PDF es posterior al
    manuscrito; si no, se dice que están sin medir y cuánto daba el anterior.
    """
    cuerpo = JSR_MD.read_text(encoding="utf-8")
    m = {}
    titulo = next((l[2:] for l in cuerpo.split("\n") if l.startswith("# ")), "")
    m["titulo"] = palabras_word(titulo)
    r = re.search(r"^## RESUMEN\s*\n(.*?)^\*\*Palabras clave", cuerpo, re.M | re.S)
    m["resumen"] = palabras_word(r.group(1)) if r else None
    k = re.search(r"^\*\*Palabras clave:\*\*\s*(.+)$", cuerpo, re.M)
    claves = [c.strip() for c in k.group(1).rstrip(".").split(";") if c.strip()] if k else []
    m["claves"] = len(claves)
    # El orden alfabetico se decia cumplido sin mirarlo. Se ordena sin tildes,
    # sin mayusculas y sin la cursiva del binomio, como en un diccionario.
    def llave(c):
        c = unicodedata.normalize("NFD", c.replace("*", "").lower())
        return "".join(ch for ch in c if unicodedata.category(ch) != "Mn")
    m["claves_en_orden"] = bool(claves) and claves == sorted(claves, key=llave)
    refs = cuerpo.split("\n## REFERENCIAS", 1)
    m["referencias"] = (len(re.findall(r"^\d+\. ", refs[1], re.M))
                        if len(refs) == 2 else 0)
    m["paginas"], m["paginas_previas"], m["por_que"] = None, None, ""
    if not JSR_PDF.exists():
        m["por_que"] = "no hay PDF maquetado"
    else:
        n = paginas_cuerpo_pdf(JSR_PDF)
        if JSR_PDF.stat().st_mtime < JSR_MD.stat().st_mtime:
            m["paginas_previas"] = n
            m["por_que"] = "el PDF maquetado es anterior a esta versión del manuscrito"
        elif n is None:
            m["por_que"] = "no se pudo leer el PDF maquetado"
        else:
            m["paginas"] = n
    return m


def normas_formato(aplicadas=NORMAS_APLICADAS, despues="este guion"):
    """(cumple, falla, sin_medir): el manuscrito contra las normas de la revista.

    `cumple` y `falla` son listas de frases; `sin_medir` es None si la
    extensión está medida sobre esta versión y, si no, la frase que lo dice.
    Lo de `aplicadas` no se mide; lo demás sale de `medidas_formato`. «Las
    cumple todas» solo puede escribirse con `falla` vacía y `sin_medir` None:
    la hoja de cesión lo decía con el título, el resumen y las palabras clave
    tecleados y sin haber medido la extensión, que el 8 de octubre pasaba del
    límite.
    """
    fm = medidas_formato()
    cumple, falla = list(aplicadas), []
    (cumple if fm["titulo"] <= TOPE_TITULO else falla).append(
        "título de %d palabras, con un máximo de %d" % (fm["titulo"], TOPE_TITULO))
    if fm["resumen"] is None:
        falla.append("el RESUMEN no se encuentra en el manuscrito para contarlo")
    else:
        (cumple if fm["resumen"] <= TOPE_RESUMEN else falla).append(
            "resumen de %d palabras, contadas como Word, con un máximo de %d"
            % (fm["resumen"], TOPE_RESUMEN))
    lo, hi = TOPE_CLAVES
    (cumple if lo <= fm["claves"] <= hi else falla).append(
        "%d palabras clave, entre %d y %d" % (fm["claves"], lo, hi))
    if fm["claves_en_orden"]:
        cumple.append("palabras clave en orden alfabético")
    else:
        falla.append("palabras clave fuera de orden alfabético")
    sin_medir = None
    if fm["paginas"] is not None:
        (cumple if fm["paginas"] <= TOPE_PAGINAS else falla).append(
            "el cuerpo en %d páginas del PDF maquetado antes de las referencias, "
            "con un límite de %d" % (fm["paginas"], TOPE_PAGINAS))
    else:
        sin_medir = ("La extensión no está medida sobre esta versión (%s%s). El "
                     "límite es de %d páginas A4 a 1,5, que en los artículos de "
                     "revisión no cuentan las referencias: se mide corriendo "
                     "`scripts/build_jsr_pdf.py` y después %s."
                     % (fm["por_que"],
                        "; el PDF anterior ya daba %d páginas antes de las "
                        "referencias" % fm["paginas_previas"]
                        if fm["paginas_previas"] else "",
                        TOPE_PAGINAS, despues))
    return cumple, falla, sin_medir


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
        # DECIA \u00abSe interrogaron 8 bases de datos y registros con 9 consultas\u00bb, y
        # ProQuest tambien se interrogo: devolvio registros que no se exportaron
        # (el manuscrito de la revista lo dice en Metodos). Las 8 son las que
        # aportaron el corpus (2026-10-14).
        "evidencia admite una s\u00edntesis cuantitativa de eficacia. El corpus procede "
        "de %d bases de datos y registros, interrogados con %d consultas \u2014Scopus "
        "en dos brazos\u2014, incluidos BVS y SciELO, que las revisiones previas han "
        "cubierto de forma desigual, con una ventana de publicaci\u00f3n de %d a %d "
        "aplicada en las que la admiten; ProQuest tambi\u00e9n se interrog\u00f3, pero lo "
        "que devolvi\u00f3 no se export\u00f3. De %s registros quedaron %s informes \u00fanicos y %d "
        "estudios, todos con el art\u00edculo completo le\u00eddo. Ese requisito se "
        "a\u00f1adi\u00f3 el 6 de octubre de 2026, con la extracci\u00f3n terminada, y el "
        "manuscrito lo declara como enmienda, con su fecha y su efecto: deja "
        "fuera %d de los %d estudios con dise\u00f1o comparativo."
        # La ventana es el filtro de la busqueda, no el estudio mas antiguo
        # del corpus; y \u00abcon publicacion recuperable\u00bb dejo de distinguir nada
        # el 2026-10-06, cuando el corpus paso a exigir el articulo completo.
        # La carta lo dice porque es lo primero que lee el Comite: presentar
        # el criterio como si hubiera regido desde el principio seria falso.
        % ("*Pseudomonas aeruginosa*", S["fuentes_distintas_n"], S["fuentes_brazos_n"],
           S["ventana_desde"], S["ventana_hasta"],
           mil(S["registros_identificados"]), mil(S["informes_unicos"]),
           S["estudios"], S["criterio_texto_comparativos"],
           S["criterio_texto_comparativos_antes"]), WD_ALIGN_PARAGRAPH.JUSTIFY)

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
    #
    # Tres frases de este parrafo eran falsas y se corrigieron el 2026-10-08:
    # - DECIA que el modelo cribo \u00abaplicando criterios y un vocabulario cerrado
    #   que los autores fijamos de antemano\u00bb. El primer dia el modelo escribio
    #   los motivos en texto libre; los seis codigos salen de esos textos y no
    #   consta que los autores los fijaran antes de empezar.
    # - DECIA que los informes que superaron el cribado \u00ablos reviso uno a uno
    #   el primer autor\u00bb. Es una declaracion de D.V. del 8 de octubre, sin
    #   registro, y va como declaracion, con la redaccion fijada.
    # - DECIA que el recribado en Rayyan no encontro \u00abningun falso negativo\u00bb,
    #   sin decir que en la primera pasada el revisor marco 6 y despues los
    #   reclasifico. Y llamaba \u00abadjudicacion por consenso\u00bb a la de la
    #   extraccion, cuando solo 14 de 539 llevan la firma de los dos.
    # - La primera correccion dejo \u00abaplicando los criterios de la Tabla 1 del
    #   manuscrito\u00bb. Tampoco se sostenia: la Tabla 1 de hoy lleva criterios
    #   que nacieron despues del cribado (NOPDF, NOORG), y el primer dia se
    #   anadieron a mitad de lote dos reglas que concretan los criterios. Va
    #   la redaccion de la hoja de hechos del 2026-10-08.
    # - DECIA \u00abese mismo dia se anadieron a mitad de lote dos reglas\u00bb, en
    #   pasiva: callaba que el modelo las incorporo a sus guiones de cribado.
    # - Y DESPUES DECIA que el modelo las «propuso» y que «decidieron los
    #   autores». Falso: lo tomo de un error de la hoja de hechos del 13-oct,
    #   corregido el 15-oct. Las anadio el modelo a mitad de lote, sin decision
    #   registrada de nadie (commits 54e5fc4 y 4a4ba98; el primer registro de
    #   decision es del 5-ago). Va como la declaracion de IA.
    par("Declaro lo siguiente, por si el Comit\u00e9 lo considera al evaluar el trabajo. "
        "La revisi\u00f3n no est\u00e1 registrada en PROSPERO ni en ning\u00fan otro registro "
        "prospectivo, y as\u00ed se declara en el manuscrito. El cribado de t\u00edtulos y "
        "res\u00famenes lo emiti\u00f3 un modelo de lenguaje (Claude Opus 5, Anthropic) "
        "como revisor \u00fanico y sin duplicaci\u00f3n. El primer d\u00eda de cribado, el 4 "
        "de agosto de 2026, escribi\u00f3 los motivos de exclusi\u00f3n en texto libre, y "
        "ese mismo d\u00eda a\u00f1adi\u00f3 a mitad de lote, en sus guiones de cribado, dos "
        "reglas que concretan los criterios \u2014fuera las endolisinas aisladas y "
        "los informes veterinarios\u2014, sin que conste una decisi\u00f3n de los "
        "autores. "
        "Despu\u00e9s us\u00f3 seis motivos cuya redacci\u00f3n procede de esos textos, y no "
        "consta que los autores los fijaran antes de empezar. Seg\u00fan "
        "declara D.V. (8 de octubre de 2026), examin\u00f3 uno a uno los informes que "
        "superaron el cribado; ese examen no qued\u00f3 registrado. Los registros que "
        "el modelo excluy\u00f3 no los reley\u00f3 ning\u00fan humano, salvo una muestra "
        "aleatoria de %d que recrib\u00f3 a ciegas en Rayyan un solo revisor (D.V.), "
        "en la primera pasada sin los criterios a la vista: marc\u00f3 %d como "
        "incluibles y, al contrastarlos con los criterios, D.V. los reclasific\u00f3 "
        "como excluidos, con lo que quedaron %d falsos negativos de %d (cota "
        "superior del IC 95 %% exacto, %s %%). "
        % (S["validacion_muestra"], S["validacion_primera_pasada_incluidos"],
           S["validacion_falsos_negativos"], S["validacion_muestra"],
           # El escalar ya viene con sus dos decimales y como texto
           # (`build_synthesis_scalars`: "%.2f"); formatearlo otra vez con %f
           # tumbaba la carta.
           str(S["validacion_ic_sup_pct"]).replace(".", ",")) +
        # OJO CON EL ORDEN DE LOS OPERADORES: `%` liga mas fuerte que `+`, asi
        # que cada grupo de literales concatenados necesita SU tupla pegada. Al
        # partir este parrafo en tres con `+`, la tupla que estaba al final se
        # quedo aplicando al ultimo trozo, que ya no tiene huecos, y el guion
        # reventaba con \u00abnot all arguments converted\u00bb.
        # DECIA \u00absobre 122 de los 124 estudios\u00bb, sin decir cuales, en una carta
        # que dos frases antes da 65 estudios: el Comite no podia casar las dos
        # cifras. Los 124 son los extraidos antes de NOPDF.
        # Y DESPUES DECIA \u00ab(entre ellos, los 65 del corpus final)\u00bb, que es cierto
        # pero que el manuscrito de la revista no dice, en una carta que remata
        # \u00abTodo ello consta en Metodos\u00bb. Se quita (2026-10-13); el dato queda en
        # el LEEME como dato del sobre.
        "La extracci\u00f3n de datos se hizo por duplicado, sin independencia "
        "acreditada, sobre %d de los %d estudios extra\u00eddos, y la "
        "adjudicaci\u00f3n de los desacuerdos "
        % (S["extraccion_estudios_ambos"], S["extraccion_estudios_r1"])
        # Dos redacciones, segun queden desacuerdos abiertos o no. Decir \u00abno ha
        # concluido\u00bb y anadir \u00ab0 de 541 siguen sin firmar\u00bb era un sinsentido.
        # DECIA \u00abPOR ESO NINGUNA CIFRA DEL ARTICULO PROCEDE DE ESOS CUADERNOS\u00bb
        # Y ERA FALSO. La completitud de reporte por desenlace --el 67,0 % de
        # brazos sin definicion operativa de exito, y la Tabla 4 entera-- se
        # calcula sobre `extraccion_adjudicada.csv`, que es la fusion de los dos
        # cuadernos. El manuscrito lo dice bien en Metodos: \u00abLa completitud de
        # reporte por desenlace procede de la extraccion adjudicada desde el
        # texto completo\u00bb. La carta, que es el primer documento que lee el
        # Comite, declaraba lo contrario.
        + ("no ha concluido: %d de %d siguen sin firmar, y esas casillas salen "
           "VAC\u00cdAS del conjunto definitivo. No se rellenan con la respuesta "
           "m\u00e1s frecuente ni con la del revisor m\u00e1s completo. "
           % (S["extraccion_conflictos_sin_firmar"], S["extraccion_desacuerdos"])
           if S["extraccion_conflictos_sin_firmar"] else
           # `extraccion_conflictos_firmados` cuenta ADJUDICADOS, no firmados
           # por los dos. Solo los de la firma conjunta constan como consenso;
           # del resto, lo comprobado es que el registro anota un unico
           # responsable, no que no hubiera consenso.
           "qued\u00f3 cerrada el 14 de septiembre de 2026: se adjudicaron %d de %d; "
           "el registro anota la firma de los dos revisores en %d \u2014los \u00fanicos que "
           "constan como consenso\u2014 y un \u00fanico responsable en %d; los %d "
           # Decia \u00absin firma conjunta\u00bb: cierto, pero no son las palabras del
           # manuscrito de la revista, que dice que no se cuentan como consenso.
           "restantes se cerraron por una regla mec\u00e1nica sobre una comparaci\u00f3n "
           "posteriormente rehecha y no se cuentan como consenso. "
           % (S["extraccion_conflictos_firmados"], S["extraccion_desacuerdos"],
              S["conflictos_resueltos_por_los_dos"],
              S["conflictos_resueltos_por_uno"],
              S["extraccion_cerrados_por_regla"])) +
        # DECIA \u00absale del cribado y de la pre-extraccion desde resumenes\u00bb sin
        # decir quien la emitio, y el Comite la habria leido como humana.
        "La caracterizaci\u00f3n estructural del corpus no depende de esos cuadernos "
        "\u2014sale del cribado y de la pre-extracci\u00f3n desde los res\u00famenes, que "
        "tambi\u00e9n emiti\u00f3 el modelo\u2014, pero la completitud de reporte por "
        "desenlace s\u00ed: procede de la extracci\u00f3n adjudicada sobre el texto "
        "completo, y as\u00ed se declara en M\u00e9todos. Todo ello consta en M\u00e9todos y "
        "en Limitaciones. "
        # DECIA \u00abTodo ello consta [...], con la concordancia medida\u00bb, justo
        # despues del cribado por el modelo: se leia como si se hubiera medido
        # tambien la del cribado. Las medidas son las de la extraccion y el
        # riesgo de sesgo; la del cribado sobre lo que el modelo admitio no se
        # midio, y sobre los excluidos lo que hay es el recribado (2026-10-13).
        # Y se dice, como el manuscrito, que esas dos no miden lecturas
        # independientes; y quien coincidio con el modelo es D.V., el unico
        # que recribo (2026-10-14).
        "Las concordancias medidas son las de la extracci\u00f3n y la del riesgo de "
        "sesgo, entre dos lecturas cuya independencia no est\u00e1 acreditada. La "
        "concordancia entre el modelo y un lector humano no se midi\u00f3 sobre lo que "
        "el modelo admiti\u00f3; sobre los %d excluidos recribados, D.V. coincidi\u00f3 con "
        "el modelo en %d en la primera pasada y en los %d tras contrastar los "
        "criterios. "
        % (S["validacion_muestra"],
           S["validacion_muestra"] - S["validacion_primera_pasada_incluidos"],
           S["validacion_muestra"] - S["validacion_falsos_negativos"]) +
        # DECIA \u00abPreferimos\u00bb, en una carta que firma D.V. solo y en primera
        # persona del singular: hablaba por N.T., que no ha aprobado por
        # escrito la version final.
        "Prefiero declararlo antes que omitirlo.",
        WD_ALIGN_PARAGRAPH.JUSTIFY)

    # LA CARTA SOLO DECLARABA EL CRIBADO, y el Comite habria entendido que el
    # resto lo hicieron personas. No se resume la declaracion de uso de IA: se
    # remite a ella y se nombra lo esencial con sus mismas palabras. Que el
    # parrafo exista en el manuscrito de la revista lo garantiza
    # `exige_declaracion_ia`, que corre antes de escribir nada.
    #
    # Tres cosas de este parrafo se corrigieron el 2026-10-13 (hoja de hechos):
    # - DECIA que el modelo \u00abpropuso, con su cita, las exclusiones\u00bb, las 118;
    #   63 NOPDF y 4 NOREC no tienen cita y 4 ORG tampoco. Va la redaccion
    #   fijada: las que se apoyan en los textos que leyo, fichas incluidas.
    # - Callaba que redacto las propuestas de criterios que decidieron los
    #   autores y los registros de decision, que el manuscrito presenta como
    #   salvaguarda.
    # - Y al reponerlo DECIA \u00ablas propuestas de criterios y de reglas que
    #   decidieron los autores\u00bb, sin mas: de las reglas de desenlace eso es una
    #   declaracion de D.V., y el registro del 12-ago las dejo como propuesta
    #   sin ratificar (2026-10-14). Va como lo dice la declaracion.
    # Y el 2026-10-15 (segunda ronda del consejo) otras tres:
    # - DECIA \u00ablas propuestas de criterios que decidieron los autores\u00bb. La
    #   unidad de inclusion la decidio D.V.; PRO e INT, por orden de D.V.; solo
    #   NOORG consta firmado por los dos. Se dice quien decidio cada una.
    # - Callaba que las ecuaciones de busqueda las redacto el modelo (commit
    #   923bbe7); la declaracion de D.V. es solo que las ejecuto.
    # - Callaba quien firmo las exclusiones a texto completo: 27 constaban a
    #   nombre de los dos y solo hay la orden de D.V. Cifras de los escalares.
    # Todo ello lo dice ya la declaracion; `CARTA_EN_REVISTA` lo comprueba.
    par("El modelo de lenguaje intervino en todas las fases de esta revisi\u00f3n, y "
        "el manuscrito lo detalla en su declaraci\u00f3n \u00abUso de inteligencia "
        "artificial\u00bb, en Declaraciones. Adem\u00e1s del cribado, el modelo redact\u00f3 "
        "las ecuaciones de b\u00fasqueda de cada plataforma, que seg\u00fan declara D.V. "
        "ejecut\u00f3 D.V. en cada interfaz con la gu\u00eda del modelo; redact\u00f3 las "
        "propuestas de criterios que se adoptaron \u2014la unidad de inclusi\u00f3n por "
        "estudio y la elegibilidad de los res\u00famenes de congreso, que decidi\u00f3 D.V.; "
        "los c\u00f3digos PRO e INT, por orden de D.V.; y el c\u00f3digo NOORG, que "
        "firmaron los dos autores\u2014 y las reglas de desenlace, que seg\u00fan declara "
        "D.V. decidieron los dos autores, aunque el registro del 12 de agosto de "
        "2026 las dej\u00f3 como propuesta sin ratificar; ley\u00f3 los textos completos y "
        "las fichas de registro y propuso, con su cita, las exclusiones que se "
        "apoyan en ellos. %s El modelo escribi\u00f3 y ejecut\u00f3 todo el "
        "c\u00f3digo del canal, del que sale cada cifra, tabla y figura, y redact\u00f3 los "
        "borradores del manuscrito, de los anexos, de esta carta y de los "
        "registros de decisi\u00f3n." % con_punto(firmas_exclusiones(S)),
        WD_ALIGN_PARAGRAPH.JUSTIFY)

    # DECIA \u00abjunto con los 25 anexos del material suplementario\u00bb: el numero de
    # anexos no lo da el manuscrito de la revista. Va como dato del sobre, que
    # es lo que es (2026-10-13).
    par("El manuscrito es original, no ha sido publicado ni est\u00e1 sometido a "
        "consideraci\u00f3n en otra revista. El canal de b\u00fasqueda, cribado y c\u00e1lculo est\u00e1 "
        "escrito en c\u00f3digo versionado y es reejecutable, y queda a disposici\u00f3n de "
        "los revisores. El material suplementario va en este mismo env\u00edo, en %d "
        "anexos." % n_anexos, WD_ALIGN_PARAGRAPH.JUSTIFY)

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


def organismo_pendiente(S):
    """El punto que bloquea el envio mientras el organismo de las fichas siga abierto.

    Las 29 fichas cuyo titulo, resumen y MeSH no decian que organismo se trata
    las descargo y leyo el modelo, que propuso con su frase un veredicto para
    cada una (decia «se leyeron», en pasiva; 2026-10-14). Los dos revisores
    firmaron el cuaderno el 2026-09-14 y diez exclusiones se aplicaron. Siete filas quedaron abiertas,
    y son justo las que no se pueden cerrar solas: seis firmadas NO CUMPLE sin
    codigo del vocabulario --un codigo nuevo es una enmienda al protocolo-- y
    una sin decidir.

    El aviso no se teclea ni se cuenta a ojo: sale de
    `quality_reports/organismo_pendiente.json`, que escribe `ingest_organismo.py`
    con lo que NO pudo aplicar. Cuando ese fichero quede vacio, el aviso
    desaparece solo.
    """
    p = ROOT / "quality_reports" / "organismo_pendiente.json"
    if not p.exists():
        return ()
    d = json.loads(p.read_text(encoding="utf-8"))
    sin_codigo = [x["study_id"] for x in d.get("firmadas_sin_codigo", [])]
    sin_decidir = list(d.get("sin_decidir", []))
    if not (sin_codigo or sin_decidir):
        return ()
    trozos = []
    if sin_codigo:
        trozos.append("%d estan firmadas NO CUMPLE pero sin codigo de exclusion "
                      "(%s): el vocabulario es cerrado y un codigo nuevo es una "
                      "enmienda al protocolo, que se declara en "
                      "`scripts/exclusion_codes.py` y se firma"
                      % (len(sin_codigo), ", ".join(sorted(sin_codigo))))
    if sin_decidir:
        trozos.append("%d sigue(n) sin decidir (%s)"
                      % (len(sin_decidir), ", ".join(sorted(sin_decidir))))
    return ("**Cerrado el organismo de las fichas de registro.** %s. Hasta que "
            "se cierren, el corpus de %s estudios puede moverse todavia, y con "
            "el el diagrama PRISMA y los porcentajes. Ver "
            "`quality_reports/organismo_pendiente.json`"
            % ("; ".join(trozos), mil(S["estudios"])),)


def escribe_leeme(destino, S, anexos, pdf_fuera=""):
    """La hoja de instrucciones del envio, con las cifras del canal.

    Se genera y no se escribe a mano por lo de siempre: la version manual del
    23 de agosto seguia diciendo 724 desacuerdos y dando por retirada a la
    segunda revisora tres dias despues de que volviera.

    `pdf_fuera` es el motivo por el que el PDF para leer no viaja (vacio si
    viaja): la tabla de la carpeta lo dice en vez de callarlo.
    """
    # El manuscrito de la revista, leido una vez: de el salen los marcadores,
    # el numero de tablas y de figuras, y lo que hay que decir del deposito.
    cuerpo = JSR_MD.read_text(encoding="utf-8") if JSR_MD.exists() else ""
    huecos = marcadores(cuerpo)
    trelles = next((x for _, ms in huecos for x in ms
                    if x.startswith("‹‹") and "TRELLES" in x.upper()), None)
    disponibilidad = next((l for l in cuerpo.split("\n")
                           if l.startswith("**Disponibilidad")), "")
    hueco_deposito = "[DATO FALTANTE" in disponibilidad
    a_peticion = "se facilita a petición" in disponibilidad
    # Lo que se mide del formato, una vez: lo usan la seccion de las normas, lo
    # que deciden los autores y la lista de lo que bloquea el envio.
    fm = medidas_formato()
    cumple, falla, sin_medir = normas_formato()
    # Lo que el 2026-10-13 el LEEME no decia y tenia que decir: que el
    # protocolo de la fase definitiva dice que este informe no se enviara, que
    # el resumen no nombra el modelo, si el manuscrito hace responder por el
    # trabajo a quien no lo ha aceptado, y si la carta afirma algo que el
    # manuscrito de la revista no recoge. Todo se lee de los ficheros.
    piloto = frase_piloto()
    n_piloto = len(re.findall(r"\bpiloto\b", cuerpo, re.I))
    resp_ajena = responsabilidad_ajena(cuerpo)
    resp_pendiente = responsabilidad_pendiente(cuerpo)
    resumen_calla, abstract_calla = resumen_sin_modelo(cuerpo)
    sin_respaldo = carta_sin_respaldo(cuerpo)

    pendientes = [
        "**ORCID de los dos autores.** La revista los pone en la nota al pie de "
        "cada autor, junto a las credenciales. En el artículo modelo se ve el "
        "formato: grado académico, filiación, ciudad, país, correo y ORCID.",
        "**La nota al pie de credenciales de cada autor**, con el mismo patrón "
        "del modelo.",
        # Decia «nadie puede firmar por ella» --sin pronombres de genero para
        # los autores-- y que esto «no deja rastro en el documento». Desde el
        # 2026-10-08 el CRediT de N.T. lleva un marcador que depende del mismo
        # escrito, y el LEEME lo tiene que nombrar.
        "**La autoría de N. Trelles conforme a ICMJE.** Cubre el criterio de "
        "contribución sustancial: extrajo %d de los %d estudios, el %s %% de lo "
        "extraído, y sigue en el proyecto. Faltan los otros tres criterios, que "
        "son actos de N. Trelles y nadie puede firmarlos en su lugar: aprobar la "
        "versión final, revisarla críticamente y aceptar responder por el "
        "trabajo. Recabadlo por escrito. "
        % (S["extraccion_estudios_ambos"], S["extraccion_estudios_r1"],
           S["extraccion_doble_pct"]) +
        ("Del mismo escrito depende el marcador que lleva el CRediT de "
         "N. Trelles, `%s`: lo que nombra se añade solo si consta por escrito, y "
         "si no consta el marcador se borra sin añadirlo." % trelles
         if trelles else
         "" if resp_pendiente else
         "Esto no deja rastro en el documento: no hay marcador que quitar, y el "
         "artículo se puede enviar sin que nada avise de que falta.") +
        # Y de el depende tambien la frase de responsabilidad de la declaracion
        # de uso de IA (2026-10-13): se cita del manuscrito, no se teclea.
        ("%s la frase de la declaración de uso de IA «%s»: cuando conste el "
         "escrito, se cambia en el maestro y se copia igual a la revista."
         % (" Y también" if trelles else "Del mismo escrito depende",
            resp_pendiente.rstrip("."))
         if resp_pendiente else ""),
        # Decia «Tampoco hay marcador», y la declaracion de disponibilidad del
        # manuscrito de la revista lleva un [DATO FALTANTE] sobre el deposito.
        ("**El depósito de datos y código.** La declaración de disponibilidad "
         "lleva un `[DATO FALTANTE]` con la decisión sobre el depósito público "
         "con DOI. Si depositáis, se reescribe la frase con el DOI; si no, se "
         "borra el marcador%s."
         % (", porque la frase ya dice que el código se facilita a petición"
            if a_peticion else "")
         if hueco_deposito else
         "**El DOI del depósito**, solo si decidís depositar los datos y el "
         "código. No hay marcador%s. Si depositáis, hay que reescribir la "
         "declaración de disponibilidad, no rellenar un hueco."
         % (": la declaración de disponibilidad dice hoy que el código se "
            "facilita a petición, que es cierto tal como está"
            if a_peticion else "")),
        "**Fechas de recepción y aceptación.** Van en blanco a propósito: las "
        "pone la revista.",
        # Decia «exportar a PDF si lo piden, que aqui no hay conversor». Las
        # dos mitades eran falsas: la revista NO acepta PDF como fichero de
        # envio, y ya hay un PDF maquetado para leer.
        "**El PDF no se envía.** La lista de comprobación de la revista dice "
        "que el fichero de envío va en «OpenOffice, Microsoft Word, RTF o "
        "WordPerfect»: lo que se sube es el `.docx`. Hay un PDF maquetado en "
        "`paper/pdf/manuscrito_JSR_final.pdf`, pero es para leer e imprimir. "
        "No está convertido del `.docx` —en esta máquina no hay conversor— "
        "sino maquetado aparte, así que sus saltos de página pueden no "
        "coincidir con los de Word.",
    ]

    md = []
    md.append("# Env\u00edo a *Journal of Science and Research* \u2014 qu\u00e9 hay aqu\u00ed y qu\u00e9 falta")
    # LO PRIMERO, ANTES QUE LA CARPETA: si este sobre se envia o no. El
    # protocolo de la fase definitiva dice que el informe piloto no se enviara,
    # y el sobre estaba listo para enviarlo sin que nada lo dijera (consejo del
    # 2026-10-13). La frase se cita del protocolo; si cambia, este aviso cambia.
    if piloto:
        md.append("")
        # DECIA \u00abNO SE ENV\u00cdA\u00bb: el protocolo dice \u00abno se enviar\u00e1 como tal\u00bb, que
        # deja abierto enviarlo como piloto. El titular no dice mas que la frase.
        md.append("> ## ANTES DE NADA: EL PROTOCOLO DICE QUE ESTE INFORME NO SE "
                  "ENVIAR\u00c1 COMO TAL")
        md.append(">")
        md.append("> El protocolo de la fase definitiva (borrador para OSF, "
                  "`revision_sistematica/protocolo/%s`) dice: \u00ab%s\u00bb Este sobre es ese "
                  "informe, preparado para enviarse. **Enviarlo exige que los autores "
                  "decidan antes una de dos cosas: o no se env\u00eda, o se cambia esa frase "
                  "del protocolo antes de depositarlo y el manuscrito se presenta como "
                  "piloto.** Hoy la palabra \u00abpiloto\u00bb aparece %d %s en el manuscrito de "
                  "la revista, y la carta lo presenta como \u00abart\u00edculo original de "
                  "revisi\u00f3n sistem\u00e1tica\u00bb: si se env\u00eda como piloto, cambian los dos."
                  % (PROTOCOLO.name, piloto, n_piloto,
                     "vez" if n_piloto == 1 else "veces"))
        md.append(">")
        md.append("> En ning\u00fan caso se pone en este manuscrito el n\u00famero de registro "
                  "de OSF: el protocolo es el de la fase definitiva y no cubre este "
                  "informe.")
    elif not n_piloto:
        md.append("")
        md.append("> **El protocolo de la fase definitiva ya no dice que el informe "
                  "piloto no se enviar\u00e1, pero el manuscrito de la revista no se "
                  "presenta como piloto** (la palabra no aparece). Comprobad que es "
                  "lo que hab\u00e9is decidido antes de enviarlo.")
    # Si Word tenia el .docx abierto, el constructor escribio el bueno al lado
    # con el sufijo _NUEVO y el viejo sigue en la carpeta con el contenido de
    # la ejecucion anterior. El aviso va aqui, en la hoja que se lee antes de
    # enviar, porque el de la consola se lo lleva el primer scroll.
    nuevo = destino / "manuscrito_JSR_final_NUEVO.docx"
    if nuevo.exists():
        md.append("")
        md.append("> ## PARA. HAY DOS MANUSCRITOS EN ESTA CARPETA")
        md.append(">")
        md.append("> Word ten\u00eda `manuscrito_JSR_final.docx` abierto cuando se gener\u00f3 "
                  "este env\u00edo, as\u00ed que no se pudo sobrescribir. **El bueno es "
                  "`manuscrito_JSR_final_NUEVO.docx`**; el otro es de una ejecuci\u00f3n "
                  "anterior y su contenido est\u00e1 desfasado.")
        md.append(">")
        md.append("> Cierra Word y vuelve a ejecutar `python scripts/build_jsr_submission.py`: "
                  "el bueno pasa a llamarse `manuscrito_JSR_final.docx`, el `_NUEVO` "
                  "desaparece y este aviso con \u00e9l. **No mandes nada mientras este "
                  "p\u00e1rrafo siga aqu\u00ed.**")
    md.append("")
    md.append("**Revista destino:** Journal of Science and Research, E-ISSN 2528-8083  ")
    md.append("(Universidad T\u00e9cnica de Babahoyo, Ecuador)  ")
    md.append("**Formato tomado de:** el art\u00edculo de Torres Vinueza y Prieto Fuenmayor, "
              "Vol. 9 N.\u00ba 2, abril\u2013junio 2024.  ")
    md.append("**Generado:** %s por `scripts/build_jsr_submission.py`. No lo edites a "
              "mano: se reescribe entero en cada ejecución."
              % datetime.date.today().isoformat())
    md.append("")
    md.append("## Por qué este envío existe")
    md.append("")
    # DECIA «el exceso son justamente las declaraciones de honestidad» --nadie
    # lo midio: el exceso son miles de palabras-- y «En JSR el problema
    # desaparece: el articulo que sirvio de modelo ocupa 19 paginas», con el 19
    # tecleado y mientras el de la revista pasaba de su limite de paginas. Y
    # que el de CMI «sigue vivo», cuando el protocolo de la fase definitiva dice
    # que el informe piloto no se enviara como tal (2026-10-13).
    md.append("Es una desviación deliberada. El manuscrito estaba preparado para "
              "*Clinical Microbiology and Infection*, y ahí no cabe: **%s palabras de "
              "texto principal contra un límite de 3 500**. JSR no limita palabras "
              "sino páginas: %d de cuerpo en los artículos de revisión, sin contar "
              "las referencias, y %s. El manuscrito de CMI sigue en el repositorio, "
              "sin someter; esto no lo sustituye."
              % (mil(S["palabras_cuerpo_es"]), TOPE_PAGINAS,
                 "hoy el de la revista tampoco cabe: %d páginas de cuerpo en el PDF "
                 "maquetado" % fm["paginas"]
                 if fm["paginas"] is not None and fm["paginas"] > TOPE_PAGINAS else
                 "el de la revista cabe: %d páginas de cuerpo en el PDF maquetado"
                 % fm["paginas"] if fm["paginas"] is not None else
                 # Sin medir, se da la ultima medida en vez de callarla.
                 "la extensión del de la revista no está medida sobre esta versión: "
                 "el PDF maquetado anterior daba %d páginas de cuerpo (ver abajo)"
                 % fm["paginas_previas"] if fm["paginas_previas"] else
                 "la extensión del de la revista no está medida sobre esta versión "
                 "(ver abajo)"))

    # LO QUE DECIDEN LOS AUTORES, y nadie puede decidir por ellos. Hasta el
    # 2026-10-13 el LEEME no lo separaba: el destino del piloto no estaba, el
    # resumen sin el modelo lo dejaba un registro de decisiones «para los
    # autores» sin que el sobre lo dijera, y la extension solo constaba en la
    # frase de las normas, no entre lo que bloquea.
    decide = []
    if piloto:
        decide.append("**Si este informe se envía.** Ver el aviso de arriba: el "
                      "protocolo de la fase definitiva dice que no se enviará como tal.")
    if resumen_calla:
        decide.append(
            "**El resumen no dice que el cribado lo emitió un modelo de lenguaje.** "
            "El RESUMEN del manuscrito de la revista no nombra el modelo%s, y es lo "
            "primero que lee el lector de la revista, aunque las decisiones del "
            "cribado de títulos y resúmenes, que delimitan el corpus, las emitió el "
            "modelo como revisor único. La frase estaba en el resumen del maestro y se "
            "retiró el 23 de agosto de 2026 en el commit `32f3f12`; el registro de "
            "decisiones del 8 de octubre de 2026 dice que se retiró por decisión del "
            "autor (el mensaje del commit enumera otras retiradas «por decisión del "
            "autor» y no nombra esta). Si se repone, va en el RESUMEN y en el "
            "ABSTRACT, y el resumen no puede pasar de %d palabras: hoy tiene %s."
            % (" (el ABSTRACT tampoco)" if abstract_calla else "",
               TOPE_RESUMEN,
               fm["resumen"] if fm["resumen"] is not None else "un número que no se "
               "pudo contar"))
    if fm["paginas"] is not None and fm["paginas"] > TOPE_PAGINAS:
        decide.append(
            "**Qué se recorta.** El cuerpo mide **%d páginas** en el PDF maquetado "
            "antes de las referencias, y el límite de la revista es de %d. Qué se "
            "recorta lo deciden los autores; las declaraciones de honestidad no se "
            "recortan." % (fm["paginas"], TOPE_PAGINAS))
    elif fm["paginas"] is None and fm["paginas_previas"]:
        decide.append(
            "**Qué se recorta, si hace falta.** La extensión no está medida sobre esta "
            "versión (%s); el PDF anterior daba **%d páginas** de cuerpo, y el límite "
            "de la revista es de %d. Qué se recorta lo deciden los autores; las "
            "declaraciones de honestidad no se recortan."
            % (fm["por_que"], fm["paginas_previas"], TOPE_PAGINAS))
    # LO QUE N.T. TIENE QUE SABER O RATIFICAR (2026-10-15). El LEEME no lo
    # decia: 27 exclusiones figuraban firmadas por N.T. sin que conste, el
    # mensaje con que se le pidio firmar el 1-sep lo redacto el modelo en
    # primera persona de D.V., y 2 descartes de solapamiento son del modelo
    # sin firma. Lo comparte la hoja de cesion (`pendiente_de_nt`).
    for titulo, texto in pendiente_de_nt(S):
        decide.append("**%s** %s" % (con_punto(titulo), texto))
    if decide:
        md.append("")
        md.append("## Lo que deciden los autores antes de enviar")
        md.append("")
        for i, t in enumerate(decide, start=1):
            md.append("%d. %s" % (i, t))
            md.append("")
    # Ni el numero de anexos ni el de tablas se teclean: el primero sale de lo
    # que se acaba de copiar y el segundo del propio manuscrito. Escritos a mano
    # envejecian en silencio --el LEEME anunciaba 14 anexos «S0 a S13» cuando ya
    # eran 17, y una lista de comprobacion mandaba mirar 4 tablas de las 6 que
    # el articulo lleva--.
    numeros = sorted({int(m.group(1)) for m in
                      (re.match(r"^S(\d{1,2})_", n) for n in anexos) if m})
    n_tablas = len(re.findall(r"^\*\*Tabla \d+\.", cuerpo, re.M))
    n_figuras = len(re.findall(r"^\*\*Figura \d+\.", cuerpo, re.M))

    md.append("")
    md.append("## Qué hay en la carpeta")
    md.append("")
    md.append("| Fichero | Qué es |")
    md.append("|---|---|")
    md.append("| `manuscrito_JSR_final.docx` | **EL FICHERO QUE SE SUBE.** Times New "
              "Roman 12, A4, interlineado 1,5. RESUMEN / ABSTRACT / INTRODUCCIÓN / "
              "DESARROLLO / METODOLOGÍA / RESULTADOS / DISCUSIÓN Y CONCLUSIONES / "
              "DECLARACIONES / REFERENCIAS. Citas Vancouver numeradas. Las %d tablas y "
              "las %d figuras van donde el texto las cita, no en un anexo al final |"
              % (n_tablas, n_figuras))
    # El .pdf va al lado del .docx y con el mismo nombre: en el portal la unica
    # diferencia a la vista es la extension. Se declara aqui, en la fila de
    # despues, para que quien mire la tabla no tenga que deducirlo.
    pdf = destino / "manuscrito_JSR_final.pdf"
    if pdf.exists():
        md.append("| `manuscrito_JSR_final.pdf` | **El mismo artículo, para LEER. NO se "
                  "sube.** La revista pide Word, RTF u OpenOffice. Ojo: se llama igual "
                  "que el `.docx` y está a su lado; en el portal la única diferencia a "
                  "la vista es la extensión. Además no está convertido del `.docx` sino "
                  "maquetado aparte, así que sus saltos de página pueden no coincidir |")
    elif pdf_fuera:
        md.append("| `manuscrito_JSR_final.pdf` | **NO VIAJA EN ESTE SOBRE**: %s. Para "
                  "que viaje, se corre `scripts/build_jsr_pdf.py` y después este "
                  "guion. No se sube en ningún caso |" % pdf_fuera)
    md.append("| `carta_de_presentacion.docx` | Carta al Comité Editorial. Declara por "
              "adelantado lo que un revisor va a preguntar |")
    md.append("| `suplementos/` | Los %d anexos (S%d a S%d), el índice y la guía, en %d "
              "ficheros: los de datos van en `.xlsx` y en `.csv`. Empieza por "
              "`00_GUIA_DEL_MATERIAL_SUPLEMENTARIO.pdf`, que dice qué pregunta contesta "
              "cada uno%s |" % (len(numeros), min(numeros), max(numeros), len(anexos),
                               ojo_indice_guia(set(anexos))))
    md.append("| `figuras/`, `tablas/` | Las mismas figuras y tablas del artículo, sueltas "
              "y numeradas COMO EN EL ARTÍCULO, por si las piden aparte |")
    leer = destino / "para_leer"
    if leer.is_dir() and any(leer.iterdir()):
        md.append("| `para_leer/` | **Nada de esto se sube.** El informe extendido "
                  "—la versión larga, con la metodología que el artículo condensa—, "
                  "las cuatro versiones del resumen con cuál se envía marcada, y la "
                  "hoja con lo que va en cada hueco de la carta de cesión de la "
                  "revista. Están en carpeta aparte para que no se suban por error: "
                  "el informe extendido tiene aspecto de manuscrito y no lo es |")
    # Lo escribe `build_criteria_table.py` en esta misma carpeta. El LEEME no lo
    # nombraba, y un fichero en el sobre que la hoja de instrucciones ignora
    # parece un resto de algo.
    suelto = destino / "tabla_criterios_inclusion_exclusion.docx"
    if suelto.exists():
        md.append("| `%s` | La Tabla 1 en un documento aparte, ya maquetada. Va también "
                  "dentro del artículo, donde el texto la cita; esta copia es por si el "
                  "portal pide los cuadros por separado. La escribe "
                  "`scripts/build_criteria_table.py` |" % suelto.name)
    md.append("")
    # LO QUE NO ESTA EN LA CARPETA Y TIENE QUE ESTAR. El LEEME no nombraba los
    # dos formularios de la revista, y sin ellos el envio ni siquiera entra en
    # revision. Se leyeron sus normas el 2026-09-14 --antes solo se decia
    # «confirmalo en el portal»-- y la lista de comprobacion es taxativa.
    # La cita de la revista va tal como se copio aquel dia, sin tocarla.
    md.append("")
    md.append("## Lo que NO está aquí y sin lo cual no arranca la revisión")
    md.append("")
    md.append("La revista provee dos formularios propios y hay que descargarlos de "
              "su sección **Archivos y formatos descargables**, en "
              "<%s>. Su lista de comprobación dice, literalmente: «No se iniciara "
              "el proceso de revision del articulo si antes no se encuentran en la "
              "plataforma (o en el correo de la revista) ademas del articulo, la "
              "carta de cesion de derechos y la informacion del(los) autor(es), en "
              "los formatos adecuados, los mismos que se encuentran en la seccion "
              "Archivos Suplementarios de la revista»." % PORTAL)
    md.append("")
    md.append("| Falta | Qu\u00e9 es |")
    md.append("|---|---|")
    md.append("| **Carta de originalidad y cesi\u00f3n de derechos** | Formulario de la "
              "revista. Ocho puntos y la firma de los dos autores, con nombre, "
              "documento de identidad, correo, ORCID y filiaci\u00f3n. Lo que va en cada "
              "hueco est\u00e1 en `para_leer/datos_carta_cesion.docx`, en este mismo sobre |")
    md.append("| **Formato de informaci\u00f3n de art\u00edculo y autores** | Otro formulario "
              "suyo, m\u00e1s la hoja de c\u00e1lculo de informaci\u00f3n de autores |")
    md.append("")
    md.append("**No sirve una carta propia.** El env\u00edo se devuelve si no llega en el "
              "formato de ellos.")
    md.append("")
    # DECIA \u00abel manuscrito las cumple todas\u00bb, con \u00abresumen de 250 palabras\u00bb y
    # \u00abel cuerpo en 23 paginas\u00bb tecleados el 14 de septiembre. El 23 ya no se
    # sostenia: el PDF maquetado del 8 de octubre pone las referencias en la
    # pagina 28. Ahora todo lo que se mide sale de `medidas_formato`, y \u00ablas
    # cumple todas\u00bb solo se escribe si de verdad se ha medido y se cumple.
    # (`cumple`, `falla` y `sin_medir` se calculan arriba, una vez.)
    if not falla and sin_medir is None:
        texto = ("Sus normas de formato, le\u00eddas el mismo d\u00eda, el manuscrito **las "
                 "cumple todas**: %s." % ", ".join(cumple))
    else:
        texto = ("Sus normas de formato, le\u00eddas el mismo d\u00eda. El manuscrito cumple "
                 "estas: %s." % ", ".join(cumple))
        if falla:
            texto += " **No cumple**: %s." % "; ".join(falla)
    if sin_medir:
        texto += " **%s**" % sin_medir
    texto += (" Las p\u00e1ginas se cuentan en el PDF maquetado, y Word puede paginar "
              "distinto.")
    md.append(texto)
    md.append("")
    md.append("Los anexos de datos viajan por partida doble: el `.xlsx` trae una hoja "
              "\u00abLeeme\u00bb y las columnas en castellano, y el `.csv` es la copia con los "
              "nombres internos que permite reejecutar el canal. Los `.csv` de esta "
              "carpeta van en UTF-8 **con BOM**, para que Excel respete las tildes al "
              "abrirlos con doble clic; si los lees desde c\u00f3digo, \u00e1brelos como "
              "`utf-8-sig`.")
    md.append("")
    md.append("## Lo que TIENES que rellenar antes de mandarlo")
    md.append("")
    # Decia «Estan marcados en el .docx» y de los cuatro solo uno lo estaba,
    # despues de anadirlo: no habia ningun ORCID ni ningun hueco de autoria en
    # el documento. Mandar quitar un marcador que no existe hace creer que lo
    # que no se ve ya esta hecho.
    #
    # Despues DECIA «Solo el primero deja marca en el .docx: un parrafo [...]
    # que empieza por [DATO FALTANTE]», y dejo de ser cierto sin que nada lo
    # dijera: hoy llevan marcadores las notas de autor, que empiezan por su
    # etiqueta y no por el marcador, la declaracion de disponibilidad y el
    # CRediT de N.T. Los parrafos con marcador se leen del manuscrito.
    if huecos:
        md.append("Son datos que el canal no puede inventar. **%s del `.docx` %s "
                  "marcadores a la vista**: %s. Cada marcador se sustituye por el "
                  "dato o se borra, según diga su punto de abajo, y ninguno puede "
                  "llegar a la revista. Lo demás no deja rastro en el documento y se "
                  "vigila desde aquí."
                  % ("%d párrafos" % len(huecos) if len(huecos) > 1 else "Un párrafo",
                     "llevan" if len(huecos) > 1 else "lleva",
                     "; ".join("«%s» (%d)" % (etq, len(ms)) for etq, ms in huecos)))
    else:
        md.append("Son datos que el canal no puede inventar. El `.docx` no lleva "
                  "ningún marcador a la vista: todo lo de abajo se vigila desde aquí.")
    md.append("")
    for i, t in enumerate(pendientes, start=1):
        md.append("%d. %s" % (i, t))
        md.append("")
    md.append("## Lo que NO hay que tocar")
    md.append("")
    # DECIA «Las declaraciones. Viajaron enteras desde el manuscrito
    # autoritativo», y el 2026-10-08 el manuscrito de la revista no llevaba la
    # declaracion de uso de IA. Ahora lo literal se comprueba
    # (`exige_declaracion_ia`, `exige_ia_en_docx`) y lo demas se presenta como
    # lo que es: un recordatorio de lo que declara el manuscrito, no su texto.
    md.append("Las declaraciones de honestidad. La de uso de inteligencia artificial "
              "viaja literal: el párrafo «Uso de inteligencia artificial» del "
              "manuscrito de la revista es el del maestro %s, y este guion se "
              "niega a construir el sobre si no lo es, o si el `.docx` no lo lleva "
              "entero. Las demás que no se pueden quitar son estas, resumidas aquí "
              "para vigilarlas; el texto que vale es el del manuscrito:"
              % ("letra por letra" if IA_SUSTITUIDAS == [] else
                 "con " + sustituciones_txt()))
    md.append("")
    md.append("- la revisión **no está registrada** en PROSPERO ni en ningún registro "
              "prospectivo;")
    # DECIA «con criterios y vocabulario cerrado fijados de antemano por los
    # autores», y el registro lo desmiente: el primer dia los motivos van en
    # texto libre y los seis codigos salen de esos textos.
    md.append("- el cribado de títulos y resúmenes lo emitió **un modelo de lenguaje "
              "(Claude Opus 5) como revisor único y sin duplicación**; el primer día "
              "escribió los motivos en texto libre, después usó seis motivos cuya "
              "redacción procede de esos textos, y no consta que los autores los "
              "fijaran antes de empezar;")
    # Quien firmo las exclusiones no estaba en esta lista, y 27 figuraban
    # firmadas por N.T. sin que conste (2026-10-15). La frase es la de la carta.
    fx = firmas_exclusiones(S)
    md.append("- %s%s;" % (fx[:1].lower(), fx[1:]))
    # DECIA «(122 de 124 estudios)» sin decir que los 124 son los extraidos
    # antes de NOPDF, y «a uno solo en 525»: lo comprobado es que el registro
    # anota un unico responsable, no que lo decidiera uno solo.
    # Y DESPUES DECIA «entre ellos los 65 del corpus final» y, de los 2 de la
    # regla, «sin firma conjunta»: lo primero el manuscrito de la revista no lo
    # dice, y lo segundo lo dice con otras palabras («no se cuentan como
    # consenso»). En una lista cuyo texto «que vale es el del manuscrito», lo
    # que el manuscrito no recoge pasa abajo, como dato del sobre (2026-10-13).
    md.append("- la extracción por duplicado **está completa** (%d de los %d estudios "
              "extraídos) y "
              % (S["extraccion_estudios_ambos"], S["extraccion_estudios_r1"]) +
              ("**la adjudicación no**: %d de los %d desacuerdos siguen sin firmar;"
               % (S["extraccion_conflictos_sin_firmar"], S["extraccion_desacuerdos"])
               if S["extraccion_conflictos_sin_firmar"] else
               "**la adjudicación también**: %d de %d adjudicados; el registro anota "
               "la firma de los dos revisores en %d —los únicos que constan como "
               "consenso— y un único responsable en %d, y %d se cerraron por una "
               "regla mecánica y no se cuentan como consenso; ni la extracción ni el "
               "riesgo de sesgo acreditan independencia;"
               % (S["extraccion_conflictos_firmados"], S["extraccion_desacuerdos"],
                  S["conflictos_resueltos_por_los_dos"],
                  S["conflictos_resueltos_por_uno"],
                  S["extraccion_cerrados_por_regla"])))
    # Esta linea decia «ninguna cifra del articulo procede de los cuadernos de
    # extraccion» y era falsa: la Tabla 4 y el 67,0 % salen de la extraccion
    # adjudicada. Estaba ademas en la lista de «lo que NO hay que tocar», o sea
    # blindada como declaracion de honestidad. Una declaracion de honestidad
    # falsa es lo peor que puede llevar este sobre.
    #
    # Y DECIA «Las 0 casillas sin acuerdo salen vacias» con
    # `extraccion_conflictos_sin_firmar`, que cuenta desacuerdos sin firmar, no
    # casillas abiertas: en S14 y S15 hay 2 abiertas. Ahora las cuenta
    # `casillas_abiertas`, y solo se dice que son las de la regla si lo son.
    abiertas, son_las_de_regla = casillas_abiertas()
    if not abiertas:
        sobre_abiertas = "No queda ninguna casilla abierta."
    # «ese conjunto» remitia a la extraccion adjudicada de la frase de al lado;
    # al pasar esto a «Datos del sobre» se quedo colgando (2026-10-14).
    elif son_las_de_regla:
        sobre_abiertas = ("Las %d casillas abiertas son las de los %d desacuerdos que "
                          "se cerraron por la regla mecánica sin firma conjunta: el "
                          "registro de conflictos los da por cerrados, pero salen "
                          "vacías de la extracción adjudicada, se cuentan como "
                          "abiertas y no se rellenan con una conjetura."
                          % (abiertas, abiertas))
    else:
        sobre_abiertas = ("Las %d casillas abiertas salen vacías de la extracción "
                          "adjudicada, se cuentan como abiertas y no se rellenan con "
                          "una conjetura." % abiertas)
    # Y LAS CASILLAS ABIERTAS IBAN AQUI, en la lista de lo que dice el
    # manuscrito, y el de la revista no las cuenta: solo dice que los 2 de la
    # regla no se cuentan como consenso. Pasan abajo, como dato del sobre.
    md.append("- **las cifras del artículo tienen dos orígenes, y el manuscrito dice "
              "cuál es cuál**: la caracterización estructural del corpus sale del "
              "cribado y de la pre-extracción desde los resúmenes, que emitió el "
              "modelo; la completitud de reporte por desenlace sale de la extracción "
              "adjudicada sobre el texto completo.")
    md.append("")
    md.append("Quitar cualquiera de estas frases para que el art\u00edculo \u00abpase mejor\u00bb "
              "convierte un trabajo honesto en uno que no lo es. Si un revisor objeta "
              "alguna, se le contesta con los datos, que est\u00e1n todos en `suplementos/`.")
    md.append("")
    md.append("**Datos del sobre, no del manuscrito.** Salen del canal y son ciertos, "
              "pero el manuscrito de la revista no los recoge, as\u00ed que no van ni en la "
              "lista de arriba ni en la carta, y nadie debe citarlos como suyos: %s %s"
              % ("los %d estudios del corpus final est\u00e1n todos entre los %d con doble "
                 "extracci\u00f3n." % (S["estudios"], S["extraccion_estudios_ambos"])
                 if S["extraccion_doble_corpus"] == S["estudios"] else
                 "%d de los %d estudios del corpus final tienen doble extracci\u00f3n."
                 % (S["extraccion_doble_corpus"], S["estudios"]),
                 sobre_abiertas))
    md.append("")
    md.append("## C\u00f3mo se regenera")
    md.append("")
    md.append("Desde `clo-author/`:")
    md.append("")
    md.append("```bash")
    md.append("python scripts/build_jsr_submission.py")
    md.append("```")
    md.append("")
    # DECIA «Si tocas el manuscrito autoritativo [...] vuelve a correrlo», como
    # si el .docx saliera del maestro. Sale de `manuscrito_JSR_final.md`, que
    # se edita por su lado.
    md.append("Reescribe el `.docx` desde `paper/manuscrito_JSR_final.md` (lo escribe "
              "`scripts/build_jsr_docx.py`), las figuras, las tablas, los suplementos, "
              "la carta y este fichero. Lo que cambie en el maestro "
              "(`paper/manuscrito_revision_sistematica.md`) no llega solo al de la "
              "revista: si cambias la declaración de uso de IA del maestro, cópiala "
              "igual en el de la revista, o este guion no construye el sobre. Si tocas "
              "el de la revista o cualquier anexo, vuelve a correrlo. No edites el "
              "`.docx` a mano salvo para los datos de autor.")
    md.append("")
    md.append("## Antes de darle a enviar")
    md.append("")
    # Lo que BLOQUEA va primero. Antes la lista abria con los ORCID y cerraba
    # con «confirmalo en el portal»; los dos formularios sin los cuales la
    # revista ni empieza no estaban.
    #
    # Tampoco estaba la aprobacion escrita de N.T.: el LEEME la explicaba mas
    # arriba pero no la pedia antes de enviar, ni el marcador de su CRediT. Y
    # la lista DECIA «Borrado el parrafo [DATO FALTANTE]», cuando el parrafo de
    # las notas de autor no se borra sino que se rellena, y «No hay marcador que
    # quitar» del deposito, cuando la declaracion de disponibilidad lleva uno.
    # Todo lo que depende de un marcador se lee ahora de `huecos`.
    #
    # Y desde el 2026-10-13 abre la lista lo que el consejo encontro sin
    # bloquear: el destino del piloto, lo que la carta afirma y el manuscrito
    # no recoge, una frase de responsabilidad que habla por N.T., la extension
    # (29 paginas contra 25 ese dia, y solo constaba en la frase de las
    # normas) y el resumen sin el modelo, que es decision de los autores.
    antes = []
    if piloto:
        antes.append("**Decidido por los autores si este informe se envía**: el "
                     "protocolo de la fase definitiva dice «%s». O no se envía, o se "
                     "cambia esa frase antes de depositar el protocolo y el manuscrito "
                     "y la carta lo presentan como piloto" % piloto.rstrip("."))
    for que in sin_respaldo:
        antes.append("**La carta dice %s, y el manuscrito de la revista no lo "
                     "recoge.** O lo recoge el manuscrito o lo quita la carta (en "
                     "`escribe_carta` de este guion): la carta remata «Todo ello consta "
                     "en Métodos y en Limitaciones»" % que)
    if resp_ajena:
        antes.append("**Cambiada la frase «%s»**: N. Trelles no ha aceptado responder "
                     "por el trabajo. Mientras no conste por escrito, la redacción es "
                     "«D.V. asume la responsabilidad por la exactitud e integridad del "
                     "trabajo; la de N.T. queda pendiente de su aprobación escrita». Si "
                     "está en la declaración de uso de IA, se cambia en el maestro y se "
                     "copia igual a la revista" % resp_ajena.rstrip("."))
    for f in falla:
        antes.append("**Corregido lo que incumple las normas de la revista**: %s" % f)
    if sin_medir:
        antes.append("**Medida la extensión sobre esta versión del manuscrito**: %s"
                     % sin_medir)
        # Sin medir, «medida la extension» no decia que la ultima medida ya
        # pasaba del limite: se pide tambien el recorte, con la cifra que dio
        # el PDF anterior, leida y no tecleada (2026-10-14).
        if fm["paginas_previas"] and fm["paginas_previas"] > TOPE_PAGINAS:
            antes.append("**Recortado el cuerpo a %d páginas como máximo**: la última "
                         "medida, sobre el PDF maquetado anterior, daba %d páginas "
                         "antes de las referencias. Qué se recorta lo deciden los "
                         "autores (ver «Lo que deciden los autores antes de enviar»)"
                         % (TOPE_PAGINAS, fm["paginas_previas"]))
    if resumen_calla:
        antes.append("Decidido por los autores si el resumen dice que el cribado lo "
                     "emitió un modelo de lenguaje (ver «Lo que deciden los autores»)")
    antes += list(organismo_pendiente(S))
    # Antes de esa aprobacion, lo que N.T. tiene que saber o ratificar
    # (2026-10-15; el detalle, en «Lo que deciden los autores antes de enviar»).
    for titulo, _ in pendiente_de_nt(S):
        antes.append("Resuelto antes de la aprobación de N. Trelles: «%s» (ver «Lo "
                     "que deciden los autores antes de enviar»)" % titulo)
    antes.append("**Aprobada por escrito por N. Trelles esta versión final** (ICMJE: "
                 "revisión crítica, aprobación y aceptación de responder por el "
                 "trabajo), y guardado ese escrito. Sin ese escrito, D. Valdiviezo no "
                 "puede firmar de buena fe la carta de cesión")
    if trelles:
        antes.append("Resuelto el marcador `%s` del CRediT de N. Trelles: lo que nombra "
                     "se añade solo si consta por escrito; si no consta, se borra sin "
                     "añadirlo" % trelles)
    if resp_pendiente:
        antes.append("Revisada la frase «%s» de la declaración de uso de IA: si consta "
                     "el escrito de N. Trelles, se cambia en el maestro y se copia igual "
                     "a la revista; si no consta, se queda como está"
                     % resp_pendiente.rstrip("."))
    antes += [
        "**Descargada, rellenada y FIRMADA la carta de cesión de derechos de la "
        "revista**, con los dos autores y después de la aprobación escrita de "
        "N. Trelles. Sin ella no arranca la revisión",
        "**Descargado y rellenado el formato de información de artículo y "
        "autores**. Tampoco arranca sin él",
        "Subido el `.docx`, NO el PDF: la revista no acepta PDF como fichero de "
        "envío",
        "ORCID y credenciales de los dos autores",
    ]
    notas = next((ms for etq, ms in huecos if etq.lower().startswith("notas de autor")),
                 None)
    if notas:
        antes.append("Sustituidos por el dato los %d marcadores de «Notas de autor» "
                     "(grados, correo y ORCID)" % len(notas))
    antes.append(
        "Decidido si se depositan datos y código, y resuelto el `[DATO FALTANTE]` "
        "de la declaración de disponibilidad: reescrita con el DOI si se deposita, "
        "y el marcador borrado si no"
        if hueco_deposito else
        "Decidido si se depositan datos y código. No hay marcador que quitar%s"
        % (": la declaración dice hoy que el código se facilita a petición, y eso "
           "es cierto tal como está" if a_peticion else ""))
    if huecos:
        antes.append("Ningún marcador `[DATO FALTANTE]` ni `‹‹…››` queda en el "
                     "`.docx` (hoy lleva %d)" % sum(len(ms) for _, ms in huecos))
    antes += [
        "Leído entero una vez en Word, buscando saltos de formato",
        "Comprobado que las %d tablas y las %d figuras se ven bien"
        % (n_tablas, n_figuras),
    ]
    for t in antes:
        md.append("- [ ] %s" % t)
    md.append("")

    ruta = destino / "LEEME_ANTES_DE_ENVIAR.md"
    ruta.write_text("\n".join(md), encoding="utf-8")
    return ruta

def main():
    # LA GUARDA, ANTES DE ESCRIBIR NADA. `exige_declaracion_ia` y
    # `exige_ia_en_docx` estaban escritas y no las llamaba nadie: el sobre se
    # habria construido igual con el parrafo de uso de IA cambiado o ausente.
    # Si no viaja literal, se para aqui, sin tocar la carpeta de envio.
    ia = exige_declaracion_ia()
    print("  %-42s literal desde el maestro (%s)"
          % ("uso de IA en %s" % JSR_MD.name, sustituciones_txt()))

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
            # abierto es distinto y mas pequeno, y son actos que solo N. Trelles
            # puede realizar. Las cifras salen de los escalares.
            # (Estas notas solo las usa `escribe_docx`, que ya no se llama: el
            # .docx lo escribe `build_jsr_docx.py` desde el manuscrito.)
            "‹‹RESOLVER ANTES DE ENVIAR: la autoría de N. Trelles conforme a "
            "ICMJE. Cubre el criterio de contribución sustancial —extrajo %d de "
            "los %d estudios, el %s %% de lo extraído— y sigue "
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
        ("Figura 2. Composición del cuerpo de evidencia.",
         ROOT / "paper" / "figuras" / "figura_2_composicion.png",
         "Nota. Sobre los estudios del corpus, todos con el artículo completo."),
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
    # El .docx lo escribe `build_jsr_docx` en SU carpeta, que no tiene por que
    # ser `destino`; y si Word tenia abierto el bueno, el recien escrito es el
    # _NUEVO. Se comprueba el que acaba de salir.
    hecho = build_jsr_docx.DEST / "manuscrito_JSR_final_NUEVO.docx"
    if not hecho.exists():
        hecho = build_jsr_docx.DEST / "manuscrito_JSR_final.docx"
    exige_ia_en_docx(hecho, ia)
    print("  %-42s lleva entero el párrafo de uso de IA" % hecho.name)

    # EL PDF VIAJA EN EL SOBRE, por decision de D.V. el 2026-09-14. Va con el
    # mismo nombre que el .docx y a su lado, asi que la unica diferencia a la
    # vista en el portal es la extension: el LEEME lo declara como «para leer,
    # NO se sube» y la lista de comprobacion lo repite. La revista pide Word,
    # RTF u OpenOffice.
    #
    # Y SOLO VIAJA SI ESTA AL DIA. Se copiaba siempre que existiera, y el del
    # 2026-10-08 era anterior al manuscrito y no llevaba la declaracion de uso
    # de IA que si lleva el .docx: el sobre habria llevado dos versiones del
    # articulo, una sin la declaracion. Si no esta al dia se retira la copia
    # vieja del sobre y el LEEME dice por que falta.
    pdf_origen = JSR_PDF
    pdf_dst = destino / pdf_origen.name
    viaja, pdf_fuera = pdf_al_dia(pdf_origen, ia)
    if viaja:
        shutil.copy2(pdf_origen, pdf_dst)
        print("  %-42s para leer; NO es el fichero de envio" % pdf_origen.name)
    else:
        if pdf_dst.exists():
            pdf_dst.unlink()
        print("  AVISO: %s NO viaja: %s.\n         Correr scripts/build_jsr_pdf.py "
              "y despues este guion." % (pdf_origen.name, pdf_fuera))

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

    # Figuras, tal como salen del canal
    dst = destino / "figuras"
    dst.mkdir(exist_ok=True)
    puestos = set()
    for pat in ("*.png", "*.pdf"):
        for f in (ROOT / "paper" / "figuras").glob(pat):
            shutil.copy2(f, dst / f.name)
            puestos.add(f.name)
    print("  %-42s %d ficheros" % ("figuras/", len(puestos)))
    poda(dst, puestos, "figuras/")

    # LAS TABLAS SUELTAS, CON EL NUMERO QUE TIENEN EN EL ARTICULO. Antes se
    # copiaba `paper/tablas/*.csv` entero, ocho ficheros con el nombre que
    # tienen en el repositorio, y ese nombre NO es el numero del articulo:
    # `tabla_4_exclusiones.csv` no es la Tabla 4 --la Tabla 4 son los
    # desenlaces-- y `tabla_3_sesgo_recuperacion.csv` no es la Tabla 3. Dos de
    # los ocho ni siquiera estan en este manuscrito: pertenecen al informe
    # extendido. Un editor que pida «las tablas aparte» abria ficheros que
    # contradicen al articulo.
    #
    # La correspondencia no se teclea: sale de `ADJUNTOS`, el mismo diccionario
    # con el que `build_jsr_docx.py` las mete en el .docx, mas la Tabla 1, que
    # va incrustada en el texto y la escribe `build_criteria_table.py`.
    import build_jsr_docx as _jsr
    dst = destino / "tablas"
    dst.mkdir(exist_ok=True)
    fuente = dict(_jsr.ADJUNTOS)
    fuente["Tabla 1."] = ROOT / "paper" / "tablas" / "tabla_criterios_inclusion_exclusion.csv"
    puestos = set()
    for etiqueta, origen in sorted(fuente.items()):
        if not etiqueta.startswith("Tabla") or not origen.exists():
            continue
        n = etiqueta.split()[1].rstrip(".")
        # el nombre del fichero conserva de que trata, tomado del nombre del canal
        asunto = re.sub(r"^tabla_(\d+_)?", "", origen.stem)
        nombre = "Tabla_%s_%s.csv" % (n, asunto)
        shutil.copy2(origen, dst / nombre)
        puestos.add(nombre)
    print("  %-42s %d ficheros, numeradas como en el articulo"
          % ("tablas/", len(puestos)))
    poda(dst, puestos, "tablas/")

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
        leeme = escribe_leeme(destino, S, copiados, "" if viaja else pdf_fuera)
        print("  %-42s instrucciones del envio" % leeme.name)

    carta = escribe_carta(destino, S, meta, n_anexos)
    print("  %-42s carta al comite" % carta.name)
    # Lo que bloquea y el LEEME ya dice, tambien aqui: el de la consola es el
    # aviso que ve quien corre el canal.
    for que in carta_sin_respaldo(JSR_MD.read_text(encoding="utf-8")):
        print("  AVISO: la carta dice %s, y el manuscrito de la revista no lo "
              "recoge" % que)
    if frase_piloto():
        print("  AVISO: el protocolo de la fase definitiva dice que el informe "
              "piloto no se enviara como tal; el LEEME lo pone en cabeza")

    # El marcador de autor viaja dentro del .docx a proposito: sin el, un ORCID
    # que falta no se distingue de un ORCID que nadie pidio. El aviso suena en
    # cada ejecucion hasta que se rellena, para que nadie lo descubra en el
    # portal de la revista.
    jsr = ROOT / "paper" / "manuscrito_JSR_final.md"
    if jsr.exists() and "[DATO FALTANTE]" in jsr.read_text(encoding="utf-8"):
        print("\n  AVISO: el manuscrito sigue llevando el parrafo de [DATO "
              "FALTANTE].\n         Faltan los dos grados academicos, los dos "
              "ORCID y el correo de N. Trelles.\n         Se rellena en "
              "paper/manuscrito_JSR_final.md y se vuelve a correr esto.")

    print("\nescrito en %s" % destino)
    return 0


if __name__ == "__main__":
    sys.exit(main())
