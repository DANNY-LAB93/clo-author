# La concordancia que el manuscrito negaba

**Estado:** APLICADO el 23 de septiembre de 2026, con la confirmación de los
dos autores sobre cómo se cerraron los desacuerdos.
**Viene de:** un encargo externo de corrección integral en veinte puntos.
**Ficheros:** `scripts/build_concordancia_rob.py` (nuevo),
`quality_reports/concordancia_rob.json` y `.csv`, `scripts/rob_bloques.py`,
`scripts/build_rob_table.py`, `scripts/build_manuscript_tables.py`,
`scripts/build_synthesis_scalars.py`, `scripts/build_auditoria_scalars.py`,
los tres manuscritos.

## Lo que el manuscrito decía, y era falso

«La evaluación se emitió por consenso, de modo que no admite medida de
concordancia entre revisores.» Lo decía en Métodos, en Resultados y en
Limitaciones, en los tres manuscritos.

Los dos cuadernos individuales están en
`revision_sistematica/riesgo_sesgo/` desde el 9 de septiembre, con **82 juicios
cada uno**. No son copias: difieren en 13.

| | Todos los cuadernos | Corpus vigente |
|---|---|---|
| Juicios comparables | 82 | **74** |
| Acuerdo bruto | 69 (84,1 %) | **62 (83,8 %)** |
| Kappa de Cohen | 0,78 | **0,78** |
| Desacuerdos | 13 | **12** |

Diez de los once estudios evaluables tienen doble lectura. EST-004 se evaluó en
un cuaderno aparte el 17 de septiembre y tiene una sola; el manuscrito lo
declara.

## Los trece fueron todos en la misma dirección

El cuaderno de consenso es **idéntico al de D. Valdiviezo en los 82 juicios** y
difiere del de N. Trelles en los 13. Preguntado el 23 de septiembre, los dos
autores confirmaron que los discutieron uno a uno y que N. Trelles aceptó el
juicio de D. Valdiviezo en todos.

Eso es un consenso y así se escribe. Pero el manuscrito dice **también** que
los doce se resolvieron en la misma dirección, porque un lector que solo vea
«resueltos por consenso» no puede calibrar lo que ese consenso vale. El
desglose, juicio a juicio, va en `quality_reports/concordancia_rob.csv`.

## Las otras tres correcciones

**7 ensayos frente a 3 con RoB 2.** La Tabla 2 clasifica por lo que declara el
resumen; RoB 2 se aplica a los que además tienen texto. De los 7, solo 3 lo
tienen; de los otros 4 no se obtuvo el artículo (EST-029, EST-078, EST-157,
EST-188). Estaba sin explicar y se leía como incoherencia.

**«% de los 78 con texto completo».** Son **78 brazos legibles**, no 78 textos
ni 78 estudios —los estudios con texto son 70—. Dos unidades distintas en la
misma tabla. La columna ya dice cuál es.

**23 057 registros y 134 informes de registro.** No eran dos corrientes: los
134 están dentro de los 23 057 (121 ClinicalTrials.gov, 10 CTIS, 3 EudraCT), y
PRISMA solo los separa a partir del cribado. Faltaba decirlo.

## Lo que NO se aplicó del encargo, y por qué

**El papel de Rayyan estaba invertido.** El encargo pedía describirlo como la
herramienta de cribado y precisar su cobertura. Aquí el cribado lo condujo un
solo revisor humano sin duplicación, con las decisiones emitidas por un modelo
de lenguaje; Rayyan se usó solo en el recribado ciego de los 350 excluidos.
Aplicarlo al pie de la letra habría convertido una declaración correcta en una
falsa.

**La restricción de idioma sí fue enmienda** —11 de agosto, con el cribado
concluido—, y el propio encargo resuelve el condicional a favor de conservarla.

## Borrado

`paper/manuscrito_JSR_editado.md`, del 14 de septiembre: ningún guion lo
escribía, ningún guardián lo comprobaba, no viajaba en el paquete ni en el
`.zip`, y llevaba nueve días quedándose atrás. Queda en el historial
(`git show 783bab8:paper/manuscrito_JSR_editado.md`).

## Lo que sigue bloqueado

Tres puntos del encargo necesitan **leer artículos**: verificar la clase de
resistencia contra el antibiograma (70 artículos), reextraer los comparativos
con comparador y tiempo de evaluación (14 artículos y un formulario que no
existe), y los 13 pares de solapamiento sin leer. Dos necesitan **firma**:
sacar del denominador principal los 4 brazos bajo el umbral de MDR, y
reestructurar el manuscrito. El detalle está en
`quality_reports/2026-09-23_respuesta-a-la-correccion-integral.md`.

**226 afirmaciones ancladas**, todas al día. Las 17 cifras se reproducen.
