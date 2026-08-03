# Ovid search strategy — Embase + MEDLINE

**Status:** READY TO RUN — not yet executed.
**Platform:** Ovid SP, **Ovid MEDLINE(R) ALL only**. The institutional
subscription does not include Embase (confirmed 2026-08-03), so this is a
single-file search and the multifile de-duplication step does not apply.
**Window:** 2016 to current, matching the pre-specified window in
`paper/sections/methods.tex` (Section `sec:methods-search`).

---

## Why this search exists, and what it fixes

The review currently rests on PubMed/MEDLINE, Scopus and ClinicalTrials.gov. Two
defects in that base are documented in the manuscript and both are structural
rather than incidental.

**1. Every executed query required a resistance term in title or abstract.** The
Population criterion explicitly *retains* arms with no resistance documentation
at all — a missing susceptibility panel in a salvage case report is treated as a
documentation gap, not as evidence of susceptibility. A search cannot require a
keyword in order to find studies it then includes on the ground that the keyword
was never recorded. This was the binding criticism of both round-5 referees, and
screening the four studies one referee named confirmed it: `Zaldastanishvili2021`
contributes two eligible arms and `Green2023` one, and **none of those records
carries a resistance term in its title or abstract**. No query this review had
run could have retrieved them.

When the resistance block was removed from PubMed the yield was not marginal: 45
records, 28 never screened, **nine of which entered the analytic dataset**. That
is the strongest available evidence that the block, not the database list, was
the constraint.

**2. Every executed query was free-text only.** Both the PubMed `[tiab]` and the
Scopus `TITLE-ABS-KEY` searches match author wording. Neither touches controlled
vocabulary. This is not a matter of degree: qualifying a term with `[tiab]`
**suppresses PubMed's automatic term mapping**, so the explicit field tag on
every query this review ran means MeSH was never consulted, not even
incidentally. The defect compounds defect 1 exactly where it hurts most, because
an indexer assigns *Pseudomonas Infections* and *Bacteriophages* to a case report
whatever words its authors chose — which is precisely the class of study that
free-text resistance terms miss.

## What this search is, and what it is not

With Embase unavailable this is **not a new database**. PubMed already covers
MEDLINE and covers it more broadly, holding ahead-of-print and
PubMed-not-MEDLINE records that Ovid MEDLINE does not. What is new is the
**retrieval axis**: controlled vocabulary, on a database this review has only
ever searched by free text. It is a methodological check on defect 2 and must be
reported as such — not as a fourth database, which would overstate it.

Both outcomes are worth having. If it surfaces eligible studies, the
free-text-only defect cost the review real evidence and the corpus grows. If it
surfaces none, that is a substantive completeness result — it shows the
un-blocked free-text strategy was not missing indexed studies — and belongs in
the manuscript rather than being quietly dropped. A search whose null result is
publishable is worth running.

**This does not close the Embase gap.** Embase indexes several thousand journals
absent from MEDLINE and is markedly stronger on European and conference
literature, which is where a substantial part of the clinical phage corpus sits
(the Eliava Institute, the Belgian consortium, the Hirszfeld Institute). That gap
stays open and stays a declared limitation until someone with Embase access runs
the same strategy.

**Therefore the core set below has no resistance block.** Resistance terms appear
only in line 14, and only to *measure* what the old strategy would have excluded.
Line 14 is a diagnostic, never a filter.

---

## The strategy

Enter one line at a time in Ovid Advanced Search (Multi-Field / command line).
Ovid will echo a hit count per line; **record every count** — the PRISMA flow
needs per-line numbers, not just the final total.

```
1     exp Pseudomonas aeruginosa/
2     exp Pseudomonas Infections/
3     ("Pseudomonas aeruginosa" or "P aeruginosa" or "P. aeruginosa" or pseudomonal).ti,ab,kf.
4     1 or 2 or 3

5     exp Bacteriophages/
6     Phage Therapy/
7     (phage* or bacteriophage* or "phage therapy" or "phage treatment" or phagotherap* or Pyophage or Intestiphage or "phage cocktail").ti,ab,kf.
8     5 or 6 or 7

9     4 and 8

10    limit 9 to (humans and yr="2016 -Current")

11    9 not (exp Animals/ not exp Humans/)

12    11 and yr="2016 -Current"

13    12 and (exp Compassionate Use Trials/ or exp Salvage Therapy/ or
      case reports.pt. or clinical trial.pt. or randomized controlled trial.pt. or
      observational study.pt. or multicenter study.pt.)

14    12 and (multidrug resistan* or multi-drug resistan* or MDR or "extensively
      drug resistan*" or XDR or "pandrug resistan*" or PDR or "difficult to treat"
      or DTR or "drug resistan*" or "antibiotic resistan*").ti,ab,kf.

15    12 not 14
```

**Line 12 is the set to export** — not 10, not 13, not 14.

- **Line 9** is the honest core: organism AND phage, with no resistance
  requirement and no publication-type requirement.
- **Line 10 and line 12 are alternatives, and 12 is preferred.** Ovid's
  `limit to humans` matches the *Humans* MeSH tag, so it silently drops records
  not yet MeSH-indexed — ahead-of-print and recently added records, which for a
  2026 search is exactly the newest and most relevant material. Line 11's
  `not (exp Animals/ not exp Humans/)` removes only records indexed animal *and
  not* human, keeping both the human-indexed and the not-yet-indexed. Run line 10
  anyway and record its count: **10 versus 12 measures how much the conventional
  humans limit would have cost**, which is worth a sentence in the manuscript.
- **Line 13 only if line 12 is unmanageably large**, and declare it if used. A
  publication-type limit *is* a filter, and MEDLINE's type tagging is weakest for
  compassionate-use and salvage reports — which is this review's dominant study
  design, so this is the filter most likely to remove exactly what we want.
- **Line 14 is a measurement, not a step.** Do not screen from it.
- **Line 15 is the finding.** It is the set of human phage/*Pseudomonas* records
  carrying **no** resistance term anywhere in title, abstract or author keywords —
  precisely the records every prior query of this review was structurally
  incapable of retrieving. Its size is the direct empirical answer to the round-5
  criticism and belongs in the manuscript whatever it turns out to be. Screen it
  first: if a new eligible study exists, this is where it is.

### Field codes and headings

`.kf.` is the Ovid MEDLINE field for author keywords. If a line errors, fall back
to `.ti,ab.` and note the change — do **not** substitute `.mp.`, which searches
the full record including the reference list and will inflate counts with records
that merely cite a phage paper.

*Phage Therapy* entered MeSH only in the 2020s, so line 6 retrieves nothing from
earlier records and the 2016–2019 window rests on lines 5 and 7. This is why the
free-text line is OR-ed with the headings rather than replaced by them, and it is
also why the controlled-vocabulary gain is concentrated in the recent literature.

If `Phage Therapy/` is rejected as unmapped, drop line 6 and re-number; lines 5
and 7 carry the block on their own.

---

## Export and hand-off

Export **line 12** as **RIS** or **CSV, including the DOI and PMID fields** —
Ovid omits identifiers under some citation-format presets, and an export without
them cannot be screened mechanically, which is the whole point. Save to:

```
data/raw/ovid_export_YYYY-MM-DD.ris
```

Then run:

```bash
python scripts/screen_ovid_export.py data/raw/ovid_export_2026-08-03.ris
```

That script diffs the export against `quality_reports/corpus_identifier_index.txt`
(42 studies, 123 identifiers) and splits the records into **already in the corpus**
/ **never screened**. It exists so that no record can be re-screened as new the
way `Ngauy2026` was — which happened because its extraction citation recorded page
numbers instead of a PMID, so no regex could match it.

---

## What must be recorded for PRISMA

Per-line hit counts, the date, the Ovid interface version, and the file searched
with its coverage dates (Ovid prints this — e.g. "Ovid MEDLINE(R) ALL 1946 to
August 02, 2026"). The manuscript reports per-database counts, so these cannot be
reconstructed later from the export alone.

Record specifically:

| Quantity | Why it is needed |
|---|---|
| count at line 9 | the un-blocked core, before any limit |
| count at line 10 | what the conventional `limit to humans` yields |
| count at line 12 | **the export set**; 12 minus 10 is the cost of that limit |
| count at line 14 | records carrying a resistance term |
| count at line 15 | **records carrying none** — the answer to the round-5 criticism |
| line 13, if used | and an explicit statement in the manuscript that it was used |

And state in the manuscript that this was **Ovid MEDLINE only**, that Embase was
unavailable to this review team, and that the search therefore tests controlled
vocabulary rather than adding a database. Claiming a fourth database here would
be false.
