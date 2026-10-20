"""Convierte los anexos del paquete en cuadernos que un revisor pueda leer.

EL PROBLEMA

Los anexos se exportan como CSV con los nombres internos del canal:
`record_id`, `verdict`, `decided_by`, `pathogen_scope`, `extraction_status`. Un
revisor que abre S3 encuentra 13 917 filas de `EXCLUDE` y `ADVANCE` sin saber
qué es una fila, cuántas debería haber, ni qué significa la columna. El fichero
es correcto y no comunica nada.

QUE HACE

Por cada CSV del paquete escribe un .xlsx con dos hojas:

  «Léeme»       qué es este anexo, cuántas filas tiene, qué significa cada
                columna, y a qué sección del manuscrito corresponde
  los datos     con las cabeceras en castellano, los códigos traducidos, la
                primera fila congelada y filtros puestos

QUE NO HACE

No toca los CSV. Se conservan tal cual, con sus nombres internos, porque son la
copia reproducible: quien quiera reejecutar el canal necesita las claves que el
canal usa, no una traducción. El .xlsx es para leer; el .csv es para verificar.
Un paquete que solo trae la versión bonita pierde la trazabilidad, y uno que
solo trae la cruda no la comunica.

Uso:
    python scripts/build_readable_annexes.py
"""
import collections
import csv
import datetime
import json
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
# Lo que las Léeme dicen con cifras, fechas o números de tabla y de sección se
# lee de donde ya se calcula (escalares, manuscritos, generadores), no se
# teclea.
from build_lista_anexos import (ES, EXCLUSIONES, REVISTA, _pies,  # noqa: E402
                                citas_s16, de_las_citadas)
from build_lista_anexos import numeracion as numeracion_manuscritos  # noqa: E402
from build_verifiables_package import (ETIQUETA_ASISTIDA, fecha_es,  # noqa: E402
                                       fechas_es, nota_etiqueta_asistida,
                                       primera_pasada)
from extraction_schema import ETIQUETAS as ETIQUETAS_EXTRACCION  # noqa: E402
import ingest_lectura_firmada as ILF  # noqa: E402

PAQ = ROOT / "verificables revisión sistemática"
SCALARS = ROOT / "quality_reports" / "synthesis_scalars.json"
csv.field_size_limit(200_000_000)
try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

# Qué es cada anexo, en una frase que un revisor entienda sin abrir el fichero.
QUE_ES = {
    # Decian «Toda decision de cribado»: S3 lleva solo el cribado vigente (el
    # del pozo), no la primera pasada del 4-ago ni la fila que corrigio en ella
    # la exclusion de Ronit 2024. Tampoco decian quien emitio las decisiones,
    # ni que 77 filas de la etapa 3 llevan la fecha de su copia y la etiqueta
    # «pending human verification». Lo que va entre llaves lo cuenta
    # complementos() sobre el CSV y sobre primera_pasada().
    "S3_decisiones_etapa2_titulo": (
        "Cada decisión del cribado vigente por TÍTULO, una por fila, con su motivo y "
        "su marca de tiempo. Las emitió todas el modelo de lenguaje (Claude Opus 5) "
        "como revisor único, sin duplicación; «Quién decidió» lo dice fila a fila. "
        "{primera_pasada}",
        "Sección 2.4. El registro es solo-anexar: una corrección es una fila nueva y ambas permanecen."),
    "S3_decisiones_etapa3_resumen": (
        "Cada decisión del cribado vigente por RESUMEN, una por fila, con su motivo y "
        "su marca de tiempo. Las emitió todas el modelo de lenguaje (Claude Opus 5) "
        "como revisor único, sin duplicación; «Quién decidió» lo dice fila a fila. "
        "{heredadas} {primera_pasada}",
        "Sección 2.4. Solo llegan aquí los registros que superaron el cribado por título."),
    # Decia «la fuente de TODA cifra que el artículo publica» y no decia quien
    # la emitio. Las dos cosas eran falsas o faltaban: la emitio el modelo, y
    # la sección 3.5 y la tabla 5 salen de la extraccion adjudicada (S14), no
    # de aqui.
    "S4_pre_extraccion_desde_resumen": (
        "La pre-extracción desde el resumen, emitida por el modelo de lenguaje "
        "(Claude Opus 5); fuente de las cifras estructurales (secciones 3.1 a 3.4).",
        "Sección 2.6. Cada fila va marcada PARCIAL: describe lo que el resumen declara, no el texto completo. "
        "Los desenlaces (sección 3.5, tabla 5) salen de la extracción adjudicada, S14."),
    # La clave llevaba el recuento de un corpus viejo y no casaba con el
    # fichero: S5 salia con la Léeme generica. Ahora se busca sin recuento.
    "S5_listado": (
        "Los estudios del corpus tras agrupar los informes, con su situación y si se obtuvo el texto completo.",
        "Sección 3.1. La unidad es el estudio, no el informe: un mismo estudio puede tener varios informes."),
    # Decia «Cómo se localizó cada texto completo, o por qué no se pudo» y
    # «Explica el sesgo de recuperación que el artículo mide». S8 no es eso: es
    # la vía resuelta de los informes sin DOI editorial (fulltext_identifiers),
    # y desde NOPDF (2026-10-06) la recuperación es del 100 % por construcción.
    # Se alinea con la descripción del índice (build_editorial_report).
    "S8_recuperacion_texto_completo": (
        "La vía de recuperación resuelta para cada informe sin DOI editorial "
        "(resúmenes de congreso, fichas de registro y algunos artículos): el "
        "identificador que se resolvió y cómo. No es el registro de los intentos "
        "de obtener cada texto completo.",
        "Sección 3.2."),
    "S9_idioma_por_informe_y_clase_de_evidencia": (
        "El idioma de cada informe y de dónde se determinó, informe a informe.",
        "Sección 2.9. Sostiene la enmienda de idioma y su impacto medido."),
    "S10_idioma_verificado_sobre_texto_completo": (
        "El idioma comprobado sobre el PDF, no sobre lo que declaraba la base de datos.",
        "Sección 2.9. El nombre de la revista no determina el idioma del artículo."),
    # No decia quien firmo cada veredicto, y S21 no tenia columna de firma: 2
    # de los pares los descarto la lectura del modelo y no constan firmados.
    # Desde el 2026-10-19 audita_pendientes.py escribe «firmado_por» y
    # «fecha», y la Léeme las cuenta (complementos()).
    "S21_solapamiento_de_pacientes": (
        "Cada par de estudios que podía describir a los mismos pacientes, con el veredicto "
        "tras leer los dos artículos y los pacientes que comparten, una clave por persona. "
        "En «Señal que lo marcó», «NO lo marco el detector» quiere decir que el par "
        "lo encontró una lectura, y la etiqueta dice cuál: la del modelo de lenguaje "
        "o la relectura de los autores, con su fecha.{s21_firmas}",
        # Decia «limitación séptima»: al añadir la limitación del cribado por
        # el modelo pasó a ser la octava en el maestro, y en el manuscrito de
        # la revista es otra. Se remite por su asunto, sin ordinal.
        "Sección 4.4, en la limitación sobre pacientes descritos en más de un "
        "estudio. Un paciente que sale en tres pares tiene la misma "
        "clave en los tres y se cuenta una vez."),
    # S23 y S24 no decian quien codifico: los dos autores firmaron la
    # conclusion en texto libre y el valor categorico lo derivo el modelo
    # (ingest_lectura_firmada.py). Las columnas que nombran son las de ETIQUETA.
    "S23_clase_de_resistencia_comprobada": (
        "La clase de resistencia de cada estudio con texto completo, comprobada contra el "
        "antibiograma del artículo, con la conclusión firmada por los dos autores en la "
        "relectura del {relectura_fecha}. Lo firmado es el texto libre de «Clase "
        "verificada (texto firmado)» y «Criterio o antibiograma (texto firmado)». Las "
        "columnas «Verificación», «Clase verificada», «Relación con la clase "
        "declarada», «Qué cambia en la extracción» y «Queda abierto» las derivó de ese "
        "texto el modelo de lenguaje ({ingest}), y su rótulo lo dice: «(lo codificó "
        "el modelo)».",
        "Sección 3.4. «Queda abierto» dice lo que la lectura no resolvió y no se "
        "cambió en la extracción."),
    "S24_comparativos_reextraidos": (
        "Los estudios con diseño comparativo, reextraídos: qué comparan, desde cuándo, "
        "hasta cuándo y si hay un contraste para P. aeruginosa.",
        "Sección 3.7. «Grupo sin fago» y «Contraste para P. aeruginosa» los derivó el "
        "modelo de lenguaje ({ingest}) del texto que los dos autores firmaron en la "
        "relectura del {relectura_fecha} y que va al lado: lo firmado es ese texto, no "
        "su codificación."),
    # S15 y S18b salian con el texto por defecto, «Anexo del material
    # suplementario.», y en S15 nadie explicaba las etiquetas: el lector tenia
    # que adivinar que «consenso» (la etiqueta de entonces) cubria tambien
    # casillas que el registro atribuye a un unico responsable.
    "S15_procedencia_de_cada_casilla": (
        "De dónde salió cada casilla de la extracción adjudicada (S14): el mismo "
        "cuadro, una fila por brazo y una columna por variable, con la etiqueta de "
        "procedencia en lugar del valor.{fuera_del_corpus}",
        # Decia que «con doble lectura» contaba tambien las «corregidas con dos
        # firmas». No es el calculo: build_outcome_scalars.DOBLE cuenta acuerdo
        # y las tres «adjudicada ...», y ninguna corregida. main() lo comprueba
        # contra DOBLE antes de escribirlo (DOBLE_DE_LA_TABLA, abajo).
        "Sección 2.6 y tabla 5, cuyo «con doble lectura» cuenta las casillas con "
        "acuerdo o adjudicadas, por uno o por los dos; las corregidas contra el "
        "texto no cuentan, tampoco las de dos firmas. Cada etiqueta se explica "
        "abajo."),
    "S18b_frases_cosechadas_por_tema": (
        "Las frases de cada artículo que el modelo de lenguaje (Claude Opus 5) "
        "localizó de forma automática, buscando expresiones, para cada dominio o "
        "tema de riesgo de sesgo, y que puso como comentario en las casillas de los "
        "formularios. Sirven para buscar en el artículo, no para sostener un juicio.",
        "Sección 2.7. Lo que sostiene cada juicio está en S18. Un tema sin frases "
        "quiere decir que el buscador no encontró la expresión, no que el artículo "
        "no trate el asunto."),
    # S14, S16, S17, S18, S20 y S22 salian con la plantilla vacía («Anexo del
    # material suplementario.» y un «Dónde se usa» en blanco). Lo que dicen
    # sale de la guía y del índice (build_package_guide, build_editorial_report);
    # los números de sección y de tabla se leen de los manuscritos (numeros()) y
    # las cifras, de los escalares o del propio CSV (complementos()).
    "S14_extraccion_adjudicada": (
        "La extracción definitiva: un valor por casilla, brazo a brazo, tras la "
        "adjudicación de los desacuerdos entre las dos extracciones, cuya "
        "independencia no está acreditada (S11). De dónde sale cada valor (acuerdo, "
        "adjudicada por los dos o por uno, corregida contra el texto, una sola "
        "lectura o abierta) está en S15, que tiene la misma forma.{fuera_del_corpus}",
        "Sostiene la sección {sec_desenlaces} (tabla {tab_desenlaces}) y el embudo "
        "de agregabilidad (sección {sec_embudo}, tabla {tab_embudo})."),
    "S16_excluidos_en_la_fase_de_texto_completo": (
        "Los estudios que el cribado admitió y que salieron después, en la fase de "
        "texto completo: uno por fila, con su código de motivo y lo que significa, "
        "la cita en que se apoya cuando la hay, quién decidió la exclusión y cuándo. "
        "El modelo de lenguaje leyó los textos completos y las fichas de registro y "
        "propuso, con su cita, las exclusiones que se apoyan en los textos que leyó. "
        "En «Quién decidió», {s16_dos} llevan la firma de los dos autores, "
        "{s16_solo} la de D.V. solo y {s16_orden} se registraron por orden de D.V., "
        "sin que conste la firma de N.T. Los NOPDF salieron por no tener el artículo "
        "completo, no porque se comprobara que incumplen los criterios; ni ellos ni "
        "los NOREC tienen nada que citar{s16_sin_cita}.{s16_citadas}",
        "Sección {sec_exclusiones} y Figura 1 (PRISMA 2020, ítem 16b)."),
    "S17_tabla6_brazo_a_brazo": (
        "La tabla del embudo de agregabilidad desglosada brazo a brazo: si cada brazo "
        "cumple cada requisito de una proporción agrupada de éxito clínico («cumple», "
        "«no cumple» o «no evaluable»), el primero que falla y por qué. La calcula "
        "el canal (build_tabla6_brazos.py) sobre la extracción adjudicada (S14), con "
        "las reglas del embudo, y se detiene si sus recuentos no coinciden con los "
        "publicados. «¿Texto completo obtenido?» no es uno de los requisitos.",
        "Sección {sec_embudo}, tabla {tab_embudo}."),
    "S18_cada_juicio_con_su_frase": (
        "Cada juicio de riesgo de sesgo, uno por fila, con lo que lo sostiene en el "
        "cuaderno firmado (una cita literal, una nota sin cita o nada, marcado como "
        "dato faltante), el cuaderno de que sale («Fuente documental»), quién lo "
        "firmó y cuándo. Los del cuaderno de consenso parten de dos cuadernos, uno a "
        "nombre de cada autor, sin independencia acreditada; el canal generó el de "
        "consenso con los juicios coincidentes ya escritos y los discrepantes en "
        "blanco. Las frases que el modelo de lenguaje localizó de forma automática y "
        "puso como comentario en los formularios están en S18b: acompañan a lo que "
        "sostiene cada juicio, no lo sustituyen.",
        "Secciones {sec_rob_metodos} y {sec_riesgo}, tabla {tab_riesgo}."),
    "S20_de_que_informe_salio_cada_brazo": (
        "De qué informe salió cada brazo extraído y con qué prueba se estableció el "
        "vínculo ({s20_vias}); «Evidencia» guarda la frase que lo demuestra. Lo "
        "establece el canal (build_brazo_informe.py), que no afirma de qué página "
        "sale cada casilla: eso es «¿Dónde viste estos datos?», el texto libre de la "
        "extracción, recortado.",
        "Sección {sec_extraccion}. Dónde mirar para comprobar cualquier dato de "
        "cualquier brazo (PRISMA 2020, ítem 10a)."),
    "S22_completitud_resumen_frente_a_texto": (
        "Para cada variable de estratificación, cuántos estudios la declaran en el "
        "texto completo, cuántos la mencionan sin poder clasificarla, cuántos callan "
        "y de cuántos no hay texto, y en cuántos el resumen no permite asignarla: "
        "separa el silencio del resumen del silencio del artículo. En «No asignable "
        "en el resumen» cuenta tanto el resumen sin valor como el que la deja como no "
        "clasificable. Lo calcula el canal (build_tabla3_completitud.py) sobre la "
        "pre-extracción desde el resumen (S4) y la extracción adjudicada (S14).",
        "Sección {sec_no_declara}. Las columnas del texto completo son las de la "
        "tabla {tab_completitud}; la columna del resumen de esa tabla se calcula "
        "aparte, sobre S4."),
}

# Lo que significa cada etiqueta de un anexo cuyas casillas son etiquetas y no
# datos. El recuento de cada una se cuenta en el propio CSV al escribir el
# Léeme, no se teclea. Si el CSV trae una etiqueta que no esta aqui, el guion
# se para: un Léeme que no explica una de sus etiquetas es justo el defecto
# que esto corrige.
ETIQUETAS_DE = {
    # Las tres «adjudicada ...» eran una sola, «consenso», hasta el 2026-10-08
    # (build_adjudicated_dataset.py). La columna resuelto_por del registro de
    # adjudicacion anota a los dos revisores en pocas filas y un unico
    # responsable en el resto; la etiqueta dice lo que anota, no mas.
    "S15_procedencia_de_cada_casilla": [
        ("acuerdo", "Los dos revisores escribieron el mismo valor, una vez "
                    "normalizado el vocabulario."),
        # «Solo estas constan como consenso» chocaba con la etiqueta
        # «corregido por consenso contra el texto» de la misma hoja; esa
        # etiqueta es ahora «corregido contra el texto (dos firmas)», y la
        # frase se acota a las adjudicadas: una casilla adjudicada por los dos
        # que despues se corrigio lleva la etiqueta de la correccion.
        ("adjudicada por los dos",
         "Los dos revisores discreparon; el valor es el del registro de "
         "adjudicación (extraction_conflicts.csv), que anota como responsables a "
         "los dos. Entre las casillas adjudicadas, solo estas constan como "
         "consenso."),
        ("adjudicada por uno (D.V.)",
         "Los dos revisores discreparon; el valor es el del registro de "
         "adjudicación, que anota un único responsable: D.V."),
        ("adjudicada por uno (N.T.)",
         "Los dos revisores discreparon; el valor es el del registro de "
         "adjudicación, que anota un único responsable: N.T."),
        # Se llamaba «corregido por consenso contra el texto» hasta el
        # 2026-10-13 (build_adjudicated_dataset.CORR_DOS). Ahora dice cuantas
        # firmas lleva, simetrica con la de una firma.
        # Solo atribuia al modelo las correcciones de modalidad. Las de la
        # relectura del 2026-09-30 llevan la firma de los dos, pero lo que
        # firmaron es la conclusion en texto libre: el valor de la casilla lo
        # derivo el modelo (ingest_lectura_firmada.py). {relectura} lo cuenta
        # frase_relectura_s15() sobre S15 y correcciones_tras_texto_completo.csv.
        ("corregido contra el texto (dos firmas)",
         "Casilla ya cerrada que una corrección posterior, con su cita literal y "
         "la firma de los dos autores, cambió contra el texto completo "
         "(correcciones_tras_texto_completo.csv). Las correcciones de modalidad las "
         "propuso el modelo de lenguaje tras leer los textos.{relectura} No cuenta "
         "como doble lectura en la tabla 5."),
        ("corregido contra el texto (una firma)",
         "Lo mismo, con la firma de un solo autor; no cuenta como doble lectura. "
         "Entre ellas están las casillas del tercer paciente de EST-121, que "
         "extrajo el modelo de lenguaje y firmó solo D.V."),
        ("sin segunda lectura",
         "Solo un revisor rellenó la casilla; no cuenta como doble lectura."),
        ("ABIERTO",
         "Los dos discreparon y el desacuerdo no está adjudicado; la casilla sale "
         "vacía en S14. Así queda también un desacuerdo que se cerró por una "
         "regla mecánica, sin firma conjunta: su valor no lo firmó nadie."),
        ("vacio", "Ninguno de los dos rellenó la casilla."),
    ],
}
NOTA_ETIQUETAS = {
    "S15_procedencia_de_cada_casilla": (
        "Una casilla adjudicada que después se corrigió contra el texto lleva la "
        "etiqueta de la corrección; por eso las casillas «adjudicada» son menos "
        "que los desacuerdos adjudicados del registro. Que el registro anote un "
        "único responsable dice quién firmó, no cuántos leyeron: la casilla la "
        "leyeron los dos, y por eso discreparon."),
}

# Las etiquetas que la Léeme de S15 dice que cuentan como doble lectura en la
# tabla 5. La frase la escribe QUE_ES; esto la ata al calculo: si
# build_outcome_scalars.DOBLE cambia, el guion se para en vez de publicar una
# descripcion que ya no es la del calculo.
DOBLE_DE_LA_TABLA = {"acuerdo", "adjudicada por los dos",
                     "adjudicada por uno (D.V.)", "adjudicada por uno (N.T.)"}

# Las Léeme remiten a la numeracion del informe extendido (el maestro). El
# manuscrito de la revista no numera las secciones y numera las tablas de otro
# modo, y estos .xlsx viajan tambien en el sobre de la revista. Decia «el
# manuscrito enviado a la revista»: no se ha enviado, y enviarlo o no lo
# deciden los autores.
NUMERACION = ("Las secciones y tablas que se citan son las del informe extendido "
              "(manuscrito maestro). En el manuscrito preparado para la revista "
              "las secciones no van numeradas")


def _uno(hallados, que, ruta):
    if len(hallados) != 1:
        raise SystemExit("NO SE ESCRIBE: %s aparece %d veces en %s, y su número "
                         "no se puede leer del manuscrito" % (que, len(hallados),
                                                              ruta.name))
    return hallados[0]


_NUMEROS = {}


def numeros():
    """Números de sección del maestro y de tabla de los dos manuscritos que
    citan las Léeme, leídos de los .md (una vez). Antes solo se conocía la
    equivalencia de la tabla 5, tecleada («allí la tabla 5 (desenlaces) es la
    Tabla 4»); las Léeme nuevas citan además las tablas de riesgo de sesgo y de
    completitud, que en la revista llevan otro número."""
    if _NUMEROS:
        return _NUMEROS
    N = numeracion_manuscritos()
    tm = ES.read_text(encoding="utf-8")
    tr = REVISTA.read_text(encoding="utf-8")
    patron_comp = r"completitud del? reporte en las variables"
    comp = (_uno([n for n, p in _pies(tm).items() if re.search(patron_comp, p, re.I)],
                 "la tabla de completitud de las variables", ES),
            _uno([n for n, p in _pies(tr).items() if re.search(patron_comp, p, re.I)],
                 "la tabla de completitud de las variables", REVISTA))
    apartados = [(m.group(1), m.group(2).strip()) for m in re.finditer(
        r"(?m)^#{2,4} +(\d+(?:\.\d+)+) +(.+?)\s*$", tm)]

    def sec(patron):
        return _uno([n for n, t in apartados if re.search(patron, t, re.I)],
                    "el apartado «%s»" % patron, ES)

    _NUMEROS.update({
        "sec_desenlaces": N["desenlaces"]["seccion_maestro"],
        "tab_desenlaces": N["desenlaces"]["tabla_maestro"],
        "sec_embudo": N["embudo"]["seccion_maestro"],
        "tab_embudo": N["embudo"]["tabla_maestro"],
        "sec_riesgo": N["riesgo"]["seccion_maestro"],
        "tab_riesgo": N["riesgo"]["tabla_maestro"],
        "tab_completitud": comp[0],
        "sec_no_declara": sec(r"no declara$"),
        "sec_exclusiones": sec(r"que salieron después$"),
        "sec_extraccion": sec(r"^extracción de datos$"),
        "sec_rob_metodos": sec(r"^riesgo de sesgo y certeza$"),
        # (nombre, número en el maestro, número en la revista)
        "_tablas": [("desenlaces", N["desenlaces"]["tabla_maestro"],
                     N["desenlaces"]["tabla_revista"]),
                    ("riesgo de sesgo", N["riesgo"]["tabla_maestro"],
                     N["riesgo"]["tabla_revista"]),
                    ("embudo de agregabilidad", N["embudo"]["tabla_maestro"],
                     N["embudo"]["tabla_revista"]),
                    ("completitud de las variables", comp[0], comp[1])],
    })
    return _NUMEROS


def numeracion(donde):
    """La advertencia de numeracion, con la equivalencia en la revista de cada
    tabla que la Léeme cita y que allí lleva otro número."""
    otras = ["la tabla %d (%s) es la Tabla %d" % (m, nombre, r)
             for nombre, m, r in numeros()["_tablas"]
             if m != r and re.search(r"\btabla %d\b" % m, donde, re.I)]
    return NUMERACION + ("; allí " + ", y ".join(otras) if otras else "") + "."


def alcance_s18b(datos, cab):
    """Qué estudios trae S18b frente a los que tienen juicio en S18.

    S18b llegó a traer frases de tres estudios sin juicio en S18 (EST-055,
    EST-063 y EST-132, en el consejo del 2026-10-13). El filtro a los estudios
    con juicio en S18 se hace en build_verifiables_package; la Léeme lo dice,
    y lo dice leyendo los dos CSV, de modo que no puede afirmar un filtro que
    no se hizo: si quedan estudios sin juicio, los nombra.
    """
    s18 = PAQ / "S18_cada_juicio_con_su_frase.csv"
    if "study_id" not in cab or not s18.exists():
        return ""
    i = cab.index("study_id")
    propios = {f[i] for f in datos if len(f) > i and f[i].strip()}
    with open(s18, encoding="utf-8-sig", newline="") as fh:
        con_juicio = {r["estudio"] for r in csv.DictReader(fh)}
    fuera = sorted(propios - con_juicio)
    if not fuera:
        return (" Solo trae los %d estudios que tienen juicio en S18; las frases "
                "cosechadas para cualquier otro estudio no se incluyen."
                % len(propios))
    return (" Trae %d estudios; %d de ellos (%s) no tienen juicio en S18."
            % (len(propios), len(fuera), ", ".join(fuera)))

# Cabeceras. Lo que el canal llama X, un revisor lo entiende como Y.
ETIQUETA = {
    "record_id": "Identificador del informe", "id": "Identificador",
    "id_provisional": "Identificador del estudio", "estudio": "Estudio",
    "arm_id": "Brazo", "orden": "Orden", "verdict": "Decisión",
    "reason": "Motivo", "decided_by": "Quién decidió", "decided_at": "Cuándo",
    "corriente": "Corriente (base o registro)", "titulo": "Título",
    "revista": "Revista", "anio": "Año", "situacion": "Situación",
    "n_informes": "Informes del estudio", "diseno": "Diseño",
    "n_brazo": "Pacientes en el brazo", "procedencia": "País",
    "texto_completo": "¿Texto completo obtenido?", "clave_de_estudio": "Clave del estudio",
    "tipo": "Tipo de informe", "identificador_resuelto": "Identificador resuelto",
    "via": "Cómo se localizó", "nota": "Nota", "duplicado_interno": "Duplicado interno",
    "fuentes": "Fuentes que lo aportaron", "paginas": "Páginas", "palabras": "Palabras",
    "idioma_texto_completo": "Idioma del texto completo", "confianza": "Confianza",
    "evidencia": "Evidencia", "idioma_previo": "Idioma declarado antes",
    "coincide": "¿Coinciden?", "idioma_declarado": "Idioma declarado",
    "fuente_declarado": "De dónde sale el idioma declarado",
    "idioma_del_texto": "Idioma del texto", "clase_de_evidencia": "Clase de evidencia",
    "prueba": "Prueba", "estado": "Estado",
    "caracteres_de_resumen": "Caracteres del resumen",
    "titulo_alternativo": "Título alternativo",
    "pathogen_scope": "¿Solo P. aeruginosa o mixto?",
    "resistance_class": "Clase de resistencia",
    "resistance_class_source": "De dónde sale la clase",
    "dtr_status": "¿Cumple criterio DTR?", "route": "Vía de administración",
    "modality": "¿Fago solo o con antibiótico?", "study_design": "Diseño del estudio",
    "extraction_status": "Estado de la extracción", "n_arm": "Pacientes en el brazo",
    "en_corpus_actual": "¿Sigue en el corpus?", "study_id": "Estudio",
    "estado_final": "¿Quedó incluido al final?",
    "motivo_de_la_exclusion": "Por qué se excluyó",
    "campo": "Variable", "resolucion": "Valor acordado",
    "resuelto_por": "Quién lo resolvió", "fecha": "Fecha",
    # Añadidas el 2026-10-19: S14, S16, S17, S18, S20, S21, S22, S23 y S24
    # salian con sus columnas internas. Las de la extracción (S4, S14, S15)
    # toman el rótulo de los formularios que rellenaron los revisores
    # (extraction_schema.ETIQUETAS), en rotulo().
    "firmado_por": "Firmado por",
    "codigo": "Código del motivo", "que_significa_el_codigo": "Qué significa el código",
    "motivo": "Motivo", "cita_del_texto": "Cita en que se apoya",
    "decidido_por": "Quién decidió",
    "diseno_adjudicado": "Diseño adjudicado", "n_exito": "Éxito clínico (n)",
    "N_brazo": "Pacientes en el brazo (N)",
    "diseno_comparativo": "Requisito: diseño comparativo",
    "numerador_valido": "Requisito: numerador válido",
    "denominador_valido": "Requisito: denominador válido",
    "definicion_operativa": "Requisito: definición operativa de éxito",
    "atribuible_a_P_aeruginosa": "Requisito: atribuible a P. aeruginosa",
    "terapeutica_no_profilactica": "Requisito: terapéutica, no profiláctica",
    "proporcion_no_tiempo": "Requisito: proporción, no tiempo",
    "primer_requisito_que_falla": "Primer requisito que falla",
    "informe": "Informe", "referencia_del_informe": "Referencia del informe",
    "instrumento": "Instrumento", "item": "Dominio (código)", "dominio": "Dominio",
    "tipo_de_juicio": "Tipo de juicio", "valor": "Juicio",
    "fuente_documental": "Fuente documental",
    "cita_que_lo_respalda": "Lo que lo sostiene (cita o nota)",
    "tipo_informe": "Tipo de informe",
    "identificadores": "Identificadores (PMID, DOI, NCT)",
    "informes_del_estudio": "Informes del estudio",
    "documento_leido": "Documento leído",
    "cita_de_extraccion": ETIQUETAS_EXTRACCION["extraction_citation"],
    "titulo_del_informe": "Título del informe",
    "variable": "Variable",
    "declarado_texto_completo": "Declarado en el texto completo",
    "declarado_no_clasificable": "Declarado pero no clasificable",
    "no_declarado_texto_completo": "No declarado en el texto completo",
    "texto_no_recuperado": "Texto completo no recuperado",
    "total": "Estudios",
    "no_asignable_en_el_resumen": "No asignable en el resumen",
    "no_asignable_en_el_resumen_pct": "No asignable en el resumen (%)",
    "silencio_del_articulo_pct": "No declarado en el texto completo (%)",
    "estudio_1": "Estudio 1", "estudio_2": "Estudio 2",
    "clave_del_paciente": "Clave del paciente",
    "pacientes_de_esa_clave": "Pacientes con esa clave",
    "paciente_o_identificador": "Paciente o identificador",
    "senal_que_lo_marco": "Señal que lo marcó",
    "pacientes_potencialmente_duplicados": "Pacientes posiblemente duplicados",
    "brazos_afectados": "Brazos afectados",
    "se_conto_una_o_dos_veces": "¿Se contó una o dos veces?",
    "veredicto": "Veredicto", "accion_necesaria": "Acción necesaria",
    "clase_en_la_extraccion_antes": "Clase en la extracción, antes",
    "procedencia_antes": "Procedencia de la clase, antes",
    "verificacion": "Verificación (lo codificó el modelo)",
    "clase_verificada_codificada": "Clase verificada (lo codificó el modelo)",
    "relacion_con_la_declarada": "Relación con la clase declarada (lo codificó el modelo)",
    "cambia_en_la_extraccion": "Qué cambia en la extracción (lo codificó el modelo)",
    "queda_abierto": "Queda abierto (lo codificó el modelo)",
    "clase_verificada_firmada": "Clase verificada (texto firmado)",
    "criterio_o_antibiograma_firmado": "Criterio o antibiograma (texto firmado)",
    "disenos": "Diseños",
    "grupo_de_comparacion_firmado_2026_09_22": "Grupo de comparación (firmado el 2026-09-22)",
    "grupo_sin_fago": "Grupo sin fago (lo codificó el modelo)",
    "contraste_para_p_aeruginosa": "Contraste para P. aeruginosa (lo codificó el modelo)",
    "brazo_control_identificado": "Brazo control identificado",
    "tipo_y_unidad_de_asignacion": "Tipo y unidad de asignación",
    "tiempo_cero": "Tiempo cero",
    "tiempo_de_evaluacion_del_desenlace": "Tiempo de evaluación del desenlace",
    "cointervenciones_y_antibiotico_concomitante": "Cointervenciones y antibiótico concomitante",
    "perdidas_y_datos_faltantes": "Pérdidas y datos faltantes",
    "estimando_reportado": "Estimando reportado",
    "hay_contraste_extraible": "¿Hay contraste extraíble?",
}

# Donde una misma columna interna significa otra cosa en un anexo concreto.
ETIQUETA_DE = {
    "S18_cada_juicio_con_su_frase": {"n": "Nº de juicio"},
    # En S8, «via» es por dónde buscar el texto; en S20, la prueba del vínculo.
    "S20_de_que_informe_salio_cada_brazo": {"via": "Cómo se estableció el vínculo"},
    # «campo» es «Variable» en el resto; aquí la variable ya va en «variable».
    "S22_completitud_resumen_frente_a_texto": {"campo": "Nombre interno de la variable"},
}


def rotulo(clave, col):
    """El rótulo legible de una columna: el propio del anexo, el general, el
    del formulario de extracción o, si no hay ninguno, el nombre interno."""
    return (ETIQUETA_DE.get(clave, {}).get(col) or ETIQUETA.get(col)
            or ETIQUETAS_EXTRACCION.get(col) or col)

# Códigos internos -> castellano. Solo donde el código no se entiende solo.
VALOR = {
    "EXCLUDE": "excluido", "ADVANCE": "pasa a resumen", "FULLTEXT": "pasa a texto completo",
    "Pseudomonas-only": "solo P. aeruginosa",
    "mixed-pathogen-with-Pseudomonas-subgroup": "mixto, con subgrupo separable",
    "not-classifiable": "no clasificable", "below-MDR-threshold": "por debajo de MDR",
    "author-reported": "declarado por el autor",
    "independently-verified": "verificado de forma independiente",
    "yes": "sí", "no": "no", "not-derivable": "no derivable",
    "PARTIAL": "parcial", "COMPLETE": "completa",
    "extraible": "extraíble", "solo-registro": "solo ficha de registro",
    "solo-resumen": "solo resumen",
    "case report": "reporte de caso único", "case series": "serie de casos",
    "RCT": "ensayo aleatorizado", "non-randomised trial": "ensayo no aleatorizado",
    "prospective cohort": "cohorte prospectiva",
    "retrospective cohort": "cohorte retrospectiva",
    "base": "base bibliográfica", "registro": "registro de ensayos",
    # Vias y modalidades. Se traducen porque son de las columnas que un revisor
    # lee primero; los identificadores de ensayo y los DOI NO se tocan, que son
    # claves y traducirlas seria destruirlas.
    "phage+antibiotic combination": "fago + antibiótico",
    "phage monotherapy": "fago en monoterapia",
    "topical/local": "tópica o local", "inhaled/nebulized": "inhalada o nebulizada",
    "IV": "intravenosa", "oral": "oral", "intravenous": "intravenosa",
    "other": "otra", "unknown": "no consta", "none": "ninguno",
    "no-latino": "no latino",
    "INCLUIDO": "incluido", "EXCLUIDO DESPUES": "excluido después",
    "ADMITIDO": "admitido",
    # «Primer requisito que falla» de S17 traía el nombre interno del requisito.
    "diseno_comparativo": "diseño comparativo", "numerador_valido": "numerador válido",
    "denominador_valido": "denominador válido",
    "definicion_operativa": "definición operativa de éxito",
    "atribuible_a_P_aeruginosa": "atribuible a P. aeruginosa",
    "terapeutica_no_profilactica": "terapéutica, no profiláctica",
    "proporcion_no_tiempo": "proporción, no tiempo",
}


_PP = {}


def _primera_pasada():
    """primera_pasada() de build_verifiables_package (la que usan S1, S6 y
    S19), una sola vez."""
    if not _PP:
        _PP.update(primera_pasada())
    return _PP


def frase_relectura_s15(cab, datos):
    """Cuántas casillas «corregido contra el texto (dos firmas)» de S15 son
    correcciones de la relectura del 2026-09-30, y qué firmaron los autores.

    Las escribe ingest_lectura_firmada.py con su FECHA y su FIRMA_CORR. Se
    cuentan sobre correcciones_tras_texto_completo.csv y se comprueba en S15 la
    etiqueta de cada una: si alguna llevara otra, la frase no valdría."""
    with open(ILF.CORR, encoding="utf-8-sig", newline="") as fh:
        corr = [r for r in csv.DictReader(fh)
                if r["fecha"] == ILF.FECHA and r["firmado_por"] == ILF.FIRMA_CORR]
    if not corr:
        return ""
    col = {c: i for i, c in enumerate(cab)}
    fila_de = {(f[col["study_id"]], f[col["arm_id"]]): f for f in datos}
    n = 0
    for r in corr:
        f = fila_de.get((r["study_id"], r["arm_id"]))
        if f is None:
            continue          # un estudio que ya no está en el corpus
        if f[col[r["campo"]]] != "corregido contra el texto (dos firmas)":
            raise SystemExit("S15: la corrección de la relectura %s %s %s lleva la "
                             "etiqueta «%s»; revisa la Léeme."
                             % (r["study_id"], r["arm_id"], r["campo"],
                                f[col[r["campo"]]]))
        n += 1
    campos = ["«%s»" % c for c in sorted(
        {rotulo("S15_procedencia_de_cada_casilla", r["campo"]) for r in corr})]
    campos = (", ".join(campos[:-1]) + " y " + campos[-1]) if len(campos) > 1 else campos[0]
    return (" %d de estas casillas (%s) son correcciones de la relectura del %s: "
            "los dos autores firmaron su conclusión en texto libre, y el valor que "
            "entró en la casilla lo derivó de ese texto el modelo de lenguaje "
            "(ingest_lectura_firmada.py). Lo firmado es la conclusión, no el valor."
            % (n, campos, fecha_es(ILF.FECHA.split(";")[0].strip())))


def complementos(clave, cab, datos):
    """Lo que va entre llaves en QUE_ES y ETIQUETAS_DE: números de sección y de
    tabla, y las cifras y fechas que cada Léeme da, contadas sobre el propio
    CSV, los escalares o el fichero del que sale el anexo. Nada se teclea, y si
    lo que la frase afirma deja de ser cierto en los datos, el guion se para."""
    out = {k: v for k, v in numeros().items() if not k.startswith("_")}
    col = {c: i for i, c in enumerate(cab)}

    def columna(c):
        return [f[col[c]] if len(f) > col[c] else "" for f in datos]

    out["ingest"] = "ingest_lectura_firmada.py"
    if "fecha" in col and clave.startswith(("S23_", "S24_")):
        out["relectura_fecha"] = fechas_es(sorted(set(columna("fecha"))))

    if clave.startswith("S3_"):
        PP = _primera_pasada()
        ajenas = sorted({q for q in columna("decided_by") if "claude-opus-5" not in q})
        if ajenas:
            raise SystemExit("%s: la Léeme dice que todas las decisiones las emitió el "
                             "modelo, y estas no: %s" % (clave, ajenas))
        n_corr = len(PP["correcciones"])
        out["primera_pasada"] = (
            "La primera pasada del %s sobre el brazo A de PubMed, que el cribado del "
            "pozo sustituyó, consta en el repositorio y no en S3 (S19)%s."
            % (fecha_es(PP["dia"]),
               "" if not n_corr else
               (", y con ella la fila que corrigió una exclusión errónea (S6)"
                if n_corr == 1 else
                ", y con ella las %d filas que corrigieron exclusiones erróneas (S6)"
                % n_corr)))
        if clave == "S3_decisiones_etapa3_resumen":
            her = [f for f in datos
                   if f[col["decided_by"]].startswith("heredada del brazo por PMID")]
            copias = sorted({f[col["decided_at"]] for f in her})
            excl = sum(1 for f in her if f[col["verdict"]] == "EXCLUDE")
            if (len(her) != PP["heredadas"] or excl != PP["heredadas_excl"]
                    or (her and copias != [PP["heredadas_copia"]])
                    or any(ETIQUETA_ASISTIDA not in f[col["decided_by"]] for f in her)):
                raise SystemExit("S3 etapa 3: las filas heredadas (%d, %d exclusiones, "
                                 "copiadas %s) ya no son las que describe S19 (%d, %d, "
                                 "%s); regenera el paquete o revisa la Léeme."
                                 % (len(her), excl, copias, PP["heredadas"],
                                    PP["heredadas_excl"], PP["heredadas_copia"]))
            out["heredadas"] = "" if not her else (
                "Las %d filas que «Quién decidió» marca como «heredada del brazo por "
                "PMID» llevan la fecha en que se copiaron al pozo (%s, a las %s), no la "
                "de la decisión: cada una repite, con el mismo veredicto y el mismo "
                "motivo, una decisión de resumen que el modelo tomó en la primera "
                "pasada. Llevan la etiqueta «%s». %s S19 explica de dónde salen."
                % (len(her), fecha_es(copias[0]), copias[0][11:16], ETIQUETA_ASISTIDA,
                   nota_etiqueta_asistida(len(her), PP["heredadas_excl"],
                                          PP["heredadas_excl_en_muestra"])))

    if clave == "S16_excluidos_en_la_fase_de_texto_completo":
        S = json.loads(SCALARS.read_text(encoding="utf-8"))
        quien = columna("decidido_por")
        orden = sum(1 for q in quien if "no consta firma de N. Trelles" in q)
        dos = sum(1 for q in quien if " y " in q)
        # Las mismas reglas que build_auditoria_scalars (8f); si el S16 que
        # viaja no da lo mismo que los escalares, está desfasado.
        cuentas = {"exclusiones_firmadas_los_dos": dos,
                   "exclusiones_orden_dv_sin_firma_nt": orden,
                   "exclusiones_firmadas_solo_dv": len(quien) - dos - orden}
        distintas = {k: (v, S.get(k)) for k, v in cuentas.items() if S.get(k) != v}
        if distintas:
            raise SystemExit("S16: quién decidió cada exclusión no cuadra con los "
                             "escalares (S16, escalar): %s" % distintas)
        out.update(s16_dos=dos, s16_orden=orden, s16_solo=len(quien) - dos - orden)
        e = citas_s16(S)
        out["s16_sin_cita"] = (", y %d más %s sin cita" % (
            e["s16_sin_cita_otros"], "van" if e["s16_sin_cita_otros"] > 1 else "va")
            if e["s16_sin_cita_otros"] else "")
        out["s16_citadas"] = de_las_citadas(e, False)

    if clave == "S20_de_que_informe_salio_cada_brazo":
        out["s20_vias"] = " o ".join("«%s»" % v for v in sorted(set(columna("via"))))

    if clave == "S21_solapamiento_de_pacientes":
        if "firmado_por" in col:
            c = collections.Counter(columna("firmado_por"))
            out["s21_firmas"] = (" Quién firmó cada veredicto y cuándo está en «Firmado "
                                 "por» y «Fecha»: %s." % "; ".join(
                                     "%d, «%s»" % (n, v) for v, n in c.most_common()))
        else:
            # El S21 que hay en el paquete es anterior a audita_pendientes.py del
            # 2026-10-19: la Léeme no nombra columnas que el fichero no trae.
            print("  AVISO: S21 no trae «firmado_por»; corre audita_pendientes.py y "
                  "build_verifiables_package.py antes que este guion.")
            out["s21_firmas"] = ""

    # S14 y S15 son copias enteras de la extracción adjudicada: traen también
    # los brazos de los estudios excluidos después, y las tablas cuentan solo
    # los del corpus. Sin decirlo, «132 filas» chocaba con «n = 73 brazos».
    if clave in ("S14_extraccion_adjudicada", "S15_procedencia_de_cada_casilla"):
        with open(EXCLUSIONES, encoding="utf-8-sig", newline="") as fh:
            fuera = {r["study_id"] for r in csv.DictReader(fh)}
        ids = columna("study_id")
        n_fuera = sum(1 for i in ids if i in fuera)
        brazos = json.loads((ROOT / "quality_reports" / "outcome_scalars.json")
                            .read_text(encoding="utf-8"))["brazos"]
        if len(ids) - n_fuera != brazos:
            raise SystemExit("%s: %d brazos del corpus, y outcome_scalars dice %d."
                             % (clave, len(ids) - n_fuera, brazos))
        out["fuera_del_corpus"] = "" if not n_fuera else (
            " De sus %d filas, %d son brazos de estudios que salieron después del "
            "cribado (S16); la sección y las tablas que se citan abajo cuentan solo "
            "los %d brazos de los estudios que siguen en el corpus%s."
            % (len(ids), n_fuera, brazos,
               "" if clave.startswith("S14_") else
               ", y los recuentos de etiquetas de esta hoja incluyen todas las filas"))

    if clave == "S15_procedencia_de_cada_casilla":
        out["relectura"] = frase_relectura_s15(cab, datos)
    return out


def main():
    if not PAQ.exists():
        print("no existe %s" % PAQ)
        return 1
    import openpyxl
    from openpyxl.styles import Font, PatternFill, Alignment
    from openpyxl.utils import get_column_letter

    AZUL = PatternFill("solid", fgColor="1F4E79")
    hechos = 0

    for csvf in sorted(PAQ.glob("S*.csv")):
        clave = csvf.stem
        # Solo para buscar la descripción: el nombre del fichero no se toca.
        busca = "S5_listado" if clave.startswith("S5_listado_") else clave
        with open(csvf, encoding="utf-8-sig", newline="") as fh:
            filas = list(csv.reader(fh))
        if not filas:
            continue
        cab, datos = filas[0], filas[1:]
        # Un anexo sin entrada salía con «Anexo del material suplementario.» y
        # un «Dónde se usa» en blanco (seis viajaron así hasta el 2026-10-19).
        # Ahora el guion se para: una Léeme vacía no se publica.
        if busca not in QUE_ES:
            raise SystemExit("%s: no tiene entrada en QUE_ES; escribe qué es y "
                             "dónde se usa antes de publicarlo." % clave)
        que, donde = QUE_ES[busca]
        extra = complementos(clave, cab, datos)
        que, donde = que.format_map(extra), donde.format_map(extra)
        if clave == "S18b_frases_cosechadas_por_tema":
            que += alcance_s18b(datos, cab)
        if clave == "S15_procedencia_de_cada_casilla":
            from build_outcome_scalars import DOBLE
            if set(DOBLE) != DOBLE_DE_LA_TABLA:
                raise SystemExit(
                    "La Léeme de S15 dice que la doble lectura de la tabla 5 "
                    "cuenta %s, y build_outcome_scalars.DOBLE cuenta %s. "
                    "Corrige la frase de QUE_ES y DOBLE_DE_LA_TABLA."
                    % (sorted(DOBLE_DE_LA_TABLA), sorted(DOBLE)))

        wb = openpyxl.Workbook()

        # ---- Léeme ---------------------------------------------------------
        p = wb.active
        p.title = "Léeme"
        p.column_dimensions["A"].width = 42
        p.column_dimensions["B"].width = 74
        lineas = [
            (clave.replace("_", " "), 15, True),
            ("", 11, False),
            ("Qué es", 12, True), (que, 11, False),
            ("", 11, False),
            ("Dónde se usa", 12, True), (donde, 11, False),
        ] + ([(numeracion(donde), 10, False)] if donde else []) + [
            ("", 11, False),
            ("Cuántas filas", 12, True), ("%d filas de datos" % len(datos), 11, False),
            ("", 11, False),
            ("Qué significa cada columna", 12, True),
        ]
        f = 1
        for txt, tam, neg in lineas:
            c = p.cell(row=f, column=1, value=txt)
            c.font = Font(size=tam, bold=neg, color="1F4E79" if neg and tam >= 12 else "000000")
            c.alignment = Alignment(wrap_text=True, vertical="top")
            f += 1
        for col in cab:
            p.cell(row=f, column=1, value=rotulo(clave, col)).font = Font(bold=True, size=10)
            p.cell(row=f, column=2, value="columna interna: %s" % col).font = Font(size=10, color="808080")
            f += 1
        if clave in ETIQUETAS_DE:
            # Las casillas de datos son etiquetas: se cuentan aqui, sobre las
            # columnas que no son la clave del brazo.
            ids = {i for i, c in enumerate(cab) if c in ("study_id", "arm_id")}
            cuenta = {}
            for fila in datos:
                for i, v in enumerate(fila):
                    if i not in ids:
                        cuenta[v] = cuenta.get(v, 0) + 1
            explicadas = dict(ETIQUETAS_DE[clave])
            sobran = sorted(set(cuenta) - set(explicadas))
            if sobran:
                raise SystemExit("%s: etiquetas sin explicar en el Léeme: %s. "
                                 "Añádelas a ETIQUETAS_DE." % (clave, sobran))
            f += 1
            c = p.cell(row=f, column=1, value="Qué significa cada etiqueta")
            c.font = Font(size=12, bold=True, color="1F4E79")
            f += 1
            for etiqueta, sentido in ETIQUETAS_DE[clave]:
                c = p.cell(row=f, column=1, value="%s (%d casillas)"
                           % (etiqueta, cuenta.get(etiqueta, 0)))
                c.font = Font(bold=True, size=10)
                c.alignment = Alignment(wrap_text=True, vertical="top")
                c = p.cell(row=f, column=2, value=sentido.format_map(extra))
                c.font = Font(size=10)
                c.alignment = Alignment(wrap_text=True, vertical="top")
                f += 1
            if clave in NOTA_ETIQUETAS:
                c = p.cell(row=f, column=2, value=NOTA_ETIQUETAS[clave])
                c.font = Font(size=10, italic=True)
                c.alignment = Alignment(wrap_text=True, vertical="top")
                f += 1
        f += 1
        p.cell(row=f, column=1, value="El CSV con los nombres internos acompaña a este fichero: "
               "es la copia reproducible.").font = Font(size=10, italic=True)
        p.cell(row=f + 2, column=1,
               value="Generado el %s" % datetime.date.today().isoformat()).font = Font(size=9, color="808080")

        # ---- datos ---------------------------------------------------------
        h = wb.create_sheet("Datos")
        h.append([rotulo(clave, c) for c in cab])
        for c in h[1]:
            c.fill, c.font = AZUL, Font(color="FFFFFF", bold=True, size=10)
            c.alignment = Alignment(wrap_text=True, vertical="center")
        h.row_dimensions[1].height = 30
        for fila in datos:
            h.append([VALOR.get((v or "").strip(), v) for v in fila])
        h.freeze_panes = "A2"
        h.auto_filter.ref = "A1:%s%d" % (get_column_letter(len(cab)), h.max_row)
        for i, col in enumerate(cab, start=1):
            ancho = 46 if col in ("titulo", "reason", "evidencia", "nota",
                                  "titulo_alternativo", "via", "motivo_de_la_exclusion",
                                  "motivo", "cita_del_texto", "cita_que_lo_respalda",
                                  "titulo_del_informe", "decidido_por",
                                  "senal_que_lo_marco") else 20
            h.column_dimensions[get_column_letter(i)].width = ancho

        sal = PAQ / (clave + ".xlsx")
        wb.save(sal)
        hechos += 1
        print("  %-48s %6d filas" % (sal.name[:48], len(datos)))

    print()
    print("%d anexos convertidos. Los CSV se conservan intactos." % hechos)
    return 0


if __name__ == "__main__":
    sys.exit(main())
