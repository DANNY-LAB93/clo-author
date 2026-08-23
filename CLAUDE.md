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
python scripts/compare_extractions.py --a revision_sistematica/extraccion/extraccion_danny_valdiviezo.xlsx --b revision_sistematica/extraccion/extraccion_nataly_trelles.xlsx --nombre-a Danny_Valdiviezo --nombre-b Nataly_Trelles

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

As of 2026-08-23. Every figure here is produced by the pipeline, not typed:
re-derive with `build_synthesis_scalars.py` and check with `check_manuscript_claims.py`.

| Component | File | Status | Description |
|-----------|------|--------|-------------|
| Manuscript | `paper/manuscrito_revision_sistematica.md` | drafted | 5122 words of main text. **Over the CMI 3,500 limit** — the overage is the honesty declarations. N.T.'s ICMJE authorship is unresolved |
| Manuscript PDF | `paper/pdf/` | built | Typeset by `build_manuscript_pdf.py`, 21 citations resolved from the `.bib` |
| Search & screening | `revision_sistematica/` | done | 23,057 records → 17,129 unique → 233 reports → 184 studies, 124 extractable |
| Full-text retrieval | `revision_sistematica/textos_completos/` | 91 / 124 (73.4%) | Biased: the missing fraction holds 47.8% of the comparative designs. Requests drafted, **not yet sent** |
| Extraction | `revision_sistematica/extraccion/` | 124 by D.V., 98 also by N.T. | D.V. extracted all 124 retrievable studies, complete on the thirteen core fields. N.T. extracted 98 of them and **withdrew from the project on 2026-08-22**. `ya_extraido` in `orden_de_extraccion.csv` is a snapshot and goes stale — count from the workbooks |
| Submission package | `verificables revisión sistemática/` | built | S0–S13 + guide + both manuscripts in PDF and `.docx` |

**Where the extraction actually stands, as of 2026-08-23:**

1. **There is no second reviewer.** Nataly Trelles withdrew on 2026-08-22. See
   `quality_reports/decisions/2026-08-23_retirada-segunda-revisora.md`. Nothing
   in the manuscript may claim duplicate extraction was completed, or that
   disagreements were settled by consensus. They were not.
2. `revision_sistematica/extraccion/extraction_conflicts.csv` holds 724 real value
   conflicts over 128 compared arm rows: median agreement 69%, median informative
   kappa 0.30 (7 of 9 categorical fields). 2 are adjudicated and signed; 722 are
   not, and will not be. These figures live in `synthesis_scalars.json` as
   `extraccion_*` — never retype them.
3. Do NOT trust an older conflict count. Until 2026-08-23 the comparator scored a
   cell one reviewer had filled and the other had not as a disagreement, which
   turned D.V.'s lead into measured discordance: 1,063 of the 1,788 it reported
   were coverage gaps, not conflicts. Fixed in `ca12d6a`.
4. `quality_reports/decisions/2026-08-12_erradicacion-regla-corregida.md` is the
   record still marked PROPUESTA. It cannot be confirmed by both reviewers any
   more; D.V. extracted all 124 studies under it.
