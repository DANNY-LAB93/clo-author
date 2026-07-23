# Decision Record — Discovery: Eligibility Restricted to Comparative Studies Only

**Date:** 2026-07-18
**Stage:** Discovery
**Decided by:** User + discovery interview

---

## Decision

Systematic review/meta-analysis eligibility is restricted to **comparative studies only** — studies reporting both a phage+antibiotic arm and an antibiotic-monotherapy arm within the same study — for evaluating adjuvant phage therapy vs. antibiotic monotherapy in MDR *Pseudomonas aeruginosa* infections.

## Context

Most published phage therapy evidence consists of single-arm case series and case reports (compassionate-use/salvage therapy). During the discovery interview, the initial direction was to include single-arm series and compare them indirectly against monotherapy benchmarks drawn from other studies. The user reversed this decision mid-interview in favor of comparative-studies-only, after the assistant flagged that single-arm phage recipients are typically the most refractory/severe patients ("salvage therapy"), making an indirect between-study comparison to monotherapy highly vulnerable to confounding by indication.

## Alternatives Considered

| Alternative | Why rejected |
|-------------|-------------|
| Include single-arm case series/reports, compare indirectly against monotherapy benchmarks from separate studies | Severe confounding by indication: patients selected for compassionate-use phage therapy are systematically sicker/more refractory than typical monotherapy cohorts, making the comparison not credible as a causal estimate |
| Mixed design: comparative studies as primary analysis + single-arm studies in a sensitivity/narrative arm | Not selected for the initial specification — user chose the simpler, stricter comparative-only design. May be revisited if the comparative-study pool proves too small (see below) |

## Key Assumptions

1. A sufficient number of comparative (dual-arm) studies exists in the literature to support a meaningful meta-analysis — **not yet verified**, this is the central feasibility risk of the whole design.
2. Within comparative studies, treatment assignment (combination vs. monotherapy), while still non-randomized in most cases, is less severely confounded than a cross-study indirect comparison, because both arms are drawn from the same clinical setting/period.

## What Would Invalidate This

- If `/discover lit` and `/discover data` find too few comparative studies (e.g., fewer than ~5-10) to support a credible pooled estimate, this design must be revisited — either reverting to include single-arm studies with narrative synthesis, or pivoting the paper to a scoping review rather than a meta-analysis.
- If the comparative studies found are overwhelmingly small retrospective cohorts with severe residual confounding even within-study (e.g., informal/undocumented allocation to phage therapy), the identification claim underlying this design weakens and should be discussed as a explicit limitation rather than assumed away.

## Approved By

User, 2026-07-18

---

## Update (2026-07-18) — Both Assumptions Failed; Pivot Decision Pending EMBASE/WoS/Scopus Search

`/discover lit` (two rounds: web-search pass, then a documented PubMed E-Utilities + ClinicalTrials.gov API pass) confirmed **both** key assumptions above fail:
- Assumption 1 (comparative studies exist in sufficient volume) — **FAILED.** 0-1 qualifying studies found across two search rounds (54+10 records screened). See `quality_reports/literature/phage_therapy_mdr_pseudomonas/` for full detail.
- The companion "2019 cutoff" decision (below) also failed — see that section.

User was offered 4 pivot options (broaden pathogen/comparator scope; convert to scoping review; reframe contribution as the evidence gap itself; run EMBASE/Web of Science/Scopus personally first) and chose to **run EMBASE/Web of Science/Scopus themselves** before deciding — these three databases require institutional login this agent cannot access. Adapted Boolean queries (Embase Ovid syntax, Scopus TITLE-ABS-KEY syntax, Web of Science TS= syntax) were handed to the user, plus a request for forward-citation ("cited by") analysis on the three anchor papers (El Haddad 2019, Uyttebroek 2022, Liu et al. 2025) using Scopus/WoS's more complete citation graphs.

**Status: SUPERSEDED by the design pivot below.** The comparative-only design is abandoned; see the new decision record immediately following.

---

# Decision Record — Discovery: Pivot to Meta-Analysis of Proportions (MDR vs. XDR, Route, Monotherapy vs. Combination)

**Date:** 2026-07-18
**Stage:** Discovery
**Decided by:** User

## Decision

Abandon the comparative-effect (RR/OR of combination vs. monotherapy) meta-analysis design. Adopt instead a **systematic review with a meta-analysis of proportions** of clinical success and safety, with pre-specified stratification by (1) MDR vs. XDR, (2) route of phage administration, and (3) treatment modality (antibiotic monotherapy vs. phage-antibiotic combination).

## Context

`/discover lit` (two search rounds, PubMed E-Utilities + ClinicalTrials.gov API) confirmed the comparative-only design was infeasible: 0-1 qualifying dual-arm comparative studies exist for MDR *P. aeruginosa* specifically (see prior decision record, above). Rather than force a comparative effect size from too few studies, or fall back to a purely narrative scoping review, the user proposed reframing the design around **pooling proportions** — a design that uses the abundant single-arm evidence appropriately (as proportions per arm/regimen, not as one side of a forced comparison) while still producing a genuine quantitative synthesis with pre-specified, clinically meaningful stratification.

## Alternatives Considered

| Alternative | Why rejected |
|-------------|-------------|
| Keep comparative-only design, broaden pathogen scope to MDR Gram-negatives/ESKAPE | Would have diluted the *Pseudomonas*-specific focus that motivated the project; proportion meta-analysis achieves a usable sample size without changing the pathogen scope |
| Revert to a purely narrative scoping review (no pooling) | Discards quantifiable signal that a proportion meta-analysis can still extract from the single-arm literature; the user preferred a design that still produces pooled numeric estimates |
| Reframe contribution purely as "documenting the evidence gap" (no synthesis of outcomes at all) | Would not use the substantial single-arm evidence base that does exist; proportion meta-analysis is a more complete use of the available data |

## Key Assumptions

1. Enough single-arm and comparative studies exist, once stratified by MDR/XDR × route × modality, for each stratum to support a meaningful pooled estimate (not yet verified per-stratum — flagged in the research spec's Open Questions as a possible sparsity problem, especially for the monotherapy-only stratum).
2. Clinical success and safety definitions, though heterogeneous across primary studies, can be extracted and pooled with transformation methods (Freeman-Tukey/logit) that are standard for proportion meta-analysis under this kind of heterogeneity.
3. MDR/XDR classification can be meaningfully assigned per study (via Magiorakos et al. 2012 criteria or author-report) despite incomplete susceptibility panel reporting in much of the primary literature.

## What Would Invalidate This

- If, after data extraction, most strata (especially the monotherapy-only stratum) turn out to have too few studies/patients for a stable pooled estimate, the stratification plan may need to be simplified (fewer strata) or some strata dropped/merged.
- If full-text review of Liu et al. (2025, IJAA) or Uyttebroek et al. (2022, Lancet ID) reveals either already performs this exact MDR/XDR-stratified, *Pseudomonas*-specific proportion analysis, the contribution statement needs revision.
- If MDR/XDR classification proves un-derivable for a large fraction of studies (susceptibility data not reported), that stratification variable may need to be dropped or handled as "MDR/XDR not further classifiable" as its own category rather than excluded.

## Approved By

User, 2026-07-18

---

# Decision Record — Discovery: Search Date Range 2019–Present

**Date:** 2026-07-18
**Stage:** Discovery
**Decided by:** User

## Decision

The literature search will cover **2019 to present**, rather than the full historical period since modern phage therapy literature began, because — per the user — no systematic review or meta-analysis of phage therapy has been published since 2019.

## Context

During discovery, the user stated that no phage therapy systematic review/meta-analysis exists from 2019 to date. Rather than treat this as a claim to take at face value, the librarian is tasked (during `/discover lit`) with identifying the specific 2019 review, using it as the search-cutoff anchor and baseline for scope comparison.

## Alternatives Considered

| Alternative | Why rejected |
|-------------|-------------|
| Full historical search (inception to present) | Redundant with the 2019 review's presumed coverage, and substantially more effort; not selected given the user's stated intent to update rather than replicate prior synthesis |
| Search from an arbitrary earlier cutoff (e.g., 2015) "to be safe" | Not selected — user was specific about 2019 as the boundary |

## Key Assumptions

1. A systematic review/meta-analysis of phage therapy was in fact published in 2019 (not yet confirmed by name/citation) and adequately covered the literature up to that point.
2. No systematic review/meta-analysis has updated that synthesis since 2019 (user's stated belief, not yet independently verified).

## What Would Invalidate This

- If the librarian cannot locate a 2019 review matching this description, the 2019 cutoff assumption is unverified and the search range should default back to a full historical search to avoid a gap.
- If a review more recent than 2019 is found during the literature search, the contribution framing ("first update since 2019") and the search cutoff both need revision.

## Approved By

User, 2026-07-18
