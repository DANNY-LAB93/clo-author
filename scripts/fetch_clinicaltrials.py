"""Retrieve both ClinicalTrials.gov arms via the v2 API, to disk.

WHY AN API AND NOT THE DOWNLOAD BUTTON. The browser export lands in a Downloads
folder with a timestamped name and no record of the query that produced it --
which is precisely the failure this review is currently repairing for its local
PDF corpus, where 394 files survive and not one query string does. The API call
IS the query string, it lives in this file, and re-running it reproduces the
result set.

THE TWO ARMS, AND WHY THE SECOND EXISTS. Arm A requires the condition to name
Pseudomonas aeruginosa. Arm B requires only the intervention. The difference is
not sensitivity tuning: a multi-pathogen trial registers a generic condition, so
arm A cannot see it. The first record arm B returns is NCT06870409,
"Bacteriophages in Addition to Antibiotics for the Treatment of Patients With
Infective Endocarditis", registered under "Endocarditis, Bacterial" -- a phage
trial that could enrol P. aeruginosa cases and that arm A will never retrieve.
This is the registry form of the same defect that made the published search miss
Pirnay 2024.

NO DATE FILTER, DELIBERATELY. Registration precedes publication, so a 2015
registration can produce a 2024 result. Filtering registries by date at search
time discards exactly the trials whose results are newest.

USAGE
    python scripts/fetch_clinicaltrials.py
"""
import csv
import json
import pathlib
import time
import urllib.parse
import urllib.request

ROOT = pathlib.Path(__file__).resolve().parent.parent
OUT = ROOT / "revision_sistematica" / "busqueda" / "clinicaltrials_gov.csv"
API = "https://clinicaltrials.gov/api/v2/studies"

ARMS = {
    "A_condition_and_intervention": {
        "query.cond": "Pseudomonas aeruginosa",
        "query.intr": "bacteriophage OR phage",
    },
    "B_intervention_only": {
        "query.intr": "bacteriophage OR phage",
    },
}

FIELDS = [
    "protocolSection.identificationModule.nctId",
    "protocolSection.identificationModule.briefTitle",
    "protocolSection.statusModule.overallStatus",
    "protocolSection.statusModule.startDateStruct.date",
    "protocolSection.designModule.studyType",
    "protocolSection.designModule.phases",
    "protocolSection.designModule.enrollmentInfo.count",
    "protocolSection.conditionsModule.conditions",
    "protocolSection.armsInterventionsModule.interventions",
    "protocolSection.sponsorCollaboratorsModule.leadSponsor.name",
]


def dig(d, path):
    cur = d
    for part in path.split("."):
        if isinstance(cur, dict):
            cur = cur.get(part)
        else:
            return None
    return cur


def flat(v):
    if v is None:
        return ""
    if isinstance(v, list):
        out = []
        for x in v:
            if isinstance(x, dict):
                out.append(x.get("name") or x.get("type") or json.dumps(x, ensure_ascii=False))
            else:
                out.append(str(x))
        return "; ".join(out)
    return str(v)


def fetch(params):
    studies, token = [], None
    while True:
        p = dict(params)
        p["pageSize"] = 100
        p["format"] = "json"
        if token:
            p["pageToken"] = token
        url = API + "?" + urllib.parse.urlencode(p)
        with urllib.request.urlopen(url, timeout=90) as r:
            d = json.load(r)
        studies.extend(d.get("studies", []))
        token = d.get("nextPageToken")
        if not token:
            break
        time.sleep(0.4)
    return studies


def main():
    seen, rows = {}, []
    for arm, params in ARMS.items():
        st = fetch(params)
        print("%-32s %4d studies" % (arm, len(st)))
        for s in st:
            nct = dig(s, "protocolSection.identificationModule.nctId")
            if nct in seen:
                seen[nct]["arms"] += ";" + arm
                continue
            row = {"nct_id": nct, "arms": arm}
            for f in FIELDS[1:]:
                row[f.split(".")[-1]] = flat(dig(s, f))
            seen[nct] = row
            rows.append(row)

    rows.sort(key=lambda r: r["nct_id"])
    OUT.parent.mkdir(parents=True, exist_ok=True)
    with open(OUT, "w", encoding="utf-8", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(rows[0]))
        w.writeheader()
        w.writerows(rows)

    only_b = sum(1 for r in rows if r["arms"] == "B_intervention_only")
    print()
    print("unique trials         : %d" % len(rows))
    print("reachable only by B   : %d  <- invisible to a condition-first search" % only_b)
    print("\nwrote", OUT)


if __name__ == "__main__":
    main()
