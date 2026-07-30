# Every study in the corpus must carry a machine-resolvable identifier.
#
# WHY THIS EXISTS. The round-5 un-blocked search produced a list of 28 records
# "never screened", and one of them -- Ngauy 2026 -- was already in the corpus.
# The sweep missed it because its extraction_citation records page numbers
# ("p.1 Abstract; p.3 Phage selection") rather than a PMID, so a regex looking
# for identifiers found nothing to match. That is not a cosmetic gap: it means
# this review cannot mechanically answer "is this record already included?",
# which is the one question a screening pass asks most often, and it is how a
# study already in the corpus came to be re-screened as new.
#
# WHAT COUNTS AS TRACEABLE. A PMID, a PMC id, or a DOI, appearing either in the
# arm's extraction_citation / incomplete_reason or in the study's bibliography
# entry. A registry identifier (NCT) counts only for registry-only records, which
# have no publication to point at.
#
# Exit status is non-zero when any study is untraceable, so the check can gate a
# build the same way the citation-coverage and macro checks do.

suppressPackageStartupMessages({
  library(here)
  library(readr)
  library(stringr)
})

out_dir <- here::here("scripts", "R", "output")

raw <- readr::read_csv(
  here::here("data", "cleaned", "phage_therapy_extraction_dataset.csv"),
  show_col_types = FALSE
)
bib <- paste(readLines(here::here("Bibliography_base.bib"), warn = FALSE),
             collapse = "\n")

# ---- identifier patterns ----------------------------------------------------
ID_PATTERNS <- c(
  pmid = "PMID[: ]*([0-9]{7,8})",
  pmc  = "PMC([0-9]{6,8})",
  doi  = "(10\\.[0-9]{4,9}/[^ ,;)}\\]]+)",
  nct  = "(NCT[0-9]{8})"
)

find_ids <- function(txt) {
  if (is.na(txt) || !nzchar(txt)) return(character(0))
  out <- character(0)
  for (nm in names(ID_PATTERNS)) {
    m <- str_match_all(txt, ID_PATTERNS[[nm]])[[1]]
    if (nrow(m) == 0) next
    vals <- unique(m[, 2])
    # A DOI at the end of a sentence picks up the full stop, which indexed the
    # same DOI twice -- once with and once without it. Trailing sentence
    # punctuation is never part of a DOI.
    if (nm == "doi") vals <- unique(sub("[.,;:)\\]]+$", "", vals))
    out <- c(out, paste0(nm, ":", vals))
  }
  out
}

# ---- bibliography entry text per key ---------------------------------------
entry_starts <- str_locate_all(bib, "@[A-Za-z]+\\{")[[1]]
bib_entries <- list()
if (nrow(entry_starts) > 0) {
  for (i in seq_len(nrow(entry_starts))) {
    from <- entry_starts[i, 1]
    to <- if (i < nrow(entry_starts)) entry_starts[i + 1, 1] - 1L else nchar(bib)
    chunk <- substr(bib, from, to)
    key <- str_match(chunk, "@[A-Za-z]+\\{([^,]+),")[, 2]
    if (!is.na(key)) bib_entries[[trimws(key)]] <- chunk
  }
}

bib_stem <- function(x) tolower(sub("_.*$", "", x))

# ---- audit ------------------------------------------------------------------
studies <- sort(unique(raw$study_id))
rows <- vector("list", length(studies))

for (i in seq_along(studies)) {
  sid <- studies[i]
  arms <- raw[raw$study_id == sid, ]
  from_extraction <- unique(unlist(lapply(
    c(arms$extraction_citation, arms$incomplete_reason), find_ids)))

  matched_keys <- names(bib_entries)[bib_stem(names(bib_entries)) == bib_stem(sid)]
  from_bib <- unique(unlist(lapply(bib_entries[matched_keys], find_ids)))

  all_ids <- unique(c(from_extraction, from_bib))

  # A registry-only record has no publication to point at, so its trial
  # registration IS its identifier and is sufficient. SWARM-P.a./AP-PA02 is the
  # only such record here: its journal_tier says "registry-only (ClinicalTrials.gov
  # structured results, no peer-reviewed publication located)". Accepting NCT for
  # these and only these keeps the check honest in both directions -- it does not
  # wave through a record that simply lacks a DOI someone failed to record.
  registry_only <- any(grepl("^registry-only", arms$journal_tier))
  publication_id <- if (registry_only) all_ids else all_ids[!startsWith(all_ids, "nct:")]

  rows[[i]] <- data.frame(
    study_id = sid,
    n_arms = nrow(arms),
    in_extraction = length(from_extraction) > 0,
    in_bib = length(from_bib) > 0,
    has_publication_id = length(publication_id) > 0,
    ids = paste(all_ids, collapse = " "),
    stringsAsFactors = FALSE
  )
}

audit <- do.call(rbind, rows)
saveRDS(audit, file.path(out_dir, "identifier_traceability.rds"))

# ---- emit the corpus identifier index ---------------------------------------
# The point of the check is not the audit, it is this file. A screening pass can
# now diff a candidate list against it and answer "is this record already
# included?" mechanically. Ngauy 2026 was re-screened as new precisely because
# no such index existed.
index_path <- here::here("quality_reports", "corpus_identifier_index.txt")
# Normalise here as well as at capture. A DOI written at the end of a sentence
# carries the full stop into the match, and the same DOI then indexed twice --
# once with and once without it. Two entries pointing at one study is not wrong,
# but an index whose job is exact-match lookup must not contain near-duplicates.
normalise_id <- function(id) {
  id <- sub("[[:punct:]]+$", "", id)
  # a normalised DOI may still legitimately end in a digit or letter; only
  # trailing sentence punctuation is removed above
  tolower(id)
}

idx <- character(0)
for (i in seq_len(nrow(audit))) {
  ids <- strsplit(audit$ids[i], " ")[[1]]
  ids <- unique(normalise_id(ids[nzchar(ids)]))
  for (id in ids) idx <- c(idx, paste0(id, "\t", audit$study_id[i]))
}
idx <- sort(unique(idx))
writeLines(
  c("# Corpus identifier index -- GENERATED by scripts/check_identifier_traceability.R",
    "# One identifier per line, tab-separated from the study_id it resolves to.",
    "# Diff a candidate screening list against this file before calling a record new.",
    paste0("# ", nrow(audit), " studies, ", length(idx), " identifiers, generated ", Sys.Date()),
    "",
    idx),
  index_path
)
cat("Wrote", index_path, "--", length(idx), "identifiers\n\n")

cat("=== Identifier traceability ===\n")
cat("Studies in the corpus                    :", nrow(audit), "\n")
cat("Traceable from the extraction citation   :", sum(audit$in_extraction), "\n")
cat("Traceable from the bibliography entry    :", sum(audit$in_bib), "\n")
cat("Traceable from EITHER                    :", sum(audit$has_publication_id), "\n\n")

gap_extraction <- audit[!audit$in_extraction, ]
if (nrow(gap_extraction) > 0) {
  cat("NOT traceable from the extraction citation (", nrow(gap_extraction), "):\n", sep = "")
  for (i in seq_len(nrow(gap_extraction))) {
    cat(sprintf("  %-24s bib=%s  %s\n",
                gap_extraction$study_id[i],
                ifelse(gap_extraction$in_bib[i], "yes", "NO "),
                substr(gap_extraction$ids[i], 1, 60)))
  }
  cat("\n")
}

untraceable <- audit[!audit$has_publication_id, ]
cat("NO publication identifier anywhere (", nrow(untraceable), "):\n", sep = "")
if (nrow(untraceable) == 0) {
  cat("  none\n")
} else {
  for (i in seq_len(nrow(untraceable))) {
    cat(sprintf("  %-24s (%d arm(s))  ids: %s\n", untraceable$study_id[i],
                untraceable$n_arms[i],
                ifelse(nzchar(untraceable$ids[i]), untraceable$ids[i], "NONE")))
  }
}

if (nrow(untraceable) > 0) {
  cat("\nFAIL: a study with no resolvable identifier cannot be checked against a",
      "\n      future search, which is how Ngauy 2026 was re-screened as new.\n")
  quit(status = 1)
}
cat("\nPASS: every study carries a resolvable publication identifier.\n")
