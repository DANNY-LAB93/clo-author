# ==============================================================================
# 09_table1_characteristics.R
# Purpose: Table 1 (Study Characteristics) -- one row per study-arm, all 16
#          arms across 14 studies (the full cleaned dataset, including the
#          one arm excluded from pooling), per the deferred-table note in
#          results.tex Section 3.2. Exports a bare `tabular` environment only
#          (INV-13; main.tex wraps with threeparttable + tablenotes).
# Project: phage_therapy_mdr_pseudomonas
# Inputs:  data/cleaned/phage_therapy_extraction_dataset.csv
# Outputs: paper/tables/phage_therapy_mdr_pseudomonas/table1_study_characteristics.tex
# Requires: 01_setup.R has been run (paths, packages, functions available)
# ==============================================================================

dat_table1 <- read_csv(data_path, show_col_types = FALSE)

#' Escape LaTeX-special characters in generated table cell text
#' (same convention as 08_tables.R's escape_tex -- % and _ both appear in
#' this dataset's free-text fields, e.g. geographic_source parentheticals).
escape_tex <- function(x) {
  x <- gsub("%", "\\\\%", x)
  x <- gsub("_", "\\\\_", x)
  x
}

# --- Short author-year labels (no automated derivation possible from the
# extraction schema alone; hand-mapped once against Bibliography_base.bib
# and results.tex Section 3.2's own citation list, kept in sync with both) --
study_label <- c(
  Tkhilaishvili2020    = "Tkhilaishvili 2020",
  Blasco2023           = "Blasco 2023",
  Ngauy2026            = "Ngauy 2026",
  Ferry2022            = "Ferry 2022",
  Liu2025_perinephric  = "Liu 2025",
  Racenis2023_LVAD     = "Racenis 2023",
  Racenis2022_femur    = "Racenis 2022",
  Pirnay2024           = "Pirnay 2024",
  Onallah2023_PASA16   = "Onallah 2023",
  Weiner2025_BX004A    = "Weiner 2025",
  Jault2019_PhagoBurn  = "Jault 2019",
  Leitner2021          = "Leitner 2021",
  ArmataAP_PA02        = "SWARM-P.a.\\ 2022",
  Aslam2019            = "Aslam 2019",
  Kohler2023           = "K\\\"ohler 2023",
  Chan2025             = "Chan 2025",
  Law2019              = "Law 2019",
  Hahn2023             = "Hahn 2023",
  Leveque2023          = "Lev\\^eque 2023",
  Duplessis2018        = "Duplessis 2018",
  Denis2026            = "Denis 2026",
  Malhotra2026         = "Malhotra 2026",
  Yang2025             = "Yang 2025",
  Li2025_biliary       = "Li 2025",
  Chan2018_omko1       = "Chan 2018",
  Arya2026_pji         = "Arya 2026"
)

design_abbrev <- c(
  "case report"          = "Case rpt.",
  "case series"          = "Case series",
  "RCT"                  = "RCT",
  "retrospective cohort" = "Retro."
)

resistance_abbrev <- c(
  "MDR"             = "MDR",
  "XDR"             = "XDR",
  "PDR"             = "PDR",
  "not-classifiable" = "NC"
)

country_abbrev <- c(
  "Multicentre"           = "Multi.",
  "Multicentre Europe"    = "Multi.\\ (EU)",
  "Multicentre CF trial"  = "Multi.\\ (CF)"
)

route_abbrev <- c(
  "topical/local"      = "Topical",
  "IV"                 = "IV",
  "inhaled/nebulized"   = "Inhaled",
  "other"              = "Other"
)

table1_rows <- dat_table1 |>
  mutate(
    study_col      = unname(study_label[study_id]),
    design_col      = unname(design_abbrev[study_design]),
    resistance_col  = unname(resistance_abbrev[resistance_class]),
    route_col       = {
      collapsed <- collapse_category(route)
      out <- ifelse(collapsed %in% names(route_abbrev), unname(route_abbrev[collapsed]), collapsed)
      # An arm whose source did not report the administration route (route = NA,
      # e.g. Malhotra 2026) shows "NR" (not reported) rather than a bare "NA".
      ifelse(is.na(collapsed) | collapsed == "NA" | is.na(out), "NR", out)
    },
    modality_col    = ifelse(
      grepl("^phage\\+antibiotic combination", modality),
      "Combo",
      ifelse(
        grepl("^phage monotherapy", modality),
        "Phage mono",
        collapse_category(modality)
      )
    ),
    country_col     = {
      collapsed <- collapse_category(geographic_source)
      ifelse(collapsed %in% names(country_abbrev), unname(country_abbrev[collapsed]), collapsed)
    },
    pooling_col     = ifelse(
      grepl(
        "NOT usable in the primary Pseudomonas-specific proportion pooling",
        incomplete_reason
      ) & !is.na(incomplete_reason),
      "Excluded$^{a}$",
      "Pooled"
    )
  ) |>
  select(
    study_col, country_col, design_col, n_arm, resistance_col,
    route_col, modality_col, pooling_col
  )

# INV-17: pre-allocate/construct rows via vapply rather than growing a
# vector inside a for loop.
table1_row_lines <- vapply(seq_len(nrow(table1_rows)), function(i) {
  sprintf(
    "%s & %s & %s & %d & %s & %s & %s & %s \\\\",
    table1_rows$study_col[i], escape_tex(table1_rows$country_col[i]),
    table1_rows$design_col[i], table1_rows$n_arm[i],
    table1_rows$resistance_col[i], escape_tex(table1_rows$route_col[i]),
    escape_tex(table1_rows$modality_col[i]), table1_rows$pooling_col[i]
  )
}, character(1L))

tex_lines_table1 <- c(
  "\\begin{tabular}{llccccll}",
  "\\toprule",
  paste(
    "Study & Country/region & Design & $n$ & Resistance &",
    "Route & Modality & Pooling \\\\"
  ),
  "\\midrule",
  table1_row_lines,
  "\\bottomrule",
  "\\end{tabular}"
)

writeLines(
  tex_lines_table1,
  file.path(table_dir, "table1_study_characteristics.tex")
)
message(
  "Wrote paper/tables/", PROJECT_SLUG, "/table1_study_characteristics.tex (",
  nrow(table1_rows), " rows)"
)

message("09_table1_characteristics.R complete.")
