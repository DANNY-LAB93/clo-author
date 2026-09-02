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
decisión de cribado de D. Valdiviezo y N. Trelles. Y si se adopta el criterio
«solo fagos», es un **cambio de los criterios de elegibilidad tomado después de
ver los resultados**: PRISMA 2020 obliga a declararlo como tal, y el informe
editorial S0 registra exactamente eso.
