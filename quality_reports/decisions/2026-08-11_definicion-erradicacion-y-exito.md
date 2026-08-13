# Reglas de extracción: erradicación microbiológica y éxito clínico

**Fecha:** 2026-08-11
**Deciden:** Danny Valdiviezo y Nataly Trelles
**Estado:** SUPERSEDIDO EN SU REGLA 1 por
`2026-08-12_erradicacion-regla-corregida.md`

> **Aviso del 2026-08-12.** La regla 1 de este documento se escribió mirando la
> tabla de discrepancias, y al aplicarla contra los artículos se rompió en cuatro
> sitios: no decía qué organismo cuenta, tomaba el primer cultivo sin mirar si el
> paciente recaía, no fijaba si manda la declaración del autor o la deducción del
> lector, y no contemplaba la terapia supresiva indefinida. Faltaba además el
> denominador. **Use la versión corregida.**
>
> Las reglas 2 (definición de éxito clínico) y 3 (blanco ≠ NA ≠ 0) de este
> documento siguen vigentes tal cual. El documento se conserva entero porque el
> registro de decisiones es solo-anexar: la corrección forma parte del rastro.

---

## Por qué hace falta

La comparación de las dos extracciones independientes dio **37 % de acuerdo en
erradicación microbiológica**, el peor de todos los campos. Al mirar los casos
uno a uno, el desacuerdo no es aleatorio: es sistemático y tiene una causa
identificable.

| Estudio | Danny | Nataly |
|---|---:|---:|
| EST-005 | 1 | 0 |
| EST-006 | 1 | 0 |
| EST-007 | 1 | 0 |
| EST-008 | 9 | 0 |
| EST-013 | 0 | 1 |

Nataly anota **0** donde Danny anota un número positivo. Eso no es un error de
lectura de ninguno de los dos: es que están respondiendo a dos preguntas
distintas con el mismo campo. Danny cuenta a los pacientes en los que el cultivo
se negativizó; Nataly anota 0 cuando el artículo no declara explícitamente
«erradicación». Ambas lecturas son razonables, y por eso hay que elegir una.

La ayuda del formulario decía solo *«En cuántos desapareció la bacteria en
cultivo»*. No dice **cuándo** se mide, ni qué hacer cuando el artículo no hace
cultivo de control, ni si `0` y «no lo reporta» son la misma cosa. Un campo así
produce divergencia por diseño.

---

## Regla 1 — Erradicación microbiológica

**Definición.** Se cuenta un paciente como erradicado cuando el artículo
reporta un **cultivo de control negativo para *P. aeruginosa*, del mismo sitio
de infección**, obtenido **después de terminar la fagoterapia**.

**Momento.** Se toma el **primer cultivo de control posterior al fin del
tratamiento** que el artículo reporte. El día en que se tomó se anota en la
columna de observaciones (por ejemplo, «cultivo negativo al día 14»). Si el
artículo da varios momentos, se usa el primero y se anotan los demás.

**Los tres valores posibles, y no son intercambiables:**

| Valor | Cuándo se usa |
|---|---|
| **un número** | Se hizo cultivo de control y fue negativo en ese número de pacientes |
| **0** | Se hizo cultivo de control y **siguió positivo** en todos |
| **NA** | **No se hizo o no se reporta** cultivo de control |

Esta es la distinción que faltaba. `0` es un dato: significa que se buscó y no
se erradicó. `NA` es un hueco: significa que no lo sabemos. Meterlos en la misma
casilla convierte un denominador en otro y altera cualquier proporción que se
calcule después.

**Colonización crónica de la vía aérea.** En fibrosis quística y
bronquiectasias, un solo cultivo negativo **no** cuenta como erradicación: en
colonización crónica la carga fluctúa y un cultivo aislado no demuestra
eliminación. En esos estudios se anota `NA` y se explica en observaciones, salvo
que el propio artículo declare erradicación sostenida con cultivos seriados.

Esto no es una preferencia de estilo. En la ronda previa de este proyecto se
comprobó que separar la colonización crónica de vía aérea del resto de sitios
**hacía desaparecer por completo la dispersión entre estudios** (τ² → 0), lo que
indica que no son un mismo desenlace medido con ruido, sino dos desenlaces
distintos. Mezclarlos es un error de categoría, no de precisión.

**Ejemplo que resuelve el caso real.** EST-008 (BX004-A, fagos nebulizados en
fibrosis quística): Danny anotó 9, Nataly 0. Con esta regla se anota **NA**, y en
observaciones: «colonización crónica de vía aérea; el ensayo reporta reducción de
carga bacteriana, no erradicación».

---

## Regla 2 — Éxito clínico y su definición

El campo «¿Cómo define el AUTOR el éxito clínico?» produjo 19 conflictos, y al
mirarlos se ve que **ninguno de los dos estaba equivocado**: los dos pegaban una
frase distinta de la Discusión del mismo artículo, porque el artículo no da una
definición operativa y el formulario obligaba a escribir algo.

**Regla.** Si el artículo **no define** qué considera éxito clínico, se escribe
literalmente:

> `SIN DEFINICIÓN OPERATIVA`

y nada más. No se pega una frase de la Discusión ni de las Conclusiones.

Si el artículo **sí la da**, se copia la frase que fija el criterio —la que dice
qué había que observar para considerar el caso un éxito— y no la que resume el
resultado. Se reconocen porque la primera es una condición («resolución de los
signos inflamatorios a las 12 semanas») y la segunda es un desenlace («el
paciente evolucionó favorablemente»).

**Por qué esto importa y no es papeleo.** Que la mayoría de los estudios no
defina el éxito clínico **es uno de los hallazgos del manuscrito**. Si cada
revisor rellena el hueco con una frase de la Discusión, el hueco desaparece del
registro y con él la prueba de que existía.

Lo mismo aplica a `clinical_success_n`: si no hay definición, hay que valorar si
la cifra puede extraerse igualmente (a menudo sí, cuando el artículo dice «los
tres pacientes se curaron»). Si no se puede, `NA`.

---

## Regla 3 — Vacío nunca significa cero

Una celda **en blanco** significa «todavía no lo he extraído». Un `NA` significa
«lo busqué y el artículo no lo dice». Un `0` significa «el artículo lo dice y es
cero».

En la comparación aparecieron celdas en blanco de un revisor frente a valores del
otro (EST-014, EST-015, EST-016). Eso no es desacuerdo: es que uno iba por
delante. El comparador ya lo separa y no lo cuenta como conflicto, pero conviene
que ninguno de los dos deje en blanco algo que sí ha mirado.

---

## Qué hacer con lo ya extraído

Los 12 conflictos de erradicación y los 19 de definición de éxito **se revisan a
la luz de esta regla**, no se descartan. Son 17 estudios: media hora entre los
dos. Conviene hacerlo antes de seguir, porque cada estudio nuevo extraído con
criterios distintos añade una discrepancia más que luego hay que resolver dos
veces.

## Constancia

Estas reglas se incorporan al texto de ayuda del propio formulario
(`scripts/extraction_schema.py`), de modo que aparecen al pasar el cursor por la
columna mientras se extrae. Una regla escrita en un documento que nadie vuelve a
abrir vale menos que la misma regla en el sitio donde se toma la decisión.
