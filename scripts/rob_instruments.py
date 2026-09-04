# -*- coding: utf-8 -*-
"""Los cuatro instrumentos de riesgo de sesgo, con sus items literales.

DE DONDE SALEN. No de memoria: cada item se recupero de su fuente oficial y un
segundo agente lo verifico contra esa misma fuente, descargandola por su cuenta.
La verificacion encontro cuatro defectos reales, todos corregidos aqui:

  1. RoB 2, pregunta 3.2: NO admite "No information". La primera recuperacion
     daba una lista unica de respuestas que implicaba que las cinco opciones
     valian para las 22 preguntas. Por eso cada pregunta lleva AQUI sus propias
     opciones, y 3.2 no tiene NI.
  2. RoB 2: faltaban las consideraciones preliminares (Box 2), que no son un
     preambulo opcional sino parte del instrumento: el diseno del ensayo, el
     objetivo del analisis y CUAL es el resultado numerico que se evalua. Sin
     eso, dos revisores pueden estar evaluando cosas distintas del mismo ensayo.
  3. ROBINS-I: los siete dominios estan bien y en orden, pero el texto ingles
     recuperado era parafrasis, no literal. Se conserva el TITULO del dominio,
     que si es literal de la Tabla 1, y la explicacion va como ayuda, no como si
     fuera el enunciado oficial.
  4. JBI reporte de caso, item 2: "the patient's history" se habia traducido
     como "historia clinica", que estrecha el sentido. La guia JBI incluye la
     historia medica, FAMILIAR y PSICOSOCIAL.

Ademas se fijo UNA sola etiqueta para "Unclear" ("No esta claro"): ofrecerla con
dos redacciones distintas habria producido desacuerdos que no son desacuerdos.

POR QUE CUATRO Y NO UNO. RoB 2 y ROBINS-I presuponen grupo de comparacion,
asignacion y seguimiento. Un reporte de caso no tiene ninguna de las tres, y
pasarlo por RoB 2 da "alto riesgo" en todos los dominios por un defecto del
instrumento, no del estudio. De ahi las dos listas JBI.

`dominio_evidencia` engancha cada pregunta con el dominio de
`evidencia_riesgo_sesgo.py`, para que el formulario traiga las frases del
articulo pegadas a la pregunta que tocan.
"""

# Opciones de respuesta. RoB 2 y ROBINS-I comparten las cinco basicas; las
# preguntas condicionales anaden "No aplicable" porque solo se responden si una
# anterior lo exige.
SI_NO = ["Sí", "Probablemente sí", "Probablemente no", "No", "Sin información"]
SI_NO_NA = SI_NO + ["No aplicable"]
SIN_NI = ["Sí", "Probablemente sí", "Probablemente no", "No", "No aplicable"]
JBI = ["Sí", "No", "No está claro", "No aplicable"]

JUICIO_ROB2 = ["Bajo riesgo de sesgo", "Algunas preocupaciones",
               "Alto riesgo de sesgo"]
JUICIO_ROBINS = ["Bajo riesgo de sesgo", "Riesgo moderado", "Riesgo grave",
                 "Riesgo crítico", "Sin información para juzgar"]
JUICIO_JBI = ["Incluir", "Excluir", "Buscar más información"]

NO_EVALUABLE = "no-evaluable"
PENDIENTE = "diseno-pendiente"

# Que instrumento le toca a cada diseno adjudicado.
POR_DISENO = {
    "RCT": "rob2",
    "non-randomised trial": "robins",
    "retrospective cohort": "robins",
    "prospective cohort": "robins",
    "case report": "jbi-caso",
    "case series": "jbi-serie",
    "other": PENDIENTE,
    "NA": PENDIENTE,
}


def _p(codigo, dominio, texto, ev, respuestas=None):
    return {"codigo": codigo, "dominio": dominio, "texto_es": texto,
            "dominio_evidencia": ev, "respuestas": respuestas or SI_NO}


INSTRUMENTOS = [
    {
        "clave": "rob2",
        "hoja": "RoB 2 (ensayos aleatoriz)",
        "nombre": "RoB 2 — Cochrane, ensayos aleatorizados (versión 22 de agosto de 2019)",
        "cuando": "Solo para ensayos aleatorizados. Evalúa el efecto de la ASIGNACIÓN "
                  "a la intervención (estimando por intención de tratar).",
        "fuente": "Higgins, Savović, Page y Sterne, RoB2 Development Group, 2019-08-22",
        # Box 2: sin esto dos revisores pueden evaluar resultados distintos.
        "preliminares": [
            ("Desenlace evaluado", "Éxito clínico|Erradicación microbiológica|"
                                   "Mortalidad|Eventos adversos|Emergencia de resistencia"),
            ("Resultado numérico concreto que se evalúa", None),
        ],
        "respuestas": SI_NO,
        "juicios": JUICIO_ROB2,
        "items": [
            _p("1.1", "1. Proceso de aleatorización",
               "¿Fue aleatoria la secuencia de asignación?", "ALEATORIZACION"),
            _p("1.2", "1. Proceso de aleatorización",
               "¿Se mantuvo oculta la secuencia de asignación hasta que los "
               "participantes fueron reclutados y asignados?", "ALEATORIZACION"),
            _p("1.3", "1. Proceso de aleatorización",
               "¿Las diferencias basales entre grupos sugieren un problema con la "
               "aleatorización?", "ALEATORIZACION"),

            _p("2.1", "2. Desviaciones de la intervención prevista",
               "¿Conocían los participantes la intervención asignada?", "CEGAMIENTO"),
            _p("2.2", "2. Desviaciones de la intervención prevista",
               "¿La conocían los cuidadores y quienes administraban la intervención?",
               "CEGAMIENTO"),
            _p("2.3", "2. Desviaciones de la intervención prevista",
               "Si sí en 2.1 o 2.2: ¿hubo desviaciones surgidas por el contexto del "
               "ensayo?", "DESVIACIONES", SI_NO_NA),
            _p("2.4", "2. Desviaciones de la intervención prevista",
               "Si sí en 2.3: ¿es probable que afectaran al desenlace?",
               "DESVIACIONES", SI_NO_NA),
            _p("2.5", "2. Desviaciones de la intervención prevista",
               "Si sí en 2.4: ¿estaban equilibradas entre los grupos?",
               "DESVIACIONES", SI_NO_NA),
            _p("2.6", "2. Desviaciones de la intervención prevista",
               "¿Se usó un análisis apropiado para estimar el efecto de la asignación "
               "(intención de tratar)?", "DESVIACIONES"),
            _p("2.7", "2. Desviaciones de la intervención prevista",
               "Si no en 2.6: ¿pudo tener un impacto sustancial no analizar a cada "
               "participante en su grupo asignado?", "DESVIACIONES", SI_NO_NA),

            _p("3.1", "3. Datos de desenlace faltantes",
               "¿Hubo datos de este desenlace para todos o casi todos los "
               "aleatorizados?", "PERDIDAS"),
            # La verificacion lo marco como bloqueante: 3.2 NO admite "Sin informacion".
            _p("3.2", "3. Datos de desenlace faltantes",
               "Si no en 3.1: ¿hay pruebas de que el resultado no se sesgó por los "
               "datos faltantes?", "PERDIDAS", SIN_NI),
            _p("3.3", "3. Datos de desenlace faltantes",
               "Si no en 3.2: ¿podría la ausencia de datos depender de su valor "
               "verdadero?", "PERDIDAS", SI_NO_NA),
            _p("3.4", "3. Datos de desenlace faltantes",
               "Si sí en 3.3: ¿es probable que dependiera de su valor verdadero?",
               "PERDIDAS", SI_NO_NA),

            _p("4.1", "4. Medición del desenlace",
               "¿Fue inapropiado el método de medición del desenlace?", "MEDICION"),
            _p("4.2", "4. Medición del desenlace",
               "¿Pudo diferir la medición entre los grupos?", "MEDICION"),
            _p("4.3", "4. Medición del desenlace",
               "Si no en 4.1 y 4.2: ¿conocían los evaluadores la intervención "
               "recibida?", "CEGAMIENTO", SI_NO_NA),
            _p("4.4", "4. Medición del desenlace",
               "Si sí en 4.3: ¿pudo influir ese conocimiento en la evaluación?",
               "CEGAMIENTO", SI_NO_NA),
            _p("4.5", "4. Medición del desenlace",
               "Si sí en 4.4: ¿es probable que influyera?", "CEGAMIENTO", SI_NO_NA),

            _p("5.1", "5. Selección del resultado notificado",
               "¿Se analizaron los datos conforme a un plan preespecificado, "
               "finalizado antes de disponer de los datos sin enmascarar?", "REPORTE"),
            _p("5.2", "5. Selección del resultado notificado",
               "¿Es probable que el resultado se seleccionara, según los resultados, "
               "entre varias mediciones elegibles del desenlace?", "REPORTE"),
            _p("5.3", "5. Selección del resultado notificado",
               "¿Es probable que se seleccionara entre varios análisis elegibles de "
               "los datos?", "REPORTE"),
        ],
    },
    {
        "clave": "robins",
        "hoja": "ROBINS-I (no aleatoriz)",
        "nombre": "ROBINS-I — estudios no aleatorizados de intervenciones",
        "cuando": "Ensayos no aleatorizados y cohortes. Un juicio por dominio y uno "
                  "global. Las categorías NO son las de RoB 2: aquí hay cinco.",
        "fuente": "Sterne et al., BMJ 2016;355:i4919 — títulos de dominio de la Tabla 1",
        "preliminares": [
            ("Desenlace evaluado", "Éxito clínico|Erradicación microbiológica|"
                                   "Mortalidad|Eventos adversos|Emergencia de resistencia"),
            ("¿Con qué ensayo aleatorizado ideal se compara?", None),
        ],
        "respuestas": SI_NO,
        "juicios": JUICIO_ROBINS,
        "items": [
            _p("D1", "Preintervención", "Sesgo por confusión", "CONFUSION",
               JUICIO_ROBINS),
            _p("D2", "Preintervención",
               "Sesgo en la selección de los participantes", "CONFUSION",
               JUICIO_ROBINS),
            _p("D3", "En la intervención",
               "Sesgo en la clasificación de las intervenciones", "CLASIFICACION",
               JUICIO_ROBINS),
            _p("D4", "Postintervención",
               "Sesgo por desviaciones de las intervenciones previstas",
               "DESVIACIONES", JUICIO_ROBINS),
            _p("D5", "Postintervención", "Sesgo por datos faltantes", "PERDIDAS",
               JUICIO_ROBINS),
            _p("D6", "Postintervención", "Sesgo en la medición de los desenlaces",
               "MEDICION", JUICIO_ROBINS),
            _p("D7", "Postintervención",
               "Sesgo en la selección del resultado notificado", "REPORTE",
               JUICIO_ROBINS),
        ],
    },
    {
        "clave": "jbi-caso",
        "hoja": "JBI reporte de caso",
        "nombre": "JBI Critical Appraisal Checklist for Case Reports (8 ítems)",
        "cuando": "Reportes de un solo caso. RoB 2 y ROBINS-I no aplican: no hay "
                  "grupo de comparación ni asignación.",
        "fuente": "Joanna Briggs Institute, jbi.global — ítems literales",
        "preliminares": [],
        "respuestas": JBI,
        "juicios": JUICIO_JBI,
        "items": [
            _p("1", "", "¿Se describieron con claridad las características "
               "demográficas del paciente?", "CASO", JBI),
            # "the patient's history" incluye la historia medica, familiar y
            # psicosocial; "historia clinica" a secas lo estrechaba.
            _p("2", "", "¿Se describió con claridad la historia del paciente "
               "—médica, familiar y psicosocial— y se presentó como una línea "
               "temporal?", "CASO", JBI),
            _p("3", "", "¿Se describió con claridad el estado clínico del paciente "
               "en el momento de la presentación?", "CASO", JBI),
            _p("4", "", "¿Se describieron con claridad las pruebas diagnósticas o los "
               "métodos de evaluación, y sus resultados?", "CASO", JBI),
            _p("5", "", "¿Se describieron con claridad la intervención o el "
               "procedimiento de tratamiento?", "CLASIFICACION", JBI),
            _p("6", "", "¿Se describió con claridad el estado clínico posterior a la "
               "intervención?", "CASO", JBI),
            _p("7", "", "¿Se identificaron y describieron los eventos adversos (daños) "
               "o los eventos no anticipados?", "CASO", JBI),
            _p("8", "", "¿El reporte de caso aporta lecciones prácticas?", "", JBI),
        ],
    },
    {
        "clave": "jbi-serie",
        "hoja": "JBI serie de casos",
        "nombre": "JBI Critical Appraisal Checklist for Case Series (10 ítems)",
        "cuando": "Series de casos. Los ítems 4 y 5 —inclusión consecutiva y "
                  "completa— son los que más discriminan en esta literatura.",
        "fuente": "Joanna Briggs Institute, jbi.global — ítems literales",
        "preliminares": [],
        "respuestas": JBI,
        "juicios": JUICIO_JBI,
        "items": [
            _p("1", "", "¿Existían criterios claros de inclusión en la serie?",
               "CONFUSION", JBI),
            _p("2", "", "¿Se midió la condición de forma estandarizada y fiable en "
               "todos los participantes?", "MEDICION", JBI),
            _p("3", "", "¿Se emplearon métodos válidos para identificar la condición "
               "en todos los participantes?", "MEDICION", JBI),
            _p("4", "", "¿La serie incluyó a los participantes de forma consecutiva?",
               "CONFUSION", JBI),
            _p("5", "", "¿La serie incluyó a los participantes de forma completa?",
               "CONFUSION", JBI),
            _p("6", "", "¿Se informaron con claridad las características demográficas "
               "de los participantes?", "CASO", JBI),
            _p("7", "", "¿Se informó con claridad la información clínica de los "
               "participantes?", "CASO", JBI),
            _p("8", "", "¿Se informaron con claridad los desenlaces o los resultados "
               "del seguimiento?", "MEDICION", JBI),
            _p("9", "", "¿Se informó con claridad la información demográfica del "
               "centro o centros de procedencia?", "CASO", JBI),
            _p("10", "", "¿Fue apropiado el análisis estadístico?", "", JBI),
        ],
    },
]


# ---------------------------------------------------------------------------
# VERSION SIMPLIFICADA, solo para los estudios con grupo de comparacion
# ---------------------------------------------------------------------------
# D.V. decidio el 2026-09-04 mantener la revision como narrativa descriptiva
# --sin metaanalisis y sin GRADE-- y anadir riesgo de sesgo SOLO a los estudios
# comparativos. Es el minimo que evita que un editor la rechace por incompleta
# en metodos, y no promete una sintesis que el propio articulo demuestra
# imposible.
#
# QUE SE SIMPLIFICA Y QUE NO. Se responde POR DOMINIO, no pregunta a pregunta.
# RoB 2 pasa de sus 22 preguntas de senalizacion a los 5 juicios de dominio que
# esas preguntas alimentan; ROBINS-I ya venia por dominio y no cambia. Lo que NO
# se simplifica es la escala: los juicios son los del instrumento, literales.
#
# ES UNA SIMPLIFICACION Y HAY QUE DECLARARLA. Sin las preguntas de senalizacion
# el juicio de dominio deja de ser reproducible por el algoritmo de RoB 2 y pasa
# a ser un juicio directo de los revisores. Eso es legitimo y comun en revisiones
# descriptivas, pero Metodos tiene que decir "a nivel de dominio" y no dejar
# creer que se aplico el algoritmo completo.

import re


def _dominios(clave):
    """Los dominios de un instrumento, en orden y sin repetir."""
    inst = next(i for i in INSTRUMENTOS if i["clave"] == clave)
    fuera, vistos = [], set()
    for it in inst["items"]:
        d = it.get("dominio", "")
        if d and d not in vistos:
            vistos.add(d)
            # El dominio de RoB 2 ya viene numerado ("1. Proceso de..."), y el
            # formulario antepone el codigo: sin quitarlo salia "1. 1. Proceso".
            cod = d.split(".")[0].strip() if "." in d[:3] else d[:4]
            texto = re.sub(r"^\s*\d+\.\s*", "", d)
            fuera.append({"codigo": cod, "dominio": d,
                          "dominio_evidencia": it.get("dominio_evidencia", ""),
                          "texto_en": texto, "texto_es": texto,
                          "respuestas": inst["juicios"]})
    return fuera


SIMPLIFICADOS = [
    {"clave": "rob2", "hoja": "RoB 2 por dominio",
     "nombre": "RoB 2 — juicio POR DOMINIO (ensayos aleatorizados)",
     "cuando": "Un juicio por dominio, sin responder las 22 preguntas de "
               "señalización. Declárese en Métodos como evaluación a nivel de dominio.",
     "fuente": next(i for i in INSTRUMENTOS if i["clave"] == "rob2")["fuente"],
     "items": _dominios("rob2"),
     "respuestas": JUICIO_ROB2,
     "juicios": JUICIO_ROB2},
    {"clave": "robins", "hoja": "ROBINS-I por dominio",
     "nombre": "ROBINS-I — juicio por dominio (no aleatorizados y cohortes)",
     "cuando": "ROBINS-I ya se responde por dominio: no se simplifica nada.",
     "fuente": next(i for i in INSTRUMENTOS if i["clave"] == "robins")["fuente"],
     "items": next(i for i in INSTRUMENTOS if i["clave"] == "robins")["items"],
     "respuestas": JUICIO_ROBINS,
     "juicios": JUICIO_ROBINS},
]

# Los disenos que llevan grupo de comparacion. Un reporte de caso o una serie no
# entran en la evaluacion simplificada: no hay nada que comparar, y su calidad se
# describe en el texto sin instrumento.
COMPARATIVOS = {"RCT", "non-randomised trial", "retrospective cohort",
                "prospective cohort"}
