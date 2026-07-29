# ==============================================================================
# 12_risk_of_bias.R
# Purpose: A reproducible, per-ARM risk-of-bias appraisal for every pooling-
#          eligible study-arm, emitted as a table rather than asserted in prose.
#
#          WHY THIS EXISTS. The manuscript claimed risk-of-bias ratings were
#          "complete for all 31 study-arms". That was false. The supporting file
#          documents per-domain judgements for seven studies, four of which
#          (Weiner 2025, Jault 2019, Leitner 2021, SWARM-P.a.) are excluded from
#          pooling by the population rule -- so only three pooling-eligible
#          studies carried a documented appraisal. Fourteen arms carried the
#          bare string "independently-rated" with no instrument and no rating.
#
#          WHAT THIS IS. Every arm remaining in the corpus is observational --
#          20 case reports, 8 case-series arms, 3 arms of one retrospective
#          cohort -- so a single instrument applies throughout: the four domains
#          of Murad et al. (2018) for case reports and series (selection,
#          ascertainment, causality, reporting). Each domain is scored by a
#          PRE-SPECIFIED RULE over extraction metadata this review already
#          records, so the appraisal is auditable and regenerates with the data.
#
#          WHAT THIS IS NOT. It is not a substitute for a second reviewer
#          reading each full text and judging each domain by hand. It is a
#          systematic, transparent floor: it uses only facts the extraction
#          already established, and where the extraction is silent it scores the
#          domain as unclear rather than favourable. The manuscript must say so.
#
# Project: phage_therapy_mdr_pseudomonas
# Inputs:  scripts/R/output/dat_analysis.rds
# Outputs: scripts/R/output/rob_per_arm.rds
#          paper/tables/phage_therapy_mdr_pseudomonas/rob_per_arm.tex
# Requires: 01_setup.R, 02_data_preparation.R have been run
# ==============================================================================

dat_analysis <- readRDS(file.path(output_dir, "dat_analysis.rds"))

# --- Domain 1: SELECTION ------------------------------------------------------
# Murad asks whether the case represents the whole of the investigator's
# experience or a selected instance. A consecutive series or a cohort answers
# yes; a stand-alone case report cannot, because publication of a single patient
# is itself the selection event. This is the domain that carries the review's
# central concern -- favourable-outcome reporting -- so it is scored strictly.
rob_selection <- function(design, citation) {
  consecutive <- grepl("consecutive", citation, ignore.case = TRUE)
  if (design == "retrospective cohort" || consecutive) {
    c("Low", "Consecutive or cohort sampling stated in the source")
  } else if (design == "case series") {
    c("Moderate", "Case series; consecutive enrolment not stated")
  } else {
    c("High", "Single-patient report; publication is itself the selection event")
  }
}

# --- Domain 2: ASCERTAINMENT --------------------------------------------------
# Were exposure and outcome adequately ascertained? Proxied by how close this
# review got to the primary record: a page/figure/table locator in the primary
# source is adequate; an abstract-only or secondary-source extraction is not,
# because the outcome definition could not be checked against the full report.
rob_ascertainment <- function(citation, incomplete) {
  txt <- paste(citation, incomplete)
  secondary <- grepl("SECONDARY SOURCE|concordant secondary", txt, ignore.case = TRUE)
  abstract  <- grepl("abstract-only|abstract only|structured abstract", txt, ignore.case = TRUE)
  locator   <- grepl("p\\.[0-9]|Fig\\.|Table [0-9]|Supplementary", citation)
  if (secondary) {
    c("High", "Outcome recovered from secondary syntheses; primary text not retrieved")
  } else if (abstract) {
    c("Moderate", "Abstract-only extraction; full text not consulted")
  } else if (locator) {
    c("Low", "Primary-source locator (page, figure or table) recorded")
  } else {
    c("Moderate", "No primary-source locator recorded")
  }
}

# --- Domain 3: CAUSALITY ------------------------------------------------------
# Can the outcome be attributed to the phage? In this corpus, essentially never:
# 30 of 31 arms give phage WITH antibiotics, so any improvement is confounded by
# co-intervention by design. Murad also asks about challenge/rechallenge and
# dose-response, neither of which this literature reports. The single
# monotherapy arm is the only one where attribution is even in principle
# available, and with n = 1 it remains weak.
rob_causality <- function(modality, n_arm) {
  if (grepl("monotherapy", modality, ignore.case = TRUE)) {
    c("Moderate", "Phage monotherapy; no antibiotic co-intervention, but n = 1")
  } else {
    c("High", "Phage given with concomitant antibiotics; effect not separable from co-intervention")
  }
}

# --- Domain 4: REPORTING ------------------------------------------------------
# Is there enough detail to replicate? Read directly off the extraction status
# this review already assigned, which records whether every pre-specified field
# was obtainable.
rob_reporting <- function(status) {
  if (identical(status, "COMPLETE")) {
    c("Low", "All pre-specified outcome fields extractable")
  } else if (identical(status, "PARTIAL")) {
    c("Moderate", "Some pre-specified outcome fields not reported")
  } else {
    c("High", "Multiple pre-specified outcome fields not reported")
  }
}

RANK <- c(Low = 1L, Moderate = 2L, High = 3L)

rob_per_arm <- purrr::map_dfr(seq_len(nrow(dat_analysis)), function(i) {
  r <- dat_analysis[i, ]
  cit <- ifelse(is.na(r$extraction_citation), "", r$extraction_citation)
  inc <- ifelse(is.na(r$incomplete_reason), "", r$incomplete_reason)

  sel <- rob_selection(r$study_design, cit)
  asc <- rob_ascertainment(cit, inc)
  cau <- rob_causality(ifelse(is.na(r$modality), "", r$modality), r$n_arm)
  rep <- rob_reporting(r$extraction_status)

  # Overall = worst domain. Murad's tool is not additive and offers no summary
  # score; taking the worst domain is the conservative reading and is stated as
  # the rule rather than left implicit.
  worst <- names(RANK)[max(RANK[c(sel[1], asc[1], cau[1], rep[1])])]

  tibble::tibble(
    study_arm_id  = r$study_arm_id,
    design        = r$study_design,
    n_arm         = r$n_arm,
    selection     = sel[1], selection_reason     = sel[2],
    ascertainment = asc[1], ascertainment_reason = asc[2],
    causality     = cau[1], causality_reason     = cau[2],
    reporting     = rep[1], reporting_reason     = rep[2],
    overall       = worst
  )
})

saveRDS(rob_per_arm, file.path(output_dir, "rob_per_arm.rds"))

message("Per-arm risk of bias (Murad 2018 domains, rule-based):")
for (d in c("selection", "ascertainment", "causality", "reporting", "overall")) {
  tab <- table(factor(rob_per_arm[[d]], levels = names(RANK)))
  message(sprintf("  %-14s Low %2d | Moderate %2d | High %2d", d, tab[1], tab[2], tab[3]))
}

# --- LaTeX table (bare tabular per INV-13) ------------------------------------
esc <- function(x) gsub("_", "\\\\_", gsub("%", "\\\\%", x))
abbr <- c(Low = "L", Moderate = "M", High = "H")

rows <- vapply(seq_len(nrow(rob_per_arm)), function(i) {
  r <- rob_per_arm[i, ]
  sprintf("%s & %s & %d & %s & %s & %s & %s & \\textbf{%s} \\\\",
          esc(r$study_arm_id), esc(r$design), r$n_arm,
          abbr[[r$selection]], abbr[[r$ascertainment]],
          abbr[[r$causality]], abbr[[r$reporting]], abbr[[r$overall]])
}, character(1L))

writeLines(
  c("\\begin{tabular}{llcccccc}", "\\toprule",
    "Study-arm & Design & $N$ & Sel. & Asc. & Cau. & Rep. & Overall \\\\",
    "\\midrule", rows, "\\bottomrule", "\\end{tabular}"),
  file.path(table_dir, "rob_per_arm.tex")
)
message("Wrote ", file.path(table_dir, "rob_per_arm.tex"), " (", nrow(rob_per_arm), " rows)")
