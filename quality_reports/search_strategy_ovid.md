# Ovid search strategy — Embase + MEDLINE

**Status:** READY TO RUN — not yet executed.
**Platform:** Ovid SP, multifile search (Embase + MEDLINE simultaneously, Ovid's own
de-duplication applied at the end).
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
vocabulary. This compounds defect 1 exactly where it hurts most: an indexer
assigns *Pseudomonas infection* and *phage therapy* to a case report whatever
words its authors chose, so Emtree/MeSH retrieves precisely the studies free-text
resistance terms miss. Ovid is the reason to expect a different result here —
not because Embase holds more records than Scopus, but because this is the first
search of this review to use indexing at all.

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
2     exp Pseudomonas infection/
3     ("Pseudomonas aeruginosa" or "P aeruginosa" or "P. aeruginosa" or pseudomonal).ti,ab,kw.
4     1 or 2 or 3

5     exp Bacteriophage/
6     exp phage therapy/
7     (phage* or bacteriophage* or "phage therapy" or "phage treatment" or phagotherap* or "Pyophage" or "Intestiphage" or "phage cocktail").ti,ab,kw.
8     5 or 6 or 7

9     4 and 8

10    limit 9 to (human and yr="2016 -Current")

11    limit 10 to (case reports or "clinical trial, all" or comparative study or
      controlled clinical trial or evaluation studies or multicenter study or
      observational study or randomized controlled trial or "review")

12    9 and (case report/ or case study/ or clinical trial/ or cohort analysis/ or
      compassionate use/ or "named patient"/ or salvage therapy/)

13    10 not (animal/ not human/)

14    13 and (multidrug resistan* or multi-drug resistan* or MDR or "extensively
      drug resistan*" or XDR or "pandrug resistan*" or PDR or "difficult to treat"
      or DTR or "drug resistan*" or "antibiotic resistan*").ti,ab,kw.

15    remove duplicates from 13
```

**Line 13 is the set to export**, not line 14 and not line 11.

- **Line 10** is the honest core: organism AND phage, humans, in window. No
  resistance requirement, no publication-type requirement.
- **Line 11 and 12** are offered only if line 10 is unmanageably large. Prefer
  screening line 13 in full. If you do use 11 or 12, say so in the manuscript —
  a publication-type limit *is* a filter and Ovid's type tagging is imperfect for
  compassionate-use reports, which is precisely this review's study design.
- **Line 13** removes the animal-only literature, which is the bulk of the
  phage/*Pseudomonas* corpus and is the one exclusion that costs nothing. The
  `not (animal/ not human/)` form is deliberate: it drops records indexed animal
  *and not* human, and keeps records indexed both.
- **Line 14 is a measurement, not a step.** Report `13 minus 14` — the number of
  human clinical records that carry **no** resistance term. That count is the
  direct empirical answer to the round-5 criticism, and it belongs in the
  manuscript whatever it turns out to be.
- **Line 15** is Ovid's cross-file de-duplication (Embase against MEDLINE). Run
  it last. Ovid reports how many it removed; record that too.

### If Ovid rejects a field code

`.ti,ab,kw.` is valid in Ovid multifile across Embase and MEDLINE. If a line
errors, fall back to `.ti,ab.` and note the change — do **not** substitute `.mp.`,
which searches the full record including references and will inflate the count
with records that merely cite a phage paper.

Emtree and MeSH headings differ between the two files. `exp phage therapy/`
exists in Emtree; MEDLINE introduced *Phage Therapy* as MeSH in 2020, so
pre-2020 MEDLINE records rely on line 7. This is expected and is why the free-text
line is OR-ed with the headings rather than replaced by them.

---

## Export and hand-off

Export **line 13** (or 15 if de-duplicated) as **RIS** or **CSV including the DOI
and PMID/Embase accession fields**. Save to:

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

Per-line hit counts, the date, the Ovid interface version, and the two files
searched with their coverage dates (Ovid prints these — e.g. "Embase 1974 to
2026 Week NN", "Ovid MEDLINE(R) ALL 1946 to August 02, 2026"). The manuscript
reports per-database counts, so these cannot be reconstructed later from the
export alone.

Also record: the count at line 13, the count at line 14, and **their difference**.
