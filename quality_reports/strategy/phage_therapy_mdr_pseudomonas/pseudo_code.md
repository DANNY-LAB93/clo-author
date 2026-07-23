# Pseudo-Code: Phage Therapy MDR/XDR *Pseudomonas aeruginosa* Meta-Analysis of Proportions

**Companion to:** `quality_reports/strategy_memo_phage_therapy_mdr_pseudomonas.md`
**Purpose:** Specification-level pseudo-code precise enough for the coder to implement without ambiguity, per `strategize` skill requirements.

---

## 1. Data Structure (input to all models)

One row per study-arm (not per study). Required columns per `strategy_memo` §2.2:

```
study_id, arm_id, n_arm, pathogen_scope, resistance_class, resistance_class_source,
route, modality, clinical_success_n, clinical_success_definition, adverse_event_n,
microbio_eradication_n, mortality_n, los_days, resistance_emergence_n, study_design,
data_provenance, rob_source, publication_year, journal_tier, geographic_source
```

Exclusion filter applied before any pooling: `pathogen_scope != "mixed-not-separable"`.

## 2. Primary Model — Per Stratum-Outcome Cell

```r
library(meta)
library(metafor)
library(clubSandwich)
library(dplyr)

MIN_STUDIES <- 3
MIN_PATIENTS <- 20

pool_stratum <- function(df, event_col, n_col, stratum_label) {

  k <- nrow(df)
  N <- sum(df[[n_col]])

  if (k < MIN_STUDIES || N < MIN_PATIENTS) {
    return(list(
      status = "NOT_POOLED",
      reason = sprintf("k=%d studies, N=%d patients (< %d studies or < %d patients threshold)",
                        k, N, MIN_STUDIES, MIN_PATIENTS),
      narrative_table = df %>% select(study_id, arm_id, !!n_col, !!event_col)
    ))
  }

  # --- Primary: GLMM binomial-normal, logit link ---
  # CONVERGENCE CONTINGENCY (strategist-critic MAJOR #1): binomial-normal GLMM via numerical
  # quadrature/integration is prone to non-convergence in the sparse/boundary-proportion regime
  # this corpus will produce — many n=1 case reports (0 or 1 events) and strata with all-0% or
  # all-100% arms. Wrap the GLMM call so warnings/errors are captured rather than silently
  # producing an unreliable point estimate, and record a per-cell convergence flag.
  glmm_warnings <- character(0)
  m_glmm <- withCallingHandlers(
    tryCatch(
      metaprop(
        event = df[[event_col]], n = df[[n_col]], studlab = df$arm_id, data = df,
        sm = "PLOGIT", method = "GLMM", method.tau = "ML", hakn = TRUE
      ),
      error = function(e) {
        glmm_warnings <<- c(glmm_warnings, paste("ERROR:", conditionMessage(e)))
        NULL
      }
    ),
    warning = function(w) {
      glmm_warnings <<- c(glmm_warnings, paste("WARNING:", conditionMessage(w)))
      invokeRestart("muffleWarning")
    }
  )

  # Convergence diagnostic (per stratum-outcome cell): flag non-convergence via (a) a caught
  # error / NULL model, (b) known rma.glmm()-family warning strings (e.g., "did not converge",
  # "Fisher scoring algorithm did not converge", "NA/NaN function evaluation", "system is
  # computationally singular"), or (c) a returned model with non-finite pooled estimate/SE.
  convergence_flag <- if (is.null(m_glmm)) {
    "FAILED_ERROR"
  } else if (any(grepl("converge|NA/NaN|singular", glmm_warnings, ignore.case = TRUE))) {
    "FAILED_WARNING"
  } else if (!is.finite(m_glmm$TE.random) || !is.finite(m_glmm$seTE.random)) {
    "FAILED_NONFINITE"
  } else {
    "CONVERGED"
  }

  # --- Sensitivity 1: Freeman-Tukey double arcsine, DerSimonian-Laird ---
  m_ft <- metaprop(
    event = df[[event_col]], n = df[[n_col]], studlab = df$arm_id, data = df,
    sm = "PFT", method = "Inverse", method.tau = "DL", hakn = TRUE
  )

  # --- Sensitivity 2: simple logit, DerSimonian-Laird ---
  m_logit_dl <- metaprop(
    event = df[[event_col]], n = df[[n_col]], studlab = df$arm_id, data = df,
    sm = "PLOGIT", method = "Inverse", method.tau = "DL", hakn = TRUE
  )

  # --- Fixed-effect sensitivity ---
  m_fe <- metaprop(
    event = df[[event_col]], n = df[[n_col]], studlab = df$arm_id, data = df,
    sm = "PLOGIT", method = "Inverse", common = TRUE, random = FALSE
  )

  # --- PRE-SPECIFIED FALLBACK ESTIMATOR (strategist-critic MAJOR #1) ---
  # If GLMM fails to converge for this specific cell, promote the logit-DerSimonian-Laird
  # sensitivity model (m_logit_dl) to serve as the *reported* primary estimate for that cell
  # only. This is a cell-level substitution, not a model-wide change: every other cell that
  # converges still reports GLMM as primary. The substitution is never silent — it is always
  # tagged via `primary_model_used` and must be rendered as a footnote/flag on the output table
  # (see Section 9).
  reported_primary <- if (convergence_flag == "CONVERGED") m_glmm else m_logit_dl
  primary_model_used <- if (convergence_flag == "CONVERGED") {
    "GLMM (binomial-normal, logit link)"
  } else {
    sprintf("FALLBACK: logit-DerSimonian-Laird (GLMM failed to converge for this cell: %s)",
            convergence_flag)
  }

  # --- RVE clustering correction if any study contributes >1 arm to this cell ---
  multi_arm_studies <- df %>% count(study_id) %>% filter(n > 1) %>% pull(study_id)
  rve_note <- if (length(multi_arm_studies) > 0) {
    "Applied clubSandwich::coef_test() with cluster = study_id; report alongside naive CI."
  } else {
    "No multi-arm studies in this cell; naive independence assumption holds by construction."
  }

  list(
    status = "POOLED",
    stratum = stratum_label, k = k, N = N,
    primary = reported_primary,
    primary_model_used = primary_model_used,     # feeds the mandatory table footnote (Section 9)
    convergence_flag = convergence_flag,          # CONVERGED / FAILED_ERROR / FAILED_WARNING / FAILED_NONFINITE
    convergence_diagnostics = glmm_warnings,      # raw captured warning/error strings, kept for audit
    glmm_raw = m_glmm,                            # retained even on failure (may be NULL) for transparency
    sens_ft = m_ft, sens_logit_dl = m_logit_dl, sens_fe = m_fe,
    rve_note = rve_note
  )
}
```

**Reporting rule tied to this contingency:** every stratum-outcome cell's convergence status is logged, not just the cells that fail — this makes "GLMM converged cleanly across all cells" itself a verifiable, citable claim rather than an unstated assumption. Cells with `convergence_flag != "CONVERGED"` must appear in the manuscript's results table with the fallback model explicitly named (never presented indistinguishably from a converged GLMM cell).

## 3. Iterate Over the Three Pre-Specified Strata

```r
outcomes <- c("clinical_success_n", "adverse_event_n", "microbio_eradication_n", "mortality_n")

strata_defs <- list(
  resistance = c("MDR", "XDR", "not-classifiable"),
  route      = c("topical/local", "IV", "inhaled/nebulized", "oral", "intra-articular", "other"),
  modality   = c("phage monotherapy", "phage+antibiotic combination", "antibiotic monotherapy")
)

results <- list()
for (outcome in outcomes) {
  for (stratum_var in names(strata_defs)) {
    for (level in strata_defs[[stratum_var]]) {
      df_sub <- dat_all %>% filter(.data[[stratum_var]] == level)
      key <- paste(outcome, stratum_var, level, sep = "__")
      results[[key]] <- pool_stratum(
        df_sub,
        event_col = outcome,
        n_col = "n_arm",
        stratum_label = key
      )
    }
  }
}

# Convergence audit summary (feeds Section 9's mandatory reporting requirement):
convergence_summary <- purrr::map_dfr(results, function(r) {
  if (r$status != "POOLED") return(NULL)
  tibble::tibble(stratum = r$stratum, convergence_flag = r$convergence_flag,
                 primary_model_used = r$primary_model_used)
})
# Any row where convergence_flag != "CONVERGED" must be flagged in the results table (Section 9).
```

## 4. Between-Subgroup Moderator Test (Subgroup Meta-Analysis, NOT Meta-Regression on a Paired Effect)

```r
# Example: does clinical success differ MDR vs XDR vs not-classifiable?
m_subgroup_test <- metaprop(
  event = dat_all$clinical_success_n, n = dat_all$n_arm,
  studlab = dat_all$arm_id, data = dat_all,
  sm = "PLOGIT", method = "GLMM", hakn = TRUE,
  subgroup = dat_all$resistance_class
)
# Extract: m_subgroup_test$pval.Q.b.random  (Cochran's Q-between test, random-effects)
```

## 5. Secondary/Contextual Pooled-All Estimate

```r
m_pooled_all_success <- metaprop(
  event = dat_all$clinical_success_n, n = dat_all$n_arm,
  studlab = dat_all$arm_id, data = dat_all,
  sm = "PLOGIT", method = "GLMM", method.tau = "ML", hakn = TRUE
)
# Label explicitly in output/tables as "secondary/contextual, not primary" per strategy_memo §1
```

## 6. Exploratory Paired Comparisons (Krakhotkin, Leitner, PhagoBurn — Labeled Exploratory Only)

```r
# Only for studies with a genuine within-study phage vs. antibiotic-monotherapy comparator,
# pending full-text Pseudomonas-subgroup confirmation. NEVER blended into primary strata.
exploratory_rr <- metabin(
  event.e = phage_arm_events, n.e = phage_arm_n,
  event.c = antibiotic_arm_events, n.c = antibiotic_arm_n,
  studlab = study_id, data = exploratory_comparative_studies,
  sm = "RR", method = "MH", random = TRUE
)
```

## 7. Falsification / Negative-Control Checks (Section 6 of memo)

```r
# 1. Publication-year trend (meta-regression moderator on transformed scale)
m_year_trend <- metareg(m_pooled_all_success, ~ publication_year)

# 2. Journal-tier gradient
m_tier_test <- metaprop(
  event = dat_all$clinical_success_n, n = dat_all$n_arm,
  studlab = dat_all$arm_id, data = dat_all,
  sm = "PLOGIT", method = "GLMM", hakn = TRUE,
  subgroup = dat_all$journal_tier
)

# 3. Funnel/small-study eyeball check (alongside formal Egger's/Peters' test, §Priority 5 #11)
funnel(m_pooled_all_success)

# 4. Route x resistance_class x geographic_source cross-tab (confounding transparency)
table(dat_all$route, dat_all$resistance_class, dat_all$geographic_source)

# 5. LOS vs. clinical-success movement comparison
pool_stratum(dat_all, event_col = "los_improved_n", n_col = "n_arm", stratum_label = "LOS_check")
# compare effect-size direction/magnitude qualitatively against clinical_success pooled estimate

# 6. AE-rate-by-year drift check
m_ae_year_trend <- metareg(
  pool_stratum(dat_all, "adverse_event_n", "n_arm", "AE_all")$primary,
  ~ publication_year
)
```

## 8. Publication Bias (Priority 5, #11 in Robustness Plan)

```r
if (nrow(df_sub) >= 10) {
  eggers_test <- metabias(m_glmm, method.bias = "Egger")  # or "Peters" (proportion-adapted)
} else {
  # Do not run; state explicitly in output: "Fewer than 10 studies in this cell — publication
  # bias assessment not performed, per pre-specified threshold."
}
```

## 9. Output Table Requirements (INV-1, INV-11 compliance)

Every pooled-estimate table exported by the coder must include, per cell: k (studies), N (patients),
point estimate, 95% CI (HKSJ-adjusted where k<10), I², τ², prediction interval, model used (GLMM
primary + which sensitivity models agree/disagree), and `NOT_POOLED` cells explicitly listed with
their reason string — never silently omitted from the table.

**Convergence-contingency reporting (strategist-critic MAJOR #1):** in addition to the above, every
`POOLED` cell's table row must include the `convergence_flag` and `primary_model_used` fields from
`pool_stratum()`. Any cell where `convergence_flag != "CONVERGED"` must carry a visible table
footnote (e.g., a dagger symbol keyed to a `tablenotes` entry per INV-1) stating: "GLMM failed to
converge for this cell ([diagnostic string]); reported estimate is the pre-specified logit-DL
fallback, not GLMM." This ensures a fallback estimate is never visually indistinguishable from a
converged GLMM estimate in the manuscript.
