Nataly, te paso el archivo de extracción de la revisión de fagos:
`extraccion_nataly_trelles.xlsx`. Tiene tres hojas.

Empieza por la hoja Ejemplo. Son dos estudios que ya extraje, con el porqué de
cada campo al lado. Leerlo toma diez minutos y se entiende mejor que cualquier
instructivo.

Donde trabajas es la hoja Extraccion. Son 159 estudios, uno por fila. Las
columnas grises, de la A a la H, identifican el estudio y no se tocan. El
id_provisional es lo que después me permite cruzar tu archivo con el mío, así
que si lo cambias se rompe el cruce. De la columna I en adelante es tuyo.

Lo más importante: no abras mi archivo ni el dataset de extracción del proyecto
mientras llenas el tuyo. Hay 42 estudios que ya extraje yo y aun así salen en
blanco, a propósito. La idea es comparar después y ver en qué discrepamos; si
ves lo que puse, la comparación ya no mide nada.

Sobre los brazos. Una fila es un brazo, no un estudio. Si el artículo permite
contar desenlaces por separado en pacientes XDR y en pacientes MDR, son dos
filas: copias la fila entera, dejas el mismo id_provisional y cambias arm_id a
B. En Pirnay 2024 son tres filas por eso, aunque todos los pacientes recibieron
el mismo tratamiento. Y al revés: si el artículo no permite separarlos, una sola
fila y resistance_class en not-classifiable. No inventes brazos donde el paper
no los da.

NA y celda vacía no son lo mismo. NA quiere decir que el artículo no lo reporta.
Vacío quiere decir que todavía no lo has mirado. El script que compara los
distingue, así que conviene ser explícita.

En extraction_citation va dónde viste el dato, tipo "p.3 Results, Tabla 2". Es
obligatorio para cualquier número. Sin eso el dato no se puede verificar después
y toca volver a abrir el paper.

Los desplegables traen las opciones cerradas, pero puedes escribir encima. Si la
vía de administración no encaja en ninguna, pon "other (instilación
intravesical)" o lo que corresponda. El paréntesis no afecta la comparación, así
que explica con confianza.

Cuando termines me pasas el archivo sin cambiarle el nombre. Corro el script que
calcula la concordancia entre las dos extracciones y saca la lista de
desacuerdos, y esos los resolvemos entre los dos.

Si 159 son muchos para el tiempo que tienes, dime y te genero una muestra
aleatoria de 40. Sirve igual, solo que reportamos qué porcentaje se verificó por
duplicado.
