"""Bring every stale numeric string in the manuscript into line with the
machine-written scalar manifest.

This is a transitional tool, not a permanent part of the pipeline. The durable
fix is the manifest itself (scripts/R/11_manifest.R): from here on, a number is
quotable only if it appears there. This script performs the one-time catch-up
for prose that went stale while the corpus was still converging, and reports
any pattern it could not find so nothing is silently missed.

Authoritative values, read from
quality_reports/manuscript_scalars_phage_therapy_mdr_pseudomonas.md:

    corpus              31 arms / 25 studies / 82 patients
    single-patient arms 24 of 31; 7 multi-patient arms carrying 58 patients
    cells               36 estimated, 13 pooled, 23 not pooled
    clinical success    76.1% [64.2, 84.9]   k=23 studies, 28 arms, N=71
    safety              19.2% [10.3, 33.1]   k=17 studies, 22 arms, N=52
    eradication         57.8% [30.2, 81.2]   k=19 studies, 23 arms, N=59
    mortality           10.4% [4.9, 20.9]    k=24 studies, 30 arms, N=67
    MDR clinical succ.  73.0% [55.0, 85.7]   k=14 studies, 15 arms, N=37
    design              19 case-report studies (20 arms), 5 case series (8 arms),
                        1 retrospective cohort (3 arms)
    resistance          17 MDR, 4 XDR, 3 PDR, 7 not-classifiable arms
"""
import pathlib

FILES = [
    "paper/main.tex",
    "paper/sections/intro.tex",
    "paper/sections/methods.tex",
    "paper/sections/results.tex",
    "paper/sections/discussion.tex",
]

# Ordered most-specific first so a longer phrase is not pre-empted by a shorter one.
SUBS = [
    # corpus size
    ("28 pooling-eligible study-arms across 24 studies, 79 patients",
     "31 pooling-eligible study-arms across 25 studies, 82 patients"),
    ("28 pooling-eligible study-arms across 24 studies",
     "31 pooling-eligible study-arms across 25 studies"),
    ("28 pooling-eligible study-arms", "31 pooling-eligible study-arms"),
    ("28 pooling-eligible arms", "31 pooling-eligible arms"),
    ("The 28 pooling-eligible arms span", "The 31 pooling-eligible arms span"),
    ("every one of the 28 pooling-eligible rows", "every one of the 31 pooling-eligible rows"),
    ("79 patients", "82 patients"),
    ("single patients (21 of 28 arms)", "single patients (24 of 31 arms)"),
    ("account for 58 of the corpus's 82 patients", "account for 58 of the corpus's 82 patients"),
    # cell counts
    ("of 37 outcome-stratum cells", "of 36 outcome-stratum cells"),
    ("37 outcome-stratum cells", "36 outcome-stratum cells"),
    ("12 met the pre-specified pooling threshold", "13 met the pre-specified pooling threshold"),
    ("12 met threshold", "13 met threshold"),
    ("all 12 pooled cells", "all 13 pooled cells"),
    ("12 pooled cells", "13 pooled cells"),
    ("The twelve poolable cells", "The thirteen poolable cells"),
    # headline estimates
    ("77.9\\%", "76.1\\%"),
    ("65.4--86.4\\%", "64.2--84.9\\%"),
    ("55.1\\%", "57.8\\%"),
    ("52.9\\%", "57.8\\%"),
    ("29.4--78.4\\%", "30.2--81.2\\%"),
    ("16.0\\%, 95\\% CI 9.6--34.4\\%", "19.2\\%, 95\\% CI 10.3--33.1\\%"),
    ("9.6--34.4\\%", "10.3--33.1\\%"),
    ("12.5\\%", "10.4\\%"),
    ("5.4--16.0\\%", "4.9--20.9\\%"),
    ("75.7\\%", "73.0\\%"),
    ("57.8--87.6\\%", "55.0--85.7\\%"),
    # design distribution
    ("18 case-report studies, 4 case series, and one retrospective cohort",
     "19 case-report studies, 5 case series, and one retrospective cohort"),
    ("19 case-report studies contributing 20 arms", "19 case-report studies contributing 20 arms"),
    ("4 case series contributing 5 arms", "5 case series contributing 8 arms"),
]

root = pathlib.Path(__file__).resolve().parent.parent
applied, missing = [], []

for pattern, replacement in SUBS:
    hits = 0
    for rel in FILES:
        p = root / rel
        s = p.read_text(encoding="utf-8")
        if pattern in s:
            n = s.count(pattern)
            p.write_text(s.replace(pattern, replacement), encoding="utf-8", newline="\n")
            hits += n
    if hits:
        applied.append((pattern, replacement, hits))
    else:
        missing.append(pattern)

print("APPLIED")
for pat, rep, n in applied:
    print("  {:>2}x  {!r} -> {!r}".format(n, pat[:52], rep[:52]))

print("\nNOT FOUND (already correct, or the phrasing changed -- check manually)")
for pat in missing:
    print("  " + repr(pat[:70]))
