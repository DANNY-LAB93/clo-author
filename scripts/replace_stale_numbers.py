"""Replace every confirmed-wrong numeric literal in the manuscript with the
macro that generates it.

Each entry is asserted to be present exactly once before substitution, so a
pattern that has already been fixed, or that never matched, fails loudly rather
than silently doing nothing. Written as a file, not a heredoc: backslash
sequences in a non-raw Python string have corrupted these .tex files three
times.

The values on the left were verified against scripts/R/output/pooled_results.rds
and the generated tables; the discrepancies are recorded in the commit message.
"""
import pathlib
import sys

BS = chr(92)


def M(name):
    """A LaTeX macro reference."""
    return BS + name


root = pathlib.Path(__file__).resolve().parent.parent

# (file, old, new, note)
EDITS = [
    # ---- results.tex: overall synthesis paragraph --------------------------
    ("paper/sections/results.tex",
     "Of 36 outcome-stratum cells defined by the pre-specified three-way stratification, 13 met the threshold of at least 3 independent studies and 20 patients",
     "Of " + M("CellsTotal") + " outcome-stratum cells defined by the pre-specified four-way stratification, "
     + M("CellsPooled") + " met the threshold of at least 3 independent studies and 20 patients",
     "cell counts were 36/13/23 against a pipeline of 44/13/31; the axis count omitted DTR"),

    ("paper/sections/results.tex",
     "the remaining 23 are narrated in " + BS + "Cref{tab:not-pooled}",
     "the remaining " + M("CellsNotPooled") + " are narrated in " + BS + "Cref{tab:not-pooled}",
     "23 against 31 not-pooled cells"),

    ("paper/sections/results.tex",
     "Pooled clinical success across 23 studies (28 arms, 71 patients) was 76.1" + BS + "% (95" + BS + "% CI 64.2--84.9" + BS + "%;",
     "Pooled clinical success across " + M("CsOverallK") + " studies (" + M("CsOverallArms")
     + " arms, " + M("CsOverallN") + " patients) was " + M("CsOverallEst") + " ("
     + M("CsOverallCI") + ";",
     "correct as written, but literals replaced so they cannot go stale"),

    ("paper/sections/results.tex",
     "Pooled eradication across 19 studies (23 arms, 59 patients) was 57.8" + BS + "% (95" + BS + "% CI 30.2--81.2" + BS + "%), pooled safety across 17 studies (22 arms, 52 patients) was 19.2" + BS + "% (95" + BS + "% CI 10.3--33.1" + BS + "%), and pooled mortality across 24 studies (30 arms, 67 patients) was 10.4" + BS + "% (95" + BS + "% CI 4.9--20.9" + BS + "%).",
     "Pooled eradication across " + M("EradOverallK") + " studies (" + M("EradOverallArms")
     + " arms, " + M("EradOverallN") + " patients) was " + M("EradOverallEst") + " ("
     + M("EradOverallCI") + "), pooled safety across " + M("SafOverallK") + " studies ("
     + M("SafOverallArms") + " arms, " + M("SafOverallN") + " patients) was " + M("SafOverallEst")
     + " (" + M("SafOverallCI") + "), and pooled mortality across " + M("MortOverallK")
     + " studies (" + M("MortOverallArms") + " arms, " + M("MortOverallN") + " patients) was "
     + M("MortOverallEst") + " (" + M("MortOverallCI") + ").",
     "literals replaced"),

    ("paper/sections/results.tex",
     "$" + BS + "tau^2$ is estimated at exactly zero in 11 of the 13 pooled cells",
     "$" + BS + "tau^2$ is estimated at exactly zero in 11 of the " + M("CellsPooled") + " pooled cells",
     "denominator from the pipeline"),

    ("paper/sections/results.tex",
     "76.1" + BS + "% is 54/71, 19.2" + BS + "% is 10/52, 10.4" + BS + "% is 7/67",
     M("CsOverallEst") + " is " + M("CsOverallEvents") + "/" + M("CsOverallN") + ", "
     + M("SafOverallEst") + " is " + M("SafOverallEvents") + "/" + M("SafOverallN") + ", "
     + M("MortOverallEst") + " is " + M("MortOverallEvents") + "/" + M("MortOverallN"),
     "crude fractions now derived from the same objects as the estimates"),

    ("paper/sections/results.tex",
     "With 24 of 31 arms contributing a single patient, a random intercept is identified only by the 7 multi-patient arms",
     "With " + M("SinglePatientArms") + " of " + M("ArmsAnalysed") + " arms contributing a single "
     "patient, a random intercept is identified only by the " + M("MultiPatientArms")
     + " multi-patient arms",
     "literals replaced"),

    ("paper/sections/results.tex",
     "The 7 deaths among 67 patients accrue over windows",
     "The " + M("MortOverallEvents") + " deaths among " + M("MortOverallN")
     + " patients accrue over windows",
     "literals replaced"),

    ("paper/sections/results.tex",
     "carries a wide interval ($" + BS + "tau^2=2.11$)",
     "carries a wide interval ($" + BS + "tau^2=" + M("EradOverallTau") + "$)",
     "tau^2 was 2.11 in prose against 2.198 in the table"),

    # ---- results.tex: the stale safety paragraph ---------------------------
    ("paper/sections/results.tex",
     "Pooled safety (at least one adverse event), across 20 studies (81 patients), is 16.0" + BS + "% (95" + BS + "% CI 10.3--33.1" + BS + "%; $" + BS + "tau^2=0.085$;",
     "Pooled safety (at least one adverse event), across " + M("SafOverallK") + " studies ("
     + M("SafOverallArms") + " arms, " + M("SafOverallN") + " patients), is " + M("SafOverallEst")
     + " (" + M("SafOverallCI") + "; $" + BS + "tau^2=" + M("SafOverallTau") + "$;",
     "reported 16.0%/20 studies/81 patients/tau2=0.085 -- every field a round-2 value"),

    ("paper/sections/results.tex",
     "Freeman-Tukey gives 7.9" + BS + "% and logit-DerSimonian-Laird gives 26.8" + BS + "% against the GLMM's 16.0" + BS + "% (" + BS + "Cref{tab:sensitivity}), and the fixed-effect model converges at 26.8" + BS + "% too.",
     "Freeman-Tukey gives " + M("SafOverallFT") + " and logit-DerSimonian-Laird gives "
     + M("SafOverallDL") + " against the GLMM's " + M("SafOverallEst") + " ("
     + BS + "Cref{tab:sensitivity}), and the fixed-effect model converges at "
     + M("SafOverallFE") + ". The Freeman-Tukey value lies "
     + BS + "emph{outside} the primary interval, which is reported here rather than left to the "
     "table: an interval that excludes the estimate an equally defensible transformation returns "
     "on the same data is not a 95" + BS + "% interval for any quantity a reader can use.",
     "sensitivity triplet was 7.9/26.8/16.0 against 8.4/27.4/19.2"),

    # ---- discussion.tex ---------------------------------------------------
    ("paper/sections/discussion.tex",
     "The GLMM estimate (19.2" + BS + "%, 95" + BS + "% CI 10.3--33.1" + BS + "%; Section~" + BS + "ref{sec:results-synthesis}) is bracketed by its sensitivity models (Freeman-Tukey 7.9" + BS + "%, logit-DerSimonian-Laird and fixed-effect both 26.8" + BS + "%)",
     "The GLMM estimate (" + M("SafOverallEstCI") + "; Section~" + BS + "ref{sec:results-synthesis}) "
     "is bracketed by its sensitivity models (Freeman-Tukey " + M("SafOverallFT")
     + ", logit-DerSimonian-Laird " + M("SafOverallDL") + ", fixed-effect " + M("SafOverallFE") + ")",
     "same stale triplet repeated in the Discussion"),
]

changed = {}
missing = []

for rel, old, new, note in EDITS:
    p = root / rel
    s = p.read_text(encoding="utf-8")
    count = s.count(old)
    if count == 0:
        missing.append((rel, note, old[:70]))
        continue
    if count > 1:
        missing.append((rel, note + "  [AMBIGUOUS: %d matches]" % count, old[:70]))
        continue
    s = s.replace(old, new, 1)
    p.write_text(s, encoding="utf-8", newline="\n")
    changed[rel] = changed.get(rel, 0) + 1
    print("  ok   " + note)

print("")
for rel, cnt in sorted(changed.items()):
    print("%-34s %d replacements" % (rel, cnt))

if missing:
    print("")
    print("NOT APPLIED (" + str(len(missing)) + "):")
    for rel, note, frag in missing:
        print("  " + rel + " :: " + note)
        print("      looked for: " + frag + "...")
    sys.exit(1)

print("")
print("all edits applied")
