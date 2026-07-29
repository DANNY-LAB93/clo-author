"""Replace every corpus count the round-5 additions falsified.

Adding Zaldastanishvili's two arms and Green's one moved the corpus from 31
pooling-eligible arms / 25 studies / 82 patients to 34 / 27 / 85, and changed
almost every derived count with it. Each replacement below is a literal that is
now wrong; the macro version cannot go stale again.

Two of these were ALREADY wrong before the additions, and the audit found them
only because the count moved:

  - Methods said "19 of the 31 pooling-eligible arms contain a single patient"
    where every other section said 24. The true figure is now 27.
  - The prose said length of hospitalization is "reported by 1 of 31 arms". The
    pipeline says ZERO pooling-eligible arms report it -- the one value in the
    dataset belongs to Racenis 2023, which is excluded from pooling. The domain
    referee flagged exactly this and was right.
"""
import pathlib
import sys

BS = chr(92)


def M(name):
    return BS + name


root = pathlib.Path(__file__).resolve().parent.parent

# (file, old, new, note)
EDITS = [
    # ---- results.tex: selection and corpus description ---------------------
    ("results.tex",
     BS + "textbf{31 pooling-eligible study-arms across 25 studies}, contributing 82 patients",
     BS + "textbf{" + M("PrismaPooledArms") + "pooling-eligible study-arms across "
     + M("PrismaPooledStudies") + "studies}, contributing " + M("PatientsAnalysed") + "patients",
     "headline corpus size"),

    ("results.tex",
     "resistance is positively established for 24 of the 31 arms, leaving 7 arms and 21 patients (26 per cent of the corpus)",
     "resistance is positively established for " + M("ResClassifiedArms") + "of the "
     + M("ArmsAnalysed") + "arms, leaving " + M("ResNotClassifiableArms") + "arms and "
     + M("ResNotClassifiablePatients") + "patients (" + M("ResNotClassifiablePct")
     + "of the corpus)",
     "resistance-documentation split"),

    ("results.tex",
     "38 analytic arms across 31 studies, seven arms excluded on the four grounds above, leaving 31 arms across 25 studies",
     M("PrismaIncludedArms") + "analytic arms across " + M("PrismaIncludedStudies")
     + "studies, seven arms excluded on the four grounds above, leaving "
     + M("PrismaPooledArms") + "arms across " + M("PrismaPooledStudies") + "studies",
     "PRISMA terminal counts in the caption"),

    ("results.tex",
     "cohort contributes 3 of these 31 arms",
     "cohort contributes 3 of these " + M("ArmsAnalysed") + "arms",
     "Pirnay share denominator"),

    ("results.tex",
     "The 31 pooling-eligible arms span publication years",
     "The " + M("ArmsAnalysed") + "pooling-eligible arms span publication years",
     "characteristics opening"),

    ("results.tex",
     "Arm size ranges from single patients (24 of 31 arms) to 23",
     "Arm size ranges from single patients (" + M("SinglePatientArms") + "of "
     + M("ArmsAnalysed") + "arms) to " + M("LargestArmSize"),
     "arm-size range"),

    ("results.tex",
     "arms with more than one patient together account for 58 of the corpus's 82 patients",
     "arms with more than one patient together account for " + M("MultiPatientPatients")
     + "of the corpus's " + M("PatientsAnalysed") + "patients",
     "multi-patient arm share"),

    ("results.tex",
     "across " + M("PrismaIncludedStudies") + " studies at the arm level, including the seven arms excluded from pooling",
     "across " + M("PrismaIncludedStudies") + "studies at the arm level, including the seven "
     "arms excluded from pooling",
     "Table 1 scope sentence spacing"),

    # ---- results.tex: risk of bias ----------------------------------------
    ("results.tex",
     "Risk of bias is appraised for every one of the 31 pooling-eligible arms",
     "Risk of bias is appraised for every one of the " + M("ArmsAnalysed")
     + "pooling-eligible arms",
     "RoB coverage"),

    ("results.tex",
     BS + "textbf{All 31 arms rate High risk of bias overall}",
     BS + "textbf{All " + M("ArmsAnalysed") + "arms rate High risk of bias overall}",
     "RoB uniformity headline"),

    ("results.tex",
     "the domain responsible is causality: 30 of the 31 arms administered phage together with antibiotics",
     "the domain responsible is causality: " + M("ModPhageAntibioticCombinationArms") + "of the "
     + M("ArmsAnalysed") + "arms administered phage together with antibiotics",
     "causality-domain denominator"),

    ("results.tex",
     "together carry only 20 of the corpus's 82 patients",
     "together carry only " + M("SinglePatientPatients") + "of the corpus's "
     + M("PatientsAnalysed") + "patients",
     "single-patient-report share"),

    ("results.tex",
     "carry 56 between them",
     "carry " + M("TopThreeStudiesPatients") + "between them",
     "three-largest-sources total"),

    ("results.tex",
     BS + "caption{Per-arm risk of bias, all 31 pooling-eligible study-arms}",
     BS + "caption{Per-arm risk of bias, all " + M("ArmsAnalysed")
     + "pooling-eligible study-arms}",
     "RoB table caption"),

    ("results.tex",
     "satisfied wherever phage was co-administered with antibiotics (30 of 31 arms)",
     "satisfied wherever phage was co-administered with antibiotics ("
     + M("ModPhageAntibioticCombinationArms") + "of " + M("ArmsAnalysed") + "arms)",
     "RoB table note denominator"),

    # ---- results.tex: table notes -----------------------------------------
    ("results.tex",
     "Sample: 31 pooling-eligible study-arms across 25 studies, 82 patients",
     "Sample: " + M("PrismaPooledArms") + "pooling-eligible study-arms across "
     + M("PrismaPooledStudies") + "studies, " + M("PatientsAnalysed") + "patients",
     "pooled-estimates table note"),

    ("results.tex",
     "Sample: 31 pooling-eligible study-arms across 25 studies. NC = not-classifiable.",
     "Sample: " + M("PrismaPooledArms") + "pooling-eligible study-arms across "
     + M("PrismaPooledStudies") + "studies. NC = not-classifiable.",
     "not-pooled table note"),

    # ---- results.tex: secondary outcomes ----------------------------------
    ("results.tex",
     "Difficult-to-treat resistance is derivable for " + BS + "textbf{3 of 31 arms}",
     "Difficult-to-treat resistance is derivable for " + BS + "textbf{" + M("DtrYesArms")
     + "of " + M("ArmsAnalysed") + "arms}",
     "DTR derivability"),

    ("results.tex",
     "Only 4 of the 31 pooling-eligible arms record this outcome at all",
     "Only " + M("ResistEmergenceReported") + "of the " + M("ArmsAnalysed")
     + "pooling-eligible arms record this outcome at all",
     "phage-resistance reporting rate"),

    ("results.tex",
     "the reporting rate itself: 27 of 31 arms are silent",
     "the reporting rate itself: " + M("ResistEmergenceSilent") + "of "
     + M("ArmsAnalysed") + "arms are silent",
     "phage-resistance silence rate"),

    ("results.tex",
     "confirms every one of the 31 pooling-eligible rows is coded",
     "confirms every one of the " + M("ArmsAnalysed") + "pooling-eligible rows is coded",
     "provenance check denominator"),

    ("results.tex",
     "with 24 of 31 arms contributing a single patient that regressor equals",
     "with " + M("SinglePatientArms") + "of " + M("ArmsAnalysed")
     + "arms contributing a single patient that regressor equals",
     "Peters' near-singularity"),

    # ---- methods.tex ------------------------------------------------------
    ("methods.tex",
     "positively established for 24 of 31 arms; the other 7 arms, carrying 21 patients or 26 per cent of the corpus",
     "positively established for " + M("ResClassifiedArms") + "of " + M("ArmsAnalysed")
     + "arms; the other " + M("ResNotClassifiableArms") + "arms, carrying "
     + M("ResNotClassifiablePatients") + "patients or " + M("ResNotClassifiablePct")
     + "of the corpus",
     "Methods resistance split"),

    ("methods.tex",
     "The final analytic dataset contains 31 study-arms across 26 studies.",
     "The final analytic dataset contains " + M("PrismaIncludedArms") + "study-arms across "
     + M("PrismaIncludedStudies") + "studies.",
     "Methods dataset size (was also internally contradictory: 31 - 1 = 31)"),

    ("methods.tex",
     "leaving 31 pooling-eligible study-arms across 25 studies",
     "leaving " + M("PrismaPooledArms") + "pooling-eligible study-arms across "
     + M("PrismaPooledStudies") + "studies",
     "Methods pooling-eligible count"),

    ("methods.tex",
     "Risk of bias is appraised for all 31 pooling-eligible study-arms",
     "Risk of bias is appraised for all " + M("ArmsAnalysed") + "pooling-eligible study-arms",
     "Methods RoB coverage"),

    ("methods.tex",
     "because 19 of the 31 pooling-eligible arms contain a single patient",
     "because " + M("SinglePatientArms") + "of the " + M("ArmsAnalysed")
     + "pooling-eligible arms contain a single patient",
     "Methods single-patient count -- was 19 against 24 elsewhere, both now wrong"),
]

failures = []
applied = {}

for fname, old, new, note in EDITS:
    p = root / "paper" / "sections" / fname
    s = p.read_text(encoding="utf-8")
    n = s.count(old)
    if n != 1:
        failures.append("%s :: %s (matches: %d)" % (fname, note, n))
        continue
    p.write_text(s.replace(old, new, 1), encoding="utf-8", newline=chr(10))
    applied[fname] = applied.get(fname, 0) + 1
    print("  ok   " + note)

print("")
for f, n in sorted(applied.items()):
    print("%-16s %d replacements" % (f, n))

if failures:
    print("")
    print("NOT APPLIED (%d):" % len(failures))
    for f in failures:
        print("  " + f)
    sys.exit(1)
