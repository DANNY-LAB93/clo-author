"""Rewrite the risk-of-bias and GRADE passages, whose central claim the round-5
additions reversed.

Through round 4 every arm in the corpus rated High risk of bias overall, because
Murad's causality domain cannot be satisfied where phage was co-administered
with antibiotics and overall rating is the maximum across domains. The review
said so, and drew the consequence honestly: the GRADE risk-of-bias domain was a
CONSTANT contributing -2 to every cell and discriminating between none. The
methods referee's sharpest objection was aimed exactly there -- a deduction
derived from a tautology is not an assessment.

Zaldastanishvili's two Eliava patients are phage monotherapy. There is no
co-intervention to separate the effect from, so they rate Moderate on causality
and Moderate overall. A stopifnot() placed in 10_grade.R at round 4 to catch
precisely this fired on the first run after they were added.

The consequences, all of which the prose must now carry:

  - 32 of 34 arms rate High overall, not all of them.
  - The GRADE risk-of-bias deduction is -1 in the nine cells containing a
    monotherapy arm and -2 in the four MDR cells, which contain none. The domain
    discriminates for the first time in this review.
  - The structural floor falls from four levels to three, and the number of cells
    sitting at it changes.
  - The reachable-branch statement in Methods is now false and is replaced.
"""
import pathlib
import sys

BS = chr(92)


def M(name):
    return BS + name + " "


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


# ---- Results: the risk-of-bias headline ------------------------------------
swap("results.tex",
     "The result is worse than the partial assessment this review previously reported. "
     + BS + "textbf{All " + M("ArmsAnalysed") + "arms rate High risk of bias overall}, and the "
     "domain responsible is causality: " + M("ModPhageAntibioticCombinationArms") + "of the "
     + M("ArmsAnalysed") + "arms administered phage together with antibiotics, so no arm can "
     "attribute its outcome to the phage rather than to the co-intervention, and Murad's causality "
     "domain cannot be satisfied anywhere in the corpus. The single exception ("
     + BS + "textcite{Arya2026_pji_natcomms}, phage monotherapy) rates Moderate on that domain and "
     "is one patient. The remaining domains do discriminate: selection is High in 20 arms, "
     "Moderate in 6 and Low in 5; ascertainment is High in 2, Moderate in 18 and Low in 11; "
     "reporting is High in 7, Moderate in 7 and Low in 17.",

     "The result is worse than the partial assessment this review previously reported, though no "
     "longer uniformly so. " + BS + "textbf{" + M("RobOverallHigh") + "of the " + M("ArmsAnalysed")
     + "arms rate High risk of bias overall and " + M("RobOverallModerate") + "rate Moderate}, and "
     "the domain responsible is causality: " + M("ModPhageAntibioticCombinationArms") + "of the "
     + M("ArmsAnalysed") + "arms administered phage together with antibiotics, so those arms cannot "
     "attribute their outcome to the phage rather than to the co-intervention. Causality is "
     "therefore High in " + M("RobCausalityHigh") + "arms and Moderate in only "
     + M("RobCausalityModerate") + " --- the three phage-monotherapy arms, where there is no "
     "co-intervention to separate the effect from. Two of those three rate Moderate "
     + BS + "emph{overall} (" + BS + "citeauthor{Zaldastanishvili2021_viruses}'s Eliava patients); "
     + BS + "textcite{Arya2026_pji_natcomms} still rates High, because publishing a single patient is "
     "itself the selection event. The other domains discriminate more sharply: selection is High in "
     + M("RobSelectionHigh") + "arms, Moderate in " + M("RobSelectionModerate") + "and Low in "
     + M("RobSelectionLow") + "; ascertainment High in " + M("RobAscertainmentHigh") + ", Moderate "
     "in " + M("RobAscertainmentModerate") + "and Low in " + M("RobAscertainmentLow") + "; "
     "reporting High in " + M("RobReportingHigh") + ", Moderate in " + M("RobReportingModerate")
     + "and Low in " + M("RobReportingLow") + ".",
     "RoB headline: uniformly High becomes 32 of 34")

# ---- Results: the two consequences paragraph -------------------------------
swap("results.tex",
     "First, the GRADE risk-of-bias domain is " + BS + "emph{uniform}: every cell is downgraded "
     "two levels, because every cell rests entirely on High-risk evidence. It therefore carries no "
     "information distinguishing one cell from another, and we report it as uniform rather than "
     "tuning a threshold until it appears to discriminate.",

     "First, the GRADE risk-of-bias domain has stopped being " + BS + "emph{uniform}, and the "
     "history matters because it was the sharpest methodological objection this review received. "
     "Through the previous round every arm rated High, so the domain deducted two levels "
     "everywhere and a referee objected --- correctly --- that a deduction following "
     "algebraically from a tautology is a constant dressed as an assessment. The two "
     "phage-monotherapy arms added at round 5 break the tautology: cells containing them now take "
     "$-$" + M("GradeRobDrop") + "and the four MDR cells, which contain none, still take $-$2 "
     "(" + BS + "Cref{tab:grade}). The domain discriminates for the first time in this review, and "
     "it does so because the corpus acquired arms where causality is assessable, not because any "
     "threshold was tuned.",
     "GRADE RoB consequence: constant becomes discriminating")

# ---- Results: the GRADE domain-profile paragraph ---------------------------
swap("results.tex",
     "First, the risk-of-bias domain is a " + BS + "emph{constant}: it deducts $-$"
     + M("GradeRobDrop") + "in every cell because every arm rates High overall on "
     + BS + "textcite{Murad2018_casereports}, which follows mechanically from the causality domain "
     "being unsatisfiable wherever phage was given with antibiotics. It therefore distinguishes no "
     "two cells, and the rule's alternative branch is unreachable in this corpus.",

     "First, the risk-of-bias domain is no longer a constant. It deducts $-$"
     + M("GradeRobDrop") + "where a phage-monotherapy arm contributes and $-$2 where none does, "
     "because " + M("RobOverallModerate") + "of the " + M("ArmsAnalysed") + "arms rate Moderate "
     "rather than High overall on " + BS + "textcite{Murad2018_casereports}. Both branches of the "
     "rule are now reached. This is the one respect in which the round-5 additions improved the "
     "certainty assessment rather than diluting it.",
     "GRADE profile: RoB constant claim replaced")

# ---- Methods: the rule statement -------------------------------------------
swap("methods.tex",
     "risk of bias, rated down two levels where every arm contributing to the cell rates High "
     "risk of bias overall on " + BS + "textcite{Murad2018_casereports} and one level otherwise "
     "--- a rule whose second branch is unreachable in this corpus, because Murad's causality "
     "domain cannot be satisfied by any arm here and the overall rating is the maximum across "
     "domains, so the deduction is " + BS + "emph{uniformly} $-$" + M("GradeRobDrop")
     + "and discriminates between no two cells (Section~" + BS + "ref{sec:results-grade})",

     "risk of bias, rated down two levels where every arm contributing to the cell rates High "
     "risk of bias overall on " + BS + "textcite{Murad2018_casereports} and one level otherwise. "
     "Both branches are reached: " + M("RobOverallHigh") + "of the " + M("ArmsAnalysed")
     + "arms rate High, and the " + M("RobOverallModerate") + "phage-monotherapy arms that rate "
     "Moderate pull the cells containing them to $-$" + M("GradeRobDrop")
     + " (Section~" + BS + "ref{sec:results-grade}). In earlier rounds, when every arm rated High, "
     "this domain was a constant and is reported as such in those versions",
     "Methods RoB rule: unreachable branch is now reachable")

if failures:
    print("")
    print("NOT APPLIED (%d):" % len(failures))
    for f in failures:
        print("  " + f)
    sys.exit(1)
print("")
print("risk-of-bias and GRADE passages rewritten")
