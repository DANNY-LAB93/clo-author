# ==============================================================================
# 05_robustness.R
# Purpose: Robustness checks per
#          quality_reports/strategy/phage_therapy_mdr_pseudomonas/robustness_plan.md
#          -- to the extent the small sample supports them:
#            Priority 1 #1:  transformation/model choice (GLMM vs FT vs logit-DL vs FE)
#            Priority 1 #2:  MDR/XDR classification sensitivity (independently-
#                             verified-only vs. all classification sources)
#            Priority 2 #4:  study-design-stratified sensitivity (RCT/cohort vs.
#                             case report/series), Q-between test
#            Priority 2 #5:  geographic-concentration exclusion (Belgium/Israel)
#            Priority 2 #6:  leave-one-out (study-level) for POOLED cells
#            Priority 3 #7:  route-collapsing sensitivity (systemic vs. local-only
#                             2-category taxonomy vs. the primary 4-category one)
#            Priority 3 #8:  Liu-reuse-tier transparency check (data_provenance)
#            Priority 4 #9:  HKSJ vs standard Wald CI width
#            Priority 4 #10: same-study multi-arm RVE clustering
#            Priority 5 #12: minimum-study-count threshold relaxation (appendix)
# Project: phage_therapy_mdr_pseudomonas
# Inputs:  scripts/R/output/dat_analysis.rds
#          scripts/R/output/pooled_results.rds
# Outputs: scripts/R/output/transformation_sensitivity.rds
#          scripts/R/output/classification_sensitivity.rds
#          scripts/R/output/study_design_subgroup_test.rds
#          scripts/R/output/geo_concentration_sensitivity.rds
#          scripts/R/output/leave_one_out.rds
#          scripts/R/output/route_2cat_sensitivity.rds
#          scripts/R/output/liu_reuse_tier_check.rds
#          scripts/R/output/hksj_vs_wald.rds
#          scripts/R/output/rve_clustering_check.rds
#          scripts/R/output/threshold_relaxation_appendix.rds
# Requires: 01_setup.R, 02_data_preparation.R, 04_estimation.R have been run
# ==============================================================================

dat_analysis   <- readRDS(file.path(output_dir, "dat_analysis.rds"))
pooled_results <- readRDS(file.path(output_dir, "pooled_results.rds"))

pooled_cells <- pooled_results[
  vapply(pooled_results, \(r) r$status == "POOLED", logical(1L))
]

# Top-level NULL/NA-safe accessor for a meta::metaprop() model's point estimate
# or CI bound. A cell whose GLMM and logit-DL both failed falls back to a
# fixed-effect model (pool_stratum()'s safe_metaprop() cascade); fixed-effect
# models expose TE.common/lower.common/upper.common, not the .random fields.
# Read .random when present and finite, else fall back to .common, else NA --
# so no NULL is ever passed to backtransform_prop() (which requires numeric).
te_random_or_common <- function(model, stem) {
  v <- model[[paste0(stem, ".random")]]
  if (is.null(v) || !is.finite(v)) v <- model[[paste0(stem, ".common")]]
  if (is.null(v) || !is.finite(v)) return(NA_real_)
  v
}
bt_safe <- function(model, stem, sm) {
  te <- te_random_or_common(model, stem)
  if (is.na(te)) NA_real_ else backtransform_prop(te, sm = sm)
}

# --- Priority 1 #1: transformation/model choice comparison --------------------
# Every POOLED cell already fit all four models in pool_stratum(). Extract
# back-transformed point estimates + 95% CIs side by side.
transformation_sensitivity <- purrr::map_dfr(pooled_cells, function(r) {
  n_harmonic <- 1 / mean(1 / r$glmm_raw$n)

  # NULL-safe extraction: pool_stratum()'s safe_metaprop() wrapper can return
  # NULL for any of the four models (near-degenerate cells, e.g. safety
  # strata with near-complete separation, can fail even the fixed-effect
  # sensitivity call) -- report NA rather than crash, per the same
  # capture-don't-crash contingency applied to the GLMM primary.
  safe_extract <- function(model, field, sm, n_harmonic = NULL) {
    if (is.null(model) || !is.finite(model[[field]])) return(NA_real_)
    if (is.null(n_harmonic)) {
      backtransform_prop(model[[field]], sm = sm)
    } else {
      backtransform_prop(model[[field]], sm = sm, n_harmonic = n_harmonic)
    }
  }

  glmm_p <- safe_extract(r$glmm_raw, "TE.random", "PLOGIT")

  tibble::tibble(
    stratum = r$stratum,
    k_studies = r$k_studies,
    n_patients = r$n_patients,
    model = c("GLMM (primary or NA if non-convergent)", "Freeman-Tukey double-arcsine DL",
              "Logit DerSimonian-Laird", "Fixed-effect (logit)"),
    p_hat = c(
      glmm_p,
      safe_extract(r$sens_ft, "TE.random", "PFT", n_harmonic),
      safe_extract(r$sens_logit_dl, "TE.random", "PLOGIT"),
      safe_extract(r$sens_fe, "TE.common", "PLOGIT")
    ),
    ci_low = c(
      safe_extract(r$glmm_raw, "lower.random", "PLOGIT"),
      safe_extract(r$sens_ft, "lower.random", "PFT", n_harmonic),
      safe_extract(r$sens_logit_dl, "lower.random", "PLOGIT"),
      safe_extract(r$sens_fe, "lower.common", "PLOGIT")
    ),
    ci_high = c(
      safe_extract(r$glmm_raw, "upper.random", "PLOGIT"),
      safe_extract(r$sens_ft, "upper.random", "PFT", n_harmonic),
      safe_extract(r$sens_logit_dl, "upper.random", "PLOGIT"),
      safe_extract(r$sens_fe, "upper.common", "PLOGIT")
    )
  )
})

# Flag cells where GLMM vs. double-arcsine point estimates diverge by more
# than 5-10 percentage points (memo Priority 1 #1 pre-specified threshold).
divergence_flags <- transformation_sensitivity |>
  filter(model %in% c("GLMM (primary or NA if non-convergent)", "Freeman-Tukey double-arcsine DL")) |>
  group_by(stratum) |>
  summarise(
    glmm_p = p_hat[model == "GLMM (primary or NA if non-convergent)"],
    ft_p   = p_hat[model == "Freeman-Tukey double-arcsine DL"],
    abs_diff_pp = abs(glmm_p - ft_p) * 100,
    # NA-safe: a fixed-effect fallback cell (GLMM and logit-DL both failed) has
    # no double-arcsine p_hat to compare against, so abs_diff_pp is NA -- treat
    # that as "not flagged" rather than letting NA propagate into the if() below.
    flagged_divergent = !is.na(abs_diff_pp) & abs_diff_pp > 5,
    .groups = "drop"
  )

message("Transformation-choice divergence (GLMM vs. double-arcsine), percentage points:")
for (i in seq_len(nrow(divergence_flags))) {
  diff_i <- divergence_flags$abs_diff_pp[i]
  message(
    "  ", divergence_flags$stratum[i], ": ",
    if (is.na(diff_i)) "n/a (fixed-effect fallback, no double-arcsine comparison)" else paste0(round(diff_i, 1), " pp"),
    if (isTRUE(divergence_flags$flagged_divergent[i])) " -- FLAGGED (>5pp)" else ""
  )
}

# --- Priority 2 #6: leave-one-out (study-level) --------------------------------
leave_one_out <- purrr::map_dfr(pooled_cells, function(r) {
  key <- r$stratum
  parts <- strsplit(key, "__")[[1]]
  outcome_name <- parts[1]
  event_col <- OUTCOME_COLS[[outcome_name]]

  # Reconstruct the exact eligible df for this cell by re-deriving the
  # filter used in 04_estimation.R (overall vs. subgroup key structure).
  if (length(parts) == 2L && parts[2] == "overall") {
    df_sub <- dat_analysis[!is.na(dat_analysis[[event_col]]), ]
  } else {
    strat_var <- parts[2]
    strat_level <- paste(parts[-c(1, 2)], collapse = "__")
    df_sub <- dat_analysis[
      !is.na(dat_analysis[[event_col]]) & !is.na(dat_analysis[[strat_var]]) & dat_analysis[[strat_var]] == strat_level,
    ]
  }

  studies <- unique(df_sub$study_id)

  full_p <- bt_safe(r$primary, "TE", r$primary$sm)

  purrr::map_dfr(studies, function(s) {
    df_loo <- df_sub[df_sub$study_id != s, ]
    if (length(unique(df_loo$study_id)) < 2L) {
      return(tibble::tibble(
        stratum = key, dropped_study = s, p_hat_loo = NA_real_,
        shift_outside_full_ci = NA
      ))
    }
    m_loo <- tryCatch(
      meta::metaprop(
        event = df_loo[[event_col]], n = df_loo$n_arm, studlab = df_loo$study_arm_id,
        sm = "PLOGIT", method = "GLMM", method.tau = "ML",
        method.random.ci = "HK", common = FALSE, random = TRUE
      ),
      error = function(e) NULL
    )
    p_loo <- if (!is.null(m_loo) && is.finite(m_loo$TE.random)) {
      backtransform_prop(m_loo$TE.random, sm = "PLOGIT")
    } else {
      NA_real_
    }
    full_ci_low  <- bt_safe(r$primary, "lower", r$primary$sm)
    full_ci_high <- bt_safe(r$primary, "upper", r$primary$sm)
    tibble::tibble(
      stratum = key,
      dropped_study = s,
      p_hat_loo = p_loo,
      shift_outside_full_ci = !is.na(p_loo) && !is.na(full_ci_low) && !is.na(full_ci_high) &&
        (p_loo < full_ci_low || p_loo > full_ci_high)
    )
  })
})

n_influential <- sum(leave_one_out$shift_outside_full_ci, na.rm = TRUE)
message(
  "Leave-one-out complete. Study-removals shifting the point estimate outside ",
  "the full-sample 95% CI: ", n_influential, " of ", nrow(leave_one_out)
)

# --- Priority 4 #9: HKSJ vs. standard Wald CI ------------------------------------
hksj_vs_wald <- purrr::map_dfr(pooled_cells, function(r) {
  key <- r$stratum
  parts <- strsplit(key, "__")[[1]]
  outcome_name <- parts[1]
  event_col <- OUTCOME_COLS[[outcome_name]]
  if (length(parts) == 2L && parts[2] == "overall") {
    df_sub <- dat_analysis[!is.na(dat_analysis[[event_col]]), ]
  } else {
    strat_var <- parts[2]
    strat_level <- paste(parts[-c(1, 2)], collapse = "__")
    df_sub <- dat_analysis[
      !is.na(dat_analysis[[event_col]]) & !is.na(dat_analysis[[strat_var]]) & dat_analysis[[strat_var]] == strat_level,
    ]
  }
  m_wald <- tryCatch(
    meta::metaprop(
      event = df_sub[[event_col]], n = df_sub$n_arm, studlab = df_sub$study_arm_id,
      sm = "PLOGIT", method = "GLMM", method.tau = "ML",
      method.random.ci = "classic", common = FALSE, random = TRUE
    ),
    error = function(e) NULL
  )
  hk_low  <- bt_safe(r$primary, "lower", r$primary$sm)
  hk_high <- bt_safe(r$primary, "upper", r$primary$sm)
  wald_low  <- if (!is.null(m_wald)) bt_safe(m_wald, "lower", "PLOGIT") else NA_real_
  wald_high <- if (!is.null(m_wald)) bt_safe(m_wald, "upper", "PLOGIT") else NA_real_
  tibble::tibble(
    stratum = key,
    ci_width_hksj = hk_high - hk_low,
    ci_width_wald = wald_high - wald_low
  )
})

message("HKSJ vs. Wald CI width comparison (HKSJ expected wider for small k):")
for (i in seq_len(nrow(hksj_vs_wald))) {
  message(
    "  ", hksj_vs_wald$stratum[i], ": HKSJ = ",
    round(hksj_vs_wald$ci_width_hksj[i], 3), ", Wald = ",
    round(hksj_vs_wald$ci_width_wald[i], 3)
  )
}

# --- Priority 4 #10: same-study multi-arm RVE clustering check -----------------
# Applied only to cells whose rve_note flags a multi-arm study.
rve_cells <- pooled_cells[
  vapply(pooled_cells, \(r) grepl("Multi-arm studies present", r$rve_note), logical(1L))
]

rve_clustering_check <- purrr::map_dfr(rve_cells, function(r) {
  key <- r$stratum
  parts <- strsplit(key, "__")[[1]]
  outcome_name <- parts[1]
  event_col <- OUTCOME_COLS[[outcome_name]]
  if (length(parts) == 2L && parts[2] == "overall") {
    df_sub <- dat_analysis[!is.na(dat_analysis[[event_col]]), ]
  } else {
    strat_var <- parts[2]
    strat_level <- paste(parts[-c(1, 2)], collapse = "__")
    df_sub <- dat_analysis[
      !is.na(dat_analysis[[event_col]]) & !is.na(dat_analysis[[strat_var]]) & dat_analysis[[strat_var]] == strat_level,
    ]
  }
  # MODEL MISMATCH -- DISCLOSED, NOT HIDDEN (methods referee, round 2).
  # metafor::robust() cannot be applied to the binomial-normal GLMM that
  # produces this review's reported estimates, so this check necessarily fits a
  # DIFFERENT model: a normal-normal inverse-variance random-effects model on
  # continuity-corrected logits (escalc measure = "PLO"). The naive and RVE
  # standard errors below are therefore internal to that auxiliary model. They
  # indicate whether clustering matters in a model of the same data; they do
  # NOT bound the GLMM-HKSJ interval reported in Table 2. The manuscript states
  # this explicitly rather than presenting the SEs as if they applied to the
  # primary model.
  dat_es <- metafor::escalc(measure = "PLO", xi = df_sub[[event_col]], ni = df_sub$n_arm)
  fit_naive <- metafor::rma(yi, vi, data = dat_es, method = "ML")
  fit_rve <- metafor::robust(fit_naive, cluster = df_sub$study_id, clubSandwich = TRUE)
  # Cluster count and Satterthwaite df govern how much to trust the RVE SE.
  # clubSandwich's CR2 correction is known to be erratic below roughly 10
  # clusters, so both are recorded and reported: an SE that moves sharply at
  # m = 7 clusters with df < 5 is a diagnostic of RVE instability, not evidence
  # about the underlying variance.
  n_clusters <- length(unique(df_sub$study_id))
  satt_df <- tryCatch(as.numeric(fit_rve$ddf)[1], error = function(e) NA_real_)
  tibble::tibble(
    stratum = key,
    n_clusters = n_clusters,
    satterthwaite_df = satt_df,
    se_naive = fit_naive$se,
    se_rve = fit_rve$se,
    ci_width_naive = fit_naive$ci.ub - fit_naive$ci.lb,
    ci_width_rve = fit_rve$ci.ub - fit_rve$ci.lb
  )
})

message("RVE clustering check (naive vs. cluster-robust SE, logit scale):")
if (nrow(rve_clustering_check) > 0L) {
  for (i in seq_len(nrow(rve_clustering_check))) {
    message(
      "  ", rve_clustering_check$stratum[i], ": naive SE = ",
      round(rve_clustering_check$se_naive[i], 3), ", RVE SE = ",
      round(rve_clustering_check$se_rve[i], 3),
      " (m = ", rve_clustering_check$n_clusters[i], " clusters, Satterthwaite df = ",
      round(rve_clustering_check$satterthwaite_df[i], 1), ")"
    )
  }
} else {
  message("  No POOLED cell contains a multi-arm study; RVE check not applicable.")
}

# --- Priority 1 #2: MDR/XDR classification sensitivity ------------------------
# Re-run the resistance-class subgroup pooling restricted to
# `resistance_class_source == "independently-verified"` only; compare k/N
# (and, where both meet the pooling threshold, the pooled estimate) against
# the main analysis using all classification sources (04_estimation.R).
resistance_levels_cs <- sort(unique(dat_analysis$resistance_class))

classification_sensitivity <- purrr::map_dfr(
  c("clinical_success", "safety", "eradication", "mortality"),
  function(outcome_name) {
    col <- OUTCOME_COLS[[outcome_name]]
    purrr::map_dfr(resistance_levels_cs, function(level) {
      df_all <- dat_analysis[
        !is.na(dat_analysis[[col]]) & dat_analysis$resistance_class == level,
      ]
      df_verified <- df_all[
        !is.na(df_all$resistance_class_source) &
          df_all$resistance_class_source == "independently-verified",
      ]
      r_all <- pool_stratum(
        df_all, col, "n_arm", paste(outcome_name, level, "all_sources", sep = "__"),
        min_studies = MIN_STUDIES, min_patients = MIN_PATIENTS
      )
      r_verified <- pool_stratum(
        df_verified, col, "n_arm", paste(outcome_name, level, "verified_only", sep = "__"),
        min_studies = MIN_STUDIES, min_patients = MIN_PATIENTS
      )
      p_all <- if (r_all$status == "POOLED") {
        bt_safe(r_all$primary, "TE", r_all$primary$sm)
      } else {
        NA_real_
      }
      p_verified <- if (r_verified$status == "POOLED") {
        bt_safe(r_verified$primary, "TE", r_verified$primary$sm)
      } else {
        NA_real_
      }
      tibble::tibble(
        outcome = outcome_name, resistance_class = level,
        status_all = r_all$status, k_studies_all = r_all$k_studies,
        n_patients_all = r_all$n_patients, p_hat_all = p_all,
        status_verified = r_verified$status, k_studies_verified = r_verified$k_studies,
        n_patients_verified = r_verified$n_patients, p_hat_verified = p_verified
      )
    })
  }
)

message("MDR/XDR classification sensitivity (all sources vs. independently-verified-only):")
for (i in seq_len(nrow(classification_sensitivity))) {
  message(
    "  ", classification_sensitivity$outcome[i], " x ", classification_sensitivity$resistance_class[i],
    ": all_sources k=", classification_sensitivity$k_studies_all[i],
    "/N=", classification_sensitivity$n_patients_all[i], " (", classification_sensitivity$status_all[i], ")",
    " vs. verified_only k=", classification_sensitivity$k_studies_verified[i],
    "/N=", classification_sensitivity$n_patients_verified[i], " (", classification_sensitivity$status_verified[i], ")"
  )
}

# --- Priority 2 #4: study-design-stratified sensitivity ------------------------
# Collapse study_design into a 2-category grouping matching the robustness
# plan's "RCT/cohort vs. case-series/compassionate-use" split; Q-between
# test on the largest POOLED outcome (clinical success, overall).
study_design_group_all <- dplyr::case_when(
  dat_analysis$study_design %in% c("RCT", "retrospective cohort") ~ "RCT/cohort",
  dat_analysis$study_design %in% c("case report", "case series") ~ "case report/series (compassionate use)",
  TRUE ~ NA_character_
)

df_design <- dat_analysis[!is.na(dat_analysis$clinical_success_n), ]
df_design$study_design_group <- study_design_group_all[!is.na(dat_analysis$clinical_success_n)]

study_design_subgroup_test <- tryCatch(
  meta::metaprop(
    event = df_design$clinical_success_n, n = df_design$n_arm,
    studlab = df_design$study_arm_id, sm = "PLOGIT", method = "GLMM",
    method.tau = "ML", method.random.ci = "HK", common = FALSE, random = TRUE,
    subgroup = df_design$study_design_group
  ),
  error = function(e) {
    message("Study-design subgroup test failed: ", conditionMessage(e))
    NULL
  }
)

if (!is.null(study_design_subgroup_test)) {
  message(
    "Study-design subgroup test (clinical success, RCT/cohort vs. case report/series): ",
    "Q-between p = ", round(study_design_subgroup_test$pval.Q.b.random, 3)
  )
}

# --- Priority 2 #5: geographic-concentration exclusion -------------------------
# Re-run the overall pooled model excluding arms from Belgium/Israel -- the
# two large aggregate-cohort sources (Pirnay2024, Onallah2023_PASA16) flagged
# a priori as an external-validity concern (memo Priority 2 #5).
geo_excluded_regions <- c("Belgium", "Israel")

geo_concentration_sensitivity <- purrr::map_dfr(
  c("clinical_success", "safety", "eradication", "mortality"),
  function(outcome_name) {
    col <- OUTCOME_COLS[[outcome_name]]
    df_full <- dat_analysis[!is.na(dat_analysis[[col]]), ]
    df_excl <- df_full[!(df_full$geographic_region %in% geo_excluded_regions), ]
    r_full <- pool_stratum(
      df_full, col, "n_arm", paste0(outcome_name, "__geo_full"),
      min_studies = MIN_STUDIES, min_patients = MIN_PATIENTS
    )
    r_excl <- pool_stratum(
      df_excl, col, "n_arm", paste0(outcome_name, "__geo_excl_belgium_israel"),
      min_studies = MIN_STUDIES, min_patients = MIN_PATIENTS
    )
    p_full <- if (r_full$status == "POOLED") {
      backtransform_prop(r_full$primary$TE.random, sm = r_full$primary$sm)
    } else {
      NA_real_
    }
    p_excl <- if (r_excl$status == "POOLED") {
      backtransform_prop(r_excl$primary$TE.random, sm = r_excl$primary$sm)
    } else {
      NA_real_
    }
    tibble::tibble(
      outcome = outcome_name,
      k_studies_full = r_full$k_studies, n_patients_full = r_full$n_patients,
      status_full = r_full$status, p_hat_full = p_full,
      k_studies_excl = r_excl$k_studies, n_patients_excl = r_excl$n_patients,
      status_excl = r_excl$status, p_hat_excl = p_excl
    )
  }
)

message("Geographic-concentration exclusion (Belgium/Israel excluded vs. full sample):")
for (i in seq_len(nrow(geo_concentration_sensitivity))) {
  message(
    "  ", geo_concentration_sensitivity$outcome[i], ": full p_hat = ",
    round(geo_concentration_sensitivity$p_hat_full[i], 3), " (", geo_concentration_sensitivity$status_full[i], ")",
    " vs. excl. p_hat = ", round(geo_concentration_sensitivity$p_hat_excl[i], 3),
    " (", geo_concentration_sensitivity$status_excl[i], ")"
  )
}

# --- Priority 3 #7: route-collapsing sensitivity -------------------------------
# Alternative 2-category route taxonomy (systemic vs. local-only), collapsed
# from the raw `route` free-text field, vs. the primary 4-category
# `route_group`. Any arm whose route text mentions a systemic administration
# keyword (IV/inhaled/nebulized/oral/intra-articular) -- including
# multi-route "other" arms with a systemic component -- is coded systemic;
# pure topical/local arms are coded local-only.
# NA-SAFE. grepl() returns FALSE for an NA route, so the previous version
# silently classified arms with an UNREPORTED route as "local only" -- three
# arms in the current corpus (Malhotra 2026, Arya 2026, Khatami 2021) were
# being asserted into a route category the sources never stated. Unreported
# routes are now carried as NA and dropped from the two-category test, which is
# the honest treatment: this review does not know their route.
route_2cat_all <- ifelse(
  is.na(dat_analysis$route),
  NA_character_,
  ifelse(
    grepl("IV|inhaled|nebulized|oral|intra-articular", dat_analysis$route, ignore.case = TRUE),
    "systemic (incl. multi-route)",
    "local only (topical/local)"
  )
)

keep_r2 <- !is.na(dat_analysis$clinical_success_n) & !is.na(route_2cat_all)
df_route2 <- dat_analysis[keep_r2, ]
df_route2$route_2cat <- route_2cat_all[keep_r2]

route_2cat_subgroup_test <- tryCatch(
  meta::metaprop(
    event = df_route2$clinical_success_n, n = df_route2$n_arm,
    studlab = df_route2$study_arm_id, sm = "PLOGIT", method = "GLMM",
    method.tau = "ML", method.random.ci = "HK", common = FALSE, random = TRUE,
    subgroup = df_route2$route_2cat
  ),
  error = function(e) {
    message("Route-collapsing (2-category) subgroup test failed: ", conditionMessage(e))
    NULL
  }
)

route_2cat_sensitivity <- purrr::map_dfr(
  unique(route_2cat_all), function(level) {
    df_sub <- dat_analysis[
      !is.na(dat_analysis$clinical_success_n) & route_2cat_all[!is.na(dat_analysis$clinical_success_n) | TRUE] == level,
    ]
    NULL
  }
)
# Rebuild cleanly (avoid the indexing footgun above): pool each 2-category
# level directly against the full dat_analysis mask.
route_2cat_sensitivity <- purrr::map_dfr(sort(unique(route_2cat_all)), function(level) {
  mask <- !is.na(dat_analysis$clinical_success_n) & route_2cat_all == level
  df_sub <- dat_analysis[mask, ]
  r <- pool_stratum(
    df_sub, "clinical_success_n", "n_arm", paste0("clinical_success__route_2cat__", level),
    min_studies = MIN_STUDIES, min_patients = MIN_PATIENTS
  )
  tibble::tibble(
    route_2cat = level, k_studies = r$k_studies, n_patients = r$n_patients,
    status = r$status
  )
})

if (!is.null(route_2cat_subgroup_test)) {
  message(
    "Route-collapsing (2-category) subgroup test (clinical success): Q-between p = ",
    round(route_2cat_subgroup_test$pval.Q.b.random, 3)
  )
}

# --- Priority 3 #8: Liu-reuse-tier transparency check --------------------------
# Compare pooled estimate using only independently-extracted rows vs. all
# rows including any Tier-3 ("directly adopted") data points (memo S3).
n_tier3_rows <- sum(dat_analysis$data_provenance != "independently-extracted", na.rm = TRUE)

liu_reuse_tier_check <- list(
  n_total_rows = nrow(dat_analysis),
  n_tier3_rows = n_tier3_rows,
  note = if (n_tier3_rows == 0L) {
    sprintf(
      paste(
        "0 of %d pooling-eligible rows use Tier-3 (directly adopted) data",
        "provenance in this extraction -- every row is coded",
        "data_provenance == 'independently-extracted' (per the strategy",
        "memo S3 decision to adopt Tier 1 + Tier 2 as default policy and",
        "require explicit per-instance sign-off for any Tier-3 use, which",
        "was never invoked). The independently-extracted-only pooled",
        "estimate and the all-rows pooled estimate are therefore IDENTICAL",
        "BY CONSTRUCTION. Reported here as a transparency confirmation",
        "(pre-specified check #8 performed, not silently skipped), not as",
        "a sensitivity comparison with two distinct estimates to contrast."
      ),
      nrow(dat_analysis)
    )
  } else {
    sprintf(
      "%d of %d rows use Tier-3 data provenance -- see classification_sensitivity-style comparison.",
      n_tier3_rows, nrow(dat_analysis)
    )
  }
)
message(liu_reuse_tier_check$note)

# --- Priority 5 #12: minimum-study-count threshold relaxation (appendix) -------
# Relaxes the pre-specified MIN_STUDIES/MIN_PATIENTS gate to k >= 2 studies,
# N >= 10 patients for every stratum-outcome cell already enumerated in
# 04_estimation.R (overall + resistance_class + route_group, all 4
# outcomes). Appendix-only, per the pre-specified plan: reported to show
# whether the primary 3/20 threshold is itself consequential, never
# promoted to the primary results table.
RELAXED_MIN_STUDIES  <- 2L
RELAXED_MIN_PATIENTS <- 10L

#' Reconstruct the eligible study-arm data.frame for a pooled_results() key
#'
#' Keys follow `outcome__overall`, `outcome__resistance_class__LEVEL`, or
#' `outcome__route_group__LEVEL`, matching 04_estimation.R's key
#' construction. Used to re-derive the exact cell-eligible subset without
#' re-running the full estimation script.
#'
#' @param key Character scalar. A name from `pooled_results`.
#' @return data.frame. The eligible study-arm rows for that cell.
reconstruct_cell_df <- function(key) {
  parts <- strsplit(key, "__")[[1]]
  outcome_name <- parts[1]
  event_col <- OUTCOME_COLS[[outcome_name]]
  if (length(parts) == 2L && parts[2] == "overall") {
    dat_analysis[!is.na(dat_analysis[[event_col]]), ]
  } else {
    strat_var <- parts[2]
    strat_level <- paste(parts[-c(1, 2)], collapse = "__")
    dat_analysis[
      !is.na(dat_analysis[[event_col]]) & !is.na(dat_analysis[[strat_var]]) & dat_analysis[[strat_var]] == strat_level,
    ]
  }
}

# A threshold is a statement about how much evidence is enough. Relaxing it can
# only resurrect a cell that failed FOR WANT OF EVIDENCE. The DTR
# "not-derivable" level did not: 04_estimation.R declines to fit it because a
# proportion computed over arms whose DTR status is unknown describes no
# definable population, which is a defect no sample size repairs. Pooling it
# here anyway -- as this appendix originally did, reporting all four such cells
# as "newly poolable" at k up to 23 and N up to 68 -- puts the two scripts in
# direct contradiction and would let a reader conclude that a larger corpus
# would rescue the DTR analysis. It would not.
NOT_ELIGIBLE_FOR_RELAXATION <- function(key) {
  grepl("__dtr_status__not-derivable$", key)
}

threshold_relaxation_appendix <- purrr::map_dfr(names(pooled_results), function(key) {
  r_primary <- pooled_results[[key]]

  if (NOT_ELIGIBLE_FOR_RELAXATION(key)) {
    return(tibble::tibble(
      stratum = key,
      status_primary = r_primary$status,
      status_relaxed = "NOT_ELIGIBLE",
      k_studies = r_primary$k_studies,
      n_patients = r_primary$n_patients,
      newly_poolable = FALSE
    ))
  }

  event_col <- OUTCOME_COLS[[strsplit(key, "__")[[1]][1]]]
  df_sub <- reconstruct_cell_df(key)
  r_relaxed <- pool_stratum(
    df_sub, event_col, "n_arm", key,
    min_studies = RELAXED_MIN_STUDIES, min_patients = RELAXED_MIN_PATIENTS
  )
  tibble::tibble(
    stratum = key,
    status_primary = r_primary$status,
    status_relaxed = r_relaxed$status,
    k_studies = r_relaxed$k_studies,
    n_patients = r_relaxed$n_patients,
    newly_poolable = r_primary$status == "NOT_POOLED" && r_relaxed$status == "POOLED"
  )
})

n_newly_poolable <- sum(threshold_relaxation_appendix$newly_poolable)
message(
  "Threshold-relaxation appendix (k>=", RELAXED_MIN_STUDIES, ", N>=", RELAXED_MIN_PATIENTS,
  "): ", n_newly_poolable, " of ", nrow(threshold_relaxation_appendix),
  " cells become newly poolable under the relaxed (non-primary) threshold."
)

# --- Save ------------------------------------------------------------------------
saveRDS(transformation_sensitivity, file.path(output_dir, "transformation_sensitivity.rds"))
saveRDS(divergence_flags, file.path(output_dir, "transformation_divergence_flags.rds"))
saveRDS(classification_sensitivity, file.path(output_dir, "classification_sensitivity.rds"))

# --- Population-eligibility sensitivity: exclude not-classifiable arms ----------
# Peer-review finding (domain referee, round 2): the Population criterion
# requires MDR/XDR/PDR P. aeruginosa, but the extraction ladder retains arms
# carrying no resistance information at all as `not-classifiable` (NC), and
# those arms then enter every "overall" pool -- including the headline clinical
# success estimate. The review's population is therefore silently broader than
# its own eligibility criterion.
#
# This check quantifies the consequence: every "overall" cell is re-pooled on
# the subset of arms whose resistance status is positively established as MDR,
# XDR or PDR, and compared against the primary estimate. It does not resolve
# the contradiction (an editorial decision, reported in the manuscript), it
# measures how much the reported proportions depend on arms that may not meet
# the population criterion.
nc_exclusion_sensitivity <- purrr::map_dfr(
  c("clinical_success", "safety", "eradication", "mortality"),
  function(outcome_name) {
    col <- OUTCOME_COLS[[outcome_name]]
    df_all <- dat_analysis[!is.na(dat_analysis[[col]]), ]
    df_classified <- df_all[df_all$resistance_class != "not-classifiable", ]

    r_all <- pool_stratum(
      df_all, col, "n_arm", paste(outcome_name, "overall_all", sep = "__"),
      min_studies = MIN_STUDIES, min_patients = MIN_PATIENTS
    )
    r_classified <- pool_stratum(
      df_classified, col, "n_arm", paste(outcome_name, "overall_classified", sep = "__"),
      min_studies = MIN_STUDIES, min_patients = MIN_PATIENTS
    )
    p_all <- if (r_all$status == "POOLED") bt_safe(r_all$primary, "TE", r_all$primary$sm) else NA_real_
    p_cls <- if (r_classified$status == "POOLED") {
      bt_safe(r_classified$primary, "TE", r_classified$primary$sm)
    } else {
      NA_real_
    }
    tibble::tibble(
      outcome = outcome_name,
      k_arms_all = r_all$k_arms, n_patients_all = r_all$n_patients,
      status_all = r_all$status, p_hat_all = p_all,
      k_arms_classified = r_classified$k_arms,
      n_patients_classified = r_classified$n_patients,
      status_classified = r_classified$status, p_hat_classified = p_cls,
      n_patients_dropped = r_all$n_patients - r_classified$n_patients,
      delta_pp = 100 * (p_cls - p_all)
    )
  }
)

saveRDS(nc_exclusion_sensitivity, file.path(output_dir, "nc_exclusion_sensitivity.rds"))

# --- De-duplication sensitivity: restore the two Pirnay-roster matches ---------
# The Methods drop Ferry 2022 and Racenis 2023 as probable duplicates of cases
# inside the Pirnay consortium roster. That crosswalk could not use country or
# treatment year (the roster publishes neither), so it is a judgement on
# clinical fields, not a determination. A judgement that changes the corpus must
# be shown both ways: this refits every overall cell with the two arms PUT BACK,
# so a reader who disagrees with the de-duplication can see exactly what it cost.
dedup_arms <- c("Ferry2022_A", "Racenis2023_LVAD_A")
dat_raw_dedup <- readr::read_csv(data_path, show_col_types = FALSE)
restored <- dat_raw_dedup[dat_raw_dedup$study_arm_id %in% dedup_arms, ]
restored$route_group    <- collapse_category(restored$route)
restored$modality_group <- collapse_category(restored$modality)
dat_with_dups <- dplyr::bind_rows(dat_analysis, restored)

dedup_sensitivity <- purrr::map_dfr(
  c("clinical_success", "safety", "eradication", "mortality"),
  function(outcome_name) {
    col <- OUTCOME_COLS[[outcome_name]]
    r_excl <- pool_stratum(
      dat_analysis[!is.na(dat_analysis[[col]]), ], col, "n_arm",
      paste0(outcome_name, "__dedup_applied"),
      min_studies = MIN_STUDIES, min_patients = MIN_PATIENTS
    )
    r_rest <- pool_stratum(
      dat_with_dups[!is.na(dat_with_dups[[col]]), ], col, "n_arm",
      paste0(outcome_name, "__dedup_restored"),
      min_studies = MIN_STUDIES, min_patients = MIN_PATIENTS
    )
    p_e <- if (r_excl$status == "POOLED") bt_safe(r_excl$primary, "TE", r_excl$primary$sm) else NA_real_
    p_r <- if (r_rest$status == "POOLED") bt_safe(r_rest$primary, "TE", r_rest$primary$sm) else NA_real_
    tibble::tibble(
      outcome = outcome_name,
      n_applied = r_excl$n_patients, p_hat_applied = p_e,
      n_restored = r_rest$n_patients, p_hat_restored = p_r,
      delta_pp = 100 * (p_r - p_e)
    )
  }
)
saveRDS(dedup_sensitivity, file.path(output_dir, "dedup_sensitivity.rds"))

# --- What the reported interval actually is -----------------------------------
# The Methods claim the Hartung-Knapp-Sidik-Jonkman adjustment is applied to
# every stratum's confidence interval. meta() does report method.random.ci =
# "HK". But an adjustment that is *labelled* is not necessarily an adjustment
# that *binds*: the Hartung-Knapp variance estimator multiplies the standard
# error by a factor q that reduces to 1 when the between-study variance estimate
# sits at zero, which is the regime this corpus is in for most cells.
#
# This check computes, per pooled cell, the ratio of the model's reported
# seTE.random to the naive complete-pooling binomial standard error on the logit
# scale, sqrt(1/r + 1/(N-r)). A ratio of exactly 1 means the reported interval
# is a plain t-interval on the logit computed from the pooled counts -- i.e. no
# Hartung-Knapp inflation, no random-effect contribution, and every patient in
# the cell treated as an independent Bernoulli draw. The manuscript must
# describe the interval it actually reports.
hk_binding_check <- purrr::map_dfr(pooled_cells, function(r) {
  m <- r$primary
  key <- r$stratum
  parts <- strsplit(key, "__")[[1]]
  col <- OUTCOME_COLS[[parts[1]]]
  if (length(parts) == 2L && parts[2] == "overall") {
    df_sub <- dat_analysis[!is.na(dat_analysis[[col]]), ]
  } else {
    sv <- parts[2]; sl <- paste(parts[-c(1, 2)], collapse = "__")
    df_sub <- dat_analysis[!is.na(dat_analysis[[col]]) & !is.na(dat_analysis[[sv]]) &
                             dat_analysis[[sv]] == sl, ]
  }
  ev <- sum(df_sub[[col]], na.rm = TRUE)
  n  <- sum(df_sub$n_arm, na.rm = TRUE)
  naive_se <- if (ev > 0 && ev < n) sqrt(1 / ev + 1 / (n - ev)) else NA_real_
  model_se <- m$seTE.random
  tibble::tibble(
    stratum   = key,
    method_ci = if (!is.null(m$method.random.ci)) m$method.random.ci else NA_character_,
    df_random = if (!is.null(m$df.random)) m$df.random else NA_real_,
    tau2      = m$tau2,
    model_se  = model_se,
    naive_binomial_se = naive_se,
    hk_inflation_ratio = if (!is.na(naive_se) && naive_se > 0) model_se / naive_se else NA_real_
  )
})
saveRDS(hk_binding_check, file.path(output_dir, "hk_binding_check.rds"))

n_identity <- sum(abs(hk_binding_check$hk_inflation_ratio - 1) < 1e-6, na.rm = TRUE)
message(sprintf(
  "
Hartung-Knapp binding check: the reported SE equals the naive complete-pooling binomial SE in %d of %d cells (inflation ratio = 1). Range of ratios: %.4f to %.4f.",
  n_identity, nrow(hk_binding_check),
  min(hk_binding_check$hk_inflation_ratio, na.rm = TRUE),
  max(hk_binding_check$hk_inflation_ratio, na.rm = TRUE)
))

message("
De-duplication sensitivity (Pirnay-roster matches restored):")
for (i in seq_len(nrow(dedup_sensitivity))) {
  row <- dedup_sensitivity[i, ]
  message(sprintf("  %-18s applied %.1f%% (N=%d) | restored %.1f%% (N=%d) | delta %+.1f pp",
    row$outcome, 100 * row$p_hat_applied, row$n_applied,
    100 * row$p_hat_restored, row$n_restored, row$delta_pp))
}


message("\nPopulation-eligibility sensitivity (excluding not-classifiable arms):")
for (i in seq_len(nrow(nc_exclusion_sensitivity))) {
  row <- nc_exclusion_sensitivity[i, ]
  message(sprintf(
    "  %-18s all: %s %.1f%% (%d arms, N=%d) | classified-only: %s %s (%d arms, N=%d) | dropped N=%d%s",
    row$outcome, row$status_all, 100 * row$p_hat_all, row$k_arms_all, row$n_patients_all,
    row$status_classified,
    if (is.na(row$p_hat_classified)) "--" else sprintf("%.1f%%", 100 * row$p_hat_classified),
    row$k_arms_classified, row$n_patients_classified, row$n_patients_dropped,
    if (is.na(row$delta_pp)) "" else sprintf(" | delta %+.1f pp", row$delta_pp)
  ))
}
saveRDS(study_design_subgroup_test, file.path(output_dir, "study_design_subgroup_test.rds"))
saveRDS(geo_concentration_sensitivity, file.path(output_dir, "geo_concentration_sensitivity.rds"))
saveRDS(leave_one_out, file.path(output_dir, "leave_one_out.rds"))
saveRDS(route_2cat_sensitivity, file.path(output_dir, "route_2cat_sensitivity.rds"))
saveRDS(route_2cat_subgroup_test, file.path(output_dir, "route_2cat_subgroup_test.rds"))
saveRDS(liu_reuse_tier_check, file.path(output_dir, "liu_reuse_tier_check.rds"))
saveRDS(hksj_vs_wald, file.path(output_dir, "hksj_vs_wald.rds"))
saveRDS(rve_clustering_check, file.path(output_dir, "rve_clustering_check.rds"))
saveRDS(threshold_relaxation_appendix, file.path(output_dir, "threshold_relaxation_appendix.rds"))

message("05_robustness.R complete.")
