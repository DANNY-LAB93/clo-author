# Manuscript scalar manifest --- phage_therapy_mdr_pseudomonas

MACHINE-WRITTEN by `scripts/R/11_manifest.R`. Do not edit by hand.

Every number quoted in `paper/main.tex` or `paper/sections/*.tex` must appear
in this file. A number that is not here is not quotable. Regenerate with
`Rscript scripts/R/00_master.R` and re-check the manuscript against it.

Generated: 2026-07-29 15:26 | seed: 20260720

## 1. Corpus

| Quantity | Value |
|---|---|
| Rows in cleaned extraction dataset (all arms) | 41 |
| Studies in cleaned extraction dataset | 33 |
| **Pooling-eligible study-arms** | **34** |
| **Pooling-eligible studies** | **27** |
| **Pooling-eligible patients** | **85** |
| Single-patient arms | 27 |
| Multi-patient arms | 7 |
| Patients contributed by multi-patient arms | 58 |

### 1.1 Exclusions (each with its own count)

| Step | n |
|---|---|
| Rows in cleaned extraction dataset | 41 |
| Excluded: Leitner2021 (trial-wide, not Pseudomonas-specific) | 1 |
| Excluded: Liu2025 (antibiogram does not meet the MDR population criterion) | 1 |
| Excluded: trial populations recruited with no MDR/XDR/PDR entry criterion | 3 |
| Excluded: case reports duplicating a patient inside the Pirnay 2024 roster | 2 |
| Rows entering stratified pooling eligibility checks | 34 |

### 1.2 Design, resistance and route distribution (pooling-eligible arms only)

**study_design**

| Level | Arms | Studies | Patients |
|---|---|---|---|
| case report | 20 | 19 | 20 |
| case series | 11 | 7 | 33 |
| retrospective cohort | 3 | 1 | 32 |

**resistance_class**

| Level | Arms | Studies | Patients |
|---|---|---|---|
| MDR | 17 | 16 | 46 |
| not-classifiable | 10 | 8 | 24 |
| PDR | 3 | 3 | 5 |
| XDR | 4 | 4 | 10 |

**route_group**

| Level | Arms | Studies | Patients |
|---|---|---|---|
| inhaled/nebulized | 5 | 4 | 13 |
| IV | 8 | 6 | 8 |
| other | 12 | 9 | 55 |
| topical/local | 6 | 6 | 6 |
| (not reported) | 3 | 3 | 3 |

**modality_group**

| Level | Arms | Studies | Patients |
|---|---|---|---|
| phage monotherapy | 3 | 2 | 3 |
| phage+antibiotic combination | 31 | 25 | 82 |

## 2. Pooled outcome-stratum cells

| Quantity | Value |
|---|---|
| **Pooled cells** | **13** |
| **Not-pooled cells** | **31** |
| Total estimated cells | 44 |

| Cell | k studies | k arms | N | Estimate | 95% CI | tau2 | 95% PI | CI width (pp) |
|---|---|---|---|---|---|---|---|---|
| clinical_success__overall | 25 | 31 | 74 | 77.0% | [65.6%, 85.5%] | 0.000 | [65.6%, 85.5%] | 19.9 |
| safety__overall | 19 | 25 | 55 | 18.2% | [9.7%, 31.4%] | 0.000 | [9.7%, 31.4%] | 21.6 |
| eradication__overall | 21 | 26 | 62 | 50.5% | [27.4%, 73.4%] | 1.997 | [4.5%, 95.7%] | 46.0 |
| mortality__overall | 26 | 33 | 70 | 10.0% | [4.7%, 20.0%] | 0.000 | [4.7%, 20.0%] | 15.3 |
| clinical_success__resistance_class__MDR | 14 | 15 | 37 | 73.0% | [55.0%, 85.7%] | 0.000 | [55.0%, 85.7%] | 30.7 |
| clinical_success__resistance_class__not-classifiable | 8 | 10 | 24 | 87.5% | [63.4%, 96.6%] | 0.000 | [63.4%, 96.6%] | 33.2 |
| safety__resistance_class__MDR | 12 | 13 | 36 | 16.7% | [7.0%, 34.6%] | 0.000 | [7.0%, 34.6%] | 27.6 |
| eradication__resistance_class__MDR | 13 | 14 | 42 | 52.0% | [10.9%, 90.5%] | 6.631 | [0.3%, 99.8%] | 79.6 |
| mortality__resistance_class__MDR | 16 | 17 | 46 | 6.5% | [1.9%, 19.8%] | 0.000 | [1.9%, 19.8%] | 17.9 |
| clinical_success__route_group__other | 9 | 12 | 55 | 78.2% | [63.6%, 88.0%] | 0.000 | [63.6%, 88.0%] | 24.4 |
| safety__route_group__other | 7 | 10 | 39 | 15.4% | [6.2%, 33.2%] | 0.000 | [6.2%, 33.2%] | 26.9 |
| eradication__route_group__other | 8 | 11 | 40 | 60.0% | [42.2%, 75.5%] | 0.000 | [42.2%, 75.5%] | 33.3 |
| mortality__route_group__other | 8 | 11 | 40 | 12.5% | [4.7%, 29.3%] | 0.000 | [4.7%, 29.3%] | 24.6 |

### 2.1 Cells NOT pooled, with reason

| Cell | k studies | k arms | N | Reason |
|---|---|---|---|---|
| clinical_success__resistance_class__PDR | 2 | 2 | 3 | k_studies = 2, N = 3 patients (threshold: >= 3 studies AND >= 20 patients) |
| clinical_success__resistance_class__XDR | 4 | 4 | 10 | k_studies = 4, N = 10 patients (threshold: >= 3 studies AND >= 20 patients) |
| safety__resistance_class__not-classifiable | 4 | 6 | 6 | k_studies = 4, N = 6 patients (threshold: >= 3 studies AND >= 20 patients) |
| safety__resistance_class__PDR | 2 | 2 | 3 | k_studies = 2, N = 3 patients (threshold: >= 3 studies AND >= 20 patients) |
| safety__resistance_class__XDR | 4 | 4 | 10 | k_studies = 4, N = 10 patients (threshold: >= 3 studies AND >= 20 patients) |
| eradication__resistance_class__not-classifiable | 4 | 5 | 5 | k_studies = 4, N = 5 patients (threshold: >= 3 studies AND >= 20 patients) |
| eradication__resistance_class__PDR | 3 | 3 | 5 | k_studies = 3, N = 5 patients (threshold: >= 3 studies AND >= 20 patients) |
| eradication__resistance_class__XDR | 4 | 4 | 10 | k_studies = 4, N = 10 patients (threshold: >= 3 studies AND >= 20 patients) |
| mortality__resistance_class__not-classifiable | 7 | 9 | 9 | k_studies = 7, N = 9 patients (threshold: >= 3 studies AND >= 20 patients) |
| mortality__resistance_class__PDR | 3 | 3 | 5 | k_studies = 3, N = 5 patients (threshold: >= 3 studies AND >= 20 patients) |
| mortality__resistance_class__XDR | 4 | 4 | 10 | k_studies = 4, N = 10 patients (threshold: >= 3 studies AND >= 20 patients) |
| clinical_success__dtr_status__yes | 2 | 2 | 3 | k_studies = 2, N = 3 patients (threshold: >= 3 studies AND >= 20 patients) |
| clinical_success__dtr_status__not-derivable | 24 | 29 | 71 | DTR status not derivable for 29 of 31 contributing arms: the source publishes no agent-level antibiogram covering all beta-lactams and both fluoroquinolones. NOT a sample-size failure -- this cell fails for ABSENT DATA and is the only stratum in this review that does. |
| safety__dtr_status__yes | 2 | 2 | 3 | k_studies = 2, N = 3 patients (threshold: >= 3 studies AND >= 20 patients) |
| safety__dtr_status__not-derivable | 18 | 23 | 52 | DTR status not derivable for 23 of 25 contributing arms: the source publishes no agent-level antibiogram covering all beta-lactams and both fluoroquinolones. NOT a sample-size failure -- this cell fails for ABSENT DATA and is the only stratum in this review that does. |
| eradication__dtr_status__yes | 3 | 3 | 5 | k_studies = 3, N = 5 patients (threshold: >= 3 studies AND >= 20 patients) |
| eradication__dtr_status__not-derivable | 20 | 23 | 57 | DTR status not derivable for 23 of 26 contributing arms: the source publishes no agent-level antibiogram covering all beta-lactams and both fluoroquinolones. NOT a sample-size failure -- this cell fails for ABSENT DATA and is the only stratum in this review that does. |
| mortality__dtr_status__yes | 3 | 3 | 5 | k_studies = 3, N = 5 patients (threshold: >= 3 studies AND >= 20 patients) |
| mortality__dtr_status__not-derivable | 25 | 30 | 65 | DTR status not derivable for 30 of 33 contributing arms: the source publishes no agent-level antibiogram covering all beta-lactams and both fluoroquinolones. NOT a sample-size failure -- this cell fails for ABSENT DATA and is the only stratum in this review that does. |
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
| Structural minimum downgrades | 3 |
| Cells at the minimum (3 downgrades) | 4 |
| ... which cells | safety__overall; mortality__overall; safety__route_group__other; mortality__route_group__other |
| Cells at the maximum (8 downgrades) | 1 |
| ... which cells | eradication__resistance_class__MDR |
| Clinical-success cells | 4 |

## 4. Robustness

### 4.1 Population-eligibility sensitivity (excluding not-classifiable arms)

| Outcome | All arms | Classified-only | Delta (pp) | Patients dropped |
|---|---|---|---|---|
| clinical_success | 77.0% | 72.0% | -5.0 | 24 |
| safety | 18.2% | 16.3% | -1.9 | 6 |
| eradication | 50.5% | 53.1% | +2.6 | 5 |
| mortality | 10.0% | 11.5% | +1.5 | 9 |

### 4.1b De-duplication sensitivity (Pirnay-roster matches restored)

| Outcome | De-dup applied | Restored | Delta (pp) |
|---|---|---|---|
| clinical_success | 77.0% (N=74) | 77.6% (N=76) | +0.6 |
| safety | 18.2% (N=55) | 17.5% (N=57) | -0.6 |
| eradication | 50.5% (N=62) | 50.5% (N=64) | -0.0 |
| mortality | 10.0% (N=70) | 11.1% (N=72) | +1.1 |

### 4.2 Transformation / model sensitivity

Rows: 52. Full comparison is in `paper/tables/.../meta_sensitivity.tex`.

### 4.2b Does the Hartung-Knapp adjustment bind?

Ratio of the model's reported SE to the naive complete-pooling binomial SE
on the logit scale. A ratio of 1 means the interval is a plain t-interval
on the pooled counts, with no variance inflation and no random-effect term.

| Cell | method.random.ci | df | tau2 | model SE | naive binomial SE | ratio |
|---|---|---|---|---|---|---|
| clinical_success__overall | HK | 30 | 0.000 | 0.2763 | 0.2763 | 1.0000 |
| safety__overall | HK | 24 | 0.000 | 0.3496 | 0.3496 | 1.0000 |
| eradication__overall | HK | 25 | 1.997 | 0.4830 | 0.2541 | 1.9005 |
| mortality__overall | HK | 32 | 0.000 | 0.3984 | 0.3984 | 1.0000 |
| clinical_success__resistance_class__MDR | HK | 14 | 0.000 | 0.3702 | 0.3702 | 1.0000 |
| clinical_success__resistance_class__not-classifiable | HK | 9 | 0.000 | 0.6172 | 0.6172 | 1.0000 |
| safety__resistance_class__MDR | HK | 12 | 0.000 | 0.4472 | 0.4472 | 1.0000 |
| eradication__resistance_class__MDR | HK | 13 | 6.631 | 1.0079 | 0.3086 | 3.2660 |
| mortality__resistance_class__MDR | HK | 16 | 0.000 | 0.5972 | 0.5972 | 1.0000 |
| clinical_success__route_group__other | HK | 11 | 0.000 | 0.3265 | 0.3265 | 1.0000 |
| safety__route_group__other | HK | 9 | 0.000 | 0.4438 | 0.4438 | 1.0000 |
| eradication__route_group__other | HK | 10 | 0.000 | 0.3227 | 0.3227 | 1.0000 |
| mortality__route_group__other | HK | 10 | 0.000 | 0.4781 | 0.4781 | 1.0000 |

Cells where the ratio is exactly 1 (adjustment does not bind): 11 of 13.

### 4.3 Cluster-robust variance check

NOTE: fitted on an AUXILIARY normal-normal model, not the reported GLMM.

| Cell | Clusters (m) | Satterthwaite df | Naive SE | RVE SE |
|---|---|---|---|---|
| clinical_success__overall | 25 | 6.5 | 0.235 | 0.158 |
| safety__overall | 19 | 5.5 | 0.272 | 0.218 |
| eradication__overall | 21 | 4.2 | 0.249 | 0.272 |
| mortality__overall | 26 | 11.0 | 0.257 | 0.192 |
| clinical_success__resistance_class__MDR | 14 | 3.6 | 0.314 | 0.147 |
| clinical_success__resistance_class__not-classifiable | 8 | 4.6 | 0.442 | 0.340 |
| safety__resistance_class__MDR | 12 | 4.4 | 0.355 | 0.273 |
| eradication__resistance_class__MDR | 13 | 3.1 | 0.309 | 0.275 |
| mortality__resistance_class__MDR | 16 | 9.8 | 0.354 | 0.292 |
| clinical_success__route_group__other | 9 | 2.4 | 0.302 | 0.197 |
| safety__route_group__other | 7 | 1.9 | 0.359 | 0.101 |
| eradication__route_group__other | 8 | 1.8 | 0.310 | 0.244 |
| mortality__route_group__other | 8 | 2.6 | 0.387 | 0.348 |

### 4.4 Geographic-concentration exclusion (Belgium/Israel removed)

```
           outcome k_studies_full n_patients_full status_full p_hat_full
1 clinical_success             25              74      POOLED  0.7702703
2           safety             19              55      POOLED  0.1818182
3      eradication             21              62      POOLED  0.5050452
4        mortality             26              70      POOLED  0.1000000
  k_studies_excl n_patients_excl status_excl   p_hat_excl
1             23              27      POOLED 7.777778e-01
2             18              23      POOLED 1.739131e-01
3             20              30      POOLED 5.295384e-01
4             25              38      POOLED 5.190443e-17
```

## 5. Falsification / small-study checks

| Cell | k studies | Eligible (k >= 10) | Peters p |
|---|---|---|---|
| clinical_success__overall | 25 | TRUE | 0.664 |
| safety__overall | 19 | TRUE | 0.176 |
| eradication__overall | 21 | TRUE | 0.816 |
| mortality__overall | 26 | TRUE | n/a |
| clinical_success__resistance_class__MDR | 14 | TRUE | n/a |
| clinical_success__resistance_class__not-classifiable | 8 | FALSE | n/a |
| safety__resistance_class__MDR | 12 | TRUE | n/a |
| eradication__resistance_class__MDR | 13 | TRUE | n/a |
| mortality__resistance_class__MDR | 16 | TRUE | n/a |
| clinical_success__route_group__other | 9 | FALSE | n/a |
| safety__route_group__other | 7 | FALSE | n/a |
| eradication__route_group__other | 8 | FALSE | n/a |
| mortality__route_group__other | 8 | FALSE | n/a |

Cells eligible for Peters' test: 8 of 13. Cells returning a finite p-value: 3.

| Quantity | Value |
|---|---|
| Publication-year trend, status | FITTED |
| Publication-year trend, coefficient (logit per year) | 0.0570 |
| Publication-year trend, standard error | 0.1080 |
| Publication-year trend, p-value | 0.598 |

## 6. Test-power diagnostics

Peters' regressor is 1/n. Arms with n = 1: 27 of 34 (79%), for which the regressor equals exactly 1. Distinct values of 1/n across the corpus: 5.

## 7. Subgroup tests and remaining reported scalars

| Quantity | Value |
|---|---|
| Study-design subgroup, Q-between p | 0.360 |
| Route 2-category subgroup, Q-between p | 0.887 |
| Journal tier high-tier, crude clinical success | 0.800 (k = 9) |
| Journal tier mid-tier, crude clinical success | 0.684 (k = 16) |

NOTE ON SEARCH YIELDS. Database hit counts (PubMed topical, Scopus native,
ClinicalTrials.gov, the supplementary PDF corpus) are recorded in the PRISMA
figure and Methods narrative, not here: they are screening-log quantities
rather than analysis outputs, and this manifest covers what the pipeline
computes. They must still reconcile against the PRISMA figure.

