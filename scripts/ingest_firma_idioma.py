# -*- coding: utf-8 -*-
"""Aplica el cuaderno de idioma del 2026-10-06 cuando lleva las dos firmas.

Lee `~/Desktop/FIRMAR_idioma_2026-10-06.xlsx` (lo escribe `make_firma_idioma.py`).
Sin las dos firmas no hace nada y lo dice. Con ellas, cada EXCLUIR anade una
fila a `exclusiones_tras_texto_completo.csv` con el codigo elegido, el motivo,
lo que se comprobo y las dos firmas; cada MANTENER queda registrado en
`revision_sistematica/lectura_pendiente/decisiones_idioma_2026-10-06.csv`.
Es idempotente.

Uso:
    python scripts/ingest_firma_idioma.py              # informe, no escribe
    python scripts/ingest_firma_idioma.py --escribir
"""
import csv
import pathlib
import shutil
import sys

from openpyxl import load_workbook

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from ingest_firma_lectura import son_los_dos, fecha  # noqa: E402

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

ROOT = pathlib.Path(__file__).resolve().parent.parent
RS = ROOT / "revision_sistematica"
CUADERNO = pathlib.Path.home() / "Desktop" / "FIRMAR_idioma_2026-10-06.xlsx"
COPIA = RS / "lectura_pendiente" / "FIRMAR_idioma_2026-10-06_firmado.xlsx"
EXCL = RS / "cribado" / "exclusiones_tras_texto_completo.csv"
DECIS = RS / "lectura_pendiente" / "decisiones_idioma_2026-10-06.csv"
CODIGO = {"EXCLUIR con NOREC (idioma no verificable)": "NOREC",
          "EXCLUIR con IDI (consta que no es inglés ni español)": "IDI"}


def main():
    escribir = "--escribir" in sys.argv
    if not CUADERNO.exists():
        print("no existe %s: nada que aplicar" % CUADERNO.name)
        return
    wb = load_workbook(CUADERNO, data_only=True)
    fi = wb["Firma"]
    r1, r2 = (str(fi.cell(row=i, column=2).value or "").strip() for i in (4, 5))
    f_firma = fecha(fi.cell(row=6, column=2).value)
    if not son_los_dos(r1, r2):
        print("cuaderno de idioma sin las dos firmas («%s», «%s»): no se aplica" % (r1, r2))
        return
    ws = wb["Idioma"]
    cab = [ws.cell(row=3, column=j).value for j in range(1, ws.max_column + 1)]
    filas = []
    for i in range(4, ws.max_row + 1):
        d = {cab[j - 1]: ws.cell(row=i, column=j).value for j in range(1, len(cab) + 1)}
        if d.get("Estudio"):
            filas.append(d)
    excl = list(csv.DictReader(open(EXCL, encoding="utf-8")))
    ya = {r["study_id"] for r in excl}
    nuevas, decis, fallos = [], [], []
    for d in filas:
        e, dec = d["Estudio"], str(d["Vuestra decisión"] or "").strip()
        if not dec:
            fallos.append("%s: sin decisión" % e)
            continue
        decis.append({"study_id": e, "decision": dec, "por_que": str(d["Por qué"] or ""),
                      "que_se_comprobo": d["Qué se comprobó"], "firmado_por": "%s; %s" % (r1, r2),
                      "fecha": f_firma})
        if dec in CODIGO and e not in ya:
            nuevas.append({
                "study_id": e, "codigo": CODIGO[dec],
                "motivo": ("Idioma no verificable sobre el artículo: solo se probó el resumen en "
                           "inglés, en una revista que no publica de forma nativa en inglés. %s %s"
                           % (d["Qué se comprobó"], str(d["Por qué"] or ""))).strip(),
                "cita_del_texto": "(no hay texto completo: el artículo no se ha podido leer)",
                "titulo": d["Título"], "decidido_por": "D. Valdiviezo y N. Trelles",
                "fecha": f_firma})
    print("CUADERNO DE IDIOMA FIRMADO EL %s por %s y %s" % (f_firma, r1, r2))
    for x in decis:
        print("   %s  %s" % (x["study_id"], x["decision"]))
    print("exclusiones nuevas: %d %s" % (len(nuevas), [n["study_id"] for n in nuevas]))
    if fallos:
        print("NO SE ESCRIBE NADA:\n  · " + "\n  · ".join(fallos))
        sys.exit(1)
    if not escribir:
        print("(informe; nada escrito. Con --escribir se aplica.)")
        return
    shutil.copy2(CUADERNO, COPIA)
    with open(DECIS, "w", encoding="utf-8-sig", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(decis[0].keys()))
        w.writeheader()
        w.writerows(decis)
    if nuevas:
        with open(EXCL, "a", encoding="utf-8", newline="") as fh:
            csv.DictWriter(fh, fieldnames=list(excl[0].keys())).writerows(nuevas)
    print("escrito %s; %d exclusiones añadidas" % (DECIS.name, len(nuevas)))


if __name__ == "__main__":
    main()
