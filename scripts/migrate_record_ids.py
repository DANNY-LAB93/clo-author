"""Migrate the screening log from positional record_ids to content-derived ones.

WHY THIS EXISTS. build_screening_corpus.py originally numbered records by
enumeration order (R000001, R000002...). That key is not stable: change the
manifest and the same report gets a different id, so a decision log keyed on it
starts pointing at other records with nothing visibly failing. The id is now a
hash of the record's identifiers. This migrates the decisions already recorded.

HOW THE MAPPING IS MADE. Old and new corpora are matched on the identifier set,
which is content and does not depend on ordering. Records with no identifier fall
back to normalised title plus year, the same rule the de-duplicator uses.

NOTHING IS OVERWRITTEN. The original log is copied aside before the migrated one
is written, and the script refuses to run if any decision fails to map -- a
decision that cannot be relocated is not silently dropped.

USAGE
    python scripts/migrate_record_ids.py --old revision_sistematica/cribado/.screening_cache/corpus_antes_filtro_scopus.csv
"""
import argparse
import csv
import pathlib
import shutil
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from deduplicate_sources import norm_title

ROOT = pathlib.Path(__file__).resolve().parent.parent
NEW = ROOT / "revision_sistematica" / "cribado" / "screening_corpus_all.csv"
LOG = ROOT / "revision_sistematica" / "cribado" / "screening_stage2_pool_decisions.csv"

csv.field_size_limit(200_000_000)


def key(r):
    ids = (r.get("identifiers") or "").strip()
    return ids if ids else "T|%s|%s" % (norm_title(r.get("title")), r.get("year"))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--old", required=True)
    args = ap.parse_args()

    def load(p):
        with open(p, encoding="utf-8", newline="") as fh:
            return list(csv.DictReader(fh))

    old, new = load(args.old), load(NEW)
    old_by_id = {r["record_id"]: key(r) for r in old}
    new_by_key = {key(r): r["record_id"] for r in new}
    print("corpus antiguo: %d | corpus nuevo: %d" % (len(old), len(new)))

    dec = load(LOG)
    print("decisiones registradas: %d" % len(dec))

    migradas, sin_mapear = [], []
    for d in dec:
        k = old_by_id.get(d["record_id"])
        nid = new_by_key.get(k) if k else None
        if nid is None:
            sin_mapear.append(d)
        else:
            d2 = dict(d)
            d2["record_id"] = nid
            migradas.append(d2)

    print("  migradas   : %d" % len(migradas))
    print("  sin mapear : %d" % len(sin_mapear))
    if sin_mapear:
        for d in sin_mapear[:8]:
            print("    orden %s (%s)" % (d["orden"], d["record_id"]))
        sys.exit("hay decisiones que no se pueden relocalizar; no se migra nada")

    backup = LOG.with_suffix(".pre_migracion.csv")
    shutil.copy(LOG, backup)
    with open(LOG, "w", encoding="utf-8", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(dec[0]))
        w.writeheader()
        w.writerows(migradas)
    print("\ncopia del log original en %s" % backup.name)
    print("log migrado: %s" % LOG.name)


if __name__ == "__main__":
    main()
