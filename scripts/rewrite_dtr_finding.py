"""Rewrite the DTR passage, whose central claim the corrected criterion falsifies.

The passage said DTR "cannot be computed from the published record at any sample
size, because the data required were never printed", and supported that with
"exactly one arm in the entire corpus reports susceptibility across all
beta-lactams and both fluoroquinolones".

Both statements were artefacts of a mis-stated criterion. Under Kadri's actual
first-line definition, six arms are adjudicable -- five positive and, for the
first time, one negative. And "no antibiogram published" was never the right
description: several of these sources print a panel. The obstacle is that the
panel is PARTIAL, and one untested first-line category blocks the call in both
directions.

The finding survives, but as a weaker and more accurate claim: DTR is reported
too rarely and too incompletely to stratify, not impossible to compute in
principle.
"""
import pathlib

BS = chr(92)


def M(name):
    return BS + name + " "


root = pathlib.Path(__file__).resolve().parent.parent
p = root / "paper" / "sections" / "results.tex"
s = p.read_text(encoding="utf-8")

start = s.find("One stratum fails for a reason none of the others do")
assert start > 0, "DTR paragraph not found"
end = s.find("\n", start)
assert end > start

new = (
    "One stratum fails for a reason none of the others do, and it is the one a clinician would "
    "most want. Difficult-to-treat resistance is adjudicable for " + BS + "textbf{"
    + M("DtrYesArms") + "arms positive and " + M("DtrNoArms") + "negative, "
    + M("DtrAdjudicable") + "of " + M("ArmsAnalysed") + "in all}; the remaining "
    + M("DtrNotDerivableArms") + "cannot be called in either direction. The positive cells carry "
    "too few patients to pool and the single negative arm carries one, so no DTR cell reaches "
    "the threshold (" + BS + "Cref{tab:not-pooled}).\n\n"

    "The reason those " + M("DtrNotDerivableArms") + "arms cannot be classified is worth stating "
    "precisely, because an earlier version of this review stated it wrongly. It is " + BS
    + "emph{not} that their sources publish no antibiogram --- several publish a panel, and this "
    "review's own extraction records the agents. It is that the panels are " + BS + "emph{partial}: "
    + BS + "textcite{Kadri2018_dtr}'s criterion requires knowing the status of every first-line "
    "category, and a single untested category blocks both a positive and a negative call. Sources "
    "typically name the agents that were administered rather than the agents that were tested, "
    "which is a different and smaller set. Where a source does report enough --- an isolate "
    "susceptible only to colistin, or only to ceftazidime-avibactam, or documented susceptible to "
    "ciprofloxacin --- the call is immediate.\n\n"

    "Earlier rounds of this review reported that DTR ``cannot be computed from the published "
    "record at any sample size''. That claim was an artefact of this review's own criterion, "
    "which required non-susceptibility to " + BS + "emph{all} $" + BS + "beta$-lactams rather than "
    "to " + BS + "citeauthor{Kadri2018_dtr}'s first-line set, and was therefore stricter than the "
    "definition it cited (Section~" + BS + "ref{sec:methods-eligibility}). Correcting it moved six "
    "arms and made DTR-negative reachable at all, a level the previous criterion had rendered "
    "impossible --- which, in retrospect, was the diagnostic sign that something was wrong. The "
    "weaker claim that survives is still worth making: the comparison current guidance treats as "
    "decision-relevant for " + BS + "textit{P." + BS + " aeruginosa} is reported too rarely and "
    "too incompletely to stratify a synthesis of this literature, and that is a statement about "
    "reporting practice rather than about phage therapy."
)

s = s[:start] + new + s[end:]
p.write_text(s, encoding="utf-8", newline=chr(10))
print("DTR finding rewritten: 'impossible at any sample size' -> 'reported too rarely to stratify'")
