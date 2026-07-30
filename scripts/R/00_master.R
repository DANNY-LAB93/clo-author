# ==============================================================================
# 00_master.R
# Purpose: Run the full phage therapy MDR/XDR Pseudomonas aeruginosa
#          meta-analysis of proportions pipeline in sequence.
# Project: phage_therapy_mdr_pseudomonas
# Usage:   Rscript scripts/R/00_master.R
#          (run from anywhere -- here() resolves the project root via
#          the .here / .Rproj marker file; no setwd() is used)
# ==============================================================================

source(here::here("scripts", "R", "01_setup.R"))
source(here::here("scripts", "R", "02_data_preparation.R"))
source(here::here("scripts", "R", "03_descriptive.R"))
source(here::here("scripts", "R", "04_estimation.R"))
source(here::here("scripts", "R", "05_robustness.R"))
source(here::here("scripts", "R", "06_falsification.R"))
source(here::here("scripts", "R", "07_figures.R"))
source(here::here("scripts", "R", "08_tables.R"))
source(here::here("scripts", "R", "09_table1_characteristics.R"))
source(here::here("scripts", "R", "10_grade.R"))
source(here::here("scripts", "R", "12_risk_of_bias.R"))
source(here::here("scripts", "R", "11_manifest.R"))
# Emits paper/generated_scalars.tex. Must run after 04_estimation.R, since a
# cell that stops pooling must lose its macros so the manuscript stops
# compiling rather than silently keeping a stale number.
source(here::here("scripts", "R", "14_prisma_counts.R"))
# Supplementary table exposing what "clinical success" means arm by arm, with
# the follow-up horizon each source states. A round-5 referee objected that no
# table let a reader see a 3-day surrogate and a 2-year cure in one numerator.
source(here::here("scripts", "R", "15_outcome_definitions.R"))
# Tests whether the pooled eradication estimate is one construct or two. A
# round-6 referee argued it is a category error; splitting chronic airway
# colonisation from other sites drives tau^2 to zero, which settles it.
source(here::here("scripts", "R", "16_eradication_site_split.R"))
# Emits quality_reports/corpus_identifier_index.txt and fails if any study
# lacks a resolvable identifier. A screening pass diffs candidate lists
# against that index; without it, Ngauy 2026 was re-screened as new when it
# was already included.
source(here::here("scripts", "check_identifier_traceability.R"))
# The macro system guarantees nothing unless the PROSE uses it. This fails the
# build when a percentage the pipeline computes is typed by hand instead --
# the defect that left "73.0%" for the MDR cell in the Introduction and
# Discussion long after the value became 75.0%.
typed_check <- system2(
  "python",
  c(shQuote(here::here("scripts", "check_no_typed_estimates.py"))),
  stdout = "", stderr = ""
)
if (!identical(as.integer(typed_check), 0L)) {
  stop("check_no_typed_estimates.py failed: a computed estimate is typed into the prose")
}
# 13 runs last: it reads the outputs of everything above, including the
# PRISMA counts, and writes the macros the manuscript compiles against.
source(here::here("scripts", "R", "13_tex_macros.R"))

message("00_master.R: full pipeline complete.")
