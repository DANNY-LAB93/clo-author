# Verificación contra los PDF: qué aguanta y qué no

**Estado:** INFORME — tres decisiones quedan en manos de los dos revisores
**Fecha:** 29 de agosto de 2026
**Motivo:** D. Valdiviezo pidió comprobar contra los artículos, y no contra las
notas de extracción, si los 3 estudios de profilaxis lo son y si los 22 brazos
de verdad no separan *P. aeruginosa*. Los 25 tienen texto completo.

---

## Los 3 de «profilaxis»: son 2, no 3

| | veredicto | prueba en el artículo |
|---|---|---|
| **EST-101** | **profilaxis CONFIRMADA, y peor** | «a phage cocktail **as a preventive measure** against VAP». Los criterios de inclusión «**excluded newborns and children with bacterial pneumonia**», y «the cultures of specific bacterial strains **did not yield positive results**». Los pacientes no tenían infección: falla la POBLACIÓN de §2.2, no solo la intervención. |
| **EST-086** | **profilaxis CONFIRMADA** | 60 pacientes de COVID-19, no seleccionados por tener infección por *P. aeruginosa*. Sus diez menciones del patógeno son de la **fabricación del cóctel**: cepa de referencia **ATCC 27853**, test de Kirby-Bauer. Ningún desenlace de paciente es atribuible a *P. aeruginosa*. |
| **EST-039** | **REFUTADA** | El título dice «for the Prevention of Recurrent Nosocomial Pneumonia», pero su resumen declara «the **elimination of multidrug-resistant microorganisms** from the bronchoalveolar lavage contents was detected in all patients», con caída de PCR y procalcitonina. Esos pacientes tenían el organismo. Es tratamiento. |

**El filtro que yo había puesto buscaba «prevent» en el título y se equivocaba.**
Sustituido por la lista de los dos comprobados en el texto completo.

## Los 22 que «no separan»: la nota no es uniformemente exacta

- **EST-091 SÍ separa.** Su tabla da el patógeno paciente a paciente
  («5 M 21 P.aeruginosa», «10 F 64 P.aeruginosa»). La nota es incorrecta ahí.
- **EST-034** separa las *solicitudes* por patógeno (92 de 644 para
  *P. aeruginosa*) pero no los desenlaces: la nota vale para lo que importa.
- **EST-146**, el único de los tres finalistas al que afecta: el artículo **sí**
  dice qué paciente tuvo qué organismo. Lo que ocurre es distinto y más
  concreto: son 12 casos «for a diverse range of bacterial infections», el
  **7/12 que se extrajo es la serie entera**, y el subgrupo de *P. aeruginosa*
  es **un paciente**. El numerador no es una proporción de *P. aeruginosa*.

No se verificaron uno a uno los 19 restantes. El filtro del embudo ya no usa la
nota: usa la lista de estudios comprobados.

---

## TRES PROBLEMAS DE CORPUS, y son vuestros

Aparecieron al abrir los ficheros y no los resuelve un script.

### 1. EST-207 tiene el PDF equivocado

Debería ser «Successful bacteriophage treatment of infection involving cardiac
implantable electronic device and aortic graft: a Trojan horse concept»
(*Europace*). El fichero guardado es **otro artículo de la misma revista**: una
página de bibliografía de «The SPRM in Japanese HF patients», cardiología. Hay
que volver a descargarlo.

### 2. EST-076 no menciona *Pseudomonas* ni una vez

«Experience Using Adjuvant Bacteriophage Therapy for the Treatment of 10
Recalcitrant Periprosthetic Joint Infections» (*Clin Infect Dis*). El PDF es el
correcto y sus palabras clave son «periprosthetic joint infections;
**Staphylococcus**; intraarticular». Cero menciones de *Pseudomonas* en cuatro
páginas. **No debería estar en una revisión sobre *P. aeruginosa*.**

### 3. EST-126 es un PDF escaneado sin texto extraíble

«Application of bacteriophage therapy in the treatment of children with acute
tonsillitis». Siete páginas, 16 MB, ni un carácter recuperable. La extracción de
ese estudio no pudo hacerse leyendo el fichero.

---

## Lo que NO cambia

El embudo sigue en **cero**. EST-039 nunca llegó a los tres finalistas, así que
el error del filtro no movía el resultado; y la exclusión de EST-146 se sostiene
sobre una razón mejor que la que se dio. Pero los filtros ahora citan lo que se
leyó en el artículo, no una expresión regular sobre el título ni una nota.

## Lo que hay que decidir

1. ¿Salen EST-101 y EST-086 del corpus? Su población no es la de §2.2.
2. ¿Sale EST-076? No hay *P. aeruginosa* en el artículo.
3. Recuperar el PDF correcto de EST-207.
4. ¿Qué se hace con EST-126, ilegible por máquina?

Las cuatro cambian los 184 estudios y el diagrama PRISMA. Son decisiones de
cribado de los dos revisores.
