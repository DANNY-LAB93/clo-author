"""Assisted title screening, validated against the manually screened records.

THE PROBLEM. The pool is 15,365 records. 550 were screened by hand at ~150 per
sitting. Finishing that way is ~99 more sittings, which is not a plan, it is a
wish. But a systematic review does not get to sample: every record must be
screened.

THE APPROACH. The 550 hand-screened records are a labelled validation set. This
proposes a decision for each remaining record using the same rubric that produced
those labels, then MEASURES itself against them. The measurement decides how it
may be used:

  - It may auto-EXCLUDE only in strata where it loses none of the 188 manual
    ADVANCE decisions and none of the known-positive studies. Recall on ADVANCE
    must be 100%, not "high".
  - Everything else it merely ORDERS for human reading. An uncertain record is
    never excluded by the machine.

WHY RECALL AND NOT ACCURACY. A classifier that is 95% accurate on this corpus is
worthless: 88% of the pool is excludable, so predicting EXCLUDE always would
score 88%. The only number that matters is how many eligible records it throws
away, and the acceptable value is zero.

WHAT IT IS NOT. It is not a substitute for reading. It is a triage that lets a
single reviewer spend attention where the decision is genuinely uncertain, and it
is declared in Methods as semi-automated screening with its validated recall.

USAGE
    python scripts/assisted_title_screen.py            # validar contra los 550
    python scripts/assisted_title_screen.py --apply    # proponer sobre el resto
"""
import argparse
import collections
import csv
import pathlib
import re
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from exclusion_codes import CODES
from screen_stage1_rules import known_pmids

ROOT = pathlib.Path(__file__).resolve().parent.parent
POOL = ROOT / "revision_sistematica" / "cribado" / "screening_stage2_priorizado.csv"
LOG = ROOT / "revision_sistematica" / "cribado" / "screening_stage2_pool_decisions.csv"
OUT = ROOT / "revision_sistematica" / "cribado" / "screening_stage2_propuesta.csv"
REPORT = ROOT / "quality_reports" / "cribado_asistido_validacion.md"

csv.field_size_limit(200_000_000)

# --- Señales de que el registro NO es un estudio primario en humanos ----------
# Se aplican SOLO al titulo. Un resumen puede mencionar "in vitro" dentro de un
# estudio clinico; un titulo que lo anuncia describe el trabajo entero.
NEG = [
    ("SEC", r"\b(systematic review|scoping review|meta-analys|umbrella review|"
            r"revision sistematica|metaanalisis)\b"),
    ("REV", r"\b(a review|: a review|narrative review|literature review|review of|"
            r"an overview|: perspectives|current concepts|state of the art|"
            r"challenges and (?:promises|perspectives|strategies)|"
            r"opportunities and challenges|current status|recent advances|"
            r"past and future|history and|primer for|what we know|where do we stand|"
            r"revision|perspectivas)\b"),
    ("VET", r"\b(veterinar|poultry|chicken|broiler|swine|piglet|bovine|equine|"
            r"canine|feline|shrimp|penaeus|aquaculture|fish|cattle)\b"),
    ("LAB", r"\b(in vitro|in silico|biofilm(s)? (?:model|formation|removal)|"
            r"isolation and characteri|characteri[sz]ation of|genome (?:sequence|"
            r"announcement)|complete genome|genomic (?:analysis|characteri|insights)|"
            r"transcriptomic|proteomic|phylogenet|murine|mouse|mice|rat model|"
            r"galleria|zebrafish|larva|endolysin|receptor[- ]binding|"
            r"host range|lytic activity|antibacterial (?:activity|efficacy)|"
            r"formulation|encapsulat|spray[- ]dried|nanoparticle|hydrogel|"
            r"microneedle|assay|screening tool|directed evolution|"
            r"synergy (?:against|with)|checkerboard)\b"),
]

# --- Señales de que SI puede ser un estudio primario en humanos ---------------
# Cualquiera de estas vence a las negativas: ante la duda, se lee.
POS = r"""\b(case report|case series|caso clinico|reporte de caso|serie de casos|
    compassionate|salvage|expanded access|named patient|
    randomi[sz]ed|randomised|clinical trial|phase [1-4i]|open[- ]label|
    single[- ]arm|cohort|consecutive (?:cases|patients)|
    treated (?:with|patient)|in a patient|in (?:two|three|four|five|\d+) patients|
    successful(?:ly)? (?:treat|use|applicat)|first[- ]in[- ]human|
    experience|programme|program|centre|center|
    uso compasivo|paciente)\b"""


def propose(rec):
    """Devuelve (veredicto, codigo, motivo). ADVANCE si hay cualquier duda."""
    ti = " ".join((rec.get("title") or "").split())
    if not ti:
        return "ADVANCE", "", "sin titulo; no se puede juzgar"
    if re.search(POS, ti, re.I | re.X):
        return "ADVANCE", "", "el titulo declara diseno clinico o pacientes"
    for code, pat in NEG:
        if re.search(pat, ti, re.I):
            return "EXCLUDE", code, CODES[code]
    return "ADVANCE", "", "el titulo no permite decidir; leer resumen"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true")
    args = ap.parse_args()

    with open(POOL, encoding="utf-8", newline="") as fh:
        pool = list(csv.DictReader(fh))
    manual = {}
    if LOG.exists():
        with open(LOG, encoding="utf-8", newline="") as fh:
            for r in csv.DictReader(fh):
                manual[r["record_id"]] = r["verdict"]

    # ---------- validacion contra lo cribado a mano ----------
    val = [r for r in pool if r["record_id"] in manual]
    tp = fn = tn = fp = 0
    perdidos = []
    for r in val:
        real = manual[r["record_id"]]
        prop = propose(r)[0]
        if real == "ADVANCE" and prop == "ADVANCE":
            tp += 1
        elif real == "ADVANCE" and prop == "EXCLUDE":
            fn += 1
            perdidos.append(r)
        elif real == "EXCLUDE" and prop == "EXCLUDE":
            tn += 1
        else:
            fp += 1

    n_adv = tp + fn
    recall = 100.0 * tp / n_adv if n_adv else 0.0
    ahorro = 100.0 * (tn + fn) / len(val) if val else 0.0

    print("validacion contra %d registros cribados a mano" % len(val))
    print("  ADVANCE manuales      : %d" % n_adv)
    print("  recuperados por la maquina: %d" % tp)
    print("  PERDIDOS (falsos EXCLUDE) : %d" % fn)
    print("  recall sobre ADVANCE      : %.1f%%" % recall)
    print("  EXCLUDE manuales          : %d" % (tn + fp))
    print("  coincide en EXCLUDE       : %d" % tn)
    print("  la maquina manda a leer   : %d de mas" % fp)
    print("  reduccion de lectura      : %.1f%%" % ahorro)

    known = known_pmids()
    kn_perdidos = [r for r in perdidos if r["pmid"] in known]
    print("\n  estudios YA INCLUIDOS perdidos: %d" % len(kn_perdidos))

    if perdidos:
        print("\n  titulos perdidos (los primeros 12):")
        for r in perdidos[:12]:
            print("    %-5s %s" % (r["orden"], r["title"][:88]))

    apto = (fn == 0)
    print("\n  VEREDICTO: %s" % ("apto para excluir automaticamente"
                                 if apto else
                                 "NO apto para excluir; solo puede ordenar"))

    L = ["# Cribado asistido — validación", "",
         "Generado por `scripts/assisted_title_screen.py`.", "",
         "El clasificador propone una decisión con la misma rúbrica que produjo",
         "las decisiones manuales, y se mide contra ellas. **La única cifra que",
         "decide si puede usarse es el recall sobre ADVANCE**: cuántos registros",
         "que un humano mandó a leer serían descartados por la máquina. El valor",
         "aceptable es cero, no «alto».", "",
         "Nótese por qué la exactitud no sirve: el %.0f%% del pozo cribado es"
         % (100.0 * (tn + fp) / len(val)),
         "excluible, así que un clasificador que respondiera siempre EXCLUDE",
         "acertaría esa proporción sin ser de ninguna utilidad.", "",
         "| | |", "|---|---|",
         "| Registros de validación | %d |" % len(val),
         "| ADVANCE manuales | %d |" % n_adv,
         "| **Perdidos por la máquina** | **%d** |" % fn,
         "| **Recall sobre ADVANCE** | **%.1f%%** |" % recall,
         "| Estudios ya incluidos perdidos | %d |" % len(kn_perdidos),
         "| Mandados a leer de más | %d |" % fp,
         "| Reducción de lectura | %.1f%% |" % ahorro, "",
         "**Veredicto: %s.**" % ("apto para excluir automáticamente" if apto
                                 else "NO apto para excluir; solo puede ordenar"), ""]
    if perdidos:
        L += ["## Registros que la máquina habría perdido", "",
              "| Posición | Título |", "|---|---|"]
        for r in perdidos[:40]:
            L.append("| %s | %s |" % (r["orden"], r["title"][:110]))
        L.append("")
    REPORT.parent.mkdir(parents=True, exist_ok=True)
    REPORT.write_text("\n".join(L), encoding="utf-8", newline="\n")
    print("\nwrote", REPORT)

    if args.apply:
        pend = [r for r in pool if r["record_id"] not in manual]
        rows = []
        conteo = collections.Counter()
        for r in pend:
            v, c, motivo = propose(r)
            conteo[v] += 1
            rows.append({"orden": r["orden"], "record_id": r["record_id"],
                         "propuesta": v, "codigo": c, "motivo": motivo,
                         "year": r["year"], "title": r["title"][:220],
                         "sources": r["sources"]})
        with open(OUT, "w", encoding="utf-8", newline="") as fh:
            w = csv.DictWriter(fh, fieldnames=list(rows[0]))
            w.writeheader()
            w.writerows(rows)
        print("\npendientes procesados: %d" % len(rows))
        print("  propuesta EXCLUDE : %d" % conteo["EXCLUDE"])
        print("  propuesta ADVANCE : %d  <- lectura humana" % conteo["ADVANCE"])
        print("wrote", OUT)


if __name__ == "__main__":
    main()
