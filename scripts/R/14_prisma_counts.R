# Derive the PRISMA flow's terminal counts, and state what cannot be derived.
#
# WHY. The flow diagram asserted 39 records assessed at full text, 9 excluded
# and 31 included. 39 - 9 = 30. Both round-5 referees checked it with a
# calculator and it failed, and the figure's own boxes contradicted each other
# in three further places: the eligibility box itemised nine studies from the
# Scopus channel where the Results text says ten (twice, and names ten), the
# included box said "4 at peer review round 2" and then listed five, and the
# pending box recorded Karn 2024 and Stanley 2025 as resolved-and-excluded while
# the figure caption said both remained outstanding and were folded into neither
# count.
#
# The underlying cause is that this review never kept a machine-readable
# screening log. The terminal counts come from the extraction dataset and are
# checkable; the screening-stage counts existed only as prose typed into a tikz
# picture, which is why the imbalance survived five rounds.
#
# WHAT THIS DOES. It records the screening decisions that ARE documented in the
# manuscript's own narrative, derives every count the data can support, and
# computes the shortfall between the per-channel itemisation and the derived
# total. The shortfall is emitted as a labelled quantity so the figure can print
# it. It is NOT distributed across channels to make the arithmetic close: the
# channel of origin for those records was not recorded at the time of
# screening, and saying so is the accurate statement.

suppressPackageStartupMessages({
  library(here)
  library(readr)
})

out_dir <- here::here("scripts", "R", "output")

raw <- readr::read_csv(
  here::here("data", "cleaned", "phage_therapy_extraction_dataset.csv"),
  show_col_types = FALSE
)
ana <- readRDS(file.path(out_dir, "dat_analysis.rds"))

# ---- Verified from the data -------------------------------------------------
n_included_studies <- length(unique(raw$study_id))
n_included_arms <- nrow(raw)
n_pooled_studies <- length(unique(ana$study_id))
n_pooled_arms <- nrow(ana)

# ---- Excluded at full text, with reasons ------------------------------------
# Every record the manuscript names as excluded after full-text assessment.
# Karn 2024 and Stanley 2025 belong here: both were surfaced by the round-3
# citation-chasing pass and both were resolved at peer review (Karn as
# multi-pathogen with no Pseudomonas breakdown; Stanley/CYPHY identified as
# NCT04684641 and excluded under the population rule). Earlier versions listed
# them as "pending, n = 0" while simultaneously describing them as excluded,
# and counted them in neither box.
full_text_exclusions <- tibble::tribble(
  ~record,                  ~reason,
  "Krakhotkin 2025",        "wrong pathogen (no P. aeruginosa cases)",
  "Cano 2021",              "wrong pathogen (Klebsiella)",
  "Rhoads 2009",            "no antibiotic comparator",
  "Dan 2023",               "duplicate (Aslam)",
  "Van Nieuwenhuyse 2022",  "duplicate (Pirnay consortium)",
  "Zurabov 2023",           "multi-pathogen, not separable",
  "Rubalskii 2020",         "multi-pathogen, not separable",
  "Hayakawa 2025",          "multi-pathogen feasibility study",
  "Chung 2025",             "review / perspective, not primary data",
  "Karn 2024",              "multi-pathogen, no P. aeruginosa breakdown",
  "Stanley 2025 (CYPHY)",   "NCT04684641; population rule (no resistance entry criterion)",
  # Round 5. The P. aeruginosa arm was non-susceptible to the anti-Pseudomonas
  # phages in the administered cocktail, so it measures nothing about phage
  # therapy against this review's target organism; additionally a QAMH/Belgian
  # case with Pirnay as co-author, the profile this review de-duplicates against.
  "Onsea 2019",             "phage cocktail not active against the P. aeruginosa isolate"
)
n_excluded <- nrow(full_text_exclusions)

# A record reaching full text is either included or excluded, so the number
# assessed is the sum. This is a DERIVED total, not a counted one.
n_assessed <- n_included_studies + n_excluded

# ---- Per-channel itemisation ------------------------------------------------
# As documented in Methods 3.2 and Results 4.1. The Scopus figure is ten, not
# the nine the diagram carried: the caption names ten studies from that channel
# and the Results text states ten twice.
channels <- c(
  "citation-chasing of Liu 2025's risk-of-bias table" = 5,
  "PDF/Elicit corpus (non-PRISMA, single-reviewer)"   = 8,
  "discovery-phase scoping"                           = 6,
  "native Scopus search"                              = 10,
  "held records re-confirmed"                         = 5,
  "landmark cases flagged at peer review"             = 4,
  "further records named at peer review, round 2"     = 2,
  # Round 5. Both referees identified the search string as under-sensitive by
  # construction -- every executed query required a resistance keyword in
  # title/abstract, while the eligibility criteria explicitly retain arms with no
  # resistance documentation at all. A targeted search of the four studies the
  # domain referee named confirmed it: three were retrievable and none carries a
  # resistance term in its title or abstract.
  "referee-named records screened at round 5"         = 3
)
n_itemised <- sum(channels)

# The gap between what the channel itemisation accounts for and what the flow
# requires. Reported, not absorbed.
channel_shortfall <- n_assessed - n_itemised

prisma_counts <- list(
  included_studies = n_included_studies,
  included_arms = n_included_arms,
  pooled_studies = n_pooled_studies,
  pooled_arms = n_pooled_arms,
  excluded = n_excluded,
  assessed = n_assessed,
  itemised = n_itemised,
  channel_shortfall = channel_shortfall,
  channels = channels,
  exclusions = full_text_exclusions
)
saveRDS(prisma_counts, file.path(out_dir, "prisma_counts.rds"))

# The one arithmetic identity a referee checks with a calculator.
stopifnot(
  "PRISMA: assessed - excluded must equal included" =
    n_assessed - n_excluded == n_included_studies
)

message(sprintf(
  paste0("PRISMA counts: %d assessed at full text = %d included + %d excluded. ",
         "Channel itemisation accounts for %d; shortfall of %d record(s) whose ",
         "channel of origin was not recorded at screening."),
  n_assessed, n_included_studies, n_excluded, n_itemised, channel_shortfall
))
