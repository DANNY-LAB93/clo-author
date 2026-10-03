# CLAUDE.MD — Revisión sistemática de fagoterapia en *P. aeruginosa* MDR

<!-- Manténlo por debajo de ~150 líneas: Claude lo carga entero en cada sesión. -->

**Institución:** Universidad Católica de Cuenca · **Autores:** D. Valdiviezo, N. Trelles
**Revista destino:** Journal of Science and Research (UTB, Ecuador), E-ISSN 2528-8083
**Idioma:** manuscrito, registros de decisión y ficheros de trabajo en español; hay un
manuscrito paralelo en inglés. **Rama:** main.

> **Alcance, desde 2026-08-12.** Este repositorio contiene **solo la revisión
> sistemática**. El metaanálisis se aparcó el 2026-08-10 y su canal se borró el
> 2026-08-12: el argumento del propio manuscrito es que este cuerpo de evidencia no
> admite síntesis cuantitativa. Se recupera con `git checkout b797339 -- metaanalisis/`.
> Lo que sobrevive está documentado en `revision_sistematica/corpus_previo/LEEME.md`.

---

## Principios

- **Ninguna cifra se teclea.** Toda cantidad del manuscrito se cita por nombre desde
  `quality_reports/synthesis_scalars.json`, que escribe `build_synthesis_scalars.py`.
- **Una sola fuente de verdad.** `paper/manuscrito_revision_sistematica.md` es el
  maestro; el inglés, el de la revista y los `.docx` derivan de él.
- **Los registros de decisión son solo-anexar.** Una corrección es una entrada nueva
  encabezada SUPERADO, nunca un borrado.
- **Un grep no es una revisión.** Si hay que verificar contra los PDF, se leen, y se
  dice cuántos se leyeron de verdad.
- **Excluir un estudio es un acto de autoría.** Lo firman los dos revisores; el canal
  no lo hace solo.
- **Nada de maquillar.** Si algo está mal, se corrige y se declara.

---

## Estructura

```
clo-author/
├── paper/                  manuscritos (maestro es./ inglés / JSR), figuras/, tablas/
├── revision_sistematica/   busqueda/ cribado/ textos_completos/ extraccion/ corpus_previo/
├── scripts/                el canal (Python)
├── quality_reports/        decisiones, planes, escalares, auditorías, instantaneas/
├── templates/              registro de decisión, mapa de afirmaciones, log de sesión
└── verificables revisión sistemática/   S0–S24 + guía + ambos manuscritos
```

`quality_reports/instantaneas/` guarda fotos de estados pasados. **Ningún script del
canal lee de ahí**: tienen las mismas columnas que los ficheros vivos y caducan sin
dar error. Ver su `LEEME.md`.

---

## Comandos

```bash
# 0. SI HAY CORRECCIONES NUEVAS: el derivado y sus escalares van antes que todo.
python scripts/ingest_lectura_firmada.py --escribir   # la lectura del 2026-09-30 (idempotente)
python scripts/ingest_firma_lectura.py --escribir     # lo firmado el 2026-10-01 (+ adenda si trae 2 firmas)
python scripts/build_adjudicated_dataset.py
python scripts/build_outcome_scalars.py

# 1. LAS CIFRAS. Siempre lo primero: todo lo de abajo las lee.
python scripts/build_synthesis_scalars.py
python scripts/build_brazo_informe.py          # de que informe salio cada brazo (S20)
python scripts/detecta_solapamiento.py         # pacientes contados dos veces (S21)
python scripts/build_tabla3_completitud.py     # resumen frente a texto completo (S22)
python scripts/build_tabla6_brazos.py          # la Tabla 6 brazo a brazo (S17)
python scripts/build_grupo_comparacion.py      # quien tiene grupo de comparacion DE VERDAD
python scripts/build_concordancia_rob.py       # concordancia entre los dos revisores en RoB
python scripts/audita_pendientes.py            # un juicio por fila, con su frase firmada
python scripts/build_auditoria_scalars.py      # funde los escalares de auditoria
                                               # OJO: despues de los de arriba
                                               # y ANTES de las tablas, que los leen

# 2. LO QUE ENTRA EN EL MANUSCRITO
python scripts/build_manuscript_tables.py      # tablas 1-6
python scripts/build_rob_table.py              # Tabla 5 y TODO el bloque de riesgo de
                                               # sesgo de los tres manuscritos. No
                                               # escribas nada a mano dentro de ese
                                               # bloque: la siguiente pasada lo borra
python scripts/build_lista_anexos.py           # la lista de anexos, en el maestro y el ingles
python scripts/build_criteria_table.py         # la tabla de criterios, y la mete en el .md
python scripts/build_structured_abstract.py    # el resumen; avisa si pasa de 250 palabras
python scripts/build_manuscript_figures.py     # PRISMA y composicion
python scripts/build_conciliacion.py           # informe->estudio->brazo, y las 8 cifras
python scripts/audita_cifras.py                # las 17 cifras, recontadas desde la fuente

# 3. EL PAQUETE DE VERIFICABLES
python scripts/build_verifiables_package.py    # S1-S24 (S11-S13 dentro). Un anexo NUEVO va
                                               # antes que build_lista_anexos, o esta se niega
python scripts/build_readable_annexes.py       # los .xlsx legibles de cada .csv
python scripts/build_editorial_report.py       # S0 y el indice
python scripts/build_package_guide.py          # la guia del paquete

# 4. LOS DOCUMENTOS DERIVADOS. Nadie los corria y por eso viajo un PDF
#    del dia anterior dentro del .zip, con 155 estudios frente a 137.
python scripts/build_maestro_docx.py           # informe_extendido.docx
python scripts/build_resumen_docx.py           # resumen_estructurado.docx
python scripts/build_cesion_datos.py           # datos_carta_cesion.docx
python scripts/build_manuscript_pdf.py         # los PDF del maestro y del ingles
python scripts/build_jsr_pdf.py                # el PDF del manuscrito de la revista

# 5. EL SOBRE
python scripts/build_criteria_table.py         # OTRA VEZ, al final: escribe el .docx
                                               # suelto del sobre y tiene que ser el ultimo
python scripts/build_jsr_submission.py         # al Escritorio
python scripts/zip_jsr_submission.py           # el .zip, comprobado fichero a fichero

# LOS CUATRO GUARDIANES. Los dos primeros contrastan con el canal;
# el tercero rehace las cuentas desde el texto solo; el cuarto mira los DATOS
# y no la prosa, que es donde nadie miraba hasta el 2026-09-16.
python scripts/check_manuscript_numbers.py     # toda cifra tiene origen
python scripts/check_manuscript_claims.py      # cada frase lleva SU escalar
python scripts/check_aritmetica.py             # las cuentas, rehechas
python scripts/check_extraccion.py             # numerador<=denominador, vocabularios, citas
python scripts/sync_manuscript_numbers.py --escribir   # las pone al dia
```

> **El orden importa.** Correrlos desordenados ya borró un anexo una vez.

---

## Estado, a 2026-10-03

Todas las cifras de abajo salen del canal. Re-derívalas antes de fiarte.

| Componente | Estado |
|---|---|
| Búsqueda y cribado | 23 057 registros → 17 129 únicos → 233 informes → 183 valorados → 51 excluidos (27 por el artículo, 17 por la ficha del registro, 7 sin poder leer ninguno) → **132 estudios, 90 extraíbles**, 98 brazos |
| Fuentes | **8 fuentes distintas en 9 brazos de búsqueda** (Scopus va en dos brazos). `fuentes_distintas_n` ≠ `fuentes_brazos_n`: no los confundas |
| Texto completo | 66 de 90 (73,3 %). El hueco está sesgado: retiene el 66,7 % de los diseños comparativos. **No se pide nada a nadie**, por decisión de D.V. del 2026-09-02 |
| Extracción | doble y adjudicada. 124 estudios D.V., 122 N.T. **541 de 541 desacuerdos cerrados**: 539 firmados por consenso, 2 por una regla superada, **0 abiertos** |
| Riesgo de sesgo | **emitido, completo y firmado**: 13 comparativos por diseño —**4 con grupo de comparación**, 3 de fago frente a no fago y **solo 2 con contraste para *P. aeruginosa*** (EST-008 parcial, EST-021)—, 10 evaluables (3 RoB 2, 7 ROBINS-I), 3 sin texto. **74 celdas: 64 de dominio + 10 globales**. Doble lectura en 9 de los 10: acuerdo 83,3 % (55/66), **kappa 0,77**, 11 desacuerdos resueltos por consenso. EST-004 tiene una sola lectura. EST-055 salió el 2026-10-01 (ORG) y con él sus 8 juicios |
| Lectura del 2026-09-30 | **firmada e ingerida**, y lo abierto **firmado el 2026-10-01**: 9 sin ningún paciente con *P. aeruginosa* tratado → **4 excluidos (ORG)**, 5 mantenidos y declarados (EST-152 y EST-170 solo la nombran al citar a EST-049 y EST-106). 35 + 7 correcciones. Bajo el umbral: 8 brazos, 6 estudios enteros, 5 mantenidos por firma. **Solapamiento: 20 pacientes en 18 estudios**, 31 pares. Leyeron los dos autores; las 23 figuras las comprobaron ellos |
| Manuscrito | maestro 8 931 palabras de cuerpo; 295 anclas, todas al día. Pasa del límite de 3 500 de CMI |
| Anexos | **S0–S24 (25 documentos)** + guía + índice. Los de datos viajan dos veces: `.xlsx` para leer, `.csv` para rehacer |
| Sobre JSR | `~/Escritorio/Envio_JSR_Fagoterapia_Pseudomonas/`. Manuscrito, carta, LEEME, 8 ficheros de tablas, 4 de figuras (2 figuras en `.pdf` y `.png`), 30 suplementos |

**Lo que falta, y es de los autores:** la adenda `~/Desktop/FIRMAR_adenda_lectura_2026-10-03.xlsx` (excluir EST-132 y mantener EST-106: hoy solo las firma D.V.); los dos ORCID, el grado académico de ambos, el
correo de N. Trelles (un marcador en `manuscrito_JSR_final.md:11`), la aprobación ICMJE
escrita de N.T. sobre la versión final, los dos formularios obligatorios de la revista,
y el registro en PROSPERO (que sigue sin hacerse y el manuscrito declara así).

---

## Lo que hay que saber antes de tocar nada

1. **Las cifras publicadas vienen de DOS sitios.** Tablas 1–4 y el PRISMA, de `cribado/`
   y `pre_extraccion_desde_resumen.csv`; las de desenlaces, de la extracción adjudicada
   vía `build_adjudicated_dataset.py` → `build_outcome_scalars.py`. El titular: **69 de
   102 brazos (67,6 %) no definen éxito clínico**, y solo 2 pasan los cuatro requisitos
   para agrupar — uno de ellos mide tiempo, así que no queda ninguno. **GRADE no se hace
   y no se hará**: no hay estimador agrupado cuya certeza calificar.

2. **Dos medidas de «antes» que no se mezclan.** La enmienda de idioma y la relectura de
   textos completos quitaron estudios cada una. Usa `*_antes_de_la_enmienda` (antes del
   idioma) y `*_antes_de_releer` (después del idioma, antes de releer).

3. **El idioma se juzga sobre el CUERPO y con la traducción automática APAGADA.** Chrome
   tradujo solo un artículo ruso al español durante esta misma comprobación. El criterio
   se había verificado sobre el resumen para 29 de 98 estudios; cuatro rusos entraron
   así y salieron el 2026-09-01 (código IDI, 78–94 % de cirílico medido).

4. **NOREC es una enmienda de otra clase.** Los demás códigos hablan de lo que el
   artículo DICE; `NOREC` habla de lo que esta revisión NO PUDO LEER. Se aplica a un
   estudio (EST-118). Extenderlo a los 24 sin texto hundiría el corpus a 113, los
   comparativos a 5 y los ECA a 3, y dejaría la recuperación en 100 % **por
   construcción**, destruyendo el sesgo que §3.2 mide. No lo extiendas sin releer eso.

5. **Un fichero derivado no sobrevive a sus datos.** Una prueba dejó
   `rob_comparativos_scalars.json` con 82 juicios inventados firmados «PRUEBA A y
   PRUEBA B», y se llegó a commitear. `build_rob_table.py` lo reconcilia en cada pasada.

6. **Tres manuscritos, un solo estado.** `rob_bloques.py` guarda los bloques de riesgo de
   sesgo del maestro y del inglés; `build_rob_table.py` escribe los tres a la vez. El
   maestro llegó a decir «no se realizó» mientras el de la revista declaraba una
   evaluación en curso, y los dos viajaban en el mismo sobre.

7. **Dos guardas en el comparador de extracciones, ninguna quitable.** Reescribía el
   fichero de conflictos con las columnas de resolución EN BLANCO (habría borrado 561
   firmas), y hasta el 2026-08-23 contaba como desacuerdo una casilla que uno rellenó y
   el otro no: ningún recuento anterior a `ca12d6a` es comparable.

8. **29 fichas de registro no decían qué organismo se trata, y el asunto está cerrado.**
   Se bajaron enteras (`revision_sistematica/textos_completos/registros/`, 25 de
   ClinicalTrials.gov y 4 de CTIS) y se leyeron una a una: **12 cumplen y se quedan, 17
   no y están excluidas**. Los dos autores firmaron dos veces el 2026-09-14: primero las
   10 con código existente (8 ORG, 2 OFF), luego las **7 que obligaron a un código nuevo**.
   **NOORG** es el undécimo código y es hermano de NOREC — los demás excluyen por lo que
   el estudio DICE, NOREC por lo que no se pudo LEER y NOORG por lo que el registro no
   DECLARA. Al leerlas apareció un duplicado: Phage4Cure-001 estaba en CTIS con dos
   identificadores y entró como dos estudios; EST-187 se fusionó en EST-186. El corpus
   fue 155 → 145 → 137. La evidencia literal está en
   `quality_reports/registros_organismo_verificado.csv`; los dos registros de decisión
   del 2026-09-14 lo cuentan entero.

9. **Los tres guardianes miran AHORA los dos manuscritos.** Hasta el 2026-09-15
   `check_manuscript_numbers.py` solo leía el maestro, y el de la revista —el único
   que viaja— no lo miraba nadie: seguía diciendo 184 estudios evaluados, 39
   exclusiones, 145 en el corpus y un 77,7 % de eventos adversos, todo superado,
   mientras su propio resumen ya daba las cifras nuevas. Ahora comprueba los dos por
   defecto, salta la lista de referencias Vancouver y hay **8 anclas nuevas sobre el
   cuerpo** del manuscrito de la revista, no solo sobre su resumen.

10. **`check_aritmetica.py` no consulta el canal, recalcula.** Los otros dos verifican
   contra los escalares, así que un escalar bien calculado y mal redactado en su frase
   les pasa (68,0 % donde era 68,9; «casi cuatro de cada diez» para 44,2 %). Este rehace
   la división, las restas del PRISMA y las sumas declaradas desde el texto solo.

12. **`extraccion_adjudicada.csv` es un DERIVADO.** Lo rehace
    `build_adjudicated_dataset.py` desde los dos cuadernos y borra cualquier cosa
    escrita ahí a mano. Una corrección posterior a la adjudicación entra por
    `correcciones_tras_texto_completo.csv`, con valor anterior, cita literal y firma.
    Editar el CSV de salida funciona hasta la siguiente pasada del canal, y entonces
    desaparece sin avisar: pasó el 2026-09-22 con las cuatro correcciones de la
    auditoría.

13. **El bloque de riesgo de sesgo lo posee `build_rob_table.py` entero.** Lo que haya
    entre `### Riesgo de sesgo` y el pie de la Tabla 5 se reescribe en cada pasada. Tres
    frases escritas a mano ahí dentro —la coherencia de los globales, el desglose de las
    celdas y en qué se apoya cada juicio— se perdieron así el 2026-09-22. Ahora las
    genera el guion; **no escribas nada a mano en ese bloque**.

14. **El manuscrito en inglés ya está al día, y ahora lo vigilan.** Iba dos revisiones
    del corpus atrás —«Of the 145 studies», «184 studies evaluated», 219, 179, 123— y su
    lista de anexos estaba **en español** y citaba 16 de los 24 que viajan. No va en el
    sobre ni en el `.zip`, y por eso ningún guardián lo miraba. Desde el 2026-09-22
    `check_manuscript_numbers.py` comprueba **los tres** manuscritos, la lista de anexos
    la escribe `build_lista_anexos.py` para el maestro y el inglés a la vez, y las
    afirmaciones ancladas pasaron de 131 a 217.

15. **Una cifra escrita EN LETRA se escapa de los guardianes.** Los tres buscan dígitos,
    y la sección 3.1.1 enumera las exclusiones con palabras: al salir EST-063 se
    volvieron falsas «Veintinueve», «Veinticuatro» y «Cuatro son protocolos», las tres a
    la vez y en los tres manuscritos, sin que nada fallara. Un hueco `{letras_<escalar>}`
    en una afirmación se resuelve ahora como la palabra, en el idioma del manuscrito.

16. **Una cifra puede estar «respaldada» por casualidad.** `check_manuscript_numbers.py`
    solo mira si el valor existe en los escalares, no si es el escalar que toca: «46»,
    «71», «18» y «95» pasaban porque esos números existen con otro significado. La
    defensa real son las anclas de `check_manuscript_claims.py`, que atan cada frase a SU
    escalar. Si añades una cifra al manuscrito, ánclala.

17. **El cribado NO lo hizo Rayyan, y confundirlo falsifica los Métodos.** Las etapas 2
    y 3 —13 894 títulos y 460 resúmenes— las condujo **un solo revisor humano (D.V.),
    sin duplicación**, y las decisiones registro a registro **las emitió Claude Opus 5**.
    Rayyan se usó **solo** en el recribado ciego de los 350 excluidos, que es la
    validación, y ahí sí lo hicieron los dos autores. Un encargo externo del 2026-09-23
    pedía describir Rayyan como la herramienta de cribado; aplicarlo habría convertido
    una declaración correcta en una falsa.

18. **La concordancia en riesgo de sesgo SÍ se puede medir, y se mide.** El manuscrito
    afirmó hasta el 2026-09-23 que «no admite medida de concordancia». Los dos cuadernos
    individuales existen y difieren en 12 juicios sobre el corpus vigente. Antes de
    escribir que algo no se puede calcular, mira si el fichero está ahí.

19. **La lectura del 2026-09-30 vive en `revision_sistematica/lectura_pendiente/`, no en
    `quality_reports/`.** `build_trabajo_pendiente.py` escribe el cuaderno EN BLANCO en
    `quality_reports/pendiente_lectura.xlsx` y lo habría pisado relleno; ahora se niega
    y escribe `_nuevo`. La traducción del texto firmado a categorías está en
    `ingest_lectura_firmada.py`, con una guarda por estudio. Lo que deja un brazo con
    más de un valor NO se aplica: va al cuaderno de firma. El solapamiento se cuenta
    por PERSONA (`P1`…`P20`), no por fila: por fila salían 22 donde son 20.

11. **Reejecutar `group_reports_into_studies.py` renumeraba estudios, y ya no.** La
    numeración estable se anclaba en la CLAVE del estudio, y la clave cambia sola en
    cuanto `fulltext_identifiers.csv` resuelve un DOI: el 2026-09-14 EST-133 y EST-188 se
    convirtieron en EST-220 y EST-221 sin que nada fallara. Ahora el ancla son los
    `record_id`, que se derivan del contenido: si el grupo de hoy comparte un informe con
    un estudio de ayer, es ese estudio. Reejecutarlo es idempotente — compruébalo con
    `git diff` sobre `study_groups.csv`.
