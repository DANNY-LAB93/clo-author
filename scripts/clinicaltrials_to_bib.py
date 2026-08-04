"""Convert the ClinicalTrials.gov result set to BibTeX.

WHY A SEPARATE FILE AND NOT Bibliography_base.bib. These are search results, not
cited references. Merging 121 registry records into the manuscript's bibliography
would put entries there that nothing cites, and the citation-coverage gate exists
precisely to keep that file in one-to-one correspondence with what the paper
uses. Entries move across by hand, one at a time, when a trial is actually cited.

ESCAPING. Registry titles carry &, %, _, # and registered-trademark symbols, and
an unescaped % in a .bib field silently truncates the rest of the line -- biber
then emits a corrupted .bbl and LaTeX reports the damage somewhere else entirely,
which has already cost this project a debugging session. Every field is escaped
here, backslash first so the other replacements are not re-escaped.

Registry records are @misc: they are protocol registrations, not articles. A
trial with a publication should be cited as the publication, with the NCT in a
note -- which is how the four already in this corpus are handled.

USAGE
    python scripts/clinicaltrials_to_bib.py
    python scripts/clinicaltrials_to_bib.py --pseudomonas-only
"""
import argparse
import csv
import pathlib
import re

ROOT = pathlib.Path(__file__).resolve().parent.parent
SRC = ROOT / "data" / "raw" / "clinicaltrials_gov.csv"
INDEX = ROOT / "quality_reports" / "corpus_identifier_index.txt"

# Backslash MUST be first, or every subsequent replacement gets re-escaped.
ESCAPES = [
    ("\\", r"\textbackslash{}"),
    ("&", r"\&"), ("%", r"\%"), ("$", r"\$"), ("#", r"\#"),
    ("_", r"\_"), ("{", r"\{"), ("}", r"\}"),
    ("~", r"\textasciitilde{}"), ("^", r"\textasciicircum{}"),
]


def tex(s):
    s = " ".join((s or "").split())
    for a, b in ESCAPES:
        s = s.replace(a, b)
    return s


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--pseudomonas-only", action="store_true")
    args = ap.parse_args()

    with open(SRC, encoding="utf-8", newline="") as fh:
        rows = list(csv.DictReader(fh))

    in_corpus = {l.split("\t")[0].split(":", 1)[1].upper()
                 for l in INDEX.read_text(encoding="utf-8").splitlines()
                 if l.startswith("nct:")}

    def mentions_pa(r):
        blob = r["conditions"] + " " + r["interventions"] + " " + r["briefTitle"]
        return re.search(r"pseudomonas|aeruginosa", blob, re.I) is not None

    sel = [r for r in rows if mentions_pa(r)] if args.pseudomonas_only else rows
    out = ROOT / "data" / "raw" / (
        "clinicaltrials_pseudomonas.bib" if args.pseudomonas_only
        else "clinicaltrials_gov.bib")

    entries = []
    for r in sorted(sel, key=lambda x: x["nct_id"]):
        nct = r["nct_id"]
        year = (re.search(r"(\d{4})", r.get("date", "")) or [None, ""])[1] \
            if r.get("date") else ""
        sponsor = tex(r.get("name", "")) or "Unknown sponsor"
        note_bits = [
            "ClinicalTrials.gov registry record",
            "status: " + tex(r.get("overallStatus", "")),
            "study type: " + tex(r.get("studyType", "")),
        ]
        if r.get("phases"):
            note_bits.append("phase: " + tex(r["phases"]))
        if r.get("count"):
            note_bits.append("enrolment: " + tex(r["count"]))
        if r.get("conditions"):
            note_bits.append("conditions: " + tex(r["conditions"]))
        if r.get("interventions"):
            note_bits.append("interventions: " + tex(r["interventions"])[:300])
        note_bits.append("retrieved 2026-08-03")
        if nct in in_corpus:
            note_bits.append("ALREADY IN THIS REVIEW'S CORPUS")

        # Omit `year` entirely when the registry gives no start date. Writing
        # "n.d." makes biber warn that the legacy year field is not an integer
        # and sorts those entries unpredictably; an absent field is what
        # biblatex expects for an undated work. Five expanded-access records
        # have no start date, which is normal -- they are open protocols.
        entries.append("\n".join([x for x in [
            "@misc{%s," % nct,
            "  author       = {{%s}}," % sponsor,
            "  title        = {{%s}}," % tex(r["briefTitle"]),
            ("  year         = {%s}," % year) if year else None,
            "  howpublished = {ClinicalTrials.gov identifier: %s}," % nct,
            "  url          = {https://clinicaltrials.gov/study/%s}," % nct,
            "  urldate      = {2026-08-03},",
            "  note         = {%s}" % "; ".join(note_bits),
            "}",
        ] if x is not None]))

    header = [
        "%% ClinicalTrials.gov search results -- GENERATED, do not edit by hand.",
        "%% Written by scripts/clinicaltrials_to_bib.py from data/raw/clinicaltrials_gov.csv",
        "%% Arm A: condition 'Pseudomonas aeruginosa' AND intervention (bacteriophage OR phage) -- 17",
        "%% Arm B: intervention (bacteriophage OR phage), all conditions -- 121",
        "%% Retrieved 2026-08-03 via the ClinicalTrials.gov v2 API. No date filter:",
        "%% registration precedes publication.",
        "%% These are SEARCH RESULTS, not cited references. Move an entry into",
        "%% Bibliography_base.bib only when the manuscript actually cites it.",
        # "%%" inside a %-formatted string collapses to one "%", which made this
        # header line differ from every other one. Concatenate instead.
        "%% Entries in this file: " + str(len(entries)),
        "",
    ]
    out.write_text("\n".join(header) + "\n\n".join(entries) + "\n",
                   encoding="utf-8", newline="\n")

    n_corpus = sum(1 for r in sel if r["nct_id"] in in_corpus)
    print("entries written        : %d" % len(entries))
    print("already in the corpus  : %d" % n_corpus)
    print("candidates to screen   : %d" % (len(entries) - n_corpus))
    print("\nwrote", out)


if __name__ == "__main__":
    main()
