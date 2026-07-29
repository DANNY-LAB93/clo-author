# Manuscript scalar manifest --- phage_therapy_mdr_pseudomonas

MACHINE-WRITTEN by `scripts/R/11_manifest.R`. Do not edit by hand.

Every number quoted in `paper/main.tex` or `paper/sections/*.tex` must appear
in this file. A number that is not here is not quotable. Regenerate with
`Rscript scripts/R/00_master.R` and re-check the manuscript against it.

Generated: 2026-07-29 11:55 | seed: 20260720

## 1. Corpus

| Quantity | Value |
|---|---|
| Rows in cleaned extraction dataset (all arms) | 38 |
| Studies in cleaned extraction dataset | 31 |
| **Pooling-eligible study-arms** | **31** |
| **Pooling-eligible studies** | **25** |
| **Pooling-eligible patients** | **82** |
| Single-patient arms | 24 |
| Multi-patient arms | 7 |
| Patients contributed by multi-patient arms | 58 |

### 1.1 Exclusions (each with its own count)

| Step | n |
|---|---|
| Rows in cleaned extraction dataset | 38 |
| Excluded: Leitner2021 (trial-wide, not Pseudomonas-specific) | 1 |
| Excluded: Liu2025 (antibiogram does not meet the MDR population criterion) | 1 |
| Excluded: trial populations recruited with no MDR/XDR/PDR entry criterion | 3 |
| Excluded: case reports duplicating a patient inside the Pirnay 2024 roster | 2 |
| Rows entering stratified pooling eligibility checks | 31 |

### 1.2 Design, resistance and route distribution (pooling-eligible arms only)

**study_design**

| Level | Arms | Studies | Patients |
|---|---|---|---|
| case report | 20 | 19 | 20 |
| case series | 8 | 5 | 30 |
| retrospective cohort | 3 | 1 | 32 |

**resistance_class**

| Level | Arms | Studies | Patients |
|---|---|---|---|
| MDR | 17 | 16 | 46 |
| not-classifiable | 7 | 6 | 21 |
| PDR | 3 | 3 | 5 |
| XDR | 4 | 4 | 10 |

**route_group**

| Level | Arms | Studies | Patients |
|---|---|---|---|
| inhaled/nebulized | 5 | 4 | 13 |
| IV | 8 | 6 | 8 |
| other | 9 | 7 | 52 |
| topical/local | 6 | 6 | 6 |
| (not reported) | 3 | 3 | 3 |

**modality_group**

| Level | Arms | Studies | Patients |
|---|---|---|---|
| phage monotherapy | 1 | 1 | 1 |
| phage+antibiotic combination | 30 | 24 | 81 |

## 2. Pooled outcome-stratum cells

| Quantity | Value |
|---|---|
| **Pooled cells** | **13** |
| **Not-pooled cells** | **31** |
| Total estimated cells | 44 |

| Cell | k studies | k arms | N | Estimate | 95% CI | tau2 | 95% PI | CI width (pp) |
|---|---|---|---|---|---|---|---|---|
| clinical_success__overall | 23 | 28 | 71 | 76.1% | [64.2%, 84.9%] | 0.000 | [64.2%, 84.9%] | 20.7 |
| safety__overall | 17 | 22 | 52 | 19.2% | [10.3%, 33.1%] | 0.000 | [10.3%, 33.1%] | 22.8 |
| eradication__overall | 19 | 23 | 59 | 57.8% | [30.2%, 81.2%] | 2.198 | [4.9%, 97.3%] | 51.0 |
| mortality__overall | 24 | 30 | 67 | 10.4% | [4.9%, 20.9%] | 0.000 | [4.9%, 20.9%] | 16.0 |
| clinical_success__resistance_class__MDR | 14 | 15 | 37 | 73.0% | [55.0%, 85.7%] | 0.000 | [55.0%, 85.7%] | 30.7 |
| clinical_success__resistance_class__not-classifiable | 6 | 7 | 21 | 85.7% | [56.6%, 96.5%] | 0.000 | [56.6%, 96.5%] | 39.9 |
| safety__resistance_class__MDR | 12 | 13 | 36 | 16.7% | [7.0%, 34.6%] | 0.000 | [7.0%, 34.6%] | 27.6 |
| eradication__resistance_class__MDR | 13 | 14 | 42 | 52.0% | [10.9%, 90.5%] | 6.631 | [0.3%, 99.8%] | 79.6 |
| mortality__resistance_class__MDR | 16 | 17 | 46 | 6.5% | [1.9%, 19.8%] | 0.000 | [1.9%, 19.8%] | 17.9 |
| clinical_success__route_group__other | 7 | 9 | 52 | 76.9% | [60.9%, 87.7%] | 0.000 | [60.9%, 87.7%] | 26.7 |
| safety__route_group__other | 5 | 7 | 36 | 16.7% | [6.3%, 37.4%] | 0.000 | [6.3%, 37.4%] | 31.1 |
| eradication__route_group__other | 6 | 8 | 37 | 64.9% | [45.0%, 80.6%] | 0.000 | [45.0%, 80.6%] | 35.7 |
| mortality__route_group__other | 6 | 8 | 37 | 13.5% | [4.8%, 32.8%] | 0.000 | [4.8%, 32.8%] | 28.0 |

### 2.1 Cells NOT pooled, with reason

| Cell | k studies | k arms | N | Reason |
|---|---|---|---|---|
| clinical_success__resistance_class__PDR | 2 | 2 | 3 | k_studies = 2, N = 3 patients (threshold: >= 3 studies AND >= 20 patients) |
| clinical_success__resistance_class__XDR | 4 | 4 | 10 | k_studies = 4, N = 10 patients (threshold: >= 3 studies AND >= 20 patients) |
| safety__resistance_class__not-classifiable | 2 | 3 | 3 | k_studies = 2, N = 3 patients (threshold: >= 3 studies AND >= 20 patients) |
| safety__resistance_class__PDR | 2 | 2 | 3 | k_studies = 2, N = 3 patients (threshold: >= 3 studies AND >= 20 patients) |
| safety__resistance_class__XDR | 4 | 4 | 10 | k_studies = 4, N = 10 patients (threshold: >= 3 studies AND >= 20 patients) |
| eradication__resistance_class__not-classifiable | 2 | 2 | 2 | k_studies = 2, N = 2 patients (threshold: >= 3 studies AND >= 20 patients) |
| eradication__resistance_class__PDR | 3 | 3 | 5 | k_studies = 3, N = 5 patients (threshold: >= 3 studies AND >= 20 patients) |
| eradication__resistance_class__XDR | 4 | 4 | 10 | k_studies = 4, N = 10 patients (threshold: >= 3 studies AND >= 20 patients) |
| mortality__resistance_class__not-classifiable | 5 | 6 | 6 | k_studies = 5, N = 6 patients (threshold: >= 3 studies AND >= 20 patients) |
| mortality__resistance_class__PDR | 3 | 3 | 5 | k_studies = 3, N = 5 patients (threshold: >= 3 studies AND >= 20 patients) |
| mortality__resistance_class__XDR | 4 | 4 | 10 | k_studies = 4, N = 10 patients (threshold: >= 3 studies AND >= 20 patients) |
| clinical_success__dtr_status__yes | 2 | 2 | 3 | k_studies = 2, N = 3 patients (threshold: >= 3 studies AND >= 20 patients) |
| clinical_success__dtr_status__not-derivable | 22 | 26 | 68 | DTR status not derivable for 26 of 28 contributing arms: the source publishes no agent-level antibiogram covering all beta-lactams and both fluoroquinolones. NOT a sample-size failure -- this cell fails for ABSENT DATA and is the only stratum in this review that does. |
| safety__dtr_status__yes | 2 | 2 | 3 | k_studies = 2, N = 3 patients (threshold: >= 3 studies AND >= 20 patients) |
| safety__dtr_status__not-derivable | 16 | 20 | 49 | DTR status not derivable for 20 of 22 contributing arms: the source publishes no agent-level antibiogram covering all beta-lactams and both fluoroquinolones. NOT a sample-size failure -- this cell fails for ABSENT DATA and is the only stratum in this review that does. |
| eradication__dtr_status__yes | 3 | 3 | 5 | k_studies = 3, N = 5 patients (threshold: >= 3 studies AND >= 20 patients) |
| eradication__dtr_status__not-derivable | 18 | 20 | 54 | DTR status not derivable for 20 of 23 contributing arms: the source publishes no agent-level antibiogram covering all beta-lactams and both fluoroquinolones. NOT a sample-size failure -- this cell fails for ABSENT DATA and is the only stratum in this review that does. |
| mortality__dtr_status__yes | 3 | 3 | 5 | k_studies = 3, N = 5 patients (threshold: >= 3 studies AND >= 20 patients) |
| mortality__dtr_status__not-derivable | 23 | 27 | 62 | DTR status not derivable for 27 of 30 contributing arms: the source publishes no agent-level antibiogram covering all beta-lactams and both fluoroquinolones. NOT a sample-size failure -- this cell fails for ABSENT DATA and is the only stratum in this review that does. |
| clinical_success__route_group__inhaled/nebulized | 2 | 2 | 2 | k_studies = 2, N = 2 patients (threshold: >= 3 studies AND >= 20 patients) |
| clinical_success__route_group__IV | 6 | 8 | 8 | k_studies = 6, N = 8 patients (threshold: >= 3 studies AND >= 20 patients) |
| clinical_success__route_group__topical/local | 6 | 6 | 6 | k_studies = 6, N = 6 patients (threshold: >= 3 studies AND >= 20 patients) |
| safety__route_group__inhaled/nebulized | 3 | 3 | 4 | k_studies = 3, N = 4 patients (threshold: >= 3 studies AND >= 20 patients) |
| safety__route_group__IV | 5 | 7 | 7 | k_studies = 5, N = 7 patients (threshold: >= 3 studies AND >= 20 patients) |
| safety__route_group__topical/local | 4 | 4 | 4 | k_studies = 4, N = 4 patients (threshold: >= 3 studies AND >= 20 patients) |
| eradication__route_group__inhaled/nebulized | 3 | 4 | 11 | k_studies = 3, N = 11 patients (threshold: >= 3 studies AND >= 20 patients) |
| eradication__route_group__IV | 5 | 5 | 5 | k_studies = 5, N = 5 patients (threshold: >= 3 studies AND >= 20 patients) |
| eradication__route_group__topical/local | 5 | 5 | 5 | k_studies = 5, N = 5 patients (threshold: >= 3 studies AND >= 20 patients) |
| mortality__route_group__inhaled/nebulized | 4 | 5 | 13 | k_studies = 4, N = 13 patients (threshold: >= 3 studies AND >= 20 patients) |
| mortality__route_group__IV | 6 | 8 | 8 | k_studies = 6, N = 8 patients (threshold: >= 3 studies AND >= 20 patients) |
| mortality__route_group__topical/local | 6 | 6 | 6 | k_studies = 6, N = 6 patients (threshold: >= 3 studies AND >= 20 patients) |

## 3. GRADE

| Quantity | Value |
|---|---|
| Cells rated | 13 |
| Certainty levels present | Very low |
| Rating is deterministic (floors before data are read) | TRUE |
| Structural minimum downgrades | 4 |
| Cells at the minimum (4 downgrades) | 5 |
| ... which cells | safety__overall; mortality__overall; safety__resistance_class__MDR; mortality__resistance_class__MDR; mortality__route_group__other |
| Cells at the maximum (8 downgrades) | 2 |
| ... which cells | eradication__overall; eradication__resistance_class__MDR |
| Clinical-success cells | 4 |

## 4. Robustness

### 4.1 Population-eligibility sensitivity (excluding not-classifiable arms)

| Outcome | All arms | Classified-only | Delta (pp) | Patients dropped |
|---|---|---|---|---|
| clinical_success | 76.1% | 72.0% | -4.1 | 21 |
| safety | 19.2% | 16.3% | -2.9 | 3 |
| eradication | 57.8% | 53.1% | -4.7 | 2 |
| mortality | 10.4% | 11.5% | +1.0 | 6 |

### 4.1b De-duplication sensitivity (Pirnay-roster matches restored)

| Outcome | De-dup applied | Restored | Delta (pp) |
|---|---|---|---|
| clinical_success | 76.1% (N=71) | 76.7% (N=73) | +0.7 |
| safety | 19.2% (N=52) | 18.5% (N=54) | -0.7 |
| eradication | 57.8% (N=59) | 57.3% (N=61) | -0.5 |
| mortality | 10.4% (N=67) | 11.6% (N=69) | +1.1 |

### 4.2 Transformation / model sensitivity

Rows: 52. Full comparison is in `paper/tables/.../meta_sensitivity.tex`.

### 4.2b Does the Hartung-Knapp adjustment bind?

Ratio of the model's reported SE to the naive complete-pooling binomial SE
on the logit scale. A ratio of 1 means the interval is a plain t-interval
on the pooled counts, with no variance inflation and no random-effect term.

| Cell | method.random.ci | df | tau2 | model SE | naive binomial SE | ratio |
|---|---|---|---|---|---|---|
| clinical_success__overall | HK | 27 | 0.000 | 0.2781 | 0.2781 | 1.0000 |
| safety__overall | HK | 21 | 0.000 | 0.3519 | 0.3519 | 1.0000 |
| eradication__overall | HK | 22 | 2.198 | 0.5552 | 0.2613 | 2.1244 |
| mortality__overall | HK | 29 | 0.000 | 0.3994 | 0.3994 | 1.0000 |
| clinical_success__resistance_class__MDR | HK | 14 | 0.000 | 0.3702 | 0.3702 | 1.0000 |
| clinical_success__resistance_class__not-classifiable | HK | 6 | 0.000 | 0.6236 | 0.6236 | 1.0000 |
| safety__resistance_class__MDR | HK | 12 | 0.000 | 0.4472 | 0.4472 | 1.0000 |
| eradication__resistance_class__MDR | HK | 13 | 6.631 | 1.0079 | 0.3086 | 3.2660 |
| mortality__resistance_class__MDR | HK | 16 | 0.000 | 0.5972 | 0.5972 | 1.0000 |
| clinical_success__route_group__other | HK | 8 | 0.000 | 0.3291 | 0.3291 | 1.0000 |
| safety__route_group__other | HK | 6 | 0.000 | 0.4472 | 0.4472 | 1.0000 |
| eradication__route_group__other | HK | 7 | 0.000 | 0.3444 | 0.3444 | 1.0000 |
| mortality__route_group__other | HK | 7 | 0.000 | 0.4809 | 0.4809 | 1.0000 |

Cells where the ratio is exactly 1 (adjustment does not bind): 11 of 13.

### 4.3 Cluster-robust variance check

NOTE: fitted on an AUXILIARY normal-normal model, not the reported GLMM.

| Cell | Clusters (m) | Satterthwaite df | Naive SE | RVE SE |
|---|---|---|---|---|
| clinical_success__overall | 23 | 5.8 | 0.243 | 0.171 |
| safety__overall | 17 | 4.7 | 0.284 | 0.247 |
| eradication__overall | 19 | 3.6 | 0.258 | 0.244 |
| mortality__overall | 24 | 9.7 | 0.268 | 0.208 |
| clinical_success__resistance_class__MDR | 14 | 3.6 | 0.314 | 0.147 |
| clinical_success__resistance_class__not-classifiable | 6 | 3.1 | 0.501 | 0.453 |
| safety__resistance_class__MDR | 12 | 4.4 | 0.355 | 0.273 |
| eradication__resistance_class__MDR | 13 | 3.1 | 0.309 | 0.275 |
| mortality__resistance_class__MDR | 16 | 9.8 | 0.354 | 0.292 |
| clinical_success__route_group__other | 7 | 1.9 | 0.319 | 0.223 |
| safety__route_group__other | 5 | 1.5 | 0.388 | 0.088 |
| eradication__route_group__other | 6 | 1.4 | 0.328 | 0.093 |
| mortality__route_group__other | 6 | 1.9 | 0.425 | 0.425 |

### 4.4 Geographic-concentration exclusion (Belgium/Israel removed)

```
           outcome k_studies_full n_patients_full status_full p_hat_full
1 clinical_success             23              71      POOLED  0.7605634
2           safety             17              52      POOLED  0.1923077
3      eradication             19              59      POOLED  0.5777767
4        mortality             24              67      POOLED  0.1044776
  k_studies_excl n_patients_excl status_excl   p_hat_excl
1             21              24      POOLED 7.500001e-01
2             16              20      POOLED 2.000000e-01
3             18              27      POOLED 7.629161e-01
4             23              35      POOLED 1.314968e-16
```

## 5. Falsification / small-study checks

| Cell | k studies | Eligible (k >= 10) | Peters p |
|---|---|---|---|
| clinical_success__overall | 23 | TRUE | 0.664 |
| safety__overall | 17 | TRUE | 0.176 |
| eradication__overall | 19 | TRUE | 0.816 |
| mortality__overall | 24 | TRUE | n/a |
| clinical_success__resistance_class__MDR | 14 | TRUE | n/a |
| clinical_success__resistance_class__not-classifiable | 6 | FALSE | n/a |
| safety__resistance_class__MDR | 12 | TRUE | n/a |
| eradication__resistance_class__MDR | 13 | TRUE | n/a |
| mortality__resistance_class__MDR | 16 | TRUE | n/a |
| clinical_success__route_group__other | 7 | FALSE | n/a |
| safety__route_group__other | 5 | FALSE | n/a |
| eradication__route_group__other | 6 | FALSE | n/a |
| mortality__route_group__other | 6 | FALSE | n/a |

Cells eligible for Peters' test: 8 of 13. Cells returning a finite p-value: 3.

| Quantity | Value |
|---|---|
| Publication-year trend, status | FITTED |
| Publication-year trend, coefficient (logit per year) | 0.0628 |
| Publication-year trend, standard error | 0.1096 |
| Publication-year trend, p-value | 0.567 |

## 6. Test-power diagnostics

Peters' regressor is 1/n. Arms with n = 1: 24 of 31 (77%), for which the regressor equals exactly 1. Distinct values of 1/n across the corpus: 5.

## 7. Subgroup tests and remaining reported scalars

| Quantity | Value |
|---|---|
| Study-design subgroup, Q-between p | 0.456 |
| Route 2-category subgroup, Q-between p | 0.858 |
| Journal tier high-tier, crude clinical success | 0.796 (k = 8) |
| Journal tier mid-tier, crude clinical success | 0.647 (k = 15) |

NOTE ON SEARCH YIELDS. Database hit counts (PubMed topical, Scopus native,
ClinicalTrials.gov, the supplementary PDF corpus) are recorded in the PRISMA
figure and Methods narrative, not here: they are screening-log quantities
rather than analysis outputs, and this manifest covers what the pipeline
computes. They must still reconcile against the PRISMA figure.

