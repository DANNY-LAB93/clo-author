# Code Review: Phage Therapy MDR/XDR *Pseudomonas aeruginosa* Meta-Analysis Pipeline

**Date:** 2026-07-20
**Reviewer:** coder-critic
**Paper type:** Descriptive/Measurement (evidence synthesis — meta-analysis of proportions)
**Severity:** STRICT / Execution phase
**Score: 64/100** — below the 80 commit gate. Requires a fix round before advancing.

Verification method: full static review of all 9 scripts + 4 function files, manual re-derivation of every reported k/N/proportion directly from `data/cleaned/phage_therapy_extraction_dataset.csv`, and cross-checking generated `.tex`/figure outputs against what the code claims to produce (no direct R execution available in this reviewer's environment).

---

## 1. Code-Strategy Alignment: PARTIAL MATCH (undisclosed scope-narrowing)

`scripts/R/functions/pool_stratum.R` implements the GLMM-primary/logit-DL-fallback convergence contingency faithfully and almost verbatim against `pseudo_code.md` §2, including the exact convergence-flag logic (`FAILED_ERROR`/`FAILED_WARNING`/`FAILED_NONFINITE`/`CONVERGED`), cell-level (never model-wide) fallback promotion, and the `rve_note`. One disclosed, well-justified refinement: the minimum-study gate is applied to `k_studies` (distinct `study_id`) rather than raw arm count — correctly reasoned in the Roxygen header as truer to the memo's "≥3 independent studies" language than the pseudo-code's literal `nrow(df)`.

Two real deviations:
- **`04_estimation.R` only runs the resistance-class and route-group subgroup breakdowns for 2 of the 4 outcome families** (`clinical_success`, `safety` — not `eradication`/`mortality`), against `pseudo_code.md` §3's literal outcome × stratum triple loop over all 4 outcomes. Reasoned in a code comment but never surfaced to the reader in `results_summary.md`.
- **Prediction intervals**, mandated by `pseudo_code.md` §9, appear only in the forest-plot figures — never as a numeric column in `meta_pooled_estimates.tex`.

## 2. Paper-to-Code Naming Map: PRESENT

Documented in both `01_setup.R` and `results_summary_phage_therapy_mdr_pseudomonas.md`. Consistent, complete, traceable.

## 3. Sanity Checks: PASS (independently verified)

Every headline number re-derived by hand from the raw CSV, all matching exactly:
- Clinical success overall: 32/36, k=10 studies
- Safety overall: 5/27, k=10
- Eradication overall: k=9, N=21
- Resistance "not-classifiable": k=3, N=27
- Route "other": k=5, N=29
- MDR NOT_POOLED cell: k_studies=4, N=5

**GLMM safety-instability caveat — CHECKS OUT.** The safety cell is a near-complete-separation pattern (11/12 arms report zero events; only `ArmataAP_PA02` reports 5/10). Removing the sole event-positive arm mechanically drives a binomial-normal GLMM's pooled logit toward −∞ — exactly the collapse the results summary describes. The three sensitivity models (FT 5.0%, logit-DL 31.0%, FE 31.0%) clustering together while GLMM (1.0%, CI [0%, 98.5%]) diverges is the textbook signature. Egger's-test gating correctly identifies exactly the two eligible cells (both k=10), computed via `meta::metabias(..., method.bias="Egger")`, not hardcoded.

**Monotherapy stratum — explicitly, correctly disclosed.** Named row in `meta_not_pooled.tex` with stated reason, never silently omitted.

## 4. Robustness: INCOMPLETE (MAJOR)

Of 13 pre-specified checks, only 7 implemented. Six missing without disclosure: #2 MDR/XDR classification sensitivity (Priority-1, feasible given data), #4 study-design-stratified sensitivity, #5 geographic-concentration sensitivity (variable derived but unused for re-running the model), #7 route-collapsing alternative taxonomy, #8 Liu-reuse-tier transparency check, #12 threshold-relaxation appendix. **Falsification Test 5** (length-of-stay vs. clinical-success) entirely absent, no code, no "not applicable" note.

---

## Code Quality (Categories 5-16)

| Category | Status | Issues |
|---|---|---|
| Project layout | OK | Clean numbered sequence, one function per file |
| Script headers | OK | Purpose/Inputs/Outputs/Requires present everywhere |
| Console output | OK | `message()` only |
| Reproducibility | WARN | `01_setup.R` has `.libPaths()` fix + single seed. **`clean_phage_extraction.R` missing the same `.libPaths()` fix** |
| Numerical discipline | OK | Proper clamping, `seq_len()`, integer literals |
| Function design | OK | Roxygen docs, `stopifnot()`, one justified `<<-` exception matching pseudo_code.md |
| Figure quality | WARN | ggplot figure correctly serif. **`meta::forest()` calls pass no `family` argument** — likely sans-serif, inconsistent with content-standards |
| Table quality | **FAIL** | **`08_tables.R` writes the I² column via `sprintf("%.0f%%", ...)` without routing through `escape_tex()`.** Confirmed in actual output — every row has a bare, unescaped `%`, opening a LaTeX comment and truncating the Model column and row terminator. **Breaks compilation.** One-line fix. `not_pooled_rows$reason` also bypasses escaping (currently harmless). |
| RDS/checkpoint pattern | OK | 18 intermediate objects saved, verified present |
| Comment quality | OK | Explains why, no dead code |
| Error handling | OK | tryCatch/withCallingHandlers correctly wraps every GLMM call |
| Prohibited patterns | WARN | Minor growing-vector pattern in `08_tables.R`'s `for` loops (harmless at this scale, but a flagged discipline violation) |

**Additional finding — INV-18 (Output Organization):** `CLAUDE.md` specifies `Output organization: by-script` but the pipeline writes flat to `paper/figures/*.pdf`/`paper/tables/*.tex` with no script-identifying subfolder.

---

## Score Breakdown

- Starting: 100
- LaTeX-breaking `%`-escaping bug (verified in generated output; breaks paper table compilation): **-10**
- Incomplete pre-registered plan (6/13 robustness checks missing undisclosed, Falsification Test 5 absent, prediction interval missing from table, outcome×stratum scope silently narrowed): **-15**
- `clean_phage_extraction.R` missing `.libPaths()` fix: **-5**
- Forest plots not serif; growing-vector-in-loop; magic number; escaping inconsistency: **-5**
- INV-18 output-organization non-compliance: **-3**
- **Final: 64/100**

## Escalation Status

None yet (first review round). Strike 1 of 3 — return to coder with the findings above, re-review after fixes.

---

## Re-Review (Round 2)

**Date:** 2026-07-21
**Reviewer:** coder-critic
**Severity:** STRICT / Execution phase
**Score: 97/100** — clears the 80 commit gate and the 90 PR gate.

Verification method: direct read of every regenerated `.tex`/figure output, full re-read of the affected scripts, and a manual re-derivation of the Falsification-Test-5 LOS count directly from `data/cleaned/phage_therapy_extraction_dataset.csv`.

### Item-by-item verification

1. **[CRITICAL] LaTeX-escaping bug — RESOLVED.** `escape_tex()` now escapes both `%` and `_` and is applied to every free-text/percent-bearing cell across all four generated tables. Confirmed by reading the actual generated files — zero bare `%` characters anywhere.
2. **[MAJOR] Outcome×stratum scope — RESOLVED.** `04_estimation.R` now runs both `resistance_class` and `route_group` breakdowns for all 4 outcome families, matching pseudo_code.md §3. Confirmed downstream via the expanded `meta_not_pooled.tex` (now 30+ rows spanning eradication/mortality cells).
3. **[MAJOR] Prediction interval — RESOLVED.** `meta_pooled_estimates.tex` now has a real, cell-specific prediction-interval column.
4. **[MAJOR] Robustness checks — RESOLVED.** All 6 previously-missing checks implemented with non-trivial output (MDR/XDR classification sensitivity, study-design sensitivity, geographic-concentration exclusion, route-collapsing alternative, Liu-reuse-tier transparency, threshold-relaxation appendix). Falsification Test 5 (LOS) independently re-derived from raw data: 1 of 15 pooling-eligible arms report `los_days` — matches the runtime message exactly.
5. **`.libPaths()` fix — RESOLVED** in `clean_phage_extraction.R`.
6. **Forest-plot serif font — RESOLVED.**
7. **Growing-vector-in-loop — RESOLVED** (genuine fix via `vapply()`, not just accepted as a trade-off).
8. **INV-18 output organization — RESOLVED** — confirmed via directory listing, all outputs in project-identifying subfolders.

### Spot-check: results_summary.md

Still correctly reports the GLMM safety-estimate instability caveat (1.0% GLMM vs. ~31% sensitivity models clustering), unchanged and accurate.

### New findings this round (minor, non-blocking)

- Dead code block in `05_robustness.R` (immediately overwritten by a correct rebuild) — harmless but should be deleted: **-2**
- Stale header comment in `06_falsification.R` ("1 of 16" vs. actual runtime "1 of 15"): **-1**

### Score Breakdown
- Starting: 100
- Dead code block: **-2**
- Stale comment: **-1**
- **Final: 97/100**

### Verdict
**PASS — commit gate and PR gate cleared.** All 4 previously-blocking issues (1 CRITICAL, 3 MAJOR) genuinely resolved, independently verified against actual generated artifacts or raw data, not just the code that claims to produce them. No re-round needed; safe to advance to writer/paper-drafting phase.

### Escalation Status
Resolved at Round 2 of 3. No escalation required.
