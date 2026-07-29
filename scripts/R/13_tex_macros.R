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
  c(paste0("\\newcommand{\\", stem2, "Reported}{", n_rep, "}"),
    paste0("\\newcommand{\\", stem2, "Silent}{", n_arms - n_rep, "}"))
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
