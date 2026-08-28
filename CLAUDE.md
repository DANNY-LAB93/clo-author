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

# Rebuild the whole submission package (S0-S13 + guide)
python scripts/build_verifiables_package.py   # S11-S13 se construyen dentro
python scripts/build_readable_annexes.py     # los .xlsx legibles de cada .csv
python scripts/build_editorial_report.py     # S0 y el indice
python scripts/build_package_guide.py        # la guia del paquete

# Rebuild the Journal of Science and Research submission on the Desktop
python scripts/build_jsr_submission.py
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

As of 2026-08-28. Every figure here is produced by the pipeline, not typed:
re-derive with `build_synthesis_scalars.py` and check with `check_manuscript_claims.py`.

| Component | File | Status | Description |
|-----------|------|--------|-------------|
| Manuscript | `paper/manuscrito_revision_sistematica.md` | drafted | 4811 words of main text. Fits JSR; over the CMI 3,500 limit. N.T. is back, so her ICMJE authorship is no longer blocked |
| Manuscript PDF | `paper/pdf/` | built | Typeset by `build_manuscript_pdf.py`, 21 citations resolved from the `.bib` |
| Search & screening | `revision_sistematica/` | done | 23,057 records → 17,129 unique → 233 reports → 184 studies, 124 extractable |
| Full-text retrieval | `revision_sistematica/textos_completos/` | 93 / 124 (75.0%) | Biased: the missing fraction holds 47.8% of the comparative designs. Requests drafted, **not yet sent** |
| Extraction | `revision_sistematica/extraccion/` | **complete + adjudicated** | D.V. extracted all 124; N.T. extracted 122. Median agreement 78%, median kappa 0.57. **559 of 575 disagreements adjudicated by consensus** on 2026-08-26; 2 closed by a superseded rule, 14 open |
| Submission package | `verificables revisión sistemática/` | built | S0–S13 + guide + both manuscripts. Data annexes ship twice: `.xlsx` to read, `.csv` to re-run |
| JSR submission | `~/Desktop/Envio_JSR_Fagoterapia_Pseudomonas/` | built | Manuscript, cover letter, README and all 14 annexes, all generated by `build_jsr_submission.py`. 7 author markers left for D.V. |

**Where the extraction actually stands, as of 2026-08-26:**

1. **Duplicate extraction is COMPLETE.** N. Trelles withdrew on 2026-08-22 and
   **returned on 2026-08-26 with her extraction finished**: 122 of the 124
   studies, so 98% of the corpus is double-extracted. The withdrawal record
   `quality_reports/decisions/2026-08-23_retirada-segunda-revisora.md` is marked
   SUPERSEDED at its head; read that header before trusting anything in it.
2. `revision_sistematica/extraccion/extraction_conflicts.csv` holds 575 value
   conflicts over 130 compared arm rows: median agreement 78%, median informative
   kappa 0.57 (8 of 9 categorical fields). **559 are adjudicated by consensus**
   (both reviewers signed, 2026-08-26), 2 were closed by a mechanical rule on a
   comparison since redone and carry NO joint signature, and 14 are open. The
   split matters: `extraccion_conflictos_firmados` counts only the 559.
   Ingest new adjudications with `scripts/ingest_adjudications.py`, never by
   hand. See `quality_reports/decisions/2026-08-28_adjudicacion-por-consenso.md`.
3. **No published figure depends on the extraction workbooks yet.** All still
   come from `cribado/` and `pre_extraccion_desde_resumen.csv`. Now that the
   adjudication is done that *could* change — reporting outcomes, risk of bias
   and GRADE becomes possible — but it is a scope decision, not yet taken.
4. Screening false-negative rate is now measured: 0 of 350 excluded records
   re-screened blind in Rayyan (exact 95% CI 0.00–1.05%). See
   `revision_sistematica/validacion_rayyan/resultado.json`.
5. `compare_extractions.py` used to rewrite the conflicts file with the three
   resolution columns BLANK. Re-running the documented command would have wiped
   all 561 signatures. It now recovers them by `(study, arm, field)` key and
   reports how many it kept. Do not remove that step.
6. Do NOT trust an older conflict count. Until 2026-08-23 the comparator scored a
   cell one reviewer had filled and the other had not as a disagreement. Fixed in
   `ca12d6a`.
