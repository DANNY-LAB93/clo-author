# ==============================================================================
# 10_grade.R
# Purpose: GRADE certainty-of-evidence assessment for every POOLED
#          outcome-stratum cell, per the peer-review panel's requirement
#          (both referees, 2026-07-23) that GRADE ratings be assigned rather
#          than merely anticipated.
#
#          Ratings are produced by PRE-SPECIFIED, DATA-DRIVEN RULES applied
#          uniformly to every cell, not by per-cell hand judgment, so the
#          assessment is reproducible and auditable. Each rule and its
#          rationale is documented inline below.
#
# Project: phage_therapy_mdr_pseudomonas
# Inputs:  scripts/R/output/pooled_results.rds
#          scripts/R/output/dat_analysis.rds
# Outputs: scripts/R/output/grade_profile.rds
#          paper/tables/phage_therapy_mdr_pseudomonas/grade_summary.tex
# Requires: 01_setup.R, 02_data_preparation.R, 04_estimation.R have been run
# ==============================================================================

pooled_results <- readRDS(file.path(output_dir, "pooled_results.rds"))
dat_analysis   <- readRDS(file.path(output_dir, "dat_analysis.rds"))

pooled_cells <- pooled_results[
  vapply(pooled_results, \(r) r$status == "POOLED", logical(1L))
]

# Local copies of the two table-formatting helpers, so this script is
# self-contained and does not depend on 08_tables.R having been sourced into
# the same environment first (the same convention 09_table1_characteristics.R
# follows for escape_tex).
label_stratum <- function(key) {
  key <- gsub("clinical_success", "Clinical success", key, fixed = TRUE)
  key <- gsub("safety", "Safety (>=1 AE)", key, fixed = TRUE)
  key <- gsub("eradication", "Eradication", key, fixed = TRUE)
  key <- gsub("mortality", "Mortality", key, fixed = TRUE)
  key <- gsub("__overall", " -- Overall", key, fixed = TRUE)
  key <- gsub("__resistance_class__", " -- Resistance: ", key, fixed = TRUE)
  key <- gsub("not-classifiable", "NC", key, fixed = TRUE)
  key <- gsub("__route_group__", " -- Route: ", key, fixed = TRUE)
  key
}

escape_tex <- function(x) {
  x <- gsub("%", "\\\\%", x)
  x <- gsub("_", "\\\\_", x)
  x
}

# --- Starting certainty --------------------------------------------------------
# GRADE starts randomized evidence at High and observational evidence at Low.
# Every pooled cell here is an uncontrolled single-arm proportion drawn
# predominantly from compassionate-use case reports and case series (the
# randomized trials contribute only their phage arms, stripped of their
# comparators), so the body of evidence for every cell starts at LOW.
START_CERTAINTY <- 2L  # 4 = High, 3 = Moderate, 2 = Low, 1 = Very low
CERTAINTY_LABEL <- c("Very low", "Low", "Moderate", "High")

# The study whose RoB2 assessment returned High risk (unmasked clinicians +
# stopped early for futility); its presence in a cell is a risk-of-bias flag.
HIGH_ROB_STUDY <- "Jault2019_PhagoBurn"

#' Reconstruct the arms contributing to a pooled cell.
#' Mirrors the subsetting logic in 04_estimation.R / 05_robustness.R exactly
#' (including the !is.na() guards) so the GRADE denominator matches the
#' denominator the estimate was actually computed from.
cell_arms <- function(key) {
  parts <- strsplit(key, "__")[[1]]
  event_col <- OUTCOME_COLS[[parts[1]]]
  if (length(parts) == 2L && parts[2] == "overall") {
    dat_analysis[!is.na(dat_analysis[[event_col]]), ]
  } else {
    strat_var <- parts[2]
    strat_level <- paste(parts[-c(1, 2)], collapse = "__")
    dat_analysis[
      !is.na(dat_analysis[[event_col]]) &
        !is.na(dat_analysis[[strat_var]]) &
        dat_analysis[[strat_var]] == strat_level,
    ]
  }
}

grade_profile <- purrr::map_dfr(pooled_cells, function(r) {
  key <- r$stratum
  outcome <- strsplit(key, "__")[[1]][1]
  df <- cell_arms(key)

  n_total <- sum(df$n_arm, na.rm = TRUE)
  n_case_report <- sum(df$n_arm[df$study_design == "case report"], na.rm = TRUE)
  case_report_share <- if (n_total > 0) n_case_report / n_total else NA_real_
  has_high_rob <- HIGH_ROB_STUDY %in% df$study_id

  # Back-transformed estimate, CI and prediction interval, on the % scale.
  p_hat  <- backtransform_prop(r$primary$TE.random, sm = r$primary$sm) * 100
  ci_lo  <- backtransform_prop(r$primary$lower.random, sm = r$primary$sm) * 100
  ci_hi  <- backtransform_prop(r$primary$upper.random, sm = r$primary$sm) * 100
  ci_width <- ci_hi - ci_lo

  has_pi <- !is.null(r$primary$lower.predict) && is.finite(r$primary$lower.predict) &&
    !is.null(r$primary$upper.predict) && is.finite(r$primary$upper.predict)
  pi_width <- if (has_pi) {
    (backtransform_prop(r$primary$upper.predict, sm = r$primary$sm) -
       backtransform_prop(r$primary$lower.predict, sm = r$primary$sm)) * 100
  } else {
    NA_real_
  }

  # --- Domain 1: Risk of bias --------------------------------------------------
  # Every cell rests on uncontrolled data, so no cell is free of serious RoB.
  # A cell is downgraded TWICE where the majority of its patients come from
  # single-patient case reports (the design least able to exclude selective
  # reporting and co-intervention effects) AND a High-risk-of-bias trial also
  # contributes.
  rob_drop <- if (!is.na(case_report_share) && case_report_share > 0.5 && has_high_rob) {
    2L
  } else {
    1L
  }
  rob_reason <- sprintf(
    "%s; %.0f%% of patients from single-patient case reports%s",
    if (rob_drop == 2L) "Very serious" else "Serious",
    100 * case_report_share,
    if (has_high_rob) "; includes a High-risk-of-bias trial (PhagoBurn)" else ""
  )

  # --- Domain 2: Inconsistency -------------------------------------------------
  # I^2 is not used: for a binomial-normal GLMM meta's I^2 is degenerate, and
  # I^2 is unreliable for proportions (Migliavaca et al. 2022). Between-study
  # heterogeneity is judged from the width of the 95% prediction interval,
  # which is the quantity that tells a reader how much the true proportion
  # varies across settings.
  incons_drop <- if (is.na(pi_width)) {
    1L
  } else if (pi_width >= 80) {
    2L
  } else if (pi_width >= 50) {
    1L
  } else {
    0L
  }
  incons_reason <- if (incons_drop == 0L) {
    sprintf("Not serious; prediction interval spans %.0f percentage points", pi_width)
  } else {
    sprintf(
      "%s; prediction interval spans %.0f percentage points (tau-squared = %.2f)",
      if (incons_drop == 2L) "Very serious" else "Serious", pi_width, r$primary$tau2
    )
  }

  # --- Domain 3: Indirectness --------------------------------------------------
  # Common to every cell: the population is a referral-selected, compassionate-use
  # salvage population treated after antibiotic failure, which is indirect to the
  # general MDR/XDR/PDR P. aeruginosa patient a clinician faces. Clinical success
  # is downgraded a second level because it is not a harmonized construct: each
  # study defines it on its own terms, across non-comparable infection syndromes
  # (biliary, cystic-fibrosis lung, prosthetic joint, vascular graft, urinary
  # tract, bacteremia, osteomyelitis). Eradication, safety and mortality are
  # comparatively objective and take the single population-level downgrade.
  indirect_drop <- if (outcome == "clinical_success") 2L else 1L
  indirect_reason <- if (indirect_drop == 2L) {
    "Very serious; compassionate-use salvage population, and success is defined per study across non-comparable syndromes"
  } else {
    "Serious; compassionate-use salvage population, indirect to the general MDR/XDR/PDR patient"
  }

  # --- Domain 4: Imprecision ---------------------------------------------------
  # Judged on the width of the 95% CI around the pooled proportion. A cell whose
  # CI spans half the parameter space or more cannot support a clinical decision.
  imprec_drop <- if (ci_width >= 50) 2L else if (ci_width >= 30) 1L else 0L
  imprec_reason <- sprintf(
    "%s; 95%% CI spans %.0f percentage points (%d patients)",
    if (imprec_drop == 2L) "Very serious" else if (imprec_drop == 1L) "Serious" else "Not serious",
    ci_width, n_total
  )

  # --- Domain 5: Publication bias ----------------------------------------------
  # Peters' test (the appropriate small-study test for proportions) was
  # non-significant for every eligible cell, but that is weak reassurance in a
  # corpus this small and this dominated by single-patient reports: a
  # compassionate-use case report describing a failure is markedly less likely
  # to be written and published than one describing a success. Every cell is
  # therefore downgraded once for strongly suspected publication bias, which we
  # cannot exclude by testing.
  pubbias_drop <- 1L
  pubbias_reason <- "Strongly suspected; favourable-outcome reporting bias is intrinsic to a compassionate-use case-report literature, and Peters' test cannot exclude it at this corpus size"

  total_drop <- rob_drop + incons_drop + indirect_drop + imprec_drop + pubbias_drop
  # GRADE has a floor: certainty cannot fall below Very low.
  final <- max(1L, START_CERTAINTY - total_drop)

  tibble::tibble(
    stratum = key,
    outcome = outcome,
    k_studies = r$k_studies,
    n_patients = n_total,
    estimate_pct = p_hat,
    ci_low_pct = ci_lo,
    ci_high_pct = ci_hi,
    case_report_share = case_report_share,
    has_high_rob = has_high_rob,
    rob_drop = rob_drop, rob_reason = rob_reason,
    inconsistency_drop = incons_drop, inconsistency_reason = incons_reason,
    indirectness_drop = indirect_drop, indirectness_reason = indirect_reason,
    imprecision_drop = imprec_drop, imprecision_reason = imprec_reason,
    pubbias_drop = pubbias_drop, pubbias_reason = pubbias_reason,
    total_downgrades = total_drop,
    certainty = CERTAINTY_LABEL[final]
  )
})

saveRDS(grade_profile, file.path(output_dir, "grade_profile.rds"))

message("GRADE certainty ratings (start: Low, observational; floor: Very low):")
for (i in seq_len(nrow(grade_profile))) {
  message(sprintf(
    "  %-52s %-9s (RoB -%d, Incons -%d, Indir -%d, Imprec -%d, PubBias -%d)",
    grade_profile$stratum[i], grade_profile$certainty[i],
    grade_profile$rob_drop[i], grade_profile$inconsistency_drop[i],
    grade_profile$indirectness_drop[i], grade_profile$imprecision_drop[i],
    grade_profile$pubbias_drop[i]
  ))
}
message(
  "Certainty distribution: ",
  paste(sprintf("%s = %d", names(table(grade_profile$certainty)),
                as.integer(table(grade_profile$certainty))), collapse = "; ")
)

# --- Export bare tabular for the manuscript (INV-13) ---------------------------
# Domain columns show how many certainty levels each domain cost: an en-dash
# for "not serious" (no downgrade), else the number of levels deducted. Plain
# text rather than GRADE's circle glyphs, which would require an extra font
# package (wasysym) in the preamble for no informational gain.
domain_mark <- function(drop) {
  if (drop == 0L) "--" else sprintf("$-$%d", drop)
}

grade_rows <- grade_profile |>
  dplyr::mutate(
    stratum_label = label_stratum(stratum),
    # Plain "%" here: escape_tex() below adds the LaTeX backslash. Writing
    # "\\%%" as well would double-escape and render a literal backslash.
    estimate_str = sprintf("%.1f%% [%.1f, %.1f]", estimate_pct, ci_low_pct, ci_high_pct)
  )

grade_row_lines <- vapply(seq_len(nrow(grade_rows)), function(i) {
  sprintf(
    "%s & %d & %d & %s & %s & %s & %s & %s & %s & %s \\\\",
    escape_tex(grade_rows$stratum_label[i]),
    grade_rows$k_studies[i], grade_rows$n_patients[i],
    escape_tex(grade_rows$estimate_str[i]),
    domain_mark(grade_rows$rob_drop[i]),
    domain_mark(grade_rows$inconsistency_drop[i]),
    domain_mark(grade_rows$indirectness_drop[i]),
    domain_mark(grade_rows$imprecision_drop[i]),
    domain_mark(grade_rows$pubbias_drop[i]),
    grade_rows$certainty[i]
  )
}, character(1L))

tex_lines_grade <- c(
  "\\begin{tabular}{lcclccccc l}",
  "\\toprule",
  paste(
    "Outcome -- Stratum & $k$ & $N$ & Pooled proportion [95\\% CI] &",
    "RoB & Incons. & Indir. & Imprec. & Pub.\\ bias & Certainty \\\\"
  ),
  "\\midrule",
  grade_row_lines,
  "\\bottomrule",
  "\\end{tabular}"
)

writeLines(
  tex_lines_grade,
  file.path(table_dir, "grade_summary.tex")
)
message(
  "Wrote paper/tables/", PROJECT_SLUG, "/grade_summary.tex (",
  nrow(grade_rows), " rows)"
)

message("10_grade.R complete.")
