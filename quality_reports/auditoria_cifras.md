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
| Publicada | 65 |
| Recalculada | 65 |
| Unidad de análisis | estudios |
| Denominador | de los 183 evaluados |
| Fuente | `study_groups.csv menos exclusiones_tras_texto_completo.csv` |
| Cálculo | 183 − 118 excluidos = 65 |

## Informes de los estudios incluidos — ✔ consistente

| | |
|---|---|
| Publicada | 80 |
| Recalculada | 80 |
| Unidad de análisis | informes |
| Denominador | de los 233 informes evaluados |
| Fuente | `study_groups.csv, filas cuyo estudio no está excluido` |
| Cálculo | 233 − 153 informes de estudios excluidos = 80 |

## Estudios con publicación recuperable — ✔ consistente

| | |
|---|---|
| Publicada | 65 |
| Recalculada | 65 |
| Unidad de análisis | estudios |
| Denominador | de los 65 incluidos |
| Fuente | `study_groups.csv, situación «extraible» o «solo-resumen» del informe designado` |
| Cálculo | 65 de 65; los otros 0 son solo ficha de registro |

## Estudios con texto obtenido — ✔ consistente

| | |
|---|---|
| Publicada | 65 |
| Recalculada | 65 |
| Unidad de análisis | estudios |
| Denominador | de los 65 recuperables |
| Fuente | `carpetas textos_completos/pdf y texto_html` |
| Cálculo | 65 de 65 recuperables = 100.0 % |

## Estudios solo con ficha de registro — ✔ consistente

| | |
|---|---|
| Publicada | 0 |
| Recalculada | 0 |
| Unidad de análisis | estudios |
| Denominador | de los 65 incluidos |
| Fuente | `study_groups.csv, estudios cuyos informes son todos ficha de registro` |
| Cálculo | 0 + 65 recuperables = 65 incluidos |

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
| Publicada | 73 |
| Recalculada | 73 |
| Unidad de análisis | brazos |
| Denominador | de los 65 estudios incluidos |
| Fuente | `extraccion_adjudicada.csv menos los estudios excluidos` |
| Cálculo | 132 filas adjudicadas − 59 de estudios excluidos después = 73 |

## Brazos con texto completo — ✔ consistente

| | |
|---|---|
| Publicada | 73 |
| Recalculada | 73 |
| Unidad de análisis | brazos |
| Denominador | de los 73 brazos extraídos |
| Fuente | `extraccion_adjudicada.csv cruzado con las carpetas de texto` |
| Cálculo | 73 de 73 brazos pertenecen a estudios con texto |

## Estudios con diseño comparativo — ✔ consistente

| | |
|---|---|
| Publicada | 9 |
| Recalculada | 9 |
| Unidad de análisis | estudios |
| Denominador | de los 65 incluidos |
| Fuente | `extraccion_adjudicada.csv, diseño adjudicado; regla firmada el 2026-09-16` |
| Cálculo | estudios con al menos un brazo de diseño RCT/non-randomised trial/prospective cohort/retrospective cohort = 9 |

## Comparativos evaluables — ✔ consistente

| | |
|---|---|
| Publicada | 9 |
| Recalculada | 9 |
| Unidad de análisis | estudios |
| Denominador | de los 9 comparativos |
| Fuente | `los comparativos cuyo estudio tiene texto completo` |
| Cálculo | 9 − 0 sin texto () = 9 |

## Ensayos en la Tabla 2 — ✔ consistente

| | |
|---|---|
| Publicada | 2 |
| Recalculada | 2 |
| Unidad de análisis | estudios |
| Denominador | de los 65 recuperables |
| Fuente | `pre_extraccion_desde_resumen.csv, diseño DECLARADO en el resumen` |
| Cálculo | criterio distinto del anterior: clasifica por el resumen y no cuenta cohortes |

## Brazos con diseño comparativo — ✔ consistente

| | |
|---|---|
| Publicada | 12 |
| Recalculada | 12 |
| Unidad de análisis | brazos |
| Denominador | de los 73 brazos extraídos |
| Fuente | `extraccion_adjudicada.csv, brazos cuyo diseño es comparativo` |
| Cálculo | 12 brazos aportados por los 9 estudios comparativos |

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
