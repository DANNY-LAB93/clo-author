"""Add the `nct` column to the screening corpus.

WHY. deduplicate_sources.py matches on DOI, PMID and NCT precisely because
ClinicalTrials.gov and Cochrane CENTRAL overlap the journal databases through
trial registrations rather than through DOIs. But the PubMed corpus carried no
NCT at all, so that arm of the match was dead: the de-duplicator reported zero
overlap between PubMed and ClinicalTrials.gov, which was an artefact of a missing
column, not a finding about the sources.

PubMed does record it. A registered trial carries
MedlineCitation/Article/DataBankList/DataBank[DataBankName='ClinicalTrials.gov']
/AccessionNumberList/AccessionNumber. This reads that field and nothing else --
NCT identifiers quoted in an abstract belong to other people's trials.

Adds a column; touches no existing one. Screening decisions keyed on PMID stay valid.

USAGE
    python scripts/add_corpus_trial_ids.py
    python scripts/add_corpus_trial_ids.py --dry-run
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
EFETCH = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi"
BATCH = 200

csv.field_size_limit(10_000_000)


def fetch(pmids, retries=4):
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
        ncts = []
        for bank in art.findall(
                "MedlineCitation/Article/DataBankList/DataBank"):
            if (bank.findtext("DataBankName") or "").strip().lower() \
                    != "clinicaltrials.gov":
                continue
            for acc in bank.findall("AccessionNumberList/AccessionNumber"):
                v = (acc.text or "").strip().upper()
                if v.startswith("NCT"):
                    ncts.append(v)
        out[pmid] = ";".join(sorted(set(ncts)))
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    with open(CORPUS, encoding="utf-8", newline="") as fh:
        rd = csv.DictReader(fh)
        cols, rows = list(rd.fieldnames), list(rd)
    pmids = [r["pmid"] for r in rows if r["pmid"]]
    print("registros: %d" % len(rows))

    found = {}
    for i in range(0, len(pmids), BATCH):
        found.update(fetch(pmids[i:i + BATCH]))
        print("  %5d / %5d" % (min(i + BATCH, len(pmids)), len(pmids)), end="\r")
        time.sleep(0.4)
    print()

    if "nct" not in cols:
        cols.insert(cols.index("doi") + 1, "nct")
    n_with = 0
    for r in rows:
        r["nct"] = found.get(r["pmid"], "")
        if r["nct"]:
            n_with += 1

    print("registros con NCT registrado : %d" % n_with)
    print("NCT distintos                : %d"
          % len({n for r in rows for n in r["nct"].split(";") if n}))

    if args.dry_run:
        print("\n--dry-run: no se escribio nada")
        return

    with open(CORPUS, "w", encoding="utf-8", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=cols)
        w.writeheader()
        w.writerows(rows)
    print("\nwrote", CORPUS)


if __name__ == "__main__":
    main()
