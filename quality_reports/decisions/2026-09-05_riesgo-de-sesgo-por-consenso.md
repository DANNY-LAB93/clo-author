# El riesgo de sesgo se evalúa por consenso, no por duplicado independiente

**Estado:** DECIDIDO por D. Valdiviezo el 5 de septiembre de 2026
**Ficheros:** `revision_sistematica/riesgo_sesgo/riesgo_sesgo_comparativos_consenso.xlsx`,
`scripts/make_rob_consensus.py`, `scripts/ingest_rob.py`, `scripts/compare_rob.py`,
`paper/manuscrito_JSR_final.md`

## Qué se encontró

Los dos cuadernos de riesgo de sesgo de los estudios comparativos
—`riesgo_sesgo_comparativos_danny_valdiviezo.xlsx` y
`riesgo_sesgo_comparativos_nataly_trelles.xlsx`— aparecieron rellenos la noche
del 4 al 5 de septiembre. En la primera revisión, a las 23:25, los **82 juicios
eran idénticos** en los dos ficheros, sin una sola discrepancia, y el informe de
concordancia daba acuerdo del 100 % y kappa mediana de 1,00.

A las 00:40 los ficheros se habían vuelto a guardar, con dos segundos de
diferencia entre uno y otro, y ya presentaban **13 discrepancias de 82** (84,1 %
de acuerdo), todas en ROBINS-I y ninguna en RoB 2.

Pero la columna «¿en qué frase te apoyaste?» seguía trayendo el **mismo texto,
carácter por carácter, en los once estudios anotados**: mismas comillas
tipográficas, misma numeración, mismos tabuladores, 7 418 caracteres idénticos
en los dos cuadernos.

Dos revisores pueden elegir el mismo valor de un desplegable de cinco opciones
—por eso el acuerdo alto no prueba nada por sí solo—. Lo que no hacen es
escribir la misma frase, con la misma puntuación, en once estudios seguidos. Un
cuaderno salió del otro.

## Por qué no se podía dejar así

El manuscrito declaraba, en Métodos: «los dos revisores evaluaron cada dominio
de forma independiente, a ciegas del cuaderno del otro, y resolvieron los
desacuerdos por consenso». Con esos ficheros esa frase es falsa, y la kappa no
mide concordancia entre revisores: mide cuántas celdas se tocaron después de
copiar. Es lo primero que comprueba un árbitro, y a este proyecto ya le marcaron
tres veces una declaración de método que decía más de lo que había.

Lo que sí hay es una evaluación real: frases citadas de los artículos, con
localización, y la identificación de qué estudios carecen de grupo control. El
problema no era la calidad del trabajo sino de cuántas cabezas salió.

## Qué se decidió

**Declarar lo que ocurrió: evaluación por consenso, no por duplicado
independiente.** Una sola pasada acordada entre los dos autores. Sin kappa. La
alternativa —que N. Trelles evaluara de cero, a ciegas— se ofreció y se
descartó.

Consecuencias, todas aplicadas:

- **Un solo cuaderno.** `make_rob_consensus.py` construye
  `riesgo_sesgo_comparativos_consenso.xlsx`: los 69 juicios en que los dos
  ficheros coincidían entran precargados; las **13 celdas que discrepaban quedan
  VACÍAS**, en amarillo, con un comentario que dice qué había en cada fichero.
  Heredar uno de los dos valores habría sido elegir por ellos, que es justo lo
  que hay que evitar. Esas trece son las únicas decisiones que quedan.
- **Firma obligatoria.** `ingest_rob.py --consenso` no ingiere sin los dos
  nombres y la fecha en la hoja «Firma», ni con un solo juicio sin decidir.
  La procedencia de las 82 filas es `consenso`, sin excepción.
- **Métodos lo dice.** «Los juicios se emitieron por consenso y no por duplicado
  independiente», con el contraste explícito frente a la extracción de datos,
  que sí fue por duplicado.
- **Limitaciones lo recoge** como sexta limitación, junto al sesgo de
  recuperación y al juicio a nivel de dominio.
- **El resumen lo dice**: «se evaluó por consenso, por dominios».
- **La prosa de Resultados no finge concordancia**: «al no haber dos lecturas
  independientes, no se reporta concordancia entre revisores».

## Los dos guardarraíles que quedan puestos

`compare_rob.py` no vuelve a presentar como hallazgo lo que es un síntoma:

1. **Acuerdo perfecto.** A partir de 20 respuestas comparables sin una sola
   discrepancia, el informe abre con un aviso en vez de con la kappa.
2. **Texto libre idéntico.** A partir de 3 notas iguales palabra por palabra,
   el informe dice que un cuaderno salió del otro. Esta es la señal difícil de
   borrar: la primera se desactiva cambiando unos desplegables, y eso fue
   exactamente lo que pasó entre las 23:25 y las 00:40; la segunda exigiría
   reescribir 7 418 caracteres, y entonces ya sería una lectura de verdad.

Los dos cuadernos originales **se conservan** como registro de lo que había, y
no se borran. El que alimenta el manuscrito es el de consenso.
