# -*- coding: utf-8 -*-
"""Ingiere el segundo cuaderno: el codigo NOORG y las siete fichas que quedaban.

ENTRADA   ~/Escritorio/FIRMAR_codigo_NOORG_y_duplicado.xlsx
          quality_reports/registros_organismo_verificado.csv      (la frase literal)
          revision_sistematica/textos_completos/registros/*.json  (la ficha entera)
SALIDA    revision_sistematica/cribado/exclusiones_tras_texto_completo.csv
          quality_reports/organismo_pendiente.json                (queda vacio)

LO QUE SE NIEGA A HACER

  1. Sin los dos nombres y la fecha, nada.
  2. Sin un «SI» en la hoja «El codigo nuevo», nada: el codigo es una enmienda
     al protocolo y sin esa aceptacion firmada no existe.
  3. Si NOORG no esta declarado en `exclusion_codes.py`, nada.

DE DONDE SALE EL MOTIVO DE CADA UNO. No de un comentario tecleado, que las dos
veces vino en blanco, sino de lo que se midio sobre la ficha entera:

  - Si la ficha NO nombra a Pseudomonas en ningun campo, el motivo lo dice asi
    y el script lo vuelve a comprobar sobre el JSON antes de escribirlo.
  - Si SI la nombra --pasa en dos-- el motivo dice donde aparece y por que no
    sirve: es el espectro litico declarado del producto, no la bacteria del
    paciente. La frase se extrae del JSON, no se redacta.

Uso:
    python scripts/ingest_noorg.py [--escribir]
"""
import argparse
import csv
import datetime
import json
import pathlib
import re
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from exclusion_codes import CODES

ROOT = pathlib.Path(__file__).resolve().parent.parent
CUADERNO = pathlib.Path.home() / "Desktop" / "FIRMAR_codigo_NOORG_y_duplicado.xlsx"
EVIDENCIA = ROOT / "quality_reports" / "registros_organismo_verificado.csv"
FICHAS = ROOT / "revision_sistematica" / "textos_completos" / "registros"
EXCLUSIONES = ROOT / "revision_sistematica" / "cribado" / "exclusiones_tras_texto_completo.csv"
PENDIENTE = ROOT / "quality_reports" / "organismo_pendiente.json"

CODIGO = "NOORG"
PSEUDO = re.compile(r"pseudomonas|aeruginosa", re.I)

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass


def hoja_pares(wb, nombre):
    """{etiqueta de la columna A: valor de la columna B}."""
    out = {}
    for fila in wb[nombre].iter_rows(values_only=True):
        if fila and fila[0] and len(fila) > 1 and fila[1] not in (None, ""):
            out[str(fila[0]).strip()] = fila[1]
    return out


def texto_fecha(v):
    if isinstance(v, datetime.datetime):
        return v.date().isoformat()
    if isinstance(v, datetime.date):
        return v.isoformat()
    return str(v).strip()


def recorre(nodo, ruta, salida):
    if isinstance(nodo, dict):
        for k, v in nodo.items():
            recorre(v, k, salida)
    elif isinstance(nodo, list):
        for v in nodo:
            recorre(v, ruta, salida)
    elif isinstance(nodo, str):
        salida.append((ruta, nodo))
    return salida


def frase(texto, clave, margen=180):
    i = texto.lower().find(clave.lower())
    ini, fin = max(0, i - margen), min(len(texto), i + len(clave) + margen)
    return (("..." if ini else "") + re.sub(r"\s+", " ", texto[ini:fin]).strip()
            + ("..." if fin < len(texto) else ""))


def evidencia_de_ausencia(est, ev):
    """El motivo y la cita, medidos sobre la ficha entera que esta en disco."""
    ident = ev["identificador"]
    nombre = ("CTIS_%s.json" % ident) if ev["registro"] == "CTIS" else ("%s.json" % ident)
    ruta = FICHAS / nombre
    if not ruta.exists():
        raise SystemExit("falta la ficha en disco: %s" % ruta)
    ficha = json.loads(ruta.read_text(encoding="utf-8"))
    campos = recorre(ficha, "", [])
    menciones = [(c, t) for c, t in campos if PSEUDO.search(t)]

    base = ("%s. Ficha completa de %s %s, bajada el 2026-09-14 y guardada en "
            "revision_sistematica/textos_completos/registros/. El estudio entro "
            "al corpus como ficha de registro sin resumen ni MeSH, de modo que "
            "el cribado no tuvo con que descartarlo."
            % (CODES[CODIGO], ev["registro"], ident))

    if not menciones:
        motivo = (base + " Comprobado sobre la ficha entera: «Pseudomonas» y "
                  "«aeruginosa» no aparecen en NINGUN campo del registro.")
        cita = "[%s] %s" % (ev["campo_de_la_ficha"], ev["frase_literal_de_la_ficha"])
    else:
        campo, texto = menciones[0]
        motivo = (base + " La ficha SI nombra a P. aeruginosa, pero en el campo "
                  "«%s» y dentro del espectro litico declarado del preparado de "
                  "fagos, no como la bacteria de los pacientes: los criterios de "
                  "elegibilidad no exigen ningun organismo." % campo)
        cita = ("[%s, donde se nombra] %s || [%s, los criterios] %s"
                % (campo, frase(texto, "aeruginosa" if "aeruginosa" in texto.lower()
                                else "pseudomonas"),
                   ev["campo_de_la_ficha"], ev["frase_literal_de_la_ficha"]))
    return motivo, cita


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--escribir", action="store_true")
    args = ap.parse_args()

    if CODIGO not in CODES:
        raise SystemExit("%s no esta declarado en exclusion_codes.py. Un codigo "
                         "sin declaracion no se aplica." % CODIGO)

    from openpyxl import load_workbook
    if not CUADERNO.exists():
        raise SystemExit("no encuentro %s" % CUADERNO)
    wb = load_workbook(CUADERNO, data_only=True)

    f = hoja_pares(wb, "Firma")
    r1 = str(f.get("Revisor 1 (nombre completo)", "")).strip()
    r2 = str(f.get("Revisor 2 (nombre completo)", "")).strip()
    fecha = texto_fecha(f.get("Fecha (AAAA-MM-DD)", ""))
    if not (r1 and r2 and fecha):
        raise SystemExit("el cuaderno no esta firmado por los dos, con fecha.")
    quien = "%s y %s" % (r1, r2)

    c = hoja_pares(wb, "El codigo nuevo")
    acepta = str(c.get("Se acepta el codigo? (SI / NO)", "")).strip().upper()
    if acepta != "SI":
        raise SystemExit("la enmienda del codigo %s no esta aceptada (dice «%s»). "
                         "Sin ella no se aplica ninguna de las siete."
                         % (CODIGO, acepta or "nada"))

    with EVIDENCIA.open(encoding="utf-8-sig", newline="") as fh:
        ev = {r["study_id"]: r for r in csv.DictReader(fh)}

    s = wb["Las siete"]
    cab = [x.value for x in s[1]]
    col = {n: i for i, n in enumerate(cab)}
    excluir, se_quedan, sin_decidir = [], [], []
    for fila in s.iter_rows(min_row=2, values_only=True):
        est = fila[col["study_id"]]
        if not est:
            continue
        d = (fila[col["decision_firmada"]] or "").strip()
        if not d:
            sin_decidir.append(est)
        elif d.upper().startswith("EXCLUIR"):
            excluir.append(est)
        else:
            se_quedan.append(est)

    print("cuaderno firmado por %s el %s" % (quien, fecha))
    print("  codigo %s: ACEPTADO como enmienda al protocolo" % CODIGO)
    print("  a excluir      : %d  (%s)" % (len(excluir), ", ".join(excluir)))
    print("  se quedan      : %d  %s" % (len(se_quedan), ", ".join(se_quedan)))
    print("  sin decidir    : %d  %s" % (len(sin_decidir), ", ".join(sin_decidir)))

    ya = []
    if EXCLUSIONES.exists():
        with EXCLUSIONES.open(encoding="utf-8", newline="") as fh:
            ya = list(csv.DictReader(fh))
    presentes = {r["study_id"] for r in ya}

    nuevas = []
    for est in excluir:
        if est in presentes:
            continue
        e = ev[est]
        motivo, cita = evidencia_de_ausencia(est, e)
        nuevas.append({"study_id": est, "codigo": CODIGO, "motivo": motivo,
                       "cita_del_texto": cita, "titulo": e["titulo_en_el_corpus"],
                       "decidido_por": quien, "fecha": fecha})
    print("\n  se anaden      : %d" % len(nuevas))
    for x in nuevas:
        print("    %s  %s  %s" % (x["study_id"], x["codigo"], x["titulo"][:58]))

    if not args.escribir:
        print("\n(ensayo: no se ha escrito nada; anade --escribir)")
        return

    if nuevas:
        cabecera = list(ya[0].keys()) if ya else list(nuevas[0].keys())
        with EXCLUSIONES.open("w", encoding="utf-8", newline="") as fh:
            w = csv.DictWriter(fh, fieldnames=cabecera)
            w.writeheader()
            w.writerows(ya + nuevas)
        print("\nescrito %s  (%d exclusiones)" % (EXCLUSIONES.name, len(ya) + len(nuevas)))

    PENDIENTE.write_text(json.dumps({
        "fecha_de_la_firma": fecha,
        "firmado_por": quien,
        "sin_decidir": sin_decidir,
        "firmadas_sin_codigo": [],
        "por_que": ("Cerrado: la enmienda del codigo %s se firmo el %s y las "
                    "exclusiones estan aplicadas." % (CODIGO, fecha)),
    }, ensure_ascii=False, indent=1), encoding="utf-8")
    print("Ahora hay que rehacer el canal entero, en el orden de CLAUDE.md.")


if __name__ == "__main__":
    main()
