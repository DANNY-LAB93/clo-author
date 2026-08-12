# Para confirmar antes de seguir extrayendo

Nataly: necesito que revises esto y me digas si estás de acuerdo. Son dos reglas
de extracción. Mientras no las cerremos no conviene tocar los 107 estudios que
faltan, porque cada uno que extraigamos con criterios distintos es una
discrepancia más que después hay que resolver dos veces.

Fecha: 12 de agosto de 2026. Regla completa en
`quality_reports/decisions/2026-08-11_definicion-erradicacion-y-exito.md`.

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
Las dos lecturas son defendibles, y por eso hay que elegir una.

La culpa es del formulario. La ayuda decía solo «en cuántos desapareció la
bacteria en cultivo». No dice cuándo se mide, ni qué hacer cuando el artículo no
hizo cultivo de control, ni si 0 y «no lo reporta» son lo mismo. Un campo así
produce divergencia por diseño.

## Regla 1: erradicación microbiológica

Se cuenta un paciente como erradicado cuando el artículo reporta un cultivo de
control negativo para *P. aeruginosa*, del mismo sitio de infección, obtenido
después de terminar la fagoterapia.

Del momento: se toma el primer cultivo de control posterior al fin del
tratamiento. El día se anota en observaciones («cultivo negativo al día 14»). Si
el artículo da varios momentos, se usa el primero y los demás se anotan.

Hay tres valores posibles y no son intercambiables:

| Valor | Cuándo |
|---|---|
| un número | Se hizo cultivo de control y salió negativo en ese número de pacientes |
| 0 | Se hizo cultivo de control y siguió positivo en todos |
| NA | No se hizo, o el artículo no lo reporta |

Esta es la distinción que nos faltaba. El 0 es un dato: se buscó y no se
erradicó. El NA es un hueco: no lo sabemos. Si los metemos en la misma casilla,
lo que cambia es el denominador de cualquier proporción que calculemos después.

Un caso aparte: colonización crónica de la vía aérea. En fibrosis quística y
bronquiectasias, un solo cultivo negativo no cuenta como erradicación, porque la
carga fluctúa y un cultivo aislado no demuestra que se eliminó. Ahí va NA y se
explica en observaciones, salvo que el propio artículo declare erradicación
sostenida con cultivos seriados.

Esto no es manía mía. En la ronda anterior del proyecto comprobamos que separar
la colonización crónica de vía aérea del resto de sitios hacía desaparecer del
todo la dispersión entre estudios. Eso significa que no son un mismo desenlace
medido con ruido, sino dos desenlaces distintos.

Con esta regla, EST-008 (BX004-A, fagos nebulizados en fibrosis quística) no es
ni 9 ni 0. Es NA, y en observaciones: colonización crónica de vía aérea, el
ensayo reporta reducción de carga bacteriana, no erradicación.

## Regla 2: definición de éxito clínico

Este campo dio 19 conflictos, y cuando los miré ninguno de los dos estaba
equivocado. Los dos pegábamos una frase distinta de la Discusión del mismo
artículo, porque el artículo no da definición operativa y el formulario obligaba
a escribir algo.

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

Para `clinical_success_n` vale lo mismo: si no hay definición, hay que ver si la
cifra se puede sacar igual. Muchas veces sí, cuando el artículo dice «los tres
pacientes se curaron». Si no se puede, NA.

## Regla 3: una casilla en blanco nunca es un cero

En blanco significa «todavía no lo extraje». NA significa «lo busqué y el
artículo no lo dice». 0 significa «el artículo lo dice y es cero».

En la comparación salieron celdas en blanco tuyas frente a valores míos y al
revés, en EST-014, EST-015 y EST-016. Eso no es desacuerdo, es que uno iba por
delante del otro. El comparador ya lo separa, pero conviene que ninguno de los
dos deje en blanco algo que sí miró.

## Lo que hay que revisar juntos, y lo que no se puede

Con la regla aplicada, de erradicación solo podemos revisar cuatro filas, porque
son las únicas cuyo artículo tenemos:

| Estudio | Yo | Tú |
|---|---:|---:|
| EST-006 | 1 | 0 |
| EST-008 | 9 | 0 |
| EST-014 | en blanco | 1 |
| EST-016 | en blanco | 1 |

Las otras ocho (EST-003 con cuatro brazos, EST-005, EST-007, EST-013 y EST-015)
no tienen texto completo. Y aquí está lo incómodo: tres de los cinco casos que
motivaron toda esta regla, EST-005, EST-007 y EST-013, son estudios de los que
solo tenemos el resumen.

O sea que en esos tres ninguno de los dos podía saber la respuesta. No
discrepamos por la definición de erradicación. Discrepamos porque estábamos
extrayendo de un resumen que no dice si hubo cultivo de control. Eso no lo
arregla ninguna regla: lo arregla conseguir el artículo.

Lo mismo con EST-003, que él solo aporta 31 de las 169 diferencias, y con
EST-015, que aporta 21. Entre los dos son el 31 % de todo el desacuerdo, y de
ninguno tenemos el PDF.

Por eso te pido dos cosas en este orden. Primero confirma las reglas, que sirven
para los 107 que faltan. Segundo, prioricemos pedir EST-003 y EST-015 por
biblioteca, porque resolverlos vale más que cualquier reunión de consenso que
hagamos.

## Confirmación

Marca lo que corresponda y me lo devuelves:

- [ ] De acuerdo con la regla 1 (erradicación)
- [ ] De acuerdo con la regla 2 (definición de éxito clínico)
- [ ] De acuerdo con la regla 3 (blanco, NA y 0 son distintos)
- [ ] No estoy de acuerdo en: ______________________________

Nombre y fecha: ______________________________

Cuando las confirmes las meto en el texto de ayuda del propio formulario, para
que salgan al pasar el cursor por la columna mientras extraes. Una regla en un
documento que nadie vuelve a abrir sirve de poco.
