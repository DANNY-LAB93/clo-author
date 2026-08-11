"""Export the stage-2 pool as RIS for import into Rayyan.

WHY RIS AND WHY RAYYAN. Screening moves to Rayyan (Ouzzani et al., Syst Rev 2016)
for three reasons that are methodological rather than convenience. It is the
tool this field cites, so the Methods can name it instead of describing a bespoke
procedure. It supports blind dual independent screening, which is the single
recurring criticism this review has not been able to answer. And its decision log
is native, so auditability stops depending on scripts written for this project.

WHAT IS EXPORTED. The records that survived stage 1, one RIS entry each, carrying
the PMID so every Rayyan decision maps back to the frozen corpus in
revision_sistematica/busqueda/screening_pubmed_union.csv. Without that mapping the exported decisions
could not be reconciled with the PRISMA counts.

WHAT PRISMA CALLS STAGE 1. PRISMA 2020's flow has a box for "records removed
before screening", explicitly including records marked ineligible by automation
tools. The 2,402 stage-1 exclusions belong there, with the rules named. They are
not screened records and must not be counted as such.

A NOTE ON RAYYAN'S OWN AI. Rayyan offers automated ranking and inclusion
suggestions. If those are used, that is model-assisted screening and requires the
same disclosure as any other -- naming the tool and stating that a human made
every final decision. Using Rayyan does not make the disclosure question go away;
it makes it a one-line answer instead of a paragraph.

USAGE
    python scripts/export_rayyan_ris.py
    python scripts/export_rayyan_ris.py --arm A_organism_first
    python scripts/export_rayyan_ris.py --chunk 2000
"""
import argparse
import csv
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
STAGE1 = ROOT / "revision_sistematica" / "cribado" / "screening_stage1.csv"
INDEX = ROOT / "quality_reports" / "corpus_identifier_index.txt"
OUTDIR = ROOT / "revision_sistematica" / "cribado" / "rayyan"

csv.field_size_limit(10_000_000)


def clean(s):
    """RIS is line-oriented: a newline inside a field silently truncates it."""
    return " ".join((s or "").split())


def ris_entry(r):
    out = ["TY  - JOUR"]
    out.append("TI  - " + clean(r["title"]))
    if r["abstract"]:
        out.append("AB  - " + clean(r["abstract"]))
    if r["first_author"]:
        out.append("AU  - " + clean(r["first_author"]))
    if r["year"]:
        out.append("PY  - " + clean(r["year"]))
    if r["journal"]:
        out.append("JO  - " + clean(r["journal"]))
    if r["doi"]:
        out.append("DO  - " + clean(r["doi"]))
    # PMID in three places: Rayyan reads different fields depending on the
    # importer it picks, and losing the id would break the mapping back to the
    # frozen corpus, which is the whole point of exporting it.
    out.append("AN  - " + r["pmid"])
    out.append("ID  - " + r["pmid"])
    out.append("UR  - https://pubmed.ncbi.nlm.nih.gov/%s/" % r["pmid"])
    if r["mesh"]:
        for kw in [k.strip() for k in r["mesh"].split(";") if k.strip()][:12]:
            out.append("KW  - " + clean(kw))
    out.append("ER  - ")
    return "\n".join(out)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--arm", default=None, help="A_organism_first | B_no_organism_block")
    ap.add_argument("--chunk", type=int, default=0, help="split into files of N records")
    args = ap.parse_args()

    if not STAGE1.exists():
        sys.exit("stage 1 not run: python scripts/screen_stage1_rules.py --apply")

    with open(STAGE1, encoding="utf-8", newline="") as fh:
        rows = [r for r in csv.DictReader(fh) if r["stage1"] == "ADVANCE"]

    if args.arm:
        rows = [r for r in rows if args.arm in (r["arms"] or "")]

    OUTDIR.mkdir(parents=True, exist_ok=True)
    stem = "rayyan_%s" % (args.arm or "stage2_pool")

    chunks = ([rows[i:i + args.chunk] for i in range(0, len(rows), args.chunk)]
              if args.chunk else [rows])
    written = []
    for i, ch in enumerate(chunks, 1):
        name = "%s.ris" % stem if len(chunks) == 1 else "%s_part%02d.ris" % (stem, i)
        path = OUTDIR / name
        path.write_text("\n\n".join(ris_entry(r) for r in ch) + "\n",
                        encoding="utf-8", newline="\n")
        written.append((path, len(ch)))

    # Known positives are in this pool. They are the calibration set: a screen
    # that excludes one has miscalibrated, and it is better to find that out on
    # a study whose eligibility is already settled than on an unknown one.
    known = {}
    for line in INDEX.read_text(encoding="utf-8").splitlines():
        if line.startswith("pmid:"):
            ident, _, sid = line.partition("\t")
            known[ident.split(":", 1)[1]] = sid.strip()
    present = sorted({known[r["pmid"]] for r in rows if r["pmid"] in known})

    print("records exported : %d" % len(rows))
    for path, n in written:
        print("   %-46s %5d records  %6.1f KB"
              % (path.relative_to(ROOT).as_posix(), n, path.stat().st_size / 1024))
    print()
    print("already-included studies inside this pool: %d" % len(present))
    print("  they are the calibration set -- if screening excludes one, the")
    print("  criteria are being applied more narrowly than the review's own.")
    print()
    print("Import into Rayyan as RIS. Keep the PMID visible: it is how every")
    print("decision maps back to revision_sistematica/busqueda/screening_pubmed_union.csv.")


if __name__ == "__main__":
    main()
