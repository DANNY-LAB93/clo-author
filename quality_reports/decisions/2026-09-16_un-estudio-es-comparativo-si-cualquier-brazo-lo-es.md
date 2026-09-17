# Un estudio es comparativo si cualquiera de sus brazos lo es

**Estado:** DECIDIDO por D. Valdiviezo el 16 de septiembre de 2026 y **aplicado**.
Deja 8 juicios de riesgo de sesgo pendientes de firma.
**Ficheros:** `scripts/make_rob_forms.py` (la regla), `scripts/build_rob_table.py`
(el párrafo de alcance), `quality_reports/rob_tabla_estado.json`,
`~/Escritorio/FIRMAR_riesgo_de_sesgo_EST-004.xlsx`
**Viene de:** la conciliación del 2026-09-15
(`quality_reports/conciliacion_recuentos.md`)

## El defecto

`make_rob_forms.corpus()` asignaba a cada estudio el diseño de **su primer
brazo** y descartaba los demás. Con dos brazos de diseño distinto, la
clasificación dependía del orden de las filas del CSV, que no significa nada.

**EST-004** tiene brazo A serie de casos (7 pacientes) y brazo B cohorte
prospectiva (2 pacientes). Por esa regla era «serie de casos» y quedaba fuera
de la evaluación de riesgo de sesgo — mientras su brazo B **sí** contaba entre
los 18 brazos comparativos del embudo de la Tabla 6. El mismo estudio era
comparativo para una tabla y no para la otra, y nada fallaba a la vista.

## La regla nueva

Un estudio es comparativo si **cualquiera** de sus brazos lo es. Entre varios
diseños comparativos gana el más exigente en instrumento —un ECA se evalúa con
RoB 2 aunque el estudio traiga también una cohorte— y si ninguno lo es se
conserva el primero, que era el comportamiento anterior.

## Lo que mueve

| | Antes | Ahora |
|---|---|---|
| Comparativos adjudicados | 14 | **15** |
| Evaluables | 11 | **12** (3 RoB 2, 9 ROBINS-I) |
| Sin texto completo | 3 | 3 (EST-029, EST-157, EST-165) |
| Juicios de dominio | 82 de 82 | **82 de 90** |

**No mueve ninguna otra cifra.** El corpus sigue en 137, los extraíbles en 95,
los brazos en 103 y el embudo de la Tabla 6 en 103→18→5→2→1→1→0: el brazo B de
EST-004 ya estaba dentro de los 18 y cae igual en el cuarto filtro, porque el
artículo no define qué contaba como éxito.

## Lo que rompe, y hay que decirlo

La evaluación de riesgo de sesgo **deja de estar completa**. El manuscrito
vuelve a llevar el aviso de PENDIENTE en su sección de riesgo de sesgo, el ítem
11 de PRISMA vuelve a PARCIAL y el 18 a NO CUMPLE. **El sobre no se puede
enviar en este estado**, y esa es la consecuencia directa de la decisión, no un
efecto colateral inesperado: EST-004 tiene texto completo, de modo que es
evaluable y hay que evaluarlo.

`FIRMAR_riesgo_de_sesgo_EST-004.xlsx` trae los 7 dominios de ROBINS-I más el
juicio global, con el contexto del estudio, el desplegable de las cinco
categorías y una columna para la frase del artículo en que se apoya cada
juicio. Va en fichero aparte a propósito: **los 82 firmados el 2026-09-09 no se
tocan**, y el cuaderno de consenso original no se regenera.

## De paso

El párrafo de alcance de `build_rob_table.py` llevaba tres cifras tecleadas
dentro de la plantilla —«El duodécimo», «los 11 ensayos» y «los 71 con texto
obtenido»— y las tres se volvieron falsas a la vez con este cambio. Ahora
entran por el diccionario, incluida la lista nominal de los que no tienen
texto. Y el guardián numérico aprendió que `EST-029` es una etiqueta y no la
cifra 29.
