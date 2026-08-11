"""Record stage-2 (title) decisions against the prioritised all-sources pool.

Decisions are keyed on record_id, not PMID: most records from Scopus, SciELO and
the trial registries have no PMID, and keying on one would silently drop them.

The log is APPEND-ONLY and keeps every row. A correction is a new row that
supersedes the previous one for that record; both stay visible. Erasing a
decision would erase the evidence that it was ever made, and this review already
had to correct one wrong exclusion -- that correction is only auditable because
the original row survived.

The known-positive audit runs at STUDY level: an included study must keep at
least one advancing report. Excluding one report of a study is legitimate (an
erratum, a duplicate registry entry); losing all of them is not.

USAGE
    python scripts/screen_stage2_pool.py --batch lote01.tsv --by "..."
    python scripts/screen_stage2_pool.py --status
"""
import argparse
import collections
import csv
import datetime
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from screen_stage1_rules import known_pmids
from exclusion_codes import CODES, code_for

ROOT = pathlib.Path(__file__).resolve().parent.parent
POOL = ROOT / "revision_sistematica" / "cribado" / "screening_stage2_priorizado.csv"
LOG = ROOT / "revision_sistematica" / "cribado" / "screening_stage2_pool_decisions.csv"
COLS = ["record_id", "orden", "verdict", "reason", "decided_by", "decided_at"]

csv.field_size_limit(200_000_000)


def load_pool():
    with open(POOL, encoding="utf-8", newline="") as fh:
        return list(csv.DictReader(fh))


def load_log():
    """Last row per record wins; every row is kept on disk."""
    if not LOG.exists():
        return {}
    with open(LOG, encoding="utf-8", newline="") as fh:
        out = {}
        for r in csv.DictReader(fh):
            out[r["record_id"]] = r
        return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--batch", help="TSV: orden <tab> ADVANCE|EXCLUDE <tab> motivo")
    ap.add_argument("--by", default="claude-opus-5 (revisor unico, sin duplicacion)")
    ap.add_argument("--status", action="store_true")
    args = ap.parse_args()

    pool = load_pool()
    by_orden = {r["orden"]: r for r in pool}
    decided = load_log()

    if args.batch:
        rows = []
        stamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
        for line in pathlib.Path(args.batch).read_text(encoding="utf-8").splitlines():
            if not line.strip():
                continue
            orden, verdict, reason = (line.split("\t") + ["", ""])[:3]
            rec = by_orden.get(orden.strip())
            if rec is None:
                sys.exit("posicion %s no existe en el pozo" % orden)
            if verdict.strip() not in ("ADVANCE", "EXCLUDE"):
                sys.exit("veredicto invalido: %s" % verdict)
            if verdict.strip() == "EXCLUDE" and code_for(reason) is None:
                sys.exit("motivo sin codigo del vocabulario cerrado, posicion %s: "
                         "%r -- usa uno de: %s"
                         % (orden, reason, ", ".join(CODES)))
            rows.append({"record_id": rec["record_id"], "orden": orden.strip(),
                         "verdict": verdict.strip(), "reason": reason.strip(),
                         "decided_by": args.by, "decided_at": stamp})
        nuevo = not LOG.exists()
        with open(LOG, "a", encoding="utf-8", newline="") as fh:
            w = csv.DictWriter(fh, fieldnames=COLS)
            if nuevo:
                w.writeheader()
            w.writerows(rows)
        print("registradas %d decisiones" % len(rows))
        decided = load_log()

    n_pool = len(pool)
    n_dec = len(decided)
    adv = sum(1 for d in decided.values() if d["verdict"] == "ADVANCE")
    exc = n_dec - adv
    print("\npozo            : %d" % n_pool)
    print("decididos       : %d (%.1f%%)" % (n_dec, 100.0 * n_dec / n_pool))
    print("  avanzan       : %d" % adv)
    print("  excluidos     : %d" % exc)
    print("pendientes      : %d" % (n_pool - n_dec))

    if exc:
        # El codigo se DERIVA del texto registrado, no se guarda aparte: asi el
        # log sigue siendo solo-anexar y la agrupacion siempre corresponde a lo
        # que de verdad se escribio al decidir.
        codigos = collections.Counter()
        sin_codigo = []
        for d in decided.values():
            if d["verdict"] != "EXCLUDE":
                continue
            c = code_for(d["reason"])
            if c is None:
                sin_codigo.append(d)
            else:
                codigos[c] += 1
        print("\nmotivos de exclusion (vocabulario cerrado):")
        for c, desc in CODES.items():
            if codigos[c]:
                print("  %-4s %4d  %s" % (c, codigos[c], desc[:58]))
        if sin_codigo:
            print("\n  AVISO: %d exclusiones sin codigo asignable:" % len(sin_codigo))
            for d in sin_codigo[:5]:
                print("    orden %s: %s" % (d["orden"], d["reason"][:70]))
            print("  Corrige el texto o anade el codigo en scripts/exclusion_codes.py.")

    # --- known-positive audit, study level ---
    known = known_pmids()
    by_study = collections.defaultdict(list)
    for r in pool:
        if r["pmid"] and r["pmid"] in known:
            by_study[known[r["pmid"]]].append(r)
    lost = []
    for sid, recs in by_study.items():
        estados = [decided.get(x["record_id"], {}).get("verdict") for x in recs]
        if estados and all(e == "EXCLUDE" for e in estados):
            lost.append((sid, recs))
    tocados = sum(1 for sid, recs in by_study.items()
                  if any(x["record_id"] in decided for x in recs))
    print("\nestudios incluidos con algun informe ya decidido: %d de %d"
          % (tocados, len(by_study)))
    if lost:
        print("\nFALLO: un estudio incluido pierde todos sus informes decididos")
        for sid, recs in lost:
            print("  %s" % sid)
        sys.exit("revisa esas decisiones antes de continuar")
    print("auditoria de control positivo: PASS")


if __name__ == "__main__":
    main()
