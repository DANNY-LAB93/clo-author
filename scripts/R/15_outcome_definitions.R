# Supplementary table: what "clinical success" actually means, arm by arm.
#
# WHY THIS EXISTS. A round-5 referee objected that the pooled clinical-success
# proportion mixes constructs a reader cannot see: "a 3-day surrogate and a
# 21-month cure in the same numerator is not one construct, and no table in the
# paper lets a reader see this." That is correct, and the review's own Results
# concede the definitional range while printing a single percentage.
#
# The referee asked for syndrome, follow-up horizon and the verbatim success
# definition as columns in Table 1. Two of the three are delivered here rather
# than there, because Table 1 already carries eight columns and the verbatim
# definitions are sentences, not cells.
#
# SYNDROME IS NOT DELIVERED, and the reason is stated rather than hidden. The
# extraction schema has no syndrome field. Deriving one by keyword from the
# existing free text was attempted and abandoned: run over the success
# definitions it left 15 of 50 arms unclassified and misassigned several others
# (an "implant loosening on X-ray" arm matched nothing; an "aortic Dacron graft"
# arm matched bone rather than device). Classifying 50 arms by hand would make
# this reviewer the single classifier for a variable that drives interpretation,
# which is the single-reviewer weakness the manuscript already declares. It is
# recorded as an outstanding gap.
#
# FOLLOW-UP HORIZON is extracted by rule from the definition text and reported
# as the LONGEST stated interval, with arms that state none marked as such. The
# point of the column is the spread, not any individual value.

suppressPackageStartupMessages({
  library(here)
  library(readr)
  library(stringr)
  library(dplyr)
})

dat <- readRDS(file.path(here::here("scripts", "R", "output"), "dat_analysis.rds"))
raw <- readr::read_csv(
  here::here("data", "cleaned", "phage_therapy_extraction_dataset.csv"),
  show_col_types = FALSE
)

# ---- follow-up horizon ------------------------------------------------------
# Convert every stated interval to days and keep the maximum. A definition may
# state several ("negative at 60 days ... no recurrence at 21 months"); the
# longest is the one that characterises the observation window.
UNIT_DAYS <- c(day = 1, week = 7, month = 30.44, year = 365.25)

longest_followup <- function(txt) {
  if (is.na(txt) || !nzchar(txt)) return(NA_real_)
  # Strip patient ages BEFORE matching intervals. The first implementation read
  # "68-year-old man" as a 68-year follow-up and "77-year-old woman" as 77 years,
  # which produced a nonsensical 4018-fold spread and would have been printed as
  # a finding. Age is the only construct in these definitions that uses a time
  # unit without denoting elapsed observation.
  txt <- gsub("(?i)\\b[0-9]+[- ]?(year|month|week|day)[- ]?old\\b", " ", txt, perl = TRUE)
  m <- str_match_all(txt, "(?i)\\b([0-9]+(?:\\.[0-9]+)?)[- ]?(day|week|month|year)s?\\b")[[1]]
  if (nrow(m) == 0) return(NA_real_)
  vals <- as.numeric(m[, 2]) * UNIT_DAYS[tolower(m[, 3])]
  max(vals, na.rm = TRUE)
}

fmt_followup <- function(days) {
  if (is.na(days)) return("not stated")
  if (days < 14) return(sprintf("%.0f d", days))
  if (days < 60) return(sprintf("%.0f wk", days / 7))
  if (days < 730) return(sprintf("%.0f mo", days / 30.44))
  sprintf("%.1f yr", days / 365.25)
}

tab <- raw |>
  filter(study_arm_id %in% dat$study_arm_id) |>
  mutate(
    fu_days = vapply(clinical_success_definition, longest_followup, numeric(1)),
    fu_label = vapply(fu_days, fmt_followup, character(1))
  ) |>
  # stated horizons first, ascending; arms stating none go last
  arrange(is.na(fu_days), fu_days) |>
  select(study_arm_id, n_arm, fu_days, fu_label, clinical_success_definition)

# ---- the spread, which is the point ----------------------------------------
stated <- tab$fu_days[!is.na(tab$fu_days)]
spread <- list(
  n_arms = nrow(tab),
  n_stated = length(stated),
  n_not_stated = sum(is.na(tab$fu_days)),
  min_days = if (length(stated)) min(stated) else NA_real_,
  max_days = if (length(stated)) max(stated) else NA_real_,
  fold_range = if (length(stated)) max(stated) / min(stated) else NA_real_
)
saveRDS(spread, file.path(here::here("scripts", "R", "output"), "followup_spread.rds"))

# ---- emit the supplementary table ------------------------------------------
escape_tex <- function(x) {
  x <- gsub("\\\\", "", x)
  x <- gsub("([%&#_$])", "\\\\\\1", x)
  x <- gsub("'", "'", x, fixed = TRUE)
  x
}

wrap_def <- function(x) {
  x <- escape_tex(x)
  # long definitions are the point of the table; keep them whole
  x
}

lines <- c(
  "\\begin{tabular}{p{2.6cm}cp{1.5cm}p{8.4cm}}",
  "\\toprule",
  "Study-arm & $n$ & Follow-up & Clinical-success definition as recorded from the source \\\\",
  "\\midrule"
)
for (i in seq_len(nrow(tab))) {
  lines <- c(lines, sprintf(
    "%s & %d & %s & %s \\\\",
    escape_tex(gsub("_", "\\\\_", tab$study_arm_id[i])),
    tab$n_arm[i], tab$fu_label[i], wrap_def(tab$clinical_success_definition[i])
  ))
}
lines <- c(lines, "\\bottomrule", "\\end{tabular}")

out_path <- file.path(
  here::here("paper", "tables", "phage_therapy_mdr_pseudomonas"),
  "outcome_definitions_by_arm.tex"
)
writeLines(lines, out_path)

message(sprintf(
  paste0("Wrote outcome_definitions_by_arm.tex (%d arms). Follow-up stated for %d, ",
         "not stated for %d; range %s to %s, a %.0f-fold spread."),
  spread$n_arms, spread$n_stated, spread$n_not_stated,
  fmt_followup(spread$min_days), fmt_followup(spread$max_days), spread$fold_range
))
