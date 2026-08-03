"""Can every included study be found by a documented database search?

WHY THIS EXISTS. This review is dropping its local PDF/Elicit channel and
declaring that searching was done in databases only. That is a clean decision,
but it is conditional, and the condition is testable: twelve of the forty-two
included studies are traceable to those folders, so removing the channel while
keeping the studies would assert a provenance that does not exist.

The channel is dispensable if and only if every included study is retrieved by a
query this review can print in its Methods. This runs that test against
PubMed/MEDLINE via NCBI E-utilities, per study, per query.

WHAT A FAILURE MEANS. A study retrieved by no documented query has not been
proven ineligible or wrong -- it has been proven undocumented. PRISMA 2020
provides a separate identification column for records found by other methods
precisely for this case. The honest options are to find a query that retrieves
it, or to keep an "other methods" channel and describe it accurately. Silently
reassigning it to a database search would be the one thing that is not allowed.

Registry-only records are excluded from the denominator: a ClinicalTrials.gov
entry with no publication cannot be retrieved from PubMed, and counting it as a
failure would be a category error.

USAGE
    python scripts/verify_database_retrievability.py
    python scripts/verify_database_retrievability.py --out quality_reports/retrievability.md
"""
import argparse
import json
import pathlib
import re
import sys
import time
import urllib.parse
import urllib.request

ROOT = pathlib.Path(__file__).resolve().parent.parent
INDEX = ROOT / "quality_reports" / "corpus_identifier_index.txt"
EUTILS = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/"

ORG = '("Pseudomonas aeruginosa"[tiab] OR "P. aeruginosa"[tiab] OR "Pseudomonas aeruginosa"[MeSH])'
PHAGE = ('("phage"[tiab] OR "bacteriophage"[tiab] OR "phage therapy"[tiab] OR '
         '"bacteriophage therapy"[tiab] OR "phagotherapy"[tiab] OR '
         '"Bacteriophages"[MeSH] OR "Phage Therapy"[MeSH])')
RESIST = ('("multidrug-resistant"[tiab] OR "MDR"[tiab] OR "extensively drug-resistant"[tiab] '
          'OR "XDR"[tiab] OR "pandrug-resistant"[tiab] OR "PDR"[tiab] OR '
          '"drug-resistant"[tiab] OR "drug resistance"[tiab])')
CLIN = ('(case reports[pt] OR clinical trial[pt] OR observational study[pt] OR '
        'comparative study[pt] OR multicenter study[pt] OR journal article[pt])')
WINDOW = '("2016"[dp] : "2026"[dp])'

# Each query is exactly what the Methods section would have to print. The order
# is deliberate: from the one this review actually ran, to the one it should have.
QUERIES = {
    "Q1 topical, resistance required (as run)":
        f"{ORG} AND {PHAGE} AND {RESIST} AND {WINDOW}",
    "Q2 un-blocked, clinical types (as run, round 5)":
        f"{ORG} AND {PHAGE} AND {CLIN} AND {WINDOW}",
    "Q3 un-blocked, humans, no type filter (proposed)":
        f"{ORG} AND {PHAGE} AND humans[mh] AND {WINDOW}",
    "Q4 un-blocked, no filters at all (maximal)":
        f"{ORG} AND {PHAGE}",
    # Q5/Q6 drop the ORGANISM block, not the resistance block. Four included
    # studies -- Pirnay 2024, Green 2023, Leitner 2021, Liu 2025 -- are
    # multi-pathogen phage-therapy reports that name no organism in title,
    # abstract or MeSH, so an organism-first architecture cannot reach them at
    # any sensitivity. Pirnay is the corpus's largest single contributor.
    "Q5 phage + clinical types, NO organism block":
        f"{PHAGE} AND {CLIN} AND {WINDOW}",
    "Q6 phage + humans, NO organism block (proposed primary)":
        f"{PHAGE} AND humans[mh] AND {WINDOW}",
}


def eutils(endpoint, params, retries=3):
    params.setdefault("retmode", "json")
    params.setdefault("tool", "clo-author-sr")
    params.setdefault("email", "dvchiqui@gmail.com")
    url = EUTILS + endpoint + "?" + urllib.parse.urlencode(params)
    for attempt in range(retries):
        try:
            with urllib.request.urlopen(url, timeout=60) as r:
                return json.load(r)
        except Exception as e:
            if attempt == retries - 1:
                raise
            time.sleep(2 * (attempt + 1))
    return None


def run_query(term):
    d = eutils("esearch.fcgi", {"db": "pubmed", "term": term, "retmax": 10000})
    res = d["esearchresult"]
    return set(res.get("idlist", [])), int(res.get("count", 0))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default=None)
    args = ap.parse_args()

    # ---- corpus ----
    ids_by_study = {}
    for line in INDEX.read_text(encoding="utf-8").splitlines():
        if line.strip() and not line.startswith("#"):
            ident, _, sid = line.partition("\t")
            ids_by_study.setdefault(sid.strip(), []).append(ident.strip())

    # ALL PMIDs per study, not the first or the last. A study frequently carries
    # both a primary article and an erratum -- Weiner 2025 carries PMID 40593506
    # (the randomized trial) and PMID 41760669 (an Author Correction). Testing
    # only one of them answers a question nobody asked: an erratum is typed
    # "Published Erratum" and is not indexed humans[mh], so any clinical filter
    # will miss it while retrieving the trial perfectly well. A study is
    # retrievable if ANY of its identifiers is retrieved.
    pmid_of, registry_only, no_pmid = {}, [], []
    for sid, ids in ids_by_study.items():
        pm = [i.split(":", 1)[1] for i in ids if i.startswith("pmid:")]
        if pm:
            pmid_of[sid] = pm
        elif all(i.startswith("nct:") for i in ids):
            registry_only.append(sid)
        else:
            no_pmid.append((sid, ids))

    # A DOI-only record still has a PubMed entry if it is indexed; ask.
    for sid, ids in list(no_pmid):
        doi = next((i.split(":", 1)[1] for i in ids if i.startswith("doi:")), None)
        if not doi:
            continue
        time.sleep(0.4)
        try:
            found, n = run_query(f'"{doi}"[aid]')
            if found:
                pmid_of[sid] = sorted(found)
                no_pmid.remove((sid, ids))
        except Exception:
            pass

    print("studies in corpus         :", len(ids_by_study))
    print("with a PubMed PMID        :", len(pmid_of))
    print("registry-only (excluded)  :", len(registry_only), registry_only)
    print("no PMID, not registry     :", len(no_pmid), [s for s, _ in no_pmid])
    print()

    # ---- run the queries ----
    results = {}
    for label, term in QUERIES.items():
        time.sleep(0.5)
        pmids, count = run_query(term)
        hit = {s for s, ps in pmid_of.items() if any(p in pmids for p in ps)}
        results[label] = {"term": term, "count": count,
                          "retrieved": len(pmids), "covers": hit}
        print("%-52s %6d records  covers %2d/%d included"
              % (label, count, len(hit), len(pmid_of)))

    # ---- who is covered by nothing ----
    covered = set().union(*(r["covers"] for r in results.values())) if results else set()
    missing = sorted(set(pmid_of) - covered)
    print()
    print("covered by at least one query :", len(covered), "of", len(pmid_of))
    print("covered by NONE               :", len(missing))
    for s in missing:
        print("    %-28s pmid:%s" % (s, ",".join(pmid_of[s])))

    if args.out:
        out = ROOT / args.out if not pathlib.Path(args.out).is_absolute() else pathlib.Path(args.out)
        L = ["# Are the included studies retrievable from PubMed?", "",
             "Generated by `scripts/verify_database_retrievability.py`.", "",
             "This tests whether the local PDF/Elicit channel is dispensable: it is,",
             "if and only if every included study is retrieved by a query the Methods",
             "section can print.", "",
             "| Query | PubMed records | Included studies covered |", "|---|---|---|"]
        for label, r in results.items():
            L.append("| %s | %d | %d / %d |" % (label, r["count"], len(r["covers"]), len(pmid_of)))
        L += ["", "## Query strings", ""]
        for label, r in results.items():
            L += ["**%s**" % label, "", "```", r["term"], "```", ""]
        L += ["## Coverage", "",
              "- studies with a PubMed record: **%d**" % len(pmid_of),
              "- covered by at least one query: **%d**" % len(covered),
              "- covered by none: **%d**" % len(missing), ""]
        if registry_only:
            L += ["Registry-only records excluded from the denominator (no publication "
                  "to retrieve): %s" % ", ".join("`%s`" % s for s in registry_only), ""]
        if no_pmid:
            L += ["Not indexed in PubMed at all: %s"
                  % ", ".join("`%s`" % s for s, _ in no_pmid), ""]
        if missing:
            L += ["### Retrieved by no documented query", "",
                  "These have not been shown ineligible -- they have been shown "
                  "undocumented. Either a query that retrieves them is found, or an "
                  "\"identified by other methods\" channel is retained and described "
                  "accurately.", ""]
            for s in missing:
                L.append("- `%s` (PMID %s)" % (s, ", ".join(pmid_of[s])))
            L.append("")
        else:
            L += ["### Result", "",
                  "**Every included study with a PubMed record is retrieved by at least "
                  "one documented query.** The local PDF/Elicit channel is dispensable: "
                  "no included study depends on it for identification.", ""]
        out.write_text("\n".join(L), encoding="utf-8", newline="\n")
        print("\nwrote", out)


if __name__ == "__main__":
    main()
