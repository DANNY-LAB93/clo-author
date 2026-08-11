# Priorización del pozo de etapa 2

Generado por `scripts/prioritise_stage2.py`.

**Esto no filtra nada.** Los 13894 registros del pozo se criban igual;
solo cambia el orden de lectura. Ningún registro se descarta por su
puntuación, y por eso la priorización no aparece en el diagrama PRISMA.

## Validación contra los estudios ya incluidos

| | |
|---|---|
| Estudios incluidos presentes en el pozo | 40 |
| Mejor posición | 1 |
| Mediana | 95 (percentil 0.7) |
| Peor posición | 1239 (percentil 8.9) |

| Leídos en los primeros… | Estudios incluidos recuperados |
|---|---|
| 500 | 34 de 40 (85%) |
| 1000 | 39 de 40 (98%) |
| 2000 | 40 de 40 (100%) |
| 5000 | 40 de 40 (100%) |

## Distribución de la puntuación

| Rango | Registros |
|---|---|
| 30+ | 8 (0.1%) |
| 20-29 | 109 (0.8%) |
| 10-19 | 1357 (9.8%) |
| 1-9 | 5002 (36.0%) |
| <=0 | 7418 (53.4%) |

## Cómo se puntúa

Coincidencias de término, ponderadas; el título vale el doble que el
resumen. Restan los marcadores de trabajo de laboratorio, que **nunca**
excluyen: un estudio clínico puede describir su caracterización in vitro
en el mismo resumen.

| Peso | Señal |
|---|---|
| +10 | terapia con fagos |
| +8 | organismo |
| +6 | diseño de caso |
| +6 | uso compasivo |
| +5 | resistencia |
| +5 | pacientes |
| +4 | producto/práctica |
| +4 | nombre de producto |
| +3 | síndrome clínico |
| -6 | in vitro |
| -6 | modelo animal |
| -5 | caracterización de fago |
| -4 | ambiental/veterinario |

Cada registro lleva en la columna `senales` los términos que
explican su puntuación, de modo que el orden es auditable registro a
registro y no un número opaco.
