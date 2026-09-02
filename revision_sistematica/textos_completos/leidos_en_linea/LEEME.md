# Intento de recuperación de los textos que faltan — 1 y 2 de septiembre de 2026

## Lo que se consiguió

- **EST-177** (ECA, *Otolaryngologia Polska*). Texto completo íntegro, en la
  **versión inglesa del propio editor**, acceso abierto. Ficha en `EST-177.md`.
  **Falla la población**: 40 pacientes con rinosinusitis crónica con pólipos;
  *P. aeruginosa* aparece solo en el espectro del gel «Otophag».

- **EST-205** (*Revista Cubana de Angiología y Cirugía Vascular*). No se pudo
  leer —`scielo.sld.cu` no resuelve ni desde el canal ni desde el navegador—
  pero **SciELO lo indexa como «Tipo de literatura: Editorial», «No citable»**,
  dos páginas (137-138) y un solo autor. Un editorial no aporta datos primarios:
  candidato a exclusión **REV**, pendiente de poder abrirlo.

- **EST-059** (*Infektsionnye Bolezni*). El depósito en Zenodo (CC-BY) existe y
  se descargó, pero son **4 369 caracteres**: metadatos y el resumen bilingüe,
  sin introducción, materiales, discusión ni referencias. **No es texto
  completo**; está en `../resumen_extendido/`, no en `../pdf/`.

## Lo que NO se consiguió, y por qué

**No hay acceso institucional en el navegador.** Comprobado sobre el ECA de más
valor (EST-118, *Lancet Infectious Diseases*): la página ofrece «Get Access»,
«Log in» y «Request your institutional access to this journal». Lo mismo en
Oxford Academic. Sin sesión de la universidad, el navegador no añade nada al
canal, y **iniciar sesión no es algo que este asistente pueda ni deba hacer**.

Probados y cerrados sin sesión institucional:

| editor | estudios | resultado |
|---|---|---|
| Elsevier / Lancet | EST-029, EST-118, EST-028, EST-064, EST-065, EST-098, EST-140 | redirección a `linkinghub`, de pago |
| SAGE | EST-073, EST-157, EST-165, EST-167 | HTTP 403 |
| Springer | EST-005, EST-110 | la URL de PDF devuelve la página de compra |
| Oxford Academic | EST-032 | «Get access»; el PDF directo da 403 |

Y antes de esto, Europe PMC ya decía que **0 de los 27 tienen vía libre hoy**
(`../disponibilidad_hoy.csv`).

## Lo único que queda

**Préstamo interbibliotecario o acceso institucional de la universidad.** El
barrido rescató **24 PMID** que el registro no tenía: con un PMID el
bibliotecario localiza el artículo al instante, así que la petición sale mucho
mejor armada que antes.

## Segunda pasada, 2 de septiembre: OpenAlex y repositorios

Europe PMC solo ve lo que indexa. Se consultó además **OpenAlex**, que agrega
copias de repositorios institucionales, para los 21 que tienen DOI o PMID.

**Resultado: una sola copia abierta y una sola en repositorio.**

- **EST-032** figura como acceso abierto híbrido, y su URL de PDF es la misma
  que ya dio 403. Comprobado también en el navegador: **Oxford Academic redirige
  ese PDF al resumen** y pide «Obtén acceso». Está declarado abierto y servido
  como cerrado; la discrepancia es del editor, no del registro.

- **EST-118** —el ECA intravesical, de los más valiosos— **tiene copia en el
  Zurich Open Repository**. La URL correcta es la canónica,
  <https://www.zora.uzh.ch/id/eprint/193520/>, confirmada de forma
  independiente por **OpenAIRE**; la forma corta que da OpenAlex
  (`/193520`) devuelve 404 tras pasar la barrera.

  **Ojo con lo que hay detrás:** OpenAlex la marca `version=submittedVersion`,
  es decir el **manuscrito enviado**, previo a revisión por pares. No es el
  artículo publicado en *Lancet Infectious Diseases*, y para extraer
  desenlaces esa diferencia importa: hay que declarar qué versión se leyó. No se
  descargó: el repositorio está protegido por **Anubis**, una barrera anti-bots
  que la propia página declara puesta «contra el rastreo agresivo por parte de
  empresas de IA». Sortearla no procede. **Ábrela tú en el navegador**: es un
  clic y la barrera se resuelve sola para una persona.

Los otros 19 solo tienen ficha en PubMed, que es metadatos, no texto.

## Estado final de la recuperación

| vía | resultado |
|---|---|
| Europe PMC | 0 de 27 con acceso libre |
| OpenAlex (copias abiertas) | 1, y el editor la sirve cerrada |
| Repositorios institucionales | 1 (EST-118, tras barrera anti-bots) |
| Editores, sin sesión institucional | 0 |
| Sin DOI ni PMID | 5 estudios, no consultables por identificador |

**Conseguidos en total: EST-177** (íntegro) y **EST-207** (que bajó D.V. por su
DOI). **EST-205** identificado como editorial pero ilegible desde aquí.

## Lo que queda, por orden de coste

1. **EST-118**: abrir la ficha de ZORA a mano. Un clic.
2. **Sesión institucional de la universidad** en el navegador: abriría de golpe
   los 14 de Elsevier, SAGE, Springer y OUP.
3. **Préstamo interbibliotecario** para el resto, ahora con los 24 PMID
   recuperados: con un PMID el bibliotecario localiza el artículo al instante.
