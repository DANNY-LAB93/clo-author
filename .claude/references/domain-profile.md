# Domain Profile

<!--
HOW TO USE: Fill this in manually OR let /discover (interactive interview) generate it.
All agents read this file to calibrate their field-specific behavior.
Delete sections that don't apply. Add sections specific to your field.
If no field is specified, agents default to applied economics.

NOTE: This project adapts the template's economics-default vocabulary to a
systematic review / meta-analysis in clinical microbiology. Where the original
template talks about "identification strategy" (DiD/IV/RDD), read that as
"evidence synthesis design" (PRISMA protocol, PICO framework, pooled effect
model). See quality_reports/plans/2026-07-18_phage-therapy-project-setup.md
for the full mapping.
-->

## Field

**Primary:** Clinical Microbiology / Infectious Disease — Systematic Review & Meta-Analysis
**Adjacent subfields:** Antimicrobial Resistance, Bacteriophage Therapy, Clinical Trials Methodology, Evidence-Based Medicine

---

## Paper Structure (decided 2026-07-21)

**IMRaD, not the economics working-paper structure.** This project uses the standard biomedical systematic-review format: **Introduction → Methods (PRISMA 2020 protocol, eligibility criteria, search strategy, data extraction, risk-of-bias assessment, statistical analysis/GLMM specification) → Results (PRISMA flow diagram, study characteristics, synthesis results per outcome/stratum) → Discussion (summary of findings, limitations, implications)**. Do NOT use `working-paper-format.md`'s Introduction/Data/Empirical-Strategy/Results/Conclusion econ structure, JEL codes, or `\citet`/`\citep` narrative conventions built around causal-identification framing. Citations still use `biblatex`; author-year style is fine for biomedical journals too. A PRISMA 2020 flow diagram figure is mandatory in Results (or as Figure 1). Abstract should follow structured-abstract conventions common in clinical journals (Background/Methods/Results/Conclusions) if the target journal expects it — check the specific journal profile once submission target is chosen.

---

## Target Journals (ranked by tier)

<!-- The Orchestrator uses this for journal selection. The Librarian prioritizes these in searches. -->

| Tier | Journals |
|------|----------|
| Broad clinical/ID | Clinical Infectious Diseases (CID), Antimicrobial Agents and Chemotherapy (AAC) |
| Broad microbiology | PLOS Pathogens, Clinical Microbiology Reviews |
| Specialty (phage/AMR) | Viruses (MDPI phage therapy special issues), Antibiotics (MDPI), Frontiers in Microbiology, Frontiers in Cellular and Infection Microbiology |
| Evidence synthesis | Cochrane Database of Systematic Reviews, Systematic Reviews (BioMed Central) |

---

## Common Data Sources

<!-- The Explorer prioritizes these. The explorer-critic knows their quirks. -->

| Dataset | Type | Access | Notes |
|---------|------|--------|-------|
| PubMed / MEDLINE | Bibliographic database | Public | Primary search engine; use MeSH terms + free text |
| EMBASE | Bibliographic database | Institutional subscription | Broader European/pharma coverage than PubMed; required for a defensible PRISMA search |
| Cochrane CENTRAL | Trials register | Public | Best source for RCTs; low noise |
| Web of Science / Scopus | Citation databases | Institutional subscription | Used for forward/backward citation chasing |
| ClinicalTrials.gov / WHO ICTRP | Trial registries | Public | Identifies unpublished/ongoing trials — needed to assess publication bias |
| Grey literature (medRxiv, bioRxiv, conference abstracts) | Preprints/abstracts | Public | Required by PRISMA 2020 to reduce publication bias; screen but flag risk of bias higher |

---

## Research Question (revised 2026-07-18 — see Decision Records)

**Current design: meta-analysis of proportions** (pivoted from an original comparative-effect design that `/discover lit` found infeasible — 0-1 qualifying comparative studies for MDR *P. aeruginosa*; full history in `quality_reports/decisions/discovery_phage_therapy_mdr_pseudomonas.md`).

- **Population:** Patients with MDR or XDR *Pseudomonas aeruginosa* infections (classified per Magiorakos et al. 2012 where derivable, else per study's own classification)
- **Intervention/regimens studied:** Bacteriophage therapy (monotherapy or adjunctive to antibiotics)
- **Outcomes (primary):** Pooled proportion of clinical success; pooled proportion of safety events (≥1 adverse event)
- **Outcomes (secondary):** Microbiological eradication, mortality, length of hospitalization, resistance emergence during treatment
- **Pre-specified stratification:** (1) MDR vs. XDR; (2) route of phage administration; (3) antibiotic monotherapy vs. phage-antibiotic combination (and phage monotherapy, if distinguishable)
- **Eligibility:** Both single-arm studies (case series, cohorts, compassionate-use reports) and comparative studies — proportions are computed per study-arm/regimen, not as a paired effect size, so single-arm evidence is fully usable (this is what resolves the earlier feasibility failure)

---

## Common Identification Strategies

<!-- The Strategist considers these first. The strategist-critic knows field-specific threats.
     Reinterpreted for evidence synthesis: "identification" = the design that lets pooled
     estimates be interpreted as valid summaries of true effect. -->

| Strategy | Typical Application | Key Assumption to Defend |
|----------|-------------------|------------------------|
| PRISMA 2020 protocol + PICO framework | Defines eligibility (Population: MDR/XDR *P. aeruginosa* infections; regimens: phage monotherapy, phage-antibiotic combination, antibiotic monotherapy; Outcomes: clinical success, safety, microbiological eradication, mortality) | Search strategy is sensitive and reproducible; screening is done in duplicate |
| Random-effects binomial-normal GLMM (logit link) — **primary pooling model, approved 2026-07-19** | Pooling clinical success and safety proportions across heterogeneous single-arm and comparative studies, spanning n=1 case reports to n=100 cohorts | Models the exact binomial likelihood at each study's own n, avoiding the Freeman-Tukey back-transformation failure mode documented in Schwarzer et al. (2019) under extreme sample-size heterogeneity. Requires a per-stratum-cell convergence contingency (fallback: logit-DerSimonian-Laily) — see `quality_reports/strategy_memo_phage_therapy_mdr_pseudomonas.md` §2.1 |
| Logit-DerSimonian-Laird and Freeman-Tukey double arcsine transformation — sensitivity models (not primary) | Robustness check on the GLMM pooled estimates; logit-DL also serves as the automatic fallback when GLMM fails to converge for a stratum cell | Sensitivity models should not materially change conclusions; if they diverge from GLMM, report both and flag prominently |
| Fixed-effects meta-analysis | Only when studies are judged clinically and methodologically homogeneous within a stratum | All studies in that stratum estimate the same true proportion — rarely defensible given design heterogeneity, but may be checked as a sensitivity comparison |
| Pre-specified subgroup analysis (not meta-regression on a paired effect size — there is none) | Stratifying pooled proportions by MDR vs. XDR, route of phage administration, monotherapy vs. combination modality | Enough studies/patients per stratum to avoid unstable estimates (small-stratum problem, especially likely for the monotherapy-only stratum — flagged in research spec Open Questions) |
| Sensitivity analysis (leave-one-out, transformation choice, author-reported vs. re-derived MDR/XDR classification) | Testing robustness of pooled proportions to influential studies, methodological choices, and classification uncertainty | Pooled estimate is not driven by one or two outlier studies or by a single analytic choice |

---

## Field Conventions

<!-- The Coder and Writer follow these. The writer-critic checks for them. -->

- PRISMA 2020 flow diagram is mandatory (records identified → screened → excluded with reasons → included)
- Protocol pre-registration in PROSPERO expected before/at the time of full-text screening
- Forest plots are the standard visualization for pooled effect sizes with 95% CIs
- Report heterogeneity as I² and τ² alongside the pooled estimate — never report a pooled effect without them
- Risk of bias assessed per-study with Cochrane RoB2 (for RCTs) or ROBINS-I (for non-randomized/observational studies)
- GRADE framework used to rate overall certainty of evidence per outcome
- Funnel plot + Egger's test (or equivalent) reported when ≥10 studies per outcome, to assess small-study/publication bias
- Dual independent screening and data extraction, with a documented conflict-resolution process

---

## Notation Conventions

<!-- The Writer and writer-critic enforce these. -->

| Symbol | Meaning | Anti-pattern |
|--------|---------|-------------|
| p̂ (or ES) | Pooled proportion (primary estimand of this review — e.g., pooled clinical success rate) | Never report a bare pooled proportion without back-transformation details and 95% CI |
| Freeman-Tukey / double arcsine | Variance-stabilizing transformation for proportions near 0/1 boundary | Don't pool raw (untransformed) proportions when many studies report proportions near 0% or 100% — variance is badly behaved |
| Logit transformation | Alternative transformation for proportion meta-analysis, used here as a sensitivity check against double arcsine | Don't treat transformation choice as inconsequential — report both if they diverge materially |
| RR | Risk ratio (dichotomous outcomes) — used only for the sparse comparative-study subset, if reported alongside proportions | Don't mix RR and OR across studies without conversion/justification |
| OR | Odds ratio | Reserve for case-control designs or logistic-regression-derived estimates |
| HR | Hazard ratio (time-to-event outcomes, e.g. survival) | Don't pool HR with RR/OR in the same forest plot |
| I² | Percentage of variability due to heterogeneity rather than chance | Don't report I² without also reporting τ² and the prediction interval |
| τ² | Between-study variance (random-effects model) | -- |
| 95% CI | Confidence interval | Always report alongside point estimate — never a bare proportion/RR/OR/HR |
| MDR / XDR | Multidrug-resistant / extensively drug-resistant, per Magiorakos et al. (2012) | Don't use "MDR" as an undifferentiated catch-all when the source study actually reports enough data to classify XDR separately |

---

## Seminal References

<!-- The Librarian ensures these are cited when relevant. The strategist-critic knows their methods. -->

| Paper | Why It Matters |
|-------|---------------|
| Page et al. (2021), PRISMA 2020 Statement | Reporting standard this review must follow |
| Higgins et al., Cochrane Handbook for Systematic Reviews of Interventions | Methodological reference for search, risk of bias, and meta-analysis choices |
| Magiorakos et al. (2012), "Multidrug-resistant, extensively drug-resistant and pandrug-resistant bacteria: an international expert proposal for interim standard definitions" (Clin Microbiol Infect) | Field-standard MDR/XDR/PDR classification criteria — the basis for this review's core stratification variable |
| El Haddad et al. (2019, CID), Uyttebroek et al. (2022, Lancet ID), Liu et al. (2025, IJAA — PMID 40633848) | Prior systematic reviews/meta-analyses of human phage therapy (identified via `/discover lit`); this review must explicitly differentiate its MDR/XDR-stratified, *Pseudomonas*-specific proportion analysis from these broader, non-stratified syntheses — see `quality_reports/literature/phage_therapy_mdr_pseudomonas/positioning.md` |

---

## Theoretical Foundational References

<!-- Not applicable — this project has no formal theory section (it is an evidence synthesis,
     not a structural/reduced-form econometric paper). Leave empty; the theorist agent should
     not be dispatched for this project (see permissions.md CONDITIONAL flag on theorist). -->

| Topic | Anchor references |
|-------|------------------|
| N/A | N/A |

---

## Paper Author Team

<!-- Used by the theorist-critic to calibrate respect. Not applicable while theorist is not dispatched.
     Fill in once authorship is finalized, in case it becomes relevant to writer-critic voice checks. -->

| Author | Foundational on |
|--------|----------------|
| [TBD] | [TBD] |

---

## Field-Specific Referee Concerns

<!-- The domain-referee and methods-referee watch for these. -->

- "Is the heterogeneity (clinical and statistical) too high to justify pooling at all?"
- "Was risk of bias assessed per study, and does it explain result heterogeneity?"
- "Have you addressed publication bias / small-study effects — most phage therapy evidence is case series and case reports?"
- "Does the pooled proportion generalize across *Pseudomonas* strains, phage cocktails, and administration routes, or is this an average of incomparable interventions?"
- "A pooled proportion of clinical success in a salvage-therapy population is not a causal effect — does the paper avoid overclaiming efficacy from what is fundamentally a descriptive/prevalence-style estimate?"
- "Is the MDR/XDR classification defensible given how much of the primary literature reports 'MDR' without full susceptibility panel data?"
- "Are the pre-specified strata (route, monotherapy vs. combination) adequately powered, or is this multiple subgroup testing on too few studies per stratum?"
- "Was the search strategy sensitive enough (PubMed alone is not sufficient for a defensible PRISMA review — EMBASE/Web of Science/Scopus access status must be disclosed)?"

---

## Quality Tolerance Thresholds

<!-- Customize for your domain's standards. Used by quality.md. -->

| Quantity | Tolerance | Rationale |
|----------|-----------|-----------|
| Pooled proportions (back-transformed) | 1e-4 | Numerical precision in meta-analysis software (R `meta`/`metafor`, `metaprop`) |
| Pooled effect estimates (RR/OR/HR), where reported from the sparse comparative subset | 1e-4 | Numerical precision in meta-analysis software |
| I² / τ² | ± 0.01 | Rounding across re-runs of the same model |
| 95% CI bounds | ± 0.001 on the transformed (arcsine/logit) scale | Numerical precision before back-transformation |
