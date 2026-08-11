# ==============================================================================
# Title:   Clean and validate the phage therapy MDR/XDR Pseudomonas extraction
#          dataset (systematic review / meta-analysis of proportions)
# Author:  data-engineer agent (clo-author pipeline)
# Date:    2026-07-19
# Purpose: Read the hand-built primary-source extraction spreadsheet
#          (metaanalisis/datos/phage_therapy_extraction_raw.csv), validate it against
#          the schema specified in
#          quality_reports/strategy/phage_therapy_mdr_pseudomonas/pseudo_code.md
#          Sec.1, apply the pre-specified eligibility filter
#          (pathogen_scope != "mixed-not-separable"), and write the
#          analysis-ready cleaned dataset + a coverage summary object.
#
# Inputs:  metaanalisis/datos/phage_therapy_extraction_raw.csv
# Outputs: metaanalisis/datos/phage_therapy_extraction_dataset.csv
#          metaanalisis/datos/phage_therapy_extraction_dataset.rds
#          metaanalisis/datos/phage_therapy_extraction_coverage_summary.rds
#
# Note: This dataset is built from MANUAL, per-study extraction from primary-
#       source PDFs (case reports/case series) read directly by the
#       data-engineer agent -- there is no upstream machine-readable raw data
#       to wrangle. This script's job is schema validation, the eligibility
#       filter, and light derived-field construction (study_arm_id), not
#       data transformation of a large tabular source.
# ==============================================================================

# --- R user library path fix (project environment note) ---------------------
# Packages are installed to R_LIBS_USER (system library is not writable in
# this environment). Must run before any library() call -- same fix as
# scripts/R/01_setup.R.
.libPaths(c(Sys.getenv("R_LIBS_USER"), .libPaths()))

library(dplyr)
library(readr)
library(here)

# ---- Paths --------------------------------------------------------------
raw_path     <- here("metaanalisis", "datos", "phage_therapy_extraction_raw.csv")
out_dir      <- here("metaanalisis", "datos")
out_csv_path <- file.path(out_dir, "phage_therapy_extraction_dataset.csv")
out_rds_path <- file.path(out_dir, "phage_therapy_extraction_dataset.rds")
out_cov_path <- file.path(out_dir, "phage_therapy_extraction_coverage_summary.rds")

dir.create(out_dir, recursive = TRUE, showWarnings = FALSE)

# ---- Required schema (per pseudo_code.md Sec.1) --------------------------
required_cols <- c(
  "study_id", "arm_id", "n_arm", "pathogen_scope", "resistance_class",
  "resistance_class_source", "route", "modality", "clinical_success_n",
  "clinical_success_definition", "adverse_event_n", "microbio_eradication_n",
  "mortality_n", "los_days", "resistance_emergence_n", "study_design",
  "data_provenance", "rob_source", "publication_year", "journal_tier",
  "geographic_source", "extraction_citation", "extraction_status",
  "incomplete_reason"
)

# ---- Read raw extraction sheet --------------------------------------------
dat_raw <- read_csv(raw_path, col_types = cols(.default = "c"), na = "NA")

missing_cols <- setdiff(required_cols, names(dat_raw))
if (length(missing_cols) > 0) {
  stop(sprintf(
    "Extraction raw sheet is missing required column(s): %s",
    paste(missing_cols, collapse = ", ")
  ))
}

# ---- Type conversions -------------------------------------------------------
dat <- dat_raw %>%
  mutate(
    n_arm                   = as.integer(n_arm),
    clinical_success_n      = as.integer(clinical_success_n),
    adverse_event_n         = as.integer(adverse_event_n),
    microbio_eradication_n  = as.integer(microbio_eradication_n),
    mortality_n             = as.integer(mortality_n),
    los_days                = as.numeric(los_days),
    resistance_emergence_n  = as.integer(resistance_emergence_n),
    publication_year        = as.integer(publication_year),
    # study_arm_id is the unique studlab identifier fed to metaprop() /
    # pool_stratum() per pseudo_code.md Sec.2 -- falls back to study_id
    # when arm_id is NA (incomplete rows with no confirmed arm structure yet)
    study_arm_id            = if_else(!is.na(arm_id), arm_id, study_id)
  )

# ---- Eligibility filter (pre-specified, strategy memo Sec.2.2) ------------
# "Mixed-not-separable arms are excluded." No rows in this extraction pass
# were coded mixed-not-separable, but the filter is applied programmatically
# (not just documented) so it activates automatically as more studies are
# added in future extraction rounds.
n_before_filter <- nrow(dat)
dat_eligible <- dat %>%
  filter(is.na(pathogen_scope) | pathogen_scope != "mixed-not-separable")
n_excluded_mixed <- n_before_filter - nrow(dat_eligible)

# ---- Coverage summary (feeds quality_reports/data_extraction_summary_*.md) -
coverage_summary <- dat_eligible %>%
  count(extraction_status, name = "n_rows")

n_complete_arms <- dat_eligible %>%
  filter(extraction_status == "COMPLETE") %>%
  nrow()

n_incomplete_rows <- dat_eligible %>%
  filter(extraction_status == "EXTRACTION_INCOMPLETE") %>%
  nrow()

n_patients_complete <- dat_eligible %>%
  filter(extraction_status == "COMPLETE") %>%
  summarise(total = sum(n_arm, na.rm = TRUE)) %>%
  pull(total)

n_monotherapy_arms <- dat_eligible %>%
  filter(extraction_status == "COMPLETE", modality == "antibiotic monotherapy") %>%
  nrow()

coverage_summary_list <- list(
  by_status              = coverage_summary,
  n_complete_arms        = n_complete_arms,
  n_incomplete_rows      = n_incomplete_rows,
  n_patients_complete    = n_patients_complete,
  n_excluded_mixed_not_separable = n_excluded_mixed,
  n_monotherapy_arms_complete = n_monotherapy_arms
)

# ---- Save outputs -----------------------------------------------------------
write_csv(dat_eligible, out_csv_path)
saveRDS(dat_eligible, out_rds_path)
saveRDS(coverage_summary_list, out_cov_path)

message("Cleaned extraction dataset written to: ", out_csv_path)
message("Rows: ", nrow(dat_eligible),
        " | COMPLETE study-arms: ", n_complete_arms,
        " | EXTRACTION_INCOMPLETE rows: ", n_incomplete_rows,
        " | Total patients (COMPLETE arms only): ", n_patients_complete,
        " | Monotherapy arms (COMPLETE): ", n_monotherapy_arms)
