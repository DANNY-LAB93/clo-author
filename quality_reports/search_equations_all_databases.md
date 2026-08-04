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

## Executed searches — all counts verified 2026-08-03

| Source | Arm A | Arm B | Non-duplicating contribution |
|---|---|---|---|
| PubMed / NCBI | 1,481 | 8,532 | **9,561** union, corpus frozen |
| Scopus | 2,875 | 9,372 | — pending de-duplication |
| ProQuest | 1,013 | 3,403 | — pending de-duplication |
| Cochrane CENTRAL | 53 | 304 | **304** |
| ClinicalTrials.gov | 17 | 121 | **121** |
| BVS — LILACS 382, CUMED 37, BINACIS 35 | — | not applicable | **~454** |
| EudraCT | — | — | **3** |
| CTIS | — | — | **5** |

Not searched, with the reason recorded: **Embase** (not in the institutional
subscription), **Web of Science** (no route found), **EBSCO** (e-book collections
only, no bibliographic database).

De-duplication must run on **DOI, PMID *and* NCT**. CENTRAL ingests
ClinicalTrials.gov records and BVS includes MEDLINE, so two of these sources
overlap other sources by construction rather than by chance.

## What this institution actually provides — verified 2026-08-03

Checked directly against the UCACUE Biblioteca Virtual portal while
authenticated, not inferred from a subscription list.

| Source | Available | Evidence |
|---|---|---|
| PubMed / NCBI | ✅ free | both arms executed, 9,561 records |
| Scopus | ✅ subscribed | listed under "Bases de datos multidisciplinar" |
| Cochrane CENTRAL | ✅ | executed: 53 / 304, Issue 7 of 12, July 2026 |
| ClinicalTrials.gov | ✅ free | both arms executed, 17 / 121 |
| EU registers | ✅ free | EudraCT and CTIS, both open |
| BVS / LILACS | ✅ subscribed | in portal, **not yet used** |
| ProQuest | ✅ subscribed | 6 databases, **names not yet recorded** |
| **Web of Science** | ❌ | no route found — see below |
| **Embase** | ❌ | portal has Ovid MEDLINE, Ovid Español and Books Ovid Odontología; none is Embase |
| **EBSCO (bibliographic)** | ❌ | only two e-book collections |

**Web of Science.** Research4Life is subscribed and lists Clarivate as a content
provider, but the two entries are *Clarivate — Current Contents* and *Clarivate —
free*. Current Contents is a table-of-contents alerting service: no citation
index, no `TS=` field searching, no export suitable for systematic screening. It
is not Web of Science. Two routes remain unchecked and neither can be verified
from here — a CEDIA consortium licence held outside the portal, and whatever
route a colleague at this institution used. WoS overlaps heavily with Scopus for
this literature, so its absence is a declared limitation rather than a blocking
one; **Embase is the material gap.**

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

### Verified 2026-08-03

| Query | Documents |
|---|---|
| Arm A — organism-first, 2016–2026 | **2,875** |
| Arm B — no organism block, MEDI/IMMU/PHAR | **9,372** |

The previous Scopus run returned 860 records using `PUBYEAR > 2018` **and a
mandatory resistance block**. Removing the block and correcting the window to
2016 yields 2,875 on arm A alone — a 3.3-fold increase before arm B is counted.
That is the size of what the resistance block was costing in this database.

### ⚠️ Chrome's page translator silently rewrote the query

Typing arm A into the Scopus advanced-search box produced this **as the field's
actual value**, not merely its rendered appearance:

```
TÍTULO-ABS-KEY ( ( "Pseudomonas aeruginosa" O "P. aeruginosa" O pseudomonal )
Y ( fago* O bacteriófago* O fagoterapia* O "terapia con fagos"
O "cóctel de fagos" O piófago O intestífago ) ) Y PUBYEAR > 2015 ...
```

`TITLE-ABS-KEY` became `TÍTULO-ABS-KEY`, `OR`/`AND` became `O`/`Y`, and **the
search terms themselves were translated** — `phage*` to `fago*`, `pyophage` to
`piófago`. Scopus's query box is a `contenteditable`, so the translator edited
the query, not a label. `document.documentElement.lang` was `es` and the root
carried the `translated` class.

Running that would have returned a number for a query nobody wrote, and nothing
downstream would have flagged it: the count would simply have been wrong.

**Mitigation, and it is the reason both counts above are trustworthy:** pass the
query in the URL instead of typing it into the page —

```
https://www.scopus.com/results/results.uri?sort=plf-f&src=s&sot=b&sdt=b&s=<URL-ENCODED QUERY>
```

The query travels as a URL parameter, so the translator never touches it, and
the results page then renders it back in English, which is the visual
confirmation that it arrived intact. **Verify that rendering every time.**

This hazard is not specific to Scopus. Any database whose search box is a
`contenteditable` — and any typed query on a page Chrome has decided to
translate — is exposed. Disable automatic translation for every database domain
before searching.

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

## 4. ~~MyEBSCO (EBSCOhost)~~ — VOID, there is no database to run it against

**Withdrawn 2026-08-03 after checking the institutional portal.** The UCACUE
Biblioteca Virtual exposes exactly two EBSCO products — *EBSCO eBooks Engineering
Core* and *EBSCO eBooks Collection*. Both are **e-book collections**. There is no
CINAHL, no MEDLINE-via-EBSCO, no Academic Search. The equation below has nowhere
to execute, and declaring EBSCO as a searched database would be false.

The strategy is retained struck-through rather than deleted, so that a reader of
this file's history can see the source was considered and why it was dropped.

<details><summary>Withdrawn equation</summary>

## ~~MyEBSCO (EBSCOhost)~~

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

</details>

## 5. Cochrane Library (Wiley) — CENTRAL — **verified and executed**

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

### Verified 2026-08-03

Run through the UCACUE portal, Title/Abstract/Keyword field:

| Query | Trials (CENTRAL) |
|---|---|
| `(bacteriophage OR phage) AND ("Pseudomonas aeruginosa" OR pseudomonal)` — arm A | **53** |
| `bacteriophage OR phage` — arm B | **304** |

Interface reports **"Cochrane Central Register of Controlled Trials, Issue 7 of
12, July 2026"** — record that string, it dates the snapshot. Cochrane Reviews,
Protocols, Editorials, Special Collections and Clinical Answers all returned
**0**, so CENTRAL is the only Cochrane database contributing. Export is enabled.

**Arm B at 304 records is small enough to screen in full.** Do that rather than
using arm A: it is the whole phage literature CENTRAL holds.

### Two findings from running it that change what can be claimed

**CENTRAL carries records sourced from Embase.** The CYPHY record is tagged
`Embase` in the results list. Cochrane runs its own systematic Embase searches
and deposits the trial records into CENTRAL. This **partially mitigates the
Embase gap — for controlled trials only.** CENTRAL holds trials; it does not hold
case reports or case series, which are roughly 90% of this review's corpus. State
the mitigation at exactly that width and no wider.

**CENTRAL also ingests ClinicalTrials.gov records.** The first arm-B result is
`NCT07698002`, one of the twelve registry candidates assessed separately. CENTRAL
and the ClinicalTrials.gov search therefore overlap, and de-duplication must run
across them on the NCT identifier, not only on DOI/PMID.

## 5b. BVS — Biblioteca Virtual en Salud (includes LILACS)

Subscribed and, until now, unused. **This is the most valuable addition available
to this review**, because LILACS indexes Latin American and Caribbean health
journals that neither MEDLINE nor Scopus covers — regional literature is exactly
the kind of coverage lost by not having Embase. It does not replace Embase; the
two index different literatures. It is a recognised source in systematic reviews.

BVS uses the iAH/VHL interface. Terms in Spanish, Portuguese and English, because
the corpus is trilingual and titles are indexed in the original language:

**Arm A**

```
(fago OR fagos OR bacteriofago OR bacteriófago OR bacteriofagos OR fagoterapia
 OR phage OR bacteriophage OR "phage therapy" OR "terapia con fagos"
 OR "terapia fágica" OR fagoterapia)
AND
("Pseudomonas aeruginosa" OR "P. aeruginosa" OR pseudomonas OR pseudomonal)
```

**Arm B**

```
(fago OR fagos OR bacteriofago OR bacteriófago OR fagoterapia OR phage
 OR bacteriophage OR "phage therapy" OR "terapia con fagos" OR "terapia fágica")
AND
(paciente OR pacientes OR "relato de caso" OR "reporte de caso" OR "serie de casos"
 OR "case report" OR clinico OR clínico OR clinical OR humano OR humanos)
```

### Verified 2026-08-03 — and arm B does not work here

| Query | LILACS Plus tab | Full BVS |
|---|---|---|
| Arm A — phage terms AND Pseudomonas | 109 | 5,649 |
| Arm B — phage terms AND clinical terms | 999 (capped) | 35,466 |
| Intervention block alone | 2,379 | 119,561 |

**Arm B is unusable in BVS and should not be run.** Its clinical block —
*paciente*, *clínico*, *humano*, *case report* — does not discriminate in a
database whose entire content is clinical, and the tab caps at 999 rather than
reporting a true count. The design rationale for arm B (reaching multi-pathogen
cohorts that name no organism) is better served here the way it is in CENTRAL:
run the intervention block alone and screen everything.

### The tab label is misleading, and the facet is what counts

**"Colección LILACS Plus" is not LILACS.** For the intervention-block query the
database facet reports:

| Database | Records |
|---|---|
| MEDLINE | 1,815 |
| **LILACS** | **382** |
| **CUMED** (Cuba) | **37** |
| **BINACIS** (Argentina) | **35** |

So the 2,379 figure is roughly three-quarters MEDLINE, which duplicates the
PubMed arm in full. **The non-duplicating yield of this source is about 454
records** — LILACS, CUMED and BINACIS combined — and that is the number to
screen and the number to report.

Open **Más filtros → base de datos** and deselect MEDLINE before exporting.
Reporting the tab total instead would double-count PubMed and inflate the PRISMA
identification box by more than 1,800 records.

## 5c. ProQuest — the six databases, and none of them is biomedical

**Enumerated 2026-08-03** from *Cambiar bases de datos → Seleccionar bases de
datos*:

| # | Database | Coverage |
|---|---|---|
| 1 | Coronavirus Research Database | — |
| 2 | Ebook Central | — |
| 3 | Education Research Index (contains ERIC and Supplemental Education Index) | 1966– |
| 4 | PRISMA Database with HAPI Index | 1966– |
| 5 | ProQuest Central | 1970– |
| 6 | Publicly Available Content Database | — |

**There is no health or medical database in this package.** No ProQuest Health &
Medical Collection, no MEDLINE via ProQuest, no Public Health Database, no
Nursing & Allied Health. What is here is education (ERIC), books, a COVID
collection, a Latin American humanities index, a general multidisciplinary
collection, and an open-access aggregator.

That sets what ProQuest can contribute. Its 1,013 and 3,403 hits come mostly from
ProQuest Central, which is general rather than biomedical, and from Publicly
Available Content Database, which aggregates open access and will therefore
duplicate PubMed Central heavily. **Expect a low unique yield after
de-duplication and report it as measured rather than as expected.** ProQuest
should be declared as searched — it was — but the Methods should name these six
so a reader can see what was and was not covered, which is precisely what naming
"EBSCO" without its panel failed to do.

### A name collision worth stating explicitly

The portal lists this resource as **"Proquest + Prisma"**, and database 4 is the
**PRISMA Database with HAPI Index** — the *Hispanic American Periodicals Index*,
covering language, literature, social sciences, history and the arts. **It has
nothing to do with the PRISMA reporting guideline** this review follows. Anyone
reading "ProQuest + PRISMA" in a methods section will assume otherwise. Write the
full database name or do not abbreviate it.

## 5c-bis. ProQuest search syntax

Confirmed 2026-08-03: institutional access via UCACUE, banner reads *"Está
buscando en 6 bases de datos"*. **The six are not named on the search page and
must be read from "Cambiar bases de datos" and written into the Methods** — a
Methods section saying "ProQuest" without naming the constituent databases is not
reproducible, exactly as "EBSCO" was not.

ProQuest field codes: `TI`, `AB`, `SU` (subject), `NOFT` (all fields except full
text — prefer it over the default, which searches full text and inflates counts
with passing mentions).

**Arm A**

```
(TI("Pseudomonas aeruginosa" OR "P. aeruginosa") OR AB("Pseudomonas aeruginosa" OR "P. aeruginosa") OR SU("Pseudomonas aeruginosa"))
AND
(TI(phage* OR bacteriophage* OR phagotherap*) OR AB(phage* OR bacteriophage* OR phagotherap*) OR SU(bacteriophages))
AND pd(20160101-20261231)
```

**Arm B**

```
(TI(phage* OR bacteriophage*) OR AB(phage* OR bacteriophage*) OR SU(bacteriophages))
AND
(AB("phage therapy" OR "bacteriophage therapy" OR compassionate OR salvage
    OR "case report" OR "case series" OR patient*))
AND pd(20160101-20261231)
```

Do **not** tick "Texto completo" or "Evaluado por expertos" as limiters: the first
restricts to what this institution can read rather than to what exists, and the
second would drop case reports in non-indexed venues. Both are availability
filters masquerading as quality filters.

### Verified 2026-08-03

| Scope | Arm A |
|---|---|
| Default — subscribed content only | 999 |
| **"Mostrar resultados fuera de la suscripción de mi biblioteca" ticked** | **1,013** |

**Tick that box.** It is off by default, and left off the search silently returns
what this library can read rather than what exists — an availability filter
applied before screening, which is not a defensible thing to do in a systematic
review. Here it hides only 14 records, but the size of the effect is not the
point: it is not measurable in advance and it varies by topic.

The 999 default reading is also a trap for a different reason: it looks exactly
like a display cap, and BVS's tab genuinely does cap at 999. Two adjacent
databases, the same number, one real and one an artefact. Check by changing the
scope and seeing whether the number moves.

ProQuest's query box is a real `<textarea>`, so the Chrome-translator hazard
documented under Scopus does not apply here — `.value` is untouched by page
translation. Verified: `document.documentElement.lang` was `es` while the query
round-tripped in English.

**Arm B: 3,403** (2026-08-03). The subscription toggle made no difference to this
set, unlike arm A where it moved 999 → 1,013.

**A submission quirk worth knowing.** Setting the query by script does not
register with ProQuest's form handler — the value appears in the box and the
search never runs. Type it, and click the *visible* "Buscar" button; the page
carries more than one element with that label and the off-screen one does
nothing. Both failures look identical from outside: the page simply stays on
`/advanced` with no error.

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

### Verified 2026-08-03 — both registers, and both have traps

**EU CTR / EudraCT** — one term at a time, because its search does **no partial
matching**:

| Term | Results |
|---|---|
| `bacteriophage` | 2 |
| `phage` | 2 |
| `"Pseudomonas aeruginosa"` | 114 (1 phage-related on page 1) |

`phage` does **not** retrieve records containing *bacteriophage*, and the two
queries return different sets. Union: **3 unique trials**.

| EudraCT | Sponsor | Disposition |
|---|---|---|
| 2022-003810-35 | BiomX Ltd. | already in corpus (BX004-A / Weiner 2025) |
| 2014-000714-65 | Pherecydes Pharma | already in corpus (PhagoBurn / Jault 2019) — **register holds posted results** |
| 2021-004469-11 | Pherecydes Pharma | exclude — *Staphylococcus aureus* PJI, wrong pathogen |

PhagoBurn's EudraCT record carries "View results". The review currently cites the
publication; the register's posted results are a second, independent source for
that trial's outcomes and should be checked against it.

**CTIS** — 5 phage trials, none of them in this corpus:

| CTIS number | Trial |
|---|---|
| 2025-521533-85-00 | TP-122_101A, Phase 1/2a bacteriophage cocktail |
| 2024-519856-94-00 | BMX-04-002, Phase 2b nebulized bacteriophage |
| 2023-507737-17-00 | HY-133, first-in-man |
| 2023-508825-29-00 | Phase 1/2a bacteriophage cocktail |
| 2023-507716-13-00 | TP-102_102, Phase 2b topical bacteriophage |

### ⚠️ CTIS's "Contain any of these terms" is not an OR

Searching `bacteriophage phage` in the field labelled **"Contain any of these
terms"** returns **0 results**. Searching `bacteriophage` alone returns **5**.
Adding a term that should broaden the search emptied it, so the field behaves as
a phrase or an AND, not the disjunction its label promises.

A reviewer who entered both terms once would record zero and conclude the
register holds no phage trials. It holds five, at least one of which
(TP-102) also appears in ClinicalTrials.gov as NCT04803708.

**Run one term per search in CTIS, and union the results by hand.** The same rule
already applies to EudraCT for a different reason (no partial matching), so the
instruction is uniform across both registers even though the underlying causes
differ.

**Positive control.** Before believing any zero from CTIS, run a term that must
return results: `cancer` gave **3,036**. A zero without a control is not a
finding, it is an untested assumption — the first `bacteriophage phage` run in
this session returned 0 with an *empty* field, and the number looked identical to
a real one.

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
