"""Rebuild the two-panel forest caption from macros.

The caption quoted the route-"other" clinical-success estimate as 77.4% (95% CI
61.9-87.8%) against a pipeline value of 76.9% (60.9-87.7%), and described the
panel as covering "7-8 studies (38-53 patients depending on outcome)" -- a range
spanning four outcomes for a panel that plots one. Both referees flagged that a
reader can count the rows and see the caption is wrong.
"""
import pathlib

BS = chr(92)


def M(name):
    return BS + name


root = pathlib.Path(__file__).resolve().parent.parent
p = root / "paper" / "sections" / "results.tex"
s = p.read_text(encoding="utf-8")

old_start = s.find(BS + "caption{Forest plots: two stratified cells meeting the pooling threshold.")
assert old_start > 0, "caption not found"
old_end = s.find("\n", old_start)
assert old_end > old_start

new = (
    BS + "caption{Forest plots: two stratified cells meeting the pooling threshold. Each row is "
    "one study-" + BS + "emph{arm}, not one study, so the row count exceeds the study count where a "
    "study contributes several arms. Panel (a): clinical success in the MDR stratum --- "
    + M("CsResMDRArms") + " arms from " + M("CsResMDRK") + " studies, " + M("CsResMDRN")
    + " patients, pooled " + M("CsResMDREstCI") + ". This estimate clears the pooling threshold "
    "only under author-reported resistance labels; restricting to independently verified "
    "classification collapses it below threshold (Section~" + BS + "ref{sec:results-robustness}). "
    "Panel (b): clinical success among arms coded a multi-route or otherwise unclassifiable "
    "(``other'') route --- " + M("CsRouteOtherArms") + " arms from " + M("CsRouteOtherK")
    + " studies, " + M("CsRouteOtherN") + " patients, pooled " + M("CsRouteOtherEstCI") + ". "
    "Both cells have $" + BS + "tau^2 = 0$, so the plotted interval is a $t$-interval on the logit "
    "of the pooled counts and carries no between-arm variance component "
    "(Section~" + BS + "ref{sec:results-robustness}). XDR, PDR and every specific single route fell "
    "below threshold and are not plotted; see " + BS + "Cref{tab:not-pooled}. Source: "
    + BS + "texttt{scripts/R/07" + BS + "_figures.R}.}"
)

s = s[:old_start] + new + s[old_end:]
p.write_text(s, encoding="utf-8", newline="\n")
print("forest caption rebuilt from macros (" + str(len(new)) + " chars, 0 numeric literals)")
