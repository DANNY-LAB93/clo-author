**Status:** COMPLETED

# Configurar clo-author para proyecto de fagoterapia en Pseudomonas MDR

## Contexto

Este repositorio es el template público **clo-author**, construido para economía empírica (identificación causal tipo DiD/IV/RDD, formato de "working paper" con JEL codes, perfiles de journals de economía/finanzas/accounting/marketing). El usuario quiere usarlo directamente (sin fork en GitHub, trabajando en este working directory) para un nuevo proyecto: una **revisión sistemática / meta-análisis sobre fagoterapia en Pseudomonas aeruginosa multirresistente (MDR)**.

Respuestas de clarificación ya obtenidas:
- Tipo de estudio: revisión sistemática / meta-análisis
- Datos: aún no recolectados (se extraerán de la literatura)
- Journals objetivo: clínicos/microbiología (ej. Clinical Infectious Diseases, Antimicrobial Agents and Chemotherapy, PLOS Pathogens)
- Institución: Universidad Católica de Cuenca

El template asume por defecto economía; README.md dice explícitamente que se adapta a "labor, public, health, development, trade, IO" — no a microbiología/biomedicina. Este plan adapta los archivos de referencia (`domain-profile.md`, `journal-profiles.md`) para este campo, dejando el resto de la arquitectura (agentes, quality gates, worker-critic pairs) intacta, ya que el flujo genérico (discovery → strategy → execution → write → peer review → submission) sí aplica a una revisión sistemática si se reinterpretan sus piezas:

| Concepto econ. | Análogo en revisión sistemática/meta-análisis |
|---|---|
| Identification strategy (DiD/IV/RDD) | Protocolo PRISMA 2020, criterios PICO, modelo de efectos fijos/aleatorios |
| Estimand | Tamaño de efecto agrupado (RR, OR, HR, SMD) |
| Robustness checks | Análisis de sensibilidad, leave-one-out, subgrupos |
| Threats to identification | Riesgo de sesgo (Cochrane RoB2/ROBINS-I), heterogeneidad (I², τ²), sesgo de publicación (Egger's test, funnel plot) |
| JEL codes | (no aplica igual — se sustituye por MeSH terms si el journal lo pide) |

**Fuera de alcance de este plan** (señalado, no resuelto): el formato LaTeX en `working-paper-format.md` (doublespacing, JEL codes, `biblatex` authoryear) no calza con el formato IMRaD/Vancouver típico de journals biomédicos. Se deja como está por ahora — se adaptará cuando se ejecute `/write` o se acerque la fase de submission.

## Cambios realizados

1. **`CLAUDE.md`** — Project/Institution/Field llenados; tabla "Current Project State" actualizada a "not started" en todos los componentes.
2. **`.claude/references/domain-profile.md`** — reescrito campo por campo para microbiología clínica/meta-análisis: journals objetivo, fuentes de datos (PubMed/EMBASE/Cochrane CENTRAL/etc.), estrategias de síntesis (PRISMA+PICO, efectos aleatorios, meta-regresión), convenciones de campo (PRISMA flow diagram, RoB2/ROBINS-I, GRADE), notación (RR/OR/HR/SMD/I²/τ²), referencias seminales (PRISMA 2020, Cochrane Handbook), preocupaciones de referees. Secciones de teoría/autoría marcadas N/A (theorist no se despacha para este proyecto).
3. **`.claude/references/journal-profiles.md`** — nueva sección `## Clinical Microbiology / Infectious Disease` con perfiles de CID, AAC, y PLOS Pathogens, mismo formato que las secciones existentes. Secciones de economía/finanzas sin modificar.
4. **Estructura de carpetas** — ya existía completa (`data/raw`, `data/cleaned`, `paper/sections`, etc.); no se crearon carpetas nuevas.

## Verificación
- CLAUDE.md sin placeholders `[BRACKETED]` remanentes en Project/Institution/Field/Current Project State — confirmado.
- domain-profile.md sin ejemplos económicos remanentes en las secciones adaptadas — confirmado.
- journal-profiles.md con formato consistente en la nueva sección — confirmado.

## Siguiente paso sugerido
`/discover interview fagoterapia pseudomonas MDR` — para construir la especificación de investigación (PICO, criterios de elegibilidad, alcance de búsqueda) antes de lanzar librarian/explorer.
