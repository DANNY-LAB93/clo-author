"""Fail the build when the manuscript quotes a number the analysis did not produce.

WHY THIS EXISTS
---------------
Two consecutive peer-review rounds returned Reject on the same finding: the
prose did not match the generated tables. The first attempted fix was a scalar
manifest emitted by `scripts/R/11_manifest.R`. That was necessary but not
sufficient, and the round-4 methods referee said exactly why:

    "Emitting them did not prevent the drift; nothing reads them back."

This script reads them back. It extracts every numeric literal from the
manuscript, normalises it, and asserts that it appears either in the manifest,
in a generated table, or in a small allowlist of quantities that are legitimately
not analysis outputs (years, section numbers, thresholds fixed by protocol).
Anything else is reported as a violation and the script exits non-zero.

WHAT IT DOES NOT DO
-------------------
It cannot tell whether a number is used in the *right sentence* -- only whether
the analysis produced it at all. A number correctly copied into the wrong claim
still passes. That residual risk is real and is why the claim-source map still
matters. What this catches is the failure mode that actually occurred: values
left behind by a corpus that moved underneath them.

USAGE
-----
    python scripts/check_manuscript_numbers.py           # report and exit 1 on failure
    python scripts/check_manuscript_numbers.py --list    # also list every matched number
"""
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent

MANUSCRIPT = [
    "paper/main.tex",
    "paper/sections/intro.tex",
    "paper/sections/methods.tex",
    "paper/sections/results.tex",
    "paper/sections/discussion.tex",
]

MANIFEST = "quality_reports/manuscript_scalars_phage_therapy_mdr_pseudomonas.md"
TABLE_DIR = "paper/tables/phage_therapy_mdr_pseudomonas"

# Numbers that are legitimately not analysis outputs.
ALLOW_EXACT = {
    # protocol-fixed thresholds
    "3", "10", "20", "30", "50", "80",
    # GRADE / counting vocabulary that appears as bare digits
    "0", "1", "2", "4", "5", "6", "7", "8", "9",
    # percentages fixed by convention
    "95", "97.5", "2.5",
}
# publication years and calendar years
YEAR = re.compile(r"^(19|20)\d{2}$")

# LaTeX constructs that contain digits but are not quantities
STRIP_PATTERNS = [
    re.compile(r"\\cite[a-z]*\{[^}]*\}"),      # citation keys
    re.compile(r"\\ref\{[^}]*\}"),             # cross-references
    re.compile(r"\\Cref\{[^}]*\}"),
    re.compile(r"\\label\{[^}]*\}"),
    re.compile(r"\\input\{[^}]*\}"),
    re.compile(r"\\includegraphics(\[[^]]*\])?\{[^}]*\}"),
    re.compile(r"%.*$", re.MULTILINE),         # LaTeX comments
    re.compile(r"\\[a-zA-Z]+"),                # any remaining control sequence
]

NUM = re.compile(r"\d+(?:\.\d+)?")


def strip_latex(text: str) -> str:
    for pat in STRIP_PATTERNS:
        text = pat.sub(" ", text)
    return text


def numbers_in(text: str) -> set:
    return {m.group(0) for m in NUM.finditer(text)}


def normalise(tokens: set) -> set:
    """Collapse trailing-zero variants so 76.10 and 76.1 compare equal."""
    out = set()
    for t in tokens:
        out.add(t)
        if "." in t:
            out.add(t.rstrip("0").rstrip("."))
    return out


def main() -> int:
    show_all = "--list" in sys.argv

    manifest_text = (ROOT / MANIFEST).read_text(encoding="utf-8")
    table_text = "\n".join(
        p.read_text(encoding="utf-8")
        for p in sorted((ROOT / TABLE_DIR).glob("*.tex"))
    )
    known = normalise(numbers_in(manifest_text) | numbers_in(table_text))

    violations = []
    matched = 0

    for rel in MANUSCRIPT:
        path = ROOT / rel
        raw = path.read_text(encoding="utf-8")
        body = strip_latex(raw)
        for tok in sorted(numbers_in(body)):
            if tok in ALLOW_EXACT or YEAR.match(tok):
                continue
            candidates = {tok}
            if "." in tok:
                candidates.add(tok.rstrip("0").rstrip("."))
            if candidates & known:
                matched += 1
                if show_all:
                    print("  ok    {:<10} {}".format(tok, rel))
            else:
                violations.append((rel, tok))

    print("Manuscript number check")
    print("  manifest: {}".format(MANIFEST))
    print("  tables:   {}/*.tex".format(TABLE_DIR))
    print("  matched:  {}".format(matched))
    print("  unmatched:{}".format(len(violations)))

    if violations:
        print("\nNUMBERS IN THE MANUSCRIPT THAT THE ANALYSIS DID NOT PRODUCE")
        print("(each is either stale, hand-computed, or a quantity the manifest")
        print(" should be emitting but does not yet)\n")
        by_file = {}
        for rel, tok in violations:
            by_file.setdefault(rel, []).append(tok)
        for rel in MANUSCRIPT:
            if rel in by_file:
                print("  " + rel)
                for tok in sorted(set(by_file[rel]), key=lambda x: (len(x), x)):
                    print("      " + tok)
        return 1

    print("\nAll quoted numbers trace to the analysis outputs.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
