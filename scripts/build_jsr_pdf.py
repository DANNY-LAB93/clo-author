"""Maqueta el manuscrito de JSR en PDF, con el formato que pide la revista.

POR QUE EXISTE, Y UN AVISO. La revista NO acepta PDF como fichero de envio: su
lista de comprobacion dice «El archivo de envio esta en formato OpenOffice,
Microsoft Word, RTF o WordPerfect». Lo que se manda es
`manuscrito_JSR_final.docx`. Este PDF es para leer, imprimir y pasarselo a
alguien sin que se le mueva la maquetacion.

EN ESTA MAQUINA NO HAY CONVERSOR. No hay Word por COM, ni LibreOffice, ni
pandoc; comprobado. Asi que el PDF no se convierte del .docx: se maqueta otra
vez desde el mismo markdown con reportlab, que es lo que ya hace
`build_manuscript_pdf.py` con el maestro y el ingles. Consecuencia que conviene
tener presente: los saltos de pagina no tienen por que coincidir con los que
Word calcule sobre el .docx.

LAS NORMAS DE LA REVISTA, leidas en revistas.utb.edu.ec el 2026-09-14 y
aplicadas aqui igual que en el .docx: A4, margenes de 3 cm, Times New Roman 12,
doble espacio, parrafos justificados y sin espacio entre consecutivos, titulo
en mayuscula sostenida a 18 pt, resalte en cursiva y no en negrita, y las
palabras clave en negrita y cursiva.

LAS TABLAS SON LAS DE JSR. El manuscrito de la revista renumera: su Tabla 1 es
la de criterios y su Tabla 5 la de riesgo de sesgo. El mapa se importa de
`build_jsr_docx` para que no haya dos versiones del mismo mapa.

Salida:
    paper/pdf/manuscrito_JSR_final.pdf

Uso:
    python scripts/build_jsr_pdf.py
"""
import csv
import pathlib
import re
import sys

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import cm
from reportlab.platypus import (BaseDocTemplate, Frame, Image, KeepTogether,
                                PageTemplate, Paragraph, Spacer, Table, TableStyle)

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from build_jsr_docx import ADJUNTOS

ROOT = pathlib.Path(__file__).resolve().parent.parent
FUENTE = ROOT / "paper" / "manuscrito_JSR_final.md"
SALIDA = ROOT / "paper" / "pdf" / "manuscrito_JSR_final.pdf"
MARGEN = 3 * cm

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass


def inline(t):
    """Markdown de linea -> marcado de reportlab.

    La negrita del markdown sale en CURSIVA, igual que en el .docx y por la
    misma directriz: «no usar letra negrita sino letra cursiva». Aqui no hay
    parametro que distinga estructura de resalte, asi que los titulos y los
    encabezados se emiten aparte, con su estilo, y nunca pasan por aqui con
    asteriscos dentro.
    """
    t = t.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
    t = re.sub(r"\*\*(.+?)\*\*", r"<i>\1</i>", t)
    t = re.sub(r"(?<![\w*])\*([^*\n]+?)\*(?![\w*])", r"<i>\1</i>", t)
    return t


def estilos():
    b = getSampleStyleSheet()
    s = {}
    # 18 pt y mayuscula sostenida: lo pide la directriz del titulo.
    s["titulo"] = ParagraphStyle("t", parent=b["Title"], fontName="Times-Bold",
                                 fontSize=18, leading=22, spaceAfter=10)
    s["titulo_en"] = ParagraphStyle("te", parent=s["titulo"], spaceAfter=16)
    s["autores"] = ParagraphStyle("a", parent=b["Normal"], fontName="Times-Roman",
                                  fontSize=12, leading=16, alignment=TA_CENTER,
                                  spaceAfter=4)
    # «no debe haber espacio entre los consecutivos»: spaceAfter = 0 en el
    # cuerpo. El doble espacio se hace con leading, 12 pt * 2.
    s["cuerpo"] = ParagraphStyle("c", parent=b["BodyText"], fontName="Times-Roman",
                                 fontSize=12, leading=24, alignment=TA_JUSTIFY,
                                 spaceAfter=0, firstLineIndent=0)
    s["clave"] = ParagraphStyle("cl", parent=s["cuerpo"], fontName="Times-BoldItalic")
    s["h1"] = ParagraphStyle("h1", parent=b["Heading1"], fontName="Times-Bold",
                             fontSize=12, leading=20, spaceBefore=14, spaceAfter=6)
    s["h2"] = ParagraphStyle("h2", parent=b["Heading2"], fontName="Times-Bold",
                             fontSize=12, leading=18, spaceBefore=10, spaceAfter=4)
    s["pie"] = ParagraphStyle("p", parent=b["BodyText"], fontName="Times-Roman",
                              fontSize=10, leading=13, alignment=TA_JUSTIFY,
                              spaceBefore=10, spaceAfter=5)
    s["celda"] = ParagraphStyle("ce", parent=b["BodyText"], fontName="Times-Roman",
                                fontSize=9, leading=11.5, spaceAfter=0)
    s["celdah"] = ParagraphStyle("ch", parent=s["celda"], fontName="Times-Bold")
    s["ref"] = ParagraphStyle("r", parent=b["BodyText"], fontName="Times-Roman",
                              fontSize=11, leading=15, spaceAfter=4,
                              leftIndent=18, firstLineIndent=-18)
    return s


def tabla_csv(ruta, st, ancho):
    with open(ruta, encoding="utf-8-sig", newline="") as fh:
        filas = [f for f in csv.reader(fh) if any(c.strip() for c in f)]
    if not filas:
        return None
    n = max(len(f) for f in filas)
    filas = [f + [""] * (n - len(f)) for f in filas]
    datos = [[Paragraph(inline(c), st["celdah" if i == 0 else "celda"]) for c in f]
             for i, f in enumerate(filas)]
    primera = max(3.0 * cm, ancho - (n - 1) * 2.4 * cm) if n > 1 else ancho
    anchos = ([primera] + [(ancho - primera) / (n - 1)] * (n - 1)) if n > 1 else [ancho]
    t = Table(datos, colWidths=anchos, repeatRows=1, hAlign="LEFT")
    t.setStyle(TableStyle([
        ("LINEABOVE", (0, 0), (-1, 0), 0.9, colors.black),
        ("LINEBELOW", (0, 0), (-1, 0), 0.5, colors.black),
        ("LINEBELOW", (0, -1), (-1, -1), 0.9, colors.black),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("TOPPADDING", (0, 0), (-1, -1), 3),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
        ("LEFTPADDING", (0, 0), (-1, -1), 2),
    ]))
    return t


def imagen(ruta, ancho):
    from reportlab.lib.utils import ImageReader
    iw, ih = ImageReader(str(ruta)).getSize()
    w = min(ancho, 15 * cm)
    return Image(str(ruta), width=w, height=w * ih / iw)


def construye(md, st, ancho):
    fuera, lineas, i, titulos = [], md.split("\n"), 0, 0
    while i < len(lineas):
        l = lineas[i].rstrip()
        i += 1
        if not l or l == "---":
            continue
        if l.startswith("# "):
            titulos += 1
            fuera.append(Paragraph(inline(l[2:].upper()),
                                   st["titulo" if titulos == 1 else "titulo_en"]))
            continue
        if l.startswith("### "):
            fuera.append(Paragraph(inline(l[4:]), st["h2"]))
            continue
        if l.startswith("## "):
            fuera.append(Paragraph(inline(l[3:].upper()), st["h1"]))
            continue
        m = re.match(r"^\*\*(Palabras clave|Keywords):\*\*\s*(.+)$", l)
        if m:
            fuera.append(Paragraph("<i>%s:</i> %s" % (m.group(1), inline(m.group(2))),
                                   st["clave"]))
            continue
        adj = next((k for k in ADJUNTOS if l.startswith("**" + k)), None)
        if adj:
            ruta = ADJUNTOS[adj]
            if not ruta.exists():
                raise SystemExit("falta %s, que la %s necesita" % (ruta.name, adj))
            cuerpo = (imagen(ruta, ancho) if ruta.suffix == ".png"
                      else tabla_csv(ruta, st, ancho))
            pie = Paragraph(inline(l), st["pie"])
            fuera.append(KeepTogether([pie, cuerpo]) if cuerpo else pie)
            fuera.append(Spacer(1, 8))
            continue
        estilo = st["ref"] if re.match(r"^\d+\. ", l) else st["cuerpo"]
        fuera.append(Paragraph(inline(l), estilo))
    return fuera


def main():
    if not FUENTE.exists():
        raise SystemExit("no encuentro %s" % FUENTE.name)
    st = estilos()
    md = FUENTE.read_text(encoding="utf-8")
    ancho = A4[0] - 2 * MARGEN
    cuerpo = construye(md, st, ancho)

    SALIDA.parent.mkdir(parents=True, exist_ok=True)
    destino = SALIDA
    try:
        open(destino, "ab").close()
    except PermissionError:
        destino = SALIDA.with_name(SALIDA.stem + "_NUEVO.pdf")
        print("AVISO: estaba abierto; escrito al lado como %s" % destino.name)

    doc = BaseDocTemplate(str(destino), pagesize=A4,
                          leftMargin=MARGEN, rightMargin=MARGEN,
                          topMargin=MARGEN, bottomMargin=MARGEN,
                          title="Fagoterapia en Pseudomonas aeruginosa multirresistente",
                          author="Valdiviezo D, Trelles N")
    marco = Frame(doc.leftMargin, doc.bottomMargin, doc.width, doc.height, id="n")

    def pie(canvas, documento):
        canvas.saveState()
        canvas.setFont("Times-Roman", 9)
        canvas.setFillColor(colors.HexColor("#666666"))
        canvas.drawCentredString(A4[0] / 2, 1.4 * cm, str(documento.page))
        canvas.drawString(MARGEN, A4[1] - 1.6 * cm,
                          "JOURNAL OF SCIENCE AND RESEARCH  E-ISSN: 2528-8083")
        canvas.restoreState()

    doc.addPageTemplates([PageTemplate(id="n", frames=[marco], onPage=pie)])
    doc.build(cuerpo)
    print("escrito %s  (%d KB)" % (destino.relative_to(ROOT),
                                   destino.stat().st_size // 1024))
    print("  A4, márgenes %.0f cm, Times New Roman 12, doble espacio" % (MARGEN / cm))
    print("  NO es el fichero de envío: la revista pide Word, RTF u OpenOffice.")


if __name__ == "__main__":
    main()
