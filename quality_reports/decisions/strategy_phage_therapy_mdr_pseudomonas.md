# Decision Record — Strategy: Meta-Analysis of Proportions Design

**Date:** 2026-07-19
**Stage:** Strategy
**Decided by:** Strategist + strategist-critic (2 rounds, final score 95/100) + user (pending sign-off on Liu et al. reuse tiers)

---

## Decision

Pool outcomes as **four families of proportions** (clinical success, safety, microbiological eradication, mortality), one per stratum cell of {MDR / XDR / not-classifiable} × {route of phage administration} × {antibiotic monotherapy / phage-antibiotic combination}, using a **random-effects binomial-normal GLMM (logit link)** as the primary pooling model, with logit-DerSimonian-Laird and double-arcsine as sensitivity models. Any genuine within-study comparator (Krakhotkin 2025, Leitner 2021, PhagoBurn) is reported as a clearly-labeled exploratory RR/risk-difference, quarantined from the primary stratified-proportions estimand.

## Context

The research spec called for a meta-analysis of proportions (per the two discovery-phase pivots documented in `quality_reports/decisions/discovery_phage_therapy_mdr_pseudomonas.md`) but left the exact pooling model, MDR/XDR classification rule, and the Liu et al. (2025) reusable-dataset reuse policy as open questions. The strategist resolved these; strategist-critic reviewed twice (84/100 → 95/100 after a fix round addressing 4 MAJOR items).

## Alternatives Considered

| Alternative | Why rejected |
|-------------|-------------|
| Double-arcsine (Freeman-Tukey) as primary pooling model, per the domain profile's original wording | Documented back-transformation failure mode (Schwarzer et al. 2019) under this corpus's extreme sample-size heterogeneity (n=1 case reports to n=100 cohorts) — can produce a pooled estimate outside the range of any observed study. GLMM avoids the transform/back-transform step by modeling the exact binomial likelihood at each study's own n. Domain-profile.md needs a wording update to reflect this (flagged for user approval). |
| Symmetric MDR/XDR classification rule (same evidentiary bar to classify either way) | Asymmetric rule (require positive confirmation to upgrade to XDR; allow MDR from partial data) is more defensible because XDR is the stronger claim — but this shrinks the XDR stratum, a documented trade-off noted in Limitations. |
| Direct adoption of Liu et al. (2025)'s case-level codings for overlapping studies (Tier 3) as default policy | Blurs the line between an independent systematic review and a re-analysis of a prior team's dataset. Adopted instead: Tier 1 (scoping) + Tier 2 (independent cross-validation with a primary-source-citation audit requirement) as default; Tier 3 requires explicit per-instance user sign-off, logged in a decision record. |
| Formal Bonferroni/Benjamini-Hochberg correction across all subgroup/moderator tests | Pre-specified subgroup analyses are conventionally treated as hypothesis-generating, not confirmatory, per Cochrane Handbook convention — explicit rationale now documented in the memo's referee-objection response, not silently omitted. |

## Key Assumptions

1. GLMM will converge for most stratum cells; a documented fallback (logit-DL) and per-cell convergence flag handle the cells where it doesn't.
2. Enough studies/patients exist per stratum cell (≥3 studies, ≥20 patients) to report a pooled estimate; below that, the stratum is reported as narrative-only "insufficient evidence," not silently dropped.
3. The Liu et al. (2025) dataset's case-level codings are useful for cross-validation and scoping but are not a substitute for this project's own independent extraction under its own outcome definitions.

## What Would Invalidate This

- If GLMM fails to converge for the majority of stratum cells (not just isolated ones), the primary model should revert to logit-DerSimonian-Laird project-wide, with GLMM demoted to a sensitivity check.
- If the coder-critic's spot-check of "independently-extracted" rows overlapping Liu et al.'s dataset finds systematic copy-and-relabel behavior, the Tier-2 policy needs tightening (100% citation-locator requirement, not just a 20% sample).
- If full-text review of Liu et al. (2025) or Uyttebroek et al. (2022) reveals either already performs this exact MDR/XDR-stratified analysis, the contribution statement (not just the strategy) needs revision.

## Approved By

Strategist-critic re-review score 95/100 (2026-07-19). User approved both pending items (2026-07-19): (a) `.claude/references/domain-profile.md` updated — GLMM (binomial-normal, logit link) is now the documented primary pooling model, with logit-DerSimonian-Laird and double-arcsine as sensitivity/fallback models; (b) Liu et al. (2025) reuse policy confirmed as **Tier 1 (scoping) + Tier 2 (independent cross-validation with primary-source-citation audit) as default policy, no Tier 3 (direct adoption) without explicit per-instance sign-off**. Both decisions are now final — the coder/data-engineer may proceed to build the extraction spreadsheet under this strategy.

## Update (2026-07-20) — Monotherapy Stratum Confirmed Empty; Pre-Specified Decision Rule Now Activated

Data extraction (via `/analyze`) plus a targeted Round 4 literature search resolved the monotherapy-stratum sparsity risk flagged throughout Discovery and Strategy:

- **Krakhotkin et al. (2025)** — confirmed via full text (PMC12042198) to include **zero** *P. aeruginosa* cases (pathogens: E. coli, K. pneumoniae, Proteus mirabilis, S. epidermidis, S. aureus only). Excluded from the extraction dataset entirely (`pathogen_scope=mixed-not-separable`, auto-filtered by the cleaning script).
- **Leitner et al. (2021)** — *P. aeruginosa* confirmed as one of six pathogens covered by the trial's phage cocktail, but an exhaustive Round 4 access attempt (PMC linkout, ResearchGate, ClinicalTrials.gov API, related systematic reviews) could not surface a Pseudomonas-specific subgroup breakdown. The trial-wide aggregate (Pyophage 5/28, placebo 9/32, antibiotics 13/37 normalization of urine culture) is not usable as a Pseudomonas-specific data point without full-text institutional access, which was not available.
- No other candidate (comparative cohort, RCT, or well-documented case series) with a genuine antibiotic-monotherapy arm for *P. aeruginosa* was found. Several external-benchmark antibiotic-only cohort studies exist (Almangour 2025, Alsaeed 2024, Maraolo 2026, Corcione 2025) but have no phage arm and are flagged as background/contextual citations only, not comparative-stratum data.

**Decision:** Per the strategy memo's pre-specified sparsity rule (Sec. 5: <3 studies → narrative-only, reported as "insufficient evidence," not silently dropped), the monotherapy-vs-combination stratification variable is **not pooled**. The paper will report this explicitly: despite a systematic search (3 discovery-phase rounds + 1 targeted Round 4), zero studies provide a genuine within-study or reliably-disaggregated antibiotic-monotherapy comparator for *P. aeruginosa* phage therapy specifically — this finding is itself reportable (an evidence-gap statement), consistent with the project's contribution framing established in Strategy.

**What would still change this:** If the user or a future search obtains Leitner et al. (2021)'s full text via institutional access and it contains a Pseudomonas-specific subgroup table, this decision should be revisited.
