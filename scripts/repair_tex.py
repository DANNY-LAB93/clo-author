"""Repair LaTeX escape damage caused by writing .tex through Python string
literals in which a backslash sequence was interpreted as a control character.

Python turns backslash-t, -r, -b, -f, -v, -a and -0 into control characters
inside a non-raw string. When the following text is a LaTeX command name, the
result is a control character followed by the tail of the command:

    backslash-tau    -> TAB       + "au"      renders as "au^2"
    backslash-ref    -> CR        + "ef{...}" renders as "ef{sec:...}"
    backslash-begin  -> BACKSPACE + "egin{}"  hard LaTeX error
    backslash-frac   -> FORMFEED  + "rac{}"
    backslash-verb   -> VTAB      + "erb"

The first two produce no LaTeX error at all and survive every compile check;
the third does error, which is how it was caught. This script repairs all of
them by reattaching the backslash.

Control characters are referenced by chr() rather than written literally,
because a literal control character in this source is what caused the damage.
"""
import pathlib
import re

TAB = chr(9)
LF = chr(10)
VTAB = chr(11)
FF = chr(12)
CR = chr(13)
BS = chr(92)
BELL = chr(7)
BACKSPACE = chr(8)
NUL = chr(0)

FILES = [
    "paper/main.tex",
    "paper/sections/intro.tex",
    "paper/sections/methods.tex",
    "paper/sections/results.tex",
    "paper/sections/discussion.tex",
    "paper/figures/phage_therapy_mdr_pseudomonas/prisma_flow_diagram.tex",
]

# (control character, tail of the LaTeX command, full command name)
REPAIRS = [
    (TAB, "au", "tau"),
    (TAB, "imes", "times"),
    (TAB, "extit", "textit"),
    (TAB, "extbf", "textbf"),
    (TAB, "extcite", "textcite"),
    (TAB, "extsc", "textsc"),
    (TAB, "ab:", "tab:"),
    (TAB, "oprule", "toprule"),
    (BACKSPACE, "egin", "begin"),
    (BACKSPACE, "ottomrule", "bottomrule"),
    (BACKSPACE, "ibliography", "bibliography"),
    (FF, "rac", "frac"),
    (FF, "ootnote", "footnote"),
    (VTAB, "erb", "verb"),
    (VTAB, "space", "vspace"),
    (BELL, "lpha", "alpha"),
    (CR, "ef{", "ref{"),
    (CR, "ow", "row"),
]

root = pathlib.Path(__file__).resolve().parent.parent
changed = 0

for rel in FILES:
    p = root / rel
    if not p.exists():
        print("skip (absent): " + rel)
        continue
    original = p.read_text(encoding="utf-8")
    s = original

    for ctrl, tail, command in REPAIRS:
        s = s.replace(ctrl + tail, BS + command)

    # "Section~" + newline + bare "ef{" left after an earlier CR strip
    s = re.sub(r"(Section)~\s*\n\s*ef\{", r"\1~" + BS + BS + "ref{", s)
    s = re.sub(r"(?m)^ef\{", BS + BS + "ref{", s)
    s = re.sub(r"([ (~])ef\{sec:", r"\1" + BS + BS + "ref{sec:", s)

    # collapse a doubled backslash introduced by an earlier repair attempt
    s = s.replace("$" + BS + BS + "tau", "$" + BS + "tau")

    # any surviving control character other than newline is damage, not content
    for ctrl in (NUL, BELL, BACKSPACE, TAB, VTAB, FF, CR):
        s = s.replace(ctrl, "")

    if s != original:
        p.write_text(s, encoding="utf-8", newline="\n")
        print("repaired: " + rel)
        changed += 1
    else:
        print("clean:    " + rel)

print("files changed: " + str(changed))
