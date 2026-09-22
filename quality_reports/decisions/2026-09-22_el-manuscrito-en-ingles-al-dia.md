# El manuscrito en inglés, al día — y los dos agujeros que lo dejaron envejecer

**Estado:** APLICADO el 22 de septiembre de 2026.
**Viene de:** `2026-09-22_las-nueve-ingeridas-y-el-ingles-que-nadie-miraba.md`,
que lo dejó declarado y sin arreglar.
**Ficheros:** `paper/manuscript_systematic_review_en.md`,
`scripts/build_lista_anexos.py` (nuevo), `scripts/check_manuscript_claims.py`,
`scripts/sync_manuscript_numbers.py`, `scripts/check_manuscript_numbers.py`,
`scripts/build_rob_table.py`, `scripts/build_package_guide.py`,
`scripts/build_synthesis_scalars.py`.

## Qué decía

Iba dos revisiones del corpus atrás: «Of the 145 studies», «184 studies
assessed for eligibility», «39 of them left the corpus», 219, 179, 123, 50, y
la composición por diseño con «4 non-randomised trials» cuando son 3. Su
sección 2.9 se titulaba «Protocol amendment: the language criterion» aunque el
cuerpo ya traía las dos enmiendas. Y arrastraba la frase que dejó de ser cierta
el 22 de septiembre: «Two arms report a numerator larger than their
denominator».

Su **lista de anexos estaba en español** —salvo dos entradas— y citaba 16 de
los 24 que el paquete envía.

## Por qué nadie lo vio

**Primer agujero: el guardián no lo miraba.** `check_manuscript_numbers.py`
comprobaba el maestro y el de la revista. El inglés no viaja en el sobre ni en
el `.zip`, así que quedó fuera. Ahora comprueba los tres.

**Segundo agujero: una cifra puede estar «respaldada» por casualidad.** Ese
guardián solo mira si el valor existe en los escalares, no si es el escalar que
le toca. «46», «71», «18» y «95» pasaban porque esos números existen con otro
significado —46 en MDR/XDR/PDR, 71 celdas de dominio, 18 series de casos—.
Salieron los cuatro a la vez al bajar el corpus a 136, en los **tres**
manuscritos, no solo en el inglés.

**Tercer agujero, y es el que más incomoda: una cifra escrita EN LETRA se
escapa entera.** Los tres guardianes buscan dígitos. La sección 3.1.1 enumera
las exclusiones con palabras, y al salir EST-063 se volvieron falsas
«Veintinueve», «Veinticuatro» y «Cuatro son protocolos» —las tres, en los tres
manuscritos— sin que nada fallara. Un hueco `{letras_<escalar>}` se resuelve
ahora como la palabra, en el idioma del manuscrito, y el sincronizador sabe
casarla contra una palabra en vez de contra un número.

## Lo que se corrigió

| | Antes | Ahora |
|---|---|---|
| Corpus, en el inglés | 145 | **136** |
| Evaluados para elegibilidad | 184 | **183** |
| Salieron al leer el texto | 39 | **47** |
| Informes agrupados | 179 | **170** |
| Solo ficha de registro | 50 | **42** |
| Brazos | 103 y 132 | **102** |
| Ensayos no aleatorizados | 4 | **3** |
| Comparativos | 11 (11,6 %) | **10 (10,6 %)** |
| Anexos citados | 16, en español | **24, en inglés** |
| «Veintinueve / Veinticuatro / Cuatro» | 29 / 24 / 4 | **30 / 25 / 5** |
| «Los 87 juicios» | 87 | **82** |

Los 87 eran las 90 filas del fichero de riesgo de sesgo menos las 3 corregidas
el 22 de septiembre: `procedencias()` contaba sin filtrar a los excluidos y
trataba una corrección firmada como una procedencia distinta del consenso.
Ahora filtra y las agrupa, porque una corrección firmada por los dos revisores
**es** un consenso; lo que cambia es cuándo se firmó.

## Lo que NO se tocó, y por qué

«**29 de los 95 estudios extraíbles**» es una **medición histórica**: cuántos
tenían la clase de evidencia de idioma mal nombrada antes de renombrarla. La
clase ya no existe, de modo que el 29 no se puede recalcular, y cambiarle el
denominador a 94 produciría un par que nadie midió nunca. La frase se puso en
pasado —«y eran 29 de los 95 estudios extraíbles de entonces»— en lugar de
maquillar las cifras, y el 29 consta como excepción declarada.

## La lista de anexos ya no se escribe a mano

`build_lista_anexos.py` la escribe en el maestro y en el inglés desde una sola
tabla, con las cifras por nombre desde los escalares, y **se niega a escribir**
si cita un anexo que el paquete no envía o si el paquete envía uno que la lista
no cita. Antes eran dos listas independientes y las dos se quedaron cortas.

## Estado

Los tres manuscritos pasan los cuatro guardianes. **217 afirmaciones ancladas**
—eran 131 esta mañana— y ninguna cifra sin respaldo en ninguno de los tres. Las
17 cifras de `audita_cifras.py` se reproducen, 17 de 17.
