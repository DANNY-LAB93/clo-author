# -*- coding: utf-8 -*-
"""Ingiere las decisiones firmadas sobre lo que la lectura del 2026-09-30 dejo abierto.

DE DONDE SALE

`make_firma_lectura.py` escribio `FIRMAR_lectura_2026-10-01.xlsx` con cuatro
hojas. Los dos autores lo devolvieron firmado el 2026-10-01 (copia intacta en
`revision_sistematica/lectura_pendiente/FIRMAR_lectura_2026-10-01_firmado.xlsx`).

QUE COMPRUEBA ANTES DE TOCAR NADA

  · las dos firmas, la fecha y la casilla de lectura de los articulos;
  · que cada fila de las hojas 1 a 3 trae una decision del desplegable;
  · que el valor de HOY en la extraccion es el que la hoja corrige.

QUE HACE

  · Hoja 1. EXCLUIR -> una fila en `exclusiones_tras_texto_completo.csv` con el
    codigo ORG, el «por que» de los autores, su frase y las dos firmas. Las
    exclusiones filtran sin borrar filas, como las 47 anteriores.
  · Hoja 2 y hoja 1 MANTENER -> nada cambia en los datos; la decision queda
    en `decisiones_firmadas_2026-10-01.csv`, que los escalares leen para que el
    manuscrito pueda decir «por decision firmada» solo de quien la tiene.
  · Hoja 3 -> las correcciones de clase, procedencia y DTR, por
    `correcciones_tras_texto_completo.csv`, igual que todas.
  · Hoja 4 -> como se hizo la lectura, al mismo fichero de decisiones.

LA ADENDA. Dos respuestas del 2026-10-03 son solo de D. Valdiviezo: excluir
EST-132 (que la hoja 1, con las dos firmas, mantiene) y mantener EST-106, que
paso por debajo del umbral al resolverse en la hoja 3. Excluir requiere las
dos firmas, asi que van a `FIRMAR_adenda_lectura_2026-10-03.xlsx`. Si esa
adenda existe y esta firmada por los dos, este guion la aplica; si no, la
ignora y lo dice.

Uso:
    python scripts/ingest_firma_lectura.py              # informe, no escribe
    python scripts/ingest_firma_lectura.py --escribir
"""
import csv
import datetime
import pathlib
import sys

from openpyxl import load_workbook

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

ROOT = pathlib.Path(__file__).resolve().parent.parent
RS = ROOT / "revision_sistematica"
LP = RS / "lectura_pendiente"
CUADERNO = LP / "FIRMAR_lectura_2026-10-01_firmado.xlsx"
ADENDA = pathlib.Path.home() / "Desktop" / "FIRMAR_adenda_lectura_2026-10-03.xlsx"
EXTR = RS / "extraccion" / "extraccion_adjudicada.csv"
PROC = RS / "extraccion" / "extraccion_adjudicada_procedencia.csv"
CORR = RS / "extraccion" / "correcciones_tras_texto_completo.csv"
EXCL = RS / "cribado" / "exclusiones_tras_texto_completo.csv"
DECIS = LP / "decisiones_firmadas_2026-10-01.csv"

FIRMA_EXCL = "D. Valdiviezo y N. Trelles"
FIRMA_CORR = "DANNY VALDIVIEZO; NATALY TRELLES"
NOMBRES = ("DANNY VALDIVIEZO", "NATALY TRELLES")

# Hoja 3: la opcion del desplegable -> lo que cambia en la extraccion.
# Una opcion que deja el brazo como esta no cambia nada, y se registra igual.
HOJA3 = {
    ("EST-004", "Dejar A en «yes» y B en «no»"): {},
    ("EST-019", "Dejar el brazo en «no»"): {},
    ("EST-042", "Dejar «PDR» y declarar que no se sostiene"): {},
    ("EST-047", "Poner «yes» (manda el aislado 2)"): {("A", "dtr_status"): "yes"},
    ("EST-048", "Corregir a «not-classifiable»"): {("A", "resistance_class"): "not-classifiable"},
    ("EST-058", "Poner «yes» (la «I» cuenta como no sensible; Kadri)"): {("A", "dtr_status"): "yes"},
    ("EST-106", "Corregir a «below-MDR-threshold»"): {("A", "resistance_class"): "below-MDR-threshold"},
    ("EST-124", "Manda el aislado PA02: «XDR» y DTR «yes»"): {
        ("A", "resistance_class"): "XDR",
        ("A", "resistance_class_source"): "independently-verified",
        ("A", "dtr_status"): "yes"},
    ("EST-169", "Dejar «not-classifiable» y declararlo mixto"): {},
}

# Como aparece P. aeruginosa en los que no tienen ningun paciente tratado con
# fagos contra ella. Sale de la lectura firmada del 2026-09-30 y se comprobo
# en el PDF el 2026-10-03: EST-152 la nombra al describir el paciente de Dan
# et al. (su ref. 10, que es EST-049) y EST-170 al describir el de su ref. 18
# (Chan et al., EST-106).
COMO_APARECE = {
    "EST-152": ("cita", "EST-049"),
    "EST-170": ("cita", "EST-106"),
    "EST-132": ("coctel", ""),
    "EST-129": ("no_diana", ""),
    "EST-135": ("no_diana", ""),
    "EST-051": ("no_diana", ""),
    "EST-096": ("no_diana", ""),
    "EST-009": ("ausente", ""),
    "EST-055": ("ausente", ""),
    "EST-181": ("ausente", ""),
    "EST-208": ("ausente", ""),
}


def leer(p, enc="utf-8"):
    with open(p, encoding=enc, newline="") as fh:
        return list(csv.DictReader(fh))


def fecha(v):
    return v.strftime("%Y-%m-%d") if hasattr(v, "strftime") else str(v or "").strip()


def firmas(ws):
    v = {ws.cell(row=i, column=1).value: ws.cell(row=i, column=2).value for i in range(4, 8)}
    r1 = str(v.get("Revisor 1 (nombre completo)") or "").strip().upper()
    r2 = str(v.get("Revisor 2 (nombre completo)") or "").strip().upper()
    f = fecha(v.get("Fecha (AAAA-MM-DD)"))
    leido = str(v.get("¿Habéis leído los artículos citados en cada hoja?") or "").strip().upper()
    return r1, r2, f, leido


def filas(ws, desde=4):
    cab = [ws.cell(row=3, column=j).value for j in range(1, ws.max_column + 1)]
    out = []
    for i in range(desde, ws.max_row + 1):
        d = {cab[j - 1]: ws.cell(row=i, column=j).value for j in range(1, len(cab) + 1)}
        if d.get("Estudio"):
            out.append(d)
    return out


def main():
    escribir = "--escribir" in sys.argv
    fallos = []
    wb = load_workbook(CUADERNO, data_only=True)

    r1, r2, f_firma, leido = firmas(wb["Firma"])
    if {r1, r2} != set(NOMBRES):
        fallos.append("firmas: «%s» y «%s»" % (r1, r2))
    if leido not in ("SI", "SÍ"):
        fallos.append("casilla de lectura: «%s»" % leido)
    try:
        datetime.date.fromisoformat(f_firma)
    except ValueError:
        fallos.append("fecha de firma: «%s»" % f_firma)

    titulos = {r["study_id"]: r["titulo"] for r in
               leer(ROOT / "quality_reports" / "pendiente_lectura_resistencia.csv", "utf-8-sig")}
    adj = {(r["study_id"], r["arm_id"]): r for r in leer(EXTR)}
    proc = {(r["study_id"], r["arm_id"]): r for r in leer(PROC)}
    excl = leer(EXCL)
    ya_fuera = {r["study_id"] for r in excl}
    corr = leer(CORR)
    hechas = {(r["study_id"], r["arm_id"], r["campo"], r["valor_corregido"]) for r in corr}

    decis, nuevas_excl, nuevas_corr = [], [], []

    # ---- hoja 1
    for d in filas(wb["1 Sin P. aeruginosa"]):
        e, dec = d["Estudio"], str(d["Vuestra decisión"] or "").strip()
        if dec not in ("EXCLUIR con el código ORG", "MANTENER en el corpus"):
            fallos.append("hoja 1 %s: decisión «%s»" % (e, dec))
            continue
        como, citado = COMO_APARECE.get(e, ("", ""))
        decis.append(dict(hoja="1 sin P. aeruginosa", study_id=e,
                          decision="excluir (ORG)" if dec.startswith("EXCLUIR") else "mantener",
                          p_aeruginosa_en_el_articulo=como, estudio_citado=citado,
                          por_que=str(d["Por qué"] or ""), frase=str(d["Frase del artículo"] or ""),
                          firmado_por=FIRMA_EXCL, fecha=f_firma))
        if dec.startswith("EXCLUIR") and e not in ya_fuera:
            nuevas_excl.append({
                "study_id": e, "codigo": "ORG",
                "motivo": ("Ningún paciente con P. aeruginosa tratado con fagos. %s. "
                           "Lectura firmada del 2026-09-30: %s"
                           % (str(d["Por qué"] or "").strip().rstrip("."),
                              " ".join(str(d["Lo que firmasteis el 30-sep"] or "").split()))),
                "cita_del_texto": " ".join(str(d["Frase del artículo"] or "").split()),
                "titulo": titulos.get(e, d.get("Título") or ""),
                "decidido_por": FIRMA_EXCL, "fecha": f_firma})

    # ---- hoja 2
    for d in filas(wb["2 Bajo el umbral"]):
        e, dec = d["Estudio"], str(d["Vuestra decisión"] or "").strip()
        if not dec.startswith(("MANTENER", "EXCLUIR")):
            fallos.append("hoja 2 %s: decisión «%s»" % (e, dec))
            continue
        if dec.startswith("EXCLUIR"):
            fallos.append("hoja 2 %s: EXCLUIR no está previsto aquí; revisarlo a mano" % e)
            continue
        decis.append(dict(hoja="2 bajo el umbral", study_id=e, decision="mantener y declarar",
                          p_aeruginosa_en_el_articulo="", estudio_citado="",
                          por_que=str(d["Por qué"] or ""), frase=str(d["Frase del artículo"] or ""),
                          firmado_por=FIRMA_EXCL, fecha=f_firma))

    # ---- hoja 3
    for d in filas(wb["3 Clase y DTR abiertos"]):
        e, dec = d["Estudio"], str(d["Vuestra decisión"] or "").strip()
        if (e, dec) not in HOJA3:
            fallos.append("hoja 3 %s: decisión no prevista «%s»" % (e, dec))
            continue
        cambios = HOJA3[(e, dec)]
        decis.append(dict(hoja="3 clase y DTR", study_id=e,
                          decision=dec + ("" if cambios else " (sin cambio en la extracción)"),
                          p_aeruginosa_en_el_articulo="", estudio_citado="",
                          por_que=str(d["Por qué"] or ""), frase=str(d["Frase del artículo"] or ""),
                          firmado_por=FIRMA_EXCL, fecha=f_firma))
        for (b, campo), nuevo in cambios.items():
            fila = adj.get((e, b))
            if fila is None:
                fallos.append("%s %s no existe en la extracción" % (e, b))
                continue
            if (e, b, campo, nuevo) in hechas or fila[campo] == nuevo:
                continue
            nuevas_corr.append({
                "study_id": e, "arm_id": b, "campo": campo, "valor_anterior": fila[campo],
                "procedencia_anterior": proc.get((e, b), {}).get(campo, ""),
                "valor_corregido": nuevo,
                "cita_literal": " ".join(str(d["Frase del artículo"] or d["Por qué"] or "").split()),
                "motivo": ("Decisión firmada del %s sobre lo que la lectura del 2026-09-30 "
                           "dejaba abierto («%s»): %s"
                           % (f_firma, " ".join(str(d["Lo que queda abierto"] or "").split()), dec)),
                "firmado_por": FIRMA_CORR, "fecha": "%s; %s" % (f_firma, f_firma)})

    # ---- hoja 4
    ws = wb["4 Cómo se hizo"]
    quien = str(ws["B3"].value or "").strip()
    modelo = str(ws["B5"].value or "").strip()
    figuras = str(ws["B7"].value or "").strip()
    if not quien:
        fallos.append("hoja 4: no dice quién leyó")
    decis.append(dict(hoja="4 cómo se hizo", study_id="", decision=quien,
                      p_aeruginosa_en_el_articulo="", estudio_citado="",
                      por_que="modelo de lenguaje: %s | transcripciones de figuras "
                              "comprobadas contra la figura: %s" % (modelo or "(en blanco: ninguno)",
                                                                     figuras),
                      frase="", firmado_por=FIRMA_EXCL, fecha=f_firma))

    # ---- adenda (dos firmas o nada)
    adenda = []
    if ADENDA.exists():
        wa = load_workbook(ADENDA, data_only=True)
        a1, a2, af, _ = firmas(wa["Firma"])
        if {a1, a2} == set(NOMBRES):
            for d in filas(wa["Adenda"]):
                adenda.append((d["Estudio"], str(d["Vuestra decisión"] or "").strip(),
                               " ".join(filter(None, [str(d.get("Por qué y qué cambia") or ""),
                                                      str(d.get("Por qué") or "")])), af))
        else:
            print("adenda: existe pero sin las dos firmas; no se aplica")
    else:
        print("adenda: todavía no existe; EST-132 y EST-106 siguen como dice el cuaderno")
    for e, dec, porque, af in adenda:
        if dec.startswith("EXCLUIR"):
            decis = [x for x in decis if not (x["study_id"] == e and x["hoja"].startswith("1"))]
            como, citado = COMO_APARECE.get(e, ("", ""))
            decis.append(dict(hoja="adenda", study_id=e, decision="excluir (ORG)",
                              p_aeruginosa_en_el_articulo=como, estudio_citado=citado,
                              por_que=porque, frase="", firmado_por=FIRMA_EXCL, fecha=af))
            if e not in ya_fuera:
                cita = next((x["frase"] for x in leer(DECIS, "utf-8-sig")
                             if x["study_id"] == e), "") if DECIS.exists() else ""
                nuevas_excl.append({"study_id": e, "codigo": "ORG",
                                    "motivo": "Sin subgrupo separable de P. aeruginosa. " + porque,
                                    "cita_del_texto": cita, "titulo": titulos.get(e, ""),
                                    "decidido_por": FIRMA_EXCL, "fecha": af})
        elif dec.startswith("MANTENER"):
            decis.append(dict(hoja="adenda", study_id=e, decision="mantener y declarar",
                              p_aeruginosa_en_el_articulo="", estudio_citado="",
                              por_que=porque, frase="", firmado_por=FIRMA_EXCL, fecha=af))

    # ------------------------------------------------------------ informe
    print("CUADERNO FIRMADO EL %s por %s y %s (lectura: %s)" % (f_firma, r1, r2, leido))
    for h in ("1", "2", "3", "4", "adenda"):
        xs = [x for x in decis if x["hoja"].startswith(h)]
        if xs:
            print("  hoja %s:" % h)
            for x in xs:
                print("     %-8s %s" % (x["study_id"], x["decision"][:90]))
    print("exclusiones nuevas: %d  %s" % (len(nuevas_excl), [x["study_id"] for x in nuevas_excl]))
    print("correcciones nuevas: %d" % len(nuevas_corr))
    for n in nuevas_corr:
        print("  %s %s %-24s %s -> %s" % (n["study_id"], n["arm_id"], n["campo"],
                                        n["valor_anterior"], n["valor_corregido"]))
    if fallos:
        print("\nNO SE ESCRIBE NADA (%d problemas):" % len(fallos))
        for f in fallos:
            print("  · " + f)
        sys.exit(1)
    if not escribir:
        print("\n(informe; nada escrito. Con --escribir se aplica.)")
        return

    with open(DECIS, "w", encoding="utf-8-sig", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(decis[0].keys()))
        w.writeheader()
        w.writerows(decis)
    if nuevas_excl:
        with open(EXCL, "a", encoding="utf-8", newline="") as fh:
            w = csv.DictWriter(fh, fieldnames=list(excl[0].keys()))
            w.writerows(nuevas_excl)
    if nuevas_corr:
        with open(CORR, "a", encoding="utf-8", newline="") as fh:
            w = csv.DictWriter(fh, fieldnames=list(corr[0].keys()))
            w.writerows(nuevas_corr)
    print("\nescrito %s; %d exclusiones y %d correcciones añadidas"
          % (DECIS.name, len(nuevas_excl), len(nuevas_corr)))


if __name__ == "__main__":
    main()
