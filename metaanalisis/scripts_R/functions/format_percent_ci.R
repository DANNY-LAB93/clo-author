#' Format a proportion and its 95% CI as "XX.X% [YY.Y%, ZZ.Z%]"
#'
#' Used consistently across tables and the results summary so a reader never
#' sees the same quantity rounded differently in two places (INV-11).
#'
#' @param p_hat Numeric. Point estimate on the proportion scale (0-1).
#' @param ci_low Numeric. Lower 95% CI bound (0-1).
#' @param ci_high Numeric. Upper 95% CI bound (0-1).
#' @param digits Integer. Decimal places for the percentage (default 1).
#' @return Character scalar/vector.
format_percent_ci <- function(p_hat, ci_low, ci_high, digits = 1L) {
  fmt <- paste0("%.", digits, "f")
  ifelse(
    is.na(p_hat),
    "--",
    sprintf(
      paste0(fmt, "%% [", fmt, "%%, ", fmt, "%%]"),
      100 * p_hat, 100 * ci_low, 100 * ci_high
    )
  )
}
