"""Ata cada cifra reportada a su frase, y falla si la frase se quedó atrás.

EL AGUJERO QUE CIERRA

`check_manuscript_numbers.py` comprueba que toda cifra del manuscrito coincida
con ALGÚN escalar del canal. Es necesario y no es suficiente: el 2026-08-13 el
manuscrito decía que se había obtenido el texto completo de 65 estudios cuando
ya eran 67, y el comprobador lo dio por bueno porque existe otro escalar,
`sin_ambito_de_patogeno`, que vale 65. La cifra estaba mal y pasaba por la
puerta de al lado.

La diferencia es de qué se comprueba. Aquel comprueba pertenencia a un conjunto;
este comprueba que UNA frase concreta lleva EL escalar que le toca. Si el corpus
cambia y la prosa no, aquí salta.

CÓMO SE AÑADE UNA AFIRMACIÓN

Una entrada por frase, con los escalares entre llaves. El formato de los números
se aplica solo: miles con espacio fino, decimales con coma en español y con
punto en inglés, tal como los escribe el manuscrito.

Falla también si una frase aparece más de una vez: dos apariciones significan
que hay dos sitios que actualizar y solo se comprobaría uno.

Uso:
    python scripts/check_manuscript_claims.py
"""
import json
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
ES = ROOT / "paper" / "manuscrito_revision_sistematica.md"
EN = ROOT / "paper" / "manuscript_systematic_review_en.md"
# El manuscrito que se envia a la revista. Estuvo SIN vigilar hasta el
# 2026-09-02: se edita a mano al reformatearlo, y sus cifras podian
# desviarse de los escalares sin que nada avisara. Lleva los dos idiomas
# dentro, asi que sus afirmaciones declaran el idioma una a una.
JSR = ROOT / "paper" / "manuscrito_JSR_final.md"
ESCALARES = ROOT / "quality_reports" / "synthesis_scalars.json"

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

# Frases que deben estar, con el escalar que manda en cada hueco.
AFIRMACIONES = [
    # ---- idioma sobre el cuerpo, 2026-10-06
    (ES, "sobre los {idioma_cuerpo_comprobados} estudios del corpus vigente con texto completo, y los {idioma_cuerpo_ingles} están en inglés. Los {idioma_no_verificable_excluidos} estudios sin texto completo cuyo idioma solo pudo probarse"),
    (EN, "on the {idioma_cuerpo_comprobados} studies of the current corpus with full text, and all {idioma_cuerpo_ingles} are in English. The {idioma_no_verificable_excluidos} studies without full text whose language could only be proven"),
    (JSR, "sobre el cuerpo de los {idioma_cuerpo_comprobados} estudios del corpus con texto completo, y los {idioma_cuerpo_ingles} están en inglés; los {idioma_no_verificable_excluidos} estudios sin texto completo cuyo idioma solo pudo probarse"),
    # ---- §3.1.1, 2026-10-06: NOREC, idioma y dos cifras tecleadas
    (ES, "**{letras_excluidos_texto_completo_IDI} más** salieron por **idioma**"),
    (EN, "**{letras_excluidos_texto_completo_IDI} more** were excluded on **language**"),
    (ES, "**{letras_excluidos_texto_completo_NOREC}** salieron, por último, por **NOREC**"),
    (EN, "**{letras_excluidos_texto_completo_NOREC}** left, finally, under **NOREC**"),
    (ES, "Los {excluidos_por_publicacion} anteriores se juzgaron sobre su publicación"),
    (EN, "The earlier {excluidos_por_publicacion} were judged on their publication"),
    (ES, "los {sin_texto_completo_total} estudios sin texto completo no se han podido comprobar contra nada"),
    (EN, "the {sin_texto_completo_total} studies without full text could not be checked against anything"),
    # ---- NOREC, 2026-10-06: el «1 estudio» iba tecleado
    (ES, "Su efecto medido: excluye **{excluidos_texto_completo_NOREC} estudios**"),
    (EN, "Its measured effect: it excludes **{excluidos_texto_completo_NOREC} studies**"),
    (JSR, "Se aplicó a **{excluidos_texto_completo_NOREC} estudios**"),
    # ---- 2026-10-06: procedencia (la escribe escribe_procedencia.py) y dos sueltas
    (EN, "of the {procedencia_declarada} studies that state their origin, {procedencia_europa_este} are from Russia, Poland, Georgia or Ukraine"),
    (JSR, "sobre los {desenlace_brazos_legibles} brazos legibles las cifras suben"),
    (ES, "No consta en {procedencia_no_declarada} de los {estudios_extraibles} estudios"),
    (EN, "It is not stated in {procedencia_no_declarada} of the {estudios_extraibles} studies"),
    (ES, "—de {rusos_antes_de_la_enmienda} estudios a"),
    (EN, "from {rusos_antes_de_la_enmienda} studies to"),
    (ES, "en {desenlace_diseno_no_clasificable} de los {desenlace_brazos} brazos no puede clasificarse —los dos revisores acordaron «NA» en los {desenlace_diseno_na_acordado}—, de modo que los recuentos por diseño son suelos sobre los {desenlace_brazos_con_diseno} restantes. De esos {desenlace_brazos_con_diseno}, **{desenlace_brazos_ensayo} brazos son ensayos**"),
    (EN, "in {desenlace_diseno_no_clasificable} of the {desenlace_brazos} arms it cannot be classified — the two reviewers agreed on \"NA\" in all {desenlace_diseno_na_acordado} — so the design counts are floors over the remaining {desenlace_brazos_con_diseno}. Of those {desenlace_brazos_con_diseno}, **{desenlace_brazos_ensayo} arms are trials**"),
    (EN, "That 42 of {estudios} studies are registry entries"),
    (EN, "Table 5 summarises it over the {desenlace_brazos} extracted arms."),
    (EN, "Those percentages are computed over all {desenlace_brazos} arms"),
    (JSR, "En {definicion_establecido_que_no_define} de ellos los revisores lo establecieron leyendo el artículo: {definicion_sin_definicion_declarada} declaran"),
    # ---- 2026-10-03: frases que solo pasaban por coincidencia (nota 16)
    (EN, "Single case reports, {casos_unicos_pct} %; comparative, {estudios_comparativos_pct} %; resistance class unassignable, {sin_clase_util_pct} %. Full text was obtained for {texto_completo_obtenido} ({texto_completo_pct} %)"),
    (EN, "the {texto_completo_pct} % figure coexists with an exclusion"),
    (EN, "**{estudios_excluidos_tras_texto_completo} of them left the corpus** and were excluded; the next subsection details them. The evidence base stands at **{estudios} studies**, grouping {informes_agrupados} reports: {estudios_un_solo_informe} with a single report and {estudios_multiinforme} with several"),
    (EN, "These {excluidos_entre_los_leidos} are the other side of that limitation, and they are **{excluidos_tras_texto_completo_pct} %** of the {estudios_leidos_a_texto_completo} studies whose full text could be read"),
    (EN, "Of the {estudios} studies, **{estudios_extraibles} have a retrievable publication**: {estudios_con_articulo} articles and {estudios_solo_resumen} that exist only as conference abstracts"),
    (EN, "**Route of administration** is not stated in **{sin_via_de_administracion_pct} %**"),
    (EN, "or is mixed with a separable subgroup, is not stated in **{sin_ambito_de_patogeno_pct} %**"),
    (EN, "(difficult-to-treat resistance) is not stated in **{sin_criterio_dtr_pct} %**"),
    (EN, "Over the {desenlace_brazos_legibles} readable arms the figures rise — from {desenlace_adverse_event_n_pct_de_los_brazos} % to {desenlace_adverse_event_n_pct_de_los_legibles} % for adverse events, from {desenlace_resistance_emergence_n_pct_de_los_brazos} % to {desenlace_resistance_emergence_n_pct_de_los_legibles} % for resistance"),
    (EN, "That {desenlace_clinical_success_n_pct_de_los_brazos} % is misleading"),
    (ES, "El cumplimiento del criterio **DTR** (*difficult-to-treat resistance*) no consta en el **{sin_criterio_dtr_pct} %**"),
    (JSR, "El cumplimiento del criterio **DTR** no consta en el **{sin_criterio_dtr_pct} %**"),
    (ES, "Estos {excluidos_entre_los_leidos} son la otra cara de esa limitación"),
    # ---- las decisiones firmadas el 2026-10-01 sobre la lectura del 30-sep
    (ES, "Los otros {bajo_umbral_estudio_entero} —{lista_bajo_umbral_estudio_entero_ids}— son estudios de un solo brazo cuyo único paciente no es multirresistente. {lista_bajo_umbral_mantenidos_22sep_ids} se mantienen en el corpus por decisión firmada de los dos autores el 22 de septiembre de 2026, y {lista_bajo_umbral_mantenidos_01oct_ids}, que quedaron por debajo del umbral"),
    (ES, "y {lista_bajo_umbral_mantenidos_03oct_ids}, que pasó por debajo del umbral al resolverse su clase ese mismo día, por la firmada el 3 de octubre"),
    (ES, "Los dos autores releyeron los {lectura_clase_estudios_leidos} estudios que entonces tenían texto completo"),
    (ES, "En {lectura_sin_pa_total} la lectura no encontró ningún paciente con *P. aeruginosa* tratado con fagos. Los dos autores excluyeron {lectura_sin_pa_excluidos} con el código ORG ({lista_lectura_sin_pa_excluidos_ids}"),
    (ES, "y mantuvieron {lectura_sin_pa_mantenidos}, que se declaran aquí con lo que el artículo dice: en {lista_lectura_sin_pa_cita_ids} la única mención de *P. aeruginosa* es la descripción del paciente de otro estudio del corpus ({lista_lectura_sin_pa_citados_ids}), y en {lista_lectura_sin_pa_no_diana_ids} el paciente tuvo *P. aeruginosa*, pero el fago no se dirigió contra ella. Lo mismo ocurre en {lista_lectura_dudosos_mantenidos_ids}, que también se mantienen"),
    (ES, "De los {lectura_clase_estudios} estudios con texto completo que quedan en el corpus, la clase pudo comprobarse en {lectura_clase_verificables}: en {lectura_clase_antibiograma} contra un antibiograma impreso y en {lectura_clase_texto} contra una descripción de la sensibilidad en el texto; en {lectura_clase_no_verificable} no hay con qué comprobarla"),
    (ES, "y los {lectura_clase_no_aplica} restantes son los mantenidos sin *P. aeruginosa* tratada"),
    (ES, "Las {lectura_correcciones} correcciones que la lectura deja inequívocas para el brazo entero —{lectura_correcciones_clase} de clase, {lectura_correcciones_procedencia} de su procedencia y {lectura_correcciones_dtr} del criterio DTR— entraron en la extracción con la firma de los dos autores. Los {lectura_abiertos_resueltos} estudios en que dejaba un brazo con más de un valor los resolvieron los dos autores el 1 de octubre de 2026: en {lectura_abiertos_corregidos} se corrigió la extracción ({lista_lectura_abiertos_corregidos_ids}) y en {lectura_abiertos_sin_cambio} se dejó como estaba ({lista_lectura_abiertos_sin_cambio_ids})"),
    (ES, "la clase de resistencia de los {lectura_clase_estudios_leidos} estudios que entonces tenían texto completo, comprobada contra el antibiograma publicado"),
    (ES, "el estimando de los {comparativos_reextraidos_leidos} estudios con diseño comparativo, {comparativos_reextraidos_leidos_con_texto} de ellos con texto"),
    (ES, "{letras_lectura_sin_pa_excluidos} de ellos se detectaron al comprobar la clase de resistencia contra el artículo"),
    (JSR, "Los otros {bajo_umbral_estudio_entero} —{lista_bajo_umbral_estudio_entero_ids}— son estudios de un solo brazo cuyo único paciente no es multirresistente. {lista_bajo_umbral_mantenidos_22sep_ids} se mantienen en el corpus por decisión firmada de los dos autores el 22 de septiembre de 2026, y {lista_bajo_umbral_mantenidos_01oct_ids}, que quedaron por debajo del umbral"),
    (JSR, "y {lista_bajo_umbral_mantenidos_03oct_ids}, que pasó por debajo del umbral al resolverse su clase ese mismo día, por la firmada el 3 de octubre"),
    (JSR, "Los dos autores releyeron los {lectura_clase_estudios_leidos} estudios que entonces tenían texto completo"),
    (JSR, "En {lectura_sin_pa_total} la lectura no encontró ningún paciente con *P. aeruginosa* tratado con fagos. Los dos autores excluyeron {lectura_sin_pa_excluidos} con el código ORG ({lista_lectura_sin_pa_excluidos_ids}"),
    (JSR, "y mantuvieron {lectura_sin_pa_mantenidos}, que se declaran aquí con lo que el artículo dice: en {lista_lectura_sin_pa_cita_ids} la única mención de *P. aeruginosa* es la descripción del paciente de otro estudio del corpus ({lista_lectura_sin_pa_citados_ids}), y en {lista_lectura_sin_pa_no_diana_ids} el paciente tuvo *P. aeruginosa*, pero el fago no se dirigió contra ella. Lo mismo ocurre en {lista_lectura_dudosos_mantenidos_ids}, que también se mantienen"),
    (JSR, "De los {lectura_clase_estudios} estudios con texto completo que quedan en el corpus, la clase pudo comprobarse en {lectura_clase_verificables}: en {lectura_clase_antibiograma} contra un antibiograma impreso y en {lectura_clase_texto} contra una descripción de la sensibilidad en el texto; en {lectura_clase_no_verificable} no hay con qué comprobarla"),
    (JSR, "y los {lectura_clase_no_aplica} restantes son los mantenidos sin *P. aeruginosa* tratada"),
    (JSR, "Las {lectura_correcciones} correcciones que la lectura deja inequívocas para el brazo entero —{lectura_correcciones_clase} de clase, {lectura_correcciones_procedencia} de su procedencia y {lectura_correcciones_dtr} del criterio DTR— entraron en la extracción con la firma de los dos autores. Los {lectura_abiertos_resueltos} estudios en que dejaba un brazo con más de un valor los resolvieron los dos autores el 1 de octubre de 2026: en {lectura_abiertos_corregidos} se corrigió la extracción ({lista_lectura_abiertos_corregidos_ids}) y en {lectura_abiertos_sin_cambio} se dejó como estaba ({lista_lectura_abiertos_sin_cambio_ids})"),
    (JSR, "la clase de resistencia de los {lectura_clase_estudios_leidos} estudios que entonces tenían texto completo, comprobada contra el antibiograma publicado"),
    (JSR, "el estimando de los {comparativos_reextraidos_leidos} estudios con diseño comparativo, {comparativos_reextraidos_leidos_con_texto} de ellos con texto"),
    (EN, "The other {bajo_umbral_estudio_entero} — {lista_bajo_umbral_estudio_entero_ids} — are single-arm studies whose only patient is not multidrug-resistant. {lista_bajo_umbral_mantenidos_22sep_ids} are kept in the corpus by signed decision of the two authors on 22 September 2026, and {lista_bajo_umbral_mantenidos_01oct_ids}, which fell below the threshold"),
    (EN, "and {lista_bajo_umbral_mantenidos_03oct_ids}, which fell below the threshold when its class was resolved that same day, by the one signed on 3 October"),
    (EN, "The two authors re-read the {lectura_clase_estudios_leidos} studies that then had full text"),
    (EN, "In {lectura_sin_pa_total} the reading found no patient with *P. aeruginosa* treated with phages. The two authors excluded {lectura_sin_pa_excluidos} with code ORG ({lista_lectura_sin_pa_excluidos_ids}"),
    (EN, "and kept {lectura_sin_pa_mantenidos}, which are declared here with what the article says: in {lista_lectura_sin_pa_cita_ids} the only mention of *P. aeruginosa* is the description of the patient of another study in the corpus ({lista_lectura_sin_pa_citados_ids}), and in {lista_lectura_sin_pa_no_diana_ids} the patient had *P. aeruginosa*, but the phage was not directed against it. The same holds in {lista_lectura_dudosos_mantenidos_ids}, which are also kept"),
    (EN, "Of the {lectura_clase_estudios} studies with full text that remain in the corpus, the class could be checked in {lectura_clase_verificables}: in {lectura_clase_antibiograma} against a printed antibiogram and in {lectura_clase_texto} against a description of susceptibility in the text; in {lectura_clase_no_verificable} there is nothing to check it against"),
    (EN, "the remaining {lectura_clase_no_aplica} are those kept without treated *P. aeruginosa*"),
    (EN, "The {lectura_correcciones} corrections the reading leaves unambiguous for the whole arm — {lectura_correcciones_clase} of class, {lectura_correcciones_procedencia} of its source and {lectura_correcciones_dtr} of the DTR criterion — entered the extraction with the signature of both authors. The {lectura_abiertos_resueltos} studies in which it left an arm with more than one value were resolved by the two authors on 1 October 2026: in {lectura_abiertos_corregidos} the extraction was corrected ({lista_lectura_abiertos_corregidos_ids}) and in {lectura_abiertos_sin_cambio} it was left as it was ({lista_lectura_abiertos_sin_cambio_ids})"),
    (EN, "the resistance class of the {lectura_clase_estudios_leidos} studies that then had full text, checked against the published antibiogram"),
    (EN, "estimand of the {comparativos_reextraidos_leidos} studies with a comparative design, {comparativos_reextraidos_leidos_con_texto} of them with text"),
    (EN, "{letras_lectura_sin_pa_excluidos} of them were detected when the resistance class was checked against the article"),
    # ---- 23 057 y 134 no son dos corrientes: la segunda esta dentro -------
    (ES, "Los {informes_de_registros} informes de registro de ensayos no son una corriente aparte de esa cifra: están dentro de los {registros_identificados} identificados ({registros_de_ClinicalTrials_gov} de ClinicalTrials.gov, {registros_de_CTIS} de CTIS y {registros_de_EudraCT} de EudraCT)"),
    (EN, "The {informes_de_registros} trial-registry reports are not a separate stream from that figure: they are among the {registros_identificados} identified ({registros_de_ClinicalTrials_gov} from ClinicalTrials.gov, {registros_de_CTIS} from CTIS and {registros_de_EudraCT} from EudraCT)"),
    # ---- concordancia en riesgo de sesgo, medida el 2026-09-23 -----------
    # El manuscrito afirmaba que NO se podia medir. Los dos cuadernos
    # individuales existen y difieren en 12 juicios sobre el corpus vigente.
    (ES, "coincidieron en {rob_acuerdo_bruto} de los {rob_juicios_comparables} juicios comparables ({rob_acuerdo_pct} %; kappa de Cohen {rob_kappa})"),
    (EN, "agreed on {rob_acuerdo_bruto} of the {rob_juicios_comparables} comparable judgements ({rob_acuerdo_pct} %; Cohen's kappa {rob_kappa})"),
    (ES, "Los dos revisores evaluaron por separado {rob_estudios_con_dos_lecturas} de los {rob_estudios_evaluables} estudios evaluables"),
    (EN, "The two reviewers assessed {rob_estudios_con_dos_lecturas} of the {rob_estudios_evaluables} assessable studies independently"),
    (ES, "la concordancia previa al consenso fue del {rob_acuerdo_pct} % ({rob_acuerdo_bruto} de {rob_juicios_comparables} juicios; kappa de Cohen {rob_kappa}), con {rob_desacuerdos} desacuerdos"),
    (JSR, "la concordancia previa fue del {rob_acuerdo_pct} % ({rob_acuerdo_bruto} de {rob_juicios_comparables} juicios; kappa de Cohen {rob_kappa}), y los {rob_desacuerdos} desacuerdos"),
    (EN, "pre-consensus agreement was {rob_acuerdo_pct} % ({rob_acuerdo_bruto} of {rob_juicios_comparables} judgements; Cohen's kappa {rob_kappa}), with {rob_desacuerdos} disagreements"),
    # ---- la lectura firmada del 2026-09-30: umbral, clase comprobada, metodos
    (EN, "**In {brazos_bajo_umbral} of the {desenlace_brazos} arms the class falls below the multidrug-resistance threshold** ({coma_brazos_bajo_umbral_ids}). {brazos_bajo_umbral_estrato} are strata"),
    (EN, "Of the {lectura_clase_verificables} checked, the class matched the coded one in {lectura_clase_coincide}; in {lectura_clase_antes_no_clasificable} the extraction had it as not classifiable and the article allowed it to be assigned — {lectura_clase_antes_nc_bajo_umbral} below the threshold and {lectura_clase_antes_nc_xdr} XDR —; in {lectura_clase_mas_grave} it was more severe than coded ({lista_lectura_clase_mas_grave_ids}); in {lectura_clase_no_se_sostiene} the declared class was not confirmed ({lista_lectura_clase_no_se_sostiene_ids}), and in {lectura_clase_mixta} it changes between patients or between isolates of the same arm ({lista_lectura_clase_mixta_ids})"),
    (EN, "contains **{pacientes_duplicados_confirmados} patients described in more than one study**, spread over {estudios_con_paciente_compartido} of the {estudios}"),
    (EN, "EST-003 shares {est003_pacientes_compartidos} of its patients: {est003_con_est070} with EST-070"),
    (EN, "EST-034 shares {est034_pacientes_compartidos} patients with EST-049, EST-061 and EST-077"),
    (EN, "states that {est108_previamente_publicados} of its {est108_casos} patients had been reported before and cites {est108_referencias_previas} references, of which **{est108_estudios_citados_en_corpus} are studies in this corpus** — {lista_est108_estudios_citados_en_corpus_ids} — contributing {est108_pacientes_citados_en_corpus} patients; to them is added {lista_est108_coincidencias_no_citadas_ids}, published later"),
    (EN, "The examination covered the {texto_completo_obtenido} full texts and gathered {pares_solapamiento_examinados} pairs: {pares_solapamiento_por_detector} flagged by a detector based on product, country and citation, and {pares_solapamiento_por_lectura} found by reading. {pares_solapamiento_confirmados} were confirmed, {pares_solapamiento_descartados} were ruled out and **none remains unread**"),
    (EN, "it prevents reading the corpus as {estudios} disjoint sets of patients"),
    (EN, "outcomes, over the adjudicated extraction (n = {desenlace_brazos} arms)"),
    (EN, "a pooled proportion of clinical success (n = {desenlace_brazos} arms)"),
    # ---- cifras que coincidian por casualidad con OTRO escalar ------------
    # «46», «71», «18», «95»: el guardian numerico las daba por respaldadas
    # porque esos valores existen en los escalares con otro significado, y el
    # sincronizador no las tocaba porque ninguna ancla las nombraba. Salieron
    # todas a la vez el 2026-09-22, al bajar el corpus a 136.
    (JSR, "los {estudios_excluidos_tras_texto_completo} estudios detectados después, en la fase de texto completo"),
    (JSR, "las {estudios_excluidos_tras_texto_completo} exclusiones detectadas en la fase de texto completo"),
    (JSR, "El examen se hizo sobre los {texto_completo_obtenido} textos completos"),
    (JSR, "procedencia geográfica de los {estudios_extraibles} estudios con publicación recuperable"),
    (JSR, "(n = {estudios_extraibles} estudios recuperables, de los que {texto_completo_obtenido} tienen texto obtenido)"),
    (JSR, "{comparativos_un_brazo} + {brazos_del_comparativo_mayor} son los {desenlace_brazos_comparativos} brazos comparativos"),
    (ES, "—{estudios_extraibles} tras las exclusiones de la sección 3.1.1—"),
    (ES, "desde el resumen de los {estudios_extraibles} estudios vigentes"),
    (ES, "sin los {estudios_excluidos_tras_texto_completo} que salieron después"),
    # Dos veces: en Metodos y en la descripcion de S4, que ahora genera
    # `build_lista_anexos.py`.
    (ES, "desde el resumen de los {estudios_extraibles} estudios con publicación recuperable", 2),
    (EN, "and without the {estudios_excluidos_tras_texto_completo} that later left"),
    (EN, "The result is {estudios} studies against the dozens handled by published reviews, and would have been {estudios_antes_de_la_enmienda} without the language restriction"),
    (EN, "of the {desenlace_brazos} arms of this literature, **not one meets both the arithmetic conditions"),
    (EN, "**{casos_unicos} single case reports ({casos_unicos_pct} %)**, {diseno_case_series} case series, {diseno_prospective_cohort} prospective cohorts, {diseno_RCT} randomised trials, {diseno_non_randomised_trial} non-randomised trials and {diseno_retrospective_cohort} retrospective cohorts"),
    (EN, "A further {diseno_no_declarado} do not state a recognisable design in the abstract"),
    (EN, "Comparative designs total **{estudios_comparativos} studies, {estudios_comparativos_pct} %** of the whole"),
    # ---- la seccion 3.1.1, que enumera las exclusiones EN LETRA ----------
    # Ningun guardian las miraba: los tres buscan digitos. Al salir EST-063 el
    # 2026-09-22 se volvieron falsas «Veintinueve», «Veinticuatro» y «Cuatro
    # son protocolos», las tres a la vez y en los tres manuscritos.
    (ES, "### 3.1.1 Los {estudios_excluidos_tras_texto_completo} estudios que el cribado admitió y que salieron después"),
    (EN, "### 3.1.1 The {estudios_excluidos_tras_texto_completo} studies the screening admitted and that later left"),
    (ES, "**{letras_excluidos_por_publicacion} salieron al juzgarlos sobre su publicación.**"),
    (EN, "**{letras_excluidos_por_publicacion} left when judged on their publication.**"),
    (JSR, "**{letras_excluidos_por_publicacion} exclusiones se decidieron sobre el artículo.**"),
    (ES, "**{letras_excluidos_leyendo_articulo}** salieron de leer su artículo"),
    (EN, "**{letras_excluidos_leyendo_articulo}** came from reading the article"),
    (ES, "**{letras_excluidos_leyendo_articulo_ORG}** no tienen a *P. aeruginosa* en ningún paciente"),
    (EN, "**{letras_excluidos_leyendo_articulo_ORG}** have *P. aeruginosa* in no patient"),
    (ES, "**{letras_excluidos_leyendo_articulo_PRO}** son protocolos de estudio"),
    (EN, "**{letras_excluidos_leyendo_articulo_PRO}** are study protocols"),
    (ES, "**{letras_excluidos_leyendo_articulo_LAB}** no tienen pacientes"),
    (EN, "**{letras_excluidos_leyendo_articulo_LAB}** have no patients"),
    (ES, "**{letras_excluidos_leyendo_articulo_INT}** administran algo que no es un bacteriófago"),
    (EN, "**{letras_excluidos_leyendo_articulo_INT}** administer something that is not a bacteriophage"),
    (ES, "**{letras_excluidos_leyendo_articulo_OFF}** no evalúan fagoterapia en pacientes"),
    (EN, "**{letras_excluidos_leyendo_articulo_OFF}** do not evaluate phage therapy in patients"),
    (ES, "**{letras_excluidos_leyendo_articulo_REV}** no aportan datos primarios propios"),
    (EN, "**{letras_excluidos_leyendo_articulo_REV}** supply no primary data of their own"),
    # ---- lo que escribieron las nueve firmas del 2026-09-22 --------------
    # Las dos primeras sustituyen una frase que se volvio FALSA al corregir la
    # extraccion: el manuscrito seguia diciendo que dos brazos declaran un
    # numerador mayor que su denominador, y ya no lo hace ninguno.
    (ES, "**hoy ningún brazo declara una proporción imposible**"),
    (JSR, "**hoy ningún brazo declara una proporción imposible**"),
    # ---- la lectura firmada del 2026-09-30, en el maestro y en el de la revista
    (ES, "**En {brazos_bajo_umbral} de los {desenlace_brazos} brazos la clase queda por debajo del umbral de multirresistencia** ({coma_brazos_bajo_umbral_ids}). {brazos_bajo_umbral_estrato} son estratos"),
    (ES, "De los {lectura_clase_verificables} comprobados, la clase coincidió con la codificada en {lectura_clase_coincide}; en {lectura_clase_antes_no_clasificable} la extracción la daba por no clasificable y el artículo permitía asignarla —{lectura_clase_antes_nc_bajo_umbral} por debajo del umbral y {lectura_clase_antes_nc_xdr} XDR—; en {lectura_clase_mas_grave} era más grave que la codificada ({lista_lectura_clase_mas_grave_ids}); en {lectura_clase_no_se_sostiene} la clase declarada no se confirmó ({lista_lectura_clase_no_se_sostiene_ids}), y en {lectura_clase_mixta} cambia entre pacientes o entre aislados del mismo brazo ({lista_lectura_clase_mixta_ids})"),
    (JSR, "**En {brazos_bajo_umbral} de los {desenlace_brazos} brazos la clase queda por debajo del umbral de multirresistencia** ({coma_brazos_bajo_umbral_ids}). {brazos_bajo_umbral_estrato} son estratos"),
    (JSR, "De los {lectura_clase_verificables} comprobados, la clase coincidió con la codificada en {lectura_clase_coincide}; en {lectura_clase_antes_no_clasificable} la extracción la daba por no clasificable y el artículo permitía asignarla —{lectura_clase_antes_nc_bajo_umbral} por debajo del umbral y {lectura_clase_antes_nc_xdr} XDR—; en {lectura_clase_mas_grave} era más grave que la codificada ({lista_lectura_clase_mas_grave_ids}); en {lectura_clase_no_se_sostiene} la clase declarada no se confirmó ({lista_lectura_clase_no_se_sostiene_ids}), y en {lectura_clase_mixta} cambia entre pacientes o entre aislados del mismo brazo ({lista_lectura_clase_mixta_ids})"),
    (ES, "contiene **{pacientes_duplicados_confirmados} pacientes descritos en más de un estudio**, repartidos entre {estudios_con_paciente_compartido} de los {estudios}"),
    (ES, "EST-003 comparte {est003_pacientes_compartidos} de sus pacientes: {est003_con_est070} con EST-070"),
    (ES, "EST-034 comparte {est034_pacientes_compartidos} pacientes con EST-049, EST-061 y EST-077"),
    (ES, "afirma que {est108_previamente_publicados} de sus {est108_casos} pacientes se habían publicado antes y remite a {est108_referencias_previas} referencias, de las que **{est108_estudios_citados_en_corpus} son estudios de este corpus** —{lista_est108_estudios_citados_en_corpus_ids}—, que aportan {est108_pacientes_citados_en_corpus} pacientes; a ellos se suma {lista_est108_coincidencias_no_citadas_ids}, publicado después"),
    (ES, "El examen se hizo sobre los {texto_completo_obtenido} textos completos y reunió {pares_solapamiento_examinados} pares: {pares_solapamiento_por_detector} los marcó un detector por producto, país y cita, y {pares_solapamiento_por_lectura} los encontró la lectura. {pares_solapamiento_confirmados} se confirmaron, {pares_solapamiento_descartados} se descartaron y **ninguno queda sin leer**"),
    (ES, "impide leer el corpus como {estudios} conjuntos disjuntos de pacientes"),
    (JSR, "de los {sesgo_evaluables} evaluables, {comparativos_con_grupo_real} tienen un grupo con el que comparar"),
    (JSR, "y en {comparativos_sin_grupo_real} las notas firmadas del dominio 1 declaran que no lo hay"),
    # Pies de tabla y descripcion de anexos: tambien llevan cifras.
    (ES, "declarados, sobre la extracción adjudicada (n = {desenlace_brazos} brazos)"),
    (ES, "Listado de los {estudios} estudios con su situación y sus informes agrupados, y de los {estudios_excluidos_tras_texto_completo} excluidos"),
    (JSR, "de una proporción agrupada de éxito clínico (n = {desenlace_brazos} brazos)"),
    (ES, "sobreviven a cada requisito de una proporción agrupada de éxito clínico (n = {desenlace_brazos} brazos)"),
    # Las tres ultimas que quedaban sin ancla. El pie de la Tabla 4 del
    # manuscrito de la revista NO lo escribe `build_manuscript_tables.py`
    # --ese numera las tablas de otra manera-- y por eso seguia en 103.
    (ES, "de los {desenlace_brazos} brazos de esta literatura, **ninguno reúne a la vez"),
    (ES, "Que {estudios_solo_registro} de {estudios} estudios sean fichas de registro"),
    (JSR, "Completitud de reporte de los cinco desenlaces declarados (n = {desenlace_brazos} brazos)"),
    (JSR, "que {estudios_solo_registro} de {estudios} estudios identificados no han publicado resultados"),
    # La composicion por diseno iba entera tecleada, y el «4 ensayos no
    # aleatorizados» se volvio falso al salir EST-063. Ahora cada diseno tiene
    # su escalar.
    (ES, "**{casos_unicos} reportes de caso único ({casos_unicos_pct} %)**, {diseno_case_series} series de casos, {diseno_prospective_cohort} cohortes prospectivas, {diseno_RCT} ensayos aleatorizados, {diseno_non_randomised_trial} ensayos no aleatorizados y {diseno_retrospective_cohort} cohortes retrospectivas"),
    (ES, "Los comparativos suman **{estudios_comparativos} estudios, el {estudios_comparativos_pct} %** del total"),
    (JSR, "**{casos_unicos} reportes de caso único ({casos_unicos_pct} %)**, {diseno_case_series} series de casos, {diseno_prospective_cohort} cohortes prospectivas, {diseno_RCT} ensayos aleatorizados"),
    (JSR, "{diseno_non_randomised_trial} ensayos no aleatorizados y {diseno_retrospective_cohort} cohortes retrospectivas"),
    (JSR, "Los ensayos, aleatorizados o no, suman **{estudios_comparativos} estudios, el {estudios_comparativos_pct} %** del total"),
    (ES, "Otros {diseno_no_declarado} no declaran su diseño de forma reconocible en el resumen"),
    (JSR, "Otros {diseno_no_declarado} no declaran su diseño de forma reconocible en el resumen"),
    # Las que quedaban sueltas por el corpus.
    (ES, "la cifra del {texto_completo_pct} % convive con una exclusión"),
    (ES, "La tabla 5 lo resume sobre los {desenlace_brazos} brazos del corpus vigente"),
    (ES, "Esos porcentajes se calculan sobre los {desenlace_brazos} brazos, e incluyen por tanto {desenlace_brazos_sin_texto_completo} de estudios"),
    (JSR, "Esos porcentajes se calculan sobre los {desenlace_brazos} brazos extraídos"),
    (JSR, "el embudo que importa para esa pregunta parte de los {desenlace_brazos} brazos"),
    (ES, "El resultado son {estudios} estudios frente a las decenas"),
    (JSR, "impide leer el corpus como {estudios} conjuntos disjuntos de pacientes"),
    (JSR, "no puede considerarse fiable, porque la categoría no puede asignarse en el **{sin_clase_util_pct} %** de los estudios"),
    (JSR, "se obtuvo el texto completo del {texto_completo_pct} % de los estudios recuperables"),

    # ---- Anadido el 2026-09-22, al ingerir las nueve firmas de la auditoria.
    # Estas frases llevaban cifras que NINGUNA ancla vigilaba: la exclusion de
    # EST-063 movio trece recuentos y aqui seguian los viejos --103 brazos,
    # 137 estudios, 95 recuperables, 74,7 %, 68,9 %-- sin que nada fallara. El
    # sincronizador solo reescribe dentro de frases ancladas, de modo que una
    # frase sin ancla es una frase que envejece en silencio.
    #
    # Van por duplicado a proposito: el maestro y el de la revista dicen lo
    # mismo con otras palabras, y una sola ancla no casa con los dos.
    (ES, "no puede asignarse en el **{sin_clase_util_pct} %** de los estudios: el {sin_clase_de_resistencia_pct} % no la menciona en absoluto y un {clase_mencionada_no_clasificable_pct} % adicional"),
    (JSR, "no puede asignarse en el **{sin_clase_util_pct} %** de los estudios: el {sin_clase_de_resistencia_pct} % no la menciona y un {clase_mencionada_no_clasificable_pct} % adicional"),
    (ES, "es mixto con subgrupo separable, no consta en el **{sin_ambito_de_patogeno_pct} %**"),
    (JSR, "es mixto con subgrupo separable— no consta en el **{sin_ambito_de_patogeno_pct} %**"),
    (JSR, "La **vía de administración** no consta en el **{sin_via_de_administracion_pct} %**"),
    (JSR, "La Tabla 4 lo resume sobre los {desenlace_brazos} brazos del corpus"),
    (ES, "con denominador ({desenlace_adverse_event_n_pct_de_los_brazos} % de los brazos) y la emergencia de resistencia al fago lo que menos ({desenlace_resistance_emergence_n_pct_de_los_brazos} %)"),
    (JSR, "con denominador ({desenlace_adverse_event_n_pct_de_los_brazos} % de los brazos) y la emergencia de resistencia al fago lo que menos ({desenlace_resistance_emergence_n_pct_de_los_brazos} %)"),
    (JSR, "consta con numerador y denominador en el **{desenlace_clinical_success_n_pct_de_los_brazos} %** de los brazos"),
    (ES, "Ese {desenlace_clinical_success_n_pct_de_los_brazos} % es, sin embargo, engañoso"),
    (JSR, "Ese {desenlace_clinical_success_n_pct_de_los_brazos} % es engañoso"),
    (ES, "Se obtuvo el texto completo de **{texto_completo_obtenido} de los {estudios_extraibles} estudios recuperables ({texto_completo_pct} %)**"),
    (JSR, "Se obtuvo el texto completo de {texto_completo_obtenido} de los {estudios_extraibles} estudios recuperables ({texto_completo_pct} %)"),
    (ES, "Casos únicos, {casos_unicos_pct} %; comparativos, {estudios_comparativos_pct} %; sin clase de resistencia asignable, {sin_clase_util_pct} %"),
    (JSR, "{estudios_solo_registro} de los {estudios} identificados existen únicamente como registro"),
    (ES, "solo {desenlace_brazos_agregables_exito_clinico} de los {desenlace_brazos} brazos reúnen los requisitos mínimos para agregar"),
    (ES, "**En {definicion_sin_definicion_operativa} de los {desenlace_brazos} brazos ({definicion_sin_definicion_pct} %) no consta una definición operativa"),
    (JSR, "**En {definicion_sin_definicion_operativa} de {desenlace_brazos} brazos extraídos ({definicion_sin_definicion_pct} %) no consta una definición operativa"),
    (ES, "De los {estudios} estudios, **{estudios_extraibles} tienen publicación recuperable**: {estudios_con_articulo} artículos"),
    # ---- La busqueda SI llevo ventana 2016-2026 (PubMed "2016"[dp]:"2026"[dp],
    # Scopus PUBYEAR, CENTRAL). El manuscrito lo decia al reves hasta el
    # 2026-08-23; ahora la ventana se declara en Metodos y en Limitaciones como
    # la restriccion que es, y el rango ya no se presenta como un hallazgo.
    # ---- validacion del cribado sobre los excluidos. Se ancla entera porque
    # es la cifra mas facil de citar mal: la tasa y su cota no significan nada
    # separadas del tamano de muestra ni del marco.
    (ES, "una muestra aleatoria de {validacion_muestra} de los {validacion_marco} registros excluidos"),
    (ES, "Los {validacion_primera_pasada_incluidos} registros marcados como incluibles en la primera pasada"),
    (ES, "fue del {validacion_tasa_pct} % ({validacion_falsos_negativos} de {validacion_muestra}; IC 95 % exacto, 0,00 a {validacion_ic_sup_pct} %)**, lo que sobre el marco de {validacion_marco} admite hasta {validacion_cota_estudios} registros perdidos"),
    (EN, "a random sample of {validacion_muestra} of the {validacion_marco} records excluded"),
    (EN, "The {validacion_primera_pasada_incluidos} records marked as includable on the first pass"),
    (EN, "was {validacion_tasa_pct} % ({validacion_falsos_negativos} of {validacion_muestra}; exact 95 % CI, 0.00 to {validacion_ic_sup_pct} %)**, which over the frame of {validacion_marco} admits up to {validacion_cota_estudios} lost records"),

    # Se ancla porque esta frase se escribio desde un diccionario truncado y
    # afirmaba 35 donde son 48.
    (ES, "de los {procedencia_declarada} estudios que declaran procedencia, {procedencia_europa_este} son de Rusia, Polonia, Georgia o Ucrania"),

    # ---- doble extraccion. Se ancla entera porque el "98" anterior estaba
    # tecleado y sobrevivio sin avisar a que la segunda revisora pasara de 98 a
    # 122 estudios: el comprobador daba 37 de 37 con una cifra obsoleta dentro.
    (ES, "el segundo extrajo {extraccion_estudios_r2} de ellos, de modo que el {extraccion_doble_pct} % del corpus tiene doble extracción"),
    (ES, "Sobre las {extraccion_filas_comparadas} filas de brazo comparables se registraron {extraccion_desacuerdos} desacuerdos de valor"),
    (ES, "fue del {extraccion_acuerdo_mediano_pct} % de acuerdo mediano y una kappa de Cohen mediana de {extraccion_kappa_mediana} sobre los {extraccion_kappas_informativas} de {extraccion_categoricos_total} campos categóricos en que resulta informativa, con un recorrido del {extraccion_acuerdo_min_pct} % al {extraccion_acuerdo_max_pct} %"),
    (EN, "the second extracted {extraccion_estudios_r2} of them, so {extraccion_doble_pct} % of the corpus is double-extracted"),
    (EN, "Over the {extraccion_filas_comparadas} comparable arm rows, {extraccion_desacuerdos} value disagreements were recorded"),
    (EN, "was {extraccion_acuerdo_mediano_pct} % median agreement and a median Cohen's kappa of {extraccion_kappa_mediana} over the {extraccion_kappas_informativas} of {extraccion_categoricos_total} categorical fields where it is informative, ranging from {extraccion_acuerdo_min_pct} % to {extraccion_acuerdo_max_pct} %"),

    (ES, "hay {extraccion_conflictos_firmados} de {extraccion_desacuerdos} adjudicadas"),
    # El RESTO tambien se ancla. El 14 de septiembre se firmaron las 14 que
    # quedaban abiertas, el escalar de firmadas subio de 525 a 539, y estas
    # frases siguieron diciendo «de las 16 restantes» y «hay 525 de 541»: el
    # sync arreglo el fragmento anclado y dejo intacta la frase de al lado,
    # que decia lo contrario tres palabras despues.
    (ES, "Las {extraccion_cerrados_por_regla} restantes se habían cerrado antes"),
    (EN, "The remaining {extraccion_cerrados_por_regla} had been closed earlier"),
    (JSR, "Hay {extraccion_conflictos_firmados} de {extraccion_desacuerdos} desacuerdos adjudicados. El registro de adjudicación anota un único responsable en {conflictos_resueltos_por_uno} de las {extraccion_desacuerdos} filas y a los dos revisores en {conflictos_resueltos_por_los_dos}"),
    (JSR, "Los {extraccion_cerrados_por_regla} restantes se cerraron por una regla mecánica"),
    (ES, "extracción de datos independiente ({extraccion_estudios_r2} de los {extraccion_estudios_r1} estudios)"),
    (EN, "{extraccion_conflictos_firmados} of {extraccion_desacuerdos} are adjudicated"),
    (EN, "independent data extraction ({extraccion_estudios_r2} of the {extraccion_estudios_r1} studies)"),

    # --- desenlaces, sobre la extraccion adjudicada (seccion 3.5 y tabla 5) ---
    (ES, "Los eventos adversos son lo que más se reporta con denominador ({desenlace_adverse_event_n_pct_de_los_brazos} %"),
    (ES, "la emergencia de resistencia al fago lo que menos ({desenlace_resistance_emergence_n_pct_de_los_brazos} %)"),
    (ES, "consta con numerador y denominador en el {desenlace_clinical_success_n_pct_de_los_brazos} % de los brazos"),
    (ES, "En {definicion_sin_definicion_operativa} de los {desenlace_brazos} brazos ({definicion_sin_definicion_pct} %)", 2),
    (ES, "dejan **{desenlace_brazos_agregables_exito_clinico} brazos de los {desenlace_brazos}**"),
    # El 60 estaba escrito a mano DENTRO del anclaje, asi que el comprobador
    # vigilaba una cifra y dejaba envejecer la de al lado. Ahora las dos son
    # escalares.
    (ES, "En {definicion_establecido_que_no_define} de ellos los revisores lo establecieron leyendo el artículo: {definicion_sin_definicion_declarada} "),
    (ES, "En los {definicion_extraccion_incompleta} restantes la extracción quedó incompleta"),
    (ES, "en {desenlace_diseno_no_clasificable} de los {desenlace_brazos} brazos no puede clasificarse"),
    (ES, "De esos {desenlace_brazos_con_diseno}, **{desenlace_brazos_ensayo} brazos son ensayos**"),
    (ES, "**{desenlace_brazos_cohorte} son cohortes**"),
    (ES, "y son {desenlace_brazos_comparativos} brazos"),
    (ES, "sobre los {desenlace_brazos_legibles} brazos legibles, en {definicion_sin_definicion_en_legibles} ({definicion_sin_definicion_legibles_pct} %)"),
    (EN, "In {definicion_establecido_que_no_define} of them the reviewers established this by reading the article: {definicion_sin_definicion_declarada} "),
    (EN, "In the remaining {definicion_extraccion_incompleta} the extraction is incomplete"),
    (EN, "in {desenlace_diseno_no_clasificable} of the {desenlace_brazos} arms it cannot be classified"),
    (EN, "Of those {desenlace_brazos_con_diseno}, **{desenlace_brazos_ensayo} arms are trials**"),
    (EN, "**{desenlace_brazos_cohorte} are cohorts**"),
    (EN, "and there are {desenlace_brazos_comparativos} arms"),
    (EN, "over the {desenlace_brazos_legibles} readable arms, in {definicion_sin_definicion_en_legibles} ({definicion_sin_definicion_legibles_pct} %)"),
    (EN, "reported with a denominator ({desenlace_adverse_event_n_pct_de_los_brazos} % of arms)"),
    (EN, "emergence of phage resistance the least ({desenlace_resistance_emergence_n_pct_de_los_brazos} %)"),
    (EN, "numerator and denominator in {desenlace_clinical_success_n_pct_de_los_brazos} % of arms"),
    (EN, "In {definicion_sin_definicion_operativa} of the {desenlace_brazos} arms ({definicion_sin_definicion_pct} %)", 2),
    (EN, "leave **{desenlace_brazos_agregables_exito_clinico} of the {desenlace_brazos} arms**"),

    (ES, "De {registros_identificados} registros quedaron {informes_unicos} informes únicos"),
    (ES, "{informes_a_texto_completo} informes formaron {estudios_antes_de_releer} estudios y, al leer los textos completos, **{estudios_excluidos_tras_texto_completo} salieron del corpus**"),
    (ES, "quedan **{estudios}**, {estudios_extraibles} con publicación recuperable."),
    (ES, "esos {informes_a_texto_completo} corresponden a **{estudios_antes_de_releer} estudios evaluados para elegibilidad**"),
    (ES, "**{estudios_excluidos_tras_texto_completo} de ellos salieron del corpus**"),
    (ES, "queda en **{estudios} estudios**, que agrupan {informes_agrupados} informes: {estudios_un_solo_informe} con un solo informe y {estudios_multiinforme} con varios"),
    (ES, "el **{excluidos_tras_texto_completo_pct} %** de los {estudios_leidos_a_texto_completo} estudios cuyo texto completo se pudo leer"),
    (ES, "La **vía de administración** no consta en el **{sin_via_de_administracion_pct} %**"),
    (ES, "Sobre los {desenlace_brazos_legibles} brazos legibles las cifras suben —del {desenlace_adverse_event_n_pct_de_los_brazos} % al {desenlace_adverse_event_n_pct_de_los_legibles} % en eventos adversos, del {desenlace_resistance_emergence_n_pct_de_los_brazos} % al {desenlace_resistance_emergence_n_pct_de_los_legibles} % en resistencia—"),
    (ES, "Se obtuvo el texto completo de {texto_completo_obtenido} ({texto_completo_pct} %)"),
    (ES, "**{texto_completo_obtenido} de los {estudios_extraibles} estudios recuperables ({texto_completo_pct} %)**"),
    (ES, "Los {texto_completo_no_obtenido} restantes siguen sin obtenerse"),
    (ES, "el texto completo se obtuvo para el {texto_completo_pct} % de los estudios recuperables"),
    (ES, "criterio de idioma eliminó {estudios_eliminados_por_idioma} estudios"),
    (ES, "concentra el {comparativos_sin_texto_pct} % de los comparativos"),
    (ES, "el corpus pasaría de {estudios} a {corpus_si_se_excluye_lo_no_recuperado} estudios, los comparativos de {estudios_comparativos} a {comparativos_si_se_excluye_lo_no_recuperado} y los ensayos aleatorizados de {ecas} a {ecas_si_se_excluye_lo_no_recuperado}**"),
    (ES, "**ninguno de los {texto_completo_no_obtenido} tiene hoy una copia de acceso abierto**"),
    (EN, "the corpus would fall from {estudios} to {corpus_si_se_excluye_lo_no_recuperado} studies, comparative designs from {estudios_comparativos} to {comparativos_si_se_excluye_lo_no_recuperado} and randomised trials from {ecas} to {ecas_si_se_excluye_lo_no_recuperado}**"),
    (EN, "**none of the {texto_completo_no_obtenido} has an open-access copy today**"),
    (ES, "Contiene {comparativos_sin_texto} de los {estudios_comparativos} estudios comparativos, el **{comparativos_sin_texto_pct} %**"),
    # La n aparece en dos leyendas, Tabla 1 y Figura 2. Se declaran las dos
    # apariciones a propósito: si un día solo se actualiza una, esto salta.
    (ES, "recuperable (n = {estudios_extraibles} estudios)", 2),
    # Los seis motivos de exclusion por titulo. Se anclan porque esta frase
    # imprimia el desglose del conjunto sin restringir mientras su total salia
    # del conjunto restringido: sumaban 13 456 bajo un total de 13 434.
    (ES, "trabajo de laboratorio o preclínico ({excluidos_titulo_LAB}), organismo distinto sin subgrupo separable ({excluidos_titulo_ORG}), revisión o comentario sin datos primarios ({excluidos_titulo_REV}), no evalúa fagoterapia en pacientes ({excluidos_titulo_OFF}), ámbito veterinario ({excluidos_titulo_VET}) y síntesis secundaria ({excluidos_titulo_SEC})"),
    # El mismo desglose en ingles. NO estaba anclado, y por eso derivo:
    # sumaba 13 456 bajo un total de 13 434, con cinco de las seis cifras
    # equivocadas. Una frase sin ancla en un solo idioma se desincroniza
    # en silencio.
    (EN, "laboratory or preclinical work ({excluidos_titulo_LAB}), other organism without a separable subgroup ({excluidos_titulo_ORG}), review or commentary without primary data ({excluidos_titulo_REV}), does not evaluate phage therapy in patients ({excluidos_titulo_OFF}), veterinary scope ({excluidos_titulo_VET}) and secondary synthesis ({excluidos_titulo_SEC})"),
    # Las decisiones que emitio el modelo. Se anclan porque al escribirlas a
    # mano se colo un recuento que duplicaba las filas de la enmienda.
    (ES, "{decisiones_titulo} decisiones de título y {decisiones_resumen} de resumen"),
    (ES, "no puede asignarse en el **{sin_clase_util_pct} %** de los estudios: el {sin_clase_de_resistencia_pct} % no la menciona en absoluto y un {clase_mencionada_no_clasificable_pct} % adicional"),
    (ES, "resumen {palabras_resumen_es};"),
    (ES, "texto principal {palabras_cuerpo_es}."),

    (EN, "From {registros_identificados} records, {informes_unicos} unique reports remained"),
    (EN, "{informes_a_texto_completo} reports formed {estudios_antes_de_releer} studies and, on reading the full texts, **{estudios_excluidos_tras_texto_completo} left the corpus**"),
    (EN, "leaving **{estudios}**, {estudios_extraibles} with a retrievable publication."),
    (EN, "Full text was obtained for {texto_completo_obtenido} ({texto_completo_pct} %)"),
    (EN, "**{texto_completo_obtenido} of the {estudios_extraibles} retrievable studies ({texto_completo_pct} %)**"),
    (EN, "The remaining {texto_completo_no_obtenido} have not been obtained"),
    (EN, "full text was obtained for {texto_completo_pct} % of the retrievable studies"),
    (EN, "language criterion removed {estudios_eliminados_por_idioma} studies"),
    (EN, "concentrates {comparativos_sin_texto_pct} % of the comparative designs"),
    (EN, "It contains {comparativos_sin_texto} of the {estudios_comparativos} comparative studies, **{comparativos_sin_texto_pct} %**"),
    (EN, "base (n = {estudios_extraibles} studies)", 2),
    (EN, "{decisiones_titulo} title decisions and {decisiones_resumen} abstract decisions"),
    (EN, "cannot be assigned in **{sin_clase_util_pct} %** of studies: {sin_clase_de_resistencia_pct} % do not mention it at all and a further {clase_mencionada_no_clasificable_pct} %"),
    (EN, "abstract {palabras_resumen_en};"),
    (EN, "main text {palabras_cuerpo_en}."),
    # ---- El resumen del manuscrito de la revista. Es lo primero que lee un
    # editor y lo unico que leen muchos, y hasta hoy no lo cubria nada.
    (JSR, "De {registros_identificados} registros quedaron {informes_unicos} informes únicos; {informes_a_texto_completo} informes formaron {estudios_antes_de_releer} estudios evaluados para elegibilidad"),
    (JSR, "de los que {estudios_excluidos_tras_texto_completo} se excluyeron: {excluidos_entre_los_leidos} por el artículo, {excluidos_sobre_la_ficha_de_registro} por la ficha del registro y {excluidos_sin_poder_leer_nada} sin poder leer ninguno"),
    (JSR, "Quedan {estudios} estudios, {estudios_extraibles} con publicación recuperable y {texto_completo_obtenido} con texto obtenido ({texto_completo_pct} %)"),
    (JSR, "De esos {estudios_extraibles}, el {casos_unicos_pct} % son reportes de caso único y el {estudios_comparativos_pct} % tiene diseño comparativo"),
    (JSR, "no puede asignarse desde el resumen en el {sin_clase_util_pct} %. En {definicion_sin_definicion_operativa} de {desenlace_brazos} brazos extraídos ({definicion_sin_definicion_pct} %) no consta una definición operativa"),
    (JSR, "con {extraccion_conflictos_firmados} de {extraccion_desacuerdos} desacuerdos adjudicados"),
    # ---- La procedencia geografica venia de un corpus anterior: decia Rusia 7,
    # Polonia y Georgia 6, y "no consta en 76", cuando son 3, 5 y 58. Nombraba
    # ademas a Iran, que no aparece en ningun estudio del corpus vigente. Las
    # cuatro exclusiones por idioma (IDI) son justo las que bajaron Rusia de 7 a 3,
    # y el parrafo no se recalculo. Se ancla el recuento que mas se cita.
    (JSR, "No consta en {procedencia_no_declarada} de los {estudios_extraibles} estudios"),
    # PRISMA 24c: las dos enmiendas y su efecto. Faltaban enteras en el
    # manuscrito de la revista, que declaraba CERO donde el maestro declara DOS.
    (JSR, "Excluyó **{estudios_eliminados_por_idioma} estudios completos** —el corpus pasó de {estudios_antes_de_la_enmienda} a {estudios_antes_de_releer}—, y la pérdida no fue uniforme: {comparativos_perdidos_por_idioma} de ellos tenían diseño comparativo y {ecas_perdidos_por_idioma} eran ensayos aleatorizados"),
    (JSR, "extendida a los {texto_completo_no_obtenido} que siguen sin texto, el corpus caería de {estudios} a {corpus_si_se_excluye_lo_no_recuperado} estudios, los comparativos de {estudios_comparativos} a {comparativos_si_se_excluye_lo_no_recuperado} y los ensayos aleatorizados de {ecas} a {ecas_si_se_excluye_lo_no_recuperado}"),
    # El riesgo de sesgo simplificado: alcance y numero de celdas. Si manana se
    # consigue el texto del ECA que falta, o se readjudica un diseno, estas
    # frases dejan de ser ciertas y aqui salta.
    (JSR, "identifica **{sesgo_comparativos_adjudicados} estudios con diseño comparativo**, de los cuales **{sesgo_evaluables} son evaluables**: {sesgo_instrumento_RoB2} ensayos aleatorizados con RoB 2 y {sesgo_instrumento_ROBINSI} ensayos no aleatorizados y cohortes con ROBINS-I"),
    # El recuento de juicios se ancla en el parrafo de alcance, que existe
    # tanto con la evaluacion pendiente como terminada. Estuvo anclado en el
    # aviso de PENDIENTE, que desaparece al completarse: al ingerir los 82
    # juicios el comprobador fallaba por una frase que ya no debia existir.
    # LOS 90 NO SON TODOS DE DOMINIO. Un arbitro rehizo la cuenta el 2026-09-16:
    # 3x5 + 9x7 = 78, no 90. Los 12 que faltaban son los juicios globales, uno
    # por estudio. La cifra era correcta y la etiqueta no, que es la manera mas
    # facil de que un recuento correcto parezca inventado.
    (JSR, "La Tabla 5 reúne **{celdas_tabla5} juicios**, y no todos son de dominio: {sesgo_instrumento_RoB2} estudios × {dominios_rob2} dominios de RoB 2 dan {juicios_rob2}, y {sesgo_instrumento_ROBINSI} × {dominios_robins} dominios de ROBINS-I dan {juicios_robins}, de modo que hay **{juicios_de_dominio} celdas de dominio**; las **{juicios_globales}** restantes son los juicios globales"),
    (JSR, "De las {juicios_de_dominio} celdas de dominio, **{juicios_con_veredicto} llevan un veredicto** y **{juicios_sin_informacion} declaran que no hay información suficiente para juzgar**"),
    # LA REGLA DEL JUICIO GLOBAL. Decia 11 de 12 y son 9: ROBINS-I reserva
    # «sin informacion» cuando un dominio lo es y ninguno es grave, de modo
    # que EST-063 y EST-116 tampoco heredan su peor dominio.
    # Reescrita el 2026-09-22: al corregirse los tres globales discordantes
    # ya no hay excepciones que contar, y la frase la genera ahora
    # `build_rob_table.py` en vez de estar escrita a mano.
    (JSR, "Se cumple en los {sesgo_evaluables} estudios evaluados, sin excepciones"),
    # ---- lo que el articulo dice cuando el resumen calla
    (JSR, "De los **{t3_con_texto}** estudios cuyo texto se obtuvo, **{t3_resistance_class_declarado}** declaran una categoría de resistencia asignable (**{t3_clase_declarada_pct} %**) —**{t3_clase_mdr_xdr_pdr}** en MDR, XDR o PDR y **{t3_clase_bajo_umbral}** por debajo del umbral de multirresistencia—, **{t3_resistance_class_no_clasificable}** la mencionan"),
    # ---- lo que acompana a cada juicio: cita, nota o nada
    (JSR, "De los {celdas_tabla5} juicios, **{citas_literales} se apoyan en una cita literal del artículo**, **{notas_del_revisor} en una nota metodológica escrita por los revisores** —una razón, no una cita— y **{juicios_sin_frase} no registran apoyo alguno**"),
    # ---- el solapamiento, con el examen sin terminar declarado
    (JSR, "contiene **{pacientes_duplicados_confirmados} pacientes descritos en más de un estudio**, repartidos entre {estudios_con_paciente_compartido} de los {estudios}"),
    # EST-108 lo declara en su propio texto; el escalar sale de leerlo,
    # no de teclearlo: `est108_frase` guarda la frase que lo dice.
    (JSR, "EST-003 comparte {est003_pacientes_compartidos} de sus pacientes: {est003_con_est070} con EST-070"),
    (JSR, "EST-034 comparte {est034_pacientes_compartidos} pacientes con EST-049, EST-061 y EST-077"),
    (JSR, "afirma que {est108_previamente_publicados} de sus {est108_casos} pacientes se habían publicado antes y remite a {est108_referencias_previas} referencias, de las que **{est108_estudios_citados_en_corpus} son estudios de este corpus** —{lista_est108_estudios_citados_en_corpus_ids}—, que aportan {est108_pacientes_citados_en_corpus} pacientes; a ellos se suma {lista_est108_coincidencias_no_citadas_ids}, publicado después"),
    (JSR, "El examen se hizo sobre los {texto_completo_obtenido} textos completos y reunió {pares_solapamiento_examinados} pares: {pares_solapamiento_por_detector} los marcó un detector por producto, país y cita, y {pares_solapamiento_por_lectura} los encontró la lectura. {pares_solapamiento_confirmados} se confirmaron, {pares_solapamiento_descartados} se descartaron y **ninguno queda sin leer**"),
    (JSR, "impide leer el corpus como {estudios} conjuntos disjuntos de pacientes"),
    # ---- el marco del recribado: titulo MAS resumen
    (JSR, "muestra aleatoria de {validacion_muestra} de los {validacion_marco} registros excluidos en el cribado: {validacion_marco_titulo} en la etapa de título y {validacion_marco_resumen} en la de resumen"),
    (JSR, "El recribado ciego de {validacion_muestra} de los {validacion_marco} registros excluidos en título y resumen"),
    # ---- cuantos brazos aporta cada comparativo
    (JSR, "De los {sesgo_comparativos_adjudicados} estudios clasificados como comparativos, {comparativos_un_brazo} aportaron un único brazo a la extracción y uno aportó {brazos_del_comparativo_mayor}"),
    # ---- reportes y series entre los leidos
    (JSR, "Los reportes y las series de casos —{casos_y_series_leidos} de los {texto_completo_obtenido} estudios leídos— no se evaluaron con instrumento formal"),
    (JSR, "ausente del {sin_criterio_dtr_pct} % de los resúmenes y derivable en {t3_dtr_status_declarado} de los {t3_con_texto} artículos leídos"),
    # ---- el embudo de la proporcion descriptiva, sin el filtro de diseno
    (JSR, "En los {desenlace_brazos} brazos extraídos del corpus **no hay un solo brazo comparador**"),
    (JSR, "dejan **{embudo_prop_numerador} brazos**; la definición operativa del éxito, **{embudo_prop_definicion}**; que el desenlace sea atribuible a *P. aeruginosa*, **{embudo_prop_atribuible}**; la administración terapéutica y no profiláctica no elimina ninguno; y que el desenlace sea una proporción y no un tiempo deja **{brazos_agrupables} brazos de {estudios_agrupables} estudios**"),
    (JSR, "**{brazos_agrupables_n1} de los {brazos_agrupables} ({brazos_agrupables_n1_pct} %) tienen un denominador de un solo paciente**"),
    # ---- de cuantas fuentes depende el corpus
    (JSR, "**{estudios_una_sola_fuente} de los {estudios} estudios incluidos ({estudios_una_sola_fuente_pct} %) los encontró una sola fuente**"),
    # --- EL CUERPO DEL MANUSCRITO DE LA REVISTA ---
    #
    # Estas siete no estaban, y su ausencia costo cara: el 2026-09-15 el cuerpo
    # seguia declarando 184 estudios evaluados, 39 exclusiones, 145 en el corpus
    # y un 77,7 % de eventos adversos, todo superado, mientras el resumen del
    # mismo fichero ya daba las cifras nuevas. Un manuscrito que se contradice a
    # si mismo entre el resumen y los Resultados es lo primero que ve un arbitro.
    (JSR, "Agrupados por estudio, esos {informes_a_texto_completo} corresponden a "
          "**{estudios_antes_de_releer} estudios evaluados para elegibilidad**"),
    (JSR, "De ellos se excluyeron **{estudios_excluidos_tras_texto_completo}**: "
          "{excluidos_entre_los_leidos} tras leer el artículo, "
          "{excluidos_sobre_la_ficha_de_registro} tras leer la ficha completa de su "
          "registro de ensayos y {excluidos_sin_poder_leer_nada} sin poder leer "
          "ninguno de los dos"),
    (JSR, "El cuerpo de evidencia queda en **{estudios} estudios**, que agrupan "
          "{informes_agrupados} informes: {estudios_un_solo_informe} con un solo "
          "informe y {estudios_multiinforme} con varios"),
    (JSR, "De los {estudios} estudios, **{estudios_extraibles} tienen publicación "
          "recuperable**: {estudios_con_articulo} artículos y {estudios_solo_resumen} "
          "que solo existen como resumen de congreso. Los **{estudios_solo_registro} "
          "restantes son únicamente fichas de registro de ensayo**"),
    (JSR, "Se identificaron **{registros_sin_organismo_n} fichas** en esa situación"),
    (JSR, "El resultado son {estudios} estudios, frente a las decenas"),
    (JSR, "Que {estudios_solo_registro} de {estudios} estudios sean fichas de registro"),
    (JSR, "Los eventos adversos son lo que más se reporta con denominador "
          "({desenlace_adverse_event_n_pct_de_los_brazos} % de los brazos)"),
    # Del resumen se ancla el trozo que sobrevive a las tres redacciones
    # --pendiente, terminada y terminada por consenso--, que es el alcance.
    (JSR, "los {sesgo_evaluables} comparativos con texto completo (RoB 2, ROBINS-I)"),
    (JSR, "the {sesgo_evaluables} comparative studies with full text (RoB 2, ROBINS-I)", 1, True),
    (JSR, "From {registros_identificados} records, {informes_unicos} unique reports remained; {informes_a_texto_completo} reports formed {estudios_antes_de_releer} studies assessed for eligibility", 1, True),
    (JSR, "of which {estudios_excluidos_tras_texto_completo} were excluded: {excluidos_entre_los_leidos} on the article, {excluidos_sobre_la_ficha_de_registro} on the registry record and {excluidos_sin_poder_leer_nada} without reading either", 1, True),
    (JSR, "{estudios} studies remain, {estudios_extraibles} with a retrievable publication and {texto_completo_obtenido} with the text obtained ({texto_completo_pct} %)", 1, True),
    (JSR, "Of those {estudios_extraibles}, {casos_unicos_pct} % are single case reports and {estudios_comparativos_pct} % have a comparative design", 1, True),
    (JSR, "cannot be assigned from the abstract in {sin_clase_util_pct} %. In {definicion_sin_definicion_operativa} of the {desenlace_brazos} extracted arms ({definicion_sin_definicion_pct} %) no operational definition", 1, True),
    (JSR, "with {extraccion_conflictos_firmados} of {extraccion_desacuerdos} disagreements adjudicated", 1, True),
]


SIN_MILLAR = {"anio_min", "anio_max"}


def formatea(valor, ingles, clave=None):
    """Como los escribe el manuscrito: miles con espacio, decimal con coma o punto."""
    if isinstance(valor, float):
        s = f"{valor:.1f}"
        return s if ingles else s.replace(".", ",")
    if clave in SIN_MILLAR:
        # Un anio no lleva separador de millar: «2 016» no es un anio, es una
        # cantidad. Agruparlo convierte 2016 en algo que ningun lector reconoce.
        return str(valor)
    if isinstance(valor, str):
        # Escalares ya formateados en origen, como la kappa ("0.30"), que
        # lleva dos decimales por convencion y no uno. Solo se ajusta el
        # separador decimal al idioma; el de millar no aplica.
        return valor if ingles else valor.replace(".", ",")
    s = f"{valor:,}".replace(",", " ")          # espacio duro de millar
    return s


# ---------------------------------------------------------------------------
# CIFRAS ESCRITAS EN LETRA
#
# Un hueco «{letras_estudios}» se resuelve como la palabra y no como el numero.
# Existe porque la seccion 3.1.1 enumera las exclusiones con palabras y ningun
# guardian las miraba: buscan digitos. Al salir EST-063 del corpus el
# 2026-09-22, «Veintinueve», «Veinticuatro» y «Cuatro son protocolos» se
# volvieron las tres falsas sin que nada fallara.
#
# Solo cubre 0-99, que es todo lo que el manuscrito escribe en letra, y
# devuelve la palabra CAPITALIZADA porque en los tres manuscritos estas cifras
# abren la oracion.
# ---------------------------------------------------------------------------
_UNI_ES = ["cero", "uno", "dos", "tres", "cuatro", "cinco", "seis", "siete",
           "ocho", "nueve", "diez", "once", "doce", "trece", "catorce",
           "quince", "diecis\u00e9is", "diecisiete", "dieciocho", "diecinueve",
           "veinte", "veintiuno", "veintid\u00f3s", "veintitr\u00e9s", "veinticuatro",
           "veinticinco", "veintis\u00e9is", "veintisiete", "veintiocho",
           "veintinueve"]
_DEC_ES = {30: "treinta", 40: "cuarenta", 50: "cincuenta", 60: "sesenta",
           70: "setenta", 80: "ochenta", 90: "noventa"}
_UNI_EN = ["zero", "one", "two", "three", "four", "five", "six", "seven",
           "eight", "nine", "ten", "eleven", "twelve", "thirteen", "fourteen",
           "fifteen", "sixteen", "seventeen", "eighteen", "nineteen"]
_DEC_EN = {20: "twenty", 30: "thirty", 40: "forty", 50: "fifty", 60: "sixty",
           70: "seventy", 80: "eighty", 90: "ninety"}


def en_letra(n, ingles):
    """El numero como palabra, capitalizada. Fuera de 0-99 devuelve el digito."""
    n = int(n)
    if not 0 <= n <= 99:
        return str(n)
    if ingles:
        if n < 20:
            p = _UNI_EN[n]
        else:
            d, u = divmod(n, 10)
            p = _DEC_EN[d * 10] + ("-" + _UNI_EN[u] if u else "")
    else:
        if n < 30:
            p = _UNI_ES[n]
        else:
            d, u = divmod(n, 10)
            p = _DEC_ES[d * 10] + (" y " + _UNI_ES[u] if u else "")
    return p[0].upper() + p[1:]


# LISTAS DE ESTUDIOS. «(EST-001 A, EST-003 B, EST-094 A, EST-108 A)» iba
# tecleado en los tres manuscritos y ningun guardian lo miraba: al reclasificar
# la lectura del 2026-09-30 tres brazos por debajo del umbral, la lista habria
# seguido diciendo cuatro. `{coma_x}` une con comas; `{lista_x}` pone «y» o
# «and» antes del ultimo, que es como se escribe en una oracion.
PREFIJOS = ("letras_", "coma_", "lista_")


def escalar_base(clave):
    for p in PREFIJOS:
        if clave.startswith(p):
            return clave[len(p):]
    return clave


def une(v, ingles, con_y):
    v = [str(x) for x in v]
    if not con_y or len(v) < 2:
        return ", ".join(v)
    return ", ".join(v[:-1]) + (" and " if ingles else " y ") + v[-1]


def valor_de(esc, clave, ingles):
    """El valor de un hueco, que puede pedir la palabra en vez del numero."""
    if clave.startswith("letras_"):
        return en_letra(esc[clave[len("letras_"):]], ingles)
    if clave.startswith("coma_"):
        return une(esc[clave[len("coma_"):]], ingles, False)
    if clave.startswith("lista_"):
        return une(esc[clave[len("lista_"):]], ingles, True)
    return formatea(esc[clave], ingles, clave)


SECCIONES = {
    "es": ["## Resumen", "## 1. Introducción", "## 2. Métodos", "## 3. Resultados",
           "## 4. Discusión", "## 5. Conclusiones", "## Declaraciones"],
    "en": ["## Abstract", "## 1. Introduction", "## 2. Methods", "## 3. Results",
           "## 4. Discussion", "## 5. Conclusions", "## Declarations"],
    # El de la revista no lleva numeracion y agrupa discusion y conclusiones,
    # que es como estructura sus articulos Journal of Science and Research.
    # Las tablas y figuras ya NO van en una seccion al final: cada pie esta
    # donde el texto la cita, y el .docx adjunta el CSV o el PNG ahi mismo.
    "jsr": ["## RESUMEN", "## ABSTRACT", "## INTRODUCCIÓN", "## DESARROLLO",
            "## METODOLOGÍA", "## RESULTADOS", "## DISCUSIÓN Y CONCLUSIONES",
            "## DECLARACIONES", "## REFERENCIAS"],
}


def comprueba_secciones(textos):
    """Falla si un manuscrito ha perdido una seccion de primer nivel.

    Existe porque un reemplazo anclado en una frase que aparecia dos veces se
    llevo por delante el resumen a medias, la introduccion entera y dos
    subsecciones de metodos del manuscrito ingles, y NADA aviso: las cifras
    seguian cuadrando, porque las cifras que quedaban eran correctas. Un
    comprobador que solo mira numeros no ve un agujero.
    """
    fallos = []
    for arch, txt in textos.items():
        cod = "en" if arch is EN else ("jsr" if arch is JSR else "es")
        for s in SECCIONES[cod]:
            if s not in txt:
                fallos.append("%s: falta la sección «%s»" % (arch.name, s))
    return fallos


def main():
    esc = json.load(open(ESCALARES, encoding="utf-8"))
    # Los desenlaces salen de la extraccion adjudicada y viven aparte. Se
    # aplanan aqui con prefijo para poder anclarlos por nombre como los demas.
    oc = ESCALARES.parent / "outcome_scalars.json"
    if oc.exists():
        O = json.load(open(oc, encoding="utf-8"))
        for k, v in O.items():
            if not isinstance(v, dict):
                esc["desenlace_" + k] = v
        for campo, d in O["desenlaces"].items():
            for k, v in d.items():
                esc["desenlace_%s_%s" % (campo, k)] = v
        for k, v in O["definicion_exito"].items():
            esc["definicion_" + k] = v
    # El alcance de la evaluacion de riesgo de sesgo tambien vive aparte, y es
    # justo el tipo de cifra que envejece: cambia con cada diseno adjudicado y
    # con cada texto completo que se consiga.
    rb = ESCALARES.parent / "rob_tabla_estado.json"
    if rb.exists():
        R = json.load(open(rb, encoding="utf-8"))
        for k, v in R.items():
            if not isinstance(v, (dict, list)):
                esc["sesgo_" + k] = v
        for k, v in R.get("por_instrumento", {}).items():
            esc["sesgo_instrumento_%s" % k.replace(" ", "").replace("-", "")] = v
    textos = {ES: ES.read_text(encoding="utf-8"), EN: EN.read_text(encoding="utf-8"),
              JSR: JSR.read_text(encoding="utf-8")}
    # el manuscrito usa espacio normal o fino indistintamente; se normaliza
    normal = {k: re.sub(r"[   ]", " ", v) for k, v in textos.items()}

    fallos, ok = comprueba_secciones(textos), 0
    for entrada in AFIRMACIONES:
        archivo, plantilla = entrada[0], entrada[1]
        veces = entrada[2] if len(entrada) > 2 else 1
        ingles = entrada[3] if len(entrada) > 3 else (archivo is EN)
        claves = re.findall(r"\{(\w+)\}", plantilla)
        # «letras_x» pide la palabra de «x»: lo que tiene que existir es x.
        faltan = [c for c in claves if escalar_base(c) not in esc]
        if faltan:
            fallos.append(f"{archivo.name}: escalar inexistente {faltan} en «{plantilla[:56]}…»")
            continue
        esperado = plantilla.format(**{c: valor_de(esc, c, ingles) for c in claves})
        esperado_n = re.sub(r"[   ]", " ", esperado)
        n = normal[archivo].count(esperado_n)
        if n == veces:
            ok += 1
            continue
        if n == 0:
            # ¿está la frase con otro número? Se localiza para poder decirlo.
            molde = re.escape(esperado_n)
            for c in claves:
                molde = molde.replace(re.escape(valor_de(esc, c, ingles)),
                                      r"([\d  .,]+)")
            hallado = re.search(molde, normal[archivo])
            detalle = (f" -- el manuscrito dice «{hallado.group(0)[:80]}»"
                       if hallado else " -- la frase no aparece en absoluto")
            fallos.append(f"{archivo.name}: DESACTUALIZADA «{esperado_n[:70]}»{detalle}")
        else:
            fallos.append(f"{archivo.name}: la frase aparece {n} veces y se "
                          f"esperaban {veces}: «{esperado_n[:60]}». Si el cambio es "
                          f"legítimo, actualiza el recuento en AFIRMACIONES.")

    print(f"afirmaciones ancladas : {len(AFIRMACIONES)}")
    print(f"al día                : {ok}")
    if not fallos:
        print("\ncada cifra reportada lleva el escalar que le toca")
        return 0
    print(f"\nDESAJUSTES ({len(fallos)}):")
    for f in fallos:
        print("   " + f)
    print("\nArréglalo con: python scripts/sync_manuscript_numbers.py --escribir")
    return 1


if __name__ == "__main__":
    sys.exit(main())
