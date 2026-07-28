# ==============================================================================
# 02_data_preparation.R
# Purpose: Load the cleaned extraction dataset, apply the analysis-specific
#          eligibility rules (beyond the data-engineer's pathogen_scope
#          filter, already applied in scripts/R/clean_phage_extraction.R),
#          and derive stratification variables (route_group, modality_group).
# Project: phage_therapy_mdr_pseudomonas
# Inputs:  data/cleaned/phage_therapy_extraction_dataset.csv
# Outputs: scripts/R/output/dat_analysis.rds
#          scripts/R/output/exclusion_log.rds
# Requires: 01_setup.R has been run (paths, packages, functions available)
# ==============================================================================

# --- Data ----------------------------------------------------------------------
dat_raw <- read_csv(data_path, show_col_types = FALSE)

message("Rows read from cleaned extraction dataset: ", nrow(dat_raw))

# --- Analysis-specific exclusion: Leitner2021 -----------------------------------
# The data-engineer's codebook/incomplete_reason field explicitly states this
# row is a trial-wide (not Pseudomonas-specific) aggregate across 6 pathogen
# types, and is "NOT usable in the primary Pseudomonas-specific proportion
# pooling as extracted" (see incomplete_reason for Leitner2021_pyophage).
# Excluded here, not silently -- logged in exclusion_log below and reported
# narratively in results_summary.md.
leitner_flag <- grepl(
  "NOT usable in the primary Pseudomonas-specific proportion pooling",
  dat_raw$incomplete_reason,
  fixed = TRUE
)
leitner_flag[is.na(leitner_flag)] <- FALSE

n_excluded_leitner <- sum(leitner_flag)

# --- Population-eligibility exclusion: Liu2025_perinephric ----------------------
# The review's Population criterion requires an infection attributed to MDR, XDR
# or PDR P. aeruginosa. The data-engineer's extraction locator for this arm
# records an ELIGIBILITY FLAG: the published antibiogram (Fig. 1B) shows
# non-susceptibility to imipenem ONLY -- one agent of roughly eleven tested --
# which does not reach the >= 3-antimicrobial-category threshold that defines
# MDR, notwithstanding the paper's own "antibiotic-resistant" framing. It was
# therefore coded not-classifiable rather than upgraded to MDR, and the
# extraction note explicitly recommended eligibility review before pooling.
#
# That review is resolved here: this is not a case of MISSING resistance
# information (the other not-classifiable arms), it is documented evidence that
# the isolate does NOT satisfy the population criterion. Retaining it would put
# a demonstrably non-MDR patient inside a review of MDR/XDR/PDR infection, so
# the arm is excluded from pooling -- logged below, and reported in the
# manuscript rather than dropped silently.
liu_flag <- dat_raw$study_arm_id == "Liu2025_perinephric_P1"
liu_flag[is.na(liu_flag)] <- FALSE

n_excluded_liu <- sum(liu_flag)

dat_pooling_eligible <- dat_raw[!leitner_flag & !liu_flag, ]

# --- Derived stratification variables -------------------------------------------
dat_analysis <- dat_pooling_eligible |>
  mutate(
    route_group    = collapse_category(route),
    modality_group = collapse_category(modality),
    # Simplified journal tier for the journal-tier falsification check
    # (Section 6, memo Falsification Test 2): leading label before "(".
    journal_tier_simple = collapse_category(journal_tier),
    # Primary country/region token for the geographic-concentration
    # robustness check (Priority 2 #5): leading label before "(".
    geographic_region = collapse_category(geographic_source)
  )

# --- Document counts (per Stage 0 requirement: every drop with counts) --------
exclusion_log <- tibble(
  step = c(
    "Rows in cleaned extraction dataset",
    "Excluded: Leitner2021 (trial-wide, not Pseudomonas-specific)",
    "Excluded: Liu2025 (antibiogram does not meet the MDR population criterion)",
    "Rows entering stratified pooling eligibility checks"
  ),
  n_rows = c(nrow(dat_raw), n_excluded_leitner, n_excluded_liu, nrow(dat_analysis))
)

message("Exclusion log:")
for (i in seq_len(nrow(exclusion_log))) {
  message("  ", exclusion_log$step[i], ": ", exclusion_log$n_rows[i])
}

# --- Modality sparsity check (pre-specified contingency, memo S5) --------------
n_antibiotic_monotherapy <- sum(
  dat_analysis$modality_group == "antibiotic monotherapy", na.rm = TRUE
)
if (n_antibiotic_monotherapy < MIN_STUDIES) {
  message(
    "Antibiotic-monotherapy stratum: ", n_antibiotic_monotherapy,
    " study-arms -- below MIN_STUDIES = ", MIN_STUDIES,
    ". Per pre-specified sparsity rule (strategy memo S5), this stratum is ",
    "NOT pooled. Reported narratively only in results_summary.md."
  )
}

# --- Save ------------------------------------------------------------------------
saveRDS(dat_analysis, file.path(output_dir, "dat_analysis.rds"))
saveRDS(exclusion_log, file.path(output_dir, "exclusion_log.rds"))
saveRDS(
  list(n_antibiotic_monotherapy = n_antibiotic_monotherapy),
  file.path(output_dir, "modality_sparsity_check.rds")
)

message("02_data_preparation.R complete. Analysis-ready rows: ", nrow(dat_analysis))
