# ==============================================================================
# 03_descriptive.R
# Purpose: Descriptive summary of the analysis-eligible extraction dataset --
#          extraction-status coverage, distribution across the three
#          pre-specified stratification variables, and per-outcome
#          availability (how many arms/patients have a non-missing
#          numerator for each of the 4 outcome families).
# Project: phage_therapy_mdr_pseudomonas
# Inputs:  scripts/R/output/dat_analysis.rds
# Outputs: scripts/R/output/descriptive_summary.rds
# Requires: 01_setup.R, 02_data_preparation.R have been run
# ==============================================================================

dat_analysis <- readRDS(file.path(output_dir, "dat_analysis.rds"))

# --- Extraction-status coverage -------------------------------------------------
extraction_status_summary <- dat_analysis |>
  count(extraction_status, name = "n_arms") |>
  arrange(desc(n_arms))

# --- Distribution across pre-specified strata -----------------------------------
resistance_class_summary <- dat_analysis |>
  count(resistance_class, name = "n_arms") |>
  arrange(desc(n_arms))

route_group_summary <- dat_analysis |>
  count(route_group, name = "n_arms") |>
  arrange(desc(n_arms))

modality_group_summary <- dat_analysis |>
  count(modality_group, name = "n_arms") |>
  arrange(desc(n_arms))

study_design_summary <- dat_analysis |>
  count(study_design, name = "n_arms") |>
  arrange(desc(n_arms))

# --- Per-outcome availability ----------------------------------------------------
outcome_availability <- purrr::imap_dfr(OUTCOME_COLS, function(col, outcome_name) {
  eligible <- !is.na(dat_analysis[[col]])
  tibble(
    outcome        = outcome_name,
    n_arms_eligible = sum(eligible),
    n_studies_eligible = length(unique(dat_analysis$study_id[eligible])),
    n_patients_eligible = sum(dat_analysis$n_arm[eligible], na.rm = TRUE)
  )
})

message("Outcome availability (arms / distinct studies / patients with non-missing numerator):")
for (i in seq_len(nrow(outcome_availability))) {
  message(
    "  ", outcome_availability$outcome[i], ": ",
    outcome_availability$n_arms_eligible[i], " arms / ",
    outcome_availability$n_studies_eligible[i], " studies / ",
    outcome_availability$n_patients_eligible[i], " patients"
  )
}

# --- Overall sample size ----------------------------------------------------------
n_total_arms     <- nrow(dat_analysis)
n_total_studies  <- length(unique(dat_analysis$study_id))
n_total_patients <- sum(dat_analysis$n_arm, na.rm = TRUE)

descriptive_summary <- list(
  n_total_arms            = n_total_arms,
  n_total_studies         = n_total_studies,
  n_total_patients        = n_total_patients,
  extraction_status       = extraction_status_summary,
  resistance_class        = resistance_class_summary,
  route_group              = route_group_summary,
  modality_group           = modality_group_summary,
  study_design             = study_design_summary,
  outcome_availability     = outcome_availability
)

saveRDS(descriptive_summary, file.path(output_dir, "descriptive_summary.rds"))

message(
  "03_descriptive.R complete. Total: ", n_total_arms, " arms / ",
  n_total_studies, " studies / ", n_total_patients, " patients."
)
