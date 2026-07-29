"""Find LaTeX control sequences that lost their leading backslash.

These are invisible to the compiler: `\texttt{x}` that became `exttt{x}` after a
regex ate the `\t` typesets the literal string "exttt" and raises no error. The
same class of damage produced "au^2" for tau and a literal "ef{sec:...}" for a
cross-reference. repair_tex.py fixes damage where the control character is still
present; this finds damage where the character was consumed entirely, leaving a
bare command tail in running text.
"""
import pathlib
import re

BS = chr(92)

# Command tails that cannot legitimately begin a word in this manuscript.
TAILS = [
    "exttt", "extbf", "extit", "extcite", "extsc",
    "egin", "nd{", "ef{", "aption", "abel{",
    "au^", "imes", "rac{", "oprule", "ottomrule", "idrule",
    "Cref{", "cite{", "arencite",
]

root = pathlib.Path(__file__).resolve().parent.parent
files = [root / "paper" / "main.tex"]
files += sorted((root / "paper" / "sections").glob("*.tex"))
files += sorted((root / "paper" / "figures").rglob("*.tex"))

hits = []
for f in files:
    if not f.exists():
        continue
    for i, line in enumerate(f.read_text(encoding="utf-8").splitlines(), 1):
        for tail in TAILS:
            for m in re.finditer(re.escape(tail), line):
                j = m.start()
                # Legitimate when the tail is the end of a real command: the
                # character before it completes the command name, and somewhere
                # to its left there is a backslash with only letters between.
                k = j - 1
                while k >= 0 and line[k].isalpha():
                    k -= 1
                if k >= 0 and line[k] == BS:
                    continue          # part of a real \command
                if j > 0 and line[j - 1].isalpha():
                    continue          # inside an ordinary word
                hits.append((f.relative_to(root), i, tail,
                             line[max(0, j - 45):j + 30]))

if not hits:
    print("no orphaned command tails found")
else:
    print("ORPHANED COMMAND TAILS (" + str(len(hits)) + "):")
    for rel, ln, tail, ctx in hits:
        print("  %s:%d  [%s]" % (rel, ln, tail))
        print("      ..." + ctx.replace(chr(9), " ") + "...")
