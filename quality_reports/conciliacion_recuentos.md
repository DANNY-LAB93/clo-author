# Conciliación de los ocho recuentos

Generado por `scripts/build_conciliacion.py`. Cada cifra sale de contar la
tabla `conciliacion_estudio_brazo.csv`, no de los escalares.

| Cifra del manuscrito | Valor | Unidad | Poblacion sobre la que se cuenta |
|---|---|---|---|
| Diseños comparativos, Tabla 2 | 10 | estudios | de los 94 recuperables, clasificados por el diseño **que declara el resumen**; NO incluye cohortes |
| Estudios con grupo de comparación, Resultados | 14 | estudios | del corpus vivo, por el diseño **adjudicado sobre el artículo**; SÍ incluye cohortes. **Regla firmada el 2026-09-16**: un estudio es comparativo si CUALQUIERA de sus brazos lo es |
| ídem, con la regla anterior | 13 | estudios | mandaba el PRIMER brazo del CSV. Se anota porque explica por qué un borrador anterior decía 13; la diferencia es EST-004 |
| Comparativos evaluables, Tabla 5 | 12 | estudios | los 14 anteriores **que tienen texto completo** |
| Primer filtro de la Tabla 6 | 17 | **brazos** | brazos de esos estudios comparativos; un estudio aporta más de un brazo |
| Filas de brazo comparadas | 130 | **filas** | brazos presentes en los DOS cuadernos (A tenía 132, B tenía 130), **incluidos los de estudios excluidos después** |
| Filas adjudicadas en total | 132 | **filas** | el cuaderno adjudicado entero; 30 pertenecen a estudios excluidos más tarde, y 132 − 30 = 102 |
| Brazos extraídos | 102 | **brazos** | todos los brazos del corpus vivo |
| Brazos legibles | 78 | **brazos** | los anteriores cuyo estudio tiene texto completo |
| Estudios con texto obtenido | 70 | estudios | del corpus vivo |

## Las tres confusiones que la tabla deshace

1. **Estudio ≠ brazo.** Tres de las ocho cifras cuentan brazos y cinco cuentan
   estudios. Los 17 brazos del primer filtro de la Tabla 6 salen de los 14
   estudios comparativos, no de otra población.
2. **Diseño declarado ≠ diseño adjudicado.** La Tabla 2 clasifica por el resumen
   sobre los 94 recuperables; la evaluación de riesgo de sesgo clasifica por el
   artículo sobre el corpus vivo. Que las dos den 10 y 14 no es contradicción:
   son criterios distintos, y la diferencia son las cohortes, que el resumen no
   cuenta como comparativas y el artículo sí.
3. **El corpus de hoy ≠ el corpus que se comparó.** Las 130 filas de brazo son un
   recuento histórico del trabajo de los dos extractores e incluyen estudios
   excluidos después. El puente es el cuaderno adjudicado: 132 filas en total,
   de las que 30 pertenecen a estudios excluidos más tarde, y quedan 102.

## Lo que esta tabla NO cierra

**Clasificar un estudio como comparativo no lo convierte en una comparación
utilizable.** Las dos cosas se cuentan por separado y no son la misma: hay 14
estudios *clasificados* como comparativos, y la Tabla 6 muestra cuántos de sus
brazos sostienen un contraste que se pueda usar. EST-004 es el caso extremo: es
comparativo porque uno de sus brazos es una cohorte prospectiva, pero sus dos
brazos son series clínicas del mismo centro sin asignación ni control externo.
La clasificación decide qué instrumento de riesgo de sesgo se aplica; no decide
que exista un comparador válido.

**Un paciente puede estar en dos estudios.** Esta tabla cuenta estudios y brazos,
no pacientes distintos. El examen de solapamiento está en
`solapamiento_candidatos.csv`.
