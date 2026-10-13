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
