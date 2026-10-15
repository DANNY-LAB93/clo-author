# Plan: protocolo depositado y fase definitiva de la revisión

**Estado:** BORRADOR. Espera la aprobación de los dos autores y el depósito en OSF.
**Fechas:** iniciado el 2026-10-07; revisado el 2026-10-08 tras dos rondas de revisión adversarial del protocolo.
**Elegido por:** D. Valdiviezo («HAZ LA DOS»).
**Protocolo:** `revision_sistematica/protocolo/protocolo_revision_sistematica.md`, versión 1.2. El `.docx` lo genera `scripts/build_protocolo_docx.py`, que se niega a producir la versión de depósito mientras quede un marcador ‹‹…››. Hoy quedan 14.

## Qué se busca

Que los criterios de la revisión que se publique estén en un **protocolo depositado antes de ejecutarla**. No es «el protocolo inicial» del trabajo hecho hasta el 6 de octubre: eso es el piloto, y lo seguirá siendo.

Lo hecho entre julio y el 6 de octubre de 2026 pasa a ser la **fase piloto**:
- no se borra;
- se declara en Métodos con el contenido íntegro de la sección 3 del protocolo, y en una frase en el resumen;
- sus datos viajan como suplemento.

## Lo que el informe final podrá decir

> «El protocolo se depositó en OSF Registries el ‹fecha› (‹DOI›), antes de la búsqueda, la selección, la extracción y la evaluación del riesgo de sesgo que se reportan. Se redactó después de una fase piloto sobre el mismo tema (julio-octubre de 2026), que empezó como metaanálisis de eficacia y cuyo corpus y resultados conocían los autores. Todos los criterios del protocolo se redactaron después de esa fase y conociendo su corpus; la sección 3.3 enumera los que difieren de los criterios con que empezó el piloto, con su fecha. Las ecuaciones de búsqueda y el conjunto de control proceden del piloto. El borrador del protocolo lo redactó un modelo de lenguaje (sección 19). Los datos del piloto se aportan como material suplementario.»

**No podrá decir:**
- que los criterios se fijaron antes de conocer el corpus piloto;
- que no hubo fase piloto;
- que el cribado de títulos y resúmenes lo hicieron humanos o por duplicado;
- que la extracción o el riesgo de sesgo del piloto fueron independientes.

## Decisiones que bloquean el depósito

Son los 14 marcadores ‹‹…›› del protocolo, agrupados.

**Datos que solo pueden dar ustedes**
1. **Fechas previstas** de inicio y de fin. Cabecera.
2. **ORCID de los dos y correo de N.T.** Sección 4.
3. **Autoría solapada.** Confirmar que ninguno de los dos firma estudios elegibles. Sección 4.
4. **Repositorio y DOI** de los datos de la fase definitiva. Sección 11.
5. **Fecha de corte** para obtener los textos. Sección 13.

**Hechos del piloto: resueltos el 2026-10-08.** D.V. declaró que diseñó las ecuaciones con la participación del modelo y que las ejecutó en cada interfaz con la guía del modelo; que examinó uno a uno lo que pasó el cribado, sin registrarlo; y que las reglas de desenlace las decidieron los dos. Están en la sección 3.1 y en la 4 del protocolo, y los manuscritos del piloto están corregidos (`quality_reports/decisions/2026-10-08_correcciones-del-piloto.md`).

**Decisiones metodológicas**

9. **Pedir textos y datos a los autores y por préstamo interbibliotecario**, o no. Sección 13.
   - En el piloto no se pidió nada, por orden de D.V. del 2-sep-2026 (commit `d57164b`; registro `2026-09-02_sin-peticiones-de-texto-completo.md`).
   - Lo que esto costó: el criterio de texto completo dejó fuera 7 de los 9 estudios comparativos según la pre-extracción del modelo. **Cinco** eran artículos publicados cuyo texto no se obtuvo: EST-029, EST-157, EST-167, EST-118 (Leitner 2021, *Lancet Infect Dis*, control positivo) y EST-173. Solo los dos resúmenes de congreso (EST-078, EST-188) no tienen artículo que pedir.
10. **Unidad del desenlace:** si se extrae el primer curso o el último cuando el artículo informa por curso. Sección 14.2.
11. **Colonización crónica:** si se estima aparte de la infección o se agrupa con ella. Sección 16.3.
12. **Umbral para agrupar y trato de los brazos de un solo paciente.** Sección 16.3.
    - Con el embudo aproximado del piloto, superan los requisitos 19 brazos de 16 estudios, 14 de ellos de un solo paciente.
    - Los requisitos 3 a 5 los aplicó el canal con reglas aproximadas, y con las reglas de la 16.3 la cifra puede cambiar.
    - El informe piloto no agrupó esos 19.
    - Cualquier umbral que se fije ahora se fija conociendo ese recuento, y el protocolo lo declara.
13. **Definición del éxito por referencia a otra publicación:** si cuenta como operativa. Anexo B.
14. **Fichas de registro antiguas:** desde qué año cuentan como «registradas sin publicación». Sección 16.6.

## Lo que propone el borrador y los autores tienen que aprobar

Lo redactó el modelo y no bloquea el `.docx`, pero el depósito equivale a aprobarlo, y la sección 19 del protocolo lo dice. Hay que leerlo antes de depositar. Lo principal:

**Regla del fago dirigido contra *P. aeruginosa* (8.4).** Exige que el paciente tenga *P. aeruginosa* en una muestra de los 30 días previos y que el fago se dirija contra ella. Se evalúa de nuevo, sin trasladar el veredicto del piloto, en los seis estudios que el piloto mantuvo por firma:
- **EST-051, EST-129 y EST-135:** firmados como «fago no diana».
- **EST-096:** también firmado así. Pero su paciente 10 recibió el fago Ps1N/734 contra *P. aeruginosa*, y lo que se contradice es si la bacteria estaba presente al empezar. Con la regla de contradicciones se tiene por presente, y el estudio se queda si se cumple lo demás.
- **EST-152 y EST-170:** ningún paciente propio tiene *P. aeruginosa*; solo la nombran al citar a EST-049 y EST-106. Eso ya era ORG en el piloto.

**Unidad de inclusión (8.1).** Un análisis intermedio y el final son el mismo estudio. Las series acumulativas son estudios distintos con solapamiento.

**Población (8.3) y desenlaces (8.5).** No se exige clase de resistencia, y la colonización crónica queda definida. Un estudio multipatógeno con desenlaces solo agregados entra solo en las medidas de completitud, y DES solo si no da ninguno.

**Precedencia entre motivos (8.9).** IDI se aplica después de comprobar los demás criterios sobre el resumen.

**Etapa 1 (12.1).**
- No excluye editoriales, cartas, notas ni *short surveys*.
- FEC respeta los registros que comparten identificador.

**Cribado (12.2 y 3.5).**
- El modelo criba en sesiones aisladas del repositorio y solo puede excluir con siete códigos; ante la duda, avanza.
- D.V. registra informe a informe lo que examina.

**Elegibilidad (12.4) y texto completo (13).**
- Los dos autores, de forma independiente, con cuadernos sin veredicto ni cita propuestos.
- Antes de un NOTXT, D.V. intenta en persona las vías que el canal no abrió.

**Extracción (14).**
- Formulario revisado y pilotado.
- Doble extracción con una comprobación nueva: que los textos libres de los dos cuadernos no coinciden carácter por carácter.
- Adjudicación con los dos nombres fila a fila.
- Reglas de clase y DTR escritas (anexo B), con la lista completa de agentes que no cuentan para el DTR.

**Pre-extracción (14.7).** La emite el modelo después de la extracción humana, y N.T. valida un 20 %.

**Riesgo de sesgo (15).** Solo en estudios con grupo concurrente sin fago. En el piloto serían 2: EST-008 y EST-021. EST-108 solo compara con y sin antibiótico entre tratados con fago.

**Síntesis (16).** Población de la estimación principal, pacientes compartidos contados una vez, GLMM en R (metafor), sin subgrupos, cuatro análisis de sensibilidad y GRADE solo si se agrupa.

## Errores del piloto que encontraron las dos rondas

Todos están verificados contra los ficheros, y la sección 3 del protocolo los declara. **Corregidos el 2026-10-08 en los tres manuscritos, los anexos, el resumen y la carta** (`quality_reports/decisions/2026-10-08_correcciones-del-piloto.md`).

1. **Quién buscó** (decisión 6).
   - Los tres manuscritos y el anexo S2 dicen que las ecuaciones «las diseñó y ejecutó D.V. … no las generó ni las ejecutó el modelo».
   - El de la revista dice además que la búsqueda, la fijación de criterios y la evaluación a texto completo se hicieron «sin intervención del modelo». En la lectura de textos completos, el modelo localizó y propuso las exclusiones con su cita.
2. **Examen humano de lo que pasó el cribado** (decisión 7). No consta. El maestro lo atribuye a D.V.; su declaración de IA y el manuscrito de la revista, a «los autores».
3. **Independencia de la extracción.** Los manuscritos hablan de doble extracción independiente, con kappa 0,62.
   - El cuaderno que N.T. entregó el 26 de agosto trae las columnas de localización del dato y de motivo de incompletitud idénticas, carácter por carácter, a las de D.V.: 107 de 107 y 106 de 106 filas, 6 564 caracteres. Comprobado hoy sobre los cuadernos.
   - El 23 de agosto no coincidían en ninguna fila.
4. **«Consenso» de la adjudicación.** De los 541 desacuerdos, el registro anota a los dos autores en 14, a uno solo en 525 (293 D.V. y 232 N.T.) y 2 se cerraron por una regla mecánica. Comprobado hoy. El manuscrito de la revista ya lo dice bien; el maestro, no.
5. **Independencia del riesgo de sesgo.** Los manuscritos dicen «por duplicado independiente», con kappa 0,74.
   - El 5 de septiembre los dos cuadernos tenían primero los 82 juicios idénticos; 75 minutos después tenían 13 discrepancias y seguían compartiendo 7 418 caracteres idénticos de notas.
   - El cuaderno de consenso lo generó el canal con 69 juicios precargados y coincide con el de D.V. en todos.
6. **Recribado ciego.** Lo hizo D.V. solo, sin los criterios a la vista. Incluyó 6 de 350, y D.V. los reclasificó como excluidos. Los manuscritos no dicen quién lo hizo. La nota 17 de CLAUDE.md, que decía «los dos autores», ya está corregida.
7. **«Piloteo» del formulario.** Los manuscritos dicen que se piloteó sobre cinco estudios, y no hay registro de ello.
8. **«23 variables».** Los cuadernos tuvieron 21 durante toda la extracción. El denominador y la persistencia de la erradicación se añadieron al esquema el 12 de agosto, pero no llegaron a los cuadernos.
9. **Control positivo.** Los manuscritos dicen 40 estudios «fijados a priori», y 40 de 40 superados.
   - El conjunto fijado tiene 42 estudios. La auditoría solo comprobaba los 40 con PMID, y solo durante el cribado.
   - Del corpus final del piloto salieron 7: Ronit 2024 por idioma, Leitner 2021 por NOREC y 5 por NOPDF. Comprobado hoy.
10. **Idioma.** Los manuscritos dan 35 estudios excluidos por idioma. Son 39: 35 en el resumen, cuyas exclusiones emitió el modelo el 11 de agosto, y 4 a texto completo. A ellos se suman 3 por idioma no verificable. Corregido en la limitación de idioma de los tres manuscritos el 2026-10-15.

## Antes del depósito: lo que hago yo, si lo aprueban

- Adaptar y fechar los guiones que leen ficheros del piloto:
  - `group_reports_into_studies.py`: numeración DEF-NNN y un `fulltext_identifiers.csv` propio;
  - `comprueba_idioma_cuerpo.py`: corpus definitivo y lectura de HTML;
  - `build_rayyan_validation_sample.py`: semilla 20261008;
  - el código FEC y el vocabulario nuevo en `exclusion_codes.py`;
  - los campos nuevos del formulario.
- Preparar el directorio aislado del cribado (sección 3.5).
- Hacer el commit del protocolo y de los guiones, para que su versión quede fechada antes del depósito.

## Quién hace cada cosa

La numeración sigue la sección 17 del protocolo.

| Paso | Quién | Qué hace el canal (escrito y ejecutado por el modelo, y así declarado en la sección 19) |
|---|---|---|
| 0. Aprobar, rellenar los marcadores y depositar en OSF | D.V. y N.T., con su cuenta | `.docx` y anexo E, campo a campo |
| 1. Separar el piloto | canal | mueve los ficheros a `revision_sistematica/piloto/` y deja inactivos los guiones con decisiones del piloto |
| 2. Búsqueda | D.V. en cada interfaz (Scopus, CENTRAL, BVS, SciELO, EudraCT y CTIS) | descarga de PubMed y ClinicalTrials.gov por API, a petición de D.V.; cuadre de recuentos |
| 3. Deduplicación y controles en el pozo | canal | todo |
| 4. Etapa 1 | canal | reglas y control positivo |
| 5. Etapas 2 y 3 | el modelo emite en sesión aislada; D.V. examina y registra lo que avanza, sin poder excluir | lotes, registro solo-anexar, control positivo |
| 6. Recribado ciego (350) | D.V. y N.T., cada uno por separado, en Rayyan | muestra con semilla fija y cálculo de las tasas |
| 7. Agrupación, enlace y fichas completas | el canal propone; D.V. confirma | búsqueda de identificadores y descarga de fichas |
| 8. Textos completos e idioma | canal, y D.V. en persona para lo que el canal no abra | descarga, registro de intentos con su autor, estimación del idioma |
| 9. Elegibilidad a texto completo | D.V. y N.T., independientes | cuadernos sin veredicto ni cita propuestos; kappa |
| 10. Piloteo del formulario | D.V. y N.T. | cinco estudios con semilla fija |
| 11. Extracción por duplicado y adjudicación | D.V. y N.T. | cuadernos sin valores precargados, comprobación de textos idénticos, comparador |
| 12. Relectura, solapamiento y fusión | D.V. y N.T. | pares candidatos por guion |
| 13. Pre-extracción desde el resumen | modelo; N.T. valida un 20 % | concordancia |
| 14. Riesgo de sesgo | D.V. y N.T. | cuadernos sin juicios precargados y concordancia |
| 15. Síntesis | canal | escalares, tablas y figuras |
| 16. Reejecución si pasan seis meses | D.V. y canal | lo mismo que en los pasos 2 a 15 |
| 17. Comparación con el piloto | canal | tabla de correspondencia, solo tras cerrar la adjudicación |
| Informe y manuscritos | el modelo redacta los borradores; los autores revisan y aprueban | así declarado en la sección 19 |

## Lo que NO se hace

- No se reejecuta ninguna búsqueda, cribado ni extracción antes del depósito.
- No se borra nada del piloto.
- No se ejecuta en la fase definitiva ningún guion que aplique decisiones del piloto (`ingest_*.py`, `add_*.py`).
- No se lee `study_groups.csv` ni `fulltext_identifiers.csv` del piloto.
- Los cuadernos que reciben los autores no llevan veredictos, citas, valores ni juicios propuestos por el modelo.

## Coste, como referencia

La cifra del corpus definitivo **no está calculada**. Si se aplican las reglas del protocolo al corpus del piloto:
- **Por PRF:** sale al menos EST-039, de profilaxis de neumonía.
- **Por la regla 8.4:** saldrían hasta cinco más, EST-051, EST-129, EST-135, EST-152 y EST-170. EST-096 probablemente se queda.
- **Por las reglas 8.2, 8.3 y 8.5:** pueden mover EST-050, EST-060, EST-075 y EST-116.
- **Lo demás:** la búsqueda actualizada y los textos que se recuperen cambiarán el resto.

**El trabajo humano grueso:**
- dos lecturas independientes de unos 180 estudios a texto completo;
- extracción doble de unos 60;
- recribado de 350 registros por cada autor.

Son varias semanas.
