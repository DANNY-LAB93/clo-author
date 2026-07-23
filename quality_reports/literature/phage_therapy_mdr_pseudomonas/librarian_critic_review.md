# Literature Review — librarian-critic
**Date:** 2026-07-18
**Phase:** Discovery (severity: encouraging/low, per quality.md — except where a critical feasibility finding requires undiluted scrutiny)
**Target:** `quality_reports/literature/phage_therapy_mdr_pseudomonas/`
**Score: 84/100**

## Verdict

**The headline feasibility finding holds up and is solid enough to escalate to the user now** — this is genuinely well-triangulated evidence, not a single-source claim. It does **not** need a full additional search round. It needs one narrow, cheap verification step (confirm the Liu et al. 2025 citation resolves) before the contribution statement in `positioning.md` is finalized around it. Recommend the escalation proceed per the librarian's own `ESCALATION_TARGET: User`, with that one caveat attached explicitly.

## Stress-Test of the Two Headline Claims

**Claim 1 — "no review since 2019" is false.** Robust. El Haddad (2019, CID, doi:10.1093/cid/ciy947) and Uyttebroek (2022, Lancet ID, doi:10.1016/S1473-3099(21)00612-5) both have complete, plausible bibliographic detail (full author lists, exact volume/pages, DOIs) and are **not** marked `% UNVERIFIED` — appropriately, since both are real, well-known papers matching known literature. This part of the claim rests on solid ground independent of the shakier Liu (2025) entry.

**Claim 2 — near-zero comparative studies for MDR *P. aeruginosa*.** The "0–1" count is corroborated by three independent lines of evidence (own search, El Haddad's own 9/30-no-comparator statistic, and two other reviews — Fatima & Hynes 2025, Yan 2026 — independently stating the same gap). That triangulation is a real methodological strength and raises confidence this isn't an artifact of an incomplete search. However:

- **No documented search strings for the negative claim.** Proving "zero comparative studies exist" requires showing what queries were actually run (e.g., "phage therapy Pseudomonas matched cohort," "propensity score," "registry," "retrospective comparative"). The bibliography shows citation-chasing through review reference lists and general web search, not targeted keyword searches for comparative-design terms. This is a legitimate gap in a negative-finding claim, even though it's partially offset by the triangulation above.
- **Registry search (ClinicalTrials.gov, WHO ICTRP) was done via generic web search, not the structured registry API** — self-disclosed in Limitations, but this is precisely the source most likely to surface an unpublished/recently-completed comparative trial that would overturn the "zero" count.

**Citation-verification discipline — one specific concern.** `Liu2025_ijaa` is correctly marked `% UNVERIFIED` in `references.bib` ("full author list beyond first six not confirmed; DOI and exact page range not independently confirmed... paywalled"). But this hedge does **not** propagate to where it matters most: the Executive Summary of `annotated_bibliography.md`, the "well-established" bullet in `frontier_map.md`, and the **draft contribution statement** in `positioning.md` all state the Liu et al. 2025 IPD meta-analysis (130 studies, through May 2025) as settled fact. This is the single highest-stakes citation in the whole packet — it's flagged as the top scooping risk and is central to both headline claims — yet its core existence (not just author-list completeness) has not been independently confirmed via a resolving DOI or direct fetch. Recommend one quick verification pass before the contribution statement quoted in `positioning.md` line 41 goes anywhere near a manuscript draft.

**Proximity scoring** — internally consistent (design-closeness as the operative axis: dual-arm RCT/trial = 2, single-arm case series = 3, reviews/mechanism = 4), and each assignment is individually justified in prose. No legend or explicit criteria for the 1–4 scale is stated anywhere before the section appears, which makes the scheme harder to audit at a glance (minor documentation gap, not an inconsistency).

**Source-access gap** — honestly disclosed (no EMBASE/Web of Science/Scopus; ClinicalTrials.gov/WHO ICTRP via web search, not API). This transparency is a genuine strength of the artifact and is exactly what should gate this from being treated as a final PRISMA-grade search — which the librarian itself says explicitly (`annotated_bibliography.md` Limitations; `positioning.md` option 5).

## Score Breakdown (librarian-critic rubric, Discovery-phase severity)

- Starting: 100
- Load-bearing citation (Liu 2025) marked unverified in .bib but stated as settled fact in prose driving the recommendation: **-5**
- No documented search strategy/query terms for the negative comparative-study claim: **-5**
- Registry search done via generic web search, not structured API, for a claim this consequential: **-3**
- No proximity-scale legend/criteria stated before the proximity table: **-2**
- "Six reviews since 2019" headline number lumps a preclinical-only review (Lancet Microbe) and a narrative-only review (Yan 2026) with true systematic reviews — caveated in-text but not in the headline count: **-2**
- **Not deducted (strengths):** recency (papers through 2026), journal quality (Lancet ID, CID, Nat Micro, Nat Comms, IJAA — no over-reliance on preprints), frontier map quality, internal consistency across all three memos, appropriate self-flagging of search-tool limitations, BibTeX completeness (no missing entries, no duplicate keys)
- **Final: 84/100**

Above the Discovery-phase commit gate (≥80). Coverage, recency, and scope calibration are strong; the deductions are concentrated entirely in citation-verification rigor and negative-claim documentation for the two claims that will drive a major pivot — exactly where scrutiny should be tightest even at "encouraging" severity.

## Files Reviewed
- `quality_reports/literature/phage_therapy_mdr_pseudomonas/annotated_bibliography.md`
- `quality_reports/literature/phage_therapy_mdr_pseudomonas/references.bib`
- `quality_reports/literature/phage_therapy_mdr_pseudomonas/frontier_map.md`
- `quality_reports/literature/phage_therapy_mdr_pseudomonas/positioning.md`
- `quality_reports/research_spec_phage_therapy_mdr_pseudomonas.md`
- `quality_reports/decisions/discovery_phage_therapy_mdr_pseudomonas.md`

---

## Round 3 Section — Five New Study Leads (Krakhotkin, Leitner, Karn, Rhoads, Stanley)

**Date:** 2026-07-18
**Phase:** Discovery (severity: encouraging/low per quality.md — with heightened scrutiny on the single most consequential claim)
**Target:** Round 3 addendum across `annotated_bibliography.md`, `references.bib`, `positioning.md`, `frontier_map.md`
**Score: 78/100** (below the 80 commit gate, narrowly)

### Verdict

Diligent, appropriately-hedged work that catches two genuine discrepancies in Liu et al.'s source table and does not overclaim any of the five leads. Deductions concentrate in process/documentation gaps, not wrong facts. Recommend one targeted fix-round, not a 3-strikes escalation.

### 1. Krakhotkin (2025), PMID 40314011 — plausible but under-verified for the highest-stakes claim

The observational-vs-RCT discrepancy is well-documented (verbatim quoted title). The 4-arm structure (antibiotic-only; phage-only; phage+furazidin; phage+furazidin+cefixime, n=178) is plausible. However, this was verified via secondary sources reporting the PubMed record, not a direct PubMed esummary/efetch call — a step down from this project's own Round 2 gold standard (used to upgrade Liu2025 from UNVERIFIED to FULLY VERIFIED). Recommend one direct PubMed esummary/efetch for PMID 40314011 before treating the 4-arm/n=178 description as settled.

### 2. Leitner (2021), Lancet ID — solid citation, but an unaddressed cross-round gap

The bibliographic core (PMID 32949500, 3-arm design, day-7 response 18%/28%/35%) is credible. But Round 2's own Query 4 already surfaced "Georgian Pyophage cocktail vs. placebo, PMID 30051571" and dismissed it as "already known to be out of scope" — without checking whether it was an earlier pilot report from the *same trial program* that later produced Leitner (2021). Same product, same site (Tbilisi/Eliava), same design family. This directly answers the "why wasn't this caught earlier" question: **a citation-chasing gap, not a keyword-search gap.** Recommend the librarian check whether PMID 30051571 is the same trial's earlier report, a protocol record, or a genuinely separate trial.

### 3. The two discrepancies caught — adequately specific, but rest on secondary sources

Both well-specified (Krakhotkin: verbatim title quote; Stanley: multiple secondary sources plus a conference-abstract precursor) but neither confirmed via a single authoritative primary fetch — a lighter standard than this project's own Round 2 gold standard. Trust provisionally; want one direct-fetch confirmation before either goes into a manuscript's Methods as a citable "we caught an error in a prior meta-analysis" point.

### 4. Rhoads (2009) rejection — holds on comparator logic, but inconsistently applied vs. Karn

Defensible on comparator grounds (saline, not antibiotics) but Karn (2024) has the *same* unresolved Pseudomonas-specificity uncertainty yet is scored "conditionally eligible." WPP-201 (Rhoads) targets *P. aeruginosa* specifically among its phage targets — under this project's proportions design (which explicitly accommodates single-arm data), a Pseudomonas-specific subgroup could still be extractable for a route-specific single-arm stratum. Worth a second look before finalizing exclusion.

### 5. Proximity scoring — internally inconsistent, contradicts the librarian's own prose ranking

Krakhotkin=3, Leitner=4, Karn=3, Rhoads=2, Stanley=4 — but the prose explicitly ranks Krakhotkin as "the most consequential finding for the project's central stratification variable" while calling Stanley "incremental." Yet Stanley scores *higher* than Krakhotkin. Direct proximity-vs-narrative contradiction. Recommend re-scoring Krakhotkin to at least tie with Leitner/Stanley, or justify the discrepancy explicitly.

### Score Breakdown
- Starting: 100
- Cross-round citation-chase gap (PMID 30051571 never reconciled with Leitner/PMID 32949500): **-8**
- Krakhotkin (2025) verified via secondary-source characterization, not direct PubMed fetch, for the single most consequential new claim: **-6**
- Proximity scores inconsistent with the librarian's own narrative importance ranking: **-5**
- Rhoads (2009) exclusion applied inconsistently relative to Karn (2024)'s identical epistemic uncertainty: **-3**
- **Not deducted (strengths):** two genuine, well-specified source-table discrepancies caught; no entry overclaims eligibility; proportionate positioning/frontier-map updates; complete BibTeX with granular verification-status notes
- **Final: 78/100**

### Commit-Gate Verdict
**Below the 80 commit gate, narrowly, for process/documentation reasons rather than substantive errors.** Recommend one targeted fix-round: (1) reconcile PMID 30051571 vs. Leitner's PMID 32949500; (2) direct PubMed esummary/efetch for Krakhotkin (PMID 40314011); (3) re-score or justify the Krakhotkin/Stanley proximity discrepancy.

---

## Round 3 Re-Review — Verification of Fix Pass

**Date:** 2026-07-19
**Phase:** Discovery (severity: encouraging/low per quality.md, with heightened scrutiny retained on citation-fabrication issues)
**Target:** Round 3 FIX PASS across `annotated_bibliography.md` and `references.bib` (Krakhotkin, Leitner, McCallin, Rhoads, Karn, Stanley entries)
**Score: 93/100**

### Verdict

All four items from the Round 3 review (score 78/100) are genuinely closed, not merely re-asserted. The fix pass is methodologically consistent with this project's own established gold standard (the Round 2 Liu2025 direct-esummary upgrade) and — notably — surfaced and transparently disclosed a citation-fabrication error the librarian itself introduced and then caught. This is exactly the behavior a critic wants to see. Clears the 80 commit gate comfortably.

### Item-by-item verification

**1. PMID 30051571 vs. Leitner's PMID 32949500 — CLOSED.** Verification method explicitly disclosed as a direct `esummary.fcgi?db=pubmed&id=30051571` call, run twice (original Round 3 pass + independent re-confirmation in the fix pass). Verdict — genuinely separate trial (McCallin et al. 2018, healthy *S. aureus* carriers, *Environmental Microbiology*) sharing only a product name and one investigator with Leitner — is specific and falsifiable. `McCallin2018_envmicrobiol` now exists in `references.bib` with a verification note citing the same PMID.

**2. Krakhotkin, PMID 40314011 — CLOSED, with one residual limitation.** Both `esummary` and `efetch` calls disclosed with structured-field-level detail (7-author byline, journal abbreviation, vol/issue/pages, dates, DOI, PMC ID, verbatim design language, n=178/four-group breakdown) — consistent across the bibliography entry, fix-pass section, and `.bib` note. Residual gap: no verbatim raw API transcript embedded (only paraphrased fields) — matches the standard already accepted for Liu2025 in Round 2, so lightly penalized only.

**3. Proximity re-score — CLOSED.** Krakhotkin now scored 4, tying Leitner (4) and Stanley (4), resolving the prior contradiction. Justification given is substantive (design-fit axis explicitly distinguished from narrative-importance axis).

**4. Rhoads/Karn consistency — CLOSED.** Both entries carry an explicit, mirrored justification: the differentiator is antibiotic-comparator structure (Karn: both arms have background antibiotics, structurally populates the stratification categories; Rhoads: saline-only, structurally cannot) — not the shared, non-differentiating Pseudomonas-specificity uncertainty.

**Fabrication correction (Leitner byline) — well-documented.** Two fabricated names ("Pantel, Kock"; "Kirss, Tanel A.") and two omitted real co-authors (Bachmann, Sybesma) disclosed with verification method stated (direct `esummary` on PMID 32949500). Transparently framed as an "unplanned finding" caught as a byproduct of the requested verification — a strength, demonstrating the verification discipline catches real errors, not just checks boxes.

### Residual issues (minor, non-blocking)
- Dual proximity-scale convention (Round 1-2's inverted scale vs. Round 3's standard scale) remains unreconciled across the whole document: **-4**
- No verbatim raw API transcripts embedded anywhere (consistent with prior accepted practice): **-3**

### Score Breakdown
- Starting: 100
- Proximity-scale duality still unresolved across rounds: **-4**
- No embedded raw API transcript (minor, consistent with prior accepted practice): **-3**
- **Final: 93/100**

### Commit-Gate Verdict
**PASS.** Clears both the 80 commit gate and the 90 PR gate. All four Round 3 deductions are substantively closed with specific, cross-checked, falsifiable evidence rather than re-assertion. Remaining items (proximity-scale unification, raw-transcript logging) are advisory, not blocking.
