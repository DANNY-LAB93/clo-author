# Instantáneas

Lo que hay aquí son **fotos de un estado que ya pasó**. Se conservan porque
documentan una decisión tomada ese día, y se guardan aparte porque su parecido
con un fichero vivo es justamente el peligro: tienen las mismas columnas que
los ficheros que el canal sí actualiza, y un script que las lea sin saberlo
computa con datos caducados sin dar ningún error.

**Regla: ningún script del canal lee nada de esta carpeta.** Si algo de aquí
hace falta para calcular, se busca la fuente viva.

---

## `2026-08-09_orden_de_extraccion.csv`

La lista con la que se repartió el trabajo de extracción: 124 estudios
ordenados por prioridad, con su diseño, su revista y dos columnas de estado,
`texto_completo` y `ya_extraido`.

**Por qué dejó de valer.** Las dos columnas de estado se escribieron el 9 de
agosto de 2026 y no se volvieron a tocar. Después de esa fecha se recuperaron
textos completos que ahí figuran como `no`, y el 1 de septiembre se excluyeron
29 estudios tras leer sus artículos. La lista de 124 identificadores sigue
siendo correcta como *lo que se repartió*; las columnas de estado no son
correctas como *lo que hay*.

**Quién la leía y qué se hizo.** La auditoría del 2026-08-26 la señaló
(`auditoria_2026-08-26/auditoria_empaquetado.md`, punto 2). El 2026-09-14 se
cortaron los dos consumidores:

| Script | Leía | Ahora lee |
|---|---|---|
| `resolve_mechanical_conflicts.py` | la columna `texto_completo`, para estratificar los conflictos en bloques A/B/C | los ficheros de `revision_sistematica/textos_completos/` en disco, igual que `build_synthesis_scalars.py` |
| `build_verifiables_package.py` | la lista de identificadores, para marcar `en_corpus_actual` en S4 | `cribado/study_groups.csv` menos `cribado/exclusiones_tras_texto_completo.csv`, igual que S5 |

El día del cambio los dos caminos daban **exactamente los mismos 95 estudios**,
de modo que ninguna cifra publicada se movió. Lo que se corrigió no fue un
número equivocado: fue que el número correcto salía de una fuente que ya no
seguía al corpus.

Las auditorías que la citan por su ruta antigua
(`quality_reports/orden_de_extraccion.csv`) no se reescriben: son registros de
lo que se vio ese día.
