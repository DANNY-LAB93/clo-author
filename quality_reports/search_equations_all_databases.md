# Search equations — all databases

**Version:** 2026-08-03
**Status:** ready to run. Nothing here has been executed except the PubMed pair,
which was validated against the 42 included studies (see
`quality_reports/retrievability_pubmed.md`).

---

## The four design rules, and why each exists

These are not stylistic preferences. Each was forced by something this review got
wrong, and each is testable.

**1. No mandatory resistance block.** The Population criterion explicitly retains
arms with no resistance documentation — a missing susceptibility panel in a
salvage case report is a documentation gap, not evidence of susceptibility. A
search cannot require a keyword in order to find studies it then includes on the
ground that the keyword was never recorded. `Zaldastanishvili2021` and
`Green2023` carry no resistance term anywhere in title or abstract; no query with
a resistance block could ever have retrieved them.

**2. Two arms, and the second drops the ORGANISM block.** This is the finding
that matters most and it is not intuitive. Four included studies —
`Pirnay2024`, `Green2023`, `Leitner2021`, `Liu2025_perinephric` — are
multi-pathogen phage-therapy reports that name **no organism** in title, abstract
or controlled vocabulary. An architecture requiring "Pseudomonas aeruginosa"
cannot reach a paper titled *"Personalized bacteriophage therapy outcomes for 100
consecutive cases"* at any sensitivity. Pirnay is the corpus's largest single
contributor. Measured in PubMed: arm A covers 36 of 40, arm B covers 29, and only
their union covers 40.

**3. Controlled vocabulary is mandatory.** Every query this review ran before now
was free-text only. Qualifying a term with `[tiab]` **suppresses PubMed's
automatic MeSH mapping**, so the explicit field tag on every prior query means
indexing was never consulted, not even incidentally. Emtree/MeSH retrieves the
case report whose authors chose different words.

**4. Do not use a bare "limit to humans".** It matches the *Humans* index term
and silently drops records not yet indexed — which in a 2026 search is the newest
material. Tested: requiring MeSH Humans loses **11 of 42** known positives. Use
`NOT (animal NOT human)` instead, which removes only what is indexed animal *and
not* human and keeps the unindexed.

**Window:** 2016–2026 throughout.

---

## 1. PubMed / NCBI — validated

The only pair below that has been run. Coverage measured per study.

**Arm A — organism-first** *(1,481 records; covers 36/40)*

```
("Pseudomonas aeruginosa"[tiab] OR "P. aeruginosa"[tiab] OR "Pseudomonas aeruginosa"[MeSH])
AND ("phage"[tiab] OR "bacteriophage"[tiab] OR "phage therapy"[tiab] OR "bacteriophage therapy"[tiab]
     OR "phagotherapy"[tiab] OR "Bacteriophages"[MeSH] OR "Phage Therapy"[MeSH])
AND (case reports[pt] OR clinical trial[pt] OR observational study[pt]
     OR comparative study[pt] OR multicenter study[pt] OR journal article[pt])
AND ("2016"[dp] : "2026"[dp])
```

**Arm B — no organism block** *(8,532 records; covers 29/40, and is the only arm
that reaches the four multi-pathogen cohorts)*

```
("phage"[tiab] OR "bacteriophage"[tiab] OR "phage therapy"[tiab] OR "bacteriophage therapy"[tiab]
 OR "phagotherapy"[tiab] OR "Bacteriophages"[MeSH] OR "Phage Therapy"[MeSH])
AND humans[mh]
AND ("2016"[dp] : "2026"[dp])
```

> Arm B uses `humans[mh]` deliberately, despite rule 4, because without it the arm
> returns >27,000 records. The cost is quantified rather than hidden: the 11
> not-yet-indexed positives it would miss are all retrieved by arm A, so the
> union is unaffected. **This only holds because both arms are run.**

Union: 9,561 unique records, 40/40 coverage.

## 2. Scopus

Scopus has no controlled vocabulary, so both arms are free-text and arm B needs a
subject-area limit to stay tractable.

**Arm A**

```
TITLE-ABS-KEY ( ( "Pseudomonas aeruginosa" OR "P. aeruginosa" OR pseudomonal )
  AND ( phage* OR bacteriophage* OR phagotherap* OR "phage therapy"
        OR "phage cocktail" OR pyophage OR intestiphage ) )
AND PUBYEAR > 2015 AND PUBYEAR < 2027
```

**Arm B**

```
TITLE-ABS-KEY ( ( phage* OR bacteriophage* OR phagotherap* )
  AND ( "phage therapy" OR "bacteriophage therapy" OR compassionate OR salvage
        OR "expanded access" OR "named patient" OR "case report" OR "case series"
        OR patient OR patients OR clinical ) )
AND PUBYEAR > 2015 AND PUBYEAR < 2027
AND ( LIMIT-TO ( SUBJAREA , "MEDI" ) OR LIMIT-TO ( SUBJAREA , "IMMU" )
      OR LIMIT-TO ( SUBJAREA , "PHAR" ) )
```

> `phage*` is safe: it expands to phage, phages, phagemid — **not** phagocyte or
> phagocytosis, which begin *phago*. Do not shorten it to `phag*`, which pulls in
> the entire phagocytosis literature.
>
> The previous Scopus run used `PUBYEAR > 2018`, inconsistent with the stated
> 2016 window. Re-run from 2016 for a uniform audit trail.

## 3. Embase (Elsevier) via Ovid

**Access caveat: the institutional Ovid subscription was confirmed on 2026-08-03
to include MEDLINE only, not Embase.** This equation is written so it is ready if
access is obtained. Until it is run, Embase remains an unsearched database and a
declared limitation — it indexes several thousand journals absent from MEDLINE
and is markedly stronger on European and conference literature, which is where a
substantial part of the clinical phage corpus sits.

```
1     exp Pseudomonas aeruginosa/
2     exp Pseudomonas infection/
3     ("Pseudomonas aeruginosa" or "P aeruginosa" or "P. aeruginosa" or pseudomonal).ti,ab,kw.
4     1 or 2 or 3

5     exp Bacteriophage/
6     exp phage therapy/
7     (phage* or bacteriophage* or phagotherap* or "phage therapy" or "phage cocktail"
      or Pyophage or Intestiphage).ti,ab,kw.
8     5 or 6 or 7

9     4 and 8                                    <- ARM A
10    8 and (exp human/ or exp case report/ or exp clinical trial/
      or exp compassionate use/ or "named patient"/ or exp salvage therapy/)   <- ARM B
11    (9 or 10) not (exp animal/ not exp human/)
12    limit 11 to yr="2016 -Current"             <- EXPORT THIS
13    12 and (multidrug resistan* or MDR or "extensively drug resistan*" or XDR
      or "pandrug resistan*" or PDR or "drug resistan*").ti,ab,kw.
14    12 not 13                                  <- DIAGNOSTIC, not a filter
```

> Line 14 is the count of human phage records carrying **no** resistance term —
> the direct measure of what a resistance block would have excluded. Report it.
> Line 12 is the export set. Never export 13.

## 4. MyEBSCO (EBSCOhost)

Syntax varies by which databases the subscription exposes. `MH` is the exact
subject heading with `+` to explode; it works in MEDLINE-via-EBSCO and CINAHL,
but the heading names differ between them, so run the free-text lines regardless.
**Record which EBSCO databases were selected** — "EBSCO" is not a database and a
Methods section naming it without the panel is not reproducible.

**Arm A**

```
( MH "Pseudomonas aeruginosa+" OR MH "Pseudomonas Infections+"
  OR TI ("Pseudomonas aeruginosa" OR "P. aeruginosa") 
  OR AB ("Pseudomonas aeruginosa" OR "P. aeruginosa") )
AND
( MH "Bacteriophages+" OR MH "Phage Therapy+"
  OR TI (phage* OR bacteriophage* OR phagotherap*)
  OR AB (phage* OR bacteriophage* OR phagotherap*) )
```
Limiters: Published Date 2016-01 to 2026-12.

**Arm B**

```
( MH "Bacteriophages+" OR MH "Phage Therapy+"
  OR TI (phage* OR bacteriophage*) OR AB (phage* OR bacteriophage*) )
AND
( TI ("phage therapy" OR compassionate OR salvage OR "case report" OR patient*)
  OR AB ("phage therapy" OR "bacteriophage therapy" OR compassionate OR salvage
         OR "expanded access" OR "case report" OR "case series" OR patient*) )
```
Limiters: Published Date 2016-01 to 2026-12; Human (if the panel offers it —
record whether it was applied, per rule 4).

## 5. Cochrane Library (Wiley) — CENTRAL

CENTRAL is small enough that arm B needs no narrowing: run the intervention block
alone and screen it all. Use the Search Manager, one line per row.

```
#1   MeSH descriptor: [Pseudomonas aeruginosa] explode all trees
#2   MeSH descriptor: [Pseudomonas Infections] explode all trees
#3   ("Pseudomonas aeruginosa" OR "P aeruginosa" OR pseudomonal):ti,ab,kw
#4   #1 OR #2 OR #3
#5   MeSH descriptor: [Bacteriophages] explode all trees
#6   ("phage" OR "phages" OR bacteriophage* OR phagotherap* OR "phage therapy"
      OR "phage cocktail" OR Pyophage OR Intestiphage):ti,ab,kw
#7   #5 OR #6
#8   #4 AND #7                       <- ARM A
#9   #7                              <- ARM B: every phage record in CENTRAL
```
Set Custom Date Range 2016 to 2026. Export #9; it subsumes #8, and report both
counts. Record CENTRAL and CDSR separately — they are different databases and
PRISMA counts them separately.

## 6. ClinicalTrials.gov (NIH)

Registries hold protocol records, not publications, so the organism/no-organism
split is what matters and no date filter should be applied at search time —
registration precedes publication and a 2015 registration can produce a 2024
result.

**Arm A** — Condition/disease: `Pseudomonas aeruginosa` · Intervention:
`bacteriophage OR phage`

**Arm B** — Intervention: `bacteriophage OR phage`, all conditions.

Expert-search equivalents:

```
A:  AREA[ConditionSearch] "Pseudomonas aeruginosa" AND AREA[InterventionSearch] (bacteriophage OR phage)
B:  AREA[InterventionSearch] (bacteriophage OR phage)
```

Arm B is the operative one: a multi-pathogen trial registers its condition
generically, which is the registry analogue of the Pirnay problem. Export both
and record `NCT` ids — the corpus index already accepts an NCT as the identifier
for registry-only records.

## 7. EU clinical trials registers — BOTH of them

This is two registers, not one, and searching only the newer misses a decade.

**EU CTR / EudraCT** (`www.clinicaltrialsregister.eu`) — trials authorised under
Directive 2001/20/EC, i.e. the legacy record set. Its search is free text with
minimal boolean support, so keep terms short and run them separately rather than
combined:

```
bacteriophage
phage therapy
Pseudomonas aeruginosa AND phage
```

**CTIS** (`euclinicaltrials.eu`) — the register under Regulation 536/2014, which
replaced EudraCT for new trials from 2022 and became mandatory in 2025. Same
terms; the interfaces differ and neither inherits the other's records.

Record for each: the register name, the date searched, the exact string, and the
number of records. Neither register supports an export format the screening
pipeline can ingest, so transcribe results manually into the screening log with
their EudraCT / CTIS numbers.

---

## What to record for PRISMA, per database

PRISMA 2020 item 7 requires the full strategy for **every** source, including all
filters and limits. For each database and each arm:

| Field | Why |
|---|---|
| database and platform | "MEDLINE via Ovid" and "MEDLINE via EBSCO" are different searches |
| interface coverage dates | Ovid and EBSCO print these; they date the snapshot |
| date run | records change daily |
| exact string, verbatim | not a paraphrase |
| filters and limits applied | including any "humans" limit — see rule 4 |
| records returned, per arm | before de-duplication |
| records after de-duplication | and the tool that did it |

The un-recorded query is the failure this document exists to prevent: the review's
local PDF corpus retains its result set — 215 PMC identifiers — but **no query
string survives for it**, which is why that channel cannot be reproduced and is
being dropped.
