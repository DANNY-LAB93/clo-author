# Criterio DTR: qué se mide, cómo se operacionaliza, y la corrección que sufrió

**Fecha:** 2026-08-13
**Estado:** VIGENTE
**Motivo del registro:** este criterio se definió mal una vez y se corrigió, y la
corrección solo constaba en la cadena de documentación de un script
(`scripts/fix_dtr_definition.py`). Un criterio de desenlace que cambió a mitad de
la revisión tiene que poder auditarse desde el registro de decisiones, no desde
el código.

---

## La fuente

Kadri SS, et al. *Difficult-to-Treat Resistance in Gram-negative Bacteremia at
173 US Hospitals.* Clin Infect Dis 2018;67(12):1803–1814. PMID 30052813,
doi 10.1093/cid/ciy378.

Su definición, literal en Métodos: **«intermediate or resistant to all reported
agents in carbapenem, beta-lactam, and fluoroquinolone categories»**.

Lo importante no es la lista, es la lógica: DTR pregunta si se agotaron los
antibióticos de **primera línea**. Los de reserva son aquello a lo que el DTR
obliga a recurrir, así que no entran en la determinación. Kadri nombra
expresamente como reserva los aminoglucósidos, la colistina/polimixina B y la
tigeciclina.

## Cómo se operacionaliza aquí

**Conjunto de primera línea:** carbapenémicos, otros betalactámicos y
fluoroquinolonas.

**Fuera de la determinación:**
- *reserva*, por el propio texto de Kadri: colistina y polimixina B,
  aminoglucósidos, tigeciclina;
- *posteriores a 2018*, que la definición no pudo enumerar: ceftazidima-avibactam,
  cefiderocol, ceftolozano-tazobactam, imipenem-relebactam.

**Los tres valores, con su asimetría, que es de principio y no de conveniencia:**

| Valor | Cuándo |
|---|---|
| `yes` | Toda la primera línea es no sensible. En la práctica: el artículo documenta actividad únicamente de agentes que quedan fuera del conjunto de primera línea |
| `no` | Basta **un** agente de primera línea sensible documentado, porque DTR exige que fallen todos |
| `not-derivable` | El resto |

La asimetría es deliberada: afirmar DTR exige agotar la lista entera, negarlo
exige un solo dato. Un criterio en el que ningún brazo pueda salir negativo no es
un criterio aplicado a datos, y ese fue exactamente el error anterior.

## El error, y quién lo encontró

Métodos y la Introducción definían DTR como «no sensibilidad a **todos** los
betalactámicos **y todas** las fluoroquinolonas». No es lo que dice Kadri, y no es
una diferencia semántica: «todos los betalactámicos» arrastra a la exigencia los
agentes de reserva y los posteriores a 2018, y vuelve el criterio **más estricto**
que el original.

La consecuencia fue que la revisión **fabricó la no-derivabilidad que después
reportó como su hallazgo principal sobre DTR**. Lo identificó un revisor de
microbiología en la ronda 6, y tenía razón.

Había una segunda señal que debió delatarlo antes: la codificación solo tenía dos
niveles, `yes` y `not-derivable`. Ningún brazo podía salir negativo.

La corrección se aplicó el 2026-07-30 sobre el conjunto de entonces, con el
fundamento anotado brazo a brazo en el propio dataset.

## Dos advertencias que el manuscrito debe llevar

**Los agentes posteriores a 2018 son un juicio declarado, no un hecho.** Los
propios autores de Kadri anotan que futuras revisiones tendrían que incorporar los
agentes nuevos. Bajo una revisión así, un aislado sensible solo a cefiderocol o
solo a ceftazidima-avibactam podría pasar a DTR-negativo. Hoy hay al menos un caso
en el corpus en esa situación (EST-015, sensible solo a cefiderocol), de modo que
la clasificación de ese brazo depende de una convención que puede cambiar.

**Panresistencia.** Un aislado PDR según Magiorakos no es sensible a nada, ni a los
de reserva. Cumple DTR por definición, porque toda la primera línea es no sensible,
aunque no encaje en la formulación «sensible solo a agentes de reserva». La regla
del formulario se amplía para decirlo, porque es el caso más claro de DTR y la
redacción anterior lo dejaba fuera.

## Estado actual en el corpus

El criterio no consta en el 98,4 % de los estudios recuperables. Esa cifra sale de
la pre-extracción desde resúmenes, y conviene leerla con cuidado: **un resumen no
imprime antibiogramas**, así que la no-derivabilidad es aquí esperable por
construcción y no es todavía una afirmación sobre el reporte del campo. Se
convertirá en una cuando la extracción por duplicado lea los antibiogramas del
texto completo.

> **Nota del 23 de agosto de 2026.** Ese paso no va a darse como estaba previsto:
> no hay extracción por duplicado desde que N. Trelles se retiró el 22 de agosto
> de 2026. La lectura de antibiogramas contra el texto completo depende ahora de
> un solo revisor y de los textos que estén en mano, que no son todos. La cifra
> sigue siendo un límite de la fuente, y así hay que leerla.


Los dos únicos casos derivables lo son porque su título o su resumen declaran el
único agente activo, y los dos están bien derivados:

| Estudio | Prueba | Valor |
|---|---|---|
| EST-015 | El resumen dice que cefiderocol fue el único antibiótico con actividad consistente sobre los seis aislados; los autores llaman al aislado «DTR-*P. aeruginosa*» | `yes` |
| EST-046 | El título dice literalmente *colistin-only-sensitive*; la colistina es de reserva y no cuenta | `yes` |
