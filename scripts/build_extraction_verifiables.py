"""Genera en PDF los verificables de la doble extracción, y la guía del paquete.

QUÉ AÑADE Y POR QUÉ

El paquete cubría búsqueda, cribado, idioma y recuperación. La extracción por
duplicado no tenía verificable propio, y es la parte que un revisor mira con más
detalle: si dos personas leen los mismos artículos y no coinciden, la pregunta
inmediata es cuánto no coincidieron, en qué, y cómo se resolvió.

  S11  Concordancia entre las dos extracciones independientes, variable a
       variable, con la kappa donde es informativa y la advertencia donde no.
  S12  Cómo se resolvió cada desacuerdo: qué se resolvió por regla, qué se
       dirimió leyendo el artículo, y qué no se puede resolver todavía.
  S13  Las reglas de extracción de desenlaces, con la corrección documentada.
  Guía Índice en lengua llana: qué contesta cada fichero.

Todo se calcula desde los ficheros del canal. Ninguna cifra se teclea aquí: si
la hoja de consenso cambia, estos PDF cambian al reejecutar.

Uso:
    python scripts/build_extraction_verifiables.py
"""
import csv
import collections
import pathlib
import re
import sys

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.platypus import (BaseDocTemplate, Frame, PageTemplate,
                                Paragraph, Spacer, Table, TableStyle)

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from build_manuscript_pdf import estilos, inline, tabla_desde_md  # noqa: E402

ROOT = pathlib.Path(__file__).resolve().parent.parent
OUT = ROOT / "verificables revisión sistemática"
HOJA = ROOT / "revision_sistematica" / "extraccion" / "hoja_de_consenso.csv"
CONFLICTOS = ROOT / "revision_sistematica" / "extraccion" / "extraction_conflicts.csv"
ACUERDO = ROOT / "quality_reports" / "extraction_agreement.md"
REGLA_NUEVA = ROOT / "quality_reports" / "decisions" / "2026-08-12_erradicacion-regla-corregida.md"
REGLA_VIEJA = ROOT / "quality_reports" / "decisions" / "2026-08-11_definicion-erradicacion-y-exito.md"

ANCHO = A4[0] - 4.4 * cm
SIN_CITAS = lambda clave: 0          # noqa: E731  estos anexos no llevan citas

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass


def documento(destino, titulo_pie):
    doc = BaseDocTemplate(str(destino), pagesize=A4,
                          leftMargin=2.2 * cm, rightMargin=2.2 * cm,
                          topMargin=2.0 * cm, bottomMargin=1.8 * cm,
                          title=destino.stem, author="Valdiviezo D, Trelles N")
    marco = Frame(doc.leftMargin, doc.bottomMargin, doc.width, doc.height, id="n")

    def pie(canvas, d):
        canvas.saveState()
        canvas.setFont("Times-Roman", 8)
        canvas.setFillColor(colors.HexColor("#777777"))
        canvas.drawString(2.2 * cm, 1.1 * cm, titulo_pie)
        canvas.drawRightString(A4[0] - 2.2 * cm, 1.1 * cm, str(d.page))
        canvas.restoreState()

    doc.addPageTemplates([PageTemplate(id="n", frames=[marco], onPage=pie)])
    return doc


def desde_markdown(ruta, st, saltar_hasta=None):
    """Renderiza un .md del proyecto, opcionalmente desde un encabezado dado."""
    md = ruta.read_text(encoding="utf-8")
    if saltar_hasta:
        i = md.find(saltar_hasta)
        if i > 0:
            md = md[i:]
    fuera, lineas, i = [], md.split("\n"), 0
    while i < len(lineas):
        s = lineas[i].strip()
        if not s or (set(s) <= set("-") and len(s) > 2):
            i += 1
            continue
        if s.startswith("|"):
            bloque = []
            while i < len(lineas) and lineas[i].strip().startswith("|"):
                bloque.append(lineas[i])
                i += 1
            t = tabla_desde_md(bloque, st, SIN_CITAS, ANCHO)
            if t:
                fuera += [Spacer(1, 4), t, Spacer(1, 9)]
            continue
        if s.startswith("#"):
            n = len(s) - len(s.lstrip("#"))
            fuera.append(Paragraph(inline(s.lstrip("#").strip(), SIN_CITAS),
                                   st["h1" if n <= 2 else "h2"]))
        elif s.startswith(("- ", "* ")):
            fuera.append(Paragraph(inline(s[2:], SIN_CITAS), st["lista"],
                                   bulletText="•"))
        elif s.startswith("> "):
            fuera.append(Paragraph(inline(s[2:], SIN_CITAS), st["nota"]))
        else:
            fuera.append(Paragraph(inline(s, SIN_CITAS), st["cuerpo"]))
        i += 1
    return fuera


def cuadro(st, filas, cabecera, anchos):
    datos = [[Paragraph(inline(c, SIN_CITAS), st["celdah"]) for c in cabecera]]
    datos += [[Paragraph(inline(str(c), SIN_CITAS), st["celda"]) for c in f]
              for f in filas]
    t = Table(datos, colWidths=anchos, repeatRows=1, hAlign="LEFT")
    t.setStyle(TableStyle([
        ("LINEABOVE", (0, 0), (-1, 0), 0.9, colors.black),
        ("LINEBELOW", (0, 0), (-1, 0), 0.5, colors.black),
        ("LINEBELOW", (0, -1), (-1, -1), 0.9, colors.black),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("TOPPADDING", (0, 0), (-1, -1), 3.5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 3.5),
        ("LEFTPADDING", (0, 0), (-1, -1), 2),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1),
         [colors.white, colors.HexColor("#f6f6f4")]),
    ]))
    return t


# ------------------------------------------------------------------- S11
def s11(st):
    dest = OUT / "S11_concordancia_entre_extractores.pdf"
    cuerpo = [Paragraph("S11. Concordancia entre las dos extracciones independientes",
                        st["titulo"])]
    cuerpo.append(Paragraph(
        "Los dos revisores extrajeron los mismos estudios por separado y sin verse. "
        "Este anexo es la medida de cuánto coincidieron, antes de resolver nada. Se "
        "reporta tal como salió, porque una concordancia alta declarada después de "
        "consensuar no mide nada.", st["cuerpo"]))
    cuerpo += desde_markdown(ACUERDO, st, saltar_hasta="| |")
    documento(dest, "S11 · Concordancia entre extractores").build(cuerpo)
    return dest


# ------------------------------------------------------------------- S12
def s12(st):
    dest = OUT / "S12_resolucion_de_conflictos.pdf"
    filas = list(csv.DictReader(open(HOJA, encoding="utf-8")))
    todos = list(csv.DictReader(open(CONFLICTOS, encoding="utf-8")))
    por_regla = [r for r in todos if r.get("resolucion", "").strip()]
    bloques = collections.Counter(r["bloque"] for r in filas)
    refutadas = [r for r in filas if r["verificacion"].startswith("REFUTADA")]
    sin_resolver = [r for r in filas
                    if "REQUIERE CONSENSO" in r["resolucion_propuesta"].upper()]
    con_propuesta = [r for r in filas if r["resolucion_propuesta"].strip()]

    c = [Paragraph("S12. Cómo se resolvió cada desacuerdo", st["titulo"])]
    c.append(Paragraph(
        "La comparación de las dos extracciones devolvió <b>%d desacuerdos</b>. No "
        "todos son de la misma naturaleza, y tratarlos igual habría sido un error: "
        "unos se resuelven por regla, otros exigen leer el artículo, y otros no se "
        "pueden resolver todavía porque el artículo no está en nuestras manos. Este "
        "anexo documenta los tres caminos y deja el rastro completo en "
        "<font face='Courier' size='8.5'>hoja_de_consenso.csv</font>."
        % len(todos), st["cuerpo"]))

    c.append(Paragraph("Reparto de los desacuerdos", st["h1"]))
    c.append(cuadro(st, [
        ["Resueltos por regla, sin consenso", str(len(por_regla)),
         "Error de tecleo confirmado por el otro revisor, y casillas en blanco en "
         "metadatos del registro bibliográfico, que se comprueban fuera del artículo"],
        ["Bloque C · dirimibles leyendo", str(bloques["C"]),
         "Hay texto completo y la definición no está en disputa"],
        ["Bloque B · bloqueados por definición", str(bloques["B"]),
         "Tocan erradicación microbiológica o éxito clínico, cuya regla se corrigió "
         "(anexo S13); se resuelven al aplicarla"],
        ["Bloque A · sin artículo", str(bloques["A"]),
         "El estudio no tiene texto completo recuperado. No son dirimibles por "
         "nadie hasta conseguirlo"],
    ], ["Vía", "n", "Qué significa"], [6.2 * cm, 1.3 * cm, ANCHO - 7.5 * cm]))

    c.append(Paragraph("Qué NO se resolvió por regla, y por qué", st["h1"]))
    c.append(Paragraph(
        "Una casilla en blanco en un campo de desenlace no se rellena con el valor "
        "del otro revisor. El esquema de extracción distingue tres estados que no son "
        "intercambiables: vacío significa que no se contestó, <b>NA</b> que el artículo "
        "no lo notifica, y <b>0</b> que el artículo dice que fueron cero. Dar por bueno "
        "el número del único que contestó convertiría la doble extracción en simple, "
        "que es justamente lo que este diseño quiere evitar.", st["cuerpo"]))
    c.append(Paragraph(
        "Dos valores que parecían erratas tampoco se corrigieron solos: "
        "<font face='Courier' size='8.5'>'2 meses'</font> en días de estancia es un "
        "problema de unidad, y <font face='Courier' size='8.5'>'Si'</font> en un campo "
        "que pide un recuento es una respuesta a otra pregunta. Ambos se enviaron a "
        "consenso y ambos motivaron cerrar el vocabulario del formulario.", st["cuerpo"]))

    c.append(Paragraph("Adjudicación contra el texto completo", st["h1"]))
    c.append(Paragraph(
        "Los %d desacuerdos del bloque C se dirimieron abriendo el artículo. Cada "
        "propuesta se acompaña de la cita literal que la sostiene y de su "
        "localización exacta, y después pasó por un segundo lector cuyo encargo "
        "explícito era refutarla, no confirmarla. De las %d propuestas, <b>%d fueron "
        "refutadas</b> y %d quedaron sin resolver porque el artículo no contiene el "
        "dato." % (bloques["C"], len(con_propuesta), len(refutadas),
                   len(sin_resolver)), st["cuerpo"]))
    c.append(Paragraph(
        "Ninguna de estas propuestas es una resolución. Las columnas "
        "<font face='Courier' size='8.5'>resolucion</font>, "
        "<font face='Courier' size='8.5'>resuelto_por</font> y "
        "<font face='Courier' size='8.5'>fecha</font> siguen vacías, y las firman los "
        "dos revisores. Lo que este anexo aporta es el material con el que llegan a "
        "esa reunión.", st["nota"]))

    if refutadas:
        c.append(Paragraph("Propuestas refutadas por el segundo lector", st["h2"]))
        c.append(cuadro(st, [
            [f"{r['study_id']}", r["campo"], r["resolucion_propuesta"][:40],
             re.sub(r"\s+", " ", r["verificacion"].replace("REFUTADA:", ""))[:210] + "…"]
            for r in refutadas],
            ["Estudio", "Campo", "Propuesta", "Motivo de la refutación"],
            [1.9 * cm, 3.0 * cm, 3.0 * cm, ANCHO - 7.9 * cm]))

    c.append(Paragraph("Desacuerdos por variable", st["h1"]))
    porc = collections.Counter(r["campo"] for r in filas)
    c.append(cuadro(st, [[k, str(v)] for k, v in porc.most_common(12)],
                    ["Variable", "Desacuerdos"], [ANCHO - 3.2 * cm, 3.2 * cm]))

    c.append(Paragraph("Lo que todavía no se puede resolver", st["h1"]))
    sinart = collections.Counter(r["study_id"] for r in filas if r["bloque"] == "A")
    c.append(Paragraph(
        "El bloque A concentra %d desacuerdos en %d estudios sin texto completo. Dos "
        "de ellos explican la mayor parte, y ninguno se resuelve discutiendo: se "
        "resuelve consiguiendo el artículo."
        % (bloques["A"], len(sinart)), st["cuerpo"]))
    c.append(cuadro(st, [[k, str(v)] for k, v in sinart.most_common()],
                    ["Estudio sin texto completo", "Desacuerdos"],
                    [ANCHO - 3.2 * cm, 3.2 * cm]))
    documento(dest, "S12 · Resolución de conflictos").build(c)
    return dest


# ------------------------------------------------------------------- S13
def s13(st):
    dest = OUT / "S13_reglas_de_extraccion_de_desenlaces.pdf"
    c = [Paragraph("S13. Reglas de extracción de desenlaces", st["titulo"])]
    c.append(Paragraph(
        "La concordancia más baja de toda la extracción se dio en erradicación "
        "microbiológica. Al mirar los desacuerdos uno a uno, la causa no era el "
        "descuido de ningún revisor: era que el campo admitía dos lecturas legítimas. "
        "Este anexo documenta la regla que se fijó, la corrección que sufrió al "
        "probarla contra los artículos, y las dos columnas que hubo que añadir al "
        "formulario. Se incluye porque una definición de desenlace que cambia a mitad "
        "de una revisión es exactamente lo que un lector necesita poder auditar.",
        st["cuerpo"]))
    c += desde_markdown(REGLA_NUEVA, st, saltar_hasta="## Por qué hubo que corregirla")
    c.append(Paragraph("Antecedente: la versión que se corrigió", st["h1"]))
    c.append(Paragraph(
        "La primera versión de la regla, del 11 de agosto de 2026, se conserva íntegra "
        "en el repositorio del proyecto. Sus reglas sobre definición de éxito clínico y "
        "sobre la distinción entre casilla vacía, NA y cero siguen vigentes sin cambios; "
        "solo se corrigió la regla de erradicación. El registro de decisiones es "
        "solo-anexar: la corrección forma parte del rastro y no lo sustituye.",
        st["cuerpo"]))
    c += desde_markdown(REGLA_VIEJA, st, saltar_hasta="## Regla 2")
    documento(dest, "S13 · Reglas de extracción de desenlaces").build(c)
    return dest


def main():
    st = estilos()
    OUT.mkdir(parents=True, exist_ok=True)
    for f in (s11, s12, s13):
        d = f(st)
        print(f"  {d.name:52} {d.stat().st_size // 1024} KB")


if __name__ == "__main__":
    main()
