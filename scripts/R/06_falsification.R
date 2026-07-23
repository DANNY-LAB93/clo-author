# ==============================================================================
# 06_falsification.R
# Purpose: Falsification / negative-control checks per
#          quality_reports/strategy/phage_therapy_mdr_pseudomonas/falsification_tests.md
#          -- adapted to the very small sample actually available:
#            Test 1: publication-year trend (meta-regression)
#            Test 2: journal-tier gradient (descriptive; formal Q-between
#                    not attempted where cell sizes are below MIN_STUDIES)
#            Test 3: small-study/sample-size effect (eyeball data)
#            Test 4: route x resistance_class x geographic_source cross-tab
#            Test 5: LOS vs. clinical-success non-mechanistic comparison --
#                    NOT_APPLICABLE in this corpus (only 1 of 16 arms reports
#                    los_days, below the minimum needed for even a qualitative
#                    directional comparison) -- stated explicitly, not silently
#                    skipped
#            Test 6: AE-rate-by-publication-year drift
#          Priority 5 #11 (robustness_plan.md): funnel/Egger's-Peters' test,
#          only where k_studies >= MIN_STUDIES_FUNNEL (pre-specified; not met
#          by any cell here -- stated explicitly, not silently skipped).
# Project: phage_therapy_mdr_pseudomonas
# Inputs:  scripts/R/output/dat_analysis.rds
#          scripts/R/output/pooled_results.rds
# Outputs: scripts/R/output/falsification_year_trend.rds
#          scripts/R/output/falsification_journal_tier.rds
#          scripts/R/output/falsification_small_study_data.rds
#          scripts/R/output/falsification_route_crosstab.rds
#          scripts/R/output/falsification_los_test5.rds
#          scripts/R/output/falsification_ae_year_trend.rds
#          scripts/R/output/funnel_eligibility.rds
# Requires: 01_setup.R, 02_data_preparation.R, 04_estimation.R have been run
# ==============================================================================

dat_analysis   <- readRDS(file.path(output_dir, "dat_analysis.rds"))
pooled_results <- readRDS(file.path(output_dir, "pooled_results.rds"))

# --- Test 1: publication-year trend (largest sufficiently-populated cell) -----
# The overall clinical-success cell is the largest POOLED cell available.
overall_success <- pooled_results[["clinical_success__overall"]]

year_trend <- if (!is.null(overall_success) && overall_success$status == "POOLED") {
  df_sub <- dat_analysis[!is.na(dat_analysis$clinical_success_n), ]
  mr <- tryCatch(
    metafor::rma(
      yi = metafor::escalc(measure = "PLO", xi = clinical_success_n, ni = n_arm, data = df_sub)$yi,
      vi = metafor::escalc(measure = "PLO", xi = clinical_success_n, ni = n_arm, data = df_sub)$vi,
      mods = ~publication_year, data = df_sub, method = "ML"
    ),
    error = function(e) {
      message("Publication-year meta-regression failed: ", conditionMessage(e))
      NULL
    }
  )
  if (is.null(mr)) {
    list(status = "FAILED", model = NULL)
  } else {
    list(
      status = "FITTED",
      coef_year = mr$b["publication_year", 1],
      se_year = mr$se[2],
      pval_year = mr$pval[2],
      model = mr
    )
  }
} else {
  list(status = "NOT_APPLICABLE", model = NULL)
}

if (identical(year_trend$status, "FITTED")) {
  message(
    "Publication-year trend (clinical success, logit scale): coef = ",
    round(year_trend$coef_year, 4), ", p = ", round(year_trend$pval_year, 3)
  )
}

# --- Test 2: journal-tier gradient (descriptive) --------------------------------
journal_tier_summary <- dat_analysis |>
  filter(!is.na(clinical_success_n)) |>
  group_by(journal_tier_simple) |>
  summarise(
    k_studies = length(unique(study_id)),
    n_patients = sum(n_arm),
    n_events = sum(clinical_success_n),
    crude_proportion = n_events / n_patients,
    .groups = "drop"
  ) |>
  arrange(desc(crude_proportion))

message("Journal-tier crude proportions (clinical success), descriptive only given small per-tier k:")
for (i in seq_len(nrow(journal_tier_summary))) {
  message(
    "  ", journal_tier_summary$journal_tier_simple[i], ": ",
    round(journal_tier_summary$crude_proportion[i], 3),
    " (k_studies = ", journal_tier_summary$k_studies[i], ")"
  )
}

# --- Test 3: small-study/sample-size effect (eyeball data) ----------------------
small_study_data <- dat_analysis |>
  filter(!is.na(clinical_success_n)) |>
  mutate(
    crude_proportion = clinical_success_n / n_arm,
    inv_sqrt_n = 1 / sqrt(n_arm)
  ) |>
  select(study_arm_id, n_arm, crude_proportion, inv_sqrt_n)

# --- Test 4: route x resistance_class x geographic_source cross-tab -----------
route_resistance_geo_crosstab <- dat_analysis |>
  count(route_group, resistance_class, geographic_region, name = "n_arms")

# Flag any route_group level effectively concentrated in a single geographic
# region (a "route effect" that is actually a center/case-mix signature).
route_geo_concentration <- dat_analysis |>
  group_by(route_group) |>
  summarise(
    n_regions = length(unique(geographic_region)),
    dominant_region_share = max(table(geographic_region)) / n(),
    .groups = "drop"
  ) |>
  mutate(single_center_signature = n_regions == 1L)

message("Route x geography concentration check:")
for (i in seq_len(nrow(route_geo_concentration))) {
  flag <- if (route_geo_concentration$single_center_signature[i]) " -- SINGLE-REGION SIGNATURE" else ""
  message(
    "  ", route_geo_concentration$route_group[i], ": ",
    route_geo_concentration$n_regions[i], " distinct region(s)", flag
  )
}

# --- Test 5: non-mechanistic outcome comparison (length of hospitalization) -----
# Should NOT show: LOS improving as dramatically as clinical success/eradication,
# if the success signal is phage-specific rather than a uniform salvage-population
# reporting-optimism artifact (falsification_tests.md Test 5).
n_los_nonNA <- sum(!is.na(dat_analysis$los_days))

los_falsification <- if (n_los_nonNA < 3L) {
  message(
    "Falsification Test 5 (LOS vs. clinical success): NOT_APPLICABLE -- only ",
    n_los_nonNA, " of ", nrow(dat_analysis),
    " arms report los_days (need >= 3 for any qualitative directional comparison). ",
    "Stated explicitly per falsification_tests.md rather than silently omitted."
  )
  list(status = "NOT_APPLICABLE", n_los_nonNA = n_los_nonNA, data = NULL)
} else {
  los_sub <- dat_analysis |>
    filter(!is.na(los_days), !is.na(clinical_success_n)) |>
    select(study_arm_id, los_days, clinical_success_n, n_arm)
  list(status = "DESCRIPTIVE_ONLY", n_los_nonNA = n_los_nonNA, data = los_sub)
}

# --- Test 6: AE-rate-by-publication-year drift ----------------------------------
overall_safety <- pooled_results[["safety__overall"]]

ae_year_trend <- if (!is.null(overall_safety) && overall_safety$status == "POOLED") {
  df_sub <- dat_analysis[!is.na(dat_analysis$adverse_event_n), ]
  es <- metafor::escalc(measure = "PLO", xi = adverse_event_n, ni = n_arm, data = df_sub)
  mr <- tryCatch(
    metafor::rma(yi, vi, mods = ~publication_year, data = es, method = "ML"),
    error = function(e) {
      message("AE-rate-by-year meta-regression failed: ", conditionMessage(e))
      NULL
    }
  )
  if (is.null(mr)) {
    list(status = "FAILED", model = NULL)
  } else {
    list(
      status = "FITTED",
      coef_year = mr$b["publication_year", 1],
      pval_year = mr$pval[2],
      model = mr
    )
  }
} else {
  list(status = "NOT_APPLICABLE", model = NULL)
}

# --- Priority 5 #11: funnel/Egger's-Peters' test, only where k_studies >= 10 ---
pooled_cells_all <- pooled_results[
  vapply(pooled_results, \(r) r$status == "POOLED", logical(1L))
]

funnel_eligibility <- purrr::map_dfr(pooled_cells_all, function(r) {
  eligible <- r$k_studies >= MIN_STUDIES_FUNNEL
  eggers <- NULL
  if (eligible) {
    eggers <- tryCatch(
      meta::metabias(r$primary, method.bias = "Egger"),
      error = function(e) {
        message("Egger's test failed for '", r$stratum, "': ", conditionMessage(e))
        NULL
      }
    )
  }
  tibble::tibble(
    stratum = r$stratum,
    k_studies = r$k_studies,
    eligible_for_funnel = eligible,
    eggers_pval = if (!is.null(eggers)) eggers$pval else NA_real_,
    eggers_statistic = if (!is.null(eggers)) eggers$statistic else NA_real_
  )
})

n_eligible <- sum(funnel_eligibility$eligible_for_funnel)
message(
  "Funnel/Egger's test eligibility (k_studies >= ", MIN_STUDIES_FUNNEL, "): ",
  n_eligible, " of ", nrow(funnel_eligibility), " POOLED cells qualify."
)
if (n_eligible == 0L) {
  message(
    "No cell meets the pre-specified k >= ", MIN_STUDIES_FUNNEL, " threshold -- ",
    "small-study-effect testing is NOT performed for any cell in this corpus, ",
    "stated explicitly per falsification_tests.md rather than silently omitted."
  )
} else {
  eligible_rows <- funnel_eligibility[funnel_eligibility$eligible_for_funnel, ]
  for (i in seq_len(nrow(eligible_rows))) {
    message(
      "  Egger's test, ", eligible_rows$stratum[i], ": p = ",
      round(eligible_rows$eggers_pval[i], 3)
    )
  }
}

# --- Save ------------------------------------------------------------------------
saveRDS(year_trend, file.path(output_dir, "falsification_year_trend.rds"))
saveRDS(journal_tier_summary, file.path(output_dir, "falsification_journal_tier.rds"))
saveRDS(small_study_data, file.path(output_dir, "falsification_small_study_data.rds"))
saveRDS(route_resistance_geo_crosstab, file.path(output_dir, "falsification_route_crosstab.rds"))
saveRDS(route_geo_concentration, file.path(output_dir, "falsification_route_geo_concentration.rds"))
saveRDS(los_falsification, file.path(output_dir, "falsification_los_test5.rds"))
saveRDS(ae_year_trend, file.path(output_dir, "falsification_ae_year_trend.rds"))
saveRDS(funnel_eligibility, file.path(output_dir, "funnel_eligibility.rds"))

message("06_falsification.R complete.")
