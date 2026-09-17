# La auditoría de las diecisiete cifras

**Estado:** APLICADO el 16 de septiembre de 2026, salvo cuatro puntos que
**esperan la firma de los dos autores**.
**Ficheros:** `scripts/audita_cifras.py`, `scripts/build_tabla3_completitud.py`,
`scripts/build_auditoria_scalars.py`, `scripts/build_brazo_informe.py`,
`scripts/detecta_solapamiento.py`, `scripts/check_extraccion.py`,
`scripts/make_firma_auditoria.py`, `paper/manuscrito_JSR_final.md`
**Viene de:** una auditoría externa que pidió reconciliar diecisiete cifras sin
dar ninguna por buena, y de los tres puntos que la auditoría del propio canal
había dejado abiertos.

## Las diecisiete cifras se reproducen

`audita_cifras.py` las vuelve a contar sobre los ficheros de datos, sin leer
`synthesis_scalars.json`, y publica para cada una su unidad, su denominador, su
fuente y el cálculo. **Las diecisiete salen.** Lo que no salía era una
etiqueta.

## Lo que estaba mal

### 1. Los 90 juicios no eran 90 juicios de dominio

3 estudios × 5 dominios de RoB 2 = 15. 9 × 7 de ROBINS-I = 63. Suman **78**.
Los 12 que faltaban son los **juicios globales**, uno por estudio. La cifra 90
era correcta; la etiqueta, no. Corregido en Resultados y anclado.

### 2. La Tabla 6 pedía diseño comparativo para agrupar proporciones

Un metaanálisis de proporciones no exige diseño comparativo. Con ese requisito
dentro, el embudo daba 0 brazos y el manuscrito concluía que ninguno reunía los
requisitos. **Sin él, sobreviven 21 brazos de 18 estudios.**

La conclusión no cambia y el argumento sí: no se agrupó porque **16 de esos 21
tienen un denominador de un solo paciente**, porque las definiciones de éxito
no nombran la misma cosa y porque los productos no son comparables. Eso es una
razón clínica y estadística, no una imposibilidad aritmética, y presentarla
como lo segundo era más débil y menos cierto. La Tabla 6 lleva ahora **dos
columnas**: efecto comparativo y proporción descriptiva.

### 3. Ningún brazo comparador se extrajo nunca

De los 103 brazos del corpus, la modalidad toma tres valores —fago con
antimicrobiano, fago en monoterapia, no declarada— y los tres son brazos
expuestos. **No hay un solo brazo de control, placebo o tratamiento estándar en
toda la extracción**, ni siquiera en los tres ensayos aleatorizados con texto
completo. De los 15 estudios clasificados como comparativos, 13 aportaron un
único brazo.

De ahí la distinción que el manuscrito hace ahora explícita: **estudio
clasificado como comparativo** ≠ **contraste utilizable para inferencia**. La
clasificación decide el instrumento de riesgo de sesgo; no crea un comparador.

### 4. La Tabla 3 medía el resumen y hablaba del estudio

La clase de resistencia no puede asignarse en el 75,8 % de los **resúmenes**.
De los 71 artículos leídos, **48 la declaran de forma clasificable, 23 la
mencionan sin poder clasificarla y ninguno calla**. La ausencia está en el
resumen, no en el estudio. La Tabla 3 separa ahora las cuatro situaciones y la
frase absoluta —«ninguna estratificación construida sobre resúmenes puede ser
correcta»— se sustituye por la medida.

### 5. El efecto de no interrogar Embase, ICTRP y ProQuest no estaba acotado

No se puede estimar lo que esas fuentes habrían aportado, pero sí medir de qué
depende lo que hay: **40 de los 137 estudios incluidos (29,2 %) los encontró
una sola fuente** —20 solo CENTRAL, 9 solo ClinicalTrials.gov, 5 solo el brazo
B de Scopus, 4 solo PubMed, 2 solo CTIS—. La cobertura no es redundante.

## Lo que se cerró de los tres puntos abiertos

**Vínculo brazo→informe.** Los 103 brazos tienen informe de origen
identificado: 71 con el título localizado dentro del documento que se leyó, 31
porque el estudio tiene un solo informe y 1 por ser el único artículo de su
grupo. Ninguno sin resolver. Anexo S20.

**Horizonte temporal.** Se declara como componente del estimando: la revisión
**no prespecificó ninguno**, y de los 34 brazos cuyo artículo da una definición
operativa de éxito, el momento de evaluación va del día 4 a los 24 meses.

**Solapamiento de pacientes.** Examinados los 71 textos completos; 16 pares
candidatos. **Uno confirmado por lectura:** el caso 3 de EST-077 —niña de 10
años, Berlin Heart EXCOR, bacteriemia por *P. aeruginosa*, PASA16, Israel— es
el caso 3 de la Tabla 4 de EST-003. Un par que el detector marcó como firme,
EST-012 con EST-026, **se descartó leyendo**: EST-012 nombra el NCT de EST-026
en su discusión, como ensayo que fracasó en reclutar, no como el ensayo en que
se trató a su paciente. Anexo S21.

## Lo que espera firma, y bloquea el envío

`~/Escritorio/FIRMAR_auditoria_2026-09-16.xlsx`, cuatro hojas:

1. **EST-021.** Juicio global «bajo riesgo» con un dominio en «algunas
   preocupaciones». RoB 2 no lo admite. Los otros 11 estudios sí heredan su
   peor dominio.
2. **EST-003.** Su definición de éxito clínico describe el ensayo BX004-A
   contra placebo, y ni «BX004» ni esa frase aparecen en el artículo de
   EST-003. De 12 fragmentos de la cita, 0 están en el texto al que se
   atribuye.
3. **EST-003 y EST-077.** El mismo paciente en los dos.
4. **EST-077.** `adverse_event_n` = 5 y el artículo no contiene «adverse», ni
   «side effect», ni «tolerability»; sí dice cuatro pacientes y cinco ciclos.

Mientras las cuatro sigan sin firmar, la sección de riesgo de sesgo lleva el
aviso de provisional y **el sobre no se puede enviar**.

## El guardián que faltaba

`check_aritmetica.py` comprobaba las cuentas del manuscrito y nadie comprobaba
los datos de los que salen. `check_extraccion.py` lo hace: numeradores contra
denominadores, diseño contra tamaño, vocabularios controlados, brazo con
informe, y si la definición entrecomillada está en el artículo al que se
atribuye. Hoy encuentra 21 incidencias, y **ninguna la corrige**: la extracción
está firmada.

Tuvo que aprender una cosa: los PDF a dos columnas parten las frases, y buscar
la cita entera daba falsos positivos en EST-007 y EST-010, cuyas frases sí
están en su artículo con texto de la otra columna metido en medio. Se trocea la
cita y se exige la mayoría de los trozos.

## Lo que sigue abierto y no es de este cuaderno

- Ocho países escritos de dos o tres maneras en `geographic_source`. No afecta
  a ninguna cifra publicada —la procedencia de la Tabla 2 sale de la
  pre-extracción— pero el vocabulario controlado no se controló.
- Tres brazos etiquetados «case report» con 2, 23 y 26 pacientes.
- El **42** aparece como dos cosas distintas: 42 reportes de caso declarados en
  el resumen y 42 estudios con denominador adjudicado de 1. Hoy coinciden. Si
  uno cambia, la prosa queda mal sin que nada avise; por eso el segundo tiene
  ya su propio escalar, `estudios_denominador_uno`.
