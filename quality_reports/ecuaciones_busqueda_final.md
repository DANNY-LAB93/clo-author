# Ecuaciones de búsqueda — revisión sistemática
### Fagoterapia para *Pseudomonas aeruginosa* MDR/XDR/PDR

**Estado:** documento operativo. Sustituye a la planificación previa al abandono del metaanálisis.
**Última verificación del inventario de bases:** 2026-08-04, contra el portal de la Biblioteca Virtual UCACUE autenticado.

---

## 1. Qué bases hay, y cuáles no

El inventario completo del portal devuelve **83 recursos**. Se enumeró de forma exhaustiva, no por búsqueda parcial, y cada ausencia se comprobó con control positivo (`scopus` → Scopus) para descartar que el filtro estuviera fallando.

### Bases utilizables

| # | Base | Acceso | Papel en la revisión |
|---|---|---|---|
| 1 | PubMed / MEDLINE | libre | Núcleo biomédico |
| 2 | Scopus | institucional | Cobertura multidisciplinar; en la ronda previa duplicó el corpus elegible |
| 3 | ProQuest + Prisma | institucional | Literatura gris y tesis |
| 4 | Biblioteca Cochrane (CENTRAL) | institucional | Ensayos; incorpora registros de Embase y de ClinicalTrials.gov |
| 5 | BVS (LILACS, CUMED, BINACIS…) | libre | Literatura regional no indexada en MEDLINE ni Scopus |
| 6 | SciELO | libre / portal | Literatura iberoamericana; solapa parcialmente con BVS |
| R1 | ClinicalTrials.gov | libre | Registro de ensayos |
| R2 | CTIS | libre | Registro de ensayos UE (post-2022) |
| R3 | EudraCT | libre | Registro de ensayos UE (pre-2022) |

### Bases confirmadas como NO disponibles

| Base | Filtro aplicado | Resultado |
|---|---|---|
| **Embase** | `embase` | Sin resultados |
| **Web of Science** | `clarivate`, `web` | Sin resultados / sólo WebSurg y Fielweb |
| **EBSCO bibliográfica** | `ebsco` | Sólo *eBooks Collection* y *eBooks Engineering Core* |

**Embase es la limitación material** y debe declararse en Métodos. Está mitigada **solo para ensayos controlados**, porque Cochrane realiza sus propias búsquedas sistemáticas en Embase y deposita esos registros en CENTRAL — y los registros de CENTRAL lo confirman: 50 de sus 226 llevan una accesión `EMBASE` en el campo `C3`. CENTRAL no contiene reportes de caso, que son ~90 % de este corpus, así que la mitigación no puede enunciarse más ancha que eso.

### Nota sobre Ovid Medline

`Ovid Medline` **sí** está en el portal. **No se cuenta como fuente adicional**: es MEDLINE, el mismo contenido que PubMed con otra interfaz. Contarla duplicaría registros en la casilla de identificación del PRISMA sin añadir un solo estudio. Se menciona aquí para dejar constancia de que la decisión fue deliberada.

---

## 2. Las cuatro reglas de diseño

Se aplican a todas las ecuaciones y explican por qué no se parecen a las de una búsqueda convencional.

**R1 — Dos brazos, y el brazo B omite el organismo.** El brazo A ancla en *P. aeruginosa*. El brazo B **no menciona el organismo en absoluto**, porque varios estudios elegibles son cohortes multipatógeno que no lo nombran en título, resumen ni vocabulario controlado. Ninguna consulta anclada en el organismo puede recuperarlos. En la validación previa, el brazo A cubría 36 de 40 estudios incluidos y el brazo B 29; **solo la unión cubría los 40**.

**R2 — Ningún término de resistencia es obligatorio.** El criterio de población retiene explícitamente los brazos sin documentación de resistencia. Una búsqueda no puede exigir una palabra clave para encontrar estudios que después incluye porque esa palabra nunca se registró. Exigirla costó, en la ronda 5, tres estudios elegibles que ninguna consulta ejecutada podía recuperar.

**R3 — Vocabulario controlado además de texto libre.** En PubMed, `[tiab]` **suprime el mapeo automático a MeSH**. Una ecuación construida solo con `[tiab]` nunca usa vocabulario controlado, aunque parezca que sí. Los descriptores se añaden de forma explícita.

**R4 — `phage*`, nunca `phag*`.** `phage*` expande a *phage, phages, phagemid*. `phag*` arrastra toda la literatura de fagocitosis, que empieza por *phago-*.

---

## 3. Ecuaciones por base

### 3.1 PubMed / MEDLINE — ejecutada

```
# Bloque organismo (ORG)
("Pseudomonas aeruginosa"[tiab] OR "P. aeruginosa"[tiab]
 OR "Pseudomonas aeruginosa"[MeSH])

# Bloque intervención (PHAGE)
("phage"[tiab] OR "bacteriophage"[tiab] OR "phage therapy"[tiab]
 OR "bacteriophage therapy"[tiab] OR "phagotherapy"[tiab]
 OR "Bacteriophages"[MeSH] OR "Phage Therapy"[MeSH])

# Bloque diseño (CLIN)
(case reports[pt] OR clinical trial[pt] OR observational study[pt]
 OR comparative study[pt] OR multicenter study[pt] OR journal article[pt])

# Ventana
("2016"[dp] : "2026"[dp])

BRAZO A:  ORG AND PHAGE AND CLIN AND ventana
BRAZO B:  PHAGE AND humans[mh] AND ventana
```

| | Registros |
|---|---|
| Brazo A | 1 481 |
| Brazo B | 8 532 |
| **Unión (corpus)** | **9 561** |

### 3.2 Scopus — contada, pendiente de exportar

Scopus no tiene vocabulario controlado, así que ambos brazos son texto libre y el brazo B necesita un límite por área temática para ser manejable.

**Brazo A**
```
TITLE-ABS-KEY ( ( "Pseudomonas aeruginosa" OR "P. aeruginosa" OR pseudomonal )
  AND ( phage* OR bacteriophage* OR phagotherap* OR "phage therapy"
        OR "phage cocktail" OR pyophage OR intestiphage ) )
AND PUBYEAR > 2015 AND PUBYEAR < 2027
```

**Brazo B**
```
TITLE-ABS-KEY ( ( phage* OR bacteriophage* OR phagotherap* )
  AND ( "phage therapy" OR "bacteriophage therapy" OR compassionate OR salvage
        OR "expanded access" OR "named patient" OR "case report" OR "case series"
        OR patient OR patients OR clinical ) )
AND PUBYEAR > 2015 AND PUBYEAR < 2027
AND ( LIMIT-TO ( SUBJAREA , "MEDI" ) OR LIMIT-TO ( SUBJAREA , "IMMU" )
      OR LIMIT-TO ( SUBJAREA , "PHAR" ) )
```

| | Registros |
|---|---|
| Brazo A | 2 875 (reconfirmado 2026-08-04) |
| Brazo B | 9 372 |

> **⚠️ Trampa 1 — el traductor de Chrome reescribe la consulta.** Al escribir en la caja de Scopus, el traductor de página cambió **el valor real del campo**, no solo su apariencia: `phage*`→`fago*`, `AND`→`Y`. La búsqueda se habría ejecutado con una ecuación que nadie escribió y habría devuelto un número plausible. **Pasar la consulta como parámetro de URL a `results.uri`**, nunca teclearla.
>
> **⚠️ Trampa 2 — exportar pide cuenta personal.** Buscar funciona con acceso institucional; el botón *Export* responde *"To use this feature you must have a Scopus account"*. El botón *Download*, contiguo, **está sin probar**. Si también la pide, la alternativa es leer la lista paginada de resultados, que da título, autores, año, fuente y DOI sin cuenta alguna.

### 3.3 ProQuest — contada, pendiente de exportar

Códigos de campo: `TI`, `AB`, `SU`, `NOFT` (todo excepto texto completo).

**Brazo A**
```
(TI("Pseudomonas aeruginosa" OR "P. aeruginosa") OR AB("Pseudomonas aeruginosa" OR "P. aeruginosa") OR SU("Pseudomonas aeruginosa"))
AND
(TI(phage* OR bacteriophage* OR phagotherap*) OR AB(phage* OR bacteriophage* OR phagotherap*) OR SU(bacteriophages))
AND pd(20160101-20261231)
```

**Brazo B**
```
(TI(phage* OR bacteriophage*) OR AB(phage* OR bacteriophage*) OR SU(bacteriophages))
AND
(AB("phage therapy" OR "bacteriophage therapy" OR compassionate OR salvage
    OR "case report" OR "case series" OR patient*))
AND pd(20160101-20261231)
```

| | Registros |
|---|---|
| Brazo A, por defecto | 998 |
| **Brazo A, con "fuera de la suscripción" activado** | **1 012** |
| Brazo B | 3 403 |

> **⚠️ Marcar "Mostrar resultados fuera de la suscripción de mi biblioteca".** Está desactivado por defecto, y dejarlo así devuelve **lo que esta biblioteca puede leer, no lo que existe** — un filtro de disponibilidad aplicado antes del cribado, que no es defendible en una revisión sistemática. Aquí mueve la cifra de 998 a 1 012. El tamaño del efecto no es el argumento: no es medible por adelantado y varía con el tema.
>
> **No marcar** "Texto completo" ni "Evaluado por expertos": el primero es otro filtro de disponibilidad y el segundo eliminaría reportes de caso publicados en revistas no indexadas.
>
> La ecuación se introduce en la primera fila de la búsqueda avanzada; el selector de campo puede quedarse en "Cualquier campo" porque los códigos van explícitos dentro de la consulta. La caja es un `<textarea>` real, de modo que el riesgo del traductor es menor que en Scopus, pero conviene igualmente verificar el valor antes de ejecutar.

### 3.4 Cochrane CENTRAL — ejecutada y descargada

Gestor de búsquedas, una línea por fila:

```
#1  MeSH descriptor: [Pseudomonas aeruginosa] explode all trees
#2  MeSH descriptor: [Pseudomonas Infections] explode all trees
#3  ("Pseudomonas aeruginosa" OR "P aeruginosa" OR pseudomonal):ti,ab,kw
#4  #1 OR #2 OR #3
#5  MeSH descriptor: [Bacteriophages] explode all trees
#6  ("phage" OR "phages" OR bacteriophage* OR phagotherap* OR "phage therapy"
     OR "phage cocktail" OR Pyophage OR Intestiphage):ti,ab,kw
#7  #5 OR #6
#8  #4 AND #7          <- brazo A
#9  #7                 <- brazo B: todo registro de fagos en CENTRAL
```

Límite: *CENTRAL Trials only → Original publication year*, entre 2016 y 2026. Mantener activada *Search word variations* (viene activada por defecto).

| | Ensayos |
|---|---|
| Brazo B, sin límite de fecha | 304 |
| **Brazo B, 2016–2026 (exportado)** | **226** |

Instantánea a registrar: **«Cochrane Central Register of Controlled Trials, Issue 7 of 12, July 2026»**. Las demás bases de Cochrane —Reviews, Protocols, Editorials, Special Collections, Clinical Answers— devuelven **0**, de modo que CENTRAL es la única que contribuye.

> **⚠️ El fichero se declara UTF-8 y es latin-1.** Leerlo como UTF-8 destruye los acentos (`Brüssow` → `Br?ssow`), que es justo lo que usa el emparejamiento por título en la deduplicación.
>
> **⚠️ El identificador propio está en `C3`, no en `UR`.** `UR` apunta al DOI interno de Cochrane y el NCT aparece en `A1` como si fuera un autor. El campo `C3` contiene pares `PUBMED 30051571`, `EMBASE 628973066`, `CTgov NCT07698002`. Sin leer `C3`, CENTRAL no deduplica contra PubMed ni contra ClinicalTrials.gov: al incorporarlo, los duplicados detectados pasaron de 82 a 145.

### 3.5 BVS — ejecutada y descargada

Términos en español, portugués e inglés, porque los títulos se indexan en su idioma original.

**Bloque de intervención, en solitario**
```
(fago OR fagos OR bacteriofago OR bacteriófago OR bacteriofagos OR fagoterapia
 OR phage OR phages OR bacteriophage OR bacteriophages OR "phage therapy"
 OR "terapia con fagos" OR "terapia fágica")
AND NOT db:("MEDLINE")
```

| | Registros |
|---|---|
| Bloque de intervención, todo BVS | 2 455 |
| MEDLINE dentro de ese total | 1 817 |
| **No duplicante (exportado)** | **638** |

Composición de los 638: LILACS 417, VETINDEX 89, CUMED 50, BINACIS 46, Sec. Est. Saúde SP 44, non-MEDLINE 26, MedCarib 17, Coleciona SUS 12, BBO 11.

> **⚠️ No ejecutar el brazo B en BVS.** Su bloque clínico —*paciente*, *clínico*, *humano*, *case report*— no discrimina en una base cuyo contenido entero es clínico, y la pestaña topa en 999 en vez de dar un conteo real.
>
> **⚠️ Excluir MEDLINE por consulta, no por clic**, para que quede reproducible en una URL. Control aritmético: 2 455 − 1 817 = 638 exacto, lo que demuestra que la cláusula actuó y no falló en silencio.
>
> **⚠️ Los PMID vienen con prefijo `mdl-`** en la etiqueta `ID` (`ID  - mdl-42450545`). Sin traducir ese prefijo, los 26 registros de origen PubMed se contarían dos veces.

### 3.6 SciELO — contada 2026-08-04, pendiente de exportar

```
fago OR fagos OR bacteriofago OR bacteriófago OR bacteriófagos OR fagoterapia
OR phage OR phages OR bacteriophage OR bacteriophages OR "phage therapy"
OR "terapia fágica"
```

| | Registros |
|---|---|
| **Bloque de intervención, en solitario** | **251** |

Mismo criterio que BVS y CENTRAL: la fuente es lo bastante pequeña para cribarla entera, de modo que no se le aplica bloque de organismo ni bloque clínico. La interfaz ofrece **Exportar**. Solapa parcialmente con BVS; la deduplicación por DOI/PMID resolverá el solape.

### 3.7 Registros de ensayos

**ClinicalTrials.gov** — 121 registros (brazo B; el brazo A da 17). Descargado.

**EudraCT** — `bacteriophage OR phage OR phagotherapy` → **3 ensayos**: 2014-000714-65 (PhagoBurn), 2022-003810-35 (BiomX, fibrosis quística) y 2021-004469-11 (PhagoDAIR I). Descargado.

**CTIS** — **10 ensayos**, unión de dos búsquedas. Descargado.

> **⚠️⚠️ El campo "Contain any of these terms" de CTIS no es un OR, y tampoco busca subcadenas.** Dos hallazgos distintos:
>
> 1. `bacteriophage phage` devuelve **0**; `bacteriophage` en solitario devuelve **5**. Añadir un término que debería ampliar la búsqueda la vacía.
> 2. `phage` devuelve **6**, y **solo 1 coincide** con los de `bacteriophage`. La coincidencia es por **palabra completa**: `phage` no encuentra `bacteriophage`.
>
> **Unión real: 10.** Entre los cinco que la búsqueda documentada previamente pasaba por alto está **Phage4Cure-001** (cóctel de fagos nebulizado en colonización pulmonar crónica por *P. aeruginosa*, dos registros), directamente sobre el tema de esta revisión.
>
> **Ejecutar un término por búsqueda y unir a mano.** El fichero `data/raw/ctis_export.csv` lleva una columna `found_by_term` que registra qué búsqueda recuperó cada ensayo.
>
> **Pendiente:** barrer también `phages`, `bacteriophages`, `phagotherapy` y `pyophage`. Con coincidencia por palabra completa, un plural es otro término.
>
> **Control positivo obligatorio.** Antes de dar por bueno cualquier cero en CTIS, ejecutar un término que deba devolver resultados: `cancer` da 3 036. Un cero sin control no es un hallazgo, es una suposición sin probar — y en esta misma revisión un `0` resultó proceder de un campo vacío.

---

## 4. Recuento consolidado

| Fuente | Recuperados | Descargado | Cribado |
|---|---|---|---|
| PubMed (unión de brazos) | 9 561 | ✅ | brazo A completo; **brazo B (5 839) pendiente** |
| Scopus | 12 247 | ❌ | — |
| ProQuest | 4 416 | ❌ | — |
| Cochrane CENTRAL | 226 | ✅ | pendiente |
| BVS | 638 | ✅ | pendiente |
| SciELO | 251 | ❌ | — |
| ClinicalTrials.gov | 121 | ✅ | pendiente |
| CTIS | 10 | ✅ | pendiente |
| EudraCT | 3 | ✅ | pendiente |
| **Total recuperado** | **27 473** | | |

De lo ya descargado —10 559 registros de seis fuentes— la deduplicación deja **10 414 únicos** (145 duplicados). Informe: `quality_reports/deduplication.md`.

**La deduplicación funciona a dos niveles**, porque PRISMA 2020 separa *informes* de *estudios*: el nivel de informe empareja por DOI y PMID y es el único que alimenta la casilla de «duplicados eliminados»; el nivel de estudio añade el NCT y agrupa protocolo y resultados de un mismo ensayo, que **no** son duplicados.

---

## 5. Qué falta

1. **Scopus** — probar *Download*; si pide cuenta, leer la lista paginada. 12 247 registros.
2. **ProQuest** — exportación en lote. 4 416 registros.
3. **SciELO** — exportar los 251.
4. **CTIS** — barrer los plurales pendientes.
5. **Cribar** brazo B de PubMed (5 839), CENTRAL, BVS, SciELO y registros.

---

## 6. Qué declarar en Métodos

- Las **seis bases bibliográficas y los tres registros** efectivamente interrogados, con fecha e instantánea de CENTRAL.
- **Embase no está disponible** en la suscripción institucional, verificado contra el inventario completo del portal. Mitigado **solo para ensayos controlados** vía CENTRAL, que incorpora registros de origen Embase (50 de 226 lo declaran en `C3`).
- **Web of Science y EBSCO bibliográfica tampoco están.** Research4Life lista *Clarivate Current Contents*, un servicio de sumarios sin índice de citas ni búsqueda por campos, que no es Web of Science.
- **Ovid MEDLINE está disponible pero no se contó como fuente adicional**, por ser el mismo contenido que PubMed.
- **Un solo revisor** en cribado y extracción, sin duplicación independiente.
- **La revisión no está registrada** en PROSPERO ni en OSF.
