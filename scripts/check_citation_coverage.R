# Every study in the corpus must be citable from the manuscript.
#
# A systematic review that includes a study but never cites it does not list it
# in the references, so a reader cannot reach roughly a third of the evidence
# base. Both round-5 referees raised this independently. This check makes the
# claim mechanical: it reads the study identifiers out of the analysis dataset
# and the exclusion log, extracts every citation key actually used in the
# manuscript sources, and reports the set difference in both directions.
#
# Exit status is non-zero when any corpus study is uncited, so the check can
# gate a build.

suppressPackageStartupMessages({
  library(here)
  library(dplyr)
  library(stringr)
})

out_dir <- here::here("scripts", "R", "output")
tex_files <- c(
  here::here("paper", "main.tex"),
  list.files(here::here("paper", "sections"), pattern = "[.]tex$", full.names = TRUE)
)

# ---- 1. Citation keys used anywhere in the manuscript -----------------------
# biblatex commands take a comma-separated key list; \Cref and \ref take labels
# and must not be counted as citations.
cite_cmds <- c(
  "parencite", "textcite", "citeauthor", "citeyear", "cite", "Parencite",
  "Textcite", "Citeauthor", "footcite", "nocite"
)
pattern <- paste0("\\\\(", paste(cite_cmds, collapse = "|"), ")\\*?(\\[[^]]*\\])*\\{([^}]*)\\}")

cited <- character(0)
for (f in tex_files) {
  if (!file.exists(f)) next
  txt <- paste(readLines(f, warn = FALSE), collapse = "\n")
  m <- stringr::str_match_all(txt, pattern)[[1]]
  if (nrow(m) > 0) {
    keys <- unlist(strsplit(m[, ncol(m)], ","))
    cited <- c(cited, trimws(keys))
  }
}
cited <- sort(unique(cited[nzchar(cited)]))

# ---- 2. Studies the review says it includes ---------------------------------
dat <- readRDS(file.path(out_dir, "dat_analysis.rds"))
included <- sort(unique(dat$study_id))

# Excluded-at-full-text studies must also be citable: PRISMA 2020 item 16b asks
# for a characteristics-of-excluded-studies listing with reasons.
excl_path <- file.path(out_dir, "exclusion_log.rds")
excluded <- character(0)
if (file.exists(excl_path)) {
  el <- readRDS(excl_path)
  id_col <- intersect(c("study_id", "study_arm_id", "record_id"), names(el))
  if (length(id_col) > 0) excluded <- sort(unique(as.character(el[[id_col[1]]])))
}

# ---- 3. Bibliography keys available ----------------------------------------
bib <- paste(readLines(here::here("Bibliography_base.bib"), warn = FALSE), collapse = "\n")
bib_keys <- stringr::str_match_all(bib, "@[A-Za-z]+\\{([^,]+),")[[1]][, 2]
bib_keys <- sort(unique(trimws(bib_keys)))

# ---- 4. Resolve study_id to bibliography key --------------------------------
# The extraction schema's study_id and the .bib key share an author-year stem
# but not the journal suffix (Pirnay2024 vs Pirnay2024_natmicrobiol), so a
# direct setdiff would report every study as uncited. Match on the stem, and
# treat an ambiguous or absent match as a finding rather than silently dropping
# it -- an unresolvable study_id means the reader cannot reach that study
# either.
stem <- function(x) tolower(sub("_.*$", "", x))

resolve <- function(sid) {
  hits <- bib_keys[stem(bib_keys) == stem(sid)]
  if (length(hits) == 1L) return(hits)
  if (length(hits) == 0L) return(NA_character_)
  # Several bib entries share the stem. This is not cosmetic: Liu2025 is both a
  # systematic review this manuscript cites as a source AND a case report this
  # manuscript includes as evidence. Citing the wrong one would attribute a
  # single patient's outcome to a review of 2,000. Resolve by requiring the bib
  # key to contain every token of the study_id, which distinguishes
  # Liu2025_mlife_perinephric from Liu2025_ijaa; report anything still
  # ambiguous rather than guessing.
  toks <- setdiff(strsplit(tolower(sid), "_")[[1]], "")
  contains_all <- vapply(hits, function(h) {
    all(vapply(toks, function(t) grepl(t, tolower(h), fixed = TRUE), logical(1)))
  }, logical(1))
  pref <- hits[contains_all]
  if (length(pref) == 1L) return(pref)
  pref2 <- hits[startsWith(tolower(hits), tolower(sid))]
  if (length(pref2) == 1L) return(pref2)
  paste0("AMBIGUOUS:", paste(hits, collapse = "|"))
}

resolved <- vapply(included, resolve, character(1))
unresolvable <- included[is.na(resolved)]
ambiguous <- included[!is.na(resolved) & startsWith(resolved, "AMBIGUOUS:")]
ok <- resolved[!is.na(resolved) & !startsWith(resolved, "AMBIGUOUS:")]

uncited_included <- names(ok)[!(ok %in% cited)]
uncited_excluded <- setdiff(excluded, cited)
cited_missing_bib <- setdiff(cited, bib_keys)

cat("=== Citation coverage ===\n")
cat("Distinct keys cited in manuscript : ", length(cited), "\n")
cat("Studies in analysis dataset       : ", length(included), "\n")
cat("Studies in exclusion log          : ", length(excluded), "\n")
cat("Entries in Bibliography_base.bib  : ", length(bib_keys), "\n\n")

# paste0(character(0), " -> ", character(0)) returns " -> ", not character(0),
# because paste0 recycles the zero-length argument to "". A report that prints
# "(1)" when it means "none" is the kind of thing this whole exercise is about.
with_arrow <- function(keys, values) {
  if (length(keys) == 0) return(character(0))
  paste0(keys, " -> ", values)
}

report_set <- function(label, x) {
  cat(label, " (", length(x), ")\n", sep = "")
  if (length(x) == 0) {
    cat("  none\n\n")
  } else {
    cat(paste0("  ", x, collapse = "\n"), "\n\n", sep = "")
  }
}

report_set("INCLUDED BUT NEVER CITED -- will not appear in the reference list:",
           with_arrow(uncited_included, ok[uncited_included]))
report_set("study_id with NO bibliography entry at all:", unresolvable)
report_set("study_id matching SEVERAL bibliography entries:",
           with_arrow(ambiguous, resolved[ambiguous]))
report_set("EXCLUDED AT FULL TEXT BUT NEVER CITED:", uncited_excluded)
report_set("CITED BUT ABSENT FROM THE .bib -- would compile as an undefined citation:", cited_missing_bib)

saveRDS(
  list(cited = cited, included = included, excluded = excluded,
       uncited_included = uncited_included, uncited_excluded = uncited_excluded,
       cited_missing_bib = cited_missing_bib),
  file.path(out_dir, "citation_coverage.rds")
)

fail <- length(uncited_included) > 0 || length(cited_missing_bib) > 0 ||
        length(unresolvable) > 0 || length(ambiguous) > 0
if (fail) {
  cat("FAIL: the manuscript does not cite every study it includes.\n")
  quit(status = 1)
}
cat("PASS: every included study is cited and every citation resolves.\n")
