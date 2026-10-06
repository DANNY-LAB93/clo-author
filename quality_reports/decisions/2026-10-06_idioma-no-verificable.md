# Tres estudios fuera porque su idioma no se puede probar

**Estado:** APLICADO el 6 de octubre de 2026.
**Viene de:** D. Valdiviezo recordó ese día que el corpus solo admite estudios
redactados en inglés o en español. Firmado en `FIRMAR_idioma_2026-10-06.xlsx` por
DANNY JAVIER VALDIVIEZO VERDUGO y NATALY ELIZABETH TRELLES AVILA (el cuaderno
decía «NATHALY»; se corrigió a petición de D. Valdiviezo en el cuaderno, en su
copia y en `decisiones_idioma_2026-10-06.csv`). SUPERA lo que el registro del
2026-09-01 decía de EST-045 y EST-059 («se conservan»).

## Lo que se comprobó

- **Los 65 PDF del corpus**: idioma del cuerpo detectado sin navegador
  (`comprueba_idioma_cuerpo.py`, nuevo paso del canal). 65 en inglés. 18 nunca se
  habían comprobado sobre el cuerpo. EST-075 tiene un 22 % de cirílico: su página 1
  es el resumen ruso de la revista; el cuerpo (pp. 2-5) está en inglés.
- **Las 42 fichas de registro**: ClinicalTrials.gov o Cochrane CENTRAL, en inglés.
  El «danés» de EST-022 era un falso positivo del detector sobre un título corto.
- **Los 24 sin texto completo**: solo prueba de título y resumen. En tres, la
  revista no publica de forma nativa en inglés: EST-045 y EST-059 (*Infektsionnye
  Bolezni*, Rusia) y EST-173 (*Surgical Chronicles*, Grecia). La ficha inglesa del
  editor de los dos rusos no enlaza el artículo ni declara su idioma.

## Lo que se decidió

Los tres salen con **NOREC** («texto completo no recuperado: no se pudo verificar
contra el artículo»). No con IDI, que afirmaría que no están en inglés ni en
español, y eso nadie lo ha visto. No es extender NOREC a los 24 sin texto (nota 4
de CLAUDE.md): son tres con una razón concreta, y el manuscrito lo dice así.

Corpus 128 estudios, 86 extraíbles, 65 con texto (75,6 %), 21 sin texto, 94 brazos.
NOREC excluye ahora 4 (EST-118 y estos tres). Los tres no tenían datos extraídos.

## Lo que se arregló de paso

- El «1 estudio» de NOREC iba tecleado en los tres manuscritos; anclado.
- La §3.1.1 no describía las exclusiones NOREC (ya faltaba EST-118): «Treinta y
  ocho» no cuadraba con su desglose. Párrafo nuevo, anclado.
- «Los 29 anteriores se juzgaron sobre el artículo» era viejo; ahora «Los 38
  anteriores se juzgaron sobre su publicación», anclado. «Los 31 sin texto
  completo» era correcto por casualidad (21 + 10); anclado.

Anclas: 315, todas al día. 17 de 17 cifras auditadas se reproducen.
