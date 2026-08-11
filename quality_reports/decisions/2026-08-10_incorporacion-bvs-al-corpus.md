# Incorporación de BVS al corpus de cribado

**Fecha:** 2026-08-10
**Fase:** Cribado (etapas 1 y 2)
**Estado:** RESUELTO — corpus reconstruido, 394 títulos cribados, cadena verificada

---

## Qué se encontró

Una comprobación de coherencia de extremo a extremo del canal PRISMA detectó que
`data/raw/bvs_non_medline.ris` estaba **en disco pero no en el manifiesto**
`data/raw/sources.json`. En consecuencia, los **638 registros descargados de BVS
nunca entraron en el corpus de cribado**: se buscaron, se exportaron y se
perdieron entre la descarga y la construcción del corpus.

La omisión fue accidental, no deliberada, y hay tres pruebas de ello:

1. `quality_reports/ecuaciones_busqueda_final.md` documenta la búsqueda BVS como
   ejecutada, con el desglose exacto por base (LILACS 417, VETINDEX 89, CUMED 50,
   BINACIS 46, Sec. Est. Saúde SP 44, non-MEDLINE 26, MedCarib 17, Coleciona SUS
   12, BBO 11 = 638) y la marca «✅ | pendiente» en la tabla de estado.
2. `search_equations_all_databases.md` la contabiliza como fuente del protocolo.
3. `scripts/deduplicate_sources.py` ya contenía la función `bvs_id()`, escrita
   específicamente para leer los PMID que BVS archiva como `ID - mdl-42450545`.
   Es decir: el lector de BVS estaba construido y probado. Solo faltaba la línea
   del manifiesto.

## Cómo se detectó

No por casualidad. La comprobación de coherencia compara, eslabón por eslabón,
lo que entra y lo que sale de cada etapa. Un aviso —14 decisiones de etapa 2
sobre registros ausentes del pozo— obligó a reconstruir el corpus previo desde
las exportaciones crudas, y al listar las fuentes representadas en el corpus
congelado apareció que BVS no figuraba en ninguna de las 16 698 filas.

## Qué se hizo

1. **Respaldo** de los artefactos congelados en `data/raw/.congelado_pre_bvs/`
   (corpus, etapa 1, pozo priorizado y manifiesto anterior).
2. **Defecto corregido en el lector** (`deduplicate_sources.py`, `strip_markup`):
   BVS y Scopus archivan el mismo artículo como `<i>Klebsiella</i>` y
   `Klebsiella`. `norm_title` borra `<` y `>` pero conserva la letra de la
   etiqueta, de modo que las dos variantes normalizaban distinto y el mismo
   informe se habría contado dos veces siempre que no llevara DOI ni PMID.
   Además la variante con marcado siempre es la más larga y ganaba el
   `longest()`, metiendo HTML en el corpus. Se eliminan las etiquetas al cargar.
   Efecto medido: 14 títulos limpiados, 0 títulos con `<` en el corpus final.
3. **Manifiesto actualizado** y corpus reconstruido.
4. **Etapa 1 reejecutada**: auditoría de control positivo SUPERADA (40 de 40
   estudios incluidos conservan al menos un informe).
5. **Pozo repriorizado** y **394 títulos nuevos cribados** en etapa 2.

## Efecto sobre el diagrama PRISMA

| Eslabón | Antes | Después | Δ |
|---|---:|---:|---:|
| Registros de origen | 22 419 | 23 057 | +638 |
| Informes únicos (corpus) | 16 698 | 17 129 | +431 |
| Excluidos en etapa 1 (reglas) | 3 189 | 3 235 | +46 |
| Pozo de cribado por título | 13 509 | 13 894 | +385 |
| Avanzan a resumen | 460 | 460 | 0 |
| Pasan a texto completo | 268 | 268 | 0 |
| Estudios | 219 | 219 | 0 |

**Ningún registro de BVS avanzó más allá del título.** Los 394 se excluyeron con
el vocabulario cerrado: LAB 230, REV 56, OFF 54, VET 44, ORG 8, SEC 2. El
contenido es literatura regional iberoamericana de fagotipificación (Salmonella,
Staphylococcus, Mycobacterium), microbiología de aguas y alimentos, veterinaria
y biología molecular clásica, en su mayoría anterior a 2000.

## Por qué el resultado no invalida el hallazgo

Que el aporte neto a la síntesis sea cero **no significa que la omisión fuera
inocua**. Significa que se puede afirmar, con la evidencia en el registro de
decisiones, que la búsqueda de BVS no aportaba estudios elegibles. Antes de
cribarla eso era una conjetura; ahora es un resultado auditable, y el diagrama
PRISMA declara los 638 registros en la casilla que les corresponde en vez de
omitir una base entera del recuento.

## Cabo suelto cerrado en la misma revisión

23 decisiones de etapa 2 apuntan a `record_id` que ya no existen en el pozo. De
ellas, 22 eran EXCLUDE y **una era ADVANCE** (`Rd069723093`, posición antigua
138), lo que planteaba la pregunta de si un registro juzgado potencialmente
elegible se había perdido al reconstruir el corpus.

Se resolvió por acotación. El mapeo posición antigua → posición nueva de los
vecinos es un desplazamiento limpio de 1 (la 137 sigue siendo *Bacteriophage
Therapy for Chronic Mastoiditis* y la antigua 139 pasa a 138), de modo que el
registro perdido era un título de 2025 alfabéticamente comprendido entre
*«Bacteriophage Therapy for Chronic Mastoiditis»* y *«Bacteriophage therapy in
women with chronic recurrent cystitis»*. En el corpus definitivo hay
**exactamente cinco** títulos en ese intervalo, y los cinco están en el pozo y
tienen decisión de etapa 2 registrada:

| record_id | pos. | etapa 2 | etapa 3 |
|---|---:|---|---|
| `R23545312bb` | 50 | EXCLUDE | — |
| `Rbd524d27e8` | 388 | ADVANCE | EXCLUDE |
| `Rff334c4762` | 621 | EXCLUDE | — |
| `Rb7ce8a80f4` | 823 | EXCLUDE | — |
| `R80de941773` | 2 652 | EXCLUDE | — |

Cualquiera que fuese el registro de la posición 138, está cribado. No se perdió
ningún candidato.

**Causa raíz del desajuste:** las 23 decisiones se tomaron entre las 23:49 del
4-08 y las 00:08 del 5-08, mientras `scopus_armB.csv` seguía escribiéndose (su
marca de tiempo es 00:25 del 5-08). Se cribó contra un pozo que aún estaba
creciendo. Las filas se conservan porque el registro es solo-anexar: borrarlas
eliminaría la prueba de que el desajuste existió.

**Regla que se deriva:** no iniciar el cribado hasta que el manifiesto esté
cerrado y todas las exportaciones tengan marca de tiempo anterior a la
construcción del corpus.

## Ficheros tocados

- `data/raw/sources.json` — añadida la entrada BVS
- `scripts/deduplicate_sources.py` — `strip_markup()` aplicado en `load()`
- `data/raw/screening_corpus_all.csv`, `screening_stage1_all.csv`,
  `screening_stage2_priorizado.csv` — reconstruidos
- `data/raw/screening_stage2_pool_decisions.csv` — +394 filas
- `data/raw/.congelado_pre_bvs/` — respaldo de la versión anterior

---

## Efecto colateral: tres tablas indexadas por posición

Reconstruir el pozo destapó un defecto que llevaba tiempo latente y que solo se
manifiesta cuando el manifiesto de fuentes cambia. Tres tablas curadas a mano se
leían por `orden` —la posición del registro en el pozo priorizado— en vez de por
`record_id`:

| Fichero | Tabla | Qué provocó |
|---|---|---|
| `scripts/group_reports_into_studies.py` | atribuciones leídas de `fulltext_identifiers.csv` | El BX004-A (11 informes) y el TP-102 (4) se partieron en dos estudios cada uno |
| `scripts/resolve_fulltext_ids.py` | `ATRIBUCION` y `SIN_PMID` | Las 24 atribuciones razonadas pasaron a apuntar a informes ajenos; los «sin resolver» subieron de 0 a 10 |
| `scripts/group_reports_into_studies.py` | numeración `EST-NNN` | Doce estudios corrieron un puesto: EST-205 (artículo cubano) pasó a EST-194 y los demás detrás |

El tercero era el más grave. `EST-NNN` es la clave con la que Danny y Nataly
tienen sus cuadernos de extracción y con la que está indexada la pre-extracción
desde resumen: renumerar en silencio habría reasignado el trabajo de dos
personas a estudios que no leyeron, sin que ningún recuento cambiara.

**Corregido:** las tres tablas se indexan ahora por `record_id`, y la numeración
`EST-NNN` se conserva entre ejecuciones leyendo la asignación anterior y dando
número nuevo solo a claves de estudio nuevas. Verificado: tres ejecuciones
consecutivas del canal producen ficheros idénticos byte a byte, y los 219
estudios conservan su número.

**Regla:** en este proyecto nada se indexa por posición. Ni decisiones, ni
atribuciones, ni numeración de estudios. La posición depende del manifiesto; el
`record_id` y la clave de estudio dependen del contenido.
