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

## Las cinco correcciones: APLICADAS, con una firma

D. Valdiviezo las revisó y ordenó aplicarlas el 1 de septiembre de 2026. Están
declaradas en `revision_sistematica/extraccion/correcciones_tras_texto_completo.csv`
--cada una con su cita literal, su valor anterior, su procedencia anterior y su
firmante-- y el constructor las aplica como **última capa**, después del acuerdo
y del consenso. El cuaderno de cada revisor sigue diciendo lo que escribió: no
se reescribe nada aguas arriba.

**Llevan UNA firma, no dos, y el fichero lo dice.** Tres de estas casillas las
escribieron igual los dos revisores y dos ya estaban cerradas por consenso, así
que corregirlas es reabrir una decisión conjunta con la firma de uno solo. Por
eso la columna de procedencia no las etiqueta «acuerdo» ni «consenso» sino
**«corregido contra el texto (una firma)»**, y **no cuentan como doble
lectura**. Quedan pendientes de la segunda revisora.

El efecto en la cifra publicada de doble lectura es el que tiene que ser, y va
en la dirección incómoda: **2 598 → 2 593 casillas, del 94,3 % al 94,2 %**.
`extraccion_conflictos_firmados` sigue en 525 porque el fichero de conflictos no
se toca; que ahora haya 523 casillas «por consenso» y 525 conflictos firmados no
es una incoherencia, es exactamente el rastro de estas dos correcciones.

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
