# Strategy Review: strategy_memo_phage_therapy_mdr_pseudomonas.md

**Date:** 2026-07-19
**Reviewer:** strategist-critic
**Severity:** Strategy phase — CONSTRUCTIVE / MEDIUM

---

## Phase 1: Claim Identification

- **Paper type:** Descriptive / Measurement (evidence synthesis — meta-analysis of proportions). Correctly identified; theorist correctly not dispatched.
- **Estimand:** Four families of pooled proportions (success, safety, eradication, mortality), each estimated per stratum cell {MDR/XDR/not-classifiable} × {route} × {modality}, under a random-effects binomial-normal GLMM logit-link model. A secondary unstratified pooled-all proportion is explicitly labeled contextual, not primary.
- **Stratification vs. paired comparison:** Correctly kept separate. The memo explicitly states the between-stratum comparison is a subgroup meta-analysis with Cochran's Q-between, not meta-regression on a paired effect size, and any genuine within-study comparator (Krakhotkin, Leitner, PhagoBurn) is quarantined as a clearly-labeled exploratory RR/risk-difference, never blended into the primary strata. This is the single most important correctness check for this design type and it passes cleanly.
- **Population/estimand scope:** Explicitly a descriptive summary of "the evidence base under its actual selection mechanism," not a population-prevalence claim — correctly hedged against overclaiming.

## Phase 2: Core Design Validity

### GLMM-vs-double-arcsine deviation
**Justified, correctly reasoned, with one unaddressed technical risk.** The memo's characterization of Schwarzer, Chemaitelly, Abu-Raddad & Rücker (2019, *Res Synth Methods*) is accurate: Freeman-Tukey back-transformation requires an arbitrary "typical" n, and with highly heterogeneous study sizes this can produce a pooled point estimate outside the range of any observed study proportion. This literature genuinely spans n=1 case reports to n=100 cohorts, so the deviation is substantively well-motivated. GLMM models the exact binomial likelihood at each study's own n_i, avoiding the transform/back-transform step. Recommending the user approve updating `domain-profile.md`'s wording rather than silently overriding it is the right procedural move.

**Gap (MAJOR):** GLMM via numerical integration has real convergence problems in the sparse/boundary-proportion regime this corpus will produce (many n=1 studies with 0 or 1 events; strata with all-0% or all-100% arms). No convergence-failure contingency is specified. Recommend: (a) convergence diagnostics reported per stratum cell, (b) a pre-specified fallback (logit-DL sensitivity model with a footnote) if GLMM fails to converge.

### MDR/XDR classification ladder
**Sound**, with one trade-off worth naming. The 4-step ladder is defensible and transparent. The asymmetric rule (require positive confirmation to upgrade to XDR, but allow MDR from partial data) is methodologically reasonable but will mechanically shrink the XDR stratum. **MINOR:** flag this trade-off explicitly in the manuscript's Limitations.

### Liu et al. (2025) Tier 1/2/3 reuse policy
**Well-designed but not fully audit-proof.** The Tier structure and `data_provenance`/`rob_source` fields give genuine traceability.

**Gap (MAJOR):** The Tier-2 cross-validation as specified cannot detect a coder who copies Liu's value directly and labels the row "independently-extracted" — comparing a copy against its own source is tautologically "in agreement." Recommend a documented-citation requirement (page/table reference) for a random subsample of independently-extracted rows, checked by the coder-critic or a second reviewer.

### Data-dictionary compatibility
No incompatibility found; the plan is grounded in what the data-assessment agent confirmed is actually reportable in the Grade-A sources.

### Sanity check
High pooled success proportions are expected and explicitly attributed to salvage-population selection, not efficacy — correctly hedged. The known-group validity check (RCT subgroup should show more modest/null results than compassionate-use subgroup) is a genuine, well-chosen internal-consistency test.

No CRITICAL issues found in Phase 2.

## Phase 3: Inference Soundness

- **Sparsity/weighting of tiny studies:** Adequately addressed — GLMM's exact-likelihood approach naturally down-weights n=1 studies via their large individual variance, and the ≥3-studies/≥20-patients threshold prevents an unstable estimate from being reported as stable.
- **Monotherapy-stratum sparsity:** A concrete, pre-specified decision rule exists (≥3 studies → pool with an explicit heterogeneity caveat; <3 → narrative-only, reported as "insufficient evidence," not silently dropped). One of the strongest parts of the memo.
- **Multiple testing (MINOR-to-MAJOR boundary):** No formal multiplicity correction discussed across the many subgroup/moderator tests. Pre-specified subgroup analyses are conventionally treated as hypothesis-generating (Cochrane Handbook convention), which partially excuses this — scored MINOR, but recommend one sentence in Methods explaining why formal adjustment is/isn't applied.
- **Clustering:** Correctly specified via `clubSandwich`, triggered only when a study contributes >1 arm to the same cell.

## Phase 4: Polish & Completeness

### The 8 referee-objection responses
Objections 1-6 and 8 are genuinely responsive.

**Objection 7 ("adequately powered, or is this multiple subgroup testing on too few studies?") is only partially responsive (MAJOR):** the response addresses power/pre-specification/threshold transparency but not the multiplicity-of-testing half of the objection. Recommend a brief multiplicity discussion or explicit statement of why it's not needed.

### PROSPERO timing argument
**Largely defensible, but incompletely connects its own disclosure to the most consequential design choice.** The memo's characterization of PROSPERO's eligibility rule is accurate, and its mitigation (register now, disclose scoping timeline, treat the 201-PDF screen as scoping-only) is the standard, correct response.

**Gap (MAJOR):** the memo names the general risk but doesn't connect it to the specific fact that the choice of GLMM as primary pooling model was itself justified by reference to already-observed, specific sample-size heterogeneity (Pirnay n=49-100, Green n=15, case reports n=1) surfaced during the same scoping process being disclosed. A sharp reviewer could reasonably ask whether the primary model was chosen *because of* what scoping already revealed. Recommend explicitly naming this in the Methods/Limitations disclosure alongside the other scoping-timeline items.

## Summary

- **Overall assessment:** MINOR ISSUES (some bordering on MAJOR; none CRITICAL)
- **Critical issues (must fix):** 0
- **Major issues (should fix):** 4 — (1) no GLMM convergence-failure contingency; (2) Tier-2 Liu-reuse audit cannot detect a copy-and-relabel shortcut; (3) PROSPERO §8 disclosure doesn't name the GLMM choice's own data-dependency; (4) referee objection #7 doesn't address testing multiplicity
- **Minor issues (consider):** 2 — asymmetric MDR/XDR rule's XDR-shrinkage trade-off not named in Limitations; monotherapy-threshold wording doesn't restate the ≥20-patient co-requirement

## Priority Recommendations
1. **[MAJOR]** Add a GLMM convergence contingency (diagnostic reporting + fallback estimator) to `pseudo_code.md`'s `pool_stratum()`.
2. **[MAJOR]** Add a documented-citation/spot-check requirement to the Liu et al. Tier-2 cross-validation process to close the copy-and-relabel loophole.
3. **[MAJOR]** Explicitly connect the GLMM primary-model choice to the scoping-timeline disclosure in §8.
4. **[MINOR]** Note the XDR-shrinkage trade-off from the asymmetric classification rule in Limitations.

## Positive Findings
- Estimand and stratification are cleanly separated from any paired-comparison framing.
- The GLMM-vs-arcsine deviation from `domain-profile.md` is correctly reasoned against the actual Schwarzer et al. (2019) mechanism, not just asserted.
- The falsification-test suite is a genuinely strong, non-boilerplate adaptation of causal falsification logic to evidence synthesis, including a well-chosen known-group validity check.

## Score: 84/100 (above the 80 commit gate)

No CRITICAL issues. Three MAJOR items should be addressed before this locks into the PROSPERO protocol, since protocol language is meant to be final.

---

## Re-Review — 2026-07-19

**Reviewer:** strategist-critic | **Severity:** Strategy phase — CONSTRUCTIVE/MEDIUM

All 4 MAJOR items and the 1 MINOR item verified fixed:

1. **GLMM convergence contingency — RESOLVED.** `pool_stratum()` wraps the GLMM call in `tryCatch`/`withCallingHandlers`, classifies `convergence_flag` into `CONVERGED`/`FAILED_ERROR`/`FAILED_WARNING`/`FAILED_NONFINITE`, falls back cell-level to the pre-computed logit-DL sensitivity model, and tags every cell with `primary_model_used`. Mandatory footnote disclosure. Thorough and correctly scoped.
2. **Liu et al. Tier-2 audit loophole — RESOLVED.** §3 adds a documented-citation requirement (20% random subsample, or all if <15 overlap) requiring a page/table/quote locator from the primary source, verified by coder-critic or a second reviewer — closes the copy-and-relabel tautology correctly.
3. **PROSPERO §8 GLMM-choice disclosure — RESOLVED.** New point explicitly names that the GLMM-primary choice was reasoned from scoping-observed sample sizes (Pirnay n=49-100, Green n=15-16, n=1 case reports), with a defensible rationale for why this doesn't invalidate the choice while still disclosing it.
4. **Referee objection #7 multiplicity — RESOLVED.** Explicit multiplicity discussion added (up to 12 formal moderator tests, no Bonferroni/BH correction) with a stated Cochrane Handbook hypothesis-generating rationale.
5. **XDR-shrinkage trade-off — RESOLVED.** §2.2 now names this explicitly and requires it in the manuscript's Limitations.

Each fix is substantively correct, not cosmetic. No new CRITICAL or MAJOR issues introduced by the fix pass. One residual, out-of-scope MINOR remains (monotherapy-threshold wording doesn't restate the ≥20-patient co-requirement) plus a trivial tidyeval-syntax nitpick in `pool_stratum()`'s `narrative_table` line (advisory only for the coder at implementation time).

**Score: 95/100** (up from 84/100)

**Verdict: PASS — commit gate cleared with margin.** No CRITICAL or MAJOR issues remain. This memo is ready to inform the coder/data-engineer's extraction spreadsheet build, and (pending user approval) ready to support PROSPERO registration — the protocol-locking language in §8 is internally consistent with §§1-7.
