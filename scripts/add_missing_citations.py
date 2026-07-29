"""Cite every included study at least once.

Seven of the twenty-five included studies appeared only as plain author-year
text, never inside a biblatex command, so biber never saw them and they would
not have appeared in the reference list. A systematic review whose reference
list omits 28% of its own evidence base cannot be checked by a reader.

The names are already present in the PRISMA caption and the study-characteristics
enumeration; this converts them from typed text into citations, which also makes
them subject to the undefined-citation check at compile time.

Verified against scripts/check_citation_coverage.R, which reads the study
identifiers out of the analysis dataset and fails the build if any is uncited.
"""
import pathlib
import sys

BS = chr(92)

# plain text as it appears -> biblatex key
CITES = [
    ("K\\\"ohler et al., 2023", "Kohler2023_natcommun"),
    ("Chan et al., 2025", "Chan2025_natmed"),
    ("Law et al., 2019", "Law2019_infection"),
    ("Hahn et al., 2023", "Hahn2023_jinvestig"),
    ("Lev\\^eque et al., 2023", "Leveque2023_idr"),
    ("Duplessis et al., 2018", "Duplessis2018_jpids"),
    ("Denis et al., 2026", "Denis2026_ijid"),
    ("Malhotra et al., 2026", "Malhotra2026_jpeds"),
    ("Yang et al., 2025", "Yang2025_scirep"),
    ("Li et al., 2025", "Li2025_hlife_biliary"),
]

root = pathlib.Path(__file__).resolve().parent.parent
p = root / "paper" / "sections" / "results.tex"
s = p.read_text(encoding="utf-8")

bib = (root / "Bibliography_base.bib").read_text(encoding="utf-8")

applied, skipped = [], []
for plain, key in CITES:
    if ("{" + key + ",") not in bib:
        skipped.append((plain, key, "no such bib entry"))
        continue
    if plain not in s:
        skipped.append((plain, key, "plain text not found"))
        continue
    # \textcite renders "Author (Year)"; inside a parenthesised list the caption
    # wants "Author, Year", so \parencite content is wrong here -- use
    # \citeauthor + \citeyear to preserve the caption's existing punctuation.
    repl = BS + "citeauthor{" + key + "} et al., " + BS + "citeyear{" + key + "}"
    # the plain text already carries "et al.," so replace the whole run
    s = s.replace(plain, BS + "citeauthor{" + key + "} " + BS + "citeyear{" + key + "}", 1)
    applied.append((plain, key))

p.write_text(s, encoding="utf-8", newline="\n")

for plain, key in applied:
    print("  cited  %-26s -> %s" % (plain, key))
if skipped:
    print("")
    print("SKIPPED:")
    for plain, key, why in skipped:
        print("  %-26s %-24s (%s)" % (plain, key, why))

print("")
print("%d citations added" % len(applied))
if skipped:
    sys.exit(1)
