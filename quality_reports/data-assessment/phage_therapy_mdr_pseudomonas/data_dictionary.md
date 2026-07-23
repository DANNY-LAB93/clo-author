# Data Dictionary — Top Candidate Primary Sources

**Scope:** For a meta-analysis of proportions, the "variables" are the fields the systematic-review extraction form must capture from each primary study's full text, not columns in a downloadable microdataset. This dictionary documents (a) the extraction-form schema implied by the research spec, (b) what is actually reported in the three top-graded (Grade A) open-access primary studies, so the coder/data-engineer knows what will and won't need author contact, and (c) — new in this revision — selection and external-validity caveats specific to the two largest aggregate cohort sources, plus a note on the reusable case-level dataset identified in `data_sources.md` Part 2.

---

## 1. Universal Extraction-Form Schema (per study-arm/regimen)

Per `research_spec_phage_therapy_mdr_pseudomonas.md` §Data, every eligible study-arm needs:

| Field | Type | Definition | Notes |
|---|---|---|---|
| `study_id` | string | First author + year (+ letter if multiple arms) | Unit of observation is study-**arm**, not study |
| `n_arm` | integer | Sample size in this arm/regimen | Denominator for all proportions below |
| `pathogen_scope` | categorical | Pseudomonas-only / mixed-pathogen-with-Pseudomonas-subgroup / mixed-not-separable | Mixed-not-separable arms are excluded per eligibility |
| `resistance_class` | categorical | MDR / XDR / PDR / not classifiable | Per Magiorakos et al. (2012) where derivable; else per study's own label (flag as `resistance_class_source` = author-reported vs. independently-verified) |
| `route` | categorical | topical/local, IV, inhaled/nebulized, oral, intra-articular, other | Pre-specified stratification variable |
| `modality` | categorical | phage monotherapy, phage+antibiotic combination, antibiotic monotherapy (rare) | Pre-specified stratification variable |
| `clinical_success_n` / `clinical_success_definition` | integer / free text | Numerator for primary outcome + the study's own definition (heterogeneous — must be tabulated per study, not assumed uniform) | |
| `adverse_event_n` | integer | Numerator for safety outcome (≥1 AE) | Serious AEs extracted separately where reported |
| `microbio_eradication_n` | integer | Secondary outcome numerator | |
| `mortality_n` | integer | Secondary outcome numerator | |
| `los_days` | continuous/summary stat | Length of hospitalization | Often reported as median/IQR, not mean — extraction form must accommodate both |
| `resistance_emergence_n` | integer | Resistance emerging during treatment | Frequently unreported — expect high missingness |
| `study_design` | categorical | RCT / prospective cohort / retrospective cohort / case series / compassionate-use | Feeds risk-of-bias tool selection (RoB2 vs. ROBINS-I vs. case-series checklist) |

---

## 2. What the Grade-A Open-Access Sources Actually Report

### Pirnay et al. (2024), *Nature Microbiology* — 100 consecutive cases

| Field | Reported? | Detail |
|---|---|---|
| `n_arm` | Yes | 100 total cases; 49/100 target pathogen = *P. aeruginosa* (largest single pathogen group) |
| `resistance_class` | Partial | MDR status implied by "difficult-to-treat"/refractory framing, but a clean MDR-vs-XDR breakdown per Magiorakos criteria is **not confirmed as reported** — requires close full-text/supplementary-table check during extraction; may need author contact (see `access_instructions.md`) |
| `route` | Yes | Multiple routes used across the cohort (the paper reports route information at the case level) — needs per-*Pseudomonas*-case extraction, not just cohort-level |
| `modality` | Yes — this is a **key finding of the paper itself**: regression analysis reports bacterial clearance ~70% less probable when phage was *not* combined with antibiotics, i.e., the paper already separates phage-alone vs. phage+antibiotic within its cohort | Directly usable for the monotherapy-vs-combination stratification, at least descriptively (not a report of proportions per se, but the underlying data should allow reconstruction) |
| `clinical_success_n` | Yes | Cohort-level: bacterial eradication 77.2%, clinical improvement 61.3% (per secondary-source summary) — *Pseudomonas*-specific sub-proportions need to be extracted from full text/supplementary tables, not assumed equal to the pooled cohort figure |
| `adverse_event_n` | Yes | 15 adverse events reported, 7 non-serious drug reactions suspected linked to BT (cohort-level; *Pseudomonas*-specific breakdown needs verification) |
| `study_design` | Yes | Multicentre, multinational, retrospective observational (single-arm) |

**Extraction risk:** This is a large, valuable dataset, but most reported statistics are cohort-wide (all 100 patients, all pathogens), not *Pseudomonas*-specific. The 49 *P. aeruginosa* cases will need to be isolated from the paper's supplementary tables (if patient-level or pathogen-stratified tables exist) — confirm during full-text extraction whether a patient-level supplementary table is included (common in Nature Microbiology papers of this type) before assuming this requires author contact. **Cross-check option (new):** Liu et al. 2025's supplementary `mmc2.pdf` (see `data_sources.md` Part 2) includes multiple case-level rows explicitly sourced from Pirnay et al. 2024 and tagged `bacteria_species_target = "pa"` — this can serve as an independent cross-validation source once this project's own extraction from Pirnay's supplementary tables is complete, though it should not substitute for that extraction (see reuse caveats in `data_sources.md`).

### Weiner et al. 2025 (BX004-A), *Nature Communications*

| Field | Reported? | Detail |
|---|---|---|
| `n_arm` | Yes | n=9 adult CF patients total; per-arm split (treatment vs. placebo) not given in the abstract — full text needed |
| `resistance_class` | No | Population is "chronic pulmonary *P. aeruginosa* infection" in CF — **not necessarily MDR-defined**; this is a structural eligibility caveat already flagged by the librarian, not just an extraction gap |
| `route` | Yes | Inhaled/nebulized |
| `modality` | Yes | Phage (BX004-A) as add-on to background antibiotics vs. placebo add-on to background antibiotics |
| `clinical_success_n` | Partial | Primary endpoint is safety/tolerability, not clinical success in the review's sense; exploratory sputum *P. aeruginosa* density reduction reported directionally but authors explicitly caution against efficacy conclusions given n=9 — expect this study to contribute mainly to the **safety** proportion, with clinical-success extraction flagged low-confidence/high-uncertainty |
| `adverse_event_n` | Yes | Primary endpoint — should be directly extractable from full text/tables |
| `study_design` | Yes | RCT, double-blind, placebo-controlled |

**Extraction risk:** An Author Correction (PMID 41760669, Feb 2026) exists — **do not extract numbers from the original without cross-checking the correction first.**

### Green et al. 2023 (PASA16), *Med* (Cell Press)

| Field | Reported? | Detail |
|---|---|---|
| `n_arm` | Yes | Case series (n reported as up to 16 patients treated; "13 of 15 patients with available data" achieved favorable outcome per secondary-source summary — confirm exact denominator in full text, since 15 vs. 16 discrepancy suggests missing-data handling that must be extracted precisely) |
| `resistance_class` | Likely Yes | "Refractory" *P. aeruginosa* infections — population selected for treatment failure, consistent with MDR/XDR though exact classification method needs full-text confirmation |
| `route` | To confirm | Not established from secondary sources — extract from full text |
| `modality` | Likely combination | Compassionate-use phage therapy typically layered on ongoing antibiotic treatment — confirm exact modality per patient in full text |
| `clinical_success_n` | Yes | ~86.6% success rate reported (13/15) |
| `adverse_event_n` | Yes | "Minimal side effects" reported — exact count needs full-text extraction, not just the qualitative summary |
| `study_design` | Yes | Single-arm compassionate-use case series |

**Extraction risk:** Author-name discrepancy flagged in `data_sources.md` (secondary source called this "Onallah et al." vs. the bibliography's "Green et al.") — resolve directly from the full text's author byline before the coder builds the extraction spreadsheet, to avoid a citation error propagating downstream. Note: Liu et al. 2025's `mmc2.pdf` cross-tabulates several rows explicitly under "Onallah 2023" as a *separate* citation from "Green 2023," which is itself informative — it suggests these may be two distinct publications/reports rather than a single misattributed one, and should be checked directly during full-text review rather than assumed to be the same underlying case series.

---

## 3. Fields Expected to Require Author Contact (Cross-Study Pattern)

Based on the above, the fields most likely to be under-reported in abstracts/secondary sources and to require either supplementary-table mining or direct author contact are:

1. **Pathogen-specific (Pseudomonas-only) sub-proportions** within mixed-pathogen studies (Pirnay 2024, TP-102) — check supplementary tables first; contact authors only if genuinely absent.
2. **MDR-vs-XDR breakdown per Magiorakos criteria** — expected to be the single largest source of "author-reported, not independently verifiable" classification across nearly all studies (flagged as Open Question #3 in the research spec).
3. **Route-specific outcome proportions** where a study uses phage therapy across multiple administration routes within one cohort (Pirnay 2024 in particular).
4. **Monotherapy-only proportions** — expected to be genuinely sparse or absent in most studies (Open Question #5 in the research spec); this may be a field where the answer is "not extractable from any current source" rather than "extractable with author contact."

---

## 4. Selection-into-Treatment: Who Is (and Isn't) in the Two Largest Aggregate Cohorts

Pirnay et al. 2024 (100 consecutive cases, Belgian consortium) and the Israeli Phage Therapy Center's 5-year compassionate-use report (PMID 37234511) are both, by construction, **referral / compassionate-use populations**, not unselected consecutive infections drawn from a general clinical population. Patients enter these cohorts only after: (a) conventional antibiotic therapy has already failed, typically across multiple regimens over months or years; (b) a treating physician has identified and actively pursued a specific regulatory access pathway (Belgium's magistral-preparation framework for the Pirnay consortium; Israel's Ministry-of-Health-authorized compassionate-use process for the IPTC); and (c) a phage-matching/production pipeline was successfully executed in time — i.e., an active phage against the patient's specific isolate had to be found or produced before the window for benefit closed.

This is a selection pattern that is **distinct from, and more specific than**, the research spec's generic "salvage-therapy" caveat. It is not simply that these are severe or treatment-refractory infections (true of nearly every study in this review); it is that *access to phage therapy itself* is gated by institutional capacity, physician referral networks, and geographic proximity to one of a small number of specialized centers — factors that plausibly correlate with unmeasured severity, socioeconomic access, and clinician sophistication in ways that differ from how patients enter, say, a randomized trial with defined inclusion/exclusion criteria (PhagoBurn, Armata SWARM-P.a., Weiner BX004-A). Pooled "clinical success" proportions from Pirnay et al. and the Israeli PTC report should therefore be interpreted as **success conditional on having successfully navigated a non-random, capacity-constrained access pathway**, not as success among all MDR/XDR *Pseudomonas* patients who might plausibly benefit from phage therapy. This is directly relevant to any between-study heterogeneity analysis: pooling these two compassionate-use registries with RCT-derived proportions is not pooling like with like, and the strategist should consider whether study-design/access-pathway is itself a moderator variable worth stratifying on, separate from the pre-specified route/modality/resistance-class strata.

## 5. External Validity: Geographic Concentration of the Most Accessible Sources

A related, practical risk for the strategist and coder: the sources that are easiest to obtain and extract from — Pirnay et al. 2024 (Belgium: Queen Astrid Military Hospital / Sciensano / KU Leuven consortium) and the Israeli Phage Therapy Center report — both originate from countries with mature, idiosyncratic regulatory pathways for compassionate/magistral phage access. Belgium's magistral-preparation framework and Israel's Ministry-of-Health-authorized IPTC pathway are, globally, unusually well-developed and well-documented mechanisms; most other jurisdictions (including the U.S., where access is far more fragmented, case-by-case, and IND/emergency-use-driven) have no comparably centralized or publicly reported program.

Because these two sources are also, not coincidentally, the **largest single-arm aggregate datasets available** for this review, there is a real risk that the pooled proportion this project ultimately reports becomes disproportionately Belgium/Israel-weighted **simply because that data was the easiest to obtain from open sources**, not because these two national programs are representative of global phage-therapy practice, of the broader population of MDR/XDR *Pseudomonas* patients, or of the health-systems context that policy-facing readers of this review are likely to care about most. This is an external-validity concern that a simple pooled point estimate will not surface on its own. The strategist should consider whether a Belgium/Israel-stratified sensitivity analysis, an explicit discussion-section caveat, or a formal test of between-country heterogeneity is warranted, rather than presenting a single pooled estimate as though the underlying source studies were geographically representative.
