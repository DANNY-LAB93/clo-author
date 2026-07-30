"""Resolve the last ten records from the un-blocked search, and correct one
exclusion the domain referee was right to challenge.

RUBALSKII 2020 -- A CORRECTED EXCLUSION, NOT A NEW STUDY

This review had excluded Rubalskii et al. 2020 as "multi-pathogen, not
separable". The domain referee challenged that directly: "my recollection is that
its results table gives per-patient pathogen and outcome, which would make the
P. aeruginosa cases separable. Please re-check and report the specific table you
consulted." Re-checked against Table 1 and the per-patient Results of the PMC
full text (PMC7277081), the referee is right and the exclusion was wrong.

Two of the eight patients involve P. aeruginosa, and they differ:

  Patient 1 -- polymicrobial, S. aureus and E. faecium alongside P. aeruginosa,
  with no organism-specific outcome. Not separable, and correctly not entered.

  Patient 8 -- MONOMICROBIAL P. aeruginosa. A 13-year-old male with an infected
  thoracotomy wound two months after double lung transplantation for cystic
  fibrosis, refractory to surgical debridement, vacuum-assisted therapy and
  continuous antibiotics. Treated with 4 mL of phage-containing fibrin glue
  sprayed over the wound intraoperatively. Outcome reported individually: the
  wound completely healed and P. aeruginosa was not detected.

So one arm was separable all along. The study is re-entered for that arm only,
and the exclusion note is corrected rather than quietly dropped. This is the
second time in round 5 that a referee's specific factual challenge to an
exclusion has been upheld.

PARDO-FREIRE 2025 -- ADMITTED

44-year-old woman with cystic fibrosis and bilateral lung transplantation,
chronic P. aeruginosa, in acute rejection with deteriorating lung function.
Nebulised phage vB_Pae_10 in two 10-day courses with nebulised colistin and oral
azithromycin. The authors label the day-75 isolate an "increased MDR phenotype,
susceptible only to ceftazidime-avibactam". ERADICATION = 0 and the distinction
matters: phage produced a 1.2 log reduction and the load returned to
pre-treatment levels by day 25; the later culture-negativity followed 21 days of
intravenous ceftazidime-avibactam, not the phage.

EIGHT REJECTED, each on a stated ground

Ngauy 2026 (PMID 41853116) is not a new record at all -- it is the Ngauy2026 arm
already in this corpus. It was missed by the PMID traceability sweep because its
extraction citation records page numbers rather than a PMID, which is a gap in
this review's own audit trail and is noted as such.

Surana 2026 (PMID 41589298) describes PDR septic shock in which NO PHAGE WAS
GIVEN; bacteriophages are mentioned only as an experimental option that "remain
unavailable in most clinical settings". The patient died on comfort measures.
Screened in by a phage-therapy keyword, excluded for absence of the
intervention.

Jernigan 2025 (PMID 39834667) reports "Induced Native Phage Therapy", which
purports to induce a patient's endogenous phages rather than administer an
exogenous lytic preparation. That is not the intervention this review defines,
and the case is additionally a multi-microbial syndrome with Aspergillus,
Mycobacterium and Staphylococcus alongside P. aeruginosa and no organism-specific
outcome.

Hayakawa 2025 (PMID 40639454), already excluded, is confirmed: it is a
feasibility study of phage PREPARATION -- "phages could be prepared for 26 of 30
strains" -- not of phage treatment.

Ferry 2024, the PHAGEinLYON Clinic programme (PMID 39491599), reports 33 treated
patients and 172 cocktails targeting "Staphylococcus aureus and/or Pseudomonas
aeruginosa", with the 69% favourable-evolution figure pooled across organisms and
no per-patient breakdown. Not separable. Excluding it also removes a
double-counting risk, since Teney 2024 was treated under the same Lyon programme.

Otava 2024 (PMID 39452183) and Eiferman 2025 (PMID 39861912) fail the population
criterion on their own antibiograms. Otava's isolate was "susceptible to all
tested antimicrobial agents except trimethoprim-sulfamethoxazole", to which
P. aeruginosa is intrinsically resistant, later acquiring levofloxacin
resistance. Eiferman's is described verbatim as "multi-susceptible
P. aeruginosa". Neither paper claims MDR, XDR or PDR, and neither reaches
Magiorakos's three-category threshold.

Gupta 2019 (PMID 31081402) reports 20 chronic non-healing wounds with E. coli,
S. aureus and P. aeruginosa, and reports outcomes as means across all patients
rather than per organism. Not separable, on the same ground as Zurabov 2023. Its
population was also recruited on failure of debridement and antibiotics rather
than on resistance.
"""
import csv
import pathlib
import sys

root = pathlib.Path(__file__).resolve().parent.parent
csv_path = root / "data" / "cleaned" / "phage_therapy_extraction_dataset.csv"

with csv_path.open(encoding="utf-8", newline="") as fh:
    reader = csv.DictReader(fh)
    fieldnames = reader.fieldnames
    rows = list(reader)
existing = {r["arm_id"] for r in rows}

new_rows = [
    {
        "study_id": "Rubalskii2020",
        "arm_id": "Rubalskii2020_P8",
        "n_arm": "1",
        "pathogen_scope": "mixed-pathogen-with-Pseudomonas-subgroup",
        "resistance_class": "not-classifiable",
        "resistance_class_source": "not-classifiable",
        "dtr_status": "not-derivable",
        "route": "topical/local (intraoperative fibrin-glue-embedded phage sprayed over the wound)",
        "modality": "phage+antibiotic combination",
        "clinical_success_n": "1",
        "clinical_success_definition": (
            "13-year-old male with a P. aeruginosa-infected thoracotomy wound two months after "
            "double lung transplantation for cystic fibrosis, refractory to surgical debridement, "
            "vacuum-assisted closure and continuous antibiotic therapy under mycophenolic acid, "
            "tacrolimus and prednisolone. Success recorded as the wound healing completely"
        ),
        "adverse_event_n": "0",
        "microbio_eradication_n": "1",
        "mortality_n": "0",
        "los_days": "NA",
        "resistance_emergence_n": "NA",
        "study_design": "case series",
        "data_provenance": "independently-extracted",
        "rob_source": "independently-rated",
        "publication_year": "2020",
        "journal_tier": "mid-tier (Antibiotics/MDPI)",
        "geographic_source": "Germany (Hannover Medical School)",
        "extraction_citation": (
            "VERIFIED (2026-07-29) from PMC full text and Table 1, PMID 32380707, PMC7277081, "
            "doi 10.3390/antibiotics9050232, Antibiotics 2020;9(5):232, Results 2.1 and Methods "
            "4.5. CORRECTS AN EXCLUSION THIS REVIEW HAD MADE. The study was previously excluded "
            "as multi-pathogen and not separable; the domain referee challenged that at round 5 "
            "and asked which table had been consulted. Table 1 does give per-patient species and "
            "outcome, and the per-patient Results narrate all eight individually. Of the two "
            "patients involving P. aeruginosa, Patient 1 is polymicrobial (S. aureus and "
            "E. faecium alongside) with no organism-specific outcome and remains out; PATIENT 8 "
            "IS MONOMICROBIAL P. aeruginosa and is entered here. Treated with 4 mL of "
            "phage-containing fibrin glue sprayed over the wound surface during debridement -- a "
            "sustained local delivery route unique in this corpus. ERADICATION = 1 and CLINICAL "
            "SUCCESS = 1: the source states the wound completely healed and P. aeruginosa was no "
            "longer detected. ADVERSE EVENT = 0: 'We did not observe any major, minor, or "
            "unexpected side effects of phage therapy in our treated patients.' MODALITY "
            "combination: 'All patients remained on conventional antibiotics during "
            "bacteriophage treatment', with regimens unchanged before and during. RESISTANCE NOT "
            "CLASSIFIABLE: Table 1's descriptor for this patient is continuous isolation despite "
            "conventional antibiotic therapy, with no MDR/XDR/PDR label and no antibiogram, so "
            "the conservative asymmetric rule retains it as not-classifiable."
        ),
        "extraction_status": "COMPLETE",
        "incomplete_reason": (
            "Resistance not classifiable: refractoriness is documented but no antibiogram or "
            "resistance label is published for this patient. Only 1 of the study's 2 "
            "P. aeruginosa patients is separable; Patient 1 is polymicrobial and excluded."
        ),
        "study_arm_id": "Rubalskii2020_P8",
    },
    {
        "study_id": "PardoFreire2025",
        "arm_id": "PardoFreire2025_A",
        "n_arm": "1",
        "pathogen_scope": "Pseudomonas-only",
        "resistance_class": "MDR",
        "resistance_class_source": "author-reported",
        "dtr_status": "not-derivable",
        "route": "inhaled/nebulized",
        "modality": "phage+antibiotic combination",
        "clinical_success_n": "1",
        "clinical_success_definition": (
            "44-year-old woman with cystic fibrosis and bilateral lung transplantation, in acute "
            "rejection with deteriorating lung function on a background of chronic P. aeruginosa. "
            "Success recorded as mucus clearance, improved pulmonary function and resolution of "
            "the acute rejection, sustained to one year"
        ),
        "adverse_event_n": "0",
        "microbio_eradication_n": "0",
        "mortality_n": "0",
        "los_days": "NA",
        "resistance_emergence_n": "NA",
        "study_design": "case report",
        "data_provenance": "independently-extracted",
        "rob_source": "independently-rated",
        "publication_year": "2025",
        "journal_tier": "mid-tier (ASM Case Reports)",
        "geographic_source": "Spain (Madrid, Hospital Puerta de Hierro; phages Valencia/Yale)",
        "extraction_citation": (
            "VERIFIED (2026-07-29) from PMC PMID 41244966, PMC12530250, "
            "doi 10.1128/asmcr.00058-24, ASM Case Rep 2025;1(5), Results and Figure 2C. "
            "Recovered by the round-5 un-blocked search. Nebulised phage vB_Pae_10, 3 mL at 1e10 "
            "PFU daily in two 10-day courses, with nebulised colistin and oral azithromycin. "
            "RESISTANCE MDR, author-reported: the day-75 isolate is described as an 'increased "
            "MDR phenotype, susceptible only to ceftazidime-avibactam', with the full antibiogram "
            "in Figure 2C. ERADICATION = 0, and the distinction is the point: phage produced a "
            "1.2 log reduction and the bacterial load returned to PRE-TREATMENT LEVELS by day 25. "
            "The patient did become culture-negative, but after 21 days of intravenous "
            "ceftazidime-avibactam following the phage courses, so the clearance cannot be "
            "attributed to the phage. ADVERSE EVENT = 0: no adverse effects were observed. "
            "DISTINCT from Chan2025 (a nine-patient cystic-fibrosis cohort at Yale) despite "
            "shared Yale co-authorship -- this is a single Spanish transplant recipient."
        ),
        "extraction_status": "COMPLETE",
        "incomplete_reason": "Length of hospitalization and phage-resistance emergence not reported.",
        "study_arm_id": "PardoFreire2025_A",
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
    print("  added: %-22s %-18s erad=%s AE=%s"
          % (r["arm_id"], r["resistance_class"], r["microbio_eradication_n"], r["adverse_event_n"]))

with csv_path.open("w", encoding="utf-8", newline="") as fh:
    writer = csv.DictWriter(fh, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(rows)

print("")
print("extraction dataset now: %d arms across %d studies"
      % (len(rows), len({r["study_id"] for r in rows})))
