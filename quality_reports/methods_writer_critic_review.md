# Writer-Critic Review: `paper/sections/methods.tex`

**Paper type:** Descriptive/measurement — systematic review & meta-analysis of proportions (IMRaD format per `.claude/references/domain-profile.md`)
**Phase:** Execution — STRICT severity
**Score: 64/100** — below the 80 commit gate. Requires a fix round.

## Verdict Summary

This is fundamentally an honest, unusually well-traced Methods section — the search hit counts, the RoB 10/6 split, the 16-arm/14-study and 15-arm/13-study counts, the Krakhotkin/Leitner/Dan2023 narratives, and every citation key all check out against the raw project files. But it contains one **CRITICAL, mechanically-verifiable factual error**, plus a cluster of citation/LaTeX and traceability issues that add up under STRICT severity.

## CRITICAL Issue

**RCT count in the Risk-of-Bias section is wrong.** Methods.tex, Sec. Risk-of-Bias: *"[RoB ratings] have not yet been completed for the 6 study-arms whose extraction remains incomplete, which include all three randomized controlled trials in the dataset..."*

Verified `study_design` for the 6 `EXTRACTION_INCOMPLETE` rows directly in `data/cleaned/phage_therapy_extraction_dataset.csv`: `Pirnay2024_table2subset` (retrospective cohort), `Onallah2023_PASA16_agg` (case series), `Weiner2025_BX004A_phage` (**RCT**), `Jault2019_PhagoBurn_phage` (**RCT**), `Leitner2021_pyophage` (**RCT**), `ArmataAP_PA02_highdose` (**RCT**). That is **four** RCTs among the 6 incomplete arms, not three. The descriptive-statistics table's "RCT 3" figure refers only to the 15 pooling-eligible arms (which exclude Leitner); Leitner is nonetheless explicitly one of "the 6 study-arms whose extraction remains incomplete" in this very sentence, so the sentence undercounts by one RCT within its own stated set. Violates INV-11 (numbers in text must match the underlying data exactly). **-15.**

## Other Findings

1. **Untraced number (INV-22).** "Pirnay et al. (2024) reports 49 *P. aeruginosa* patients across a 100-patient multinational cohort" — the "100-patient" figure appears nowhere in the claim-source map, the extraction CSV, or the codebook. Plausibly true of the source paper, but untraced per this project's own traceability standard. **-5.**
2. **Missing citation commands.** "Magiorakos et al.\ (2012) criteria" appears twice (Eligibility; Data Extraction) as bare prose with no `\parencite`/`\textcite` to `Magiorakos2012_mdrxdr`, despite the same reference being properly cited in `intro.tex`. **-4.**
3. **Duplicated citation.** "Krakhotkin et al.\ (2025) \parencite{Krakhotkin2025_currurol}" — manually typing "et al. (2025)" and then adding `\parencite` renders a redundant double citation. Should be `\textcite{Krakhotkin2025_currurol}`. **-3.**
4. **Cross-section number mismatch.** `intro.tex`: "at least eight further systematic reviews... since 2019." `methods.tex`: "at least eight to nine further systematic reviews... since 2019." Same underlying fact, different precision. **-2.**
5. **Provenance-tag ambiguity.** The claim "no row currently carries a `cross-validated-against-Liu2025` label" is true for the cleaned/pooling dataset (16 rows) but the raw dataset contains an excluded row (`Dan2023_immune_substudy`) carrying exactly that label (used there to confirm duplicate-patient status, not Tier-2 value cross-validation). Not a contradiction of the literal claim, but worth a clarifying phrase ("in the final analytic dataset") to preempt an auditor's confusion. **-2.**
6. **Format.** Manual `Section~\ref{}` throughout rather than `\cref{}` — no `main.tex`/preamble exists yet, so not yet blocking, but flag for conversion once assembled. **-1.**
7. **Writing quality.** The "X, not Y" self-referential-honesty construction ("not a technicality," "not a rounding error," "not a silent departure," etc.) recurs dozens of times — a stylistic tic that reads performative on repetition. Register is more discursive/confessional than a typical published Methods section in this journal tier (CID/AAC/Viruses/Antibiotics); will need trimming before submission even though the transparency is commendable. **-5.**

## Honesty-Critical Claims (verification)

1. **PROSPERO non-registration** — holds. No registration record exists anywhere in project files; stated plainly.
2. **RoB 10/6 split** — holds exactly against the CSV. However, the composition of that 6-arm group is misdescribed (see CRITICAL above).
3. **`data_provenance = independently-extracted` for every row, no `cross-validated-against-Liu2025` label** — holds for the current/cleaned 16-row dataset. Minor ambiguity noted in item 5 re: the raw dataset's excluded Dan2023 row.
4. **EMBASE/WoS/Scopus not searched** — holds, consistently, with no contradicting claim elsewhere.

## Verified and Clean

- Search hit counts (54, 48, 10, 44) match `annotated_bibliography.md` exactly.
- Krakhotkin, Dan2023, and Leitner narratives all match the decision records and raw CSV notes precisely.
- All 18 new/carried-over bibliography keys resolve in `Bibliography_base.bib`.
- 16 arms/14 studies → 15 pooling-eligible/13 studies arithmetic is correct.
- GLMM/HKSJ/convergence-contingency, 13 robustness checks, 6 falsification checks, and the LOS "not applicable, 1 of 15" claim all match `results_summary_phage_therapy_mdr_pseudomonas.md` and coder-critic's Round 2 re-review (97/100).

## Score Breakdown
- Starting: 100
- CRITICAL RCT-count error: **-15**
- Untraced "100-patient" figure: **-5**
- Missing Magiorakos citations (2 instances): **-4**
- Duplicated Krakhotkin citation: **-3**
- Intro/Methods "eight" vs "eight to nine" mismatch: **-2**
- Provenance-tag ambiguity: **-2**
- Manual Section refs (non-blocking, flagged): **-1**
- Performative writing tic / register too discursive for target journals: **-5**
- **Final: 64/100**

---

## Re-Review (2026-07-21, post-fix pass)

**Score: 97/100** — clears both the 80 commit gate and the 90 PR gate.

**Verdict: PASS.** All 7 items from the prior round were verified fixed against source data, not merely asserted fixed.

### Item-by-item verification

1. **[CRITICAL] RCT count — FIXED, independently re-verified.** Methods.tex now reads "all four randomized controlled trials." Direct read of `data/cleaned/phage_therapy_extraction_dataset.csv` confirms 4 of the 6 `EXTRACTION_INCOMPLETE` arms are RCT (Weiner2025, Jault2019/PhagoBurn, Leitner2021, ArmataAP_PA02), and 2 are not (Pirnay2024 = retrospective cohort, Onallah2023 = case series).
2. **[MAJOR] "100-patient" figure — FIXED.** New row added to the claim-source map citing `data_dictionary.md` and `annotated_bibliography.md` as the source-paper's own reported cohort size. Legitimate.
3. **[MAJOR] Magiorakos citations — FIXED.** Both bare-prose instances now use `\textcite{Magiorakos2012_mdrxdr}`.
4. **[MINOR] Krakhotkin duplicate — FIXED.**
5. **[MINOR] Cross-section mismatch — FIXED, reasoning sound.** "Eight" verified correct for a claim scoped to human phage therapy reviews (the 9th post-2019 synthesis is preclinical/animal-only).
6. **[MINOR] Provenance-tag ambiguity — FIXED.**
7. **[MINOR, style] Performative tic — SUBSTANTIALLY FIXED.** Reduced from dozens to 12 instances, each now serving genuine disambiguation. All substantive honesty disclosures (PROSPERO non-registration, single-reviewer process, outstanding RoB/cross-validation work) remain clearly stated.

### Score Breakdown
- Starting: 100
- Manual Section refs (deferred pending main.tex assembly, non-blocking): **-1**
- Residual discursive register (improved, not eliminated): **-2**
- **Final: 97/100**

No new errors introduced by the fix pass.
