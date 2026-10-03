# La lectura firmada del 30 de septiembre

**Estado:** APLICADO el 1 de octubre de 2026 en todo lo que la lectura deja
inequívoco. Lo que deja abierto está en `~/Desktop/FIRMAR_lectura_2026-10-01.xlsx`,
sin firmar.
**Viene de:** los puntos 2, 7 y 15 del encargo de corrección integral del
2026-09-23, que no se podían cumplir sin leer artículos. `build_trabajo_pendiente.py`
escribió los listados; los dos autores los devolvieron rellenos y firmados
(«DANNY VALDIVIEZO/ NATALY TRELLES», 2026-09-30).
**Ficheros:** `revision_sistematica/lectura_pendiente/` (copia intacta del cuaderno
y los tres CSV firmados), `scripts/ingest_lectura_firmada.py`,
`scripts/comprueba_citas_lectura.py`, `scripts/make_firma_lectura.py` (nuevos);
`correcciones_tras_texto_completo.csv` (+35 filas), `audita_pendientes.py`,
`build_auditoria_scalars.py`, `build_rob_table.py`, `rob_bloques.py`,
`check_manuscript_claims.py`, `sync_manuscript_numbers.py`,
`build_verifiables_package.py`, `build_lista_anexos.py`, `build_package_guide.py`,
`build_readable_annexes.py`, `build_trabajo_pendiente.py`, los tres manuscritos.

## Qué se comprobó del cuaderno, y qué no

Una comprobación **mecánica**, no una revisión: `comprueba_citas_lectura.py` busca
cada frase entrecomillada en el texto del PDF del estudio al que se atribuye.
**481 citas; 457 de texto, todas en su PDF y todas en la página que declaran.**
Se abrieron los 70 PDF. Las otras 24: 23 son transcripciones de figuras marcadas
«[imagen]» (antibiogramas leídos de una figura) que no se pueden comprobar así, y
una es la abreviatura «n.s.». Nadie ha comprobado aquí las 23 transcripciones
contra sus figuras.

El cuaderno no dice quién leyó los artículos ni si intervino un modelo de
lenguaje. El manuscrito dice solo lo que consta —que cada conclusión lleva la
firma de los dos— y la pregunta va en la hoja 4 del cuaderno de firma.

## Punto 2 — la clase de resistencia, contra el artículo

70 estudios con texto completo. La traducción del texto firmado a categorías
está en `ingest_lectura_firmada.py`, estudio por estudio, y cada una lleva una
guarda: si la frase firmada no dice lo que la categoría supone, el guion se
niega. Las 70 pasan.

| Verificación | Estudios |
|---|---|
| contra un antibiograma impreso | 22 |
| contra una descripción de la sensibilidad en el texto | 8 |
| no verificable (antibiograma no publicado o en un suplemento no obtenido) | 31 |
| **ningún paciente con *P. aeruginosa* tratado con fagos** | **9** |

De los 30 comprobados: 18 coinciden; 5 estaban como «not-classifiable» y el
artículo permite asignarlos (EST-053, EST-057 y EST-088 por debajo del umbral;
EST-046 y EST-105 XDR); 2 son más graves (EST-043 y EST-047, XDR donde constaba
MDR); en 3 la clase declarada no se confirma (EST-015 es XDR y no PDR porque la
colistina es sensible; EST-030 solo confirma MDR; el antibiograma de EST-042
contradice la PDR); 2 son mixtos (EST-124, EST-169).

**35 correcciones a la extracción**: 8 de clase, 17 de procedencia (a
«independently-verified», solo donde hay antibiograma impreso) y 10 de DTR. Entran
por `correcciones_tras_texto_completo.csv` con el valor anterior, la primera cita
del cuaderno y las dos firmas. Una segunda pasada no añade nada.

**Lo que mueve:** brazos por debajo del umbral 4 → **7**; estudios de un solo
brazo por debajo del umbral 2 → **5**; clase asignable en el texto completo 48 →
**53 de 70** (75,7 %); DTR derivable 69 → **67**.

**Lo que NO se aplicó**, y por qué: 9 estudios dejan el brazo con más de un valor
(EST-004, 019, 042, 047, 048, 058, 106, 124, 169). Por ejemplo, EST-169 tiene un
paciente por debajo del umbral y otro XDR en un mismo brazo; codificarlo exige
partir el brazo y reextraer el desenlace de cada uno. Van a la hoja 3.

## Los nueve sin *P. aeruginosa*

EST-009, EST-055, EST-129, EST-132, EST-135, EST-152, EST-170, EST-181 y
EST-208. La lectura lo dice con su frase: en EST-009 no se aisló *P. aeruginosa*;
EST-055 no la tiene entre sus aislados; en EST-129 no fue diana del fago;
EST-132 no informa cuántos pacientes la tenían; en EST-135 fue una sobreinfección
no tratada con fagos; EST-152, EST-181 y EST-208 son de *S. aureus*; EST-170 es de
*K. pneumoniae*. No cumplen el criterio de población.

**No se excluyen.** Excluir es un acto de autoría y lo que firmasteis el 30 era
la clase, no la exclusión. Van a la hoja 1, con EST-051 y EST-096 como dudosos.
Pesan: EST-055 y EST-132 son dos de los cinco con grupo de comparación, y los dos
y EST-152 están en la Tabla 7.

## Punto 7 — los comparativos

14 reextraídos, 11 con texto. Ninguno contradice la hoja 6 del 22 de septiembre,
pero la acota: **de los 5 con grupo de comparación, 4 comparan fago con ausencia de
fago** (EST-108 compara con y sin antibiótico dentro de los tratados con fago), y
**solo 2 dan un contraste para *P. aeruginosa***: EST-021 (HR con IC) y EST-008
(parcial: diferencias de medias y valores p de 7 frente a 2, sin dispersión ni
intervalo). EST-055 no tiene ningún paciente con *P. aeruginosa* y EST-132 no
desglosa por organismo. Lo genera `build_rob_table.py` en los tres manuscritos.

## Punto 15 — el solapamiento

Los 13 pares sin leer se leyeron y **los 13 se descartan**. La lectura añadió
otros 19, y los 19 solapan: 11 ya estaban confirmados y se confirman de nuevo
(uno de ellos con 6 pacientes donde se contaba 1), 1 estaba sin resolver
(EST-049 + EST-061) y 7 son nuevos:

- EST-003 + EST-070 son dos series del mismo centro y comparten **6** pacientes,
  no 1. EST-003 comparte en total **8**.
- EST-034, EST-049, EST-061 y EST-077 (UCSD) comparten **3**: el trasplantado
  pulmonar de 67 años sale en tres estudios.
- EST-108 incluye además a EST-002 (por cita, ref. 26) y, muy probablemente, a
  EST-088 (mismo niño, misma infección, mismos fagos; salió después).

**20 pacientes descritos en más de un estudio, en 18 estudios**, frente a 11 en 13.
35 pares examinados: 19 confirmados, 16 descartados, 0 sin leer, 0 sin resolver.

El recuento contaba claves por FILA y habría dado 22: una fila puede llevar seis
personas. Ahora cuenta personas (`P1`…`P20`), y una persona que sale en tres
pares se cuenta una vez.

## Lo que el manuscrito no decía y ahora dice

- El maestro y el inglés **no declaraban el solapamiento de pacientes**; solo el
  de la revista. Ahora es su séptima limitación.
- **S21 enviaba los candidatos del detector, sin veredicto**, y el manuscrito
  remitía a él para el desglose. Ahora envía cada par examinado con su veredicto,
  sus pacientes y la frase firmada.
- Tres cifras del solapamiento del de la revista iban tecleadas («3 se
  descartaron, 1 quedó sin resolver», «quince referencias»). Ahora salen de
  escalares, y «quince» se cuenta desde el texto de EST-108.
- Las listas de estudios («EST-001 A, EST-003 B…») iban tecleadas. Los guardianes
  aceptan ahora `{coma_x}` y `{lista_x}`.

## Pendiente, y es de los autores

El cuaderno `FIRMAR_lectura_2026-10-01.xlsx`: los 9 (+2) sin *P. aeruginosa*, los 3
por debajo del umbral, los 9 brazos abiertos y cómo se hizo la lectura. Mientras
no se firme, el manuscrito declara esos puntos como pendientes y no se puede
enviar.
