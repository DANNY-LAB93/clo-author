#' Pool a stratum-outcome cell with GLMM primary and logit-DL fallback
#'
#' Implements `quality_reports/strategy/phage_therapy_mdr_pseudomonas/
#' pseudo_code.md` Section 2 exactly, with one disclosed refinement: the
#' minimum-study gate is applied to the count of *distinct studies*
#' (`k_studies`), not the arm count, since the strategy memo's own threshold
#' language is "≥ 3 independent studies" (Section 2.1) -- an arm-count
#' gate would let a single study contributing 3+ arms pass on its own.
#'
#' Primary model: random-effects GLMM (binomial-normal, logit link).
#' Convergence is checked per pseudo_code.md §2's contingency: a caught
#' error, a known non-convergence warning string, or a non-finite pooled
#' estimate/SE all mark the cell as non-converged, in which case the
#' logit-DerSimonian-Laird sensitivity model is promoted to be the
#' *reported* primary for that cell only (never silently).
#'
#' @param df data.frame. One row per eligible study-arm for this cell. Must
#'   contain `study_id`, `study_arm_id`, `n_col`, and `event_col`.
#' @param event_col Character. Name of the numerator column in `df`.
#' @param n_col Character. Name of the denominator column in `df` (arm n).
#' @param stratum_label Character. Human-readable label for this cell, used
#'   in reporting and as the key in the results list.
#' @param min_studies Integer. Minimum distinct studies to attempt pooling.
#' @param min_patients Integer. Minimum pooled patients to attempt pooling.
#' @return Named list. If `status == "NOT_POOLED"`, contains `reason` and
#'   `narrative_table`. If `status == "POOLED"`, contains the primary model
#'   (`primary`), `primary_model_used`, `convergence_flag`,
#'   `convergence_diagnostics`, all sensitivity models, `k_arms`,
#'   `k_studies`, `n_patients`, and `rve_note`.
pool_stratum <- function(df, event_col, n_col, stratum_label,
                          min_studies = 3L, min_patients = 20L) {

  stopifnot(is.data.frame(df))
  required_cols <- c("study_id", "study_arm_id", event_col, n_col)
  stopifnot(all(required_cols %in% names(df)))

  # Defensive: drop any row with a missing event count, missing arm size, or a
  # missing study id before counting or model-fitting. A caller that subsets
  # with a condition evaluating to NA (e.g. `route_group == "other"` when a
  # study's route is NA) can pass in phantom all-NA rows; an NA in the event
  # vector makes meta::metaprop() abort with "'x' must be nonnegative and
  # integer", which previously left a threshold-passing cell marked POOLED with
  # a NULL model. Filtering here makes pooling robust regardless of the caller.
  df <- df[!is.na(df[[event_col]]) & !is.na(df[[n_col]]) & !is.na(df$study_id), , drop = FALSE]

  k_arms <- nrow(df)
  k_studies <- length(unique(df$study_id))
  n_patients <- sum(df[[n_col]], na.rm = TRUE)

  if (k_studies < min_studies || n_patients < min_patients) {
    return(list(
      status = "NOT_POOLED",
      stratum = stratum_label,
      k_arms = k_arms,
      k_studies = k_studies,
      n_patients = n_patients,
      reason = sprintf(
        "k_studies = %d, N = %d patients (threshold: >= %d studies AND >= %d patients)",
        k_studies, n_patients, min_studies, min_patients
      ),
      narrative_table = df[, c("study_id", "study_arm_id", n_col, event_col)]
    ))
  }

  event <- df[[event_col]]
  n_arm <- df[[n_col]]
  studlab <- df$study_arm_id

  # --- Primary: GLMM binomial-normal, logit link ----------------------------
  # CONVERGENCE CONTINGENCY (strategy memo S2.1 / pseudo_code.md S2): capture
  # warnings/errors rather than letting an unreliable point estimate through
  # silently.
  # NOTE on `<<-` below: this is a deliberate, narrow exception to the
  # project's general `<<-` prohibition (coding-standards-r.md S9). Condition
  # handlers passed to withCallingHandlers()/tryCatch() run in their own
  # frame; `<<-` into the enclosing pool_stratum() frame is the standard R
  # idiom for accumulating captured warning/error text (there is no return
  # value to use instead once invokeRestart() resumes execution). This
  # mirrors pseudo_code.md S2's own approved specification verbatim.
  glmm_warnings <- character(0)
  m_glmm <- withCallingHandlers(
    tryCatch(
      meta::metaprop(
        event = event, n = n_arm, studlab = studlab,
        sm = "PLOGIT", method = "GLMM", method.tau = "ML",
        method.random.ci = "HK", common = FALSE, random = TRUE
      ),
      error = function(e) {
        glmm_warnings <<- c(glmm_warnings, paste("ERROR:", conditionMessage(e)))
        NULL
      }
    ),
    warning = function(w) {
      glmm_warnings <<- c(glmm_warnings, paste("WARNING:", conditionMessage(w)))
      invokeRestart("muffleWarning")
    }
  )

  convergence_flag <- if (is.null(m_glmm)) {
    "FAILED_ERROR"
  } else if (any(grepl("converge|NA/NaN|singular", glmm_warnings, ignore.case = TRUE))) {
    "FAILED_WARNING"
  } else if (!is.finite(m_glmm$TE.random) || !is.finite(m_glmm$seTE.random)) {
    "FAILED_NONFINITE"
  } else {
    "CONVERGED"
  }

  # --- Safe wrapper: meta package's internal multi-estimator heterogeneity
  # diagnostics (populated even for method.tau="DL"/fixed-effect calls) can
  # invoke metafor::rma(method="REML") under the hood and throw an uncaught
  # "Fisher scoring algorithm did not converge" error for near-degenerate
  # cells (e.g. safety strata with near-complete separation). Originally only
  # the GLMM primary call was protected; a real cell (safety, after adding
  # the Pirnay MDR/XDR/PDR strata) hit this in an unprotected sensitivity
  # call and crashed the whole pipeline. All four metaprop() calls now share
  # this same capture-don't-crash contingency.
  safe_metaprop <- function(...) {
    call_warnings <- character(0)
    result <- withCallingHandlers(
      tryCatch(meta::metaprop(...), error = function(e) {
        call_warnings <<- c(call_warnings, paste("ERROR:", conditionMessage(e)))
        NULL
      }),
      warning = function(w) {
        call_warnings <<- c(call_warnings, paste("WARNING:", conditionMessage(w)))
        invokeRestart("muffleWarning")
      }
    )
    list(model = result, warnings = call_warnings)
  }

  # --- Sensitivity 1: Freeman-Tukey double arcsine, DerSimonian-Laird -------
  ft_res <- safe_metaprop(
    event = event, n = n_arm, studlab = studlab,
    sm = "PFT", method = "Inverse", method.tau = "DL",
    method.random.ci = "HK", common = FALSE, random = TRUE
  )
  m_ft <- ft_res$model

  # --- Sensitivity 2: simple logit, DerSimonian-Laird -----------------------
  # Also serves as the pre-specified cell-level fallback on GLMM failure.
  logit_dl_res <- safe_metaprop(
    event = event, n = n_arm, studlab = studlab,
    sm = "PLOGIT", method = "Inverse", method.tau = "DL",
    method.random.ci = "HK", common = FALSE, random = TRUE
  )
  m_logit_dl <- logit_dl_res$model

  # --- Fixed-effect sensitivity ----------------------------------------------
  fe_res <- safe_metaprop(
    event = event, n = n_arm, studlab = studlab,
    sm = "PLOGIT", method = "Inverse", common = TRUE, random = FALSE
  )
  m_fe <- fe_res$model

  # --- Cascading fallback: GLMM -> logit-DL -> fixed-effect -----------------
  # If the pre-specified fallback (logit-DL) *also* fails to converge, cascade
  # to fixed-effect (which has no tau^2 to estimate and cannot hit this same
  # failure mode) rather than crash or silently report a NULL model.
  if (convergence_flag == "CONVERGED") {
    reported_primary <- m_glmm
    primary_model_used <- "GLMM (binomial-normal, logit link)"
  } else if (!is.null(m_logit_dl)) {
    reported_primary <- m_logit_dl
    primary_model_used <- sprintf(
      "FALLBACK: logit-DerSimonian-Laird (GLMM failed to converge for this cell: %s)",
      convergence_flag
    )
  } else {
    reported_primary <- m_fe
    convergence_flag <- paste0(convergence_flag, "_AND_LOGIT_DL_FAILED")
    primary_model_used <- sprintf(
      "FALLBACK: fixed-effect (GLMM AND logit-DerSimonian-Laird both failed to converge for this cell: %s / %s)",
      convergence_flag, paste(logit_dl_res$warnings, collapse = "; ")
    )
  }

  # --- Same-study multi-arm clustering note ---------------------------------
  arm_counts <- table(df$study_id)
  multi_arm_studies <- names(arm_counts[arm_counts > 1L])
  rve_note <- if (length(multi_arm_studies) > 0L) {
    sprintf(
      "Multi-arm studies present in this cell (%s) -- naive-independence CI may understate variance; see 05_robustness.R RVE check.",
      paste(multi_arm_studies, collapse = ", ")
    )
  } else {
    "No multi-arm studies in this cell; naive independence assumption holds by construction."
  }

  list(
    status = "POOLED",
    stratum = stratum_label,
    k_arms = k_arms,
    k_studies = k_studies,
    n_patients = n_patients,
    primary = reported_primary,
    primary_model_used = primary_model_used,
    convergence_flag = convergence_flag,
    convergence_diagnostics = glmm_warnings,
    glmm_raw = m_glmm,
    sens_ft = m_ft,
    sens_logit_dl = m_logit_dl,
    sens_fe = m_fe,
    rve_note = rve_note
  )
}
