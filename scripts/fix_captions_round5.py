"""Replace the last stale literals the round-5 corpus change left behind.

Found by classify_unmatched.py, which prints each unmatched numeric literal with
its context so the residue can be judged rather than counted. Four groups
survived as typed values and every one of them moved:

  - forest-plot captions describing "the 20 studies contributing clinical-success
    data (67 patients)" and "the 20 studies contributing safety data (81
    patients)" with a diamond at 16.0%. Both counts and the estimate are from a
    superseded corpus, and both captions also say "studies" where each plotted
    row is an ARM.
  - the overall clinical-success estimate quoted in a caption.
  - the pooled mortality proportion in the follow-up-horizon paragraph.
  - the naive-versus-cluster-robust standard errors, where the round-5 additions
    moved not only the values but the DIRECTION of one comparison, which is the
    part a reader reasons from.
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


swap("results.tex",
     "Each row is one of the 20 studies contributing clinical-success data (67 patients); markers "
     "show the study-specific proportion with 95" + BS + "% CI, the diamond shows the GLMM pooled "
     "estimate (76.1" + BS + "%, 95" + BS + "% CI 64.2--84.9" + BS + "%).",

     "Each row is one of the " + M("CsOverallArms") + "study-" + BS + "emph{arms} contributing "
     "clinical-success data (" + M("CsOverallK") + "studies, " + M("CsOverallN")
     + "patients); markers show the arm-specific proportion with 95" + BS + "% CI, the diamond "
     "shows the GLMM pooled estimate (" + M("CsOverallEstCI") + ").",
     "clinical-success forest caption: arms not studies, and the estimate")

swap("results.tex",
     "Each row is one of the 20 studies contributing safety data (81 patients); the GLMM diamond "
     "shows 16.0" + BS + "%",

     "Each row is one of the " + M("SafOverallArms") + "study-" + BS + "emph{arms} contributing "
     "safety data (" + M("SafOverallK") + "studies, " + M("SafOverallN") + "patients); the GLMM "
     "diamond shows " + M("SafOverallEst"),
     "safety forest caption: arms not studies, and the estimate")

swap("results.tex",
     "The pooled 10.4" + BS + "% is therefore an all-cause proportion",
     "The pooled " + M("MortOverallEst") + "is therefore an all-cause proportion",
     "pooled mortality in the follow-up-horizon paragraph")

swap("results.tex",
     "for clinical success overall, naive SE 0.243 versus 0.171 under clustering; for eradication "
     "overall, 0.258 versus 0.244)",

     "for clinical success overall, naive SE " + M("RveCsNaive") + "against "
     + M("RveCsRobust") + "under clustering, so the robust interval is "
     + BS + "emph{narrower}; for eradication overall, " + M("RveEradNaive") + "against "
     + M("RveEradRobust") + ", so it is " + BS + "emph{wider})",
     "cluster-robust standard errors, with the direction of each comparison stated")

if failures:
    print("")
    print("NOT APPLIED (%d):" % len(failures))
    for f in failures:
        print("  " + f)
    sys.exit(1)
print("")
print("captions and residual literals reconciled")
