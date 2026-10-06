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
| Publicada | 128 |
| Recalculada | 128 |
| Unidad de análisis | estudios |
| Denominador | de los 183 evaluados |
| Fuente | `study_groups.csv menos exclusiones_tras_texto_completo.csv` |
| Cálculo | 183 − 55 excluidos = 128 |

## Informes de los estudios incluidos — ✔ consistente

| | |
|---|---|
| Publicada | 161 |
| Recalculada | 161 |
| Unidad de análisis | informes |
| Denominador | de los 233 informes evaluados |
| Fuente | `study_groups.csv, filas cuyo estudio no está excluido` |
| Cálculo | 233 − 72 informes de estudios excluidos = 161 |

## Estudios con publicación recuperable — ✔ consistente

| | |
|---|---|
| Publicada | 86 |
| Recalculada | 86 |
| Unidad de análisis | estudios |
| Denominador | de los 128 incluidos |
| Fuente | `study_groups.csv, situación «extraible» o «solo-resumen» del informe designado` |
| Cálculo | 86 de 128; los otros 42 son solo ficha de registro |

## Estudios con texto obtenido — ✔ consistente

| | |
|---|---|
| Publicada | 65 |
| Recalculada | 65 |
| Unidad de análisis | estudios |
| Denominador | de los 86 recuperables |
| Fuente | `carpetas textos_completos/pdf y texto_html` |
| Cálculo | 65 de 86 recuperables = 75.6 % |

## Estudios solo con ficha de registro — ✔ consistente

| | |
|---|---|
| Publicada | 42 |
| Recalculada | 42 |
| Unidad de análisis | estudios |
| Denominador | de los 128 incluidos |
| Fuente | `study_groups.csv, estudios cuyos informes son todos ficha de registro` |
| Cálculo | 42 + 86 recuperables = 128 incluidos |

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
| Publicada | 94 |
| Recalculada | 94 |
| Unidad de análisis | brazos |
| Denominador | de los 128 estudios incluidos |
| Fuente | `extraccion_adjudicada.csv menos los estudios excluidos` |
| Cálculo | 132 filas adjudicadas − 38 de estudios excluidos después = 94 |

## Brazos con texto completo — ✔ consistente

| | |
|---|---|
| Publicada | 73 |
| Recalculada | 73 |
| Unidad de análisis | brazos |
| Denominador | de los 94 brazos extraídos |
| Fuente | `extraccion_adjudicada.csv cruzado con las carpetas de texto` |
| Cálculo | 73 de 94 brazos pertenecen a estudios con texto |

## Estudios con diseño comparativo — ✔ consistente

| | |
|---|---|
| Publicada | 12 |
| Recalculada | 12 |
| Unidad de análisis | estudios |
| Denominador | de los 128 incluidos |
| Fuente | `extraccion_adjudicada.csv, diseño adjudicado; regla firmada el 2026-09-16` |
| Cálculo | estudios con al menos un brazo de diseño RCT/non-randomised trial/prospective cohort/retrospective cohort = 12 |

## Comparativos evaluables — ✔ consistente

| | |
|---|---|
| Publicada | 9 |
| Recalculada | 9 |
| Unidad de análisis | estudios |
| Denominador | de los 12 comparativos |
| Fuente | `los comparativos cuyo estudio tiene texto completo` |
| Cálculo | 12 − 3 sin texto (EST-029, EST-157, EST-165) = 9 |

## Ensayos en la Tabla 2 — ✔ consistente

| | |
|---|---|
| Publicada | 7 |
| Recalculada | 7 |
| Unidad de análisis | estudios |
| Denominador | de los 86 recuperables |
| Fuente | `pre_extraccion_desde_resumen.csv, diseño DECLARADO en el resumen` |
| Cálculo | criterio distinto del anterior: clasifica por el resumen y no cuenta cohortes |

## Brazos con diseño comparativo — ✔ consistente

| | |
|---|---|
| Publicada | 15 |
| Recalculada | 15 |
| Unidad de análisis | brazos |
| Denominador | de los 94 brazos extraídos |
| Fuente | `extraccion_adjudicada.csv, brazos cuyo diseño es comparativo` |
| Cálculo | 15 brazos aportados por los 12 estudios comparativos |

## Celdas de la Tabla 5 — ✔ consistente

| | |
|---|---|
| Publicada | 68 |
| Recalculada | 68 |
| Unidad de análisis | celdas de juicio |
| Denominador | de los 9 estudios evaluables |
| Fuente | `riesgo_sesgo_comparativos_adjudicado.csv` |
| Cálculo | 2 × 5 dominios de RoB 2 = 10; 7 × 7 dominios de ROBINS-I = 49; 10 + 49 = 59 juicios de dominio; más 9 juicios globales, uno por estudio, = 68 celdas |
| Advertencia | el manuscrito las llama «juicios de dominio» y no lo son: 59 son de dominio y 9 son globales |
