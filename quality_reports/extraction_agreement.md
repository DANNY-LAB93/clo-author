# Concordancia entre extracciones independientes

Generado el 2026-08-11 por `scripts/compare_extractions.py`.

| | |
|---|---:|
| Danny Valdiviezo | 164 filas |
| Nataly Trelles | 164 filas |
| Filas comparadas (brazos en ambos) | 162 |
| Solo en Danny Valdiviezo | 2 |
| Solo en Nataly Trelles | 2 |
| Conflictos de valor | 169 |

Acuerdo mediano entre las dos extracciones: **70 %**.

Kappa mediana de los campos donde la kappa es informativa (5 de 8 categóricos): **0.38**. Los demás se excluyen porque su distribución está tan sesgada que la kappa mide el sesgo y no la concordancia.

## Por variable

| variable | tipo | n | acuerdos | % acuerdo | kappa / dispersión |
|---|---|---:|---:|---:|---|
| `pathogen_scope` | categórico | 20 | 17 | 85% | 0.00 (leve) — acuerdo alto con kappa baja: distribucion muy sesgada, la kappa no es informativa aqui |
| `resistance_class` | categórico | 19 | 11 | 58% | 0.44 (moderada) |
| `resistance_class_source` | categórico | 19 | 16 | 84% | 0.00 (leve) — acuerdo alto con kappa baja: distribucion muy sesgada, la kappa no es informativa aqui |
| `dtr_status` | categórico | 19 | 13 | 68% | 0.08 (leve) |
| `route` | categórico | 19 | 10 | 53% | 0.38 (aceptable) |
| `modality` | categórico | 19 | 10 | 53% | -0.12 (pobre) |
| `study_design` | categórico | 19 | 16 | 84% | 0.75 (sustancial) |
| `extraction_status` | categórico | 19 | 14 | 74% | 0.00 (leve) |
| `n_arm` | numérico | 19 | 12 | 63% | dif. media 1.00 |
| `clinical_success_n` | numérico | 19 | 10 | 53% | dif. media 0.40 |
| `adverse_event_n` | numérico | 19 | 11 | 58% | dif. media 0.33 |
| `microbio_eradication_n` | numérico | 19 | 7 | 37% | dif. media 1.33 |
| `mortality_n` | numérico | 19 | 14 | 74% | dif. media 0.07 |
| `los_days` | numérico | 19 | 15 | 79% | dif. media — |
| `resistance_emergence_n` | numérico | 20 | 14 | 70% | dif. media — |
| `publication_year` | numérico | 19 | 15 | 79% | dif. media 0.06 |

## Diferencias de cobertura, no de valor

Filas presentes en una sola extracción. No entran en la kappa: casi siempre
significan que un revisor separó brazos que el otro agrupó, no que discrepen
sobre un dato.

- solo en Danny Valdiviezo: `EST-003` brazo B
- solo en Danny Valdiviezo: `EST-009` brazo A
- solo en Nataly Trelles: `EST-003	3` brazo B
- solo en Nataly Trelles: `EST-009` brazo NA

## Qué hacer ahora

1. Abrir `revision_sistematica/extraccion/extraction_conflicts.csv` y resolver fila a fila.
2. Rellenar `resolucion`, `resuelto_por` y `fecha`: el rastro de la resolución
   es lo que permite escribir en Métodos que los desacuerdos se resolvieron por
   consenso, y con qué frecuencia hizo falta.
3. Volcar los valores acordados al dataset de extracción y volver a ejecutar
   este script para dejar constancia de la concordancia previa a la resolución.
