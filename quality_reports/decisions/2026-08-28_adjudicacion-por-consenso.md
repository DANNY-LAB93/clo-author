# Adjudicación por consenso de los desacuerdos de extracción

**Estado:** ADOPTADA
**Fecha:** 28 de agosto de 2026
**Deciden:** D. Valdiviezo y N. Trelles (firmas en el cuaderno)
**Afecta a:** §2.6, S11, S12, escalares `extraccion_*`, `compare_extractions.py`

## Qué ha pasado

Los dos revisores resolvieron por consenso 571 de los 573 desacuerdos abiertos
sobre `ADJUDICACION_conflictos.xlsx`, firmando cada fila con su nombre y la
fecha. De esas 571, **559 se ingirieron** al fichero de conflictos y 12 no.

| | |
|---|---:|
| Desacuerdos totales | 575 |
| **Adjudicados por consenso** | **559** |
| Cerrados por regla, sin firma conjunta | 2 |
| Pendientes | 14 |

## Lo que hubo que normalizar, y lo que no se tocó

Los revisores rellenaron el cuaderno en castellano y el esquema está en inglés.
`scripts/ingest_adjudications.py` traduce **solo** lo que está en su tabla
`EQUIVALENCIAS`, entrada por entrada:

| traducción | n | por qué |
|---|---:|---|
| `NO` → `no` | 21 | solo mayúsculas |
| `no derivable` → `NA` (`route`, `modality`) | 21 | el registro del 11 de agosto define `NA` como «un hueco: significa que no lo sabemos» |
| `no derivable` → `not-derivable` (`dtr_status`) | 2 | el esquema lo tiene literal |
| `Intravenosa` → `IV` | 1 | castellano |
| `topica/local` → `topical/local` | 1 | castellano |

Cualquier otro valor fuera del vocabulario **se rechaza y se informa**; el
script no aproxima al valor más parecido.

## Las 14 que quedan, y por qué

**10 por un fallo del formulario, no de los revisores.** El cuaderno de
adjudicación ofrecía «no derivable» en todos los desplegables. En `study_design`
y `extraction_status` el esquema no tiene ese hueco: no admiten «no lo sé».
Los revisores eligieron una opción que yo puse y que el esquema no acepta.
Elegir por ellos entre `other` y `PARTIAL` sería inventar una respuesta que
nadie dio, así que quedan abiertas.

- `study_design` = «no derivable»: EST-020, EST-059, EST-073, EST-098, EST-115,
  EST-133, EST-157, EST-165, EST-219
- `extraction_status` = «no derivable»: EST-167

**4 que exigen volver al artículo.**

- EST-051 `microbio_eradication_n` = «SI» — el campo pide un recuento
- EST-051 `study_design` — resuelto pero sin firmante
- EST-001 `extraction_status` — sin valor acordado
- EST-043 `adverse_event_n` — sin valor acordado

## Las 2 de `journal_tier`

EST-017 y EST-170 se habían cerrado antes aplicando la regla mecánica R2
—«casilla en blanco en un metadato objetivo»— sobre una comparación que después
se rehizo. Al rehacerla las dos casillas estaban llenas y discrepaban («alto»
frente a «bajo» y «medio»), así que la regla dejó de corresponder y la
resolución quedó arrastrada.

No se borra el valor, porque es el que se usó. Su columna `resuelto_por` pasa a
decir la verdad —«cerrado por regla mecánica sobre una comparación superada;
SIN firma conjunta»— y el escalar `extraccion_conflictos_firmados` las excluye:
**559, no 561**. Contarlas como adjudicadas infla en dos la cifra publicada.

Quedan pendientes de pasar por el mismo consenso que las demás.

## Un riesgo que había y ya no está

`compare_extractions.py` reescribía el fichero de conflictos con las tres
columnas de resolución **en blanco**. Volver a ejecutarlo —que es el comando
documentado en `CLAUDE.md`— habría borrado de un plumazo las 561 firmas. Ahora
las recupera por clave `(estudio, brazo, campo)` antes de escribir, y avisa de
cuántas conserva. Si una recomparación hace desaparecer un desacuerdo, su
resolución desaparece con él: se firmó sobre unos valores concretos.

## Qué cambia en el manuscrito

§2.6 pasa de «hay 2 de 575 adjudicadas» a «hay 559 de 575», con las 16 restantes
desglosadas. Ninguna otra cifra publicada se mueve: las tablas 1 a 4 y la figura
PRISMA siguen saliendo de `cribado/` y de `pre_extraccion_desde_resumen.csv`.

## Lo que esto desbloquea, y lo que no

Con la adjudicación hecha, los cuadernos de extracción **pueden** empezar a
sostener cifras publicadas: desenlaces, riesgo de sesgo, GRADE. Eso es una
decisión de alcance que no se toma aquí.

Lo que no cambia: siguen faltando 31 textos completos, y la fracción que falta
concentra el 47,8 % de los diseños comparativos.


---

# ANEXO al mismo registro — 28 de agosto de 2026, más tarde

## El diccionario de traducción estaba incompleto: 575 → 547

Al construir el conjunto adjudicado se vio que el comparador puntuaba como
discrepancia lo que solo era el mismo valor escrito de otra forma. `VALOR_DE_ES`
no recogía `local/topica`, `intravenosa` ni `fago solo`.

**28 de los 575 «desacuerdos» eran eso**, y la prueba de que nunca fueron
desacuerdos es que los revisores los adjudicaron, uno a uno, exactamente al
valor que los dos ya habían escrito cada uno a su manera (`topica/local` frente
a `local/topica` → resuelto `topical/local`).

Completado el diccionario y rehecha la comparación:

| | antes | ahora |
|---|---:|---:|
| Desacuerdos | 575 | **547** |
| Acuerdo mediano | 78 % | 78 % |
| Acuerdo mínimo por variable | 55 % | **64 %** |
| Kappa mediana | 0,57 | **0,62** |
| Adjudicados por consenso | 559 | **531** |

La corrección mueve la concordancia **hacia arriba**, que es la dirección que
obliga a declararlo en vez de aplicarlo en silencio. No se añadió ninguna
equivalencia dudosa: `estudio observacional` NO se traduce, porque puede ser
cohorte prospectiva, retrospectiva o serie de casos, y elegir una sería decidir
por el revisor.

## Se reportan desenlaces por primera vez

Con la extracción adjudicada, la sección 3.5 y la tabla 5 son las primeras
cifras del manuscrito que dependen de los cuadernos de extracción. Cada una va
acompañada del porcentaje de sus casillas con doble lectura.

| | |
|---|---:|
| Brazos extraídos | 132 |
| Eventos adversos con numerador y denominador | 97 (73,5 %) |
| Mortalidad | 90 (68,2 %) |
| Éxito clínico | 83 (62,9 %) |
| Erradicación microbiológica | 66 (50,0 %) |
| Emergencia de resistencia al fago | 32 (24,2 %) |
| **Brazos sin definición operativa de éxito clínico** | **69 (52,3 %)** |
| Brazos de diseño comparativo | 24 |
| **Brazos que reúnen los cuatro requisitos para agregar** | **3** |

Los tres brazos agregables miden cosas distintas: EST-021 el *tiempo* hasta una
reducción sostenida de carga bacteriana por hisopo; EST-101 la ausencia o
resolución de un síndrome de seis signos sin NAV; EST-146 el alivio sintomático
«con independencia de si la bacteria se detectaba». No hay dos comparables.

## Riesgo de sesgo y GRADE: no se hacen, y por qué

**No se ha evaluado el riesgo de sesgo y la revisión no lo reporta.** Exige que
los dos revisores lean cada artículo y emitan un juicio por dominio; es trabajo
humano pendiente. No se sustituye por ningún indicador derivado del diseño, que
mediría otra cosa. Además, 31 de los 124 estudios siguen sin texto completo, de
modo que una evaluación hecha hoy dejaría fuera una fracción no aleatoria.

**GRADE tampoco.** Califica la certeza de una estimación agrupada, y no hay
ninguna: con 3 brazos agregables no se presenta ninguna proporción común.
Calificar la certeza de un resultado inexistente sería un trámite.

Esto queda declarado en §2.7, no omitido.

## Lo que queda pendiente

- 14 desacuerdos abiertos (10 por el hueco de «no derivable» en el formulario)
- 2 filas de `journal_tier` cerradas sin firma conjunta
- 31 textos completos sin recuperar
- riesgo de sesgo por estudio, cuando se decida acometerlo
