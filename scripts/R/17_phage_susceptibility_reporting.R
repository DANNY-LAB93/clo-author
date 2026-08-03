# How often does this literature say whether the phage was active on the isolate?
#
# WHY THIS EXISTS. A round-6 microbiology referee made two connected points.
#
# First, the review already treats in-vitro activity as ELIGIBILITY-RELEVANT: it
# excluded Onsea 2019 because that study's XDR P. aeruginosa was non-susceptible
# to the anti-Pseudomonas phages in the administered cocktail, so the arm
# "measures nothing about phage therapy against this review's target organism".
# Having made activity a criterion, the review must record it.
#
# Second, the review does not record it. There is no field for the phage
# preparation, its dose, its duration, whether a phagogram was performed, or
# whether the preparation was documented active against the patient's strain.
# The words phagogram, efficiency of plating and spot test appear nowhere in the
# manuscript, although several sources report them.
#
# WHAT THIS SCRIPT DOES. It counts, over the recorded extraction text, how many
# arms document any phage-susceptibility testing at all. It does NOT invent a
# per-arm activity variable: with the data this review holds, that variable would
# be missing for the overwhelming majority of arms, and a variable that is
# missing for most of the corpus should be reported as a gap rather than modelled
# as a covariate.
#
# The count is the finding. It is the same class of reporting-completeness
# failure as the DTR one, and it bears on GRADE indirectness: where a source does
# not say whether the phage could lyse the organism, the reader cannot know
# whether the intervention was delivered.

suppressPackageStartupMessages({
  library(here)
  library(readr)
})

out_dir <- here::here("scripts", "R", "output")
dat <- readRDS(file.path(out_dir, "dat_analysis.rds"))
raw <- readr::read_csv(
  here::here("data", "cleaned", "phage_therapy_extraction_dataset.csv"),
  show_col_types = FALSE
)

pooling <- raw[raw$study_arm_id %in% dat$study_arm_id, ]
blob <- paste(
  ifelse(is.na(pooling$extraction_citation), "", pooling$extraction_citation),
  ifelse(is.na(pooling$incomplete_reason), "", pooling$incomplete_reason)
)

# Any evidence in the recorded extraction that phage susceptibility was TESTED.
# Deliberately broad: a false positive here understates the gap, which is the
# conservative direction for a claim that reporting is poor.
TESTED <- paste(
  "phagogram", "efficiency of plating", "\\bEOP\\b", "spot test",
  "phage.susceptib", "susceptib\\w* to the phage", "in vitro activ",
  "active on the (patient|strain)", "remained phage-susceptible",
  sep = "|"
)
tested <- grepl(TESTED, blob, ignore.case = TRUE, perl = TRUE)

phage_susc <- list(
  n_arms = nrow(pooling),
  n_tested_documented = sum(tested),
  n_silent = sum(!tested),
  arms_documented = sort(pooling$study_arm_id[tested])
)
saveRDS(phage_susc, file.path(out_dir, "phage_susceptibility_reporting.rds"))

message(sprintf(
  paste0("Phage-susceptibility testing is documented for %d of %d pooling-eligible arms; ",
         "%d are silent. Documented: %s"),
  phage_susc$n_tested_documented, phage_susc$n_arms, phage_susc$n_silent,
  paste(phage_susc$arms_documented, collapse = ", ")
))
