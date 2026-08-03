"""Import the local PICO screening spreadsheet into the repository.

WHY THIS EXISTS. scripts/R/14_prisma_counts.R states, as the explanation for why
the PRISMA screening-stage counts could not be derived, that "this review never
kept a machine-readable screening log". That is false. A structured log exists --
Cribado_Sistematico_COMPLETO_76_3.xlsx -- with a row per document and columns for
each PICO criterion, a final decision, and the verbatim text supporting it. It
has simply never been in the repository, so no script could see it and no referee
could check it.

That is the whole defect in miniature: the review's screening was better
documented than the manuscript claims, and none of the documentation was
version-controlled, which left an identification channel that could be described
but not audited.

WHAT THIS DOES. Converts the workbook to CSV under data/raw/ so the decisions are
versioned, diffable and citable. It normalises nothing and judges nothing: the
decisions are imported verbatim, including the one row whose decision reads
"EXCLUIDO (duplicado de #40)" rather than a bare EXCLUIDO, because collapsing
that into EXCLUIDO would destroy the reason.

The formula-bearing summary sheet is deliberately NOT imported. Its cells contain
Excel formulas rather than values, and a count that must be recomputed by a
spreadsheet engine is not a count this project can verify.

USAGE
    python scripts/import_screening_log.py "C:/path/to/Cribado_Sistematico_COMPLETO_76_3.xlsx"
"""
import csv
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
OUT = ROOT / "data" / "raw" / "local_screening_log.csv"


def main():
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    src = pathlib.Path(sys.argv[1])
    if not src.exists():
        sys.exit("workbook not found: %s" % src)

    try:
        import openpyxl
    except ImportError:
        sys.exit("openpyxl required: python -m pip install openpyxl")

    wb = openpyxl.load_workbook(str(src), read_only=True, data_only=True)
    sheet = next((s for s in wb.sheetnames if s.lower().startswith("cribado")), wb.sheetnames[0])
    ws = wb[sheet]

    rows = [r for r in ws.iter_rows(values_only=True) if any(c is not None for c in r)]
    if not rows:
        sys.exit("sheet %s is empty" % sheet)

    header = [str(h).replace("\n", " ").strip() if h is not None else "" for h in rows[0]]
    body = rows[1:]

    OUT.parent.mkdir(parents=True, exist_ok=True)
    with open(OUT, "w", encoding="utf-8", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(header)
        for r in body:
            w.writerow([
                str(c).replace("\n", " ").strip() if c is not None else ""
                for c in r
            ])

    # Report the decision distribution so the import is self-checking.
    try:
        di = header.index("Decisión final")
    except ValueError:
        di = None

    print("source sheet   :", sheet)
    print("records        :", len(body))
    if di is not None:
        counts = {}
        for r in body:
            k = str(r[di]).strip() if r[di] is not None else "(blank)"
            counts[k] = counts.get(k, 0) + 1
        print("decisions      :")
        for k, v in sorted(counts.items(), key=lambda kv: -kv[1]):
            print("   %3d  %s" % (v, k))
    print("\nwrote", OUT)


if __name__ == "__main__":
    main()
