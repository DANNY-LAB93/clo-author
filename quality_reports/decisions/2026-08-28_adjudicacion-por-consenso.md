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

---

# SEGUNDO ANEXO — 29 de agosto de 2026

## La revisión adversarial encontró que el hallazgo estaba mal por dos sitios

Un concejo de cuatro lentes sobre el análisis de desenlaces devolvió 37
hallazgos. Seis de sus refutadores murieron por límite de sesión, así que los
materiales se verificaron a mano. Dos afectaban a la cifra publicada, y los dos
iban en la dirección que **ablanda** el hallazgo, que es la que obliga a mirar
con más dureza.

### 1. «na» contaba como definición operativa: 52,3 % → 67,4 %

`build_outcome_scalars.py` solo descartaba el texto literal
«SIN DEFINICIÓN OPERATIVA». En 20 brazos el campo valía `na`, que es el token
de dato ausente que declara el propio esquema, y los dos revisores lo
escribieron por separado. El script los sumaba a «con definición».

Corregido, y desglosado, porque no todo el que no define lo hace por lo mismo:

| | n | % de 132 |
|---|---:|---:|
| Con definición operativa | 43 | 32,6 |
| El artículo no la da (declarado por los revisores) | 58 | 43,9 |
| Campo sin dato (`na`) | 2 | 1,5 |
| Extracción incompleta: no consta ni lo uno ni lo otro | 29 | 22,0 |
| **Sin definición operativa** | **89** | **67,4** |

La distinción del último bloque importa: en 29 brazos **no se puede afirmar que
los revisores concluyeran nada**, porque no terminaron de leer el artículo. La
redacción anterior decía «los dos revisores concluyeron, por consenso», y de 69
brazos eso solo era cierto en 60. Corregido en los dos manuscritos.

### 2. Uno de los «3 brazos» es PhagoBurn, y §3.6 dice que no reporta proporción

§3.5 contaba EST-021 entre los 3 brazos que reúnen numerador, denominador,
diseño comparativo y definición. §3.6, doce líneas más abajo, dice que el
desenlace principal de PhagoBurn es el **tiempo** hasta una reducción sostenida
de la carga bacteriana y que por eso no entra en un metaanálisis de
proporciones. Las dos cosas no pueden ser ciertas.

Lo son las dos por separado: PhagoBurn cumple los cuatro requisitos formales
**y** su desenlace no es una proporción. Así que el embudo tiene un paso más, y
el manuscrito ahora lo dice: de los 3 que cumplen los cuatro requisitos, **queda
2** que reporten algo agregable como proporción. Y los dos definen el éxito de
forma distinta.

### 3. Tres defectos menores, corregidos también

- **Dos brazos con numerador mayor que su denominador** (13 éxitos sobre 1
  paciente en EST-003; 5 eventos adversos sobre 4 en EST-077). Entraban en la
  completitud como proporciones válidas. Ahora se señalan como error de reporte
  y quedan fuera del cruce de agregables.
- **30 de los 132 brazos no tienen diseño clasificable** (20 con «NA» acordado,
  10 abiertos). «24 comparativos» es un suelo sobre 102, no un total sobre 132,
  y la tabla 5 y §3.5 lo dicen.
- **Seis contradicciones de texto** que el commit anterior dejó sueltas: §2.4
  seguía diciendo que la pre-extracción es «la fuente de toda cifra»; §4.4 que
  «este informe no presenta desenlaces»; §2.8 remitía a §3.5 tras renumerarla;
  el manuscrito inglés no tenía actualizada §2.6 ni el pie de la tabla 5; y S1
  conservaba en los ítems 9, 11, 15, 18, 19, 20 y 22 promesas que §2.7 ya había
  retirado.

## Lo que NO cambia

La conclusión, que sale reforzada: el corpus no admite una síntesis cuantitativa
de eficacia, y ahora la cifra que lo demuestra es 2 brazos de 132, no 3.

---

# TERCER ANEXO — 29 de agosto de 2026, los 26 hallazgos restantes

Los seis refutadores del concejo murieron por límite de sesión, así que sus 26
hallazgos quedaron sin verificar. Verificados a mano uno a uno: **25 reales, 1
falso**.

## El falso

El agente afirmó que §3.2 dice 31 estudios sin texto completo y la extracción
marca 32. **S5 y el escalar coinciden en 31.** El agente contó mal.

## Lo que había mal, por tronco

### El fusionador trataba el mobiliario del formulario como datos

Las ocho columnas de navegación que el formulario trae prerrellenadas —`Nº`,
`Pos.`, título, revista, año, tipo, cómo encontrarlo, abrir artículo— entraban
como variables extraídas. Consecuencias, todas medidas:

| | antes | ahora |
|---|---:|---:|
| Campos en el conjunto | 29 | **21** (los del esquema) |
| Casillas con dato | 3 826 | **2 754** |
| Doble lectura | 95,1 % | **94,3 %** |
| Casillas abiertas | 17 | **16** |

Las 16 abiertas cuadran ahora exactamente con el fichero de conflictos (14 sin
resolver + 2 cerradas por regla). La 17.ª era el título de EST-075.

Además, `casillas_con_dato` restaba las «vacío» pero no las ABIERTO, que
también salen vacías, y el aviso «FUERA DEL VOCABULARIO» decía «los dos
coincidieron» contando 16 celdas que leyó uno solo.

### El plegado para comparar se estaba publicando

`normaliza` pasa el texto libre a minúsculas para poder compararlo. El
fusionador guardaba **ese** valor, así que «Bélgica» salía como «belgica» en el
fichero que se entrega: 392 celdas. Ahora los categóricos se guardan en su forma
canónica —que es el dato— y el texto libre y los números conservan lo que
escribió el revisor.

### 6 desacuerdos más que eran solo una tilde

`geographic_source`: «Bélgica»/«Belgica», «Irán»/«Iran». `normaliza` plegaba
mayúsculas pero no tildes en los campos de TEXTO. Corregido:

    desacuerdos 547 -> 541 | adjudicados 531 -> 525 | 525 + 2 + 14 = 541

Es la segunda corrección que **sube** la concordancia. Declarada igual que la
primera.

### La tabla 5 confundía silencio con hueco documental

Los porcentajes se calculaban sobre los 132 brazos, de los que 31 pertenecen a
estudios sin texto completo: nadie pudo extraer nada de ellos. La tabla contaba
ese hueco nuestro como si el artículo hubiera callado —y §2.7 declina el riesgo
de sesgo por esos mismos 31 textos, así que el manuscrito se contradecía.

Ahora la tabla da **dos denominadores**:

| Desenlace | de 132 | de 101 legibles |
|---|---:|---:|
| Éxito clínico | 62,9 % | 80,2 % |
| Erradicación | 50,0 % | 63,4 % |
| Mortalidad | 68,2 % | 84,2 % |
| Eventos adversos | 73,5 % | 84,2 % |
| Resistencia al fago | 24,2 % | 31,7 % |

### El denominador de la erradicación no es el del brazo

El esquema declara `microbio_eradication_denom` (a cuántos se les hizo cultivo
de control) y `microbio_eradication_sustained`. **Ninguno llegó a los
cuadernos**: se añadieron el 12 de agosto, con los formularios ya repartidos.
La fila usa por eso `n_arm`, que sobreestima el denominador. Declarado en la
nota de la tabla en vez de callado.

### «Comparativo» describe el estudio, no el fichero

De los 24 brazos comparativos, solo 5 pertenecen a un estudio con más de un
brazo extraído, y **ninguno de los 3 agregables tiene aquí su comparador**: la
extracción se hizo por brazo y se extrajo el de fago. Para una proporción de un
solo brazo basta; para cualquier cosa que se llame «comparado con qué», no.
Dicho en la nota.

### Cosas menores, todas corregidas

- «El formulario, con 31 variables» → son **23**; las otras 8 son navegación.
- `check_manuscript_numbers.py` no conocía `outcome_scalars.json` y su recorrido
  bajaba un solo nivel: 12 cifras de §3.5 salían SIN RESPALDO. Ahora 4, y las 4
  son anteriores a este trabajo.
- `sync_manuscript_numbers.py` reventaba con KeyError al citar un escalar de
  desenlace, porque comparte la lista de afirmaciones y no aplanaba el fichero.
- Un párrafo fósil en el §2.6 inglés decía «Extraction **is planned to be**
  independent and in duplicate» dos párrafos antes del mismo texto en pasado.
- El comentario de `VALOR_DE_ES` decía que los revisores escribieron las seis
  variantes; escribieron cuatro. Las dos con tilde van por si acaso.
- Las celdas de una sola lectura entraban sin normalizar mientras las de acuerdo
  salían canónicas: la misma respuesta aparecía de dos formas en la columna.
- El docstring del fusionador decía «las 14 casillas»; el script produce las que
  produce y ahora lo dice al terminar.

---

# CUARTO ANEXO — 29 de agosto de 2026, el concejo de dos árbitros

Dos árbitros —uno de dominio clínico, otro de PRISMA— leyeron el manuscrito
entero. **Los dos: revisión mayor.** Verifiqué a mano cada objeción material.

## Lo que tumbaron: el titular descansaba en dos brazos inelegibles

El artículo decía «quedan 2». Los dos incumplen los criterios que la propia
§2.2 declara:

| | por qué no es elegible |
|---|---|
| **EST-101** | «…to **Prevent** Ventilator-Associated Pneumonia in Children». Es profilaxis, y §2.2 exige administración **terapéutica**. Su desenlace —ausencia de NAV incidente— no mide lo mismo que curar una infección establecida. |
| **EST-146** | su propia fila anota «el artículo no separa los datos de *P. aeruginosa*», que es exactamente la condición que §2.2 pone para admitir un estudio mixto. Su numerador cuenta pacientes de varias especies. |

Ninguna de las dos es una interpretación mía: la primera está en el título del
artículo, la segunda la escribieron los revisores en la extracción.

**El embudo, con §2.2 aplicada:**

| requisito acumulado | quedan |
|---|---:|
| brazos extraídos | 132 |
| diseño comparativo | 24 |
| numerador y denominador coherentes | 8 |
| definición operativa del éxito | 3 |
| desenlace atribuible a *P. aeruginosa* | 2 |
| administración terapéutica, no profiláctica | 1 |
| reporta una proporción, no un tiempo | **0** |

**Ningún brazo del corpus** reúne a la vez las condiciones aritméticas y los
criterios de elegibilidad. Es un resultado más fuerte que «quedan 2», no más
débil. Nueva tabla 6.

## Lo que queda en manos de los dos revisores

Si EST-101, EST-039 y EST-086 —los tres estudios de profilaxis extraídos— y los
**22 brazos** cuya extracción anota «el artículo no separa los datos de
*P. aeruginosa*» debieron entrar en el corpus es una **decisión de cribado**,
no de un script: cambiaría los 184 estudios y el diagrama PRISMA. Aquí solo se
aplica §2.2 al cruce que decide si algo es agregable, que es donde la pregunta
se vuelve aritmética.

Nótese la distinción: `incomplete_reason` es una nota de extracción («no pude
sacar este desenlace»), no necesariamente un juicio de elegibilidad («este
estudio no debió entrar»). Un estudio puede tener población separable y aun así
no reportar los desenlaces por patógeno.

## «Comparativo» significaba dos cosas

§3.3 y la Tabla 1 llaman comparativos solo a los ensayos: **23 estudios**.
§3.5 y la Tabla 5 incluían además las cohortes: **24 brazos**. Un lector que ve
23 y 24 supone que son el mismo conjunto. No lo son: 13 ensayos y 11 cohortes.
Ahora los dos sentidos se nombran y se publican por separado.

## Dos huecos del paquete

- **S3 entregaba 13 917 decisiones de título** contra las 13 894 que declara el
  manuscrito. Las 23 de más son decisiones sobre registros de una versión
  anterior del corpus; el registro es solo-anexar y se conservan, pero iban sin
  marcar y un árbitro las contó. Ahora llevan `en_corpus_actual`, igual que S9.
  El «huérfano» Rd069723093 —avanzó de título y nunca tuvo decisión de resumen—
  es una de esas 23.
- **La extracción adjudicada no viajaba.** §3.5 y las tablas 5 y 6 salen de un
  fichero que el paquete no contenía: solo iba S4, la pre-extracción. Un árbitro
  no podía comprobar ni el 89/132 ni el embudo. Ahora son **S14** (un valor por
  casilla) y **S15** (la procedencia de cada casilla).

## Y una cifra que faltaba

El 67,4 % sin definición operativa no llevaba doble denominador, siendo la que
sostiene el hallazgo, mientras las otras cinco filas de la Tabla 5 sí lo llevan.
Sobre los 101 brazos legibles es **58,4 %**. Añadido.

## Lo que los árbitros NO objetaron

El árbitro de dominio comprobó S5 y no echa en falta ningún ensayo ni serie
emblemática: están PhagoBurn, Leitner, CYPHY, BX004, TP-102, PASA16, la serie
del Eliava, el centro israelí y los 100 casos de Pirnay. Y considera la
conclusión general justificada. Lo que no se sostenía era la cadena numérica.

## Sigue pendiente, del informe de métodos

- La validación de Rayyan no nombra quién recribó ni quién adjudicó los 6
  discrepantes, y no separa por etapa (solo ~6 de los 350 vienen del resumen).
- La incoherencia RoB / Tabla 5 sigue en pie a juicio del árbitro: si hacen
  falta dos lectores y faltan 31 textos para el riesgo de sesgo, valdría igual
  para la Tabla 5, que sí se publica.
- Una segunda enmienda no declarada, en S13.
