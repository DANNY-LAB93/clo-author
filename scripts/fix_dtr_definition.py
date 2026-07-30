"""Re-code difficult-to-treat resistance against Kadri's actual definition.

THE ERROR. Methods and the Introduction defined DTR as "non-susceptibility to
ALL beta-lactams AND ALL fluoroquinolones". That is not what Kadri et al. 2018
(Clin Infect Dis 67:1803-1814, PMID 30052813, doi 10.1093/cid/ciy378) define.
Their Methods say verbatim: "intermediate or resistant to all reported agents in
carbapenem, beta-lactam, and fluoroquinolone categories", framed throughout as
resistance to all FIRST-LINE agents, with aminoglycosides, colistin/polymyxin-B
and tigecycline explicitly named as RESERVE agents that DTR patients are forced
onto and that do NOT enter the determination.

The difference is not semantic. "All beta-lactams" pulls reserve and post-2018
agents into the requirement, making the criterion STRICTER than Kadri's. This
review therefore manufactured the non-derivability it then reported as its
headline DTR finding. A round-6 microbiology referee identified this and was
right.

A second tell should have caught it earlier: the coding had only two levels,
"yes" and "not-derivable". A criterion under which no arm can ever be shown
NEGATIVE is not a criterion being applied to data.

THE CORRECTED RULE, and its asymmetry, which is principled rather than
convenient:

  DTR-POSITIVE is established when the source documents susceptibility ONLY to
  agents outside Kadri's first-line set -- colistin, aminoglycosides, tigecycline
  (reserve by Kadri's own text), or agents postdating the 2018 definition
  (ceftazidime-avibactam, cefiderocol), which Kadri's authors note future
  revisions would need to address.

  DTR-NEGATIVE is established by a SINGLE documented susceptible first-line
  agent, because DTR requires non-susceptibility to all of them.

  NOT-DERIVABLE otherwise.

WHAT IS RE-CODED, and what deliberately is not. Only arms whose own extraction
record carries the evidence are changed. Tkhilaishvili 2020 stays not-derivable:
its record reads "susceptible only to colistin +/- ceftazidime", and ceftazidime
IS first-line, so the "+/-" leaves the call genuinely open. Leveque 2023 and
Kohler 2023 stay not-derivable because this review's extraction records no
agent-level data for them, whatever their sources may print -- re-deriving from
a referee's recollection rather than from the record would repeat the original
error in the opposite direction.
"""
import csv
import pathlib
import sys

root = pathlib.Path(__file__).resolve().parent.parent
csv_path = root / "data" / "cleaned" / "phage_therapy_extraction_dataset.csv"

RECODE = {
    # arm_id: (new dtr_status, basis recorded in the dataset)
    "Aslam2019_P2": (
        "yes",
        "DTR re-derived under Kadri's first-line criterion (2026-07-30): the source states the "
        "isolate was 'sensitive to only colistin'. Colistin is a RESERVE agent by Kadri's own "
        "text and does not enter the determination, so the isolate is non-susceptible to every "
        "first-line agent and is DTR-positive. Previously coded not-derivable under this review's "
        "mis-stated 'all beta-lactams' criterion."
    ),
    "PardoFreire2025_A": (
        "yes",
        "DTR re-derived under Kadri's first-line criterion (2026-07-30): the source describes the "
        "day-75 isolate as 'susceptible only to ceftazidime-avibactam', with the full antibiogram "
        "in its Figure 2C. Ceftazidime-avibactam postdates Kadri 2018 and is not among the "
        "first-line agents the definition enumerates, so every first-line agent is non-susceptible "
        "and the isolate is DTR-positive. Flagged as a judgement about a post-2018 agent: Kadri's "
        "authors note that future revisions would need to incorporate newer agents, and under such "
        "a revision this arm could become DTR-negative."
    ),
    "Jennes2017_A": (
        "yes",
        "DTR re-derived under Kadri's first-line criterion (2026-07-30): 'colistin-only-sensitive' "
        "means susceptible to a reserve agent alone, so non-susceptible to every first-line agent, "
        "DTR-positive. Recorded although the arm is excluded from pooling as a probable "
        "Pirnay-roster duplicate, so that the de-duplication sensitivity analysis carries the "
        "correct status."
    ),
    "Chan2018_omko1_A": (
        "no",
        "DTR re-derived under Kadri's first-line criterion (2026-07-30): this review's own "
        "extraction records that the case antibiogram shows early CIPROFLOXACIN SUSCEPTIBILITY, "
        "and ceftazidime was administered therapeutically. A single susceptible first-line agent "
        "is definitive against DTR. This is the first arm in the review that can be shown "
        "DTR-NEGATIVE -- a category the previous criterion made unreachable."
    ),
    "Chung2026_A": (
        "no",
        "DTR re-derived under Kadri's first-line criterion (2026-07-30): the isolate was "
        "susceptible to meropenem, piperacillin-tazobactam and ceftazidime-avibactam and only "
        "intermediate to ciprofloxacin. Susceptible first-line agents in two categories, so "
        "definitively DTR-negative. Arm remains excluded from pooling on the population criterion."
    ),
    "Ronit2024_A": (
        "no",
        "DTR re-derived under Kadri's first-line criterion (2026-07-30): the isolate was "
        "susceptible to meropenem and ciprofloxacin -- a carbapenem and a fluoroquinolone -- so "
        "definitively DTR-negative. Arm remains excluded from pooling on the population criterion."
    ),
}

with csv_path.open(encoding="utf-8", newline="") as fh:
    reader = csv.DictReader(fh)
    fieldnames = reader.fieldnames
    rows = list(reader)

changed = []
for r in rows:
    aid = r["arm_id"]
    if aid not in RECODE:
        continue
    new_status, basis = RECODE[aid]
    if r["dtr_status"] == new_status and basis[:40] in (r.get("extraction_citation") or ""):
        continue
    old = r["dtr_status"]
    r["dtr_status"] = new_status
    r["extraction_citation"] = ((r.get("extraction_citation") or "").rstrip() + " " + basis).strip()
    changed.append((aid, old, new_status))

with csv_path.open("w", encoding="utf-8", newline="") as fh:
    writer = csv.DictWriter(fh, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(rows)

for aid, old, new in changed:
    print("  %-22s %s -> %s" % (aid, old, new))
print("")
print("%d arm(s) re-coded" % len(changed))

missing = set(RECODE) - {a for a, _, _ in changed}
if missing:
    print("already at target coding: " + ", ".join(sorted(missing)))
