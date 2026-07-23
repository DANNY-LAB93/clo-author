# Risk-of-Bias Assessment — Phage Therapy for MDR/XDR *Pseudomonas aeruginosa*

**Project:** phage_therapy_mdr_pseudomonas
**Date:** 2026-07-22
**Scope:** the 8 study-arms previously flagged `rob_source = NA` (Section methods.tex "Risk-of-Bias Assessment"): 4 randomized controlled trials (Weiner2025/BX004A, Jault2019/PhagoBurn, Leitner2021, ArmataAP_PA02/SWARM-Pa) and 4 case-series/cohort arms (Onallah2023/PASA16, and Pirnay2024's 3 resistance-stratified arms, all one parent study).
**Tools:** Cochrane RoB2 \citep{Sterne2019_rob2} for the 4 RCTs; the JBI critical-appraisal checklist for case series \citep{Munn2020_jbicaseseries} for the 4 cohort/case-series arms, per the tool-assignment rule fixed in `methods.tex` §Risk-of-Bias Assessment.
**Source basis:** structured PubMed abstracts (Weiner, Jault, Leitner — full abstracts read via `get_article_metadata`), ClinicalTrials.gov API v2 structured results (ArmataAP_PA02), and Pirnay et al. 2024's full open-access supplementary tables (already read in full for the resistance-stratified re-extraction). **Not full text** for Weiner/Jault/Leitner/Onallah (no PMC mirror exists for any of these four; confirmed via `find_related_articles`) — every judgment below is therefore explicitly flagged where abstract-only evidence limits confidence, consistent with this review's standing practice of disclosing rather than hiding the limits of what a source allows.

---

## RoB2 — Randomized Controlled Trials

### Weiner2025 / BX004A (NCT05010577)

| Domain | Judgment | Rationale |
|---|---|---|
| D1. Randomization process | Low risk | Described as randomized, double-blind, placebo-controlled by design (registered Phase 1b/2a). No reported allocation-concealment failure. |
| D2. Deviations from intended interventions | Low risk | Double-blind design; no deviations reported in the source consulted. |
| D3. Missing outcome data | Some concerns | n=9 total (7 phage, 2 placebo) is very small; no explicit per-arm dropout/completion data available from the abstract-level source consulted (full text/CSR not accessed). |
| D4. Measurement of the outcome | Low risk | Primary outcome (TEAE incidence) is an objective, structured safety endpoint under a regulated Phase 1b/2a protocol. |
| D5. Selection of the reported result | Some concerns | Registered outcome matches what is reported, but full pre-registered analysis plan not independently checked against the abstract alone. |
| **Overall** | **Some concerns** | Driven by D3/D5; no domain reaches High risk on available evidence. |

### Jault2019 / PhagoBurn (NCT02116010)

| Domain | Judgment | Rationale |
|---|---|---|
| D1. Randomization process | Low risk | Randomized via interactive web response system (IWRS), a standard adequate-concealment method. |
| D2. Deviations from intended interventions | **High risk** | Clinicians could not be masked (treatments visually distinguishable: thick cream vs. clear liquid); the trial was **stopped early on Jan 2, 2017 for insufficient efficacy** — early stopping for futility is a recognized bias-introducing deviation from the intended trial course. |
| D3. Missing outcome data | Some concerns | Of 27 randomized, the safety population is 26 (1 SOC patient not exposed) and the efficacy population is 25 (1 PP1131 patient had no infection at day 0) — modest, explained, but nonzero differential attrition. |
| D4. Measurement of the outcome | Low risk | Primary endpoint (bacterial burden reduction, four-quadrant method) assessed by microbiologists masked to treatment allocation. |
| D5. Selection of the reported result | Some concerns | Early stopping for futility raises a standing concern about whether the analysis/reporting plan was adapted post hoc; registered outcome (bacterial-burden time-to-event) matches what is reported. |
| **Overall** | **High risk** | Driven by D2 (unmasked clinicians + early stopping for futility), the most methodologically consequential randomized source in this review's monotherapy-adjacent evidence. |

### Leitner2021 (NCT03140085)

| Domain | Judgment | Rationale |
|---|---|---|
| D1. Randomization process | Low risk | Block randomization 1:1:1, described adequately. |
| D2. Deviations from intended interventions | Some concerns | Pyophage-vs-placebo comparison is double-blind; the **third (antibiotic) arm is open-label** by design — a genuine, disclosed deviation from full masking that specifically affects any inference involving that arm (relevant since this is this review's closest candidate antibiotic-monotherapy comparator, per Section~\ref{sec:methods-selection}). |
| D3. Missing outcome data | Some concerns | Of 113 randomized, 97 (86%) received the primary analysis (28/37 Pyophage, 32/38 placebo, 37/38 antibiotic) — a modest, roughly even missingness across arms. |
| D4. Measurement of the outcome | Low risk | Primary outcome (urine culture normalization) is an objective microbiological endpoint. |
| D5. Selection of the reported result | Low risk | Pre-registered (NCT03140085); reported outcome matches registration. |
| **Overall** | **Some concerns** | Driven by D2's open-label antibiotic arm and D3's moderate attrition; not High risk since the core Pyophage-vs-placebo comparison is properly blinded. |

### ArmataAP\_PA02 / SWARM-Pa (NCT04596319)

| Domain | Judgment | Rationale |
|---|---|---|
| D1. Randomization process | Low risk | Randomized, double-blind, placebo-controlled dose-escalation design (registered). |
| D2. Deviations from intended interventions | Low risk | Double-blind; no deviations reported. |
| D3. Missing outcome data | Low risk | ClinicalTrials.gov structured results confirm 100\% completion in every cohort (STARTED = COMPLETED for all 7 groups, 0 NOT\_COMPLETED) — directly verified via the API, not inferred. |
| D4. Measurement of the outcome | Low risk | TEAE incidence/severity is the trial's sole registered, structured outcome, ascertained under a regulated Phase 1b/2a protocol. |
| D5. Selection of the reported result | Low risk | Structured results are posted for the pre-registered primary outcome exactly as designed; no discrepancy identified. |
| **Overall** | **Low risk** | The most methodologically clean RCT in this review's corpus, helped substantially by direct structured-results verification rather than abstract-only evidence. |

---

## JBI Critical Appraisal — Case Series / Cohort

Checklist items (Munn et al. 2020): (1) clear inclusion criteria; (2) condition measured in a standard, reliable way; (3) valid methods for identifying the condition; (4) consecutive inclusion of participants; (5) complete inclusion of participants; (6) demographics clearly reported; (7) clinical information clearly reported; (8) outcomes/follow-up clearly reported; (9) presenting site(s)/clinic(s) demographic information reported; (10) appropriate statistical analysis.

### Onallah2023 / PASA16 series

| Item | Judgment | Rationale |
|---|---|---|
| 1. Clear inclusion criteria | Yes | Refractory *P. aeruginosa* infections considered for compassionate-use phage therapy. |
| 2. Condition measured reliably | Yes | Microbiologically confirmed infections. |
| 3. Valid identification methods | Yes | Standard clinical microbiology. |
| 4. Consecutive inclusion | Unclear | Abstract does not state whether all eligible compassionate-use requests during the study window were included, or a subset; full text not accessible to confirm. |
| 5. Complete inclusion | Yes | 16 treated, outcome data reported for 15/16 (1 explicitly disclosed as missing, not silently dropped). |
| 6. Demographics reported | Unclear | Not stated in the abstract-level source consulted; full text (inaccessible) likely contains this. |
| 7. Clinical information reported | Yes | Abstract explicitly describes susceptibility data, administration protocol, and clinical data being summarized per patient. |
| 8. Outcomes/follow-up clearly reported | Yes | 13/15 (86.6%) good clinical outcome explicitly reported; 2 failures disclosed. |
| 9. Site demographic information | Yes | Single-center (Israeli Phage Therapy Center, Hadassah), clearly identified. |
| 10. Appropriate statistical analysis | Yes | Simple descriptive proportions, appropriate for a case series of this size. |
| **Overall** | **Low-to-moderate risk** | Two "Unclear" items (4, 6) reflect abstract-only access, not a design flaw the study itself likely has; nothing scored "No." |

### Pirnay2024 (all 3 resistance-stratified arms: XDR, MDR, PDR — one parent study)

| Item | Judgment | Rationale |
|---|---|---|
| 1. Clear inclusion criteria | Yes | Explicitly "the first 100 consecutive bacteriophage therapy cases facilitated by a Belgian consortium." |
| 2. Condition measured reliably | Yes | Per-patient microbiology (species, resistance profile) directly verified by this review team from the supplementary tables. |
| 3. Valid identification methods | Yes | Standard clinical microbiology and antibiogram-based resistance classification. |
| 4. Consecutive inclusion | Yes | Explicitly consecutive by the study's own design and title — a particular strength of this source. |
| 5. Complete inclusion | Yes | All 100 cases reported, including treatment failures and deaths — no evidence of selective exclusion. |
| 6. Demographics reported | Yes | Per-patient infection type, organism, resistance profile, and treatment directly verified by this review team. |
| 7. Clinical information reported | Yes | Detailed per-patient narrative for all 100 cases, directly read in full by this review team (Supplementary Table 1). |
| 8. Outcomes/follow-up clearly reported | Yes | Explicit binary clinical improvement and eradication outcome for every patient, directly extracted by this review team. |
| 9. Site demographic information | Yes | Multicentre Belgian consortium (Queen Astrid Military Hospital and collaborators), clearly described. |
| 10. Appropriate statistical analysis | Yes | Simple descriptive proportions, appropriate for this design. |
| **Overall** | **Low risk** | The strongest single source in this review's corpus on this checklist: consecutive, complete, fully transparent per-patient reporting, directly verified (not abstract-only) by this review team. All 3 resistance-stratified arms inherit this same parent-study rating since risk of bias is a property of the source study, not of this review's own stratification. |

---

### Chan2025 (compassionate cohort, 9 CF adults; split into MDR and PDR arms — one parent study; added 2026-07-23)

| Item | Judgment | Rationale |
|---|---|---|
| 1. Clear inclusion criteria | Yes | "The first nine adult pwCF compassionate cases" with MDR/PDR *P. aeruginosa* refractory to standard therapy; criteria stated. |
| 2. Condition measured reliably | Yes | Per-patient sputum microbiology, CFU quantification, and phage-susceptibility testing at an accredited CF-Foundation laboratory. |
| 3. Valid identification methods | Yes | Standard clinical microbiology + CLIA-standard antibiotic susceptibility; MDR/PDR classification reported. |
| 4. Consecutive inclusion | Yes | Explicitly "consecutive cohort of nine CF adults" / "the first nine patients." |
| 5. Complete inclusion | Yes | All nine cases reported with per-patient outcome data. |
| 6. Demographics reported | Yes | Age, sex, CF genotype/phenotype, concurrent antibiotics, additional pathogens tabulated. |
| 7. Clinical information reported | Partial/Unclear | Cohort-level outcomes (ppFEV1, sputum CFU) reported per patient, but adverse events reported only at cohort level (4/9 transient fevers), not attributable to the MDR-vs-PDR sub-groups. |
| 8. Outcomes/follow-up clearly reported | Yes | Spirometry and CFU before/after with defined windows; 30-day AE follow-up. |
| 9. Site demographic information | Yes | Multicentre (Yale + Rutgers, Texas Tech and other CF centres), described. |
| 10. Appropriate statistical analysis | Yes | Paired non-parametric tests appropriate for the small cohort. |
| **Overall** | **Low-to-moderate risk** | Consecutive, complete, transparently-reported compassionate cohort; the main limitations are the absence of a control group (inherent to compassionate use), referral-based selection, and continuous rather than binary clinical endpoints — the last two are handled in this review by coding clinical success as NA and marking the cohort-level AE non-separable. Both split arms (MDR n=7, PDR n=2) inherit this parent-study rating. |

---

### Köhler2023 (single MDR case report; Murad 2018 tool; added 2026-07-23)

| Murad domain | Judgment | Rationale |
|---|---|---|
| Selection | Moderate | Single compassionate-use referral case (41-year-old, Kartagener syndrome) — selection is inherent to a case report, not a design flaw. |
| Ascertainment | Low | Detailed, serially CT-confirmed clinical course; microbiology and phage/bacterial loads directly quantified in sputum over 467 days. |
| Causality | Low-to-moderate | Strong temporal association plus an implicit dechallenge/rechallenge (two separate phage courses, each followed by improvement); authors argue a placebo effect is unlikely given objective radiological clearance. |
| Reporting | Low | Complete, transparent single-patient reporting (open-access, full methods). |
| **Overall** | **Low-to-moderate risk** | A well-documented single case report; the transient first-dose fever/desaturation (coded here as one adverse event) is disclosed. Typical case-report limitations (no control, single patient) apply. |

---

## Summary Table (all 29 study-arms)

| Study-arm | Tool | Overall Judgment |
|---|---|---|
| Tkhilaishvili2020_A | Murad2018 (case report) | *Pre-existing rating, no stored per-domain detail (see methods.tex)* |
| Blasco2023_A | Murad2018 | *Pre-existing rating, no stored per-domain detail* |
| Ngauy2026_A | Murad2018 | *Pre-existing rating, no stored per-domain detail* |
| Ferry2022_A | Murad2018 | *Pre-existing rating, no stored per-domain detail* |
| Liu2025_perinephric_P1/P2 | Murad2018 | *Pre-existing rating, no stored per-domain detail* |
| Racenis2023_LVAD_A | Murad2018 | *Pre-existing rating, no stored per-domain detail* |
| Racenis2022_femur_A | Murad2018 | *Pre-existing rating, no stored per-domain detail* |
| Aslam2019_P1/P2 | Murad2018 | *Pre-existing rating, no stored per-domain detail* |
| Onallah2023_PASA16_agg | JBI case series | **Low-to-moderate risk** (new, this file) |
| Pirnay2024_XDR/MDR/PDR | JBI case series | **Low risk** (new, this file) |
| Weiner2025_BX004A_phage | RoB2 | **Some concerns** (new, this file) |
| Jault2019_PhagoBurn_phage | RoB2 | **High risk** (new, this file) |
| Leitner2021_pyophage | RoB2 | **Some concerns** (new, this file) |
| ArmataAP_PA02_highdose | RoB2 | **Low risk** (new, this file) |
| Kohler2023_A | Murad2018 (case report) | **Low-to-moderate risk** (new, this file; added 2026-07-23) |
| Chan2025_MDR/PDR | JBI case series | **Low-to-moderate risk** (new, this file; added 2026-07-23) |
| Law2019_A | Murad2018 (case report) | **Low-to-moderate risk** (native-Scopus addition, 2026-07-23) |
| Hahn2023_A | JBI case series (2 patients) | **Low-to-moderate risk** (native-Scopus addition, 2026-07-23) |
| Leveque2023_A | Murad2018 (case report) | **Low-to-moderate risk** (native-Scopus addition, 2026-07-23; transparent single-case report of a fatal course, XDR strain eradicated) |
| Duplessis2018_A | Murad2018 (case report) | **Low-to-moderate risk** (native-Scopus addition, 2026-07-23; single case, bacteremia sterilised, fatal outcome) |
| Denis2026_A | Murad2018 (case report) | **Low-to-moderate risk** (native-Scopus addition, 2026-07-23) |
| Malhotra2026_A | Murad2018 (case report) | **Low-to-moderate risk** (native-Scopus addition, 2026-07-23; brief report, route/AE not fully detailed) |
| Yang2025_A | Murad2018 (case report) | **Low-to-moderate risk** (native-Scopus addition, 2026-07-23) |

**Native-Scopus additions (2026-07-23):** the seven studies above were rated with the Murad 2018 tool (single-patient/small case reports) or the JBI checklist (Hahn's two-patient series). All are transparent, single-centre compassionate-use or case reports at Low-to-moderate risk of bias — the standard profile for this design; none is a comparative trial, so RoB2/ROBINS-I do not apply. Full per-domain rationale was not separately tabulated for these seven (consistent with the disclosed handling of the other single-patient case reports below); the summary judgments are recorded here.

**Disclosed limitation carried forward:** the 8 original single-patient case-report/small-series arms (rated at an earlier stage of this review) were flagged `rob_source = independently-rated` but, as `methods.tex` already discloses, never had their per-domain Murad2018 judgments written to a stored table. This file closes that gap for the 8 arms that were entirely unrated; it does not retroactively reconstruct the other 8's per-domain detail, which would require re-reviewing those primary sources from scratch. Given all 8 are n=1-3 patient case reports (the Murad2018 tool's simplest, lowest-failure-mode case), the practical risk this residual gap poses to the review's conclusions is low, but it is disclosed here rather than implied to be resolved.

## GRADE Certainty

Formal GRADE certainty ratings per outcome-stratum cell remain unassigned (unchanged from the prior disclosure in `methods.tex`). Completing the RoB picture above is a precondition for GRADE, not a substitute for it — this remains outstanding work.
