# Robustness Plan: Phage Therapy MDR/XDR *Pseudomonas aeruginosa* Meta-Analysis of Proportions

**Design:** Descriptive / measurement — random-effects meta-analysis of proportions (GLMM-logit primary)
**Date:** 2026-07-19
**Companion to:** `quality_reports/strategy_memo_phage_therapy_mdr_pseudomonas.md` §5 (full narrative justification there; this file is the checklist form per the `robustness-plan.md` template convention)

## Ordered Checks (Most Threatening First)

### Priority 1: Model/Assumption-Threatening
| # | Check | Assumption Tested | Implementation | Expected Result |
|---|-------|-------------------|-----------------|------------------|
| 1 | Transformation/model choice (GLMM-logit vs. double-arcsine vs. logit-DL) | Pooling model does not drive the conclusion (Schwarzer et al. 2019 mechanism) | `meta::metaprop()` with `sm="PLOGIT"/method="GLMM"` vs. `sm="PFT"` vs. `sm="PLOGIT"/method="Inverse"` | Similar point estimates, overlapping CIs; divergence >5-10pp reported as a finding |
| 2 | MDR/XDR classification sensitivity | Author-reported classification does not distort the core stratification variable | Re-run restricted to `resistance_class_source == "independently verified"` | Directionally similar to full sample |
| 3 | Fixed- vs. random-effects | Random-effects (pre-specified primary) actually matters given heterogeneity | Report both per stratum | RE preferred; large FE/RE gap documents heterogeneity magnitude |

### Priority 2: Design-Quality / Selection Sensitivity
| # | Check | What Changes | Implementation | Expected Result |
|---|-------|--------------|-----------------|------------------|
| 4 | Study-design-stratified sensitivity | RCT/cohort vs. case-series/compassionate-use | Subgroup by `study_design`, Q-between test | Compassionate-use strata likely higher "success" — selection-into-treatment mechanism |
| 5 | Geographic-concentration sensitivity | Belgium/Israel excluded vs. included | Re-run pooled model excluding those `geographic_source` arms | Material shift reported explicitly per external-validity flag |
| 6 | Leave-one-out | Influential-study robustness (Pirnay n=49 flagged a priori) | Drop each study, recompute | Stable estimates; Pirnay flagged regardless of outcome |

### Priority 3: Specification/Categorization Sensitivity
| # | Check | What Changes | Implementation | Expected Result |
|---|-------|--------------|-----------------|------------------|
| 7 | Route-collapsing sensitivity | Fine-grained vs. 2-category (systemic vs. local) route taxonomy | Re-run both taxonomies | Directionally consistent |
| 8 | Liu-reuse-tier transparency check | Independently-extracted-only vs. all rows incl. any Tier-3 adoptions | Compare pooled estimate under both sets | Small difference if Tier-3 use is genuinely narrow (per memo §3) |

### Priority 4: Inference Robustness
| # | Check | What Changes | Implementation | Expected Result |
|---|-------|--------------|-----------------|------------------|
| 9 | HKSJ vs. standard Wald CI | Small-stratum inference confidence | `hakn = TRUE` vs. `FALSE` | HKSJ wider for k<10; HKSJ is primary |
| 10 | Same-study multi-arm clustering (RVE) | Independence assumption for multi-arm studies | `clubSandwich` clustering by `study_id` | Modestly wider CIs where applicable; RVE primary where applicable |

### Priority 5: Publication Bias and Threshold Sensitivity
| # | Check | Logic | Implementation | Expected Result |
|---|-------|-------|-----------------|------------------|
| 11 | Funnel plot + Egger's/Peters'-type test | Small-study/publication-bias effects | Applied only where k≥10 (pre-specified) | Reported even if null; explicit statement where k<10 |
| 12 | Minimum-study-count threshold relaxation (≥2 studies/≥10 patients) | Whether the ≥3/≥20 primary threshold is itself consequential | Appendix-only table, clearly labeled below pre-specified bar | Documented, not promoted to primary results |
| 13 | Monotherapy-stratum contingency rule application | ≥3 qualifying studies (Krakhotkin, Leitner, pending EMBASE/WoS/Scopus) → pool; else narrative-only | Apply decision rule once full text obtained | Reported regardless of outcome — "cannot pool" is itself a finding |

## Design-Specific Notes (Descriptive/Measurement Defaults, Adapted)

Per the `strategize` skill's Descriptive design-specific defaults (alternative construction choices, alternative data sources, temporal stability, sensitivity to outliers, subgroup consistency) — mapped here as:
- Alternative construction choices → Priority 1 (transformation/model) and Priority 3 (route-collapsing)
- Alternative data sources → Priority 2 #5 (geographic concentration) and Priority 3 #8 (Liu-reuse tier)
- Temporal stability → Falsification check (publication-year trend, see `falsification_tests.md`)
- Sensitivity to outliers → Priority 2 #6 (leave-one-out)
- Subgroup consistency → Priority 1 #2, Priority 2 #4, Priority 3 #7
