# ==============================================================================
# 11_manifest.R
# Purpose: Emit EVERY scalar the manuscript quotes into one machine-written,
#          human-readable file. The manuscript must quote only from this file.
#
#          WHY THIS EXISTS. Round-3 peer review returned Reject from both
#          referees, converging independently on the same finding: the prose did
#          not match the generated tables. Roughly a dozen quantities disagreed,
#          the corpus size was stated five different ways, and paragraphs
#          described pooled cells that no longer existed. The cause was
#          mechanical: the corpus changed several times and the prose was
#          updated by hand-listed string replacement each time, so anything not
#          on the list silently went stale.
#
#          The one part of the pipeline that did NOT drift was the GRADE counts,
#          because 10_grade.R emits them rather than leaving them to prose. This
#          script generalises that pattern to every reported scalar.
#
#          RULE FOR AUTHORS: if a number appears in main.tex or sections/*.tex,
#          it must appear here first. If it is not here, it is not quotable.
#
# Project: phage_therapy_mdr_pseudomonas
# Inputs:  scripts/R/output/*.rds (all pipeline outputs)
# Outputs: quality_reports/manuscript_scalars_phage_therapy_mdr_pseudomonas.md
# Requires: 01_setup.R through 10_grade.R have been run
# ==============================================================================

dat_analysis   <- readRDS(file.path(output_dir, "dat_analysis.rds"))
exclusion_log  <- readRDS(file.path(output_dir, "exclusion_log.rds"))
pooled_results <- readRDS(file.path(output_dir, "pooled_results.rds"))
grade_profile  <- readRDS(file.path(output_dir, "grade_profile.rds"))
grade_counts   <- readRDS(file.path(output_dir, "grade_counts.rds"))
dat_raw_all    <- readr::read_csv(data_path, show_col_types = FALSE)

#' Read an optional pipeline output without aborting the manifest.
#' Robustness/falsification artefacts are written by scripts that can legitimately
#' skip a check; a missing file is reported as such rather than crashing.
safe_read <- function(name) {
  f <- file.path(output_dir, name)
  if (file.exists(f)) readRDS(f) else NULL
}

fmt_pct <- function(x, d = 1) if (is.null(x) || is.na(x)) "n/a" else sprintf(paste0("%.", d, "f%%"), 100 * x)
fmt_num <- function(x, d = 3) if (is.null(x) || is.na(x)) "n/a" else sprintf(paste0("%.", d, "f"), x)

L <- c()
add <- function(...) L <<- c(L, paste0(...))

add("# Manuscript scalar manifest --- phage_therapy_mdr_pseudomonas")
add("")
add("MACHINE-WRITTEN by `scripts/R/11_manifest.R`. Do not edit by hand.")
add("")
add("Every number quoted in `paper/main.tex` or `paper/sections/*.tex` must appear")
add("in this file. A number that is not here is not quotable. Regenerate with")
add("`Rscript scripts/R/00_master.R` and re-check the manuscript against it.")
add("")
add("Generated: ", format(Sys.time(), "%Y-%m-%d %H:%M"), " | seed: ", SEED)
add("")

# --- Corpus -------------------------------------------------------------------
add("## 1. Corpus")
add("")
add("| Quantity | Value |")
add("|---|---|")
add("| Rows in cleaned extraction dataset (all arms) | ", nrow(dat_raw_all), " |")
add("| Studies in cleaned extraction dataset | ", length(unique(dat_raw_all$study_id)), " |")
add("| **Pooling-eligible study-arms** | **", nrow(dat_analysis), "** |")
add("| **Pooling-eligible studies** | **", length(unique(dat_analysis$study_id)), "** |")
add("| **Pooling-eligible patients** | **", sum(dat_analysis$n_arm, na.rm = TRUE), "** |")
add("| Single-patient arms | ", sum(dat_analysis$n_arm == 1, na.rm = TRUE), " |")
add("| Multi-patient arms | ", sum(dat_analysis$n_arm > 1, na.rm = TRUE), " |")
add("| Patients contributed by multi-patient arms | ", sum(dat_analysis$n_arm[dat_analysis$n_arm > 1], na.rm = TRUE), " |")
add("")

add("### 1.1 Exclusions (each with its own count)")
add("")
add("| Step | n |")
add("|---|---|")
for (i in seq_len(nrow(exclusion_log))) {
  add("| ", exclusion_log$step[i], " | ", exclusion_log$n_rows[i], " |")
}
add("")

add("### 1.2 Design, resistance and route distribution (pooling-eligible arms only)")
add("")
for (v in c("study_design", "resistance_class", "route_group", "modality_group")) {
  add("**", v, "**")
  add("")
  add("| Level | Arms | Studies | Patients |")
  add("|---|---|---|---|")
  for (lv in sort(unique(as.character(dat_analysis[[v]])), na.last = TRUE)) {
    sub <- if (is.na(lv)) dat_analysis[is.na(dat_analysis[[v]]), ] else dat_analysis[!is.na(dat_analysis[[v]]) & dat_analysis[[v]] == lv, ]
    add("| ", ifelse(is.na(lv), "(not reported)", lv), " | ", nrow(sub), " | ",
        length(unique(sub$study_id)), " | ", sum(sub$n_arm, na.rm = TRUE), " |")
  }
  add("")
}

# --- Pooled cells -------------------------------------------------------------
pooled_cells <- pooled_results[vapply(pooled_results, \(r) r$status == "POOLED", logical(1L))]
not_pooled   <- pooled_results[vapply(pooled_results, \(r) r$status != "POOLED", logical(1L))]

add("## 2. Pooled outcome-stratum cells")
add("")
add("| Quantity | Value |")
add("|---|---|")
add("| **Pooled cells** | **", length(pooled_cells), "** |")
add("| **Not-pooled cells** | **", length(not_pooled), "** |")
add("| Total estimated cells | ", length(pooled_results), " |")
add("")
add("| Cell | k studies | k arms | N | Estimate | 95% CI | tau2 | 95% PI | CI width (pp) |")
add("|---|---|---|---|---|---|---|---|---|")
for (r in pooled_cells) {
  p  <- backtransform_prop(r$primary$TE.random, sm = r$primary$sm)
  lo <- backtransform_prop(r$primary$lower.random, sm = r$primary$sm)
  hi <- backtransform_prop(r$primary$upper.random, sm = r$primary$sm)
  has_pi <- !is.null(r$primary$lower.predict) && is.finite(r$primary$lower.predict)
  pil <- if (has_pi) backtransform_prop(r$primary$lower.predict, sm = r$primary$sm) else NA_real_
  pih <- if (has_pi) backtransform_prop(r$primary$upper.predict, sm = r$primary$sm) else NA_real_
  add("| ", r$stratum, " | ", r$k_studies, " | ", r$k_arms, " | ", r$n_patients, " | ",
      fmt_pct(p), " | [", fmt_pct(lo), ", ", fmt_pct(hi), "] | ", fmt_num(r$primary$tau2),
      " | [", fmt_pct(pil), ", ", fmt_pct(pih), "] | ", sprintf("%.1f", 100 * (hi - lo)), " |")
}
add("")
add("### 2.1 Cells NOT pooled, with reason")
add("")
add("| Cell | k studies | k arms | N | Reason |")
add("|---|---|---|---|---|")
for (r in not_pooled) {
  reason <- if (!is.null(r$reason)) r$reason else r$status
  add("| ", r$stratum, " | ", r$k_studies, " | ", r$k_arms, " | ", r$n_patients, " | ", reason, " |")
}
add("")

# --- GRADE --------------------------------------------------------------------
add("## 3. GRADE")
add("")
add("| Quantity | Value |")
add("|---|---|")
add("| Cells rated | ", grade_counts$n_cells, " |")
add("| Certainty levels present | ", paste(sort(unique(grade_profile$certainty)), collapse = ", "), " |")
add("| Rating is deterministic (floors before data are read) | ", grade_counts$rating_is_deterministic, " |")
add("| Structural minimum downgrades | ", grade_counts$structural_minimum_downgrades, " |")
add("| Cells at the minimum (", grade_counts$min_downgrades, " downgrades) | ", grade_counts$n_min_downgrades, " |")
add("| ... which cells | ", paste(grade_counts$cells_at_min, collapse = "; "), " |")
add("| Cells at the maximum (", grade_counts$max_downgrades, " downgrades) | ", grade_counts$n_max_downgrades, " |")
add("| ... which cells | ", paste(grade_counts$cells_at_max, collapse = "; "), " |")
add("| Clinical-success cells | ", grade_counts$n_clinical_success, " |")
add("")

# --- Robustness ---------------------------------------------------------------
add("## 4. Robustness")
add("")

nc <- safe_read("nc_exclusion_sensitivity.rds")
if (!is.null(nc)) {
  add("### 4.1 Population-eligibility sensitivity (excluding not-classifiable arms)")
  add("")
  add("| Outcome | All arms | Classified-only | Delta (pp) | Patients dropped |")
  add("|---|---|---|---|---|")
  for (i in seq_len(nrow(nc))) {
    add("| ", nc$outcome[i], " | ", fmt_pct(nc$p_hat_all[i]), " | ", fmt_pct(nc$p_hat_classified[i]),
        " | ", sprintf("%+.1f", nc$delta_pp[i]), " | ", nc$n_patients_dropped[i], " |")
  }
  add("")
}

ts <- safe_read("transformation_sensitivity.rds")
if (!is.null(ts)) {
  add("### 4.2 Transformation / model sensitivity")
  add("")
  add("Rows: ", nrow(ts), ". Full comparison is in `paper/tables/.../meta_sensitivity.tex`.")
  add("")
}

rve <- safe_read("rve_clustering_check.rds")
if (!is.null(rve) && nrow(rve) > 0) {
  add("### 4.3 Cluster-robust variance check")
  add("")
  add("NOTE: fitted on an AUXILIARY normal-normal model, not the reported GLMM.")
  add("")
  add("| Cell | Clusters (m) | Satterthwaite df | Naive SE | RVE SE |")
  add("|---|---|---|---|---|")
  for (i in seq_len(nrow(rve))) {
    add("| ", rve$stratum[i], " | ", rve$n_clusters[i], " | ", fmt_num(rve$satterthwaite_df[i], 1),
        " | ", fmt_num(rve$se_naive[i]), " | ", fmt_num(rve$se_rve[i]), " |")
  }
  add("")
}

geo <- safe_read("geo_concentration_sensitivity.rds")
if (!is.null(geo)) {
  add("### 4.4 Geographic-concentration exclusion (Belgium/Israel removed)")
  add("")
  add("```")
  add(paste(utils::capture.output(print(as.data.frame(geo))), collapse = "\n"))
  add("```")
  add("")
}

# --- Falsification ------------------------------------------------------------
add("## 5. Falsification / small-study checks")
add("")
fe <- safe_read("funnel_eligibility.rds")
if (!is.null(fe)) {
  add("| Cell | k studies | Eligible (k >= ", MIN_STUDIES_FUNNEL, ") | Peters p |")
  add("|---|---|---|---|")
  for (i in seq_len(nrow(fe))) {
    add("| ", fe$stratum[i], " | ", fe$k_studies[i], " | ", fe$eligible[i], " | ",
        fmt_num(fe$peters_pval[i]), " |")
  }
  add("")
  add("Cells eligible for Peters' test: ", sum(fe$eligible, na.rm = TRUE),
      " of ", nrow(fe), ". Cells returning a finite p-value: ",
      sum(is.finite(fe$peters_pval)), ".")
  add("")
}

yt <- safe_read("falsification_year_trend.rds")
if (!is.null(yt)) {
  add("Publication-year trend (clinical success, logit scale): ",
      paste(utils::capture.output(print(unlist(yt))), collapse = " "))
  add("")
}

# --- Regressor degeneracy (reported as a power caveat, not a null result) ------
add("## 6. Test-power diagnostics")
add("")
n1 <- sum(dat_analysis$n_arm == 1, na.rm = TRUE)
add("Peters' regressor is 1/n. Arms with n = 1: ", n1, " of ", nrow(dat_analysis),
    " (", sprintf("%.0f%%", 100 * n1 / nrow(dat_analysis)),
    "), for which the regressor equals exactly 1. Distinct values of 1/n across ",
    "the corpus: ", length(unique(1 / dat_analysis$n_arm[!is.na(dat_analysis$n_arm)])), ".")
add("")

manifest_path <- file.path(
  here::here("quality_reports"),
  "manuscript_scalars_phage_therapy_mdr_pseudomonas.md"
)
writeLines(L, manifest_path)
message("11_manifest.R complete. Wrote ", manifest_path, " (", length(L), " lines).")
