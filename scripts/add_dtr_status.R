# One-off: add a `dtr_status` column to the cleaned extraction dataset.
#
# WHY. Magiorakos MDR/XDR/PDR counts NON-SUSCEPTIBLE CATEGORIES. Difficult-to-
# treat resistance (DTR; Kadri et al., Clin Infect Dis 2018) instead asks
# whether ALL first-line agents are lost -- non-susceptibility to every
# beta-lactam AND every fluoroquinolone -- because that is what forces a
# clinician onto reserve agents. Since the newer antipseudomonals
# (ceftolozane-tazobactam, ceftazidime-avibactam, imipenem-relebactam,
# cefiderocol) redrew the MDR boundary, DTR is the category IDSA guidance and
# the modern P. aeruginosa literature use for treatment decisions.
#
# DTR IS NOT A FIFTH LEVEL OF resistance_class. It cuts across it: an isolate
# can be MDR and DTR, or MDR and not DTR (three non-susceptible categories while
# cefepime still works). Encoding it as a sibling level would force a false
# exclusivity. It is therefore a SEPARATE binary axis, stratified in parallel.
#
# CODING RULE, deliberately conservative:
#   "yes"           - PDR arms only. PDR means non-susceptibility to all agents
#                     in all categories, which logically entails non-
#                     susceptibility to all beta-lactams and all
#                     fluoroquinolones. PDR therefore ENTAILS DTR; no panel is
#                     needed for the inference.
#   "not-derivable" - everything else. XDR does NOT entail DTR (it permits
#                     susceptibility in up to two categories, which may include
#                     a beta-lactam), and MDR certainly does not. Deriving DTR
#                     for those arms requires an agent-level antibiogram
#                     covering all beta-lactams and both fluoroquinolones.
#
# WHY ALMOST NOTHING IS DERIVABLE. Of 31 pooling-eligible arms, exactly one
# (Liu 2025 Patient 2) carries a published panel wide enough to call DTR on the
# data rather than by entailment. The rest name between one and five agents --
# usually the drug that was administered, not an antibiogram. This is the
# finding: the DTR cells fail for ABSENT DATA, not for too few patients, and
# they are the only cells in the review that fail for that reason.
p <- "data/cleaned/phage_therapy_extraction_dataset.csv"
d <- read.csv(p, stringsAsFactors = FALSE, check.names = FALSE)

stopifnot(!"dtr_status" %in% names(d))

d$dtr_status <- ifelse(
  !is.na(d$resistance_class) & d$resistance_class == "PDR",
  "yes",
  "not-derivable"
)

# Place it immediately after resistance_class_source so the resistance block
# reads together.
pos <- which(names(d) == "resistance_class_source")
ord <- append(setdiff(seq_along(d), which(names(d) == "dtr_status")),
              which(names(d) == "dtr_status"), after = pos)
d <- d[, ord]

write.csv(d, p, row.names = FALSE, na = "NA")

cat("dtr_status added.\n")
print(table(d$dtr_status, d$resistance_class, useNA = "ifany"))
