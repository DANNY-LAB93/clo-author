# Verify the generated macros reproduce the generated tables exactly.
#
# The macros and the tables are both built from pooled_results.rds, so they
# should agree by construction. This check exists because "should agree by
# construction" is what was believed about the manuscript and the manifest, and
# it was false for most of a Results section. A generated artifact that is never
# compared to its sibling is an assumption, not a guarantee.
#
# Every macro value must appear in the corresponding row of
# meta_pooled_estimates.tex. Exit non-zero on any mismatch.

suppressPackageStartupMessages({
  library(here)
  library(stringr)
})

macros_path <- here::here("paper", "generated_scalars.tex")
table_path <- here::here("paper", "tables", "phage_therapy_mdr_pseudomonas",
                         "meta_pooled_estimates.tex")

macro_lines <- readLines(macros_path, warn = FALSE)
tab_lines <- readLines(table_path, warn = FALSE)

# ---- parse macros -----------------------------------------------------------
m <- str_match(macro_lines, "^\\\\newcommand\\{\\\\([A-Za-z]+)\\}\\{(.*)\\}$")
macros <- setNames(m[!is.na(m[, 2]), 3], m[!is.na(m[, 2]), 2])

# ---- parse the table --------------------------------------------------------
# Rows look like:
#   Clinical success -- Overall & 23 & 28 & 71 & 76.1\% [64.2\%, 84.9\%] & 0.000 & [..] & GLMM \\
body <- tab_lines[grepl("&", tab_lines) & !grepl("Outcome -- Stratum", tab_lines)]

row_key <- function(label) {
  label <- trimws(label)
  out <- if (grepl("^Clinical success", label)) "Cs"
    else if (grepl("^Safety", label)) "Saf"
    else if (grepl("^Eradication", label)) "Erad"
    else if (grepl("^Mortality", label)) "Mort"
    else return(NA_character_)
  strat <- sub("^[^-]*-- *", "", label)
  strat <- trimws(strat)
  suffix <- if (strat == "Overall") "Overall"
    else if (grepl("Resistance: MDR", strat)) "ResMDR"
    else if (grepl("Resistance: NC", strat)) "ResNotClassifiable"
    else if (grepl("Route: other", strat)) "RouteOther"
    else return(NA_character_)
  paste0(out, suffix)
}

failures <- character(0)
checked <- 0L

for (ln in body) {
  cells <- strsplit(sub("\\\\\\\\\\s*$", "", ln), "&", fixed = TRUE)[[1]]
  if (length(cells) < 6) next
  key <- row_key(cells[1])
  if (is.na(key)) next

  tab_k <- trimws(cells[2])
  tab_arms <- trimws(cells[3])
  tab_n <- trimws(cells[4])
  tab_est <- trimws(cells[5])   # "76.1\% [64.2\%, 84.9\%]"
  tab_tau <- trimws(cells[6])

  parts <- str_match(tab_est, "^([0-9.]+\\\\%) \\[([0-9.]+\\\\%), ([0-9.]+\\\\%)\\]$")
  if (is.na(parts[1])) {
    failures <- c(failures, paste0(key, ": could not parse estimate cell '", tab_est, "'"))
    next
  }

  expect <- list(Est = parts[2], Lo = parts[3], Hi = parts[4],
                 K = tab_k, Arms = tab_arms, N = tab_n, Tau = tab_tau)

  for (suffix in names(expect)) {
    nm <- paste0(key, suffix)
    checked <- checked + 1L
    if (!nm %in% names(macros)) {
      failures <- c(failures, paste0("MISSING macro \\", nm))
      next
    }
    got <- macros[[nm]]
    want <- expect[[suffix]]
    if (!identical(got, want)) {
      failures <- c(failures,
        sprintf("MISMATCH \\%s: macro='%s' table='%s'", nm, got, want))
    }
  }
}

# ---- sensitivity models -----------------------------------------------------
# Added after the first implementation emitted 7.1% for Freeman-Tukey against
# the table's 8.4%, because the macro omitted the harmonic-mean argument the
# back-transform needs. That was caught by reading. Nothing else should be.
sens_path <- here::here("paper", "tables", "phage_therapy_mdr_pseudomonas",
                        "meta_sensitivity.tex")
if (file.exists(sens_path)) {
  sens_lines <- readLines(sens_path, warn = FALSE)
  model_suffix <- function(model) {
    if (grepl("Freeman-Tukey", model)) "FT"
    else if (grepl("DerSimonian", model)) "DL"
    else if (grepl("Fixed-effect", model)) "FE"
    else NA_character_
  }
  for (ln in sens_lines[grepl("&", sens_lines)]) {
    cells <- strsplit(sub("\\\\\\\\\\s*$", "", ln), "&", fixed = TRUE)[[1]]
    if (length(cells) < 3) next
    key <- row_key(cells[1])
    suf <- model_suffix(cells[2])
    if (is.na(key) || is.na(suf)) next
    est <- str_match(trimws(cells[3]), "^([0-9.]+\\\\%)")[, 2]
    if (is.na(est)) next
    nm <- paste0(key, suf)
    checked <- checked + 1L
    if (!nm %in% names(macros)) {
      failures <- c(failures, paste0("MISSING macro \\", nm))
    } else if (!identical(macros[[nm]], est)) {
      failures <- c(failures,
        sprintf("MISMATCH \\%s: macro='%s' table='%s'", nm, macros[[nm]], est))
    }
  }
}

cat("=== macros vs generated table ===\n")
cat("macros parsed :", length(macros), "\n")
cat("values checked:", checked, "\n\n")

if (length(failures) > 0) {
  cat("FAIL --", length(failures), "discrepancies:\n")
  cat(paste0("  ", failures, collapse = "\n"), "\n")
  quit(status = 1)
}
cat("PASS: every macro reproduces its table row exactly.\n")
