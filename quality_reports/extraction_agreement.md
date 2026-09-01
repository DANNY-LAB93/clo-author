# Concordancia entre extracciones independientes

Generado el 2026-08-31 por `scripts/compare_extractions.py`.

| | |
|---|---:|
| Danny_Valdiviezo | 132 filas |
| Nataly_Trelles | 130 filas |
| Filas comparadas (brazos en ambos) | 130 |
| Solo en Danny_Valdiviezo | 2 |
| Solo en Nataly_Trelles | 0 |
| Conflictos de valor | 541 |

Acuerdo mediano entre las dos extracciones: **78 %**.

Kappa mediana de los campos donde la kappa es informativa (8 de 9 categóricos): **0.62**. Los demás se excluyen porque su distribución está tan sesgada que la kappa mide el sesgo y no la concordancia.

## Por variable

| variable | tipo | n | acuerdos | % acuerdo | kappa / dispersión |
|---|---|---:|---:|---:|---|
| `pathogen_scope` | categórico | 130 | 130 | 100% | 1.00 (casi perfecta) |
| `resistance_class` | categórico | 130 | 130 | 100% | 1.00 (casi perfecta) |
| `resistance_class_source` | categórico | 130 | 130 | 100% | 1.00 (casi perfecta) |
| `dtr_status` | categórico | 130 | 99 | 76% | 0.52 (moderada) |
| `route` | categórico | 130 | 90 | 69% | 0.62 (sustancial) |
| `modality` | categórico | 130 | 99 | 76% | 0.59 (moderada) |
| `study_design` | categórico | 130 | 85 | 65% | 0.57 (moderada) |
| `extraction_status` | categórico | 130 | 101 | 78% | 0.55 (moderada) |
| `microbio_eradication_sustained` | categórico | 0 | 0 | — | sin filas comparables |
| `n_arm` | numérico | 130 | 100 | 77% | dif. media 3.55 |
| `clinical_success_n` | numérico | 130 | 102 | 78% | dif. media 0.51 |
| `adverse_event_n` | numérico | 130 | 94 | 72% | dif. media 0.22 |
| `microbio_eradication_n` | numérico | 119 | 76 | 64% | dif. media 0.70 |
| `microbio_eradication_denom` | numérico | 0 | 0 | — | dif. media — |
| `mortality_n` | numérico | 119 | 91 | 76% | dif. media 0.38 |
| `los_days` | numérico | 92 | 83 | 90% | dif. media 0.00 |
| `resistance_emergence_n` | numérico | 92 | 79 | 86% | dif. media 0.00 |
| `publication_year` | numérico | 130 | 117 | 90% | dif. media 0.27 |

## Celdas que solo un revisor llegó a rellenar

Son **114** celdas. No entran en el acuerdo ni en la kappa, y no son
conflictos: nadie ha discrepado de nada, simplemente un revisor iba por
delante del otro. Contarlas como desacuerdo convertiría la ventaja de un
revisor en discordancia medida y hundiría la kappa sin que hubiera
discrepancia alguna.

| variable | celdas sin pareja |
|---|---:|
| `los_days` | 38 |
| `resistance_emergence_n` | 38 |
| `journal_tier` | 14 |
| `microbio_eradication_n` | 11 |
| `mortality_n` | 11 |
| `extraction_citation` | 1 |
| `incomplete_reason` | 1 |

## Diferencias de cobertura, no de valor

Filas presentes en una sola extracción. No entran en la kappa: casi siempre
significan que un revisor separó brazos que el otro agrupó, no que discrepen
sobre un dato.

- solo en Danny_Valdiviezo: `EST-207` brazo A
- solo en Danny_Valdiviezo: `EST-208` brazo A

## Qué hacer ahora

1. Abrir `revision_sistematica/extraccion/extraction_conflicts.csv` y resolver fila a fila.
2. Rellenar `resolucion`, `resuelto_por` y `fecha`: el rastro de la resolución
   es lo que permite escribir en Métodos que los desacuerdos se resolvieron por
   consenso, y con qué frecuencia hizo falta.
3. Volcar los valores acordados al dataset de extracción y volver a ejecutar
   este script para dejar constancia de la concordancia previa a la resolución.
