# Results Summary — Phage Therapy for MDR/XDR *Pseudomonas aeruginosa*

**Project:** phage_therapy_mdr_pseudomonas
**Date:** 2026-07-22 (two re-runs this date: first after completing Pirnay et al. 2024's remaining 32 MDR/XDR/PDR-eligible patients, second after completing 2 of the remaining 5 pending extractions — Jault2019/PhagoBurn and ArmataAP_PA02/SWARM-P.a. — using newly available PubMed and ClinicalTrials.gov API tools; see Data Notes for both)

## Second Update (this date): Jault2019/PhagoBurn + ArmataAP_PA02 Completed

Using newly available structured-data tools (a PubMed full-text/metadata MCP server and a ClinicalTrials.gov API v2 MCP server), completed 2 of the 5 remaining EXTRACTION_INCOMPLETE arms:
- **Jault2019/PhagoBurn** (PMID 30292481): full structured abstract retrieved directly — adverse_event_n=3 (of 13 safety-population patients), mortality_n=1, now COMPLETE. Clinical success remains structurally NOT extractable (time-to-event primary endpoint, not a fixed-timepoint proportion) — disclosed as a design property, not a gap.
- **ArmataAP_PA02/SWARM-Pa** (NCT04596319): direct ClinicalTrials.gov API v2 query against `resultsSection.adverseEventsModule` confirmed the existing adverse_event_n=5/10 for the highest-dose cohort ("Cohort 4 MAD") exactly, and added mortality_n=0 (deathsNumAffected=0). Now COMPLETE. Clinical success and eradication are structurally NOT_APPLICABLE (this trial's only registered outcome is TEAE incidence — a pure Phase 1b/2a safety/tolerability design, confirmed via the trial's own outcomes module).
- **Weiner2025's Author Correction** (PMID 41760669, PMC12949002) read in full: corrects only a chemistry figure (synthetic-medium sample-size mislabeling); explicitly states no effect on results/conclusions. Flag resolved with a clean negative finding.
- **Onallah2023 and Leitner2021**: richer structured abstracts obtained (confirming existing numbers precisely for Onallah; confirming Leitner's abstract genuinely has no *P. aeruginosa*-specific breakdown, closing off that avenue) but both remain EXTRACTION_INCOMPLETE — Onallah's exact AE count and Leitner's Pseudomonas-subgroup isolation are not resolvable from anything short of full text, which remains inaccessible (no PMC mirror for either, confirmed via `find_related_articles`).

**Consequence:** COMPLETE arms rose from 13 to 15 (of 18 total); EXTRACTION_INCOMPLETE fell from 5 to 3. Pooled cells rose from 12 to 14 (new: safety and mortality in the not-classifiable resistance stratum, both driven by the Jault2019/ArmataAP_PA02 completions). Overall safety moved 14.2%→18.2% (k=11→12, N=59→72); overall mortality moved from NOT_POOLED to POOLED for the first time at 10.8% (k=11, N=65). Egger's test now covers a third outcome (mortality, newly crossing k≥10) at p=0.074 (not significant) alongside clinical success (p=0.48) and safety (p=0.49, was 0.42). Leave-one-out no longer flags the *overall* safety estimate as sensitive to any single study (an improvement); the not-classifiable stratum's new mortality estimate is sensitive to removing Jault2019/PhagoBurn specifically.

---

## First Update (this date): Pirnay 2024 Full Re-Extraction
**Scripts:** `scripts/R/00_master.R` (runs `01_setup.R` through `09_table1_characteristics.R` in sequence)
**Design:** Descriptive/measurement — random-effects meta-analysis of proportions (GLMM-logit primary; logit-DL and Freeman-Tukey double-arcsine sensitivity/fallback), per `quality_reports/strategy_memo_phage_therapy_mdr_pseudomonas.md`

> **Read this before the numbers below:** this is a **preliminary, illustrative synthesis of a small evidence base** (18 extracted study-arms; 17 pooling-eligible after excluding one non-*Pseudomonas*-specific row; 13 distinct studies). It is not a definitive, adequately powered systematic review. Every pooled estimate below should be read with that caveat attached, not as a settled clinical finding.

---

## What Changed From the Prior Run (2026-07-20)

Pirnay et al. (2024)'s remaining 38 *P. aeruginosa* patients (of the study's full 49-patient subgroup) were previously unextracted — only an 11-patient subset with full case-narrative detail had been extracted. A full-text pass against the paper's open-access PMC supplementary tables (PMC11153159, CC BY) resolved this: all 49 *P. aeruginosa*-targeted patients were identified and cross-tabulated for clinical improvement, microbiological eradication, adverse events, and mortality. Of these 49, **17 are classified "UDR" (usual drug resistance) — not MDR/XDR/PDR — and are excluded from this review's dataset entirely as ineligible** (a correction this review's own eligibility criteria required, only detectable once per-patient resistance data became available; two patients in the *prior* 11-patient subset, #30 and #71, were also UDR and are now excluded, a genuine correction to the previously-approved extraction). The remaining **32 patients are MDR/XDR/PDR-eligible** and replace the old 11-patient aggregate row with three new resistance-stratified arms (XDR n=7, MDR n=23, PDR n=2).

This changed the review's headline finding: **the MDR resistance stratum is now poolable across all four outcomes** (k=5 studies, N=28 patients) — previously the review's core stratification aim (MDR vs. XDR) was formally unachievable with the available corpus; it now is, for MDR specifically. XDR (k=3, N=9) and PDR (k=3, N=4) remain below the N≥20 threshold and are still not pooled.

A second, code-level consequence: the added MDR/XDR/PDR strata changed the safety outcome's data composition enough that an unprotected sensitivity-model call (`meta::metaprop()`'s internal REML heterogeneity diagnostic, invoked even for the DerSimonian-Laird and fixed-effect sensitivity calls) crashed the pipeline with "Fisher scoring algorithm did not converge." `scripts/R/functions/pool_stratum.R` was fixed to wrap **all four** models (GLMM primary + 3 sensitivity models) in the same capture-don't-crash contingency previously applied only to the GLMM primary, with a GLMM → logit-DL → fixed-effect cascading fallback if more than one model fails for a cell. No cell in this run actually needed the third-level fallback (fixed-effect only), but the contingency now exists.

---

## Paper-to-Code Naming Map

(unchanged from the prior run — see `scripts/R/01_setup.R`'s Paper-to-Code Naming Map comment block)

---

## Key Findings

**14 cells** now meet the pre-specified pooling threshold (**≥3 independent studies AND ≥20 pooled patients**) — up from 5 in the original run, 12 after the Pirnay update, 14 after completing Jault2019/PhagoBurn and ArmataAP_PA02 (see "Second Update" above; the 2 new cells are safety and mortality in the not-classifiable resistance stratum). All others are reported as "insufficient evidence," not forced estimates. The table below reflects the 12-cell state from the Pirnay update; see "Second Update" above for the current overall-safety (18.2%) and overall-mortality (10.8%, now POOLED) figures, which superseded the 14.2%/NOT_POOLED figures shown here.

| Outcome — Stratum | $k$ (studies) | $N$ (patients) | Pooled proportion (GLMM, 95% CI, HKSJ) | $I^2$ | $\tau^2$ |
|---|---|---|---|---|---|
| Clinical success — Overall | 10 | 57 | **77.2% [63.1%, 87.0%]** | 0% | 0 |
| Safety (≥1 AE) — Overall | 11 | 59 | **14.2% [3.5%, 43.0%]** | 0% | 0.553 |
| Microbiological eradication — Overall | 9 | 42 | **64.3% [47.2%, 78.4%]** | 0% | 0 |
| Mortality — Overall | 9 | 42 | **14.3% [6.0%, 30.3%]** | 0% | 0 |
| Clinical success — Resistance: MDR | 5 | 28 | **71.4% [46.0%, 88.0%]** | 0% | 0 |
| Safety (≥1 AE) — Resistance: MDR | 5 | 28 | **14.3% [4.0%, 40.0%]** | 0% | 0 |
| Microbiological eradication — Resistance: MDR | 5 | 28 | **64.3% [39.5%, 83.2%]** | 0% | 0 |
| Mortality — Resistance: MDR | 5 | 28 | **7.1% [1.2%, 33.7%]** | 0% | 0 |
| Clinical success — Route: "other" (multi-route arms) | 5 | 50 | **78.0% [60.6%, 89.1%]** | 0% | 0 |
| Safety (≥1 AE) — Route: "other" | 4 | 35 | **17.1% [6.1%, 39.6%]** | 0% | 0 |
| Microbiological eradication — Route: "other" | 4 | 35 | **62.9% [40.8%, 80.6%]** | 0% | 0 |
| Mortality — Route: "other" | 4 | 35 | **14.3% [4.6%, 36.6%]** | 0% | 0 |

Full table: `paper/tables/phage_therapy_mdr_pseudomonas/meta_pooled_estimates.tex` (12 rows).

### Interpretation

- The headline clinical-success proportion is now 77.2% across 10 studies / 57 patients (down from 86.1%/36 patients in the prior run — the additional Pirnay patients, drawn from a broader, less curated slice of that cohort, pull the estimate toward a more moderate value, consistent with a case-report-selection effect diluting as more representative data enters the pool).
- **The MDR resistance stratum is now poolable across all four outcomes** (k=5, N=28) — this is the review's first successful resistance-stratified estimate and directly answers part of the originally-blocked core research question. **XDR (k=3, N=9) and PDR (k=3, N=4) remain below the N≥20 patient threshold** and are still reported narratively only, not pooled — the MDR-vs-XDR *comparison* itself therefore still cannot be completed, even though MDR alone can now be estimated.
- Route stratification: only the heterogeneous "other" (multi-route) bucket meets the threshold (k=4-5, N=35-50, driven substantially by Pirnay's mixed-route patients); topical/local, IV, and inhaled/nebulized remain below threshold for every outcome.
- **Modality (monotherapy vs. combination) remains unpoolable**: 0 of 17 pooling-eligible arms are coded pure antibiotic monotherapy — unchanged from before.
- **Within the MDR stratum, Pirnay 2024 is the dominant contributor** (23 of 28 MDR patients, 82%) — leave-one-out confirms dropping Pirnay collapses the MDR safety and mortality estimates to a numerically-indistinguishable-from-zero value (see Robustness). The MDR pooled estimate should be read as "mostly Pirnay's cohort, corroborated by a handful of smaller studies," not as an even-weighted synthesis across independent sources.

---

## Robustness

| Check | Result | Table/Figure |
|---|---|---|
| Transformation/model choice (GLMM vs. FT vs. logit-DL vs. FE) | Diverges by **>5pp in 11 of 12 POOLED cells** (range 4.6-11.9pp; only `eradication__route_group__other` at 4.6pp falls just under the 5pp flag threshold) | `paper/tables/phage_therapy_mdr_pseudomonas/meta_sensitivity.tex` |
| Leave-one-out (study-level) | **4 of 76** study-removals shift a pooled estimate outside the full-sample 95% CI, **all four are "drop Pirnay2024"**: `safety__overall` (→1.0%), `safety__resistance_class__MDR` (→~0%), `mortality__resistance_class__MDR` (→~0%), `safety__route_group__other` (→~0%) | `leave_one_out.rds` |
| HKSJ vs. standard Wald CI | HKSJ wider in every POOLED cell (e.g. `clinical_success__resistance_class__MDR`: 0.420 vs. 0.326) | `hksj_vs_wald.rds` |
| Same-study multi-arm RVE clustering | Direction is cell-specific, not uniformly wider: e.g. `eradication__route_group__other` naive SE 0.342 → RVE SE 0.098 (narrower); `mortality__route_group__other` naive SE 0.457 → RVE SE 0.514 (wider) | `rve_clustering_check.rds` |
| MDR/XDR classification sensitivity (all sources vs. independently-verified-only) | `clinical_success x MDR`: all-sources k=5/N=28 (POOLED) vs. verified-only k=3/N=4 (NOT_POOLED) — **the MDR pooled result depends on author-reported (not independently re-derived) classifications for most of its 28 patients** | `classification_sensitivity.rds` |
| Geographic-concentration exclusion (Belgium/Israel) | Safety remains POOLED after exclusion (0.142 → 0.010); clinical success, eradication, and mortality all become NOT_POOLED once Belgium/Israel are excluded (insufficient remaining k/N) | `geo_concentration_sensitivity.rds` |
| Route-collapsing (2-category) subgroup test | Q-between p = 0.916 (clinical success) | — |
| Study-design subgroup test | Q-between p = 0.284 (clinical success, RCT/cohort vs. case report/series) | — |

### Robustness Assessment

Two distinct instability patterns now coexist:
1. **The overall safety/AE estimate remains unstable**, as before, but the driver has shifted: previously ArmataAP_PA02 alone (near-complete separation, 1 of 12 arms positive); now **Pirnay2024 is the dominant driver of both the overall safety estimate and, more consequentially, the entire MDR-specific safety and mortality estimates** (leave-one-out collapses all three to ~0% on removal). The logit-DL/fixed-effect sensitivity estimates (safety overall ≈ 31%, similarly elevated for MDR) remain more credible than the near-zero GLMM figures for these specific cells.
2. **The MDR clinical-success and eradication estimates are comparatively more stable** (do not shift outside their CI on any single-study removal), but rest on classification-sensitivity data showing the MDR pool depends heavily on author-reported (not independently re-verified) resistance labels — a genuine, disclosed limitation, not a fatal flaw.

---

## Descriptive Statistics

| Variable | Value |
|---|---|
| Total pooling-eligible study-arms | 17 (18 extracted, 1 excluded — Leitner2021, see Data Notes) |
| Total distinct studies | 13 |
| Total patients (sum of `n_arm`, pooling-eligible arms) | 87 |
| Extraction status | 15 COMPLETE, 3 EXTRACTION_INCOMPLETE (updated after the second round this date; table below reflects the intermediate 13/5 state) |
| Resistance class | MDR 5 arms/28 patients, not-classifiable 6 arms, XDR 3 arms/9 patients, PDR 2 arms/4 patients |
| Route (collapsed) | other 5 arms/50 patients, topical/local 5, IV 3, inhaled/nebulized 2 |
| Modality (collapsed) | phage+antibiotic combination 16, phage monotherapy 1, **antibiotic monotherapy 0** |
| Study design | case report 7 arms, RCT 3, case series 2, retrospective cohort 3 (Pirnay's 3 resistance-stratified arms) |
| Outcome availability | clinical success: 14 arms/10 studies/57 pts; safety: 15/11/59; eradication: 13/9/42; mortality: 13/9/42 |

---

## Falsification / Negative-Control Checks

| Test | Result | Interpretation |
|---|---|---|
| Publication-year trend (clinical success) | coef = −0.087 (logit scale), p = 0.648 | No unexplained secular trend — passes |
| Journal-tier gradient (descriptive) | High-tier 78.0% (k=4 studies) vs. mid-tier 71.4% (k=6) | Small gradient, not formally tested (only 2 tiers, small per-tier k) |
| Route × geography concentration check | No route category is a single-region signature (2-5 distinct regions per route) | Passes |
| Small-study/sample-size eyeball plot | `small_study_eyeball.pdf` | Visual complement to Egger's below |
| **Egger's test (k≥10 only)** | **Clinical success: p = 0.48; Safety: p = 0.42 — NEITHER significant** | **Reverses the prior run's finding** (previously p=0.022 and p=0.002, both significant). Eradication and mortality remain below the k≥10 eligibility threshold (k=9) and are not tested. The additional Pirnay patients — a large, less-selected cohort slice rather than more n=1 case reports — appear to have diluted the funnel asymmetry that drove the prior significant result. **This is a genuine, disclosed reversal, not a discarded inconvenient finding**: the small-study-effect narrative central to the prior Discussion draft no longer holds as stated and that section must be corrected, not just re-worded. |
| Falsification Test 5 (LOS vs. clinical success) | NOT_APPLICABLE — only 1 of 17 arms report `los_days` | Unchanged from prior run |

---

## Data Notes

- **Sample:** 18 study-arms extracted; 1 excluded before any pooling (`Leitner2021_pyophage`, unchanged reason — trial-wide, 6-pathogen aggregate with no confirmable *Pseudomonas*-specific breakdown).
- **Pirnay2024 replacement (2026-07-22):** the prior single aggregated row (`Pirnay2024_table2subset`, n=11, resistance_class=not-classifiable) is replaced by three resistance-stratified rows built from the paper's open-access PMC11153159 supplementary tables (all 100 patients, individually coded): `Pirnay2024_XDR` (n=7), `Pirnay2024_MDR` (n=23), `Pirnay2024_PDR` (n=2) — 32 patients total, cross-validated against the prior 11-patient subset (9 of 11 patients match exactly; 2 — case #30 and #71 — are now excluded as UDR, not MDR/XDR/PDR, a genuine eligibility correction only possible once per-patient resistance data was available). Full citation locator and per-patient case numbers are in `data/raw/phage_therapy_extraction_raw.csv`'s `extraction_citation` field for each of the three new rows.
- **Missing-outcome exclusions (per outcome, not per row):** `clinical_success_n` is NA for Weiner2025 (continuous CFU log-reduction outcome) and Jault2019/PhagoBurn (time-to-event primary outcome). `adverse_event_n` is NA for Onallah2023/PASA16 and Jault2019 (Pirnay now has adverse_event_n populated for all three new rows, no longer NA).
- **Merge/join:** none — single flat extraction table, no external merge.

---

## Flags and Anomalies

1. **The overall and MDR-specific safety/mortality GLMM estimates are numerically unstable, now driven by Pirnay2024 rather than ArmataAP_PA02.** Leave-one-out confirms removing Pirnay2024 collapses `safety__overall`, `safety__resistance_class__MDR`, `mortality__resistance_class__MDR`, and `safety__route_group__other` all to a numerically-indistinguishable-from-zero value. The logit-DL/fixed-effect sensitivity models remain more credible for these specific cells than the GLMM point estimates.
2. **MDR is now poolable; XDR and PDR are not.** The review's core stratification aim is now partially achievable: MDR alone has a pooled estimate for all 4 outcomes, but the MDR-vs-XDR *comparison* the review originally set out to make still cannot be completed (XDR k=3/N=9, PDR k=3/N=4, both below N≥20).
3. **Egger's test result reversed from significant to non-significant** for both eligible outcomes (clinical success, safety) after adding the Pirnay patients. This is a genuine, substantively important change to the Discussion's small-study-effects narrative, not a rounding update.
4. **The MDR pooled result rests heavily on author-reported (not independently re-verified) resistance classifications** — classification-sensitivity check shows the MDR cell would fail the pooling threshold entirely (k=3, N=4) if restricted to independently-verified-only classifications.
5. **The modality (monotherapy vs. combination) stratification remains empty** (0 antibiotic-monotherapy arms) — unchanged.
6. **Environment note (unchanged):** `Rscript -e '...'` segfaults reproducibly for complex multi-line inline scripts in this environment; running the identical code as a `.R` file works correctly. Not a GLMM/pipeline defect.
7. **Code fix applied this run:** `pool_stratum.R`'s three sensitivity-model calls (Freeman-Tukey, logit-DL, fixed-effect) were previously unprotected against `meta::metaprop()`'s internal REML-diagnostic crash risk — only the GLMM primary call had this protection. A real cell (`safety__overall`, after the Pirnay data changed its composition) hit this and crashed the pipeline. Fixed by wrapping all four calls in the same capture-don't-crash contingency, with a GLMM → logit-DL → fixed-effect cascading fallback. **The fixed-effect model itself now fails to converge for `safety__overall`** (reported as NA/em-dash in `meta_sensitivity.tex`, Table 4) — a new, disclosed instability distinct from the GLMM's own; the same near-complete-separation pattern destabilizing the primary model apparently also breaks the fixed-effect sensitivity calculation for this specific cell.
8. **Table-width overflow fixed (pre-existing, not introduced this run):** `meta_pooled_estimates.tex` (8 columns) and `meta_not_pooled.tex` were overflowing the page's text width by up to ~290pt (roughly 4 inches) at `\footnotesize`, silently truncating the rightmost 2-3 columns and the table notes off the visible page — confirmed via a page-by-page visual render, not caught by any prior compile-only check. Fixed by (a) switching all four meta-analysis tables to `\scriptsize` with tightened `\tabcolsep`, (b) shortening repeated boilerplate in `label_stratum()` (dropped the redundant "(secondary/contextual)" suffix, already stated once in the table note; "Microbiological eradication" to "Eradication"), and (c) replacing `meta_not_pooled.tex`'s repeated full-sentence "reason" column (identical on 24 of 25 rows) with a terse per-row criterion flag ($k<3$, $N<20$, or both) — the full threshold wording already lives once in the table note. All four tables re-verified via `pdftoppm` render after the fix; no more columns or notes text run off the page.

---

## Output Files

### Tables
| File | Description |
|---|---|
| `paper/tables/phage_therapy_mdr_pseudomonas/meta_pooled_estimates.tex` | 12 POOLED cells |
| `paper/tables/phage_therapy_mdr_pseudomonas/meta_not_pooled.tex` | 25 NOT_POOLED/NOT_ATTEMPTED cells |
| `paper/tables/phage_therapy_mdr_pseudomonas/meta_sensitivity.tex` | GLMM vs. FT vs. logit-DL vs. FE, all 12 POOLED cells (48 rows) |
| `paper/tables/phage_therapy_mdr_pseudomonas/table1_study_characteristics.tex` | 18 study-arm rows (Pirnay now 3 rows, not 1) |

### Figures
Forest plots regenerated for the same 3 named cells as before (`forest_clinical_success_overall.pdf`, `forest_safety_overall.pdf`, `forest_clinical_success_route_other.pdf`) plus `small_study_eyeball.pdf`. **Note:** the prior run's `forest_clinical_success_resistance_notclassifiable.pdf` cell (not-classifiable, k=3) is no longer POOLED in this run (now k=2, below threshold, since Pirnay's patients moved out of "not-classifiable" into MDR/XDR/PDR) — that specific forest plot is stale and should be treated as superseded; a new `forest_clinical_success_resistance_MDR.pdf`-equivalent has not yet been separately named/generated by `07_figures.R` (it currently names forest plots by an allowlist that predates this run's new MDR cell — flagged for the coder-critic as a follow-up, not blocking, since the MDR estimate is already fully reported in the pooled-estimates table).

### Scripts
`scripts/R/00_master.R` → `01_setup.R` ... `09_table1_characteristics.R`; `scripts/R/functions/pool_stratum.R` modified this run (see Flag #7).
