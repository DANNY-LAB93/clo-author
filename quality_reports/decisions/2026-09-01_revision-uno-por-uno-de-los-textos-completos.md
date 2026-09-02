# Revisión uno por uno de los 93 textos completos

**Estado:** INFORME — las exclusiones las deciden los dos revisores
**Fecha:** 1 de septiembre de 2026
**Ficheros:** `revision_sistematica/verificacion_texto_completo/hallazgos.csv`,
`scripts/cache_fulltext.py`, `scripts/evidencia_intervencion.py`,
`scripts/evidencia_diseno.py`

## Qué se hizo, y en qué se diferencia de lo anterior

El 29 de agosto se presentó como «barrido de los 124 estudios» algo que no lo
era: un script contaba apariciones de «aeruginosa» y miraba una ventana de
±130 caracteres. Ese filtro **falló en 2 de los 11 que marcó** (EST-135 y
EST-184 sí tenían el patógeno en el paciente), solo miraba estudios con tres
menciones o menos, y presumía de una cobertura de 124 textos que no existe.

Cobertura real, medida: **93 legibles y 31 sin texto completo**, coincidiendo
con el 93/124 que el manuscrito ya declara. Los 31 no son revisables contra
nada.

Ahora se extrajo el texto de cada artículo una vez a disco
(`cache_fulltext.py`) y se leyó estudio por estudio. Los scripts de evidencia
**no dictaminan**: sacan las frases donde se dice qué se administró y qué tipo
de documento es, y la lectura la hace una persona. Ese fue justamente el fallo
del barrido anterior.

## Resultado: 22 de los 93 tienen un problema

### La intervención no es un fago (2)

- **EST-017** — el agente es «Inducen-Res®», una solución oral *«imprinted with
  the induction signatures required to induce diverse populations of native
  monovalent and polyvalent phages»*. **No se administra ningún fago**: se
  afirma inducir los del propio paciente. Del centro «Bioregulatory Medicine».
  Y además el paciente **no tenía diagnóstico**: *«despite not having a primary
  diagnosis of the specific types of infections involved… could be
  anticipated»*.
- **EST-199** — *«Successful use of a phage **endolysin**»*. Una endolisina es
  una enzima derivada del fago, no un bacteriófago. 79 menciones de «lysin».

### El fago nunca se administró (1)

- **EST-037** — shock séptico por *P. aeruginosa* PDR. El fago aparece nueve
  veces, todas como opción indisponible: *«Experimental therapies, including
  bacteriophages… remain unavailable in most clinical settings»*.

### No es un estudio de fagoterapia (1)

- **EST-185** — mediastinitis esternal en trasplantados, algoritmo
  reconstructivo. **Una** mención de fago en 43 000 caracteres, en una celda de
  tabla junto a ocho antimicrobianos.

### Protocolos sin resultados (4)

**EST-035** (Trials 2022, «will be» ×99), **EST-052** (CYPHY Yale, versión 11,
×223), **EST-083** (PHAGEFORCE), **EST-122** (STAMP, ×80). Dicen lo que se
hará. No hay desenlaces.

### Sin pacientes (3)

- **EST-020** — *«C57BL/6J mice were ventilated… in a murine model»*.
- **EST-093** — *«24 h static time kills and… 7-day hollow fibre infection
  model»*.
- **EST-041** — artículo de métodos: *«an efficient modular pipeline»* de
  preparación de fagos.

### No es un estudio primario (1)

- **EST-060** — *«Opinion… Personal Experience and Literature Review»*.

### *P. aeruginosa* no está en el paciente (9)

EST-076, EST-086, EST-101, EST-126, EST-130, EST-131, EST-159, EST-178,
EST-212. Detalle en `2026-08-29_pseudomonas-en-el-producto-no-en-el-paciente.md`.

### PDF equivocado, artículo localizado (1)

- **EST-207** — el fichero tiene el final de un artículo de insuficiencia
  cardíaca, pero también la cabecera del artículo pretendido. Identificado y
  confirmado en PubMed: Exarchos V, Tkhilaishvili T, Potapov E, Starck C,
  Trampuz A, Schoenrath F. *Successful bacteriophage treatment of infection
  involving cardiac implantable electronic device and aortic graft: a Trojan
  horse concept.* **Europace 2020;22(4):597. DOI 10.1093/europace/euz319**
  (PMID 31740948). Pedirlo por ese DOI, no por número de página. Es un
  artículo de **una página**.

## La modalidad, aparte

De 132 brazos: **81 fago+antibiótico, 19 monoterapia, 32 sin codificar**. Los
32 no son dejadez: **27 de ellos no tienen texto completo que leer**.

Cuatro de los 19 «monoterapia» **no lo son según su propio artículo**:

- **EST-019** — *«maintaining the standard-of-care antibiotics during the
  treatment»*.
- **EST-085** — la figura rotula *«the application of phage and antibiotics»*, y
  el antibiótico *«was completely stopped at April 14»*: lo había.
- **EST-038** — *«bacteria, which were targeted by antibiotics as well as by
  phages»*.
- **EST-178** — *«**adding** of polyvalent bacteriophage»* dentro de una
  estrategia de prescripción diferida de antibióticos.

Y **EST-118**, un ECA, tiene la modalidad codificada **desde el resumen**: no
hay texto completo.

Verificadas contra el artículo, seis sí lo son: EST-012 (*«phage therapy alone
without antibiotics»*), EST-031 (*«no antibiotic therapy was given during the
entire course»*), EST-039 (*«without antibiotic use throughout the period»*),
EST-046 (*«intravenous bacteriophage monotherapy»*), EST-152 (*«without
concomitant use of antibiotics»*) y EST-080 (solo cócteles de fagos).

## El embudo no se mueve

| filtro | actual | sin los 21 | solo fago | sin los 21 y solo fago |
|---|---:|---:|---:|---:|
| brazos de partida | 132 | 111 | 19 | 11 |
| diseño comparativo | 24 | 17 | 5 | 3 |
| numerador y denominador coherentes | 8 | 5 | 1 | 1 |
| definición operativa del éxito | 3 | 2 | 1 | 1 |
| atribuible a *P. aeruginosa* | 2 | 1 | 1 | 1 |
| terapéutica, no profiláctica | 1 | 1 | 1 | 1 |
| proporción, no un tiempo | **0** | **0** | **0** | **0** |

El hallazgo del manuscrito **no depende de ninguna de estas decisiones**. Eso
importa: significa que corregir el corpus no se hizo para salvar la conclusión,
y que la conclusión no se sostiene sobre los errores.

## Lo que esto mide

**22 de 93 (23,7 %)** de los estudios con texto completo no cumplen lo que §2.2
pide. Y es un **suelo**: 31 estudios no tienen texto que leer.

La causa es la misma en casi todos: el cribado de títulos y resúmenes lo emitió
un modelo de lenguaje como revisor único. Un resumen de protocolo, un resumen
de modelo murino y un resumen de piobacteriófago polivalente **se parecen
mucho** a un resumen elegible. La diferencia está en el artículo.

§2.4 ya declara que los registros que el modelo excluyó no los releyó ningún
humano. Esto es la otra cara, y ahora con cifra: lo que **incluyó** de más.
Merece entrar en las limitaciones con el 23,7 % y con estos ejemplos, porque un
ejemplo medido vale más que una advertencia genérica.

## Qué hay que decidir

Excluir estos estudios cambia los 184, los 124 y el diagrama PRISMA. Es
decisión de cribado de D. Valdiviezo y N. Trelles.

---

# Adenda, 1 de septiembre de 2026: el criterio NO cambia

**D. Valdiviezo decide mantener las dos modalidades**: fago solo y fago con
antibiótico siguen siendo elegibles, como hasta ahora.

Consecuencias, y son buenas:

- **No hay cambio de criterios de elegibilidad.** No hay nada que declarar como
  post hoc bajo PRISMA 2020, y las columnas del embudo «solo fago» de la tabla
  de arriba quedan como lo que eran: un análisis de sensibilidad que muestra que
  la conclusión no dependía de esa decisión.
- **Ninguno de los 22 estudios marcados lo estaba por usar antibiótico
  concomitante.** Los motivos son otros --no es un fago, no hay pacientes, es un
  protocolo, el patógeno no está en el paciente--, así que la lista sigue
  entera. La decisión de Danny no rescata a ninguno.

## Verificación completa de `modality`, ya que se queda

Como el campo se queda en el esquema y la extracción adjudicada **se publica
entera como anexo S14**, se verificaron contra el texto **todos** los brazos con
PDF legible, no solo los 19 de monoterapia:

| grupo | brazos con texto | contradicciones |
|---|---:|---:|
| fago+antibiótico | 64 | **0** |
| monoterapia | 18 | **4** |
| NA | 2 | 0 |

Los 64 de combinación cuadran: donde aparece «phage alone» es en una cita
bibliográfica, en un ensayo in vitro, o en un «*antibiotics were stopped after
N days*» que precisamente confirma que los había.

Se comprobaron además dos que levantaron bandera y **aguantan**: EST-034 es una
serie de casos real (*«First 10 Consecutive Cases… at a Single Center in the
United States»*), no una propuesta preventiva; y EST-055 es un *«prospective,
observational, comparative study»*, no un protocolo.

`modality` **no alimenta ninguna cifra del manuscrito** --se comprobó: solo
aparece en `sin_modalidad`, que se calcula desde la pre-extracción y no se cita
en el texto--. Pero viaja en S14, así que un valor equivocado ahí es un dato
publicado equivocado.

## Las cinco correcciones: APLICADAS Y FIRMADAS POR LOS DOS

D. Valdiviezo las revisó y ordenó aplicarlas el 1 de septiembre de 2026. Están
declaradas en `revision_sistematica/extraccion/correcciones_tras_texto_completo.csv`
--cada una con su cita literal, su valor anterior, su procedencia anterior y su
firmante-- y el constructor las aplica como **última capa**, después del acuerdo
y del consenso. El cuaderno de cada revisor sigue diciendo lo que escribió: no
se reescribe nada aguas arriba.

### Las dos firmas, y por qué se pidió la segunda

Tres de estas casillas las escribieron **igual los dos revisores** y dos ya
estaban **cerradas por consenso**. Corregirlas es reabrir una decisión conjunta,
así que se aplicaron primero con **una sola firma** y así quedaron etiquetadas
--«corregido contra el texto (una firma)», y sin contar como doble lectura--
mientras se le mandaba a N. Trelles el paquete para revisarlas.

El paquete (`revision_sistematica/extraccion/firma_nataly/`) no llevaba un
resumen: llevaba **la misma prueba** que reabrió cada casilla --la cita literal
y el PDF del artículo-- porque una firma sobre un resumen no verifica nada.
EST-118 iba sin PDF a propósito: no tenerlo es justamente su problema.

**N. Trelles firmó las cinco el 1 de septiembre de 2026**, las cinco con «sí» y
sin objeciones. `scripts/ingest_firma_correcciones.py` las recogió tras
comprobar, fila a fila, que el cuaderno devuelto seguía proponiendo lo mismo que
el enviado --mismo estudio, mismo brazo, mismo campo, mismo valor, misma cita--;
una fila alterada no se habría ingerido. Un «no» tampoco revierte nada solo:
reabre la casilla.

Con las dos firmas, la procedencia pasa a **«corregido por consenso contra el
texto»** y **sí cuenta como doble lectura**, que es lo que es: dos personas
mirando la misma casilla y firmándola. La cifra publicada vuelve a **2 598
casillas, 94,3 %** --el mismo valor de antes de las correcciones, por el mismo
número de casillas, no por casualidad.

`extraccion_conflictos_firmados` sigue en 525 porque el fichero de conflictos no
se toca. Que haya 523 casillas «por consenso» más 5 corregidas y 525 conflictos
firmados no es una incoherencia: es el rastro de que dos de esos consensos se
corrigieron después contra el texto. El desglose que imprime el constructor
declara las cinco por separado, para que la suma cuadre a la vista.

Se comprobó qué más se movía: **nada**. El embudo sale idéntico
(132→24→8→3→2→1→0), las seis tablas del manuscrito se reconstruyen sin un solo
cambio, y las 71 afirmaciones ancladas siguen al día.

| estudio | de | a | confianza | la frase que lo decide |
|---|---|---|---|---|
| EST-019 | monoterapia | fago+antibiótico | alta | *«maintaining the standard-of-care antibiotics during the treatment»* |
| EST-085 | monoterapia | fago+antibiótico | alta | *«the antibiotic was completely stopped at April 14»* |
| EST-118 | monoterapia | **NA** | alta | no hay texto completo: se codificó desde el resumen, y es un ECA |
| EST-038 | monoterapia | fago+antibiótico | media | *«targeted by antibiotics as well as by phages»* |
| EST-178 | monoterapia | fago+antibiótico | media | *«**adding** of polyvalent bacteriophage»* a una prescripción diferida |

Aplicadas, la monoterapia verificada baja de 19 a 14 brazos y el reparto queda
en **85 fago+antibiótico · 33 NA · 14 monoterapia**.

---

# EST-207: conseguido, y dice algo peor de lo que se sospechaba

D. Valdiviezo descargó el artículo por su DOI el 1 de septiembre. Ya está
instalado y la caché reconstruida.

**Exarchos V, Tkhilaishvili T, Potapov E, Starck C, Trampuz A, Schoenrath F.**
*Successful bacteriophage treatment of infection involving cardiac implantable
electronic device and aortic graft: a Trojan horse concept.* Europace
2020;22(4):597. DOI 10.1093/europace/euz319. PMID 31740948.

Es un **EP CASE EXPRESS de una página**, 2 766 caracteres. Varón de 41 años con
síndrome de Marfan, infección de bolsillo de un DAI y fístula al *bypass*
carotídeo-subclavio; se explantó el dispositivo, se trató con cierre asistido
por vacío y antibióticos, y al no lograrse control se **añadió** fagoterapia
local.

**No nombra ningún microorganismo.** Ni *Pseudomonas*, ni *aeruginosa*, ni
ningún otro: cero menciones en todo el artículo. No es que no separe el subgrupo
--que es lo que decía el `incomplete_reason` extraído--, es que no hay patógeno
documentado en ninguna parte. Y la versión completa del caso no está en la
revista: remite a una página de e-learning de la ESC.

Se añade a `hallazgos.csv` con esa categoría. Dos apuntes más: la fila la
extrajo **un solo revisor** (toda ella «sin segunda lectura»), y la modalidad
codificada --fago+antibiótico-- **sí es correcta**, como confirma la frase del
artículo.

## Por qué se había recuperado mal, y qué se hizo con eso

El PDF anterior era la página 597 de una revista japonesa de insuficiencia
cardíaca. El artículo correcto también está en la **página 597**: se recuperó
por número de página en vez de por DOI.

Lo grave no es el fallo, es que **el canal no lo detectaba**: daba por
recuperado un texto completo con que existiera el fichero, así que S5 declaraba
`texto_completo: sí` y EST-207 entraba en el recuento de 93/124. **El 93 estaba
inflado en uno hasta hoy.**

`scripts/verificar_pdf_corresponde.py` cierra ese hueco: coteja el título que
S5 declara contra el texto de cada PDF. Resultado sobre los 93: **todos son el
artículo que dicen ser.**

Una nota sobre el propio comprobador, porque su primera versión era mala.
Buscaba el título como cadena seguida y marcó cuatro --EST-049, EST-076,
EST-105, EST-164--; **los cuatro eran falsos**. En un artículo a dos columnas la
extracción entrelaza los bloques y parte el título («Development of Host Immune
| *Observations suggest…* | Response to Bacteriophage»), y EST-105 es una página
de *Research letters* con dos cartas mezcladas. Se reescribió para contar
**cuántas palabras distintivas del título aparecen**, sin importar el orden. Con
eso, 93 de 93 coinciden y no queda ningún falso positivo. Se deja anotado
porque es el mismo error que la ventana de 130 caracteres: un cotejo que se
equivoca en lo que marca no informa de lo que no marca.

---

# Los 22 salen del corpus. PRISMA actualizado

**D. Valdiviezo ordenó excluirlos el 1 de septiembre de 2026.** Hecho, y con
todo el canal detrás.

## Cómo se excluyen, y por qué no se borran

`study_groups.csv` **no se toca**: sigue siendo el registro de lo que decidió
el cribado, y falsificarlo para que cuadre sería exactamente lo contrario de
lo que este paquete existe para permitir. La exclusión vive en su propia capa,
`revision_sistematica/cribado/exclusiones_tras_texto_completo.csv`, con el
código de motivo, la explicación, **la frase del artículo** que la sostiene y
la firma de los dos revisores. El canal la aplica al calcular.

Hicieron falta **dos códigos nuevos** en el vocabulario cerrado, declarados
como tales con su fecha: **PRO** (protocolo de estudio, sin resultados) e
**INT** (la intervención no es un bacteriófago). No son una enmienda a los
criterios --§2.2 ya exigía pacientes tratados con fagos, y ni un protocolo ni
una endolisina lo cumplen--: son motivos que hacían falta para **agrupar** las
exclusiones como pide PRISMA. Meterlos con calzador en OFF («otra terapia»)
habría escondido el hallazgo en una categoría cajón de sastre.

| código | qué es | n |
|---|---|---:|
| ORG | *P. aeruginosa* no está en el paciente | 10 |
| PRO | protocolo, sin resultados | 4 |
| LAB | sin pacientes: laboratorio, preclínico | 3 |
| INT | la intervención no es un bacteriófago | 2 |
| OFF | no evalúa fagoterapia en pacientes | 2 |
| REV | revisión narrativa, sin datos propios | 1 |

## La cadena del corpus, entera

| | estudios | extraíbles | comparativos | ECA |
|---|---:|---:|---:|---:|
| antes de la enmienda de idioma | 219 | 159 | 41 | 21 |
| tras el idioma (−35) | 184 | 124 | 23 | 16 |
| **tras releer los textos (−22)** | **162** | **102** | **16** | **11** |

El diagrama PRISMA tiene ahora la casilla que le faltaba: **Estudios evaluados
para elegibilidad (184, agrupando 233 informes) → Excluidos al releer el texto
completo (22 estudios, 32 informes, con sus seis motivos) → Estudios incluidos
(162, agrupando 201 informes)**. Sin esa casilla entraban 233 informes y salían
201 sin que nada explicara los 32 que faltaban.

## Un descuento que se había vuelto doble

`comparativos_perdidos_por_idioma` se calculaba restando los comparativos de
hoy a los de antes de la enmienda. En cuanto salieron los 22, esa resta empezó
a **atribuirle al idioma pérdidas que no eran suyas**: 25 en vez de 18. Ahora
cada pérdida se mide contra su propio antes, y hay dos escalares distintos.
Lo mismo pasaba con `estudios_antes_de_la_enmienda`, que salía 197 en vez de
219 porque partía del corpus de hoy.

## Un anclaje que vigilaba una cifra y dejaba envejecer la de al lado

El comprobador de afirmaciones tenía **el número 60 escrito a mano dentro del
propio anclaje**: `"En 60 de ellos los revisores lo establecieron leyendo el
artículo: {definicion_sin_definicion_declarada}"`. Vigilaba la segunda cifra y
no la primera, así que la primera pudo quedarse vieja sin que nada saltara.
Corregido en las dos lenguas, y el anclaje pasó de 71 afirmaciones a **79**.

## Lo que el propio canal detuvo

Tres guardas dispararon durante la reconstrucción, y las tres tenían razón:

- **S9** declaraba 233 informes incluidos sobre un corpus de 201. Ahora
  descuenta los 32 y a cada uno le pone su motivo real, no uno genérico.
- **S12** citaba EST-020, que ya no está en S5. No era un fallo de generación
  sino historia: los desacuerdos se resolvieron sobre el corpus de 184. Ahora
  se admite y se distingue.
- **La guía del paquete** avisó de dos ficheros sin describir. Su catálogo
  tenía además `S5_listado_184_estudios` tecleado dentro --la misma trampa que
  el propio S5 evita calculándolo--; ahora se resuelve por patrón. Y el
  limpiador borraba el `.csv` viejo pero no el `.xlsx`, así que el paquete
  llegó a tener dos S5 que decían cosas distintas.

## Qué cambia en el manuscrito, y qué no

**Cambia:** el diagrama, las seis tablas, §3.1 (con un apartado nuevo, 3.1.1,
que reporta las 22 exclusiones con sus motivos), §3.3, §3.4, §3.5, §3.6, §2.6,
§2.7, la discusión, el resumen, y el ítem **16b de PRISMA**, que pasa de
PARCIAL a **CUMPLE**: ahora hay exclusiones en texto completo con motivo, y el
anexo **S16** las lleva con su cita para que un revisor pueda discrepar.

La recuperación de texto completo **baja del 75,0 % al 69,6 %**, y el sesgo de
recuperación **empeora**: lo no recuperado concentra ahora el 68,8 % de los
comparativos, antes el 47,8 %. Era de esperar --los 22 salieron precisamente de
los que sí se pudieron leer-- y se reporta tal cual.

**No cambia:** el hallazgo. El embudo sigue acabando en **cero**
(110 → 17 → 5 → 2 → 1 → 1 → 0). Ninguna de las 79 afirmaciones ancladas quedó
sin respaldo.
