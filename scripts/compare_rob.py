"""Compara las dos evaluaciones de riesgo de sesgo: concordancia y conflictos.

QUÉ MIDE. Por cada pregunta de cada instrumento: porcentaje de acuerdo y kappa
de Cohen sobre el valor tal cual lo eligieron del desplegable. No hay que
normalizar nada porque el vocabulario es cerrado: o eligieron la misma opción o
no.

LA KAPPA NO SIEMPRE EXISTE, y aquí va a pasar mucho. Si los dos revisores
respondieron "No" a la misma pregunta en los cuarenta reportes de caso, no hay
variación y la kappa sale 0/0. Se informa "no calculable (sin variación)", no un
cero que parecería desacuerdo total. Con 3 estudios en RoB 2, casi ninguna de
sus 22 preguntas va a tener kappa; eso NO es un defecto de la evaluación, es lo
que ocurre cuando el denominador es tres.

NO PISA LAS FIRMAS. Al volver a ejecutarse recupera las resoluciones ya escritas
por la clave (estudio, instrumento, pregunta) y dice cuántas conservó. El
comparador de la extracción llegó a reescribir el fichero con las columnas de
resolución EN BLANCO, y ejecutar el comando documentado habría borrado 561
firmas. No se quita ese paso.

UNA CELDA VACÍA NO ES UN DESACUERDO. Si uno respondió y el otro no llegó a esa
fila, es cobertura, no discrepancia: se cuenta aparte. Mezclarlo hundiría la
kappa atribuyendo a desacuerdo lo que es trabajo a medias.

USO
    python scripts/compare_rob.py
    python scripts/compare_rob.py --a ruta/uno.xlsx --b ruta/otro.xlsx
"""
import argparse
import collections
import csv
import datetime
import pathlib
import sys

try:
    import openpyxl
except ImportError:
    raise SystemExit("hace falta openpyxl: python -m pip install openpyxl")

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from rob_instruments import INSTRUMENTOS

ROOT = pathlib.Path(__file__).resolve().parent.parent
DEST = ROOT / "revision_sistematica" / "riesgo_sesgo"
CONFLICTOS = DEST / "riesgo_sesgo_conflictos.csv"
INFORME = ROOT / "quality_reports" / "rob_agreement.md"

COLS = ["study_id", "instrumento", "item", "pregunta", "valor_a", "valor_b",
        "resolucion", "resuelto_por", "fecha"]

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass


def kappa(pares):
    """Kappa de Cohen. Devuelve (valor|None, motivo si es None)."""
    n = len(pares)
    if n == 0:
        return None, "sin filas comparables"
    cats = sorted({x for p in pares for x in p})
    if len(cats) < 2:
        return None, "no calculable (sin variación: una sola categoría)"
    po = sum(1 for a, b in pares if a == b) / n
    ca = collections.Counter(a for a, _ in pares)
    cb = collections.Counter(b for _, b in pares)
    pe = sum((ca[c] / n) * (cb[c] / n) for c in cats)
    if abs(1 - pe) < 1e-12:
        return None, "no calculable (acuerdo esperado = 1)"
    return (po - pe) / (1 - pe), None


def etiqueta(k):
    if k is None:
        return "—"
    for lim, txt in ((0.81, "casi perfecta"), (0.61, "sustancial"),
                     (0.41, "moderada"), (0.21, "aceptable"), (0.0, "leve")):
        if k >= lim:
            return txt
    return "pobre"


def lee_libro(p):
    """{(estudio, instrumento, item): valor}. El juicio global va como item 'GLOBAL'."""
    wb = openpyxl.load_workbook(p, data_only=True)
    fuera = {}
    for inst in INSTRUMENTOS:
        hoja = inst["hoja"][:31]
        if hoja not in wb.sheetnames:
            continue
        ws = wb[hoja]
        n_ctx = 5                       # las columnas de contexto del formulario
        codigos = [it["codigo"] for it in inst["items"]] + ["GLOBAL"]
        for fila in ws.iter_rows(min_row=4):
            s = fila[0].value
            if not s:
                continue
            for k, cod in enumerate(codigos):
                j = n_ctx + k
                if j >= len(fila):
                    break
                v = fila[j].value
                fuera[(str(s).strip(), inst["clave"], cod)] = (
                    str(v).strip() if v is not None else "")
    return fuera


def previas():
    """Las resoluciones ya firmadas, para no perderlas al reescribir."""
    if not CONFLICTOS.exists():
        return {}
    with open(CONFLICTOS, encoding="utf-8-sig", newline="") as fh:
        return {(r["study_id"], r["instrumento"], r["item"]): r
                for r in csv.DictReader(fh)
                if (r.get("resolucion") or "").strip()}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--a", default=str(DEST / "riesgo_sesgo_danny_valdiviezo.xlsx"))
    ap.add_argument("--b", default=str(DEST / "riesgo_sesgo_nataly_trelles.xlsx"))
    args = ap.parse_args()

    pa, pb = pathlib.Path(args.a), pathlib.Path(args.b)
    for p in (pa, pb):
        if not p.exists():
            raise SystemExit("no encuentro %s" % p)
    A, B = lee_libro(pa), lee_libro(pb)
    guardadas = previas()

    pregunta = {}
    for inst in INSTRUMENTOS:
        for it in inst["items"]:
            pregunta[(inst["clave"], it["codigo"])] = it["texto_es"]
        pregunta[(inst["clave"], "GLOBAL")] = "JUICIO GLOBAL del estudio"

    por_item = collections.defaultdict(list)
    conflictos, sin_pareja, vacias = [], 0, 0
    for clave in sorted(set(A) | set(B)):
        s, inst, cod = clave
        va, vb = A.get(clave, ""), B.get(clave, "")
        if not va and not vb:
            vacias += 1
            continue
        if not va or not vb:
            sin_pareja += 1
            continue
        por_item[(inst, cod)].append((va, vb))
        if va != vb:
            prev = guardadas.get(clave, {})
            conflictos.append({
                "study_id": s, "instrumento": inst, "item": cod,
                "pregunta": pregunta.get((inst, cod), ""),
                "valor_a": va, "valor_b": vb,
                "resolucion": prev.get("resolucion", ""),
                "resuelto_por": prev.get("resuelto_por", ""),
                "fecha": prev.get("fecha", "")})

    DEST.mkdir(parents=True, exist_ok=True)
    with open(CONFLICTOS, "w", encoding="utf-8-sig", newline="") as fh:
        w = csv.DictWriter(fh, COLS)
        w.writeheader()
        w.writerows(conflictos)

    comparadas = sum(len(v) for v in por_item.values())
    # "Escrita" y "firmada" no son lo mismo, y el ingestor solo se queda con
    # las firmadas. Contarlas juntas aqui haria creer que hay mas consenso del
    # que hay.
    escritas = sum(1 for c in conflictos if c["resolucion"])
    firmadas = sum(1 for c in conflictos if c["resolucion"] and c["resuelto_por"])
    lineas = ["# Concordancia en la evaluación del riesgo de sesgo", "",
              "Generado el %s por `compare_rob.py`." % datetime.date.today().isoformat(),
              "", "| | |", "|---|---:|",
              "| Respuestas comparables (los dos contestaron) | %d |" % comparadas,
              "| Desacuerdos | %d |" % len(conflictos),
              "| Resueltos y firmados | %d |" % firmadas,
              "| Con valor escrito pero SIN firma (no se ingieren) | %d |"
              % (escritas - firmadas),
              "| Sin pareja (solo uno contestó) | %d |" % sin_pareja,
              "| Sin contestar por ninguno | %d |" % vacias, ""]

    if comparadas:
        acuerdo = 100.0 * (comparadas - len(conflictos)) / comparadas
        lineas += ["Acuerdo global: **%.1f %%** sobre %d respuestas.\n" % (acuerdo, comparadas)]

    kk = []
    for inst in INSTRUMENTOS:
        filas = [(cod, por_item[(inst["clave"], cod)])
                 for cod in [it["codigo"] for it in inst["items"]] + ["GLOBAL"]
                 if por_item.get((inst["clave"], cod))]
        if not filas:
            continue
        lineas += ["## %s" % inst["nombre"], "",
                   "| Pregunta | n | Acuerdo | Kappa | |", "|---|---:|---:|---:|---|"]
        for cod, pares in filas:
            k, motivo = kappa(pares)
            ac = 100.0 * sum(1 for a, b in pares if a == b) / len(pares)
            if k is not None:
                kk.append(k)
            lineas.append("| %s | %d | %.0f %% | %s | %s |" % (
                cod, len(pares), ac,
                "%.2f" % k if k is not None else "—",
                etiqueta(k) if k is not None else motivo))
        lineas.append("")

    if kk:
        kk.sort()
        med = kk[len(kk) // 2] if len(kk) % 2 else (kk[len(kk) // 2 - 1] + kk[len(kk) // 2]) / 2
        lineas += ["Kappa mediana sobre las %d preguntas en que es calculable: "
                   "**%.2f** (%s).\n" % (len(kk), med, etiqueta(med))]
    else:
        lineas += ["Ninguna pregunta admite kappa todavía: hace falta variación "
                   "en las respuestas, y con pocos estudios por instrumento no "
                   "siempre la hay.\n"]

    INFORME.write_text("\n".join(lineas), encoding="utf-8")

    print("comparadas %d respuestas · %d desacuerdos (%d firmados, %d escritos "
          "sin firma)" % (comparadas, len(conflictos), firmadas,
                          escritas - firmadas))
    print("sin pareja %d · sin contestar %d" % (sin_pareja, vacias))
    print("escrito %s" % CONFLICTOS.relative_to(ROOT))
    print("escrito %s" % INFORME.relative_to(ROOT))


if __name__ == "__main__":
    main()
