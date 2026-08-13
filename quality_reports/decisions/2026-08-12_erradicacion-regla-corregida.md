# Erradicación microbiológica: la regla, corregida contra los artículos

**Fecha:** 2026-08-12
**Deciden:** Danny Valdiviezo y Nataly Trelles
**Estado:** PROPUESTA — pendiente de que ambos revisores la confirmen
**Sustituye a:** `2026-08-11_definicion-erradicacion-y-exito.md`, que queda como
antecedente. Las reglas 2 (definición de éxito clínico) y 3 (blanco ≠ NA ≠ 0) de
aquel documento siguen vigentes tal cual y no se repiten aquí.

---

## Por qué hubo que corregirla

La regla del 11 de agosto se escribió mirando la tabla de discrepancias. Al
aplicarla después contra los cuatro artículos que sí tenemos, se rompió en
cuatro sitios distintos. No estaba mal orientada: estaba incompleta, y cada
hueco es un sitio por donde dos revisores honestos vuelven a divergir.

De las cuatro filas de erradicación que se pueden revisar contra el texto, la
regla anterior determinaba sola **una**. Las otras tres admitían las dos
respuestas.

---

## Hueco 1 — No decía qué organismo cuenta

La regla pedía «cultivo de control negativo para *P. aeruginosa*». Pero esta
revisión trata de *P. aeruginosa* **resistente**, y la diferencia decide casos.

**EST-014** (empiema por *P. aeruginosa* resistente a carbapenémicos). El
artículo reporta crecimiento en líquido pleural los días 0, 1, 4 y 5 tras la
fagoterapia. Desde el día 7 hasta el alta, lo que crece es una cepa **sensible a
carbapenémicos**, que los autores tratan como colonizador, y ya no se aísla la
resistente.

Por la letra de la regla, no hubo erradicación: sigue creciendo *P. aeruginosa*.
Por la pregunta de la revisión, sí la hubo: el organismo que motivó el
tratamiento desapareció. Nataly anotó 1 y Danny lo dejó en blanco, y ninguno de
los dos estaba contraviniendo la regla.

**Corrección.** El organismo diana es el aislado resistente que motivó el
tratamiento, no la especie. La persistencia de una cepa sensible no anula la
erradicación del diana, y se anota en observaciones.

## Hueco 2 — El primer cultivo puede mentir

La regla mandaba tomar el primer cultivo de control posterior al tratamiento.
Aplicada tal cual, cuenta como erradicado a un paciente que recayó dos veces.

**EST-016** (osteomielitis femoral, Riga). Tras los fagos, dos punciones del
fémur salen negativas. En el recambio de cadera de septiembre de 2019 la parte
distal del fémur crece *P. aeruginosa* MDR. Dieciséis días más tarde se hace un
DAIR y los frotis periprotésicos vuelven a ser positivos. Recién el 4 de octubre
las punciones salen negativas.

Con «el primer cultivo de control», EST-016 es un 1 sin matices.

**Corrección.** Se añade la columna `microbio_eradication_sustained`, con
ventana de 30 días desde el primer cultivo negativo: `sostenida` si no vuelve a
crecer el diana, `recaida` si vuelve, `no evaluable` si no hubo erradicación o
no hay cultivos de seguimiento. La recaída no borra la erradicación inicial: son
dos datos y los dos hacen falta.

## Hueco 3 — No decía si manda el autor o el lector

**EST-006** (paciente quemado, *P. aeruginosa* XDR). Los autores cierran la
Discusión diciendo que la sinergia fago-antibiótico no consiguió éxito
microbiológico, aunque el desenlace clínico fue favorable.

Danny anotó 1 y Nataly 0. Aquí el artículo zanja, y la regla anterior no decía
qué hacer cuando la declaración del autor y la deducción del lector no coinciden.

**Corrección.** Si el artículo declara explícitamente el resultado
microbiológico, esa declaración manda. Solo se deduce de los cultivos cuando el
artículo calla.

## Hueco 4 — Hay estudios sin fin de tratamiento

**EST-012** es supresión crónica de *P. aeruginosa* MDR en infección protésica.
El tratamiento no termina; esa es la intención terapéutica. «El primer cultivo
posterior al fin del tratamiento» no tiene referente.

**Corrección.** En terapia supresiva indefinida se toma el cultivo del cierre
del seguimiento y se hace constar que no hubo fin de tratamiento.

## Hueco 5 — Faltaba el denominador

El formulario tenía `microbio_eradication_n` y ningún sitio donde anotar a
cuántos pacientes se les hizo cultivo de control.

En reportes de caso da igual, porque el denominador es 1. Deja de dar igual en
EST-003, que es una serie con cuatro brazos, y en los 16 ensayos aleatorizados
del corpus: si de 10 pacientes solo 6 tuvieron cultivo de control y 4
negativizaron, el dato es 4/6 y no 4/10.

Esto no es un refinamiento opcional. **Agregar proporciones sin comprobar el
denominador es precisamente lo que el manuscrito le reprocha a las síntesis
publicadas.** Recogerlo mal en el propio formulario y criticarlo en la Discusión
no se sostiene.

**Corrección.** Se añade la columna `microbio_eradication_denom`.

---

## La excepción de vía aérea, ahora cerrada

La regla anterior sacaba de erradicación la colonización crónica de vía aérea y
nombraba fibrosis quística y bronquiectasias. No decía nada de neumonía asociada
a ventilador, trasplante pulmonar ni EPOC. Con 107 estudios por extraer, esa
lista abierta es una divergencia esperando a ocurrir.

La lista queda **cerrada** en cinco cuadros: fibrosis quística, bronquiectasias,
EPOC, colonización postrasplante pulmonar, y traqueostomía o ventilación
prolongada. Cualquier otro cuadro respiratorio se rige por la regla general.

El fundamento no cambia: en la ronda previa del proyecto se comprobó que separar
la colonización crónica de vía aérea del resto de sitios hacía desaparecer por
completo la dispersión entre estudios (τ² → 0). No son un mismo desenlace con
ruido, sino dos desenlaces distintos.

---

## Qué pasa con las cuatro filas que se pueden revisar

| Estudio | Danny | Nataly | Con la regla corregida |
|---|---:|---:|---|
| EST-006 | 1 | 0 | **0** — el autor declara que no hubo éxito microbiológico (hueco 3) |
| EST-008 | 9 | 0 | **NA** — colonización crónica de vía aérea, fibrosis quística |
| EST-014 | en blanco | 1 | **1** sobre el organismo diana, anotando la cepa sensible persistente (hueco 1) |
| EST-016 | en blanco | 1 | **1** inicial y `recaida` en la columna nueva (hueco 2) |

Las cuatro quedan determinadas por la regla, sin depender de quién las lea. Con
la versión anterior, solo EST-008 lo estaba.

## Las otras ocho filas siguen sin poder resolverse

EST-003 (cuatro brazos), EST-005, EST-007, EST-013 y EST-015 no tienen texto
completo. Ninguna regla las arregla: se extrajeron desde el resumen, y un
resumen no dice si hubo cultivo de control.

Conviene decirlo sin rodeos porque cambia la prioridad. Tres de los cinco casos
que motivaron la regla del 11 de agosto —EST-005, EST-007 y EST-013— son de
estos. Allí los revisores no discrepaban sobre qué es erradicar. Discrepaban
porque no tenían el artículo.

EST-015, EST-007 y EST-013 son de acceso abierto y fallaron por HTTP 403 al
descargarlos con robot, no por estar cerrados: se recuperan abriéndolos en el
navegador. EST-003 y EST-005 sí necesitan préstamo interbibliotecario.

## Constancia

Las tres columnas viven ya en `scripts/extraction_schema.py`, con esta regla
completa en el texto de ayuda que sale al pasar el cursor por el encabezado. El
formulario ofrece `sostenida / recaida / no evaluable` como desplegable cerrado,
para que no vuelva a colarse un valor a mano.
