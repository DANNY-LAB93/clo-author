"""Unify every source into one screening corpus, one row per de-duplicated report.

WHY. The stage-1 rule engine was written against the PubMed CSV and reads MeSH
and PubMed publication types. Seven of the eight sources have neither. Rather
than weaken the rules to whatever the poorest source carries, this builds one
corpus with a normalised schema and records, per row, WHICH fields are actually
present -- so a rule can decline to fire on a record it cannot judge instead of
guessing.

FIELD MERGING. A report retrieved from two sources gives two descriptions of the
same thing. For each field the richest value wins: the longest abstract, the
first non-empty MeSH string, the union of document types. That is safe because
the report-level clustering has already established they are the same report,
and it is what makes a Scopus abstract usable for a record PubMed returned
without one.

WHAT IT DOES NOT DO. It does not infer missing metadata. A Scopus record has no
MeSH and gets an empty MeSH field, not a guessed one; the applicability columns
say so, and the rules honour that.

USAGE
    python scripts/build_screening_corpus.py --manifest revision_sistematica/busqueda/sources.json
"""
import argparse
import collections
import csv
import hashlib
import json
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from deduplicate_sources import (ROOT, load, keys_for, norm_title, Union)

csv.field_size_limit(200_000_000)

OUT_DEFAULT = "revision_sistematica/cribado/screening_corpus_all.csv"
FIELDS = ["record_id", "title", "abstract", "year", "journal", "doctype",
          "mesh", "keywords", "pmid", "doi", "nct", "identifiers", "sources",
          "n_source_records", "has_mesh", "has_doctype", "has_abstract"]


def longest(vals):
    vals = [v for v in vals if (v or "").strip()]
    return max(vals, key=len) if vals else ""


def first_nonempty(vals):
    return next((v for v in vals if (v or "").strip()), "")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--manifest", default="revision_sistematica/busqueda/sources.json")
    ap.add_argument("--out", default=OUT_DEFAULT)
    args = ap.parse_args()

    man = json.loads((ROOT / args.manifest).read_text(encoding="utf-8"))
    records = []
    for label, rel in man.items():
        p = ROOT / rel
        if not p.exists():
            print("FALTA, omitida: %-26s %s" % (label, p.name))
            continue
        recs = load(p)
        for r in recs:
            r["source"] = label
            records.append(r)
        print("%-26s %6d registros" % (label, len(recs)))

    parsed = [keys_for(r) for r in records]
    keys = [k for k, _ in parsed]
    allids = [a for _, a in parsed]

    # Report-level clustering only: DOI and PMID, never NCT. Identical to the
    # de-duplicator, because the screening corpus must contain exactly the rows
    # the PRISMA "records screened" box counts.
    report_keys = [{k for k in ks if not k.startswith("nct:")} for ks in keys]
    u = Union()
    owner = {}
    for i in range(len(records)):
        u.find(("rec", i))
        for k in report_keys[i]:
            if k in owner:
                u.union(("rec", owner[k]), ("rec", i))
            else:
                owner[k] = i
    title_owner = {}
    for i in range(len(records)):
        if report_keys[i]:
            continue
        t = norm_title(records[i]["title"])
        if len(t) < 15:
            continue
        tk = (t, records[i]["year"])
        if tk in title_owner:
            u.union(("rec", title_owner[tk]), ("rec", i))
        else:
            title_owner[tk] = i

    groups = {}
    for i in range(len(records)):
        groups.setdefault(u.find(("rec", i)), []).append(i)

    def stable_id(ids, title, year):
        """Identificador derivado del CONTENIDO, no del orden de enumeracion.

        Un record_id asignado por posicion cambia en cuanto cambia el manifiesto,
        y las decisiones de cribado que apuntan a el pasan a senalar otro
        registro sin que nada falle a la vista. Derivarlo de los identificadores
        --o del titulo y el ano cuando no hay ninguno-- hace que el mismo informe
        conserve su clave entre reconstrucciones.
        """
        base = " ".join(ids) if ids else "%s|%s" % (norm_title(title), year)
        return "R" + hashlib.sha1(base.encode("utf-8")).hexdigest()[:10]

    rows = []
    vistos = collections.Counter()
    for members in groups.values():
        g = [records[i] for i in members]
        ids = sorted(set().union(*(allids[i] for i in members)))
        pick = lambda f: longest([x.get(f, "") for x in g])
        one = lambda pref: next((k.split(":", 1)[1] for k in ids
                                 if k.startswith(pref)), "")
        mesh = first_nonempty([x.get("mesh", "") for x in g])
        doctype = "; ".join(sorted({x.get("doctype", "").strip() for x in g
                                    if x.get("doctype", "").strip()}))
        abstract = pick("abstract")
        rid = stable_id(ids, pick("title"), first_nonempty([x.get("year", "") for x in g]))
        vistos[rid] += 1
        if vistos[rid] > 1:                 # colision: desambiguar, nunca pisar
            rid = "%s-%d" % (rid, vistos[rid])
        rows.append({
            "record_id": rid,
            "title": " ".join((pick("title") or "").split()),
            "abstract": " ".join(abstract.split()),
            "year": first_nonempty([x.get("year", "") for x in g]),
            "journal": pick("journal"),
            "doctype": doctype,
            "mesh": mesh,
            "keywords": pick("keywords"),
            "pmid": one("pmid:"), "doi": one("doi:"), "nct": one("nct:"),
            "identifiers": " ".join(ids),
            "sources": "; ".join(sorted({x["source"] for x in g})),
            "n_source_records": len(members),
            # Applicability flags. A rule that needs a field must check these
            # rather than treat an empty field as a negative finding.
            "has_mesh": "1" if mesh.strip() else "0",
            "has_doctype": "1" if doctype.strip() else "0",
            "has_abstract": "1" if abstract.strip() else "0",
        })
    rows.sort(key=lambda r: (r["year"], r["title"]))

    out = ROOT / args.out
    out.parent.mkdir(parents=True, exist_ok=True)
    with open(out, "w", encoding="utf-8", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=FIELDS)
        w.writeheader()
        w.writerows(rows)

    n = len(rows)
    print("\nregistros de origen : %d" % len(records))
    print("informes unicos     : %d" % n)
    print("con resumen         : %5d (%4.1f%%)"
          % (sum(1 for r in rows if r["has_abstract"] == "1"),
             100.0 * sum(1 for r in rows if r["has_abstract"] == "1") / n))
    print("con MeSH            : %5d (%4.1f%%)"
          % (sum(1 for r in rows if r["has_mesh"] == "1"),
             100.0 * sum(1 for r in rows if r["has_mesh"] == "1") / n))
    print("con tipo documental : %5d (%4.1f%%)"
          % (sum(1 for r in rows if r["has_doctype"] == "1"),
             100.0 * sum(1 for r in rows if r["has_doctype"] == "1") / n))
    print("\nwrote", out)


if __name__ == "__main__":
    main()
