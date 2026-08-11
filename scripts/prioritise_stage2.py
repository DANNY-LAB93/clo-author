"""Order the stage-2 pool by how likely a record is to be eligible.

WHAT THIS IS NOT. It is not a filter. Every record that reached stage 2 is still
screened; only the reading order changes. No record is ever dropped by its score,
and the output carries the whole pool. Ordering is a scheduling decision, not an
eligibility decision, and the distinction is what keeps it out of the PRISMA flow
diagram entirely.

WHY ORDER AT ALL. The pool is 15,365 records for one reviewer. Reading the likely
eligible first means the corpus stabilises early: if 200 consecutive records at
the top yield nothing new, that is informative about saturation in a way that
reading in retrieval order never is.

THE SCORE. Weighted term hits, title counting more than abstract, minus terms
that mark laboratory work. Deliberately interpretable: every record carries the
terms that earned its score, so a decision can be traced rather than trusted.

VALIDATION IS THE POINT. A scoring scheme nobody checked is a guess. This ranks
the 40 already-included studies inside the pool and reports where they land. If
they do not concentrate at the top, the scheme is wrong and the report says so
instead of quietly shipping a bad order.

USAGE
    python scripts/prioritise_stage2.py
    python scripts/prioritise_stage2.py --apply
"""
import argparse
import collections
import csv
import pathlib
import re
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from screen_stage1_rules import known_pmids

ROOT = pathlib.Path(__file__).resolve().parent.parent
SRC = ROOT / "revision_sistematica" / "cribado" / "screening_stage1_all.csv"
OUT = ROOT / "revision_sistematica" / "cribado" / "screening_stage2_priorizado.csv"
REPORT = ROOT / "quality_reports" / "priorizacion_etapa2.md"

csv.field_size_limit(200_000_000)

# (peso, patrón, etiqueta). El peso se aplica al título; el resumen cuenta la
# mitad, redondeando hacia abajo.
SIGNALS = [
    (10, r"\bphage therapy\b|\bbacteriophage therapy\b|\bphagotherap\w*|\bfagoterapia\b|\bterapia f[áa]gica\b", "terapia con fagos"),
    (8,  r"\bpseudomonas aeruginosa\b|\bp\.? aeruginosa\b|\bpseudomonal\b", "organismo"),
    (6,  r"\bcase report\b|\bcase series\b|\bcaso cl[íi]nico\b|\breporte de caso\b|\bserie de casos\b", "diseño de caso"),
    (6,  r"\bcompassionate\b|\bsalvage\b|\bexpanded access\b|\bnamed patient\b|\buso compasivo\b", "uso compasivo"),
    (5,  r"\bmultidrug[- ]resistant\b|\bextensively drug[- ]resistant\b|\bpandrug[- ]resistant\b|\bMDR\b|\bXDR\b|\bPDR\b|\bcarbapenem[- ]resistant\b|\bmultirresistente\b", "resistencia"),
    (5,  r"\bpatient\b|\bpatients\b|\bpaciente\b|\bpacientes\b|\btreated with\b|\btratad[oa]s? con\b", "pacientes"),
    (4,  r"\bphage cocktail\b|\bpersonali[sz]ed (?:bacterio)?phage\b|\bmagistral\b|\bphage[- ]antibiotic synergy\b", "producto/práctica"),
    (4,  r"\bOMKO1\b|\bAB-PA01\b|\bAP-PA02\b|\bBFC-?1\b|\bPP1131\b|\bBX004\b|\bTP-10\d\b|\bPASA16\b|\bpyophage\b|\bintestiphage\b|\bPhagoBurn\b|\bPhage4Cure\b|\bEliava\b", "nombre de producto"),
    (3,  r"\bosteomyelitis\b|\bprosthetic joint\b|\bendocarditis\b|\bbacteraemia\b|\bbacteremia\b|\bcystic fibrosis\b|\bventilator[- ]associated\b|\bburn wound\b|\bgraft infection\b", "síndrome clínico"),
]

# Marcadores de trabajo de laboratorio. Restan, nunca excluyen: un ensayo clínico
# puede describir su caracterización in vitro en el mismo resumen.
PENALTIES = [
    (-6, r"\bin vitro\b|\bbiofilm model\b|\bplanktonic\b", "in vitro"),
    (-6, r"\bmurine\b|\bmouse\b|\bmice\b|\brat model\b|\bgalleria\b|\bzebrafish\b|\blarvae\b", "modelo animal"),
    (-5, r"\bgenome (?:sequence|announcement)\b|\bcomplete genome\b|\bisolation and characteri[sz]ation\b|\bcharacteri[sz]ation of (?:a |the )?novel\b", "caracterización de fago"),
    (-4, r"\bwastewater\b|\bsewage\b|\bpoultry\b|\bfood\b|\baquaculture\b|\bsoil\b|\brhizosphere\b|\bplant\b", "ambiental/veterinario"),
]


def score(rec):
    """Devuelve (puntuación, etiquetas que la explican)."""
    ti = (rec.get("title") or "").lower()
    ab = (rec.get("abstract") or "").lower()
    total, tags = 0, []
    for w, pat, label in SIGNALS:
        in_ti = re.search(pat, ti, re.I) is not None
        in_ab = re.search(pat, ab, re.I) is not None
        if in_ti:
            total += w
            tags.append(label)
        elif in_ab:
            total += w // 2
            tags.append(label + "(res)")
    for w, pat, label in PENALTIES:
        if re.search(pat, ti, re.I):
            total += w
            tags.append(label)
        elif re.search(pat, ab, re.I):
            total += w // 2
            tags.append(label + "(res)")
    return total, tags


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true")
    args = ap.parse_args()

    if not SRC.exists():
        sys.exit("falta %s: corre screen_stage1_all_sources.py --apply" % SRC.name)
    with open(SRC, encoding="utf-8", newline="") as fh:
        rows = [r for r in csv.DictReader(fh) if r["stage1"] == "ADVANCE"]
    n = len(rows)
    print("pozo de etapa 2: %d registros\n" % n)

    for r in rows:
        s, tags = score(r)
        r["prioridad"] = s
        r["senales"] = ", ".join(dict.fromkeys(tags))
    rows.sort(key=lambda r: (-r["prioridad"], r["year"], r["title"]))
    for i, r in enumerate(rows, 1):
        r["orden"] = i

    # --- validación: dónde caen los estudios ya incluidos ---
    known = known_pmids()
    pos = [r for r in rows if r["pmid"] and r["pmid"] in known]
    ranks = sorted(r["orden"] for r in pos)
    print("estudios incluidos presentes en el pozo: %d" % len(pos))
    if ranks:
        med = ranks[len(ranks) // 2]
        print("  mejor posicion  : %d" % ranks[0])
        print("  mediana         : %d  (percentil %.1f)" % (med, 100.0 * med / n))
        print("  peor posicion   : %d  (percentil %.1f)" % (ranks[-1], 100.0 * ranks[-1] / n))
        for cut in (500, 1000, 2000, 5000):
            got = sum(1 for x in ranks if x <= cut)
            print("  en los primeros %5d: %2d de %d (%.0f%%)"
                  % (cut, got, len(pos), 100.0 * got / len(pos)))

    dist = collections.Counter()
    for r in rows:
        s = r["prioridad"]
        dist["30+" if s >= 30 else "20-29" if s >= 20 else "10-19" if s >= 10
             else "1-9" if s >= 1 else "<=0"] += 1
    print("\ndistribucion de puntuacion:")
    for k in ("30+", "20-29", "10-19", "1-9", "<=0"):
        print("  %-6s %6d (%4.1f%%)" % (k, dist[k], 100.0 * dist[k] / n))

    L = ["# Priorización del pozo de etapa 2", "",
         "Generado por `scripts/prioritise_stage2.py`.", "",
         "**Esto no filtra nada.** Los %d registros del pozo se criban igual;" % n,
         "solo cambia el orden de lectura. Ningún registro se descarta por su",
         "puntuación, y por eso la priorización no aparece en el diagrama PRISMA.", "",
         "## Validación contra los estudios ya incluidos", "",
         "| | |", "|---|---|",
         "| Estudios incluidos presentes en el pozo | %d |" % len(pos)]
    if ranks:
        L += ["| Mejor posición | %d |" % ranks[0],
              "| Mediana | %d (percentil %.1f) |" % (med, 100.0 * med / n),
              "| Peor posición | %d (percentil %.1f) |" % (ranks[-1], 100.0 * ranks[-1] / n)]
        L += ["", "| Leídos en los primeros… | Estudios incluidos recuperados |", "|---|---|"]
        for cut in (500, 1000, 2000, 5000):
            got = sum(1 for x in ranks if x <= cut)
            L.append("| %d | %d de %d (%.0f%%) |" % (cut, got, len(pos), 100.0 * got / len(pos)))
    L += ["", "## Distribución de la puntuación", "",
          "| Rango | Registros |", "|---|---|"]
    for k in ("30+", "20-29", "10-19", "1-9", "<=0"):
        L.append("| %s | %d (%.1f%%) |" % (k, dist[k], 100.0 * dist[k] / n))
    L += ["", "## Cómo se puntúa", "",
          "Coincidencias de término, ponderadas; el título vale el doble que el",
          "resumen. Restan los marcadores de trabajo de laboratorio, que **nunca**",
          "excluyen: un estudio clínico puede describir su caracterización in vitro",
          "en el mismo resumen.", "",
          "| Peso | Señal |", "|---|---|"]
    for w, _, label in SIGNALS:
        L.append("| +%d | %s |" % (w, label))
    for w, _, label in PENALTIES:
        L.append("| %d | %s |" % (w, label))
    L += ["", "Cada registro lleva en la columna `senales` los términos que",
          "explican su puntuación, de modo que el orden es auditable registro a",
          "registro y no un número opaco.", ""]
    REPORT.parent.mkdir(parents=True, exist_ok=True)
    REPORT.write_text("\n".join(L), encoding="utf-8", newline="\n")
    print("\nwrote", REPORT)

    if args.apply:
        cols = ["orden", "prioridad", "senales"] + [c for c in rows[0]
                                                    if c not in ("orden", "prioridad", "senales")]
        with open(OUT, "w", encoding="utf-8", newline="") as fh:
            w = csv.DictWriter(fh, fieldnames=cols)
            w.writeheader()
            w.writerows(rows)
        print("wrote", OUT)


if __name__ == "__main__":
    main()
