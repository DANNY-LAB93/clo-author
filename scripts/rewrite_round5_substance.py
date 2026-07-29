"""Rewrite the passages whose MEANING, not just arithmetic, the round-5
additions changed.

Four substantive changes:

1. MODALITY. The review said "exactly one arm is phage monotherapy" and built an
   argument on it: that with one exception the published record contains no
   patient given phage without a concomitant antibiotic. Zaldastanishvili's two
   Eliava patients are both phage monotherapy -- one took antibiotics once in
   three years during an intercurrent viral illness, the other refused them
   outright -- so the stratum now holds three arms. The argument survives in
   direction but not in strength, and the two new arms are the only ones in the
   corpus where a non-eradication outcome can be attributed to phage rather than
   to a co-intervention.

2. LENGTH OF HOSPITALIZATION. The text said this was reported by one arm. The
   pipeline says ZERO pooling-eligible arms report it: the single los_days value
   in the dataset belongs to Racenis 2023, which is excluded from pooling. The
   domain referee flagged exactly this.

3. POPULATION-ELIGIBILITY SENSITIVITY. The Results paragraph named PhagoBurn,
   SWARM-P.a. and BX004-A as the not-classifiable arms contributing "45 of the
   corpus's 82 patients". All three are excluded from pooling and cannot
   contribute to any pooled estimate. Both referees flagged it. Replaced with
   the arms that actually carry the stratum.

4. THE "CLEAN THREE-BY-FOUR GRID". The Discussion described the thirteen poolable
   cells as a three-by-four grid, which is twelve, and attributed the tidiness to
   the population criterion having removed the arms "propping up the
   not-classifiable stratum". The not-classifiable clinical-success cell is
   pooled, and is now larger than before.
"""
import pathlib
import sys

BS = chr(92)


def M(name):
    return BS + name


root = pathlib.Path(__file__).resolve().parent.parent
failures = []


def swap(fname, old, new, note):
    p = root / "paper" / "sections" / fname
    s = p.read_text(encoding="utf-8")
    if s.count(old) != 1:
        failures.append("%s :: %s (matches %d)" % (fname, note, s.count(old)))
        return
    p.write_text(s.replace(old, new, 1), encoding="utf-8", newline=chr(10))
    print("  ok   " + note)


# --- 1. modality, characteristics section ------------------------------------
swap("results.tex",
     "Modality is overwhelmingly combination therapy (30 of 31 arms); exactly one arm is phage "
     "monotherapy --- " + BS + "textcite{Arya2026_pji_natcomms}, an intermittent phage-only "
     "regimen with no antibiotic --- so the phage-monotherapy stratum holds a single arm of a "
     "single patient, while no arm is coded pure antibiotic monotherapy.",

     "Modality is overwhelmingly combination therapy (" + M("ModPhageAntibioticCombinationArms")
     + "of " + M("ArmsAnalysed") + "arms). " + M("ModPhageMonotherapyArms") + "arms are phage "
     "monotherapy: " + BS + "textcite{Arya2026_pji_natcomms}, an intermittent phage-only regimen "
     "for a periprosthetic joint infection, and the two Eliava Phage Therapy Center patients in "
     + BS + "textcite{Zaldastanishvili2021_viruses}, both of whom came to that centre expressly to "
     "replace antibiotics with phages and did --- one taking antibiotics once in three years "
     "during an intercurrent viral illness, the other refusing them outright. No arm is coded "
     "pure antibiotic monotherapy.",
     "modality description: one monotherapy arm becomes three")

# --- 2. modality, stratified section ----------------------------------------
swap("results.tex",
     "Modality could not be stratified at all. " + M("ModPhageMonotherapyArms") + " of the "
     + M("ArmsAnalysed") + " arms is phage monotherapy (" + BS
     + "textcite{Arya2026_pji_natcomms}, one patient) and the other "
     + M("ModPhageAntibioticCombinationArms") + " combine phage with antibiotics, so there is no "
     "antibiotic-monotherapy stratum to compare against and no poolable phage-monotherapy "
     "stratum either (" + BS + "Cref{tab:not-pooled}, final row). This is the cleanest single "
     "statement of what the corpus cannot answer: with one exception the published record does "
     "not contain a patient given phage without a concomitant antibiotic, so no arm in this "
     "synthesis can attribute its outcome to the phage.",

     "Modality still could not be stratified. " + M("ModPhageMonotherapyArms") + "of the "
     + M("ArmsAnalysed") + "arms are phage monotherapy and the other "
     + M("ModPhageAntibioticCombinationArms") + "combine phage with antibiotics, so there is no "
     "antibiotic-monotherapy stratum to compare against and the phage-monotherapy stratum holds "
     "three patients --- far below the twenty-patient floor (" + BS + "Cref{tab:not-pooled}, "
     "final row). The direction of the point stands and is the cleanest statement of what this "
     "corpus cannot answer: in all but " + M("ModPhageMonotherapyArms") + "arms the published "
     "record does not contain a patient given phage without a concomitant antibiotic, so almost "
     "no arm here can attribute its outcome to the phage rather than to the co-intervention. "
     "Those three arms are correspondingly the most informative in the review on that question, "
     "and two of the three --- " + BS + "citeauthor{Zaldastanishvili2021_viruses}'s Eliava "
     "patients --- did " + BS + "emph{not} achieve eradication.",
     "modality stratum paragraph: rewritten for three arms")

# --- 3. length of hospitalization -------------------------------------------
swap("results.tex",
     BS + "textbf{Length of hospitalization.} Reported by 1 of 31 arms, so no synthesis was "
     "attempted (Section~" + BS + "ref{sec:methods-outcomes}).",

     BS + "textbf{Length of hospitalization.} Reported by " + M("LosReported") + "of the "
     + M("ArmsAnalysed") + "pooling-eligible arms, so no synthesis was attempted "
     "(Section~" + BS + "ref{sec:methods-outcomes}). Earlier drafts reported this as one arm. The "
     "single length-of-stay value in the extraction dataset belongs to "
     + BS + "citeauthor{Racenis2023_viruses}, which the de-duplication rule removes from pooling, "
     "so no arm contributing to any estimate in this review reports it.",
     "length of hospitalization: one arm becomes zero")

# --- 4. population-eligibility sensitivity ----------------------------------
old_sens_start = "phage arm ($n=13$), the SWARM-P.a.\\ high-dose cohort ($n=10$), and BX004-A's phage arm ($n=7$) --- and they contribute 45 of the corpus's " + M("PatientsAnalysed") + "patients."
p = root / "paper" / "sections" / "results.tex"
s = p.read_text(encoding="utf-8")
i = s.find("phage arm ($n=13$), the SWARM-P.a.")
if i < 0:
    failures.append("results.tex :: population-eligibility sensitivity anchor not found")
else:
    # replace from the start of the sentence naming the arms through the end of
    # the delta list, which is also wrong
    sent_start = s.rfind(".", 0, i - 200)
    j = s.find("percentage points, 17 patients d", i)
    j2 = s.find(".", j) if j > 0 else -1
    if j2 < 0:
        failures.append("results.tex :: could not locate the end of the sensitivity sentence")
    else:
        new_sens = (
            " The " + M("ResNotClassifiableArms") + "arms whose resistance status this review "
            "cannot establish carry " + M("ResNotClassifiablePatients") + "patients, "
            + M("ResNotClassifiablePct") + "of the corpus, and the largest of them by far is "
            + BS + "citeauthor{Onallah2023_med}'s PASA16 series ($n=15$); the rest are single "
            "patients. They enter every ``overall'' pool, including the headline clinical-success "
            "estimate. Re-pooling each overall cell on only those arms whose resistance status is "
            "positively established moves every one of the four: clinical success falls by "
            + M("NcSensClinicalSuccessDeltaAbs") + "percentage points ("
            + M("NcSensClinicalSuccessDropped") + "patients dropped), safety by "
            + M("NcSensSafetyDeltaAbs") + " (" + M("NcSensSafetyDropped") + "), while eradication "
            "rises by " + M("NcSensEradicationDeltaAbs") + " (" + M("NcSensEradicationDropped")
            + ") and mortality by " + M("NcSensMortalityDeltaAbs") + " ("
            + M("NcSensMortalityDropped") + ")."
        )
        s = s[:sent_start + 1] + new_sens + s[j2 + 1:]
        p.write_text(s, encoding="utf-8", newline=chr(10))
        print("  ok   population-eligibility sensitivity: named arms and deltas corrected")

# --- 5. the "clean three-by-four grid" --------------------------------------
swap("discussion.tex",
     "The thirteen poolable cells now form a clean three-by-four grid --- four outcomes, each "
     "pooled overall, within MDR, and within the route-``other'' bucket --- because tightening "
     "the population criterion removed the trial arms that had been propping up the "
     "not-classifiable and inhaled/nebulized strata.",

     "The " + M("CellsPooled") + "poolable cells are four outcomes pooled three ways --- overall, "
     "within MDR, and within the route-``other'' bucket --- plus one more: clinical success "
     "within the " + BS + "emph{not-classifiable} resistance stratum, which is the cell this "
     "review regards as its least defensible and its most informative "
     "(Section~" + BS + "ref{sec:results-stratified}). Two of those three strata are residual "
     "categories rather than clinical classes, which is itself the finding: the stratification "
     "succeeds mainly where the strata are undefined.",
     "grid claim: twelve cells described as thirteen, and the NC cell omitted")

if failures:
    print("")
    print("NOT APPLIED (%d):" % len(failures))
    for f in failures:
        print("  " + f)
    sys.exit(1)
print("")
print("substantive rewrites complete")
