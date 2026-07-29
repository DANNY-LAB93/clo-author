"""Rebuild the PRISMA flow diagram's terminal boxes from pipeline macros.

Four defects, all found independently by both round-5 referees:

  1. 39 assessed minus 9 excluded = 30, against 31 included. The one arithmetic
     identity every referee checks with a calculator.
  2. The eligibility box itemised nine studies from the Scopus channel; the
     caption names ten from that channel and the Results text says ten twice.
  3. The included box said "4 at peer review round 2" and then listed five.
  4. The pending box recorded Karn 2024 and Stanley 2025 as resolved and
     excluded, while the caption said both remained outstanding and were folded
     into neither count. They are excluded, and are now counted as such.

Every number comes from 14_prisma_counts.R, which derives the assessed total as
included + excluded and asserts the identity. The per-channel itemisation
accounts for 40 of the 42; the remaining 2 records' channel of origin was not
recorded at screening, and the box says so rather than distributing them to make
the sum close.
"""
import pathlib

BS = chr(92)
NL = chr(10)


def M(name):
    return BS + name


def replace_node(text, node_id, new_line):
    """Replace the whole line defining a tikz node.

    An earlier version matched up to the first semicolon after the node id.
    Node text can CONTAIN a semicolon -- the pending box did ("Maddocks 2019 was
    in this category; its outcome data...") -- so the match truncated mid-node
    and left the original tail attached, producing 56 fatal errors. Each node
    occupies one line, so operate on lines.
    """
    out, hits = [], 0
    for line in text.split(NL):
        if line.lstrip().startswith(BS + "node") and ("(" + node_id + ")") in line:
            out.append(new_line)
            hits += 1
        else:
            out.append(line)
    assert hits == 1, "expected exactly one node (%s), found %d" % (node_id, hits)
    return NL.join(out)


root = pathlib.Path(__file__).resolve().parent.parent
p = root / "paper" / "figures" / "phage_therapy_mdr_pseudomonas" / "prisma_flow_diagram.tex"
s = p.read_text(encoding="utf-8")
orig = s

BULLET = BS + BS + "$" + BS + "bullet$ "

elig_new = (
    BS + "node[wide] (elig) at (6.0,-6.3) {" + BS + "textbf{Assessed for full-text eligibility: "
    "$n=" + M("PrismaAssessed") + "$ records} (derived as " + M("PrismaIncludedStudies")
    + " included $+$ " + M("PrismaExcluded") + " excluded). Channel of origin is documented for "
    + M("PrismaItemised") + ": 5 citation-chased $+$ 8 via the PDF corpus $+$ 6 via "
    "discovery-phase scoping $+$ 10 via the native Scopus search $+$ 5 held records re-confirmed "
    "$+$ 4 landmark cases flagged at peer review $+$ 2 further records named at peer review, "
    "round 2. The remaining " + M("PrismaShortfall") + " were not attributed to a channel at the "
    "time of screening and are not assigned to one here.};"
)

excl_new = (
    BS + "node[box, text width=4.6cm, minimum height=4.6cm] (excl) at (0.6,-9.1) {"
    + BS + "textbf{Excluded, $n=" + M("PrismaExcluded") + "$}"
    + BULLET + "Krakhotkin 2025 -- wrong pathogen"
    + BULLET + "Cano 2021 -- wrong pathogen (" + BS + "textit{Klebsiella})"
    + BULLET + "Rhoads 2009 -- no antibiotic comparator"
    + BULLET + "Dan 2023 -- duplicate (Aslam)"
    + BULLET + "Van Nieuwenhuyse 2022 -- duplicate (Pirnay consortium)"
    + BULLET + "Zurabov 2023, Rubalskii 2020 -- multi-pathogen, not separable"
    + BULLET + "Hayakawa 2025 -- multi-pathogen feasibility"
    + BULLET + "Chung 2025 -- review/perspective"
    + BULLET + "Karn 2024 -- multi-pathogen, no " + BS + "textit{Pseudomonas} breakdown"
    + BULLET + "Stanley 2025 (CYPHY, NCT04684641) -- population rule};"
)

pend_new = (
    BS + "node[box, text width=4.6cm, minimum height=4.6cm] (pend) at (6.0,-9.1) {"
    + BS + "textbf{Reports not retrieved, $n=1$}" + BS + BS
    + "Maddocks 2019: full text never obtained (paywalled, no PMC deposit). Outcome data were "
    "recovered from two concordant secondary syntheses, a weaker provenance than every other "
    "included study." + BS + BS + BS + "smallskip "
    + BS + "textbf{Pending / unresolved, $n=0$}" + BS + BS
    + "Karn 2024 and Stanley 2025 were both resolved at peer review and are counted among the "
    "exclusions at left.};"
)

incl_new = (
    BS + "node[box, text width=4.6cm, minimum height=4.6cm] (incl) at (11.4,-9.1) {"
    + BS + "textbf{Included in the analytic dataset:}" + BS + BS
    + BS + "textbf{$n=" + M("PrismaIncludedStudies") + "$ studies, "
    + M("PrismaIncludedArms") + " study-arms}" + BS + BS + BS + "smallskip "
    "Ten added by the native Scopus search; 2 landmark cases at peer review (Chan 2018, "
    "Arya 2026); 5 at peer review round 2 (Ferry 2021, Maddocks 2019, Aslam 2020, Cesta 2023, "
    "Khatami 2021).};"
)

s = replace_node(s, "elig", elig_new)
s = replace_node(s, "excl", excl_new)
s = replace_node(s, "pend", pend_new)
s = replace_node(s, "incl", incl_new)

s = s.replace("$n=25$ studies, 31 study-arms.",
              "$n=" + M("PrismaPooledStudies") + "$ studies, "
              + M("PrismaPooledArms") + " study-arms.")
s = s.replace("Seven of the 38 analytic arms",
              "Seven of the " + M("PrismaIncludedArms") + " analytic arms")

assert s != orig, "no substitutions applied"
p.write_text(s, encoding="utf-8", newline=NL)
print("PRISMA boxes rebuilt from macros")
print("  assessed = included + excluded, asserted in 14_prisma_counts.R")
print("  channel shortfall printed rather than absorbed")
