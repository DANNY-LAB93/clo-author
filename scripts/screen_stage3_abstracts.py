"""Stage 3: abstract screening of the records that survived title screening.

At title stage the rule was permissive -- reviews advanced, because a review can
be the only published account of a case series and a title rarely says whether
one is inside. At abstract stage that latitude closes: an abstract states the
design, so a review with no primary patient data can now be excluded, and a
laboratory study that survived an ambiguous title can be settled.

Decisions go to their own log, separate from stage 2, so the two stages stay
distinguishable in the PRISMA flow. Same rules as stage 2 otherwise: --by is
mandatory, every decision carries a reason, corrections are appended with
--override and the last row per PMID wins.

Verdicts:
  FULLTEXT  -- retrieve and assess the full text
  EXCLUDE   -- with a reason

USAGE
    python scripts/screen_stage3_abstracts.py --status
    python scripts/screen_stage3_abstracts.py --next 60
    python scripts/screen_stage3_abstracts.py --record d.tsv --by "..."
    python scripts/screen_stage3_abstracts.py --audit
"""
import argparse
import csv
import datetime
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
STAGE1 = ROOT / "data" / "raw" / "screening_stage1.csv"
STAGE2 = ROOT / "data" / "raw" / "screening_stage2_decisions.csv"
LOG = ROOT / "data" / "raw" / "screening_stage3_decisions.csv"
INDEX = ROOT / "quality_reports" / "corpus_identifier_index.txt"

csv.field_size_limit(10_000_000)
FIELDS = ["pmid", "verdict", "reason", "decided_by", "decided_at"]
VERDICTS = {"FULLTEXT", "EXCLUDE"}

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass


def load_pool():
    """Records that ADVANCED at stage 2, with their stage-1 metadata."""
    with open(STAGE1, encoding="utf-8", newline="") as fh:
        meta = {r["pmid"]: r for r in csv.DictReader(fh)}
    adv = {}
    with open(STAGE2, encoding="utf-8", newline="") as fh:
        for r in csv.DictReader(fh):
            adv[r["pmid"]] = r          # last row wins; corrections supersede
    return [meta[p] for p, d in adv.items()
            if d["verdict"] == "ADVANCE" and p in meta]


def load_log():
    if not LOG.exists():
        return {}
    with open(LOG, encoding="utf-8", newline="") as fh:
        out = {}
        for r in csv.DictReader(fh):
            out[r["pmid"]] = r
        return out


def known_pmids():
    out = {}
    for line in INDEX.read_text(encoding="utf-8").splitlines():
        if line.startswith("pmid:"):
            ident, _, sid = line.partition("\t")
            out[ident.split(":", 1)[1]] = sid.strip()
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--status", action="store_true")
    ap.add_argument("--next", type=int, default=0)
    ap.add_argument("--chars", type=int, default=380,
                    help="abstract characters to print per record")
    ap.add_argument("--record", default=None)
    ap.add_argument("--by", default=None)
    ap.add_argument("--override", action="store_true")
    ap.add_argument("--audit", action="store_true")
    args = ap.parse_args()

    pool = load_pool()
    done = load_log()

    if args.record:
        if not args.by:
            sys.exit("--by is mandatory: every decision records who made it")
        src = pathlib.Path(args.record)
        if not src.is_absolute():
            src = ROOT / src
        now = datetime.datetime.now().isoformat(timespec="seconds")
        valid = {r["pmid"] for r in pool}
        rows, bad = [], []
        for ln in src.read_text(encoding="utf-8").splitlines():
            if not ln.strip() or ln.lstrip().startswith("#"):
                continue
            parts = ln.rstrip("\n").split("\t")
            if len(parts) < 3:
                bad.append(("malformed", ln[:60])); continue
            pmid, verdict, reason = parts[0].strip(), parts[1].strip().upper(), parts[2].strip()
            if pmid not in valid:
                bad.append(("not in stage-3 pool", pmid)); continue
            if verdict not in VERDICTS:
                bad.append(("bad verdict", "%s %s" % (pmid, verdict))); continue
            if pmid in done and not args.override:
                bad.append(("already decided", pmid)); continue
            rows.append({"pmid": pmid, "verdict": verdict, "reason": reason,
                         "decided_by": args.by, "decided_at": now})
        if bad:
            print("rejected %d line(s):" % len(bad))
            for why, what in bad[:10]:
                print("   %-22s %s" % (why, what))
        if rows:
            exists = LOG.exists()
            with open(LOG, "a", encoding="utf-8", newline="") as fh:
                w = csv.DictWriter(fh, fieldnames=FIELDS)
                if not exists:
                    w.writeheader()
                w.writerows(rows)
            print("recorded %d decision(s) by %s" % (len(rows), args.by))
        done = load_log()

    if args.audit:
        known = known_pmids()
        wrong = [(p, known[p], done[p]["reason"]) for p in known
                 if p in done and done[p]["verdict"] == "EXCLUDE"]
        print("known positives decided at stage 3:",
              sum(1 for p in known if p in done))
        if wrong:
            print("EXCLUDED IN ERROR -- a known included study was screened out:")
            for p, sid, why in wrong:
                print("   %-9s %-24s %s" % (p, sid, why))
            sys.exit(1)
        print("no known included study has been excluded at stage 3.")
        return

    n_ft = sum(1 for r in done.values() if r["verdict"] == "FULLTEXT")
    n_ex = sum(1 for r in done.values() if r["verdict"] == "EXCLUDE")
    print("stage-3 pool : %d" % len(pool))
    print("decided      : %d  (FULLTEXT %d / EXCLUDE %d)" % (len(done), n_ft, n_ex))
    print("remaining    : %d" % (len(pool) - len(done)))

    if args.next:
        todo = sorted([r for r in pool if r["pmid"] not in done],
                      key=lambda r: (r["year"], r["pmid"]))[:args.next]
        print("\n# next %d records -- decide FULLTEXT or EXCLUDE" % len(todo))
        for r in todo:
            ab = " ".join((r["abstract"] or "").split())
            print("\n%s | %s | %s" % (r["pmid"], r["year"], " ".join(r["title"].split())[:130]))
            print("   %s" % (ab[:args.chars] if ab else "(no abstract)"))


if __name__ == "__main__":
    main()
