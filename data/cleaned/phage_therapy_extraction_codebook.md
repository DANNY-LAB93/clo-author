# Codebook — `phage_therapy_extraction_dataset.csv`

One row per study-arm (not per patient, except where a study reports only n=1). Produced by `scripts/R/clean_phage_extraction.R` from `data/raw/phage_therapy_extraction_raw.csv`, per the schema in `quality_reports/strategy/phage_therapy_mdr_pseudomonas/pseudo_code.md` Sec. 1.

| Column | Type | Description |
|---|---|---|
| `study_id` | character | First-author + year identifier |
| `arm_id` | character | Unique study-arm identifier (`study_arm_id` in downstream pooling code); falls back to `study_id` when arm structure isn't yet confirmed |
| `n_arm` | integer | Number of patients in this arm |
| `pathogen_scope` | character | `Pseudomonas-only`, `mixed-pathogen-with-Pseudomonas-subgroup`, or `mixed-not-separable` (auto-excluded by the cleaning script's eligibility filter) |
| `resistance_class` | character | `MDR`, `XDR`, `PDR`, or `not-classifiable` |
| `resistance_class_source` | character | `independently-verified` (re-derived from reported susceptibility data per Magiorakos et al. 2012), `author-reported`, or `not-classifiable` |
| `route` | character | Route(s) of phage administration |
| `modality` | character | `phage monotherapy`, `phage+antibiotic combination`, or free-text noting comparator structure for RCTs |
| `clinical_success_n` | integer | Numerator for clinical success/improvement (NA if outcome is continuous/time-to-event, not binary) |
| `clinical_success_definition` | character | Per-study definition of "success" (heterogeneous across studies — document per Open Questions in the research spec) |
| `adverse_event_n` | integer | Numerator for ≥1 adverse event |
| `microbio_eradication_n` | integer | Numerator for microbiological eradication |
| `mortality_n` | integer | Numerator for death |
| `los_days` | numeric | Length of hospitalization, if reported |
| `resistance_emergence_n` | integer | Numerator for phage or antibiotic resistance emerging during treatment |
| `study_design` | character | RCT, retrospective cohort, prospective cohort, case series, case report |
| `data_provenance` | character | `independently-extracted`, `cross-validated-against-Liu2025`, per the Tier 1/2/3 reuse policy in the strategy memo Sec. 3 |
| `rob_source` | character | Risk-of-bias assessment source, if reused from Liu et al. (2025)'s supplementary dataset |
| `publication_year` | integer | |
| `journal_tier` | character | Qualitative venue tier, for narrative context only (not used in pooling) |
| `geographic_source` | character | Country/region/consortium |
| `extraction_citation` | character | Documented primary-source locator (page/table/quote) per the Sec. 3 audit requirement; also used to log verification method (direct fetch, WebSearch, PubMed esummary/efetch, etc.) |
| `extraction_status` | character | `COMPLETE`, `EXTRACTION_INCOMPLETE`, `EXCLUDED_WRONG_PATHOGEN`, `EXCLUDED_DUPLICATE` |
| `incomplete_reason` | character | What's missing and why, for `EXTRACTION_INCOMPLETE`/`EXCLUDED_*` rows |
| `study_arm_id` (derived) | character | Constructed by the cleaning script: `arm_id` if present, else `study_id` — the unique label fed to `metaprop()`/`pool_stratum()` |

## Known Limitations (see `quality_reports/data_extraction_summary_phage_therapy_mdr_pseudomonas.md` for detail)

- Monotherapy stratum is empty (0 study-arms) — both candidate studies (Krakhotkin 2025, Leitner 2021) failed on full-text verification.
- Pirnay 2024 (largest single study, 49 Pseudomonas patients) is only partially represented — 11 patients with full detail from the paper's Table 2 case narratives; the remaining ~38 are in a supplementary file not yet located.
- Several rows have `clinical_success_n = NA` because their primary outcome is continuous or time-to-event, not a binary proportion (Weiner 2025, Jault 2019) — these are not poolable in the primary proportion meta-analysis and should be reported narratively.
