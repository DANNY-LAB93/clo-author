"""Stage 1 of screening: deterministic rules only, validated against known positives.

WHY A RULE STAGE FIRST. The union of the two search arms is roughly 9,500
records, and the review has already been criticised once for screening that could
not be audited. A rule stage is auditable in a way judgement is not: every
exclusion names the rule that fired, the rules are printable in the Methods, and
anyone can re-run them and get the same answer. Whatever survives goes to
title/abstract assessment, which is where judgement belongs.

THE VALIDATION THAT MAKES THIS SAFE. The 42 studies already included are known
positives. A rule that excludes any of them is wrong by construction, and the
script FAILS rather than reporting, because a filter that silently drops a known
eligible study would do the same to an unknown one. Run --validate before
--apply; --apply refuses to run if validation fails.

WHAT IS DELIBERATELY NOT A RULE:
  - "must mention Pseudomonas". Arm B exists precisely because Pirnay 2024,
    Green 2023, Leitner 2021 and Liu 2025 name no organism in title, abstract or
    MeSH. Filtering on the organism would undo the arm and re-lose the four.
  - "must not be a review". A review of phage therapy can be the only published
    account of a case series, and this corpus already contains records recovered
    by citation-chasing a review's risk-of-bias table.
  - year filters. The window is already in the query.

USAGE
    python scripts/screen_stage1_rules.py --validate
    python scripts/screen_stage1_rules.py --apply --out revision_sistematica/cribado/screening_stage1.csv
"""
import argparse
import csv
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
CORPUS = ROOT / "revision_sistematica" / "busqueda" / "screening_pubmed_union.csv"
INDEX = ROOT / "quality_reports" / "corpus_identifier_index.txt"

csv.field_size_limit(10_000_000)


def has_mesh(r, term):
    return re.search(r"(^|;\s*)%s(\s*;|$)" % re.escape(term), r["mesh"] or "", re.I) is not None


def pubtypes(r):
    return {p.strip().lower() for p in (r["pubtypes"] or "").split(";") if p.strip()}


# Each rule returns a reason string to EXCLUDE, or None to keep.
# Rules are intentionally few and blunt. Anything requiring interpretation is
# not a rule; it is stage 2.

def rule_animal_not_human(r):
    """Indexed Animals and not Humans -- MEDLINE's own species determination."""
    if has_mesh(r, "Animals") and not has_mesh(r, "Humans"):
        return "preclinical: MeSH Animals without Humans"
    return None


def rule_non_data_pubtype(r):
    """Article types that cannot carry primary clinical observations."""
    pts = pubtypes(r)
    blocked = {"editorial", "comment", "news", "newspaper article", "biography",
               "published erratum", "retraction of publication", "patient education handout"}
    hit = pts & blocked
    # A record typed BOTH editorial and journal article may still carry data.
    if hit and not (pts & {"case reports", "clinical trial", "randomized controlled trial",
                           "observational study", "multicenter study", "comparative study"}):
        return "non-data article type: %s" % ", ".join(sorted(hit))
    return None


def rule_no_title(r):
    if not (r["title"] or "").strip():
        return "no title retrieved"
    return None


def rule_phage_as_laboratory_tool(r):
    """Phage display, typing and library work -- the word "phage" as a molecular
    biology technique, not as a therapeutic. This is the only content-based rule
    that survived validation.

    Four candidate content filters were tested against the 42 known positives.
    Requiring MeSH Humans lost 11 of them (recent records are not yet indexed --
    the same defect that makes Ovid's "limit to humans" wrong here). Requiring a
    clinical keyword in title or abstract lost 5. The disjunction of the two
    still lost 2, Leveque 2023 and Ngauy 2026. Only this rule lost none, and it
    removes 2,140 records. The lesson is recorded because it keeps recurring:
    keyword classifiers fail on interpretive variables in this corpus, and the
    only safe automated rules are the ones about what a paper IS, not what it is
    about."""
    pat = (r"\b(phage display|phage typing|display librar|biopanning|"
           r"phagemid|scFv|nanobody)\b")
    blob = (r["title"] or "") + " " + (r["abstract"] or "")
    if re.search(pat, blob, re.I):
        return "phage as a laboratory technique (display/typing/library), not a therapeutic"
    return None


RULES = [rule_no_title, rule_non_data_pubtype, rule_animal_not_human,
         rule_phage_as_laboratory_tool]


def load_corpus():
    if not CORPUS.exists():
        sys.exit("corpus not fetched: run scripts/fetch_screening_corpus.py first")
    with open(CORPUS, encoding="utf-8", newline="") as fh:
        return list(csv.DictReader(fh))


def known_pmids():
    out = {}
    for line in INDEX.read_text(encoding="utf-8").splitlines():
        if line.strip() and not line.startswith("#"):
            ident, _, sid = line.partition("\t")
            if ident.startswith("pmid:"):
                out[ident.split(":", 1)[1]] = sid.strip()
    return out


def classify(r):
    for rule in RULES:
        reason = rule(r)
        if reason:
            return reason, rule.__name__
    return None, None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--validate", action="store_true")
    ap.add_argument("--apply", action="store_true")
    ap.add_argument("--out", default="revision_sistematica/cribado/screening_stage1.csv")
    args = ap.parse_args()

    rows = load_corpus()
    known = known_pmids()
    print("records in corpus  :", len(rows))
    print("known positives    :", len(known), "PMIDs from", len(set(known.values())), "studies")

    present = [r for r in rows if r["pmid"] in known]
    print("known positives present in the fetched corpus:", len(present))
    print()

    # ---- validation: no rule may exclude a known positive ----
    casualties = []
    for r in present:
        reason, rule = classify(r)
        if reason:
            casualties.append((r["pmid"], known[r["pmid"]], rule, reason, r["title"][:60]))

    if casualties:
        print("VALIDATION FAILED -- these rules exclude known eligible studies:")
        for pmid, sid, rule, reason, title in casualties:
            print("   %-9s %-24s %s" % (pmid, sid, rule))
            print("      %s" % reason)
            print("      %s" % title)
    else:
        print("VALIDATION PASSED: no rule excludes any known included study.")
    print()

    # ---- what the rules would do to the whole corpus ----
    counts, kept = {}, []
    for r in rows:
        reason, rule = classify(r)
        if reason:
            counts[rule] = counts.get(rule, 0) + 1
        else:
            kept.append(r)
    print("stage-1 exclusions by rule:")
    for rule, n in sorted(counts.items(), key=lambda kv: -kv[1]):
        print("   %-26s %5d" % (rule, n))
    print("   %-26s %5d" % ("TOTAL EXCLUDED", sum(counts.values())))
    print()
    print("advancing to stage 2       : %5d" % len(kept))

    if args.apply:
        if casualties:
            sys.exit("\nrefusing to apply: validation failed (see above)")
        out = ROOT / args.out
        with open(out, "w", encoding="utf-8", newline="") as fh:
            w = csv.DictWriter(fh, fieldnames=list(rows[0]) + ["stage1", "stage1_rule"])
            w.writeheader()
            for r in rows:
                reason, rule = classify(r)
                d = dict(r)
                d["stage1"] = "EXCLUDED" if reason else "ADVANCE"
                d["stage1_rule"] = reason or ""
                w.writerow(d)
        print("\nwrote", out, "(every record, with its rule)")


if __name__ == "__main__":
    main()
