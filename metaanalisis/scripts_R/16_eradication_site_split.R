# Does the eradication construct hold together, or is it two constructs?
#
# WHY THIS EXISTS. A round-6 microbiology referee argued that the pooled
# eradication proportion is a category error: it aggregates sterile-site culture
# negativity, absence from a chronically colonised airway, single-site wound
# swabs, an explanted implant, and relapse-free follow-up with no culture at all.
# The specific objection was that in ESTABLISHED chronic airway infection --
# cystic fibrosis, primary ciliary dyskinesia with bronchiectasis, chronic
# interstitial-lung-disease colonisation -- eradication is neither achieved nor
# the therapeutic target. The field's endpoints there are bacterial density,
# exacerbation frequency and ppFEV1; "eradication" is a protocol concept reserved
# for EARLY, new acquisition, not for the established biofilm state.
#
# The referee proposed a falsifiable test: pool within site class and show
# whether the split is what generates the between-arm variance. This runs it.
#
# THE CLASSIFICATION IS AN EXPLICIT LIST, NOT A KEYWORD RULE. A first attempt
# used regular expressions over the recorded free text and misclassified
# Rubalskii's Patient 8 -- a thoracotomy WOUND infection after lung
# transplantation -- as chronic airway, because the phrase "lung transplant"
# appears in its description. Every arm below was read and assigned by hand, and
# the list is stated here so a reader can disagree with any single call.

suppressPackageStartupMessages({
  library(here)
  library(meta)
})

out_dir <- here::here("metaanalisis", "scripts_R", "output")
dat <- readRDS(file.path(out_dir, "dat_analysis.rds"))

# Arms whose infection is ESTABLISHED chronic airway colonisation, where
# eradication is not the therapeutic target:
#   Chan2025_MDR / _PDR        cystic-fibrosis cohort, sputum CFU endpoints
#   Zaldastanishvili2021_P1    cystic fibrosis, chronic lung infection since childhood
#   Zaldastanishvili2021_P2    primary ciliary dyskinesia with bronchiectasis
#   Li2023_ILD_A               progressive interstitial lung disease, chronic colonisation
#   PardoFreire2025_A          cystic fibrosis and lung transplant, chronic background
#   Law2019_A                  cystic fibrosis, pneumonia on a chronic airway
#   Leveque2023_A              chronic bronchopulmonary infection post lung transplant
#
# Deliberately NOT in this list: Rubalskii2020_P8 (thoracotomy wound after lung
# transplantation -- a surgical-site infection, not an airway one), and the
# acute-pneumonia arms (Yang 2025, Teney 2024, Maddocks 2019), where clearance
# is a coherent goal.
CHRONIC_AIRWAY_ARMS <- c(
  "Chan2025_MDR", "Chan2025_PDR",
  "Zaldastanishvili2021_P1", "Zaldastanishvili2021_P2",
  "Li2023_ILD_A", "PardoFreire2025_A",
  "Law2019_A", "Leveque2023_A"
)

erad <- dat[!is.na(dat$microbio_eradication_n), ]
erad$site_class <- ifelse(erad$study_arm_id %in% CHRONIC_AIRWAY_ARMS,
                          "chronic airway", "other site")

pool_one <- function(df, label) {
  if (nrow(df) == 0) return(NULL)
  m <- try(suppressWarnings(meta::metaprop(
    event = df$microbio_eradication_n, n = df$n_arm, studlab = df$study_arm_id,
    sm = "PLOGIT", method = "GLMM", method.tau = "ML",
    method.random.ci = "HK", prediction = TRUE
  )), silent = TRUE)
  if (inherits(m, "try-error")) return(NULL)
  list(
    label = label,
    k_arms = nrow(df),
    k_studies = length(unique(df$study_id)),
    n_patients = sum(df$n_arm, na.rm = TRUE),
    n_events = sum(df$microbio_eradication_n, na.rm = TRUE),
    crude = sum(df$microbio_eradication_n, na.rm = TRUE) / sum(df$n_arm, na.rm = TRUE),
    p_hat = plogis(m$TE.random),
    ci_low = plogis(m$lower.random),
    ci_high = plogis(m$upper.random),
    tau2 = m$tau2
  )
}

full <- pool_one(erad, "all sites (as reported)")
air  <- pool_one(erad[erad$site_class == "chronic airway", ], "chronic airway")
oth  <- pool_one(erad[erad$site_class == "other site", ], "other site")

split <- list(full = full, chronic_airway = air, other_site = oth,
              arms_chronic_airway = CHRONIC_AIRWAY_ARMS)
saveRDS(split, file.path(out_dir, "eradication_site_split.rds"))

fmt <- function(x) if (is.null(x)) "--" else sprintf("%.1f%%", 100 * x)
message("Eradication by site class:")
for (r in list(full, air, oth)) {
  if (is.null(r)) next
  message(sprintf(
    "  %-24s k=%2d arms=%2d N=%3d events=%3d crude=%s pooled=%s [%s, %s] tau2=%.3f",
    r$label, r$k_studies, r$k_arms, r$n_patients, r$n_events,
    fmt(r$crude), fmt(r$p_hat), fmt(r$ci_low), fmt(r$ci_high), r$tau2))
}
if (!is.null(full) && !is.null(air) && !is.null(oth)) {
  message(sprintf(
    "  tau^2 falls from %.3f (all sites) to %.3f (chronic airway) and %.3f (other sites).",
    full$tau2, air$tau2, oth$tau2))
}
