"""Route the Introduction and Discussion through the macro system.

The macro system was built and verified against results.tex. A round-6 referee
found that the Introduction and Discussion still carried hand-typed estimates:
both state the MDR clinical-success cell as "73.0% (95% CI 55.0-85.7%)" when the
current value is 75.0% (58.1-86.6%). The claim that "the prose is a build
product" was therefore true of one section and false of the manuscript.

Also corrected here is a leave-one-out sentence that was wrong in three separate
ways. It read: "The MDR-specific safety and mortality estimates, the route-'other'
safety estimate, and the not-classifiable resistance stratum's mortality estimate
remain sensitive, collapsing to a value indistinguishable from zero if Pirnay or
Jault 2019 is removed."

  - Jault 2019 (PhagoBurn) is excluded from pooling by the population criterion
    and appears NOWHERE in leave_one_out.rds. A sensitivity attributed to a study
    that is not in the analysis.
  - The not-classifiable MORTALITY cell does not pool (k = 9, N = 11). A
    leave-one-out result reported for a cell that does not exist.
  - MDR SAFETY is not among the sensitive cells. The three that are flagged are
    mortality overall, mortality within MDR, and safety in route-"other" -- all
    to Pirnay and to no one else.
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


PC = BS + "%"

# ---- Introduction: the MDR estimate -----------------------------------------
swap("intro.tex",
     "MDR isolates specifically now have a pooled estimate (73.0" + PC + " clinical success, 95"
     + PC + " CI 55.0--85.7" + PC + ").",
     "MDR isolates specifically now have a pooled estimate (" + M("CsResMDREstCI")
     + "clinical success).",
     "Introduction: MDR estimate was 73.0% (55.0-85.7); current value is derived")

# ---- Discussion: the MDR estimate -------------------------------------------
swap("discussion.tex",
     "the MDR-specific pooled estimate (73.0" + PC + " clinical success, 95" + PC
     + " CI 55.0--85.7" + PC + ")",
     "the MDR-specific pooled estimate (" + M("CsResMDREstCI") + "clinical success)",
     "Discussion: same stale MDR estimate")

# ---- Discussion: the leave-one-out sentence ---------------------------------
swap("discussion.tex",
     "The MDR-specific safety and mortality estimates, the route-``other'' safety estimate, and "
     "the not-classifiable resistance stratum's mortality estimate remain sensitive, however, "
     "collapsing to a value indistinguishable from zero if " + BS
     + "citeauthor{Pirnay2024_natmicrobiol} or " + BS + "citeauthor{Jault2019_phagoburn} is "
     "removed.",

     "Exactly " + M("LooSensitiveCells") + "cells are sensitive to the removal of a single "
     "study, and all " + M("LooSensitiveCells") + "are sensitive to the same one: overall "
     "mortality, mortality within MDR, and safety in the route-``other'' bucket each collapse to "
     "a value indistinguishable from zero when " + BS + "citeauthor{Pirnay2024_natmicrobiol} is "
     "removed. No other study's removal moves any cell outside its own confidence interval. An "
     "earlier version of this paragraph also named MDR safety, a not-classifiable mortality "
     "estimate, and " + BS + "citeauthor{Jault2019_phagoburn}; MDR safety is not flagged, the "
     "not-classifiable mortality cell does not pool, and "
     + BS + "citeauthor{Jault2019_phagoburn} is excluded from pooling by the population criterion "
     "and appears nowhere in the leave-one-out.",
     "Discussion: leave-one-out corrected -- 3 cells, all to Pirnay, Jault not in the analysis")

if failures:
    print("")
    print("NOT APPLIED (%d):" % len(failures))
    for f in failures:
        print("  " + f)
    sys.exit(1)
print("")
print("Introduction and Discussion routed through the macro system")
