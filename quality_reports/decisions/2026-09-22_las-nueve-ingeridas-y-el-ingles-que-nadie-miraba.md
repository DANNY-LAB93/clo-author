# Las nueve, ingeridas — y el manuscrito en inglés que nadie miraba

**Estado:** APLICADO el 22 de septiembre de 2026, con las dos firmas.
**SUPERA** el estado «comprobado, no ingerido» de
`2026-09-22_las-nueve-firmadas-y-una-cita-de-otro-articulo.md`, que quedó
cerrado en cuanto D. Valdiviezo resolvió el punto 8.
**Ficheros:** `scripts/ingest_firma_auditoria.py` (nuevo),
`scripts/build_grupo_comparacion.py` (nuevo),
`revision_sistematica/extraccion/correcciones_tras_texto_completo.csv`,
`revision_sistematica/cribado/exclusiones_tras_texto_completo.csv`,
`revision_sistematica/riesgo_sesgo/riesgo_sesgo_comparativos_adjudicado.csv`,
`revision_sistematica/riesgo_sesgo/grupo_de_comparacion_real.csv` (nuevo).

## El punto 8, resuelto

La hoja 8 firmaba «el numerador 6 sobre denominador 12» y la ficha de
extracción no tiene denominador propio del desenlace. D. Valdiviezo decidió el
22 de septiembre: **se registra 6/13 y la mITT de 12 se declara en nota.** No
se añade columna y no se reabre el formulario de los 102 brazos.

## Dónde entró cada cosa

`extraccion_adjudicada.csv` **es un derivado**: lo rehace
`build_adjudicated_dataset.py` desde los dos cuadernos, y se llevó por delante
las cuatro correcciones la primera vez que se escribieron ahí. Entraron donde
entraron las quince del 2026-09-01: en
`correcciones_tras_texto_completo.csv`, con valor anterior, valor corregido,
cita literal, motivo y las dos firmas. Los cuadernos siguen diciendo lo que
cada revisor escribió.

| Hoja | Dónde entró |
|---|---|
| 1, 7 | `riesgo_sesgo_comparativos_adjudicado.csv`, tres juicios globales |
| 2, 4, 8 | 9 filas nuevas en `correcciones_tras_texto_completo.csv` |
| 5 | 1 fila en `exclusiones_tras_texto_completo.csv`, código PRO |
| 3, 6, 9 | prosa del manuscrito, ninguna casilla de datos |

**Nada se borró.** Los ocho juicios de EST-063 siguen en su fichero, que es el
registro de lo que se juzgó de verdad; lo que cambió es que cuatro guiones que
los contaban sin filtrar —`build_auditoria_scalars`, `audita_cifras`,
`audita_pendientes` y `build_verifiables_package`— ahora descuentan a los
excluidos, igual que `study_groups` conserva a los excluidos del cribado y el
canal no los suma.

## Lo que movió

| | Antes | Ahora |
|---|---|---|
| Estudios | 137 | **136** |
| Informes agrupados | 171 | **170** |
| Recuperables | 95 | **94** |
| Con texto completo | 71 | **70** (74,5 %) |
| Brazos | 103 | **102** |
| Comparativos adjudicados | 15 | **14** |
| Evaluables | 12 | **11** |
| Celdas de la Tabla 5 | 90 (78 + 12) | **82 (71 + 11)** |
| Exclusiones tras texto completo | 46 | **47** (PRO 4 → 5) |
| Globales discordantes | 3 | **0** |
| Brazos con numerador imposible | 2 | **0** |

Las 17 cifras de `audita_cifras.py` vuelven a reproducirse, 17 de 17.
Los 21 brazos del embudo descriptivo no cambian.

## Tres cosas que el canal tapaba, y ahora no

**1. EST-116 salía discordante estando bien.** El comparador esperaba la cadena
«sin informacion» y el juicio se llama «Sin información para juzgar». En cuanto
se corrigió el global, el estudio pasó a contarse como discordante. Con la
comparación arreglada, **los 11 juicios globales se corresponden con sus
dominios y no hay ninguna excepción.**

**2. Tres frases del manuscrito estaban escritas a mano dentro del bloque que
`build_rob_table.py` reescribe entero**, y la primera pasada se las llevó sin
avisar: la coherencia de los globales, el desglose de las celdas de la Tabla 5
y en qué se apoya cada juicio. Ahora las genera el guion.

**3. Una frase se había vuelto falsa, no obsoleta.** Los dos manuscritos decían
«dos brazos declaran un numerador mayor que su denominador». Al corregir
EST-003 y EST-077 dejó de haber ninguno, y ninguna cifra fallaba porque la
frase no llevaba ancla. Se reescribió, y ahora está anclada.

## 33 anclas nuevas

`check_manuscript_claims.py` pasa de 131 a **179 afirmaciones**. Las nuevas
vigilan lo que nadie vigilaba: la composición por diseño —que llevaba los siete
recuentos tecleados y cuyo «4 ensayos no aleatorizados» se volvió falso—, los
pies de tabla, la descripción de los anexos y las frases que escriben las nueve
decisiones. Cada diseño tiene además su propio escalar (`diseno_case_report`,
`diseno_RCT`…), y el grupo de comparación real tiene el suyo, derivado de un
fichero firmado y no de la prosa.

## Lo que NO se arregló, y hay que decirlo

**El manuscrito en inglés lleva 19 cifras sin respaldo y va dos revisiones del
corpus atrás.** Dice «Of the 145 studies», «184 studies evaluated», 219, 179,
123: cifras de antes del 2026-09-14. No viaja en el sobre ni en el `.zip`, y
por eso no lo miraba ningún guardián. Desde hoy `check_manuscript_numbers.py`
sí lo mira —y por eso termina con error—, pero ponerlo al día **no es
sincronizar cifras**: hay pasajes enteros cuyo contenido ya no es cierto, y eso
lo reescribe una persona.
