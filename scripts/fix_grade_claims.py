"""Correct the two places where the manuscript states a GRADE risk-of-bias rule
the code does not implement, and the passage whose downgrade counts contradict
the GRADE table.

The Methods described a rule requiring that "single-patient case reports
contribute more than half the cell's patients AND the one High-risk-of-bias
trial also contributes". Neither clause can fire in this corpus: the population
criterion removed every trial, and single-patient reports never exceed 35% of
any cell's patients. That rule could therefore never yield -2, yet every cell in
grade_summary.tex carries -2. The implemented rule (10_grade.R Domain 1)
conditions on every contributing arm rating High risk overall, which is true
everywhere because Murad's causality domain cannot be satisfied where phage was
co-administered with antibiotics.

This is the same class of defect as the Hartung-Knapp claim corrected earlier:
a methodological statement in the text that the arithmetic does not support.
"""
import pathlib
import sys

BS = chr(92)


def M(name):
    return BS + name


root = pathlib.Path(__file__).resolve().parent.parent
failures = []

# ---- Methods: state the rule that is actually implemented -------------------
p = root / "paper" / "sections" / "methods.tex"
s = p.read_text(encoding="utf-8")

old = ("risk of bias, rated down two levels where single-patient case reports contribute more "
       "than half the cell's patients " + BS + "emph{and} the one High-risk-of-bias trial also "
       "contributes, and one level otherwise")

new = ("risk of bias, rated down two levels where every arm contributing to the cell rates High "
       "risk of bias overall on " + BS + "textcite{Murad2018_casereports} and one level otherwise "
       "--- a rule whose second branch is unreachable in this corpus, because Murad's causality "
       "domain cannot be satisfied by any arm here and the overall rating is the maximum across "
       "domains, so the deduction is " + BS + "emph{uniformly} $-$" + M("GradeRobDrop")
       + " and discriminates between no two cells (Section~" + BS + "ref{sec:results-grade})")

if old in s:
    s = s.replace(old, new, 1)
    p.write_text(s, encoding="utf-8", newline="\n")
    print("  ok   Methods now states the implemented risk-of-bias rule")
else:
    failures.append("Methods risk-of-bias rule")

# ---- Results: the GRADE paragraph's counts ----------------------------------
p = root / "paper" / "sections" / "results.tex"
s = p.read_text(encoding="utf-8")

REPL = [
    ("Five cells carry the minimum burden of three downgrades",
     M("GradeCellsAtMin") + " cells carry the minimum burden of "
     + M("GradeMinDowngrades") + " downgrades",
     "five cells at 'three' downgrades; the table gives four"),

    ("three of the five domains",
     "three of the five domains",
     None),  # placeholder, skipped below if unchanged
]

for old_t, new_t, note in REPL:
    if note is None:
        continue
    if old_t in s:
        s = s.replace(old_t, new_t, 1)
        print("  ok   " + note)
    else:
        failures.append(note)

p.write_text(s, encoding="utf-8", newline="\n")

if failures:
    print("")
    print("NOT APPLIED:")
    for f in failures:
        print("  " + f)
    sys.exit(1)
print("")
print("GRADE claims corrected")
