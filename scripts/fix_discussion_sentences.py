"""Repair two damaged sentences in the Discussion and correct the sensitivity
deltas they carry.

(1) The Peters' paragraph lost a clause mid-sentence: "...because the standard
    error is a deterministic function of the proportion and Under Peters' test
    only three of the eight eligible cells return a finite p-value..." Two
    sentences were spliced. The same paragraph also states the eligibility
    count two ways ("the four outcome-overall cells" and "the eight eligible
    cells").

(2) The limitations paragraph repeats "remain not classifiable" around a
    parenthesis, and reports the population-eligibility sensitivity as moving
    "safety and eradication not at all and clinical success by 3.1 percentage
    points". The pipeline gives -4.1, -2.9, -4.7 and +1.0 pp; nothing moves
    "not at all".
"""
import pathlib
import sys

BS = chr(92)


def M(name):
    return BS + name


root = pathlib.Path(__file__).resolve().parent.parent
p = root / "paper" / "sections" / "discussion.tex"
s = p.read_text(encoding="utf-8")
failures = []

# ---- (1) the spliced Peters' sentence --------------------------------------
old1 = ("For small-study effects we now use Peters' regression test, applied to the four "
        "outcome-overall cells with at least ten studies as pre-specified; Egger's linear "
        "regression, used in an earlier version of this review, is invalid for a meta-analysis "
        "of proportions, because the standard error is a deterministic function of the "
        "proportion and Under Peters' test only three of the eight eligible cells return a "
        "finite $p$-value, and none is significant:")

new1 = ("For small-study effects we now use Peters' regression test. Egger's linear regression, "
        "used in an earlier version of this review, is invalid for a meta-analysis of "
        "proportions, because the standard error there is a deterministic function of the "
        "proportion itself, so the regressor and the outcome are mechanically linked and the "
        "test has no null to reject. Peters' test replaces the standard error with the inverse "
        "sample size, which breaks that link. It is pre-specified for cells with at least ten "
        "studies, which is " + M("PetersEligible") + " of the " + M("PetersCellsTotal")
        + " pooled cells; of those, only " + M("PetersFinite") + " return a finite $p$-value, "
        "and none is significant:")

if old1 in s:
    s = s.replace(old1, new1, 1)
    print("  ok   Peters' sentence de-spliced and eligibility stated once")
else:
    failures.append("Peters' sentence")

# ---- (2) the duplicated clause and the wrong deltas ------------------------
old2 = "arms) remain not classifiable, and excluding them moves safety and eradication not at all and clinical success"
new2 = ("arms), and excluding them moves every one of the four pooled overall estimates: clinical "
        "success by " + M("NcSensClinicalSuccessDeltaAbs") + " percentage points ("
        + M("NcSensClinicalSuccessDropped") + " patients dropped), safety by "
        + M("NcSensSafetyDeltaAbs") + " (" + M("NcSensSafetyDropped") + "), eradication by "
        + M("NcSensEradicationDeltaAbs") + " (" + M("NcSensEradicationDropped")
        + "), and mortality by " + M("NcSensMortalityDeltaAbs") + " in the opposite direction ("
        + M("NcSensMortalityDropped") + "). No outcome is unaffected, and clinical success")

if old2 in s:
    s = s.replace(old2, new2, 1)
    print("  ok   duplicated clause removed; deltas replaced with pipeline values")
else:
    failures.append("duplicated 'remain not classifiable' clause")

p.write_text(s, encoding="utf-8", newline="\n")

if failures:
    print("")
    print("NOT APPLIED:")
    for f in failures:
        print("  " + f)
    sys.exit(1)
print("discussion sentences repaired")
