# Concordancia entre extracciones independientes

Generado el 2026-08-23 por `scripts/compare_extractions.py`.

| | |
|---|---:|
| Danny_Valdiviezo | 132 filas |
| Nataly_Trelles | 129 filas |
| Filas comparadas (brazos en ambos) | 128 |
| Solo en Danny_Valdiviezo | 4 |
| Solo en Nataly_Trelles | 1 |
| Conflictos de valor | 724 |

Acuerdo mediano entre las dos extracciones: **69 %**.

Kappa mediana de los campos donde la kappa es informativa (7 de 9 categóricos): **0.30**. Los demás se excluyen porque su distribución está tan sesgada que la kappa mide el sesgo y no la concordancia.

## Por variable

| variable | tipo | n | acuerdos | % acuerdo | kappa / dispersión |
|---|---|---:|---:|---:|---|
| `pathogen_scope` | categórico | 84 | 41 | 49% | 0.27 (aceptable) |
| `resistance_class` | categórico | 84 | 56 | 67% | 0.49 (moderada) |
| `resistance_class_source` | categórico | 21 | 20 | 95% | 0.00 (leve) — acuerdo alto con kappa baja: distribucion muy sesgada, la kappa no es informativa aqui |
| `dtr_status` | categórico | 84 | 58 | 69% | 0.31 (aceptable) |
| `route` | categórico | 84 | 32 | 38% | 0.30 (aceptable) |
| `modality` | categórico | 84 | 55 | 65% | 0.21 (leve) |
| `study_design` | categórico | 84 | 51 | 61% | 0.43 (moderada) |
| `extraction_status` | categórico | 97 | 70 | 72% | 0.04 (leve) |
| `microbio_eradication_sustained` | categórico | 0 | 0 | — | sin filas comparables |
| `n_arm` | numérico | 97 | 65 | 67% | dif. media 7.94 |
| `clinical_success_n` | numérico | 84 | 57 | 68% | dif. media 0.45 |
| `adverse_event_n` | numérico | 84 | 60 | 71% | dif. media 0.24 |
| `microbio_eradication_n` | numérico | 84 | 39 | 46% | dif. media 0.82 |
| `microbio_eradication_denom` | numérico | 0 | 0 | — | dif. media — |
| `mortality_n` | numérico | 84 | 59 | 70% | dif. media 0.38 |
| `los_days` | numérico | 20 | 19 | 95% | dif. media — |
| `resistance_emergence_n` | numérico | 21 | 16 | 76% | dif. media — |
| `publication_year` | numérico | 84 | 80 | 95% | dif. media 0.17 |

## Celdas que solo un revisor llegó a rellenar

Son **1064** celdas. No entran en el acuerdo ni en la kappa, y no son
conflictos: nadie ha discrepado de nada, simplemente un revisor iba por
delante del otro. Contarlas como desacuerdo convertiría la ventaja de un
revisor en discordancia medida y hundiría la kappa sin que hubiera
discrepancia alguna.

| variable | celdas sin pareja |
|---|---:|
| `los_days` | 108 |
| `resistance_class_source` | 107 |
| `resistance_emergence_n` | 107 |
| `pathogen_scope` | 44 |
| `resistance_class` | 44 |
| `dtr_status` | 44 |
| `route` | 44 |
| `modality` | 44 |
| `study_design` | 44 |
| `clinical_success_n` | 44 |
| `adverse_event_n` | 44 |
| `microbio_eradication_n` | 44 |
| `mortality_n` | 44 |
| `publication_year` | 44 |
| `clinical_success_definition` | 44 |
| `geographic_source` | 43 |
| `extraction_citation` | 43 |
| `journal_tier` | 36 |
| `extraction_status` | 31 |
| `n_arm` | 31 |
| `incomplete_reason` | 30 |

## Diferencias de cobertura, no de valor

Filas presentes en una sola extracción. No entran en la kappa: casi siempre
significan que un revisor separó brazos que el otro agrupó, no que discrepen
sobre un dato.

- solo en Danny_Valdiviezo: `EST-009` brazo A
- solo en Danny_Valdiviezo: `EST-108` brazo B
- solo en Danny_Valdiviezo: `EST-108` brazo C
- solo en Danny_Valdiviezo: `EST-108` brazo D
- solo en Nataly_Trelles: `EST-009` brazo NA

## Qué hacer ahora

1. Abrir `revision_sistematica/extraccion/extraction_conflicts.csv` y resolver fila a fila.
2. Rellenar `resolucion`, `resuelto_por` y `fecha`: el rastro de la resolución
   es lo que permite escribir en Métodos que los desacuerdos se resolvieron por
   consenso, y con qué frecuencia hizo falta.
3. Volcar los valores acordados al dataset de extracción y volver a ejecutar
   este script para dejar constancia de la concordancia previa a la resolución.
