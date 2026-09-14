# «Verificabilidad» pasa a «completitud del reporte»

**Fecha:** 2026-09-14 (segunda revisión del título del mismo día; ver
[2026-09-14_titulo-acortado-a-141-caracteres.md](2026-09-14_titulo-acortado-a-141-caracteres.md))
**Decide:** D. Valdiviezo
**Estado:** APLICADO

## Qué cambia

| | Castellano | Inglés |
|---|---|---|
| **Antes** (141 / 141) | …revisión sistemática de la literatura clínica y de su **verificabilidad** | …a systematic review of the clinical literature and its **verifiability** |
| **Ahora** (148 / 150) | …revisión sistemática de la literatura clínica y **la completitud de su reporte** | …a systematic review of the clinical literature and its **reporting completeness** |

## De dónde sale

D. Valdiviezo pidió sustituir «verificabilidad» por «replicabilidad **o algún
sinónimo**». Se sometió a un concejo de doce evaluadores: tres pesquisas sobre
los ficheros, cuatro dictámenes con lentes distintas, un escéptico por dictamen
y un acta final.

## «Replicabilidad» quedó descartada por unanimidad

Los cuatro dictámenes votaron lo mismo y ninguno fue refutado en ese punto.

**Nombra algo que este trabajo no hizo.** Replicabilidad es que un estudio
distinto, con datos propios, obtenga un resultado concordante (NASEM 2019:
*«obtaining consistent results across studies aimed at answering the same
scientific question, each of which has obtained its own data»*). Aquí no se
comparó el resultado de ningún estudio con el de otro: no hay estimación
agrupada, no se aplicó GRADE, y el hallazgo central es que **ningún brazo llega
a ser sumando utilizable**.

**No hay una sola frase sobre repetir estudios en los tres manuscritos.** La
única aparición de la raíz «replic-» es **el fago replicándose en su
hospedador**. El título obligaría al lector a desactivar el sentido dominante
de la palabra en el mismo renglón en que dice «fagoterapia».

**No se puede arreglar con ediciones.** Para que el título no mintiera haría
falta añadir al cuerpo al menos dos resultados comparables sobre la misma
pregunta, cada uno con sus datos, y compararlos. Sería otra revisión, no una
edición. Estipular una definición privada en la línea 41 contradiría el uso
consagrado y el primer revisor que abra la sección 3 lo vería.

**«Reproducibilidad» tampoco**, y por una razón propia: la palabra ya está
ocupada dos veces en el texto —la reproducibilidad algorítmica que la
evaluación de sesgo declara **no** tener, y la reproducibilidad del método de
la propia revisión—.

## Por qué «completitud del reporte»

1. **Es la palabra que el trabajo ya usa para lo que mide.** Encabeza los
   resultados («### Completitud del reporte en las variables de
   estratificación»), titula las Tablas 3 y 4, y cierra la conclusión.
2. **Rima con el objetivo del resumen**, literal: «determina si su estructura y
   **reporte** admiten una síntesis cuantitativa de eficacia».
3. **No promete de más.** No promete verdad, ni repetición, ni un efecto
   agrupado. «Verificabilidad de la literatura clínica» se lee a la primera
   como «¿es cierto lo que dicen?», que no es la pregunta.
4. **Es legible sin definición.** «Verificabilidad» solo se sostenía porque la
   línea 41 la definía en el mismo renglón; en un índice esa definición no
   viaja.

## Lo que se pierde, y se pierde a sabiendas

**Cobertura.** El trabajo declara **tres** componentes medidos: recuperabilidad
del informe (§3.1 y §3.2), completitud de reporte estructural (§3.4) y
completitud de reporte de desenlaces (§3.5). El término nuevo nombra dos y deja
fuera el primero —los 60 de 155 estudios sin publicación y los 71 de 95 con
texto obtenido—. Un estudio que nunca publicó no tiene reporte cuya completitud
medir. **Se prefiere un título que dice menos a uno que dice otra cosa.** En el
cuerpo la recuperabilidad se sigue nombrando: se añadió explícitamente a la
pregunta de investigación y a la frase de los tres componentes.

**Una pregunta que el título invita.** Buena parte de la literatura titulada
«reporting completeness» puntúa adherencia a CONSORT, CARE o STROBE, y esta
revisión no aplicó ninguna guía: contó presencia y ausencia. La respuesta se
adelantó en la carta de presentación y en el anexo S0, antes de que la
pregunten.

**Longitud.** +7 caracteres en castellano y +9 en inglés sobre el título de
141/141 de esta mañana. Siguen por debajo de los 162/157 que se recortaron.

## Dónde se aplicó

Fuentes editadas a mano:

- `paper/manuscrito_JSR_final.md` — títulos (1, 3) y pregunta de investigación (41)
- `paper/manuscrito_revision_sistematica.md` — título (1), pregunta (40), frase de componentes (101)
- `paper/manuscript_systematic_review_en.md` — título (1), pregunta (40), frase de componentes (103)
- `paper/manuscrito_JSR_editado.md` — títulos y pregunta (borrador huérfano, al día a propósito)
- `scripts/build_jsr_submission.py` — `titulo_es`, `titulo_en`, y un párrafo nuevo en la carta al Comité que aclara que no se puntuó ninguna guía
- `scripts/build_package_guide.py` — portada de la guía
- `scripts/build_editorial_report.py` — el párrafo de S0, reescrito para narrar los **dos** cambios de título del día con sus longitudes, y la descripción de la opción B
- `scripts/build_synthesis_scalars.py` y `scripts/exclusion_codes.py` — docstring y comentario internos

**No se tocó, a propósito:** el verbo *verificar* del resumen, de resultados y
de la conclusión —es un verbo dentro de una frase, no la etiqueta del
constructo—; la carpeta «verificables revisión sistemática», cuyo nombre viene
de los anexos probatorios y que nombran diez scripts por ruta literal; el acta
anterior del 14 de septiembre y la auditoría archivada del 26 de agosto, que
son registro histórico.

## Comprobado después

Los cuatro comprobadores en verde. El grep de control sobre `paper/` y
`scripts/` deja solo tres apariciones de «verificabilidad», y las tres son la
narración histórica del anexo S0, que cita el término anterior a propósito.

## Pendiente por causa ajena

Word tenía `manuscrito_JSR_final.docx` abierto durante la reconstrucción, de
modo que el sobre quedó con **dos** manuscritos: el bueno es
`manuscrito_JSR_final_NUEVO.docx`. El LEEME del envío lleva ahora un aviso en
cabecera que aparece solo mientras exista ese fichero. Se resuelve cerrando
Word y volviendo a ejecutar `build_jsr_submission.py`.
