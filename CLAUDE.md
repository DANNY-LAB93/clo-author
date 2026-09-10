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

# The three guards on the manuscript's numbers. The first two check against the
# pipeline; the third redoes the arithmetic from the text alone.
python scripts/check_manuscript_numbers.py     # toda cifra tiene origen
python scripts/check_manuscript_claims.py      # cada frase lleva SU escalar
python scripts/check_aritmetica.py             # las cuentas, rehechas
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

As of 2026-09-01. Every figure here is produced by the pipeline, not typed:
re-derive with `build_synthesis_scalars.py` and check with `check_manuscript_claims.py`.

| Component | File | Status | Description |
|-----------|------|--------|-------------|
| Manuscript | `paper/manuscrito_revision_sistematica.md` | drafted | 6,164 words of main text, abstract 264. Fits JSR; over the CMI 3,500 limit. New §3.1.1 reports the 29 exclusions with reasons; §2.9 now declares TWO amendments |
| Manuscript PDF | `paper/pdf/` | built | Typeset by `build_manuscript_pdf.py`, 21 citations resolved from the `.bib` |
| Search & screening | `revision_sistematica/` | done | 23,057 records → 17,129 unique → 233 reports → 184 assessed → **29 excluded after screening** (24 on reading the article, 4 on language, 1 on not being retrievable) → 155 studies, 95 extractable |
| Full-text retrieval | `revision_sistematica/textos_completos/` | 71 / 95 (74.7%) | Biased: the missing fraction holds 54.5% of the comparative designs. Re-checked 2026-09-02 against **three** independent indexes (Europe PMC, OpenAlex, Semantic Scholar): **0 of the 27 have an open copy**. **No requests will be made** — the interlibrary-loan and author-request route was dropped on D.V.'s instruction and its scripts and drafts deleted. The gap is reported as a limit, not as pending |
| Extraction | `revision_sistematica/extraccion/` | **complete + adjudicated** | D.V. extracted all 124; N.T. extracted 122. Median agreement 78%, median kappa 0.62. **525 of 541 disagreements adjudicated by consensus**; 2 closed by a superseded rule, 14 open |
| Submission package | `verificables revisión sistemática/` | built | S0–S16 + guide + both manuscripts. **S16** carries the 29 exclusions with their code, reason and the sentence from the article (PRISMA 16b, now CUMPLE). Data annexes ship twice: `.xlsx` to read, `.csv` to re-run |
| JSR submission | `~/Desktop/Envio_JSR_Fagoterapia_Pseudomonas/` | built | Manuscript, cover letter, README and all 14 annexes, all generated by `build_jsr_submission.py`. 7 author markers left for D.V. |

**Where things actually stand, as of 2026-09-09:**

1. **Duplicate extraction is COMPLETE and adjudicated.** D.V. extracted all
   124 studies, N.T. 122 of them — 98% double-extracted. Over 130 compared arm
   rows: 541 value conflicts, median agreement 78%, median informative kappa
   0.62. **525 adjudicated by consensus**; 2 closed by a rule on a comparison
   since redone (no joint signature), 14 open. `extraccion_conflictos_firmados`
   counts only the 525. Ingest with `ingest_adjudications.py`, never by hand.
   N.T.'s 2026-08-22 withdrawal record is marked SUPERSEDED at its head — read
   that header before trusting anything in it.
2. **Published figures come from TWO places.** Tables 1-4 and the PRISMA figure
   from `cribado/` and `pre_extraccion_desde_resumen.csv`; the outcome tables
   from the adjudicated extraction via `build_adjudicated_dataset.py` →
   `build_outcome_scalars.py`. The headline: **69 of 103 arms (67.0%)** have no
   operational definition of clinical success, and only 2 survive the four
   requirements for pooling — one of those measures time, so none remains.
   GRADE is NOT done and will not be: there is no pooled estimate whose
   certainty to rate. Risk of bias IS scoped — see item 10.
3. Screening false-negative rate is measured: 0 of 350 excluded records
   re-screened blind in Rayyan (exact 95% CI 0.00–1.05%). See
   `revision_sistematica/validacion_rayyan/resultado.json`.
4. **Two guards on the extraction comparator, neither removable.** It used to
   rewrite the conflicts file with the resolution columns BLANK — running the
   documented command would have wiped 561 signatures; it now recovers them by
   `(study, arm, field)` and reports how many it kept. And until 2026-08-23 it
   scored a cell one reviewer filled and the other did not as a disagreement,
   so no conflict count from before `ca12d6a` is comparable.

5. **22 studies were excluded on 2026-09-01 after reading their full texts**,
   and this is the corpus you now work with: **155 studies, 95 extractable, 103
   extracted arms** (29 exclusions as of 2026-09-02). They are NOT deleted from `study_groups.csv` — that file
   stays as the record of what screening decided. The exclusion is a separate
   layer, `revision_sistematica/cribado/exclusiones_tras_texto_completo.csv`,
   with a reason code, the sentence from the article and both signatures; the
   pipeline applies it when computing. Two new codes were added to the closed
   vocabulary: **PRO** (protocol, no results) and **INT** (the intervention is
   not a bacteriophage). See
   `quality_reports/decisions/2026-09-01_revision-uno-por-uno-de-los-textos-completos.md`.
6. **Two measurements of "before" must not be mixed.** The language amendment
   and the full-text re-reading each removed studies, and subtracting today's
   count from the pre-amendment one attributed both losses to language. Use
   `*_antes_de_la_enmienda` (before language) and `*_antes_de_releer` (after
   language, before re-reading). The scalars now carry both.
7. **The language criterion was verified on the ABSTRACT, not the article**, for
   every study without a retrieved full text — 29 of the 98. The evidence class
   was called "A. texto probado", which asserted more than was checked. Four
   Russian-journal studies entered the corpus that way and were excluded on
   2026-09-01 (code IDI) after measuring their publisher pages: 78–94 % Cyrillic
   body, no English edition. When retrieving a missing text, check the language
   **on the body and with machine translation OFF** — Chrome silently translated
   a Russian article into Spanish during this very check. See
   `quality_reports/decisions/2026-09-01_idioma-verificado-sobre-el-resumen-no-el-articulo.md`.
8. **There is no request route, by decision.** On 2026-09-02 D.V. dropped
    interlibrary loan and author requests, and `build_request_package.py` plus
    its three outputs were deleted. Removing it exposed a false claim: the
    acknowledgements thanked the library for "handling the interlibrary loan
    requests" and the authors "who responded to full-text requests" — **no
    request was ever sent**. That paragraph is gone. §3.2 now states what was
    actually done and that the gap is not mitigated.
9. **NOREC is an amendment of a different kind, and §2.9 says so.** Every other
    exclusion code refers to what the article SAYS; `NOREC` refers to what this
    review COULD NOT READ — a property of the process, not of the study. It is
    applied to one study (EST-118). The counterfactual is computed by the
    pipeline and declared in the manuscript because it is severe: applied to all
    24 studies still without text, the corpus falls 155 → 131, comparatives
    11 → 5, RCTs 7 → 3, and the retrieval rate becomes 100 % **by
    construction**, destroying the very bias §3.2 measures. Do not extend it
    without re-reading that paragraph.

10. **Risk of bias: scoped, by consensus, and NOT yet issued.** Comparative
    designs only, adjudicated on the article, not on the abstract: **12 with a
    comparison group, 11 assessable** (3 RoB 2, 8 ROBINS-I), 1 without full
    text. Judgements are **domain-level** — no RoB 2 signalling questions — so
    Methods says "a nivel de dominio" and must never imply the full algorithm.

    The two per-reviewer workbooks turned out NOT to be independent: the
    free-text column carried the same text character for character in all
    eleven annotated studies. Nudging 13 dropdowns afterwards produced 13
    disagreements and a kappa of 0.78 that measured nothing. D.V. decided on
    2026-09-05 to declare what happened: **evaluación por consenso, sin kappa**.
    See `quality_reports/decisions/2026-09-05_riesgo-de-sesgo-por-consenso.md`.

    The live file is `riesgo_sesgo_comparativos_consenso.xlsx`: 69 judgements
    pre-filled where both books agreed, **13 left blank** where they differed,
    plus a signature sheet. `ingest_rob.py --consenso` refuses without both
    names, the date, and all 82 decided. The two original workbooks stay as the
    record and are not filled further.

    `compare_rob.py` now refuses to present two symptoms as findings: perfect
    agreement over ≥20 responses, and ≥3 free-text notes identical word for
    word. The second is the one that survives someone editing dropdowns.

11. **A derived file must not outlive its data.** A 2026-09-05 test left
    `rob_comparativos_scalars.json` holding 82 invented judgements signed
    "PRUEBA A y PRUEBA B", and it was committed. `build_rob_table.py` now
    reconciles that file against the adjudicated CSV on every run and
    regenerates it if it claims more than the CSV holds.

12. **Three manuscripts, one state.** `rob_bloques.py` holds the risk-of-bias
    blocks for the master and the English translation; `build_rob_table.py`
    writes all three at once, in the pending or the finished wording. The
    master had gone on saying "neither assessment was carried out" while the
    journal manuscript already declared one in progress — and both ship in the
    same envelope.

13. **`check_aritmetica.py` recomputes; it does not consult the pipeline.**
    The other two checkers verify against the scalars, so a well-computed
    scalar badly worded in its sentence passes them (68.0 % where it was 68.9;
    "casi cuatro de cada diez" for 44.2 %). This one redoes the division, the
    PRISMA subtractions and the declared sums from the manuscript text alone.
