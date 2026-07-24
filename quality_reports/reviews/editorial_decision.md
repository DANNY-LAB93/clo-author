# Editorial Decision — Phage Therapy MDR/XDR/PDR P. aeruginosa Meta-Analysis

**Date:** 2026-07-23
**Manuscript:** Phage Therapy for MDR/XDR/PDR *Pseudomonas aeruginosa*: A Systematic Review and Meta-Analysis of Proportions
**Process:** Two blind, independent referees (domain + methods), Peer Review phase, maximum severity. Editorial synthesis (judgment, not score averaging).

## Referee Recommendations

| Referee | Score | Recommendation |
|---------|-------|----------------|
| Methods | 65/100 | MAJOR REVISIONS (borderline reject) |
| Domain | 59/100 | REJECT (soft; boundary with Major Revisions) |

## Editorial Decision: **MAJOR REVISIONS** + re-target to a specialty/evidence-synthesis venue

Both referees praised the manuscript's exemplary honesty and strong external-validity handling, and both independently reached the same core defects. The domain referee's "reject" is explicitly a soft-reject that maps to Major Revisions at a specialty venue (Viruses, Antibiotics, Systematic Reviews, Frontiers) rather than the top ID tier (CID/Lancet ID/AAC). Integrating both, the editorial decision is **MAJOR REVISIONS**, conditional on the convergent concerns below, with a realistic venue re-target away from the top ID tier.

## CONVERGENT major concerns (both referees — highest priority)

1. **Heterogeneity table incoherent: I²=0% reported for all 16 cells alongside τ² up to 7.34 and prediction intervals near [0,100].** A real, first-read-catchable defect (GLMM I²-extraction artifact or table bug). Fix the I²/τ² consistency, or drop I² for GLMM proportion cells (τ² + PI is the defensible pair; I² is documented as unreliable for proportions).
2. **Egger's test is the wrong small-study test for boundary proportions; the one "significant" result (mortality p=0.02) is likely an artifact of two n=1, 100%-mortality reports and is elevated to the abstract.** Switch to Peters' test (the pre-specified alternative); revise the abstract/Discussion if Peters' is non-significant.
3. **The headline "first MDR-specific pooled estimate" is dominated by one cohort (Pirnay, 23/35 = 66%) and collapses to k=3/N=4 under the review's own independently-verified-only classification check.** Reframe from a "first pooled estimate" headline to a single-cohort characterization, OR independently re-derive Magiorakos classification from raw antibiograms so it survives verification.
4. **Numeric inconsistency:** discussion.tex says "seventeen studies" for clinical success where Results/tables/forest caption say 18 (65 patients). Reconcile (easy fix).
5. **Degenerate cells presented as pooled estimates** (mortality inhaled/nebulized 0/23 → "0.0% [0.0–100.0%]"; k=3 HKSJ cells). Demote to the narrative/not-pooled table with exact/rule-of-three bounds.

## Domain-referee-specific major concerns

6. **Corpus likely incomplete for landmark P. aeruginosa phage cases.** Screen (in or out, with documented reasons): OMKO1 / Chan & Turner 2018 (aortic graft — the canonical case), Cano et al. 2021 (CID, PJI), Rubalskii et al. 2020 (cardiac/graft), Doub et al. (PJI). EMBASE + Web of Science remain unsearched.
7. **RCT comparator arms (PhagoBurn, Leitner, BX004-A, CYPHY) discarded and pooled as single-arm proportions** — report the within-RCT comparative signals as the highest-certainty evidence.
8. **"Clinical success" pooled across incompatible endpoints** (biliary / CF ppFEV1 / PJI remission / UTI clearance) — harmonize the definition or restrict/demote the cross-syndrome pool.
9. **Not a completed systematic review:** no PROSPERO, no GRADE (every cell unassigned), single-reviewer extraction, two planned cross-validations (Liu Tier-2, RoB spot-check) never executed.

## Methods-referee-specific major concerns

10. **Multi-arm-study non-independence** (Pirnay 3 arms, Aslam/Liu/Chan 2 arms) handled by naive-independence primary with an erratic RVE robustness note — make cluster-robust intervals primary, or collapse to one arm per study within a cell.
11. **HKSJ at k=3** produces fat-tailed t(2 df) intervals; raise the effective floor or justify against the instability literature.

## Prioritized action list

**A. Real defects the analysis team can fix now (no new data):**
- I²/τ² reporting (Major 1) — pipeline/table fix
- Egger's → Peters' test (Major 2) — 06_falsification.R
- "seventeen"→"eighteen studies" (Major 4) — one-word fix
- Demote degenerate/zero-event cells to narrative (Major 5)
- Cluster-robust intervals primary for multi-arm cells (Major 10)

**B. Analytic/framing changes the team can implement:**
- Reframe MDR estimate as single-cohort characterization (Major 3)
- Foreground within-RCT comparative evidence (Major 7)
- Harmonize / demote cross-syndrome "clinical success" pool (Major 8)
- Execute the two planned cross-validations (Major 9 partial)

**C. Requires the user / real-world action:**
- EMBASE + Web of Science searches; screen the landmark cases (Major 6)
- GRADE ratings per outcome-stratum cell (Major 9)
- Retrospective PROSPERO registration (Major 9)
- Dual-independent (or re-screened) extraction (Major 9)
- Real author names/affiliations/target-venue selection

## Bottom line

Not acceptable as-is. The paper's honesty is real but does not substitute for a completed search, coherent heterogeneity reporting, a correct small-study test, and a headline that survives its own sensitivity check. With the Section-A fixes (mechanical/statistical) plus the search completion and GRADE (Section C), this becomes a credible Major-Revisions submission at a specialty evidence-synthesis venue — not the top ID tier as a full article.

---

## Group A corrections IMPLEMENTED (2026-07-23, post-panel)

The analysis-team-fixable defects were implemented and the pipeline re-run:

1. **I²/τ² (convergent Major):** Diagnosed — for a binomial-normal GLMM, `meta::metaprop`'s `$I2` derives from the GLMM conditional Q (~0 by construction), giving I²=0% even when τ² is large (e.g. MDR eradication τ²=7.34). FIXED: I² column removed from the pooled-estimates table; heterogeneity now reported as τ² + 95% prediction interval (defensible pair for proportion GLMMs; I² unreliable for proportions per Migliavaca 2022). Table note updated.
2. **Egger's → Peters' (convergent Major) — REVERSES the mortality finding:** Egger's is invalid for boundary proportions. Switched to Peters' test in `06_falsification.R`. New Peters' p-values (only the 4 outcome-overall cells support the test; MDR-specific cells return NA): clinical success 0.66, safety 0.38, eradication 0.82, **mortality 0.24 (was Egger's 0.02)**. NO outcome now shows significant small-study asymmetry. The abstract/results/discussion were rewritten: the "significant mortality asymmetry / pooled mortality may under-estimate" claim is recast as a boundary-invalid Egger's artifact, corrected by Peters'.
3. **Degenerate cell (Major):** Zero-/all-event guard added to `pool_stratum.R`: a cell with 0 (or all) events is uninformative as a pooled proportion and is now reported narratively with an exact rule-of-three bound. Mortality inhaled/nebulized (0/23) demoted from the pooled table (now Table 3, reason "0 events", ~13% one-sided upper bound). Pooled cells 16 → 15.
4. **Numeric + framing (Major/minor):** discussion "seventeen"→"eighteen studies"; MDR estimate reframed throughout (abstract/intro/results/discussion) as a single-cohort, author-reported-labels-dependent characterization that collapses to k=3/N=4 under independently-verified-only classification — not a robust "first estimate."

**Verified:** full pipeline re-run clean (exit 0); manuscript recompiled clean (zero fatal, zero undefined); Table 2 visually confirmed at 7 columns (τ², no I²) and 15 rows; mortality-inhaled shows "0 events" in Table 3; abstract 145 words.

**Group A item left as a larger revision (not fully implemented):** making cluster-robust (RVE) intervals PRIMARY for multi-arm cells (methods Major 10). The manuscript discloses the multi-arm dependence and reports the RVE robustness check, but the primary CIs remain naive-independence. Fully re-basing the primary analysis on RVE is deferred as a larger re-analysis.

**Groups B and C (search completion, GRADE, PROSPERO, dual extraction, RCT-comparator foregrounding, cross-syndrome harmonization) remain outstanding** — several require the user's action.
