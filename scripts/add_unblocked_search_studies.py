"""Add the four eligible arms recovered by the un-blocked PubMed search.

Both round-5 referees identified the search string, not database access, as the
binding constraint: every executed query required a resistance term in
title/abstract, while the Population criterion explicitly RETAINS arms with no
resistance documentation. The methods referee set a falsifiable bar -- "if the
un-blocked search yields <=2 new eligible studies, I will accept that the corpus
is near-complete and withdraw this comment."

Re-running PubMed as TITLE/ABSTRACT "Pseudomonas aeruginosa" AND phage-therapy
terms, restricted to case reports / clinical trials / observational studies and
2016-2026, returned 45 records. 17 were already traceable to the corpus. Of the
28 never screened, seven survived title/abstract screening as apparently
eligible; full-text screening then admitted FOUR and rejected three, each on a
rule this review already applies elsewhere.

ADMITTED

Casazza et al. 2025, Otol Neurotol 46:e117-e119 (PMID 39965256,
doi 10.1097/MAO.0000000000004417). 47-year-old woman, chronic mastoiditis from
MDR P. aeruginosa on a background of cystic fibrosis and lung-transplant
immunosuppression. Ten concurrent parenteral and intratympanic doses of two
custom phages, then IV antibiotics. The only one of the four additions that
achieved eradication: "subsequent cultures showed no growth" at five months.
Extracted from the structured abstract; no safety statement is made, so the
adverse-event numerator is left missing rather than set to zero.

Teney et al. 2024, Viruses 16:1080 (PMID 39066242, PMC11281479,
doi 10.3390/v16071080). 52-year-old man, 81% total-body-surface burns, four
successive episodes of ventilator-associated pneumonia with bacteraemia from an
NDM-1-producing XDR strain. Two 7-day courses of nebulised plus intravenous
phage 43 days apart, with imipenem-relebactam, inhaled colistin and
interferon-gamma. ERADICATION = 0 on the paper's own conclusion, verbatim:
"Although PAS did not result in microbial success, the clinical outcome was
favorable." Extubated on the last day of the second course and discharged after
203 ICU days.

Li et al. 2023, Microb Biotechnol 16:862-867 (PMID 36636832, PMC10034620,
doi 10.1111/1751-7915.14217). 40-year-old man, progressive interstitial lung
disease, pyomelanin-producing MDR strain resistant to all 100 dsDNA phages in
the library and treated with the dsRNA phage phiYY by nebuliser over three
courses. ADVERSE EVENT = 1: transient fever to 38.7C after every course, which
the authors attribute to phage-driven bacterial lysis or to the dsRNA phage
itself. This is only the second phage-attributable adverse event in the whole
corpus. ERADICATION = 0 -- the paper carries a section headed "reasons for the
failure to completely eradicate", and recurrences occurred 1-3 days after each
course.

Chen et al. 2022, Biosci Trends 16:158-162 (PMID 35444073,
doi 10.5582/bst.2022.01147). 68-year-old man, post-pneumonectomy empyema with
broncho-pleural fistula from carbapenem-resistant P. aeruginosa, treated with a
personalised two-phage preparation continuously for 24 days plus conventional
antibiotics, with clearance of the pathogen. RESISTANCE NOT CLASSIFIABLE: the
source states carbapenem resistance but publishes no full antibiogram and no
MDR/XDR/PDR label, so the conservative asymmetric rule retains the arm as
not-classifiable rather than upgrading it. Route is not reported in the source
available and is coded as such rather than inferred from the indication.

REJECTED, each under a rule already in force

Chung et al. 2026, Nat Commun 17:1385 (PMID 41513696, doi
10.1038/s41467-025-68136-y). The isolate was only INTERMEDIATE to ciprofloxacin
and remained susceptible to piperacillin-tazobactam, ceftazidime-avibactam and
meropenem; the authors label it "fluoroquinolone non-susceptible" and never
MDR/XDR/PDR. Non-susceptibility in one Magiorakos category, not three. Excluded
on the same ground as Liu 2025 Patient 1.

Ronit et al. 2024, Ugeskr Laeger 186:V09230617 (PMID 38305316,
doi 10.61409/V09230617). 82-year-old man, prosthetic aortic graft. Isolate
resistant to piperacillin-tazobactam and ceftazidime but SUSCEPTIBLE to
meropenem and ciprofloxacin -- two categories, not three. Excluded on the
antibiogram. The Queen Astrid Military Hospital co-authorship raised a
Pirnay-roster duplication question, which resolves independently: the phage was
given in 2023 and the roster closes on 30 April 2022.

Jennes et al. 2017, Crit Care 21:129 (PMID 28583189, PMC5460490,
doi 10.1186/s13054-017-1709-y). Eligible on population -- a colistin-only-
sensitive isolate is XDR -- and substantively valuable, being a fourth
phage-monotherapy arm and a death. Excluded as a PROBABLE PIRNAY-ROSTER
DUPLICATE. It is a Queen Astrid Military Hospital case treated with BFC1 in
November 2016, inside the roster's 1 January 2008 to 30 April 2022 window, with
Pirnay as senior author, and the roster states that 27 of its 100 cases were
published elsewhere. Roster case 13 matches on species, centre, product, route
and the wound-plus-bloodstream indication; the discrepancy is that case 13 is
recorded as surviving whereas this patient died four months after treatment,
which a shorter roster follow-up window would explain. Roster case 3, the only
other XDR death, is a respiratory infection treated by inhalation for four days
and is a different patient. Excluded for consistency with the treatment of Ferry
2022 and Racenis 2023, and added to the restore-both sensitivity analysis.
"""
import csv
import pathlib
import sys

root = pathlib.Path(__file__).resolve().parent.parent
csv_path = root / "metaanalisis" / "datos" / "phage_therapy_extraction_dataset.csv"

with csv_path.open(encoding="utf-8", newline="") as fh:
    reader = csv.DictReader(fh)
    fieldnames = reader.fieldnames
    rows = list(reader)

existing = {r["arm_id"] for r in rows}

PROV = ("Recovered by the round-5 un-blocked PubMed search (title/abstract "
        "'Pseudomonas aeruginosa' AND phage-therapy terms, clinical publication "
        "types, 2016-2026), run after both referees identified the resistance "
        "block in every previous query as the binding constraint. ")

new_rows = [
    {
        "study_id": "Casazza2025",
        "arm_id": "Casazza2025_A",
        "n_arm": "1",
        "pathogen_scope": "Pseudomonas-only",
        "resistance_class": "MDR",
        "resistance_class_source": "author-reported",
        "dtr_status": "not-derivable",
        "route": "other (multi-route: parenteral + intratympanic instillation)",
        "modality": "phage+antibiotic combination",
        "clinical_success_n": "1",
        "clinical_success_definition": (
            "47-year-old woman with chronic mastoiditis from MDR P. aeruginosa on a "
            "background of cystic-fibrosis ciliary dysfunction and lung-transplant "
            "immunosuppression. Success recorded as resolution of infection confirmed by "
            "symptomatology, cultures and imaging: at five months, resolution of otorrhoea, "
            "headache and hearing impairment"
        ),
        "adverse_event_n": "NA",
        "microbio_eradication_n": "1",
        "mortality_n": "0",
        "los_days": "NA",
        "resistance_emergence_n": "NA",
        "study_design": "case report",
        "data_provenance": "independently-extracted",
        "rob_source": "independently-rated",
        "publication_year": "2025",
        "journal_tier": "mid-tier (Otology & Neurotology)",
        "geographic_source": "USA (Dallas, UT Southwestern)",
        "extraction_citation": PROV + (
            "VERIFIED (2026-07-29) from the structured abstract, PMID 39965256, "
            "doi 10.1097/MAO.0000000000004417, Otol Neurotol 2025;46(4):e117-e119. Ten "
            "concurrent parenteral and intratympanic doses of two custom anti-Pseudomonas "
            "phages followed by IV antibiotic therapy. ERADICATION = 1 on the verbatim "
            "statement that subsequent cultures showed no growth -- the only one of the four "
            "round-5 additions to achieve it. ADVERSE EVENTS LEFT MISSING, not zero: the "
            "abstract makes no safety statement, and setting an unreported numerator to zero "
            "is the error this review criticises elsewhere. Full text not retrieved."
        ),
        "extraction_status": "PARTIAL",
        "incomplete_reason": (
            "Adverse-event count not reported in the available source. Length of stay and "
            "phage-resistance emergence not reported."
        ),
        "study_arm_id": "Casazza2025_A",
    },
    {
        "study_id": "Teney2024",
        "arm_id": "Teney2024_A",
        "n_arm": "1",
        "pathogen_scope": "Pseudomonas-only",
        "resistance_class": "XDR",
        "resistance_class_source": "author-reported",
        "dtr_status": "not-derivable",
        "route": "other (multi-route: nebulized + IV, concurrently)",
        "modality": "phage+antibiotic combination",
        "clinical_success_n": "1",
        "clinical_success_definition": (
            "52-year-old man with self-inflicted burns over 81% of total body surface area and "
            "four successive episodes of ventilator-associated pneumonia with bacteraemia from "
            "an NDM-1-producing XDR strain. Success recorded as reduced bronchorrhoea and "
            "oxygen dependence, improving skin grafts, extubation on the last day of the second "
            "phage course, and discharge from intensive care after 203 days"
        ),
        "adverse_event_n": "0",
        "microbio_eradication_n": "0",
        "mortality_n": "0",
        "los_days": "NA",
        "resistance_emergence_n": "0",
        "study_design": "case report",
        "data_provenance": "independently-extracted",
        "rob_source": "independently-rated",
        "publication_year": "2024",
        "journal_tier": "mid-tier (Viruses/MDPI)",
        "geographic_source": "France (Lyon, Hospices Civils; Phaxiam phages)",
        "extraction_citation": PROV + (
            "VERIFIED (2026-07-29) from PMC full text, PMID 39066242, PMC11281479, "
            "doi 10.3390/v16071080, Viruses 2024;16(7):1080, Section 2 and Conclusions. Phages "
            "PP1792 and PP1797 (Phaxiam), two 7-day courses 43 days apart, three inhaled doses "
            "plus daily IV injection per course, with imipenem-cilastatin-relebactam, inhaled "
            "colistin, later cefiderocol, and interferon-gamma. ERADICATION = 0 on the paper's "
            "own conclusion, verbatim: 'Although PAS did not result in microbial success, the "
            "clinical outcome was favorable.' A recurrence with the same strain occurred one "
            "month after the first course and a fourth episode after the second. ADVERSE EVENT "
            "= 0: no event attributable to phage therapy was recorded, stated for both courses, "
            "with liver and renal function tested twice weekly. PHAGE RESISTANCE = 0: a repeat "
            "phagogram showed the same susceptibility. NOT A DUPLICATE of Ferry 2021 or Ferry "
            "2022 despite shared Lyon authorship -- different indication (burn VAP versus "
            "prosthetic-joint and spondylodiscitis) and different phage source (Phaxiam versus "
            "Queen Astrid BFC1)."
        ),
        "extraction_status": "COMPLETE",
        "incomplete_reason": "Length of hospitalization not separately reported (203 ICU days is a stay, not a treatment LOS).",
        "study_arm_id": "Teney2024_A",
    },
    {
        "study_id": "Li2023_ILD",
        "arm_id": "Li2023_ILD_A",
        "n_arm": "1",
        "pathogen_scope": "Pseudomonas-only",
        "resistance_class": "MDR",
        "resistance_class_source": "author-reported",
        "dtr_status": "not-derivable",
        "route": "inhaled/nebulized",
        "modality": "phage+antibiotic combination",
        "clinical_success_n": "1",
        "clinical_success_definition": (
            "40-year-old man with progressive interstitial lung disease, type I respiratory "
            "failure and chronic infection by a pyomelanin-producing MDR strain resistant to "
            "all 100 dsDNA phages in the treating library. Success recorded as decreased cough, "
            "expectoration and dyspnoea, reduced bacterial burden, complete cessation of "
            "antibiotics, and discharge with relieved symptoms; lung transplantation six months "
            "later with no lung infection on follow-up"
        ),
        "adverse_event_n": "1",
        "microbio_eradication_n": "0",
        "mortality_n": "0",
        "los_days": "NA",
        "resistance_emergence_n": "0",
        "study_design": "case report",
        "data_provenance": "independently-extracted",
        "rob_source": "independently-rated",
        "publication_year": "2023",
        "journal_tier": "mid-tier (Microbial Biotechnology)",
        "geographic_source": "China (Shanghai Public Health Clinical Center)",
        "extraction_citation": PROV + (
            "VERIFIED (2026-07-29) from PMC full text, PMID 36636832, PMC10034620, "
            "doi 10.1111/1751-7915.14217, Microb Biotechnol 2023;16(4):862-867, Results and "
            "Discussion. First-in-human application of a double-stranded RNA phage: phiYY by "
            "vibrating-mesh nebuliser, three courses. ADVERSE EVENT = 1: transient fever to "
            "38.7C after every course, resolving with indomethacin, which the authors attribute "
            "to bacterial lysate released by phage progeny production or to an immune response "
            "to the dsRNA phage itself. This is the SECOND phage-attributable adverse event in "
            "the whole corpus, after Aslam 2020 Case 8. ERADICATION = 0: the paper carries a "
            "passage headed 'reasons for the failure to completely eradicate', and recurrences "
            "occurred 1-3 days after each course. PHAGE RESISTANCE = 0: every recurrent isolate "
            "remained susceptible to phiYY, which the authors state rules phage resistance out "
            "as the cause of persistence. DISTINCT from Li2025_biliary (hLife, biliary-tract "
            "infection) and from Liu2025_perinephric -- different patients, sites and centres."
        ),
        "extraction_status": "COMPLETE",
        "incomplete_reason": "Length of hospitalization not reported.",
        "study_arm_id": "Li2023_ILD_A",
    },
    {
        "study_id": "Chen2022_empyema",
        "arm_id": "Chen2022_empyema_A",
        "n_arm": "1",
        "pathogen_scope": "Pseudomonas-only",
        "resistance_class": "not-classifiable",
        "resistance_class_source": "not-classifiable",
        "dtr_status": "not-derivable",
        "route": "NA",
        "modality": "phage+antibiotic combination",
        "clinical_success_n": "1",
        "clinical_success_definition": (
            "68-year-old man with post-pneumonectomy empyema and broncho-pleural fistula from "
            "carbapenem-resistant P. aeruginosa. Success recorded as clearance of the pathogen "
            "and improvement of the clinical outcome"
        ),
        "adverse_event_n": "0",
        "microbio_eradication_n": "1",
        "mortality_n": "0",
        "los_days": "NA",
        "resistance_emergence_n": "NA",
        "study_design": "case report",
        "data_provenance": "independently-extracted",
        "rob_source": "independently-rated",
        "publication_year": "2022",
        "journal_tier": "mid-tier (BioScience Trends)",
        "geographic_source": "China (Shenzhen, Third People's Hospital)",
        "extraction_citation": PROV + (
            "VERIFIED (2026-07-29) from the published abstract, PMID 35444073, "
            "doi 10.5582/bst.2022.01147, Biosci Trends 2022;16(2):158-162. Personalised lytic "
            "two-phage preparation administered continuously for 24 days with conventional "
            "antibiotics. RESISTANCE NOT CLASSIFIABLE: the source states carbapenem resistance "
            "but publishes no full antibiogram and applies no MDR/XDR/PDR label. Carbapenem "
            "resistance alone is non-susceptibility in one Magiorakos category, so the arm is "
            "coded not-classifiable and RETAINED under the conservative asymmetric rule -- "
            "unlike Chung 2026 and Ronit 2024, whose published antibiograms positively "
            "establish susceptibility to most categories and which are therefore excluded. "
            "ROUTE NOT REPORTED in the available source and coded NA rather than inferred from "
            "the indication. ADVERSE EVENT = 0 on the statement that treatment was "
            "well-tolerated. ERADICATION = 1 on the statement of pathogen clearance. Full text "
            "behind a publisher paywall; the antibiogram would resolve the resistance coding "
            "and is recorded as an outstanding gap."
        ),
        "extraction_status": "PARTIAL",
        "incomplete_reason": (
            "Full antibiogram, route of administration, and length of stay not available from "
            "the abstract; full text paywalled. Resistance not classifiable in consequence."
        ),
        "study_arm_id": "Chen2022_empyema_A",
    },
]

for r in new_rows:
    if r["arm_id"] in existing:
        print("  already present, skipping: " + r["arm_id"])
        continue
    missing = set(fieldnames) - set(r)
    extra = set(r) - set(fieldnames)
    if missing or extra:
        print("SCHEMA MISMATCH for %s" % r["arm_id"])
        if missing:
            print("   missing: %s" % sorted(missing))
        if extra:
            print("   unknown: %s" % sorted(extra))
        sys.exit(1)
    rows.append(r)
    print("  added: %-24s %-18s erad=%s AE=%s"
          % (r["arm_id"], r["resistance_class"], r["microbio_eradication_n"], r["adverse_event_n"]))

with csv_path.open("w", encoding="utf-8", newline="") as fh:
    writer = csv.DictWriter(fh, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(rows)

print("")
print("extraction dataset now: %d arms across %d studies"
      % (len(rows), len({r["study_id"] for r in rows})))
