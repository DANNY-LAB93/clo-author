# Respuesta al encargo de corrección integral — 23 de septiembre de 2026

Las veinte instrucciones, comprobadas una a una contra los ficheros del
proyecto antes de tocar el manuscrito. Tres se apoyan en premisas que aquí no
se cumplen y aplicarlas literalmente habría hecho falso el manuscrito.

---

## Producto 2 — Tabla de cambios

| Punto | Sección | Problema | Corrección aplicada | Justificación | Fichero |
|---|---|---|---|---|---|
| 8 | Métodos 2.7, Resultados 3.7, Limitaciones | El manuscrito afirmaba que la evaluación «no admite medida de concordancia entre revisores». Los dos cuadernos individuales existen y difieren en 12 juicios | Medida y publicada: 62 de 74 (83,8 %), kappa de Cohen 0,78, 12 desacuerdos resueltos por consenso, los 12 en la misma dirección | Afirmar que un dato no se puede calcular cuando sí se puede es un error de hecho, no de estilo | `build_concordancia_rob.py`, `rob_bloques.py`, `build_rob_table.py` |
| 19 | Resultados 3.7 | 7 ensayos aleatorizados en la Tabla 2 frente a 3 evaluados con RoB 2, sin explicación | Declarado: solo 3 de los 7 tienen texto completo; de los otros 4 no se obtuvo el artículo (EST-029, EST-078, EST-157, EST-188) | Dos denominadores distintos leídos como incoherencia | `build_rob_table.py` |
| 11 | Tabla 5 | La columna «% de los 78 con texto completo» mezclaba unidades: 78 son BRAZOS, 70 son estudios con texto | Renombrada «% de los 78 brazos legibles» | Un denominador de brazo no se etiqueta como si fuera de estudio | `build_manuscript_tables.py` |
| 5 | Resultados 3.1 | 23 057 registros y 134 informes de registro sin decir si el segundo está dentro del primero | Declarado: los 134 están dentro (121 ClinicalTrials.gov, 10 CTIS, 3 EudraCT), y PRISMA los separa solo a partir del cribado | No era una discrepancia sino una omisión | `build_synthesis_scalars.py`, los dos manuscritos |

---

## Producto 3 — Reconciliación numérica

| Cifra | Original | Corregida | Fórmula | Denominador | Verificación |
|---|---|---|---|---|---|
| Estudios recuperables | 94 / 95 | **94** | corpus − solo-registro | 136 | `audita_cifras.py`, 17/17 |
| Textos completos | 70 / 78 / 79 | **70 estudios, 78 brazos** | dos unidades distintas | 94 y 102 | Tabla 5, columna renombrada |
| Comparativos | 10 / 14 | **10 por resumen, 14 adjudicados** | dos criterios declarados | 94 | `build_conciliacion.py` |
| ECA frente a RoB 2 | 7 / 3 | **7 por resumen, 3 con texto** | 7 − 4 sin artículo | 94 | `ecas_con_texto` |
| Brazos | 102 / 130 | **102 vivos, 130 filas comparadas** | 132 adjudicadas − 30 de excluidos | — | `build_conciliacion.py` |
| Concordancia riesgo de sesgo | «no calculable» | **83,8 %, kappa 0,78** | 62 / 74 | 74 juicios de 10 estudios | `concordancia_rob.csv` |
| Flujo PRISMA | 233 → 183 → 47 → 136 | sin cambio | 183 − 47 = 136 | — | `check_aritmetica.py` |
| Informes agrupados | 170 en 136 | sin cambio | 114 + 22 multiinforme | — | `audita_cifras.py` |
| Registros | 23 057 y 134 | **134 dentro de 23 057** | 121 + 10 + 3 | 23 057 | `registros_de_*` |

---

## Producto 4 — Información que tienen que aportar los autores

**Requiere leer artículos; no se puede rellenar sin abrirlos.**

1. **Punto 2 — clase de resistencia verificable.** Clasificar los 70 estudios
   leídos en MDR / XDR / PDR / DTR verificables frente a «declarada no
   verificable» exige el antibiograma de cada uno. Hoy el dato es la etiqueta
   textual del artículo, y así se declara.
2. **Punto 7 — reextracción de los comparativos.** Comparador, tiempo cero,
   tiempo de evaluación, cointervenciones y pérdidas no existen como campos.
   Son 14 artículos y un formulario nuevo. Lo medido hoy: **0 brazos con
   comparador extraído** sobre 102.
3. **Punto 15 — solapamiento de pacientes.** 11 pares confirmados, 3
   descartados, 1 sin resolver y **13 sin leer**.

**Requiere firma de los dos autores; es acto de autoría.**

4. **Puntos 2 y 12 — población del análisis principal.** Sacar del denominador
   a los 4 brazos por debajo del umbral de multirresistencia cambia la
   población de la revisión.
5. **Punto 18 — reestructuración.** Cambia la versión que se envía.

**Sigue faltando, de antes.** Los dos ORCID, los grados académicos, el correo
de N. Trelles, la aprobación ICMJE escrita, los dos formularios de la revista y
el registro en PROSPERO.

---

## Lo que NO se aplicó, y por qué

**Punto 4 — el papel de Rayyan está invertido en el encargo.** Pide describir
Rayyan como herramienta de apoyo a la selección. Aquí el cribado de las etapas
2 y 3 lo condujo **un solo revisor humano (D.V.), sin duplicación**, y las
decisiones registro a registro **las emitió un modelo de lenguaje (Claude Opus
5)**. Rayyan se usó **solo** en el recribado ciego de los 350 excluidos, que es
la validación, y ahí sí lo hicieron los dos autores. El manuscrito ya lo
declara así en §2.4, en §3.1.1 y en las Declaraciones. Escribirlo como pide el
punto 4 convertiría una declaración correcta en una falsa.

**Punto 3 — la restricción de idioma sí fue una enmienda.** El encargo pide
eliminar la sección de enmiendas *si* los criterios se fijaron antes del
cribado. Los registros fechados dicen que se adoptó el **11 de agosto de 2026,
con el cribado concluido**. El propio encargo resuelve el condicional: se
conserva, con su efecto medido (35 estudios).

**Punto 5 — no había discrepancia que resolver** entre 23 057 y 134, solo una
omisión, ya corregida.

**Punto 8, primera mitad — ya estaba cumplido.** §2.7 declara desde antes que
la evaluación es a nivel de dominio, sin responder las preguntas de
señalización, y que no debe atribuírsele reproducibilidad algorítmica.

**Puntos 1, 13, 14 y 16 — parcialmente cumplidos.** Los dos embudos ya están
separados; «eficacia» ya se usa solo para discutir si cabe una síntesis, nunca
para afirmarla; el manuscrito ya dice «sin publicación localizable» y no «sesgo
de publicación confirmado».

---

## Un hallazgo que no estaba en el encargo

De los 13 desacuerdos de riesgo de sesgo, el cuaderno de consenso adoptó el
juicio de D. Valdiviezo en **los 13** y el de N. Trelles en **ninguno**. Los dos
autores confirmaron el 23 de septiembre de 2026 que los discutieron uno a uno y
que N. Trelles aceptó el juicio de D.V. en todos. El manuscrito lo dice así —y
dice también que los 13 fueron en la misma dirección, porque el lector necesita
ese dato para calibrar lo que vale ese consenso.

`paper/manuscrito_JSR_editado.md`, del 14 de septiembre, sigue en el
repositorio fuera del canal y fuera de los guardianes. No lo escribe ningún
guion y nadie lo comprueba. Conviene borrarlo o meterlo en el canal.
