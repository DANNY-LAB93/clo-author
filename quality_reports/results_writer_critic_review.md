# Writer-Critic Review: `paper/sections/results.tex`

**Paper type:** Descriptive/measurement systematic review + meta-analysis of proportions (IMRaD, per domain-profile.md)
**Phase:** Execution — STRICT severity
**Score: 57/100 — FAILS the 80 commit gate. Two CRITICAL issues found.**

## CRITICAL Issues

### 1. Bibliography gap is NOT closed

Of the 8 previously-uncited case reports added to `Bibliography_base.bib` (`Onallah2023_med`, `Tkhilaishvili2020_aac`, `Blasco2023_frontmed`, `Ferry2022_natcomms`, `Ngauy2026_asmcr`, `Racenis2022_frontmed`, `Racenis2023_viruses`, `Liu2025_mlife_perinephric`), only 2 (`Onallah2023_med`, `Liu2025_mlife_perinephric`) are cited anywhere in `results.tex`. The other 6 are confirmed real extraction-dataset rows contributing to the headline pooled numbers, yet appear nowhere in the paper. Results.tex defers the one fix (a Table 1) as future work, meaning six included studies are completely untraceable via any `\cite` command — a genuine PRISMA-adjacent completeness failure for a systematic review.

### 2. Internal-process jargon leaked into manuscript prose

Line 136: "This is exactly the small-study/publication-bias pattern the domain-referee concern anticipates..." — "domain-referee" is this project's internal multi-agent role name, not a real actor in the scientific literature. Isolated to this one line (intro.tex and methods.tex are clean). Must be rewritten with no reference to the review pipeline itself.

## Moderate/Minor Issues

3. **INV-2 (figure notes):** All four figures place the explanatory note in a `\begin{quote}` block below `\caption{}` rather than inside the caption itself. Consistent across all four figures. **-5**
4. **Clarity:** "changes the pooled estimate by more than 5 percentage points in 4 of the 5 pooled cells... safety diverges by roughly 30 points, as above" reads as if only 4 of 5 cells diverge, when in fact all 5 of 5 diverge by >5pp. **-3**

## What Checks Out (verified, no issues)

- PRISMA flow diagram honestly disclosed as not yet produced (confirmed against `paper/figures/`).
- 86.1% consistently framed as "secondary and contextual," not a treatment-effect claim.
- GLMM safety instability reported prominently and accurately (1.0% GLMM vs. ~31% sensitivity-model estimate), matching `results_summary.md` Flag #1 exactly.
- Egger's test (p=0.022, p=0.002) reported as a genuine finding, not minimized.
- All 32 NOT_POOLED cells reported as insufficient evidence, framed as the review's central finding.
- Every cross-checked number matches tables/figures/results_summary.md exactly (INV-11 clean).
- Methods/Results consistency: "16 arms/14 studies... 15 pooling-eligible/13 studies" stated identically in both sections — the Leitner-inclusion distinction is not miscounted.
- All other citation keys used in results.tex resolve in `Bibliography_base.bib`.

## Score Breakdown
100 − 15 (leaked internal-process jargon) − 20 (bibliography gap only 25% closed) − 5 (figure notes outside `\caption{}`) − 3 (confusing divergence-count phrasing) = **57/100**

**Verdict:** FAIL. Recommend a fix round before re-review; not yet an escalation (issues are section-specific and correctable without a structural rewrite).

---

## Re-Review

**Phase:** Execution — STRICT severity
**Score: 97/100 — PASSES the 80 commit gate.**

### Verification of Prior CRITICAL Issues

1. **Bibliography gap — RESOLVED.** Study Characteristics subsection now names all 7 case-report studies via resolving `\textcite`/`\citeauthor` commands: `Tkhilaishvili2020_aac`, `Blasco2023_frontmed`, `Ferry2022_natcomms`, `Ngauy2026_asmcr`, `Racenis2022_frontmed`, `Racenis2023_viruses`, and `Aslam2019_ajt`. All 6 previously-uncited keys confirmed present in `Bibliography_base.bib`. No included study is untraceable via `\cite`.
2. **Leaked internal-process jargon — RESOLVED.** Full-file grep for pipeline terminology returns zero matches. Rewritten to "referees reviewing case-report-heavy evidence syntheses" — legitimate domain language.

### Verification of Prior MINOR Issues

3. **INV-2 figure notes — RESOLVED.** All 4 figures now carry their explanatory notes fully inside `\caption{}`. No residual `\begin{quote}` blocks.
4. **Divergence phrasing — RESOLVED.** Now correctly attributes >5pp divergence to "all 5 pooled cells."

### Spot-Check: No Regression in Previously-Clean Numbers
86.1% CI, GLMM safety instability (1.0% vs. ~31%), and Egger's test p-values (0.022, 0.002) all remain consistent across text, figures, and tables. No new table/figure-formatting violations introduced.

### Score Breakdown
100 − 3 (several robustness sub-checks and the study-characteristics table remain explicitly flagged as "outstanding work before submission" — honest disclosure, not a fabrication risk, but still incomplete deliverables per the paper's own admission) = **97/100**

**Verdict: PASS.** Both CRITICAL and both MINOR issues fully resolved with no collateral damage. Cleared for commit gate.
