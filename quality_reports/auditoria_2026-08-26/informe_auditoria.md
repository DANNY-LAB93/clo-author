# Auditoría de primera pasada — envío a *Journal of Science and Research*

**Objeto:** paquete `Envio_JSR_Fagoterapia_Pseudomonas` (revisión sistemática de
fagoterapia en *Pseudomonas aeruginosa*, n = 124 estudios recuperables).
**Alcance:** consistencia interna de las 4 tablas contra sí mismas y contra el
texto del manuscrito; contraste formal de las afirmaciones de sesgo; revisión
ortográfica de los CSV sueltos.

## Qué hay y qué no

La carpeta no contiene datos primarios: no hay cuadernos de extracción, ni el
fichero de cribado, ni la tabla registro-por-estudio. Lo disponible son cuatro
tablas **agregadas** y el manuscrito. Esto acota lo que una primera pasada puede
hacer: no se pueden recalcular incidencias, ni reajustar la estratificación, ni
verificar el etiquetado de un estudio concreto. Sí se puede —y es lo que un
revisor hará— comprobar que **todas las cifras publicadas son mutuamente
consistentes**. Es la auditoría que se ha ejecutado.

## Resultado: 60 de 60 comprobaciones cuadran

Ninguna cifra del manuscrito contradice a otra. Verificado:

- **Flujo PRISMA completo.** 23 057 − 5 928 = 17 129 únicos; 17 129 − 3 235 =
  13 894 títulos; 13 894 − 13 434 = 460 a resumen; 460 − 227 = 233 a texto
  completo; 154 + 30 = 184 estudios; 121 + 3 = 124 recuperables; 184 − 124 = 60
  solo con ficha de registro. Cada resta cierra exactamente.
- **Tabla 4 reconcilia con el flujo en ambos ejes.** Las siete filas de motivos
  suman 13 434 por título y 227 por resumen — precisamente los dos números de
  exclusión del diagrama — y cada fila cuadra en horizontal con su total.
- **Tabla 1.** Los siete diseños suman 124; la columna de procedencia suma 124;
  los 24 porcentajes coinciden con n/124 al primer decimal; comparativos =
  16 aleatorizados + 7 no aleatorizados = 23 (18,5 %).
- **Tabla 2.** Las cinco variables suman 124 en declara + no declara, y los diez
  porcentajes coinciden.
- **Tabla 3 cruza con Tabla 1 en tres puntos independientes:** comparativos
  12 + 11 = 23; casos únicos 40 + 9 = 49; aleatorizados 8 + 8 = 16.
- **Enmienda de idioma.** 219 → 184 y 159 → 124 dan la misma pérdida de 35, y
  coinciden con la fila IDI de la Tabla 4 (35 informes).

## Un solo punto de redondeo, no un error

El texto dice que la clase de resistencia no es asignable en el **80,6 %**. La
suma de los dos porcentajes citados (70,2 % + 10,5 %) da 80,7 %. El valor exacto
es 100/124 = **80,65 %**, así que el 80,6 % del texto es correcto y la
discrepancia de 0,1 pp es artefacto de sumar cifras ya redondeadas. Sugerencia
opcional: escribir «el 70,2 % no la menciona y otros 13 estudios (10,5 %) la
mencionan de forma inclasificable» — con el n explícito la aritmética del lector
cierra sola.

## Las afirmaciones de sesgo, contrastadas

El manuscrito afirma cualitativamente dos sesgos. Ambos resisten una prueba
formal (Fisher exacto bilateral):

| Afirmación | Datos | OR | p |
|---|---|---|---|
| Los comparativos se concentran en la fracción no recuperada | 12/91 vs 11/33 | 0,30 | **0,017** |
| Los aleatorizados, igual | 8/91 vs 8/33 | 0,30 | **0,034** |
| La enmienda de idioma eliminó comparativos de forma desproporcionada | 18/35 vs 23/124 | 4,65 | **0,0003** |
| Los casos únicos se concentran en la fracción recuperada | 40/91 vs 9/33 | 2,09 | 0,10 |

Las tres primeras son defendibles y **pueden citarse con su p**, lo que refuerza
la sección de limitaciones: el sesgo de recuperación no es una sospecha, es
medible. La cuarta no alcanza significación; conviene no afirmarla en términos
inferenciales aunque la dirección sea la esperada.

## Dos cifras derivadas que merecen aparecer en el texto

1. **La clase de resistencia realmente utilizable es el 19,4 %** (24 de 124: los
   37 que la declaran menos los 13 inclasificables). El manuscrito da el
   complemento (80,6 % inservible); el positivo es más contundente y no está
   escrito.
2. **La fracción no recuperada concentra el 31,9 % de los pacientes declarados**
   (489 de 1 531). La Tabla 3 tiene los dos números pero no el cociente, y este
   cierra el argumento del sesgo de recuperación en términos de pacientes, no
   solo de estudios.

## Cuestiones de forma en los CSV

Diez topónimos y motivos de exclusión han perdido la tilde en los ficheros
sueltos: `Belgica`, `Iran` (Tabla 1) y `Revision`, `Sintesis`, `revision`,
`preclinico`, `modelizacion`, `infeccion`, `epidemiologia`, `evalua` (Tabla 4).
El detalle por línea está en `auditoria_ortografia.csv`. Si estos CSV se envían
como material suplementario, conviene corregirlos — y como la carpeta se
regenera desde `scripts/build_jsr_submission.py`, la corrección va en el script,
no en el CSV.

## Lo que esta auditoría NO cubre

- **Nada sobre la veracidad del etiquetado.** Que 49 estudios estén marcados
  como caso único es internamente consistente; si esa clasificación es correcta
  solo se comprueba contra los registros, que no están aquí.
- **Las declaraciones de honestidad no se han tocado.** El cribado por un modelo
  de lenguaje como revisor único, los 724 desacuerdos sin reconciliar y la
  ausencia de registro en PROSPERO/OSF son limitaciones declaradas, no errores
  aritméticos, y quedan fuera del alcance de una comprobación de consistencia.
- **Los pendientes de envío siguen pendientes** y ninguno es resoluble por
  cálculo: ORCID y credenciales de los dos autores, y sobre todo la **autoría de
  N. Trelles**, que el propio README marca como la cuestión seria sin resolver.

## Recomendación

Desde el punto de vista de la consistencia numérica, el manuscrito está listo:
no hay ninguna cifra que un revisor pueda impugnar por no cuadrar. Los tres
cambios que aportarían algo son incrementales — el n explícito en el 80,6 %, el
19,4 % de resistencia utilizable, el 31,9 % de pacientes no recuperados — y los
dos últimos añaden fuerza argumental sin tocar ninguna declaración.
