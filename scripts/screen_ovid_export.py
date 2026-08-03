"""Split an Ovid export into 'already in this corpus' and 'never screened'.

WHY THIS EXISTS. Ngauy 2026 was re-screened as new during round 5 although it was
already included, because its extraction citation records page numbers rather
than a PMID and no regex could match it. The fix was
scripts/check_identifier_traceability.R, which guarantees every included study
carries a resolvable identifier and emits
quality_reports/corpus_identifier_index.txt. This script is the other half: it
consumes that index so an incoming search result can be classified mechanically
instead of by eye.

WHAT IT DOES NOT DO. It does not decide eligibility. A record it reports as
"never screened" is a record to screen, not a record to include -- the
Population, Intervention and design criteria in Section sec:methods-eligibility
still have to be applied by a human to the full text. The only question this
answers is the one that is mechanical: have we seen this record before?

USAGE
    python scripts/screen_ovid_export.py data/raw/ovid_export_2026-08-03.ris
    python scripts/screen_ovid_export.py <file> --out quality_reports/ovid_screen.md

Accepts RIS (Ovid's default) or CSV. Identifier extraction is deliberately
liberal: every field of every record is scanned for a DOI, PMID or PMC id, the
same way the R check scans free-text extraction citations. A false match here
costs a record being flagged as already-seen, which the worksheet makes visible,
whereas a missed match silently re-screens a study we already hold.
"""
import argparse
import csv
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
INDEX = ROOT / "quality_reports" / "corpus_identifier_index.txt"

ID_PATTERNS = {
    "pmid": re.compile(r"(?:PMID|MEDLINE)[: ]*(\d{7,8})", re.I),
    "pmc":  re.compile(r"PMC(\d{6,8})", re.I),
    "doi":  re.compile(r"(10\.\d{4,9}/[^\s,;)}\]]+)"),
}


def normalise(kind, value):
    """Match the normalisation the index generator applies, or lookups silently miss."""
    if kind == "doi":
        value = re.sub(r"[.,;:)\]]+$", "", value)
    return (kind + ":" + value).lower()


def ids_in(text):
    out = []
    for kind, pat in ID_PATTERNS.items():
        for v in pat.findall(text or ""):
            out.append(normalise(kind, v))
    return list(dict.fromkeys(out))


# ---- readers ----------------------------------------------------------------
def read_ris(text):
    """Ovid RIS. Records are separated by ER; tags are 'XX  - value'."""
    records, cur = [], {}
    for line in text.splitlines():
        m = re.match(r"^([A-Z][A-Z0-9])\s{2}-\s?(.*)$", line)
        if m:
            tag, val = m.group(1), m.group(2).strip()
            if tag == "ER":
                if cur:
                    records.append(cur)
                cur = {}
            else:
                cur.setdefault(tag, []).append(val)
        elif cur and line.strip():
            # continuation of the previous tag's value
            last = list(cur)[-1] if cur else None
            if last:
                cur[last][-1] += " " + line.strip()
    if cur:
        records.append(cur)

    out = []
    for r in records:
        first = lambda *tags: next(
            (r[t][0] for t in tags if t in r and r[t]), "")
        out.append({
            "title": first("TI", "T1"),
            "year": re.sub(r"\D", "", first("PY", "Y1", "DA"))[:4],
            "author": first("AU", "A1"),
            "journal": first("JO", "JF", "T2", "JA"),
            "blob": "\n".join(v for vs in r.values() for v in vs),
        })
    return out


def read_csv_export(text):
    rows = list(csv.DictReader(text.splitlines()))
    out = []
    for r in rows:
        low = {(k or "").strip().lower(): (v or "") for k, v in r.items()}
        pick = lambda *names: next(
            (low[n] for n in names if n in low and low[n]), "")
        out.append({
            "title": pick("title", "ti", "article title"),
            "year": re.sub(r"\D", "", pick("year", "publication year", "py"))[:4],
            "author": pick("author", "authors", "au"),
            "journal": pick("journal", "source", "publication"),
            "blob": "\n".join(f"{k}: {v}" for k, v in low.items()),
        })
    return out


# ---- main -------------------------------------------------------------------
def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("export", help="Ovid .ris or .csv export")
    ap.add_argument("--out", default=None, help="write a screening worksheet here")
    args = ap.parse_args()

    path = pathlib.Path(args.export)
    if not path.is_absolute():
        path = ROOT / path
    if not path.exists():
        sys.exit("export not found: %s" % path)
    if not INDEX.exists():
        sys.exit("corpus index missing -- run scripts/check_identifier_traceability.R first")

    # corpus index: identifier -> study_id
    corpus = {}
    for line in INDEX.read_text(encoding="utf-8").splitlines():
        if not line.strip() or line.startswith("#"):
            continue
        ident, _, sid = line.partition("\t")
        corpus[ident.strip().lower()] = sid.strip()

    text = path.read_text(encoding="utf-8", errors="replace")
    records = read_csv_export(text) if path.suffix.lower() == ".csv" else read_ris(text)
    if not records:
        sys.exit("parsed 0 records from %s -- wrong format?" % path.name)

    seen, new, no_id = [], [], []
    for rec in records:
        found = ids_in(rec["blob"])
        hits = {i: corpus[i] for i in found if i in corpus}
        rec["ids"] = found
        if hits:
            rec["matches"] = hits
            seen.append(rec)
        elif not found:
            no_id.append(rec)          # cannot be classified either way
        else:
            new.append(rec)

    print("records parsed              :", len(records))
    print("already in the corpus       :", len(seen))
    print("never screened              :", len(new))
    print("no identifier in the record :", len(no_id),
          "  <-- screen these by hand; the export carries nothing to match on")
    print()
    print("distinct corpus studies hit :",
          len({s for r in seen for s in r["matches"].values()}), "of",
          len(set(corpus.values())))

    if args.out:
        out = pathlib.Path(args.out)
        if not out.is_absolute():
            out = ROOT / out
        lines = [
            "# Ovid export screening worksheet",
            "",
            "Source: `%s`" % path.name,
            "",
            "Classified against `quality_reports/corpus_identifier_index.txt`.",
            "**Already in the corpus** is mechanical and final. **Never screened**",
            "means exactly that -- these still need eligibility applied at full text.",
            "",
            "| | n |",
            "|---|---|",
            "| records parsed | %d |" % len(records),
            "| already in the corpus | %d |" % len(seen),
            "| never screened | %d |" % len(new),
            "| no identifier to match on | %d |" % len(no_id),
            "",
            "## Never screened — decide eligibility on each",
            "",
            "| # | Year | First author | Title | Journal | Identifier | Decision |",
            "|---|------|--------------|-------|---------|-----------|----------|",
        ]
        for i, r in enumerate(sorted(new, key=lambda x: (x["year"], x["title"])), 1):
            lines.append("| %d | %s | %s | %s | %s | `%s` |  |" % (
                i, r["year"] or "?", (r["author"] or "?")[:28],
                (r["title"] or "?").replace("|", "/")[:90],
                (r["journal"] or "?")[:34],
                r["ids"][0] if r["ids"] else ""))

        if no_id:
            lines += ["", "## No identifier — screen by hand", "",
                      "| # | Year | First author | Title |",
                      "|---|------|--------------|-------|"]
            for i, r in enumerate(no_id, 1):
                lines.append("| %d | %s | %s | %s |" % (
                    i, r["year"] or "?", (r["author"] or "?")[:28],
                    (r["title"] or "?").replace("|", "/")[:90]))

        lines += ["", "## Already in the corpus — no action", ""]
        for r in sorted(seen, key=lambda x: sorted(x["matches"].values())):
            lines.append("- %s (%s) -> **%s**" % (
                (r["title"] or "?")[:80], r["year"] or "?",
                ", ".join(sorted(set(r["matches"].values())))))

        out.write_text("\n".join(lines) + "\n", encoding="utf-8")
        print("\nworksheet written to", out)


if __name__ == "__main__":
    main()
