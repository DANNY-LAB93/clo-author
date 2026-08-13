# Para confirmar antes de seguir extrayendo

Nataly: necesito que revises esto y me digas si estás de acuerdo. Son tres
reglas de extracción y dos columnas nuevas. Mientras no las cerremos no conviene
tocar los 107 estudios que faltan, porque cada uno que extraigamos con criterios
distintos es una discrepancia más que después hay que resolver dos veces.

Fecha: 12 de agosto de 2026. Regla completa y el porqué de cada punto en
`quality_reports/decisions/2026-08-12_erradicacion-regla-corregida.md`.

## Qué pasó

Comparé tu cuaderno con el mío. De 162 filas que teníamos los dos, salieron 169
diferencias. El campo peor parado fue erradicación microbiológica: coincidimos
en el 37 %.

Miré caso por caso y el desacuerdo no es aleatorio. Donde yo pongo un número
positivo, tú pones 0.

| Estudio | Yo | Tú |
|---|---:|---:|
| EST-005 | 1 | 0 |
| EST-006 | 1 | 0 |
| EST-007 | 1 | 0 |
| EST-008 | 9 | 0 |
| EST-013 | 0 | 1 |

No es que uno de los dos esté leyendo mal. Estamos contestando dos preguntas
distintas en la misma casilla. Yo cuento pacientes a los que se les negativizó
el cultivo. Tú pones 0 cuando el artículo no dice la palabra «erradicación».

La culpa es del formulario. La ayuda decía solo «en cuántos desapareció la
bacteria en cultivo». No dice cuándo se mide, ni qué hacer cuando el artículo no
hizo cultivo de control, ni si 0 y «no lo reporta» son lo mismo.

Escribí una primera versión de la regla el lunes, y después la probé contra los
cuatro artículos que sí tenemos. Se rompió en cuatro sitios. Lo que va abajo es
la versión que aguanta esa prueba: de las cuatro filas que podemos revisar, la
primera versión solo determinaba una sola.

## Regla 1: erradicación microbiológica

Se cuenta un paciente como erradicado cuando el artículo reporta un cultivo de
control negativo para el organismo diana, del mismo sitio de infección, obtenido
después de terminar la fagoterapia. Con cuatro precisiones que hacen falta.

**Qué organismo.** El diana es el aislado resistente que motivó el tratamiento,
no la especie. Si desaparece la cepa resistente pero sigue creciendo una
sensible, cuenta como erradicación y la persistencia se anota en observaciones.

Es lo que pasa en EST-014, el empiema. El artículo reporta *P. aeruginosa* en
líquido pleural los días 0, 1, 4 y 5 tras los fagos. Del día 7 al alta lo que
crece es una cepa sensible a carbapenémicos, que los autores tratan como
colonizador, y la resistente ya no aparece. Tú pusiste 1 y yo lo dejé en blanco.
Con esta precisión, tu 1 es lo correcto.

**Cuándo se mide.** El primer cultivo posterior al fin del tratamiento, y el día
se anota en observaciones. Si el tratamiento es supresivo indefinido y no
termina, como en EST-012, se usa el cultivo del cierre del seguimiento y se hace
constar.

**Quién manda.** Si el artículo declara el resultado microbiológico, esa
declaración gana sobre lo que nosotros deduzcamos de los cultivos. Solo
deducimos cuando el artículo calla.

Esto resuelve EST-006, el paciente quemado. Los autores cierran la Discusión
diciendo que la combinación fago-antibiótico no consiguió éxito microbiológico,
aunque clínicamente le fue bien. Yo puse 1 y tú 0. El artículo te da la razón.

**Los tres valores no son intercambiables.**

| Valor | Cuándo |
|---|---|
| un número | Se hizo cultivo de control y salió negativo en ese número de pacientes |
| 0 | Se hizo cultivo de control y siguió positivo en todos |
| NA | No se hizo, o el artículo no lo reporta |

El 0 es un dato: se buscó y no se erradicó. El NA es un hueco: no lo sabemos. Si
los metemos en la misma casilla, lo que cambia es el denominador de cualquier
proporción que calculemos después.

**Colonización crónica de vía aérea.** Ahí un solo cultivo negativo no cuenta
como erradicación, porque la carga fluctúa y un cultivo aislado no demuestra que
se eliminó. Va NA y se explica, salvo que el artículo declare erradicación
sostenida con cultivos seriados.

La lista es cerrada y son estos cinco cuadros: fibrosis quística,
bronquiectasias, EPOC, colonización postrasplante pulmonar, y traqueostomía o
ventilación prolongada. Cualquier otro cuadro respiratorio va por la regla
general. La cierro a propósito: la primera versión nombraba solo dos y no decía
qué hacer con las demás, y con 107 estudios por delante eso es divergencia
garantizada.

Esto no es manía mía. En la ronda anterior comprobamos que separar la
colonización crónica de vía aérea del resto de sitios hacía desaparecer del todo
la dispersión entre estudios. Son dos desenlaces distintos, no uno con ruido.

Con esta regla, EST-008 (BX004-A, fagos nebulizados en fibrosis quística) no es
ni 9 ni 0. Es NA, y en observaciones: colonización crónica de vía aérea, el
ensayo reporta reducción de carga bacteriana, no erradicación.

## Dos columnas nuevas

**A cuántos se les hizo cultivo de control.** El formulario tenía el número de
erradicados y ningún sitio para el denominador. Si un brazo tiene 10 pacientes
pero solo a 6 se les hizo cultivo y 4 negativizaron, el dato es 4/6, no 4/10.

En casos clínicos de un paciente esto se contesta solo. Importa en EST-003, que
es una serie con cuatro brazos, y en los 16 ensayos aleatorizados del corpus. Y
tiene filo, porque agregar proporciones sin comprobar el denominador es
exactamente lo que nuestro manuscrito les critica a las revisiones publicadas.
No podemos reprochárselo en la Discusión y recogerlo mal en nuestro formulario.

**Si la erradicación se sostuvo.** Desplegable con tres opciones: sostenida,
recaída, no evaluable. Se mira si vuelve a crecer el organismo diana en los 30
días siguientes al primer cultivo negativo.

Esta la añadí por EST-016, la osteomielitis de fémur. Tras los fagos, dos
punciones salen negativas. Luego, en el recambio de cadera, la parte distal del
fémur crece *P. aeruginosa* MDR. Dieciséis días después se hace un DAIR y los
frotis vuelven a salir positivos. Recién el 4 de octubre negativizan. Con la
regla anterior ese paciente contaba como erradicado y punto.

Una recaída no borra la erradicación inicial. La casilla del número se queda con
su cifra; la recaída va en la columna nueva. Son dos datos y los dos hacen falta.

## Regla 2: definición de éxito clínico

Sin cambios respecto a lo que te mandé el lunes. Este campo dio 19 conflictos y
ninguno de los dos estaba equivocado: los dos pegábamos una frase distinta de la
Discusión del mismo artículo, porque el artículo no da definición operativa y el
formulario obligaba a escribir algo.

Si el artículo no define qué considera éxito clínico, se escribe literalmente
`SIN DEFINICIÓN OPERATIVA` y nada más. No se pega una frase de la Discusión ni
de las Conclusiones.

Si sí la da, se copia la frase que fija el criterio, la que dice qué había que
observar para considerar el caso un éxito. No la que resume el resultado. Se
distinguen porque la primera es una condición («resolución de los signos
inflamatorios a las 12 semanas») y la segunda es un desenlace («el paciente
evolucionó favorablemente»).

Que la mayoría de los estudios no defina el éxito clínico es uno de los
hallazgos del manuscrito. Si cada uno rellena el hueco con una frase de la
Discusión, el hueco desaparece del registro y con él la prueba de que existía.

Para el número de éxitos vale lo mismo: si no hay definición, hay que ver si la
cifra se puede sacar igual. Muchas veces sí, cuando el artículo dice «los tres
pacientes se curaron». Si no se puede, NA.

## Regla 3: una casilla en blanco nunca es un cero

En blanco significa «todavía no lo extraje». NA significa «lo busqué y el
artículo no lo dice». 0 significa «el artículo lo dice y es cero».

En la comparación salieron celdas en blanco tuyas frente a valores míos y al
revés, en EST-014, EST-015 y EST-016. Eso no es desacuerdo, es que uno iba por
delante del otro. Conviene que ninguno de los dos deje en blanco algo que sí
miró.

Aparte, al revisar EST-016 vi que mis dieciséis casillas están vacías. Esa fila
es tuya sola, así que no deberíamos cerrarla como consenso hasta que yo la
extraiga en paralelo. La completo yo.

## Cómo quedan las cuatro filas que podemos revisar

| Estudio | Yo | Tú | Con la regla |
|---|---:|---:|---|
| EST-006 | 1 | 0 | **0** — el autor declara que no hubo éxito microbiológico |
| EST-008 | 9 | 0 | **NA** — colonización crónica de vía aérea |
| EST-014 | en blanco | 1 | **1** sobre el organismo diana, anotando la cepa sensible |
| EST-016 | en blanco | 1 | **1** inicial, y `recaída` en la columna nueva |

Las cuatro quedan determinadas sin depender de quién las lea. Con la versión del
lunes solo lo estaba EST-008.

## Lo que no se puede resolver, y por qué importa

Las otras ocho filas de erradicación no tienen texto completo: EST-003 con
cuatro brazos, EST-005, EST-007, EST-013 y EST-015.

Aquí está lo incómodo. Tres de los cinco casos que motivaron toda esta regla,
EST-005, EST-007 y EST-013, son estudios de los que solo tenemos el resumen. En
esos tres ninguno de los dos podía saber la respuesta. No discrepábamos por la
definición de erradicación: discrepábamos porque el resumen no dice si hubo
cultivo de control.

Y pesa más de lo que parece. EST-003 aporta él solo 31 de las 169 diferencias, y
EST-015 otras 21. Entre los dos, el 31 % de todo el desacuerdo, y de ninguno
tenemos el PDF.

La buena noticia es que tres de ellos son de acceso abierto y fallaron por un
error 403 al descargarlos automáticamente, no por estar cerrados: EST-015,
EST-007 y EST-013 se bajan abriéndolos a mano en el navegador. Solo EST-003 y
EST-005 necesitan préstamo interbibliotecario.

Así que te pido dos cosas, en este orden. Primero confirma las reglas, que
sirven para los 107 que faltan. Segundo, bajemos esos tres a mano esta semana y
pidamos EST-003 por biblioteca, porque resolver EST-003 y EST-015 vale más que
cualquier reunión de consenso que hagamos.

## Confirmación

Marca lo que corresponda y me lo devuelves:

- [ ] De acuerdo con la regla 1 (erradicación, con las cuatro precisiones)
- [ ] De acuerdo con la lista cerrada de cinco cuadros de colonización crónica
- [ ] De acuerdo con las dos columnas nuevas (denominador y erradicación sostenida)
- [ ] De acuerdo con la regla 2 (definición de éxito clínico)
- [ ] De acuerdo con la regla 3 (blanco, NA y 0 son distintos)
- [ ] No estoy de acuerdo en: ______________________________

Nombre y fecha: ______________________________

Las reglas ya están metidas en el texto de ayuda del formulario, así que salen
al pasar el cursor por el encabezado de cada columna mientras extraes. En cuanto
me confirmes, regenero los dos cuadernos con las columnas nuevas sin perder nada
de lo que ya está lleno.
