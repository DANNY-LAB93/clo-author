# ==============================================================================
# 08_tables.R
# Purpose: Publication-ready summary tables. Exports bare `tabular`
#          environments only (no \begin{table}, \caption{}, or notes --
#          INV-13; main.tex wraps these with threeparttable + tablenotes).
#          Table 1: pooled stratum-outcome cells with k, N, pooled
#          proportion + 95% CI, I^2, tau^2, prediction interval, and model
#          used (dagger marker on fallback cells, per pseudo_code.md S9 --
#          footnote TEXT belongs in main.tex, the marker itself is
#          legitimate bare-tabular content).
#          Table 2: NOT_POOLED / NOT_ATTEMPTED cells with the stated reason.
#          Table 3: transformation/model sensitivity comparison.
#          Table 4 (appendix-only): minimum-study-count threshold
#          relaxation (Priority 5 #12, robustness_plan.md) -- clearly
#          labeled below the pre-specified pooling bar, never promoted to
#          primary results.
#
#          All `%`-bearing cell values (I^2, prediction interval, NOT_POOLED
#          reason strings) are routed through escape_tex() before being
#          written -- an earlier version wrote the I^2 column unescaped,
#          which opened a LaTeX comment mid-row and truncated every row in
#          the primary results table (coder-critic review, fixed here).
# Project: phage_therapy_mdr_pseudomonas
# Inputs:  scripts/R/output/pooled_results.rds
#          scripts/R/output/modality_skip_note.rds
#          scripts/R/output/transformation_sensitivity.rds
#          scripts/R/output/threshold_relaxation_appendix.rds
# Outputs: paper/tables/phage_therapy_mdr_pseudomonas/meta_pooled_estimates.tex
#          paper/tables/phage_therapy_mdr_pseudomonas/meta_not_pooled.tex
#          paper/tables/phage_therapy_mdr_pseudomonas/meta_sensitivity.tex
#          paper/tables/phage_therapy_mdr_pseudomonas/meta_threshold_relaxation_appendix.tex
# Requires: 01_setup.R, 04_estimation.R, 05_robustness.R have been run
# ==============================================================================

pooled_results             <- readRDS(file.path(output_dir, "pooled_results.rds"))
modality_skip_note         <- readRDS(file.path(output_dir, "modality_skip_note.rds"))
transformation_sensitivity <- readRDS(file.path(output_dir, "transformation_sensitivity.rds"))
threshold_relaxation_appendix <- readRDS(file.path(output_dir, "threshold_relaxation_appendix.rds"))

# --- Human-readable stratum labels -----------------------------------------------
label_stratum <- function(key) {
  key <- gsub("clinical_success", "Clinical success", key, fixed = TRUE)
  key <- gsub("safety", "Safety (>=1 AE)", key, fixed = TRUE)
  key <- gsub("eradication", "Eradication", key, fixed = TRUE)
  key <- gsub("mortality", "Mortality", key, fixed = TRUE)
  # "(secondary/contextual)" dropped from the label itself (2026-07-22, table
  # width fix) -- this qualifier is already stated once in the table note
  # ("'Overall' rows are secondary/contextual...") and repeating it in every
  # "Overall" row's stratum label was a meaningful contributor to
  # meta_pooled_estimates.tex overflowing the page width.
  key <- gsub("__overall", " -- Overall", key, fixed = TRUE)
  key <- gsub("__resistance_class__", " -- Resistance: ", key, fixed = TRUE)
  # "not-classifiable" -> "NC", matching the abbreviation already used in
  # Table 1 (09_table1_characteristics.R) -- also trims real width from
  # meta_pooled_estimates.tex, which overflowed the page at the full spelling
  # once this stratum started appearing as a POOLED (not just NOT_POOLED) row.
  key <- gsub("not-classifiable", "NC", key, fixed = TRUE)
  key <- gsub("__route_group__", " -- Route: ", key, fixed = TRUE)
  key
}

#' Escape LaTeX-special characters in generated table cell text
#'
#' Applied to every cell that is free text or contains a literal `%`
#' (I^2, prediction-interval strings, NOT_POOLED reason strings). Never
#' applied to hand-authored LaTeX markup cells (e.g. the `$^\dagger$`
#' convergence-fallback marker), which must pass through unescaped.
#'
#' @param x Character vector.
#' @return Character vector with `%` and `_` escaped for LaTeX.
escape_tex <- function(x) {
  x <- gsub("%", "\\\\%", x)
  x <- gsub("_", "\\\\_", x)
  x
}

# --- Table 1: Pooled estimates ---------------------------------------------------
pooled_cells <- pooled_results[
  vapply(pooled_results, \(r) r$status == "POOLED", logical(1L))
]

pooled_rows <- purrr::map_dfr(pooled_cells, function(r) {
  p_hat   <- backtransform_prop(r$primary$TE.random, sm = r$primary$sm)
  ci_low  <- backtransform_prop(r$primary$lower.random, sm = r$primary$sm)
  ci_high <- backtransform_prop(r$primary$upper.random, sm = r$primary$sm)

  # Prediction interval (pseudo_code.md S9 mandatory column). Only defined
  # when the model has enough cells to compute one (k >= 3, already
  # guaranteed by MIN_STUDIES); guarded regardless in case a future relaxed
  # threshold run feeds a k = 2 cell through this same table builder.
  has_pi <- !is.null(r$primary$lower.predict) && !is.null(r$primary$upper.predict) &&
    is.finite(r$primary$lower.predict) && is.finite(r$primary$upper.predict)
  pi_low  <- if (has_pi) backtransform_prop(r$primary$lower.predict, sm = r$primary$sm) else NA_real_
  pi_high <- if (has_pi) backtransform_prop(r$primary$upper.predict, sm = r$primary$sm) else NA_real_

  tibble::tibble(
    stratum = label_stratum(r$stratum),
    k_studies = r$k_studies,
    n_patients = r$n_patients,
    estimate = format_percent_ci(p_hat, ci_low, ci_high),
    # I^2 deliberately NOT reported: for a binomial-normal GLMM, meta::metaprop's
    # $I2 slot derives from the GLMM conditional Q (which is ~0 by construction),
    # giving a degenerate I^2 = 0% even for cells with large tau^2 -- an
    # internally contradictory pairing. I^2 is in any case documented as
    # unreliable for meta-analyses of proportions (Migliavaca et al. 2022). We
    # report tau^2 and the 95% prediction interval, the defensible heterogeneity
    # pair for a proportion GLMM, and omit I^2 entirely.
    tau2 = sprintf("%.3f", r$primary$tau2),
    pred_interval = if (has_pi) {
      sprintf("[%.1f%%, %.1f%%]", 100 * pi_low, 100 * pi_high)
    } else {
      "n/a (k too small)"
    },
    model_marker = if (r$convergence_flag != "CONVERGED") "GLMM$^\\dagger$" else "GLMM"
  )
})

# INV-17: pre-allocate/construct rows via vapply rather than growing a
# vector inside a for loop.
pooled_row_lines <- vapply(seq_len(nrow(pooled_rows)), function(i) {
  sprintf(
    "%s & %d & %d & %s & %s & %s & %s \\\\",
    escape_tex(pooled_rows$stratum[i]), pooled_rows$k_studies[i],
    pooled_rows$n_patients[i], escape_tex(pooled_rows$estimate[i]),
    pooled_rows$tau2[i],
    escape_tex(pooled_rows$pred_interval[i]), pooled_rows$model_marker[i]
  )
}, character(1L))

tex_lines_pooled <- c(
  "\\begin{tabular}{lccccccc}",
  "\\toprule",
  paste(
    "Outcome -- Stratum & Studies ($k$) & Patients ($N$) &",
    "Pooled proportion [95\\% CI] & $\\tau^2$ &",
    "95\\% prediction interval & Model \\\\"
  ),
  "\\midrule",
  pooled_row_lines,
  "\\bottomrule",
  "\\end{tabular}"
)

writeLines(tex_lines_pooled, file.path(table_dir, "meta_pooled_estimates.tex"))
message("Wrote paper/tables/", PROJECT_SLUG, "/meta_pooled_estimates.tex (", nrow(pooled_rows), " rows)")

# --- Table 2: NOT_POOLED / NOT_ATTEMPTED cells ----------------------------------
not_pooled_cells <- pooled_results[
  vapply(pooled_results, \(r) r$status == "NOT_POOLED", logical(1L))
]

not_pooled_rows <- purrr::map_dfr(not_pooled_cells, function(r) {
  # Terse, row-specific reason (which criterion actually failed) rather than
  # repeating the full threshold sentence on every row -- k and N are already
  # shown in their own columns, and the full threshold wording lives once in
  # the table note. The prior repeated-boilerplate version overflowed the
  # page width once the not-pooled row count grew (25 rows after the Pirnay
  # resistance-stratified re-extraction added 3 new NOT_POOLED cells).
  k_fail <- r$k_studies < MIN_STUDIES
  n_fail <- r$n_patients < MIN_PATIENTS
  # A cell can be NOT_POOLED either for failing the k/N gate or for zero-/all-
  # event degeneracy (which passes k/N but is uninformative as a proportion --
  # see pool_stratum()). Detect the latter from its reason string.
  reason <- if (grepl("zero-event", r$reason)) {
    "0 events"
  } else if (grepl("all-event", r$reason)) {
    "all events"
  } else if (k_fail && n_fail) {
    sprintf("$k<%d$, $N<%d$", MIN_STUDIES, MIN_PATIENTS)
  } else if (k_fail) {
    sprintf("$k<%d$", MIN_STUDIES)
  } else {
    sprintf("$N<%d$", MIN_PATIENTS)
  }
  tibble::tibble(
    stratum = label_stratum(r$stratum),
    k_studies = r$k_studies,
    n_patients = r$n_patients,
    reason = reason
  )
})
not_pooled_rows <- dplyr::bind_rows(
  not_pooled_rows,
  tibble::tibble(
    stratum = "Modality: antibiotic monotherapy (all outcomes)",
    k_studies = 0L, n_patients = 0L,
    reason = "0 arms (stratum empty)"
  )
)

not_pooled_row_lines <- vapply(seq_len(nrow(not_pooled_rows)), function(i) {
  sprintf(
    "%s & %d & %d & %s \\\\",
    escape_tex(not_pooled_rows$stratum[i]), not_pooled_rows$k_studies[i],
    not_pooled_rows$n_patients[i], escape_tex(not_pooled_rows$reason[i])
  )
}, character(1L))

tex_lines_not_pooled <- c(
  "\\begin{tabular}{lccl}",
  "\\toprule",
  "Outcome -- Stratum & Studies ($k$) & Patients ($N$) & Reason not pooled \\\\",
  "\\midrule",
  not_pooled_row_lines,
  "\\bottomrule",
  "\\end{tabular}"
)

writeLines(tex_lines_not_pooled, file.path(table_dir, "meta_not_pooled.tex"))
message("Wrote paper/tables/", PROJECT_SLUG, "/meta_not_pooled.tex (", nrow(not_pooled_rows), " rows)")

# --- Table 3: Transformation/model sensitivity comparison -----------------------
sens_rows <- transformation_sensitivity |>
  mutate(estimate = format_percent_ci(p_hat, ci_low, ci_high)) |>
  select(stratum, model, estimate)

sens_row_lines <- vapply(seq_len(nrow(sens_rows)), function(i) {
  sprintf(
    "%s & %s & %s \\\\",
    escape_tex(label_stratum(sens_rows$stratum[i])),
    escape_tex(sens_rows$model[i]), escape_tex(sens_rows$estimate[i])
  )
}, character(1L))

tex_lines_sens <- c(
  "\\begin{tabular}{llc}",
  "\\toprule",
  "Stratum & Model & Pooled proportion [95\\% CI] \\\\",
  "\\midrule",
  sens_row_lines,
  "\\bottomrule",
  "\\end{tabular}"
)

writeLines(tex_lines_sens, file.path(table_dir, "meta_sensitivity.tex"))
message("Wrote paper/tables/", PROJECT_SLUG, "/meta_sensitivity.tex (", nrow(sens_rows), " rows)")

# --- Table 4 (appendix-only): threshold relaxation ------------------------------
# Priority 5 #12 (robustness_plan.md): minimum-study-count threshold
# relaxed to k >= 2 studies / N >= 10 patients. Reported here as a clearly
# labeled APPENDIX table -- never merged into Table 1, never treated as a
# primary result, per the pre-specified plan.
relax_rows <- threshold_relaxation_appendix |>
  mutate(
    stratum_label = label_stratum(stratum),
    flag = ifelse(newly_poolable, "NEW (relaxed)", "")
  )

relax_row_lines <- vapply(seq_len(nrow(relax_rows)), function(i) {
  sprintf(
    "%s & %s & %s & %d & %d & %s \\\\",
    escape_tex(relax_rows$stratum_label[i]),
    escape_tex(relax_rows$status_primary[i]),
    escape_tex(relax_rows$status_relaxed[i]),
    relax_rows$k_studies[i], relax_rows$n_patients[i],
    escape_tex(relax_rows$flag[i])
  )
}, character(1L))

tex_lines_relax <- c(
  "\\begin{tabular}{lllccl}",
  "\\toprule",
  paste(
    "Outcome -- Stratum & Primary$^a$ &",
    "Relaxed$^b$ & $k$ (relaxed) & $N$ (relaxed) & Flag \\\\"
  ),
  "\\midrule",
  relax_row_lines,
  "\\bottomrule",
  "\\end{tabular}"
)

writeLines(tex_lines_relax, file.path(table_dir, "meta_threshold_relaxation_appendix.tex"))
message(
  "Wrote paper/tables/", PROJECT_SLUG, "/meta_threshold_relaxation_appendix.tex (",
  nrow(relax_rows), " rows; appendix-only, not a primary result)"
)

message("08_tables.R complete.")
