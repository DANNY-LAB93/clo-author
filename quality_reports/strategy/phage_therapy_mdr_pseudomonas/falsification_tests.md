# Falsification / Negative-Control Tests: Phage Therapy MDR/XDR *Pseudomonas aeruginosa* Meta-Analysis

**Companion to:** `quality_reports/strategy_memo_phage_therapy_mdr_pseudomonas.md` §6
**Purpose:** For a descriptive/measurement design, "falsification tests" are patterns that should NOT appear absent a documented, plausible mechanism — their presence without explanation signals artifact (reporting drift, selection/referral confounding, publication-standard changes) rather than a genuine, interpretable summary of the evidence.

## Test 1 — Publication-Year Trend
**Should NOT show:** a strong, unexplained monotonic increase in pooled clinical-success proportion over calendar time.
**Implementation:** meta-regression of the transformed proportion on publication year (continuous moderator), within the largest sufficiently-populated stratum.
**Interpretation:** null/weak coefficient expected. A strong trend requires a documented mechanism (e.g., improving phage-production/purification technology explicitly described in primary studies) before being treated as a real secular improvement; otherwise, flag as reporting-standard drift.

## Test 2 — Journal-Tier Gradient
**Should NOT show:** systematically higher pooled success proportions in higher-impact-tier journals absent a genuine quality-outcome relationship.
**Implementation:** subgroup by journal tier (domain-profile Target Journals ranking as proxy, or generic high/low split); compare pooled proportions and run Q-between.
**Interpretation:** a strong tier gradient signals selective-reporting/editorial-severity distortion, not a clinical finding.

## Test 3 — Small-Study/Sample-Size Effect (Eyeball Check)
**Should NOT show:** small arms (n<10) reporting systematically higher success than large arms beyond what the formal funnel/Egger's test already captures.
**Implementation:** plot proportion vs. 1/sqrt(n) per stratum, alongside the formal Priority-5 test.
**Interpretation:** used as a simple visual cross-check since small-study effects in a mostly-single-arm literature can be missed by a single formal test alone.

## Test 4 — Route × Resistance-Class × Geographic-Source Confounding
**Should NOT show:** an apparent "route effect" that is actually a single-hospital or single-country signature.
**Implementation:** cross-tabulate route × resistance_class × geographic_source before interpreting any route-stratum difference.
**Interpretation:** if a route category is effectively one center's case mix, state explicitly that the pattern is a center/case-mix effect, not a generalizable route effect.

## Test 5 — Non-Mechanistic Outcome Comparison (Length of Hospitalization)
**Should NOT show:** length-of-hospitalization improving as dramatically as clinical success/eradication, if the success signal is genuinely phage-specific rather than a uniform salvage-population reporting-optimism artifact.
**Implementation:** pool LOS-improvement proportion (or a directional summary given LOS is often reported as median/IQR, not a proportion) using the same stratification, compare direction/magnitude qualitatively against the clinical-success pooled estimate.
**Interpretation:** if every outcome — including outcomes with no obvious direct phage mechanism — moves favorably to a similar degree, that suggests a uniform reporting/selection artifact, not a phage-specific effect; disclose as an interpretive caveat in Discussion.

## Test 6 — Adverse-Event Rate Drift by Publication Year
**Should NOT show:** AE proportions mechanically declining with publication year absent a documented change in AE ascertainment method.
**Implementation:** meta-regression of AE proportion on publication year, same method as Test 1.
**Interpretation:** apparent "improving safety over time" with no ascertainment-method change documented is an underreporting-drift risk to disclose, not evidence phage therapy has become safer.

---

## Validation Tests (Descriptive-Design Analog to Causal Falsification, per Skill Workflow)

Since this is a descriptive/measurement design, the skill's validation-plan concept applies alongside falsification:

- **Internal validation:** every pooled proportion must respect [0,1] bounds after back-transformation (sanity check on the GLMM/double-arcsine back-transform); I²/τ²/prediction interval always reported together, never a bare point estimate (per domain-profile Notation Conventions).
- **External validation:** compare this project's pooled-all (secondary/contextual) estimate against the headline figures reported in Liu et al. (2025), Uyttebroek et al. (2022), and El Haddad et al. (2019) — expect broad directional agreement (all report high single-arm "success" rates); large divergence would itself require explanation (different eligibility criteria, different outcome definitions) before being reported as a novel finding.
- **Known-group validity:** the RCT-only subgroup (PhagoBurn, Leitner, CF placebo trials, pending Krakhotkin/Karn/Stanley confirmation) should show a *different* (generally more modest, or even null/negative, per PhagoBurn and Leitner's actual results) pooled proportion than the compassionate-use/case-series subgroup — this is a known-group check the design should reproduce given the documented selection-into-treatment mechanism; failure to see this divergence would itself be worth investigating.
