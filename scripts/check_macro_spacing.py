"""Detect and repair generated-macro references that swallowed their space.

A LaTeX control word is terminated by a non-letter, so writing

    \\CsOverallK studies

is correct -- TeX eats the space, and the \\xspace in the macro body puts it
back -- while writing

    \\CsOverallKstudies

is a single undefined control sequence. I made this mistake three separate
times while converting prose to macros, each time producing a compile failure
whose message named a control sequence that does not appear anywhere in the
source. This finds them mechanically: any control word that begins with a
defined macro name, continues with lowercase letters, and is not itself a
defined macro, is a swallowed space.

Run with --check to report only (exit 1 on any finding); default repairs.
"""
import pathlib
import re
import sys

BS = chr(92)

root = pathlib.Path(__file__).resolve().parent.parent
macros_file = root / "paper" / "generated_scalars.tex"

defined = set(re.findall(
    r"^" + re.escape(BS) + r"newcommand\{" + re.escape(BS) + r"([A-Za-z]+)\}",
    macros_file.read_text(encoding="utf-8"),
    re.M,
))
# Longest first, so \CsOverallEstCI is preferred over \CsOverallEst.
by_length = sorted(defined, key=len, reverse=True)

files = [root / "paper" / "main.tex"]
files += sorted((root / "paper" / "sections").glob("*.tex"))
files += sorted((root / "paper" / "figures").rglob("*.tex"))

check_only = "--check" in sys.argv
findings = []
repaired = 0

for f in files:
    if not f.exists():
        continue
    text = f.read_text(encoding="utf-8")
    original = text

    def fix(m):
        global repaired
        word = m.group(1)
        if word in defined:
            return m.group(0)
        for name in by_length:
            if len(word) > len(name) and word.startswith(name) and word[len(name)].islower():
                findings.append((f.relative_to(root), BS + word, BS + name + " " + word[len(name):]))
                repaired += 1
                return BS + name + " " + word[len(name):]
        return m.group(0)

    text = re.sub(re.escape(BS) + r"([A-Za-z]+)", fix, text)

    if text != original and not check_only:
        f.write_text(text, encoding="utf-8", newline=chr(10))

if not findings:
    print("no swallowed-space macro references found")
    sys.exit(0)

print("SWALLOWED-SPACE MACRO REFERENCES (%d):" % len(findings))
for rel, bad, good in findings:
    print("  %s" % rel)
    print("      %-34s -> %s" % (bad, good))

if check_only:
    sys.exit(1)
print("")
print("repaired %d reference(s)" % repaired)
