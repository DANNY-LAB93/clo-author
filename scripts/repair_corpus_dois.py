"""Repair the `doi` column of the screening corpus.

WHY THIS EXISTS. The first version of fetch_screening_corpus.py read the DOI with
`art.iter("ArticleId")`, which walks the whole PubmedArticle subtree. That subtree
contains PubmedData/ReferenceList/Reference/ArticleIdList -- one id list per CITED
REFERENCE. A phage genomics paper cites 60-80 works, so the loop ended on the last
reference's DOI and stored it as the article's own. Verified on PMID 28472930: the
stored DOI was 10.1038/nmeth.1923 (Bowtie2); the real one is 10.1186/s12864-017-3729-z.

The consequence was not cosmetic. 447 DOIs were shared by more than one record,
covering 1,129 rows, and the de-duplicator matches on DOI -- so records citing the
same tool were being merged into one "study". The same wrong DOIs were also printed
in the reviewer workbook.

WHAT THIS DOES. Re-fetches every PMID in the corpus, reads the DOI from
PubmedData/ArticleIdList only (falling back to Article/ELocationID[@EIdType=doi]),
and rewrites the doi column in place. Every other column is untouched, so screening
decisions already recorded against these PMIDs stay valid.

It reports what changed rather than overwriting silently, and writes the full
before/after list to quality_reports/doi_repair.md so the correction is auditable.

USAGE
    python scripts/repair_corpus_dois.py
    python scripts/repair_corpus_dois.py --dry-run     # report, write nothing
"""
import argparse
import csv
import pathlib
import time
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET

ROOT = pathlib.Path(__file__).resolve().parent.parent
CORPUS = ROOT / "revision_sistematica" / "busqueda" / "screening_pubmed_union.csv"
REPORT = ROOT / "quality_reports" / "doi_repair.md"
EFETCH = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi"
BATCH = 200

csv.field_size_limit(10_000_000)


def fetch(pmids, retries=4):
    """DOIs for a batch of PMIDs, keyed by PMID. POST because a 200-id query
    string exceeds what NCBI accepts reliably on GET."""
    data = urllib.parse.urlencode({
        "db": "pubmed", "retmode": "xml", "id": ",".join(pmids),
        "tool": "clo-author-sr", "email": "dvchiqui@gmail.com",
    }).encode()
    for attempt in range(retries):
        try:
            with urllib.request.urlopen(EFETCH, data=data, timeout=180) as r:
                root = ET.fromstring(r.read())
            break
        except Exception:
            if attempt == retries - 1:
                raise
            time.sleep(3 * (attempt + 1))

    out = {}
    for art in root.findall("PubmedArticle"):
        pmid = art.findtext("MedlineCitation/PMID") or ""
        # the article's own id list -- never the reference list
        doi = next(((e.text or "").strip()
                    for e in art.findall("PubmedData/ArticleIdList/ArticleId")
                    if e.get("IdType") == "doi"), "")
        if not doi:
            a = art.find("MedlineCitation/Article")
            if a is not None:
                doi = next(((e.text or "").strip()
                            for e in a.findall("ELocationID")
                            if e.get("EIdType") == "doi"), "")
        out[pmid] = doi
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    with open(CORPUS, encoding="utf-8", newline="") as fh:
        rd = csv.DictReader(fh)
        cols, rows = rd.fieldnames, list(rd)
    pmids = [r["pmid"] for r in rows if r["pmid"]]
    print("registros: %d" % len(rows))

    true_doi = {}
    for i in range(0, len(pmids), BATCH):
        chunk = pmids[i:i + BATCH]
        true_doi.update(fetch(chunk))
        print("  %5d / %5d" % (min(i + BATCH, len(pmids)), len(pmids)), end="\r")
        time.sleep(0.4)                       # NCBI: <=3 requests/second
    print()

    changed, gained, lost, missing = [], 0, 0, 0
    for r in rows:
        old = (r.get("doi") or "").strip()
        if r["pmid"] not in true_doi:
            missing += 1
            continue                          # leave untouched rather than blank it
        new = true_doi[r["pmid"]]
        if new != old:
            changed.append((r["pmid"], old, new, " ".join(r["title"].split())[:80]))
            if old and not new:
                lost += 1
            elif new and not old:
                gained += 1
            r["doi"] = new

    dups_before = len(rows) - len({(r["pmid"]) for r in rows})
    seen = {}
    for r in rows:
        d = r["doi"].strip().lower()
        if d:
            seen.setdefault(d, []).append(r["pmid"])
    shared = {d: p for d, p in seen.items() if len(p) > 1}

    print("DOIs corregidos          : %d" % len(changed))
    print("  ganados (estaba vacio) : %d" % gained)
    print("  perdidos (queda vacio) : %d" % lost)
    print("PMID no devueltos        : %d" % missing)
    print("DOIs aun compartidos     : %d  (filas: %d)"
          % (len(shared), sum(len(v) for v in shared.values())))
    assert dups_before == 0, "el corpus dejo de ser unico por PMID"

    if args.dry_run:
        print("\n--dry-run: no se escribio nada")
        return

    with open(CORPUS, "w", encoding="utf-8", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=cols)
        w.writeheader()
        w.writerows(rows)

    L = ["# DOI repair -- screening corpus", "",
         "The `doi` column was populated from the wrong node of the PubMed XML.",
         "`art.iter(\"ArticleId\")` walks the whole subtree, including",
         "`PubmedData/ReferenceList/Reference/ArticleIdList`, so the stored value was",
         "the DOI of the article's **last cited reference**. Re-read from",
         "`PubmedData/ArticleIdList` only.", "",
         "| | n |", "|---|---|",
         "| Records in corpus | %d |" % len(rows),
         "| DOIs corrected | %d |" % len(changed),
         "| DOIs recovered where the field was empty | %d |" % gained,
         "| Records PubMed no longer returns (left untouched) | %d |" % missing,
         "| DOIs still shared by more than one record | %d |" % len(shared), "",
         "Any DOI still shared is a genuine collision (erratum, reprint, multipart",
         "article) and is listed below for inspection.", ""]
    if shared:
        L += ["| DOI | PMIDs |", "|---|---|"]
        for d, ps in sorted(shared.items(), key=lambda kv: -len(kv[1]))[:40]:
            L.append("| %s | %s |" % (d, ", ".join(ps)))
        L.append("")
    L += ["## Every correction", "", "| PMID | stored (wrong) | actual | title |",
          "|---|---|---|---|"]
    for p, old, new, t in changed:
        L.append("| %s | %s | %s | %s |" % (p, old or "*(empty)*", new or "*(none)*", t))

    REPORT.parent.mkdir(parents=True, exist_ok=True)
    REPORT.write_text("\n".join(L), encoding="utf-8", newline="\n")
    print("\nwrote", CORPUS)
    print("wrote", REPORT)


if __name__ == "__main__":
    main()
