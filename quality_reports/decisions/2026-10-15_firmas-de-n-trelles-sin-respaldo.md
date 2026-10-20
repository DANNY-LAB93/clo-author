# 2026-10-15 — Firmas de N. Trelles que el registro no respalda

**Estado:** CORREGIDO en los datos, los manuscritos, el protocolo y los anexos. **Queda pendiente de N.T.**
**Origen:** segunda ronda del consejo adversarial (15 de octubre), comprobada contra los ficheros y el historial antes de corregir.
**Pedido por:** D. Valdiviezo, «corrige todos los errores».

## Lo que se encontró

1. **27 exclusiones a texto completo figuraban como firmadas por los dos autores y solo consta la orden de D.V.**
   - En `revision_sistematica/cribado/exclusiones_tras_texto_completo.csv`, 26 filas del 1 de septiembre de 2026 y 1 del 2 de septiembre llevaban `decidido_por` = «D. Valdiviezo y N. Trelles».
   - Las escribió a mano el modelo en los commits `8992c13`, `2ea2224` y `7287dee`. Los tres dicen «Orden de D. Valdiviezo», y los dos primeros añaden «firma de los dos revisores» o «las dos firmas» sin ningún soporte.
   - No hay cuaderno `FIRMAR_*` ni guion `ingest_*` detrás de esas filas. Todas las tandas posteriores (14-sep, 22-sep, 1 y 3-oct, 6-oct) sí salen de cuadernos firmados con los dos nombres.
   - Recuento resultante: 89 exclusiones con firma de los dos, 2 firmadas solo por D.V. (EST-118 y EST-205) y 27 por orden de D.V. sin firma de N.T.
2. **El paquete con que se pidió a N.T. firmar las 5 correcciones de modalidad lo redactó el modelo en primera persona de D.V.**
   - `revision_sistematica/extraccion/firma_nataly/mensaje.md` (commit `d14e927`, con Claude como coautor) dice: «Leyendo los textos completos uno por uno encontré cinco brazos…». La lectura y la propuesta las hizo el modelo (commit `5749bca`).
   - La firma de N.T. (commit `ea891a8`) se obtuvo con ese texto.
3. **Dos veredictos de solapamiento sin firma.** EST-108 con EST-034 y EST-108 con EST-044 los descartó la lectura del modelo del 22-sep (commit `284cc14`). No están en `lectura_solapamiento_firmada.csv`. Los manuscritos decían que cada veredicto lleva la firma de los dos.
4. **Atribuciones a «los autores» sin respaldo.**
   - Las dos reglas del 4-ago (endolisinas y veterinaria) las añadió el modelo en sus guiones de lote, y no consta decisión de nadie.
   - La unidad de inclusión del 5-ago la decidió D.V. («Decide: usuario (DANNY-LAB93)»).
   - PRO e INT se crearon por orden de D.V. (`8992c13`). Solo NOORG consta firmado por los dos.
5. **Las ecuaciones de búsqueda las redactó el modelo** (commit `923bbe7`, «Write search equations for all seven databases»). Que D.V. las diseñara no figura en su declaración del 8-oct.

## Lo que se cambió

- **Los datos.** En el CSV, esas 27 filas dicen ahora «D. Valdiviezo (orden del 2026-09-0X; no consta firma de N. Trelles)». Es una sustitución de texto en esas 27 líneas y nada más; la versión anterior queda en el historial de git. Los guiones que distinguen «los dos» por « y » las cuentan ya como de un solo autor.
- **Escalares nuevos y anclados:** `exclusiones_firmadas_los_dos` (89), `exclusiones_firmadas_solo_dv` (2), `exclusiones_orden_dv_sin_firma_nt` (27), `pares_solapamiento_firmados` (28) y `pares_solapamiento_sin_firma` (2).
- **La declaración de uso de IA** dice ahora:
  - quién decidió cada criterio que propuso el modelo;
  - que las dos reglas del 4-ago las añadió el modelo sin decisión registrada;
  - que el modelo redactó las ecuaciones;
  - cuántas exclusiones firmó cada uno;
  - que el modelo descartó 2 pares sin firma;
  - que redactó en primera persona de D.V. los mensajes a N.T.
- **Lo mismo en Métodos, el CRediT, el protocolo y los anexos.**

## Lo que queda, y es de los autores

- **Que N.T. ratifique por escrito las 27 exclusiones**, si está de acuerdo, en un cuaderno de firma como los demás. Mientras no lo haga, los documentos dicen que no consta su firma.
- **Que N.T. sepa, antes de aprobar el manuscrito, que el mensaje del 1 de septiembre lo redactó el modelo** y que la lectura que presentaba como de D.V. era del modelo. Su firma de aquellas 5 correcciones se obtuvo con ese texto.
- **Que N.T. firme o no los 2 descartes de solapamiento del modelo.**
