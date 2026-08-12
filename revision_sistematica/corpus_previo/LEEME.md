# Corpus de la extracción previa — NO es la extracción en curso

**Cuidado: esto no se toca para extraer.** La extracción viva son los dos
cuadernos de `revision_sistematica/extraccion/`. Lo de aquí es material anterior
que se conserva porque hay código que lo lee.

## Qué es

Estos tres archivos vienen de la extracción que se hizo **antes** de la
reconstrucción PRISMA, cuando el corpus tenía 40 brazos sobre 33 estudios. La
revisión actual identifica **184 estudios**, de los cuales 124 son extraíbles.
Las cifras de aquí, por tanto, **no son las del manuscrito** y no deben citarse.

| Archivo | Para qué sigue haciendo falta |
|---|---|
| `phage_therapy_extraction_dataset.csv` | `make_extraction_forms.py` lee su columna `journal_tier` para no reasignar niveles de revista ya decididos, y `compare_extractions.py` lo admite como término de comparación (`--a corpus`). |
| `phage_therapy_extraction_codebook.md` | Documenta las columnas del CSV anterior. Sin él, el CSV es opaco. |
| `document_corpus_manifest.csv` | Salida de `build_document_corpus_manifest.py`: una fila por documento del corpus. |

## De dónde salió

Estaba en `metaanalisis/datos/`. El 2026-08-12 se eliminó la carpeta
`metaanalisis/` entera —el canal de metaanálisis en R quedó aparcado el
2026-08-10 y el manuscrito actual sostiene que este cuerpo de evidencia no
admite síntesis cuantitativa— y estos tres archivos se rescataron aquí porque
quince scripts los referenciaban.

Lo eliminado sigue recuperable del historial de git:

```
git checkout b797339 -- metaanalisis/
```

Ahí están el canal completo en R (`00_master.R` … `17_*.R`), la extracción
cruda (`phage_therapy_extraction_raw.csv`) y las salidas del metaanálisis.
El contenido intelectual de esa extracción sobrevive en el CSV limpio que sí
está en esta carpeta.
