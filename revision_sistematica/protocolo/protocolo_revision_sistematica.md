# Fagoterapia en infecciones por *Pseudomonas aeruginosa* resistente: protocolo de una revisión sistemática de la literatura clínica y la completitud de su reporte

**Versión:** 1.2, borrador para depósito en OSF Registries con la plantilla *Generalized Systematic Review Registration* (van den Akker et al., *Syst Rev* 2023;12:170).
**Fecha e identificador:** los asigna OSF al registrar. Ninguna etapa de la fase definitiva (sección 17) empieza antes de esa fecha.
**Tipo de revisión:** revisión sistemática de estudios clínicos, con evaluación de la completitud del reporte y de la viabilidad de una síntesis cuantitativa.
**Palabras clave:** bacteriófagos; fagoterapia; *Pseudomonas aeruginosa*; multirresistencia; revisión sistemática; PRISMA.

**Estado al registrar:**

| Etapa | Fase piloto | Fase definitiva |
|---|---|---|
| Búsqueda | completada (ejecuciones documentadas: 3 y 4-ago-2026) | no iniciada |
| Cribado de título y resumen | completado | no iniciado |
| Elegibilidad a texto completo | completada | no iniciada |
| Extracción | completada y adjudicada | no iniciada |
| Riesgo de sesgo | completado | no iniciado |
| Síntesis | completada | no iniciada |

**Fechas previstas de la fase definitiva:** inicio ‹‹FECHA, POSTERIOR AL DEPÓSITO››; fin ‹‹FECHA››. El informe de la fase piloto no se ha enviado a ninguna revista y no se enviará como tal.

---

## 1. Identificación

Protocolo de una revisión sistemática, redactado conforme a PRISMA-P 2015 (Moher et al., *Syst Rev* 2015;4:1). La revisión se reportará conforme a PRISMA 2020 (Page et al., *BMJ* 2021;372:n71). El anexo E hace corresponder cada campo de la plantilla de OSF con la sección que lo responde.

## 2. Registro

Se deposita en OSF Registries. **No se registra en PROSPERO**, que solo admite revisiones cuya extracción de datos no ha empezado: la fase piloto (sección 3) extrajo datos. Lo que se registra es la **fase definitiva**, y todo lo que la sección 17 enumera se hará después de la fecha del depósito.

## 3. La fase piloto y lo que los autores ya conocen

Esta sección es obligatoria. Todo informe derivado de este protocolo la reproduce en Métodos y la resume en una frase en el resumen.

### 3.1 Qué se hizo

Entre julio y el 6 de octubre de 2026 los autores condujeron una fase piloto sobre el mismo tema, pero **no con la misma pregunta**.
- **Julio de 2026.** Fue una revisión con un metaanálisis exploratorio de eficacia, de 40 brazos de 33 estudios. Agrupó proporciones de éxito clínico y de erradicación, y calificó con GRADE 15 celdas.
- **10 de agosto de 2026.** Con los datos a la vista, se aparcó el metaanálisis, y la pregunta pasó a la caracterización y la «verificabilidad» del cuerpo de evidencia.
- **14 de septiembre de 2026.** La pregunta se renombró «completitud del reporte».

Las preguntas de la sección 7 se formularon, por tanto, conociendo el corpus del piloto.

- **Búsqueda.**
  - **Fuentes:** ocho, con las ecuaciones del anexo A, salvo CTIS, que se interrogó con dos términos. ProQuest se interrogó en dos brazos (4 416 registros) y no se exportó.
  - **Fechas:** las ejecuciones documentadas son del 3 y el 4 de agosto de 2026. La exportación de BVS se incorporó al corpus el 10 de agosto.
  - **Autoría de las búsquedas.** Las ecuaciones de cada plataforma y sus reglas de diseño las redactó el modelo (3 de agosto de 2026). Según declara D.V. (8 de octubre de 2026), las ejecutó en cada interfaz con la guía del modelo. Los mensajes de los commits del 3 de agosto de 2026, que redactó el modelo, narran la ejecución en primera persona; según D.V., el modelo le guiaba y redactó esos mensajes. Los registros de PubMed y ClinicalTrials.gov se descargaron por API con guiones escritos por el modelo; solo los recuentos de ClinicalTrials.gov se cuadraron con los de la interfaz. No consta la fecha de la ejecución de Scopus cuya exportación entró al corpus (2 871 y 9 360 registros).
- **Uso del modelo en el piloto.** Lo detalla, completo, la declaración de uso de inteligencia artificial del informe piloto (`paper/manuscrito_revision_sistematica.md`, Declaraciones); esta sección no la resume.
- **Selección.**
  - La etapa 1 aplicó cuatro reglas deterministas.
  - Las decisiones de las etapas 2 y 3 las emitió un modelo de lenguaje (Claude Opus 5, Anthropic). El registro las anota como «revisor único, sin duplicación».
  - **El vocabulario de motivos no estaba fijado antes de empezar.** Las decisiones del primer día de cribado de títulos (4 de agosto de 2026) llevan el motivo en texto libre, con 20 redacciones distintas en sus exclusiones; los seis códigos, cuya redacción procede de esos textos, se usaron desde el 5 de agosto, y las exclusiones del primer día se asignaron después a un código. No consta que los autores fijaran los códigos antes de empezar. Ese mismo día el modelo añadió a mitad de lote, en sus guiones de cribado, la exclusión de las endolisinas aisladas y la de los informes veterinarios, sin que conste una decisión de los autores.
  - **Lo que hizo D.V.** Fue el único revisor humano. D.V. examinó uno a uno los informes que superaron el cribado (declaración de D.V., 8 de octubre de 2026), pero ese examen no quedó registrado: las columnas de decisión y de revisor de la hoja Texto_completo están vacías.
  - Lo que el modelo excluyó no lo releyó ningún humano, salvo una muestra de 350 que D.V. recribó en Rayyan sin otro revisor y sin los criterios a la vista. Incluyó 6, y al contrastarlos con los criterios D.V. los reclasificó como excluidos (0 de 350).
  - La restricción de idioma se aplicó el 11 de agosto de 2026, con el cribado concluido. El modelo emitió las 35 exclusiones de la etapa de resumen: 32 al aplicar la restricción y 3 tras consultar el texto completo o la web del editor. Entre ellas hay un control positivo (Ronit 2024, en danés).
  - Siguieron la agrupación de informes en estudios y la lectura de los textos completos. En esa lectura el modelo localizó y propuso las exclusiones, con la frase del artículo o de la ficha cuando la hubo; las 63 por no disponer del artículo (NOPDF) responden a un criterio que pidió D.V. el 6 de octubre de 2026. De las 118, los dos autores firmaron 89; D.V. firmó solo dos el 2 de septiembre de 2026, EST-118 (NOREC) y EST-205 (REV, decidida sobre la indexación de SciELO sin leer el texto), y 27 se registraron por orden de D.V. del 1 y el 2 de septiembre sin que conste la firma de N.T. En las fichas de registro, el cuaderno llevaba ya el veredicto y la frase propuestos.
  - Además, 4 estudios salieron por IDI a texto completo el 1 de septiembre de 2026, por orden de D.V. y sin que conste la firma de N.T., y 3 por idioma no verificable el 6 de octubre (NOREC).
- **Pre-extracción desde el resumen.** La emitió el modelo, y fue la fuente de las cifras estructurales del piloto: diseño, completitud en el resumen y efecto de los criterios.
- **Extracción.**
  - **Cuadernos.** Hubo dos cuadernos, uno por autor; el segundo cubre 122 de los 124 estudios extraídos.
  - **Independencia: no está acreditada.** En la columna de texto libre que localiza cada dato, el cuaderno que N.T. entregó el 26 de agosto de 2026, al reincorporarse, coincide carácter por carácter con el de D.V. en las 107 filas comparables, con las mismas erratas («MATERILAES Y METODOS», 49 veces). El 23 de agosto no coincidía en ninguna de 84. La columna de motivo de incompletitud también coincide en todas las filas, pero es un desplegable de lista cerrada, y eso solo no prueba nada. La concordancia del piloto (kappa mediana 0,62) no mide, por tanto, dos lecturas independientes.
  - **Desacuerdos.** Los 541 desacuerdos de valor se cerraron en el cuaderno de adjudicación. El registro anota a los dos autores en 14 y a un solo autor en 525 (293 D.V. y 232 N.T.); otros 2 se cerraron por una regla mecánica, sin firma conjunta.
  - **Formulario.** El formulario tuvo 21 variables de datos durante toda la extracción. No consta un piloteo documentado.
  - **Relectura.** Después hubo una relectura dirigida de los textos completos, con cada conclusión firmada por los dos.
- **Riesgo de sesgo. No fue independiente.**
  - La noche del 4 al 5 de septiembre de 2026, los dos cuadernos traían los 82 juicios idénticos.
  - Setenta y cinco minutos después se habían vuelto a guardar, con dos segundos de diferencia, con 13 discrepancias, y seguían compartiendo 7 418 caracteres idénticos en las notas de apoyo. El registro del 5 de septiembre concluye que un cuaderno salió del otro.
  - El cuaderno de consenso lo generó el canal con los 69 juicios coincidentes precargados, y coincide con el de D.V. en todos los juicios.
- **Revisores.** N.T. se retiró del 22 al 26 de agosto de 2026 y volvió.

### 3.2 Lo que los autores saben

Los autores conocen el corpus del piloto y sus resultados, entre ellos estos:
- **Corpus.** Quedó en 65 estudios y 73 brazos. De los 42 controles positivos, siguen en él 35. Salieron uno por idioma (Ronit 2024), uno por NOREC (Leitner 2021, EST-118) y cinco por NOPDF (ArmataAP_PA02, Casazza 2025, Duplessis 2018, Law 2019 y Maddocks 2019).
- **Definición del éxito.** 43 de los 73 brazos (58,9 %) no daban una definición operativa del éxito clínico.
- **Embudo del piloto.**
  - Lo superaban 19 brazos de 16 estudios: 14 tenían un solo paciente y los 5 restantes eran series de 2 a 5 pacientes.
  - Aplicó los requisitos 3 a 5 con reglas aproximadas del canal, porque no existían los campos del anexo B: una nota de extracción y una lista fija para la atribución, una expresión regular sobre el título para la finalidad, y una lista fija de un estudio (EST-021) para la métrica. Con las reglas de la sección 16.3 el recuento puede cambiar.
  - Solo 2 brazos reunían diseño comparativo, numerador, denominador y definición, y ninguno superaba el embudo completo.
- **Idioma.**
  - El criterio excluyó 39 estudios: 35 en el cribado de resúmenes (sección 3.1) y 4 a texto completo. Otros 3 salieron por idioma no verificable.
  - Según la pre-extracción del modelo, la restricción se llevó 18 de los 41 ensayos y 5 de los 21 ensayos aleatorizados.
- **Texto completo.** El criterio dejó fuera 7 de los 9 estudios clasificados como comparativos según la pre-extracción del modelo:
  - cinco eran artículos publicados cuyo texto no se obtuvo: EST-029, EST-157 y EST-167; EST-118 (Leitner et al., *Lancet Infect Dis* 2021, control positivo), del que solo se localizó la versión enviada, tras una barrera de acceso automatizado; y EST-173, cuyo idioma no pudo verificarse sin el texto;
  - los otros dos (EST-078 y EST-188) solo existen como resúmenes de congreso.
- **Metaanálisis exploratorio de julio.** Separar la colonización crónica de vía aérea dejaba sin heterogeneidad la erradicación del resto de sitios (τ² = 0). De ahí sale la regla correspondiente del anexo B.

Los autores esperan que la fase definitiva dé resultados del mismo orden.

### 3.3 Criterios de este protocolo que difieren de aquellos con que empezó el piloto

**Todos los criterios de este protocolo se redactaron después del piloto y conociendo su corpus.** La tabla enumera los que difieren del criterio con que el piloto empezó, con la fecha en que cambió en el piloto, cuando cambió allí.

| Criterio | Al empezar el piloto | En este protocolo | Origen |
|---|---|---|---|
| Pregunta y objetivos | eficacia, con metaanálisis | completitud del reporte y viabilidad de la síntesis (sección 7) | metaanálisis aparcado y pregunta reformulada el 10-ago-2026; renombrada el 14-sep-2026 |
| Unidad de inclusión y resúmenes de congreso | por informe; los resúmenes de congreso, elegibles | por estudio; los resúmenes de congreso, excluidos (NOTXT) | unidad por estudio y resúmenes elegibles decididos el 5-ago-2026, con el cribado en curso; la exclusión de los resúmenes revierte esa decisión |
| Reglas de extracción | definiciones de cada estudio, salvo DTR (definición propia según Kadri 2018, desde el 28-jul-2026) | reglas propias de erradicación, éxito clínico, clase, DTR y colonización de vía aérea (anexo B) | DTR corregida el 30-jul-2026 sobre los datos del metaanálisis exploratorio y registrada el 13-ago, con una ayuda del formulario que listaba solo dos agentes posteriores a 2018; la excepción de vía aérea, motivada por ese metaanálisis, escrita el 11-ago y cerrada el 12-ago; erradicación y éxito clínico, 11 y 12-ago, con la extracción piloto a la vista; la regla del 12-ago quedó en el registro como propuesta sin ratificar por los dos (según declara D.V., 8-oct-2026, la decidieron los dos autores); las reglas de clase de resistencia, de las nueve decisiones firmadas el 1-oct-2026 |
| Idioma | sin restricción | inglés o español, comprobado sobre el cuerpo del artículo y sin traducción automática (IDI) | restricción adoptada el 11-ago-2026, con el cribado concluido; comprobación sobre el cuerpo el 1-sep y el 6-oct |
| Texto completo | no se exigía; las fichas de registro y los resúmenes de congreso eran estudios del corpus | se exige el texto completo de un artículo publicado (NOTXT) | 2-sep-2026 para un estudio (NOREC) y 6-oct-2026 para todos (NOPDF), con la extracción terminada |
| NOREC, NOORG y NOPDF | no existían | sustituidos por NOTXT | 2-sep, 14-sep y 6-oct-2026 |
| PRO e INT | el criterio existía, sin código propio | códigos propios | 1-sep-2026; no cambiaron el criterio |
| Población y resistencia | infección «clasificada MDR, XDR o PDR, o descrita en términos que impliquen esas categorías» | la elegibilidad no exige clase de resistencia; los estudios por debajo del umbral se incluyen y se declaran | el piloto mantuvo por firma 6 estudios por debajo del umbral (22-sep, 1-oct y 3-oct-2026) |
| Fago dirigido contra *P. aeruginosa* (sección 8.4) | no se exigía de forma explícita | se exige (DIA) | regla nueva y **contraria a lo firmado en el piloto**, que el 1-oct-2026 mantuvo 4 estudios firmados como «fago no diana» (EST-051, EST-096, EST-129, EST-135; en EST-096 la etiqueta no se sostiene: la paciente 10 recibió Ps1N/734 contra *P. aeruginosa*, y lo contradictorio es si la bacteria seguía presente) y, contra su propio criterio de población (ORG), 2 en que ningún paciente propio tenía *P. aeruginosa* (EST-152 y EST-170, que solo citan los casos de EST-049 y EST-106) |
| Profilaxis y desenlaces | sin código | códigos PRF y DES | nuevos |
| Ventana de años | se aplicó solo en la consulta de PubMed, Scopus y CENTRAL; entraron 495 registros anteriores a 2016 | regla FEC en la etapa 1 para los registros bibliográficos | nueva |
| Tipos documentales excluidos en la etapa 1 | incluían editoriales, cartas, notas y *short surveys* (554 registros) | solo erratas, retractaciones, noticias, biografías y material para pacientes | nueva; evita excluir sin leer cartas con casos |
| IDI en título o resumen | se aplicó en el cribado de resúmenes (35) | solo a texto completo | nueva |
| Vocabulario de las etapas 2 y 3 | texto libre el primer día (4-ago-2026); seis códigos desde el 5-ago, redactados por el modelo a partir de esos textos | siete (se añade PRF), fijados antes de empezar | nueva; en el piloto el vocabulario no estaba fijado antes del cribado |
| Riesgo de sesgo | estudios con diseño comparativo, por etiqueta de diseño | estudios con grupo concurrente sin fago (sección 15) | en el piloto, 7 de 9 evaluados no tenían grupo concurrente sin fago, y 6 de 9 no tenían ningún grupo de comparación |
| Requisitos de agrupación y umbral (sección 16.3) | no fijados | fijados aquí | los requisitos 3 a 5 se añadieron en el piloto el 1-sep-2026 con reglas aproximadas; el umbral se fija conociendo el recuento de la sección 3.2 |
| Recribado ciego | un revisor (D.V.), sin los criterios a la vista; incluyó 6 de 350, y D.V. los reclasificó como excluidos | los dos autores, de forma independiente, con la sección 8 a la vista y consenso entre ellos | nuevo |
| Formulario de extracción | 21 variables de datos durante toda la extracción; el denominador y la persistencia de la erradicación se añadieron al esquema el 12-ago-2026, pero no llegaron a los cuadernos | revisado (sección 14.2) y pilotado antes de extraer | nuevo; no consta un piloteo documentado del formulario del piloto |

### 3.4 Qué se reutiliza y qué no

**Se reutiliza, con los cambios de la sección 3.3:**
- las ecuaciones de búsqueda (anexo A);
- el conjunto de 42 estudios de control positivo (sección 12.5 y anexo D):
  - se fijó el 29 de julio de 2026 (commit 20574ce, 123 identificadores), antes del cribado piloto;
  - sus identificadores, no los estudios, se corrigieron en la versión generada el 5 de agosto y registrada el 10 de agosto (commit 4258270, 114 identificadores), con el cribado piloto en curso, incluidos dos PMID que usa la auditoría;
  - procede del metaanálisis exploratorio de julio de 2026, primera etapa del piloto, que se hizo con asistencia de modelos de lenguaje, y las ecuaciones se diseñaron para recuperarlo, así que no prueba la sensibilidad de la búsqueda: solo acota lo que pierde la selección;
- el código del canal de búsqueda, deduplicación, etapa 1, agrupación y cálculo de cifras.

**No se reutiliza ninguna decisión del piloto:** ni de cribado, ni de agrupación de informes en estudios, ni de elegibilidad, ni de extracción, ni de riesgo de sesgo. En consecuencia:
- No se ejecuta en la fase definitiva ningún guion que aplique decisiones o datos del piloto: los `ingest_*.py`, los `add_*.py`, `correcciones_tras_texto_completo.csv` y los cuadernos de firma.
- Los estudios se numeran en un espacio propio (DEF-NNN), sin leer el `study_groups.csv` ni el `fulltext_identifiers.csv` del piloto.
- Los ficheros del piloto se trasladan a `revision_sistematica/piloto/` antes de la búsqueda.
- **Antes del depósito** se adaptan y se fechan los guiones que leen ficheros del piloto:
  - `group_reports_into_studies.py`: numeración DEF-NNN y un `fulltext_identifiers.csv` propio, vacío;
  - `comprueba_idioma_cuerpo.py`: corpus definitivo y lectura de la copia HTML;
  - `build_rayyan_validation_sample.py`: semilla 20261008 y decisiones de la fase definitiva;
  - cualquier otro guion reutilizado que lea `cribado/`, `textos_completos/` o `extraccion/`.
- La lista de guiones reutilizados, con el identificador de su versión, se deposita con este protocolo.

### 3.5 Los datos del piloto y la comparación

Los datos del piloto no se borran: se aportan como material suplementario del informe final, separados de los de la fase definitiva.

**Cuándo se compara.** Solo después de cerrar la adjudicación definitiva. La tabla de correspondencia entre DEF-NNN y la numeración del piloto se construye en ese momento.

**Qué se compara:**
- los estudios presentes en ambos corpus;
- los presentes en uno solo, con el código o la decisión que lo explica;
- en los presentes en ambos, el acuerdo campo a campo de la extracción.

**Límite de la independencia: los autores.** Los dos extrajeron entre agosto y octubre de 2026 la mayor parte de los estudios que volverán a leer. No consultar los ficheros del piloto no los enmascara, y se declara como límite.

**Límite de la independencia: el modelo.** Una sesión de Claude Code abierta en el repositorio carga sola el CLAUDE.md y la memoria del proyecto, que describen el corpus piloto. Por eso las decisiones de las etapas 2 y 3 se emiten en sesiones abiertas en un directorio **fuera del repositorio**, que solo contiene el anexo C, el lote que se criba y el guion que registra la respuesta, sin CLAUDE.md y con la memoria automática desactivada. Cada lote registra el directorio de trabajo y la lista de ficheros visibles en la sesión.

## 4. Autores

- **Danny Valdiviezo**, Facultad de Medicina, Universidad Católica de Cuenca, Cuenca, Ecuador. Autor de correspondencia: Av. de las Américas y Humboldt, Cuenca, Ecuador; dvchiqui@gmail.com. ORCID ‹‹ORCID››.
- **Nataly Elizabeth Trelles Avila**, Facultad de Medicina, Universidad Católica de Cuenca, Cuenca, Ecuador. Correo ‹‹CORREO››. ORCID ‹‹ORCID››.

**Contribuciones** (las tareas del modelo de lenguaje están en la sección 19):
- **D.V.:**
  - concepción;
  - ejecución de las búsquedas en las interfaces (sección 10);
  - conducción del cribado, cuyas decisiones emite el modelo;
  - elegibilidad a texto completo, extracción y riesgo de sesgo;
  - recribado ciego;
  - aprobación del protocolo que redactó el modelo.
- **N.T.:**
  - decisión, con D.V., de las reglas de desenlace que redactó el modelo el 11 y el 12 de agosto de 2026 (declaración de D.V., 8 de octubre de 2026; el registro del 12 de agosto la deja como propuesta sin ratificar);
  - elegibilidad a texto completo, extracción y riesgo de sesgo independientes;
  - recribado ciego;
  - validación de la pre-extracción;
  - aprobación del protocolo.

**Garante:** D.V.
**Autoría solapada:** ‹‹CONFIRMAR: ninguno de los autores firma estudios elegibles››.

## 5. Cambios posteriores al depósito

Todo cambio a este protocolo se registra en OSF como actualización, con fecha y motivo, **antes** de aplicarse. El informe final enumera cada uno con su efecto medido sobre el corpus.

Un motivo de exclusión que no encaje en el vocabulario de la sección 8.8 no recibe un código improvisado: el estudio permanece hasta que los dos autores registren el cambio.

## 6. Justificación

*P. aeruginosa* figura entre los patógenos prioritarios de la Organización Mundial de la Salud. La lista de 2017 lo situó en prioridad crítica (Tacconelli et al., *Lancet Infect Dis* 2018;18:318-27), y la actualización de 2024 pasó su forma resistente a carbapenémicos a prioridad alta.

La literatura clínica sobre fagoterapia creció como una acumulación de casos de rescate publicados de uno en uno, con una publicación condicionada al desenlace (Aslam et al., *Am J Transplant* 2019). Además, el fago se da a menudo junto con antimicrobianos activos (Chan et al., *Evol Med Public Health* 2018).

Las síntesis publicadas agregan esa literatura en proporciones globales de éxito clínico (Uyttebroek et al., *Lancet Infect Dis* 2022; Liu et al., *Int J Antimicrob Agents* 2025). Hacerlo presupone tres cosas que rara vez se comprueban:
1. que la clase de resistencia con que se estratifica resiste el contraste con los criterios que dice aplicar;
2. que el desenlace agregado nombra lo mismo en todos los estudios;
3. que la intervención es bastante homogénea para que una proporción común signifique algo.

Esta revisión examina esas premisas antes de cualquier estimación.

## 7. Objetivos y preguntas

**Pregunta principal.** En pacientes con infección o colonización crónica por *P. aeruginosa* tratados con bacteriófagos líticos, solos o con antimicrobianos, ¿reúne la literatura clínica publicada los requisitos de completitud de reporte, estructura y homogeneidad que exige una síntesis cuantitativa de eficacia?

**Preguntas secundarias:**
1. ¿Con qué frecuencia declaran los estudios, en el resumen y en el texto completo, la clase de resistencia, la vía, el ámbito de patógeno y el criterio DTR?
2. ¿Con qué frecuencia informan cada uno de los cinco desenlaces con numerador y denominador, y una definición operativa del éxito clínico?
3. ¿Coincide la clase de resistencia declarada con la que permite asignar el antibiograma publicado?
4. ¿Qué parte de la evidencia identificada deja fuera cada uno de los criterios de idioma y de texto completo, y qué diseños pierde?
5. ¿Cuántos estudios registrados no tienen publicación?

**Expectativas.** Ver la sección 3.2.

## 8. Criterios de elegibilidad

### 8.1 Unidad de inclusión
La unidad es el **estudio**, no el informe (PRISMA 2020).

- **Un mismo estudio.** Varios informes son un solo estudio cuando describen el mismo ensayo o la misma cohorte (mismo registro, mismo protocolo o misma selección de pacientes), aunque uno informe más pacientes o más seguimiento que otro. Es el caso de un análisis intermedio y el final.
- **Estudios distintos con solapamiento.** Lo son cuando un estudio con su propia selección incorpora pacientes de otro, como las series acumulativas o los programas que reúnen casos ya publicados (sección 14.6).

### 8.2 Diseño
Se incluyen los estudios primarios con pacientes tratados:
- ensayos aleatorizados y no aleatorizados;
- cohortes prospectivas y retrospectivas;
- series de casos;
- reportes de caso.

Un informe que describe al menos un paciente propio tratado con fagos y al menos un desenlace de la sección 8.5 es un estudio primario, cualquiera que sea su etiqueta: editorial, carta, opinión, revisión o artículo de métodos.

Se excluyen, siempre que no contengan ninguno de esos pacientes:
- protocolos sin resultados (PRO);
- revisiones narrativas, editoriales y comentarios sin datos primarios propios (REV);
- revisiones sistemáticas y de alcance (SEC);
- trabajo de laboratorio, preclínico o de modelización, incluidos los modelos animales de laboratorio (LAB);
- estudios en animales de granja o de compañía, o con aislados veterinarios (VET).

### 8.3 Población
Se incluyen los pacientes humanos con infección por *P. aeruginosa*, o con colonización crónica tratada con intención de erradicarla o suprimirla.

- **Colonización crónica:** la de vía aérea en fibrosis quística, bronquiectasias, EPOC, postrasplante pulmonar, o traqueostomía o ventilación prolongada. Requiere al menos dos cultivos positivos en doce meses, o que el artículo la declare crónica con un criterio explícito.
- **Profilaxis:** la administración a portadores no crónicos, o a pacientes sin infección, para prevenir una infección (PRF). Si un estudio tiene un brazo de prevención y otro de tratamiento, se incluyen solo los pacientes tratados, siempre que sean separables.

**Resistencia.** La pregunta se refiere a la infección resistente: MDR, XDR o PDR según Magiorakos et al. (*Clin Microbiol Infect* 2012;18:268-81). Pero **la elegibilidad no exige que el estudio documente la clase**, porque medir con qué frecuencia la documenta es una de las preguntas (sección 7). Un estudio cuyos pacientes no alcancen la definición MDR, sensibles incluidos, se incluye y se declara. La sección 16.3 dice qué brazos entran en una proporción agrupada.

**Separabilidad de un estudio con varios patógenos:**
- **Cumple** si permite identificar a los pacientes con *P. aeruginosa* y extraer para ellos al menos un desenlace de la sección 8.5, por paciente o agregado por organismo. Si da datos por paciente, se extraen solo los de *P. aeruginosa*.
- **Entra solo en las medidas de completitud** si identifica a esos pacientes pero solo da sus desenlaces agregados con los de otros organismos. Su ámbito es «mixto sin desenlace separable» y sus brazos llevan atribuible = no.
- **No cumple (ORG)** si no permite saber cuántos tenían *P. aeruginosa*.
- **Infección polimicrobiana de un paciente.** Cumple la separabilidad; la atribución de su desenlace se registra en el campo atribuible (anexo B).

### 8.4 Intervención
Se incluye la administración de bacteriófagos líticos, por cualquier vía, solos o con antimicrobianos.

**Fago dirigido contra *P. aeruginosa*.** El estudio cumple si al menos un paciente con *P. aeruginosa* aislada del sitio tratado, en una muestra tomada en los 30 días previos al primer fago, recibió un preparado que se dirige contra ella, es decir:
- con al menos un fago de actividad lítica **comprobada** frente a su aislado; o,
- si el artículo no informa fagograma, un fago **declarado activo** frente a *P. aeruginosa* por los autores del estudio para ese paciente y administrado por esa infección. El espectro comercial del producto no basta.

**Contradicciones.** Puede que el artículo se contradiga sobre la presencia de *P. aeruginosa* antes del fago: por ejemplo, una tabla con carga bacteriana previa y un texto que la da por negativa. Entonces se tiene por presente a efectos de esta regla, y la contradicción se declara. El requisito de que el preparado se dirija contra ella se sigue aplicando.

**No cumple:**
- **ORG:** ningún paciente tiene *P. aeruginosa* aislada en esa ventana. Incluye que solo figure en el espectro del producto, en la discusión o en la descripción del paciente de otro estudio.
- **DIA:** algún paciente la tiene en esa ventana, pero el fago se dirigió contra otro organismo, o el fagograma muestra que ningún fago del preparado es activo frente a su aislado.

**Otras exclusiones por la intervención:**
- **INT:** endolisinas, fagos no líticos y otros derivados sin la partícula viral.
- **OFF:** el informe no evalúa la administración de fagos a pacientes. Incluye encuestas, epidemiología, biobancos, prensa, el fago mencionado pero no administrado, u otra terapia.

### 8.5 Comparador y desenlaces
No se exige comparador.

El estudio tiene que informar, para los pacientes con *P. aeruginosa* tratados con fagos, al menos uno de estos cinco desenlaces, por separado o agregado con pacientes de otros organismos. Si solo lo da agregado, el estudio entra solo en las medidas de completitud (sección 8.3). DES se aplica solo si no informa ninguno, ni siquiera agregado.

Van en orden de prioridad, con sus definiciones completas en el anexo B:
1. **Éxito clínico.** Pacientes que mejoraron según la definición del propio autor. Si el artículo no da una definición operativa (anexo B), se anota SIN DEFINICIÓN OPERATIVA, y la cifra se extrae si el artículo permite contarla.
2. **Erradicación microbiológica.** Cultivo de control negativo para el aislado resistente que motivó el tratamiento, del mismo sitio y posterior al fin de la fagoterapia, con denominador propio y persistencia a 30 días.
3. **Eventos adversos.** Pacientes con algún evento adverso atribuido o no al fago.
4. **Mortalidad.** Fallecidos durante el seguimiento.
5. **Emergencia de resistencia al fago.** Pacientes en que aparece durante el tratamiento.

**Desenlace principal de la revisión:** la proporción de brazos que informan el éxito clínico con numerador, denominador y definición operativa. Los demás resultados de la sección 16.1 son secundarios.

### 8.6 Características del informe
- **Año de publicación:** de 2016 a 2026 (FEC; sección 12.1). El año del estudio es el de su informe de extracción (sección 14.1).
- **Idioma.**
  - El texto completo tiene que estar redactado en inglés o en español. Se comprueba sobre el **cuerpo del artículo concreto** y sin traducción automática, no sobre el título, el resumen, los metadatos ni la revista (IDI, solo a texto completo).
  - Si existe una versión íntegra en inglés o español de ese artículo y no se obtiene, el código es NOTXT, no IDI.
- **Texto completo admisible:**
  - Cumple el texto íntegro de un artículo publicado en revista: PDF o HTML del editor, de PMC o de Europe PMC, o el manuscrito aceptado del autor en un repositorio. Las cartas con datos de pacientes son artículos publicados.
  - No cumplen (NOTXT): la versión enviada de un artículo publicado, los preprints sin versión publicada, las tesis, los resúmenes de congreso y las fichas de registro sin artículo.
  - Toda lectura en HTML se archiva como copia fechada.
  - El material suplementario se busca por las mismas vías cuando el artículo remite a él para un dato que se extrae.

### 8.7 Registros de ensayos
Se buscan igual que las bases bibliográficas, por dos motivos: para enlazar cada ficha con su publicación (sección 12.3) y para **contar** los estudios registrados sin publicación (sección 16.6). Una ficha sin artículo sale del corpus con NOTXT, pero antes se comprueba contra las secciones 8.2 a 8.5 sobre la ficha completa descargada del registro (sección 8.9).

### 8.8 Vocabulario cerrado de motivos de exclusión

| Código | Motivo | Etapas en que se usa |
|---|---|---|
| FEC | publicado antes de 2016 | 1 (solo por regla), 4 |
| ORG | ningún paciente con *P. aeruginosa*, o datos no separables (8.3, 8.4) | 2 y 3 (solo cuando ningún paciente tiene *P. aeruginosa*), 4 |
| DIA | fago no dirigido contra *P. aeruginosa* (8.4) | 4 |
| REV | sin datos primarios propios: revisión narrativa, editorial, comentario | 2, 3, 4 |
| SEC | revisión sistemática o de alcance | 2, 3, 4 |
| LAB | laboratorio, preclínico o modelización, incluidos los modelos animales de laboratorio | 2, 3, 4 |
| VET | animales de granja o de compañía, o aislados veterinarios | 2, 3, 4 |
| OFF | no evalúa la administración de fagos a pacientes (8.4) | 2, 3, 4 |
| PRF | profilaxis (8.3) | 2, 3, 4 |
| PRO | protocolo sin resultados | 4 |
| INT | la intervención no es un bacteriófago lítico | 4 |
| DES | ninguno de los cinco desenlaces, ni siquiera agregado | 4 |
| IDI | cuerpo del artículo ni en inglés ni en español | 4 |
| NOTXT | sin texto completo admisible (8.6) | 4 |

Un registro que no encaja en ningún código **avanza**; no se excluye.

### 8.9 Precedencia entre motivos
Si un estudio incumple varios criterios, se registra el primero de este orden y los demás se anotan como motivos secundarios:
1. FEC.
2. **Si no hay texto completo admisible:** los criterios de 8.2 a 8.5 que puedan comprobarse sobre el informe disponible (resumen o ficha completa) y, si los cumple, NOTXT.
3. **Si hay texto completo y su cuerpo no está en inglés ni en español:** los criterios de 8.2 a 8.5 que puedan comprobarse sobre el resumen en inglés o español y, si los cumple, IDI, salvo el caso de la sección 8.6, que es NOTXT.
4. **Si hay texto completo en inglés o español:** PRO, REV, SEC, LAB, VET, INT, OFF o PRF, ORG o DIA, y DES.

## 9. Fuentes de información

**Bases bibliográficas:**
- PubMed;
- Scopus;
- Cochrane CENTRAL, vía Wiley;
- portal BVS, excluida su colección MEDLINE;
- SciELO.

**Registros de ensayos:** ClinicalTrials.gov, EudraCT y CTIS.

**Brazos de búsqueda.** PubMed, Scopus, CENTRAL y ClinicalTrials.gov se interrogan en dos brazos cada uno (anexo A):
- **A:** organismo e intervención.
- **B:** intervención, sin el organismo, para recuperar series multipatógeno que no lo nombran.

**Lo que no se busca:**
- **Fuera de la suscripción institucional:** Embase, Web of Science y EBSCO bibliográfica. Embase queda mitigada solo para ensayos controlados, por los registros de origen Embase que contiene CENTRAL.
- **Disponibles y no interrogadas:** ProQuest y el ICTRP de la OMS. Se declara como limitación.
- **Ovid MEDLINE:** no se cuenta como fuente adicional, porque es el mismo contenido que PubMed.

**Otras estrategias.** No se revisan listas de referencias ni citas posteriores, ni se busca por nombre de producto, y se declara como limitación. La búsqueda exploratoria por nombre de producto del piloto, que encontró 113 PMID ausentes de su corpus de PubMed (9 561 registros), no se repite.

## 10. Estrategia de búsqueda

Se ejecutan las ecuaciones literales del anexo A con la fecha de la fase definitiva.

**CTIS.** Su buscador casa palabras completas y no hace OR, así que se interroga con un término por búsqueda (*bacteriophage*, *bacteriophages*, *phage*, *phages*, *phagotherapy*, *pyophage*) y se unen los resultados. Un cero solo se acepta si un término de control da resultados.

**Ventana.** La de 2016 a 2026 se aplica en la consulta de PubMed, Scopus y CENTRAL, y por regla (FEC) en BVS y SciELO. No se aplica a los registros de ensayos (sección 12.1). No se restringe el idioma en la consulta.

**Quién ejecuta y cómo:**
- **En las interfaces.** D.V. ejecuta cada ecuación en la interfaz de su fuente (Scopus, CENTRAL, BVS, SciELO, EudraCT y CTIS), sin el traductor automático del navegador, que en el piloto reescribió una consulta de Scopus. Anota la fecha y el número de resultados de cada brazo.
- **Por API.** Los registros de PubMed y de ClinicalTrials.gov se descargan con los guiones `fetch_screening_corpus.py` y `fetch_clinicaltrials.py`, que contienen la consulta literal del anexo A. Los ejecuta el modelo de lenguaje, a petición de D.V., en una sesión registrada (sección 19).
- **Registro.** El de cada ejecución dice quién la hizo.
- **Cuadre.** Antes de cribar, el recuento descargado se cuadra con el de la interfaz.

**Repetición.** Si entre la última ejecución y el envío del informe pasan más de seis meses, se reejecutan las ecuaciones, y lo nuevo pasa por todas las etapas (sección 17).

**Justificación de las reglas de las ecuaciones:**
1. el brazo B omite el organismo, para recuperar series multipatógeno que no lo nombran;
2. ningún término de resistencia es obligatorio;
3. vocabulario controlado además de texto libre;
4. *phage\** y nunca *phag\**, que arrastra la fagocitosis.

## 11. Gestión de datos y programas

**Gestión:**
- Todo registro lleva una clave derivada de su contenido, no de su posición.
- La deduplicación cruza DOI, PMID y NCT de forma transitiva, leyendo los identificadores solo de campos identificadores. Los registros sin identificador se comparan por título normalizado y año, sin coincidencia difusa.
- Las decisiones se escriben en registros **solo-anexar**: una corrección es una fila nueva, y la original se conserva.

**Programas:**
- canal en Python (carpeta `scripts/` del repositorio, versión fechada antes del depósito; sección 3.4);
- Rayyan para el recribado ciego;
- cuadernos `.xlsx` para la elegibilidad, la extracción y el riesgo de sesgo;
- R con el paquete metafor, si se agrupa (sección 16.3);
- el modelo de lenguaje de la sección 19.

**Datos que se publican:** exportaciones crudas de cada consulta, registros de las etapas 1 a 4, cuadernos de los dos autores, extracción adjudicada, juicios de riesgo de sesgo, instrucciones del modelo y código del canal. Se depositan en ‹‹REPOSITORIO Y DOI››, separados de los del piloto.

## 12. Selección de los estudios

### 12.1 Etapa 1: reglas deterministas
Cada exclusión nombra la regla que la disparó:
1. **Sin título.**
2. **Tipo documental sin datos primarios.**
   - Solo excluye estos tipos: *Published Erratum* o *Erratum*, *Retraction*, *News*, *Newspaper Article*, *Biography* y *Patient Education Handout*.
   - Si el registro tiene además un tipo con datos, avanza.
   - *Editorial*, *Comment*, *Letter*, *Note* y *Short survey* pasan a la etapa 2.
3. **MeSH *Animals* sin *Humans*.** Solo juzga los registros que tienen MeSH; los demás avanzan.
4. **Fago como herramienta de laboratorio:** *phage display*, tipado, bibliotecas.
5. **FEC.** Año de publicación anterior a 2016 en la exportación (DP en PubMed, PUBYEAR en Scopus, año en BVS y SciELO).
   - Excluye solo si ningún otro registro del pozo comparte con él DOI, PMID o identificador de registro; si lo comparte, se conserva para la agrupación.
   - No se aplica a las fichas de registro de ensayos, cuyo año es el de inicio del estudio y no el de su publicación.
   - Un registro sin año avanza.

### 12.2 Etapas 2 (títulos) y 3 (resúmenes)
Las decisiones registro a registro las emite el **modelo de lenguaje** de la sección 19 como **revisor único, sin duplicación**; D.V. es el único revisor humano. El modelo trabaja con las instrucciones literales del anexo C y el aislamiento de la sección 3.5.

**Qué ve el modelo:**
- etapa 2: el título;
- etapa 3: título, resumen, revista, tipo documental y año;
- etapa 3, si es una ficha de registro: título oficial, resumen breve, condiciones, intervenciones, criterios de elegibilidad y diseño (asignación y enmascaramiento).

**Qué puede decidir.** Solo los códigos ORG, REV, SEC, LAB, VET, OFF y PRF (sección 8.8), o «avanza».
- FEC lo aplica únicamente la regla de la etapa 1.
- Ante la duda, avanza.
- Una respuesta que no sea uno de esos valores, o un error de llamada, se cuenta como «avanza», y las dos cosas quedan en el registro.

**Qué se registra.** Cada decisión se registra con su motivo, el identificador del modelo y la marca de tiempo.

**Qué hace D.V.:**
- Examina uno a uno los informes que superan la etapa 3, y lo registra informe a informe, con fecha, en el cuaderno de cribado. No puede excluirlos: solo puede marcar dudas para la etapa 4.
- **Los registros que el modelo excluye no los relee ningún humano**, salvo los 350 de la muestra de la sección 12.6. Esa muestra acota la tasa de error; no valida cada exclusión.

### 12.3 Agrupación de informes en estudios
El guion `group_reports_into_studies.py` propone la agrupación por identificadores compartidos, y D.V. la confirma informe a informe. Para agrupar se admite un identificador de registro (NCT, EudraCT, CTIS) hallado en el resumen de un artículo.

Cada ficha de registro se enlaza con su publicación buscando su identificador, con fecha, en:
- PubMed (campo de identificador secundario y texto);
- Europe PMC (texto completo);
- el campo de publicaciones de la propia ficha.

La ficha completa de cada registro se descarga del registro antes de la etapa 4.

Los estudios se numeran DEF-NNN. Los informes que, leídos a texto completo o al examinar el solapamiento, resulten ser el mismo estudio (sección 8.1) se fusionan, y se adjudican de nuevo los campos afectados. La agrupación se aporta íntegra.

### 12.4 Etapa 4: elegibilidad a texto completo
**Quién.** Los dos autores evalúan **de forma independiente** cada estudio contra la sección 8. Los cuadernos se generan sin veredicto propuesto y sin cita precargada: cada autor busca y copia la frase del artículo en que se apoya.

**Idioma.** El guion `comprueba_idioma_cuerpo.py` estima, sin navegador, el idioma del cuerpo del texto sobre el PDF o sobre la copia HTML archivada. Usa la frecuencia de palabras vacías de ocho idiomas y la fracción de cirílico y de caracteres CJK. Ese resultado es un dato; la exclusión por IDI la firman los dos autores.

**Exclusiones NOTXT.** En lugar de la frase del artículo, se aporta el registro de cada intento de obtención: vía, fecha, resultado y quién lo hizo (canal o D.V.).

**Concordancia y consenso.** Antes del consenso se informan el acuerdo y la kappa de Cohen, sobre la decisión y sobre el código. Si no hay consenso, el estudio permanece y la discrepancia se declara.

**Firma.** Toda exclusión lleva la firma de los dos.

### 12.5 Control positivo
El conjunto son los 42 estudios del anexo D, que se comprueban por DOI, PMID o NCT. En el piloto, la auditoría solo pudo comprobar los 40 que tenían PMID.

**Búsqueda.** Tras deduplicar se comprueba que cada control está en el pozo. Un control ausente se informa como pérdida de la búsqueda. Esto no valida la sensibilidad de la búsqueda, que se diseñó para recuperar este conjunto (sección 3.4).

**Etapas 1 a 3.** Perder un control es un fallo, salvo que lo excluya FEC. Si ocurre:
1. el cribado se detiene y los dos autores leen el texto completo del control;
2. si cumple la sección 8, se corrigen la regla o las instrucciones del modelo, el cambio se registra en OSF antes de reanudar, y se recriban todos los registros ya decididos;
3. si no cumple, se informa con su nombre y el código comprobado.

**Etapa 4.** Un control excluido se informa con su nombre y su motivo.

### 12.6 Recribado ciego
**Muestra.** 350 registros, tomados con semilla fija (20261008) de todos los excluidos en las etapas 2 y 3 por `build_rayyan_validation_sample.py`. Si no aparece ningún error, ese tamaño acota la tasa de exclusión errónea por debajo del 1,05 % (IC 95 % exacto).

**Cómo.** Cada autor la recriba en Rayyan, por separado, sin ver el veredicto original y con la sección 8 a la vista. Los desacuerdos se resuelven por consenso.

**Qué se informa.** Dos tasas, con IC 95 % de Clopper-Pearson:
1. los registros que al menos un autor habría hecho avanzar;
2. los que, leídos a texto completo por los dos, cumplen la sección 8.

**Qué pasa con los recuperados.** Los registros que, tras el consenso, habrían avanzado entran en la agrupación (sección 17, paso 7) y siguen los pasos siguientes como los demás. La tasa 2 se calcula al cerrar la elegibilidad.

## 13. Obtención del texto completo

**Vías:**
- Unpaywall, Europe PMC, OpenAlex y Semantic Scholar;
- la página del editor;
- la suscripción institucional de la Universidad Católica de Cuenca;
- ‹‹DECISIÓN DE LOS AUTORES: la solicitud a los autores del estudio (dos intentos separados por 15 días) y el préstamo interbibliotecario, para el texto completo y para los datos faltantes. En el piloto no se usaron, por decisión de D.V. del 2-sep-2026 (commit d57164b)››.

**Antes de registrar NOTXT**, D.V. intenta en persona, con el navegador y la suscripción institucional, cada vía que el canal no haya podido abrir. En el piloto, un estudio se perdió por una barrera de acceso automatizado.

**Registro.** Cada intento se registra por estudio, con su fecha y quién lo hizo (canal o D.V.).

**Fecha de corte.** ‹‹FECHA››. Lo que no se haya obtenido para entonces es NOTXT.

## 14. Extracción de datos

### 14.1 Informe del que se extrae
Se extrae del artículo de texto completo con más pacientes y el seguimiento más largo. Los demás informes solo completan los campos que ese artículo no da, citándolos. Las discrepancias numéricas entre informes se registran y no se promedian. El informe de extracción de cada estudio se fija antes de extraer.

### 14.2 Formulario
El anexo B define cada variable con sus valores admitidos.

**Cambios respecto del piloto:**
- se añaden un denominador propio para cada desenlace;
- se añaden los campos de unidad del desenlace, tipo de definición del éxito, clase declarada, atribuible, finalidad, métrica del éxito, momento de la medida, fila de control y pacientes compartidos;
- se elimina el nivel de la revista, que no tenía criterio.

**Brazo.**
- **Qué es:** el conjunto de pacientes con *P. aeruginosa* de un estudio que recibieron fago con la misma estrategia y cuyos desenlaces el artículo informa por separado. Si el artículo los separa por clase de resistencia, cada clase es un brazo.
- **Grupos sin fago.** Placebo, atención estándar o antimicrobiano solo no son brazos: se extraen en una fila marcada «control».
- **Preparados que no cumplen la sección 8.4.** Los pacientes con *P. aeruginosa* que los recibieron no forman parte de ningún brazo: se cuentan aparte, con su desenlace, y se declaran.

**Unidad.** La unidad de numerador y denominador es el paciente.
- Si el artículo informa por curso o por infección y permite separar, se extrae ‹‹DECISIÓN DE LOS AUTORES: el primer curso / el último curso›› de cada paciente.
- Si no permite separar, se extrae lo que dé, con su unidad (campo unidad_desenlace), y el brazo no cumple el requisito 1 de la sección 16.3.

**Piloteo.** Antes de extraer, los dos autores pilotean el formulario sobre 5 estudios del corpus definitivo, elegidos con la semilla 20261008. Todo cambio que resulte se registra en OSF antes de extraer el resto.

### 14.3 Procedimiento
- Los dos autores extraen **por duplicado e independientemente**, sin consultar el cuaderno del otro ni ningún fichero del piloto. Los cuadernos se generan sin valores precargados.
- La concordancia (porcentaje de acuerdo y kappa de Cohen por campo categórico) se mide antes de resolver los desacuerdos. Antes de medirla se comprueba que los textos libres de los dos cuadernos no coinciden carácter por carácter; si coinciden, se declara y la concordancia no se presenta como independiente.
- Los desacuerdos se resuelven por consenso de los dos, con registro fila a fila de los dos nombres y la fecha. Si no hay consenso, la celda queda NA y se declara.

### 14.4 Datos faltantes
- **Significado de cada valor.** Una celda vacía significa «no extraído»; NA, que el artículo no lo dice; 0, que lo dice y es cero.
- **Cierre.** Ninguna celda vacía se admite al cerrar la extracción.
- **Imputación.** No se imputa ningún valor.
- **Completitud.** En las medidas de completitud, NA cuenta como no informado.
- **Viabilidad.** Un brazo con NA en el numerador o el denominador del éxito clínico no cumple el requisito 1 de la sección 16.3.

### 14.5 Relectura dirigida
Después de adjudicar, los dos autores vuelven al artículo, con la cita y su firma, para tres cuestiones:
1. comprobar la clase de resistencia contra el antibiograma publicado, con las reglas del anexo B;
2. reextraer, en los estudios con grupo concurrente sin fago, el comparador, la asignación, el tiempo cero, el tiempo de evaluación, las cointervenciones, las pérdidas y el estimando;
3. examinar los pares de estudios que pueden describir a los mismos pacientes (sección 14.6).

### 14.6 Pacientes descritos en más de un estudio
**Pares candidatos.** Los genera un guion por mismo centro, producto o país y por citas cruzadas, y la lectura añade los que encuentre.

**Veredicto.** Cada par se cierra con la frase del artículo en que se apoya y la firma de los dos:
- **confirmado**, con los pacientes compartidos;
- **probable**, por cita o por coincidencia de datos sin identificador. Se trata como confirmado en la estimación principal y se explora en el análisis de sensibilidad 2 de la sección 16.3;
- **descartado**.

**Pacientes compartidos.** Cada uno recibe una clave de persona (P-NN), con el estudio donde se conserva y su desenlace (anexo B).

### 14.7 Pre-extracción desde el resumen
La emite el modelo de lenguaje con las instrucciones del anexo C, **después** de cerrar la extracción humana y sin que la vean los extractores. Se marca como parcial.

Es la única fuente de la medida de completitud en el resumen (sección 16.1) y de la descripción de los estudios excluidos por idioma o por texto completo, de los que no hay extracción humana. Para una ficha de registro, lee el diseño y el número de pacientes de los campos de la ficha.

**Validación.** N.T. codifica de forma independiente las mismas variables en una muestra aleatoria del 20 % de los estudios (semilla 20261008), y se informa la concordancia con el modelo.

## 15. Riesgo de sesgo

**Qué estudios.** Los que tienen **grupo concurrente sin fago**: pacientes con *P. aeruginosa*, concurrentes, que no reciben fago (placebo, atención estándar o antimicrobiano solo), con el desenlace informado por separado.
- **Comparación sin grupo sin fago.** Los estudios con etiqueta de diseño comparativo sin ese grupo se describen y no se evalúan. Es el caso de los que comparan fago con y sin antibiótico entre tratados con fago.
- **Reportes y series de casos.** No se evalúan con instrumento formal: carecen de comparador, de asignación y de seguimiento estructurado.

**Instrumentos:**
- **RoB 2** (Sterne et al., *BMJ* 2019;366:l4898) para los ensayos aleatorizados;
- **ROBINS-I** en su versión de 2016 (Sterne et al., *BMJ* 2016;355:i4919) para los no aleatorizados y las cohortes.

**Sobre qué resultado.** El éxito clínico, o el desenlace principal del estudio si no informa éxito clínico.

**Confusores preespecificados para ROBINS-I:** gravedad de la infección, control del foco (cirugía o retirada de dispositivo), antimicrobianos activos concomitantes, inmunosupresión y colonización crónica frente a infección aguda.

**Cómo se juzga.** Un juicio por dominio y uno global, sin responder las preguntas de señalización de RoB 2. Lo hacen los dos autores por duplicado e independientemente, en cuadernos generados sin juicios precargados. Se informa la concordancia previa al consenso, con la misma comprobación de textos libres coincidentes de la sección 14.3.

**Uso.** Los juicios se tabulan por dominio. Si se estima un efecto comparativo, un análisis de sensibilidad excluye los estudios con riesgo alto o grave.

## 16. Síntesis

### 16.1 Medidas de completitud
**Unidad.** El estudio, para las variables de estratificación; el brazo, para los desenlaces.

**Variables de estratificación:**
- clase de resistencia;
- vía;
- ámbito de patógeno;
- criterio DTR.

**Cómo se mide.** Para cada variable se informa en tres situaciones: declarada, mencionada pero no clasificable, o no declarada. Se mide dos veces: en el resumen, con la pre-extracción del modelo, y en el texto completo, con la extracción adjudicada (campo resistance_class_declarada para la clase).
- **Declara la clase** quien escribe MDR, XDR o PDR o sus nombres completos (*multidrug-*, *extensively drug-*, *pandrug-resistant*; multirresistente, extremadamente resistente, panresistente), o da un antibiograma que permite asignarla.
- **Mención no clasificable:** un término de resistencia que no es ninguno de esos, como «resistente a carbapenémicos», *drug-resistant* o *antibiotic-resistant*.

**Desenlaces:**
- para cada uno de los cinco, la proporción de brazos que lo informan con numerador y denominador;
- para el éxito clínico, además, la proporción con definición operativa (anexo B).

**Clase de resistencia:** la concordancia entre la declarada y la asignable con el antibiograma publicado.

**Fuente de cada medida.** El informe la declara junto a cada cifra:
- la medida en el resumen sale solo de la pre-extracción del modelo, validada por N.T. en el 20 % de los estudios (sección 14.7);
- la medida en el texto completo sale de la extracción adjudicada.

### 16.2 Síntesis narrativa
Tablas de:
- características del corpus (diseño, año, procedencia, vía, modalidad), desde la extracción adjudicada;
- completitud en el resumen frente al texto completo;
- efecto de los criterios de idioma y de texto completo;
- exclusiones por código y etapa;
- completitud por desenlace;
- embudo brazo a brazo de los requisitos de la sección 16.3.

No se usa recuento de votos.

### 16.3 Viabilidad de una proporción agrupada y plan si se agrupa
**Requisitos.** Se aplican brazo a brazo, en este orden y con los campos del anexo B:
1. numerador y denominador del éxito clínico (clinical_success_n y clinical_success_den), coherentes: el numerador no mayor que el denominador, y unidad_desenlace = paciente;
2. definición operativa del éxito clínico (definicion_tipo = en el artículo, o por referencia si así lo deciden los autores en el anexo B);
3. desenlace atribuible a *P. aeruginosa* (atribuible = sí);
4. finalidad terapéutica (finalidad = infección o colonización crónica). ‹‹DECISIÓN DE LOS AUTORES: la estimación principal incluye solo infección y la colonización crónica se estima aparte / se agrupan las dos, con análisis de sensibilidad››;
5. éxito clínico extraído como recuento binario (metrica_exito = recuento binario).

Para un efecto comparativo se exige además grupo concurrente sin fago (sección 15).

**Desenlace que se agrupa.** El éxito clínico en la última medida que informe el artículo (momento_exito_dias). El requisito 5 se refiere al dato extraído en ese campo, no al desenlace principal del estudio.

**Población de la estimación principal.**
- Entran los brazos MDR, XDR o PDR, o no clasificables.
- Los brazos por debajo del umbral MDR entran solo en un análisis de sensibilidad.
- Un brazo con pacientes de distinta clase se parte si el artículo da datos por paciente. Si no, se clasifica como mixto y sale de la estimación principal.

**Pacientes compartidos.** Cada paciente cuenta una sola vez:
- se conserva en el estudio que da su desenlace por separado y, a igualdad, en el más antiguo;
- se retira del numerador y del denominador de los demás estudios cuando el artículo da datos por paciente;
- si no se puede retirar, el brazo que lo contiene sale de la estimación principal y entra en un análisis de sensibilidad.

**Umbral.** ‹‹DECISIÓN DE LOS AUTORES: se agrupa solo si, dentro de la población de la estimación principal y tras retirar los pacientes compartidos, al menos [k] brazos con denominador de al menos [m] pacientes, de al menos [j] estudios sin solapamiento entre sí, cumplen los requisitos 1 a 5; los brazos de un solo paciente [no cuentan para el umbral ni entran en la estimación principal / cuentan y entran, con análisis de sensibilidad sin ellos]›› El umbral es una convención de los autores, no procede de una fuente metodológica, y se fija conociendo el recuento aproximado de la sección 3.2.

**Si se alcanza el umbral:**
- **Modelo.** GLMM logit-normal (R, metafor, `rma.glmm`), con efecto aleatorio de estudio y, cuando un estudio aporta varios brazos, de brazo anidado en estudio. Se informan IC 95 %, τ² e intervalo de predicción al 95 %.
- **Efecto comparativo.** Razón de riesgos con IC 95 %. Se agrupa por efectos aleatorios solo si hay al menos 2 estudios con grupo concurrente sin fago del mismo diseño.
- **Subgrupos.** Ninguno.
- **Análisis de sensibilidad:**
  1. con los brazos por debajo del umbral MDR;
  2. sin los brazos con pacientes compartidos, confirmados o probables;
  3. con o sin los brazos de un solo paciente, según lo que no haga la estimación principal;
  4. dejando fuera un estudio cada vez.
- **Certeza.** Se califica con GRADE: parte de alta para los ensayos aleatorizados y de baja para los estudios observacionales.

**Si no se alcanza:** no se agrupa, no hay análisis estadísticos de subgrupos ni de sensibilidad, no se aplica GRADE, y la síntesis es narrativa (sección 16.2).

### 16.4 Criterios para las conclusiones
- **Si no se alcanza el umbral.** La conclusión es que este cuerpo de evidencia no admite una proporción agrupada, y no se presenta ninguna.
- **Si se alcanza.** La estimación se presenta con su población, su certeza GRADE y sus análisis de sensibilidad, y no se extrapola a infecciones que no cubre.

### 16.5 Efecto de los criterios del informe
Para los criterios de idioma (IDI) y de texto completo (NOTXT) se informa, por separado y en conjunto:
- cuántos estudios deja fuera cada uno;
- cuántos diseños comparativos, según la pre-extracción del modelo;
- cuántos pacientes declarados.

Se cuentan además los estudios cuyo único motivo comprobable es IDI o NOTXT.

### 16.6 Sesgos de publicación y de notificación
**Registrado sin publicación.** Un estudio cuenta como tal si se cumplen las tres condiciones:
- su ficha completa, leída por los dos autores, cumple las secciones 8.2 a 8.5;
- su estado es completado, terminado o desconocido, con fecha de finalización primaria anterior en al menos 24 meses a la búsqueda;
- no se localiza ninguna publicación (sección 12.3).

‹‹DECISIÓN DE LOS AUTORES: solo cuentan las fichas con fecha de finalización primaria desde [año]; las anteriores se cuentan aparte››. Las fichas sin organismo declarado, y los estudios no iniciados, en reclutamiento o retirados, también se cuentan aparte.

**Notificación selectiva.** En los estudios con ficha y artículo, se compara el desenlace principal registrado con el publicado.

**Pruebas de asimetría.** Solo si se agrupa y hay al menos 10 estudios.

### 16.7 Enmascaramiento, fiabilidad y conciliación de la síntesis
La síntesis no se enmascara. Todas las cifras las calcula el canal desde los ficheros adjudicados y son reejecutables. No hay conciliación de la síntesis entre personas, porque no la calculan personas.

## 17. Fase definitiva: orden de ejecución

Ninguna etapa empieza antes del depósito.
1. Separar el piloto (`revision_sistematica/piloto/`) y dejar inactivos los guiones que llevan decisiones del piloto.
2. Búsqueda (sección 10).
3. Deduplicación, y comprobación de que cada control positivo está en el pozo.
4. Etapa 1, y control positivo.
5. Etapas 2 y 3, y control positivo. D.V. examina y registra lo que avanza, sin poder excluir.
6. Recribado ciego. Lo que, tras el consenso, habría avanzado entra en el paso 7.
7. Agrupación en estudios, enlace de cada ficha con su publicación y descarga de la ficha completa de cada registro.
8. Obtención del texto completo, con los intentos en persona de D.V. y las solicitudes si se adoptan, hasta la fecha de corte; y estimación del idioma.
9. Elegibilidad por los dos autores, y control positivo.
10. Piloteo del formulario, y registro en OSF de los cambios que resulten.
11. Extracción por duplicado y adjudicación.
12. Relectura dirigida, examen del solapamiento y fusión de los estudios que resulten ser el mismo (sección 8.1), con nueva adjudicación de los campos afectados.
13. Pre-extracción del modelo desde el resumen, y su validación.
14. Riesgo de sesgo.
15. Síntesis.
16. Si han pasado más de seis meses desde la búsqueda: reejecución (sección 10), y paso de lo nuevo por los pasos 3 a 15.
17. Comparación con el piloto (sección 3.5).

Cada etapa queda fechada en el registro de decisiones.

## 18. Declaraciones

- **Financiación:** ninguna.
- **Patrocinador:** ninguno. La Universidad Católica de Cuenca aporta el acceso a las bases mediante su suscripción y no interviene en el protocolo.
- **Conflictos de interés:** ninguno.

## 19. Uso de inteligencia artificial

**Cribado.** Las decisiones registro a registro de las etapas 2 y 3 las emite un modelo de lenguaje como revisor único, sin duplicación. D.V. es el único revisor humano: examina y registra lo que avanza, sin poder excluir.
- Un modelo de lenguaje generativo de la familia Claude (Anthropic) emite las decisiones registro a registro de las etapas 2 y 3. Aplica los criterios y el vocabulario cerrado de este protocolo y las instrucciones literales del anexo C, que redactó él mismo.
- Las decisiones se emiten en sesiones de Claude Code aisladas del repositorio (sección 3.5). No se controlan la temperatura ni la semilla de generación; se registra el identificador del modelo en cada decisión.
- Los informes que superan la etapa 3 los examina D.V. uno a uno. **Los que el modelo excluye no los relee ningún humano**, salvo los 350 de la muestra de la sección 12.6.

**Pre-extracción.** El modelo emite también la pre-extracción desde el resumen. Es la única fuente de las medidas de completitud del resumen y del efecto de los criterios del informe (sección 16), y N.T. la valida en el 20 % de los estudios.

**Canal.** El modelo escribió y ejecuta el código del canal:
- la descarga de PubMed y ClinicalTrials.gov por API, a petición de D.V.;
- la deduplicación y la etapa 1;
- la propuesta de agrupación;
- la localización y descarga de los textos completos. De lo que no consigue, y de los intentos de D.V. en persona, depende NOTXT, que firman los dos autores;
- la estimación del idioma del cuerpo de cada artículo, que es el dato en que se apoya IDI;
- la muestra del recribado ciego y los pares candidatos de solapamiento;
- la generación de los cuadernos que rellenan los autores, sin valores precargados, y la comparación, normalización e ingesta de sus respuestas, con las normalizaciones publicadas;
- el cálculo de cifras, tablas y figuras.

**Redacción.**
- El modelo redacta los borradores del informe y de los manuscritos, sobre las cifras del canal, y los autores los revisan y los aprueban.
- Redactó también el borrador de este protocolo, incluidas sus definiciones, sus reglas y los anexos B y C. Los autores lo aprueban antes del depósito, y sus cambios constan en el historial del repositorio.
- El protocolo se revisó con rondas de crítica hechas por el mismo modelo.
- Los umbrales y las demás decisiones marcadas como de los autores los fijan ellos.

**Las ecuaciones.** Las del anexo A vienen del piloto, donde las redactó el modelo y, según declara D.V., las ejecutó D.V. (sección 3.1). En la fase definitiva no se modifican.

**Lo que el modelo no hace.** No emite juicios de elegibilidad a texto completo, de extracción ni de riesgo de sesgo, ni participa en el recribado ciego. No ejecuta las búsquedas en las interfaces. Los cuadernos que reciben los autores no llevan veredictos, citas ni valores propuestos por él.

---

## Anexo A. Ecuaciones de búsqueda

### PubMed
```
ORG   = ("Pseudomonas aeruginosa"[tiab] OR "P. aeruginosa"[tiab] OR "Pseudomonas aeruginosa"[MeSH])
PHAGE = ("phage"[tiab] OR "bacteriophage"[tiab] OR "phage therapy"[tiab] OR "bacteriophage therapy"[tiab]
         OR "phagotherapy"[tiab] OR "Bacteriophages"[MeSH] OR "Phage Therapy"[MeSH])
CLIN  = (case reports[pt] OR clinical trial[pt] OR observational study[pt] OR comparative study[pt]
         OR multicenter study[pt] OR journal article[pt])
VENTANA = ("2016"[dp] : "2026"[dp])
Brazo A: ORG AND PHAGE AND CLIN AND VENTANA
Brazo B: PHAGE AND humans[mh] AND VENTANA
```

### Scopus
La consulta se pasa como parámetro de la URL de resultados y no se teclea en la caja, para que el traductor del navegador no la reescriba.
```
Brazo A:
TITLE-ABS-KEY ( ( "Pseudomonas aeruginosa" OR "P. aeruginosa" OR pseudomonal )
  AND ( phage* OR bacteriophage* OR phagotherap* OR "phage therapy" OR "phage cocktail"
        OR pyophage OR intestiphage ) )
AND PUBYEAR > 2015 AND PUBYEAR < 2027

Brazo B:
TITLE-ABS-KEY ( ( phage* OR bacteriophage* OR phagotherap* )
  AND ( "phage therapy" OR "bacteriophage therapy" OR compassionate OR salvage OR "expanded access"
        OR "named patient" OR "case report" OR "case series" OR patient OR patients OR clinical ) )
AND PUBYEAR > 2015 AND PUBYEAR < 2027
AND ( LIMIT-TO ( SUBJAREA , "MEDI" ) OR LIMIT-TO ( SUBJAREA , "IMMU" ) OR LIMIT-TO ( SUBJAREA , "PHAR" ) )
```

### Cochrane CENTRAL (Wiley)
```
#1 MeSH descriptor: [Pseudomonas aeruginosa] explode all trees
#2 MeSH descriptor: [Pseudomonas Infections] explode all trees
#3 ("Pseudomonas aeruginosa" OR "P aeruginosa" OR pseudomonal):ti,ab,kw
#4 #1 OR #2 OR #3
#5 MeSH descriptor: [Bacteriophages] explode all trees
#6 ("phage" OR "phages" OR bacteriophage* OR phagotherap* OR "phage therapy" OR "phage cocktail"
    OR Pyophage OR Intestiphage):ti,ab,kw
#7 #5 OR #6
#8 #4 AND #7     (brazo A)
#9 #7            (brazo B)
```
**Límites.** *CENTRAL Trials*, año de publicación original de 2016 a 2026, con *Search word variations* activada. Se registra el número (*Issue*) de CENTRAL consultado, por ejemplo «Issue 7 of 12, July 2026».

**Lectura del fichero.** Se lee como latin-1, y el identificador propio de cada registro está en el campo `C3`.

### BVS
```
(fago OR fagos OR bacteriofago OR bacteriófago OR bacteriofagos OR fagoterapia OR phage OR phages
 OR bacteriophage OR bacteriophages OR "phage therapy" OR "terapia con fagos" OR "terapia fágica")
AND NOT db:("MEDLINE")
```
Los PMID llegan con el prefijo `mdl-`, que se traduce antes de deduplicar.

### SciELO
```
fago OR fagos OR bacteriofago OR bacteriófago OR bacteriófagos OR fagoterapia OR phage OR phages
OR bacteriophage OR bacteriophages OR "phage therapy" OR "terapia fágica"
```

### ClinicalTrials.gov (API v2)
```
Brazo A: query.cond = "Pseudomonas aeruginosa"; query.intr = "bacteriophage OR phage"
Brazo B: query.intr = "bacteriophage OR phage"
```

### EudraCT
```
bacteriophage OR phage OR phagotherapy
```

### CTIS
Un término por búsqueda, con unión manual: *bacteriophage*, *bacteriophages*, *phage*, *phages*, *phagotherapy*, *pyophage*. Término de control: *cancer*.

## Anexo B. Diccionario de variables y reglas de extracción

Una fila por brazo. Los valores entre corchetes son los únicos admitidos. Las reglas de este anexo las redactó el modelo a partir de las del piloto y de las decisiones firmadas en él (sección 3.3); los autores las aprueban expresamente antes del depósito.

**Identificación**
- **study_id:** DEF-NNN.
- **arm_id:** A, B, C… según la definición de brazo de la sección 14.2.
- **fila_control:** [sí, no]. Las filas de control no son brazos y no entran en la viabilidad.
- **informe_de_extraccion:** identificador del informe del que se extrae (sección 14.1).

**Diseño y población**
- **study_design:** lo que el artículo es, no lo que dice ser. Un «estudio» de un paciente es un reporte de caso. [ensayo aleatorizado, ensayo no aleatorizado, cohorte prospectiva, cohorte retrospectiva, serie de casos, reporte de caso, otro]
- **n_arm:** pacientes de este brazo.
- **pathogen_scope:** [solo *P. aeruginosa*, mixto con subgrupo separable, mixto sin desenlace separable]
- **atribuible:** si el desenlace extraído corresponde a pacientes con *P. aeruginosa*. [sí, no, no se sabe]
- **finalidad:** [infección, colonización crónica, profilaxis]

**Clase de resistencia**
- **resistance_class_declarada:** lo que dice el artículo, con las definiciones de la sección 16.1. [MDR, XDR, PDR, mencionada pero no clasificable, no mencionada]
- **resistance_class:** la clase asignada según Magiorakos et al. [MDR, XDR, PDR, por debajo del umbral MDR, no clasificable, mixto]
- **resistance_class_source:** [declarada por el autor, verificada con el antibiograma, verificada con el texto, no clasificable]
- **Reglas de asignación de la clase y del DTR:**
  - se asignan con el último aislado del sitio tratado anterior al primer fago;
  - la «I» cuenta como no sensible, como en Magiorakos, aunque el artículo use EUCAST 2019 o posterior;
  - una categoría no probada no cuenta como no sensible; si eso impide decidir entre dos clases, se codifica la inferior y se anota «superior no derivable»;
  - los agentes que no figuran en Magiorakos y la resistencia intrínseca no cuentan para la clase;
  - un brazo con pacientes de clase distinta es «mixto».
- **dtr_status:** *difficult-to-treat resistance* según Kadri et al. (*Clin Infect Dis* 2018;67:1803-14). [sí, no, no derivable, mixto]
  - **sí:** toda la primera línea (carbapenémicos, otros betalactámicos y fluoroquinolonas) es no sensible, incluido el aislado PDR;
  - **no:** basta un agente de primera línea sensible documentado;
  - **no derivable:** el resto.
  - **Agentes que no cuentan:** los de reserva (colistina, polimixina B, aminoglucósidos, tigeciclina) y los posteriores a 2018 (ceftazidima-avibactam, ceftolozano-tazobactam, imipenem-relebactam, cefiderocol).

**Intervención**
- **route:** si hay varias vías, «otra», con la explicación. [IV, inhalada o nebulizada, tópica o local, oral, intravesical, intraarticular, otra, NA]
- **modality:** [fago en monoterapia, fago con antibiótico, fago con otro, NA]

**Desenlaces.** Cada uno lleva numerador y denominador propio, y cada valor es un número, 0 o NA.
- **unidad_desenlace:** [paciente, curso, infección] (sección 14.2).
- **Éxito clínico:**
  - **clinical_success_n y clinical_success_den:** numerador según la definición del autor.
  - **clinical_success_definition:** la definición literal del autor, o exactamente SIN DEFINICIÓN OPERATIVA. Es definición operativa la que fija qué había que observar, en qué plazo o con qué instrumento para contar a un paciente como éxito clínico. No lo es el juicio del médico sin criterio declarado, ni la definición de un desenlace microbiológico o de un tiempo.
  - **definicion_tipo:** [en el artículo, por referencia a otra publicación, juicio clínico sin criterio, ninguna]. ‹‹DECISIÓN DE LOS AUTORES: si la definición dada solo por referencia a otra publicación cuenta como definición operativa››
  - **metrica_exito:** [recuento binario, tiempo, variable continua, no informado]
  - **momento_exito_dias:** días desde el inicio del fago hasta la última medida del éxito que informe el artículo (sección 16.3).
- **Erradicación:**
  - **eradication_n:** cultivo de control negativo para el organismo diana, es decir, el aislado resistente que motivó el tratamiento, no la especie. Del mismo sitio, en el primer cultivo de control posterior al fin de la fagoterapia, del que se anota el día. En terapia supresiva indefinida, el cultivo del cierre del seguimiento. Si el artículo declara el resultado microbiológico, esa declaración manda.
  - **eradication_den:** pacientes con cultivo de control.
  - **eradication_sustained:** [sostenida, recaída, no evaluable], según los 30 días siguientes al primer cultivo negativo.
  - **Colonización crónica de vía aérea:** un solo cultivo negativo se anota NA, salvo que el artículo declare erradicación sostenida con cultivos seriados.
- **Eventos adversos (adverse_event_n y adverse_event_den):** pacientes con algún evento adverso. Cero notificados es 0, no NA.
- **Mortalidad (mortality_n y mortality_den):** fallecidos en el seguimiento.
- **Emergencia de resistencia al fago (resistance_emergence_n y resistance_emergence_den):** pacientes en que aparece durante el tratamiento.
- **los_days:** días de estancia hospitalaria.

**Pacientes compartidos (sección 14.6).** Por cada uno: clave de persona (P-NN), estudios en que aparece, estudio donde se conserva y su desenlace.

**Contexto y trazabilidad**
- **publication_year**.
- **geographic_source:** país y, si consta, ciudad.
- **extraction_citation:** página, tabla o figura de cada cifra del brazo.
- **extraction_status:** [completa, parcial, incompleta]
- **incomplete_reason:** qué faltó y por qué.

## Anexo C. Instrucciones literales al modelo de lenguaje

**Etapa 2 (título).**
> Recibes el título de un registro bibliográfico. La revisión incluye estudios con pacientes humanos con infección o colonización crónica por *Pseudomonas aeruginosa* tratados con bacteriófagos líticos. Responde con un solo valor de esta lista: AVANZA, ORG, REV, SEC, LAB, VET, OFF, PRF. ORG: el título muestra que el estudio trata otro organismo y ningún paciente con *P. aeruginosa*. REV: revisión narrativa, editorial o comentario sin datos de pacientes propios. SEC: revisión sistemática o de alcance. LAB: laboratorio, preclínico o modelización, incluidos los modelos animales de laboratorio, sin pacientes tratados. VET: animales de granja o de compañía, o aislados veterinarios. OFF: no trata de administrar fagos a pacientes (encuesta, epidemiología, prensa, otra terapia, fago como herramienta de laboratorio). PRF: administración para prevenir una infección a personas sin infección o a portadores no crónicos; si el título menciona también el tratamiento de una infección, responde AVANZA. Si el título no permite decidirlo con seguridad, responde AVANZA. No uses ningún otro código. No excluyas por el idioma ni por el año. Si el título sugiere que se describe al menos un paciente tratado con fagos, responde AVANZA aunque sea una carta, un editorial o una revisión.

**Etapa 3 (resumen).** La misma instrucción, con estos cambios:
- recibes el título, el resumen, la revista, el tipo documental y el año;
- si es una ficha de registro de ensayo, recibes el título oficial, el resumen breve, las condiciones, las intervenciones, los criterios de elegibilidad y el diseño;
- ORG también cuando el resumen o la ficha muestran que ningún paciente tiene *P. aeruginosa*;
- PRF se responde AVANZA si el resumen o la ficha mencionan también el tratamiento de una infección;
- el año no se usa para excluir.

**Pre-extracción desde el resumen.**
> Recibes el título y el resumen de un estudio, o los campos de una ficha de registro de ensayo. Para cada variable, contesta solo con lo que el texto dice: no deduzcas lo que no está escrito. study_design: [ensayo aleatorizado, ensayo no aleatorizado, cohorte prospectiva, cohorte retrospectiva, serie de casos, reporte de caso, no declarado]. resistance_class_declarada: [MDR, XDR, PDR, mencionada pero no clasificable, no mencionada]; declara la clase quien escribe MDR, XDR o PDR o sus nombres completos, o da un antibiograma que permite asignarla; «mencionada pero no clasificable» es un término de resistencia que no es ninguno de esos, como «resistente a carbapenémicos». route, pathogen_scope y dtr_status: el valor del anexo B, o «no declarado». n_arm: número de pacientes, o «no declarado». clinical_success_definition: la definición literal si el texto la da, o «no declarada». Marca la fila como PARCIAL.

## Anexo D. Conjunto de control positivo

42 estudios fijados el 29 de julio de 2026, antes del cribado piloto (commit 20574ce). Sus identificadores, no los estudios, se corrigieron en la versión generada el 5 de agosto y registrada el 10 de agosto de 2026 (commit 4258270; `quality_reports/corpus_identifier_index.txt`). Se comprueban por DOI, PMID o NCT:

ArmataAP_PA02; Arya2026_pji; Aslam2019; Aslam2020; Blasco2023; Casazza2025; Cesta2023; Chan2018_omko1; Chan2025; Chen2022_empyema; Chung2026; Denis2026; Duplessis2018; Ferry2021; Ferry2022; Green2023; Hahn2023; Jault2019_PhagoBurn; Jennes2017; Khatami2021; Kohler2023; Law2019; Leitner2021; Leveque2023; Li2023_ILD; Li2025_biliary; Liu2025_perinephric; Maddocks2019; Malhotra2026; Ngauy2026; Onallah2023_PASA16; PardoFreire2025; Pirnay2024; Racenis2022_femur; Racenis2023_LVAD; Ronit2024; Rubalskii2020; Teney2024; Tkhilaishvili2020; Weiner2025_BX004A; Yang2025; Zaldastanishvili2021.

## Anexo E. Correspondencia con la plantilla GSRRF de OSF

| Campo | Sección |
|---|---|
| 1 Título | título |
| 2 Contribuidores | 4 |
| 3 Materias | palabras clave |
| 4 Tareas y funciones | 4 y 19 |
| 5 Tipo de revisión | cabecera |
| 6 Etapas de la revisión | 17 |
| 7 Etapa actual | Estado al registrar |
| 8 Fecha de inicio | Fechas previstas |
| 9 Fecha de fin | Fechas previstas |
| 10 Antecedentes | 6 |
| 11 Preguntas principales | 7 |
| 12 Preguntas secundarias | 7 |
| 13 Expectativas | 3.2 |
| 14 Desenlaces y variables principales | 8.5, 16.1 |
| 15 Intervención | 8.4 |
| 16 Variables adicionales | anexo B |
| 17 Programas | 11 |
| 18 Financiación | 18 |
| 19 Conflictos de interés | 18 |
| 20 Autoría solapada | 4 |
| 21 Bases de datos | 9 |
| 22 Interfaces | 9 y anexo A |
| 23 Literatura gris | 9 (registros de ensayos; no se busca más literatura gris) |
| 24 Criterios de inclusión y exclusión | 8 |
| 25 Ecuaciones | anexo A |
| 26 Validación de la búsqueda | no se valida la sensibilidad de la búsqueda: el conjunto de control (anexo D) se usó para diseñar las ecuaciones y solo acota lo que pierde la selección (3.4 y 12.5); tras deduplicar se comprueba que cada control está en el pozo (17, paso 3) |
| 27 Otras estrategias de búsqueda | 9 |
| 28 Contacto con autores | 13 |
| 29 Resultados del contacto | no aplica al registrar |
| 30 Caducidad y repetición de la búsqueda | 10 y 17, paso 16 |
| 31 Justificación de la estrategia | 10 |
| 32 Otros detalles de la búsqueda | 10 y anexo A |
| 33 Etapas del cribado | 12.1-12.4: etapa 1, ordenador; etapas 2 y 3, exclusiones emitidas por IA sin supervisión humana registro a registro, y lo que avanza, revisado por un humano; etapa 4, dos humanos independientes |
| 34 Campos visibles al cribar y enmascaramiento | 12.2 y 3.5; no se enmascaran autores ni revista |
| 35 Criterios de exclusión usados | 8.8 |
| 36 Instrucciones del cribado | anexo C |
| 37 Fiabilidad del cribado | 12.4, 12.6 |
| 38 Conciliación del cribado | 12.4 y 12.6; las etapas 2 y 3 no tienen conciliación (un solo revisor) |
| 39 Muestreo y tamaño de muestra | 12.6 |
| 40 Justificación del procedimiento de cribado | 12.2 y 19; sin justificación más allá de la descripción y de la validación de 12.6 |
| 41 Gestión y publicación de datos | 11 |
| 42 Otros detalles del cribado | 12.3 |
| 43 Entidades que se extraen | anexo B |
| 44 Etapas de la extracción | 14.2, 14.3, 14.5 |
| 45 Instrucciones de extracción | anexo B |
| 46 Enmascaramiento de los extractores | 3.5, 14.3 |
| 47 Fiabilidad de la extracción | 14.3 |
| 48 Conciliación de la extracción | 14.3 |
| 49 Justificación del procedimiento de extracción | 14; sin justificación más allá de la descripción |
| 50 Gestión y publicación de datos | 11 |
| 51 Otros detalles de la extracción | 14.6, 14.7 |
| 52 Transformaciones previstas | 16.3 (logit) |
| 53 Datos faltantes | 14.4 |
| 54 Validación de datos | 14.3, 14.5, 14.7 y 16.7 |
| 55 Evaluación de la calidad | 15 |
| 56 Plan de síntesis | 16 |
| 57 Criterios para las conclusiones | 16.4 |
| 58 Enmascaramiento en la síntesis | 16.7 |
| 59 Fiabilidad de la síntesis | 16.7 |
| 60 Conciliación de la síntesis | no aplica: la síntesis la calcula el canal (16.7) |
| 61 Sesgo de publicación | 16.6 |
| 62 Análisis de sensibilidad | 16.3 |
| 63 Justificación del procedimiento de síntesis | 6, 16.3 |
| 64 Gestión y publicación de los datos de la síntesis | 11 |
| 65 Otros detalles de la síntesis | 16.5 |
