# Manuscript scalar manifest --- phage_therapy_mdr_pseudomonas

MACHINE-WRITTEN by `scripts/R/11_manifest.R`. Do not edit by hand.

Every number quoted in `paper/main.tex` or `paper/sections/*.tex` must appear
in this file. A number that is not here is not quotable. Regenerate with
`Rscript scripts/R/00_master.R` and re-check the manuscript against it.

Generated: 2026-07-29 20:09 | seed: 20260720

## 1. Corpus

| Quantity | Value |
|---|---|
| Rows in cleaned extraction dataset (all arms) | 48 |
| Studies in cleaned extraction dataset | 40 |
| **Pooling-eligible study-arms** | **38** |
| **Pooling-eligible studies** | **31** |
| **Pooling-eligible patients** | **89** |
| Single-patient arms | 31 |
| Multi-patient arms | 7 |
| Patients contributed by multi-patient arms | 58 |

### 1.1 Exclusions (each with its own count)

| Step | n |
|---|---|
| Rows in cleaned extraction dataset | 48 |
| Excluded: Leitner2021 (trial-wide, not Pseudomonas-specific) | 1 |
| Excluded: published antibiogram below the MDR population criterion | 3 |
| Excluded: trial populations recruited with no MDR/XDR/PDR entry criterion | 3 |
| Excluded: case reports duplicating a patient inside the Pirnay 2024 roster | 3 |
| Rows entering stratified pooling eligibility checks | 38 |

### 1.2 Design, resistance and route distribution (pooling-eligible arms only)

**study_design**

| Level | Arms | Studies | Patients |
|---|---|---|---|
| case report | 24 | 23 | 24 |
| case series | 11 | 7 | 33 |
| retrospective cohort | 3 | 1 | 32 |

**resistance_class**

| Level | Arms | Studies | Patients |
|---|---|---|---|
| MDR | 19 | 18 | 48 |
| not-classifiable | 11 | 9 | 25 |
| PDR | 3 | 3 | 5 |
| XDR | 5 | 5 | 11 |

**route_group**

| Level | Arms | Studies | Patients |
|---|---|---|---|
| inhaled/nebulized | 6 | 5 | 14 |
| IV | 8 | 6 | 8 |
| other | 14 | 11 | 57 |
| topical/local | 6 | 6 | 6 |
| (not reported) | 4 | 4 | 4 |

**modality_group**

| Level | Arms | Studies | Patients |
|---|---|---|---|
| phage monotherapy | 3 | 2 | 3 |
| phage+antibiotic combination | 35 | 29 | 86 |

## 2. Pooled outcome-stratum cells

| Quantity | Value |
|---|---|
| **Pooled cells** | **13** |
| **Not-pooled cells** | **31** |
| Total estimated cells | 44 |

| Cell | k studies | k arms | N | Estimate | 95% CI | tau2 | 95% PI | CI width (pp) |
|---|---|---|---|---|---|---|---|---|
| clinical_success__overall | 29 | 35 | 78 | 78.2% | [67.3%, 86.2%] | 0.000 | [67.3%, 86.2%] | 19.0 |
| safety__overall | 22 | 28 | 58 | 19.0% | [10.5%, 31.8%] | 0.000 | [10.5%, 31.8%] | 21.2 |
| eradication__overall | 25 | 30 | 66 | 50.4% | [28.6%, 72.1%] | 1.996 | [4.7%, 95.5%] | 43.5 |
| mortality__overall | 30 | 37 | 74 | 9.5% | [4.5%, 19.0%] | 0.000 | [4.5%, 19.0%] | 14.5 |
| clinical_success__resistance_class__MDR | 16 | 17 | 39 | 74.4% | [57.1%, 86.3%] | 0.000 | [57.1%, 86.3%] | 29.2 |
| clinical_success__resistance_class__not-classifiable | 9 | 11 | 25 | 88.0% | [65.0%, 96.7%] | 0.000 | [65.0%, 96.7%] | 31.6 |
| safety__resistance_class__MDR | 13 | 14 | 37 | 18.9% | [8.6%, 36.6%] | 0.000 | [8.6%, 36.6%] | 28.0 |
| eradication__resistance_class__MDR | 15 | 16 | 44 | 51.8% | [12.6%, 88.9%] | 6.552 | [0.3%, 99.7%] | 76.3 |
| mortality__resistance_class__MDR | 18 | 19 | 48 | 6.3% | [1.9%, 18.9%] | 0.000 | [1.9%, 18.9%] | 17.0 |
| clinical_success__route_group__other | 11 | 14 | 57 | 78.9% | [65.0%, 88.3%] | 0.000 | [65.0%, 88.3%] | 23.3 |
| safety__route_group__other | 8 | 11 | 40 | 15.0% | [6.2%, 32.1%] | 0.000 | [6.2%, 32.1%] | 26.0 |
| eradication__route_group__other | 10 | 13 | 42 | 59.5% | [42.6%, 74.5%] | 0.000 | [42.6%, 74.5%] | 31.9 |
| mortality__route_group__other | 10 | 13 | 42 | 11.9% | [4.6%, 27.6%] | 0.000 | [4.6%, 27.6%] | 23.1 |

### 2.1 Cells NOT pooled, with reason

| Cell | k studies | k arms | N | Reason |
|---|---|---|---|---|
| clinical_success__resistance_class__PDR | 2 | 2 | 3 | k_studies = 2, N = 3 patients (threshold: >= 3 studies AND >= 20 patients) |
| clinical_success__resistance_class__XDR | 5 | 5 | 11 | k_studies = 5, N = 11 patients (threshold: >= 3 studies AND >= 20 patients) |
| safety__resistance_class__not-classifiable | 5 | 7 | 7 | k_studies = 5, N = 7 patients (threshold: >= 3 studies AND >= 20 patients) |
| safety__resistance_class__PDR | 2 | 2 | 3 | k_studies = 2, N = 3 patients (threshold: >= 3 studies AND >= 20 patients) |
| safety__resistance_class__XDR | 5 | 5 | 11 | k_studies = 5, N = 11 patients (threshold: >= 3 studies AND >= 20 patients) |
| eradication__resistance_class__not-classifiable | 5 | 6 | 6 | k_studies = 5, N = 6 patients (threshold: >= 3 studies AND >= 20 patients) |
| eradication__resistance_class__PDR | 3 | 3 | 5 | k_studies = 3, N = 5 patients (threshold: >= 3 studies AND >= 20 patients) |
| eradication__resistance_class__XDR | 5 | 5 | 11 | k_studies = 5, N = 11 patients (threshold: >= 3 studies AND >= 20 patients) |
| mortality__resistance_class__not-classifiable | 8 | 10 | 10 | k_studies = 8, N = 10 patients (threshold: >= 3 studies AND >= 20 patients) |
| mortality__resistance_class__PDR | 3 | 3 | 5 | k_studies = 3, N = 5 patients (threshold: >= 3 studies AND >= 20 patients) |
| mortality__resistance_class__XDR | 5 | 5 | 11 | k_studies = 5, N = 11 patients (threshold: >= 3 studies AND >= 20 patients) |
| clinical_success__dtr_status__yes | 2 | 2 | 3 | k_studies = 2, N = 3 patients (threshold: >= 3 studies AND >= 20 patients) |
| clinical_success__dtr_status__not-derivable | 28 | 33 | 75 | DTR status not derivable for 33 of 35 contributing arms: the source publishes no agent-level antibiogram covering all beta-lactams and both fluoroquinolones. NOT a sample-size failure -- this cell fails for ABSENT DATA and is the only stratum in this review that does. |
| safety__dtr_status__yes | 2 | 2 | 3 | k_studies = 2, N = 3 patients (threshold: >= 3 studies AND >= 20 patients) |
| safety__dtr_status__not-derivable | 21 | 26 | 55 | DTR status not derivable for 26 of 28 contributing arms: the source publishes no agent-level antibiogram covering all beta-lactams and both fluoroquinolones. NOT a sample-size failure -- this cell fails for ABSENT DATA and is the only stratum in this review that does. |
| eradication__dtr_status__yes | 3 | 3 | 5 | k_studies = 3, N = 5 patients (threshold: >= 3 studies AND >= 20 patients) |
| eradication__dtr_status__not-derivable | 24 | 27 | 61 | DTR status not derivable for 27 of 30 contributing arms: the source publishes no agent-level antibiogram covering all beta-lactams and both fluoroquinolones. NOT a sample-size failure -- this cell fails for ABSENT DATA and is the only stratum in this review that does. |
| mortality__dtr_status__yes | 3 | 3 | 5 | k_studies = 3, N = 5 patients (threshold: >= 3 studies AND >= 20 patients) |
| mortality__dtr_status__not-derivable | 29 | 34 | 69 | DTR status not derivable for 34 of 37 contributing arms: the source publishes no agent-level antibiogram covering all beta-lactams and both fluoroquinolones. NOT a sample-size failure -- this cell fails for ABSENT DATA and is the only stratum in this review that does. |
| clinical_success__route_group__inhaled/nebulized | 3 | 3 | 3 | k_studies = 3, N = 3 patients (threshold: >= 3 studies AND >= 20 patients) |
| clinical_success__route_group__IV | 6 | 8 | 8 | k_studies = 6, N = 8 patients (threshold: >= 3 studies AND >= 20 patients) |
| clinical_success__route_group__topical/local | 6 | 6 | 6 | k_studies = 6, N = 6 patients (threshold: >= 3 studies AND >= 20 patients) |
| safety__route_group__inhaled/nebulized | 4 | 4 | 5 | k_studies = 4, N = 5 patients (threshold: >= 3 studies AND >= 20 patients) |
| safety__route_group__IV | 5 | 7 | 7 | k_studies = 5, N = 7 patients (threshold: >= 3 studies AND >= 20 patients) |
| safety__route_group__topical/local | 4 | 4 | 4 | k_studies = 4, N = 4 patients (threshold: >= 3 studies AND >= 20 patients) |
| eradication__route_group__inhaled/nebulized | 4 | 5 | 12 | k_studies = 4, N = 12 patients (threshold: >= 3 studies AND >= 20 patients) |
| eradication__route_group__IV | 5 | 5 | 5 | k_studies = 5, N = 5 patients (threshold: >= 3 studies AND >= 20 patients) |
| eradication__route_group__topical/local | 5 | 5 | 5 | k_studies = 5, N = 5 patients (threshold: >= 3 studies AND >= 20 patients) |
| mortality__route_group__inhaled/nebulized | 5 | 6 | 14 | k_studies = 5, N = 14 patients (threshold: >= 3 studies AND >= 20 patients) |
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
| clinical_success | 78.2% | 73.6% | -4.6 | 25 |
| safety | 19.0% | 17.6% | -1.3 | 7 |
| eradication | 50.4% | 50.5% | +0.1 | 6 |
| mortality | 9.5% | 10.9% | +1.5 | 10 |

### 4.1b De-duplication sensitivity (Pirnay-roster matches restored)

| Outcome | De-dup applied | Restored | Delta (pp) |
|---|---|---|---|
| clinical_success | 78.2% (N=78) | 78.7% (N=80) | +0.5 |
| safety | 19.0% (N=58) | 18.3% (N=60) | -0.6 |
| eradication | 50.4% (N=66) | 50.4% (N=68) | -0.0 |
| mortality | 9.5% (N=74) | 10.5% (N=76) | +1.1 |

### 4.2 Transformation / model sensitivity

Rows: 52. Full comparison is in `paper/tables/.../meta_sensitivity.tex`.

### 4.2b Does the Hartung-Knapp adjustment bind?

Ratio of the model's reported SE to the naive complete-pooling binomial SE
on the logit scale. A ratio of 1 means the interval is a plain t-interval
on the pooled counts, with no variance inflation and no random-effect term.

| Cell | method.random.ci | df | tau2 | model SE | naive binomial SE | ratio |
|---|---|---|---|---|---|---|
| clinical_success__overall | HK | 34 | 0.000 | 0.2743 | 0.2743 | 1.0000 |
| safety__overall | HK | 27 | 0.000 | 0.3349 | 0.3349 | 1.0000 |
| eradication__overall | HK | 29 | 1.996 | 0.4556 | 0.2463 | 1.8498 |
| mortality__overall | HK | 36 | 0.000 | 0.3972 | 0.3972 | 1.0000 |
| clinical_success__resistance_class__MDR | HK | 16 | 0.000 | 0.3667 | 0.3667 | 1.0000 |
| clinical_success__resistance_class__not-classifiable | HK | 10 | 0.000 | 0.6155 | 0.6155 | 1.0000 |
| safety__resistance_class__MDR | HK | 13 | 0.000 | 0.4198 | 0.4198 | 1.0000 |
| eradication__resistance_class__MDR | HK | 15 | 6.552 | 0.9417 | 0.3015 | 3.1232 |
| mortality__resistance_class__MDR | HK | 18 | 0.000 | 0.5963 | 0.5963 | 1.0000 |
| clinical_success__route_group__other | HK | 13 | 0.000 | 0.3249 | 0.3249 | 1.0000 |
| safety__route_group__other | HK | 10 | 0.000 | 0.4428 | 0.4428 | 1.0000 |
| eradication__route_group__other | HK | 12 | 0.000 | 0.3144 | 0.3144 | 1.0000 |
| mortality__route_group__other | HK | 12 | 0.000 | 0.4765 | 0.4765 | 1.0000 |

Cells where the ratio is exactly 1 (adjustment does not bind): 11 of 13.

### 4.3 Cluster-robust variance check

NOTE: fitted on an AUXILIARY normal-normal model, not the reported GLMM.

| Cell | Clusters (m) | Satterthwaite df | Naive SE | RVE SE |
|---|---|---|---|---|
| clinical_success__overall | 29 | 7.6 | 0.226 | 0.144 |
| safety__overall | 22 | 6.4 | 0.261 | 0.221 |
| eradication__overall | 25 | 5.0 | 0.238 | 0.254 |
| mortality__overall | 30 | 13.0 | 0.245 | 0.174 |
| clinical_success__resistance_class__MDR | 16 | 4.2 | 0.303 | 0.131 |
| clinical_success__resistance_class__not-classifiable | 9 | 5.2 | 0.427 | 0.314 |
| safety__resistance_class__MDR | 13 | 4.8 | 0.347 | 0.317 |
| eradication__resistance_class__MDR | 15 | 3.6 | 0.299 | 0.264 |
| mortality__resistance_class__MDR | 18 | 11.3 | 0.339 | 0.270 |
| clinical_success__route_group__other | 11 | 2.7 | 0.292 | 0.183 |
| safety__route_group__other | 8 | 2.1 | 0.350 | 0.101 |
| eradication__route_group__other | 10 | 2.0 | 0.299 | 0.244 |
| mortality__route_group__other | 10 | 3.2 | 0.367 | 0.312 |

### 4.4 Geographic-concentration exclusion (Belgium/Israel removed)

```
           outcome k_studies_full n_patients_full status_full p_hat_full
1 clinical_success             29              78      POOLED 0.78205128
2           safety             22              58      POOLED 0.18965517
3      eradication             25              66      POOLED 0.50448960
4        mortality             30              74      POOLED 0.09459459
  k_studies_excl n_patients_excl status_excl   p_hat_excl
1             27              31      POOLED 8.064516e-01
2             21              26      POOLED 1.923077e-01
3             24              34      POOLED 5.224332e-01
4             29              42      POOLED 1.723150e-17
```

## 5. Falsification / small-study checks

| Cell | k studies | Eligible (k >= 10) | Peters p |
|---|---|---|---|
| clinical_success__overall | 29 | TRUE | 0.664 |
| safety__overall | 22 | TRUE | 0.176 |
| eradication__overall | 25 | TRUE | 0.816 |
| mortality__overall | 30 | TRUE | n/a |
| clinical_success__resistance_class__MDR | 16 | TRUE | n/a |
| clinical_success__resistance_class__not-classifiable | 9 | FALSE | n/a |
| safety__resistance_class__MDR | 13 | TRUE | n/a |
| eradication__resistance_class__MDR | 15 | TRUE | n/a |
| mortality__resistance_class__MDR | 18 | TRUE | n/a |
| clinical_success__route_group__other | 11 | TRUE | 0.664 |
| safety__route_group__other | 8 | FALSE | n/a |
| eradication__route_group__other | 10 | TRUE | 0.816 |
| mortality__route_group__other | 10 | TRUE | n/a |

Cells eligible for Peters' test: 11 of 13. Cells returning a finite p-value: 5.

| Quantity | Value |
|---|---|
| Publication-year trend, status | FITTED |
| Publication-year trend, coefficient (logit per year) | 0.0585 |
| Publication-year trend, standard error | 0.1064 |
| Publication-year trend, p-value | 0.583 |

## 6. Test-power diagnostics

Peters' regressor is 1/n. Arms with n = 1: 31 of 38 (82%), for which the regressor equals exactly 1. Distinct values of 1/n across the corpus: 5.

## 7. Subgroup tests and remaining reported scalars

| Quantity | Value |
|---|---|
| Study-design subgroup, Q-between p | 0.262 |
| Route 2-category subgroup, Q-between p | 0.704 |
| Journal tier high-tier, crude clinical success | 0.800 (k = 9) |
| Journal tier mid-tier, crude clinical success | 0.739 (k = 20) |

NOTE ON SEARCH YIELDS. Database hit counts (PubMed topical, Scopus native,
ClinicalTrials.gov, the supplementary PDF corpus) are recorded in the PRISMA
figure and Methods narrative, not here: they are screening-log quantities
rather than analysis outputs, and this manifest covers what the pipeline
computes. They must still reconcile against the PRISMA figure.

