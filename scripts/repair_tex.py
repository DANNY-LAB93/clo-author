"""One-off repair of LaTeX escape damage in the manuscript .tex files.

Editing .tex through shell heredocs converted several LaTeX control sequences
into the control characters they name:

    backslash-tau  ->  TAB + "au"       (renders as "au^2", no LaTeX error)
    backslash-ref  ->  CR  + "ef{...}"  (renders the literal text "ef{sec:...}")

Neither raises a LaTeX error, so a successful compile does not catch them.
Control characters are referenced by chr() rather than written literally, since
a literal control character in the source is what caused the damage in the
first place.
"""
import pathlib
import re

TAB = chr(9)
CR = chr(13)
BS = chr(92)  # backslash

FILES = [
    "paper/main.tex",
    "paper/sections/intro.tex",
    "paper/sections/methods.tex",
    "paper/sections/results.tex",
    "paper/sections/discussion.tex",
]

# TAB followed by the tail of a LaTeX command name -> restore the backslash.
TAB_REPAIRS = [
    ("au", "tau"),
    ("imes", "times"),
    ("extit", "textit"),
    ("extbf", "textbf"),
    ("extcite", "textcite"),
]

root = pathlib.Path(__file__).resolve().parent.parent
total = 0

for rel in FILES:
    p = root / rel
    original = p.read_text(encoding="utf-8")
    s = original

    for tail, command in TAB_REPAIRS:
        s = s.replace(TAB + tail, BS + command)

    # CR + "ef{" -> backslash + "ref{"
    s = s.replace(CR + "ef{", BS + "ref{")
    s = re.sub(r"(Section)~\s*\n\s*ef\{", r"\1~" + BS + BS + "ref{", s)
    s = re.sub(r"(?m)^ef\{", BS + BS + "ref{", s)
    s = re.sub(r"([ (~])ef\{sec:", r"\1" + BS + BS + "ref{sec:", s)

    # collapse any doubled backslash introduced by an earlier repair attempt
    s = s.replace("$" + BS + BS + "tau", "$" + BS + "tau")

    # whatever control characters survive are damage, not content
    s = s.replace(CR, "").replace(TAB, "")

    if s != original:
        p.write_text(s, encoding="utf-8", newline="\n")
        print("repaired: " + rel)
        total += 1
    else:
        print("clean:    " + rel)

print("files changed: " + str(total))
