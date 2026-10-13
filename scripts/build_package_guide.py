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
import re
import sys

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.platypus import Paragraph, Spacer

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from build_manuscript_pdf import estilos, inline  # noqa: E402
from build_extraction_verifiables import ANCHO, SIN_CITAS, cuadro, documento  # noqa: E402
# La misma cuenta de S16 que escribe la lista de anexos de los manuscritos: la
# guía y la lista no pueden describir el anexo con cifras distintas.
from build_lista_anexos import citas_s16  # noqa: E402

ROOT = pathlib.Path(__file__).resolve().parent.parent
OUT = ROOT / "verificables revisión sistemática"

# La guia describia «los 90 juicios de riesgo de sesgo» con una cifra tecleada,
# y se volvio falsa el 2026-09-22 al salir EST-063 del corpus. Ahora entra por
# el escalar, como todo lo demas.
_S = json.loads((ROOT / "quality_reports" / "synthesis_scalars.json")
                .read_text(encoding="utf-8"))
_S16 = citas_s16(_S)
# Desacuerdos de extracción que siguen sin adjudicar. Cambia la forma de varias
# frases, no solo una cifra: con 0 no se puede decir «no ha concluido».
_PENDIENTES = _S["extraccion_conflictos_sin_firmar"]


def _enumera(nums):
    """[1, 2] -> «1 y 2»; [1..7] -> «1 a 7»; si hay huecos, los enumera."""
    nums = sorted(nums)
    if len(nums) == 1:
        return "%d" % nums[0]
    if len(nums) > 2 and nums == list(range(nums[0], nums[-1] + 1)):
        return "%d a %d" % (nums[0], nums[-1])
    return ", ".join("%d" % n for n in nums[:-1]) + " y %d" % nums[-1]


def _figuras_y_tablas():
    """Qué hay de verdad en «figuras y tablas», leído del disco.

    Decía «las cuatro tablas del manuscrito» con la cifra tecleada, y la
    carpeta trae siete tablas numeradas y la de criterios: se quedó vieja en
    cuanto el manuscrito ganó tablas, sin que nada fallara."""
    d = OUT / "figuras y tablas"
    if not d.is_dir():
        return "Figuras y tablas del manuscrito."

    def numeros(patron, comodin):
        ms = (re.match(patron, p.name) for p in d.glob(comodin))
        return [int(m.group(1)) for m in ms if m]

    figs = numeros(r"figura_(\d+)_", "figura_*.pdf")
    tabs = numeros(r"tabla_(\d+)_", "tabla_*.csv")
    partes = []
    if figs:
        partes.append(("Figura %s" if len(figs) == 1 else "Figuras %s")
                      % _enumera(figs) + " en PDF vectorial")
    if tabs:
        partes.append(("la tabla %s" if len(tabs) == 1 else "las tablas %s")
                      % _enumera(tabs) + " del manuscrito en CSV")
    texto = ", y ".join(partes) if partes else "Figuras y tablas del manuscrito"
    if list(d.glob("tabla_criterios*.csv")):
        texto += ", más la tabla de criterios de elegibilidad"
    return texto[0].upper() + texto[1:] + "."


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
        # Decía «Informe editorial» sin decir quién lo escribió. Lo redactó el
        # modelo de lenguaje haciendo de editor de revista (docstring de
        # build_editorial_report.py), y así podía tomarse por la valoración de
        # una persona.
        ("S0_informe_editorial.docx", "Evaluación previa del manuscrito que "
         "redactó el modelo de lenguaje en el papel de un editor de revista; no "
         "es una evaluación editorial externa.",
         "Si alguna decisión metodológica se tomó después de ver los resultados."),
    ]),
    ("Protocolo y reporte", [
        ("S1_lista_PRISMA_2020.docx", "Lista PRISMA 2020, ítem por ítem, con la "
         "página donde se cumple.", "Si el reporte cumple PRISMA sin buscarlo a mano."),
        ("S7_declaraciones_ICMJE.docx", "Autoría según CRediT, conflictos de interés, "
         "financiación y uso de IA.", "Quién hizo qué y con qué financiación."),
    ]),
    ("Búsqueda", [
        # Prometía «con fecha» de cada búsqueda y no hay fecha por fuente: la
        # ejecución de Scopus cuya exportación entró al corpus no la tiene
        # registrada. «Ocho» iba además tecleado.
        ("S2_estrategias_de_busqueda.docx", "La cadena de búsqueda literal de cada "
         "una de las %d fuentes, con su número de registros."
         % _S["fuentes_distintas_n"],
         "Si la búsqueda es reproducible: se copia y se reejecuta."),
    ]),
    ("Cribado", [
        # «Con su motivo codificado» no vale para todas las filas: las del
        # primer día, y algunas de la etapa de resumen, van en texto libre. Y
        # no decía quién emitió las decisiones.
        ("S3_decisiones_etapa2_titulo.xlsx + .csv", "Decisión de cribado por título para "
         "cada registro, con su motivo y quién la emitió: el modelo de lenguaje, "
         "como revisor único.",
         "Por qué se excluyó cualquier registro concreto."),
        ("S3_decisiones_etapa3_resumen.xlsx + .csv", "Lo mismo en la lectura de resumen.",
         "Por qué un estudio no llegó a texto completo."),
        # Decía «40 estudios», tecleado: se fijaron 42 y la comprobación por
        # PMID alcanza a 40. Y no decía que el conjunto procede de una revisión
        # hecha con modelos de lenguaje ni que las ecuaciones se diseñaron para
        # recuperarlo, que es lo que limita lo que la auditoría puede afirmar.
        ("S6_auditoria_controles_positivos.docx", "Auditoría del cribado, tras "
         "cada etapa, contra los %d estudios fijados antes del cribado como "
         "elegibles conocidos, procedentes del metaanálisis exploratorio de julio "
         "de 2026, hecho con asistencia de modelos de lenguaje. La comprobación "
         "automática alcanza a los %d que tienen PMID."
         % (_S["controles_fijados"], _S["controles_comprobables_pmid"]),
         "Si el cribado perdió alguno de los controles comprobables. No mide la "
         "sensibilidad de la búsqueda: las ecuaciones se diseñaron para "
         "recuperarlos."),
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
        # Decía que todos llevan «la frase del artículo que lo sostiene» y que
        # «el texto completo desmintió» a todos. Los NOPDF salieron por no tener
        # el artículo, no porque el texto los desmintiera, y ni ellos ni los
        # NOREC tienen frase que citar.
        ("S16_excluidos_tras_leer_el_texto_completo.xlsx + .csv",
         "Los %d estudios que el cribado admitió y que salieron después, con su "
         "código de motivo y quién firmó la exclusión. %d llevan la cita en que "
         "se apoya; los %d sin el artículo completo (NOPDF) y los %d sin texto "
         "que se pudiera leer (NOREC) no tienen nada que citar%s"
         % (_S["estudios_excluidos_tras_texto_completo"], _S16["s16_con_cita"],
            _S["excluidos_texto_completo_NOPDF"],
            _S["excluidos_texto_completo_NOREC"],
            (", y %d más %s sin cita." % (_S16["s16_sin_cita_otros"],
                                          "van" if _S16["s16_sin_cita_otros"] > 1
                                          else "va"))
            if _S16["s16_sin_cita_otros"] else "."),
         "Por qué salió cada uno y, cuando hay cita, tenerla delante para poder "
         "discrepar (PRISMA 16b)."),
        ("S8_recuperacion_texto_completo.xlsx + .csv", "Qué se intentó para conseguir cada "
         "texto completo y con qué resultado.",
         "Si el sesgo de recuperación se documentó o se ocultó."),
        ("S20_de_que_informe_salio_cada_brazo.xlsx + .csv", "Cada brazo extraído con el "
         "informe del que salió, y con qué prueba se estableció el vínculo: el título "
         "localizado dentro del documento leído, el informe único del estudio o el único "
         "artículo del grupo.",
         "Dónde mirar para comprobar cualquier dato de cualquier brazo (PRISMA 10)."),
        ("S21_solapamiento_de_pacientes.xlsx + .csv", "Los %d pares de estudios que "
         "podían describir a los mismos pacientes, con la señal que los marcó, el "
         "veredicto tras leer los dos artículos, los pacientes compartidos y la frase "
         "firmada en que se apoya." % _S["pares_solapamiento_examinados"],
         "Si el corpus cuenta a algún paciente dos veces, y cuál."),
    ]),
    ("Extracción", [
        ("S4_pre_extraccion_desde_resumen.xlsx + .csv", "Pre-extracción desde el resumen, "
         "que emitió el modelo de lenguaje, marcada como parcial en cada registro.",
         "De dónde salen las cifras de estructura del corpus."),
        ("S22_completitud_resumen_frente_a_texto.xlsx + .csv", "Para cada variable de "
         "estratificación, cuántos estudios la declaran en el texto completo, cuántos la "
         "mencionan sin poder clasificarla, cuántos callan y de cuántos no hay texto.",
         "Separar la ausencia en el resumen de la ausencia en el estudio."),
        ("S23_clase_de_resistencia_comprobada.xlsx + .csv", "La clase de resistencia de "
         "los %d estudios que tenían texto completo, comprobada contra el antibiograma: la "
         "conclusión firmada, la frase o la tabla en que se apoya, cómo se codificó y qué "
         "cambió en la extracción." % _S["lectura_clase_estudios_leidos"],
         "Comprobar si un paciente es multirresistente sin fiarse de la etiqueta del autor."),
        ("S24_comparativos_reextraidos.xlsx + .csv", "Los %d estudios con diseño "
         "comparativo, reextraídos: comparador, asignación, tiempo cero, tiempo de "
         "evaluación, cointervenciones, pérdidas, estimando y si hay un contraste para "
         "P. aeruginosa." % _S["comparativos_reextraidos_leidos"],
         "Ver qué comparan de verdad los estudios que se llaman comparativos."),
        ("S17_tabla6_brazo_a_brazo.xlsx + .csv", "La Tabla 6 desglosada: los siete "
         "requisitos, brazo a brazo, con el primero que falla y por qué.",
         "Comprobar el embudo de agregabilidad sin fiarse del recuento."),
        # «Qué verificaron los autores» repartía entre los dos un examen que,
        # según declara D.V. (8 de octubre de 2026), hizo D.V. y que no quedó
        # registrado.
        ("S19_cribado_con_modelo_de_lenguaje.docx", "Qué modelo emitió las decisiones de "
         "cribado, cuándo, sobre qué ficheros, qué examinó D.V., según su declaración, "
         "y qué no quedó registrado, marcado como dato faltante.",
         "Juzgar el procedimiento de cribado, incluido lo que no se puede reconstruir."),
        # Nombraba «S18_evidencia_por_dominio», que no existe: la guía lo daba
        # por NO ENCONTRADO y listaba el S18 real como fichero sin describir.
        # Decía además que cada juicio tiene «la frase del artículo en que se
        # apoya», y en algunos el cuaderno no registra apoyo alguno.
        ("S18_cada_juicio_con_su_frase.xlsx + .csv", "Cada uno de los %d juicios "
         "de riesgo de sesgo, con lo que lo sostiene en el cuaderno firmado: una "
         "cita literal en %d, una nota sin cita en %d y nada en %d, marcados como "
         "dato faltante."
         % (_S["celdas_tabla5"], _S["citas_literales"], _S["notas_del_revisor"],
            _S["juicios_sin_frase"]),
         "Discrepar de un juicio concreto teniendo delante lo que lo sostiene, o "
         "ver que no consta nada."),
        # S18b no estaba descrito: salía como fichero huérfano.
        ("S18b_frases_cosechadas_por_tema.xlsx + .csv", "Las frases de cada "
         "artículo que el modelo de lenguaje localizó de forma automática para "
         "cada dominio de riesgo de sesgo, y que puso como comentario en las "
         "casillas de los formularios.",
         "Qué tenían delante los revisores al juzgar cada dominio. Acompañan a "
         "los juicios; lo que sostiene cada uno está en S18."),
        # Decía «en todas las filas», sin cifra: son las filas comparables, y el
        # recuento sale del escalar.
        ("S11_concordancia_entre_extractores.pdf", "Concordancia entre las dos "
         "extracciones, variable a variable, antes de resolver nada. Su "
         "independencia no está acreditada: una columna de texto libre coincide "
         "carácter por carácter entre los dos cuadernos en %d de las %d filas "
         "comparables, erratas incluidas."
         % (_S["extraccion_localizacion_identicas"],
            _S["extraccion_localizacion_comparables"]),
         "Cuánto coinciden los dos cuadernos, y por qué no mide dos lecturas "
         "independientes."),
        # Hablaba de desacuerdos «pendientes de conseguirlo» cuando ya no queda
        # ninguno, y no decía quién adjudicó. «Según el registro»: lo comprobado
        # es el responsable que anota resuelto_por, no cómo se tomó la decisión.
        ("S12_resolucion_de_conflictos.pdf", "Cómo se cerraron los %d "
         "desacuerdos: adjudicados, según el registro, por los dos revisores (%d) "
         "o por uno solo (%d), o cerrados por una regla mecánica, sin firma "
         "conjunta (%d)%s"
         % (_S["extraccion_desacuerdos"], _S["conflictos_resueltos_por_los_dos"],
            _S["conflictos_resueltos_por_uno"], _S["extraccion_cerrados_por_regla"],
            "; %d siguen sin adjudicar." % _PENDIENTES if _PENDIENTES else "."),
         "Si los desacuerdos se adjudicaron o se taparon, y quién los adjudicó "
         "según el registro."),
        # «Tras resolver los desacuerdos por consenso» y «la resolvieron por
        # consenso» eran falsos: el registro anota a los dos revisores solo en
        # una parte de los desacuerdos y a uno solo en el resto. Las etiquetas
        # son las de S15 tras separar quién adjudicó.
        ("S14_extraccion_adjudicada.csv", "La extracción definitiva: un valor por "
         "casilla, brazo a brazo, tras la adjudicación de los desacuerdos.",
         "Toda cifra de la sección 3.5 y de las tablas 5 y 6."),
        ("S15_procedencia_de_cada_casilla.csv", "Para cada casilla de S14, de "
         "dónde sale su valor: acuerdo, adjudicada por los dos, adjudicada por "
         "uno, corregida contra el texto, una sola lectura o abierta.",
         "Cuánta doble lectura hay detrás de cada cifra, y cuántas casillas "
         "adjudicó, según el registro, una sola persona."),
        ("S13_reglas_de_extraccion_de_desenlaces.pdf", "Definición de erradicación "
         "microbiológica y de éxito clínico, con su corrección documentada.",
         "Si la definición de desenlace cambió, cuándo y por qué."),
    ]),
    ("Figuras y tablas", [
        ("figuras y tablas", _figuras_y_tablas(),
         "Los datos exactos que hay detrás de cada figura y de cada tabla."),
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
    # Decía «el rastro completo», y no lo es: S19 señala lo que no quedó
    # registrado (el examen que declara D.V. de lo que superó el cribado).
    c.append(Paragraph(
        "Este paquete contiene el rastro registrado de la revisión: qué se buscó, qué "
        "se excluyó y por qué, qué no se pudo conseguir, y en qué no coincidieron los "
        "dos revisores; lo que no quedó registrado se señala como tal (S19). Está "
        "ordenado por la etapa que documenta. Cada entrada dice qué contiene el "
        "fichero y qué pregunta permite contestar, para que no haga falta abrirlos "
        "todos.", st["cuerpo"]))
    # Decía «ningún dato se transcribió a mano», y la extracción y los juicios
    # de riesgo de sesgo los emitieron los autores en sus cuadernos (así lo dice
    # la declaración de uso de IA). Y no decía quién escribió el canal. La
    # versión siguiente, «Ninguna cifra de este paquete se copió a mano», seguía
    # sin sostenerse: los valores de los cuadernos de extracción (pacientes,
    # éxitos, eventos) son cifras que se pasaron a mano desde los artículos. Lo
    # que no se teclea son los recuentos y porcentajes que el canal calcula.
    c.append(Paragraph(
        "Los ficheros en <b>CSV</b> son datos, pensados para abrirse en una hoja de "
        "cálculo y filtrarse; los que están en <b>PDF</b> o <b>Word</b> son documentos "
        "para leer. Ningún recuento ni porcentaje de este paquete se tecleó al "
        "escribirlo: los calcula, a partir de los registros de decisión y de los "
        "cuadernos de extracción y de riesgo de sesgo, el canal de código que "
        "escribió y ejecutó el modelo de lenguaje, el mismo que produce las cifras "
        "del manuscrito, y se regeneran reejecutándolo.", st["nota"]))

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
    # DECÍA «Lo que no ha concluido es la adjudicación por consenso de los
    # desacuerdos: 0 de los 541 siguen sin firmar. Por eso este informe no
    # presenta estimaciones de eficacia, ni riesgo de sesgo, ni certeza GRADE
    # [...] y ninguna cifra publicada depende de los cuadernos de extracción».
    # Era falso entero: con 0 pendientes la adjudicación SÍ ha concluido; no fue
    # «por consenso» (el registro anota a los dos revisores solo en una parte y
    # a uno solo en el resto); el manuscrito SÍ presenta riesgo de sesgo (sección
    # 3.7, tabla 7), y la sección 3.5 y las tablas 5 y 6 salen de la extracción
    # adjudicada, que es la fusión de los dos cuadernos. Ahora hay dos
    # redacciones, según queden o no desacuerdos sin adjudicar, y todas las
    # cifras salen de los escalares. Del riesgo de sesgo, lo que sale de la
    # extracción adjudicada es el DISEÑO que decide qué estudios se evalúan
    # (make_rob_forms.py lee study_design de extraccion_adjudicada.csv); los
    # juicios se emitieron en cuadernos propios (sección 2.7), y así se dice:
    # escribir que «salen de la extracción» sería atribuirles otro origen.
    e = {"ambos": S["extraccion_estudios_ambos"], "r1": S["extraccion_estudios_r1"],
         "loc_id": S["extraccion_localizacion_identicas"],
         "loc_comp": S["extraccion_localizacion_comparables"],
         "desac": S["extraccion_desacuerdos"],
         "adj": S["extraccion_conflictos_firmados"],
         "dos": S["conflictos_resueltos_por_los_dos"],
         "uno": S["conflictos_resueltos_por_uno"],
         "regla": S["extraccion_cerrados_por_regla"],
         "pend": S["extraccion_conflictos_sin_firmar"],
         "rob": S["celdas_tabla5"], "ev": S["rob_estudios_evaluables"],
         "rob2": S["rob_estudios_con_dos_lecturas"],
         "rob1": S["rob_estudios_con_una_lectura"],
         "rob_des": S["rob_desacuerdos"], "rob_dv": S["rob_resueltos_hacia_r1"]}
    # Si las partes no suman el todo, la advertencia diría algo que no cuadra.
    # Mejor no escribirla.
    if (e["adj"] + e["regla"] + e["pend"] != e["desac"]
            or e["dos"] + e["uno"] != e["adj"]
            or e["rob2"] + e["rob1"] != e["ev"]):
        raise SystemExit("NO SE ESCRIBE LA GUÍA: los escalares de adjudicación o "
                         "de riesgo de sesgo no suman: %r" % e)
    indep = ("sin independencia acreditada: la columna de texto libre que localiza "
             "cada dato coincide carácter por carácter entre los dos cuadernos en "
             "%(loc_id)d de las %(loc_comp)d filas comparables (S11)" % e)
    if e["pend"]:
        p1 = ("La extracción por duplicado <b>está completa</b>: los dos revisores "
              "extrajeron %(ambos)d de los %(r1)d estudios, " % e + indep
              + ". Lo que <b>no ha concluido</b> es la adjudicación de los "
              "desacuerdos: de los %(desac)d, %(pend)d siguen sin adjudicar, y esas "
              "casillas salen vacías de la extracción adjudicada (S14) y figuran "
              "como abiertas en S15; no se rellenan con una conjetura. De los "
              "%(adj)d adjudicados, el registro anota a los dos revisores en "
              "%(dos)d, los únicos que constan como consenso, y a uno solo en "
              "%(uno)d; %(regla)d se cerraron por una regla mecánica, sin firma "
              "conjunta (S12)." % e)
    else:
        p1 = ("La extracción por duplicado y la adjudicación de sus desacuerdos "
              "<b>están cerradas</b>. Los dos revisores extrajeron %(ambos)d de los "
              "%(r1)d estudios, " % e + indep
              + ". De los %(desac)d desacuerdos, %(adj)d están adjudicados: el "
              "registro anota a los dos revisores en %(dos)d, los únicos que "
              "constan como consenso, y a uno solo en %(uno)d. Los %(regla)d "
              "restantes se cerraron por una regla mecánica, sin firma conjunta "
              "(S12)." % e)
    c.append(Paragraph(p1, st["cuerpo"]))
    una = ("" if not e["rob1"] else
           " El estudio restante tiene una sola lectura." if e["rob1"] == 1 else
           " Los %(rob1)d restantes tienen una sola lectura." % e)
    c.append(Paragraph(
        "De esa extracción adjudicada (S14) salen la sección 3.5 y las tablas 5 y 6 "
        "del manuscrito, y el diseño que decide qué estudios se evalúan en riesgo de "
        "sesgo%s. Los %d juicios de riesgo de sesgo de la sección 3.7 y la tabla 7 "
        "(S18) se emitieron en cuadernos aparte: en %d de los %d estudios "
        "evaluables hubo dos, uno a nombre de cada autor, cuya independencia "
        "tampoco está acreditada, y se cerraron en un cuaderno de consenso que el "
        "modelo de lenguaje generó con los juicios coincidentes precargados y que "
        "firmaron los dos autores; de los %d juicios en que los dos cuadernos "
        "discrepaban, %s se resolvieron hacia el de D.V.%s"
        % (", de modo que esas cifras pueden cambiar cuando se adjudique lo "
           "pendiente" if e["pend"] else "",
           e["rob"], e["rob2"], e["ev"], e["rob_des"],
           "los %d" % e["rob_dv"] if e["rob_dv"] == e["rob_des"] else
           "%d" % e["rob_dv"], una),
        st["cuerpo"]))
    c.append(Paragraph(
        "GRADE no se aplica: califica la certeza de una estimación agrupada, y el "
        "manuscrito no presenta ninguna (sección 3.6).", st["cuerpo"]))
    # Decía que S11 a S13 muestran «qué estudios no se pueden adjudicar todavía
    # porque no se ha conseguido su texto completo»: hoy no queda ninguno.
    c.append(Paragraph(
        "Los anexos S11 a S15 documentan ese proceso sin suavizarlo: cuánto "
        "coincidían los dos cuadernos antes de resolver nada y por qué esa "
        "concordancia no mide dos lecturas independientes (S11), cómo se cerraron "
        "los desacuerdos%s (S12), las reglas de desenlace (S13), el valor final "
        "de cada casilla (S14) y de dónde sale (S15).%s"
        % ((", quién los adjudicó según el registro y cuáles siguen sin adjudicar",
            " Se incluyen porque el estado real de una adjudicación en marcha es "
            "información que el lector necesita, y no algo que deba esperar a "
            "estar resuelto para poder auditarse.")
           if e["pend"] else (" y quién los adjudicó según el registro", "")),
        st["cuerpo"]))

    documento(dest, "Guía del material suplementario").build(c)
    print(f"  {dest.name:52} {dest.stat().st_size // 1024} KB")
    if huerfanos:
        print(f"  aviso: {len(huerfanos)} ficheros sin describir -> {huerfanos}")


if __name__ == "__main__":
    main()
