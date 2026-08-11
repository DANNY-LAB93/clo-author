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

out_dir <- here::here("metaanalisis", "scripts_R", "output")

raw <- readr::read_csv(
  here::here("metaanalisis", "datos", "phage_therapy_extraction_dataset.csv"),
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
    # OJO: la clase de caracteres original era "[.,;:)\\]]+$", que en las
    # expresiones regulares de base R (TRE) NO escapa el corchete dentro de la
    # clase -- la barra invertida es literal ahí. El patrón exigía terminar en
    # "]" y por eso nunca recortó nada: el índice llevaba DOI acabados en punto
    # ("10.2147/IDR.S413900.") desde el principio.
    if (nm == "doi") vals <- unique(sub("[.,;:]+$", "", vals))
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

# ---- qué entrada bib pertenece a qué estudio --------------------------------
# El stem (autor+año) NO identifica un artículo. Liu2025_perinephric (mLife,
# serie de dos casos) y Liu2025_ijaa (metaanálisis en Int J Antimicrob Agents)
# comparten stem "liu2025", así que el estudio incluido absorbió el DOI y el
# PMID del metaanálisis. Como la auditoría de control positivo indexa por PMID
# y el único PMID heredado era el ajeno, excluir correctamente el metaanálisis
# hacía saltar la auditoría por el artículo equivocado.
#
# Regla: si el study_id lleva sufijo discriminante tras el primer "_", la clave
# bib debe llevarlo también. Si no lo lleva y hay varias candidatas, se para en
# vez de fusionarlas: una fusión silenciosa es indistinguible de un acierto.
bib_tail <- function(x) tolower(sub("^[^_]*_?", "", x))

# El discriminante del study_id solo se exige cuando hay ambigüedad de verdad.
# Study_id y clave bib nombran cosas distintas -- Weiner2025_BX004A (el producto)
# vive en Weiner2025_natcomms (la revista) -- así que pedirlo siempre dejaría sin
# DOI a estudios que tienen una única entrada perfectamente identificada.
match_bib_keys <- function(sid) {
  cand <- names(bib_entries)[bib_stem(names(bib_entries)) == bib_stem(sid)]
  if (length(cand) <= 1) return(cand)
  tail <- bib_tail(sid)
  hit <- if (nzchar(tail)) cand[grepl(tail, tolower(cand), fixed = TRUE)] else character(0)
  if (length(hit) == 1) return(hit)
  stop("clave bib ambigua para ", sid, ": ", paste(cand, collapse = ", "),
       " -- el study_id necesita un sufijo que solo case con una de ellas")
}

# ---- identificadores propios de una entrada bib -----------------------------
# El DOI se lee SOLO del campo estructurado doi = {...}. Los DOI que aparecen
# dentro de note son de otros artículos: la nota de Li2025_hlife_biliary cita
# la tabulación de casos de Chen et al. 2026 (10.1111/jgh.70308) como fuente
# secundaria, y ese DOI quedó indexado como si fuera el estudio.
# PMID y PMC sí se leen de la nota, porque es donde esta revisión registra la
# verificación de la propia entrada.
ids_from_entry <- function(chunk) {
  out <- character(0)
  doi <- str_match(chunk, "(?m)^[ \t]*doi[ \t]*=[ \t]*\\{([^}]+)\\}")[, 2]
  if (!is.na(doi)) out <- c(out, paste0("doi:", tolower(trimws(doi))))
  note <- str_match(chunk, "(?s)note[ \t]*=[ \t]*\\{(.*)")[, 2]
  if (!is.na(note)) {
    for (nm in c("pmid", "pmc", "nct")) {
      m <- str_match_all(note, ID_PATTERNS[[nm]])[[1]]
      if (nrow(m) > 0) out <- c(out, paste0(nm, ":", unique(m[, 2])))
    }
    # Excepción deliberada a "los DOI de la nota son de otros": una fe de
    # erratas es OTRO informe DEL MISMO estudio, no otro estudio. La nota de
    # Weiner2025_BX004A registra así el erratum de Nat Commun 2026, y perderlo
    # dejaría a ese registro sin reconocer si aparece en una búsqueda futura.
    er <- str_match_all(
      note,
      # El hueco NO puede excluir puntos: la cita intermedia los lleva
      # ("Erratum: Nat Commun. 2026 Feb 27;17(1):2057, doi: 10.1038/...").
      "(?i)(?:erratum|corrigendum|correction)[\\s\\S]{0,160}?doi:?[ \t]*(10\\.[0-9]{4,9}/[^ ,;)}]+)"
    )[[1]]
    if (nrow(er) > 0) {
      out <- c(out, paste0("doi:", tolower(sub("[.,;:]+$", "", unique(er[, 2])))))
    }
  }
  unique(out)
}

# ---- descarte de identificadores ajenos -------------------------------------
# El corpus cribado sabe, para cada PMID, con qué DOI se publicó. Eso convierte
# "¿este identificador es de este estudio?" en una pregunta decidible: si el
# PMID resuelve a un artículo cuyo DOI no es el DOI estructurado de la entrada
# bib, es de otro artículo y se descarta. Los identificadores que el corpus no
# puede resolver (PMC, NCT, PMID ausentes del pozo) se conservan: descartarlos
# por no poder comprobarlos perdería trazabilidad real por una sospecha.
corpus <- readr::read_csv(
  here::here("revision_sistematica", "cribado", "screening_stage2_priorizado.csv"),
  col_select = c("doi", "pmid"), show_col_types = FALSE,
  progress = FALSE
)
corpus <- corpus[!is.na(corpus$pmid) & nzchar(as.character(corpus$pmid)), ]
doi_of_pmid <- setNames(tolower(as.character(corpus$doi)),
                        as.character(corpus$pmid))

drop_foreign <- function(ids, from_bib, sid, matched_keys = character(0)) {
  # unlist() sobre una lista vacía devuelve NULL, no character(0).
  ids <- as.character(ids)
  from_bib <- as.character(from_bib)
  if (length(ids) == 0) return(character(0))

  # Un identificador que OTRA entrada bib reclama como propio no puede ser de
  # este estudio. Así caen los PMC que el corpus no sabe resolver: PMC11216685 y
  # PMC9724797 son de las dos revisiones de Eur Respir Rev (Vaezi2024_errev,
  # Mitropoulou2022_errev), citadas como fuente secundaria en la extracción de
  # Maddocks2019 y absorbidas junto con sus PMID.
  otras <- setdiff(names(bib_entries), matched_keys)
  ajenos <- unique(unlist(lapply(bib_entries[otras], ids_from_entry)))
  if (length(ajenos) > 0) {
    fuera <- ids %in% ajenos
    if (any(fuera)) {
      message("  ", sid, ": descartados ", sum(fuera),
              " identificadores de otra entrada bib -- ",
              paste(ids[fuera], collapse = " "))
      ids <- ids[!fuera]
    }
  }
  if (length(ids) == 0) return(character(0))

  own <- from_bib[startsWith(from_bib, "doi:")]
  if (length(own) == 0) return(ids)      # sin DOI propio no hay con qué contrastar
  # Un DOI no distingue mayúsculas y arrastra puntuación de la prosa que lo
  # cita. Sin normalizar ambos lados, "10.1164/rccm.201904-0839LE" leído de la
  # extracción no coincidiría con el mismo DOI leído del campo estructurado y el
  # estudio se descartaría a sí mismo.
  norm <- function(d) sub("[.,;:]+$", "", tolower(d))
  # Un estudio puede tener más de un informe propio (artículo + fe de erratas),
  # así que se contrasta contra el CONJUNTO de sus DOI, no contra uno solo.
  own_doi <- norm(sub("^doi:", "", own))
  keep <- vapply(ids, function(id) {
    if (startsWith(id, "doi:")) return(norm(sub("^doi:", "", id)) %in% own_doi)
    if (startsWith(id, "pmid:")) {
      # `[[` sobre un nombre inexistente aborta; `[` devuelve NA, que es lo que
      # queremos: un PMID que no está en el pozo no se puede desmentir.
      d <- unname(doi_of_pmid[sub("^pmid:", "", id)])
      if (length(d) == 0 || is.na(d) || !nzchar(d)) return(TRUE)
      # Cochrane CENTRAL asigna un DOI sustituto propio (10.1002/central/cn-...)
      # al registro que indexa; no es el DOI del artículo, así que no sirve para
      # desmentir nada. Sin esta excepción, Leitner2021 perdía su PMID real.
      if (startsWith(d, "10.1002/central/")) return(TRUE)
      return(norm(d) %in% own_doi)
    }
    TRUE
  }, logical(1))
  if (any(!keep)) {
    message("  ", sid, ": descartados ", sum(!keep), " identificadores ajenos -- ",
            paste(ids[!keep], collapse = " "))
  }
  ids[keep]
}

# ---- audit ------------------------------------------------------------------
studies <- sort(unique(raw$study_id))
rows <- vector("list", length(studies))

for (i in seq_along(studies)) {
  sid <- studies[i]
  arms <- raw[raw$study_id == sid, ]
  from_extraction <- unique(unlist(lapply(
    c(arms$extraction_citation, arms$incomplete_reason), find_ids)))

  matched_keys <- match_bib_keys(sid)
  from_bib <- unique(unlist(lapply(bib_entries[matched_keys], ids_from_entry)))

  # extraction_citation e incomplete_reason son prosa de PROCEDENCIA: nombran la
  # fuente de la que se extrajeron los datos, que a menudo es un tercero. La
  # fila de Maddocks2019 cita dos revisiones de Eur Respir Rev como fuentes
  # secundarias, y sus dos DOI y sus dos PMID acabaron indexados como si fueran
  # el informe de Maddocks. Pero descartar la extracción entera es peor: para
  # ocho estudios es el único sitio donde consta su PMID. Se conserva la unión y
  # se filtra contra el corpus (ver drop_foreign): un identificador que resuelve
  # a un artículo con OTRO DOI no es de este estudio.
  all_ids <- drop_foreign(unique(c(from_extraction, from_bib)), from_bib, sid,
                         matched_keys)

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
