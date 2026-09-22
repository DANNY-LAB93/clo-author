# Las nueve firmadas, y una cita que era de otro artículo

**Estado:** FIRMADO por D. Valdiviezo y N. Trelles el 22 de septiembre de 2026.
**Comprobado, no ingerido**: falta resolver el punto 8, que pide un campo que
el formulario de extracción no tiene.
**Ficheros:** `~/Escritorio/FIRMAR_auditoria_2026-09-16.xlsx` (las nueve hojas
más la firma), `scripts/make_firma_auditoria.py` (lo construyó).
**Viene de:** la auditoría de cierre del 2026-09-16.

## Lo que volvió firmado

Las nueve decisiones están escogidas, las dos firmas puestas y la casilla
«¿habéis leído los artículos citados en cada hoja?» dice SI.

| | Decisión firmada |
|---|---|
| 1. EST-021 global | Corregirlo a «Algunas preocupaciones» |
| 2. EST-003 definición | Sustituir la definición por la del propio artículo y poner el numerador del brazo A en NA |
| 3. Solapamiento | Confirmar los once y declararlo en Resultados y en Limitaciones |
| 4. EST-077 | Son ciclos de tratamiento, no eventos: el campo va a NA |
| 5. EST-063 | Se excluye como protocolo; PRO pasa de 4 a 5 |
| 6. Comparativos | «15 con diseño comparativo, de los cuales 5 con grupo de comparación» |
| 7. EST-063 y EST-116 | Corregir los dos globales a «Sin información para juzgar» |
| 8. EST-021 extracción | n_arm = 13, mortality_n = 1, numerador 6 sobre denominador 12 |
| 9. EST-001 y EST-094 | Mantenerlos y declarar cuántos brazos quedan bajo el umbral |

## La cita de la hoja 4 no era de EST-077

Decía: «No adverse events were reported during treatment. At the 2-year
follow-up, the patient had no relapse without any suppressive treatment.»

Esa frase aparece **entera en EST-077 cero veces**. Aparece entera en
**EST-007** (Denis *et al.*, *Int J Infect Dis* 2026), que es el resumen de un
caso único de osteítis frontal en Rennes. Un estudio de un paciente no puede
sostener un juicio sobre un campo de cuatro pacientes y cinco ciclos. Buscada
por trozos en los 93 textos completos en caché, la única coincidencia es
EST-007.

La decisión firmada —que el 5 cuenta ciclos y no eventos— **es correcta**, y el
propio EST-077 la sostiene: «We performed a retrospective review of four
patients that underwent five separate courses of intravenous (IV) phage
therapy…», y en Resultados, sin entrelazar, «Four patients received five
separate courses of antibiotic and phage combination therapy.» La casilla se
sustituyó por esas dos.

**Pero el artículo no guarda silencio sobre los daños.** Describe uno sin usar
la palabra «adverse»: «Phage and meropenem were stopped on day 51 due to
concern for inflammatory/allergic reaction to either the antibiotic or phage.»
Poner el campo en NA es correcto para el número 5; la revisión **no puede decir
que EST-077 no informa de ningún evento**.

## Las otras ocho, comprobadas una a una

Cada frase se buscó por trozos de 24 caracteres en el texto del artículo que la
hoja nombra, porque el texto en caché sale a dos columnas entrelazadas y la
comparación de la cadena entera falla siempre.

| Hoja | Veredicto |
|---|---|
| 1. EST-021 global | Literal en EST-021, Métodos |
| 2. EST-003 | Pasaje correcto, redacción suavizada. Sustituida por la literal |
| 3. Solapamiento | **Estaba vacía.** Rellenada con las dos declaraciones literales |
| 5. EST-063 | Literal en EST-063 |
| 6. Comparativos | «sin grupo de control» no es cita de nada. Sustituida por las siete notas firmadas del dominio 1 |
| 7. EST-063 y EST-116 | **Estaba vacía.** Rellenada con la regla de ROBINS-I y las cuatro notas firmadas |
| 8. EST-021 extracción | Literal en EST-021, resumen |
| 9. EST-001 y EST-094 | Las dos literales, en su artículo |

De paso: el nombre de la segunda revisora estaba escrito «NATALY ELIZABTEH» y
en el resto del proyecto va «Nataly Elizabeth Trelles Avila». Corregido, porque
el nombre de una firma tiene que ser el mismo que el del manuscrito.

## El punto 8 no se puede ingerir como está escrito

«El numerador 6 sobre denominador 12» necesita un denominador propio del
desenlace, y el formulario de extracción **no tiene ese campo**. Tiene un solo
`n_arm`, y la Tabla 6 usa `N_brazo = n_arm` como denominador. Con n_arm = 13,
el par queda en 6/13, que no es lo firmado.

Es el mismo agujero que «comparador» y «tiempo de evaluación»: el dato existe
en el artículo y no existe en la ficha. Cerrarlo pide una columna nueva
—`clinical_success_denominator`— y eso reabre el formulario para los 103
brazos, o bien se registra 6/13 y la mITT de 12 se declara en nota. **Esa
elección es de los dos autores y no se toma aquí.**

## Las ocho restantes tampoco se han ingerido todavía

La 5 sola mueve trece recuentos: corpus 137 → 136, recuperables 95 → 94, con
texto 71 → 70, brazos 103 → 102, comparativos 15 → 14, evaluables 12 → 11,
juicios 90 → 82, exclusiones 46 → 47. Los 21 brazos del embudo descriptivo no
cambian. Nada de eso se ha tocado: el cuaderno está comprobado, y la ingestión
se hace de una vez, después de resolver el punto 8.
