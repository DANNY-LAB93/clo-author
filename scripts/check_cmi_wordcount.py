"""Word-count the CMI submission version against the journal's 3,500 limit.

Counts the main text only -- Introduction through Discussion -- excluding the
title block, abstract, keywords, references and all LaTeX comments, which is
what CMI counts. Macro calls count as one word each, which is what they
typeset as.
"""
import pathlib
import re

BS = chr(92)
p = pathlib.Path(r"C:\Users\Equipo\Desktop\claude code tesisi\clo-author\paper\main_cmi.tex")
s = p.read_text(encoding="utf-8")

# main text runs from \section{Introduction} to \printbibliography
i = s.find(BS + "section{Introduction}")
j = s.find(BS + "printbibliography")
body = s[i:j]

# strip comments, then LaTeX control sequences and braces
body = re.sub(r"(?m)^%.*$", "", body)
body = re.sub(r"(?<!" + re.escape(BS) + r")%.*$", "", body, flags=re.M)

sections = {}
for m in re.finditer(re.escape(BS) + r"section\*?\{([^}]+)\}", body):
    sections[m.start()] = m.group(1)

def wc(chunk):
    t = re.sub(re.escape(BS) + r"[a-zA-Z]+\*?", " X ", chunk)   # macro -> one token
    t = re.sub(r"[{}$~\\]", " ", t)
    t = re.sub(r"\s+", " ", t)
    return len([w for w in t.split() if re.search(r"[A-Za-z0-9]", w)])

keys = sorted(sections)
total = 0
for n, k in enumerate(keys):
    end = keys[n + 1] if n + 1 < len(keys) else len(body)
    c = wc(body[k:end])
    total += c
    print("  %-46s %5d" % (sections[k][:46], c))

print("  " + "-" * 52)
print("  %-46s %5d" % ("TOTAL main text", total))
print("  %-46s %5d" % ("CMI limit", 3500))
print("  %-46s %5d" % ("margin", 3500 - total))

# abstract
a = re.search(re.escape(BS) + r"begin\{abstract\}(.*?)" + re.escape(BS) + r"end\{abstract\}", s, re.S)
if a:
    print()
    print("  %-46s %5d  (limit 300)" % ("structured abstract", wc(a.group(1))))
