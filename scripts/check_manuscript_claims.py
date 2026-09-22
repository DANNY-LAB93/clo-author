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
    (JSR, "identifica **{sesgo_comparativos_adjudicados} estudios con grupo de comparación**, de los cuales **{sesgo_evaluables} son evaluables**: {sesgo_instrumento_RoB2} ensayos aleatorizados con RoB 2 y {sesgo_instrumento_ROBINSI} ensayos no aleatorizados y cohortes con ROBINS-I"),
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
    (JSR, "En {globales_heredan_peor} de los {sesgo_evaluables} estudios el juicio global se corresponde con sus dominios"),
    (JSR, "Se cumple en {globales_heredan_peor} de los {sesgo_evaluables} estudios evaluados"),
    # ---- lo que el articulo dice cuando el resumen calla
    (JSR, "De los **{t3_con_texto}** estudios cuyo texto se obtuvo, **{t3_resistance_class_declarado}** declaran una categoría de resistencia asignable (**{t3_clase_declarada_pct} %**) —**{t3_clase_mdr_xdr_pdr}** en MDR, XDR o PDR y **{t3_clase_bajo_umbral}** por debajo del umbral de multirresistencia—, **{t3_resistance_class_no_clasificable}** la mencionan"),
    # ---- lo que acompana a cada juicio: cita, nota o nada
    (JSR, "De los {celdas_tabla5} juicios, **{citas_literales} se apoyan en una cita literal del artículo**, **{notas_del_revisor} en una nota metodológica escrita por los revisores** —una razón, no una cita— y **{juicios_sin_frase} no registran apoyo alguno**"),
    # ---- el solapamiento, con el examen sin terminar declarado
    (JSR, "contiene **{pacientes_duplicados_confirmados} pacientes descritos en más de un estudio**, repartidos entre {estudios_con_paciente_compartido} de los {estudios}"),
    # EST-108 lo declara en su propio texto; el escalar sale de leerlo,
    # no de teclearlo: `est108_frase` guarda la frase que lo dice.
    (JSR, "afirma que {est108_previamente_publicados} de sus {est108_casos} pacientes se habían publicado antes"),
    (JSR, "produjo {pares_solapamiento_examinados} pares candidatos, de los que {pares_solapamiento_confirmados} se confirmaron leyendo, 3 se descartaron, 1 quedó sin resolver y **{pares_solapamiento_sin_leer} siguen sin leer**"),
    # ---- el marco del recribado: titulo MAS resumen
    (JSR, "muestra aleatoria de {validacion_muestra} de los {validacion_marco} registros excluidos en el cribado: {validacion_marco_titulo} en la etapa de título y {validacion_marco_resumen} en la de resumen"),
    (JSR, "El recribado ciego de {validacion_muestra} de los {validacion_marco} registros excluidos en título y resumen"),
    # ---- cuantos brazos aporta cada comparativo
    (JSR, "De los {sesgo_comparativos_adjudicados} estudios clasificados como comparativos, {comparativos_un_brazo} aportaron un único brazo a la extracción y uno aportó {brazos_del_comparativo_mayor}"),
    # ---- reportes y series entre los leidos
    (JSR, "Los reportes y las series de casos —{casos_y_series_leidos} de los {texto_completo_obtenido} estudios leídos— no se evaluaron con instrumento formal"),
    (JSR, "derivable en {t3_dtr_status_declarado} de los {t3_con_texto} artículos leídos"),
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
        faltan = [c for c in claves if c not in esc]
        if faltan:
            fallos.append(f"{archivo.name}: escalar inexistente {faltan} en «{plantilla[:56]}…»")
            continue
        esperado = plantilla.format(**{c: formatea(esc[c], ingles, c) for c in claves})
        esperado_n = re.sub(r"[   ]", " ", esperado)
        n = normal[archivo].count(esperado_n)
        if n == veces:
            ok += 1
            continue
        if n == 0:
            # ¿está la frase con otro número? Se localiza para poder decirlo.
            molde = re.escape(esperado_n)
            for c in claves:
                molde = molde.replace(re.escape(formatea(esc[c], ingles, c)),
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
