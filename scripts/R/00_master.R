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

message("00_master.R: full pipeline complete.")
