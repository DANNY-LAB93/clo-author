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
# Arms whose PUBLISHED ANTIBIOGRAM positively establishes non-susceptibility in
# fewer than the three Magiorakos categories the MDR population criterion
# requires. This is a different failure from "resistance not documented": these
# sources print a panel, and the panel shows the organism was susceptible to most
# of it. Arms with no antibiogram and no MDR/XDR/PDR label remain
# not-classifiable and are RETAINED -- the asymmetry is deliberate and is argued
# in the Methods.
#
# Liu 2025 Patient 1: 1 of ~11 tested agents resistant.
# Chung 2026: intermediate to ciprofloxacin only; susceptible to
#   piperacillin-tazobactam, ceftazidime-avibactam and meropenem.
# Ronit 2024: resistant to piperacillin-tazobactam and ceftazidime; susceptible
#   to meropenem and ciprofloxacin -- two categories, not three.
BELOW_MDR_THRESHOLD_ARMS <- c(
  "Liu2025_perinephric_P1",
  "Chung2026_A",
  "Ronit2024_A"
)
liu_flag <- dat_raw$study_arm_id %in% BELOW_MDR_THRESHOLD_ARMS
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

# --- Consortium double-counting exclusion: cases inside the Pirnay 2024 roster --
# Pirnay et al. 2024 is a retrospective cohort of the first 100 CONSECUTIVE cases
# facilitated by the Belgian (Queen Astrid Military Hospital) consortium. Its
# three resistance-stratified arms are already in this dataset. Any separately
# published case report describing a patient inside that roster would therefore
# be counted twice -- once in the cohort aggregate and once as a case report.
# Van Nieuwenhuyse 2022 was previously identified and excluded on exactly this
# ground, which established the risk is real rather than theoretical.
#
# A systematic crosswalk was run (2026-07-28) against the roster in the paper's
# Supplementary Table 1, which lists all 100 cases with primary infection type,
# narrative description, involved species, resistance profile and bacteriophage
# product. NOTE: that table carries NO country and NO treatment-year column, so
# the match is made on indication + species + resistance profile + phage product
# + outcome pattern, not on provenance. Fifty of the 100 cases involve
# P. aeruginosa. Two of this review's case-report arms match one of them closely
# enough that duplication cannot be excluded, and per the conservative rule the
# CASE REPORT is dropped and the cohort entry retained:
#
#   Ferry2022_A  ~ Pirnay case #79. #79 is the ONLY chronic spondylodiscitis in
#     the entire roster, is P. aeruginosa, uses the Belgian PNM + PT07 phages,
#     and per this review's own Pirnay extraction was not eradicated, had an
#     adverse event and died -- matching Ferry 2022's eradication=0 and
#     mortality=1 exactly. Ferry 2022 sources its phages from Belgium. The
#     resistance labels differ (roster XDR, case report PDR derived from MICs),
#     which is the expected discrepancy between consortium coding and an
#     independent MIC-based derivation, not evidence of a different patient.
#
#   Racenis2023_LVAD_A ~ Pirnay case #56, "Persistent LVAD driveline infection",
#     P. aeruginosa, MDR, phages 14-1 + PNM + PT07 with ceftolozane/tazobactam.
#     Racenis 2023 states its phages came from Belgium QAMH. Indication, species,
#     resistance class and phage source all agree.
#
# NOT excluded, because no clean match was found: Racenis2022_femur_A (the
# roster's femoral cases are UDR (#23) or XDR (#27); ours is MDR),
# Blasco2023_A (roster #92 mentions a leg stump and MDR bacteraemia but the rest
# of its narrative does not correspond), and Tkhilaishvili2020_A (the roster's
# only prosthetic-knee P. aeruginosa case, #15, is UDR; ours is XDR, and the
# Berlin centre sources phages independently). These three are retained and the
# residual uncertainty is reported in the manuscript rather than resolved here.
PIRNAY_ROSTER_DUPLICATE_ARMS <- c(
  "Ferry2022_A",          # ~ Pirnay case #79 (chronic spondylodiscitis)
  "Racenis2023_LVAD_A",   # ~ Pirnay case #56 (persistent LVAD driveline infection)
  # Round 5. Queen Astrid Military Hospital, BFC1, treated November 2016 --
  # inside the roster's 1 Jan 2008 to 30 Apr 2022 window -- with Pirnay as senior
  # author, and the roster records 27 of its 100 cases as published elsewhere.
  # Roster case 13 matches on species, centre, product, intravenous route and the
  # wound-plus-bloodstream indication. Case 13 is recorded as surviving whereas
  # this patient died at four months, which a shorter roster follow-up explains;
  # roster case 3, the only other XDR death, is a respiratory infection treated by
  # inhalation for four days and is a different patient.
  "Jennes2017_A"
)
pirnay_dup_flag <- dat_raw$study_arm_id %in% PIRNAY_ROSTER_DUPLICATE_ARMS

n_excluded_pirnay_dup <- sum(pirnay_dup_flag)

dat_pooling_eligible <- dat_raw[
  !leitner_flag & !liu_flag & !trialpop_flag & !pirnay_dup_flag,
]

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
    "Excluded: published antibiogram below the MDR population criterion",
    "Excluded: trial populations recruited with no MDR/XDR/PDR entry criterion",
    "Excluded: case reports duplicating a patient inside the Pirnay 2024 roster",
    "Rows entering stratified pooling eligibility checks"
  ),
  n_rows = c(nrow(dat_raw), n_excluded_leitner, n_excluded_liu,
             n_excluded_trialpop, n_excluded_pirnay_dup, nrow(dat_analysis))
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
