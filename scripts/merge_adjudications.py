"""Vuelca en la hoja de consenso lo que la adjudicación contra el texto propuso.

QUÉ ES UNA ADJUDICACIÓN Y QUÉ NO ES

Un tercer lector abrió el artículo y, para cada conflicto, dijo qué encontró y
dónde. Eso llena tres columnas: `evidencia` (la cita que lo decide),
`resolucion_propuesta` y `razon`.

Lo que NO llena es `resolucion`, `resuelto_por` ni `fecha`. Esas tres son la
resolución de verdad y las firman los dos revisores. La propuesta es material
para que la reunión de consenso dure media hora en vez de tres, no un sustituto
de la reunión: lo que se declara en Métodos es que los desacuerdos se
resolvieron por consenso entre los revisores, y eso tiene que ser cierto.

LA COLUMNA `verificacion`

Cada propuesta pasa por un segundo lector cuyo encargo es tumbarla. Si la
refuta, la propuesta se conserva pero queda marcada, con el motivo. Una
propuesta refutada no se borra: saber que dos lectores no coincidieron sobre lo
que dice el artículo es información sobre el artículo.

Uso:
    python scripts/merge_adjudications.py <adjudicado.json> [--verificado <ver.json>]
"""
import argparse
import csv
import json
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
HOJA = ROOT / "revision_sistematica" / "extraccion" / "hoja_de_consenso.csv"

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

COLUMNAS_NUEVAS = ["evidencia", "localizacion", "resolucion_propuesta", "razon",
                   "confianza", "coincide_con", "verificacion"]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("adjudicado", help="JSON {study_id: [resoluciones]}")
    ap.add_argument("--verificado", help="JSON {study_id: [veredictos]}", default=None)
    args = ap.parse_args()

    adj = json.load(open(args.adjudicado, encoding="utf-8"))
    ver = json.load(open(args.verificado, encoding="utf-8")) if args.verificado else {}

    filas = list(csv.DictReader(open(HOJA, encoding="utf-8")))
    campos = list(filas[0].keys())
    for c in COLUMNAS_NUEVAS:
        if c not in campos:
            campos.insert(campos.index("resolucion"), c)

    indice = {}
    for est, res in adj.items():
        for r in res:
            indice[(est, str(r.get("arm_id", "")).strip(), r.get("campo", ""))] = r
    indice_ver = {}
    for est, vs in ver.items():
        for v in vs:
            indice_ver[(est, str(v.get("arm_id", "")).strip(), v.get("campo", ""))] = v

    puestos = refutadas = sin_resolver = 0
    for f in filas:
        for c in COLUMNAS_NUEVAS:
            f.setdefault(c, "")
        clave = (f["study_id"], f["arm_id"].strip(), f["campo"])
        r = indice.get(clave)
        if not r:
            continue
        puestos += 1
        f["evidencia"] = "" if r.get("evidencia") is None else r["evidencia"]
        f["localizacion"] = r.get("localizacion", "")
        f["resolucion_propuesta"] = r.get("propuesta", "")
        f["razon"] = r.get("razon", "")
        f["confianza"] = r.get("confianza", "")
        f["coincide_con"] = r.get("coincide_con", "")
        if "REQUIERE CONSENSO" in str(r.get("propuesta", "")).upper():
            sin_resolver += 1
        v = indice_ver.get(clave)
        if v is None:
            f["verificacion"] = "sin verificar"
        elif v.get("refutada"):
            refutadas += 1
            f["verificacion"] = f"REFUTADA: {v.get('motivo', '')}"
            if v.get("correccion"):
                f["verificacion"] += f" | alternativa: {v['correccion']}"
        else:
            f["verificacion"] = f"aguanta: {v.get('motivo', '')}"

    with open(HOJA, "w", encoding="utf-8", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=campos)
        w.writeheader()
        w.writerows(filas)

    print(f"filas de la hoja: {len(filas)}")
    print(f"  con propuesta volcada: {puestos}")
    print(f"  el artículo no las resuelve: {sin_resolver}")
    print(f"  refutadas por el verificador: {refutadas}")
    print(f"  sin verificar todavía: {puestos - len(indice_ver)}")
    print(f"\nescrito {HOJA}")


if __name__ == "__main__":
    main()
