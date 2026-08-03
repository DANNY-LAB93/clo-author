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
# The underlying cause was stated here, for five rounds, as "this review never
# kept a machine-readable screening log". THAT WAS FALSE, and the correction
# matters more than the original claim did.
#
# A structured log exists -- Cribado_Sistematico_COMPLETO_76_3.xlsx, 75 documents
# with a row each, a column per PICO criterion, a final decision and the verbatim
# text supporting it. It was never in the repository, so no script could read it,
# no referee could check it, and the person who wrote this comment could not see
# it either. It is now imported to data/raw/local_screening_log.csv by
# scripts/import_screening_log.py.
#
# The real cause is therefore narrower and less excusable than the one recorded
# here: the screening WAS documented, and the documentation was not
# version-controlled. The terminal counts come from the extraction dataset and
# are checkable; the screening-stage counts existed only as prose typed into a
# tikz picture, which is why the imbalance survived five rounds.
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
  # Rubalskii 2020 was here until round 5. The domain referee challenged the
  # "not separable" call, Table 1 upheld the challenge, and its Patient 8 --
  # monomicrobial P. aeruginosa with an individually reported outcome -- is now
  # in the analytic dataset. Listing it as an exclusion as well would count the
  # study twice.
  "Hayakawa 2025",          "multi-pathogen feasibility study",
  "Chung 2025",             "review / perspective, not primary data",
  "Karn 2024",              "multi-pathogen, no P. aeruginosa breakdown",
  "Stanley 2025 (CYPHY)",   "NCT04684641; population rule (no resistance entry criterion)",
  # Round 5. The P. aeruginosa arm was non-susceptible to the anti-Pseudomonas
  # phages in the administered cocktail, so it measures nothing about phage
  # therapy against this review's target organism; additionally a QAMH/Belgian
  # case with Pirnay as co-author, the profile this review de-duplicates against.
  "Onsea 2019",             "phage cocktail not active against the P. aeruginosa isolate",
  # Round 5, un-blocked search. Screened in by a phage-therapy keyword and
  # excluded on a stated ground each.
  "Surana 2026",            "no phage administered; phages named only as unavailable",
  "Jernigan 2025",          "induced native phage, not exogenous administration; multi-pathogen",
  "Ferry 2024 (PHAGEinLYON)", "programme report; no P. aeruginosa-separable outcome",
  "Otava 2024",             "isolate susceptible to all agents but trimethoprim-sulfa",
  "Eiferman 2025",          "isolate described verbatim as multi-susceptible",
  "Gupta 2019",             "outcomes pooled across pathogens; not separable"
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
  "referee-named records screened at round 5"         = 3,
  # Round 5, second pass. The methods referee set a falsifiable bar: re-run the
  # search with the resistance block REMOVED, and if it yields two or fewer new
  # eligible studies the corpus is near-complete. PubMed as title/abstract
  # "Pseudomonas aeruginosa" AND phage-therapy terms, clinical publication types,
  # 2016-2026, returned 45 records; 17 were already traceable to this corpus and
  # 28 had never been screened. Seven of those 28 entered the analytic dataset --
  # four pooled, three extracted and then excluded on the population or
  # de-duplication rules. The bar was not met, and the concession that the search
  # remains under-sensitive is reported as a finding rather than a caveat.
  "un-blocked PubMed search, round 5"                 = 14
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
