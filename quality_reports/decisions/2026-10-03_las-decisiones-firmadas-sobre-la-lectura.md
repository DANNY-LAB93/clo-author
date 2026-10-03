# Las decisiones firmadas sobre lo que la lectura dejó abierto

**Estado:** APLICADO el 3 de octubre de 2026, salvo dos decisiones con una sola
firma que esperan la adenda.
**Viene de:** `2026-10-01_la-lectura-firmada-del-30-de-septiembre.md`. El cuaderno
`FIRMAR_lectura_2026-10-01.xlsx` volvió firmado por DANNY VALDIVIEZO y NATALY
TRELLES, con fecha 2026-10-01 y la casilla de lectura en SI. Copia intacta en
`revision_sistematica/lectura_pendiente/FIRMAR_lectura_2026-10-01_firmado.xlsx`.
**Ficheros:** `scripts/ingest_firma_lectura.py`, `scripts/make_firma_adenda_lectura.py`
(nuevos); `decisiones_firmadas_2026-10-01.csv`; `exclusiones_tras_texto_completo.csv`
(+4); `correcciones_tras_texto_completo.csv` (+7); `audita_pendientes.py`,
`build_auditoria_scalars.py`, `check_manuscript_claims.py`, `audita_cifras.py`,
`build_lista_anexos.py`, `build_package_guide.py`, los tres manuscritos.

## Lo que se aplicó

| Hoja | Decisión |
|---|---|
| 1 | **Excluidos con ORG: EST-009, EST-055, EST-181, EST-208.** Mantenidos: EST-129, EST-132, EST-135, EST-152, EST-170, EST-051, EST-096 |
| 2 | EST-053, EST-057, EST-088: se mantienen y se declaran, como EST-001 y EST-094 |
| 3 | Corregidos: EST-047 DTR → yes; EST-048 → not-classifiable; EST-058 DTR → yes (Kadri); EST-106 → below-MDR-threshold; EST-124 → XDR, verificada, DTR yes (manda PA02). Sin cambio: EST-004, EST-019, EST-042 (PDR que no se sostiene, declarado), EST-169 (mixto, declarado) |
| 4 | «La leímos los dos; cada uno los artículos completos». Las 23 transcripciones de figuras: «Sí; todas» comprobadas contra la figura. Ningún modelo de lenguaje declarado |

El corpus pasa de **136 a 132 estudios** (90 extraíbles, 66 con texto, 98 brazos).
EST-055 era un comparativo con grupo de comparación y evaluado con ROBINS-I: los
comparativos pasan a 13, los evaluables a 10, los que tienen grupo a 4, la Tabla 5
a 74 celdas, y la concordancia a 55 de 66 (83,3 %; kappa 0,77). Los pares de
solapamiento con estudios excluidos salen de la tabla: 31 pares, 19 confirmados,
12 descartados; los 20 pacientes duplicados no cambian.

## Lo que se preguntó antes de aplicar, y por qué

Siete «MANTENER» de la hoja 1 chocaban con la lectura del 30 de septiembre o con
el criterio de población. Se comprobó en los PDF:

- **EST-152**: la frase citada («A multidrug-resistant Pseudomonas aeruginosa in a
  lung transplant recipient…», p. 6) describe el paciente de Dan et al., su ref. 10,
  que es **EST-049**.
- **EST-170**: la frase («Phage therapy was described in one patient with Dacron
  aortic graft infection…», p. 4) describe el de su ref. 18, Chan et al., que es
  **EST-106**.
- **EST-132**: la frase es la composición del cóctel empírico (p. 2).
- EST-129 y EST-135: el paciente tuvo *P. aeruginosa*, pero el fago (ISP, anti-
  estafilocócico) no iba contra ella; en EST-135 fue una sobreinfección posterior.

D. Valdiviezo respondió el 3 de octubre: mantener EST-152 y EST-170 **y declararlo**;
mantener los cuatro dudosos y declararlo; **excluir EST-132**; mantener EST-106.

## Lo que NO se aplicó

**EST-132.** La hoja 1, con las dos firmas, dice MANTENER; la respuesta del 3 de
octubre es de una sola persona, y excluir es un acto de autoría que firman los dos.
Sigue en el corpus y el manuscrito lo declara como mantenido. **EST-106**: su
permanencia, que tampoco se firmó en la hoja 2, figura como pendiente. Las dos van
en `~/Desktop/FIRMAR_adenda_lectura_2026-10-03.xlsx`; `ingest_firma_lectura.py` la
aplica en cuanto lleve las dos firmas. Si EST-132 sale, la frase «en EST-132 solo
figura en la composición del cóctel» pierde su ancla y el guardián lo dirá.

## Lo que se encontró al reconstruir

- El maestro decía «Estos 23 son la otra cara… el 29,0 % de los 93»: el porcentaje
  estaba anclado y se actualizó solo; el 23 no, y era 27.
- El párrafo del diseño ya era incoherente antes de hoy: «12 no clasificables —12
  con NA acordado y 7 abiertos—», «suelos sobre los 84» y «de esos 86», con 0
  desacuerdos abiertos. Reescrito y anclado.
- El de la revista decía «En 48 de ellos… 47 declaran» sin ancla; son 47 y 46.
- **16 cifras del inglés** pasaban solo porque coincidían con otro escalar (nota 16
  de CLAUDE.md): 136, 170, 47, 94, 91, 102 (dos veces), 74,5, 44,7, 75,5, 52,1, 38,3,
  97,9, 78 brazos legibles y sus porcentajes, 68,6. Ancladas y al día.
- «del mismo modo que los diez anteriores», en letra y sin ancla, era falso con 15
  exclusiones ORG. Reescrito sin cifra.

Anclas: 295, todas al día. 17 de 17 cifras auditadas se reproducen.
