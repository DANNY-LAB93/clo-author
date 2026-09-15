# -*- coding: utf-8 -*-
"""Ingiere el cuaderno firmado del organismo de las fichas de registro.

ENTRADA   ~/Escritorio/FIRMAR_organismo_de_los_registros.xlsx
          quality_reports/registros_organismo_verificado.csv   (la evidencia)
SALIDA    revision_sistematica/cribado/exclusiones_tras_texto_completo.csv
          (solo-anexar: nunca reescribe una fila que ya esta)

LO QUE SE NIEGA A HACER

  1. Sin los dos nombres y la fecha en la hoja «Firma», no aplica nada.
  2. Solo aplica una exclusion cuyo codigo este en el vocabulario cerrado de
     `exclusion_codes.py`. Una fila firmada NO CUMPLE sin codigo NO se aplica:
     se lista y se para. Un codigo nuevo es una enmienda al protocolo y se
     declara en `exclusion_codes.py` con su fecha y su motivo, no se inventa
     aqui para que cuadre un recuento.
  3. No redacta la cita. La frase que justifica cada exclusion se copia literal
     de `registros_organismo_verificado.csv`, que a su vez la extrajo del JSON
     de la ficha. Si el estudio no tiene frase, no se aplica.

Uso:
    python scripts/ingest_organismo.py [--escribir]

Sin `--escribir` enseña lo que haria y no toca nada.
"""
import argparse
import csv
import datetime
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from exclusion_codes import CODES

ROOT = pathlib.Path(__file__).resolve().parent.parent
CUADERNO = pathlib.Path.home() / "Desktop" / "FIRMAR_organismo_de_los_registros.xlsx"
EVIDENCIA = ROOT / "quality_reports" / "registros_organismo_verificado.csv"
EXCLUSIONES = ROOT / "revision_sistematica" / "cribado" / "exclusiones_tras_texto_completo.csv"

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass


def firma(wb):
    """Los dos nombres y la fecha, o se para."""
    h = wb["Firma"]
    campos = {}
    for fila in h.iter_rows(values_only=True):
        if fila and fila[0] and len(fila) > 1 and fila[1]:
            campos[str(fila[0]).strip()] = fila[1]
    r1 = str(campos.get("Revisor 1 (nombre completo)", "")).strip()
    r2 = str(campos.get("Revisor 2 (nombre completo)", "")).strip()
    f = campos.get("Fecha (AAAA-MM-DD)")
    if isinstance(f, datetime.datetime):
        f = f.date()
    if not (r1 and r2 and f):
        raise SystemExit(
            "El cuaderno no esta firmado: hace falta el nombre completo de los "
            "dos revisores y la fecha en la hoja «Firma». No se aplica nada.")
    return r1, r2, (f.isoformat() if hasattr(f, "isoformat") else str(f).strip())


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--escribir", action="store_true",
                    help="sin esto, no modifica ningun archivo")
    args = ap.parse_args()

    from openpyxl import load_workbook
    if not CUADERNO.exists():
        raise SystemExit("no encuentro el cuaderno firmado en %s" % CUADERNO)
    wb = load_workbook(CUADERNO, data_only=True)
    r1, r2, fecha = firma(wb)
    quien = "%s y %s" % (r1, r2)

    with EVIDENCIA.open(encoding="utf-8-sig", newline="") as fh:
        ev = {r["study_id"]: r for r in csv.DictReader(fh)}

    hoja = wb["Fichas"]
    cab = [c.value for c in hoja[1]]
    col = {n: i for i, n in enumerate(cab)}
    decididas, sin_decidir, sin_codigo, cambiadas = [], [], [], []
    for fila in hoja.iter_rows(min_row=2, values_only=True):
        est = fila[col["study_id"]]
        if not est:
            continue
        propuesto = (fila[col["veredicto_propuesto"]] or "").strip()
        firmado = (fila[col["decision_firmada"]] or "").strip()
        codigo = (fila[col["codigo"]] or "").strip()
        if not firmado:
            sin_decidir.append(est)
            continue
        if firmado != propuesto:
            cambiadas.append((est, propuesto, firmado,
                              (fila[col["comentario"]] or "").strip()))
        if firmado != "NO CUMPLE":
            continue
        if codigo not in CODES:
            sin_codigo.append((est, propuesto, codigo or "(vacio)"))
            continue
        decididas.append((est, codigo))

    print("cuaderno firmado por %s el %s" % (quien, fecha))
    print("  filas con decision      : %d" % (len(decididas) + len(sin_codigo) +
                                              sum(1 for f in hoja.iter_rows(min_row=2, values_only=True)
                                                  if f[col["study_id"]] and (f[col["decision_firmada"]] or "").strip()
                                                  and (f[col["decision_firmada"]] or "").strip() != "NO CUMPLE")))
    print("  exclusiones aplicables  : %d" % len(decididas))
    if cambiadas:
        print("\n  el firmante CAMBIO la propuesta en %d filas:" % len(cambiadas))
        for est, p, f, c in cambiadas:
            print("    %s  %s -> %s   %s" % (est, p, f, c or "(sin comentario)"))
    if sin_decidir:
        print("\n  sin decidir (%d): %s" % (len(sin_decidir), ", ".join(sin_decidir)))
    if sin_codigo:
        print("\n  firmadas NO CUMPLE pero SIN codigo del vocabulario (%d):"
              % len(sin_codigo))
        for est, p, c in sin_codigo:
            print("    %s  propuesta %s, codigo %s" % (est, p, c))
        print("    Estas NO se aplican. El vocabulario de exclusion es cerrado:")
        print("    un codigo nuevo es una enmienda al protocolo y se declara en")
        print("    scripts/exclusion_codes.py con su fecha y su motivo.")

    ya = []
    if EXCLUSIONES.exists():
        with EXCLUSIONES.open(encoding="utf-8", newline="") as fh:
            ya = list(csv.DictReader(fh))
    presentes = {r["study_id"] for r in ya}
    nuevas = []
    for est, codigo in decididas:
        if est in presentes:
            continue
        e = ev.get(est)
        if not e or not e["frase_literal_de_la_ficha"].strip():
            raise SystemExit("%s no tiene frase literal en %s; no se aplica"
                             % (est, EVIDENCIA.name))
        nuevas.append({
            "study_id": est,
            "codigo": codigo,
            "motivo": ("%s. Verificado sobre la ficha completa del registro "
                       "(%s %s), bajada el 2026-09-14 y guardada en "
                       "revision_sistematica/textos_completos/registros/. El "
                       "estudio entro al corpus como ficha de registro sin "
                       "resumen ni MeSH, de modo que el cribado no tuvo con "
                       "que descartarlo."
                       % (CODES[codigo], e["registro"], e["identificador"])),
            "cita_del_texto": "[%s] %s" % (e["campo_de_la_ficha"],
                                           e["frase_literal_de_la_ficha"]),
            "titulo": e["titulo_en_el_corpus"],
            "decidido_por": quien,
            "fecha": fecha,
        })

    print("\n  ya estaban en el fichero : %d" % (len(decididas) - len(nuevas)))
    print("  se anaden                : %d" % len(nuevas))
    for n in nuevas:
        print("    %s  %s  %s" % (n["study_id"], n["codigo"], n["titulo"][:62]))

    # LO QUE QUEDA ABIERTO SE ESCRIBE EN DISCO, no solo en la pantalla. El
    # sobre de la revista lee este fichero para decidir si avisa: una firma
    # que este script no puede aplicar tiene que seguir bloqueando el envio,
    # y si solo se imprimiera aqui desapareceria con el terminal.
    pendiente = {
        "fecha_de_la_firma": fecha,
        "firmado_por": quien,
        "sin_decidir": sin_decidir,
        "firmadas_sin_codigo": [
            {"study_id": e, "veredicto_propuesto": p, "decision_firmada": "NO CUMPLE"}
            for e, p, _ in sin_codigo],
        "por_que": ("Un codigo nuevo es una enmienda al protocolo: se declara en "
                    "scripts/exclusion_codes.py con su fecha y su motivo, y lo "
                    "firman los dos revisores. Hasta entonces estas exclusiones "
                    "no se aplican."),
    }
    if args.escribir:
        import json
        (ROOT / "quality_reports" / "organismo_pendiente.json").write_text(
            json.dumps(pendiente, ensure_ascii=False, indent=1), encoding="utf-8")

    if not args.escribir:
        print("\n(ensayo: no se ha escrito nada; anade --escribir)")
        return
    if not nuevas:
        print("\nnada que anadir")
        return
    cab_ex = list(ya[0].keys()) if ya else list(nuevas[0].keys())
    with EXCLUSIONES.open("w", encoding="utf-8", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=cab_ex)
        w.writeheader()
        w.writerows(ya + nuevas)
    print("\nescrito %s  (%d exclusiones en total)"
          % (EXCLUSIONES, len(ya) + len(nuevas)))
    print("Ahora hay que rehacer el canal entero, en el orden de CLAUDE.md.")


if __name__ == "__main__":
    main()
