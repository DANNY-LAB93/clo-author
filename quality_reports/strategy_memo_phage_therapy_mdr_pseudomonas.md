# Strategy Memo: Phage Therapy for MDR/XDR *Pseudomonas aeruginosa* — A Stratified Meta-Analysis of Proportions

**Date:** 2026-07-19
**Project:** phage_therapy_mdr_pseudomonas
**Paper type:** **Descriptive / Measurement** (evidence synthesis) — a systematic review producing a validated, stratified pooled-proportion measure of clinical outcomes. No causal design (DiD/IV/RDD) applies. Per `.claude/references/domain-profile.md`, "identification strategy" is reinterpreted here as **the design that lets pooled proportions be validly interpreted as summaries of the evidence base** — not as causal effects. There is no comparative-effect (RR/OR) primary estimand because the discovery phase confirmed (two independent search rounds, 0-1 qualifying dual-arm comparative studies) that the literature cannot support one. No secondary structural or theory component; the theorist agent should **not** be dispatched (per `permissions.md` CONDITIONAL flag).

---

## Pre-Strategy Report

**Date:** 2026-07-19
**Project:** phage_therapy_mdr_pseudomonas

### Inputs Read
- **Research spec:** `quality_reports/research_spec_phage_therapy_mdr_pseudomonas.md` — read in full (revision history, PICO, empirical strategy, Open Questions).
- **Decision record:** `quality_reports/decisions/discovery_phage_therapy_mdr_pseudomonas.md` — read in full (three decision records: comparative-only design → failed; pivot to proportions meta-analysis → approved; 2019 search-cutoff → failed, superseded).
- **Literature review:** `quality_reports/literature/phage_therapy_mdr_pseudomonas/{annotated_bibliography.md, positioning.md, frontier_map.md, librarian_critic_review.md}` — read in full, including all three rounds (final librarian-critic score 93/100).
- **Data assessment:** `quality_reports/data-assessment/phage_therapy_mdr_pseudomonas/{data_sources.md, data_dictionary.md, access_instructions.md, explorer_critic_review.md}` — read in full, including Round 1→2 revisions and the orchestrator's independent verification of `mmc2.pdf` (final explorer-critic score 89/100).
- **Domain profile:** `.claude/references/domain-profile.md` — loaded (Research Question, Common Identification Strategies, Notation Conventions, Field-Specific Referee Concerns sections read in full — this file has been substantially rewritten for this project, not left at economics defaults).
- **Research journal:** `quality_reports/research_journal.md` — read in full, including the 2026-07-19 entry documenting the ad hoc 201-PDF PRISMA screening (`Cribado_Sistematico_201_PubMed_Elicit.xlsx`, referenced but not independently re-opened by this agent — its contents are taken from the journal's summary, per task instructions).

### Research Question
Among patients with MDR/XDR *Pseudomonas aeruginosa* infections treated with bacteriophage therapy, what is the pooled proportion of clinical success and the pooled proportion of safety events, and how do these vary by resistance category (MDR vs. XDR), route of phage administration, and treatment modality (antibiotic monotherapy vs. phage-antibiotic combination)?

### Key Findings from Literature
- **No comparative-effect design is feasible.** Three search rounds (PubMed E-Utilities, ClinicalTrials.gov API v2, forward-citation screening of Liu et al. 2025's own supplementary RoB tables, and an ad hoc 201-PDF screen) converge on the same conclusion: essentially 0-1 genuine dual-arm comparative studies exist that combine (a) an MDR/XDR-*Pseudomonas*-specific population, (b) a real antibiotic-monotherapy arm, and (c) a real phage+antibiotic-combination arm, in the same study. This is why the project pivoted from a comparative-effect meta-analysis to a **meta-analysis of proportions** — the only design the evidence base can actually support.
- **8-9 prior systematic reviews/meta-analyses exist since 2019** (El Haddad 2019, Aranaga 2022, Uyttebroek 2022, Ibrahim 2025, Liu et al. 2025 [IJAA, IPD meta-analysis, 130 studies], Terlizzi 2026, Terzi 2026, plus a preclinical-only Lancet Microbe 2022 review and a CF-specific 2023 review). **None stratifies by MDR vs. XDR for *Pseudomonas* specifically, and none isolates comparative vs. single-arm evidence.** This is the project's contribution.
- **Liu et al. (2025) is the single highest scooping-risk paper** and also, critically, the source of a reusable supplementary case-level dataset (`mmc2.pdf`, ~324 rows, ~130 studies) — see Section 3 below, the most consequential open decision in this memo.
- **Two genuinely new comparative leads surfaced from Liu et al.'s own RoB tables**, independently verified via direct PubMed calls: **Krakhotkin et al. (2025)** (4-arm observational comparative study: antibiotic-only, phage-only, phage+1 antibiotic, phage+2 antibiotics, n=178, MDR cystitis, Pseudomonas-specificity unconfirmed) and **Leitner et al. (2021)** (3-arm RCT: phage vs. placebo vs. **systemic antibiotics**, n=113, UTI, Pseudomonas confirmed among enrolled pathogens but subgroup proportion unconfirmed). These are the closest structural precedents found anywhere in this search for the monotherapy-vs-combination stratification and are central to the sparsity contingency plan in Section 4 below.
- **Methodological anchors for the pooling model:** Freeman & Tukey (1950) and Miller (1978) for the double-arcsine transformation; Hamza, van Houwelingen & Stijnen (2008) and Nyaga et al. (2014) for GLMM-based prevalence meta-analysis; **Schwarzer, Chemaitelly, Abu-Raddad & Rücker (2019, Res Synth Methods)** for the documented failure mode of double-arcsine back-transformation under heterogeneous study sizes (directly relevant here — this literature ranges from n=1 case reports to n=100 cohorts); IntHout, Ioannidis & Borm (2014) for the Hartung-Knapp-Sidik-Jonkman (HKSJ) adjustment recommended for the small number of studies expected per stratum; Munn et al. (2015) and Barker et al. (2021, JBI) for prevalence-meta-analysis best practice generally; Murad et al. (2018) for case-report/small-case-series critical appraisal.

### Available Data
- **Primary extraction targets (Grade A/B, accessible without institutional subscription):** Pirnay et al. 2024 (100 cases, 49 *P. aeruginosa*), Weiner et al. 2025/BX004-A (n=9, CF, RCT), Green et al. 2023/PASA16 (n=15-16, case series), Jault et al. 2019/PhagoBurn (n=27, RCT vs. SOC), Armata AP-PA02 (n=29, CT.gov structured results only). Two studies (Nir-Paz/TP-102, Petrovic-Fabijan) are paywalled and lower-priority (no confirmed Pseudomonas/MDR subgroup or background-pathogen only).
- **Registry-style aggregate sources:** Belgian consortium (= Pirnay 2024, already counted) and the Israeli Phage Therapy Center 5-year report (PMID 37234511, OA, mixed-pathogen, Pseudomonas subgroup to confirm).
- **Reusable structured dataset:** Liu et al. (2025)'s supplementary `mmc2.pdf` — ~324-row case-level table across ~130 studies, with a schema closely overlapping this project's own extraction form, plus pre-existing RoB2/ROBINS-I/NHLBI/JBI risk-of-bias assessments for ~90 studies. This is the single most consequential open resourcing decision — see Section 3.
- **Variation available for identification (i.e., for pooling):** no panel/time-series structure; the "variation" here is **cross-study variation in reported proportions**, decomposed by the three pre-specified stratification variables (MDR/XDR, route, modality) plus study design (RCT/cohort/case series) as a risk-of-bias moderator.
- **Known data limitations:** (1) EMBASE/Web of Science/Scopus remain unsearched — user-dependent, not yet closed; (2) most primary studies report cohort-wide, not *Pseudomonas*-specific, statistics (Pirnay, Israeli PTC) — sub-extraction from supplementary tables required; (3) MDR/XDR classification is expected to be author-reported (not independently Magiorakos-verifiable) for a large fraction of studies; (4) the antibiotic-monotherapy-only stratum may be genuinely unextractable beyond Krakhotkin/Leitner (both pending full-text Pseudomonas-subgroup confirmation); (5) the two most accessible large aggregate cohorts (Pirnay/Belgium, Israeli PTC) share a referral/compassionate-use selection mechanism and a Belgium/Israel geographic concentration that risks non-representativeness of the pooled estimate.

### Candidate Designs
1. **Random-effects meta-analysis of proportions, GLMM (binomial-normal, logit link) primary, double-arcsine and simple logit-DL as sensitivity** — feasible; exploits the abundant single-arm evidence without requiring a paired comparator; explicitly handles the varying study sizes (n=1 to n=100) that make naive double-arcsine back-transformation risky (Schwarzer et al. 2019). **Recommended primary design — see Section 1.**
2. **Random-effects meta-analysis of proportions, Freeman-Tukey double-arcsine primary (per the domain profile's current literal wording)** — feasible, but flagged as the methodologically weaker choice given this project's specific sample-size heterogeneity; retained as the first sensitivity check, not primary. **Deviation from domain-profile.md flagged explicitly below — recommend the user approve updating that file.**
3. **Comparative-effect (RR/OR) meta-analysis restricted to Krakhotkin/Leitner/PhagoBurn** — not feasible as a primary design (n=2-3 studies, none confirmed Pseudomonas-specific yet); retained only as a clearly-labeled exploratory/supplementary analysis, never as the paper's headline result.
4. **Narrative-only scoping review (no pooling)** — feasible but rejected; discards quantifiable signal the single-arm literature can support, and the user has already approved the proportions-pooling design (decision record, 2026-07-18).

### Missing Inputs
- **Full text of Liu et al. (2025) and Uyttebroek et al. (2022)** not yet obtained — needed to finalize the contribution-differentiation claim (research spec Open Question #1). **ASSUMED:** proceeding on the current differentiation framing (MDR/XDR-*Pseudomonas*-specific stratification not present in either prior synthesis, per abstract-level evidence); flag for revision once full text is read.
- **EMBASE/Web of Science/Scopus searches** — pending user's institutional access. **ASSUMED:** the strategy below is designed to be re-run, not redesigned, once these results arrive (i.e., additional studies slot into the existing extraction schema and stratification plan; they do not require a new design).
- **PROSPERO/WHO ICTRP direct queries** — blocked (HTTP 403 / JS-gated) in this agent's environment; only indirect web-search verification exists. See Section 8.
- **Pseudomonas-specific, MDR/XDR-classified subgroup data for Krakhotkin (2025), Leitner (2021), Karn (2024), Rhoads (2009), Stanley (2025)** — all five require full-text retrieval before their eligibility/extraction can be finalized. This directly gates the monotherapy-stratum contingency plan (Section 4).
- **Green et al. (2023) vs. "Onallah et al." authorship discrepancy** — unresolved; must be settled before the coder builds the extraction spreadsheet (data_sources.md already flags this).
- **The 201-PDF ad hoc screening result (12 INCLUIDO/9 new candidates)** — this agent did not independently re-open the `.xlsx`; its status and disposition are addressed explicitly in Section 8 as a registration-timing issue.
- **Dual-independent-extraction resourcing** — the domain profile's Field Conventions require dual independent screening/extraction, but team capacity is not documented in any discovery artifact. **ASSUMED:** flagged as an open resourcing question for the user/orchestrator before the coder begins (see Section 2).

Proceeding to strategy design.

---

## Cross-Reference: Task Items → Memo Sections

| Requested item | Section |
|---|---|
| 1. Design/estimand/comparison structure | §1 Estimand, §2 Specification |
| 2. PICO → extraction form mapping, MDR/XDR decision rule | §2 Specification (2.2) |
| 3. Liu et al. (2025) dataset reuse decision | §3 (standalone) |
| 4. Risk of bias approach | §4 (standalone) |
| 5. Sensitivity/robustness plan | §5 Robustness Plan |
| 6. Falsification/negative-control checks | §6 (standalone) |
| 7. Referee objection anticipation | §7 Threats |
| 8. PRISMA/registration considerations | §8 (standalone) |
| Assumptions (mandatory section) | §3.5-style content folded into §1.3/§Assumptions below |

---

## 1. Estimand

**What are we estimating?** Not a causal treatment effect. Four families of pooled proportions, each defined at the study-arm level and estimated separately within each pre-specified stratum (not pooled into one headline number):

$$
\hat{p}_{\text{success}}^{(s)}, \quad \hat{p}_{\text{safety}}^{(s)}, \quad \hat{p}_{\text{eradication}}^{(s)}, \quad \hat{p}_{\text{mortality}}^{(s)}
$$

where $s$ indexes a stratum cell defined by the cross of {MDR, XDR, not-classifiable} × {route: topical/local, IV, inhaled/nebulized, oral, intra-articular, other} × {modality: phage monotherapy, phage+antibiotic combination, antibiotic monotherapy}.

**In words:** the true underlying proportion of patients experiencing each outcome, among the population of patients described in the published/registered literature meeting this review's eligibility criteria (MDR or XDR *P. aeruginosa* infection, treated with bacteriophage in the given route/modality) — **not** a claim about the general population of all MDR/XDR *Pseudomonas* patients who might plausibly benefit from phage therapy. This distinction matters because the two largest, most accessible cohorts (Pirnay/Belgium, Israeli PTC) are referral/compassionate-use populations (§ data_dictionary.md §4) — the estimand is explicitly a **descriptive summary of the available evidence base under its actual selection mechanism**, not an unbiased estimate of population prevalence.

**Population:** patients meeting the eligibility criteria above, as reported in eligible primary studies (single-arm and comparative), 2019-present (subject to the search-cutoff revision in Section 8) plus any pre-2019 studies surfaced by full-text retrieval of the five Round-3 leads.

**Compliers/LATE characterization:** N/A — there is no instrument or treatment-assignment mechanism being exploited; every stratum cell is a direct proportion, not a local average treatment effect.

**Secondary, contextual estimand (not the headline result):** an unstratified pooled-all proportion, $\hat{p}_{\text{success}}^{(\text{all})}$, reported only for comparability with prior non-stratified reviews (El Haddad, Uyttebroek, Liu et al.) — explicitly labeled in the manuscript as **secondary/contextual, not primary**, per the research spec's own Expected Results framing ("the comparative value of this design is in the stratified breakdown ... rather than a single headline pooled number").

**Comparison structure:** Between-stratum comparisons are **subgroup meta-analyses with a formal moderator test** (Cochran's Q-between via a mixed-effects meta-regression with a categorical moderator, computed on the transformed proportion scale), **not** the "meta-regression on a paired effect size" the domain profile explicitly warns against (there is no paired effect size to regress). This is a standard, legitimate technique in prevalence meta-analysis (Cochrane Handbook prevalence chapter; Doi et al.) and should not be confused with regressing a comparative treatment effect on covariates.

**Where a genuine within-study comparator exists** (Krakhotkin, Leitner, PhagoBurn, and the three CF placebo trials, contingent on full-text confirmation), a paired RR/risk-difference is reported as a clearly-labeled **exploratory supplementary analysis**, never substituted for or blended into the primary stratified-proportions analysis, and never presented as a headline finding given n≤6 such studies.

---

## 2. Specification

### 2.1 Pooling Model

**Primary model — random-effects GLMM (binomial-normal), logit link.** For each stratum cell $s$ with studies $i = 1, \dots, k_s$:

$$
r_i \mid p_i \sim \text{Binomial}(n_i, p_i) \quad \text{(exact binomial likelihood, no continuity correction)}
$$
$$
\text{logit}(p_i) = \mu_s + u_i, \qquad u_i \sim N(0, \tau_s^2)
$$

The pooled proportion is $\hat{p}_s = \text{expit}(\hat{\mu}_s)$, with a 95% CI computed on the logit scale and back-transformed. **Justification for deviating from the domain profile's literal "double-arcsine primary" wording:** this literature spans n=1 case reports to n=100 cohorts (Pirnay). Schwarzer, Chemaitelly, Abu-Raddad & Rücker (2019, *Res Synth Methods*) show that double-arcsine back-transformation, which requires an arbitrary "typical" sample size (commonly the harmonic mean), can produce pooled point estimates that lie **outside the range of any observed study proportion** precisely when study sizes are this heterogeneous. The GLMM avoids this because it models the exact binomial likelihood at each study's own $n_i$ directly, with no transformation/back-transformation step and no continuity correction needed even at proportions of 0% or 100% (expected to be common here, e.g., Green et al.'s reported "13/15" or single-arm cohorts with zero adverse events). **This is a strategist decision, not a silent override — recommend the user approve updating `domain-profile.md`'s Common Identification Strategies table to reflect GLMM-logit as primary, double-arcsine as sensitivity** (the reverse of its current literal wording).

**Sensitivity models (Section 5):**
- Freeman-Tukey double-arcsine transformation, DerSimonian-Laird $\tau^2$ estimator, back-transformed via Miller (1978) using the stratum's harmonic mean $n$.
- Simple logit transformation with inverse-variance DerSimonian-Laird pooling (isolates the GLMM-vs-transformation contribution from the DL-vs-REML contribution).

**Fixed-effect model:** reported only as a supplementary sensitivity comparison (per research spec), never as the primary model — random-effects is essentially certain to be appropriate given the deliberate mixing of RCTs, prospective/retrospective cohorts, and case series with heterogeneous phage products, routes, and outcome definitions (Assumption 1, below).

**Small-stratum inference adjustment:** when a stratum has fewer than 10 studies (expected for most strata here), apply the Hartung-Knapp-Sidik-Jonkman (HKSJ) adjustment to the random-effects CI (IntHout, Ioannidis & Borm 2014) rather than a standard Wald-type CI, which is overconfident with few studies. If a stratum has only 2-3 studies, report the fixed-effect estimate alongside the (necessarily imprecise) random-effects estimate, with an explicit caveat rather than a falsely precise $\tau^2$.

**GLMM convergence contingency (addresses strategist-critic MAJOR #1):** binomial-normal GLMM estimated via numerical quadrature/integration has a real, well-documented risk of non-convergence in exactly the sparse/boundary-proportion regime this corpus will produce — many n=1 case reports with 0 or 1 events, and strata where every arm reports 0% or 100% of an outcome. This is not a hypothetical edge case here; it is the expected data structure (Green n=15-16, most case reports n=1, several strata with small k). Accordingly:
- **Per-cell convergence diagnostics are mandatory, not optional.** Every stratum-outcome cell's GLMM fit is checked for convergence (captured errors, known non-convergence warning strings, or non-finite pooled estimate/SE) and the result is logged, whether it converges or not (full implementation in `pseudo_code.md` §2, `pool_stratum()`).
- **Pre-specified fallback:** if GLMM fails to converge for a given cell, that cell's *reported* primary estimate is the logit-DerSimonian-Laird sensitivity model (already computed as Sensitivity 2, above) — never a silently-degraded GLMM output, and never left unreported. The substitution is cell-level only; GLMM remains primary wherever it converges.
- **Disclosure requirement:** any cell using the fallback carries an explicit table footnote naming the fallback and the reason (per INV-1), so a reader can immediately distinguish "GLMM, converged" cells from "fallback, GLMM did not converge" cells rather than treating the whole results table as uniformly GLMM-based.

**Non-independence of multiple arms from the same study (clustering analog):** where a single study contributes more than one arm to the *same* stratum-outcome cell (e.g., Krakhotkin's four arms, or Pirnay's multiple within-cohort routes), those arms are **not independent** (shared site, shared measurement protocol, shared investigators). Use robust variance estimation (RVE, via `clubSandwich`/`robumeta`) clustering by `study_id` when this occurs, rather than treating same-study arms as independent draws.

**Pseudo-code (R, `meta` + `metafor`):**
```r
library(meta)      # metaprop()
library(metafor)   # rma.glmm(), escalc()
library(clubSandwich) # RVE when same-study arms co-occur in a stratum

# --- one call per stratum cell (MDR x route x modality), e.g. success outcome ---
run_stratum_prop <- function(dat_stratum, event_col, n_col) {

  # Primary: GLMM (binomial-normal), logit link
  m_glmm <- metaprop(
    event   = dat_stratum[[event_col]],
    n       = dat_stratum[[n_col]],
    studlab = dat_stratum$study_arm_id,
    data    = dat_stratum,
    sm      = "PLOGIT",
    method  = "GLMM",         # binomial-normal random-effects model (Hamza et al. 2008)
    hakn    = TRUE,           # Hartung-Knapp-Sidik-Jonkman adjustment
    method.tau = "ML"
  )

  # Sensitivity 1: Freeman-Tukey double arcsine, DerSimonian-Laird
  m_ft <- metaprop(
    event = dat_stratum[[event_col]], n = dat_stratum[[n_col]],
    studlab = dat_stratum$study_arm_id, data = dat_stratum,
    sm = "PFT", method = "Inverse", method.tau = "DL", hakn = TRUE
  )

  # Sensitivity 2: simple logit, DerSimonian-Laird (isolates transformation vs. model choice;
  # also serves as the pre-specified fallback if m_glmm fails to converge — see pseudo_code.md §2)
  m_logit_dl <- metaprop(
    event = dat_stratum[[event_col]], n = dat_stratum[[n_col]],
    studlab = dat_stratum$study_arm_id, data = dat_stratum,
    sm = "PLOGIT", method = "Inverse", method.tau = "DL", hakn = TRUE
  )

  # Fixed-effect sensitivity
  m_fe <- metaprop(
    event = dat_stratum[[event_col]], n = dat_stratum[[n_col]],
    studlab = dat_stratum$study_arm_id, data = dat_stratum,
    sm = "PLOGIT", method = "Inverse", common = TRUE, random = FALSE
  )

  list(primary = m_glmm, ft = m_ft, logit_dl = m_logit_dl, fixed = m_fe)
}

# --- moderator test across strata (subgroup meta-analysis, NOT meta-regression on a paired effect) ---
m_full_by_stratum <- metaprop(
  event = dat_all$clinical_success_n, n = dat_all$n_arm,
  studlab = dat_all$study_arm_id, data = dat_all,
  sm = "PLOGIT", method = "GLMM", hakn = TRUE,
  subgroup = dat_all$resistance_class      # e.g. MDR vs XDR vs not-classifiable
)
# m_full_by_stratum$pval.Q.b.random gives the between-subgroup heterogeneity test (Cochran's Q-between)

# --- clustering correction when a study contributes >1 arm to the same stratum ---
# (applied post-hoc to check whether naive independence assumption changes CI width materially)
```

**Full convergence-contingency implementation (per-cell diagnostics + fallback logic) is specified in `quality_reports/strategy/phage_therapy_mdr_pseudomonas/pseudo_code.md`, Section 2 — the coder implements `pool_stratum()` exactly as written there, not the simplified illustrative version above.**

**Minimum-study/minimum-patient reporting threshold (pre-specified, ASSUMED — flagged for user confirmation):** a stratum-outcome cell is reported as a formal pooled estimate (point estimate + CI) only if it has **≥3 independent studies AND ≥20 pooled patients**. Below this threshold, report the individual study-level proportions narratively in a supplementary table, explicitly stating "insufficient data to support formal pooling" — do not report an unstable point estimate from 1-2 studies as though it were a stable finding. This threshold is a judgment call, not a fixed field convention; the user should confirm or adjust it before it is locked into the PROSPERO protocol (Section 8).

### 2.2 PICO → Extraction Form Mapping

**Unit of extraction:** study-arm/regimen (not study) — a study contributing four arms (e.g., Krakhotkin) contributes four rows.

**Extraction schema** (base: `data_dictionary.md` §1, refined here):

| Field | Type | Definition | Decision rule for ambiguity |
|---|---|---|---|
| `study_id` / `arm_id` | string | First author + year + arm letter | — |
| `n_arm` | integer | Denominator | — |
| `pathogen_scope` | categorical | Pseudomonas-only / mixed-with-PA-subgroup / mixed-not-separable | Mixed-not-separable arms are **excluded** |
| `resistance_class` | categorical | MDR / XDR / PDR / not-classifiable | See MDR/XDR decision rule below |
| `resistance_class_source` | categorical | independently-verified / author-reported | Always populated alongside `resistance_class` — never silently dropped |
| `route` | categorical | topical/local, IV, inhaled/nebulized, oral, intra-articular, other | Collapse to "other" only if <3 studies after full extraction (see §2.1 threshold) |
| `modality` | categorical | phage monotherapy / phage+antibiotic combination / antibiotic monotherapy | See Krakhotkin/Leitner note below |
| `clinical_success_n` / `_definition` | int / text | Numerator + verbatim study definition | Heterogeneous definitions tabulated per study, never assumed uniform |
| `adverse_event_n` | integer | ≥1 AE | Serious AEs extracted as a separate field where reported |
| `microbio_eradication_n`, `mortality_n`, `los_days`, `resistance_emergence_n` | — | Secondary outcomes | High expected missingness on `resistance_emergence_n`; do not impute |
| `study_design` | categorical | RCT / prospective cohort / retrospective cohort / case series / compassionate-use / case report | Feeds RoB tool selection (§4) |
| `data_provenance` | categorical (**new field**) | independently-extracted / cross-validated-against-Liu2025 / adopted-from-Liu2025-with-signoff | Mandatory — see §3 |
| `rob_source` | categorical (**new field**) | independently-rated / adopted-from-Liu2025-spot-checked / adopted-from-Liu2025-not-checked | Mandatory — see §4 |

**MDR vs. XDR classification decision rule (ambiguity-resolution ladder):**
1. If the study reports a full antibiogram/susceptibility panel sufficient to independently apply Magiorakos et al. (2012) criteria (non-susceptible to ≥1 agent in ≥3 of the defined antimicrobial categories = MDR; non-susceptible to all but ≤2 categories = XDR; non-susceptible to all tested agents in all categories = PDR) → code `resistance_class_source = "independently verified"`.
2. Else if the study explicitly labels the isolate/patient population "MDR" or "XDR" per its own stated criteria, without full raw susceptibility data → code `resistance_class_source = "author-reported"`, using the author's label as-is.
3. Else if partial susceptibility data are reported (some but not all Magiorakos categories tested) → apply an **asymmetric conservative rule**: classify as MDR if the reported data support non-susceptibility in ≥3 categories; do **not** upgrade to XDR unless the study explicitly documents susceptibility testing (not just omission) across enough categories to positively confirm ≤2-category susceptibility. Ambiguous cases are flagged for adjudication (dual-reviewer confirmation, or single-reviewer-plus-documented-rationale if dual extraction is not resourced — see the open resourcing question below).
4. If no classification information is given at all (no susceptibility data, no author label) → code `resistance_class = "not classifiable"`. **This is retained as its own explicit third stratification category, reported alongside MDR and XDR** — not silently dropped and not merged into either category — per the research spec's own suggestion, and consistent with PRISMA transparency (attrition should be visible, not invisible).

**Limitations note — XDR-shrinkage trade-off (MINOR, flagged by strategist-critic):** the asymmetric rule in step 3 is deliberately conservative in one direction only: it requires *positive confirmation* of susceptibility across enough categories to upgrade a case to XDR, but allows an MDR call from partial (incomplete-panel) data. This asymmetry is defensible — it prevents false XDR upgrades from missing-not-tested categories being mistaken for missing-because-resistant — but it has a mechanical consequence: the XDR stratum will be **systematically smaller** than it would be under a symmetric rule, because any partially-tested isolate that might plausibly be XDR defaults to MDR (or to "not classifiable") rather than XDR absent explicit confirmation. This is a trade-off between classification conservatism and XDR-stratum statistical power, not a design flaw — but it must be **named explicitly in the manuscript's Limitations section**, not left implicit, since a reader comparing this review's XDR proportion against another review's could otherwise misattribute a smaller/different XDR estimate to a clinical difference rather than to this classification-rule artifact.

**Krakhotkin/Leitner `modality` coding note:** Krakhotkin's Group IV ("furazidin+cefixime, no phage") is coded `antibiotic monotherapy` in the sense of "no phage," even though it is a two-drug antibiotic combination — flag this explicitly in a footnote so a reader does not assume "monotherapy" means single-antibiotic-agent. Leitner's antibiotic arm ("systemic antibiotics," no phage) is the cleanest true antibiotic-monotherapy arm in the entire corpus if a Pseudomonas subgroup is confirmed extractable.

**Dual independent extraction (open resourcing question, flagged not assumed):** the domain profile's Field Conventions specify dual independent extraction with documented conflict resolution. No discovery artifact documents whether this project has the personnel to do full dual extraction of every field for every study. **Recommend, at minimum, mandatory second-reviewer confirmation for: (a) every MDR/XDR classification call that falls under rule 3 above, and (b) every outcome-definition judgment call where a study's "success" definition is ambiguous.** If full dual extraction of all fields is not feasible given team size, this is a legitimate descoping the user should make explicitly (and disclose in Methods/Limitations), not something this memo assumes silently.

---

## 3. The Liu et al. (2025) Dataset Reuse Decision

**This is the single most consequential open decision flagged by both discovery agents (data_sources.md Part 2; explorer-critic Round 2, residual gap: "no explicit process for capturing/logging strategist+user sign-off before tier-(c) reuse").**

**Recommendation: adopt Tier 1 (scoping) + Tier 2 (independent cross-validation) as the default project policy. Do NOT adopt Tier 3 (direct adoption of codings) as a blanket policy — Tier 3 requires the user's explicit, per-instance sign-off, logged in a decision record, and is expected to be used rarely, only as a narrowly-scoped exception.**

### Tier 1 (Scoping) — Adopt without further sign-off; already yielding value
Use `mmc2.pdf`'s ~324-row table purely to identify which of Liu et al.'s ~130 included studies are `bacteria_species_target = "pa"` (*P. aeruginosa*)-tagged, and cross-reference this list against this project's own PubMed/CT.gov-derived study list. **This has already worked**: it surfaced Krakhotkin, Leitner, Karn, Rhoads, and Stanley — all previously uncatalogued by this project's own two independent librarian search rounds. This is standard, low-risk PRISMA practice (using a competing/prior review's reference list for citation-chasing is completely normal) and does not compromise the "independent systematic review" framing, since no outcome data is imported — only citation leads.

### Tier 2 (Independent Cross-Validation) — Adopt as default practice for all overlapping studies
For every study this project independently extracts from a primary source, and which also appears in `mmc2.pdf`, compare this project's independently-derived `clinical_success_n`, `bacteria_erad`, and `ad_event` codings against Liu et al.'s corresponding row. Any discrepancy is:
- Flagged, not silently reconciled.
- Resolved by **re-reading the primary source**, never by defaulting to Liu et al.'s value.
- Reported as a transparency/quality metric in the manuscript's Methods section (e.g., a percent-agreement or Cohen's kappa statistic across the overlapping study set) — this is a genuine, citable methodological strength ("we independently verified our extraction against a prior IPD meta-analysis's codings for N overlapping studies and found X% agreement"), directly analogous to this project's own precedent of catching two errors in Liu et al.'s source table (Krakhotkin misclassified as RCT; Stanley misattributed journal) — concrete evidence that Liu's table is not error-free and should never be treated as ground truth.

**Audit-loophole closure — documented-citation requirement (addresses strategist-critic MAJOR #2):** as originally specified, 100% cross-validation of overlapping studies cannot actually detect the failure mode it is meant to catch. A coder who simply copies Liu et al.'s value into this project's extraction sheet and labels the row `data_provenance = "independently-extracted"` will trivially "agree" with Liu's row on cross-validation, because the comparison is then a value against a copy of itself — not two independent extractions. Cross-validation alone is tautological in exactly the case it is supposed to guard against. To close this loophole:
- **Documented-citation requirement:** for a randomly drawn subsample (recommend 20%, or all studies if fewer than 15 overlap) of rows labeled `data_provenance = "independently-extracted"` that also appear in `mmc2.pdf`, the coder must additionally record the specific primary-source locator supporting the extracted value — a page number, table/figure number, or verbatim quote from the primary study (not from Liu et al.'s supplement) — in a new `extraction_citation` field.
- **Independent check:** this documented citation is verified by the coder-critic (or, if unavailable, a second human reviewer) against the actual primary-source PDF, confirming the cited page/table/quote genuinely supports the extracted value. A row that cannot produce a verifiable primary-source locator is re-flagged as `data_provenance = "cross-validated-against-Liu2025"` (or, if truly re-derived from Liu's table alone, escalated to the Tier 3 sign-off process below) rather than left mislabeled as independent.
- **Why this closes the gap:** a coder who copied Liu's value cannot, in general, produce a genuine independent page/table/quote locator from the *primary* source without actually having read it — this converts an easily-gameable label into a costly-to-fake evidentiary trail, and gives the coder-critic something concrete to audit rather than a self-referential agreement check.

### Tier 3 (Direct Adoption) — NOT the default; requires explicit per-instance user sign-off
Directly importing Liu et al.'s codings for overlapping studies, in place of independent extraction, is **not recommended as a blanket policy** because:
1. **Definitional mismatch risk.** Liu's `cli_impr`/`bacteria_erad` reflect *their* operational definitions of "clinical improvement"/"eradication," which the research spec explicitly anticipates will differ from this project's own pre-specified outcome definitions (heterogeneous "success" definitions across the primary literature is a named Open Question). Silently importing Liu's binary codings would launder that definitional heterogeneity rather than document it.
2. **Independence/framing risk.** This project's contribution rests on being an independent, MDR/XDR-*Pseudomonas*-specific stratified synthesis, differentiated from Liu et al. Wholesale adoption of Liu's case-level codings blurs the line between an independent review and an unacknowledged re-analysis of a prior team's IPD dataset — a distinction the explorer's own data-sources report explicitly flags as a line not to cross without sign-off.
3. **Demonstrated error risk.** This project's own verification work already caught two source-table errors in Liu et al. (Krakhotkin RCT misclassification; Stanley journal misattribution). Treating Liu's codings as ground truth would propagate any further, yet-undetected errors directly into this project's pooled estimates.
4. **Provenance/attribution risk.** A referee (per domain-profile's Field-Specific Referee Concerns) could reasonably ask whether outcome counts were independently verified or borrowed — Tier 3 use without disclosure is not defensible under any journal's authorship/data-integrity norms.

**Narrow exception (the only sanctioned Tier-3 use):** for a specific study where every access route in `access_instructions.md` has been exhausted and full-text extraction is confirmed infeasible (e.g., Nir-Paz/TP-102, or a specific case report unavailable through any channel), a per-study, per-instance Tier-3 use may be considered — **but only with**:
- An explicit `data_provenance = "adopted-from-Liu2025-with-signoff"` flag on that row (the mandatory field added to the extraction schema in §2.2).
- A dedicated decision-record entry in `quality_reports/decisions/` naming the specific study, the specific field(s) adopted, and the user's explicit approval — logged the same way the project has already logged its two prior design pivots.
- Explicit citation in the manuscript ("outcome count as reported in Liu et al. 2025's supplementary dataset, independently re-extraction not possible; not independently verified") rather than silent inclusion as though independently extracted.

**Action item before the coder builds the extraction spreadsheet:** present this recommendation to the user for sign-off (Tier 1+2 approved by default per this memo, including the documented-citation spot-check above; Tier 3 requires case-by-case approval) and set up the `data_provenance`/`extraction_citation` logging fields now, not retroactively.

---

## 4. Risk of Bias Approach

- **Comparative studies** (Krakhotkin 2025 [observational — **not** RCT, despite Liu et al.'s mis-tabulation], Leitner 2021 [RCT], PhagoBurn [RCT], the three-to-four CF placebo trials [RCTs]) → **ROBINS-I** for the non-randomized comparative study (Krakhotkin), **Cochrane RoB2** for the genuine RCTs.
- **Single-arm studies** (the large majority of the corpus: Pirnay, Green, Israeli PTC, most case reports) → **JBI Checklist for Case Series** (Munn et al., part of the JBI Manual for Evidence Synthesis) as the primary tool for case series/cohorts, since it is validated specifically for prevalence-type single-arm data and aligns methodologically with the proportion-meta-analysis approach used here. Use **Murad et al. (2018)** critical appraisal specifically for the smallest reports (n=1-3 patients), since several JBI case-series items (e.g., "consecutive/complete inclusion") are not meaningful at that scale.
- **Reuse of Liu et al.'s existing RoB assessments** (`mmc2.pdf` contains RoB2 for 9 RCTs, ROBINS-I for 2 comparative cohorts, and NHLBI/JBI for ~90 case series/reports, per the orchestrator's independent verification): apply the **same Tier-1/Tier-2 logic as Section 3** — use Liu's existing ratings as a starting point/cross-check, but do not adopt wholesale. Specifically:
  - Independently re-rate a minimum of a **20% random sample of the ~90 overlapping studies, or all studies falling within the three pre-specified strata (MDR/XDR × route × modality), whichever set is larger.**
  - For every re-rated study, record `rob_source = "independently rated"`; for studies whose Liu rating is adopted after this spot-check confirms agreement, record `rob_source = "adopted-from-Liu2025-spot-checked"`; do not use `"adopted-from-Liu2025-not-checked"` as a final status for any study included in the primary analysis — that status is a transitional/tracking flag only, to be resolved before the manuscript's synthesis stage.
  - For any study found via this project's own independent search (not in Liu's ~130 — e.g., candidates from the 201-PDF ad hoc screen) rate from scratch; there is no reuse question for these.
- **GRADE certainty rating**, per outcome and stratum: expect most strata to land at **"Very Low" certainty**, given the predominance of single-arm, non-randomized, small, salvage/referral-population evidence. State this expectation upfront in the Methods as a pre-committed, not a post-hoc-surprised, conclusion — this pre-commitment itself blunts a referee's "did you even look at study quality" objection (Section 7, Objection 2).
- **RoB-stratified sensitivity analysis** (does the pooled proportion differ between higher- and lower-RoB study designs) is itself part of the robustness plan — see §5, Priority 2.

---

## 5. Robustness Plan

Ordered most-threatening to least-threatening.

### Priority 1: Model/Assumption-Threatening
| # | Check | What It Tests | Implementation | Expected Result |
|---|---|---|---|---|
| 1 | Transformation/model choice | Whether GLMM-logit vs. double-arcsine vs. simple logit-DL materially changes the pooled point estimate/CI | Report all three side-by-side per stratum (pseudo-code §2.1) | Similar point estimates and overlapping CIs; if they diverge by >5-10 pp, report as a finding, not a footnote (Schwarzer et al. 2019 mechanism) |
| 2 | MDR/XDR classification sensitivity | Whether restricting to independently-verified classification (vs. including author-reported) changes stratum estimates | Re-run §2.1 model with `resistance_class_source == "independently verified"` only, compare to full sample | Directionally similar; large divergence flags the classification variable as fragile |
| 3 | Fixed- vs. random-effects | Whether the a priori random-effects choice matters in practice | Report FE alongside RE for every stratum (pseudo-code) | RE preferred throughout given expected heterogeneity; large FE/RE divergence itself documents heterogeneity magnitude |

### Priority 2: Design-Quality / Selection Sensitivity
| # | Check | What It Tests | Implementation | Expected Result |
|---|---|---|---|---|
| 4 | Study-design-stratified sensitivity | Whether RCT/prospective-cohort proportions differ from retrospective/compassionate-use case-series proportions | Subgroup by `study_design`, report Q-between | Compassionate-use/case-series strata likely show higher "success" than RCT strata — the selection-into-treatment mechanism (data_dictionary §4) predicts this directly |
| 5 | Geographic-concentration sensitivity | Whether the pooled estimate is driven by the two most accessible cohorts (Pirnay/Belgium, Israeli PTC) | Re-run §2.1 model excluding Belgium- and Israel-sourced arms, compare | If exclusion materially shifts the estimate, report explicitly per data_dictionary §5's external-validity flag |
| 6 | Leave-one-out | Influential-study robustness (esp. Pirnay, the largest single source at 49 Pseudomonas cases) | Drop each study, recompute pooled estimate; flag any study whose removal shifts the point estimate beyond the CI of the full-sample estimate | Stable estimates; Pirnay flagged for explicit reporting given its outsized weight regardless of outcome |

### Priority 3: Specification/Categorization Sensitivity
| # | Check | What It Tests | Implementation | Expected Result |
|---|---|---|---|---|
| 7 | Route-collapsing sensitivity | Whether fine-grained route categories are an artifact of granularity | Report both the full route taxonomy and a collapsed systemic (IV/oral) vs. local (topical/inhaled/intra-articular) 2-category version | Directionally consistent; large divergence flags route as a fragile stratifier |
| 8 | Liu-reuse-tier transparency check | Whether any Tier-3 "adopted" data points (if used at all, per §3) move the pooled estimate | Compare pooled estimate using only independently-extracted rows vs. all rows including any Tier-3 adoptions | Should be small if Tier-3 use is genuinely rare/narrow, per §3's design |

### Priority 4: Inference Robustness
| # | Check | What It Tests | Implementation | Expected Result |
|---|---|---|---|---|
| 9 | HKSJ vs. standard Wald CI | Whether small-stratum inference is overconfident | Compare CI widths under `hakn = TRUE` vs. `FALSE` | HKSJ CIs wider for small strata — report HKSJ as primary per §2.1 |
| 10 | Same-study multi-arm clustering | Whether treating same-study arms as independent understates variance | Compare naive vs. RVE-clustered (`clubSandwich`) CIs for strata where a study contributes >1 arm | RVE CIs modestly wider; report RVE as primary where applicable |

### Priority 5: Publication Bias and Minimum-Threshold Sensitivity
| # | Check | What It Tests | Implementation | Expected Result |
|---|---|---|---|---|
| 11 | Funnel plot + Egger's/Peters' test (proportion-adapted) | Small-study/publication-bias effects | Applied per stratum-outcome cell with ≥10 studies (pre-specified threshold) | Report even if null; do not skip silently for cells below 10 studies — state explicitly why (per Section 6, Objection 3) |
| 12 | Minimum-study-count threshold relaxation | Whether the pre-specified ≥3-studies/≥20-patients reporting threshold (§2.1) is itself consequential | Re-run with a relaxed threshold (≥2 studies/≥10 patients) as an appendix table, clearly labeled as below the pre-specified bar | Document but do not promote relaxed-threshold estimates to primary results |
| 13 | Monotherapy-stratum contingency application | Whether the pre-specified sparsity decision rule (Section on operationalization below) changes the paper's structure | Apply the decision rule (≥3 studies test) to the actual extracted monotherapy data once Krakhotkin/Leitner full text is obtained | Documented regardless of outcome — a "cannot pool" finding is itself a reportable result, not a null result to hide |
| 14 | Exclusión de estudios cuya única fuente es un resumen de congreso | Si la inclusión de evidencia solo comunicada en congresos mueve la proporción agrupada | Re-ejecutar cada celda estrato-desenlace excluyendo los estudios marcados `solo-resumen` en `data/raw/study_groups.csv` (3 estudios: posiciones 288, 888, 4039) | Se informa siempre, salga como salga; una diferencia apreciable con solo 3 estudios indicaría que la síntesis es frágil ante la fuente, no que los resúmenes sobren |

**Regla de unidad de inclusión (enmienda de protocolo, 2026-08-05):**

La unidad de inclusión es el **estudio**, no el informe. Un mismo ensayo llega a este pozo como ficha de registro, resúmenes de congreso y artículo: el BX004-A aporta **once informes** (un artículo en *Nature Communications*, seis resúmenes de congreso y cuatro fichas de registro). Extraer de más de uno duplicaría los mismos pacientes en el metaanálisis.

- Los informes se agrupan en estudios con `scripts/group_reports_into_studies.py`, que encadena NCT propio → NCT declarado dentro del resumen → atribución razonada y documentada → título normalizado. La columna `informe_para_extraer` designa una sola fuente por estudio, prefiriendo el artículo sobre el resumen y el resumen sobre la ficha.
- **Los resúmenes de congreso son elegibles.** Excluirlos de oficio introduciría sesgo de notificación justo donde esta revisión es más vulnerable: la fagoterapia es una terapia emergente cuya evidencia se comunica con frecuencia primero —o solo— en congresos, de modo que el material descartado no sería aleatorio.
- Cuando el resumen es un informe adicional de un estudio ya representado por un artículo, **no cuenta como estudio aparte**: se usa como fuente complementaria y para contrastar si los desenlaces comunicados en el congreso coinciden con los del artículo.
- Cuando el resumen es la **única** fuente del estudio, el estudio se incluye, se identifica como tal en la tabla de características, se somete a la comprobación #14 y su certeza se degrada por limitaciones de notificación en GRADE.
- Los estudios cuya única fuente es una **ficha de registro** (60 de 219) no entran en la síntesis: se listan como estudios en curso o sin resultados publicados, que es una categoría propia del diagrama PRISMA 2020 y un hallazgo en sí mismo sobre el estado del campo.

Reparto actual: **268 informes → 219 estudios**; 156 extraíbles, 60 solo-registro, 3 solo-resumen.

**Monotherapy-stratum decision rule (sparsity contingency, addressing research spec Open Question #5 directly):**
- **If** full-text retrieval confirms ≥3 studies with extractable *P. aeruginosa*-specific, arm-level antibiotic-monotherapy outcome counts (candidates: Krakhotkin Group IV, Leitner's antibiotic arm, plus any studies surfaced by pending EMBASE/WoS/Scopus searches) → pool as a formal fourth stratum using the identical §2.1 model, with an explicit caveat that this stratum's population (UTI/cystitis) differs from the invasive-infection population dominating the other strata, so side-by-side reporting (not causal comparison) is appropriate, **except** for the 1-3 genuine within-study comparators, which may additionally report a labeled exploratory RR (Section 1).
- **If** fewer than 3 studies qualify → do **not** report a pooled monotherapy proportion. Present the 1-2 available comparative studies (Krakhotkin, Leitner) narratively in a "landscape" table alongside the phage-containing strata, with the explicit statement: "insufficient comparative evidence exists to support formal pooling of an antibiotic-monotherapy-only stratum for MDR/XDR *P. aeruginosa* specifically" — this is itself a defensible, citable finding for a descriptive review, not a design failure requiring narrative workaround.

---

## 6. Falsification / Negative-Control Checks

Adapted from causal-inference falsification logic to evidence-synthesis: patterns that, if present without a plausible mechanistic explanation, would suggest the pooled proportions reflect artifacts (reporting drift, publication-standard changes, referral-pattern confounds) rather than a genuine, interpretable summary of the evidence.

1. **Publication year should not show a strong, unexplained monotonic trend in the pooled success proportion.** Pre-specify a meta-regression of the transformed proportion on publication year (as a continuous moderator, within the largest stratum with sufficient studies). Expect a null or weak coefficient. If a strong trend appears, investigate whether it is explained by a documented, legitimate mechanism (e.g., improving phage-purification/production technology described in the primary studies) before treating it as evidence of a real secular improvement — and flag as a red flag for reporting-standard drift if no such mechanism is found.
2. **Journal tier should not systematically predict the pooled outcome proportion**, absent a genuine quality-outcome relationship worth investigating. Split studies by journal tier (using the domain profile's own Target Journals ranking as a rough proxy, or a generic high/low-impact split) and compare pooled proportions. A strong tier gradient (higher-impact journals reporting systematically higher success) would itself be evidence of selective-reporting/severity-of-editorial-review distortion, not a clinical finding.
3. **Sample size (arm n) should not be strongly, mechanically correlated with a higher reported proportion** beyond what the funnel-plot/Egger's test (Section 5, #11) already checks — used here as a simple eyeball diagnostic (plot proportion vs. $1/\sqrt{n}$) alongside the formal test, since small-study effects in a mostly-single-arm literature can be easy to miss if only the formal test is reported.
4. **Route of administration should not be confounded with geographic/referral-center source in a way that masquerades as a route effect.** Before interpreting any route-stratum difference, cross-tabulate route × resistance-class × geographic source; if a route category is effectively a single-hospital signature (e.g., all intra-articular cases come from one center), the "route effect" is a center/case-mix effect, not a generalizable route effect — state this explicitly rather than implying a route-specific clinical mechanism.
5. **Length-of-hospitalization (a less phage-specific, more system-driven outcome) should not improve as dramatically as clinical success/eradication if the success signal is phage-specific rather than a general salvage-population reporting-optimism artifact.** If every outcome — including outcomes with no obvious direct phage mechanism — moves in the same "favorable" direction to a similar degree, that is suggestive of a uniform reporting/selection artifact rather than a phage-specific signal, and should be flagged in the Discussion as an interpretive caveat.
6. **Adverse-event proportions should not mechanically decline with publication year purely due to changing pharmacovigilance/reporting standards.** If newer studies (2024-2026) report systematically lower AE rates than older studies (2019-2021) with no documented change in AE ascertainment method, treat this as an underreporting-drift risk to disclose, not as evidence that phage therapy has become safer over time.

---

## 7. Threats

**Top 5 referee objections (per domain-profile's Field-Specific Referee Concerns) and pre-planned responses:**

1. **"Is the heterogeneity (clinical and statistical) too high to justify pooling at all?"**
   - **Response:** Random-effects model always used; I², τ², and prediction intervals reported for every pooled estimate (never a bare point estimate). The paper's headline contribution is explicitly framed as the **stratified breakdown**, not a single pooled number — the unstratified pooled-all estimate is reported only as secondary/contextual (§1). Pre-specify and report whether stratification reduces residual $\tau^2$ relative to the pooled-all model, as a formal internal check that the stratification variables are doing real explanatory work, not just adding complexity.

2. **"Was risk of bias assessed per study, and does it explain result heterogeneity?"**
   - **Response:** Per-study RoB via ROBINS-I/RoB2 (comparative) and JBI/Murad (single-arm) — Section 4. Design-quality-stratified sensitivity analysis (§5 Priority 2, #4) directly tests whether RCT/cohort proportions differ from case-series proportions. GRADE certainty rating reported per outcome/stratum, with the expectation of "Very Low" certainty for most strata stated upfront, not discovered as a surprise late in review.

3. **"Have you addressed publication bias / small-study effects — most phage therapy evidence is case series and case reports?"**
   - **Response:** Funnel plot + Egger's/Peters'-type test where ≥10 studies per stratum-outcome cell (§5 Priority 5, #11); explicit selection-into-treatment discussion citing the specific Belgian-magistral/Israeli-compassionate-use referral mechanisms (data_dictionary §4), not a generic "salvage bias" boilerplate; geographic-concentration sensitivity (§5 Priority 2, #5).

4. **"Does the pooled proportion generalize across *Pseudomonas* strains, phage cocktails, and administration routes, or is this an average of incomparable interventions?"**
   - **Response:** This is precisely why the design pre-specifies three stratification axes instead of reporting one number (§1, §2.1). Explicit Discussion language: the pooled estimate is conditional on route/modality/resistance-class, never presented as a single "efficacy" figure. Route-collapsing sensitivity (§5 Priority 3, #7) shows whether findings are an artifact of category granularity.

5. **"A pooled proportion of clinical success in a salvage-therapy population is not a causal effect — does the paper avoid overclaiming efficacy from what is fundamentally a descriptive/prevalence-style estimate?"**
   - **Response:** No causal verbs anywhere in the manuscript (per content-invariant INV-8) — "proportion of patients experiencing clinical success," never "phage therapy improved/caused/increased success." An explicit Discussion paragraph names the specific selection mechanism (compassionate-use, referral-gated access, no randomized/controlled comparator for the overwhelming majority of the corpus) as the reason a causal reading is unwarranted.

**Additional objections anticipated (beyond the top 5, briefly noted):**

6. **"Is the MDR/XDR classification defensible given how much of the primary literature reports 'MDR' without full susceptibility panel data?"** → Explicit `resistance_class_source` provenance field per arm; sensitivity analysis restricting to independently-verified-only classification (§5 Priority 1, #2); transparent "not classifiable" third category rather than silent exclusion (§2.2); the asymmetric-rule XDR-shrinkage trade-off named explicitly in Limitations (§2.2).

7. **"Are the pre-specified strata adequately powered, or is this multiple subgroup testing on too few studies per stratum?"** → This objection has two distinct parts, both addressed:
   - **Power/pre-specification:** Pre-specified minimum-study/minimum-patient thresholds (§2.1); explicit Discussion acknowledgment of underpowered strata (especially monotherapy); **all** pre-specified strata reported regardless of significance or null result — no post-hoc suppression of underwhelming strata.
   - **Multiplicity of testing (addresses strategist-critic MAJOR #4):** The design runs subgroup/moderator tests (Cochran's Q-between) across 4 outcomes × 3 stratification variables — up to 12 formal moderator tests, before counting the additional falsification/sensitivity checks in §5-6. No formal multiple-comparisons correction (e.g., Bonferroni, Benjamini-Hochberg) is applied, and this is a deliberate, disclosed choice rather than an oversight: per Cochrane Handbook convention (Ch. 10, subgroup analysis guidance), pre-specified subgroup analyses in a systematic review are treated as **hypothesis-generating rather than confirmatory**, since (a) the stratification variables were specified for substantive clinical reasons before data extraction (not chosen post hoc after seeing which splits looked significant), (b) the paper's headline claim is explicitly the *pattern* of stratified estimates and their overlapping/non-overlapping CIs, not a binary "is Q-between significant" verdict for any single test, and (c) formal correction would not meaningfully change the paper's interpretive stance, since Section 7's own framing already treats no single subgroup p-value as dispositive. The manuscript's Methods section states this reasoning explicitly (rather than silently omitting a multiplicity discussion), so a referee sees the choice was considered, not overlooked.

8. **"Was the search strategy sensitive enough (PubMed alone is not sufficient for a defensible PRISMA review)?"** → See Section 8: EMBASE/WoS/Scopus status disclosed explicitly in Methods/Limitations as user-pending, with a committed plan to re-run before submission, not silently omitted.

---

## 8. PRISMA / Registration Considerations

**Can PROSPERO registration still happen given three rounds of discovery-phase scoping have already occurred, including an ad hoc 201-PDF screening?**

**Yes — registration should happen now, and this is a genuine methodological question worth addressing explicitly, not glossing over.**

PROSPERO's own eligibility rule is that a protocol cannot be registered once **data extraction and synthesis are substantively underway or complete** — it explicitly does not prohibit having conducted preliminary scoping/feasibility searches beforehand. Virtually every systematic review conducts an informal scoping pass before writing a protocol, precisely to determine whether the PICO and eligibility criteria are viable to commit to in writing. That gate has clearly not been crossed here: no formal, systematic **dual-reviewer** extraction has begun; the discovery-phase work consists of (a) feasibility/design-pivot scoping (comparative-only design tested and rejected; proportions design adopted), (b) three rounds of literature-landscape mapping (positioning, frontier map, scooping-risk assessment), and (c) one **informal, single-reviewer, ad hoc** 201-PDF screening pass.

**The genuine risk to manage, honestly:** the researcher has already seen study-level result content during this scoping process (e.g., approximate success-rate figures for Green et al., Pirnay et al.), which creates a real, if modest, risk that protocol choices (stratification boundaries, outcome definitions, sparsity thresholds) could be quietly tuned toward a more favorable-looking result once registered — the evidence-synthesis analog of "looking at the data before pre-registering an RCT." This memo's response:

1. **Register now, before formal dual-reviewer extraction begins** — do not wait further, since delay only increases (not decreases) this risk.
2. **The registered protocol's eligibility criteria, outcome definitions, stratification plan, and sparsity/reporting thresholds must match this memo exactly** — this memo is written to serve as that locking document. Any subsequent deviation from what is registered should be logged as a documented protocol amendment (PROSPERO supports this), not a silent change.
3. **Explicitly disclose the discovery-phase scoping timeline in the protocol and eventual manuscript Methods** (search dates, the two design pivots, the informal 201-PDF pass) — PROSPERO's own template has fields for anticipated start date and preliminary search activity; transparency about what came before registration is the standard mitigation for this risk, not an admission of invalidity.
4. **Treat the ad hoc 201-PDF screening (12 INCLUIDO / 189 EXCLUIDO, 9 genuinely new candidates) as a Tier-1/Tier-2-equivalent scoping-and-cross-validation input, not a final answer.** It was conducted by a single reviewer using the project's own PICO criteria (a defensible, reproducible methodology per the research journal's description), but it predates protocol registration and did not use the dual-independent-reviewer process the domain profile's Field Conventions require. **Recommend it be re-screened (or, at minimum, independently spot-checked by a second reviewer) once the protocol is registered**, rather than its 12/189 disposition being carried forward wholesale into the formal PRISMA flow diagram as though it were the final screening pass. This mirrors exactly the reasoning applied to the Liu et al. dataset in Section 3 — a genuinely useful scoping tool, not a substitute for the formal, registered process.
5. **Re-check PROSPERO directly for competing protocols before finalizing registration.** The discovery-phase check was blocked (HTTP 403, JS/session-gated) and only an indirect web-search-mediated check was possible, which found no competing protocol matching this exact PICO — but this is a partial, not exhaustive, verification. A human with direct PROSPERO browser access should re-run this check as an action item before submission.
6. **Register the current (proportions) design, not the abandoned comparative-only design.** Given the project's own pivot history (comparative-only → proportions, logged in the decision record), it would be a genuine error to register a protocol describing the design that was already rejected for infeasibility — a mismatch a referee familiar with PROSPERO conventions could flag immediately.
7. **Name the GLMM-choice instance of this risk directly, not just the general category (addresses strategist-critic MAJOR #3).** The general disclosure in points 1-6 above covers the *category* of risk (protocol choices tuned after seeing scoping-phase data), but one specific design choice in this memo was itself justified using scoping-phase knowledge of concrete study sample sizes: §2.1's decision to make binomial-normal GLMM (rather than the domain profile's literal double-arcsine default) the primary pooling model was reasoned from already-observed sample-size heterogeneity across specific studies encountered during scoping — Pirnay et al. (n=49-100), Green et al. (n=15-16), and the numerous n=1 case reports. A sharp reviewer could reasonably ask whether the GLMM-primary choice was made *because of* what scoping had already revealed about this specific corpus, rather than being a design decision made independent of the data. This memo's position is that the choice remains defensible on its methodological merits regardless of when the sample-size heterogeneity was observed — the Schwarzer et al. (2019) failure mode is a property of double-arcsine back-transformation under wide sample-size ranges in general, not something invented post hoc to justify a favorable result, and the same choice would be recommended for any evidence base with this documented size structure. But the memo explicitly acknowledges that this is the sharpest, most consequential instance of the general scoping-timing risk named above, not a separate, unstated exception to it, and this instance should be named explicitly (not left implicit) in the registered protocol's own disclosure language and in the eventual manuscript's Methods/Limitations section.

**Action items, in order:** (a) finalize this memo's specification with the user; (b) submit the PROSPERO registration using this memo's exact eligibility/outcome/stratification language, including the explicit GLMM-choice disclosure in point 7 above; (c) begin formal dual-reviewer screening/extraction only after registration; (d) re-run or spot-check the informal 201-PDF screen against the registered criteria; (e) re-run the direct PROSPERO competing-protocol check once a human has browser access.

---

## Secondary Analyses

### Heterogeneity
- **MDR vs. XDR vs. not-classifiable:** justified by the research question's core stratification aim; also the variable most likely to carry classification-uncertainty risk (Section 7, Objection 6).
- **Route of administration:** justified by plausible pharmacokinetic/delivery differences (e.g., inhaled vs. IV phage exposure at the infection site); route-collapsing sensitivity (§5) checks robustness to category granularity.
- **Modality (monotherapy vs. combination):** the project's originally-intended comparative question, now operationalized as parallel proportions rather than a paired effect, with an explicit sparsity contingency plan (§5).
- **Study design (RCT/cohort/case series):** not one of the three pre-specified clinical strata, but a necessary risk-of-bias/selection moderator (§5 Priority 2), given the referral/compassionate-use selection mechanism documented in data_dictionary §4.

### Mechanism / Channel
- Not applicable in the causal-inference sense (this is a descriptive synthesis). The closest analog is the falsification check in Section 6, #5 (comparing clinical-success/eradication movement against a less-mechanistically-plausible outcome, length of hospitalization) as an internal-consistency check on whether the observed pattern is phage-specific or a general reporting artifact.
