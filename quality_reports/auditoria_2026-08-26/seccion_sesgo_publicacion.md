# Sesgo de publicación en los registros del corpus — texto propuesto

Este análisis **sí usa el corpus del manuscrito**. Los identificadores de registro se
recuperaron de `revision_sistematica/cribado/study_groups.csv`: 39 de los 60 estudios
clasificados como solo-registro tienen un NCT recuperable. Los 21 restantes provienen de
CTIS, EudraCT y otros registros sin API equivalente.

Comprobación previa: el censo que se había construido a ciegas contra ClinicalTrials.gov
coincide **exactamente** con `revision_sistematica/busqueda/clinicaltrials_gov.csv`
—121 registros, intersección total, ninguno sobrante por ningún lado—, lo que valida la
ecuación de búsqueda del artículo de forma independiente.

---

## Métodos (para añadir a la sección de métodos de síntesis)

Los 121 registros del export de ClinicalTrials.gov se adjudicaron uno a uno sobre la
ficha completa, retirando 18: cinco por usar fagos como herramienta de laboratorio y no
como terapia —presentación en fago para mapear epítopos, MS2 como indicador de
desinfección de agua, MS2 como marcador de contaminación de equipo de protección,
phiX174 como antígeno de vacuna— y uno por una errata de «Phase II» escrita «Phage II».
Los productos identificados solo por nombre comercial (TP-102, LBP-EC01, BX002-A,
BX005-A, AP-SA02, MP101, DUOFAG) se confirmaron sobre la ficha antes de retenerlos.
Quedaron **103 registros de fagoterapia**.

De los 103 registros de fagoterapia, 31 tienen estado COMPLETED o TERMINATED; 28 de
ellos declaran además fecha de finalización primaria, y son esos 28 los que se cruzaron
contra PubMed por su identificador NCT, con una ventana de gracia de 24 meses desde el
cierre. Los 3 sin fecha declarada quedan fuera del análisis de latencia porque no hay
punto de partida desde el que contar. El intervalo de confianza es exacto por Clopper-Pearson.

## Resultados (para añadir como subsección de resultados)

**Estado de los 39 estudios solo-registro con NCT.** Dieciocho están en curso o por
empezar, nueve cerrados, seis retirados o no disponibles y **seis en estado UNKNOWN**, es
decir, con la ficha sin actualizar en más de dos años sobre un ensayo que declaraba estar
en marcha. Los cuatro grupos suman los 39. El estado se tomó del campo `overallStatus` del
propio export del artículo (`revision_sistematica/busqueda/clinicaltrials_gov.csv`), no del
censo depurado de 103 registros: uno de los 39 —NCT05277350, COMPLETED— se retiró de ese
censo en la adjudicación por no acreditar fago terapéutico, pero sigue siendo uno de los
39 estudios solo-registro y cuenta en este desglose. En conjunto declaran **2 309 pacientes previstos**, frente a los 1 042
pacientes de los 91 estudios con texto completo obtenido.

Nota de conciliación de denominadores: los 39 incluyen NCT05277350, y por tanto sus 36
pacientes entran en los 2 309. Ese registro no entra, en cambio, en el análisis de tasa de
publicación de la subsección siguiente, que parte de los 103 registros de fagoterapia. La
diferencia —39 aquí, 38 allí— es intencionada; antes del envío debe decidirse si el registro
se retiene con justificación o se retira del recuento de solo-registro con NCT.

**Tasa de no publicación.** De los 23 ensayos de fagoterapia cerrados hace 24 meses o más,
**14 no tienen publicación indexada que cite su identificador de registro: el 60,9 %
(IC 95 % 38,5 a 80,3 %)**. Esos 14 declaran 671 pacientes reclutados, frente a 496 en los
9 que sí publicaron. La latencia mediana de los no publicados es de 74,9 meses desde el
cierre, y el caso extremo lleva **235 meses —19,6 años— cerrado sin publicar**
(NCT00089180, National Cancer Institute, 100 pacientes).

**Control de circularidad.** Siete de esos 23 ensayos pertenecen al subgrupo solo-registro
del propio corpus, donde la no publicación es una consecuencia definicional del cribado.
Restringiendo el análisis a los **16 ensayos que el cribado no clasificó como
solo-registro**, la tasa es de **8 de 16, el 50,0 % (IC 95 % 24,7 a 75,3 %)**. El sesgo,
por tanto, no es un artefacto de la clasificación.

**Un error de clasificación.** NCT00937274, clasificado como solo-registro, sí tiene
publicación: un ensayo aleatorizado de fagoterapia oral en diarrea infantil (EBioMedicine,
2016; PMID 26981577). Es el único error sobre 39 registros cribados, y debe corregirse
antes del envío.

## Interpretación (para la discusión)

La medida reemplaza una observación cualitativa por una tasa con intervalo de confianza, y
tiene tres consecuencias para el argumento.

Primera, **refuerza la conclusión sobre la viabilidad de la síntesis**. Con la mitad de los
ensayos cerrados sin publicar —incluso descontando el subgrupo definido por la propia
clasificación—, cualquier metaanálisis del campo trabaja sobre un subconjunto seleccionado
por la publicación misma, y no solo por la recuperación del texto completo. Es un sesgo que
se acumula sobre el de idioma y el de recuperación ya medidos.

Segunda, **responde al ítem 21 de PRISMA**, hoy PARCIAL en la lista de comprobación. Un
análisis del registro es la evidencia que ese ítem pide y permite elevarlo a CUMPLE.

Tercera, **es un desenlace de meta-investigación por derecho propio**. La tasa con su
latencia, más los registros en estado UNKNOWN, son citables con independencia del resto del
artículo.

## Límites de este análisis

El cruce por identificador NCT **subestima la publicación**: un artículo que reporte el
ensayo sin citar su NCT en el registro indexado cuenta como no publicado. La dirección del
error es conocida y conservadora en contra de la tesis, lo que conviene declarar. El
control es el cribado manual por título, patrocinador y ventana temporal en los 14 casos.

El análisis cubre 39 de los 60 estudios solo-registro. Los 21 restantes provienen de CTIS
(10 registros en el export del artículo), EudraCT (3) y otros registros que no exponen una
interfaz consultable equivalente; su cribado exige consulta manual.

El intervalo de confianza es ancho porque el denominador es pequeño: 23 ensayos en el
análisis principal, 16 en el control de circularidad. Es una limitación del campo, no del
método.
