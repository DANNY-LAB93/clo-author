"""Stage 2: title/abstract screening, one decision per record, resumable.

WHY A HARNESS RATHER THAN A SCRIPT THAT DECIDES. Stage 1 was rules, and rules can
be re-run. Stage 2 is judgement, and judgement has to be recorded because it
cannot be re-derived. Every decision written here carries the record it applies
to, the verdict, a reason, and who made it. That is the difference between this
screen and the undeclared one this review already has to answer for.

WHO DECIDES. The `--by` field is mandatory and is written into every row. When an
assistant model screens, `--by` names the model. This is not bookkeeping: an
assisted screen is publishable when it is disclosed, logged per decision, and
verified by a human, and unpublishable when it is not. The log is what makes the
first three true; stage 3 is the fourth.

THE TITLE-STAGE RULE IS DELIBERATELY PERMISSIVE. Exclude only what is clearly not
a report of phage administered to human patients. Anything ambiguous advances --
a title that cannot be judged is not a title that can be excluded. Over-inclusion
costs reading time at the abstract stage; over-exclusion costs a study, silently,
and this review has already lost studies that way.

USAGE
    python scripts/screen_stage2.py --status
    python scripts/screen_stage2.py --next 200            # print the next batch
    python scripts/screen_stage2.py --next 200 --abstracts
    python scripts/screen_stage2.py --record decisions.tsv --by "claude-opus-5"
    python scripts/screen_stage2.py --audit               # re-check known positives

decisions.tsv is three tab-separated columns: pmid, verdict, reason.
Verdicts: ADVANCE (to abstract/full text) or EXCLUDE.
"""
import argparse
import csv
import datetime
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
STAGE1 = ROOT / "data" / "raw" / "screening_stage1.csv"
LOG = ROOT / "data" / "raw" / "screening_stage2_decisions.csv"
INDEX = ROOT / "quality_reports" / "corpus_identifier_index.txt"

csv.field_size_limit(10_000_000)
FIELDS = ["pmid", "verdict", "reason", "decided_by", "decided_at"]

# Titles carry Greek letters, en dashes and accented author names. The Windows
# console is cp1252 and raises on all of them, which would abort a batch
# part-way through and make the screen non-reproducible. Force UTF-8 out.
try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass


def load_pool():
    with open(STAGE1, encoding="utf-8", newline="") as fh:
        return [r for r in csv.DictReader(fh) if r["stage1"] == "ADVANCE"]


def load_log():
    if not LOG.exists():
        return {}
    with open(LOG, encoding="utf-8", newline="") as fh:
        return {r["pmid"]: r for r in csv.DictReader(fh)}


def append_log(rows):
    exists = LOG.exists()
    with open(LOG, "a", encoding="utf-8", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=FIELDS)
        if not exists:
            w.writeheader()
        w.writerows(rows)


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
    ap.add_argument("--abstracts", action="store_true")
    ap.add_argument("--record", default=None)
    ap.add_argument("--by", default=None)
    ap.add_argument("--audit", action="store_true")
    # Screening order is not neutral. The pool is in PMID order, so screening it
    # front-to-back starts with the oldest and least relevant records. Arm A is
    # 1,320 records and holds 36 of the 40 known positives; arm B is 5,839 and
    # holds four that nothing else can reach. Doing arm A first front-loads the
    # yield without changing what eventually gets screened.
    ap.add_argument("--arm", default=None,
                    help="A_organism_first | B_no_organism_block")
    args = ap.parse_args()

    pool = load_pool()
    if args.arm:
        pool = [r for r in pool if args.arm in (r.get("arms") or "")]
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
                bad.append(("malformed", ln[:60]))
                continue
            pmid, verdict, reason = parts[0].strip(), parts[1].strip().upper(), parts[2].strip()
            if pmid not in valid:
                bad.append(("not in stage-2 pool", pmid))
                continue
            if verdict not in {"ADVANCE", "EXCLUDE"}:
                bad.append(("bad verdict", "%s %s" % (pmid, verdict)))
                continue
            if pmid in done:
                bad.append(("already decided", pmid))
                continue
            rows.append({"pmid": pmid, "verdict": verdict, "reason": reason,
                         "decided_by": args.by, "decided_at": now})
        if bad:
            print("rejected %d line(s):" % len(bad))
            for why, what in bad[:12]:
                print("   %-22s %s" % (why, what))
        if rows:
            append_log(rows)
            print("recorded %d decision(s) by %s" % (len(rows), args.by))
        done = load_log()

    if args.audit:
        known = known_pmids()
        wrong = [(p, known[p], done[p]["reason"]) for p in known
                 if p in done and done[p]["verdict"] == "EXCLUDE"]
        print("known positives decided so far:",
              sum(1 for p in known if p in done), "of", len(known))
        if wrong:
            print("EXCLUDED IN ERROR -- a known included study was screened out:")
            for p, sid, why in wrong:
                print("   %-9s %-24s %s" % (p, sid, why))
            sys.exit(1)
        print("no known included study has been excluded.")
        return

    n_adv = sum(1 for r in done.values() if r["verdict"] == "ADVANCE")
    n_exc = sum(1 for r in done.values() if r["verdict"] == "EXCLUDE")
    print("stage-2 pool     : %d" % len(pool))
    print("decided          : %d  (ADVANCE %d / EXCLUDE %d)" % (len(done), n_adv, n_exc))
    print("remaining        : %d" % (len(pool) - len(done)))

    if args.next:
        todo = [r for r in pool if r["pmid"] not in done][:args.next]
        print("\n# next %d records -- decide each as ADVANCE or EXCLUDE" % len(todo))
        print("# pmid\tyear\ttitle")
        for r in todo:
            title = " ".join((r["title"] or "").split())
            line = "%s\t%s\t%s" % (r["pmid"], r["year"], title[:190])
            if args.abstracts:
                ab = " ".join((r["abstract"] or "").split())
                line += "\n\t\tABSTRACT: " + ab[:600]
            print(line)


if __name__ == "__main__":
    main()
