# -*- coding: utf-8 -*-
"""La Tabla 6, desglosada brazo a brazo.

La Tabla 6 del manuscrito es un embudo: siete filas y cuántos brazos quedan en
cada una. Eso basta para el argumento, pero no permite al lector comprobar
POR QUE cae cada brazo. Este script emite la misma decisión a nivel de brazo,
con cumple / no cumple / no evaluable en cada uno de los siete requisitos y el
motivo concreto de la primera caída.

Las reglas NO se redefinen aquí: son las mismas de `build_outcome_scalars.py`,
importadas o replicadas literalmente, y el script comprueba que los recuentos
que produce coinciden con los del embudo publicado. Si no coinciden, aborta.

SALIDA
    quality_reports/tabla6_brazo_a_brazo.csv
"""
import csv
import json
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
RS = ROOT / "revision_sistematica"
QR = ROOT / "quality_reports"
csv.field_size_limit(200_000_000)
try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

COMPARATIVOS = {"RCT", "non-randomised trial", "retrospective cohort",
                "prospective cohort"}
NO_ATRIBUIBLE = {"EST-146"}   # ver build_outcome_scalars.py
TIEMPO = {"EST-021"}          # PhagoBurn: el desenlace principal es un tiempo

REQUISITOS = ("diseno_comparativo", "numerador_valido", "denominador_valido",
              "definicion_operativa", "atribuible_a_P_aeruginosa",
              "terapeutica_no_profilactica", "proporcion_no_tiempo")


def es_numero(v):
    try:
        float(str(v).strip().replace(",", "."))
        return True
    except (TypeError, ValueError):
        return False


def sin_definicion(v):
    v = (v or "").strip()
    return (not v) or v.upper().startswith("SIN DEFINICION") or v.upper() == "NA"


def main():
    adj = list(csv.DictReader(open(RS / "extraccion" / "extraccion_adjudicada.csv",
                                   encoding="utf-8", newline="")))
    fuera = {r["study_id"] for r in
             csv.DictReader(open(RS / "cribado" / "exclusiones_tras_texto_completo.csv",
                                 encoding="utf-8", newline=""))}
    filas = [r for r in adj if r["study_id"] not in fuera]

    s5 = sorted((ROOT / "verificables revisión sistemática").glob("S5_listado_*_estudios.csv"))
    titulo, con_texto = {}, {}
    if s5:
        for r in csv.DictReader(open(s5[0], encoding="utf-8-sig", newline="")):
            titulo[r["id"]] = r.get("titulo", "")
            con_texto[r["id"]] = r["texto_completo"].strip().lower().startswith(("s", "y"))

    salida = []
    for r in filas:
        e, a = r["study_id"], r["arm_id"]
        d = (r.get("study_design") or "").strip()
        n = r.get("clinical_success_n")
        N = r.get("n_arm")
        v = {}
        v["diseno_comparativo"] = "cumple" if d in COMPARATIVOS else (
            "no evaluable" if not d or d == "NA" else "no cumple")
        v["denominador_valido"] = "cumple" if es_numero(N) else "no cumple"
        if not es_numero(n):
            v["numerador_valido"] = "no cumple"
        elif es_numero(N) and float(n) > float(N):
            v["numerador_valido"] = "no cumple"
        else:
            v["numerador_valido"] = "cumple"
        v["definicion_operativa"] = "no cumple" if sin_definicion(
            r.get("clinical_success_definition")) else "cumple"
        no_separa = "no separa" in (r.get("incomplete_reason") or "").lower()
        v["atribuible_a_P_aeruginosa"] = "no cumple" if (e in NO_ATRIBUIBLE or no_separa) else "cumple"
        prof = re.search(r"\bprevent|\bprophyla|\bprofilax", titulo.get(e, ""), re.I)
        v["terapeutica_no_profilactica"] = "no cumple" if prof else "cumple"
        v["proporcion_no_tiempo"] = "no cumple" if e in TIEMPO else "cumple"

        # el primer requisito que falla, que es el que lo saca del embudo
        cae = next((k for k in REQUISITOS if v[k] != "cumple"), "")
        motivo = {
            "diseno_comparativo": "diseño «%s»: sin grupo de comparación" % (d or "no declarado"),
            "numerador_valido": "éxito clínico n=«%s» sobre N=«%s»" % (n or "", N or ""),
            "denominador_valido": "no consta el tamaño del brazo",
            "definicion_operativa": "el artículo no define qué contaba como éxito",
            "atribuible_a_P_aeruginosa": "el numerador no es una proporción de P. aeruginosa",
            "terapeutica_no_profilactica": "administración profiláctica, no terapéutica",
            "proporcion_no_tiempo": "el desenlace principal es un tiempo, no una proporción",
        }.get(cae, "")
        fila = {"study_id": e, "arm_id": a, "diseno_adjudicado": d,
                "n_exito": n, "N_brazo": N,
                "texto_completo": "sí" if con_texto.get(e) else "no"}
        fila.update(v)
        fila["primer_requisito_que_falla"] = cae
        fila["motivo"] = motivo
        salida.append(fila)

    # --- se contrasta contra el embudo publicado; si no cuadra, no se escribe
    O = json.loads((QR / "outcome_scalars.json").read_text(encoding="utf-8"))
    pub = {p["filtro"]: p["quedan"] for p in O["embudo"]}
    vivos = list(salida)
    acum, nombres = [], ["diseño comparativo", "numerador y denominador coherentes",
                         "definición operativa del éxito",
                         "desenlace atribuible a P. aeruginosa",
                         "administración terapéutica, no profiláctica",
                         "reporta una proporción, no un tiempo"]
    reqs = [("diseno_comparativo",), ("numerador_valido", "denominador_valido"),
            ("definicion_operativa",), ("atribuible_a_P_aeruginosa",),
            ("terapeutica_no_profilactica",), ("proporcion_no_tiempo",)]
    for nombre, grupo in zip(nombres, reqs):
        vivos = [f for f in vivos if all(f[k] == "cumple" for k in grupo)]
        acum.append((nombre, len(vivos)))
    desajuste = [(n_, v_, pub.get(n_)) for n_, v_ in acum if pub.get(n_) != v_]
    if len(salida) != pub.get("brazos extraídos") or desajuste:
        print("NO SE ESCRIBE: el desglose no reproduce el embudo publicado.", file=sys.stderr)
        print("  brazos: %d aquí, %d publicado" % (len(salida), pub.get("brazos extraídos")),
              file=sys.stderr)
        for n_, v_, p_ in desajuste:
            print("  %-45s aquí %s, publicado %s" % (n_, v_, p_), file=sys.stderr)
        raise SystemExit(1)

    ruta = QR / "tabla6_brazo_a_brazo.csv"
    with ruta.open("w", encoding="utf-8-sig", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(salida[0].keys()))
        w.writeheader()
        w.writerows(salida)
    print("%d brazos desglosados; reproduce el embudo publicado" % len(salida))
    for n_, v_ in acum:
        print("   %-45s %3d" % (n_, v_))
    print("escrito %s" % ruta.name)


if __name__ == "__main__":
    main()
