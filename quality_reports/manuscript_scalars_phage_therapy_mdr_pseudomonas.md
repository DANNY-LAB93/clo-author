# Manuscript scalar manifest --- phage_therapy_mdr_pseudomonas

MACHINE-WRITTEN by `scripts/R/11_manifest.R`. Do not edit by hand.

Every number quoted in `paper/main.tex` or `paper/sections/*.tex` must appear
in this file. A number that is not here is not quotable. Regenerate with
`Rscript scripts/R/00_master.R` and re-check the manuscript against it.

Generated: 2026-07-30 13:15 | seed: 20260720

## 1. Corpus

| Quantity | Value |
|---|---|
| Rows in cleaned extraction dataset (all arms) | 50 |
| Studies in cleaned extraction dataset | 42 |
| **Pooling-eligible study-arms** | **40** |
| **Pooling-eligible studies** | **33** |
| **Pooling-eligible patients** | **91** |
| Single-patient arms | 33 |
| Multi-patient arms | 7 |
| Patients contributed by multi-patient arms | 58 |

### 1.1 Exclusions (each with its own count)

| Step | n |
|---|---|
| Rows in cleaned extraction dataset | 50 |
| Excluded: Leitner2021 (trial-wide, not Pseudomonas-specific) | 1 |
| Excluded: published antibiogram below the MDR population criterion | 3 |
| Excluded: trial populations recruited with no MDR/XDR/PDR entry criterion | 3 |
| Excluded: case reports duplicating a patient inside the Pirnay 2024 roster | 3 |
| Rows entering stratified pooling eligibility checks | 40 |

### 1.2 Design, resistance and route distribution (pooling-eligible arms only)

**study_design**

| Level | Arms | Studies | Patients |
|---|---|---|---|
| case report | 25 | 24 | 25 |
| case series | 12 | 8 | 34 |
| retrospective cohort | 3 | 1 | 32 |

**resistance_class**

| Level | Arms | Studies | Patients |
|---|---|---|---|
| MDR | 20 | 19 | 49 |
| not-classifiable | 12 | 10 | 26 |
| PDR | 3 | 3 | 5 |
| XDR | 5 | 5 | 11 |

**route_group**

| Level | Arms | Studies | Patients |
|---|---|---|---|
| inhaled/nebulized | 7 | 6 | 15 |
| IV | 8 | 6 | 8 |
| other | 14 | 11 | 57 |
| topical/local | 7 | 7 | 7 |
| (not reported) | 4 | 4 | 4 |

**modality_group**

| Level | Arms | Studies | Patients |
|---|---|---|---|
| phage monotherapy | 3 | 2 | 3 |
| phage+antibiotic combination | 37 | 31 | 88 |

## 2. Pooled outcome-stratum cells

| Quantity | Value |
|---|---|
| **Pooled cells** | **13** |
| **Not-pooled cells** | **35** |
| Total estimated cells | 48 |

| Cell | k studies | k arms | N | Estimate | 95% CI | tau2 | 95% PI | CI width (pp) |
|---|---|---|---|---|---|---|---|---|
| clinical_success__overall | 31 | 37 | 80 | 78.7% | [68.0%, 86.6%] | 0.000 | [68.0%, 86.6%] | 18.5 |
| safety__overall | 24 | 30 | 60 | 18.3% | [10.2%, 30.8%] | 0.000 | [10.2%, 30.8%] | 20.6 |
| eradication__overall | 27 | 32 | 68 | 50.4% | [29.2%, 71.5%] | 1.995 | [4.7%, 95.4%] | 42.4 |
| mortality__overall | 32 | 39 | 76 | 9.2% | [4.3%, 18.5%] | 0.000 | [4.3%, 18.5%] | 14.1 |
| clinical_success__resistance_class__MDR | 17 | 18 | 40 | 75.0% | [58.1%, 86.6%] | 0.000 | [58.1%, 86.6%] | 28.5 |
| clinical_success__resistance_class__not-classifiable | 10 | 12 | 26 | 88.5% | [66.5%, 96.7%] | 0.000 | [66.5%, 96.7%] | 30.2 |
| safety__resistance_class__MDR | 14 | 15 | 38 | 18.4% | [8.4%, 35.7%] | 0.000 | [8.4%, 35.7%] | 27.2 |
| eradication__resistance_class__MDR | 16 | 17 | 45 | 46.5% | [12.0%, 84.7%] | 6.092 | [0.3%, 99.6%] | 72.6 |
| mortality__resistance_class__MDR | 19 | 20 | 49 | 6.1% | [1.8%, 18.5%] | 0.000 | [1.8%, 18.5%] | 16.7 |
| clinical_success__route_group__other | 11 | 14 | 57 | 78.9% | [65.0%, 88.3%] | 0.000 | [65.0%, 88.3%] | 23.3 |
| safety__route_group__other | 8 | 11 | 40 | 15.0% | [6.2%, 32.1%] | 0.000 | [6.2%, 32.1%] | 26.0 |
| eradication__route_group__other | 10 | 13 | 42 | 59.5% | [42.6%, 74.5%] | 0.000 | [42.6%, 74.5%] | 31.9 |
| mortality__route_group__other | 10 | 13 | 42 | 11.9% | [4.6%, 27.6%] | 0.000 | [4.6%, 27.6%] | 23.1 |

### 2.1 Cells NOT pooled, with reason

| Cell | k studies | k arms | N | Reason |
|---|---|---|---|---|
| clinical_success__resistance_class__PDR | 2 | 2 | 3 | k_studies = 2, N = 3 patients (threshold: >= 3 studies AND >= 20 patients) |
| clinical_success__resistance_class__XDR | 5 | 5 | 11 | k_studies = 5, N = 11 patients (threshold: >= 3 studies AND >= 20 patients) |
| safety__resistance_class__not-classifiable | 6 | 8 | 8 | k_studies = 6, N = 8 patients (threshold: >= 3 studies AND >= 20 patients) |
| safety__resistance_class__PDR | 2 | 2 | 3 | k_studies = 2, N = 3 patients (threshold: >= 3 studies AND >= 20 patients) |
| safety__resistance_class__XDR | 5 | 5 | 11 | k_studies = 5, N = 11 patients (threshold: >= 3 studies AND >= 20 patients) |
| eradication__resistance_class__not-classifiable | 6 | 7 | 7 | k_studies = 6, N = 7 patients (threshold: >= 3 studies AND >= 20 patients) |
| eradication__resistance_class__PDR | 3 | 3 | 5 | k_studies = 3, N = 5 patients (threshold: >= 3 studies AND >= 20 patients) |
| eradication__resistance_class__XDR | 5 | 5 | 11 | k_studies = 5, N = 11 patients (threshold: >= 3 studies AND >= 20 patients) |
| mortality__resistance_class__not-classifiable | 9 | 11 | 11 | k_studies = 9, N = 11 patients (threshold: >= 3 studies AND >= 20 patients) |
| mortality__resistance_class__PDR | 3 | 3 | 5 | k_studies = 3, N = 5 patients (threshold: >= 3 studies AND >= 20 patients) |
| mortality__resistance_class__XDR | 5 | 5 | 11 | k_studies = 5, N = 11 patients (threshold: >= 3 studies AND >= 20 patients) |
| clinical_success__dtr_status__yes | 4 | 4 | 5 | k_studies = 4, N = 5 patients (threshold: >= 3 studies AND >= 20 patients) |
| clinical_success__dtr_status__no | 1 | 1 | 1 | k_studies = 1, N = 1 patients (threshold: >= 3 studies AND >= 20 patients) |
| clinical_success__dtr_status__not-derivable | 28 | 32 | 74 | DTR status not derivable for 32 of 37 contributing arms; 5 were adjudicable against Kadri's first-line criterion. The obstacle is a PARTIAL antibiogram, not an absent one: a source may print several agents and still leave at least one first-line category untested, and one untested first-line category is enough to prevent both a positive and a negative call. This is a reporting-completeness failure rather than a sample-size failure. |
| safety__dtr_status__yes | 4 | 4 | 5 | k_studies = 4, N = 5 patients (threshold: >= 3 studies AND >= 20 patients) |
| safety__dtr_status__no | 1 | 1 | 1 | k_studies = 1, N = 1 patients (threshold: >= 3 studies AND >= 20 patients) |
| safety__dtr_status__not-derivable | 21 | 25 | 54 | DTR status not derivable for 25 of 30 contributing arms; 5 were adjudicable against Kadri's first-line criterion. The obstacle is a PARTIAL antibiogram, not an absent one: a source may print several agents and still leave at least one first-line category untested, and one untested first-line category is enough to prevent both a positive and a negative call. This is a reporting-completeness failure rather than a sample-size failure. |
| eradication__dtr_status__yes | 5 | 5 | 7 | k_studies = 5, N = 7 patients (threshold: >= 3 studies AND >= 20 patients) |
| eradication__dtr_status__no | 1 | 1 | 1 | k_studies = 1, N = 1 patients (threshold: >= 3 studies AND >= 20 patients) |
| eradication__dtr_status__not-derivable | 24 | 26 | 60 | DTR status not derivable for 26 of 32 contributing arms; 6 were adjudicable against Kadri's first-line criterion. The obstacle is a PARTIAL antibiogram, not an absent one: a source may print several agents and still leave at least one first-line category untested, and one untested first-line category is enough to prevent both a positive and a negative call. This is a reporting-completeness failure rather than a sample-size failure. |
| mortality__dtr_status__yes | 5 | 5 | 7 | k_studies = 5, N = 7 patients (threshold: >= 3 studies AND >= 20 patients) |
| mortality__dtr_status__no | 1 | 1 | 1 | k_studies = 1, N = 1 patients (threshold: >= 3 studies AND >= 20 patients) |
| mortality__dtr_status__not-derivable | 29 | 33 | 68 | DTR status not derivable for 33 of 39 contributing arms; 6 were adjudicable against Kadri's first-line criterion. The obstacle is a PARTIAL antibiogram, not an absent one: a source may print several agents and still leave at least one first-line category untested, and one untested first-line category is enough to prevent both a positive and a negative call. This is a reporting-completeness failure rather than a sample-size failure. |
| clinical_success__route_group__inhaled/nebulized | 4 | 4 | 4 | k_studies = 4, N = 4 patients (threshold: >= 3 studies AND >= 20 patients) |
| clinical_success__route_group__IV | 6 | 8 | 8 | k_studies = 6, N = 8 patients (threshold: >= 3 studies AND >= 20 patients) |
| clinical_success__route_group__topical/local | 7 | 7 | 7 | k_studies = 7, N = 7 patients (threshold: >= 3 studies AND >= 20 patients) |
| safety__route_group__inhaled/nebulized | 5 | 5 | 6 | k_studies = 5, N = 6 patients (threshold: >= 3 studies AND >= 20 patients) |
| safety__route_group__IV | 5 | 7 | 7 | k_studies = 5, N = 7 patients (threshold: >= 3 studies AND >= 20 patients) |
| safety__route_group__topical/local | 5 | 5 | 5 | k_studies = 5, N = 5 patients (threshold: >= 3 studies AND >= 20 patients) |
| eradication__route_group__inhaled/nebulized | 5 | 6 | 13 | k_studies = 5, N = 13 patients (threshold: >= 3 studies AND >= 20 patients) |
| eradication__route_group__IV | 5 | 5 | 5 | k_studies = 5, N = 5 patients (threshold: >= 3 studies AND >= 20 patients) |
| eradication__route_group__topical/local | 6 | 6 | 6 | k_studies = 6, N = 6 patients (threshold: >= 3 studies AND >= 20 patients) |
| mortality__route_group__inhaled/nebulized | 6 | 7 | 15 | k_studies = 6, N = 15 patients (threshold: >= 3 studies AND >= 20 patients) |
| mortality__route_group__IV | 6 | 8 | 8 | k_studies = 6, N = 8 patients (threshold: >= 3 studies AND >= 20 patients) |
| mortality__route_group__topical/local | 7 | 7 | 7 | k_studies = 7, N = 7 patients (threshold: >= 3 studies AND >= 20 patients) |

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
| clinical_success | 78.7% | 74.1% | -4.7 | 26 |
| safety | 18.3% | 17.3% | -1.0 | 8 |
| eradication | 50.4% | 48.4% | -2.1 | 7 |
| mortality | 9.2% | 10.8% | +1.6 | 11 |

### 4.1b De-duplication sensitivity (Pirnay-roster matches restored)

| Outcome | De-dup applied | Restored | Delta (pp) |
|---|---|---|---|
| clinical_success | 78.7% (N=80) | 79.3% (N=82) | +0.5 |
| safety | 18.3% (N=60) | 17.7% (N=62) | -0.6 |
| eradication | 50.4% (N=68) | 50.4% (N=70) | -0.0 |
| mortality | 9.2% (N=76) | 10.3% (N=78) | +1.0 |

### 4.2 Transformation / model sensitivity

Rows: 52. Full comparison is in `paper/tables/.../meta_sensitivity.tex`.

### 4.2b Does the Hartung-Knapp adjustment bind?

Ratio of the model's reported SE to the naive complete-pooling binomial SE
on the logit scale. A ratio of 1 means the interval is a plain t-interval
on the pooled counts, with no variance inflation and no random-effect term.

| Cell | method.random.ci | df | tau2 | model SE | naive binomial SE | ratio |
|---|---|---|---|---|---|---|
| clinical_success__overall | HK | 36 | 0.000 | 0.2733 | 0.2733 | 1.0000 |
| safety__overall | HK | 29 | 0.000 | 0.3336 | 0.3336 | 1.0000 |
| eradication__overall | HK | 31 | 1.995 | 0.4436 | 0.2426 | 1.8281 |
| mortality__overall | HK | 38 | 0.000 | 0.3967 | 0.3967 | 1.0000 |
| clinical_success__resistance_class__MDR | HK | 17 | 0.000 | 0.3651 | 0.3651 | 1.0000 |
| clinical_success__resistance_class__not-classifiable | HK | 11 | 0.000 | 0.6138 | 0.6138 | 1.0000 |
| safety__resistance_class__MDR | HK | 14 | 0.000 | 0.4185 | 0.4185 | 1.0000 |
| eradication__resistance_class__MDR | HK | 16 | 6.092 | 0.8720 | 0.2982 | 2.9239 |
| mortality__resistance_class__MDR | HK | 19 | 0.000 | 0.5959 | 0.5959 | 1.0000 |
| clinical_success__route_group__other | HK | 13 | 0.000 | 0.3249 | 0.3249 | 1.0000 |
| safety__route_group__other | HK | 10 | 0.000 | 0.4428 | 0.4428 | 1.0000 |
| eradication__route_group__other | HK | 12 | 0.000 | 0.3144 | 0.3144 | 1.0000 |
| mortality__route_group__other | HK | 12 | 0.000 | 0.4765 | 0.4765 | 1.0000 |

Cells where the ratio is exactly 1 (adjustment does not bind): 11 of 13.

### 4.3 Cluster-robust variance check

NOTE: fitted on an AUXILIARY normal-normal model, not the reported GLMM.

| Cell | Clusters (m) | Satterthwaite df | Naive SE | RVE SE |
|---|---|---|---|---|
| clinical_success__overall | 31 | 8.2 | 0.222 | 0.138 |
| safety__overall | 24 | 7.0 | 0.255 | 0.206 |
| eradication__overall | 27 | 5.4 | 0.233 | 0.247 |
| mortality__overall | 32 | 14.0 | 0.240 | 0.166 |
| clinical_success__resistance_class__MDR | 17 | 4.5 | 0.298 | 0.124 |
| clinical_success__resistance_class__not-classifiable | 10 | 5.9 | 0.413 | 0.292 |
| safety__resistance_class__MDR | 14 | 5.2 | 0.339 | 0.298 |
| eradication__resistance_class__MDR | 16 | 3.8 | 0.294 | 0.275 |
| mortality__resistance_class__MDR | 19 | 12.1 | 0.332 | 0.260 |
| clinical_success__route_group__other | 11 | 2.7 | 0.292 | 0.183 |
| safety__route_group__other | 8 | 2.1 | 0.350 | 0.101 |
| eradication__route_group__other | 10 | 2.0 | 0.299 | 0.244 |
| mortality__route_group__other | 10 | 3.2 | 0.367 | 0.312 |

### 4.4 Geographic-concentration exclusion (Belgium/Israel removed)

```
           outcome k_studies_full n_patients_full status_full p_hat_full
1 clinical_success             31              80      POOLED 0.78749999
2           safety             24              60      POOLED 0.18333333
3      eradication             27              68      POOLED 0.50425612
4        mortality             32              76      POOLED 0.09210526
  k_studies_excl n_patients_excl status_excl   p_hat_excl
1             29              33      POOLED 8.181818e-01
2             23              28      POOLED 1.785714e-01
3             26              36      POOLED 5.198165e-01
4             31              44      POOLED 1.218655e-17
```

## 5. Falsification / small-study checks

| Cell | k studies | Eligible (k >= 10) | Peters p |
|---|---|---|---|
| clinical_success__overall | 31 | TRUE | 0.664 |
| safety__overall | 24 | TRUE | 0.176 |
| eradication__overall | 27 | TRUE | 0.816 |
| mortality__overall | 32 | TRUE | n/a |
| clinical_success__resistance_class__MDR | 17 | TRUE | n/a |
| clinical_success__resistance_class__not-classifiable | 10 | TRUE | n/a |
| safety__resistance_class__MDR | 14 | TRUE | n/a |
| eradication__resistance_class__MDR | 16 | TRUE | n/a |
| mortality__resistance_class__MDR | 19 | TRUE | n/a |
| clinical_success__route_group__other | 11 | TRUE | 0.664 |
| safety__route_group__other | 8 | FALSE | n/a |
| eradication__route_group__other | 10 | TRUE | 0.816 |
| mortality__route_group__other | 10 | TRUE | n/a |

Cells eligible for Peters' test: 12 of 13. Cells returning a finite p-value: 5.

| Quantity | Value |
|---|---|
| Publication-year trend, status | FITTED |
| Publication-year trend, coefficient (logit per year) | 0.0549 |
| Publication-year trend, standard error | 0.1037 |
| Publication-year trend, p-value | 0.596 |

## 6. Test-power diagnostics

Peters' regressor is 1/n. Arms with n = 1: 33 of 40 (82%), for which the regressor equals exactly 1. Distinct values of 1/n across the corpus: 5.

## 7. Subgroup tests and remaining reported scalars

| Quantity | Value |
|---|---|
| Study-design subgroup, Q-between p | 0.224 |
| Route 2-category subgroup, Q-between p | 0.728 |
| Journal tier high-tier, crude clinical success | 0.800 (k = 9) |
| Journal tier mid-tier, crude clinical success | 0.760 (k = 22) |

NOTE ON SEARCH YIELDS. Database hit counts (PubMed topical, Scopus native,
ClinicalTrials.gov, the supplementary PDF corpus) are recorded in the PRISMA
figure and Methods narrative, not here: they are screening-log quantities
rather than analysis outputs, and this manifest covers what the pipeline
computes. They must still reconcile against the PRISMA figure.

