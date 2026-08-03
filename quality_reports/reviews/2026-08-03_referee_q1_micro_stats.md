# Referee report — Q1 clinical microbiology / infectious diseases

**Manuscript:** *Phage Therapy for MDR/XDR/PDR* Pseudomonas aeruginosa*: A Systematic Review and Meta-Analysis of Proportions*
**Reviewer remit:** MDR *P. aeruginosa* microbiology + proportion meta-analysis methodology
**Date:** 2026-08-03

> **Note on verification.** Every manuscript figure cited below was re-derived from
> the authors' own pipeline output before being used in an argument. Two of the
> figures supplied to me in the review brief did not survive that check and are
> corrected in-line where they appear (§4, §11).

---

## 1. Editorial recommendation

**Major Revision** — the synthesis is methodologically sound and unusually transparent, but it mislabels its own statistical machinery in 11 of 13 pooled cells, stratifies on the wrong clinical axis, and confines the only non-confounded evidence in the field (the randomized trials) to narrative text while granting quantitative status to the reporting-biased single-arm literature; none of these is fatal and all are correctable without new data.

## 2. Executive summary (198 words)

This review should not be reclassified as a scoping review, and I part company with that suggestion. Its most valuable outputs are precisely the quantitative ones a scoping review cannot generate: the demonstration that eradication heterogeneity is a mixture artefact (τ² falls from 1.995 to exactly 0.000 once chronic-airway arms are separated), and the classification-sensitivity analysis showing the MDR stratum collapses from 17 studies to 2 under independently verified resistance labels. Those are findings, and they are quantitative.

What must change is the labelling and the architecture around them. In 11 of 13 pooled cells τ̂² = 0, so no random effect is identified and the "random-effects meta-analysis" is an exact binomial proportion with a t-quantile; calling it otherwise misleads. Stratification is by administration route when the authors' own data show syndrome is the operative axis. Resistance-class labels are author-asserted and, when verified, do not support pooling at all.

Microbiologically, the intervention is under-ascertained in a way the review now concedes but has not propagated: 3 of 40 arms document that the phage was active against the isolate, and 9 of 40 assess resistance emergence.

## 3. Detailed microbiological analysis (Axes 1–3)

### 3.1 The population criterion in the post-BL/BLI era (Axis 1)

The Magiorakos/Kadri dual axis is defensible but is doing less work than the manuscript believes, and for a reason the manuscript half-identifies.

Magiorakos counts *categories* resisted. Ceftazidime-avibactam, ceftolozane-tazobactam and cefiderocol postdate the 2012 scheme, and an isolate meeting the 2012 XDR definition may today be comfortably treatable — the label is a statement about the 2012 formulary, not about therapeutic options at the bedside. Kadri's DTR is the correct instrument for the decision the manuscript cares about (are all first-line agents lost?), and the authors are right to carry it. The manuscript's own correction of its DTR criterion — it had required non-susceptibility to *all* β-lactams, which is stricter than Kadri's first-line set and rendered DTR-negative unreachable — is exemplary self-correction and should be retained in the text, not tidied away.

The residual problem is that DTR is adjudicable in a minority of arms, and the stated reason is right: sources name the agents *administered*, not the agents *tested*. This is the single most consequential reporting failure in the corpus and it is stated well.

**However, the manuscript does not draw the inference that follows.** If resistance class is author-asserted and only partially verifiable, then resistance class is not a valid stratification variable, and the classification-sensitivity analysis proves it: under independently verified labels the MDR clinical-success cell falls to **2 studies and 3 patients** and is not poolable at all. Stratifying the primary synthesis on a variable that dissolves under verification is not a limitation to be noted — it is a reason to demote the resistance-stratified estimates from primary results to sensitivity analyses. See §6, row 2.

### 3.2 The randomized-trial exclusion (Axis 1, continued)

Here I am more critical than the brief.

The exclusion rule is coherent as stated: a trial enrolling on chronic colonization or burn-wound infection without a resistance filter is estimating a different estimand. I accept that. And the concern that a burn cohort's isolates might still be resistant is weaker than it appears, since the manuscript's rule turns on the *population definition*, not on any individual isolate.

The serious problem is structural and the manuscript does not confront it. The exclusion removes **every randomized trial** from the quantitative synthesis. Those trials — PhagoBurn (stopped for futility), CYPHY (−0.59 vs −0.89 log CFU/mL, no separation), BX004-A (safety met, efficacy underpowered), SWARM-P.a. (no efficacy claim) — constitute the field's only comparative evidence, and it is uniformly null or negative. Meanwhile the compassionate-use literature, whose publication is conditional on favourable outcome, retains quantitative status and yields 78.7% clinical success.

The result is an asymmetry that no reader can be expected to correct for unaided: **the positive evidence is pooled and the negative evidence is prose.** Whatever the estimand justification, a synthesis whose architecture systematically assigns quantitative weight to the biased stream and narrative weight to the unbiased one will be read as supporting phage therapy. This must be addressed structurally, not by a caveat (§6, row 1).

### 3.3 Phage resistance and the ascertainment problem (Axis 2)

The 44% figure (4 of 9 arms assessed) should not be reported as a rate. It is conditioned on assessment, and assessment is not random: an arm is investigated for phage resistance largely when failure prompts the question. The 4 is therefore a floor on *documented* emergence and an unknown quantity relative to true emergence — biased upward by indication, downward by the 31 arms where non-assessment guaranteed non-detection. State both directions or omit the percentage.

This connects to a finding the authors have now made and should elevate: **3 of 40 arms document any phage-susceptibility testing** — a phagogram, an EOP measurement, a spot test, or a plain statement of activity. Taken together, these two counts say something sharper than either alone: *this literature does not routinely establish that the phage could lyse the organism, nor whether it stopped being able to.* That is a statement about the intervention's ascertainment, and it belongs in the abstract, not only in a results subsection.

On the mechanistic question: yes, 4 documented escapes across O-antigen loss (Li 2025), efflux-mediated trade-off (Chan 2018, OMKO1/MexAB-OprM) and population diversification (Zaldastanishvili 2021) is a coherent signal that narrow cocktails are unsustainable in this organism — but with n=9 assessed, the review cannot carry that claim quantitatively and should attribute it to the mechanistic literature rather than to its own corpus.

### 3.4 Syndrome versus route (Axis 3)

**I regard this as the most actionable microbiological finding in the manuscript, and the authors have under-exploited it.**

The split is genuine, not a category error in the pejorative sense — it is a category error the authors have already diagnosed and quantified. Among non-airway sites, pooled eradication is 62.3% with τ² = **0.000**; among chronic-airway arms it degenerates (3.1%, 95% CI 0.0–96.9%, τ² = 17.097). A variance component that falls from 1.995 to exactly zero on a single clinically motivated split is about as clean a demonstration as this literature permits that the pooled construct was a mixture.

The microbiology is not in doubt: in established endobronchial biofilm — cystic fibrosis, bronchiectasis in primary ciliary dyskinesia, chronic ILD colonization — eradication is neither achieved nor sought by any antimicrobial modality, and the field's endpoints there are density, exacerbation frequency and lung function. Pooling that with sterilized bacteraemias and explanted culture-negative implants measures case-mix.

**Recommendation:** syndrome (sterile-site/bloodstream, device-related, bone and joint, chronic airway, wound/soft tissue) should replace route as a pre-specified stratification axis, or at minimum join it. Route is a property of the delivery system; syndrome is a property of the biology that determines whether the endpoint is attainable. The authors' own τ² is the evidence.

## 4. Detailed statistical analysis (Axes 4–10)

### 4.1 The GLMM versus Freeman-Tukey (Axis 4) — the brief's inference is wrong

The brief asks whether the cross-model divergence indicates the data are too sparse for *any* model. **It does not, and the pattern is diagnostic in the authors' favour.** This is the one axis where I disagree with the premise, and the arithmetic settles it.

For overall mortality (k = 32 studies, N = 76 patients, 7 events):

| Model | Estimate |
|---|---|
| Crude proportion, 7/76 | **9.21%** |
| Binomial-normal GLMM | **9.2%** |
| Freeman-Tukey double arcsine | 0.5% |
| Logit DerSimonian-Laird | 24.0% |
| Logit fixed-effect | 24.0% |

Two facts the brief's framing obscures. First, **the GLMM reproduces the crude proportion exactly** — which is the correct behaviour when τ̂² = 0 and the binomial likelihood is used without approximation. Second, **DL and FE are identical to three significant figures**, necessarily so, because τ̂² = 0 under DL collapses the random-effects model onto the fixed-effect one. So the "three models" are not three competing random-effects estimators. They are one correctly specified likelihood, plus two known failure modes of normal approximations to sparse binomial data:

- **Freeman-Tukey's 0.5%** is the documented back-transformation pathology under extreme sample-size heterogeneity (arms from n = 1 to n = 23), exactly as Schwarzer, Chemaitelly, Abu-Raddad & Rücker (2019) describe; the harmonic-mean back-transformation is not defined sensibly when the n distribution is this skewed.
- **DL's 24.0%** is a continuity-correction artefact. With 33 of 40 arms at n = 1, the logit is undefined for every zero-event arm, the 0.5 correction is applied throughout, and inverse-variance weighting on the corrected logit scale pulls systematically toward 0.5. This is precisely why Cochrane Handbook §10.4.4.1 and Stijnen, Hamza & Özdemir (2010) recommend the exact binomial likelihood over normal approximations for rare events.

The same signature recurs in the not-classifiable clinical-success cell: crude 23/26 = 88.46%, GLMM 88.5%, FT 98.2%, DL/FE 76.6% — GLMM on the crude value, the approximations diverging in *opposite* directions.

**The authors' model choice is correct and their justification, while adequate, undersells itself.** They should replace the current appeal to Schwarzer with this arithmetic: a model that returns the observed proportion when no heterogeneity is identified is behaving correctly; models that return 0.5% and 24.0% when 9.2% was observed are exhibiting named, citable failure modes. Table 6 is evidence *for* the primary model.

### 4.2 τ² = 0 and the random-effects label (Axis 5) — agreed, and this is the highest-priority statistical change

The authors' interpretation of τ̂² = 0 as non-identification rather than homogeneity is correct and creditable: with 33 of 40 arms contributing a single patient, the random intercept is identified only by the 7 multi-patient arms, and a boundary estimate is what one expects.

But the reporting does not follow the interpretation. When τ̂² = 0 the GLMM *is* a fixed-effect binomial model with a t-quantile; the prediction interval collapses onto the confidence interval (visible in the authors' own output, where `PIlo`/`PIhi` equal the CI bounds for the not-classifiable cell); and no between-study variance is being propagated. Presenting these as "random-effects estimates with 95% CI and prediction interval" implies an uncertainty architecture that is not there.

**Required:** in the 11 cells with τ̂² = 0, report the estimate as a pooled binomial proportion with an exact or t-based interval, state τ̂² = 0 and that it is at the boundary, and **suppress the prediction interval** rather than printing one identical to the CI. Retain the random-effects presentation only for the two eradication cells where τ̂² > 0. This is not a downgrade of the analysis; it is an accurate description of it.

### 4.3 Intra-study dependency (Axis 6)

The dependency is real: study-arm as unit (40) against study (33), with Pirnay et al. contributing three resistance-stratified arms drawn from one consecutive cohort.

I do not think a Bayesian hierarchical model rescues this, and I would discourage the authors from adding one. With 33 singleton arms, a weakly informative prior on τ² does not recover information the data lack — it substitutes the prior for the estimate, and the posterior for τ² would be prior-dominated. That is less honest than a boundary estimate that announces itself. The authors' cluster-robust check, with Satterthwaite df of 3.6–9.7, already tells the correct story: **below roughly 10 clusters, no robust-variance method delivers nominal coverage** (Tipton 2015; Pustejovsky & Tipton 2018), so the honest conclusion is that dependency cannot be adequately corrected, not that a different estimator would correct it.

**Required:** state that explicitly, and — because it is the fix that actually works — report a leave-one-study-out analysis omitting Pirnay entirely for the MDR stratum, so the reader sees the estimate with and without the dominant cluster.

### 4.4 HKSJ (Axis 7)

When τ̂² = 0, HKSJ's variance inflation factor reduces to 1 and only the t-quantile survives (2.028 versus 1.960 at 36 df). This is a negligible widening and provides no protection against the actual threat, which is not Type I error from unmodelled heterogeneity but selection on outcome in the source literature. Reporting "HKSJ applied" across all cells implies a robustness that is absent in 11 of them; say where it binds and where it does not. In the two cells where it does bind, the SE ratio of 2.92 is substantial and appropriately reported.

Bootstrap or permutation inference would not help: with 33 singleton arms the resampling distribution is dominated by the same sparse structure, and permutation requires an exchangeability null that single-arm proportions do not furnish.

### 4.5 Publication bias (Axis 8) — abandon the tests, and replace them with the analysis you already have

The switch from Egger to Peters was correct — Egger's regression is invalid for proportions because the standard error is a deterministic function of the proportion, inducing mechanical correlation between regressor and outcome (Hunter et al. 2014). The switch should be stated as a correction, which it is, not buried.

But Peters' test is equally uninformative here, and for a reason worth stating plainly: its regressor is 1/n, which equals 1 for 33 of 40 arms and takes five distinct values in total. **No funnel-based method has power distinguishable from zero on this corpus**, and the reported p-values (0.66, 0.18, 0.82) should not be presented as evidence of absence. Selection models (Vevea & Woods) will not help either — they require a distribution of p-values, and single-arm proportions do not generate one.

**The authors should delete the funnel-plot machinery and put in its place the structural analysis they are uniquely positioned to perform, and have already assembled the pieces for:** the four randomized trials are uniformly null or negative; the compassionate-use corpus, whose publication is conditional on outcome, yields 78.7%. That contrast *is* the publication-bias analysis, it is far more informative than any regression on 1/n, and it converts a methodological dead end into the paper's most important comparison (§6, row 1).

### 4.6 Pooling threshold and the not-classifiable cell (Axis 9)

The k ≥ 3 / N ≥ 20 threshold is reasonable and, importantly, pre-specified. The appendix relaxation (k ≥ 2, N ≥ 10) is acceptable *because* it is confined to an appendix and explicitly not promoted — I would not remove it, since a reader who wants to know what the threshold cost is entitled to see it. Keep it, and keep the label.

The not-classifiable clinical-success cell is a different matter and the brief's suspicion is well founded. This stratum is defined by the *absence* of resistance documentation, and it returns the highest point estimate in the review (88.5%, 95% CI 66.5–96.7%), above the MDR stratum (75.0%). Under the authors' own eligibility logic — a missing panel is a documentation gap, not evidence of susceptibility — there is no biological mechanism by which absence of documentation should predict success. Two explanations remain: these patients were less resistant, or documentation quality is inversely related to outcome.

**This is testable with data the authors already hold.** They report a journal-tier falsification analysis; the same machinery should be turned on this question — does resistance documentation vary with journal tier, publication year, or report length? Whatever the answer, the cell should carry an explicit statement that it is a stratum defined by missingness and cannot be interpreted as a resistance class. I would not suppress it; suppressing the highest estimate because it is inconvenient is its own bias.

### 4.7 GRADE (Axis 10)

Every cell reaching Very low is not a failure of GRADE's discrimination — it is the correct answer, arrived at by an external and recognised standard, and that external provenance has rhetorical value precisely because the conclusion is unwelcome. I would **not** move it to an appendix.

The authors should, however, state the determinism explicitly: for uncontrolled observational proportions, risk of bias, indirectness and publication bias each deduct at least one level from a Low starting point, so Very low is structurally guaranteed and carries no information about *relative* certainty across cells. A brief statement to that effect converts an apparent redundancy into an honest disclosure. A parallel narrative descriptor is unnecessary.

## 5. Integrated analysis (Axes 11–12)

### 5.1 Should this become a scoping review? (Axis 11) — No, and the reasoning matters

I disagree with reclassification, and the argument is not one of convenience.

A scoping review cannot produce this manuscript's two most valuable results. Neither the eradication mixture demonstration (τ² 1.995 → 0.000 on the airway/non-airway split) nor the classification-sensitivity collapse (MDR clinical success: 17 studies at author-reported labels, **2 studies and 3 patients** verified — the brief's "3 studies / 4 patients" understates the collapse) is available without fitting models. Both are quantitative findings *about the evidence base*, and they are the most useful things in the paper. Discarding the apparatus that generated them to satisfy a genre label would destroy the contribution.

The legitimate concern behind the suggestion is that readers will extract "78.7%" and treat it as efficacy. That is a real and serious risk, and the authors' epistemological framing — "a proportion of the published record, not of treated patients" — is necessary but insufficient, because it is a sentence and the number is a headline.

**The fix is architectural rather than generic.** Demote the pooled proportions from the abstract's principal result to a descriptive characterisation of the published record; promote to the principal result what the review actually establishes — that resistance class dissolves under verification, that eradication is not one construct, that the intervention is documented as active in 3 of 40 arms, and that the randomized evidence is null. The paper then reports what it can support. It remains a meta-analysis, and it becomes an honest one.

### 5.2 RCTs versus compassionate use (Axis 12)

The partition is defensible on estimand grounds and indefensible in presentation, as argued in §3.2. The four trials are the only comparative evidence in the field and their signal is null to negative.

**A structured comparison table is required, not optional** — RCTs versus observational arms, with design, population, whether resistance was an entry criterion, endpoint, and result. It should appear in the main text near the pooled estimates, not in Section 4.2 discussion prose. Without it, the manuscript's architecture communicates a conclusion its authors explicitly disclaim.

## 6. Mandatory changes

| # | Priority | Required change | Justification | Reference |
|---|---|---|---|---|
| 1 | **Critical** | Add a structured RCT-versus-observational comparison table to the main text adjacent to the pooled estimates; state that the only comparative evidence is null/negative while pooled proportions derive from outcome-conditional reports | Quantitative status is currently granted to the biased evidence stream and narrative status to the unbiased one; readers cannot correct this unaided | PRISMA 2020 items 13d, 20d, 22; Cochrane Handbook §13.3 |
| 2 | **Critical** | Demote resistance-stratified pooled estimates to sensitivity analyses; report the verified-classification collapse (MDR clinical success: 2 studies, 3 patients) in the main text and abstract | A stratification variable that dissolves under independent verification cannot carry primary results | PRISMA 2020 item 16; GRADE indirectness |
| 3 | **Critical** | In the 11 cells with τ̂² = 0, report pooled binomial proportions with exact/t-based intervals; state the boundary estimate; suppress the prediction interval; retain random-effects presentation only for the two eradication cells | A prediction interval identical to the CI implies uncertainty propagation that does not occur | Cochrane Handbook §10.10.4.1; Veroniki et al. 2016 |
| 4 | **Major** | Replace route with infection syndrome as a pre-specified stratification axis, or add it; report the airway/non-airway eradication split as a primary result | The authors' own τ² (1.995 → 0.000) shows syndrome, not route, governs whether the endpoint is attainable | Cochrane Handbook §10.11.5 |
| 5 | **Major** | Delete Peters' test and funnel-plot machinery; state that no funnel-based method has power on this corpus; substitute the RCT-versus-observational contrast as the publication-bias assessment | Regressor is 1/n = 1 for 33 of 40 arms with five distinct values; reported p-values cannot support inference | Hunter et al. 2014; Cochrane Handbook §13.3.5.4 |
| 6 | **Major** | Report phage-susceptibility documentation (3/40 arms) and resistance-emergence ascertainment (9/40 assessed) in the abstract; remove the 44% figure or state its bidirectional ascertainment bias | A rate conditioned on non-random assessment is not a rate; the intervention's activity is unverified in 92.5% of arms | GRADE indirectness; PRISMA 2020 item 13 |
| 7 | **Major** | Reframe the Table 6 cross-model comparison as support for the GLMM: state that GLMM reproduces the crude proportion while FT and DL exhibit named failure modes (back-transformation under n-heterogeneity; continuity correction with 33 singleton arms) | Currently presented as unexplained instability; it is diagnostic evidence for the primary model | Schwarzer et al. 2019; Stijnen et al. 2010; Cochrane Handbook §10.4.4.1 |
| 8 | **Minor** | Add leave-one-study-out omitting Pirnay for the MDR stratum; state that with Satterthwaite df 3.6–9.7 no robust-variance method achieves nominal coverage and dependency cannot be adequately corrected | Cluster-robust correction is being reported as a remedy where it is diagnostic only | Tipton 2015; Pustejovsky & Tipton 2018 |

## 7. Questions for the authors

1. Under independently verified resistance classification the MDR clinical-success cell falls to 2 studies and 3 patients. Given that resistance class is the review's primary stratification axis, on what basis should any resistance-stratified pooled estimate retain primary-result status rather than being reported solely as a sensitivity analysis?

2. Of 40 pooling-eligible arms, 3 document that the administered preparation was active in vitro against the patient's isolate. Onsea 2019 was excluded precisely because its cocktail was inactive — establishing that inactive administration occurs and is not hypothetical. What proportion of the remaining 37 arms would have to have received an inactive preparation before the pooled clinical-success estimate ceased to describe phage therapy at all, and can you bound that quantity?

3. The not-classifiable stratum, defined by absence of resistance documentation, yields the review's highest clinical-success estimate (88.5%) — above the MDR stratum (75.0%). Using your existing journal-tier and publication-year falsification machinery, does resistance documentation covary with report characteristics in a way consistent with outcome-dependent reporting, and if so what does that imply for the 78.7% overall estimate?

4. Your eradication τ² falls from 1.995 to exactly 0.000 when chronic-airway arms are separated, indicating the pooled construct was a mixture. Applying the same test to clinical success across infection syndromes, does the clinical-success construct survive, and if it does not, what is the justification for reporting a pooled clinical-success proportion at all?

5. The four randomized trials are uniformly null or negative and are excluded from quantitative synthesis on estimand grounds; the compassionate-use corpus is retained and yields 78.7%. If the review's population criterion were relaxed to admit the trials, what would the pooled clinical-success estimate become — and if that number is materially lower, how do you justify an architecture in which the estimand definition and the direction of publication bias act in the same direction?

## 8. Reviewer conclusion (147 words)

The *P. aeruginosa* phage-therapy evidence base is not mature enough to support a meta-analysis whose headline output is a pooled efficacy-like proportion — 33 of 40 arms carry one patient, resistance labels dissolve under verification, the intervention's activity against the target organism is documented in 3 arms, and the only randomized evidence is null. It is, however, mature enough for the paper this manuscript is roughly 80% of the way to being: a quantitative anatomy of why the evidence cannot yet answer the clinical question, with the mixture-artefact and classification-collapse analyses as its principal results.

The authors' transparency is genuinely exceptional — they correct their own DTR criterion, disclose an un-blocked search that enlarged their corpus, and interpret τ̂² = 0 correctly as non-identification. That candour is the manuscript's chief asset. The required revisions ask them to let the architecture of the paper say what their prose already concedes.
