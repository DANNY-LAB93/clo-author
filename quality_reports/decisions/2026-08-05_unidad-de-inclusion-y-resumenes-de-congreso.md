# Decisión de protocolo — Unidad de inclusión y resúmenes de congreso

**Fecha:** 2026-08-05
**Fase:** Selección de estudios, antes de la evaluación a texto completo
**Decide:** usuario (DANNY-LAB93), a propuesta razonada del asistente
**Afecta a:** diagrama PRISMA, tabla de características, plan de sensibilidad, GRADE

---

## La pregunta

De los 268 informes que pasan a texto completo, 15 son resúmenes de congreso.
¿Cuentan como informe elegible por sí mismos o solo como señal para localizar la
publicación completa?

## Lo que decidió el dato, no la doctrina

La pregunta parecía afectar a 15 registros. Al agrupar los informes por estudio
resultó que **12 de esos 15 son informes adicionales de ensayos que ya tienen
publicación completa incluida** (siete del BX004-A, dos del CYPHY, uno de TP-102,
dos del programa de Leitner). Solo **3** son la única fuente de su estudio:

| orden | fuente | estudio |
|---|---|---|
| 288 | Int J Diabetes Dev Ctries 2025 | fagoterapia en pie diabético, estudio piloto (India) |
| 888 | Eur Urol Suppl 2016 | cribado in vitro y aplicación in vivo en ITU (grupo de Leitner) |
| 4039 | Nephrol Dial Transplant 2020 | ITU recurrente en trasplantadas renales posmenopáusicas |

La decisión afecta, por tanto, a tres estudios.

## Decisión

**Los resúmenes de congreso son elegibles. La unidad de inclusión es el estudio,
no el informe.**

1. Resumen que es informe adicional de un estudio ya representado → no cuenta
   como estudio aparte; fuente complementaria y contraste de desenlaces.
2. Resumen que es la única fuente de su estudio → se incluye, se identifica en la
   tabla de características, entra en la comprobación de sensibilidad #14 del
   memo de estrategia y su certeza se degrada por limitaciones de notificación.
3. Estudio cuya única fuente es una ficha de registro → no entra en la síntesis;
   se lista como estudio en curso o sin resultados publicados.

## Por qué, y por qué no lo contrario

Excluir de oficio la evidencia comunicada solo en congresos introduce sesgo de
notificación: lo que no llega a publicación completa tiende a diferir de lo que
sí llega. El argumento pesa aquí más de lo habitual porque la fagoterapia es una
terapia emergente cuya evidencia son en buena parte usos compasivos y series
pequeñas, comunicadas primero —o solo— en congresos; el material descartado no
sería aleatorio.

La alternativa («solo como señal para buscar la publicación») es correcta para
los 12 que tienen artículo, y es exactamente lo que hace esta decisión con ellos.
Para los 3 restantes significaría descartarlos en silencio. Además, haber buscado
la publicación y no encontrarla es un dato relevante sobre no publicación, que la
revisión debería medir y no ocultar.

El coste está acotado y es comprobable: con 3 estudios afectados, el análisis de
sensibilidad zanja empíricamente si cambian algo.

## Qué se implementó

- `scripts/group_reports_into_studies.py` — agrupa los 268 informes en 219
  estudios y designa una única fuente de extracción por estudio.
- Cadena de agrupación: NCT propio → NCT declarado dentro del resumen →
  atribución razonada (`fulltext_identifiers.csv`) → título normalizado.
- Columna `EXTRAER DE ESTE` en la hoja `Texto_completo` de `cribado_pozo.xlsx`.
- Comprobación #14 añadida al plan de robustez (memo de estrategia, Prioridad 5).

## Riesgo que esto evita, y que era real

Antes de agrupar, los siete resúmenes del BX004-A figuraban como siete estudios
distintos. Extraer de dos de ellos habría metido a los mismos pacientes dos veces
en el metaanálisis. Además, el artículo del BX004-A en *Nature Communications*
(PMID 40593506) **no lleva el NCT en su registro bibliográfico**, así que en la
primera versión de la agrupación el ensayo salía clasificado como «solo-resumen»
—teniendo publicación completa— y se habría ido al análisis de sensibilidad que
excluye precisamente los estudios solo-resumen. Se corrigió rastreando el NCT
dentro del texto del resumen, aceptándolo solo cuando ese NCT ya existe como
registro propio de otro informe del pozo.

## Reparto resultante

| | informes | estudios |
|---|---:|---:|
| Total a texto completo | 268 | 219 |
| Con artículo del que extraer | — | 156 |
| Solo ficha de registro (en curso / sin resultados) | — | 60 |
| Solo resumen de congreso | — | 3 |

---

# Adenda — Doble extracción independiente (2026-08-05)

El cribado lo hizo un revisor único. Para que la extracción no herede esa
limitación se monta doble extracción con resolución de conflictos documentada.

**Procedimiento**

1. `python scripts/make_extraction_forms.py --revisor "Nombre"` genera un
   formulario **ciego**: sin ningún valor previo, ni siquiera para los 42
   estudios que este proyecto ya tiene extraídos. Prerrellenar destruiría la
   medida.
2. Cada revisor rellena el suyo sin ver el del otro ni el dataset de extracción.
3. `python scripts/compare_extractions.py --a ... --b ...` calcula la kappa de
   Cohen por variable categórica, el acuerdo exacto y la diferencia media en las
   numéricas, y escribe la lista de conflictos.
4. Los conflictos se resuelven por consenso en `data/raw/extraction_conflicts.csv`,
   dejando quién resolvió y cuándo. **La concordancia se informa ANTES de la
   resolución**: la kappa posterior al consenso siempre es 1 y no dice nada.

**Si el segundo revisor solo puede hacer una muestra**, `--muestra N --semilla S`
genera un subconjunto aleatorio reproducible; se declara el porcentaje verificado
y la concordancia observada en ese subconjunto.

**Decisiones de medida que no son neutrales**

- La concordancia se mide sobre el valor **normalizado**: `route` tiene 23
  variantes en el corpus, casi todas `other (...)` con el paréntesis redactado de
  otra forma. Comparadas literalmente, dos revisores que codificaron ambos "otra
  vía" contarían como desacuerdo y la kappa se hundiría por un artefacto de
  redacción. El texto literal se conserva en la lista de conflictos.
- Una fila presente en una sola extracción **no** es desacuerdo de valor sino de
  cobertura (un revisor separó brazos que el otro agrupó). Se cuenta aparte;
  mezclarlo atribuiría a discrepancia lo que es diferencia de granularidad.
- Cuando ambos revisores usan una sola categoría, la kappa es 0/0. Se informa
  "no calculable (sin variación)", no un 0 que parecería desacuerdo total.
- El emparejamiento va por `id_provisional`, no por `study_id`: el pozo no guarda
  el autor, así que el id "Autor Año" no se puede componer hasta leer el texto, y
  dos revisores lo escribirían distinto.

**Estado:** formularios generados para 159 estudios (156 extraíbles + 3
solo-resumen) en `data/extraction/`. Maquinaria probada de punta a punta: 10
discrepancias sembradas, 10 detectadas, 0 falsos positivos por reescritura del
paréntesis.
