# CLAUDE.MD -- Empirical Research with Claude Code

<!-- Keep this file under ~150 lines — Claude loads it every session. -->

**Project:** Phage Therapy for MDR *Pseudomonas aeruginosa*: A Systematic Review
**Institution:** Universidad Católica de Cuenca
**Field:** Clinical Microbiology / Infectious Disease — Systematic Review (adapted from the economics-default template; see `.claude/references/domain-profile.md`)
**Branch:** main
**Language:** the manuscript, the decision records and the working files are in Spanish; there is a parallel English manuscript for submission.

> **Scope, since 2026-08-12.** This repository holds **the systematic review only**.
> The meta-analysis was parked on 2026-08-10 and its pipeline deleted on 2026-08-12:
> the manuscript's own argument is that this body of evidence does not admit a
> quantitative synthesis. Recover it with `git checkout b797339 -- metaanalisis/`
> if that ever changes. What survives of it is documented in
> `revision_sistematica/corpus_previo/LEEME.md`.

---

## Core Principles

- **Plan first** -- enter plan mode before non-trivial tasks; save plans to `quality_reports/plans/`
- **Verify after** -- compile and confirm output at the end of every task
- **Single source of truth** -- `paper/manuscrito_revision_sistematica.md` is authoritative; the English version and the `.docx` package derive from it
- **No number is typed by hand** -- every quantity in the manuscript is cited by name from `quality_reports/synthesis_scalars.json`, produced by `scripts/build_synthesis_scalars.py`
- **Quality gates** -- weighted aggregate score; nothing ships below 80/100; see `quality.md`
- **Worker-critic pairs** -- every creator has a paired critic; critics never edit files
- **Auto-memory** -- corrections and preferences are saved automatically via Claude Code's built-in memory system

---

## Folder Structure

```
clo-author/
├── CLAUDE.MD                       # This file
├── .claude/                        # Rules, skills, agents, hooks
├── Bibliography_base.bib           # Centralized bibliography
├── paper/                          # The manuscript (source of truth)
│   ├── manuscrito_revision_sistematica.md   # Authoritative, Spanish
│   ├── manuscript_systematic_review_en.md   # Derived, for submission
│   ├── figuras/                    # figura_1_prisma, figura_2_composicion (.pdf/.png)
│   └── tablas/                     # tabla_1 .. tabla_4 (.csv/.md)
├── revision_sistematica/           # The review itself — the bulk of the work
│   ├── busqueda/                   # Search exports, per source
│   ├── cribado/                    # Screening decisions by stage, study groups
│   ├── textos_completos/           # Retrieved PDFs and HTML text
│   ├── extraccion/                 # Both reviewers' workbooks + conflicts
│   └── corpus_previo/              # Pre-PRISMA extraction — read its LEEME first
├── scripts/                        # The pipeline (Python + some R)
├── quality_reports/                # Decisions, plans, scalars, agreement, journal
├── templates/                      # Decision record, claim-source map, session log
└── verificables revisión sistemática/   # Submission package: S0–S10 + .docx
```

**Not here on purpose:** no `data/`, no LaTeX build. The review's data lives inside
`revision_sistematica/`, and the manuscript is Markdown → `.docx`.

---

## Commands

```bash
# Recompute every figure the manuscript cites, from the current corpus
python scripts/build_synthesis_scalars.py

# Rebuild the manuscript's tables 1-4
python scripts/build_manuscript_tables.py

# Compare the two independent extractions -> agreement report + conflicts file
python scripts/compare_extractions.py --a revision_sistematica/extraccion/recibido/danny.xlsx --b revision_sistematica/extraccion/recibido/nataly.xlsx

# Regenerate both extraction workbooks without losing what is already filled in
python scripts/make_extraction_forms.py

# Rebuild the S0-S10 submission package
python scripts/build_verifiables_package.py
```

> **Order matters.** `build_synthesis_scalars.py` runs first: the tables, the figures
> and the manuscript all read the scalars it writes. Never edit a number downstream.

---

## Quality Thresholds

| Score | Gate | Applies To |
|-------|------|------------|
| 80 | Commit | Weighted aggregate (blocking) |
| 90 | PR | Weighted aggregate (blocking) |
| 95 | Submission | Aggregate + all components >= 80 |
| -- | Advisory | Talks (reported, non-blocking) |

See `quality.md` for weighted aggregation formula.

---

## Skills Quick Reference

| Command | What It Does |
|---------|-------------|
| `/new-project [topic]` | Full pipeline: idea → paper (orchestrated) |
| `/discover [mode] [topic]` | Discovery: interview, literature, data, ideation |
| `/strategize [mode] [question]` | Identification strategy, pre-analysis plan, or formal theory section (`theory` mode) |
| `/analyze [dataset]` | End-to-end data analysis |
| `/write [section]` | Draft paper sections + humanizer pass (`style-guide` mode extracts voice from prior papers) |
| `/review [file/--flag]` | Quality reviews (routes by target: paper, code, peer) |
| `/revise [report]` | R&R cycle: classify + route referee comments |
| `/talk [mode] [format]` | Create, audit, or compile Beamer presentations |
| `/submit [mode]` | Journal targeting → package → audit → final gate |
| `/tools [subcommand]` | Utilities: commit, compile, validate-bib, journal, etc. |
| `/checkpoint [--flag]` | Session handoff: memory + SESSION_REPORT + research journal (+ Obsidian if configured) |

---

## Output Organization

Figures go to `paper/figuras/`, tables to `paper/tablas/`, both named by what they
show (`figura_1_prisma`, `tabla_3_sesgo_recuperacion`) and not by the script that
made them. Reports and decisions go to `quality_reports/`.

---

## Current Project State

As of 2026-08-12.

| Component | File | Status | Description |
|-----------|------|--------|-------------|
| Manuscript | `paper/manuscrito_revision_sistematica.md` | drafted | 3,898 words. Missing only CRediT contributions and acknowledgements before submission |
| Search & screening | `revision_sistematica/` | done | 23,057 records → 17,129 unique → 233 reports → 184 studies, 124 extractable |
| Full-text retrieval | `revision_sistematica/textos_completos/` | 65 / 124 (52.4%) | Biased: 13 of the 23 comparative studies are missing. Requests drafted, **not yet sent** |
| Extraction | `revision_sistematica/extraccion/` | 17 / 124 | **Blocked.** See below |
| Submission package | `verificables revisión sistemática/` | built | S0–S10 + both `.docx`, regenerated by `build_verifiables_package.py` |

**What blocks the extraction, in order:**

1. `quality_reports/decisions/2026-08-11_definicion-erradicacion-y-exito.md` is still
   marked PROPUESTA. Both reviewers must confirm it before extracting further —
   otherwise the remaining 107 studies inherit the same divergence.
2. `revision_sistematica/extraccion/extraction_conflicts.csv` holds 169 value
   conflicts, none resolved. Median agreement 70%, median informative kappa 0.38.
   Fill `resolucion` / `resuelto_por` / `fecha` — that trail is what licenses the
   Methods claim that disagreements were settled by consensus.
