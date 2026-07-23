# Access Instructions and Timeline Estimates

**Scope:** How to actually obtain each source graded in `data_sources.md`, and realistic timelines. Ordered by priority for the extraction stage.

**Revised 2026-07-18 (Round 2):** Adds the Liu et al. 2025 supplementary-dataset access route (a major upgrade from "not accessible"), and documents the additional BiomX SEC-filing/investor-relations check for the APT/BiomX rejection.

---

## Immediate (0 days — already accessible)

| Source | How to Access | Notes |
|---|---|---|
| Pirnay et al. (2024) | `https://pmc.ncbi.nlm.nih.gov/articles/PMC11153159/` (PMC full text) — also mirrored at ORBi (`orbi.uliege.be/handle/2268/319367`, CC-BY postprint PDF) and medRxiv (`2023.08.28.23294728`) | Use the PMC or ORBi version for citation; the medRxiv preprint should NOT be cited over the published Nature Microbiology version if numbers differ — cross-check. See `data_dictionary.md` §4 for a selection-into-treatment caveat before extracting/interpreting the pooled success rate. |
| Weiner et al. 2025 (BX004-A) | `https://www.nature.com/articles/s41467-025-60598-4` | Nature Communications is CC-BY by default; if the live site presents a login wall (bot-detection artifact observed in this search), retry via a direct browser session or Google Scholar cached PDF link — do not assume paywall from a single blocked fetch. Also retrieve the Author Correction, `s41467-026-70146-3`. |
| Green et al. 2023 (PASA16) | `https://www.cell.com/med/fulltext/S2666-6340(23)00225-8` | Confirmed directly accessible full text. |
| ClinicalTrials.gov structured results (Armata AP-PA02) | `https://clinicaltrials.gov/study/NCT04596319` → Results tab | Public, no login required. |
| PubMed/MEDLINE, ClinicalTrials.gov API | Already in use per `annotated_bibliography.md` Round 2 documented queries | No further action. |
| Israeli Phage Therapy Center compassionate-use report | PMID 37234511, Open Forum Infectious Diseases (fully OA journal) — `academic.oup.com/ofid/article/10/5/ofad221/7133195` | Newly identified in this pass; add to extraction queue as a candidate single-arm source, pending confirmation of a *Pseudomonas*-specific breakdown in the full text. See `data_dictionary.md` §4–5 for selection/external-validity caveats before treating the pooled 77.7% figure as a general population estimate. |
| **Liu et al. 2025 (IJAA) supplementary case-level dataset — NEW (Round 2)** | `https://ars.els-cdn.com/content/image/1-s2.0-S0924857925001256-mmc1.docx` (supplementary methods/PRISMA material, ~1.6 MB) and `https://ars.els-cdn.com/content/image/1-s2.0-S0924857925001256-mmc2.pdf` (**the case-level extraction dataset itself**, ~625 KB, ~324 rows across ~130 studies) | **Both files return HTTP 200 with no subscription or login required, even though the main article (`sciencedirect.com/science/article/abs/pii/S0924857925001256`, DOI 10.1016/j.ijantimicag.2025.107570) is paywalled.** This is a major, previously-missed shortcut — see `data_sources.md` Part 2 for full content description and reuse caveats. Action: download and review `mmc2.pdf` in full before the coder builds the extraction spreadsheet, to scope which of the ~130 included studies have *P. aeruginosa*-specific arms. Do not treat this as a substitute for independent extraction without the strategist's explicit sign-off (see reuse-tier discussion in `data_sources.md`). |

---

## Short Timeline (1–7 days — obtainable with modest effort, no institutional login needed)

| Source | Action Needed | Estimated Time |
|---|---|---|
| Jault et al. 2019 (PhagoBurn) | Download the ORBi author-postprint `.docx` (`orbi.uliege.be/handle/2268/231568`); if numbers in the postprint look preliminary/inconsistent with the published abstract, request the typeset PDF from a co-author or via interlibrary loan | 1–2 days |
| Confirm Green et al. 2023 author byline (Green vs. Onallah discrepancy) | Read the full text directly (already accessible, see above) and correct the bibliography entry if needed. Cross-check against Liu et al.'s `mmc2.pdf`, which cites "Onallah 2023" and "Green 2023" as apparently distinct references — resolve whether these are the same study before finalizing. | <1 day — should be done before the coder builds the extraction spreadsheet |
| Read Liu et al. `mmc1.docx` in full (supplementary methods/PRISMA material) | Not fully parsed in this pass — confirm it does not itself contain additional structured data (e.g., a study-characteristics table) beyond `mmc2.pdf` | <1 day |

---

## Medium Timeline (User's Institutional Access — 1–3 weeks, user-dependent, not blockable by this agent)

| Source | Action Needed | Estimated Time |
|---|---|---|
| Nir-Paz et al. 2025 (TP-102), *Med* | Access via user's institutional subscription (ScienceDirect/Cell Press) or interlibrary loan; low priority given no confirmed *Pseudomonas*/MDR subgroup in the abstract | 1–2 weeks if pursued at all — recommend deprioritizing unless the full text reveals a usable subgroup |
| Petrovic-Fabijan et al. 2020, *Nature Microbiology* | Institutional subscription or interlibrary loan | 1–2 weeks — low priority (background *S. aureus*, not core evidence) |
| Liu et al. 2025 (IJAA) main-text article | Institutional subscription (ScienceDirect/Elsevier) — **the supplementary case-level dataset is now confirmed accessible without this (see Immediate section above)**; institutional access to the main text is still worth obtaining for the narrative methods/discussion and any content not captured in the supplementary files | 1 week to obtain, now lower priority than before since the underlying dataset is already in hand |
| Uyttebroek et al. 2022, *Lancet Infect Dis* | Institutional subscription; check KU Leuven Lirias repository directly (not conclusively checked in this pass — worth a direct visit to `lirias.kuleuven.be`) | 1 week |
| El Haddad et al. 2019, *CID* | Institutional subscription (Oxford Academic) | 1 week |
| EMBASE | User's own institutional access — already in progress per research spec | User-dependent; re-run adapted Boolean queries already provided by the librarian |
| Web of Science / Scopus | User's own institutional access — already in progress per research spec | User-dependent; primary added value is citation-chasing the three anchor reviews |
| Cochrane Library / CENTRAL | User's own institutional access, if pursued — but see note below | Low priority: no dedicated Cochrane review exists on this topic, and CENTRAL's underlying trial records are already covered via PubMed + ClinicalTrials.gov |

---

## Author-Contact Track (2–6 weeks, standard systematic-review practice — not yet initiated)

Per the research spec's Open Questions (MDR/XDR reclassification risk, route granularity, monotherapy sparsity), the following author-contact requests are flagged as feasible for a future step (not undertaken here, per task scope):

| Study | Contact | What to Request | Feasibility |
|---|---|---|---|
| Pirnay et al. 2024 | Jean-Paul Pirnay (Queen Astrid Military Hospital) | *Pseudomonas*-specific subgroup breakdown (MDR/XDR, route, modality) if not resolvable from supplementary tables | High — active, responsive research group with a track record of consortium collaboration |
| Uyttebroek et al. 2022 / Pirnay 2024 (same consortium) | Willem-Jan Metsemakers / Jean-Paul Pirnay | Single combined request could cover both papers' unresolved subgroup questions | High |
| Nir-Paz et al. 2025 (TP-102) | Ran Nir-Paz (Hadassah) | *Pseudomonas*-specific subgroup within the pooled 3-pathogen results | Moderate-High |
| Jault et al. 2019 (PhagoBurn) | Patrick Jault / Pherecydes Pharma | MDR classification method for enrolled burn-wound infections | Moderate (older trial, commercial sponsor) |
| Weiner et al. 2025 (BX004-A) | BiomX (Merav Bassan) | Per-arm sample size split, MDR status of enrolled CF patients | Moderate (industry sponsor, proprietary data policies may limit response; note BiomX has since exited the phage-therapy space per recent SEC filings — see Not Currently Actionable section below — which may reduce responsiveness) |

**Recommended timeline for author contact:** Initiate only after full-text/supplementary-table extraction is complete and specific gaps are identified — do not contact authors speculatively before confirming what is genuinely missing from the published record (standard practice, reduces unnecessary correspondence).

---

## Not Currently Actionable (No Access Path Exists)

| Source | Why | Revisit When |
|---|---|---|
| Eliava Phage Therapy Center consolidated registry | Does not exist as a structured dataset | Would require direct institutional partnership/data-sharing agreement — out of scope for this review's timeline |
| Adaptive Phage Therapeutics / BiomX compassionate-use aggregate data | Not publicly published as a structured dataset. **Additional check performed this round:** BiomX's SEC filings (10-K/10-Q) and investor-relations materials (press releases, corporate presentations) were searched specifically, since this source category would be missed by a journal/OSF-focused search. Result: BiomX discloses only qualitative, promotional-context compassionate-use claims (e.g., "100s of compassionate use cases with no significant side effects"; anecdotal CF-patient CFU/FEV1% figures for ~11 patients) — not a structured, per-patient extractable dataset, and explicitly disclaimed as non-predictive in the filings themselves. Recent filings also indicate BiomX has discontinued its clinical-stage phage programs. | Low priority to revisit — company has exited the phage-therapy space; would require direct industry contact with a now-defunct program, low likelihood of response |
| ASM Phage Therapy Coordination Network registry | Not yet operational | Track ASM.org for launch announcement; likely a multi-year horizon |
| WHO ICTRP structured query | Portal not programmatically accessible in this environment | A user with direct browser access to `trialsearch.who.int` could manually re-run the search, or request the bulk XML data download from WHO — feasible but requires a human operator, not this agent |
| PROSPERO exhaustive database query | HTTP 403 on direct query | Same as above — requires a human operator with a standard browser session |
