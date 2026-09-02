# Este repositorio es PRIVADO, y tiene que seguir siéndolo

**No lo hagas público.** Contiene **106 artículos científicos en PDF**
(`revision_sistematica/textos_completos/pdf/`) descargados bajo suscripción
institucional o licencia de lectura. Tenerlos aquí para trabajar es un uso
normal; publicarlos sería redistribuirlos, y eso no lo permite la licencia de
la mayoría de esas revistas.

Hay un fork **público** del proyecto en `DANNY-LAB93/clo-author`, que es la
plantilla de la que salió el andamiaje. **La tesis nunca se ha subido ahí y no
debe subirse**: comprobado el 1 de septiembre de 2026, no contiene ninguno de
los PDF.

## Qué es esto

El respaldo completo de la revisión sistemática *Fagoterapia en infecciones por
Pseudomonas aeruginosa multirresistente*, de D. Valdiviezo y N. Trelles
(Universidad Católica de Cuenca).

Lleva todo lo que hace falta para reconstruir el trabajo desde cero:

- el manuscrito en español y en inglés, y los PDF maquetados;
- el canal completo en `scripts/`, que recalcula cada cifra del manuscrito;
- las búsquedas, el cribado, los textos completos y las dos extracciones;
- las actas de decisión en `quality_reports/decisions/`, que son el porqué de
  cada cosa;
- el paquete de anexos S0–S16 listo para enviar.

## Cómo volver a levantarlo

```bash
git clone https://github.com/DANNY-LAB93/tesis-fagoterapia-pseudomonas.git
cd tesis-fagoterapia-pseudomonas
python scripts/build_synthesis_scalars.py     # primero: todo lo demás lo lee
python scripts/build_manuscript_tables.py
python scripts/build_manuscript_figures.py
python scripts/check_manuscript_claims.py     # comprueba que ninguna cifra miente
```

`CLAUDE.md` explica el orden y el estado del proyecto.

## Lo único que no cabe entero

`revision_sistematica/busqueda/scopus_armB.csv` son 174 MB y GitHub corta en
100, así que viaja comprimido como `scopus_armB.csv.gz`. Para usarlo:

```bash
gunzip -k revision_sistematica/busqueda/scopus_armB.csv.gz
```

Es un export de Scopus y **no se regenera solo**: hace falta acceso a Scopus
para volver a obtenerlo, así que conviene no perderlo.
