# Provenance of the local document corpus

**Date:** 2026-08-03
**Corpus root:** `C:\Users\Equipo\Desktop\opcion 1` (outside the repository)
**Manifest:** `data/raw/document_corpus_manifest.csv` — one row per file
**Screening log:** `data/raw/local_screening_log.csv` — 75 records, imported verbatim

---

## Why this document exists

The manuscript names a local PDF corpus as a PRISMA identification channel
contributing eight records, and the folder it pointed at held no record of what
was in it or where any of it came from. A channel whose contents cannot be
enumerated cannot be re-screened — by a referee, or by the authors a year from
now. That is a reproducibility failure under PRISMA 2020 items 6–7, and it is a
different and more serious thing than the methodological limitation the
manuscript currently declares (single-reviewer, no dual independent screening).
Being candid that a channel was informal is not the same as being able to say
what was in it.

This document closes that gap. It is deliberately separate from the manuscript's
limitations section, because the finding cuts in both directions.

## What was actually there

| Folder | PDFs | Resolved to an identifier | Matching an included study |
|---|---|---|---|
| `PUBMED ELICIT` | 201 | 190 | 9 |
| `pubmed` | 73 | 72 | 4 |
| `SCOPUS ELICIT` | 61 | 56 | 2 |
| `SCOPUS` | 59 | 58 | 2 |
| **Total** | **394** | **376 (95.4%)** | **17 files → 12 distinct studies** |

**The manuscript declares one folder of 201 documents. Four exist, holding 394.**
The folder names themselves carry the provenance the manuscript said was absent:
`PUBMED ELICIT` and `SCOPUS ELICIT` record both the source database and the fact
that the batch was processed through Elicit.

Identifiers were recovered from the file name where present, then from PDF
document metadata (142 files), then from the text of page 1 (234 files). Page 1
only, deliberately: the reference list of any phage paper cites dozens of DOIs,
and scanning the full document would attribute other authors' identifiers to the
file.

## A structured screening log exists, and the pipeline said it did not

`scripts/R/14_prisma_counts.R` recorded, for five review rounds, that "this
review never kept a machine-readable screening log", and offered that as the
explanation for why the PRISMA screening-stage counts could not be derived.

**That was false.** `Cribado_Sistematico_COMPLETO_76_3.xlsx` holds 75 documents,
one row each, with a column per PICO criterion (population, intervention, design,
recency), a final decision, the verbatim text supporting it, the origin of the
bacterial strain, and whether the organism is *P. aeruginosa* specifically.

Decisions: **69 EXCLUIDO, 5 INCLUIDO, 1 EXCLUIDO (duplicado de #40)**.

The real cause is therefore narrower and less excusable than the one recorded:
the screening *was* documented; the documentation was not version-controlled, so
no script could read it and no referee could check it. It is now imported to
`data/raw/local_screening_log.csv`.

## The screening log agrees with the review's final dispositions

All five INCLUIDO decisions cohere with where those studies ended up:

| Screening-log decision | Disposition in this review |
|---|---|
| Aslam et al. 2019 | included |
| PhagoBurn (Jault et al.) | included; excluded from pooling by the population rule |
| Teney et al. 2024 | included, pooled |
| Personalised inhaled phage, cystic fibrosis (2025) | included |
| Van Nieuwenhuyse et al. 2022 | **excluded** — duplicate of the Pirnay consortium roster |

The informal channel and the formal review reached the same conclusions. That is
a corroboration of the corpus, not a threat to it — but it was unavailable as
evidence for as long as the log sat outside the repository.

## Every unresolved file was checked by hand

Eighteen files yielded no identifier. Each was inspected rather than assumed
irrelevant, because an unidentifiable clinical report is exactly how a study goes
missing:

- **Surana et al. 2026**, *Pan-Resistant P. aeruginosa Septic Shock in a
  Critically Ill Patient* — a genuine PDR clinical case report, and the one that
  most warranted checking. It is already a **documented full-text exclusion**: no
  phage was administered, the phages are named only as unavailable.
- *Refractory P. aeruginosa bronchopulmonary infection after lung transplant* —
  already in the corpus (Lévêque et al. 2023).
- The remaining sixteen are preclinical: phage isolation and characterisation,
  genome sequencing, biofilm assays, murine aerosol models, endolysin and
  artilysin engineering.

**No eligible study was missed in these folders.**

## By what search were these documents retrieved? — the queries were not recorded

This is the question the manifest does not answer, and the honest answer is that
**no query string survives for this channel.** The corpus root was searched
exhaustively for a search export — no `.nbib`, `.ris`, `.csv` or `.txt` from
PubMed or Scopus exists.

What does survive is the **result set, not the query**:

- `Descargar_PDFs.html` lists **215 unique PMC identifiers** under the heading
  "Mis Artículos Libres (PMC)" — a PubMed result set restricted to PMC free full
  text, from which the 201 files in `PUBMED ELICIT` were downloaded. Every link
  is a bare `ncbi.nlm.nih.gov/pmc/articles/PMCxxxxxxx/pdf/`. The file was searched
  for `term=`, `query=` and any parameterised PubMed URL: **there are none.**
- The folder names record the database and that the batch passed through Elicit.
- Two screening spreadsheets record the decisions.

Missing, for both PubMed and Scopus: the query string, the date the search was
run, the filters and limits applied, and the count at each stage. That is
**PRISMA 2020 item 7** ("full search strategies for all databases, registers and
websites, including any filters and limits used"), and for this channel it is not
recoverable. It must be declared as such. The 215 PMC identifiers should be
deposited as the supplementary record of what the search returned, since that is
the strongest evidence that does exist.

## The screening was performed by a language model, and the manuscript does not say so

`MARKDOWN_OUT/import os.py` is the screening script. It converts each PDF to
markdown and submits it to a **locally hosted large language model —
`qwen2.5-coder:7b` served by Ollama at `localhost:11434`** — under a prompt that
instructs it to act as a methodological reviewer, apply the PICO criteria, and
return `VERDICTO FINAL: [INCLUIDO o EXCLUIDO]` with a reason. The Scopus
spreadsheet independently confirms this: its justification column reads
"Excluido **automáticamente** por…".

The manuscript describes this channel as an *"informal, single-reviewer screening
pass"*. A reader will understand "single-reviewer" to mean one human rather than
two. **It was not a human.** This must be disclosed, with the model named — not
because the screen was necessarily worse (its decisions corroborate the review's
final dispositions, see above), but because undisclosed automated screening is a
misdescription of methods, and journal and ICMJE policy now require AI-assistance
disclosure.

The correct description is: an exploratory, non-PRISMA screening pass in which a
locally hosted language model (`qwen2.5-coder:7b`) applied the PICO criteria to
full-text conversions, with decisions recorded per record and subsequently
reviewed by the author.

### The automated screen applied a stricter recency criterion than the review

The prompt in `import os.py` sets *"Antigüedad: Fecha menor o igual a 5 años"* —
a five-year window, where this review's stated window is 2016–2026. A stricter
filter inside a channel is a mechanism for losing eligible studies, so it was
tested rather than assumed harmless.

**It was harmless, and this is now checkable rather than asserted.** In the
imported log, the number of records excluded on recency alone — with population,
intervention and design all met — is **zero**. Nine records fall in 2016–2020,
and each is marked as meeting the criterion, several with an explicit note that
the cutoff was extended to 2019. The relaxation was applied in practice. The
discrepancy should still be recorded, because it was undocumented and its
harmlessness was luck rather than design.

## What this changes, and what it does not

**Closed.** The channel is enumerable. Every included study traceable to it can
be named, and no included study depends on a source that cannot be reproduced.

**Not closed, and it should be stated in the manuscript:**

1. The manuscript describes **one** folder of 201 documents. There are **four**,
   holding 394. The described channel is a subset of the operation actually run.
2. The screening log covers **75** records, not 394. The other three folders were
   screened without a comparable log, or with one not yet located.
3. `Descargar_PDFs.html` records the PMC URL each file was fetched from, but
   names them `PMCxxxxxxx.pdf` while the files on disk are named by title. **Zero
   of 394 files could be matched back to a download URL.** The one true
   provenance artefact in the corpus is broken by a rename, and that is worth
   recording as a lesson rather than repairing retroactively — a re-derived link
   would be a guess.
4. The corpus lives outside the repository and is not under version control. The
   manifest fixes traceability; it does not fix custody.

## Recommendation for the manuscript

Replace "a 201-document PDF corpus" with an accurate description: a local
document corpus of 394 records across four database-labelled batches, screened in
part against a structured PICO log of 75 records whose decisions are reproduced
in `data/raw/local_screening_log.csv`, and enumerated in
`data/raw/document_corpus_manifest.csv`. State that 12 included studies are
traceable to it, that its screening decisions agree with the review's final
dispositions, and that the 18 unresolvable files were checked individually and
contained no eligible study.

That is a stronger claim than the one currently made, and unlike the current one
it can be verified.
