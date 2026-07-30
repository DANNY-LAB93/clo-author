"""Where do percentage literals still survive in the manuscript?

The macro system was built and verified against results.tex. A round-6 referee
found that the Introduction and Discussion still carry hardcoded estimates --
"73.0% clinical success, 95% CI 55.0-85.7%" for the MDR cell, whose current value
is 75.0% (58.1-86.6%). The claim that "the prose is a build product" was
therefore true of one section and false of the manuscript.

This quantifies the gap per file so the fix can be scoped, and it is the check
that should have existed from the start.
"""
import pathlib
import re

BS = chr(92)
root = pathlib.Path(__file__).resolve().parent.parent

# a percentage literal: digits, optional decimal, then an escaped percent sign
LIT = re.compile(r"\b\d{1,3}(?:\.\d+)?" + re.escape(BS) + r"%")
# a reference to a generated macro
MAC = re.compile(re.escape(BS) + r"[A-Z][A-Za-z]*(?:Est|EstCI|CI|Lo|Hi|Tau|FT|DL|FE)\b")

files = [root / "paper" / "main.tex"]
files += sorted((root / "paper" / "sections").glob("*.tex"))

total_lit = 0
print("%-18s %8s %8s   surviving literals" % ("file", "literals", "macros"))
print("-" * 78)
for f in files:
    body = f.read_text(encoding="utf-8")
    lits = LIT.findall(body)
    macs = MAC.findall(body)
    total_lit += len(lits)
    shown = " ".join(sorted(set(lits))[:14])
    print("%-18s %8d %8d   %s" % (f.name, len(lits), len(macs), shown))

print("-" * 78)
print("total surviving percentage literals: %d" % total_lit)
print("")
print("Context for each, so a reader can judge which are estimates and which are")
print("thresholds, quotations or unrelated quantities:")
print("")
for f in files:
    body = f.read_text(encoding="utf-8")
    for m in LIT.finditer(body):
        a, b = max(0, m.start() - 78), min(len(body), m.end() + 42)
        print("  %-16s ...%s..." % (f.name, re.sub(r"\s+", " ", body[a:b])))
