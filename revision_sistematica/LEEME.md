# Revisión sistemática — fagoterapia en *Pseudomonas aeruginosa* MDR/XDR/PDR

Todo lo que sostiene la revisión sistemática vive aquí. **El metaanálisis está en
`metaanalisis/` y no comparte ningún fichero con esta carpeta.**

| Carpeta | Qué contiene |
|---|---|
| `busqueda/` | Exportaciones crudas de cada base, tal como se descargaron, y `sources.json`, el manifiesto que declara cuáles entran en el corpus. |
| `cribado/` | Corpus unificado, etapa 1 por reglas, pozo priorizado, registros de decisión de las etapas 2 y 3, y la agrupación de informes en estudios. |
| `extraccion/` | Cuadernos de extracción de Danny y de Nataly, la pre-extracción desde resumen y los paquetes de petición de texto completo. |
| `textos_completos/` | PDFs recuperados (`pdf/`) y la trazabilidad de identificadores y descargas. |

## Reglas que no se saltan

1. **`sources.json` manda.** Un fichero de búsqueda que no esté en el manifiesto
   no entra en el corpus y no aparece en el diagrama PRISMA. Así se perdieron 638
   registros de BVS hasta el 2026-08-10.
2. **Los registros de decisión son solo-anexar.** Una corrección es una fila
   nueva que sustituye a la anterior; las dos se quedan. Borrar una decisión
   borra la prueba de que se tomó.
3. **Nada se indexa por posición.** Las claves son `record_id` (derivado del
   contenido) y `clave` de estudio. La posición en el pozo cambia en cuanto
   cambia el manifiesto, y una tabla leída por posición pasa a apuntar a otro
   registro sin que nada falle a la vista. Ha ocurrido tres veces.
4. **`EST-NNN` no se reasigna.** La numeración se conserva entre ejecuciones
   porque está en los cuadernos de las dos personas que extraen.

## Comprobación

```
python scripts/check_pipeline_coherence.py
```

Cuadra eslabón por eslabón: corpus → etapa 1 → pozo → etapa 2 → etapa 3 →
estudios → pre-extracción, y exige que toda fuente declarada esté representada.
Sale con código 1 si algo no cuadra.
