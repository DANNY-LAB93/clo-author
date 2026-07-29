suppressPackageStartupMessages(library(here))
pr <- readRDS(here::here("scripts", "R", "output", "pooled_results.rds"))

show <- function(key) {
  if (!key %in% names(pr)) { cat(key, ": ABSENT\n"); return(invisible()) }
  c_ <- pr[[key]]
  cat(sprintf("%-52s %-10s k=%s arms=%s N=%s",
              key, c_$status, c_$k_studies, c_$k_arms, c_$n_patients))
  if (identical(as.character(c_$status), "POOLED")) {
    m <- c_$primary
    cat(sprintf("  events=%d", sum(m$event, na.rm = TRUE)))
  } else {
    cat(sprintf("  reason=%s", paste(c_$reason, collapse = "; ")))
  }
  cat("\n")
}

cat("=== cells the Results text currently asserts ===\n")
for (k in c("clinical_success__resistance_class__MDR",
            "safety__resistance_class__MDR",
            "eradication__resistance_class__MDR",
            "mortality__resistance_class__MDR",
            "clinical_success__resistance_class__not-classifiable",
            "safety__resistance_class__not-classifiable",
            "mortality__resistance_class__not-classifiable",
            "clinical_success__resistance_class__XDR",
            "clinical_success__resistance_class__PDR",
            "safety__route_group__inhaled/nebulized",
            "mortality__route_group__inhaled/nebulized",
            "clinical_success__route_group__other",
            "safety__route_group__other",
            "eradication__route_group__other",
            "mortality__route_group__other",
            "clinical_success__route_group__topical/local",
            "clinical_success__route_group__IV")) show(k)

cat("\n=== zero-event cells among the not-pooled: exact Clopper-Pearson bound ===\n")
dat <- readRDS(here::here("scripts", "R", "output", "dat_analysis.rds"))
for (rg in unique(dat$route_group)) {
  sub <- dat[dat$route_group == rg, ]
  d <- sub$mortality_n
  ok <- !is.na(d)
  if (!any(ok)) next
  deaths <- sum(d[ok]); n <- sum(sub$n_arm[ok])
  bound <- if (deaths == 0) 1 - 0.025^(1 / n) else NA
  cat(sprintf("route=%-18s deaths=%d N=%d  arms=%d", rg, deaths, n, sum(ok)))
  if (deaths == 0) cat(sprintf("  CP 97.5%% upper = %.1f%%", 100 * bound))
  cat("\n")
}

cat("\n=== XDR / PDR span across outcomes (text claims ranges) ===\n")
for (lev in c("XDR", "PDR")) {
  ks <- c(); ns <- c()
  for (o in c("clinical_success", "safety", "eradication", "mortality")) {
    key <- paste0(o, "__resistance_class__", lev)
    if (key %in% names(pr)) { ks <- c(ks, pr[[key]]$k_studies); ns <- c(ns, pr[[key]]$n_patients) }
  }
  cat(sprintf("%s: k range %d-%d, N range %d-%d\n", lev, min(ks), max(ks), min(ns), max(ns)))
}

cat("\n=== modality: how many antibiotic-monotherapy / phage-monotherapy arms? ===\n")
print(table(dat$modality_group, useNA = "ifany"))
