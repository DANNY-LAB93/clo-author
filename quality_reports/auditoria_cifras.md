# Auditoría de las diecisiete cifras

Generado por `scripts/audita_cifras.py`. Cada cifra se vuelve a contar
sobre los ficheros de datos; ninguna se lee de `synthesis_scalars.json`.

**17 de 17 cifras se reproducen exactamente.**

## Registros identificados — ✔ consistente

| | |
|---|---|
| Publicada | 23057 |
| Recalculada | 23057 |
| Unidad de análisis | registros (filas de exportación) |
| Denominador | no aplica: es la primera casilla del diagrama |
| Fuente | `screening_corpus_all.csv, columna n_source_records` |
| Cálculo | suma de n_source_records sobre los 17129 informes únicos = 23057 |
| Advertencia | la tabla de fuentes del anexo suma 22967, que son pares informe×fuente: la diferencia de 90 son registros repetidos DENTRO de una misma fuente, casi todos de BVS, que agrega dieciséis colecciones |

## Informes únicos — ✔ consistente

| | |
|---|---|
| Publicada | 17129 |
| Recalculada | 17129 |
| Unidad de análisis | informes |
| Denominador | de los 23057 registros |
| Fuente | `screening_corpus_all.csv, número de filas` |
| Cálculo | 23057 registros − 5928 duplicados = 17129 |

## Informes a texto completo — ✔ consistente

| | |
|---|---|
| Publicada | 233 |
| Recalculada | 233 |
| Unidad de análisis | informes |
| Denominador | de los 17129 informes únicos |
| Fuente | `study_groups.csv, número de filas` |
| Cálculo | 233 filas, una por informe evaluado a texto completo |

## Estudios evaluados para elegibilidad — ✔ consistente

| | |
|---|---|
| Publicada | 183 |
| Recalculada | 183 |
| Unidad de análisis | estudios |
| Denominador | de los 233 informes |
| Fuente | `study_groups.csv, valores distintos de la columna estudio` |
| Cálculo | 233 informes agrupados en 183 estudios |

## Estudios incluidos — ✔ consistente

| | |
|---|---|
| Publicada | 137 |
| Recalculada | 137 |
| Unidad de análisis | estudios |
| Denominador | de los 183 evaluados |
| Fuente | `study_groups.csv menos exclusiones_tras_texto_completo.csv` |
| Cálculo | 183 − 46 excluidos = 137 |

## Informes de los estudios incluidos — ✔ consistente

| | |
|---|---|
| Publicada | 171 |
| Recalculada | 171 |
| Unidad de análisis | informes |
| Denominador | de los 233 informes evaluados |
| Fuente | `study_groups.csv, filas cuyo estudio no está excluido` |
| Cálculo | 233 − 62 informes de estudios excluidos = 171 |

## Estudios con publicación recuperable — ✔ consistente

| | |
|---|---|
| Publicada | 95 |
| Recalculada | 95 |
| Unidad de análisis | estudios |
| Denominador | de los 137 incluidos |
| Fuente | `study_groups.csv, situación «extraible» o «solo-resumen» del informe designado` |
| Cálculo | 95 de 137; los otros 42 son solo ficha de registro |

## Estudios con texto obtenido — ✔ consistente

| | |
|---|---|
| Publicada | 71 |
| Recalculada | 71 |
| Unidad de análisis | estudios |
| Denominador | de los 95 recuperables |
| Fuente | `carpetas textos_completos/pdf y texto_html` |
| Cálculo | 71 de 95 recuperables = 74.7 % |

## Estudios solo con ficha de registro — ✔ consistente

| | |
|---|---|
| Publicada | 42 |
| Recalculada | 42 |
| Unidad de análisis | estudios |
| Denominador | de los 137 incluidos |
| Fuente | `study_groups.csv, estudios cuyos informes son todos ficha de registro` |
| Cálculo | 42 + 95 recuperables = 137 incluidos |

## Filas de brazo comparadas — ✔ consistente

| | |
|---|---|
| Publicada | 130 |
| Recalculada | 130 |
| Unidad de análisis | filas de brazo |
| Denominador | brazos presentes en los dos cuadernos de extracción |
| Fuente | `quality_reports/extraction_agreement.json` |
| Cálculo | cuaderno A 132 filas, cuaderno B 130 filas, en común 130; es un recuento histórico e incluye estudios excluidos después |

## Brazos extraídos — ✔ consistente

| | |
|---|---|
| Publicada | 103 |
| Recalculada | 103 |
| Unidad de análisis | brazos |
| Denominador | de los 137 estudios incluidos |
| Fuente | `extraccion_adjudicada.csv menos los estudios excluidos` |
| Cálculo | 132 filas adjudicadas − 29 de estudios excluidos después = 103 |

## Brazos con texto completo — ✔ consistente

| | |
|---|---|
| Publicada | 79 |
| Recalculada | 79 |
| Unidad de análisis | brazos |
| Denominador | de los 103 brazos extraídos |
| Fuente | `extraccion_adjudicada.csv cruzado con las carpetas de texto` |
| Cálculo | 79 de 103 brazos pertenecen a estudios con texto |

## Estudios con grupo de comparación — ✔ consistente

| | |
|---|---|
| Publicada | 15 |
| Recalculada | 15 |
| Unidad de análisis | estudios |
| Denominador | de los 137 incluidos |
| Fuente | `extraccion_adjudicada.csv, diseño adjudicado; regla firmada el 2026-09-16` |
| Cálculo | estudios con al menos un brazo de diseño RCT/non-randomised trial/prospective cohort/retrospective cohort = 15 |

## Comparativos evaluables — ✔ consistente

| | |
|---|---|
| Publicada | 12 |
| Recalculada | 12 |
| Unidad de análisis | estudios |
| Denominador | de los 15 comparativos |
| Fuente | `los comparativos cuyo estudio tiene texto completo` |
| Cálculo | 15 − 3 sin texto (EST-029, EST-157, EST-165) = 12 |

## Ensayos en la Tabla 2 — ✔ consistente

| | |
|---|---|
| Publicada | 11 |
| Recalculada | 11 |
| Unidad de análisis | estudios |
| Denominador | de los 95 recuperables |
| Fuente | `pre_extraccion_desde_resumen.csv, diseño DECLARADO en el resumen` |
| Cálculo | criterio distinto del anterior: clasifica por el resumen y no cuenta cohortes |

## Brazos con diseño comparativo — ✔ consistente

| | |
|---|---|
| Publicada | 18 |
| Recalculada | 18 |
| Unidad de análisis | brazos |
| Denominador | de los 103 brazos extraídos |
| Fuente | `extraccion_adjudicada.csv, brazos cuyo diseño es comparativo` |
| Cálculo | 18 brazos aportados por los 15 estudios comparativos |

## Celdas de la Tabla 5 — ✔ consistente

| | |
|---|---|
| Publicada | 90 |
| Recalculada | 90 |
| Unidad de análisis | celdas de juicio |
| Denominador | de los 12 estudios evaluables |
| Fuente | `riesgo_sesgo_comparativos_adjudicado.csv` |
| Cálculo | 3 × 5 dominios de RoB 2 = 15; 9 × 7 dominios de ROBINS-I = 63; 15 + 63 = 78 juicios de dominio; más 12 juicios globales, uno por estudio, = 90 celdas |
| Advertencia | el manuscrito las llama «juicios de dominio» y no lo son: 78 son de dominio y 12 son globales |
