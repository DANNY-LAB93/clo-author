# Solo estudios con el PDF completo: NOREC se generaliza

**Estado:** APLICADO en los datos el 6 de octubre de 2026; la prosa de los tres
manuscritos se reescribe a continuación.
**Viene de:** D. Valdiviezo pidió ese día un criterio de exclusión nuevo, «PDF que
no posean acceso completo», con alcance a los artículos sin texto, a los resúmenes
de congreso y a las fichas de registro sin artículo, y con el sesgo de recuperación
declarado como efecto. Firmado por DANNY JAVIER VALDIVIEZO VERDUGO y NATALY
ELIZABETH TRELLES AVILA en `FIRMAR_texto_completo_2026-10-06.xlsx` («APROBAR»;
motivo: «NO SE PUEDE LEER PDF»). Copia en `revision_sistematica/lectura_pendiente/`.
**Ficheros:** `exclusion_codes.py` (código NOPDF, el duodécimo),
`make_firma_nopdf.py`, `ingest_firma_nopdf.py`, `build_synthesis_scalars.py`
(escalares `criterio_texto_*`; los diseños existen siempre aunque valgan 0),
`build_manuscript_tables.py` (Tabla 3 nueva).

## Lo que cambia

63 estudios salen con NOPDF: 18 artículos cuyo texto no se obtuvo, 3 resúmenes de
congreso y 42 fichas de registro. Corpus 128 → **65 estudios**, todos con el texto
completo leído; 73 brazos; 118 exclusiones tras el texto completo.

**El efecto del criterio, medido** (Tabla 3, ahora «incluidos frente a excluidos por
no tener el texto»): de los 25 artículos y resúmenes excluidos por no tener el texto
(NOREC y NOPDF), 7 son diseños comparativos según su resumen —el 77,8 % de los 9 que
había— y 5 son ensayos aleatorizados de 7. Declaran 316 pacientes, frente a 348 de
los incluidos. A eso se suman las 42 fichas de registro. La recuperación de texto
completo es del 100 % por construcción.

## Cómo se presenta, y por qué no de otra forma

D. Valdiviezo pidió dos veces presentarlo «como parte del inicio del protocolo, no
como enmienda», porque el manuscrito es todavía un borrador. No se hace: el criterio
se decidió con el cribado y la extracción terminados, el manuscrito afirma que los
criterios se fijaron antes del cribado y que el registro de decisiones fechado lo
acompaña, y ese registro y el historial lo fechan el 6 de octubre. Declararlo como
previo sería describir un procedimiento que no ocurrió.

Lo que sí se hace: en la tabla de criterios figura junto a los demás, sin marca; en
la sección de enmiendas no es una tercera enmienda sino la **ampliación de la
segunda** (NOREC, 2 de septiembre), con su fecha en una frase y su efecto medido.

## Lo que el manuscrito decía y deja de ser cierto

Que NOREC no se generalizaba porque vaciaría la medida del sesgo de recuperación.
Ahora se generalizó; la medida se conserva como efecto del criterio y la limitación
se reescribe para decir lo que cuesta.

---

## 2026-10-07 — Los tres manuscritos, reescritos para el corpus de 65

Entrada añadida; lo de arriba no se toca.

**Cómo queda presentado.** En la Tabla 1 el criterio figura junto a los demás, sin
marca, en una sola fila con NOREC («Estudios sin el texto completo del artículo en
PDF: no recuperado, o disponible solo como resumen de congreso o ficha de registro de
ensayo clínico»); la fila de inclusión que admitía fichas de registro y resúmenes
desaparece. En la sección 2.9 del maestro y del inglés, y en «Enmiendas al protocolo»
del de la revista, es la **ampliación de la segunda enmienda**, con su fecha (6 de
octubre de 2026, con el cribado y la extracción terminados) y su efecto medido: 67
estudios fuera contando NOREC, 7 de 9 diseños comparativos (77,8 %), 5 de 7 ensayos
aleatorizados. El texto dice expresamente que se declara con su fecha «en lugar de
presentarse como si hubiera regido desde el principio». La carta de presentación lo
dice también. La petición de D.V. de presentarlo como criterio inicial sigue sin
aplicarse, por lo que consta arriba.

**Qué cambió en la prosa.** Resumen, unidad de inclusión, §2.6 (doble extracción: el
98 % es de lo extraído; del corpus vigente, 65 de 65), §2.7, §2.9, §3.1, §3.1.1 (un
párrafo nuevo para los 63 NOPDF, de los que no se afirma que incumplan nada), §3.2 (la
recuperación se mide justo antes del criterio: 65 de 86, 75,6 %; la de hoy es del
100 % por construcción), §3.3, §3.4, §3.5 (desaparecen los «brazos legibles» y el
segundo denominador), §3.6 (el embudo: 2 → 1 → 1 → 0), Discusión, Implicaciones y las
limitaciones primera y quinta (cuarta en la revista). Las tablas 2 y 5 pierden la
columna que repetía la anterior cifra por cifra.

**Errores que salieron al hacerlo, y se corrigieron.**
- La Tabla 1 y el resumen de la revista daban como ventana de búsqueda «2017-2026»:
  tomaban el estudio más antiguo del corpus (`anio_min`), que al salir los NOPDF pasó
  de 2016 a 2017. La ventana es el filtro de la búsqueda; ahora sale de
  `fetch_screening_corpus.py` (escalares `ventana_desde`, `ventana_hasta`).
- La conciliación contaba 12 comparativos evaluables donde la Tabla 5 tiene 9: incluía
  los juicios de estudios ya excluidos (EST-055, EST-063, EST-132).
- El manuscrito de la revista desglosaba los estudios de fuente única como «20 solo
  Cochrane CENTRAL, 9 solo ClinicalTrials.gov, 5 solo el brazo B de Scopus, 4 solo
  PubMed y 2 solo CTIS» —suma 40— junto a un total anclado de 6. El dato es 4 PubMed
  y 2 brazo B de Scopus; la frase la arma ahora el canal (`una_sola_fuente_desglose`).
- El cuerpo de la revista arrastraba cifras viejas sin ancla: «11» sin *P. aeruginosa*
  (son 16), «4» protocolos (5), «21 brazos» (19), «42 denominadores de uno» (38),
  «solo uno de cada nueve es un ensayo». Corregidas y ancladas.
- El año de publicación decía «2016–2026, el 80,0 % desde 2020» sin ancla: son
  2017–2026 y 86,2 %.
- «Ninguno reúne las condiciones aritméticas y los criterios de elegibilidad» era
  falso para PhagoBurn, que cumple los dos y cae por la métrica (mide un tiempo). Se
  añade «y la métrica».

**Guardianes al cerrar.** 347 anclas al día; ninguna cifra sin origen en los tres
manuscritos; la aritmética cuadra; coherencia del canal sin fallos; `audita_cifras`
reproduce las 17 cifras. Documentos derivados, sobre y `.zip` rehechos.
