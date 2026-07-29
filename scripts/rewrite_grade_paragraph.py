"""Rewrite the GRADE domain-profile paragraph against grade_summary.tex.

Errors corrected, each verified against the generated table:

  - "the route-'other' safety estimate" was named among the minimally
    downgraded cells. That cell carries five downgrades. The fifth minimal cell
    is route-"other" MORTALITY.
  - "each rated down once for risk of bias" -- the deduction is two levels in
    every cell.
  - "three cells accumulate seven downgrades ... MDR eradication, the
    not-classifiable safety cell, and the inhaled/nebulized safety cell". There
    are TWO cells at EIGHT: overall eradication and MDR eradication. Two of the
    three named are not pooled at all and have no GRADE row.
  - "The three clinical-success cells" -- there are four.
  - "The two structural downgrades that apply to every cell" -- three domains
    are always-on (risk of bias, indirectness, publication bias), giving a
    structural floor of four levels, not two.

The paragraph also now states the collinearity a referee raised: with tau^2 = 0
the prediction interval equals the confidence interval, so the inconsistency and
imprecision domains are keyed to the same number and cannot fire independently.
"""
import pathlib

BS = chr(92)


def M(name):
    return BS + name


root = pathlib.Path(__file__).resolve().parent.parent
p = root / "paper" / "sections" / "results.tex"
s = p.read_text(encoding="utf-8")

start = s.find("What does discriminate is the domain profile in ")
assert start > 0, "GRADE paragraph anchor not found"
end = s.find("\n", start)
assert end > start

new = (
    "What does discriminate is the domain profile in " + BS + "Cref{tab:grade}, and it is the "
    "profile rather than the floored rating that carries the information. "
    + M("GradeCellsAtMin") + " cells carry the minimum burden of " + M("GradeMinDowngrades")
    + " downgrades --- overall safety, overall mortality, MDR safety, MDR mortality, and the "
    "route-``other'' " + BS + "emph{mortality} estimate --- each rated down twice for risk of "
    "bias, once for salvage-population indirectness and once for suspected publication bias, but "
    "not at all for inconsistency or imprecision. That the MDR safety and mortality cells sit "
    "among the least-downgraded in the review is worth noting explicitly, since the MDR stratum "
    "is elsewhere this review's most fragile finding. At the other extreme, "
    + M("GradeCellsAtMax") + " cells accumulate " + M("GradeMaxDowngrades")
    + " downgrades --- overall eradication and MDR eradication --- each combining very serious "
    "inconsistency (a prediction interval spanning almost the entire 0--100" + BS + "% range) "
    "with very serious imprecision on top of the structural floor. All " + M("GradeClinicalSuccessCells")
    + " clinical-success cells take a second indirectness downgrade, because success is defined "
    "by each primary study on its own terms across non-comparable infection syndromes "
    "(Section~" + BS + "ref{sec:methods-eligibility}), so the pooled construct is not a single "
    "clinical outcome.\n\n"

    "Two properties of this profile limit how much of it should be read as assessment rather "
    "than arithmetic, and we state both. First, the risk-of-bias domain is a "
    + BS + "emph{constant}: it deducts $-$" + M("GradeRobDrop") + " in every cell because every "
    "arm rates High overall on " + BS + "textcite{Murad2018_casereports}, which follows "
    "mechanically from the causality domain being unsatisfiable wherever phage was given with "
    "antibiotics. It therefore distinguishes no two cells, and the rule's alternative branch is "
    "unreachable in this corpus. Second, inconsistency and imprecision are "
    + BS + "emph{collinear by construction} in the 11 cells where $" + BS + "tau^2$ is estimated "
    "at zero: the inconsistency domain is keyed to the width of the prediction interval and the "
    "imprecision domain to the width of the confidence interval, and in those cells the two "
    "intervals are numerically identical (Section~" + BS + "ref{sec:results-robustness}). The "
    "domains cannot fire independently there, so a cell downgraded on both is being penalised "
    "twice for one fact. The " + M("GradeCellsAtMax") + " cells at the maximum are precisely the "
    "two with $" + BS + "tau^2 > 0$, which is where the two domains do measure different things.\n\n"

    "The structural floor is " + M("GradeStructuralMinimum") + " levels: risk of bias, "
    "salvage-population indirectness and suspected publication bias apply to every cell without "
    "exception, and none of the three can be remedied by adding more case reports of the same "
    "kind. That is the sharpest statement this review can make about what would and would not "
    "improve the evidence --- and it is why the Very low rating is a property of the study "
    "design available in this literature, not a verdict this review reached about particular "
    "studies."
)

s = s[:start] + new + s[end:]
p.write_text(s, encoding="utf-8", newline="\n")
print("GRADE paragraph rewritten (" + str(len(new)) + " chars)")
