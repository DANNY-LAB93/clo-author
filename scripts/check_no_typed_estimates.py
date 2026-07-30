"""Fail the build when the prose types a percentage that the pipeline computes.

WHY THIS EXISTS. The macro system was built and verified against results.tex, and
its guarantee was stated as "the prose is a build product". A round-6 referee
showed that was true of one section and false of the manuscript: the Introduction
and Discussion still carried "73.0% (95% CI 55.0-85.7%)" for the MDR cell long
after the value became 75.0% (58.1-86.6%). The existing checks could not catch it
-- check_macros_match_tables.R verifies macros against tables, and both were
right; nothing verified that the PROSE used the macros.

THE RULE. A percentage literal in the manuscript is a defect when it matches, to
one decimal place, a value the pipeline emits as a macro. Such a number is by
construction a computed estimate that was typed instead of referenced, and it
will go stale the next time the corpus changes.

WHAT IS ALLOWED, and why each exemption is narrow:

  - integer percentages (95%, 100%, 0%, 20%, 80%) -- confidence levels, decision
    thresholds and boundary descriptions, none of which the pipeline computes;
  - values inside a verbatim quotation from a source, or describing a patient
    (an 81% total-body-surface burn is a fact about a person, not an estimate);
  - values explicitly marked as superseded, where the manuscript deliberately
    quotes an old figure in order to retract it. These must carry the marker
    comment % TYPED-ESTIMATE-OK on the same line, so the exemption is visible in
    the source and has to be argued for rather than assumed.

Run with --list to see every match without failing.
"""
import pathlib
import re
import sys

BS = chr(92)
root = pathlib.Path(__file__).resolve().parent.parent

MARKER = "% TYPED-ESTIMATE-OK"

macro_file = root / "paper" / "generated_scalars.tex"
macro_text = macro_file.read_text(encoding="utf-8")

# every one-decimal percentage the pipeline emits, e.g. 75.0\% inside a macro body
emitted = set(re.findall(r"(\d{1,3}\.\d)" + re.escape(BS) + r"%", macro_text))

# percentage literals in the prose, one decimal place
LIT = re.compile(r"(?<![\d.])(\d{1,3}\.\d)" + re.escape(BS) + r"%")

files = [root / "paper" / "main.tex"]
files += sorted((root / "paper" / "sections").glob("*.tex"))

list_only = "--list" in sys.argv
findings = []

for f in files:
    for lineno, line in enumerate(f.read_text(encoding="utf-8").splitlines(), 1):
        if MARKER in line:
            continue
        for m in LIT.finditer(line):
            val = m.group(1)
            if val not in emitted:
                continue
            a = max(0, m.start() - 70)
            b = min(len(line), m.end() + 40)
            findings.append((f.name, lineno, val, re.sub(r"\s+", " ", line[a:b])))

print("pipeline emits %d distinct one-decimal percentages" % len(emitted))
print("typed percentages in the prose that match one: %d" % len(findings))
print("")

if not findings:
    print("PASS: no computed estimate is typed into the prose.")
    sys.exit(0)

for fname, lineno, val, ctx in findings:
    print("  %s:%d  %s%%" % (fname, lineno, val))
    print("      ...%s..." % ctx)

print("")
if list_only:
    sys.exit(0)
print("FAIL: each of these is a computed value typed by hand. Replace it with the")
print("      macro for its cell, or -- if the manuscript quotes it deliberately as")
print("      a superseded figure -- mark the line with '%s'." % MARKER)
sys.exit(1)
