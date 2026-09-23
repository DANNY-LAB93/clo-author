# -*- coding: utf-8 -*-
"""Concordancia entre los dos revisores en riesgo de sesgo, ANTES del consenso.

POR QUE EXISTE

El manuscrito afirmaba que la evaluacion de riesgo de sesgo «se emitio por
consenso, de modo que no admite medida de concordancia». Era falso: los dos
cuadernos individuales existen, traen 82 juicios cada uno y difieren en 13. La
concordancia si se puede medir, y se mide aqui.

Lo confirmaron los dos autores el 2026-09-23: los 13 desacuerdos se discutieron
uno a uno y N. Trelles acepto el juicio de D. Valdiviezo en los trece. Eso es
un consenso, y el manuscrito lo dice --junto con el dato de que los trece se
resolvieron en la misma direccion, que es informacion que el lector necesita
para calibrar lo que vale ese consenso.

QUE MIDE

  · acuerdo bruto: cuantos juicios coinciden sobre cuantos comparables;
  · kappa de Cohen, sobre las categorias que de verdad aparecen;
  · en que direccion se resolvio cada desacuerdo.

Las dos medidas se dan sobre el corpus VIGENTE. Los cuadernos incluyen ademas
a EST-063, que salio del corpus el 2026-09-22, y sus juicios no cuentan.

Salida:
    quality_reports/concordancia_rob.json
    quality_reports/concordancia_rob.csv   (un desacuerdo por fila)

Uso:
    python scripts/build_concordancia_rob.py
"""
import collections
import csv
import json
import pathlib
import re
import sys
import unicodedata

from openpyxl import load_workbook

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

ROOT = pathlib.Path(__file__).resolve().parent.parent
RS = ROOT / "revision_sistematica" / "riesgo_sesgo"
EXCL = ROOT / "revision_sistematica" / "cribado" / "exclusiones_tras_texto_completo.csv"
QR = ROOT / "quality_reports"

A_XLSX = RS / "riesgo_sesgo_comparativos_danny_valdiviezo.xlsx"
B_XLSX = RS / "riesgo_sesgo_comparativos_nataly_trelles.xlsx"
C_XLSX = RS / "riesgo_sesgo_comparativos_consenso.xlsx"
NOMBRES = {"A": "D. Valdiviezo", "B": "N. Trelles"}

# Las siete categorias literales de los dos instrumentos. Se reconocen por su
# texto porque los cuadernos son formularios con desplegable, no una tabla.
CATEGORIAS = ("bajo riesgo", "algunas preocupaciones", "alto riesgo",
              "riesgo moderado", "riesgo grave", "riesgo critico",
              "sin informacion")


def plano(s):
    s = unicodedata.normalize("NFKD", str(s or "").lower())
    return "".join(c for c in s if not unicodedata.combining(c)).strip()


def juicios(ruta):
    """(estudio, n) -> juicio, en el orden en que el formulario los pide.

    La clave es la POSICION dentro de la fila del estudio, no el nombre del
    dominio: los tres cuadernos salen de la misma plantilla, de modo que la
    posicion n es el mismo dominio en los tres. Comparar por nombre exigiria
    leer los encabezados, que estan fusionados.
    """
    wb = load_workbook(ruta, data_only=True)
    out = {}
    for hoja in wb.sheetnames:
        for fila in wb[hoja].iter_rows(values_only=True):
            if not fila or not fila[0]:
                continue
            est = str(fila[0]).strip()
            if not re.match(r"^EST-\d+$", est):
                continue
            n = 0
            for celda in fila[1:]:
                p = plano(celda)
                if any(c in p for c in CATEGORIAS):
                    n += 1
                    out[(est, n)] = p
    return out


def kappa_de_cohen(claves, A, B):
    n = len(claves)
    if not n:
        return 0.0, 0.0
    po = sum(1 for k in claves if A[k] == B[k]) / n
    cats = {A[k] for k in claves} | {B[k] for k in claves}
    ca = collections.Counter(A[k] for k in claves)
    cb = collections.Counter(B[k] for k in claves)
    pe = sum((ca[c] / n) * (cb[c] / n) for c in cats)
    return po, (po - pe) / (1 - pe) if pe < 1 else float("nan")


def main():
    for f in (A_XLSX, B_XLSX, C_XLSX):
        if not f.exists():
            raise SystemExit("falta %s" % f.name)

    A, B, C = juicios(A_XLSX), juicios(B_XLSX), juicios(C_XLSX)
    fuera = {r["study_id"] for r in csv.DictReader(open(EXCL, encoding="utf-8"))}

    todas = sorted(set(A) & set(B))
    vivas = [k for k in todas if k[0] not in fuera]
    if not vivas:
        raise SystemExit("no hay juicios comparables en el corpus vigente")

    po, kappa = kappa_de_cohen(vivas, A, B)
    desacuerdos = [k for k in vivas if A[k] != B[k]]

    # Hacia donde se resolvio cada uno. Que los trece fueran en la misma
    # direccion es un dato del lector, no un detalle interno.
    hacia = collections.Counter()
    filas = []
    for k in desacuerdos:
        c = C.get(k)
        quien = ("A" if c == A[k] else "B" if c == B[k] else "otro")
        hacia[quien] += 1
        filas.append({
            "study_id": k[0],
            "posicion_en_el_formulario": k[1],
            "juicio_de_D_Valdiviezo": A[k],
            "juicio_de_N_Trelles": B[k],
            "juicio_de_consenso": c or "(no consta)",
            "resuelto_hacia": NOMBRES.get(quien, "un tercer valor"),
        })

    S = {
        "rob_juicios_comparables": len(vivas),
        "rob_acuerdo_bruto": sum(1 for k in vivas if A[k] == B[k]),
        "rob_acuerdo_pct": round(100.0 * po, 1),
        "rob_kappa": "%.2f" % kappa,
        "rob_desacuerdos": len(desacuerdos),
        "rob_resueltos_hacia_r1": hacia["A"],
        "rob_resueltos_hacia_r2": hacia["B"],
        "rob_resueltos_tercer_valor": hacia["otro"],
        "rob_estudios_con_dos_lecturas": len({k[0] for k in vivas}),
        "rob_juicios_en_los_cuadernos": len(todas),
    }
    (QR / "concordancia_rob.json").write_text(
        json.dumps(S, indent=2, ensure_ascii=False), encoding="utf-8")

    with open(QR / "concordancia_rob.csv", "w", encoding="utf-8-sig",
              newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(filas[0].keys()))
        w.writeheader()
        w.writerows(filas)

    print("concordancia sobre el corpus vigente: %d juicios de %d estudios"
          % (S["rob_juicios_comparables"], S["rob_estudios_con_dos_lecturas"]))
    print("  acuerdo bruto   %d/%d = %s %%"
          % (S["rob_acuerdo_bruto"], S["rob_juicios_comparables"],
             S["rob_acuerdo_pct"]))
    print("  kappa de Cohen  %s" % S["rob_kappa"])
    print("  desacuerdos     %d, resueltos %d hacia %s y %d hacia %s"
          % (S["rob_desacuerdos"], S["rob_resueltos_hacia_r1"], NOMBRES["A"],
             S["rob_resueltos_hacia_r2"], NOMBRES["B"]))
    print("escritos concordancia_rob.json y .csv")


if __name__ == "__main__":
    main()
