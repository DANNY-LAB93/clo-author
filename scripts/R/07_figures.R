# ==============================================================================
# 07_figures.R
# Purpose: Publication-ready figures -- forest plots (the domain-standard
#          visualization for pooled proportions with 95% CIs, per
#          .claude/references/domain-profile.md Field Conventions) for every
#          POOLED cell, plus the small-study/sample-size eyeball scatter
#          (falsification Test 3).
# Project: phage_therapy_mdr_pseudomonas
# Inputs:  scripts/R/output/pooled_results.rds
#          scripts/R/output/falsification_small_study_data.rds
# Outputs: paper/figures/phage_therapy_mdr_pseudomonas/forest_clinical_success_overall.pdf
#          paper/figures/phage_therapy_mdr_pseudomonas/forest_safety_overall.pdf
#          paper/figures/phage_therapy_mdr_pseudomonas/forest_clinical_success_resistance_notclassifiable.pdf
#          paper/figures/phage_therapy_mdr_pseudomonas/forest_clinical_success_route_other.pdf
#          paper/figures/phage_therapy_mdr_pseudomonas/small_study_eyeball.pdf
# Requires: 01_setup.R, 04_estimation.R, 06_falsification.R have been run
# ==============================================================================

pooled_results <- readRDS(file.path(output_dir, "pooled_results.rds"))

#' Save a forest plot for a POOLED pool_stratum() cell result
#'
#' Uses meta::forest() (the package's own vetted forest-plot renderer,
#' consistent with the domain profile's "forest plots are the standard
#' visualization" convention). No title is drawn on the plot itself
#' (INV-12 principle applied even outside ggplot) -- the caption in
#' main.tex carries the title.
# Clean, publication-quality study labels for the forest plots. The pooling
# models carry the raw study_arm_id key (e.g. "Pirnay2024_MDR") as studlab;
# meta::forest() prints that key verbatim, which is dataset-internal, not
# reader-facing (content-standards.md: figure labels must be human-readable).
# This lookup is display-only -- it is applied to model$studlab immediately
# before rendering and never touches the pooled estimate, so it cannot alter
# any numeric result. A study contributing more than one arm to the same plot
# gets a disambiguating suffix (resistance class for Pirnay's three arms;
# patient number for the two-patient case series) so no two rows collide.
forest_studlab <- c(
  ArmataAP_PA02_highdose    = "Armata (2022)",
  Aslam2019_P1              = "Aslam (2019), Pt 1",
  Aslam2019_P2              = "Aslam (2019), Pt 2",
  Blasco2023_A              = "Blasco (2023)",
  Ferry2022_A               = "Ferry (2022)",
  Jault2019_PhagoBurn_phage = "Jault (2019)",
  Leitner2021_pyophage      = "Leitner (2021)",
  Liu2025_perinephric_P1    = "Liu (2025), Pt 1",
  Liu2025_perinephric_P2    = "Liu (2025), Pt 2",
  Ngauy2026_A               = "Ngauy (2026)",
  Onallah2023_PASA16_agg    = "Onallah (2023)",
  Pirnay2024_XDR            = "Pirnay (2024), XDR",
  Pirnay2024_MDR            = "Pirnay (2024), MDR",
  Pirnay2024_PDR            = "Pirnay (2024), PDR",
  Racenis2022_femur_A       = "Racenis (2022)",
  Racenis2023_LVAD_A        = "Racenis (2023)",
  Tkhilaishvili2020_A       = "Tkhilaishvili (2020)",
  Weiner2025_BX004A_phage   = "Weiner (2025)",
  Kohler2023_A              = "Köhler (2023)",
  Chan2025_MDR              = "Chan (2025), MDR",
  Chan2025_PDR              = "Chan (2025), PDR",
  Law2019_A                 = "Law (2019)",
  Hahn2023_A                = "Hahn (2023)",
  Leveque2023_A             = "Levêque (2023)",
  Duplessis2018_A           = "Duplessis (2018)",
  Denis2026_A               = "Denis (2026)",
  Malhotra2026_A            = "Malhotra (2026)",
  Yang2025_A                = "Yang (2025)",
  Li2025_biliary_A          = "Li (2025)",
  Chan2018_omko1_A          = "Chan (2018)",
  Arya2026_pji_A            = "Arya (2026)"
)

#' Map a vector of raw study-arm keys to clean author-year labels.
#' Any key not in the lookup falls through unchanged, so a newly added arm
#' surfaces as its raw key (visible, not silently dropped) rather than NA.
clean_studlab <- function(keys) {
  mapped <- forest_studlab[keys]
  ifelse(is.na(mapped), keys, unname(mapped))
}

save_forest_plot <- function(model, file_path, convergence_note = NULL) {
  model$studlab <- clean_studlab(model$studlab)
  # A cell that fell back to a fixed-effect model (GLMM and logit-DL both failed
  # to converge; pool_stratum()'s safe_metaprop() cascade) has no random-effects
  # summary or prediction interval -- draw the common (fixed-effect) diamond and
  # suppress the prediction interval, so meta::forest() doesn't error on a
  # missing TE.random. Random-effects cells are drawn as before.
  has_random <- !is.null(model$TE.random) && is.finite(model$TE.random)
  grDevices::pdf(file_path, width = 8, height = max(4, 0.4 * model$k + 2), family = "serif")
  meta::forest(
    model,
    common = !has_random,
    random = has_random,
    prediction = has_random,
    print.tau2 = has_random,
    print.I2 = TRUE,
    leftlabs = c("Study", "Events", "Total"),
    rightlabs = c("Proportion", "95% CI"),
    xlab = "Proportion"
  )
  note2 <- convergence_note
  if (!has_random) {
    fe_note <- "Fixed-effect model shown (random-effects GLMM and logit-DL did not converge for this cell)."
    note2 <- if (is.null(convergence_note)) fe_note else paste(convergence_note, fe_note)
  }
  if (!is.null(note2)) {
    graphics::mtext(note2, side = 1, line = 4, cex = 0.7, adj = 0)
  }
  grDevices::dev.off()
}

forest_targets <- list(
  clinical_success_overall = "clinical_success__overall",
  safety_overall            = "safety__overall",
  # Superseded by the MDR-stratified cell below once the Pirnay 2024
  # resistance-stratified re-extraction (2026-07-22) moved its patients out
  # of "not-classifiable" into MDR/XDR/PDR -- this cell dropped to k=2 and
  # is no longer POOLED. Left in the target list (skipped gracefully by the
  # loop's status check below) rather than silently deleted, so a stale
  # cached .pdf from a prior run is never mistaken for current output.
  clinical_success_resistance_notclassifiable =
    "clinical_success__resistance_class__not-classifiable",
  clinical_success_resistance_MDR = "clinical_success__resistance_class__MDR",
  clinical_success_route_other = "clinical_success__route_group__other"
)

for (fig_name in names(forest_targets)) {
  key <- forest_targets[[fig_name]]
  r <- pooled_results[[key]]
  if (is.null(r) || r$status != "POOLED") {
    message("Skipping forest plot for '", key, "': not a POOLED cell.")
    next
  }
  note <- if (r$convergence_flag != "CONVERGED") {
    sprintf("Note: %s", r$primary_model_used)
  } else {
    NULL
  }
  save_forest_plot(
    r$primary,
    file.path(figure_dir, paste0("forest_", fig_name, ".pdf")),
    convergence_note = note
  )
  message("Saved forest plot: forest_", fig_name, ".pdf")
}

# --- Small-study/sample-size eyeball check (falsification Test 3) --------------
small_study_data <- readRDS(file.path(output_dir, "falsification_small_study_data.rds"))

p_small_study <- ggplot(small_study_data, aes(x = inv_sqrt_n, y = crude_proportion)) +
  geom_point(size = 2.2, shape = 16, alpha = 0.8) +
  geom_smooth(method = "lm", se = TRUE, linewidth = 0.6, linetype = "dashed", color = "grey30") +
  scale_x_continuous(name = expression(1 / sqrt(n))) +
  scale_y_continuous(name = "Crude clinical success proportion", limits = c(0, 1)) +
  theme_minimal(base_family = "serif", base_size = 12) +
  theme(panel.grid.minor = element_blank())

# suppressWarnings: ggplot2's internal gtable/legend-key construction emits a
# benign "no non-missing arguments to max" warning on some point/ribbon-layer
# combinations with this few observations -- diagnosed via sys.calls() to
# originate inside ggplot_gtable(), not from project data or code; confirmed
# the rendered figure is correct before suppressing.
suppressWarnings(
  ggsave(
    file.path(figure_dir, "small_study_eyeball.pdf"),
    plot = p_small_study, width = 6, height = 4.5, device = "pdf"
  )
)
message("Saved figure: small_study_eyeball.pdf")

message("07_figures.R complete.")
