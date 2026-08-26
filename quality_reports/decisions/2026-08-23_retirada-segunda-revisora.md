# ⚠️ SUPERADO — N. Trelles se reincorporó el 26 de agosto de 2026

**Este registro describe una situación que duró tres días y ya no rige.** Se
conserva porque el registro es solo-anexar y porque la concordancia que midió es
la del corpus a medio extraer, que hoy sirve de contraste.

Lo que rige desde el 26 de agosto de 2026:

| | entonces | ahora |
|---|---:|---:|
| Estudios extraídos por N.T. | 98 | **122 de 124** |
| Corpus con doble extracción | 79 % | **98 %** |
| Desacuerdos | 724 | **575** |
| Acuerdo mediano | 69 % | **78 %** |
| Kappa mediana | 0,30 | **0,57** |
| Adjudicados | 2 | 2, y el resto ya se puede resolver |

La extracción por duplicado **está completa** y la resolución por consenso vuelve
a ser posible. La autoría de N.T. conforme a ICMJE deja de estar en el aire: ha
vuelto al proyecto y puede aprobar la versión final y responder por el trabajo.

Lo que NO cambia: la decisión de que ninguna cifra publicada dependa de los
cuadernos de extracción sigue en pie, porque las 573 discrepancias que quedan no
están adjudicadas todavía.

---

# Retirada de la segunda revisora: qué pasa con la extracción

**Estado:** ADOPTADA
**Fecha:** 23 de agosto de 2026
**Decide:** D. Valdiviezo
**Afecta a:** Métodos (extracción), Limitaciones, PRISMA ítem 10a, CRediT,
`compare_extractions.py`, `merge_adjudications.py`

## Qué ha pasado

N. Trelles se retiró del proyecto el 22 de agosto de 2026, antes de que se
celebrara ninguna reunión de consenso. No la habrá.

## Qué había extraído cada uno

| | Estudios | Celdas con dato |
|---|---:|---:|
| D. Valdiviezo | **124 de 124** | 2 698 |
| N. Trelles | 98 | 1 622 |

La extracción de D.V. está completa al 100 % en los trece campos nucleares
(`pathogen_scope`, `resistance_class`, `dtr_status`, `route`, `modality`,
`study_design`, `n_arm`, `clinical_success_n`, `microbio_eradication_n`,
`mortality_n`, `adverse_event_n`, `publication_year`, `extraction_status`) para
los 124 estudios. Los 98 estudios de N.T. son todos subconjunto de los de D.V.:
no aportó ninguno que él no tuviera.

## Qué se decide

1. **La extracción de registro es la de D. Valdiviezo.** Está completa y es de
   un solo extractor. Se declara así, sin rodeos, en Métodos y en el ítem 10a
   de PRISMA.

2. **La extracción de N.T. no se descarta: se convierte en submuestra de
   fiabilidad.** 98 de los 124 estudios (79 %) fueron extraídos por dos
   revisores de forma independiente. Eso permite *medir* el error del extractor
   único en vez de solo advertir de él, que es más de lo que reporta la mayoría
   de revisiones de un solo revisor.

3. **No se adjudica nada por consenso, porque no hay con quién.** De los 724
   desacuerdos reales, 2 están firmados y 722 no. No se van a firmar. Cualquier
   frase que diga o insinúe que los desacuerdos se resolvieron por consenso
   entre los revisores tiene que caer.

4. **El fichero de registro de N.T. es su cuaderno tal como lo entregó**, sin
   mezclar. Entregó dos versiones (98 estudios y 80); el consolidado que unía
   ambas se conserva como `consolidado_dos_pasadas_SIN_ADJUDICAR.xlsx` pero no
   es el de registro: su regla «gana la más reciente» no la firmó nadie, y se
   construyó para la reunión que ya no va a existir.

   Se toma la versión de 98 estudios, que es la más completa **y la que menos
   favorece**: concuerda con D.V. un 65,9 % en campos puntuables, frente al
   89,5 % de la versión de 80. Cuando no puedes establecer cuál es la definitiva,
   quedarte con la que te favorece es maquillar.

## Lo que mide la submuestra

Sobre 128 filas de brazo comparables:

| | |
|---|---:|
| Desacuerdos reales | 724 |
| Acuerdo mediano | 69 % |
| Kappa mediana (7 de 9 categóricos informativos) | 0,30 |

Por variable, el acuerdo va del 38 % (`route`) al 95 % (`publication_year`,
`los_days`, `resistance_class_source`).

**Estas cifras sustituyen a unas anteriores que estaban mal.** El comparador
contaba como desacuerdo toda celda que un revisor hubiera rellenado y el otro
no. Como D.V. iba muy por delante, su ventaja se estaba midiendo como
discordancia: 1 063 de los 1 788 «conflictos» (60 %) eran celdas que N.T. no
había tocado. Corregido en `ca12d6a`. La prueba de que el arreglo es correcto
está en `publication_year`, que es un dato objetivo y pasó del 62 % al 95 %.

## Qué NO cambia

Ninguna cifra publicada. `build_synthesis_scalars.py` no lee ninguno de los dos
cuadernos de extracción: lee `revision_sistematica/cribado/*` y
`pre_extraccion_desde_resumen.csv`. Las tablas 1 a 4, la figura PRISMA y todo
escalar del manuscrito salen del cribado y de la pre-extracción desde
resúmenes. La retirada afecta a cómo se describe el método, no a los resultados.

## Cómo hay que leer una kappa de 0,30

Con honestidad y sin estirarla en ninguna de las dos direcciones.

No es buena. Pero no se puede repartir la culpa entre las cuatro causas
plausibles —informes primarios mal reportados, formulario ambiguo, distinta
experiencia de los revisores, o una de las dos pasadas anterior a la regla
corregida de erradicación— porque la revisora se fue antes de que se pudiera
preguntar. Decir que la baja concordancia *demuestra* que esta literatura está
mal reportada sería usarla como argumento cuando es solo compatible con él.

Lo que sí se puede afirmar: dos lectores entrenados, con el mismo formulario y
los mismos informes, coincidieron en cerca de dos tercios de los campos
puntuables. Eso se reporta tal cual, en Limitaciones, y el lector juzga.

## Lo que queda en manos de D. Valdiviezo, y no puede decidirse por él

**La autoría de N. Trelles según ICMJE.** Contribuyó de forma sustancial a la
adquisición de datos (98 estudios extraídos de forma independiente), lo que
cubre el primer criterio. Los otros tres —redacción o revisión crítica,
aprobación de la versión final, y acuerdo de responder por el trabajo— exigen
actos suyos que solo ella puede realizar, y se ha retirado.

No se puede incluir a alguien como autor si no aprueba la versión final. Tampoco
se le puede borrar el trabajo. Las dos salidas habituales son ofrecerle la
autoría por escrito con un plazo, o reconocerla en agradecimientos detallando lo
que hizo. Decidir eso, y contactarla, es de D.V.

Hasta que lo decida, `CRediT` queda con la contribución de N.T. descrita por lo
que consta que hizo, sin firmar.
