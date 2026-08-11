# Metaanálisis — APARCADO

**Este trabajo está en pausa por decisión del 2026-08-10: ahora mismo solo se
avanza en la revisión sistemática.** Se conserva completo y funcionando para
retomarlo, pero **no debe mezclarse con `revision_sistematica/`**.

| Carpeta | Qué contiene |
|---|---|
| `datos/` | Extracción por brazos (`phage_therapy_extraction_raw.csv`), el conjunto limpio, su libro de códigos y el manifiesto del corpus documental. |
| `scripts_R/` | Canal completo en R: preparación, estimación de proporciones agrupadas, robustez, falsación, figuras, tablas, GRADE y riesgo de sesgo. |

## Aviso importante antes de retomarlo

Los datos de `datos/` proceden de una extracción **anterior** a la reconstrucción
PRISMA. La revisión sistemática en curso identifica **219 estudios** frente a los
40 sobre los que se construyó este metaanálisis. Cuando se retome, el conjunto de
estudios habrá que rehacerlo desde `revision_sistematica/cribado/study_groups.csv`
y desde la extracción por duplicado, no desde estos ficheros.

## Ejecución

```
Rscript metaanalisis/scripts_R/00_master.R
```
