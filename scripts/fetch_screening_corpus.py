"""Fetch the full record set for the two-arm PubMed strategy, once, to disk.

WHY THIS EXISTS. The review is re-running its search in databases only, and the
verified strategy needs two arms because an organism-first query structurally
cannot retrieve multi-pathogen phage cohorts -- Pirnay 2024 among them. This
downloads every record in the union so screening happens against a frozen local
copy rather than against a moving database.

Freezing matters. PubMed changes daily; a screen run over two sessions against
the live API is not one screen, and the counts would not reconcile. The output
file IS the screening denominator, and its record count is what the PRISMA flow
must report.

Resumable: batches already written are not re-fetched.

USAGE
    python scripts/fetch_screening_corpus.py
    python scripts/fetch_screening_corpus.py --limit 400     # smoke test
"""
import argparse
import csv
import json
import pathlib
import re
import sys
import time
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET

ROOT = pathlib.Path(__file__).resolve().parent.parent
OUT = ROOT / "revision_sistematica" / "busqueda" / "screening_pubmed_union.csv"
CACHE = ROOT / "revision_sistematica" / "cribado" / ".screening_cache"
EUTILS = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/"

ORG = '("Pseudomonas aeruginosa"[tiab] OR "P. aeruginosa"[tiab] OR "Pseudomonas aeruginosa"[MeSH])'
PHAGE = ('("phage"[tiab] OR "bacteriophage"[tiab] OR "phage therapy"[tiab] OR '
         '"bacteriophage therapy"[tiab] OR "phagotherapy"[tiab] OR '
         '"Bacteriophages"[MeSH] OR "Phage Therapy"[MeSH])')
CLIN = ('(case reports[pt] OR clinical trial[pt] OR observational study[pt] OR '
        'comparative study[pt] OR multicenter study[pt] OR journal article[pt])')
WINDOW = '("2016"[dp] : "2026"[dp])'

ARMS = {
    "A_organism_first": f"{ORG} AND {PHAGE} AND {CLIN} AND {WINDOW}",
    "B_no_organism_block": f"{PHAGE} AND humans[mh] AND {WINDOW}",
}


def eutils(endpoint, params, parse="json", retries=4):
    params.setdefault("tool", "clo-author-sr")
    params.setdefault("email", "dvchiqui@gmail.com")
    if parse == "json":
        params.setdefault("retmode", "json")
    url = EUTILS + endpoint + "?" + urllib.parse.urlencode(params)
    for attempt in range(retries):
        try:
            with urllib.request.urlopen(url, timeout=120) as r:
                raw = r.read()
            return json.loads(raw) if parse == "json" else ET.fromstring(raw)
        except Exception:
            if attempt == retries - 1:
                raise
            time.sleep(3 * (attempt + 1))


def txt(node, path, sep=" "):
    if node is None:
        return ""
    vals = [("".join(e.itertext())).strip() for e in node.findall(path)]
    return sep.join(v for v in vals if v)


def parse_article(art):
    med = art.find("MedlineCitation")
    if med is None:
        return None
    pmid = txt(med, "PMID")
    a = med.find("Article")
    abstract = txt(a, "Abstract/AbstractText", " ") if a is not None else ""
    year = txt(a, "Journal/JournalIssue/PubDate/Year") if a is not None else ""
    if not year:
        md = txt(a, "Journal/JournalIssue/PubDate/MedlineDate") if a is not None else ""
        m = re.search(r"(\d{4})", md)
        year = m.group(1) if m else ""
    authors = a.findall("AuthorList/Author") if a is not None else []
    first = ""
    if authors:
        first = (txt(authors[0], "LastName") + " " + txt(authors[0], "Initials")).strip()
        if not first:
            first = txt(authors[0], "CollectiveName")
    # The article's OWN id list only. art.iter() walks the whole subtree, which
    # includes PubmedData/ReferenceList/Reference/ArticleIdList -- one entry per
    # cited reference. A phage genomics paper cites 60-80 of them, so iterating
    # the subtree stores the last reference's DOI (Bowtie2, Trimmomatic, PHASTER)
    # as if it were the article's. Same failure class as scanning a PDF's
    # bibliography; see build_document_corpus_manifest.py.
    doi = next(((e.text or "").strip()
                for e in art.findall("PubmedData/ArticleIdList/ArticleId")
                if e.get("IdType") == "doi"), "")
    if not doi and a is not None:
        doi = next(((e.text or "").strip()
                    for e in a.findall("ELocationID")
                    if e.get("EIdType") == "doi"), "")
    return {
        "pmid": pmid,
        "year": year,
        "first_author": first,
        "title": txt(a, "ArticleTitle") if a is not None else "",
        "abstract": abstract,
        "journal": txt(a, "Journal/Title") if a is not None else "",
        "pubtypes": txt(a, "PublicationTypeList/PublicationType", "; ") if a is not None else "",
        "mesh": txt(med, "MeshHeadingList/MeshHeading/DescriptorName", "; "),
        "doi": doi,
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--limit", type=int, default=None)
    args = ap.parse_args()
    CACHE.mkdir(parents=True, exist_ok=True)

    # ---- arm membership, recorded per record ----
    arm_of = {}
    for name, term in ARMS.items():
        d = eutils("esearch.fcgi", {"db": "pubmed", "term": term, "retmax": 100000})
        ids = d["esearchresult"].get("idlist", [])
        print("%-22s %6s records" % (name, d["esearchresult"]["count"]))
        for p in ids:
            arm_of.setdefault(p, []).append(name)
        time.sleep(0.5)

    pmids = sorted(arm_of, key=int)
    if args.limit:
        pmids = pmids[:args.limit]
    print("union                  %6d unique records\n" % len(pmids))

    # ---- fetch in batches, cached ----
    BATCH = 200
    records = {}
    for i in range(0, len(pmids), BATCH):
        chunk = pmids[i:i + BATCH]
        cache_file = CACHE / ("%s.json" % chunk[0])
        if cache_file.exists():
            for r in json.loads(cache_file.read_text(encoding="utf-8")):
                records[r["pmid"]] = r
            continue
        root = eutils("efetch.fcgi",
                      {"db": "pubmed", "id": ",".join(chunk), "retmode": "xml"},
                      parse="xml")
        got = []
        for art in root.findall("PubmedArticle"):
            r = parse_article(art)
            if r:
                got.append(r)
                records[r["pmid"]] = r
        cache_file.write_text(json.dumps(got), encoding="utf-8")
        print("   fetched %d/%d" % (min(i + BATCH, len(pmids)), len(pmids)), flush=True)
        time.sleep(0.4)

    rows = []
    for p in pmids:
        r = records.get(p)
        if not r:
            rows.append({"pmid": p, "year": "", "first_author": "", "title": "",
                         "abstract": "", "journal": "", "pubtypes": "", "mesh": "",
                         "doi": "", "arms": ";".join(arm_of.get(p, [])),
                         "fetch_status": "NOT_RETURNED"})
            continue
        r = dict(r)
        r["arms"] = ";".join(arm_of.get(p, []))
        r["fetch_status"] = "ok"
        rows.append(r)

    OUT.parent.mkdir(parents=True, exist_ok=True)
    with open(OUT, "w", encoding="utf-8", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(rows[0]))
        w.writeheader()
        w.writerows(rows)

    n_abs = sum(1 for r in rows if r["abstract"])
    print("\nrecords written        : %d" % len(rows))
    print("with an abstract       : %d" % n_abs)
    print("title only, no abstract: %d" % (len(rows) - n_abs))
    print("failed to fetch        : %d" % sum(1 for r in rows if r["fetch_status"] != "ok"))
    print("\nwrote", OUT)


if __name__ == "__main__":
    main()
