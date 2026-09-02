"""Convierte el manuscrito editado para JSR a .docx con el formato de la revista.

Times New Roman 12, A4, márgenes de una pulgada, interlineado doble,
texto justificado y cabecera con el ISSN. Los encabezados de sección van en
versalitas y negrita; las tablas en markdown se convierten en tablas de Word.

Entrada:
    paper/manuscrito_JSR_final.md

Salida:
    ~/Desktop/Envio_JSR_Fagoterapia_Pseudomonas/manuscrito_JSR_final.docx

Uso:
    python scripts/build_jsr_docx.py
"""
import pathlib
import re
import sys

import docx
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.shared import Pt, Inches, Mm
import csv as _csv

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

ROOT = pathlib.Path(__file__).resolve().parent.parent
FUENTE = ROOT / "paper" / "manuscrito_JSR_final.md"
DEST = pathlib.Path.home() / "Desktop" / "Envio_JSR_Fagoterapia_Pseudomonas"
TNR = "Times New Roman"
TABLAS = ROOT / "paper" / "tablas"
FIGURAS = ROOT / "paper" / "figuras"

# El manuscrito renumero sus tablas al reestructurarse para la revista: la
# Tabla 1 es la de criterios, que va escrita en el propio markdown, y las
# demas vienen de los CSV que produce el canal. Este mapa es el unico sitio
# donde se declara esa correspondencia.
ADJUNTOS = {
    "Tabla 2.": TABLAS / "tabla_1_caracteristicas.csv",
    "Tabla 3.": TABLAS / "tabla_2_completitud.csv",
    "Tabla 4.": TABLAS / "tabla_5_desenlaces.csv",
    "Tabla 5.": TABLAS / "tabla_6_embudo.csv",
    "Figura 1.": FIGURAS / "figura_1_prisma.png",
    "Figura 2.": FIGURAS / "figura_2_composicion.png",
}


def documento():
    d = docx.Document()
    s = d.sections[0]
    # A4 y doble espacio: lo que piden las normas de la revista
    # (revistas.utb.edu.ec/index.php/sr, consultadas el 2026-09-02).
    s.page_width, s.page_height = Mm(210), Mm(297)
    for lado in ("left_margin", "right_margin", "top_margin", "bottom_margin"):
        setattr(s, lado, Inches(1))
    n = d.styles["Normal"]
    n.font.name = TNR
    n.font.size = Pt(12)
    n.paragraph_format.space_after = Pt(10)
    n.paragraph_format.line_spacing = 2.0
    cab = s.header.paragraphs[0]
    cab.text = "JOURNAL OF SCIENCE AND RESEARCH E-ISSN: 2528-8083"
    cab.runs[0].font.size = Pt(10)
    cab.runs[0].font.name = TNR
    return d


def escribe(p, txt, size=12, negrita=False, cursiva=False):
    """Resuelve **negrita** y *cursiva* en linea, que es como viene el markdown."""
    for trozo in re.split(r"(\*\*[^*]+\*\*|\*[^*]+\*)", txt):
        if not trozo:
            continue
        neg = trozo.startswith("**")
        cur = trozo.startswith("*") and not neg
        r = p.add_run(trozo.strip("*"))
        r.font.name = TNR
        r.font.size = Pt(size)
        r.bold = negrita or neg
        r.italic = cursiva or cur


def tabla(d, filas):
    """Una tabla markdown -> tabla de Word, con la cabecera en negrita."""
    cols = [c.strip() for c in filas[0].strip("|").split("|")]
    cuerpo = [[c.strip() for c in f.strip("|").split("|")] for f in filas[2:]]
    t = d.add_table(rows=1, cols=len(cols))
    t.style = "Table Grid"
    t.alignment = WD_TABLE_ALIGNMENT.CENTER
    for i, c in enumerate(cols):
        cel = t.rows[0].cells[i]
        cel.text = ""
        escribe(cel.paragraphs[0], c, size=10, negrita=True)
    for fila in cuerpo:
        cs = t.add_row().cells
        for i, v in enumerate(fila[:len(cols)]):
            cs[i].text = ""
            escribe(cs[i].paragraphs[0], v, size=10)
    d.add_paragraph()


def tabla_csv(d, ruta):
    with open(ruta, encoding="utf-8-sig", newline="") as fh:
        filas = [r for r in _csv.reader(fh) if any(c.strip() for c in r)]
    if not filas:
        return
    t = d.add_table(rows=1, cols=len(filas[0]))
    t.style = "Table Grid"
    t.alignment = WD_TABLE_ALIGNMENT.CENTER
    for i, c in enumerate(filas[0]):
        cel = t.rows[0].cells[i]
        cel.text = ""
        escribe(cel.paragraphs[0], c, size=9, negrita=True)
    for f in filas[1:]:
        cs = t.add_row().cells
        for i, v in enumerate(f[:len(filas[0])]):
            cs[i].text = ""
            escribe(cs[i].paragraphs[0], v, size=9)
    d.add_paragraph()


def figura(d, ruta):
    p = d.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.add_run().add_picture(str(ruta), width=Inches(5.6))
    d.add_paragraph()


def main():
    if not FUENTE.exists():
        print("no encuentro %s" % FUENTE.name)
        return 1
    lineas = FUENTE.read_text(encoding="utf-8").split("\n")
    d = documento()
    i, titulos = 0, 0
    while i < len(lineas):
        l = lineas[i].rstrip()
        # tabla: se consume entera de una vez
        if l.startswith("|"):
            bloque = []
            while i < len(lineas) and lineas[i].startswith("|"):
                bloque.append(lineas[i])
                i += 1
            if len(bloque) > 2:
                tabla(d, bloque)
            continue
        i += 1
        if not l or l == "---":
            continue
        if l.startswith("# "):
            titulos += 1
            p = d.add_paragraph()
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            p.paragraph_format.space_after = Pt(6 if titulos == 1 else 12)
            escribe(p, l[2:], size=14, negrita=True, cursiva=False)
            continue
        if l.startswith("### "):
            p = d.add_paragraph()
            p.alignment = WD_ALIGN_PARAGRAPH.LEFT
            p.paragraph_format.space_before = Pt(10)
            p.paragraph_format.space_after = Pt(6)
            escribe(p, l[4:], size=12, negrita=True)
            continue
        if l.startswith("## "):
            p = d.add_paragraph()
            p.alignment = WD_ALIGN_PARAGRAPH.LEFT
            p.paragraph_format.space_before = Pt(14)
            p.paragraph_format.space_after = Pt(8)
            escribe(p, l[3:].upper(), size=12, negrita=True)
            continue
        # pie de tabla o figura: se escribe y se adjunta lo que nombra
        adj = next((k for k in ADJUNTOS if l.startswith("**" + k)), None)
        if adj:
            pie = d.add_paragraph()
            pie.alignment = WD_ALIGN_PARAGRAPH.LEFT
            pie.paragraph_format.space_before = Pt(12)
            pie.paragraph_format.space_after = Pt(6)
            pie.paragraph_format.line_spacing = 1.0
            escribe(pie, l, size=10)
            ruta = ADJUNTOS[adj]
            if not ruta.exists():
                raise SystemExit("falta %s, que la %s necesita" % (ruta.name, adj))
            (figura if ruta.suffix == ".png" else tabla_csv)(d, ruta)
            continue

        # referencia numerada o vineta: sangria francesa
        p = d.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        if re.match(r"^\d+\. ", l) or l.startswith("- "):
            p.paragraph_format.left_indent = Inches(0.4)
            p.paragraph_format.first_line_indent = Inches(-0.4)
            p.paragraph_format.space_after = Pt(6)
            p.paragraph_format.line_spacing = 1.15
            if l.startswith("- "):
                l = "• " + l[2:]
        escribe(p, l)

    DEST.mkdir(parents=True, exist_ok=True)
    salida = DEST / "manuscrito_JSR_final.docx"
    try:
        d.save(salida)
    except PermissionError:
        # Word bloquea el fichero mientras lo tiene abierto. Se escribe al lado
        # y se dice, en vez de morir o de dejar creer que se guardo.
        salida = DEST / "manuscrito_JSR_final_NUEVO.docx"
        d.save(salida)
        print("AVISO: el .docx estaba abierto en Word y no se pudo sobrescribir.")
        print("       Cierra Word y renombra este fichero, o vuelve a ejecutar el guion.")
    print("escrito %s  (%d KB)" % (salida, salida.stat().st_size // 1024))
    print("  Times New Roman 12, A4, márgenes 1\", interlineado doble, justificado")


if __name__ == "__main__":
    main()
