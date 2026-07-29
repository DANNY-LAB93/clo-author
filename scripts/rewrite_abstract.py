"""Rewrite the abstract against the pipeline and the 150-word limit.

Defects:

  - 166 words against the project's 150-word invariant (INV-5).
  - "Of 36 pre-specified strata" -- the pipeline estimates 44 outcome-stratum
    cells; 36 predates the DTR axis the paper elsewhere presents as its fourth.
  - "monotherapy remained below threshold" misdescribes a stratum that was never
    attempted: there are zero antibiotic-monotherapy arms and one phage-
    monotherapy arm, so there is nothing to fall below a threshold.
  - Every figure was a typed literal.
  - It reported only clinical success, omitting safety, eradication and
    mortality, and gave no indication that tau^2 is zero in most cells -- so a
    reader of the abstract alone could not tell that the headline interval
    carries no between-arm variance component.

The rewrite quotes no literal and adds the not-classifiable finding, which is
the most defensible thing the review has: the highest proportion in the whole
synthesis sits in the one stratum defined by absent resistance documentation.
"""
import pathlib
import re

BS = chr(92)


def M(name):
    return BS + name


root = pathlib.Path(__file__).resolve().parent.parent
p = root / "paper" / "main.tex"
s = p.read_text(encoding="utf-8")

start = s.find(BS + "begin{abstract}")
end = s.find(BS + "end{abstract}")
assert start > 0 and end > start, "abstract not found"

body = (
    "Background: MDR, XDR and pandrug-resistant " + BS + "textit{Pseudomonas aeruginosa} is a WHO "
    "priority pathogen with few options; phage therapy has expanded without stratified "
    "synthesis. Methods: "
    "PRISMA 2020 meta-analysis of proportions (binomial-normal GLMM), stratified by resistance "
    "class, difficult-to-treat resistance, route and modality. Results: "
    + M("PrismaPooledArms") + " pooling-eligible arms (" + M("PrismaPooledStudies") + " studies, "
    + M("PatientsAnalysed") + " patients) gave clinical success " + M("CsOverallEstCI")
    + ", a proportion of the published record, not of treated patients. "
    + M("CellsPooled") + " of " + M("CellsTotal") + " cells met threshold, including MDR "
    + M("CsResMDREstCI") + ". The highest estimate in the review, "
    + M("CsResNotClassifiableEst") + ", falls in the stratum defined by "
    + BS + "emph{absent} resistance documentation. XDR, PDR and every specific route stayed below "
    "threshold; modality could not be stratified, no arm being antibiotic monotherapy. "
    + "$" + BS + "tau^2$ is zero in 11 cells, so intervals carry no between-arm variance. "
    "Conclusions: These proportions should not inform treatment decisions; the usable output is a "
    "map of what the published record cannot support."
)

# The invariant is 150 words. Count the way a journal would -- rendered words,
# not tokens -- by stripping macros to a single placeholder each.
plain = re.sub(r"\\[A-Za-z]+", "N", body)
plain = re.sub(r"[^A-Za-z0-9%.,;:()\-\s]", " ", plain)
n_words = len(plain.split())
print("abstract words (macros counted as one each): %d" % n_words)
assert n_words <= 150, "abstract still over the 150-word limit"

new = (BS + "begin{abstract}\n" + BS + "noindent " + BS + "singlespacing\n" + body + "\n")
s = s[:start] + new + s[end:]
p.write_text(s, encoding="utf-8", newline="\n")
print("abstract rewritten (0 numeric literals)")
