> **SUPERADO EN PARTE — leer antes que nada. Anotado el 10 de septiembre de 2026.**
>
> Esta carpeta vivía dentro del sobre de envío, que no es su sitio: no es material
> para la revista y no estaba versionada en ninguna parte. Se movió al repositorio
> tal cual, sin tocar el cuerpo del informe, que es solo-anexar.
>
> **Los tres bloqueantes están resueltos**, comprobados uno a uno el 10-09-2026:
>
> - **Bloqueante 1.** La cifra de N. Trelles ya no se teclea: sale de los
>   escalares en los dos sitios donde aparecía, y hoy dice 122 de 124 (98 %),
>   no 98. El marcador de autoría ICMJE sigue puesto a propósito: falta que
>   ella apruebe la versión final, y eso no lo firma nadie por ella.
> - **Bloqueante 2.** El manuscrito reporta su concordancia de extracción: 78 %
>   de acuerdo mediano y kappa de Cohen mediana de 0,62.
> - **Bloqueante 3.** El sobre lleva los 16 anexos que el manuscrito cita, en 36
>   ficheros (los de datos viajan en `.csv` y en `.xlsx`).
>
> **Los puntos 4, 5, 6 y la Oportunidad NO se han vuelto a comprobar.** No se
> dan por resueltos: se dan por no revisados desde el 26 de agosto.
>
> Aviso obsoleto del cuerpo: ya no existe `manuscrito_JSR.docx`. El sobre lleva
> un solo manuscrito, `manuscrito_JSR_final.docx`, y ningún fichero de esta
> carpeta se regenera dentro de él.

---

# Correcciones pendientes antes de enviar

Auditoría del 26 de agosto de 2026 sobre el paquete de envío y sobre el proyecto
`clo-author`, del que este paquete se genera. Cada punto lleva el fichero y la línea donde
se corrige.

**Este fichero sobrevive a `build_jsr_submission.py`.** Ese script sobrescribe
`manuscrito_JSR.docx`, `figuras/` y `tablas/`, pero no borra el resto de la carpeta. Aun
así, **ninguna corrección debe hacerse editando los ficheros de esta carpeta**: todos se
regeneran desde `clo-author`. Corrige en el origen que cada punto indica y vuelve a
ejecutar el script.

---

## Bloqueante 1 — La cifra que sostiene la autoría ICMJE está desactualizada

`quality_reports/extraction_agreement.json` se generó el 23-08 a las 11:44. El cuaderno
`revision_sistematica/extraccion/extraccion_nataly_trelles.xlsx` se modificó el **25-08 a
las 23:31**, dos días después, y el JSON no se regeneró.

La cifra «98 estudios» que ese JSON publica aparece en tres sitios:

| Fichero | Línea | Texto |
|---|---|---|
| `paper/manuscrito_revision_sistematica.md` | 101 | «un segundo revisor extrajo de forma independiente 98 de ellos» |
| `scripts/build_jsr_submission.py` | 358 | marcador de autoría de N. Trelles: «extrajo 98 de …» |
| `LEEME_ANTES_DE_ENVIAR.md` (esta carpeta) | 44 | «extrajo 98 de los 124 estudios de forma independiente» |

**Por qué es bloqueante.** Esa cifra es el argumento de contribución sustancial ICMJE en un
caso de coautoría declarado como no resuelto. No puede enviarse un número que el propio
proyecto ya no reproduce.

**Acción.** Volver a ejecutar el comparador antes de cualquier otra cosa:

```bash
python scripts/compare_extractions.py \
  --a revision_sistematica/extraccion/extraccion_danny_valdiviezo.xlsx \
  --b revision_sistematica/extraccion/extraccion_nataly_trelles.xlsx \
  --nombre-a Danny_Valdiviezo --nombre-b Nataly_Trelles
```

Y propagar el número resultante a los tres sitios de la tabla.

**Advertencia sobre las cifras de este punto.** Tres lecturas independientes de los mismos
cuadernos dan tres recuentos distintos de estudios del segundo revisor: 98 (el JSON
publicado), 104 y 107. Las tres reimplementan la carga por vías distintas. **La única cifra
válida es la que produzca el script del proyecto al reejecutarse**, porque es el que define
la convención de emparejamiento. No se propone aquí ningún número sustituto.

## Bloqueante 2 — El manuscrito no reporta su propia concordancia de extracción

Existe un cálculo de concordancia entre los dos extractores en
`quality_reports/extraction_agreement.json` —acuerdo mediano en torno al 69 %, kappa
mediana en torno a 0,30, conflictos de valor en el orden de las centenas— y **ninguno de
esos términos ni de esas cifras aparece en el manuscrito**. La sección de metodología
declara la concordancia como prevista y describe la doble extracción parcial, pero no
publica el resultado.

Además, `S11_concordancia_entre_extractores.pdf` (el anexo que sí la reporta) declara otras
cifras distintas: 164 filas por revisor, 162 comparadas, 169 conflictos, acuerdo del 70 %,
kappa de 0,38. El anexo es del 20-08; el JSON, del 23-08. Son dos instantáneas de un
cálculo que se rehizo.

**Por qué es bloqueante.** Omitir una concordancia baja es exactamente lo que un revisor
calificará de reporte selectivo. Declararla, en cambio, es coherente con la franqueza que
el resto del manuscrito ya practica al publicar sus otras limitaciones.

**Acción.** Regenerar el cálculo (comando del bloqueante 1), regenerar S11 desde el
resultado nuevo, y añadir a la sección de metodología un párrafo con la cifra resultante,
la convención de emparejamiento usada y la razón por la que algunas kappas no son
informativas. La discrepancia entre el anexo y el JSON desaparece al regenerar ambos desde
la misma entrada.

## Bloqueante 3 — El paquete lleva 3 de los 14 anexos que el manuscrito cita

La línea 10 del manuscrito declara «Material suplementario: 14 anexos (S0–S13) y su guía».
Esta carpeta contiene **S1, S2 y S7**. Faltan S0, S3 (dos ficheros), S4, S5, S6, S8, S9,
S10, S11, S12 y S13, más el índice y la guía. Todos existen en
`clo-author/verificables revisión sistemática/`.

**No es un problema de inexistencia sino de empaquetado.** `build_jsr_submission.py` copia
únicamente `paper/figuras/*` y `paper/tablas/*` (líneas 402–408). No tiene ningún paso que
copie suplementos: los tres presentes entraron por una copia manual ajena al script. Por
eso reejecutar el script no los añadirá.

**Acción.** El parche está preparado y verificado en `parche_empaquetado/`: añade el paso de
copia con lista blanca por patrón y una comprobación de cobertura que avisa si el manuscrito
cita un anexo que no viajó. Probado contra un destino de prueba, copia 17 ficheros —los 14
anexos, el índice y la guía— y deja fuera los cuatro renderizados del manuscrito. Ver
`parche_empaquetado/LEEME_parche_suplementos.md`.

**Orden importa.** S11 y S12 no deben añadirse antes de resolver los bloqueantes 1 y 2 y el
punto siguiente: hoy arrastran cifras y clasificaciones desactualizadas.

## Punto 4 — Un fichero obsoleto contamina la estratificación de conflictos

`quality_reports/orden_de_extraccion.csv` (11-08) declara 65 estudios con texto completo y
59 sin. Los escalares canónicos de `quality_reports/synthesis_scalars.json` (25-08) dicen
91 y 33. El censo de identificadores del CSV sigue siendo válido; su columna de estado
documental, no.

**No contamina el manuscrito ni las cuatro tablas de esta carpeta.** Se verificó: las
cifras 91/33 se derivan del inventario en disco, no de ese CSV, y `tabla_2_completitud.csv`
reproduce los escalares canónicos sin desviación.

**Sí contamina S12.** `resolve_mechanical_conflicts.py` (líneas 62, 134-135, 171) usa la
columna caducada para clasificar cada desacuerdo según haya o no texto que consultar. Con
el estado real en disco, el bloque de «no consultables» pasa de 264 a 20 desacuerdos: unos
244 quedan hoy archivados como irresolubles cuando el artículo sí está disponible.

**Acción.** Que `resolve_mechanical_conflicts.py` lea el inventario en disco —o
`synthesis_scalars.json`— en lugar de `orden_de_extraccion.csv`, reejecutarlo, y regenerar
S12. Marcar el CSV como instantánea histórica para que no vuelva a usarse como fuente.

## Punto 5 — Un estudio clasificado como solo-registro sí tiene publicación

`NCT00937274` figura en el corpus como solo-registro, pero tiene publicación indexada: un
ensayo aleatorizado de fagoterapia oral en diarrea infantil (*EBioMedicine*, 2016;
PMID 26981577). Es un error de clasificación sobre 39 registros cribados.

**Acción.** Reclasificar el estudio y comprobar si su reclasificación mueve alguna cifra
del diagrama de flujo.

## Punto 6 — Inconsistencias internas del texto

| Dónde | Problema |
|---|---|
| Recuento de fuentes | El texto dice «ocho bases» en un sitio y «nueve fuentes» en otro |
| Discusión | Una expresión fraccionaria de la proporción de comparativos no coincide con lo medido en Resultados |
| Cuerpo del texto | Artefactos de gestor bibliográfico y marcadores de plantilla sin resolver |
| Tablas suplementarias | Términos sin tilde (detalle en `auditoria_ortografia.csv`) |
| Anexo PRISMA | El ítem 17 se declara CUMPLE, pero no existe la tabla estudio por estudio que lo respalda |

## Oportunidad — Análisis de sesgo de publicación

Los 60 estudios solo-registro admiten convertirse en una medida con intervalo de confianza
en lugar de una observación cualitativa. El análisis está hecho y el texto propuesto,
redactado: eleva el ítem 21 de PRISMA de PARCIAL a CUMPLE y es un desenlace de
meta-investigación citable por sí mismo. Requiere decidir antes la conciliación de
denominadores que el propio texto propuesto señala.

---

## Orden recomendado

1. Regenerar el cálculo de concordancia y propagar la cifra a los tres sitios (bloqueante 1).
2. Añadir al manuscrito el párrafo de concordancia y regenerar S11 (bloqueante 2).
3. Corregir la fuente de `resolve_mechanical_conflicts.py` y regenerar S12 (punto 4).
4. Añadir el paso de copia de suplementos al script de empaquetado (bloqueante 3).
5. Corregir las inconsistencias de texto y la reclasificación (puntos 5 y 6).
6. Reejecutar `build_jsr_submission.py` y verificar que la carpeta lleva los 14 anexos.
