# Data Extraction Summary — Phage Therapy MDR/XDR *Pseudomonas aeruginosa*

**Date:** 2026-07-20
**Source:** `data/raw/phage_therapy_extraction_raw.csv` → `data/cleaned/phage_therapy_extraction_dataset.csv` (via `scripts/R/clean_phage_extraction.R`)

## Coverage

| Status | Rows | Notes |
|---|---|---|
| COMPLETE | 10 | Single-patient case reports/series with full extraction: Tkhilaishvili 2020, Blasco 2023, Ngauy 2026, Ferry 2022, Liu2025-perinephric (×2 arms), Racenis 2023 (LVAD), Racenis 2022 (femur), Aslam 2019 (Patient 1, Patient 2) |
| EXTRACTION_INCOMPLETE | 6 | Pirnay 2024 (11/49-patient detailed subset only), Onallah/Green 2023 PASA16 (aggregate n=15, missing exact AE count/MDR-XDR), Weiner 2025/BX004-A (arm split confirmed 7 phage/2 placebo, AE/Author-Correction not fully verified), Jault 2019/PhagoBurn (time-to-event primary outcome, AE/eradication/mortality not independently confirmed), Leitner 2021 (Pseudomonas subgroup blocked on access), Armata AP-PA02 (highest-dose cohort only, other cohorts not confirmed) |
| EXCLUDED_WRONG_PATHOGEN | 1 | Krakhotkin 2025 — confirmed via full text to contain zero *P. aeruginosa* cases |
| EXCLUDED_DUPLICATE | 1 | Dan2023 immune substudy — confirmed same patient as Aslam2019 Patient 1 |

**Total usable patients for the primary proportion pooling (combination-therapy stratum):** ~36 across ~12 study-arms (10 complete case reports + Pirnay's 11-patient subset + Onallah's 15-patient aggregate), all phage+antibiotic combination, all *P. aeruginosa*-confirmed.

## Critical Finding: Monotherapy Stratum Empty

**Zero studies provide a usable antibiotic-monotherapy comparator for *P. aeruginosa*.** Both candidate studies failed:
- Krakhotkin 2025 — zero Pseudomonas cases (wrong pathogen population entirely)
- Leitner 2021 — Pseudomonas is one of six covered pathogens, no subgroup breakdown found despite an exhaustive Round 4 literature search (PMC linkout, ResearchGate, ClinicalTrials.gov API, related systematic reviews)

Per the strategy memo's pre-specified decision rule (Sec. 5), this stratum is reported as "insufficient evidence" narratively, not pooled. See `quality_reports/decisions/strategy_phage_therapy_mdr_pseudomonas.md` (2026-07-20 update).

## Remaining Gaps (lower priority, deferred)

- Pirnay 2024: the other ~38 of 49 Pseudomonas patients are only in "Supplementary Table 1," a separate file not locatable via the routes attempted (ORBi postprint main text, PMC, guessed Nature supplementary-file URL pattern).
- Jault 2019/PhagoBurn: binary-timepoint AE/eradication/mortality counts (only the time-to-event primary endpoint is confirmed).
- Weiner 2025: Author Correction (PMID 41760669, Feb 2026) not checked for revised numbers.
- Onallah/Green 2023: exact adverse-event count and per-patient MDR/XDR status not available from the secondary source consulted (cell.com/ScienceDirect full text returned HTTP 403).
- Armata AP-PA02: only the highest-dose cohort's TEAE count is confirmed; other dose cohorts and any efficacy data are not.

None of these gaps block a first pooled analysis of the combination-therapy stratum — they would improve precision (more patients, more complete AE/mortality data) if closed in a future round.

## R Environment

R 4.6.1 installed at `C:\Program Files\R\R-4.6.1` (not on the sandbox's default PATH — invoke via full path or add to PATH). Packages installed to a user library (`Sys.getenv("R_LIBS_USER")`, since the system library is not writable): dplyr, readr, here, meta, metafor, clubSandwich, ggplot2 (plus dependencies). Scripts should call `.libPaths(c(Sys.getenv("R_LIBS_USER"), .libPaths()))` before `library()` calls, or the user should add the user library to their R profile.
