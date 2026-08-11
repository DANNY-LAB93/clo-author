"""Make every study in the corpus traceable from its own extraction record.

Seven studies carried no PMID, PMC id or DOI in extraction_citation. They were
resolvable from the bibliography, so nothing in the manuscript was wrong -- but
the extraction record is what a screening pass greps, and the consequence was
concrete: the round-5 un-blocked search produced a list of 28 records "never
screened" and one of them, Ngauy 2026, was already in the corpus. Its citation
records page numbers ("p.1 Abstract; p.3 Phage selection") rather than an
identifier, so no regex could match it, and a study already included was
re-screened as new.

Identifiers below were taken from each study's bibliography entry and, where the
entry carried only a DOI, recovered from PubMed:

  Blasco 2023          PMID 37275366   (bib had DOI only)
  Ferry 2022           PMID 35869081   (bib had PMC + DOI; PMID via PubMed)
  Liu 2025 perinephric PMID 40633848
  Ngauy 2026           PMID 41853116
  Racenis 2022 femur   PMID 35547216
  Racenis 2023 LVAD    PMID 37243293
  Tkhilaishvili 2020   PMID 31527029   (bib had DOI only)

Each is prepended to the arm's extraction_citation as a leading identifier
block, so the record is greppable without disturbing the provenance narrative
that follows it.
"""
import csv
import pathlib
import sys

root = pathlib.Path(__file__).resolve().parent.parent
csv_path = root / "metaanalisis" / "datos" / "phage_therapy_extraction_dataset.csv"

# study_id -> identifier block to prepend
IDS = {
    "Blasco2023":          "PMID 37275366, PMC10235614, doi 10.3389/fmed.2023.1199657.",
    "Ferry2022":           "PMID 35869081, PMC9306240, doi 10.1038/s41467-022-31837-9.",
    "Liu2025_perinephric": "PMID 40633848, doi 10.1016/j.ijantimicag.2025.107570.",
    "Ngauy2026":           "PMID 41853116, PMC12955376, doi 10.1128/asmcr.00108-25.",
    "Racenis2022_femur":   "PMID 35547216, doi 10.3389/fmed.2022.851310.",
    "Racenis2023_LVAD":    "PMID 37243293, PMC10223274, doi 10.3390/v15051210.",
    "Tkhilaishvili2020":   "PMID 31527029, PMC7187616, doi 10.1128/AAC.00924-19.",
}

with csv_path.open(encoding="utf-8", newline="") as fh:
    reader = csv.DictReader(fh)
    fieldnames = reader.fieldnames
    rows = list(reader)

patched = 0
seen = set()
for r in rows:
    sid = r["study_id"]
    if sid not in IDS:
        continue
    cite = r.get("extraction_citation") or ""
    block = IDS[sid]
    # idempotent: skip if the PMID is already present anywhere in the citation
    pmid = block.split(",")[0]
    if pmid in cite:
        continue
    r["extraction_citation"] = (block + " " + cite).strip()
    patched += 1
    seen.add(sid)

with csv_path.open("w", encoding="utf-8", newline="") as fh:
    writer = csv.DictWriter(fh, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(rows)

for sid in sorted(seen):
    print("  identifier block prepended: " + sid)
print("")
print("%d arm(s) across %d study(ies) patched" % (patched, len(seen)))

missing = set(IDS) - seen
if missing:
    print("")
    print("ALREADY TRACEABLE, no change needed: " + ", ".join(sorted(missing)))
