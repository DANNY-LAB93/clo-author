# NOORG: el undécimo código, las siete últimas fichas y un ensayo contado dos veces

**Estado:** APLICADO el 14 de septiembre de 2026. Enmienda al protocolo y siete
exclusiones firmadas por D. Valdiviezo y N. Trelles. **El asunto del organismo
de las fichas queda cerrado.**
**Ficheros:** `scripts/exclusion_codes.py`, `scripts/ingest_noorg.py`,
`scripts/group_reports_into_studies.py`,
`revision_sistematica/cribado/exclusiones_tras_texto_completo.csv`,
`revision_sistematica/textos_completos/fulltext_identifiers.csv`
**Viene de:** [2026-09-14_diez-exclusiones-firmadas-y-un-codigo-que-falta.md](2026-09-14_diez-exclusiones-firmadas-y-un-codigo-que-falta.md)

## Lo que se firmó

Las siete filas abiertas, las siete con el mismo veredicto: **excluir con
NOORG**. La enmienda del código, aceptada. Y en la hoja del duplicado,
EST-186 como ficha principal, «por fecha»: es la versión de 2023 del protocolo,
la vigente, y EST-187 es la de 2022 que quedó atrás.

El comentario por estudio volvió a venir en blanco, las dos veces. Lo pedí como
obligatorio y no lo era: el motivo de cada exclusión no depende de que nadie lo
teclee. Lo fija el código que sí firmaron más la evidencia que ya estaba
extraída de la ficha, y así se construye —`ingest_noorg.py` no redacta nada—.
Lo dejo dicho porque lo anuncié al revés.

## El código

```
NOORG   La ficha de registro no declara ningún organismo: el criterio de
        P. aeruginosa no se puede verificar ni a favor ni en contra
```

**Por qué no valía ORG.** ORG afirma «organismo distinto de *P. aeruginosa*».
En estas siete fichas no hay organismo ninguno. Decir «distinto» sería afirmar
más de lo comprobado, que es exactamente el error que costó cuatro exclusiones
por idioma el 1 de septiembre: la clase de evidencia se llamaba «texto probado»
y solo se había leído el resumen.

**De qué familia es.** Hermano de NOREC. Los nueve primeros códigos excluyen
por lo que el estudio **dice**; NOREC por lo que la revisión **no pudo leer**;
NOORG por lo que el registro **no declara**. Los dos últimos son propiedades
del proceso, no del estudio, y el manuscrito los declara como tales.

**El motivo y la cita, medidos, no redactados.** Para cinco de las siete el
script vuelve a comprobar sobre el JSON entero que «Pseudomonas» y «aeruginosa»
no aparecen en ningún campo, y lo escribe así. Para las otras dos —EST-141 y
EST-203— sí aparecen, y el motivo dice dónde y por qué no sirve: están en el
espectro lítico declarado del preparado de fagos, no en la bacteria de los
pacientes, cuyos criterios de elegibilidad no exigen ningún organismo. La frase
se extrae del JSON en los dos casos.

## El duplicado, y lo que destapó

Phage4Cure-001 está en CTIS con dos identificadores, uno por versión del
protocolo («two part», decisión 2023-07-07, y «three part», decisión
2023-08-08). Entró como dos estudios porque sus títulos difieren en dos
palabras.

Lo llamativo es que **los dos informes llevaban escrito el mismo código de
protocolo desde el principio**, en la columna `identificador_resuelto` de
`fulltext_identifiers.csv`. La cadena de claves de
`group_reports_into_studies.py` solo entendía NCT, PMID y DOI, así que ignoraba
esa atribución y agrupaba por título. **Eran 21 las atribuciones ignoradas**:
ChiCTR, IRCT, ACTRN, CTRI, KCT, números CTIS y códigos de protocolo. Ahora la
cadena las honra. De las 21, solo Phage4Cure-001 se repite, de modo que el
cambio fusiona exactamente el par que los autores firmaron y no toca nada más
—comprobado con `git diff`: cambiaron dos registros, ninguno más—.

## El defecto que apareció al reejecutar, y que era el peligroso

Reejecutar `group_reports_into_studies.py` **renumeraba estudios del corpus sin
que nada fallara**. La numeración estable se anclaba en la clave del estudio, y
la clave cambia sola: en cuanto `fulltext_identifiers.csv` resuelve el DOI de un
resumen de congreso, la clave pasa de `T:titulo...` a `doi:...`, el estudio
parece nuevo y recibe un número nuevo. En la primera reejecución de hoy,
**EST-133 y EST-188 se convirtieron en EST-220 y EST-221**. Sus números están en
los cuadernos de extracción firmados por las dos personas: renumerar en silencio
reasigna el trabajo de alguien a un estudio que no leyó. Se revirtió.

El ancla ahora son los **informes**: un estudio es el conjunto de sus
`record_id`, que se derivan del contenido. Si el grupo de hoy comparte aunque
sea un informe con un estudio de ayer, es ese estudio y conserva su número,
cambie su clave lo que cambie. Y cuando hereda de más de uno —una fusión— se
queda con el número más bajo y el script lo anuncia. Reejecutarlo es ahora
idempotente: `git diff` sobre `study_groups.csv` sale vacío.

## Lo que se movió

| | Antes | Ahora |
|---|---|---|
| Estudios | 155 | **137** |
| Excluidos tras el cribado | 29 | **46** (22 por el artículo, 17 por la ficha, 7 sin poder leer nada) |
| Estudios evaluados para elegibilidad | 184 | **183** (la fusión) |
| Solo ficha de registro | 60 | **42** |
| Informes agrupados | 190 | **171** |

**Lo que NO se movió, y es lo que sostiene el artículo:** 95 extraíbles, 103
brazos, 71 textos completos (74,7 %), 11 comparativos, 82 juicios de riesgo de
sesgo, el 67,0 % de brazos sin definición operativa de éxito clínico, el 44,2 %
de reportes de caso único. Los 18 estudios que salieron eran todos
`solo-registro`, sin texto y sin brazo extraído.

## Lo que cuesta, y que consta en el manuscrito

Estos siete estudios eran parte de la evidencia de lo que el propio artículo
sostiene: que este cuerpo de literatura no admite verificación. Lo dije antes de
que se firmara y lo repito aquí porque ahora está aplicado. Salen del total y se
cuentan uno por uno en la Figura 1 y en S16, con su código y con la frase del
registro que lo sostiene. El párrafo de §3.1.1 lo declara en los tres
manuscritos: «conviene decir lo que cuestan».
