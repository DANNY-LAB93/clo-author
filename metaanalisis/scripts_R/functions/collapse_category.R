#' Collapse a free-text extraction field to its leading category label
#'
#' Several extraction-form fields (`route`, `modality`) mix a controlled
#' category label with free-text qualifiers in parentheses, e.g.
#' `"other (multi-route: IV + local wound/driveline irrigation concurrently)"`
#' or `"phage monotherapy (vs. placebo and vs. systemic-antibiotic comparator
#' arms -- see notes)"`. For stratified pooling we need the controlled label
#' only. This extracts the substring before the first `"("` and trims
#' whitespace; if there is no parenthetical, the trimmed original string is
#' returned unchanged.
#'
#' @param x Character vector.
#' @return Character vector of collapsed category labels.
collapse_category <- function(x) {
  stopifnot(is.character(x) || all(is.na(x)))
  before_paren <- sub("\\(.*$", "", x)
  trimws(before_paren)
}
