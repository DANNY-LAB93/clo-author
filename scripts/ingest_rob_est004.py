# -*- coding: utf-8 -*-
"""Ingiere los 8 juicios de EST-004, firmados aparte.

POR QUE UN INGESTOR PROPIO. El cuaderno de consenso de los otros 11 estudios
está firmado desde el 2026-09-09 y no se regenera: su guard lo impide y así
debe ser. EST-004 entró el 2026-09-16, al cambiar la regla de diseño por
estudio, y se firmó en un cuaderno aparte. Este script lo añade sin abrir el
otro, de modo que ingerirlo no puede pisar nada de lo anterior.

LO QUE SE NIEGA A HACER
  1. Sin los dos nombres y la fecha, nada.
  2. Sin los 8 juicios, nada: un estudio a medio evaluar no se ingiere.
  3. Sin la frase del artículo en cada dominio, nada: un juicio sin cita no es
     comprobable, y la cita es lo que permite a un árbitro discrepar.
  4. Si EST-004 ya está en el fichero adjudicado, no lo vuelve a añadir.
  5. Un valor fuera del vocabulario cerrado NO se adivina. La única excepción
     es una permutación exacta de una entrada --«Riesgo bajo» por «Bajo riesgo
     de sesgo»--, que se normaliza y se declara por pantalla; cualquier otra
     cosa aborta.

SALIDA
    revision_sistematica/riesgo_sesgo/riesgo_sesgo_comparativos_adjudicado.csv
    revision_sistematica/riesgo_sesgo/evidencia_por_dominio.csv   (solo-anexar)
"""
import csv
import datetime
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
DEST = ROOT / "revision_sistematica" / "riesgo_sesgo"
ADJ = DEST / "riesgo_sesgo_comparativos_adjudicado.csv"
EVID = DEST / "evidencia_por_dominio.csv"
CUADERNO = pathlib.Path.home() / "Desktop" / "FIRMAR_riesgo_de_sesgo_EST-004.xlsx"
ESTUDIO = "EST-004"
INSTRUMENTO = "robins"
HOJA = "ROBINS-I EST-004"

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from rob_instruments import JUICIO_ROBINS, SIMPLIFICADOS

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass


def normaliza(v):
    """Devuelve (valor_canonico, aviso) o (None, motivo) si no se reconoce."""
    v = " ".join((v or "").split())
    if v in JUICIO_ROBINS:
        return v, None
    # permutacion exacta de las mismas palabras: «Riesgo bajo» -> «Bajo riesgo
    # de sesgo» es la unica que ocurre, y no admite otra lectura.
    clave = sorted(v.lower().replace("de sesgo", "").split())
    for c in JUICIO_ROBINS:
        if sorted(c.lower().replace("de sesgo", "").split()) == clave:
            return c, "«%s» normalizado a «%s»" % (v, c)
    return None, "«%s» no está en el vocabulario de ROBINS-I" % v


def main():
    from openpyxl import load_workbook
    if not CUADERNO.exists():
        raise SystemExit("no encuentro %s" % CUADERNO)
    wb = load_workbook(CUADERNO, data_only=True)

    f = {}
    for fila in wb["Firma"].iter_rows(values_only=True):
        if fila and fila[0] and len(fila) > 1 and fila[1] not in (None, ""):
            f[str(fila[0]).strip()] = fila[1]
    r1 = str(f.get("Revisor 1 (nombre completo)", "")).strip()
    r2 = str(f.get("Revisor 2 (nombre completo)", "")).strip()
    fecha = f.get("Fecha (AAAA-MM-DD)")
    if isinstance(fecha, (datetime.datetime, datetime.date)):
        fecha = (fecha.date() if isinstance(fecha, datetime.datetime) else fecha).isoformat()
    fecha = str(fecha or "").strip()
    if not (r1 and r2 and fecha):
        raise SystemExit("el cuaderno no está firmado por los dos, con fecha.")
    quien = "%s y %s" % (r1, r2)

    inst = next(i for i in SIMPLIFICADOS if i["clave"] == INSTRUMENTO)
    esperados = [it["codigo"] for it in inst["items"]] + ["GLOBAL"]
    dominio_evid = {it["codigo"]: it.get("dominio_evidencia", it["codigo"])
                    for it in inst["items"]}
    titulo_dom = {it["codigo"]: it["texto_es"] for it in inst["items"]}
    titulo_dom["GLOBAL"] = "Juicio global del estudio"

    s = wb[HOJA]
    leidos, avisos, problemas = {}, [], []
    for fila in s.iter_rows(min_row=12, values_only=True):
        cod = (str(fila[0]).strip() if fila and fila[0] else "")
        if cod not in esperados:
            continue
        valor, frase, nota = (fila[2], fila[3], fila[4])
        v, aviso = normaliza(valor)
        if v is None:
            problemas.append("%s: %s" % (cod, aviso))
            continue
        if aviso:
            avisos.append("%s: %s" % (cod, aviso))
        if not (frase and str(frase).strip()):
            problemas.append("%s: sin frase del artículo" % cod)
            continue
        leidos[cod] = (v, " ".join(str(frase).split()), " ".join(str(nota or "").split()))

    faltan = [c for c in esperados if c not in leidos]
    if faltan:
        problemas.append("sin rellenar: %s" % ", ".join(faltan))
    if problemas:
        print("NO SE INGIERE. Problemas:", file=sys.stderr)
        for p in problemas:
            print("  " + p, file=sys.stderr)
        raise SystemExit(1)

    ya = list(csv.DictReader(open(ADJ, encoding="utf-8-sig", newline="")))
    if any(x["study_id"] == ESTUDIO for x in ya):
        print("%s ya está en %s; no se vuelve a añadir." % (ESTUDIO, ADJ.name))
        return
    cab = list(ya[0].keys())
    nuevas = [{"study_id": ESTUDIO, "instrumento": INSTRUMENTO, "item": c,
               "valor": leidos[c][0], "procedencia": "consenso",
               "firmado_por": quien, "fecha": fecha} for c in esperados]
    with ADJ.open("w", encoding="utf-8-sig", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=cab)
        w.writeheader()
        w.writerows(ya + nuevas)

    # La evidencia es solo-anexar: nunca se reescribe lo que ya está.
    ev = list(csv.DictReader(open(EVID, encoding="utf-8-sig", newline="")))
    cab_ev = list(ev[0].keys())
    ev_nuevas = []
    for c in esperados:
        v, frase, nota = leidos[c]
        fila = {k: "" for k in cab_ev}
        fila.update(study_id=ESTUDIO, dominio=dominio_evid.get(c, c),
                    titulo=titulo_dom.get(c, c), n=1,
                    frase=frase + ((" || Nota: " + nota) if nota else ""))
        ev_nuevas.append({k: fila.get(k, "") for k in cab_ev})
    with EVID.open("w", encoding="utf-8-sig", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=cab_ev)
        w.writeheader()
        w.writerows(ev + ev_nuevas)

    print("%s ingerido: %d juicios firmados por %s el %s"
          % (ESTUDIO, len(nuevas), quien, fecha))
    for a in avisos:
        print("  AVISO  " + a)
    hoy = datetime.date.today().isoformat()
    if fecha > hoy:
        print("  AVISO  la fecha firmada (%s) es posterior a hoy (%s); se "
              "ingiere tal cual, pero conviene confirmarla." % (fecha, hoy))
    print("  %s -> %d filas" % (ADJ.name, len(ya) + len(nuevas)))
    print("  %s -> %d filas" % (EVID.name, len(ev) + len(ev_nuevas)))
    print("Ahora: python scripts/build_rob_table.py y el canal entero.")


if __name__ == "__main__":
    main()
