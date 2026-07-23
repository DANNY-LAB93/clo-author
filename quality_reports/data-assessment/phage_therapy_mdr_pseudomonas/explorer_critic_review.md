# Data Assessment Review — explorer-critic
**Date:** 2026-07-18
**Severity:** Discovery (encouraging/low) — with targeted stress-testing of two headline claims per orchestrator instruction
**Artifact reviewed:** quality_reports/data-assessment/phage_therapy_mdr_pseudomonas/{data_sources.md, data_dictionary.md, access_instructions.md}
**Score: 57/100** (Round 1 — below the 80 commit gate)

## Headline Claim Stress Test

### Claim 1 — "Liu et al. (2025) has no reusable IPD dataset; extraction must be from scratch"
**Verdict: directionally plausible but under-verified.** The evidence base is (a) one blocked WebFetch to the ScienceDirect abstract page (HTTP 403), (b) a general web search for OSF/Zenodo/GitHub/Figshare mentions, (c) the PROSPERO record (which by design would not contain a dataset). The explorer appropriately hedges this ("should not be assumed... worth checking once full text is obtained") rather than stating it as settled fact — that hedging is good practice.

However, a 403 on the main-text URL is genuinely weak evidence of "no dataset." Two specific, low-cost alternate routes were not attempted and should have been, before publishing this as a headline finding:
- **Elsevier's supplementary-materials CDN pattern** (`ars.els-cdn.com/content/image/1-s2.0-{pii}-mmc1.{pdf,docx,xlsx}`) — Elsevier frequently hosts supplementary files openly even when the main article is paywalled. This was not tried.
- **A PMC linkout check** for PMID 40633848 (via NCBI's `elink.fcgi` or the PMC front end) — even though IJAA is a subscription journal, an NIH-funded co-author could trigger a PMC deposit. No PMC ID lookup is documented for this specific PMID.

Neither omission invalidates the claim, but it means "no reusable dataset" is currently a search-non-finding, not a verified negative.

### Claim 2 — "~86% of primary extraction-target studies are open/accessible; only 2 of 7 are confirmed paywalled"
**Verdict: does not hold up on a straightforward recount of the explorer's own table — this is the most important finding of this review.**

The Part 1 table itself grades the 7 studies as: Pirnay (A), Weiner (A), Green (A), Jault/PhagoBurn (B), Armata (B), Nir-Paz/TP-102 (C), Petrovic-Fabijan (C). That is **3 Grade-A, 2 Grade-B, 2 Grade-C** studies.

But the summary text states "4 confirmed openly accessible (A)," which is inconsistent with the table (only 3 A-rows), and this erroneous "4" is what produces the "86%" figure repeated in the Overall Feasibility Summary.

**Corrected arithmetic:** 3 A + 2 B = 5 of 7 = **71.4%**, not 86%. This does not overturn the qualitative takeaway (majority accessible, no institutional access strictly required for these 7), but the specific anchor number needs correction before downstream agents (strategist, coder) rely on it for resourcing/timeline planning.

## 5-Point Assessment (Grade A/B sources)

1. **Measurement validity — PARTIAL PASS.** `data_dictionary.md` correctly flags that Pirnay's headline statistics are cohort-wide (all 100 patients, all pathogens), not Pseudomonas-specific, and that Weiner's clinical-success extraction is low-confidence (safety-primary endpoint, n=9). Good nuance, but not cross-referenced from the headline "86%" claim — a reader skimming only the summary would not know "accessible" ≠ "contains the pre-specified stratified counts."
2. **Sample selection — GAP.** No discussion of who is included/excluded from the Pirnay (Belgian compassionate-use pathway) or Israeli Phage Therapy Center cohorts — both are almost certainly referral/salvage populations, a selection pattern specific to these sources and distinct from the research spec's generic salvage-therapy caveat.
3. **External validity — GAP.** No flag that the most "accessible" aggregate sources concentrate in two specific national programs (Belgium, Israel) with idiosyncratic regulatory pathways for phage access — a practical risk that the pooled estimate becomes disproportionately Belgium/Israel-weighted simply because that data is easiest to obtain.
4. **Identification/design compatibility — MOSTLY GOOD.** Part 3 of the data dictionary correctly separates "full-text accessible" from "contains fields needed for MDR-vs-XDR/route/modality stratification," and correctly predicts the monotherapy-only stratum may be unextractable from current sources. Not linked back to the "86%" headline, risking misreading in isolation.
5. **Known issues — INCONSISTENT COVERAGE.** Corrections/discrepancies checked for Weiner, Petrovic-Fabijan, Green — good diligence. No equivalent check for Pirnay et al. 2024 or the Israeli 5-year report, despite Pirnay being the single largest data source this project will lean on.

## Rejection Table Sanity Check

- Eliava, ASM Coordination Network, Cochrane, WHO ICTRP, PROSPERO — adequately justified. No concerns.
- Liu et al. 2025 supplementary IPD dataset — deserves a second look (Elsevier supplementary-CDN route and PMC linkout not attempted).
- Adaptive Phage Therapeutics / BiomX — thinly evidenced rejection. BiomX is publicly traded (NASDAQ: PHGE); SEC filings (10-K/10-Q) and investor-relations materials are a plausible public source of aggregate outcome disclosures not covered by a journal/OSF-focused search.

## Score Breakdown
- Starting: 100
- Headline "86%" accessibility figure is an arithmetic/count error, repeated in two locations, contradicting the explorer's own table (actual: 5/7 = 71%, not 6/7 = 86%): **-15**
- Liu et al. 2025 "no dataset" negative claim under-verified (PMC linkout and Elsevier supplementary-CDN route not attempted): **-10**
- No discussion of selection-into-treatment effects for the two "registry-like" aggregate sources (Pirnay, Israeli PTC): **-8**
- No discussion of external validity / geographic concentration (Belgium + Israel) among the most accessible sources: **-5**
- APT/BiomX rejection thinly evidenced (no SEC-filing/investor-material check): **-3**
- Known-issues/corrections check not performed for Pirnay et al. or Israeli PTC report specifically: **-2**
- **Final: 57/100**

## Recommendation
Below the 80 commit gate — one revision round needed, not an escalation. All flagged issues are concretely fixable. The underlying qualitative picture (majority of extraction targets accessible; no IPD shortcut exists) is likely still correct — the report's rigor, not its direction, needs work.

---

## Round 2 Re-Review

**Score: 89/100 — PASS (clears the 80 commit gate)**

Re-read all three revised files in full and cross-checked against the six Round 1 fix requirements (no independent web-fetch replication possible from this critic's tool grant — assessment based on internal consistency, specificity, and plausibility of documented content):

1. **Arithmetic** — Fixed. Corrected to 3/7 (43%) fully open, 5/7 (71%) accessible-with-effort, with an explicit "Correction (Round 2)" callout. Consistent across all summary locations.
2. **Liu et al. mmc2.pdf claim** — Elsevier supplementary-CDN route and PMC linkout documented as actually attempted, with specific HTTP status codes, file sizes, and a concrete, domain-plausible field list (`case_id`, `phage_route`, `phage_abx_co`, `cli_impr`, `bacteria_erad`, etc.). The three-tier reuse framing (scoping / cross-validation / direct-adoption, gated by explicit strategist+user sign-off before tier (c)) is an adequate safeguard against silent re-analysis of someone else's dataset. Residual concern: this remains a single-agent, self-reported PDF read with no independent-confirmation step specified before the coder/data-engineer relies on it.
3. **Selection-into-treatment** — Fixed, with source-specific mechanism (Belgian/Israeli referral pathways) correctly distinguished from the generic salvage-therapy caveat.
4. **External validity / geographic concentration** — Fixed, with a recommendation for stratified sensitivity analysis.
5. **APT/BiomX SEC-filing check** — Fixed, with quoted disclosures and BiomX's exit from the phage-therapy space noted.
6. **Known-issues/corrections check (Pirnay, Israeli PTC)** — Fixed, with null results honestly reported rather than omitted.

**Residual gaps (minor, non-blocking):** no documented mechanism for logging strategist/user sign-off before high-risk reuse of `mmc2.pdf`; Green-vs-Onallah authorship discrepancy remains unresolved (appropriately flagged as pending, not a blocker).

### Score Breakdown
- Starting: 100
- Liu et al. mmc2.pdf claim credible and well-caveated but remains an unverified single-agent read with no independent-confirmation step specified: **-8**
- No explicit process for capturing/logging strategist+user sign-off before tier-(c) reuse: **-3**
- **Final: 89/100**

### Verdict
**PASS.** All six Round 1 fixes substantively addressed, not cosmetically patched. Advisory (non-blocking): before the coder/data-engineer treats `mmc2.pdf` as ground truth for any cross-validation or scoping use, have a human or a second independent tool-call confirm the file's row count and field list directly.

---

## Independent Orchestrator Verification (2026-07-18)

Per the critic's advisory, the orchestrator independently fetched and read `mmc2.pdf` directly (not relying on the explorer's self-report). **Confirmed, first-hand:**
- The file is a genuine ~324-row case-level extraction table (rows 1-324, one per patient-case-episode), with exactly the field names the explorer reported (`case_id`, `report_id`, `reference`, `inf_site_main`, `bacteria_species_target` — including many rows tagged `pa` for *P. aeruginosa* — `phage_route`, `phage_composition`, `phage_abx_co`, `cli_impr`, `bacteria_erad`, `ad_event`, `phage_resis`, etc.), plus a full variable dictionary with value labels.
- The file contains substantially MORE than the explorer's report described: immune/PK/neutralization/antiphage-antibody "breakout" sheets, and — critically — **RoB2 risk-of-bias assessments for 9 named RCTs, ROBINS-I assessments for 2 comparative cohort studies, and NHLBI (case series) / JBI (case reports) quality-assessment checklists already completed for ~90 individual studies/cases.** This is a substantial, ready-made risk-of-bias resource this project can cross-check against rather than only reference for study identification.
- **New finding not previously caught by this project's own two librarian search rounds:** the RCT table (`RCT RoB2` sheet) lists **Krakhotkin et al. (2025), *Current Urology* 19(2):125-132** — "phage alone or plus antibiotics" vs. "antibiotics only," outcome ACSS questionnaire, with a stated result of "statistically significant improvements." This is a comparative study with a monotherapy-vs-combination structure directly relevant to this project's third stratification variable — not yet confirmed as *Pseudomonas*/MDR-specific, and not in this project's own `annotated_bibliography.md`. Also newly surfaced: Leitner et al. 2021 (Pyo vs. placebo/SOC), Karn et al. 2024, Rhoads et al. 2009 (WPP-201 vs. saline), Stanley et al. 2024 (YPT-01 vs. placebo, Journal of Cystic Fibrosis) — none previously catalogued by this project's librarian, all warranting a relevance check for *Pseudomonas*/MDR eligibility.

**Action item for next literature pass:** add Krakhotkin 2025, Leitner 2021, Karn 2024, Rhoads 2009, and Stanley 2024 to the librarian's screening queue and confirm/reject each for *Pseudomonas*-specific, MDR-relevant eligibility.
