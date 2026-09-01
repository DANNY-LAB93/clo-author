"""Extrae UNA VEZ el texto de cada texto completo y lo deja en caché.

POR QUÉ EXISTE

Comprobar algo contra los artículos --si el paciente tenía de verdad el
patógeno, si la intervención fue fago solo o fago con antibiótico-- exige
abrir los PDF. Abrirlos con pdfplumber cuesta minutos, así que en la práctica
se acaba haciendo un `grep` con una heurística y llamándolo revisión. Esa
heurística ya dio dos falsos positivos (EST-135 y EST-184), y los dio porque
miraba una ventana de caracteres en vez del artículo.

Este script rompe ese compromiso: extrae el texto una vez, lo guarda, y a
partir de ahí cualquier comprobación es instantánea y se puede hacer sobre el
texto entero. La caché NO se versiona --son artículos con derechos-- y se
regenera con este mismo script.

Salida:
    revision_sistematica/textos_completos/texto_cache/EST-nnn.txt
    revision_sistematica/textos_completos/texto_cache/_inventario.csv

Uso:
    python scripts/cache_fulltext.py
"""
import csv
import pathlib
import sys
import warnings

warnings.filterwarnings("ignore")
import pdfplumber  # noqa: E402

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

ROOT = pathlib.Path(__file__).resolve().parent.parent
FT = ROOT / "revision_sistematica" / "textos_completos"
CACHE = FT / "texto_cache"
DATOS = ROOT / "revision_sistematica" / "extraccion" / "extraccion_adjudicada.csv"

# Por debajo de esto no hay artículo que leer: es una portada, un aviso de
# acceso denegado o un PDF de solo imagen. Se marca, no se descarta en silencio.
MINIMO = 1500


def texto_de(p):
    try:
        with pdfplumber.open(p) as doc:
            return "".join((pg.extract_text() or "") for pg in doc.pages)
    except Exception as e:
        return f"__ERROR__ {e}"


def main():
    CACHE.mkdir(exist_ok=True)
    ids = sorted({r["study_id"] for r in csv.DictReader(
        open(DATOS, encoding="utf-8-sig"))})
    inv = []
    for i, s in enumerate(ids, 1):
        pdf = FT / "pdf" / f"{s}.pdf"
        alt = (list((FT / "texto_html").glob(f"{s}*"))
               + list((FT / "resultados_registro").glob(f"{s}*")))
        if pdf.exists():
            t, origen = texto_de(pdf), "pdf"
        elif alt:
            t = alt[0].read_text(encoding="utf-8", errors="replace")
            origen = alt[0].parent.name
        else:
            inv.append({"study_id": s, "origen": "SIN TEXTO COMPLETO",
                        "caracteres": 0, "estado": "no recuperado"})
            continue
        if t.startswith("__ERROR__"):
            estado = "ilegible"
        elif len(t) < MINIMO:
            estado = "demasiado corto"
        else:
            estado = "legible"
        if estado == "legible":
            (CACHE / f"{s}.txt").write_text(t, encoding="utf-8")
        inv.append({"study_id": s, "origen": origen,
                    "caracteres": len(t), "estado": estado})
        print(f"  [{i:3d}/{len(ids)}] {s}  {len(t):7d}  {estado}", flush=True)

    with open(CACHE / "_inventario.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, ["study_id", "origen", "caracteres", "estado"])
        w.writeheader()
        w.writerows(inv)

    from collections import Counter
    c = Counter(x["estado"] for x in inv)
    print(f"\n{len(ids)} estudios en la extracción adjudicada")
    for k, v in c.most_common():
        print(f"  {v:4d}  {k}")
    faltan = [x["study_id"] for x in inv if x["estado"] != "legible"]
    print(f"\nNO revisables contra el texto completo ({len(faltan)}):")
    print("  " + " ".join(faltan))


if __name__ == "__main__":
    main()
