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
