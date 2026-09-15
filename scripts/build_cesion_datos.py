"""Hoja de datos para rellenar la carta de cesion de derechos de JSR.

QUE ES Y QUE NO ES. NO es la carta. La carta la provee la revista y hay que
descargarla de su seccion «Archivos y formatos descargables»; su lista de
comprobacion dice que el envio se devuelve si no llega en el formato de ellos.
Esto es la hoja con lo que va en cada hueco de ESE documento, para no tener que
buscar el titulo exacto ni volver a teclearlo.

DE DONDE SALE. El titulo se lee del manuscrito de envio, no se teclea. Lo
demas son datos de autor que el proyecto no tiene y que solo pueden poner
ellos: documento de identidad, ORCID y el correo de N. Trelles. Se dejan en
blanco a proposito y marcados.

Salida:
    paper/docx/datos_carta_cesion.docx

Uso:
    python scripts/build_cesion_datos.py
"""
import pathlib
import re
import sys

try:
    import docx
    from docx.enum.text import WD_ALIGN_PARAGRAPH
    from docx.shared import Pt, Inches, Mm, RGBColor
except ImportError:
    raise SystemExit("hace falta python-docx: python -m pip install python-docx")

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from build_jsr_docx import escribe

ROOT = pathlib.Path(__file__).resolve().parent.parent
JSR = ROOT / "paper" / "manuscrito_JSR_final.md"
DEST = ROOT / "paper" / "docx"
TNR = "Times New Roman"

FORMULARIO = "https://revistas.utb.edu.ec/index.php/sr/about/submissions"

# Los ocho puntos que el firmante acepta, copiados de la carta de la revista el
# 14 de septiembre de 2026. Se reproducen aqui PARA COMPROBARLOS, no para
# sustituir al documento: junto a cada uno va si este trabajo lo cumple y donde
# consta. El que firme tiene que poder responder por los ocho.
PUNTOS = [
    ("Se esta de acuerdo con el contenido publicado en el mismo.",
     "Lo firman los dos autores. Ver el punto pendiente al final."),
    ("Cesion a titulo gratuito de la totalidad de los derechos patrimoniales de "
     "autor derivados del articulo, a favor de la citada publicacion.",
     "Decision de los autores. No afecta a nada de lo construido."),
    ("Se esta de acuerdo con el orden en el que aparecen los autores.",
     "D. Valdiviezo primero, N. Trelles segunda, como en el manuscrito."),
    ("No existen personas adicionales que satisfagan los criterios de autoria y "
     "no hayan sido incluidas.",
     "Cierto: la revision la hicieron dos personas."),
    ("La persona designada como autor de correspondencia es el unico contacto y "
     "el responsable de comunicarse con el resto de los autores y de autorizar "
     "la version final de publicacion.",
     "D. Valdiviezo es el autor de correspondencia. ATENCION: esto le obliga a "
     "haber recabado la aprobacion de N. Trelles ANTES de firmar."),
    ("El articulo contiene material original e inedito, el trabajo de terceros "
     "esta citado, y las citas textuales, parafrasis y referencias estan "
     "identificadas en el texto.",
     "20 referencias en Vancouver, resueltas desde el .bib. Ninguna cita sin "
     "entrada. Ver tambien la declaracion de uso de IA del manuscrito, que no "
     "se retira."),
    ("El articulo no ha sido publicado anteriormente ni esta sometido a "
     "publicacion en otra revista.",
     "Cierto. El manuscrito preparado para Clinical Microbiology and Infection "
     "nunca se envio; sigue en el repositorio sin someter."),
    ("Se aceptan las condiciones de la Revista JSR en cuanto a normas, "
     "procedimientos, formato, edicion grafica, correccion y otros "
     "requerimientos que se solicitan en la convocatoria.",
     "OJO: el manuscrito incumple hoy cinco normas de formato de la revista. "
     "Estan listadas al final de esta hoja."),
]

INCUMPLE = [
    ("Margenes", "exige 3,0 cm en los cuatro lados", "el .docx lleva 2,54 cm"),
    ("Titulo", "exige MAYUSCULA SOSTENIDA, negrita, 18 pt",
     "va en minusculas y a 14 pt (las 19 palabras si caben en el maximo de 20)"),
    ("Resalte", "exige cursiva y prohibe la negrita para resaltar",
     "hay 112 fragmentos en negrita en el cuerpo"),
    ("Palabras clave", "exige orden alfabetico, en negrita y cursiva",
     "«farmacorresistencia» va detras de «Pseudomonas»; ni negrita ni cursiva"),
    ("Parrafos", "exige que no haya espacio entre parrafos consecutivos",
     "el estilo lleva 10 pt despues de cada uno"),
]

CUMPLE = [
    "A4", "Times New Roman 12", "una columna a doble espacio",
    "parrafos justificados", "resumen de 250 palabras, en el maximo",
    "cinco palabras clave, dentro del rango de tres a cinco",
    "decimales con coma", "millares con espacio fino",
    "figuras en PNG, ademas del PDF vectorial",
]

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass


def documento():
    d = docx.Document()
    s = d.sections[0]
    s.page_width, s.page_height = Mm(210), Mm(297)
    for lado in ("left_margin", "right_margin", "top_margin", "bottom_margin"):
        setattr(s, lado, Inches(0.9))
    n = d.styles["Normal"]
    n.font.name, n.font.size = TNR, Pt(11)
    n.paragraph_format.space_after = Pt(7)
    n.paragraph_format.line_spacing = 1.25
    cab = s.header.paragraphs[0]
    cab.text = ("Hoja de datos — NO es la carta. La carta se descarga de la revista "
                "y se firma a mano.")
    cab.runs[0].font.size, cab.runs[0].font.name = Pt(9), TNR
    cab.runs[0].italic = True
    return d


def h(d, txt, size=13, antes=14):
    p = d.add_paragraph()
    p.paragraph_format.space_before = Pt(antes)
    p.paragraph_format.space_after = Pt(5)
    escribe(p, txt, size=size, negrita=True)


def fila(d, etiqueta, valor, rojo=False):
    p = d.add_paragraph()
    p.paragraph_format.left_indent = Inches(0.3)
    p.paragraph_format.first_line_indent = Inches(-0.3)
    p.paragraph_format.space_after = Pt(4)
    r = p.add_run(etiqueta + "  ")
    r.font.name, r.font.size, r.bold = TNR, Pt(11), True
    r2 = p.add_run(valor)
    r2.font.name, r2.font.size = TNR, Pt(11)
    if rojo:
        r2.font.color.rgb = RGBColor(0xA0, 0x30, 0x20)


def main():
    if not JSR.exists():
        raise SystemExit("no encuentro %s" % JSR.name)
    lineas = JSR.read_text(encoding="utf-8").split("\n")
    titulo_es = next(l[2:].strip() for l in lineas if l.startswith("# "))
    titulo_es = titulo_es.replace("*", "")

    d = documento()
    p = d.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    escribe(p, "Datos para la carta de cesión de derechos de JSR", size=15, negrita=True)

    p = d.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    escribe(p, "Esta hoja **no es la carta**. La carta la provee la revista, se llama "
               "«Carta de originalidad y cesión de derechos» y se descarga de la sección "
               "«Archivos y formatos descargables» de %s. Su lista de comprobación avisa "
               "de que **no se inicia la revisión** si no llegan el artículo, esta carta y "
               "el formato de información de autores, en los formatos de ellos. Aquí está "
               "lo que va en cada hueco." % FORMULARIO, size=10.5)

    h(d, "Lo que hay que escribir en la carta")
    fila(d, "Lugar y fecha:", "Cuenca, Ecuador — dd/mm/aa el día que se firme")
    fila(d, "Nombre del artículo:", titulo_es)
    p = d.add_paragraph()
    p.paragraph_format.left_indent = Inches(0.3)
    escribe(p, "*(%d palabras, dentro del máximo de 20 que pide la revista. El binomio "
               "va en cursiva: Pseudomonas aeruginosa.)*" % len(titulo_es.split()), size=9.5)

    h(d, "Firma del Autor I", size=12, antes=12)
    fila(d, "Nombres y apellidos:", "Danny Valdiviezo")
    fila(d, "Documento de identidad:", "PENDIENTE — solo lo tiene él", rojo=True)
    fila(d, "Correo electrónico:", "dvchiqui@gmail.com")
    fila(d, "Número ORCID:", "PENDIENTE (opcional para la revista)", rojo=True)
    fila(d, "Filiación:", "Facultad de Medicina, Universidad Católica de Cuenca, "
                          "Cuenca, Ecuador")

    h(d, "Firma del Autor II", size=12, antes=12)
    fila(d, "Nombres y apellidos:", "Nataly Trelles")
    fila(d, "Documento de identidad:", "PENDIENTE", rojo=True)
    fila(d, "Correo electrónico:", "PENDIENTE", rojo=True)
    fila(d, "Número ORCID:", "PENDIENTE (opcional para la revista)", rojo=True)
    fila(d, "Filiación:", "Facultad de Medicina, Universidad Católica de Cuenca, "
                          "Cuenca, Ecuador")

    h(d, "Los ocho puntos que se firman, y cómo está cada uno")
    p = d.add_paragraph()
    escribe(p, "Copiados de la carta de la revista el 14 de septiembre de 2026, para "
               "comprobarlos antes de firmar. Quien firma responde por los ocho.", size=10)
    for i, (punto, estado) in enumerate(PUNTOS, 1):
        p = d.add_paragraph()
        p.paragraph_format.left_indent = Inches(0.35)
        p.paragraph_format.first_line_indent = Inches(-0.35)
        p.paragraph_format.space_after = Pt(2)
        escribe(p, "%d. %s" % (i, punto), size=10.5)
        q = d.add_paragraph()
        q.paragraph_format.left_indent = Inches(0.6)
        q.paragraph_format.space_after = Pt(7)
        r = q.add_run(estado)
        r.font.name, r.font.size, r.italic = TNR, Pt(10), True
        r.font.color.rgb = (RGBColor(0xA0, 0x30, 0x20)
                            if estado.startswith(("OJO", "ATENCION")) else
                            RGBColor(0x44, 0x44, 0x44))

    h(d, "El punto 8 no se puede firmar hoy sin reparos")
    p = d.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    escribe(p, "Firmar el punto 8 es aceptar las normas de formato de la revista. "
               "Leídas en su web el 14 de septiembre de 2026, el manuscrito **incumple "
               "cinco**:", size=10.5)
    for que, exige, hay in INCUMPLE:
        p = d.add_paragraph()
        p.paragraph_format.left_indent = Inches(0.35)
        p.paragraph_format.first_line_indent = Inches(-0.35)
        p.paragraph_format.space_after = Pt(3)
        escribe(p, "• **%s.** La norma %s; %s." % (que, exige, hay), size=10.5)
    p = d.add_paragraph()
    p.paragraph_format.space_before = Pt(8)
    escribe(p, "Cumple en cambio: %s." % ", ".join(CUMPLE), size=10.5)

    h(d, "Y lo que ninguna hoja resuelve")
    p = d.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    escribe(p, "El punto 5 dice que el autor de correspondencia es **responsable de "
               "autorizar la versión final**. D. Valdiviezo no puede firmarlo de buena fe "
               "mientras N. Trelles no haya aprobado por escrito esta versión. Es el mismo "
               "criterio ICMJE que el manuscrito lleva pendiente, y aquí pasa de ser una "
               "buena práctica a ser una declaración firmada.", size=10.5)

    DEST.mkdir(parents=True, exist_ok=True)
    salida = DEST / "datos_carta_cesion.docx"
    try:
        d.save(salida)
    except PermissionError:
        salida = DEST / "datos_carta_cesion_NUEVO.docx"
        d.save(salida)
        print("AVISO: estaba abierto en Word; escrito al lado como %s" % salida.name)
    print("escrito %s  (%d KB)" % (salida.relative_to(ROOT), salida.stat().st_size // 1024))
    print("  titulo leido del manuscrito: %d palabras" % len(titulo_es.split()))
    print("  %d normas de formato incumplidas" % len(INCUMPLE))


if __name__ == "__main__":
    main()
