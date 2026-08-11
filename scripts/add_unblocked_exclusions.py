"""Enter the three round-5 full-text exclusions into the extraction dataset so
their exclusion is logged by the pipeline rather than asserted in prose.

Liu 2025 Patient 1 is already handled this way: it sits in the dataset and is
removed by a named rule, so the exclusion appears in exclusion_log.rds and is
auditable. Chung 2026 and Ronit 2024 fail the SAME rule -- a published antibiogram
that does not reach the MDR threshold -- and Jennes 2017 fails the same
de-duplication rule as Ferry 2022 and Racenis 2023. Recording them the same way
keeps the exclusion log complete and lets the restore-both sensitivity analysis
include Jennes.
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

new_rows = [
    {
        "study_id": "Jennes2017",
        "arm_id": "Jennes2017_A",
        "n_arm": "1",
        "pathogen_scope": "Pseudomonas-only",
        "resistance_class": "XDR",
        "resistance_class_source": "independently-verified",
        "dtr_status": "not-derivable",
        "route": "other (multi-route: IV infusion + wound irrigation, concurrently)",
        "modality": "phage monotherapy",
        "clinical_success_n": "1",
        "clinical_success_definition": (
            "61-year-old man with large necrotic pressure sores and colistin-only-sensitive "
            "P. aeruginosa septicaemia, in whom antibiotics had been withdrawn for "
            "colistin nephrotoxicity. Success recorded as blood cultures turning negative "
            "immediately, resolution of fever, falling C-reactive protein and recovery of renal "
            "function without haemofiltration"
        ),
        "adverse_event_n": "0",
        "microbio_eradication_n": "0",
        "mortality_n": "1",
        "los_days": "NA",
        "resistance_emergence_n": "NA",
        "study_design": "case report",
        "data_provenance": "independently-extracted",
        "rob_source": "independently-rated",
        "publication_year": "2017",
        "journal_tier": "high-tier (Critical Care)",
        "geographic_source": "Belgium (Brussels, Queen Astrid Military Hospital)",
        "extraction_citation": (
            "VERIFIED (2026-07-29) from PMC full text, PMID 28583189, PMC5460490, "
            "doi 10.1186/s13054-017-1709-y, Crit Care 2017;21:129. Purified BFC1 cocktail, two "
            "phages active in vitro on the patient's isolates, 50 microlitres as a 6-hour IV "
            "infusion daily for 10 days plus 50 mL wound irrigation every 8 hours for 10 days. "
            "PHAGE MONOTHERAPY: antibiotic therapy had been discontinued to prevent further "
            "kidney damage before phage was started, and the paper presents itself as the first "
            "contemporary report of intravenous phage monotherapy against P. aeruginosa "
            "septicaemia. RESISTANCE XDR, independently derived: an isolate susceptible only to "
            "colistin is non-susceptible in all but one Magiorakos category. ERADICATION = 0: "
            "the pressure sores remained infected with several species including P. aeruginosa, "
            "causing further sepsis episodes. MORTALITY = 1: the patient died four months after "
            "phage therapy of refractory cardiac arrest with blood-culture-confirmed sepsis, "
            "from an organism the source states was SUSCEPTIBLE to the antibiotics he was "
            "receiving -- an all-cause death not attributable to the phage-treated organism, "
            "coded as this review codes the other deaths. "
            "EXCLUDED AS A PROBABLE PIRNAY-ROSTER DUPLICATE. Queen Astrid Military Hospital, "
            "BFC1, treated November 2016, inside the roster's 1 January 2008 to 30 April 2022 "
            "window, Pirnay senior author, and the roster records that 27 of its 100 cases were "
            "published elsewhere. Roster case 13 matches on species, centre, product, "
            "intravenous route and the wound-plus-bloodstream indication; case 13 is recorded as "
            "surviving, which a follow-up window shorter than four months would explain. Roster "
            "case 3, the only other XDR death, is a respiratory infection treated by inhalation "
            "for four days and is a different patient. Excluded for consistency with Ferry 2022 "
            "and Racenis 2023 and restored in the de-duplication sensitivity analysis."
        ),
        "extraction_status": "COMPLETE",
        "incomplete_reason": (
            "Excluded from pooling as a probable duplicate of a patient inside the Pirnay 2024 "
            "consortium roster; restored in the de-duplication sensitivity analysis."
        ),
        "study_arm_id": "Jennes2017_A",
    },
    {
        "study_id": "Chung2026",
        "arm_id": "Chung2026_A",
        "n_arm": "1",
        "pathogen_scope": "Pseudomonas-only",
        "resistance_class": "below-MDR-threshold",
        "resistance_class_source": "independently-verified",
        "dtr_status": "not-derivable",
        "route": "IV",
        "modality": "phage+antibiotic combination",
        "clinical_success_n": "1",
        "clinical_success_definition": (
            "36-year-old woman, refractory P. aeruginosa mediastinitis and vascular graft "
            "infection; radiological improvement on 18F-FDG PET/CT and no recurrence of "
            "bacteraemia at 12 months on oral levofloxacin suppression"
        ),
        "adverse_event_n": "0",
        "microbio_eradication_n": "0",
        "mortality_n": "0",
        "los_days": "NA",
        "resistance_emergence_n": "NA",
        "study_design": "case report",
        "data_provenance": "independently-extracted",
        "rob_source": "independently-rated",
        "publication_year": "2026",
        "journal_tier": "high-tier (Nature Communications)",
        "geographic_source": "Singapore (Singapore General Hospital)",
        "extraction_citation": (
            "VERIFIED (2026-07-29) from PMC PMID 41513696, PMC12877064, "
            "doi 10.1038/s41467-025-68136-y, Nat Commun 2026;17:1385. EXCLUDED: THE ANTIBIOGRAM "
            "DOES NOT MEET THE MDR POPULATION CRITERION. The isolates were only INTERMEDIATE to "
            "ciprofloxacin and remained susceptible to piperacillin-tazobactam, "
            "ceftazidime-avibactam and meropenem; the authors label the organism "
            "'fluoroquinolone non-susceptible' and never MDR, XDR or PDR. That is "
            "non-susceptibility in one Magiorakos category against the three the criterion "
            "requires. Excluded on the same ground, and by the same rule, as Liu 2025 "
            "Patient 1. Distinct from the Chung 2025 record excluded earlier as a "
            "review/perspective."
        ),
        "extraction_status": "COMPLETE",
        "incomplete_reason": (
            "Excluded from pooling: published antibiogram establishes non-susceptibility in one "
            "antimicrobial category, below the MDR threshold this review requires."
        ),
        "study_arm_id": "Chung2026_A",
    },
    {
        "study_id": "Ronit2024",
        "arm_id": "Ronit2024_A",
        "n_arm": "1",
        "pathogen_scope": "Pseudomonas-only",
        "resistance_class": "below-MDR-threshold",
        "resistance_class_source": "independently-verified",
        "dtr_status": "not-derivable",
        "route": "IV",
        "modality": "phage+antibiotic combination",
        "clinical_success_n": "1",
        "clinical_success_definition": (
            "82-year-old man, chronic relapsing P. aeruginosa infection of a prosthetic aortic "
            "graft; no recurrent Pseudomonas bacteraemia during follow-up on lifelong "
            "suppressive antibiotics"
        ),
        "adverse_event_n": "0",
        "microbio_eradication_n": "NA",
        "mortality_n": "1",
        "los_days": "NA",
        "resistance_emergence_n": "NA",
        "study_design": "case report",
        "data_provenance": "independently-extracted",
        "rob_source": "independently-rated",
        "publication_year": "2024",
        "journal_tier": "mid-tier (Ugeskrift for Laeger)",
        "geographic_source": "Denmark (Roskilde; phages from Belgium QAMH)",
        "extraction_citation": (
            "VERIFIED (2026-07-29) from the publisher full text, PMID 38305316, "
            "doi 10.61409/V09230617, Ugeskr Laeger 2024;186(3), Danish language with English "
            "abstract. Phages 4P and 4K from the Queen Astrid Military Hospital, intravenous "
            "over 10 days without adverse effects, with meropenem and ciprofloxacin continued "
            "two further weeks and then lifelong suppression. The patient died six months later "
            "of aortic thrombosis, not infection. EXCLUDED: THE ANTIBIOGRAM DOES NOT MEET THE "
            "MDR POPULATION CRITERION. The isolate was resistant to piperacillin-tazobactam and "
            "ceftazidime but SUSCEPTIBLE to meropenem and ciprofloxacin -- two Magiorakos "
            "categories against the three required -- and the authors apply no MDR/XDR/PDR "
            "label. A Pirnay-roster duplication question arose from the Queen Astrid "
            "co-authorship and resolves independently: the phage was given in 2023 and the "
            "roster closes on 30 April 2022."
        ),
        "extraction_status": "COMPLETE",
        "incomplete_reason": (
            "Excluded from pooling: published antibiogram establishes non-susceptibility in two "
            "antimicrobial categories, below the MDR threshold this review requires. Eradication "
            "not determinable under concurrent suppressive antibiotics."
        ),
        "study_arm_id": "Ronit2024_A",
    },
]

for r in new_rows:
    if r["arm_id"] in existing:
        print("  already present, skipping: " + r["arm_id"])
        continue
    missing = set(fieldnames) - set(r)
    extra = set(r) - set(fieldnames)
    if missing or extra:
        print("SCHEMA MISMATCH for %s: missing=%s unknown=%s"
              % (r["arm_id"], sorted(missing), sorted(extra)))
        sys.exit(1)
    rows.append(r)
    print("  added (for exclusion): %-18s %s" % (r["arm_id"], r["resistance_class"]))

with csv_path.open("w", encoding="utf-8", newline="") as fh:
    writer = csv.DictWriter(fh, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(rows)

print("")
print("extraction dataset now: %d arms across %d studies"
      % (len(rows), len({r["study_id"] for r in rows})))
