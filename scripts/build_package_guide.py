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
import json
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

# La guia describia «los 90 juicios de riesgo de sesgo» con una cifra tecleada,
# y se volvio falsa el 2026-09-22 al salir EST-063 del corpus. Ahora entra por
# el escalar, como todo lo demas.
_S = json.loads((ROOT / "quality_reports" / "synthesis_scalars.json")
                .read_text(encoding="utf-8"))

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
         "una de las ocho fuentes, con fecha y número de registros.",
         "Si la búsqueda es reproducible: se copia y se reejecuta."),
    ]),
    ("Cribado", [
        ("S3_decisiones_etapa2_titulo.xlsx + .csv", "Decisión de cribado por título para "
         "cada registro, con su motivo codificado.",
         "Por qué se excluyó cualquier registro concreto."),
        ("S3_decisiones_etapa3_resumen.xlsx + .csv", "Lo mismo en la lectura de resumen.",
         "Por qué un estudio no llegó a texto completo."),
        ("S6_auditoria_controles_positivos.docx", "Auditoría contra 40 estudios "
         "conocidos de antemano como elegibles, tras cada etapa.",
         "Si el cribado perdió estudios que debía capturar."),
    ]),
    ("Idioma", [
        ("S9_idioma_por_informe_y_clase_de_evidencia.xlsx + .csv", "Idioma de cada informe y "
         "clase de evidencia que aportaba.",
         "Qué se perdió al restringir a inglés y español."),
        ("S10_idioma_verificado_sobre_texto_completo.xlsx + .csv", "Verificación del idioma "
         "sobre el texto completo del PDF, no sobre los metadatos.",
         "Si la clasificación de idioma se comprobó o se dio por buena."),
    ]),
    ("Corpus y recuperación", [
        ("S5_listado_*_estudios.xlsx + .csv", "Los estudios incluidos, con sus informes "
         "agrupados.", "Qué estudios componen el cuerpo de evidencia."),
        ("S16_excluidos_tras_leer_el_texto_completo.xlsx + .csv",
         "Los estudios que el cribado admitió y el texto completo desmintió, con "
         "su código de motivo y la frase del artículo que lo sostiene.",
         "Por qué salió cada uno, con la cita delante para poder discrepar (PRISMA 16b)."),
        ("S8_recuperacion_texto_completo.xlsx + .csv", "Qué se intentó para conseguir cada "
         "texto completo y con qué resultado.",
         "Si el sesgo de recuperación se documentó o se ocultó."),
        ("S20_de_que_informe_salio_cada_brazo.xlsx + .csv", "Cada brazo extraído con el "
         "informe del que salió, y con qué prueba se estableció el vínculo: el título "
         "localizado dentro del documento leído, el informe único del estudio o el único "
         "artículo del grupo.",
         "Dónde mirar para comprobar cualquier dato de cualquier brazo (PRISMA 10)."),
        ("S21_solapamiento_de_pacientes.xlsx + .csv", "Los pares de estudios que pueden "
         "describir a los mismos pacientes, con la señal que los marcó y la frase literal.",
         "Si el corpus cuenta a algún paciente dos veces, y cuál."),
    ]),
    ("Extracción", [
        ("S4_pre_extraccion_desde_resumen.xlsx + .csv", "Pre-extracción desde el resumen, "
         "marcada como parcial en cada registro.",
         "De dónde salen las cifras de estructura del corpus."),
        ("S22_completitud_resumen_frente_a_texto.xlsx + .csv", "Para cada variable de "
         "estratificación, cuántos estudios la declaran en el texto completo, cuántos la "
         "mencionan sin poder clasificarla, cuántos callan y de cuántos no hay texto.",
         "Separar la ausencia en el resumen de la ausencia en el estudio."),
        ("S17_tabla6_brazo_a_brazo.xlsx + .csv", "La Tabla 6 desglosada: los siete "
         "requisitos, brazo a brazo, con el primero que falla y por qué.",
         "Comprobar el embudo de agregabilidad sin fiarse del recuento."),
        ("S19_cribado_con_modelo_de_lenguaje.docx", "Qué modelo emitió las decisiones de "
         "cribado, cuándo, sobre qué ficheros, qué verificaron los autores y qué NO quedó "
         "registrado, marcado como dato faltante.",
         "Juzgar el procedimiento de cribado, incluido lo que no se puede reconstruir."),
        ("S18_evidencia_por_dominio.xlsx + .csv", "La frase del artículo en que se apoya "
         "cada uno de los %d juicios de riesgo de sesgo." % _S["celdas_tabla5"],
         "Discrepar de un juicio concreto teniendo delante lo que lo sostiene."),
        ("S11_concordancia_entre_extractores.pdf", "Concordancia entre las dos "
         "extracciones independientes, variable a variable, antes de resolver nada.",
         "Cuánto coincidieron de verdad los dos revisores."),
        ("S12_resolucion_de_conflictos.pdf", "Cómo se trató cada desacuerdo: por "
         "regla, leyendo el artículo, o pendiente de conseguirlo.",
         "Si los desacuerdos se resolvieron o se taparon."),
        ("S14_extraccion_adjudicada.csv", "La extracción definitiva: un valor por "
         "casilla, brazo a brazo, tras resolver los desacuerdos por consenso.",
         "Toda cifra de la sección 3.5 y de las tablas 5 y 6."),
        ("S15_procedencia_de_cada_casilla.csv", "Para cada casilla de S14, si la "
         "acordaron los dos revisores, la resolvieron por consenso, la escribió "
         "uno solo, o sigue abierta.",
         "Cuánta doble lectura hay detrás de cada cifra."),
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
    S = json.loads((ROOT / "quality_reports" / "synthesis_scalars.json")
                   .read_text(encoding="utf-8"))
    dest = OUT / "00_GUIA_DEL_MATERIAL_SUPLEMENTARIO.pdf"

    c = [Paragraph("Guía del material suplementario", st["titulo"])]
    c.append(Paragraph(
        "Fagoterapia en infecciones por <i>Pseudomonas aeruginosa</i> multirresistente: "
        "revisión sistemática de la literatura clínica y la completitud de su reporte",
        st["autores"]))
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
            # Un anexo de datos son DOS ficheros: el .xlsx que se lee y el .csv
            # reproducible. La entrada los nombra juntos, asi que hay que
            # resolver los dos y marcar los dos como descritos; si no, la
            # comprobacion de cobertura los da por huerfanos y la guia acaba
            # avisando de que no describe ficheros que si describe.
            partes = [x.strip() for x in nombre.split("+")]
            # Un anexo cuyo nombre lleva el recuento dentro --S5-- cambia de
            # nombre cada vez que cambia el corpus. Teclearlo aqui es la misma
            # trampa que el propio S5 evita calculandolo: se resuelve por
            # patron, y si no aparece ninguno la guia lo dira como NO ENCONTRADO.
            if "*" in partes[0]:
                hallados = sorted(OUT.glob(partes[0]))
                if hallados:
                    partes[0] = hallados[0].name
                    nombre = nombre.replace("S5_listado_*_estudios", hallados[0].stem)
            raiz = partes[0].rsplit(".", 1)[0]
            reales = []
            for x in partes:
                # "S3_algo.xlsx" ya es un nombre; ".csv" es solo la extension
                # del mismo anexo y hay que pegarla a la raiz.
                reales.append(x if not x.startswith(".") else raiz + x)
            for x in reales:
                descritos.add(x)
            faltan = [x for x in reales if not (OUT / x).exists()]
            if faltan:
                filas.append([f"<b>{nombre}</b>", "NO ENCONTRADO: %s" % ", ".join(faltan),
                              "—", "—"])
                continue
            tam = tamano(OUT / reales[0])
            filas.append([nombre, que_es, para_que, tam])
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
    # Lo que falta es la adjudicacion, no la extraccion. Decir «la extraccion no
    # ha concluido» era cierto hasta el 26 de agosto y dejo de serlo cuando la
    # segunda revisora entrego sus 122 estudios. Las dos cifras salen de los
    # escalares, para que la frase no pueda volver a quedarse vieja.
    c.append(Paragraph(
        "La extracción por duplicado <b>está completa</b>: %d de los %d estudios "
        "fueron extraídos por dos revisores de forma independiente. Lo que no ha "
        "concluido es la <b>adjudicación por consenso</b> de los desacuerdos: %d de "
        "los %d siguen sin firmar. Por eso este informe no presenta estimaciones de "
        "eficacia, ni riesgo de sesgo, ni certeza GRADE: presenta la estructura del "
        "cuerpo de evidencia y su completitud de reporte, que es lo que la "
        "pre-extracción sostiene, y ninguna cifra publicada depende de los cuadernos "
        "de extracción."
        % (S["extraccion_estudios_ambos"], S["extraccion_estudios_r1"],
           S["extraccion_conflictos_sin_firmar"], S["extraccion_desacuerdos"]),
        st["cuerpo"]))
    c.append(Paragraph(
        "Los anexos S11 a S13 documentan ese estado sin suavizarlo: cuánto "
        "coincidieron los dos revisores antes de resolver nada, dónde está hoy cada "
        "desacuerdo, y qué estudios no se pueden adjudicar todavía porque no se ha "
        "conseguido su texto completo. Se incluyen precisamente porque el estado real "
        "de una revisión en marcha es información que el lector necesita, y no algo "
        "que deba esperar a estar resuelto para poder auditarse.", st["cuerpo"]))

    documento(dest, "Guía del material suplementario").build(c)
    print(f"  {dest.name:52} {dest.stat().st_size // 1024} KB")
    if huerfanos:
        print(f"  aviso: {len(huerfanos)} ficheros sin describir -> {huerfanos}")


if __name__ == "__main__":
    main()
