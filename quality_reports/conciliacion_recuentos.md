# Conciliación de los ocho recuentos

Generado por `scripts/build_conciliacion.py`. Cada cifra sale de contar la
tabla `conciliacion_estudio_brazo.csv`, no de los escalares.

| Cifra del manuscrito | Valor | Unidad | Poblacion sobre la que se cuenta |
|---|---|---|---|
| Diseños comparativos, Tabla 2 | 2 | estudios | de los 65 recuperables, clasificados por el diseño **que declara el resumen**; NO incluye cohortes |
| Estudios con diseño comparativo, Resultados | 9 | estudios | del corpus vivo, por el diseño **adjudicado sobre el artículo**; SÍ incluye cohortes. **Regla firmada el 2026-09-16**: un estudio es comparativo si CUALQUIERA de sus brazos lo es |
| ídem, con la regla anterior | 8 | estudios | mandaba el PRIMER brazo del CSV. Se anota porque explica por qué un borrador anterior decía 8; la diferencia es EST-004 |
| Comparativos evaluables, Tabla 5 | 9 | estudios | los 9 anteriores **que tienen texto completo** |
| Primer filtro de la Tabla 6 | 12 | **brazos** | brazos de esos estudios comparativos; un estudio aporta más de un brazo |
| Filas de brazo comparadas | 130 | **filas** | brazos presentes en los DOS cuadernos (A tenía 132, B tenía 130), **incluidos los de estudios excluidos después** |
| Filas adjudicadas en total | 132 | **filas** | el cuaderno adjudicado entero; 59 pertenecen a estudios excluidos más tarde, y 132 − 59 = 73 |
| Brazos extraídos | 73 | **brazos** | todos los brazos del corpus vivo |
| Brazos legibles | 73 | **brazos** | los anteriores cuyo estudio tiene texto completo |
| Estudios con texto obtenido | 65 | estudios | del corpus vivo |

## Las tres confusiones que la tabla deshace

1. **Estudio ≠ brazo.** Tres de las ocho cifras cuentan brazos y cinco cuentan
   estudios. Los 12 brazos del primer filtro de la Tabla 6 salen de los 9
   estudios comparativos, no de otra población.
2. **Diseño declarado ≠ diseño adjudicado.** La Tabla 2 clasifica por el resumen
   sobre los 65 recuperables; la evaluación de riesgo de sesgo clasifica por el
   artículo sobre el corpus vivo. Que las dos den 2 y 9 no es contradicción:
   son criterios distintos, y la diferencia son las cohortes, que el resumen no
   cuenta como comparativas y el artículo sí.
3. **El corpus de hoy ≠ el corpus que se comparó.** Las 130 filas de brazo son un
   recuento histórico del trabajo de los dos extractores e incluyen estudios
   excluidos después. El puente es el cuaderno adjudicado: 132 filas en total,
   de las que 59 pertenecen a estudios excluidos más tarde, y quedan 73.

## Lo que esta tabla NO cierra

**Clasificar un estudio como comparativo no lo convierte en una comparación
utilizable.** Las dos cosas se cuentan por separado y no son la misma: hay 9
estudios *clasificados* como comparativos, y la Tabla 6 muestra cuántos de sus
brazos sostienen un contraste que se pueda usar. EST-004 es el caso extremo: es
comparativo porque uno de sus brazos es una cohorte prospectiva, pero sus dos
brazos son series clínicas del mismo centro sin asignación ni control externo.
La clasificación decide qué instrumento de riesgo de sesgo se aplica; no decide
que exista un comparador válido.

**Un paciente puede estar en dos estudios.** Esta tabla cuenta estudios y brazos,
no pacientes distintos. El examen de solapamiento está en
`solapamiento_candidatos.csv`.
