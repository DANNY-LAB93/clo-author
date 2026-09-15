# 29 fichas de registro no decían qué organismo se trata, y diez de ellas no cumplen

**Estado:** MEDIDO el 14 de septiembre de 2026. **NO aplicado.** Espera la firma
de los dos revisores.
**Ficheros:** `scripts/fetch_registros.py`, `scripts/verifica_organismo_registros.py`,
`quality_reports/registros_sin_organismo.json`,
`quality_reports/registros_organismo_verificado.csv`,
`revision_sistematica/textos_completos/registros/` (29 fichas completas),
`~/Escritorio/FIRMAR_organismo_de_los_registros.xlsx`

## Qué se encontró

Al comprobar EST-204 contra ClinicalTrials.gov —una sola ficha, por curiosidad—
resultó que NCT00937274 es *«Randomized, Double Blind Placebo-controlled Studies
to Evaluate the Effect of an Orally-fed Escherichia Coli (E. Coli) Phage in the
Management of ETEC and EPEC Induced Diarrhea in Children»*: un ensayo de fago
contra *E. coli* en niños con diarrea en Bangladesh, patrocinado por Nestlé.
Ni una palabra de *P. aeruginosa*.

Sobrevivió al cribado porque su registro exportado **solo tenía título**:
`has_abstract = 0`, `has_mesh = 0`. El cribador —el modelo, como revisor único—
vio «Antibacterial Treatment Against Diarrhea in Oral Rehydration Solution» y
un término de fago, y no tenía con qué descartarlo.

Eso obligaba a preguntar cuántas más hay así. **29 de los 155 estudios del
corpus son fichas de registro cuyo título, resumen y MeSH no permiten saber el
organismo** (`registros_sin_organismo.json`). De los 60 estudios que son solo
ficha de registro, casi la mitad.

## Qué se hizo

Se bajó **la ficha entera de las 29**, y quedaron en disco:

- 25 de ClinicalTrials.gov, API v2, en `textos_completos/registros/<NCT>.json`
- 4 del registro europeo CTIS, API pública, en `.../CTIS_<id>.json`
  (EST-138, EST-186, EST-187 y EST-191 no tienen NCT: su identificador en el
  corpus es un resto del título, `T:phage4cure001…`)

Se leyeron **una por una**, no con un grep. La diferencia importa: el filtro
automático dice que 13 de las 29 no nombran *Pseudomonas* en ninguna parte de
su ficha, y eso ni acierta ni falla del todo. Por un lado, EST-072 **sí** nombra
*P. aeruginosa* —y aun así no cumple: la menciona al describir las colecciones
de fagos de la empresa, mientras su criterio de inclusión exige *«Monobacterial
Infection due to S. aureus»*. Por otro, EST-203 y EST-141 nombran *P. aeruginosa*
solo dentro del espectro lítico del preparado, no como el organismo del paciente.

`verifica_organismo_registros.py` no redacta ninguna evidencia: por cada estudio
se declara **en qué campo de la ficha** está lo que sostiene la lectura, y el
script **extrae la frase literal del JSON**. Si la frase no está donde se dice
que está, aborta sin escribir nada.

## Lo que salió

| Veredicto | N | Qué significa |
|---|---|---|
| CUMPLE | 12 | la ficha nombra *P. aeruginosa* entre los organismos de la población que va a tratar |
| NO CUMPLE | 10 | la ficha exige otro organismo (ORG, 8) o incumple otro criterio (OFF, 2) |
| INDETERMINADO | 7 | la ficha no permite saberlo |

**Los ocho ORG**, con lo que dice su propia ficha:

| Estudio | Registro | Lo que exige |
|---|---|---|
| EST-072 | NCT06605651 | «Monobacterial Infection due to S. aureus» |
| EST-138 | CTIS 2022-500541-24-00 | úlceras de pie diabético «infected by Staphylococcus aureus» |
| EST-150 | NCT06827041 | *S. epidermidis* multirresistente, N-of-1, un solo paciente |
| EST-182 | NCT06938867 | *E. coli* resistente a fluoroquinolonas, pretrasplante |
| EST-204 | NCT00937274 | *E. coli* ETEC/EPEC, diarrea infantil |
| EST-210 | NCT05277350 | **sujetos sanos** con «E. coli present in feces sample» |
| EST-216 | NCT05967130 | ITU por enterobacterias BLEE en trasplante renal |
| EST-218 | NCT07076238 | micobacterias no tuberculosas |

**Los dos OFF** no fallan por organismo sino por diseño: EST-211 (NCT05618418,
BATTLE) es observacional y su intervención registrada es literalmente «No
intervention» —correlaciona bacterias con supervivencia en hepatitis alcohólica,
no administra fagos—; EST-213 (NCT05314426) es un **biobanco**, sin intervención
y sin desenlace.

**Los siete INDETERMINADO** son el hallazgo que más le importa a este artículo,
porque son exactamente lo que el título promete medir: EST-087 (cohorte
PHAGEinLYON, «severe infection treated with bacteriophage»), EST-141 (amigdalitis
aguda en niños, sin criterio microbiológico), EST-148 (ITU recurrente, un solo
paciente), EST-192 (prevención de neumonía asociada a ventilación), EST-203
(úlceras venosas, WPP-201), EST-209 y EST-214 (las dos cohortes de seguridad de
Lyon). Sus fichas no dicen qué bacteria se trató. **La propuesta no es
excluirlos: es dejarlos y declarar que el registro no permite verificarlo.**

Aparte, EST-186 y EST-187 son **el mismo ensayo** (Phage4Cure-001) con dos
identificadores CTIS. Los dos cumplen el criterio del organismo; lo que hay que
decidir es si uno de los dos es un informe más y no un estudio nuevo.

## Qué NO se hizo, y por qué

**No se tocó el corpus.** Sigue en 155 estudios. Excluir diez mueve el total,
el diagrama PRISMA, la Tabla 4 de exclusiones y todos los porcentajes calculados
sobre el total — cifras que ya están escritas en el manuscrito. Eso no lo firma
un script.

El cuaderno `FIRMAR_organismo_de_los_registros.xlsx` lleva, por estudio, la
propuesta, el campo de la ficha y la frase literal, un desplegable para
confirmarla o cambiarla, y una hoja de firma. Cuando estén las dos firmas se
ingiere, se vuelve a correr el canal entero y se rehacen los tres guardianes.

## Lo que esto dice del cribado

No es un fallo de ejecución: es el límite declarado del método. El cribado lo
condujo un revisor único y las decisiones registro a registro las emitió el
modelo; **los registros que excluyó no los releyó ningún humano**. Aquí se ve el
otro lado del mismo hecho: una ficha con solo título no da con qué excluir, y
entra. La validación de falsos negativos (0 de 350, IC 95 % 0,00–1,05 %) medía
lo que salió de más, no lo que entró de más.

Diez estudios que no cumplen sobre 155 es un **6,5 % de falsos positivos**, todos
concentrados en el estrato de fichas de registro. Se reporte o no como exclusión,
eso se declara en el manuscrito.
