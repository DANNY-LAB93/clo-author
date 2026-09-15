# Diez exclusiones firmadas y aplicadas; seis esperan un código que no existe

> **ACTUALIZADO el 14 de septiembre de 2026, más tarde el mismo día.** Las siete
> filas que este registro dejaba abiertas ya están cerradas: la enmienda del
> código NOORG se firmó y las siete exclusiones están aplicadas. El corpus está
> en 137, no en 145. El texto de abajo se conserva entero porque es lo que se
> propuso y por qué. Ver
> [2026-09-14_codigo-noorg-y-la-fusion-de-phage4cure.md](2026-09-14_codigo-noorg-y-la-fusion-de-phage4cure.md).

**Estado:** APLICADO el 14 de septiembre de 2026, firmado por D. Valdiviezo y
N. Trelles. **Siete filas siguen abiertas.**
**Ficheros:** `scripts/ingest_organismo.py`, `scripts/make_firma_noorg.py`,
`revision_sistematica/cribado/exclusiones_tras_texto_completo.csv`,
`quality_reports/organismo_pendiente.json`,
`~/Escritorio/FIRMAR_codigo_NOORG_y_duplicado.xlsx`
**Viene de:** [2026-09-14_organismo-de-las-fichas-de-registro.md](2026-09-14_organismo-de-las-fichas-de-registro.md)

## Lo que devolvió el cuaderno

Firmado por los dos revisores con nombre completo y fecha. De 29 filas, 28
decididas y una en blanco. Los 12 CUMPLE y los 10 NO CUMPLE, confirmados tal y
como venían propuestos. Y **seis INDETERMINADO cambiados a NO CUMPLE**:
EST-141, EST-148, EST-192, EST-203, EST-209 y EST-214, ninguno con comentario.
En la hoja del duplicado, N. Trelles confirmó que EST-186 y EST-187 son el
mismo ensayo.

## Lo que se aplicó

Las **diez** exclusiones confirmadas, con su código ya existente (ORG en ocho,
OFF en dos), su motivo y la frase literal de la ficha. El corpus pasa de **155
a 145 estudios**.

Nada de lo que se movió toca la extracción ni los desenlaces: los diez son
`solo-registro`, ninguno tiene texto completo y ninguno aportó un brazo
extraído. Los extraíbles siguen en 95, los brazos en 103, el 67,0 % sin
definición operativa de éxito clínico y el 44,2 % de reportes de caso único no
se mueven. Lo que cambia es el total, el diagrama PRISMA, el recuento de
informes agrupados (190 → 179) y el número de estudios que son solo ficha de
registro (60 → 50).

## Lo que NO se aplicó, y por qué

**Las seis firmadas NO CUMPLE sin código.** No es un tecnicismo. Los diez que
sí entraron fallan porque su ficha **exige otro organismo** —*S. aureus*,
*E. coli*, micobacterias— y ese motivo es ORG. Estas seis **no nombran bacteria
alguna**. Llamarlas ORG sería escribir en el anexo que el organismo es
«distinto de *P. aeruginosa*» cuando lo que consta es que no consta: afirmaría
más de lo comprobado, que es exactamente el error que ya costó cuatro
exclusiones por idioma el 1 de septiembre.

`exclusion_codes.py` lo dice en su cabecera: ningún código se inventa sobre la
marcha, y uno nuevo es una enmienda al protocolo que se declara con su fecha y
su motivo. Así entraron IDI, PRO, INT y NOREC. Por eso `ingest_organismo.py`
se niega a aplicar una fila firmada NO CUMPLE sin código, las escribe en
`quality_reports/organismo_pendiente.json`, y el LEEME del sobre lee ese
fichero y bloquea el envío mientras no esté vacío.

**EST-087** quedó sin decidir.

**El duplicado** está confirmado pero no aplicado: falta decir cuál de las dos
fichas CTIS es la principal. Es una fusión de informes, no una exclusión, y en
el PRISMA se cuenta distinto. El mecanismo está identificado —la cadena de
claves de `group_reports_into_studies.py`, que ya conserva la numeración
estable— pero tocarla es tocar lo que mantiene los EST-NNN fijos en los
cuadernos firmados de las dos personas, y eso no se hace de paso.

## Lo que se propone para cerrarlo

Un código más, **NOORG**: «la ficha de registro no declara ningún organismo; el
criterio de *P. aeruginosa* no se puede verificar ni a favor ni en contra».

Es hermano de NOREC y conviene verlo así: los demás códigos excluyen por lo que
el estudio **dice**; NOREC excluye por lo que esta revisión **no pudo leer**, y
NOORG por lo que el registro **no declara**. Los tres últimos son propiedades
del proceso, no del estudio, y el manuscrito está obligado a decirlo, igual que
hace con NOREC en §2.9.

`FIRMAR_codigo_NOORG_y_duplicado.xlsx` lleva las siete filas con su frase
literal, la enmienda del código para aceptarla o rechazarla, la pregunta del
duplicado y una hoja de firma. El comentario por estudio es obligatorio: es el
texto que PRISMA 16b exige y el que se imprime en S16.

## La objeción que hay que dejar por escrito

Estos siete estudios son la prueba de lo que el artículo sostiene. El título
promete medir si este cuerpo de evidencia admite verificación y réplica, y
«hay fichas de registro cuya bacteria no consta en ninguna parte» es un
resultado, no un estorbo. Excluirlos es defendible —no cumplen un criterio que
no se puede comprobar— y dejarlos también, declarándolos. Lo que no es
defendible es que desaparezcan sin que el lector se entere. Sea cual sea la
firma, la cifra se reporta.

## De paso, dos defectos que salieron al mover esto

1. **El reparto de exclusiones era binario y se volvió falso.** El manuscrito
   decía «X al leer el artículo y Y sin poder leerlo». Meter en «sin poder
   leerlo» diez estudios cuya ficha completa se bajó y se leyó habría dicho al
   lector lo contrario de lo que pasó. Hay un tercer grupo y ahora se declara:
   **22 por el artículo, 10 por la ficha del registro, 7 sin poder leer
   ninguno de los dos**. Los escalares `excluidos_sobre_la_ficha_de_registro` y
   `excluidos_sin_poder_leer_nada` lo sostienen.

2. **`sync_manuscript_numbers.py` se comía la puntuación.** Su comodín era una
   clase de caracteres que incluía el punto y el espacio, así que en una
   plantilla que empieza por un hueco absorbía el final de la frase anterior.
   De ahí venía «without being able to read it155 studies remain», que viajó en
   el resumen en inglés. Ahora el comodín describe un número y nada más.

3. **El resumen se pasaba del tope de la revista.** `build_structured_abstract.py`
   no está en el orden documentado de CLAUDE.md, así que nadie lo corría: el
   párrafo corrido en español llegó a 262 palabras con el tope en 250. Se
   recortó la metodología sin tocar ninguna cifra ni ninguna afirmación —250 en
   español, 245 en inglés— y el script pasa a estar en la lista de comandos.
