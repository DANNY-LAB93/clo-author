"""Guía del material suplementario: qué contesta cada fichero del paquete.

POR QUÉ HACE FALTA

Un paquete de catorce anexos sin guía obliga al revisor a abrirlos uno por uno
para averiguar cuál responde a su duda. Este PDF es el mapa: para cada fichero
dice qué contiene, qué pregunta permite contestar y qué formato tiene, y agrupa
los anexos por la etapa de la revisión que documentan.

El inventario se lee del disco, no de una lista escrita a mano. Si un anexo
desaparece o cambia de tamaño, la guía lo refleja al reejecutar; y si aparece un
fichero que nadie ha descrito, la guía lo dice en lugar de callarlo.

Uso:
    python scripts/build_package_guide.py
"""
import csv
import pathlib
import sys

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.platypus import Paragraph, Spacer

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from build_manuscript_pdf import estilos, inline  # noqa: E402
from build_extraction_verifiables import ANCHO, SIN_CITAS, cuadro, documento  # noqa: E402

ROOT = pathlib.Path(__file__).resolve().parent.parent
OUT = ROOT / "verificables revisión sistemática"

# Qué es cada anexo y qué deja comprobar. El orden es el del paquete.
CATALOGO = [
    ("Manuscrito", [
        ("manuscrito_revision_sistematica.pdf", "Manuscrito maquetado en español, "
         "con las citas numeradas y la lista de referencias.",
         "El documento que se envía, en su forma final."),
        ("manuscript_systematic_review_en.pdf", "El mismo, en inglés.",
         "La versión para revistas de habla inglesa."),
        ("manuscrito_es.docx", "Manuscrito en Word, español.",
         "La versión editable, para las revistas que exigen .docx."),
        ("manuscript_en.docx", "Manuscrito en Word, inglés.",
         "Igual, en inglés."),
        ("S0_informe_editorial.docx", "Informe editorial: qué se decidió y cuándo.",
         "Si alguna decisión metodológica se tomó después de ver los resultados."),
    ]),
    ("Protocolo y reporte", [
        ("S1_lista_PRISMA_2020.docx", "Lista PRISMA 2020, ítem por ítem, con la "
         "página donde se cumple.", "Si el reporte cumple PRISMA sin buscarlo a mano."),
        ("S7_declaraciones_ICMJE.docx", "Autoría según CRediT, conflictos de interés, "
         "financiación y uso de IA.", "Quién hizo qué y con qué financiación."),
    ]),
    ("Búsqueda", [
        ("S2_estrategias_de_busqueda.docx", "La cadena de búsqueda literal de cada "
         "una de las nueve fuentes, con fecha y número de registros.",
         "Si la búsqueda es reproducible: se copia y se reejecuta."),
    ]),
    ("Cribado", [
        ("S3_decisiones_etapa2_titulo.csv", "Decisión de cribado por título para "
         "cada registro, con su motivo codificado.",
         "Por qué se excluyó cualquier registro concreto."),
        ("S3_decisiones_etapa3_resumen.csv", "Lo mismo en la lectura de resumen.",
         "Por qué un estudio no llegó a texto completo."),
        ("S6_auditoria_controles_positivos.docx", "Auditoría contra 40 estudios "
         "conocidos de antemano como elegibles, tras cada etapa.",
         "Si el cribado perdió estudios que debía capturar."),
    ]),
    ("Idioma", [
        ("S9_idioma_por_informe_y_clase_de_evidencia.csv", "Idioma de cada informe y "
         "clase de evidencia que aportaba.",
         "Qué se perdió al restringir a inglés y español."),
        ("S10_idioma_verificado_sobre_texto_completo.csv", "Verificación del idioma "
         "sobre el texto completo del PDF, no sobre los metadatos.",
         "Si la clasificación de idioma se comprobó o se dio por buena."),
    ]),
    ("Corpus y recuperación", [
        ("S5_listado_184_estudios.csv", "Los 184 estudios incluidos, con sus informes "
         "agrupados.", "Qué estudios componen el cuerpo de evidencia."),
        ("S8_recuperacion_texto_completo.csv", "Qué se intentó para conseguir cada "
         "texto completo y con qué resultado.",
         "Si el sesgo de recuperación se documentó o se ocultó."),
    ]),
    ("Extracción", [
        ("S4_pre_extraccion_desde_resumen.csv", "Pre-extracción desde el resumen, "
         "marcada como parcial en cada registro.",
         "De dónde salen las cifras de estructura del corpus."),
        ("S11_concordancia_entre_extractores.pdf", "Concordancia entre las dos "
         "extracciones independientes, variable a variable, antes de resolver nada.",
         "Cuánto coincidieron de verdad los dos revisores."),
        ("S12_resolucion_de_conflictos.pdf", "Cómo se trató cada desacuerdo: por "
         "regla, leyendo el artículo, o pendiente de conseguirlo.",
         "Si los desacuerdos se resolvieron o se taparon."),
        ("S13_reglas_de_extraccion_de_desenlaces.pdf", "Definición de erradicación "
         "microbiológica y de éxito clínico, con su corrección documentada.",
         "Si la definición de desenlace cambió, cuándo y por qué."),
    ]),
    ("Figuras y tablas", [
        ("figuras y tablas", "Figuras 1 y 2 en PDF vectorial, y las cuatro tablas "
         "del manuscrito en CSV.", "Los datos exactos que hay detrás de cada figura."),
    ]),
]

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass


def tamano(p):
    if p.is_dir():
        return f"{sum(1 for _ in p.iterdir())} ficheros"
    kb = p.stat().st_size / 1024
    if p.suffix == ".csv":
        try:
            n = sum(1 for _ in csv.reader(open(p, encoding="utf-8-sig"))) - 1
            return f"{n:,} filas".replace(",", " ")
        except Exception:
            pass
    return f"{kb:,.0f} KB".replace(",", " ")


def main():
    st = estilos()
    dest = OUT / "00_GUIA_DEL_MATERIAL_SUPLEMENTARIO.pdf"

    c = [Paragraph("Guía del material suplementario", st["titulo"])]
    c.append(Paragraph(
        "Fagoterapia en infecciones por <i>Pseudomonas aeruginosa</i> multirresistente: "
        "revisión sistemática de la estructura y la verificabilidad del cuerpo de "
        "evidencia clínica", st["autores"]))
    c.append(Spacer(1, 10))
    c.append(Paragraph(
        "Este paquete contiene el rastro completo de la revisión: qué se buscó, qué se "
        "excluyó y por qué, qué no se pudo conseguir, y en qué no coincidieron los dos "
        "revisores. Está ordenado por la etapa que documenta. Cada entrada dice qué "
        "contiene el fichero y qué pregunta permite contestar, para que no haga falta "
        "abrirlos todos.", st["cuerpo"]))
    c.append(Paragraph(
        "Los ficheros en <b>CSV</b> son datos, pensados para abrirse en una hoja de "
        "cálculo y filtrarse; los que están en <b>PDF</b> o <b>Word</b> son documentos "
        "para leer. Ningún dato de este paquete se transcribió a mano: todos salen del "
        "canal de código que produce también las cifras del manuscrito, y se regeneran "
        "reejecutándolo.", st["nota"]))

    descritos = set()
    for seccion, entradas in CATALOGO:
        filas = []
        for nombre, que_es, para_que in entradas:
            p = OUT / nombre
            descritos.add(nombre)
            if not p.exists():
                filas.append([f"<b>{nombre}</b>", "NO ENCONTRADO", "—", "—"])
                continue
            filas.append([nombre, que_es, para_que, tamano(p)])
        c.append(Paragraph(seccion, st["h1"]))
        c.append(cuadro(st, filas,
                        ["Fichero", "Qué contiene", "Qué permite comprobar", "Tamaño"],
                        [4.6 * cm, 4.6 * cm, ANCHO - 12.0 * cm, 2.8 * cm]))

    huerfanos = sorted(p.name for p in OUT.iterdir()
                       if p.name not in descritos
                       and not p.name.startswith("00_")
                       and p.suffix.lower() in (".csv", ".pdf", ".docx"))
    if huerfanos:
        c.append(Paragraph("Ficheros del paquete que esta guía no describe", st["h1"]))
        c.append(Paragraph(
            "Aparecen aquí para que la guía no dé por completo lo que no lo está: "
            + ", ".join(huerfanos) + ".", st["nota"]))

    c.append(Paragraph("Advertencia sobre el alcance de esta revisión", st["h1"]))
    c.append(Paragraph(
        "La extracción por duplicado <b>no ha concluido</b>. Este informe no presenta "
        "estimaciones de eficacia, ni riesgo de sesgo, ni certeza GRADE: presenta la "
        "estructura del cuerpo de evidencia y su completitud de reporte, que es lo que "
        "la pre-extracción sostiene. Los anexos S11 a S13 documentan el estado de la "
        "extracción en curso, incluidos los desacuerdos que siguen abiertos y los "
        "estudios cuyo texto completo no se ha conseguido. Se incluyen precisamente "
        "porque el estado real de una revisión en marcha es información que el lector "
        "necesita, y no algo que deba esperar a estar resuelto para poder auditarse.",
        st["cuerpo"]))

    documento(dest, "Guía del material suplementario").build(c)
    print(f"  {dest.name:52} {dest.stat().st_size // 1024} KB")
    if huerfanos:
        print(f"  aviso: {len(huerfanos)} ficheros sin describir -> {huerfanos}")


if __name__ == "__main__":
    main()
