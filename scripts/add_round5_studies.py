"""Add the three study-arms recovered by the round-5 referee-prompted search.

Both round-5 referees said the search was under-sensitive by construction: every
executed query required a resistance keyword in title/abstract, while the
eligibility criteria explicitly retain arms with no resistance documentation at
all. A targeted PubMed search of the four studies the domain referee named
confirms the criticism -- two of the four are eligible and were missed, and
neither carries an MDR/XDR/PDR term in its title or abstract.

WHAT IS ADDED, and why each survives screening.

Zaldastanishvili et al. 2021, Viruses 13:1901 (PMID 34696331, PMC8540005,
doi 10.3390/v13101901). Three patients at the Eliava Phage Therapy Center,
Tbilisi; two are P. aeruginosa (the third is Klebsiella and is not entered).
These are the review's second and third PHAGE-MONOTHERAPY arms: both patients
came to EPTC explicitly to replace antibiotics with phages, and both did.
Patient 1 took antibiotics once in three years, during an intercurrent viral
illness; Patient 2 refused antibiotic therapy outright. Neither achieved
eradication -- the paper exists to report bacterial persistence, and its
Discussion states verbatim that "long-term total bacterial clearance was not
achieved in any of the discussed cases". Both are coded eradication = 0 on that
sentence, not on inference.

Green et al. 2023, Clin Infect Dis 77:1079-1091 (PMID 37279523, PMC10573729,
doi 10.1093/cid/ciad335). Twelve expanded-access customized phage cases from
Baylor's TAILOR production centre; exactly one is P. aeruginosa (Case 11, LVAD
driveline). Separable per-case, so entered as a single arm.

DE-DUPLICATION AGAINST Aslam2020_C5 AND _C8. Both existing arms are ventricular
assist device infections with P. aeruginosa treated with phage, so the match had
to be adjudicated rather than assumed. It fails on four independent fields:
phage identity (Green Case 11 used phages 6917 and 6959 from Baylor TAILOR; C5
used GD-1; C8 used SDSU1/SDSU2, then PAK_P1, then PPM3), regulatory record
(Green Case 11 is IND 27807; the Aslam cases carry no matching IND), dosing
schedule (Green q12h IV for 6 weeks plus a single intraoperative dose; C5 q8h IV
for 6 weeks with no intraoperative dose), and -- decisively -- chronology: Green
Case 11's outcome text records the patient off antibiotics "since May 2022",
which cannot describe a case published in September 2020. The outcomes also run
opposite: Green Case 11 improved clinically, while C5 and C8 are both recorded
"Outcome: Failure" verbatim.

WHAT IS NOT ADDED.

Onsea et al. 2019, Viruses 11:891 (PMID 31548497, doi 10.3390/v11100891). Four
musculoskeletal infections at Leuven with QAMH's BFC1 cocktail. Patient 2 did
carry an XDR P. aeruginosa, but the paper states that organism was NON-
SUSCEPTIBLE to the anti-Pseudomonas phages in the cocktail (PNM, 14-1); the team
proceeded because the co-infecting Staphylococcus was susceptible. Phage was
administered to the patient but was not active against the P. aeruginosa, so the
arm does not measure phage therapy against this review's target organism. It is
additionally a QAMH/Belgian case with Pirnay as a co-author, i.e. the exact
profile of the consortium roster this review already de-duplicates against.
Recorded as a full-text exclusion.

"Doub 2023" does not exist as a distinct clinical study. PubMed returns four
Doub-authored records mentioning Pseudomonas: the Arya 2026 prosthetic-joint
case already in this corpus (Doub is a co-author), an in-vitro wound-vacuum
biofilm study, and two others, none of them an eligible clinical report.
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

ZALD_CITE = (
    "VERIFIED (2026-07-29) from PMC full text, PMID 34696331, PMC8540005, "
    "doi 10.3390/v13101901, Viruses 2021;13(10):1901, Sections 3.1-3.2 and 4. "
    "Recovered by a round-5 referee-prompted PubMed search after both referees "
    "identified the search string as under-sensitive by construction: every "
    "executed query required a resistance keyword, and this paper's title and "
    "abstract carry none. Three patients are reported; two are P. aeruginosa "
    "and are entered separately, the third (Klebsiella UTI) is out of scope. "
    "ERADICATION = 0 for both on the Discussion's verbatim statement that "
    "'long-term total bacterial clearance was not achieved in any of the "
    "discussed cases' -- coded on the source's own summary, not inferred from "
    "the case narratives. RESISTANCE NOT CLASSIFIABLE: the paper documents "
    "years of failing antibiotic therapy but publishes no antibiogram and no "
    "MDR/XDR/PDR label, so the conservative asymmetric rule applies. "
    "PHAGE RESISTANCE EMERGED in both patients and is documented by PFGE and "
    "spot-test across serial isolates."
)

new_rows = [
    {
        "study_id": "Zaldastanishvili2021",
        "arm_id": "Zaldastanishvili2021_P1",
        "n_arm": "1",
        "pathogen_scope": "mixed-pathogen-with-Pseudomonas-subgroup",
        "resistance_class": "not-classifiable",
        "resistance_class_source": "not-classifiable",
        "dtr_status": "not-derivable",
        "route": "other (multi-route: oral and nebulized/inhaled, concurrently)",
        "modality": "phage monotherapy",
        "clinical_success_n": "1",
        "clinical_success_definition": (
            "43-year-old male with cystic fibrosis and chronic P. aeruginosa lower "
            "respiratory tract infection managed with IV antibiotics since childhood. "
            "Success is recorded as replacement of antibiotics by phages with subjective "
            "symptom alleviation and a 10- to 100-fold reduction in sputum bacterial load; "
            "the organism was never absent from any sputum culture over 2017-2020"
        ),
        "adverse_event_n": "0",
        "microbio_eradication_n": "0",
        "mortality_n": "0",
        "los_days": "NA",
        "resistance_emergence_n": "1",
        "study_design": "case series",
        "data_provenance": "independently-extracted",
        "rob_source": "independently-rated",
        "publication_year": "2021",
        "journal_tier": "mid-tier (Viruses/MDPI)",
        "geographic_source": "Georgia (Tbilisi, Eliava Phage Therapy Center)",
        "extraction_citation": ZALD_CITE + " PATIENT 1: Pyo and Intesti Bacteriophage "
                               "orally and by nebuliser from Jan 2017, then two successive "
                               "custom phages (Apr 2019, Oct 2019) by nebuliser. Took "
                               "antibiotics once in the whole period, during an intercurrent "
                               "viral illness, so coded phage monotherapy.",
        "extraction_status": "COMPLETE",
        "incomplete_reason": (
            "Resistance not classifiable: no antibiogram and no MDR/XDR/PDR label published. "
            "Length of stay not reported (outpatient/telemedicine model)."
        ),
        "study_arm_id": "Zaldastanishvili2021_P1",
    },
    {
        "study_id": "Zaldastanishvili2021",
        "arm_id": "Zaldastanishvili2021_P2",
        "n_arm": "1",
        "pathogen_scope": "mixed-pathogen-with-Pseudomonas-subgroup",
        "resistance_class": "not-classifiable",
        "resistance_class_source": "not-classifiable",
        "dtr_status": "not-derivable",
        "route": "other (oral administration only; nebuliser not tolerated)",
        "modality": "phage monotherapy",
        "clinical_success_n": "1",
        "clinical_success_definition": (
            "64-year-old female with primary ciliary dyskinesia and bronchiectasis who "
            "refused antibiotic therapy options. Success is recorded as management of the "
            "infection with phages alone across five successive custom preparations "
            "(2018-2021) with subjective symptom alleviation and no adverse effects"
        ),
        "adverse_event_n": "0",
        "microbio_eradication_n": "0",
        "mortality_n": "0",
        "los_days": "NA",
        "resistance_emergence_n": "1",
        "study_design": "case series",
        "data_provenance": "independently-extracted",
        "rob_source": "independently-rated",
        "publication_year": "2021",
        "journal_tier": "mid-tier (Viruses/MDPI)",
        "geographic_source": "Georgia (Tbilisi, Eliava Phage Therapy Center)",
        "extraction_citation": ZALD_CITE + " PATIENT 2: strain resistant to Pyo and Intesti "
                               "from the first culture, so five successive custom phages were "
                               "used orally (Sep 2018 onward). ERADICATION CODED 0 DESPITE a "
                               "single negative sputum culture in late July 2021: the paper "
                               "reports that result as arriving shortly before submission and "
                               "its Discussion still states clearance was not achieved in any "
                               "case. Coding it as eradication would contradict the source.",
        "extraction_status": "COMPLETE",
        "incomplete_reason": (
            "Resistance not classifiable: no antibiogram and no MDR/XDR/PDR label published. "
            "Length of stay not reported."
        ),
        "study_arm_id": "Zaldastanishvili2021_P2",
    },
    {
        "study_id": "Green2023",
        "arm_id": "Green2023_C11",
        "n_arm": "1",
        "pathogen_scope": "mixed-pathogen-with-Pseudomonas-subgroup",
        "resistance_class": "not-classifiable",
        "resistance_class_source": "not-classifiable",
        "dtr_status": "not-derivable",
        "route": "other (multi-route: IV infusion + single intraoperative dose)",
        "modality": "phage+antibiotic combination",
        "clinical_success_n": "1",
        "clinical_success_definition": (
            "Persistent disseminated left-ventricular-assist-device driveline infection "
            "(strain MYC4). Recorded by the source as clinical improvement: computed "
            "tomography shows no evidence of infection and the patient has been off "
            "antibiotic treatment since May 2022 and stable, while scant driveline "
            "drainage remains culture-positive and is controlled with local wound care"
        ),
        "adverse_event_n": "0",
        "microbio_eradication_n": "0",
        "mortality_n": "0",
        "los_days": "NA",
        "resistance_emergence_n": "NA",
        "study_design": "case series",
        "data_provenance": "independently-extracted",
        "rob_source": "independently-rated",
        "publication_year": "2023",
        "journal_tier": "high-tier (Clinical Infectious Diseases)",
        "geographic_source": "USA (Houston, Baylor College of Medicine TAILOR Labs)",
        "extraction_citation": (
            "VERIFIED (2026-07-29) from PMC PMID 37279523, PMC10573729, "
            "doi 10.1093/cid/ciad335, Clin Infect Dis 2023;77(8):1079-1091, per-case "
            "results table. Recovered by a round-5 referee-prompted search; the record "
            "names neither the organism nor a resistance term in its title or abstract "
            "and could not be retrieved by any query this review had executed. Twelve "
            "cases are reported and exactly one is P. aeruginosa (Case 11); the other "
            "eleven are E. coli, E. cloacae, K. aerogenes, K. pneumoniae, S. aureus and "
            "E. faecium and are out of scope. CASE 11: phages 6917 and 6959 under IND "
            "27807, 1e10 PFU/mL q12h IV for 6 weeks plus 1e11 PFU/mL intraoperatively "
            "once, with cefepime. ERADICATION = 0: drainage remains culture-positive. "
            "CLINICAL SUCCESS = 1: the source records improvement, off antibiotics since "
            "May 2022. DE-DUPLICATION AGAINST Aslam2020_C5 AND _C8, both P. aeruginosa "
            "ventricular-assist-device arms already in this corpus. Distinct on four "
            "independent fields: phage identity (6917/6959 from Baylor TAILOR vs GD-1 for "
            "C5 and SDSU1/SDSU2/PAK_P1/PPM3 for C8), regulatory record (IND 27807, "
            "unmatched), dosing (q12h IV plus one intraoperative dose vs C5's q8h IV with "
            "none), and chronology -- a May 2022 follow-up cannot appear in a paper "
            "published September 2020. The outcomes also run opposite: C5 and C8 are both "
            "recorded 'Outcome: Failure' verbatim. RESISTANCE NOT CLASSIFIABLE: the series "
            "describes 'difficult-to-treat antimicrobial resistant infections' collectively "
            "but publishes no per-case antibiogram and no MDR/XDR/PDR label for Case 11."
        ),
        "extraction_status": "COMPLETE",
        "incomplete_reason": (
            "Resistance not classifiable: series-level resistance framing only, no per-case "
            "antibiogram. Length of stay and phage-resistance emergence not reported."
        ),
        "study_arm_id": "Green2023_C11",
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
    print("  added: %-26s n=%s  %s" % (r["arm_id"], r["n_arm"], r["modality"]))

with csv_path.open("w", encoding="utf-8", newline="") as fh:
    writer = csv.DictWriter(fh, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(rows)

print("")
print("extraction dataset now: %d arms across %d studies"
      % (len(rows), len({r["study_id"] for r in rows})))
