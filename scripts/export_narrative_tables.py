"""Build the narrative-synthesis tables (A and B) from the analysis set.

WHY A SCRIPT AND NOT HAND-TYPING. The narrative rewrite drops the pooled
estimates, so the tables become the evidence a reader checks. Typing 40 rows by
hand would put numbers in the manuscript that no script can regenerate, which is
exactly the failure this project already caught once (a spelled-out count that
survived every gate because it was words, not a macro).

THE ANALYSIS SET is dat_analysis.rds, built by scripts/R/02_data_preparation.R:
the cleaned extraction minus (i) Leitner 2021, trial-wide and not
Pseudomonas-specific, (ii) an arm whose published antibiogram falls below the MDR
population criterion, (iii) trial populations recruited with no MDR/XDR/PDR entry
criterion, and (iv) case reports duplicating a patient inside the Pirnay 2024
roster. R is not on PATH here, so the same filter is re-applied to the CSV and
the result is CHECKED against the manuscript scalars (40 arms, 33 studies, 91
patients). If the check fails the script stops rather than emitting a table that
disagrees with the manuscript.

SITE BLOCKS follow the eradication finding: chronic airway colonisation is a
different therapeutic target from an acute infection elsewhere, so the outcome
table is blocked by site rather than pooled across it.

USAGE
    python scripts/export_narrative_tables.py
"""
import csv
import pathlib
import re

ROOT = pathlib.Path(__file__).resolve().parent.parent
SRC = ROOT / "metaanalisis" / "datos" / "phage_therapy_extraction_dataset.csv"
SCALARS = ROOT / "paper" / "generated_scalars.tex"
OUT = ROOT / "paper" / "narrative_tables.md"

csv.field_size_limit(10_000_000)

# The four exclusions applied by 02_data_preparation.R, named explicitly so they
# are auditable here as well as in the R pipeline. The set starts from ALL rows
# of the cleaned extraction -- extraction_status is not a pooling filter.
PIRNAY_ROSTER_DUPLICATES = {"Ferry2022_A", "Racenis2023_LVAD_A", "Jennes2017_A"}
BELOW_MDR_THRESHOLD = {"Liu2025_perinephric_P1", "Chung2026_A", "Ronit2024_A"}
NO_RESISTANCE_CRITERION = {"Jault2019_PhagoBurn_phage", "ArmataAP_PA02_highdose",
                           "Weiner2025_BX004A_phage"}
LEITNER_MARK = "NOT usable in the primary Pseudomonas-specific proportion pooling"
EXCLUDED_IDS = PIRNAY_ROSTER_DUPLICATES | BELOW_MDR_THRESHOLD | NO_RESISTANCE_CRITERION


def scalars():
    t = SCALARS.read_text(encoding="utf-8")
    out = {}
    for m in re.finditer(r"\\newcommand\{\\(\w+)\}\{(.*?)\}\s*$", t, re.M):
        out[m.group(1)] = m.group(2).replace("\\xspace", "").replace("\\%", "%").strip()
    return out


def num(v):
    try:
        return int(float((v or "").strip()))
    except (TypeError, ValueError):
        return None


def pct(k, n):
    if k is None or not n:
        return "no informado"
    return "%d/%d (%.0f%%)" % (k, n, 100.0 * k / n)


def airway(r):
    """Chronic airway colonisation vs. other sites.

    The extraction has no site column, so route plus the success definition is
    the best available proxy: inhaled/nebulised delivery in a cystic-fibrosis or
    bronchiectasis context is chronic airway colonisation. Any arm this rule
    cannot place is reported in its own block rather than forced into one.
    """
    blob = " ".join([r.get("route", ""), r.get("clinical_success_definition", ""),
                     r.get("study_id", "")]).lower()
    if re.search(r"inhal|nebuli", blob) and re.search(
            r"cystic|fibrosis|bronchiect|chronic|coloni", blob):
        return "airway"
    if re.search(r"inhal|nebuli", blob):
        return "airway"
    if not r.get("route", "").strip() or "not reported" in blob:
        return "unspecified"
    return "other"


def main():
    with open(SRC, encoding="utf-8", newline="") as fh:
        rows = list(csv.DictReader(fh))

    keep = [r for r in rows
            if r["study_arm_id"] not in EXCLUDED_IDS
            and LEITNER_MARK not in (r.get("incomplete_reason") or "")]

    s = scalars()
    want = (int(s["ArmsAnalysed"]), int(s["StudiesAnalysed"]), int(s["PatientsAnalysed"]))
    got = (len(keep), len({r["study_id"] for r in keep}),
           sum(num(r["n_arm"]) or 0 for r in keep))
    if got != want:
        raise SystemExit(
            "El filtro no reproduce el conjunto analitico del manuscrito.\n"
            "  esperado (brazos, estudios, pacientes): %s\n"
            "  obtenido                              : %s\n"
            "No se emite tabla: una tabla que no cuadra con los escalares es peor\n"
            "que no tener tabla." % (want, got))

    L = ["<!-- GENERADO por scripts/export_narrative_tables.py. No editar a mano. -->",
         "", "### Tabla A. Características de los estudios incluidos", "",
         "| Estudio | Año | Origen | Diseño | n | Vía | Modalidad | Resistencia (fuente) "
         "| Actividad fágica in vitro | Definición de éxito clínico |",
         "|---|---|---|---|---|---|---|---|---|---|"]

    def short(v, n=42):
        v = " ".join((v or "").split())
        return (v[:n] + "…") if len(v) > n else (v or "no informado")

    for r in sorted(keep, key=lambda x: (x["publication_year"], x["study_id"])):
        src = {"independently-verified": "verificada",
               "author-reported": "etiqueta del autor",
               "not-classifiable": "no informada"}.get(
                   r["resistance_class_source"].strip(), r["resistance_class_source"])
        L.append("| %s | %s | %s | %s | %s | %s | %s | %s (%s) | %s | %s |" % (
            r["study_id"], r["publication_year"], short(r["geographic_source"], 24),
            short(r["study_design"], 22), r["n_arm"], short(r["route"], 26),
            short(r["modality"], 26), r["resistance_class"], src,
            "no documentada", short(r["clinical_success_definition"], 48)))

    blocks = [("other", "(a) Infección aguda en sitios no pulmonares"),
              ("airway", "(b) Colonización o infección crónica de la vía aérea"),
              ("unspecified", "(c) Sitio no especificado")]

    L += ["", "### Tabla B. Desenlaces por brazo (datos crudos, sin agrupar)", ""]
    for key, label in blocks:
        sub = [r for r in keep if airway(r) == key]
        if not sub:
            continue
        L += ["", "**%s** — %d brazos, %d pacientes" % (
            label, len(sub), sum(num(r["n_arm"]) or 0 for r in sub)), "",
            "| Estudio (brazo) | n | Éxito clínico | Erradicación | Mortalidad | Eventos adversos |",
            "|---|---|---|---|---|---|"]
        for r in sorted(sub, key=lambda x: x["study_id"]):
            n = num(r["n_arm"])
            L.append("| %s | %s | %s | %s | %s | %s |" % (
                r["study_arm_id"], n,
                pct(num(r["clinical_success_n"]), n),
                pct(num(r["microbio_eradication_n"]), n),
                pct(num(r["mortality_n"]), n),
                pct(num(r["adverse_event_n"]), n)))

    OUT.write_text("\n".join(L) + "\n", encoding="utf-8", newline="\n")
    print("conjunto analitico verificado contra los escalares: %d brazos, %d estudios, %d pacientes"
          % got)
    for key, label in blocks:
        sub = [r for r in keep if airway(r) == key]
        print("  %-52s %2d brazos, %2d pacientes"
              % (label, len(sub), sum(num(r["n_arm"]) or 0 for r in sub)))
    print("\nwrote", OUT)


if __name__ == "__main__":
    main()
