#' Back-transform a pooled proportion from the analysis scale to [0, 1]
#'
#' `meta::metaprop()` returns pooled estimates (`TE.random`, `lower.random`,
#' `upper.random`, etc.) on the transformed scale used for pooling (logit for
#' `sm = "PLOGIT"`, Freeman-Tukey double-arcsine for `sm = "PFT"`). Neither
#' `metaprop()` nor `summary.meta()` exposes a public, numeric back-transform
#' helper -- the back-transformation only happens inside `print`/`forest`
#' methods. This wraps the package's own (unexported) `meta:::backtransf()`,
#' which is exactly what those print/forest methods call internally, rather
#' than re-deriving the Freeman-Tukey/Miller (1978) inverse by hand -- a
#' formula whose fragility under heterogeneous sample sizes is precisely the
#' Schwarzer et al. (2019) failure mode this project's strategy memo (S2.1)
#' is designed around. Re-implementing it independently would risk
#' introducing the same class of error the memo warns about.
#'
#' @param x Numeric vector on the transformed scale (e.g. `TE.random`,
#'   `lower.random`, `upper.random`).
#' @param sm Character. Summary measure used by `metaprop()` (`"PLOGIT"` or
#'   `"PFT"`).
#' @param n_harmonic Numeric. Harmonic mean of arm sizes, required for the
#'   Freeman-Tukey (`"PFT"`) back-transform; ignored for `"PLOGIT"`.
#' @return Numeric vector of back-transformed proportions in \[0, 1\].
backtransform_prop <- function(x, sm, n_harmonic = 1) {
  stopifnot(is.numeric(x))
  stopifnot(sm %in% c("PLOGIT", "PFT"))

  p_hat <- tryCatch(
    meta:::backtransf(x, sm = sm, n = n_harmonic),
    error = function(e) {
      # Documented fallback: PLOGIT has a trivial, dependency-free closed
      # form. PFT has no safe closed-form fallback here (that fragility is
      # exactly the point) -- fail loudly rather than silently guessing.
      if (sm == "PLOGIT") {
        stats::plogis(x)
      } else {
        stop(sprintf(
          "backtransform_prop(): meta:::backtransf() failed for sm = '%s' and no safe fallback exists: %s",
          sm, conditionMessage(e)
        ))
      }
    }
  )

  # Numerical discipline: clamp to [0, 1] -- CDF-like quantities must never
  # leave their support due to floating-point back-transformation error.
  pmin(pmax(p_hat, 0), 1)
}
