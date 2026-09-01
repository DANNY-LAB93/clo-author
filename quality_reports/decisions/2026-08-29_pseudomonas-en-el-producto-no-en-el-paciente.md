# *P. aeruginosa* en la etiqueta del fago, no en el paciente

**Estado:** INFORME — la decisión de exclusión es de los dos revisores
**Fecha:** 29 de agosto de 2026

Al comprobar contra los PDF los estudios de profilaxis apareció un patrón, y se
barrieron los 124 estudios extraídos buscándolo: artículos donde
*P. aeruginosa* aparece en el **espectro del producto**, en la **introducción**
o en la **bibliografía**, pero **no en ningún paciente**.

## Los diez confirmados, leídos uno a uno

| estudio | qué son los pacientes | dónde aparece *P. aeruginosa* |
|---|---|---|
| **EST-076** | 10 artroplastias infectadas | **en ningún sitio**. Palabras clave: «periprosthetic joint infections; *Staphylococcus*» |
| **EST-178** | rinosinusitis aguda, fago polivalente | **en ningún sitio**, en 22 710 caracteres. Ni «Pseudomon», ni «pyocyaneus», ni cirílico |
| **EST-083** | — | solo en la **introducción**: «MRSA and MDR-PA present a significant health threat» |
| **EST-126** | 212 niños con amigdalitis aguda | **etiqueta del piobacteriófago** («the drug is recommended for use in treating…») y una referencia |
| **EST-130** | — | solo en la **lista de referencias** |
| **EST-131** | — | solo en la **lista de referencias**, sus tres menciones |
| **EST-159** | — | **espectro del cóctel SniPha 360** |
| **EST-212** | — | espectro de SniPha 360; y el artículo dice «microbiological analysis of intraoperative samples confirmed infection with ***Staphylococcus aureus* and *Proteus mirabilis***» |
| **EST-086** | 60 pacientes de COVID-19 | **cepa de referencia ATCC 27853** usada para fabricar el cóctel |
| **EST-101** | niños ventilados; los criterios «excluded children with bacterial pneumonia» | cultivos **negativos** |

## Dos que el barrido marcó y NO lo son

La heurística usaba una ventana de ±130 caracteres alrededor de «aeruginosa» y
buscaba la palabra «patient» o «culture». Falla cuando el artículo lo dice de
otra manera:

- **EST-135**: «a bacterial culture of the hematoma revealed **superinfection
  with *Pseudomonas aeruginosa***, *Achromobacter* spp., and *Proteus
  mirabilis*». El paciente lo tenía. **Legítimo.**
- **EST-184**: «wound cultures grew polymicrobial organisms, including
  **carbapenem-resistant *Pseudomonas aeruginosa***». **Legítimo.**

## Lo que este barrido NO cubre

Solo mira estudios con **tres menciones o menos**. EST-086 y EST-101, que
también fallan, tienen muchas menciones y los cazó otra comprobación. **Diez es
un suelo, no un total**: puede haber estudios con muchas menciones donde todas
sean de fondo, y este barrido no los ve.

Tampoco cubre EST-207, cuyo PDF es de otro artículo.

## Por qué pasó, y por qué importa

Tiene una explicación mecánica y no es un descuido de nadie. El cribado de
títulos y resúmenes lo emitió un modelo de lenguaje como revisor único, y un
resumen que dice «piobacteriófago polivalente activo frente a *S. aureus*,
*E. coli*, *P. aeruginosa*…» **parece** elegible: el patógeno está ahí, en el
texto. Distinguir el espectro de un producto de la etiología de un paciente
exige leer el artículo, no el resumen.

Esto es lo que §2.4 declara en abstracto —«los registros que el modelo excluyó
no los releyó ningún humano»— y aquí se ve el otro lado: lo que el modelo
**incluyó** de más. Es un ejemplo medido, no una advertencia genérica, y merece
entrar en las limitaciones con su cifra.

Dos de los diez usan el mismo producto comercial, **SniPha 360**, cuyo
prospecto enumera *P. aeruginosa*. Es un modo de fallo reconocible y
buscable.

## Qué hay que decidir

Excluir estos estudios cambiaría los 184, los 124 y el diagrama PRISMA. Es una
decisión de cribado de D. Valdiviezo y N. Trelles, no de un script. Lo que sí
puede afirmarse ya, y con estas diez pruebas delante, es que el corpus contiene
estudios cuya población no cumple §2.2.
