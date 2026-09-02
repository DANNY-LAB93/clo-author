# El criterio de idioma se verificó sobre el resumen, no sobre el artículo

**Estado:** INFORME — la exclusión la deciden los dos revisores
**Fecha:** 1 de septiembre de 2026
**Origen:** D. Valdiviezo recordó el criterio —«solo español e inglés, nada
más»— y añadió: «sin traducción». Las dos cosas resultaron necesarias.

## Lo primero: el navegador estaba traduciendo

Al abrir el primer artículo ruso en Chrome, la página llegó **en español**. No
porque el artículo lo estuviera: porque Chrome lo tradujo automáticamente. Si
esa lectura se hubiera dado por buena, un artículo íntegramente en ruso habría
quedado registrado como legible en español.

Todas las comprobaciones siguientes se hicieron **descargando la página sin
navegador**, que no traduce nada, y midiendo el alfabeto carácter a carácter.

## El fallo de fondo

`idioma_verificacion.csv` marca **29 de los 102 estudios extraíbles** con la
clase **«A. texto probado»**, la más fuerte del esquema. Pero esos 29 **no
tienen texto completo recuperado**. Lo que el detector midió fue el **resumen**
que indexa la base bibliográfica, no el cuerpo del artículo.

Para un artículo de *Infection* o del *Journal of Chemotherapy* da igual: son
revistas anglófonas y el cuerpo está en inglés. Para una revista que publica en
otra lengua **con resumen en inglés** —que es la norma en Rusia, Polonia o
Ucrania— la medición dice exactamente lo contrario de la verdad.

El propio manuscrito avisa de esto en §2.5: hay que analizar «las páginas
centrales del artículo y no la portada, que muchas revistas publican en inglés
aunque el cuerpo no lo esté». La regla estaba escrita; no se aplicó a los
estudios sin texto completo, porque no había texto que analizar.

## Cuatro estudios que no cumplen el criterio

Los cuatro son de **Хирургия / Pirogov Russian Journal of Surgery**, en
mediasphera.ru. Medido sobre la página del editor, sin traducir:

| estudio | diseño | cirílico | latino |
|---|---|---:|---:|
| **EST-092** | ECA | **94,1 %** | 2 457 |
| **EST-103** | ECA | **77,9 %** | 2 008 |
| **EST-147** | reporte de caso | **91,0 %** | 24 374 cir. / 2 422 lat. |
| **EST-219** | ensayo no aleatorizado | **93,0 %** | 1 285 |

Lo latino es el resumen en inglés, las palabras clave y las referencias. El
cuerpo es ruso.

**No existe versión inglesa.** Se comprobaron las tres rutas del sitio: `/en/`
devuelve 404, `?lang=en` devuelve la misma página cirílica, y la descarga
`/downloads/en/` no entrega un PDF. La premisa que los mantuvo en el corpus
—«las revistas que editan una versión íntegra en inglés se conservaron»— es
falsa para esta revista.

Los cuatro figuran en el registro como `idioma_declarado = rus`, y aun así
`ADMITIDO`. El dato para excluirlos estaba en el fichero desde el principio.

## EST-219, además, falla por población

Su texto completo se leyó (en ruso, sin traducir). Son 111 pacientes con
infecciones purulentas de la mano, repartidos en dos grupos de 55 y 56. Los
patógenos predominantes fueron ***Staphylococcus* y *Streptococcus***, y
*Pasteurella multocida* tras mordeduras de animales. *P. aeruginosa* aparece en
un solo sitio: la **composición del piobacteriófago complejo** —«содержащий
очищенные фильтраты фаголизатов бактерий Staphylococcus, Enterococcus,
Streptococcus, Escherichia coli, Proteus vulgaris, Proteus mirabilis,
**Pseudomonas aeruginosa**, Klebsiella pneumoniae, Klebsiella oxytoca»—.

Es el mismo patrón que motivó las diez exclusiones ORG del 1 de septiembre, y
confirma lo que aquel informe decía: **22 de 93 era un suelo**. En cuanto se
consigue un texto más, aparece otro.

## Los que se comprobaron y AGUANTAN

- **EST-045** y **EST-059** (*Infektsionnye Bolezni*): el DOI resuelve a la
  ficha **inglesa** del editor (phdynasty.ru/en/), 95 % latina. Esa editorial sí
  publica edición inglesa, que es justo el supuesto de §2.5. Se conservan, pero
  siguen **sin texto completo**, así que la clase «A. texto probado» tampoco les
  corresponde.
- **EST-205** (*Revista Cubana de Angiología y Cirugía Vascular*): español,
  clase A legítima. Cumple.
- **EST-177** (*Otolaryngologia Polska*): la página del editor no renderiza sin
  JavaScript y la comprobación quedó **sin resolver**. No se afirma nada de él.

## Qué hay que decidir, y qué hay que arreglar

1. **Excluir EST-092, EST-103, EST-147 y EST-219** por idioma. Dos son ECA y
   uno es un ensayo no aleatorizado, así que la pérdida cae otra vez sobre los
   comparativos: de 16 quedarían 13, y de 11 ECA quedarían 9.
2. **La clase «A. texto probado» no puede aplicarse a un estudio sin texto
   completo.** Son 29. Hay que reetiquetarlos a una clase que diga la verdad
   —el idioma se infirió del resumen— y S10 debe dejar de contarlos como
   verificados sobre el texto íntegro.
3. Al recuperar cada texto que falta hay que **comprobar el idioma sobre el
   cuerpo**, no sobre el resumen, y **sin traducción automática**.
