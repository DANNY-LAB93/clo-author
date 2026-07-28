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

# --- Population-eligibility exclusion: trial populations without a resistance
#     entry criterion -----------------------------------------------------------
# Resolves the eligibility contradiction the domain referee identified, by
# tightening the Population criterion rather than by disclosure alone.
#
# THE RULE. A study-arm is excluded when its source population was RECRUITED
# WITHOUT ANY MDR/XDR/PDR REQUIREMENT -- that is, when the trial's own
# eligibility criteria admit patients on the basis of P. aeruginosa infection or
# chronic colonization alone. For such arms the absence of a resistance label is
# not a reporting gap; the population demonstrably was not selected for
# resistance, so the arm does not satisfy this review's Population criterion.
#
# THE DISTINCTION THIS PRESERVES. Individual compassionate-use and salvage
# reports whose resistance status is simply UNREPORTED are retained and still
# coded not-classifiable (Onallah 2023, whose full text is paywalled but whose
# population is explicitly refractory infection; Ferry 2021, a relapsing
# prosthetic joint infection in which explantation was not feasible). Those
# populations ARE the salvage population this review targets; only the
# documentation is missing. Absence of a susceptibility panel in a salvage case
# report is a reporting gap; absence of a resistance criterion in a trial
# protocol is a different population.
#
# WHAT THIS COSTS. All three randomized trials leave the synthesis: PhagoBurn
# (burn-wound infection, MDR not an enrollment criterion), SWARM-P.a./AP-PA02
# and BX004-A (both cystic-fibrosis chronic pulmonary colonization). They remain
# available to the Discussion as external comparative evidence, which is the
# more honest place for them: they were never estimating this review's estimand.
# The same rule keeps out three further completed trials identified in a
# ClinicalTrials.gov sweep (NCT04684641 CYPHY, NCT05616221 Tailwind,
# NCT05453578 WRAIR-PAM-CF1), none of which imposes a resistance criterion.
NO_RESISTANCE_CRITERION_ARMS <- c(
  "Jault2019_PhagoBurn_phage",  # burn-wound infection; MDR not an entry criterion
  "ArmataAP_PA02_highdose",     # CF chronic pulmonary colonization; no resistance criterion
  "Weiner2025_BX004A_phage"     # CF chronic pulmonary infection; no resistance criterion
)
trialpop_flag <- dat_raw$study_arm_id %in% NO_RESISTANCE_CRITERION_ARMS

n_excluded_trialpop <- sum(trialpop_flag)

dat_pooling_eligible <- dat_raw[!leitner_flag & !liu_flag & !trialpop_flag, ]

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
    "Excluded: trial populations recruited with no MDR/XDR/PDR entry criterion",
    "Rows entering stratified pooling eligibility checks"
  ),
  n_rows = c(nrow(dat_raw), n_excluded_leitner, n_excluded_liu,
             n_excluded_trialpop, nrow(dat_analysis))
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
