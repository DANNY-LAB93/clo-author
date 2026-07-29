"""Classify every numeric literal the manuscript still quotes without a
pipeline-generated source.

check_manuscript_numbers.py reports a count of unmatched numbers. A count is not
an audit: it was 55 for several rounds and I could not honestly say all 55 were
benign without looking at each. This prints each unmatched number with the text
around it, grouped by what kind of number it appears to be, so the residue can
be judged rather than assumed.

Categories that are legitimately not pipeline-derived:
  - registry and identifier fragments (NCT numbers, DOIs, PMIDs, ISSNs)
  - section, table and figure cross-reference numbers
  - dates and years
  - values quoted FROM a cited source rather than computed here
  - methodological thresholds fixed by protocol (k >= 3, N >= 20, alpha)

Anything not in those categories is a number the manuscript asserts on its own
authority, and each one is either a macro waiting to be written or an error.
"""
import pathlib
import re
import subprocess
import sys

root = pathlib.Path(__file__).resolve().parent.parent

# Reuse the existing checker's notion of "unmatched" rather than re-deriving it.
res = subprocess.run([sys.executable, str(root / "scripts" / "check_manuscript_numbers.py")],
                     capture_output=True, text=True, cwd=str(root))
out = res.stdout + res.stderr
unmatched = [ln.strip() for ln in out.splitlines() if re.fullmatch(r"\s+[0-9][0-9.]*", ln)]
unmatched = sorted(set(unmatched), key=lambda x: (len(x), x))

sources = [root / "paper" / "main.tex"] + sorted((root / "paper" / "sections").glob("*.tex"))
text = {}
for f in sources:
    text[f.name] = f.read_text(encoding="utf-8")

PATTERNS = [
    ("registry/identifier", re.compile(r"(NCT\d*|doi|DOI|PMID|PMC|ISSN|ClinicalTrials)")),
    ("cross-reference",     re.compile(r"(Section|Table|Figure|Cref|ref\{|item|PRISMA 2020)")),
    ("date/year",           re.compile(r"(20\d\d|19\d\d|-\d\d-\d\d)")),
    ("protocol threshold",  re.compile(r"(threshold|at least|k *[>\\]|N *[>\\]|pre-specified|alpha)")),
    ("p-value/statistic",   re.compile(r"(\$p\s*=|p-value|Q-between|coefficient|standard error)")),
    ("quoted from source",  re.compile(r"(cite|textcite|parencite|citeauthor)")),
]

buckets = {}
for num in unmatched:
    ctxs = []
    for fname, body in text.items():
        for m in re.finditer(r"(?<![0-9.])" + re.escape(num) + r"(?![0-9])", body):
            a, b = max(0, m.start() - 90), min(len(body), m.end() + 60)
            ctxs.append((fname, re.sub(r"\s+", " ", body[a:b])))
    if not ctxs:
        buckets.setdefault("not found in prose (table/figure only)", []).append((num, ""))
        continue
    fname, ctx = ctxs[0]
    label = "UNCLASSIFIED -- asserted on the manuscript's own authority"
    for name, pat in PATTERNS:
        if pat.search(ctx):
            label = name
            break
    buckets.setdefault(label, []).append((num, "%s :: ...%s..." % (fname, ctx)))

order = ["UNCLASSIFIED -- asserted on the manuscript's own authority"] + \
        [n for n, _ in PATTERNS] + ["not found in prose (table/figure only)"]

print("Unmatched numeric literals: %d\n" % len(unmatched))
for label in order:
    items = buckets.get(label)
    if not items:
        continue
    print("=" * 78)
    print("%s  (%d)" % (label.upper(), len(items)))
    print("=" * 78)
    for num, ctx in items:
        print("  %-10s %s" % (num, ctx[:150]))
    print()

n_bad = len(buckets.get("UNCLASSIFIED -- asserted on the manuscript's own authority", []))
print("Numbers requiring a macro or a correction: %d" % n_bad)
