# Writer-Critic Review: `paper/sections/discussion.tex`

**Phase:** Execution (STRICT severity) | **Paper type:** Descriptive systematic review / meta-analysis of proportions | **Score: 74/100**

## Score Breakdown (starting at 100)

| Deduction | Points | Invariant / Category |
|---|---|---|
| Unsupported, direction-committed claim about grey literature effect on outcomes, no citation | -10 | Category 1 (unsupported claim) / needs citation |
| RCT-count inconsistency: Discussion says "4 randomized trials," but the section it cites (`results.tex` §Risk of Bias) says "3 pooling-eligible randomized trials" | -6 | INV-11 (numbers must match across sections) |
| "All report pooled success proportions broadly consistent with 86.1%" overclaims quantitative agreement for Uyttebroek (2022) and Liu (2025), neither of which has a documented comparable percentage anywhere in this project's literature files | -6 | INV-22 (traceability) |
| Citation-style inconsistency: `\textcite{}` used correctly at first mention, then reverts to bare prose without citation macros later | -3 | LaTeX/style consistency |
| Length: ~1,270 words, above the paper's own established 800-1,200 advisory range (already self-flagged) | -1 | Advisory |

## CRITICAL issue

**Limitations, item 4:** "grey literature of this kind more often reports favorable outcomes, so closing this gap would more likely add successes than failures" is a new directional claim not established anywhere in methods.tex or results.tex, and is in tension with standard meta-analytic publication-bias logic (missing non-indexed/grey literature more commonly skews negative results out of the visible record — the file-drawer effect — the opposite direction). Needs a supporting citation, an explicit hedge, or removal.

## The self-flagged "one unrated trial" inference — VERIFIED, HOLDS UP

Cross-checked against `data/cleaned/phage_therapy_extraction_dataset.csv`: `ArmataAP_PA02_highdose` has `rob_source = NA` (among the 6 unrated arms) and is independently confirmed as the sole event-positive safety arm (5/10 patients) driving the safety signal's instability. Fair, non-overreaching inference.

## Other checks (all passed)

- 86.1% CI, 37/5 cell count, GLMM 1.0% vs. ~31%, Egger's p=0.022/0.002, Pirnay 11/49, leave-one-out 84.0%/86.1% — all traced exactly.
- No overclaiming of 86.1% beyond what Intro/Results established.
- All citation keys resolve in `Bibliography_base.bib`.
- Limitations #1-3 directionality reasoning is logically sound and appropriately bidirectional.

**Verdict:** Below 80 commit gate. Fix round needed for the 3 substantive items (grey-literature claim, RCT count, overclaimed prior-literature agreement) plus citation-style consistency.

---

## Re-Review (Round 2)

**Score: 89/100** — PASSES commit gate (>=80); does not yet reach PR gate (90).

| Check | Status | Points |
|---|---|---|
| Grey-literature directional claim (Limitations #4) | New logic error introduced: text asserted over-reporting of favorable outcomes would push estimate DOWN, contradicting the Safety Findings subsection's own finding that case reports skew favorable (should push UP) | -10 |
| RCT-count inconsistency | Fixed — results.tex now explicit: "4 randomized trials (3 pooling-eligible, plus Leitner's trial excluded from pooling)"; matches discussion.tex | 0 |
| Overclaimed prior-literature numerical agreement | Fixed — states direction/favorability agreement only, with explicit caveat that no comparable figure exists | 0 |
| Citation-style inconsistency | Fixed — `\textcite{}` used consistently | 0 |
| Length (advisory) | Still applies | -1 |

**Verdict:** Commit-gate PASS. Recommend a targeted follow-up: fix the up/down polarity in Limitations item 4.

---

## Re-Review (Round 3 — targeted polarity fix)

**Score: 96/100** — final.

The grey-literature sentence now correctly states that closing the EMBASE/Web of Science/Scopus gap would plausibly push the pooled estimate further up (not down), consistent with the Safety Findings subsection's own small-study-effect finding, while retaining an appropriate hedge ("most plausibly," "could be wrong"). No spillover issues introduced elsewhere.

**Final verdict: PASS.** Clears both the 80 commit gate and the 90 PR gate.
