# -*- coding: utf-8 -*-
"""Los bloques de riesgo de sesgo que `build_rob_table.py` escribe en cada manuscrito.

TRES DOCUMENTOS, UN SOLO ESTADO. El manuscrito de la revista, el maestro en
español y su traducción al inglés dicen lo mismo sobre el riesgo de sesgo, y
tienen que cambiar a la vez. Hasta ahora solo el de la revista se regeneraba:
el maestro seguía diciendo «ninguna de las dos evaluaciones se ha realizado»
mientras el de la revista ya declaraba una evaluación por consenso en curso.
Los dos viajan en el mismo sobre --el paquete de suplementos sale del maestro--
y contradecirse dentro de un envío es de las cosas que un editor lee primero.

CADA BLOQUE TIENE DOS REDACCIONES. La de PENDIENTE dice que la evaluación está
en curso y cuántos juicios faltan; la de HECHO dice qué se evaluó, con qué
instrumento y por consenso. La segunda solo se escribe cuando el fichero
adjudicado trae los 82 juicios firmados.

GRADE NO CAMBIA en ninguna de las dos: no hay estimación agrupada cuya certeza
calificar, y eso no depende de que el riesgo de sesgo se evalúe o no.
"""

# --- manuscrito de la revista -----------------------------------------------
# Lo escribe build_rob_table.py con su propio ALCANCE/AVISO; aquí solo viven
# los otros dos, que llevan numeracion de seccion y citas de pandoc.

MAESTRO_INI = "### 2.7 Riesgo de sesgo y certeza"
MAESTRO_FIN = "### 2.8 Métodos de síntesis y reproducibilidad"

MAESTRO_COMUN = (
    "El riesgo de sesgo se evalúa **solo en los estudios con diseño "
    "comparativo**: los %(ev)d que el diseño adjudicado sobre el artículo "
    "identifica como comparativos, todos con texto completo, como el resto del "
    "corpus desde el criterio de la sección 2.9. Los ensayos aleatorizados con "
    "RoB 2 [@Sterne2019_rob2] y los no aleatorizados y las cohortes con "
    "ROBINS-I [@Sterne2016_robinsi].\n\n"
    "La evaluación se emite **a nivel de dominio**: un juicio por dominio con "
    "las categorías literales de cada instrumento, sin responder las preguntas "
    "de señalización con que RoB 2 deriva ese juicio por algoritmo. Es una "
    "simplificación deliberada en una revisión descriptiva sin estimación "
    "agrupada, y se declara para que no se le atribuya una reproducibilidad "
    "algorítmica que no tiene. Los reportes y las series de casos no se "
    "evalúan con instrumento formal, por decisión y no por imposibilidad: "
    "carecen de comparador, de asignación y de seguimiento estructurado, y una "
    "herramienta construida sobre esos supuestos produce un riesgo alto "
    "uniforme que informa del instrumento y no del estudio "
    "[@Murad2018_casereports; @Munn2020_jbicaseseries].\n\n"
    "**Los juicios se emiten por duplicado independiente y se resuelven por "
    "consenso.** Cada autor evalúa por separado, con el artículo delante, y los "
    "desacuerdos se discuten uno a uno hasta acordar un juicio. La "
    "concordancia previa al consenso se reporta en la sección 3.7, igual que "
    "la de la extracción de datos (sección 2.6). Un estudio, incorporado a la "
    "evaluación después de las demás, tiene una sola lectura y se declara "
    "como tal.\n\n"
    "**GRADE no se aplica**, y el motivo no depende de lo anterior: califica "
    "la certeza de una estimación agrupada y esta revisión no presenta "
    "ninguna. La sección 3.5 muestra que solo %(agregables)d de los %(brazos)d brazos "
    "reúnen los requisitos mínimos para agregar, y ninguno los conserva tras "
    "aplicar los criterios de elegibilidad. Calificar la certeza de un "
    "resultado que no existe sería un trámite, no una evaluación "
    "[@Guyatt2011_grade].")

MAESTRO_PENDIENTE = (
    "\n\n**La evaluación está en curso: faltan %(faltan)d de los %(celdas)d "
    "juicios.** Mientras falte alguno, esta revisión no reporta riesgo de "
    "sesgo, y ningún indicador derivado del diseño lo sustituye.")

MAESTRO_HECHO = (
    "\n\nLa sección 3.7 reporta los %(celdas)d juicios y la tabla de dominios.")

EN_INI = "### 2.7 Risk of bias and certainty"
EN_FIN = "### 2.8 Synthesis methods and reproducibility"

EN_COMUN = (
    "Risk of bias is assessed **only in studies with a comparative design**: "
    "the %(ev)d that the design adjudicated on the article identifies as "
    "comparative, all with full text, as is the whole corpus since the "
    "criterion of section 2.9. Randomised trials with RoB 2 "
    "[@Sterne2019_rob2], and non-randomised trials and cohorts with ROBINS-I "
    "[@Sterne2016_robinsi].\n\n"
    "The assessment is issued **at domain level**: one judgement per domain "
    "with each instrument's literal categories, without answering the "
    "signalling questions through which RoB 2 derives that judgement "
    "algorithmically. This is a deliberate simplification in a descriptive "
    "review with no pooled estimate, and it is declared so that no algorithmic "
    "reproducibility is attributed to it. Case reports and case series are not "
    "assessed with a formal instrument, by decision and not by impossibility: "
    "they have no comparator, no allocation and no structured follow-up, and a "
    "tool built on those assumptions yields a uniform high risk that reports "
    "on the instrument rather than on the study [@Murad2018_casereports; "
    "@Munn2020_jbicaseseries].\n\n"
    "**Judgements are issued by consensus between the two authors, not in "
    "independent duplicate and resolved by consensus.** Each author assesses "
    "separately, with the article in front of them, and disagreements are "
    "discussed one by one until a judgement is agreed. Pre-consensus agreement "
    "is reported in section 3.7, as it is for data extraction (section 2.6). "
    "One study, added to the assessment after the others, has a single "
    "reading and is declared as such. Nothing further is "
    "reported. The limitation is stated in section 4.4.\n\n"
    "**GRADE is not applied**, and the reason does not depend on the above: it "
    "rates the certainty of a pooled estimate and this review presents none. "
    "Section 3.5 shows that only %(agregables)d of the %(brazos)d arms meet the minimum "
    "requirements for pooling, and none survives the eligibility criteria. "
    "Rating the certainty of a result that does not exist would be a "
    "formality, not an assessment [@Guyatt2011_grade].")

EN_PENDIENTE = (
    "\n\n**The assessment is under way: %(faltan)d of the %(celdas)d "
    "judgements are outstanding.** While any is outstanding this review "
    "reports no risk of bias, and no design-derived indicator substitutes "
    "for it.")

EN_HECHO = (
    "\n\nSection 3.7 reports the %(celdas)d judgements and the domain table.")

# La limitacion, en su seccion. Se sustituye la frase entera para que no quede
# "ni evaluacion del riesgo de sesgo" cuando ya la hay.
LIMITACION = [
    ("paper/manuscrito_revision_sistematica.md",
     "pero no presenta estimaciones de eficacia, ni evaluación del riesgo de "
     "sesgo, ni certeza GRADE (sección 2.7): es una caracterización del cuerpo "
     "de evidencia, no una síntesis de sus resultados.",
     "pero no presenta estimaciones de eficacia ni certeza GRADE (sección "
     "2.7): es una caracterización del cuerpo de evidencia, no una síntesis de "
     "sus resultados. El riesgo de sesgo se evalúa solo en los estudios "
     "comparativos con texto completo, a nivel de dominio y por consenso, de "
     "modo que hereda el sesgo de recuperación y no admite medida de "
     "concordancia entre revisores."),
    ("paper/manuscript_systematic_review_en.md",
     "but presents no efficacy estimates, no risk-of-bias assessment and no "
     "GRADE certainty (section 2.7): it is a characterisation of the evidence "
     "base, not a synthesis of its results.",
     "but presents no efficacy estimates and no GRADE certainty (section 2.7): "
     "it is a characterisation of the evidence base, not a synthesis of its "
     "results. Risk of bias is assessed only in the comparative studies with "
     "full text, at domain level and by consensus, so it inherits the "
     "retrieval bias; pre-consensus inter-reviewer agreement is reported."),
]

BLOQUES = [
    ("paper/manuscrito_revision_sistematica.md", MAESTRO_INI, MAESTRO_FIN,
     MAESTRO_COMUN, MAESTRO_PENDIENTE, MAESTRO_HECHO),
    ("paper/manuscript_systematic_review_en.md", EN_INI, EN_FIN,
     EN_COMUN, EN_PENDIENTE, EN_HECHO),
]


# --- Metodos del manuscrito de la revista ------------------------------------
# El concejo del 2026-09-07 lo cazo: estos parrafos estaban en pasado --"se
# evaluo", "los juicios se emitieron", "los dos autores evaluaron cada dominio
# con el articulo delante"-- sobre 82 juicios que no existen. El manuscrito se
# contradecia consigo mismo tres veces: el resumen decia "esta en evaluacion",
# Metodos decia "se emitieron" y una nota entre corchetes decia que no. Ahora
# el tiempo verbal sale del estado, como todo lo demas.

JSR_MET_INI = "### Evaluación del riesgo de sesgo"
JSR_MET_FIN = "### Síntesis"

JSR_MET = (
    "El riesgo de sesgo se evalúa únicamente en los estudios con diseño "
    "comparativo, que son los únicos capaces de sostener una afirmación de "
    "eficacia relativa, y solo en aquellos cuyo texto completo se obtuvo. El "
    "diseño que determina el instrumento es el adjudicado sobre el artículo, no "
    "el que declara el resumen. Los ensayos aleatorizados se evalúan con RoB 2 "
    "(11), y los ensayos no aleatorizados y las cohortes con ROBINS-I (12).\n\n"
    "La evaluación se emite **a nivel de dominio**: un juicio por cada dominio "
    "del instrumento, con las categorías literales de cada herramienta, sin "
    "responder las preguntas de señalización que RoB 2 utiliza para derivar el "
    "juicio de dominio mediante su algoritmo. Es una simplificación deliberada, "
    "acorde con una revisión descriptiva sin estimación agrupada, y se declara "
    "aquí para que no se atribuya a esta evaluación una reproducibilidad "
    "algorítmica que no tiene. ROBINS-I se responde por dominio en su "
    "formulación original, de modo que en su caso no hay simplificación "
    "alguna.\n\n"
    "**Los juicios se emiten por duplicado independiente y se resuelven por consenso.** "
    "Cada autor evalúa por separado, con el artículo delante, registrando la "
    "frase del texto en que se apoya; los desacuerdos se discuten uno a uno "
    "hasta acordar un juicio único. La concordancia previa al consenso se "
    "reporta, igual que la de la extracción de datos. Un estudio, incorporado "
    "a la evaluación después de los demás, tiene una sola lectura y se declara "
    "como tal.%(estado)s\n\n"
    "Los reportes de caso y las series de casos no se evalúan con instrumento "
    "formal, por decisión y no por imposibilidad: carecen de grupo de "
    "comparación, de asignación y de seguimiento estructurado, y aplicarles una "
    "herramienta construida sobre esos tres supuestos produce un riesgo alto "
    "uniforme que informa sobre el instrumento y no sobre el estudio (13). Sus "
    "limitaciones metodológicas se describen de forma narrativa en los "
    "Resultados.")

JSR_MET_PENDIENTE = (
    "\n\n**La evaluación está en curso: faltan %(faltan)d de los %(celdas)d "
    "juicios.** Mientras falte alguno, esta revisión no reporta riesgo de "
    "sesgo, y ningún indicador derivado del diseño lo sustituye.")

JSR_MET_HECHO = ""


# --- Seccion 3.7 del maestro y su traduccion ---------------------------------
# El maestro no tenia resultados de riesgo de sesgo en ninguna parte: sus
# Resultados acababan en 3.6. Al completarse la evaluacion, la redaccion HECHO
# de 2.7 y el item 18 de la lista PRISMA empezaron los dos a remitir a una
# "seccion 3.7" que no existia. O se escribe, o las dos remisiones cuelgan.
#
# Solo existe cuando la evaluacion esta completa: mientras falte un juicio, 2.7
# dice que la revision NO reporta riesgo de sesgo, y una seccion de resultados
# vacia lo contradiria.

SEC37 = [
    ("paper/manuscrito_revision_sistematica.md", "## 4. Discusi",
     "### 3.7 Riesgo de sesgo de los estudios comparativos\n\n"
     "%(prosa)s\n\n"
     "%(contraste)s\n\n"
     "**Tabla 7.** Riesgo de sesgo por dominio de los %(ev)d estudios "
     "comparativos evaluables. RoB 2 en los ensayos aleatorizados (cinco "
     "dominios) y ROBINS-I en los no aleatorizados y las cohortes (siete). "
     "«n. a.» marca los dominios que el instrumento no contempla, no un juicio "
     "que falte.\n\n"),
    ("paper/manuscript_systematic_review_en.md", "## 4. Discussio",
     "### 3.7 Risk of bias in the comparative studies\n\n"
     "%(prosa_en)s\n\n"
     "%(contraste_en)s\n\n"
     "**Table 7.** Domain-level risk of bias for the %(ev)d assessable "
     "comparative studies. RoB 2 for randomised trials (five domains) and "
     "ROBINS-I for non-randomised trials and cohorts (seven). \u201cn. a.\u201d marks "
     "domains the instrument does not contemplate, not a missing judgement.\n\n"),
]
