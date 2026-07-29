"""Replace the damaged risk-of-bias block in Methods.

Three defects, all flagged by both round-5 referees:

  1. A sentence is spliced mid-clause: "...is withdrawn (Section 4.3).\ 2019,
     Leveque et al. 2023, Duplessis et al. 2018, ..." -- a fragment beginning
     inside a list with no subject.

  2. The block then rates the single-patient reports "Low-to-moderate risk"
     under the JBI and Murad tools -- the exact characterisation the sentence
     immediately before it withdraws, and the opposite of what the executed
     appraisal (12_risk_of_bias.R) returns, which is High for all 31 arms.

  3. It reports RoB2 and JBI ratings for four randomised trials -- PhagoBurn,
     BX004-A, SWARM-P.a./AP-PA02 and Leitner -- and describes PhagoBurn as
     anchoring "this review's phage-monotherapy-adjacent evidence". The
     population criterion removed every one of those arms from pooling. They
     contribute to no pooled estimate and no GRADE cell, so presenting their
     ratings as part of the review's risk-of-bias picture describes a synthesis
     that no longer exists.

The replacement states the appraisal that was executed, says plainly what
happened to the earlier trial ratings, and keeps the two facts in the old block
that remain true and load-bearing: that Pirnay's per-patient supplementary data
were read in full, and that the planned Liu 2025 spot-check was never performed.
"""
import pathlib

BS = chr(92)
root = pathlib.Path(__file__).resolve().parent.parent
p = root / "paper" / "sections" / "methods.tex"
s = p.read_text(encoding="utf-8")

start_marker = "(Section~" + BS + "ref{sec:results-rob})." + BS + " 2019,"
start = s.find(start_marker)
assert start > 0, "damaged block start not found"

end_marker = "This risk-of-bias picture is the input to the GRADE certainty assessment described below, which was carried out once it was complete."
end = s.find(end_marker)
assert end > start, "damaged block end not found"
end += len(end_marker)

new = (
    "(Section~" + BS + "ref{sec:results-rob}). Two consequences of that withdrawal should be "
    "stated rather than left implicit. First, the appraisal now returns "
    + BS + "emph{High} risk overall for every one of the "
    + BS + "ArmsAnalysed pooling-eligible arms, because Murad's causality domain cannot be "
    "satisfied wherever phage was co-administered with antibiotics and overall rating is the "
    "maximum across domains; the earlier characterisation was not merely unretained but "
    "directionally wrong. Second, this review's earlier rounds carried RoB2 ratings for four "
    "randomised trials and JBI ratings for several cohorts and series. The population criterion "
    "(Section~" + BS + "ref{sec:methods-eligibility}) has since removed every trial arm from "
    "pooling, so those ratings now describe arms that contribute to no pooled estimate and no "
    "GRADE cell. They are not reported here, because reporting them would describe a synthesis "
    "this review no longer performs.\n\n"

    "Two elements of that earlier work do carry forward and are recorded for provenance. "
    + BS + "citeauthor{Pirnay2024_natmicrobiol}'s full per-patient supplementary data were read "
    "in full for this review's resistance-stratified re-extraction "
    "(Section~" + BS + "ref{sec:results-characteristics}), and that reading is what supports the "
    "arm-level resistance classification of the single largest contributing cohort. The planned "
    "reuse of " + BS + "textcite{Liu2025_ijaa}'s existing risk-of-bias assessments was to be "
    "gated on independently re-rating at minimum a 20" + BS + "% random sample of overlapping "
    "studies, or all studies falling within this review's pre-specified strata, whichever is "
    "larger. That spot-check has not been performed, no study-arm carries an "
    + BS + "texttt{adopted-from-Liu2025-spot-checked} disposition, and accordingly none of "
    + BS + "citeauthor{Liu2025_ijaa}'s ratings is used anywhere in this review."
)

s = s[:start] + new + s[end:]
p.write_text(s, encoding="utf-8", newline="\n")
print("Methods risk-of-bias block replaced (" + str(len(new)) + " chars)")
print("  removed: spliced fragment, withdrawn Low-to-moderate ratings,")
print("           RoB2/JBI ratings for four arms no longer in the synthesis")
