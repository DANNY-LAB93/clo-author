# ==============================================================================
# 04_estimation.R
# Purpose: Main specification -- pool_stratum() run for (a) the overall
#          (unstratified, secondary/contextual per memo S1) proportion for
#          each of the 4 outcome families, (b) the resistance-class
#          (MDR/XDR/PDR/not-classifiable) subgroup for ALL 4 outcome
#          families, and (c) the route_group subgroup for ALL 4 outcome
#          families -- matching pseudo_code.md S3's literal outcome x
#          stratum triple loop (a prior draft of this script narrowed (b)
#          and (c) to clinical_success/safety only; that undisclosed scope
#          restriction was flagged by coder-critic and is corrected here).
#          The modality (monotherapy vs. combination) stratification is
#          explicitly NOT attempted -- logged with a stated reason instead
#          of a forced pooled estimate, per the pre-specified sparsity
#          contingency (strategy memo S5). Many eradication/mortality
#          subgroup cells will be NOT_POOLED given the corpus's small size;
#          this is itself informative (an evidence-base gap, not a
#          meaningless output) and every such cell is reported with its
#          reason string in meta_not_pooled.tex, never silently dropped.
# Project: phage_therapy_mdr_pseudomonas
# Inputs:  scripts/R/output/dat_analysis.rds
# Outputs: scripts/R/output/pooled_results.rds
#          scripts/R/output/modality_skip_note.rds
# Requires: 01_setup.R, 02_data_preparation.R have been run
# ==============================================================================

dat_analysis <- readRDS(file.path(output_dir, "dat_analysis.rds"))

# --- (a) Overall (secondary/contextual) pooled proportion, all 4 outcomes -----
overall_results <- purrr::imap(OUTCOME_COLS, function(col, outcome_name) {
  df_sub <- dat_analysis[!is.na(dat_analysis[[col]]), ]
  pool_stratum(
    df_sub,
    event_col = col, n_col = "n_arm",
    stratum_label = paste0(outcome_name, "__overall"),
    min_studies = MIN_STUDIES, min_patients = MIN_PATIENTS
  )
})
names(overall_results) <- paste0(names(OUTCOME_COLS), "__overall")

# --- (b) Resistance-class subgroup (MDR / XDR / PDR / not-classifiable) ------
# Run for ALL 4 outcome families, per pseudo_code.md S3's literal loop.
resistance_levels <- sort(unique(dat_analysis$resistance_class))

resistance_results <- list()
for (outcome_name in names(OUTCOME_COLS)) {
  col <- OUTCOME_COLS[[outcome_name]]
  for (level in resistance_levels) {
    df_sub <- dat_analysis[
      !is.na(dat_analysis[[col]]) &
        !is.na(dat_analysis$resistance_class) &
        dat_analysis$resistance_class == level,
    ]
    key <- paste(outcome_name, "resistance_class", level, sep = "__")
    resistance_results[[key]] <- pool_stratum(
      df_sub,
      event_col = col, n_col = "n_arm", stratum_label = key,
      min_studies = MIN_STUDIES, min_patients = MIN_PATIENTS
    )
  }
}

# --- (c) Route-of-administration subgroup -------------------------------------
# Run for ALL 4 outcome families, per pseudo_code.md S3's literal loop.
route_levels <- sort(unique(dat_analysis$route_group))

route_results <- list()
for (outcome_name in names(OUTCOME_COLS)) {
  col <- OUTCOME_COLS[[outcome_name]]
  for (level in route_levels) {
    df_sub <- dat_analysis[
      !is.na(dat_analysis[[col]]) &
        !is.na(dat_analysis$route_group) &
        dat_analysis$route_group == level,
    ]
    key <- paste(outcome_name, "route_group", level, sep = "__")
    route_results[[key]] <- pool_stratum(
      df_sub,
      event_col = col, n_col = "n_arm", stratum_label = key,
      min_studies = MIN_STUDIES, min_patients = MIN_PATIENTS
    )
  }
}

# --- (d) Modality stratum: explicitly SKIPPED, not silently omitted -----------
# Pre-specified sparsity rule (strategy memo S5): if full-text retrieval
# confirms >= 3 studies with extractable antibiotic-monotherapy arms, pool as
# a formal fourth stratum; otherwise report narratively. The data-preparation
# check (02_data_preparation.R) confirmed 0 study-arms are coded pure
# "antibiotic monotherapy" -- both candidate studies (Krakhotkin 2025,
# Leitner 2021) failed full-text verification (Krakhotkin never entered the
# extraction sheet; Leitner's Pseudomonas-specific breakdown was
# unconfirmable and its row was excluded in 02_data_preparation.R). This is
# itself a reportable finding, not a gap in the analysis.
modality_sparsity <- readRDS(file.path(output_dir, "modality_sparsity_check.rds"))
modality_skip_note <- list(
  status = "NOT_ATTEMPTED",
  stratum = "modality (antibiotic monotherapy vs. phage +/- combination)",
  reason = sprintf(
    paste(
      "Antibiotic-monotherapy stratum has %d study-arms (< MIN_STUDIES = %d).",
      "Per the pre-specified sparsity contingency (strategy memo Section 5),",
      "no pooled estimate is reported for this stratum. The two candidate",
      "comparator studies (Krakhotkin 2025, Leitner 2021) both failed",
      "full-text Pseudomonas-specific verification -- Krakhotkin was never",
      "confirmed extractable and does not appear in the extraction sheet;",
      "Leitner's Pseudomonas subgroup could not be isolated from its",
      "trial-wide, 6-pathogen aggregate and was excluded from pooling in",
      "02_data_preparation.R. This is reported as a finding: insufficient",
      "comparative evidence exists to support formal pooling of an",
      "antibiotic-monotherapy-only stratum for MDR/XDR P. aeruginosa",
      "specifically."
    ),
    modality_sparsity$n_antibiotic_monotherapy, MIN_STUDIES
  )
)
message(modality_skip_note$reason)

# --- Combine and save --------------------------------------------------------------
pooled_results <- c(overall_results, resistance_results, route_results)

# Convergence audit summary (mandatory reporting per pseudo_code.md S9)
convergence_summary <- purrr::map_dfr(pooled_results, function(r) {
  if (r$status != "POOLED") return(NULL)
  tibble::tibble(
    stratum = r$stratum,
    k_studies = r$k_studies,
    n_patients = r$n_patients,
    convergence_flag = r$convergence_flag,
    primary_model_used = r$primary_model_used
  )
})

message("Convergence summary (POOLED cells only):")
for (i in seq_len(nrow(convergence_summary))) {
  message(
    "  ", convergence_summary$stratum[i], ": ",
    convergence_summary$convergence_flag[i], " -> ",
    convergence_summary$primary_model_used[i]
  )
}

not_pooled_summary <- purrr::map_dfr(pooled_results, function(r) {
  if (r$status != "NOT_POOLED") return(NULL)
  tibble::tibble(stratum = r$stratum, reason = r$reason)
})

saveRDS(pooled_results, file.path(output_dir, "pooled_results.rds"))
saveRDS(convergence_summary, file.path(output_dir, "convergence_summary.rds"))
saveRDS(not_pooled_summary, file.path(output_dir, "not_pooled_summary.rds"))
saveRDS(modality_skip_note, file.path(output_dir, "modality_skip_note.rds"))

message(
  "04_estimation.R complete. POOLED cells: ", nrow(convergence_summary),
  " | NOT_POOLED cells: ", nrow(not_pooled_summary)
)
