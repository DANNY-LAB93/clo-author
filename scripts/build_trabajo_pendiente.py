# -*- coding: utf-8 -*-
"""Los articulos que hay que ABRIR para desbloquear el encargo del 2026-09-23.

POR QUE EXISTE

Tres de los veinte puntos de la correccion integral no se pueden cumplir sin
leer articulos, y el encargo prohibe inventar los datos. Este guion escribe,
estudio por estudio, cual hay que abrir y que hay que sacar de el, para que el
trabajo se pueda repartir y comprobar en vez de estimarse a ojo.

  · punto 2  -- clase de resistencia verificable contra el antibiograma
  · punto 7  -- reextraccion de los comparativos: comparador, tiempo cero,
                tiempo de evaluacion, cointervenciones y perdidas
  · punto 15 -- los pares de solapamiento que siguen sin leer

Ninguna de las tres listas se teclea: salen de los mismos ficheros que el
manuscrito.

Salidas:
    quality_reports/pendiente_lectura_resistencia.csv
    quality_reports/pendiente_lectura_comparativos.csv
    quality_reports/pendiente_lectura_solapamiento.csv
    quality_reports/pendiente_lectura.xlsx        (las tres, una hoja cada una)

Uso:
    python scripts/build_trabajo_pendiente.py
"""
import collections
import csv
import pathlib
import sys

from openpyxl import Workbook
from openpyxl.styles import Alignment, Font, PatternFill
from openpyxl.utils import get_column_letter

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

ROOT = pathlib.Path(__file__).resolve().parent.parent
RS = ROOT / "revision_sistematica"
QR = ROOT / "quality_reports"
PDF = RS / "textos_completos" / "pdf"

COMPARATIVOS = {"RCT", "non-randomised trial", "prospective cohort",
                "retrospective cohort"}


def leer(p, enc="utf-8"):
    with open(p, encoding=enc, newline="") as fh:
        return list(csv.DictReader(fh))


def contexto():
    fuera = {r["study_id"] for r in
             leer(RS / "cribado" / "exclusiones_tras_texto_completo.csv")}
    grupos = {"EST-%03d" % int(r["estudio"]): r
              for r in leer(RS / "cribado" / "study_groups.csv")
              if r["informe_para_extraer"] == "SI"}
    pdfs = {p.stem for p in PDF.iterdir()}
    adj = leer(RS / "extraccion" / "extraccion_adjudicada.csv", "utf-8-sig")
    por_est = collections.defaultdict(list)
    for r in adj:
        por_est[r["study_id"]].append(r)
    return fuera, grupos, pdfs, por_est


def titulo(grupos, est):
    g = grupos.get(est, {})
    for k in ("titulo", "title", "titulo_del_informe"):
        if g.get(k):
            return " ".join(str(g[k]).split())
    return "(sin título en study_groups)"


def resistencia(fuera, grupos, pdfs, por_est):
    """Los estudios leidos, con la clase que tienen hoy y de donde sale."""
    filas = []
    for est in sorted(grupos):
        if est in fuera or est not in pdfs:
            continue
        if grupos[est]["situacion"] not in ("extraible", "solo-resumen"):
            continue
        br = por_est.get(est, [])
        clases = sorted({(r["resistance_class"] or "(vacío)") for r in br})
        fuentes = sorted({(r["resistance_class_source"] or "(vacío)") for r in br})
        # Lo que hay que verificar es distinto segun lo que haya hoy.
        if "not-classifiable" in clases:
            tarea = ("Leer el antibiograma y decidir si permite MDR, XDR, PDR o "
                     "DTR; si no, dejarlo en «declarada no verificable»")
        elif "below-MDR-threshold" in clases:
            tarea = ("Confirmar sobre el antibiograma que el paciente está por "
                     "debajo del umbral, y si el estudio es de un solo brazo")
        else:
            tarea = ("Confirmar la clase contra el antibiograma: hoy es lo que "
                     "declara el autor, no lo que se ha verificado")
        filas.append({
            "study_id": est,
            "pdf": "revision_sistematica/textos_completos/pdf/%s.pdf" % est,
            "brazos": len(br),
            "clase_hoy": " / ".join(clases),
            "fuente_de_la_clase_hoy": " / ".join(fuentes),
            "que_hay_que_sacar_del_articulo": tarea,
            "clase_verificada": "",
            "criterio_o_antibiograma_en_que_te_apoyas": "",
            "firmado_por": "",
            "fecha": "",
            "titulo": titulo(grupos, est),
        })
    return filas


def comparativos(fuera, grupos, pdfs, por_est):
    """Los comparativos adjudicados, con los campos que NO existen hoy."""
    grupo = {}
    g = RS / "riesgo_sesgo" / "grupo_de_comparacion_real.csv"
    if g.exists():
        grupo = {r["study_id"]: r for r in leer(g)}
    ests = sorted({e for e, br in por_est.items()
                   if e not in fuera
                   and any(r["study_design"] in COMPARATIVOS for r in br)})
    filas = []
    for est in ests:
        br = por_est[est]
        tiene = grupo.get(est, {}).get("tiene_grupo_de_comparacion", "")
        filas.append({
            "study_id": est,
            "pdf": ("revision_sistematica/textos_completos/pdf/%s.pdf" % est
                    if est in pdfs else "NO SE OBTUVO EL TEXTO COMPLETO"),
            "brazos_extraidos_hoy": len(br),
            "disenos": " / ".join(sorted({r["study_design"] for r in br})),
            "grupo_de_comparacion_firmado": tiene or "(sin juicio: no hay texto)",
            # Los cinco campos que el formulario no tiene. Van vacios a
            # proposito: rellenarlos es el trabajo.
            "brazo_control_identificado": "",
            "tipo_y_unidad_de_asignacion": "",
            "tiempo_cero": "",
            "tiempo_de_evaluacion_del_desenlace": "",
            "cointervenciones_y_antibiotico_concomitante": "",
            "perdidas_y_datos_faltantes": "",
            "estimando_reportado": "",
            "hay_contraste_extraible": "",
            "firmado_por": "",
            "fecha": "",
            "titulo": titulo(grupos, est),
        })
    return filas


def solapamiento(grupos, pdfs):
    """Los pares que el detector marco y que nadie ha leido todavia."""
    p = QR / "pendiente2_solapamiento.csv"
    if not p.exists():
        return []
    filas = []
    for r in leer(p, "utf-8-sig"):
        if "SIN LEER" not in (r.get("veredicto") or ""):
            continue
        a, b = r.get("estudio_1", ""), r.get("estudio_2", "")
        filas.append({
            "estudio_1": a,
            "estudio_2": b,
            "pdf_1": ("revision_sistematica/textos_completos/pdf/%s.pdf" % a
                      if a in pdfs else "sin texto"),
            "pdf_2": ("revision_sistematica/textos_completos/pdf/%s.pdf" % b
                      if b in pdfs else "sin texto"),
            "senal_que_lo_marco": r.get("senal_que_lo_marco", ""),
            "evidencia": " ".join((r.get("evidencia") or "").split())[:300],
            "que_hay_que_comprobar": ("Si los pacientes son los mismos: edad, "
                                      "sexo, sitio de infección, producto, "
                                      "centro y fechas"),
            "veredicto_tras_leer": "",
            "pacientes_duplicados": "",
            "frase_en_que_te_apoyas": "",
            "firmado_por": "",
            "fecha": "",
            "titulo_1": titulo(grupos, a),
            "titulo_2": titulo(grupos, b),
        })
    return filas


def escribe_csv(ruta, filas):
    with open(ruta, "w", encoding="utf-8-sig", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(filas[0].keys()))
        w.writeheader()
        w.writerows(filas)


def escribe_xlsx(ruta, hojas):
    wb = Workbook()
    wb.remove(wb.active)
    cab = Font(bold=True, color="FFFFFF")
    relleno = PatternFill("solid", fgColor="44546A")
    vacia = PatternFill("solid", fgColor="FFF3CD")
    for nombre, filas in hojas:
        ws = wb.create_sheet(nombre[:31])
        cols = list(filas[0].keys())
        ws.append(cols)
        for c in ws[1]:
            c.font, c.fill = cab, relleno
            c.alignment = Alignment(wrap_text=True, vertical="center")
        for f in filas:
            ws.append([f[c] for c in cols])
        # Las columnas que van vacias se pintan: son las que hay que rellenar.
        for j, c in enumerate(cols, 1):
            ancho = max(len(c), *(len(str(f[c])) for f in filas))
            ws.column_dimensions[get_column_letter(j)].width = min(46, ancho + 2)
            if all(not str(f[c]).strip() for f in filas):
                for i in range(2, len(filas) + 2):
                    ws.cell(row=i, column=j).fill = vacia
        ws.freeze_panes = "A2"
        ws.auto_filter.ref = ws.dimensions
    try:
        wb.save(ruta)
        return ruta
    except PermissionError:
        alt = ruta.with_name(ruta.stem + "_nuevo.xlsx")
        wb.save(alt)
        return alt


def main():
    fuera, grupos, pdfs, por_est = contexto()
    res = resistencia(fuera, grupos, pdfs, por_est)
    com = comparativos(fuera, grupos, pdfs, por_est)
    sol = solapamiento(grupos, pdfs)

    escribe_csv(QR / "pendiente_lectura_resistencia.csv", res)
    escribe_csv(QR / "pendiente_lectura_comparativos.csv", com)
    if sol:
        escribe_csv(QR / "pendiente_lectura_solapamiento.csv", sol)

    hojas = [("2 resistencia", res), ("7 comparativos", com)]
    if sol:
        hojas.append(("15 solapamiento", sol))
    x = escribe_xlsx(QR / "pendiente_lectura.xlsx", hojas)

    print("punto 2  · clase de resistencia   %3d artículos" % len(res))
    nc = sum(1 for r in res if "not-classifiable" in r["clase_hoy"])
    print("             de ellos, %d traen hoy «not-classifiable»" % nc)
    print("punto 7  · comparativos           %3d estudios (%d con texto, %d sin)"
          % (len(com), sum(1 for r in com if r["pdf"].endswith(".pdf")),
             sum(1 for r in com if not r["pdf"].endswith(".pdf"))))
    print("punto 15 · solapamiento           %3d pares" % len(sol))
    print()
    print("escrito %s" % x.name)


if __name__ == "__main__":
    main()
