# Los tres cuadernos de Nataly, consolidados en uno

**Fecha:** 22 de agosto de 2026
**Fichero resultante:** `extraccion_nataly_trelles.xlsx` (hoja `Extraccion`)
**Cómo se hizo:** `python scripts/consolidate_extractions.py` — reproducible

## Qué eran los tres ficheros

| Fichero recibido | Celdas con dato | Qué resultó ser |
|---|---|---|
| `extraccion_segundo_revisor (1).xlsx` | 1 622 | Pasada A |
| `extraccion_segundo_revisor 2334.xlsx` | 1 622 | **La misma pasada A**, reguardada |
| `extraccion_nataly_trelles.xlsx` | 872 | Pasada B, distinta |

Los dos primeros son el mismo cuaderno. Parecían diferir en 39 celdas, pero las 39
eran de `journal_tier`, que no se teclea: es un `VLOOKUP` contra la hoja `Revistas`
y lleva el número de fila dentro de la fórmula (`VLOOKUP(D44,…)` frente a
`VLOOKUP(D48,…)`). Al insertarse filas, la fórmula se reescribe sola y las dos
copias dejan de coincidir *en el texto* sin que nadie haya extraído nada distinto.

Así que en realidad no eran tres extracciones, sino **dos**.

## Qué hay ahora en el fichero

- **1 923 celdas** únicas, la unión de las dos pasadas.
- **9 celdas no se copiaron**, todas de `journal_tier`. La hoja las recalcula desde
  `Revistas`; copiar el valor por encima habría roto la búsqueda. Están declaradas
  en la salida del script, no descartadas en silencio.
- Una hoja nueva, **`Conflictos`**, con 163 filas.

## La hoja `Conflictos` es lo que queda por hacer

Son las celdas donde las dos pasadas **dicen cosas distintas** sobre el mismo
estudio y el mismo campo. No están resueltas. En la hoja de extracción quedó el
valor de la pasada más reciente, pero eso es un marcador de posición, no una
decisión: elegir en silencio habría fabricado un acuerdo que no existe.

Se concentran en **22 estudios**, y por campo:

| Campo | n | | Campo | n |
|---|---|---|---|---|
| `incomplete_reason` | 21 | | `clinical_success_n` | 8 |
| `clinical_success_definition` | 18 | | `n_arm` | 7 |
| `extraction_citation` | 18 | | `adverse_event_n` | 7 |
| `dtr_status` | 15 | | `pathogen_scope` | 7 |
| `microbio_eradication_n` | 12 | | `extraction_status` | 6 |
| `route` | 12 | | resto | 32 |
| `geographic_source` | 9 | | | |

**Para resolver:** rellenar las dos últimas columnas, `Cuál vale` y
`Quién lo resolvió`. Esa firma es lo que respalda la frase de Métodos que dice que
los desacuerdos se zanjaron por consenso; sin ella, la frase no se sostiene.

## Un patrón que conviene mirar antes de decidir

En varios estudios la pasada A escribe `NA` donde la B escribe `0` o una cifra:

- `EST-008 clinical_success_n` → A: `NA` · B: `9`
- `EST-008 microbio_eradication_n` → A: `NA` · B: `0`
- `EST-012 clinical_success_definition` → A: `SIN DEFINICIÓN OPERATIVA` · B: una frase copiada del artículo

Eso es exactamente lo que cambió la regla corregida de erradicación y éxito
(`quality_reports/decisions/2026-08-12_erradicacion-regla-corregida.md`): que un
dato ausente es `NA` y no `0`, y que una definición que el artículo no da se
marca como tal en vez de parafrasearse.

Si la pasada A es posterior a esa corrección, buena parte de los 163 se resuelve
en bloque a favor de A. **Pero eso lo confirma Nataly, no el script.** El orden por
fecha del fichero no basta: las tres copias se guardaron el mismo día.

Los `dtr_status` (15) hay que mirarlos uno a uno de todos modos — ahí las dos
pasadas discrepan en el sentido de la respuesta (`si` frente a `no`), no en cómo
codificar un vacío.
