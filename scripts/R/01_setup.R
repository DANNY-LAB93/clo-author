# ==============================================================================
# 01_setup.R
# Purpose: Paths, libraries, seed, constants, and the paper-to-code naming
#          map for the phage therapy MDR/XDR Pseudomonas aeruginosa
#          meta-analysis of proportions.
# Project: phage_therapy_mdr_pseudomonas
# Companion: quality_reports/strategy_memo_phage_therapy_mdr_pseudomonas.md
#            quality_reports/strategy/phage_therapy_mdr_pseudomonas/pseudo_code.md
# Inputs:  none (defines paths/constants used by all downstream scripts)
# Outputs: none
# ==============================================================================

# --- R user library path fix (project environment note) ---------------------
# Packages are installed to R_LIBS_USER (system library is not writable in
# this environment). Must run before any library() call.
.libPaths(c(Sys.getenv("R_LIBS_USER"), .libPaths()))

# --- Packages -----------------------------------------------------------------
library(here)
library(readr)
library(dplyr)
library(purrr)
library(tibble)
library(meta)
library(metafor)
library(clubSandwich)
library(ggplot2)

# --- Seed ----------------------------------------------------------------------
# Single seed for the whole pipeline. No stochastic simulation is used in the
# primary GLMM/DL pooling (numerical optimization is deterministic given
# data + starting values), but metaprop()'s prediction-interval machinery and
# any bootstrap-adjacent diagnostics reference the global RNG state, so a
# seed is set once here per project convention (INV-14).
SEED <- 20260720L
set.seed(SEED)

# --- Source project functions --------------------------------------------------
source(here("scripts", "R", "functions", "backtransform_prop.R"))
source(here("scripts", "R", "functions", "pool_stratum.R"))
source(here("scripts", "R", "functions", "collapse_category.R"))
source(here("scripts", "R", "functions", "format_percent_ci.R"))

# --- Paths -----------------------------------------------------------------------
# Output Organization: by-script (CLAUDE.md) -- all tables/figures produced by
# this pipeline go into a project-identifying subfolder rather than flat into
# paper/tables/ or paper/figures/ (INV-18).
PROJECT_SLUG <- "phage_therapy_mdr_pseudomonas"

data_path    <- here("data", "cleaned", "phage_therapy_extraction_dataset.csv")
output_dir   <- here("scripts", "R", "output")
table_dir    <- here("paper", "tables", PROJECT_SLUG)
figure_dir   <- here("paper", "figures", PROJECT_SLUG)
results_path <- here(
  "quality_reports", "results_summary_phage_therapy_mdr_pseudomonas.md"
)

dir.create(output_dir, recursive = TRUE, showWarnings = FALSE)
dir.create(table_dir,  recursive = TRUE, showWarnings = FALSE)
dir.create(figure_dir, recursive = TRUE, showWarnings = FALSE)

# --- Pre-specified thresholds (strategy memo S2.1 / pseudo_code.md S2) --------
MIN_STUDIES  <- 3L
MIN_PATIENTS <- 20L
MIN_STUDIES_FUNNEL <- 10L  # Egger's/Peters' test only run at/above this k

# --- Outcome families (strategy memo S1) ---------------------------------------
OUTCOME_COLS <- c(
  clinical_success = "clinical_success_n",
  safety           = "adverse_event_n",
  eradication      = "microbio_eradication_n",
  mortality        = "mortality_n"
)

# ==============================================================================
# Paper-to-Code Naming Map (locked in Pre-Code Report, reproduced here per
# analyze/templates/paper-to-code-map.md convention)
# ==============================================================================
# Memo concept              | Code name               | Description
# ------------------------------------------------------------------------------
# Study-arm label            | study_arm_id            | Unique arm ID -> metaprop() studlab
# Study cluster              | study_id                | Groups arms for RVE clustering
# n_i                        | n_arm                   | Arm denominator
# Clinical success numerator | clinical_success_n      | Outcome 1 (primary)
# Safety/AE numerator        | adverse_event_n         | Outcome 2 (primary)
# Eradication numerator      | microbio_eradication_n  | Outcome 3 (secondary)
# Mortality numerator        | mortality_n             | Outcome 4 (secondary)
# Resistance stratum         | resistance_class        | MDR/XDR/PDR/not-classifiable
# Route stratum (collapsed)  | route_group             | topical/local, IV,
#                            |                         | inhaled/nebulized, other
# Modality stratum(collapsed)| modality_group          | phage monotherapy /
#                            |                         | phage+antibiotic combination /
#                            |                         | antibiotic monotherapy
# Pooled proportion          | p_hat                   | Back-transformed pooled estimate
# GLMM primary/fallback tag  | primary_model_used      | Which model is reported per cell
# Convergence status         | convergence_flag        | CONVERGED / FAILED_*
# k (studies), pre-spec gate | k_studies               | distinct study_id count (see
#                            |                         | Pre-Code Report deviation note:
#                            |                         | stricter than pseudo_code.md's
#                            |                         | literal nrow(df) arm-count)
# N (patients)               | n_patients              | sum(n_arm) in the cell
# ==============================================================================

message("01_setup.R complete. SEED = ", SEED)
