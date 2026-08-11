"""Stage-1 rule screening across ALL sources, not just PubMed.

WHY A SECOND ENGINE. The original screen_stage1_rules.py is written against the
PubMed CSV and its decisions on arm A are already audited and acted on. This runs
the SAME rules over the unified corpus (all eight sources) without disturbing
that file. The rules themselves are imported, not copied, so there is one
definition of each and they cannot drift apart.

THE APPLICABILITY PROBLEM, AND HOW IT IS HANDLED. Two of the four rules read
fields only MEDLINE supplies:

  - rule_animal_not_human needs MeSH. 48.7% of the corpus has it.
  - rule_non_data_pubtype needs publication types. Scopus supplies its own
    "Document Type" vocabulary, which is mapped here; registry records have
    neither.

An absent field is NOT a negative finding. A Scopus record with no MeSH has not
been shown to be human research; it has been shown nothing. So a rule that cannot
read its field returns NOT APPLICABLE and the record advances to stage 2, where a
human reads it. The alternative -- treating silence as evidence -- is the exact
failure this review already documented when three of four candidate content
filters lost known-positive studies.

The report states, per rule, how many records it could and could not judge. That
number belongs in the manuscript: a rule applied to 49% of the corpus is not the
same claim as a rule applied to all of it.

USAGE
    python scripts/screen_stage1_all_sources.py
    python scripts/screen_stage1_all_sources.py --apply
"""
import argparse
import collections
import csv
import pathlib
import re
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from screen_stage1_rules import (rule_no_title, rule_phage_as_laboratory_tool,
                                 known_pmids)

ROOT = pathlib.Path(__file__).resolve().parent.parent
CORPUS = ROOT / "revision_sistematica" / "cribado" / "screening_corpus_all.csv"
OUT = ROOT / "revision_sistematica" / "cribado" / "screening_stage1_all.csv"
REPORT = ROOT / "quality_reports" / "stage1_all_sources.md"

csv.field_size_limit(200_000_000)

NOT_APPLICABLE = "__NA__"

# Scopus document types that cannot carry primary clinical observations, mapped
# onto the same intent as the PubMed publication-type rule. "Conference Paper"
# is deliberately NOT here: conference abstracts are exactly where compassionate
# -use cases surface first, and excluding them by rule would contradict this
# review's own argument about publication bias.
SCOPUS_BLOCKED = {"editorial", "erratum", "note", "letter", "short survey",
                  "retracted"}
SCOPUS_KEEP = {"article", "review", "conference paper", "book chapter", "book",
               "data paper"}


def rule_animal_not_human_scoped(r):
    """MeSH Animals without Humans -- MEDLINE's own species determination.

    Fires only where MeSH exists. Without it the record is unjudged, not human.
    """
    if r.get("has_mesh") != "1":
        return NOT_APPLICABLE
    mesh = r.get("mesh") or ""
    has = lambda t: re.search(r"(^|;\s*)%s(\s*;|$)" % re.escape(t), mesh, re.I)
    if has("Animals") and not has("Humans"):
        return "preclinico: MeSH Animals sin Humans"
    return None


def rule_non_data_doctype(r):
    """Article types that cannot carry primary clinical observations.

    Reads PubMed publication types and Scopus document types from the same
    merged field. A record typed both editorial AND something data-bearing is
    kept: the combination usually means a journal filed a case report under an
    editorial heading.
    """
    if r.get("has_doctype") != "1":
        return NOT_APPLICABLE
    types = {t.strip().lower() for t in re.split(r"[;,]", r.get("doctype") or "")
             if t.strip()}
    blocked = SCOPUS_BLOCKED | {
        "comment", "news", "newspaper article", "biography",
        "published erratum", "retraction of publication",
        "patient education handout"}
    data_bearing = {"case reports", "clinical trial", "randomized controlled trial",
                    "observational study", "multicenter study", "comparative study",
                    "journal article", "article"}
    hit = types & blocked
    if hit and not (types & data_bearing):
        return "tipo documental sin datos primarios: %s" % ", ".join(sorted(hit))
    return None


RULES = [rule_no_title, rule_non_data_doctype, rule_animal_not_human_scoped,
         rule_phage_as_laboratory_tool]


def classify(r):
    """First rule that excludes wins. NOT APPLICABLE never excludes."""
    for rule in RULES:
        reason = rule(r)
        if reason and reason != NOT_APPLICABLE:
            return reason, rule.__name__
    return None, None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true",
                    help="escribir el CSV con la decision de cada registro")
    args = ap.parse_args()

    if not CORPUS.exists():
        sys.exit("falta el corpus unificado: corre scripts/build_screening_corpus.py")
    with open(CORPUS, encoding="utf-8", newline="") as fh:
        rows = list(csv.DictReader(fh))
    print("corpus unificado: %d informes\n" % len(rows))

    applicable = collections.Counter()
    excluded = collections.Counter()
    for r in rows:
        for rule in RULES:
            v = rule(r)
            if v != NOT_APPLICABLE:
                applicable[rule.__name__] += 1
        reason, which = classify(r)
        r["stage1"] = "EXCLUDED" if reason else "ADVANCE"
        r["stage1_rule"] = which or ""
        r["stage1_reason"] = reason or ""
        if which:
            excluded[which] += 1

    n = len(rows)
    print("%-34s %10s %10s" % ("regla", "aplicable", "excluye"))
    for rule in RULES:
        k = rule.__name__
        print("  %-32s %6d (%4.1f%%) %8d"
              % (k, applicable[k], 100.0 * applicable[k] / n, excluded[k]))
    n_ex = sum(excluded.values())
    print("\n  TOTAL EXCLUIDOS               %6d" % n_ex)
    print("  PASAN A ETAPA 2               %6d" % (n - n_ex))

    # --- known-positive audit, AT STUDY LEVEL ---
    #
    # The test is not "every identifier of an included study survives" but "each
    # included study keeps at least one surviving report". Those differ, and the
    # difference is not academic: the corpus contains "Author Correction: Phage
    # therapy with nebulized cocktail BX004-A...", an erratum whose PMID the
    # identifier index maps to Weiner2025_BX004A. Excluding that erratum is
    # correct -- a correction carries no primary data -- and the study stays
    # included through its original report. A record-level audit failed on it and
    # would have pushed us to weaken a rule that was right.
    known = known_pmids()
    by_study = collections.defaultdict(list)
    for r in rows:
        if r["pmid"] and r["pmid"] in known:
            by_study[known[r["pmid"]]].append(r)

    lost, kept = [], []
    for sid, recs in sorted(by_study.items()):
        if any(x["stage1"] == "ADVANCE" for x in recs):
            kept.append(sid)
        else:
            lost.append((sid, recs))

    print("\nestudios incluidos presentes en el corpus: %d" % len(by_study))
    print("  conservan al menos un informe : %d" % len(kept))
    dropped = [(sid, x) for sid, recs in by_study.items() for x in recs
               if x["stage1"] == "EXCLUDED"]
    if dropped:
        print("  informes sueltos excluidos    : %d" % len(dropped))
        for sid, x in dropped[:6]:
            print("      %-22s %s -- %s" % (sid, x["pmid"], x["stage1_reason"][:58]))
    if lost:
        print("\nFALLO: un estudio incluido pierde TODOS sus informes")
        for sid, recs in lost:
            print("  %s" % sid)
            for x in recs:
                print("      %s -- %s" % (x["pmid"], x["stage1_reason"]))
        sys.exit("no usar esta salida")
    print("VALIDACION SUPERADA: ningun estudio incluido pierde todos sus informes.")
    present = [r for r in rows if r["pmid"] and r["pmid"] in known]

    L = ["# Etapa 1 — cribado por regla, todas las fuentes", "",
         "Generado por `scripts/screen_stage1_all_sources.py` sobre el corpus",
         "unificado de %d informes deduplicados." % n, "",
         "## Aplicabilidad y efecto de cada regla", "",
         "Una regla que no puede leer su campo devuelve NO APLICABLE y el registro",
         "avanza. Un campo ausente no es un hallazgo negativo.", "",
         "| Regla | Registros que puede juzgar | Excluye |", "|---|---|---|"]
    for rule in RULES:
        k = rule.__name__
        L.append("| `%s` | %d (%.1f%%) | %d |"
                 % (k, applicable[k], 100.0 * applicable[k] / n, excluded[k]))
    L += ["| **Total excluidos** | | **%d** |" % n_ex,
          "| **Pasan a etapa 2** | | **%d** |" % (n - n_ex), "",
          "## Nota sobre la cobertura de las reglas", "",
          "`rule_animal_not_human_scoped` depende de MeSH, que solo aporta PubMed:",
          "puede juzgar el %.1f%% del corpus. Los registros de Scopus, SciELO y los"
          % (100.0 * applicable["rule_animal_not_human_scoped"] / n),
          "registros de ensayos no llevan indexación de especie, así que su",
          "condición humana o preclínica se decide en la etapa 2, leyendo.", "",
          "`rule_non_data_doctype` combina los tipos de publicación de PubMed con",
          "el vocabulario *Document Type* de Scopus. **Conference Paper no se",
          "excluye**: los resúmenes de congreso son justamente donde aparecen",
          "primero los casos de uso compasivo, y excluirlos por regla contradiría",
          "el argumento de esta revisión sobre el sesgo de publicación.", "",
          "## Control positivo", "",
          "%d de los %d estudios ya incluidos están presentes en el corpus y"
          % (len(present), len(known)),
          "**ninguna regla excluye a ninguno**. La comprobación sale con error si",
          "eso deja de cumplirse.", ""]
    REPORT.parent.mkdir(parents=True, exist_ok=True)
    REPORT.write_text("\n".join(L), encoding="utf-8", newline="\n")
    print("wrote", REPORT)

    if args.apply:
        cols = list(rows[0])
        with open(OUT, "w", encoding="utf-8", newline="") as fh:
            w = csv.DictWriter(fh, fieldnames=cols)
            w.writeheader()
            w.writerows(rows)
        print("wrote", OUT)


if __name__ == "__main__":
    main()
