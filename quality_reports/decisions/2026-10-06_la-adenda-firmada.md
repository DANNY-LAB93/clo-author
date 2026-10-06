# La adenda firmada: EST-132 sale y EST-106 se queda

**Estado:** APLICADO el 6 de octubre de 2026.
**Viene de:** `2026-10-03_las-decisiones-firmadas-sobre-la-lectura.md`. Las dos
decisiones que el 3 de octubre solo tenían la respuesta de D. Valdiviezo se
firmaron en `FIRMAR_adenda_lectura_2026-10-03.xlsx` por DANNY JAVIER VALDIVIEZO
VERDUGO y NATALY ELIZABETH TRELLES AVILA, fecha 2026-10-03, lectura SI. Copia
intacta en `revision_sistematica/lectura_pendiente/FIRMAR_adenda_lectura_2026-10-03_firmado.xlsx`.

## Lo que se aplicó

- **EST-132 sale con ORG.** Motivo firmado: «no separa pacientes con Pseudomonas».
  El artículo solo nombra *P. aeruginosa* en la composición del cóctel empírico.
  Era un ECA con grupo de comparación y evaluado con RoB 2.
- **EST-106 se mantiene y se declara**, como los otros cinco estudios de un solo
  brazo por debajo del umbral. Ya no queda ninguno sin decisión.

Corpus: 132 → **131 estudios**, 89 extraíbles, 65 con texto (73,0 %), 97 brazos.
Riesgo de sesgo: 12 comparativos, **9 evaluables**, 68 celdas, **3 con grupo de
comparación** (EST-008, EST-021, EST-108), 2 de fago frente a no fago y los 2 con
contraste para *P. aeruginosa*. Concordancia: 49 de 60 (81,7 %), kappa 0,74; EST-132
no tenía desacuerdos, así que los 11 siguen.

## Lo que hubo que tocar en el canal

- `ingest_firma_lectura.py` solo aceptaba la firma corta; la adenda se firmó con
  el nombre completo. Ahora acepta las dos formas, una por autor.
- La frase generada del contraste acababa en «parcial): .» si ningún estudio de
  fago frente a no fago se queda sin contraste. Corregida, y en inglés «both».
- **La procedencia geográfica del maestro y del inglés venía de un corpus
  anterior** («Rusia (7)… Irán… No consta en 76»), y el reparto por país del de la
  revista también estaba viejo; solo su «No consta en N de los M» estaba anclado.
  Ahora la escribe `escribe_procedencia.py` desde los datos en los tres.
- Dos cifras más pasaban por coincidencia: «79 brazos legibles» (son 73) en el de
  la revista y «48 estudios que declaran origen, 21 de Europa del Este» (34 y 13)
  en el inglés. Ancladas.

Anclas: 301, todas al día. 17 de 17 cifras auditadas se reproducen.
