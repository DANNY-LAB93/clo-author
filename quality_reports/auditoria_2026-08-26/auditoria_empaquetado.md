# Auditoría del empaquetado del envío a *Journal of Science and Research*

**Fecha de la auditoría:** 26 de agosto de 2026
**Alcance:** proyecto `clo-author` (carpeta A) y paquete `Envio_JSR_Fagoterapia_Pseudomonas` (carpeta B), ambos leídos en modo solo lectura. Todo el análisis se hizo sobre copias en el espacio de trabajo; no se escribió, modificó ni borró nada en A ni en B.

Cada afirmación cita fichero y línea. Cuando una cifra se recalculó, se indica que procede de un recómputo propio y no de un fichero publicado.

---

## 1. Qué script construye el paquete y qué declara incluir

**Respuesta: el paquete lo construye `scripts/build_jsr_submission.py`, y ese script no copia ningún suplemento. No hay lista codificada de S3–S13 que los excluya, ni filtro que los descarte: la copia de suplementos no existe como paso en el script.**

Evidencia en `A/scripts/build_jsr_submission.py`:

| Línea | Contenido | Lectura |
|---|---|---|
| 36 | `DESTINO_POR_DEFECTO = pathlib.Path.home() / "Desktop" / "Envio_JSR_Fagoterapia_Pseudomonas"` | El destino por defecto es exactamente la carpeta B. |
| 272–273 | `destino = pathlib.Path(sys.argv[1]) if len(sys.argv) > 1 else DESTINO_POR_DEFECTO` / `destino.mkdir(parents=True, exist_ok=True)` | Crea B si no existe. |
| 396–397 | `docx_out = destino / "manuscrito_JSR.docx"` / `escribe_docx(...)` | Escribe el manuscrito. |
| 402–408 | `for sub, patrones in (("figuras", ("*.png", "*.pdf")), ("tablas", ("*.csv",))):` … `shutil.copy2(f, dst / f.name)` | **El único bucle de copia del script.** Cubre dos subcarpetas —`figuras` y `tablas`— y tres patrones de extensión. No hay una tercera entrada para los suplementos. |

Búsquedas de confirmación sobre `A/scripts/` (todas con cero coincidencias en `build_jsr_submission.py`):

- `grep -rn "S1_lista_PRISMA\|S2_estrategias\|carta_de_presentacion\|LEEME_ANTES"` — ninguna coincidencia en este script.
- `grep -rn "suplement\|SUPLEMENT"` — ninguna coincidencia en este script.
- `grep -rn "verificables"` — ninguna coincidencia en este script.

Los otros tres candidatos quedan descartados como constructores de B:

- **`build_verifiables_package.py`** produce la carpeta `verificables revisión sistemática` dentro de A, no la carpeta B. Su ruta de salida no apunta al escritorio.
- **`build_request_package.py`** genera peticiones de texto completo a biblioteca y a autores; pertenece a la etapa de recuperación documental, no al envío.
- **`build_package_guide.py`** genera `00_GUIA_DEL_MATERIAL_SUPLEMENTARIO.pdf` sobre un catálogo codificado por secciones, y contrasta ese catálogo contra el disco para delatar ficheros no descritos. Describe los suplementos; no los copia a B.

### Cómo llegaron entonces S1, S2 y S7 a la carpeta B

No hay script que los copie. La hipótesis mecánica es una copia manual, y la evidencia la sostiene:

Comparación propia de cada pareja B / `A/verificables revisión sistemática/`, sobre el fichero completo:

| Fichero | Bytes (idénticos) | MD5 en B | MD5 en A | ¿Igual? |
|---|---:|---|---|:-:|
| `S1_lista_PRISMA_2020.docx` | 37 906 | `fbbe53118cc6…` | `2058dd21663b…` | no |
| `S2_estrategias_de_busqueda.docx` | 42 344 | `42d6c4b9450a…` | `993a4ffcba39…` | no |
| `S7_declaraciones_ICMJE.docx` | 36 363 | `dfe511041e08…` | `3f5f7ead1d9c…` | no |

Es decir: **mismo tamaño en bytes, distinto resumen MD5 del fichero completo**. Al abrir cada `.docx` como ZIP y comparar el miembro `word/document.xml`, en cambio, **los tres coinciden byte a byte**. La diferencia está en el envoltorio ZIP —marcas de tiempo de los miembros—, no en el texto.

Eso es la huella de una copia hecha fuera del canal del script: el contenido es el mismo, el contenedor se reescribió.

**Conclusión de la pregunta 1.** La omisión de S3–S6 y S8–S13 no es una lista codificada ni un filtro: es un **paso que no existe** en `build_jsr_submission.py`. Los tres suplementos presentes entraron por una vía que el script no controla. Y esto agrava el problema práctico: `B/LEEME_ANTES_DE_ENVIAR.md` (línea 81) instruye «`python scripts/build_jsr_submission.py`» y su línea 84 advierte que «reescribe esta carpeta entera». Volver a ejecutarlo no añadirá los diez suplementos que faltan; se limitará a regenerar el manuscrito, las figuras y las tablas.

---

## 2. ¿Contamina `quality_reports/orden_de_extraccion.csv` alguna tabla o cifra del envío?

**Respuesta: no. Ninguna cifra del manuscrito ni de las cuatro tablas del envío procede de ese fichero. Pero sí contamina dos anexos suplementarios —y uno de ellos, S12, está entre los que faltan en el paquete.**

### 2.1 El fichero y su discrepancia

`A/quality_reports/orden_de_extraccion.csv` (modificado el 2026-08-11 15:10) tiene **124 filas** y la columna `texto_completo` reparte **65 «si» y 59 «no»** (recuento propio sobre el fichero). Los escalares canónicos de `A/quality_reports/synthesis_scalars.json` (2026-08-25 08:48) dicen `texto_completo_obtenido = 91` y `texto_completo_no_obtenido = 33`.

Cotejo propio del conjunto de identificadores contra el corpus canónico derivado de `A/revision_sistematica/cribado/study_groups.csv`:

- Los **124 identificadores del CSV coinciden exactamente** con los 124 estudios extraíbles canónicos: ninguno sobra, ninguno falta.
- Su columna `texto_completo`, en cambio, **discrepa del estado real en disco en 26 de los 124 estudios**.

Es decir: el censo de estudios sigue vigente; el estado de recuperación documental que declara está caducado.

### 2.2 Por dónde no entra

- **Las cifras 91 / 33 no salen de ahí.** `build_synthesis_scalars.py`, líneas 133–139, las deriva de la intersección entre los estudios extraíbles y el inventario de textos completos en disco (`extraibles & pdfs`). `grep -n "orden_de_extraccion" build_synthesis_scalars.py` devuelve **cero coincidencias**: el generador de escalares no lee ese fichero.
- **Las tablas del envío no lo tocan.** `build_manuscript_tables.py` toma sus cifras de `synthesis_scalars.json` y del cribado. Verificación numérica propia: la `tabla_2_completitud.csv` del paquete B reproduce los escalares canónicos sin desviación —87/70,2 % sin clase de resistencia, 65/52,4 % sin ámbito de patógeno, 71/57,3 % sin vía de administración, 87/70,2 % sin modalidad, 122/98,4 % sin criterio DTR—.
- **El manuscrito tampoco.** La línea 22 de `A/paper/manuscrito_revision_sistematica.md` reporta «texto completo de 91 estudios (73,4 %)», que son los escalares del 25-08, no los 65 del CSV del 11-08.

### 2.3 Por dónde sí entra

`grep -rn "orden_de_extraccion" A/scripts/` da dos consumidores, y los dos importan:

**a) `resolve_mechanical_conflicts.py`, líneas 62, 134–135, 171.** Lee el CSV, construye `tiene_texto = {k: (v.get("texto_completo") == "si") ...}` y en la línea 171 usa `if not tiene_texto.get(r["study_id"], False)` para asignar cada desacuerdo al bloque A («no hay texto que consultar»), B o C. La estratificación completa de los 724 conflictos depende de esa columna caducada.

Recómputo propio de los 724 desacuerdos de `extraction_conflicts.csv`, con las dos fuentes:

| Fuente del estado de texto completo | Bloque A | Bloque B | Bloque C |
|---|---:|---:|---:|
| `orden_de_extraccion.csv` (11-08, el que usa el script) | 264 | 98 | 360 |
| Estado real en disco (recómputo propio) | 20 | 149 | 553 |

El bloque A pasaría de 264 a 20 desacuerdos. Con el CSV caducado, **244 desacuerdos quedan clasificados como «no consultables por falta de texto» cuando el texto sí está en disco**. Eso no es un error de redondeo: es la diferencia entre un conflicto archivado y un conflicto que hay que resolver.

Además, `hoja_de_consenso.csv` (2026-08-13 11:34) contiene **152 filas** repartidas en A=69, B=18, C=65 (recuento propio) —una muestra trabajada, no los 724—, y su reparto por bloques no coincide con ninguna de las dos estratificaciones recalculadas. La hoja publicada es anterior a la versión actual de `extraction_conflicts.csv` (2026-08-23 11:44).

**b) `build_verifiables_package.py`.** Usa el CSV para derivar la columna `en_corpus_actual` del anexo S4. Verificación propia: los 159 registros de `S4_pre_extraccion_desde_resumen.csv` llevan esa columna, y las 124 filas marcadas `si` **coinciden exactamente con el corpus canónico**. Aquí el uso es legítimo: solo se explota el censo de identificadores, que sigue vigente, no la columna caducada.

### 2.4 Alcance real de la contaminación

La cadena contaminada es: `orden_de_extraccion.csv` → `resolve_mechanical_conflicts.py` → estratificación por bloques → `S12_resolucion_de_conflictos.pdf` (generado por `build_extraction_verifiables.py`, líneas 40 y 148, que lee `hoja_de_consenso.csv`).

Esa cadena **no llega al manuscrito**. Comprobación por búsqueda en `A/paper/manuscrito_revision_sistematica.md`: los términos «bloque», «152» y «hoja_de_consenso» no aparecen en ninguna línea. La única cifra de extracción que el manuscrito publica es la línea 101 —«Un revisor extrajo los 124 estudios […]; un segundo revisor extrajo de forma independiente 98 de ellos»— y viene del JSON de concordancia, no del CSV caducado.

**Conclusión de la pregunta 2.** El fichero obsoleto **no contamina ninguna cifra del manuscrito ni de las cuatro tablas del envío**. La declaración de `LEEME_ANTES_DE_ENVIAR.md` («ninguna cifra del artículo procede de los cuadernos de extracción») se sostiene en este punto. Lo que sí contamina es la estratificación de conflictos que sustenta S12, con 244 desacuerdos mal clasificados. Como S12 no está en el paquete, esa contaminación no viaja en el envío actual —pero se activaría en el momento de completar el paquete con los suplementos que faltan.

---

## 3. Qué script calcula `quality_reports/extraction_agreement.json` y con qué entradas

**Respuesta: lo calcula `scripts/compare_extractions.py`, a partir de los dos cuadernos `.xlsx` de extracción. No filtra filas ni estudios por ningún criterio de contenido; sí separa deliberadamente la falta de dato del desacuerdo de valor. El JSON publicado está desactualizado respecto de los ficheros que hoy están en disco.**

Localización por `grep -rn "extraction_agreement" A/scripts/`:

- **Escritor:** `compare_extractions.py`, línea 279: `(ROOT / "quality_reports" / "extraction_agreement.json").write_text(...)`.
- **Consumidor:** `build_extraction_verifiables.py`, línea 42 (`ACUERDO = ROOT / "quality_reports" / "extraction_agreement.md"`), que alimenta el anexo S11.

### 3.1 Entradas

Las rutas no están codificadas: llegan por argumento (líneas 122–125: `--a`, `--b`, `--nombre-a`, `--nombre-b`). La invocación canónica está documentada en `A/CLAUDE.md`, línea 71:

```
python scripts/compare_extractions.py --a revision_sistematica/extraccion/extraccion_danny_valdiviezo.xlsx \
                                      --b revision_sistematica/extraccion/extraccion_nataly_trelles.xlsx \
                                      --nombre-a Danny_Valdiviezo --nombre-b Nataly_Trelles
```

Cada cuaderno se lee con `cargar()` (línea 52), que toma la hoja `Extraccion`, traduce las etiquetas de columna al esquema interno vía `CAMPO_DE_ETIQUETA` de `extraction_schema.py`, e indexa por la pareja (identificador de estudio, `arm_id`).

### 3.2 Qué filtra

- **Filas sin identificador:** línea 76, `if not sid: continue`. Es el único descarte de filas.
- **No hay filtro por estudio, por diseño, por disponibilidad de texto completo ni por corpus.** El script compara lo que encuentra en los dos cuadernos.
- **Solo compara la intersección:** línea 129, `comunes = sorted(set(A) & set(B))`. Las filas que existen en un solo cuaderno no entran en la concordancia; se cuentan aparte como desacuerdo de cobertura, no de valor. El propio encabezado del script razona esa decisión: mezclarlas hundiría la kappa atribuyendo a discrepancia lo que es diferencia de granularidad.
- **Celda vacía ≠ desacuerdo:** líneas 146 y 190, `if va is None or vb is None:` con el comentario «mismo criterio: falta ≠ discrepa». Una celda que un revisor no llegó a tocar no cuenta como conflicto.
- **Texto libre no se puntúa:** se lista para revisión visual sin fabricar una cifra de concordancia.

### 3.3 El JSON publicado está desactualizado

`extraction_agreement.md` declara «Generado el 2026-08-23 por `scripts/compare_extractions.py`», y el commit `cbf678d` (08-23 11:44) lo confirma. Pero `extraccion_nataly_trelles.xlsx` se modificó el **2026-08-25 23:31**, dos días después, y `git status` lo muestra como modificado sin confirmar.

Recómputo propio reimplementando la carga y el conteo del script sobre los ficheros que hoy están en disco:

| Magnitud | JSON publicado (23-08 11:44) | Recómputo sobre el disco (26-08) |
|---|---:|---:|
| Filas revisor A | 132 | 132 |
| Filas revisor B | 129 | 130 |
| Filas comparadas (comunes) | 128 | 129 |
| Estudios extraídos por A | 124 | 124 |
| Estudios extraídos por B | **98** | **104** |
| Estudios en ambos | **98** | **104** |

**Consecuencia directa sobre el envío.** La cifra «98» que el JSON publica aparece en dos lugares del paquete:

- `A/paper/manuscrito_revision_sistematica.md`, línea 101: «un segundo revisor extrajo de forma independiente 98 de ellos».
- `A/scripts/build_jsr_submission.py`, línea 358: el marcador de autoría de N. Trelles, que justifica su contribución sustancial ICMJE con «extrajo 98 de …». Ese texto se inyecta en `manuscrito_JSR.docx`.
- `B/LEEME_ANTES_DE_ENVIAR.md`, punto 3: «extrajo 98 de los 124 estudios de forma independiente».

Según los cuadernos actuales, el número es **104**, no 98. La cifra no está inventada —viene del JSON, que se generó correctamente el 23 de agosto— pero el cuaderno cambió después y el JSON no se regeneró. Dado que la cifra sustenta un argumento de autoría ICMJE en un caso de coautoría no resuelta, conviene volver a ejecutar `compare_extractions.py` antes de enviar y decidir con el número correcto.

*Precisión sobre el alcance de este recómputo:* reimplementé la lectura de los cuadernos y el recuento de filas y estudios reutilizando el esquema de extracción del propio proyecto. No recalculé las kappas ni los porcentajes de acuerdo. No puedo afirmar, con la evidencia reunida, si las 724 discrepancias, la kappa mediana de 0,30 o el acuerdo mediano del 69 % cambian con el cuaderno actualizado; lo que sí está establecido es que su entrada cambió.

---

## 4. Inventario de los suplementos

El detalle completo está en `inventario_suplementos.csv`. Resumen:

La carpeta `A/verificables revisión sistemática/` contiene **21 ficheros**: los 14 anexos S0–S13 en **15 ficheros** (S3 son dos: `S3_decisiones_etapa2_titulo.csv` y `S3_decisiones_etapa3_resumen.csv`, tal como el manuscrito declara en su línea 256), el índice `00_INDICE.docx`, la guía `00_GUIA_DEL_MATERIAL_SUPLEMENTARIO.pdf`, y cuatro renderizados del manuscrito en `.docx` y `.pdf`.

| Anexo | Fichero | Bytes | Modificado | ¿En el envío? | Cita en el manuscrito |
|---|---|---:|---|:-:|---|
| S0 | `S0_informe_editorial.docx` | 39 655 | 2026-08-20 07:44 | **no** | líneas 10, 253 |
| S1 | `S1_lista_PRISMA_2020.docx` | 37 906 | 2026-08-25 08:48 | sí | línea 254 |
| S2 | `S2_estrategias_de_busqueda.docx` | 42 344 | 2026-08-25 08:48 | sí | línea 255 |
| S3 | `S3_decisiones_etapa2_titulo.csv` | 2 269 090 | 2026-08-10 19:57 | **no** | líneas 83, 230, 256 |
| S3 | `S3_decisiones_etapa3_resumen.csv` | 89 150 | 2026-08-11 11:27 | **no** | líneas 83, 230, 256 |
| S4 | `S4_pre_extraccion_desde_resumen.csv` | 69 412 | 2026-08-25 08:48 | **no** | líneas 230, 257 |
| S5 | `S5_listado_184_estudios.csv` | 48 671 | 2026-08-25 08:48 | **no** | líneas 83, 258 |
| S6 | `S6_auditoria_controles_positivos.docx` | 36 694 | 2026-08-25 08:48 | **no** | línea 259 |
| S7 | `S7_declaraciones_ICMJE.docx` | 36 363 | 2026-08-25 08:48 | sí | línea 260 |
| S8 | `S8_recuperacion_texto_completo.csv` | 16 767 | 2026-08-17 22:26 | **no** | línea 261 |
| S9 | `S9_idioma_por_informe_y_clase_de_evidencia.csv` | 70 484 | 2026-08-11 08:46 | **no** | línea 262 |
| S10 | `S10_idioma_verificado_sobre_texto_completo.csv` | 16 335 | 2026-08-13 14:54 | **no** | línea 263 |
| S11 | `S11_concordancia_entre_extractores.pdf` | 5 579 | 2026-08-20 07:44 | **no** | línea 264 |
| S12 | `S12_resolucion_de_conflictos.pdf` | 8 381 | 2026-08-20 07:44 | **no** | línea 265 |
| S13 | `S13_reglas_de_extraccion_de_desenlaces.pdf` | 14 058 | 2026-08-20 07:44 | **no** | líneas 10, 266 |
| — | `00_GUIA_DEL_MATERIAL_SUPLEMENTARIO.pdf` | 8 344 | 2026-08-20 07:44 | **no** | línea 268, sin nombrar el fichero |
| — | `00_INDICE.docx` | 37 069 | 2026-08-19 23:03 | **no** | no |

**Los 14 anexos están citados en el manuscrito; 11 de ellos no están en el paquete.** Presentes: S1, S2, S7. Ausentes: S0, S3 (ambos ficheros), S4, S5, S6, S8, S9, S10, S11, S12, S13, más el índice y la guía.

Discrepancias documentales que conviene resolver antes de enviar:

- La línea 10 del manuscrito declara «Material suplementario: 14 anexos (S0–S13) y su guía». El paquete lleva 3 anexos y ninguna guía. Un revisor que cuente los adjuntos verá la contradicción en la primera página.
- El manuscrito cita S12 por su título («Resolución de conflictos de extracción», línea 265). Ese anexo es precisamente el afectado por la estratificación caducada de la pregunta 2. Añadirlo al paquete sin regenerar `resolve_mechanical_conflicts.py` metería en el envío 244 desacuerdos mal clasificados.
- S11 se apoya en `extraction_agreement.md`, cuyo origen está desactualizado respecto de los cuadernos actuales (pregunta 3).
- Cuatro renderizados del manuscrito (`manuscrito_es.docx`, `manuscript_en.docx`, y sus dos PDF) conviven en la carpeta de verificables sin ser anexos. No son material suplementario; conviene no confundirlos con él al armar el paquete.

---

## Lo que esta auditoría no puede establecer

Por honestidad sobre los límites de la evidencia reunida:

- **Quién copió S1, S2 y S7 a la carpeta B, y cuándo.** La evidencia de contenido idéntico con envoltorio ZIP distinto es compatible con una copia manual, pero no identifica al agente ni el momento. No hay registro en el historial de versiones que lo documente, porque B está fuera del repositorio.
- **Si las kappas y los porcentajes de acuerdo del JSON de concordancia cambian con el cuaderno actualizado.** Solo se recalcularon recuentos de filas y de estudios.
- **Por qué `hoja_de_consenso.csv` tiene 152 filas y no 724.** El reparto por bloques de la hoja no coincide con ninguna de las dos estratificaciones recalculadas, y la hoja es anterior a la versión actual del fichero de conflictos. Puede ser una muestra trabajada a mano, una versión previa, o el resultado de un criterio distinto; con los ficheros leídos no se puede decidir entre esas opciones.
- **Si el portal de la revista exige los suplementos como ficheros separados o en un único adjunto.** Es un requisito del sistema editorial, no del repositorio.
