# Emit every prose-quotable number as a LaTeX macro.
#
# WHY THIS EXISTS. Across five review rounds the manuscript repeatedly quoted
# numbers that the pipeline did not produce: estimates from a superseded corpus,
# confidence intervals attached to the wrong point estimate, and -- worst --
# three outcome-stratum cells reported as pooled that the pipeline had refused
# to pool, complete with invented denominators and intervals. Two guards already
# existed and neither caught it. The scalar manifest is a document, so nothing
# forces the prose to agree with it; check_manuscript_numbers.py tests only
# whether a number appears SOMEWHERE in the known set, so a value that is real
# for one cell passes when quoted for another.
#
# The fix is to make the prose a build product. Every pooled cell emits macros
# named after the cell. The manuscript writes \csOverallEst instead of "76.1\%".
# Three properties follow, and only the third is new:
#
#   1. A stale number cannot survive, because there is no literal to go stale.
#   2. A number cannot migrate between cells, because the macro names the cell.
#   3. A cell that STOPS being poolable deletes its own macros, so any sentence
#      still quoting it fails the build with an undefined control sequence.
#      This is the property that would have caught the three fabricated cells.
#
# Macros are emitted ONLY for cells the pipeline actually pooled. That asymmetry
# is deliberate and is the whole mechanism -- do not add a fallback that emits
# an empty or placeholder macro for a not-pooled cell.

suppressPackageStartupMessages({
  library(here)
})

# Use the SAME back-transformation the tables and the manifest use. If the
# macros computed the proportion independently they could drift from the table
# they are supposed to agree with, which is the failure mode this file exists
# to remove.
source(here::here("scripts", "R", "functions", "backtransform_prop.R"))

out_dir <- here::here("scripts", "R", "output")
pooled <- readRDS(file.path(out_dir, "pooled_results.rds"))
dat <- readRDS(file.path(out_dir, "dat_analysis.rds"))

target <- here::here("paper", "generated_scalars.tex")

# ---- helpers ----------------------------------------------------------------
# LaTeX macro names may contain only letters, so cell keys are camel-cased.
camel <- function(x) {
  x <- gsub("[^A-Za-z0-9]+", " ", x)
  parts <- strsplit(trimws(x), " +")[[1]]
  if (length(parts) == 0) return("")
  paste0(toupper(substring(parts, 1, 1)), substring(parts, 2), collapse = "")
}

# Digits are spelled out: \csOverallK cannot be \cs1K.
num_word <- c("Zero", "One", "Two", "Three", "Four", "Five",
              "Six", "Seven", "Eight", "Nine")
despecialise <- function(x) {
  for (i in 0:9) x <- gsub(as.character(i), num_word[i + 1], x)
  x
}

pct <- function(p, d = 1) sprintf(paste0("%.", d, "f\\%%"), 100 * p)
num <- function(x, d = 3) sprintf(paste0("%.", d, "f"), x)

# Every macro body ends with \xspace. A LaTeX control word swallows the
# whitespace after it, so "\CellsPooled cells" would typeset as "13cells" --
# which it did, throughout the first compiled draft of this system. xspace
# restores the space unless the following token is punctuation or a closing
# brace. It requires \usepackage{xspace}, which main.tex loads.
XS <- "\\xspace"

lines <- c(
  "% GENERATED FILE -- DO NOT EDIT.",
  "% Written by scripts/R/13_tex_macros.R. Edit the pipeline, not this file.",
  "%",
  "% Every macro below corresponds to a cell the pipeline POOLED. A cell that",
  "% falls below the pooling threshold emits no macros, so a sentence that still",
  "% quotes it will fail to compile. That is intended: see the header of",
  "% scripts/R/13_tex_macros.R.",
  ""
)

# ---- per-cell macros --------------------------------------------------------
short_outcome <- c(
  clinical_success = "Cs", safety = "Saf",
  eradication = "Erad", mortality = "Mort"
)

cell_macro_stem <- function(key) {
  parts <- strsplit(key, "__", fixed = TRUE)[[1]]
  outcome <- short_outcome[[parts[1]]]
  if (is.null(outcome) || is.na(outcome)) outcome <- camel(parts[1])
  if (length(parts) == 2 && parts[2] == "overall") {
    return(paste0(outcome, "Overall"))
  }
  # stratum_var + level, e.g. resistance_class + MDR -> ResistanceMDR
  var_short <- c(resistance_class = "Res", route_group = "Route",
                 dtr_status = "Dtr", modality = "Mod")
  vs <- var_short[[parts[2]]]
  if (is.null(vs) || is.na(vs)) vs <- camel(parts[2])
  paste0(outcome, vs, despecialise(camel(parts[3])))
}

emitted <- character(0)
n_pooled <- 0L

for (key in names(pooled)) {
  cell <- pooled[[key]]
  status <- cell$status
  is_pooled <- !is.null(status) && identical(as.character(status), "POOLED")

  stem <- cell_macro_stem(key)

  add <- function(suffix, value) {
    lines <<- c(lines, paste0("\\newcommand{\\", stem, suffix, "}{", value, XS, "}"))
  }

  # Sample sizes are facts about the corpus and are emitted for EVERY cell,
  # pooled or not: the text legitimately needs to say how small a cell that
  # failed the threshold actually was. Estimates and intervals are emitted only
  # for pooled cells -- that asymmetry is the guard.
  if (!is_pooled) {
    lines <- c(lines, paste0("% ", key, "  [NOT POOLED -- sizes only, no estimate]"))
    add("K", format(cell$k_studies))
    add("Arms", format(cell$k_arms))
    add("N", format(cell$n_patients))
    lines <- c(lines, "")
    next
  }

  n_pooled <- n_pooled + 1L
  emitted <- c(emitted, stem)

  lines <- c(lines, paste0("% ", key))
  m <- cell$primary
  est <- backtransform_prop(m$TE.random, sm = m$sm)
  lo  <- backtransform_prop(m$lower.random, sm = m$sm)
  hi  <- backtransform_prop(m$upper.random, sm = m$sm)

  add("Est", pct(est))
  add("Lo", pct(lo))
  add("Hi", pct(hi))
  add("CI", paste0("95\\% CI ", pct(lo), "--", pct(hi)))
  add("EstCI", paste0(pct(est), " (95\\% CI ", pct(lo), "--", pct(hi), ")"))
  add("K", format(cell$k_studies))
  add("Arms", format(cell$k_arms))
  add("N", format(cell$n_patients))
  add("Events", format(sum(m$event, na.rm = TRUE)))
  add("Tau", num(m$tau2))

  # Alternative estimators. The manuscript quoted these for overall safety at
  # values from a superseded corpus (7.9/26.8 against the true 8.4/27.4), and
  # both round-5 referees noted that for three of the four overall outcomes an
  # alternative estimator falls OUTSIDE the primary interval. Emitting them
  # keeps that comparison honest.
  # The Freeman-Tukey back-transform needs the harmonic mean of arm sizes. Use
  # the identical expression 05_robustness.R uses to build the sensitivity
  # table, or the macro and the table it is compared against will disagree --
  # which they did on first implementation (7.1% against the table's 8.4%).
  # Field names are stated per model rather than guessed by fallback: the
  # fixed-effect object carries BOTH TE.common and a TE.random, and a generic
  # "use TE.random if present" rule silently read the random-effects estimate
  # out of the fixed-effect model (20.7% against the table's 20.5%). The table
  # generator's own field choices are mirrored exactly.
  n_harmonic <- 1 / mean(1 / cell$glmm_raw$n)
  sens_spec <- list(
    list(sfx = "FT", slot = "sens_ft",        field = "TE.random", sm = "PFT"),
    list(sfx = "DL", slot = "sens_logit_dl",  field = "TE.random", sm = "PLOGIT"),
    list(sfx = "FE", slot = "sens_fe",        field = "TE.common", sm = "PLOGIT")
  )
  for (sp in sens_spec) {
    sm_obj <- cell[[sp$slot]]
    if (is.null(sm_obj)) next
    te <- sm_obj[[sp$field]]
    if (is.null(te) || length(te) != 1 || !is.finite(te)) next
    nh <- if (identical(sp$sm, "PFT")) n_harmonic else 1
    add(sp$sfx, pct(backtransform_prop(te, sm = sp$sm, n_harmonic = nh)))
  }

  # The prediction interval is emitted only where meta() produced one. In the
  # 11 cells with tau^2 = 0 it collapses onto the CI; that collapse is discussed
  # in the text and is not hidden here.
  has_pi <- !is.null(m$lower.predict) && length(m$lower.predict) == 1 &&
            is.finite(m$lower.predict)
  if (has_pi) {
    add("PIlo", pct(backtransform_prop(m$lower.predict, sm = m$sm)))
    add("PIhi", pct(backtransform_prop(m$upper.predict, sm = m$sm)))
    add("PI", paste0("[", pct(backtransform_prop(m$lower.predict, sm = m$sm)),
                     ", ", pct(backtransform_prop(m$upper.predict, sm = m$sm)), "]"))
  }
  lines <- c(lines, "")
}

# ---- corpus-level macros ----------------------------------------------------
# These are the counts the manuscript got wrong in four consecutive captions.
n_cells_total <- length(pooled)
n_cells_pooled <- n_pooled
n_cells_not <- n_cells_total - n_pooled

lines <- c(lines,
  "% ---- corpus and cell counts ----",
  paste0("\\newcommand{\\CellsTotal}{", n_cells_total, XS, "}"),
  paste0("\\newcommand{\\CellsPooled}{", n_cells_pooled, XS, "}"),
  paste0("\\newcommand{\\CellsNotPooled}{", n_cells_not, XS, "}"),
  paste0("\\newcommand{\\ArmsAnalysed}{", nrow(dat), XS, "}"),
  paste0("\\newcommand{\\StudiesAnalysed}{", length(unique(dat$study_id)), XS, "}"),
  paste0("\\newcommand{\\PatientsAnalysed}{", sum(dat$n_arm, na.rm = TRUE), XS, "}"),
  ""
)

# ---- robustness and falsification scalars -----------------------------------
# These are the quantities the Discussion misreported: the Peters' eligibility
# count (stated three different ways across the manuscript) and the
# population-eligibility deltas (stated with four different sets of values, two
# of which were internally impossible -- a nonzero delta between identical
# numbers).
safe_read <- function(f) {
  p <- file.path(out_dir, f)
  if (file.exists(p)) readRDS(p) else NULL
}

fe <- safe_read("funnel_eligibility.rds")
if (!is.null(fe)) {
  elig_col <- intersect(c("eligible_for_funnel", "eligible"), names(fe))
  if (length(elig_col) > 0) {
    n_elig <- sum(fe[[elig_col[1]]], na.rm = TRUE)
    pcol <- intersect(c("peters_p", "p_value", "peters_pval"), names(fe))
    n_finite <- if (length(pcol) > 0) sum(is.finite(fe[[pcol[1]]])) else NA_integer_
    lines <- c(lines,
      "% ---- Peters' small-study test ----",
      paste0("\\newcommand{\\PetersEligible}{", n_elig, XS, "}"),
      paste0("\\newcommand{\\PetersCellsTotal}{", nrow(fe), XS, "}"),
      paste0("\\newcommand{\\PetersFinite}{", n_finite, XS, "}"),
      "")
  }
}

nc <- safe_read("nc_exclusion_sensitivity.rds")
if (!is.null(nc) && nrow(nc) > 0) {
  ocol <- intersect(c("outcome"), names(nc))
  dcol <- intersect(c("delta_pp", "delta"), names(nc))
  ncol_drop <- intersect(c("n_patients_dropped", "patients_dropped", "n_dropped"),
                         names(nc))
  if (length(ocol) > 0 && length(dcol) > 0) {
    lines <- c(lines, "% ---- population-eligibility sensitivity ----")
    for (i in seq_len(nrow(nc))) {
      stem2 <- paste0("NcSens", despecialise(camel(nc[[ocol[1]]][i])))
      d <- nc[[dcol[1]]][i]
      lines <- c(lines,
        paste0("\\newcommand{\\", stem2, "Delta}{",
               sprintf("%+.1f", d), "}"),
        paste0("\\newcommand{\\", stem2, "DeltaAbs}{", sprintf("%.1f", abs(d)), "}"))
      if (length(ncol_drop) > 0) {
        lines <- c(lines, paste0("\\newcommand{\\", stem2, "Dropped}{",
                                 nc[[ncol_drop[1]]][i], "}"))
      }
    }
    lines <- c(lines, "")
  }
}

# ---- GRADE ------------------------------------------------------------------
# The manuscript stated the structural minimum as three against a table showing
# four, named the wrong cells as minimally downgraded, and described a
# risk-of-bias rule the code does not implement. Emit the counts.
gc <- safe_read("grade_counts.rds")
gp <- safe_read("grade_profile.rds")
if (!is.null(gc)) {
  lines <- c(lines, "% ---- GRADE ----",
    paste0("\\newcommand{\\GradeCells}{", gc$n_cells, XS, "}"),
    paste0("\\newcommand{\\GradeStructuralMinimum}{", gc$structural_minimum_downgrades, XS, "}"),
    paste0("\\newcommand{\\GradeMinDowngrades}{", gc$min_downgrades, XS, "}"),
    paste0("\\newcommand{\\GradeCellsAtMin}{", gc$n_min_downgrades, XS, "}"),
    paste0("\\newcommand{\\GradeMaxDowngrades}{", gc$max_downgrades, XS, "}"),
    paste0("\\newcommand{\\GradeCellsAtMax}{", gc$n_max_downgrades, XS, "}"),
    paste0("\\newcommand{\\GradeClinicalSuccessCells}{", gc$n_clinical_success, "}"))
  if (!is.null(gp)) {
    # Every cell's risk-of-bias deduction is identical by construction; state
    # the constant so the text can say so without typing it.
    lines <- c(lines,
      paste0("\\newcommand{\\GradeRobDrop}{", unique(gp$rob_drop)[1], XS, "}"),
      paste0("\\newcommand{\\GradeRobIsUniform}{",
             if (length(unique(gp$rob_drop)) == 1L) "yes" else "no", "}"))
  }
  lines <- c(lines, "")
}

tr <- safe_read("threshold_relaxation_appendix.rds")
if (!is.null(tr)) {
  lines <- c(lines, "% ---- threshold relaxation ----",
    paste0("\\newcommand{\\RelaxNewlyPoolable}{", sum(tr$newly_poolable, na.rm = TRUE), XS, "}"),
    paste0("\\newcommand{\\RelaxNotEligible}{",
           sum(tr$status_relaxed == "NOT_ELIGIBLE", na.rm = TRUE), "}"),
    "")
}

# ---- falsification and small-study test statistics --------------------------
# The last numeric literals in the prose: Peters' p-values, the publication-year
# trend, and the Hartung-Knapp inflation ratio. Each was typed.
if (!is.null(fe) && "peters_pval" %in% names(fe)) {
  short <- c(clinical_success__overall = "Cs", safety__overall = "Saf",
             eradication__overall = "Erad", mortality__overall = "Mort")
  lines <- c(lines, "% ---- Peters' p-values ----")
  for (i in seq_len(nrow(fe))) {
    # [[ ]] on a named vector errors for an absent key rather than returning
    # NULL, and most strata are not in this lookup by design.
    key <- fe$stratum[i]
    if (!key %in% names(short)) next
    nm <- unname(short[key])
    pv <- fe$peters_pval[i]
    if (!is.finite(pv)) next
    lines <- c(lines, paste0("\\newcommand{\\Peters", nm, "P}{", sprintf("%.2f", pv), "}"))
  }
  lines <- c(lines, "")
}

yt <- safe_read("falsification_year_trend.rds")
if (!is.null(yt) && identical(yt$status, "FITTED")) {
  lines <- c(lines, "% ---- publication-year trend ----",
    paste0("\\newcommand{\\YearTrendCoef}{", sprintf("%.3f", as.numeric(yt$coef_year)), "}"),
    paste0("\\newcommand{\\YearTrendSE}{", sprintf("%.3f", as.numeric(yt$se_year)), "}"),
    paste0("\\newcommand{\\YearTrendP}{", sprintf("%.2f", as.numeric(yt$pval_year)), "}"),
    "")
}

# The t quantile the reported intervals actually use, and the normal quantile
# they are compared against. The t value depends on the degrees of freedom, so
# typing it fixes a number that moves whenever the corpus does.
cs <- pooled[["clinical_success__overall"]]
if (!is.null(cs$primary$df.random) && is.finite(cs$primary$df.random)) {
  dfr <- cs$primary$df.random
  lines <- c(lines, "% ---- interval quantiles ----",
    paste0("\\newcommand{\\TQuantile}{", sprintf("%.3f", qt(0.975, dfr)), "}"),
    paste0("\\newcommand{\\TQuantileDf}{", dfr, "}"),
    paste0("\\newcommand{\\ZQuantile}{", sprintf("%.3f", qnorm(0.975)), "}"),
    "")
}

hk <- safe_read("hk_binding_check.rds")
if (!is.null(hk) && "hk_inflation_ratio" %in% names(hk)) {
  r <- hk$hk_inflation_ratio
  lines <- c(lines, "% ---- Hartung-Knapp binding diagnostic ----",
    paste0("\\newcommand{\\HkCellsAtUnity}{", sum(abs(r - 1) < 1e-6, na.rm = TRUE), "}"),
    paste0("\\newcommand{\\HkCellsTotal}{", nrow(hk), "}"),
    paste0("\\newcommand{\\HkMaxRatio}{", sprintf("%.2f", max(r, na.rm = TRUE)), "}"),
    "")
}

# ---- geographic-concentration and de-duplication sensitivity -----------------
# Both passages quoted before-and-after pairs from the round-4 corpus. Emitting
# them means the pair moves together when the corpus does, instead of one half
# going stale.
geo <- safe_read("geo_concentration_sensitivity.rds")
if (!is.null(geo)) {
  sh <- c(clinical_success = "Cs", safety = "Saf", eradication = "Erad", mortality = "Mort")
  lines <- c(lines, "% ---- geographic-concentration exclusion ----")
  for (i in seq_len(nrow(geo))) {
    k <- geo$outcome[i]
    if (!k %in% names(sh)) next
    nm <- unname(sh[k])
    lines <- c(lines,
      paste0("\\newcommand{\\Geo", nm, "Full}{", pct(geo$p_hat_full[i]), "}"),
      paste0("\\newcommand{\\Geo", nm, "Excl}{", pct(geo$p_hat_excl[i]), "}"),
      paste0("\\newcommand{\\Geo", nm, "ExclN}{", geo$n_patients_excl[i], "}"))
  }
  lines <- c(lines, "")
}

dd <- safe_read("dedup_sensitivity.rds")
if (!is.null(dd)) {
  sh <- c(clinical_success = "Cs", safety = "Saf", eradication = "Erad", mortality = "Mort")
  lines <- c(lines, "% ---- de-duplication restore-both sensitivity ----")
  for (i in seq_len(nrow(dd))) {
    k <- dd$outcome[i]
    if (!k %in% names(sh)) next
    nm <- unname(sh[k])
    lines <- c(lines,
      paste0("\\newcommand{\\Dedup", nm, "Applied}{", pct(dd$p_hat_applied[i]), "}"),
      paste0("\\newcommand{\\Dedup", nm, "Restored}{", pct(dd$p_hat_restored[i]), "}"))
  }
  lines <- c(lines,
    paste0("\\newcommand{\\DedupMaxShiftPP}{",
           sprintf("%.1f", max(abs(dd$delta_pp), na.rm = TRUE)), "}"),
    "")
}

# ---- resistance-classification provenance ------------------------------------
# How many MDR / XDR calls this review re-derived from a published antibiogram
# rather than adopting the source's own label. The prose quoted four and three of
# four; the round-5 additions moved both, and the claim is load-bearing because
# it is what the classification-restriction sensitivity analysis turns on.
for (cls in c("MDR", "XDR", "PDR")) {
  sel <- dat$resistance_class == cls
  if (!any(sel)) next
  lines <- c(lines,
    paste0("\\newcommand{\\Res", cls, "Verified}{",
           sum(sel & dat$resistance_class_source == "independently-verified",
               na.rm = TRUE), "}"),
    paste0("\\newcommand{\\Res", cls, "Authored}{",
           sum(sel & dat$resistance_class_source == "author-reported",
               na.rm = TRUE), "}"))
}
lines <- c(lines, "")

# ---- eradication by site class ----------------------------------------------
# The quantity that settles whether pooled eradication is one construct. Emitted
# per class so the manuscript can report the split rather than assert coherence.
es <- safe_read("eradication_site_split.rds")
if (!is.null(es)) {
  for (sp in list(c("Full", "full"), c("Air", "chronic_airway"), c("Other", "other_site"))) {
    r <- es[[sp[2]]]
    if (is.null(r)) next
    lines <- c(lines,
      paste0("\\newcommand{\\Erad", sp[1], "Est}{", sprintf("%.1f", 100 * r$p_hat), "\\%}"),
      paste0("\\newcommand{\\Erad", sp[1], "CI}{95\\% CI ",
             sprintf("%.1f", 100 * r$ci_low), "\\%--",
             sprintf("%.1f", 100 * r$ci_high), "\\%}"),
      paste0("\\newcommand{\\Erad", sp[1], "Tau}{", sprintf("%.3f", r$tau2), "}"),
      paste0("\\newcommand{\\Erad", sp[1], "Arms}{", r$k_arms, "}"),
      paste0("\\newcommand{\\Erad", sp[1], "K}{", r$k_studies, "}"),
      paste0("\\newcommand{\\Erad", sp[1], "N}{", r$n_patients, "}"),
      paste0("\\newcommand{\\Erad", sp[1], "Events}{", r$n_events, "}"))
  }
  lines <- c(lines, "")
}

# ---- journal-tier falsification check ---------------------------------------
# The Results quoted 79.6% (8 studies) against 69.2% (12 studies) and called the
# gap "roughly 10 percentage points". A round-5 referee showed the arithmetic did
# not hold; the corpus has since moved twice more. Derive it.
jt <- safe_read("falsification_journal_tier.rds")
if (!is.null(jt) && "journal_tier_simple" %in% names(jt)) {
  for (i in seq_len(nrow(jt))) {
    lab <- if (grepl("^high", jt$journal_tier_simple[i])) "High" else
           if (grepl("^mid", jt$journal_tier_simple[i])) "Mid" else NA
    if (is.na(lab)) next
    lines <- c(lines,
      paste0("\\newcommand{\\JournalTier", lab, "Prop}{",
             sprintf("%.1f", 100 * jt$crude_proportion[i]), "\\%}"),
      paste0("\\newcommand{\\JournalTier", lab, "K}{", jt$k_studies[i], "}"))
  }
  hi <- jt$crude_proportion[grepl("^high", jt$journal_tier_simple)]
  mi <- jt$crude_proportion[grepl("^mid", jt$journal_tier_simple)]
  if (length(hi) && length(mi)) {
    lines <- c(lines, paste0("\\newcommand{\\JournalTierGapPP}{",
                             sprintf("%.1f", 100 * (hi[1] - mi[1])), "}"))
  }
  lines <- c(lines, "")
}

# ---- single-source dominance of the MDR stratum ------------------------------
# The Discussion quoted Pirnay's share of the MDR pools as 62% and 53%. Both were
# from a superseded corpus; both are the load-bearing numbers in the paragraph
# that concedes single-cohort dependence, so they must move with the data.
for (sp in list(c("Cs", "clinical_success_n"), c("Erad", "microbio_eradication_n"))) {
  col <- sp[2]
  if (!col %in% names(dat)) next
  sel <- dat$resistance_class == "MDR" & !is.na(dat[[col]])
  tot <- sum(dat$n_arm[sel], na.rm = TRUE)
  pir <- sum(dat$n_arm[sel & dat$study_id == "Pirnay2024"], na.rm = TRUE)
  if (tot == 0) next
  lines <- c(lines,
    paste0("\\newcommand{\\PirnayShareMDR", sp[1], "}{",
           sprintf("%.0f", 100 * pir / tot), "\\%}"),
    paste0("\\newcommand{\\PirnayNMDR", sp[1], "}{", pir, "}"),
    paste0("\\newcommand{\\PoolNMDR", sp[1], "}{", tot, "}"))
}
lines <- c(lines, "")

# ---- leave-one-out sensitivity ----------------------------------------------
# The Discussion asserted that removing Pirnay OR Jault collapses several cells,
# including a not-classifiable MORTALITY estimate. Jault is excluded from pooling
# and appears nowhere in the leave-one-out; the not-classifiable mortality cell
# does not pool. Derive the actual result so the sentence cannot drift again.
loo <- safe_read("leave_one_out.rds")
if (!is.null(loo) && "shift_outside_full_ci" %in% names(loo)) {
  flagged <- loo[loo$shift_outside_full_ci %in% TRUE, , drop = FALSE]
  studies <- sort(unique(flagged$dropped_study))
  lines <- c(lines, "% ---- leave-one-out ----",
    paste0("\\newcommand{\\LooSensitiveCells}{", nrow(flagged), "}"),
    paste0("\\newcommand{\\LooSensitiveStudies}{", length(studies), "}"),
    paste0("\\newcommand{\\LooDominantStudy}{",
           if (length(studies) == 1) studies[1] else paste(studies, collapse = ", "), "}"),
    "")
}

# ---- DTR adjudicability -----------------------------------------------------
# The corrected Kadri criterion makes DTR-negative reachable, so the axis now has
# an adjudicable total rather than only a positive count.
if ("dtr_status" %in% names(dat)) {
  n_yes <- sum(dat$dtr_status == "yes", na.rm = TRUE)
  n_no  <- sum(dat$dtr_status == "no", na.rm = TRUE)
  lines <- c(lines, "% ---- DTR adjudicability ----",
    paste0("\\newcommand{\\DtrAdjudicable}{", n_yes + n_no, "}"), "")
}

# ---- follow-up horizon spread -----------------------------------------------
# The quantity a referee asked to be made visible: clinical success is counted
# over windows ranging from days to years, and most arms state no window at all.
fus <- safe_read("followup_spread.rds")
if (!is.null(fus)) {
  fmt_fu <- function(d) {
    if (is.na(d)) return("not stated")
    if (d < 14) return(sprintf("%.0f days", d))
    if (d < 60) return(sprintf("%.0f weeks", d / 7))
    if (d < 730) return(sprintf("%.0f months", d / 30.44))
    sprintf("%.0f years", d / 365.25)
  }
  lines <- c(lines, "% ---- follow-up horizon ----",
    paste0("\\newcommand{\\FollowUpStated}{", fus$n_stated, "}"),
    paste0("\\newcommand{\\FollowUpNotStated}{", fus$n_not_stated, "}"),
    paste0("\\newcommand{\\FollowUpMin}{", fmt_fu(fus$min_days), "}"),
    paste0("\\newcommand{\\FollowUpMax}{", fmt_fu(fus$max_days), "}"),
    paste0("\\newcommand{\\FollowUpFold}{", sprintf("%.0f", fus$fold_range), "}"),
    "")
}

# ---- PRISMA channel itemisation ---------------------------------------------
# The flow diagram printed \PrismaItemised and then hard-typed a breakdown beside
# it. The macro tracked the pipeline; the typed list did not. Round 5 added two
# channels (3 referee-named + 14 un-blocked PubMed) to 14_prisma_counts.R and the
# tikz node was never updated, so the figure asserted 57 and itemised 40 in the
# same sentence -- a 17-record contradiction inside the one figure every referee
# checks with a calculator. Emitting the list from the same object that computes
# the total makes the two incapable of disagreeing.
pc <- safe_read("prisma_counts.rds")
if (!is.null(pc)) {
  ch <- pc$channels
  parts <- paste0(unname(ch), " ", names(ch))
  listing <- paste(parts, collapse = " $+$ ")
  # Assert before emitting: the printed list must sum to the printed total.
  if (sum(ch) != pc$itemised) {
    stop(sprintf("PRISMA channel list sums to %d but itemised total is %d",
                 sum(ch), pc$itemised))
  }
  lines <- c(lines, "% ---- PRISMA channel itemisation ----",
    paste0("\\newcommand{\\PrismaChannelList}{", listing, "}"),
    paste0("\\newcommand{\\PrismaChannelCount}{", length(ch), "}"),
    "")
}

# ---- phage-susceptibility reporting -----------------------------------------
# The review made in-vitro activity an eligibility criterion (Onsea 2019 was
# excluded on it) and then never recorded it. This is how often the primary
# sources say whether the administered phage could lyse the organism at all.
psr <- safe_read("phage_susceptibility_reporting.rds")
if (!is.null(psr)) {
  lines <- c(lines, "% ---- phage-susceptibility reporting ----",
    paste0("\\newcommand{\\PhageSuscArms}{", psr$n_arms, "}"),
    paste0("\\newcommand{\\PhageSuscDocumented}{", psr$n_tested_documented, "}"),
    paste0("\\newcommand{\\PhageSuscSilent}{", psr$n_silent, "}"),
    paste0("\\newcommand{\\PhageSuscSilentPct}{",
           pct(psr$n_silent / psr$n_arms, 0), "}"),
    "")
}

# ---- risk-of-bias distribution ----------------------------------------------
# Through round 4 every arm rated High overall and the prose said so. The
# round-5 phage-monotherapy arms rate Moderate on causality -- there is no
# co-intervention to separate the effect from -- and therefore Moderate overall,
# so the domain is no longer uniform and the GRADE deduction now discriminates.
# Every per-domain count the prose quotes is emitted here.
rob <- safe_read("rob_per_arm.rds")
if (!is.null(rob)) {
  lines <- c(lines, "% ---- risk of bias, per-domain distribution ----")
  for (dom in c("selection", "ascertainment", "causality", "reporting", "overall")) {
    if (!dom %in% names(rob)) next
    stem2 <- paste0("Rob", camel(dom))
    for (lv in c("High", "Moderate", "Low")) {
      lines <- c(lines, paste0("\\newcommand{\\", stem2, lv, "}{",
                               sum(rob[[dom]] == lv, na.rm = TRUE), "}"))
    }
  }
  lines <- c(lines, "")
}

# ---- cluster-robust variance check ------------------------------------------
# The Results quote naive-vs-RVE standard errors for two cells. Both moved when
# the corpus grew, and the DIRECTION of the comparison moved with them, which is
# the part a reader reasons from.
rv <- safe_read("rve_clustering_check.rds")
if (!is.null(rv)) {
  short_rv <- c(clinical_success__overall = "Cs", safety__overall = "Saf",
                eradication__overall = "Erad", mortality__overall = "Mort")
  lines <- c(lines, "% ---- cluster-robust variance ----")
  for (i in seq_len(nrow(rv))) {
    key <- rv$stratum[i]
    if (!key %in% names(short_rv)) next
    nm <- unname(short_rv[key])
    lines <- c(lines,
      paste0("\\newcommand{\\Rve", nm, "Naive}{", sprintf("%.3f", rv$se_naive[i]), "}"),
      paste0("\\newcommand{\\Rve", nm, "Robust}{", sprintf("%.3f", rv$se_rve[i]), "}"),
      paste0("\\newcommand{\\Rve", nm, "Df}{", sprintf("%.1f", rv$satterthwaite_df[i]), "}"))
  }
  lines <- c(lines, "")
}

pc <- safe_read("prisma_counts.rds")
if (!is.null(pc)) {
  lines <- c(lines, "% ---- PRISMA flow ----",
    paste0("\\newcommand{\\PrismaAssessed}{", pc$assessed, "}"),
    paste0("\\newcommand{\\PrismaExcluded}{", pc$excluded, "}"),
    paste0("\\newcommand{\\PrismaIncludedStudies}{", pc$included_studies, "}"),
    paste0("\\newcommand{\\PrismaIncludedArms}{", pc$included_arms, "}"),
    paste0("\\newcommand{\\PrismaPooledStudies}{", pc$pooled_studies, "}"),
    paste0("\\newcommand{\\PrismaPooledArms}{", pc$pooled_arms, "}"),
    paste0("\\newcommand{\\PrismaItemised}{", pc$itemised, "}"),
    paste0("\\newcommand{\\PrismaShortfall}{", pc$channel_shortfall, "}"),
    "")
}

# ---- exact bounds for zero-event route cells --------------------------------
# A zero-event cell has no informative pooled proportion, so the text reports an
# exact one-sided Clopper-Pearson bound instead. The bound depends on the
# denominator, and the manuscript previously quoted one computed for a
# denominator the corpus does not have. Emitting it from the data removes that
# possibility.
for (rg in unique(dat$route_group)) {
  sub <- dat[dat$route_group == rg, ]
  ok <- !is.na(sub$mortality_n)
  if (!any(ok)) next
  deaths <- sum(sub$mortality_n[ok])
  n <- sum(sub$n_arm[ok])
  if (deaths != 0 || n == 0) next
  stem <- paste0("MortZero", despecialise(camel(rg)))
  lines <- c(lines,
    paste0("\\newcommand{\\", stem, "N}{", n, "}"),
    paste0("\\newcommand{\\", stem, "Arms}{", sum(ok), "}"),
    paste0("\\newcommand{\\", stem, "CPupper}{", pct(1 - 0.025^(1 / n)), "}"))
}
lines <- c(lines, "")

# Arm distribution by stratum -- the §4.2 counts that summed to 30 not 31.
# Levels must sum to the corpus size. Dropping NA silently would understate the
# denominator, which is precisely how §4.2's route counts came to sum to 30
# against a 31-arm corpus. An arm with no recorded level is a real arm and gets
# its own "NotReported" macro; the total is then asserted.
dist_macro <- function(prefix, column) {
  if (!column %in% names(dat)) return(character(0))
  v <- dat[[column]]
  v[is.na(v) | !nzchar(trimws(as.character(v)))] <- "not reported"
  tb <- table(v)
  out <- character(0)
  for (lv in names(tb)) {
    out <- c(out, paste0("\\newcommand{\\", prefix, despecialise(camel(lv)),
                         "Arms}{", as.integer(tb[[lv]]), "}"))
  }
  if (sum(tb) != nrow(dat)) {
    stop(sprintf("dist_macro(%s): levels sum to %d but the corpus has %d arms",
                 column, sum(tb), nrow(dat)))
  }
  out
}
lines <- c(lines, "% ---- arm distribution by stratum ----",
           dist_macro("Res", "resistance_class"),
           dist_macro("Route", "route_group"),
           dist_macro("Dtr", "dtr_status"),
           dist_macro("Mod", "modality_group"),
           "")

# ---- corpus-composition scalars the prose quotes -----------------------------
# Every one of these was a typed literal that the round-5 additions falsified.
# They are derived here so the next corpus change cannot leave them stale.
n_arms <- nrow(dat)
n_pat <- sum(dat$n_arm, na.rm = TRUE)
nc_arms <- sum(dat$resistance_class == "not-classifiable", na.rm = TRUE)
nc_pat <- sum(dat$n_arm[dat$resistance_class == "not-classifiable"], na.rm = TRUE)
single <- dat$n_arm == 1

# The three largest contributing studies, by patients. The prose named Pirnay,
# Onallah and Chan and asserted 56 patients; both the identity and the total
# have to follow the data.
by_study <- sort(tapply(dat$n_arm, dat$study_id, sum, na.rm = TRUE), decreasing = TRUE)
top3 <- head(by_study, 3)

lines <- c(lines, "% ---- corpus composition ----",
  paste0("\\newcommand{\\ResClassifiedArms}{", n_arms - nc_arms, "}"),
  paste0("\\newcommand{\\ResNotClassifiablePatients}{", nc_pat, "}"),
  paste0("\\newcommand{\\ResNotClassifiablePct}{",
         sprintf("%.0f", 100 * nc_pat / n_pat), "\\%}"),
  paste0("\\newcommand{\\SinglePatientPatients}{", sum(dat$n_arm[single], na.rm = TRUE), "}"),
  paste0("\\newcommand{\\MultiPatientPatients}{", sum(dat$n_arm[!single], na.rm = TRUE), "}"),
  paste0("\\newcommand{\\TopThreeStudiesPatients}{", sum(top3), "}"),
  paste0("\\newcommand{\\LargestArmSize}{", max(dat$n_arm, na.rm = TRUE), "}"),
  "")

# Outcome-reporting completeness: how many arms report each secondary outcome.
report_macro <- function(col, stem2) {
  if (!col %in% names(dat)) return(character(0))
  n_rep <- sum(!is.na(dat[[col]]))
  n_ev <- sum(dat[[col]], na.rm = TRUE)
  # The EVENT count among arms that actually assessed the outcome. Reporting only
  # the reporting RATE hid the substantive quantity: a round-6 referee pointed
  # out that where investigators looked for phage resistance, roughly half found
  # it -- a statement about phage therapy, not merely about publication practice.
  c(paste0("\\newcommand{\\", stem2, "Reported}{", n_rep, "}"),
    paste0("\\newcommand{\\", stem2, "Silent}{", n_arms - n_rep, "}"),
    paste0("\\newcommand{\\", stem2, "Events}{", n_ev, "}"),
    paste0("\\newcommand{\\", stem2, "EventPct}{",
           if (n_rep > 0) sprintf("%.0f\\%%", 100 * n_ev / n_rep) else "n/a", "}"))
}
lines <- c(lines, "% ---- secondary-outcome reporting completeness ----",
           report_macro("resistance_emergence_n", "ResistEmergence"),
           report_macro("los_days", "Los"),
           "")

# Single-patient arms: quoted as both 19 and 24 in different sections.
if ("n_arm" %in% names(dat)) {
  lines <- c(lines,
    paste0("\\newcommand{\\SinglePatientArms}{",
           sum(dat$n_arm == 1, na.rm = TRUE), "}"),
    paste0("\\newcommand{\\MultiPatientArms}{",
           sum(dat$n_arm > 1, na.rm = TRUE), "}"),
    "")
}

# Normalise xspace in ONE place rather than at each emission site. Macros are
# written by several code paths (per-cell, stratum distributions, zero-event
# bounds, GRADE, Peters', relaxation) and patching each one leaves gaps -- it
# left 36 of 354 without xspace on the first attempt, which typesets as
# "5cells". Enforce the invariant on the finished output instead.
XS_RE <- "\\\\xspace\\}$"
lines <- vapply(lines, function(ln) {
  if (!grepl("^\\\\newcommand\\{", ln)) return(ln)
  if (grepl(XS_RE, ln)) return(ln)
  # Build by string surgery, not sub(): a backslash in sub()'s replacement is
  # an escape character, so paste0(XS, "}") as a replacement silently drops it.
  paste0(substr(ln, 1, nchar(ln) - 1), XS, "}")
}, character(1), USE.NAMES = FALSE)

n_cmd <- sum(grepl("^\\\\newcommand\\{", lines))
n_xs <- sum(grepl("^\\\\newcommand\\{.*\\\\xspace\\}$", lines))
if (n_cmd != n_xs) {
  stop(sprintf("xspace invariant violated: %d macros, %d carry xspace", n_cmd, n_xs))
}

writeLines(lines, target)

cat("Wrote", target, "\n")
cat("  pooled cells with macros :", n_pooled, "of", n_cells_total, "\n")
cat("  macro stems              :", paste(sort(emitted), collapse = ", "), "\n")
