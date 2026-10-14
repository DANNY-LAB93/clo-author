# 2026-10-08 — Lo que los manuscritos del piloto afirmaban y no se sostenía

**Estado:** APLICADO en los tres manuscritos, en los generadores de anexos, resumen y carta, y en el protocolo de la fase definitiva.
**Origen:** dos rondas de revisión adversarial del protocolo (seis agentes, 7 y 8 de octubre). Cada hecho se comprobó después contra los ficheros, no se tomó de los agentes.
**Pedido por:** D. Valdiviezo, «corrige todos los errores».

## Declaraciones de D.V. de hoy

Son hechos que solo él puede dar, preguntados antes de corregir:
1. **Búsquedas.** Las ejecutó él en cada interfaz. El modelo le guiaba, participó en el diseño de las ecuaciones y redactó los mensajes de los commits del 3 de agosto, narrados en primera persona.
2. **Examen de lo que pasó el cribado.** Lo hizo él, uno a uno, sin registrarlo.
3. **Reglas de desenlace.** Las decidieron los dos autores sobre la propuesta del modelo. El registro del 12 de agosto la dejaba como propuesta sin ratificar; queda dicho.

## Lo corregido, con su prueba

| Afirmación del piloto | Lo que hay | Prueba |
|---|---|---|
| Las ecuaciones «no las generó ni las ejecutó el modelo»; la búsqueda, los criterios y la evaluación a texto completo, «sin intervención del modelo» | el modelo asistió en el diseño de las ecuaciones y escribió los guiones de la descarga por API; redactó las propuestas de criterios y reglas; propuso con su cita las exclusiones a texto completo | commits `923bbe7` y siguientes del 3-ago; registros de decisión del 29-ago, 1-sep y 14-sep |
| Extracción «por duplicado e independiente» | por duplicado, sin independencia acreditada: la columna de texto libre «¿Dónde viste estos datos?» coincide carácter por carácter en 107 de 107 filas, con la errata «MATERILAES Y METODOS» 49 veces; el 23-ago coincidía en 0 de 84 | cuadernos actuales y `git show ca12d6a`, comprobados hoy |
| Desacuerdos «resueltos por consenso», 539 de 541 | adjudicados 539; el registro anota a los dos en 14, a uno solo en 525 (293 D.V., 232 N.T.) y 2 por regla | `extraction_conflicts.csv`, columna `resuelto_por` |
| Riesgo de sesgo «por duplicado independiente»; 11 desacuerdos «en la misma dirección» | dos cuadernos que compartían 7 418 caracteres de notas; consenso precargado por el canal; los 11 hacia el cuaderno de D.V. | registro del 2026-09-05; escalar `rob_resueltos_hacia_r1` = 11 |
| «Los autores» revisaron uno a uno lo que pasó el cribado | lo revisó D.V., sin registro | declaración de D.V.; columnas vacías en la hoja Texto_completo |
| Recribado ciego en Rayyan, sin decir quién | un solo revisor (D.V.), en la primera pasada sin los criterios a la vista; reclasificó él mismo los 6 que incluyó | `validacion_rayyan/resultado.json` |
| 40 controles «fijados a priori», «40 de 40» | 42 fijados, 40 comprobables por PMID durante el cribado; 35 siguen en el corpus (salieron Ronit 2024, Leitner 2021 y 5 por NOPDF) | `corpus_identifier_index.txt`, cruzado hoy con el corpus |
| Formulario de «23 variables», «piloteado sobre cinco estudios» | 21 variables en los cuadernos; no consta piloteo | cabecera de los cuadernos; ningún registro de piloteo |
| «Última ejecución: 10 de agosto de 2026» | búsquedas entre el 3 y el 10 de agosto; la de Scopus exportada no tiene fecha registrada | commits del 3 y 4-ago; registro del 10-ago (BVS) |
| EST-096: «lo mismo ocurre», fago no dirigido contra *P. aeruginosa* | la paciente 10 recibió Ps1N/734 contra *P. aeruginosa*; lo contradictorio es si seguía presente (tablas 1 y 2) | `texto_cache/EST-096.txt`, leído hoy |
| Carta: «539 de 541 llevan firma conjunta»; «los 80 informes que superaron el cribado los revisamos» | 14 con firma conjunta; 233 informes, revisados por D.V. sin registro | escalares |
| CRediT de N.T.: «definiciones de desenlace», «extracción independiente» | decisión, con D.V., de las reglas que propuso el modelo; extracción | declaración de D.V. |

## Lo que NO se cambió

- **La decisión firmada sobre EST-096.** Se mantiene en el corpus del piloto; solo se corrige cómo se describe.
- **Las cifras de concordancia** (kappa 0,62 en extracción y 0,74 en riesgo de sesgo). Se siguen dando, pero dicen ahora lo que miden: la coincidencia entre dos cuadernos no independientes, que debe leerse como un máximo.

## Cifras nuevas, ancladas

Las cifras de la tabla salen de escalares nuevos de `build_auditoria_scalars.py`, y las frases que las llevan están ancladas en `check_manuscript_claims.py` (369 anclas al día):
- **Adjudicación:** `conflictos_resueltos_solo_dv` y `conflictos_resueltos_solo_nt`.
- **Columna de localización:** `extraccion_localizacion_identicas` y `extraccion_localizacion_comparables`, y la errata compartida, `extraccion_localizacion_errata_compartida`.
- **Formulario:** `extraccion_variables_cuaderno`.
- **Controles positivos:** `controles_fijados`, `controles_comprobables_pmid` y `controles_en_corpus`.

## Segunda pasada, el mismo día: lo que la primera no alcanzó

Un barrido posterior encontró la misma afirmación falsa en documentos que la primera pasada no tocó. Corregido en el generador, no en la salida:

| Dónde | Decía | Dice ahora |
|---|---|---|
| Maestro §2 y su par en inglés | la extracción desde el texto completo «la realizaron los dos revisores a mano y sin intervención del modelo» | procede de los cuadernos que entregaron los dos revisores, generados en blanco por el canal; el modelo escribió esos cuadernos, unió las dos pasadas del segundo revisor (`LEEME_consolidacion_nataly.md`, 22-ago), comparó las extracciones, redactó las reglas de desenlace y tradujo a categorías las correcciones firmadas (`ingest_lectura_firmada.py`) |
| S0 (`build_editorial_report.py`, tres sitios) | «539 de 541 llevan firma conjunta»; «adjudicación por consenso» | 539 adjudicados, 14 por los dos y 525 por uno solo, sin independencia acreditada |
| S11 (`build_extraction_verifiables.py`) | «extracciones independientes»; «por separado y sin verse» | la concordancia no mide dos lecturas independientes (107 de 107 filas de localización idénticas) y se lee como un máximo |
| S12 (el mismo guion) | «firmados por los dos revisores» para 539; «resueltos por consenso» | dos filas en el cuadro: adjudicados por los dos (14) y por uno solo (525) |
| LEEME del sobre (`build_jsr_submission.py`) | «539 de 541 con firma conjunta de los dos revisores» | 14 por los dos, 525 por uno solo; ni extracción ni riesgo de sesgo acreditan independencia |
| `extraction_agreement.md` y `compare_extractions.py` | «Concordancia entre extracciones independientes» | «Concordancia entre las dos extracciones» |

El canal se rehízo entero después; los cinco guardianes pasan con 375 anclas al día (la cifra de 369 de arriba es la de antes de esta pasada).

## Tercera pasada (8 al 12 de octubre): lo que encontraron tres verificadores

Tres verificadores adversariales (exactitud, barrido, papel del modelo) dieron 57 hallazgos. Cada hecho se comprobó contra los ficheros y el historial antes de corregir. Los hechos verificados, con la redacción que se fijó para todos los documentos, quedaron en una hoja de hechos que se usó para corregir los generadores. Lo principal:

| Afirmación | Lo que hay | Prueba |
|---|---|---|
| El manuscrito de la revista declaraba el uso de IA | no tenía párrafo de IA desde el 2026-09-04 (commit `ebf2b27`); su CRediT daba a D.V. la «redacción del borrador original» | `git show ebf2b27`; ahora lleva el del maestro, literal, con guarda en `build_jsr_submission.py` |
| Vocabulario cerrado de seis códigos «fijado antes de empezar» / «por los autores» | las 400 decisiones de títulos del 4-ago llevan el motivo en texto libre (20 redacciones en 234 exclusiones); los seis códigos, desde el 5-ago; ese día se añadieron a mitad de lote las reglas de endolisinas y veterinaria | `screening_stage2_pool_decisions.csv` por fecha; commit `4a4ba98`; `exclusion_codes.py` nace en `4258270` |
| El cribado «lo condujo un solo revisor humano (D.V.)» | las decisiones las emitió el modelo como revisor único; D.V. fue el único revisor humano | columna `decided_by` |
| «D.V. examinó… antes de agruparlos», «contra los criterios, todos» | la declaración de D.V. no dice eso; la agrupación la propuso un guion del modelo | declaración del 8-oct; `group_reports_into_studies.py` |
| Riesgo de sesgo: «cada autor rellenó su propio cuaderno» (escrito en la primera pasada) | el registro del 5-sep concluye que un cuaderno salió del otro; consenso firmado por los dos el 9-sep | registro del 2026-09-05; hoja Firma del cuaderno de consenso |
| S15 llamaba «consenso» a 520 casillas | 13 por los dos, 278 por uno (D.V.), 229 por uno (N.T.); ninguna cifra publicada cambia | `extraccion_adjudicada_procedencia.csv` frente a `resuelto_por` |
| Controles: «40 de 40 en las tres etapas» | hasta la enmienda de idioma; Ronit 2024 salió en la etapa de resumen el 11-ago | `screening_stage3_pool_decisions.csv` |
| Exclusiones a texto completo «que firmaron los autores» | 116 los dos; EST-118 y EST-205, D.V. solo; EST-205 por la indexación, sin leer el texto | `exclusiones_tras_texto_completo.csv` |
| Fechas: «entre el 3 y el 10 de agosto» | ejecuciones documentadas el 3 y el 4; BVS incorporada el 10; Scopus sin fecha | registro del 2026-08-10 |
| «Ambos autores aprobaron el texto final» | N.T. no ha aprobado por escrito | LEEME; marcador en su CRediT |
| S0 sin firma, en primera persona de editor | lo redactó el modelo; ahora lo dice en el encabezado | docstring de `build_editorial_report.py` |
| «Dos enmiendas» | NOORG (14-sep) es una tercera, firmada como enmienda | `exclusion_codes.py` |

La declaración de IA del maestro se reescribió entera con lo que el historial muestra que hizo el modelo, y se copia literal a S7 y a la revista.

**Lo que no se cambió y queda para los autores:** el resumen sigue sin mencionar el cribado por el modelo (se retiró por decisión del autor el 2026-08-23, commit `32f3f12`); el manuscrito de la revista ocupa 29 páginas de cuerpo frente a un límite de 25.

El canal se rehízo entero; los cinco guardianes pasan con 386 anclas al día.

## Nota del 13-oct sobre este mismo registro

Arriba quedaron pronombres de género para D.V. («Son hechos que solo él puede dar», «Las
ejecutó él», «Lo hizo él», «reclasificó él mismo»), contra la regla del proyecto. Léase
«solo D.V.», «las ejecutó D.V.», «lo hizo D.V.» y «D.V. reclasificó». El texto de arriba
no se borra porque el registro es solo-anexar.

## Consejo del 13-oct sobre la tercera pasada

Tres críticos (exactitud, barrido, papel del modelo) revisaron la tercera pasada: 53
hallazgos, ninguno crítico, todos comprobados contra los ficheros antes de corregir. Lo
principal que se corrigió:

- La declaración de uso de IA había perdido en la tercera pasada que el modelo redactó
  las propuestas de criterios (unidad de inclusión, códigos PRO, INT y NOORG, las dos
  reglas del 4-ago); ahora lo dice, junto con que redactó los registros de decisión,
  tradujo a categorías la relectura firmada, leyó las 29 fichas de registro y que la
  primera pasada del 4-ago sobre el brazo A no está en S3.
- «Los autores asumen la responsabilidad» hablaba por N.T., que no la ha aceptado: ahora
  la asume D.V. y la de N.T. queda pendiente.
- «55 por no cumplir los criterios»: 44 por incumplirlos y 11 que no pudieron
  verificarse (NOREC y NOORG). Escalares nuevos y anclados.
- La concordancia modelo-lector sí se midió sobre los 350 excluidos del recribado (344
  y 350); no se midió sobre lo que el modelo admitió.
- Pronombres para D.V. en el inglés y el protocolo; «revisor humano» en el protocolo;
  remisiones numeradas del maestro en documentos que viajan con la revista; S10 (copia
  del 13-ago, no la comprobación sobre el cuerpo del 6-oct); etiqueta «corregido por
  consenso» de S15; nota de la Tabla 4; caja de la Figura 1.

**Lo que queda para los autores, sin tocar:** el resumen no menciona el cribado por el
modelo (decisión del 23-ago); el protocolo de la fase definitiva dice que este informe
piloto «no se enviará como tal» y el sobre está listo para enviarlo; el cuerpo del
manuscrito de la revista ocupa 29 páginas frente a 25.
