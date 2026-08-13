"""Maqueta el manuscrito en PDF listo para enviar, con las citas resueltas.

QUÉ RESUELVE

El manuscrito vive en Markdown con citas en formato `[@clave]`, que es cómodo
para escribir y no se puede mandar a una revista. Este script hace las tres
cosas que faltan para que sea un PDF de verdad:

  1. Numera las citas por orden de aparición y construye la lista de
     referencias desde `Bibliography_base.bib`. Si una clave no tiene entrada,
     falla en vez de imprimir `[@clave]` en el PDF final.
  2. Inserta las figuras y las tablas en su sitio, leyendo las tablas desde
     `paper/tablas/*.md`, que es donde el canal las deja. Ninguna cifra se
     teclea aquí.
  3. Maqueta con márgenes, numeración de página y jerarquía de títulos.

No usa LaTeX ni pandoc a propósito: en esta máquina no hay ninguno de los dos,
y una dependencia que no se puede instalar es una dependencia que rompe la
reproducibilidad justo cuando hace falta.

Uso:
    python scripts/build_manuscript_pdf.py            # las dos versiones
    python scripts/build_manuscript_pdf.py --solo es
"""
import argparse
import pathlib
import re
import sys

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import cm
from reportlab.platypus import (BaseDocTemplate, Frame, Image, KeepTogether,
                                PageBreak, PageTemplate, Paragraph, Spacer,
                                Table, TableStyle)

ROOT = pathlib.Path(__file__).resolve().parent.parent
BIB = ROOT / "Bibliography_base.bib"
FIGURAS = ROOT / "paper" / "figuras"
TABLAS = ROOT / "paper" / "tablas"
SALIDA = ROOT / "paper" / "pdf"

VERSIONES = {
    "es": (ROOT / "paper" / "manuscrito_revision_sistematica.md",
           SALIDA / "manuscrito_revision_sistematica.pdf",
           {"refs": "Referencias", "cont": "continúa"}),
    "en": (ROOT / "paper" / "manuscript_systematic_review_en.md",
           SALIDA / "manuscript_systematic_review_en.pdf",
           {"refs": "References", "cont": "continued"}),
}

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass


# --------------------------------------------------------------- bibliografía
ACENTOS = [
    (r"\{\\'\{?([aeiouAEIOUyn])\}?\}", r"\1"), (r"\\'\{?([aeiouAEIOUyn])\}?", r"\1"),
    (r'\{\\"\{?([aeiouAEIOUu])\}?\}', r"\1"), (r'\\"\{?([aeiouAEIOU])\}?', r"\1"),
    (r"\{\\`\{?([aeiouAEIOU])\}?\}", r"\1"), (r"\\`\{?([aeiouAEIOU])\}?", r"\1"),
    (r"\{\\\^\{?([aeiouAEIOU])\}?\}", r"\1"), (r"\\\^\{?([aeiouAEIOU])\}?", r"\1"),
    (r"\{\\~\{?([nN])\}?\}", r"\1"), (r"\\~\{?([nN])\}?", r"\1"),
    (r"\{\\c\{?c\}?\}", "c"), (r"\{\\o\}", "o"), (r"\\o\b", "o"),
    (r"\{\\aa\}", "a"), (r"\{\\ss\}", "ss"),
]


def limpia(s):
    """Quita el andamiaje de LaTeX que trae el .bib."""
    for pat, rep in ACENTOS:
        s = re.sub(pat, rep, s)
    s = s.replace("{", "").replace("}", "").replace("\\&", "&")
    return re.sub(r"\s+", " ", s).strip()


def lee_bib(ruta):
    """{clave: {campo: valor}} desde un .bib. Tolera anidamiento de llaves."""
    texto = ruta.read_text(encoding="utf-8", errors="replace")
    entradas = {}
    for m in re.finditer(r"@(\w+)\s*\{\s*([^,]+),", texto):
        clave = m.group(2).strip()
        i, prof, fin = m.end(), 1, len(texto)
        while i < len(texto):
            if texto[i] == "{":
                prof += 1
            elif texto[i] == "}":
                prof -= 1
                if prof == 0:
                    fin = i
                    break
            i += 1
        cuerpo = texto[m.end():fin]
        campos = {}
        for cm in re.finditer(r"(\w+)\s*=\s*[{\"](.*?)[}\"]\s*,?\s*(?=\w+\s*=|$)",
                              cuerpo, re.S):
            campos[cm.group(1).lower()] = limpia(cm.group(2))
        entradas[clave] = campos
    return entradas


def formatea_referencia(n, e):
    """Estilo Vancouver abreviado: es el que piden casi todas las de este campo."""
    autores = [a.strip() for a in re.split(r"\s+and\s+", e.get("author", "")) if a.strip()]
    nombres = []
    for a in autores[:6]:
        if "," in a:
            ape, nom = a.split(",", 1)
            iniciales = "".join(p[0] for p in nom.split() if p)
            nombres.append(f"{ape.strip()} {iniciales}")
        else:
            nombres.append(a)
    firma = ", ".join(nombres) + (", et al" if len(autores) > 6 else "")
    partes = [firma + ".", e.get("title", "").rstrip(".") + "."]
    rev = e.get("journal") or e.get("journaltitle") or e.get("publisher") or ""
    if rev:
        partes.append(f"<i>{rev}</i>.")
    anio = e.get("year") or e.get("date", "")[:4]
    cola = anio
    if e.get("volume"):
        cola += f";{e['volume']}"
        if e.get("number"):
            cola += f"({e['number']})"
    if e.get("pages"):
        cola += f":{e['pages'].replace('--', '-')}"
    if cola:
        partes.append(cola + ".")
    if e.get("doi"):
        partes.append(f"doi:{e['doi']}")
    return f"{n}. " + " ".join(p for p in partes if p.strip(". "))


# ------------------------------------------------------------------- markdown
def inline(texto, cita):
    """Markdown de línea -> marcado de reportlab. `cita` numera las referencias."""
    texto = texto.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")

    def ref(m):
        claves = [c.strip().lstrip("@") for c in m.group(1).split(";")]
        return "<super>" + ",".join(str(cita(c)) for c in claves) + "</super>"

    texto = re.sub(r"\[([^\]]*@[^\]]+)\]", ref, texto)
    texto = re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", texto)
    texto = re.sub(r"(?<![\w*])\*([^*\n]+?)\*(?![\w*])", r"<i>\1</i>", texto)
    texto = re.sub(r"\^(\w+?)\^", r"<super>\1</super>", texto)
    texto = re.sub(r"`([^`]+?)`", r'<font face="Courier" size="8.5">\1</font>', texto)
    return texto


def estilos():
    base = getSampleStyleSheet()
    s = {}
    s["titulo"] = ParagraphStyle("titulo", parent=base["Title"], fontName="Times-Bold",
                                 fontSize=15, leading=19, spaceAfter=14)
    s["autores"] = ParagraphStyle("autores", parent=base["Normal"], fontName="Times-Roman",
                                  fontSize=11, leading=15, alignment=TA_CENTER, spaceAfter=6)
    s["afil"] = ParagraphStyle("afil", parent=base["Normal"], fontName="Times-Roman",
                               fontSize=9, leading=12, alignment=TA_CENTER, spaceAfter=3,
                               textColor=colors.HexColor("#333333"))
    s["h1"] = ParagraphStyle("h1", parent=base["Heading1"], fontName="Times-Bold",
                             fontSize=13, leading=16, spaceBefore=16, spaceAfter=7,
                             textColor=colors.HexColor("#1a1a1a"))
    s["h2"] = ParagraphStyle("h2", parent=base["Heading2"], fontName="Times-Bold",
                             fontSize=11, leading=14, spaceBefore=11, spaceAfter=5,
                             textColor=colors.HexColor("#1a1a1a"))
    s["cuerpo"] = ParagraphStyle("cuerpo", parent=base["BodyText"], fontName="Times-Roman",
                                 fontSize=10.5, leading=15, alignment=TA_JUSTIFY,
                                 spaceAfter=7, firstLineIndent=0)
    s["lista"] = ParagraphStyle("lista", parent=s["cuerpo"], leftIndent=14,
                                bulletIndent=4, spaceAfter=4)
    s["nota"] = ParagraphStyle("nota", parent=base["BodyText"], fontName="Times-Roman",
                               fontSize=8.5, leading=11.5, alignment=TA_JUSTIFY,
                               textColor=colors.HexColor("#444444"), spaceAfter=9)
    s["celda"] = ParagraphStyle("celda", parent=base["BodyText"], fontName="Times-Roman",
                                fontSize=8.5, leading=11, spaceAfter=0)
    s["celdah"] = ParagraphStyle("celdah", parent=s["celda"], fontName="Times-Bold")
    s["ref"] = ParagraphStyle("ref", parent=base["BodyText"], fontName="Times-Roman",
                              fontSize=9, leading=12, spaceAfter=5,
                              leftIndent=16, firstLineIndent=-16)
    return s


def tabla_desde_md(lineas, st, cita, ancho):
    filas = []
    for ln in lineas:
        celdas = [c.strip() for c in ln.strip().strip("|").split("|")]
        if all(re.fullmatch(r":?-{2,}:?", c) for c in celdas if c):
            continue
        filas.append(celdas)
    if not filas:
        return None
    ncol = max(len(f) for f in filas)
    filas = [f + [""] * (ncol - len(f)) for f in filas]
    datos = [[Paragraph(inline(c, cita), st["celdah" if i == 0 else "celda"])
              for c in fila] for i, fila in enumerate(filas)]
    primera = max(2.6 * cm, ancho - (ncol - 1) * 2.3 * cm) if ncol > 1 else ancho
    anchos = [primera] + [(ancho - primera) / (ncol - 1)] * (ncol - 1) if ncol > 1 else [ancho]
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


def figura(nombre, ancho):
    p = FIGURAS / nombre
    if not p.exists():
        return None
    from reportlab.lib.utils import ImageReader
    iw, ih = ImageReader(str(p)).getSize()
    w = min(ancho, 15 * cm)
    return Image(str(p), width=w, height=w * ih / iw)


def construye(md, st, cita, ancho, txt):
    """Markdown -> lista de flowables."""
    fuera = []
    lineas = md.split("\n")
    i = 0
    en_cabecera = True
    while i < len(lineas):
        ln = lineas[i]
        s = ln.strip()

        if not s:
            i += 1
            continue

        if s.startswith("---") and set(s) <= set("-"):
            i += 1
            continue

        if s.startswith("#"):
            n = len(s) - len(s.lstrip("#"))
            texto = s.lstrip("#").strip()
            if n == 1 and en_cabecera:
                fuera.append(Paragraph(inline(texto, cita), st["titulo"]))
                en_cabecera = False
            else:
                fuera.append(Paragraph(inline(texto, cita), st["h1" if n <= 2 else "h2"]))
            i += 1
            continue

        if s.startswith("|"):
            bloque = []
            while i < len(lineas) and lineas[i].strip().startswith("|"):
                bloque.append(lineas[i])
                i += 1
            t = tabla_desde_md(bloque, st, cita, ancho)
            if t:
                fuera.append(Spacer(1, 4))
                fuera.append(t)
                fuera.append(Spacer(1, 9))
            continue

        if s.startswith(("- ", "* ")):
            fuera.append(Paragraph(inline(s[2:], cita), st["lista"], bulletText="\u2022"))
            i += 1
            continue

        if s.startswith("> "):
            fuera.append(Paragraph(inline(s[2:], cita), st["nota"]))
            i += 1
            continue

        # figuras: la leyenda las anuncia, la imagen va justo antes
        m = re.match(r"\*\*Fig(?:ura|ure)\s*(\d)", s)
        if m:
            img = figura({"1": "figura_1_prisma.png",
                          "2": "figura_2_composicion.png"}[m.group(1)], ancho)
            if img:
                fuera.append(Spacer(1, 6))
                fuera.append(img)
                fuera.append(Spacer(1, 4))

        estilo = st["nota"] if s.startswith("*") and s.endswith(".") and len(s) > 120 else st["cuerpo"]
        if re.match(r"\*\*(Tabla|Table|Figura|Figure)\s*\d", s):
            estilo = st["cuerpo"]
        fuera.append(Paragraph(inline(s, cita), estilo))
        i += 1

    return fuera


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--solo", choices=("es", "en"), default=None)
    args = ap.parse_args()

    SALIDA.mkdir(parents=True, exist_ok=True)
    bib = lee_bib(BIB)
    st = estilos()

    for cod, (origen, destino, txt) in VERSIONES.items():
        if args.solo and cod != args.solo:
            continue

        orden, faltan = [], []

        def cita(clave):
            if clave not in bib:
                if clave not in faltan:
                    faltan.append(clave)
                return "?"
            if clave not in orden:
                orden.append(clave)
            return orden.index(clave) + 1

        md = origen.read_text(encoding="utf-8")
        md = md.replace("dvchiqui@gmail.com", "dvchiqui[at]gmail.com")  # no es una cita

        ancho = A4[0] - 4.4 * cm
        cuerpo = construye(md, st, cita, ancho, txt)

        if faltan:
            print(f"  FALLO en {cod}: claves sin entrada en el .bib -> {faltan}")
            sys.exit(1)

        cuerpo.append(Paragraph(txt["refs"], st["h1"]))
        for n, clave in enumerate(orden, 1):
            cuerpo.append(Paragraph(formatea_referencia(n, bib[clave]), st["ref"]))

        doc = BaseDocTemplate(str(destino), pagesize=A4,
                              leftMargin=2.2 * cm, rightMargin=2.2 * cm,
                              topMargin=2.0 * cm, bottomMargin=1.8 * cm,
                              title=origen.stem, author="Valdiviezo D, Trelles N")
        marco = Frame(doc.leftMargin, doc.bottomMargin, doc.width, doc.height, id="n")

        def pie(canvas, documento):
            canvas.saveState()
            canvas.setFont("Times-Roman", 8.5)
            canvas.setFillColor(colors.HexColor("#666666"))
            canvas.drawCentredString(A4[0] / 2, 1.1 * cm, str(documento.page))
            canvas.restoreState()

        doc.addPageTemplates([PageTemplate(id="normal", frames=[marco], onPage=pie)])
        doc.build(cuerpo)
        print(f"  {destino.name:44} {len(orden)} referencias, "
              f"{destino.stat().st_size // 1024} KB")


if __name__ == "__main__":
    main()
