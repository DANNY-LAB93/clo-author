# El título pierde «estructura» y gana la fórmula de la revista

**Fecha:** 2026-09-14
**Decide:** D. Valdiviezo
**Estado:** APLICADO

## Qué cambia

**Antes** (162 caracteres):

> Fagoterapia en infecciones por *Pseudomonas aeruginosa* multirresistente: revisión sistemática de **la estructura y la verificabilidad del cuerpo de evidencia clínica**

**Ahora** (141 caracteres):

> Fagoterapia en infecciones por *Pseudomonas aeruginosa* multirresistente: revisión sistemática de **la literatura clínica y de su verificabilidad**

**Inglés**, de 157 a 141 caracteres:

> Phage therapy for multidrug-resistant *Pseudomonas aeruginosa* infections: a systematic review of **the clinical literature and its verifiability**

## De dónde sale

D. Valdiviezo propuso el 14 de septiembre dos cambios a la vez: escribir
«multidrogorresistente» en lugar de «multirresistente», y sustituir «de la
estructura y la verificabilidad» por «de la literatura y verificabilidad». Se
sometieron a un concejo de quince evaluadores —cuatro pesquisas sobre los
ficheros, cinco dictámenes con lentes distintas, un escéptico por dictamen y un
acta final—.

**El término se rechazó.** En el corpus del propio proyecto la familia
«multirresist\*» aparece en 17 artículos y la familia «multidrogo-» en 2, que
son el mismo artículo boliviano indexado dos veces y que escribe el término de
cuatro maneras distintas entre su título, su resumen y sus palabras clave. Pesa
más la coherencia interna: el cuerpo del manuscrito define la categoría en las
líneas 37 y 96, y esta última se regenera desde `build_criteria_table.py`.
Cambiar solo el título dejaría el artículo nombrando la misma categoría de
cuatro formas, en un trabajo cuyo argumento es que la evidencia no se puede
verificar porque no dice las cosas de forma comprobable.

**El alcance se rechazó tal como venía redactado, y se adoptó una tercera
forma.** «y verificabilidad» sin artículo queda coja; la redacción propuesta no
acortaba (164 caracteres contra 162); y el reparo de longitud era del propio
proyecto, que lo imprimía dentro del anexo S0 que viaja a la revista. La forma
adoptada resuelve las tres cosas.

## Lo que se pierde, y es una pérdida consciente

«Estructura» es el sustantivo de la pregunta de investigación: *«¿posee el
cuerpo de evidencia sobre fagoterapia en P. aeruginosa resistente la estructura
y la verificabilidad […] que una estimación agrupada exige?»*. El título nombra
ahora **una** de las dos propiedades.

**La pregunta de investigación no se tocó**, ni el objetivo del resumen, ni el
resumen estructurado. Siguen diciendo las dos. El título es más corto que su
propio objeto, y eso se acepta.

Segunda pérdida, menor pero real: **«literatura» no cubre los registros de
ensayo**, y más de uno de cada tres estudios identificados existe únicamente
como registro, sin resultados publicados. «Cuerpo de evidencia» sí los cubría.

## Lo que se gana

- **21 caracteres menos**, que era el reparo que el propio proyecto tenía
  anotado desde antes.
- Se conserva **«verificabilidad»**, el término que distingue este trabajo de
  las revisiones que agregan desenlaces: en los 17 129 títulos del corpus,
  «estructur\*» aparece 341 veces y «verificab\*» ninguna.
- Se adopta la fórmula **«revisión sistemática de la literatura»**, que es la
  que usa el artículo de JSR tomado como modelo (Torres Vinueza y Prieto
  Fuenmayor, Vol. 9 N.º 2, 2024). **Las normas de la revista no se han leído**:
  esto es un precedente observado en un artículo, no una norma verificada.

## Argumentos que NO sostienen esta decisión

El contraste del concejo refutó cuatro de los cinco dictámenes. Quedan aquí
tachados para que nadie los reutilice:

- «droga significa estupefaciente» — falso; el DLE lo recoge en primera acepción
  como sustancia de uso en medicina;
- «Fundéu proscribe multidrogorresistente» — la recomendación es ortográfica y
  ni lo menciona;
- «el título colisiona con las revisiones (6) y (7)» — están en inglés y
  ninguna lleva *Pseudomonas* en el título;
- «es un zeugma» — norma inventada;
- «el guion de priorización obliga al término» — `prioritise_stage2.py` ordena
  la lectura, no filtra, y lo declara en su cabecera.

## Dónde se aplicó

Fuentes (se editan a mano):

- `paper/manuscrito_JSR_final.md` líneas 1 y 3
- `paper/manuscrito_revision_sistematica.md` línea 1
- `paper/manuscript_systematic_review_en.md` línea 1
- `paper/manuscrito_JSR_editado.md` líneas 1 y 3 (borrador huérfano, se
  mantiene al día para que no quede una cuarta copia divergiendo)
- `scripts/build_jsr_submission.py`, claves `titulo_es` y `titulo_en`
- `scripts/build_package_guide.py`, portada de la guía
- `scripts/build_editorial_report.py`, la observación que pedía acortarlo, hoy
  reescrita para decir que se acortó y qué se perdió

No se tocaron, a propósito: la pregunta de investigación y el objetivo del
resumen; `build_structured_abstract.py`; las formas cortas del título, que no
llevaban «estructura» (`LEEME_RESPALDO.md`, subtítulo de S1, cabecera del
informe extendido); `prioritise_stage2.py`; y la copia archivada de la
auditoría del 26 de agosto.

Regenerados después: los dos PDF del manuscrito y sus copias en el paquete, los
dos `.docx` de manuscrito, S0, S1, S2, el índice, la guía, el informe extendido,
y en el sobre el manuscrito y la carta de presentación.

## Comprobado después

Los cuatro comprobadores en verde: 102 afirmaciones ancladas al día, la
aritmética recalculada desde el texto, ninguna cifra sin origen, 0 fallos de
coherencia del canal. El binomio va en cursiva en el título del manuscrito y en
el de la carta.
