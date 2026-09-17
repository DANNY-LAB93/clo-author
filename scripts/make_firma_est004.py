# -*- coding: utf-8 -*-
"""El cuaderno de los ocho juicios que faltan: EST-004 con ROBINS-I.

POR QUE SOLO ESTE ESTUDIO. El 2026-09-16 D. Valdiviezo firmó la regla nueva de
diseño por estudio: un estudio es comparativo si CUALQUIERA de sus brazos lo
es. Con ella, EST-004 --brazo A serie de casos, brazo B cohorte prospectiva--
entra en la evaluación de riesgo de sesgo, que pasa de 11 a 12 evaluables y de
82 a 90 juicios. Los 82 firmados el 2026-09-09 NO se tocan: este cuaderno trae
solo los 8 nuevos, en fichero aparte, para que ingerirlo no pueda pisarlos.

SALIDA
    ~/Escritorio/FIRMAR_riesgo_de_sesgo_EST-004.xlsx
"""
import csv
import json
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
RS = ROOT / "revision_sistematica"
CUADERNO = pathlib.Path.home() / "Desktop" / "FIRMAR_riesgo_de_sesgo_EST-004.xlsx"
ESTUDIO = "EST-004"
csv.field_size_limit(200_000_000)
try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import rob_instruments as RI


def contexto():
    """Lo que el artículo dice de este estudio, para no tener que buscarlo."""
    d = {"titulo": "", "revista": "", "anio": "", "brazos": []}
    for g in csv.DictReader(open(RS / "cribado" / "study_groups.csv",
                                 encoding="utf-8", newline="")):
        if "EST-%03d" % int(g["estudio"]) == ESTUDIO and g["informe_para_extraer"] == "SI":
            d.update(titulo=g["titulo"], revista=g["revista"], anio=g["anio"])
    for r in csv.DictReader(open(RS / "extraccion" / "extraccion_adjudicada.csv",
                                 encoding="utf-8", newline="")):
        if r["study_id"] == ESTUDIO:
            d["brazos"].append(r)
    return d


def main():
    from openpyxl import Workbook
    from openpyxl.styles import Alignment, Font, PatternFill
    from openpyxl.worksheet.datavalidation import DataValidation

    inst = next(i for i in RI.SIMPLIFICADOS if i["clave"] == "robins")
    ctx = contexto()
    if not ctx["brazos"]:
        raise SystemExit("no encuentro %s en la extracción adjudicada" % ESTUDIO)

    negrita = Font(bold=True)
    cab = PatternFill("solid", fgColor="D9E1F2")
    ojo = PatternFill("solid", fgColor="FCE4D6")
    gris = PatternFill("solid", fgColor="EDEDED")
    arriba = Alignment(vertical="top", wrap_text=True)
    wb = Workbook()

    h = wb.active
    h.title = "Empieza aqui"
    h.column_dimensions["A"].width = 112
    texto = [
        ("Ocho juicios, un solo estudio", True),
        ("", False),
        ("El 16 de septiembre firmaste la regla nueva: un estudio es comparativo si CUALQUIERA de sus brazos", False),
        ("lo es. Antes mandaba el primer brazo, y por eso %s quedaba fuera." % ESTUDIO, False),
        ("", False),
        ("Su brazo A es una serie de casos (7 pacientes) y su brazo B una cohorte prospectiva (2 pacientes).", False),
        ("Con la regla vieja el estudio era «serie de casos» y no se evaluaba; con la nueva es comparativo,", False),
        ("tiene texto completo y hay que evaluarlo con ROBINS-I, igual que las otras ocho cohortes.", False),
        ("", False),
        ("Lo que esto cambia", True),
        ("", False),
        ("  comparativos       14 -> 15", False),
        ("  evaluables         11 -> 12", False),
        ("  juicios de dominio 82 -> 90", False),
        ("", False),
        ("Los 82 que firmasteis el 9 de septiembre NO se tocan. Este cuaderno trae solo los 8 nuevos, en un", False),
        ("fichero aparte, para que ingerirlo no pueda pisar nada de lo anterior.", False),
        ("", False),
        ("Mientras estos 8 falten, el manuscrito lleva un aviso de PENDIENTE en la sección de riesgo de", False),
        ("sesgo y el ítem 18 de PRISMA vuelve a PARCIAL. No se puede enviar así.", False),
        ("", False),
        ("Cómo se rellena", True),
        ("", False),
        ("Una fila por dominio, con el artículo delante. En «juicio» se escoge del desplegable; en «frase en", False),
        ("que os apoyáis» va la cita literal del artículo que sostiene ese juicio, que es lo que permite a un", False),
        ("árbitro discrepar. Sin frase, el juicio no es comprobable.", False),
        ("", False),
        ("Ejemplo:", False),
        ("  D1  Sesgo por confusión", False),
        ("      juicio: Riesgo grave", False),
        ("      frase : «Patients were offered phage therapy at the discretion of the treating team»", False),
        ("      nota  : no hay ajuste por gravedad basal ni por tratamiento antibiótico concomitante", False),
        ("", False),
        ("El juicio global va en la última fila y NO es automático: lo decidís vosotros leyendo los siete", False),
        ("dominios. En ROBINS-I la convención es que el estudio hereda el peor de sus dominios, pero si os", False),
        ("apartáis de ella, decidlo en la nota.", False),
    ]
    for i, (t, b) in enumerate(texto, start=1):
        c = h.cell(row=i, column=1, value=t)
        if b:
            c.font = negrita

    s = wb.create_sheet("ROBINS-I EST-004")
    s.cell(row=1, column=1, value=inst["nombre"]).font = Font(bold=True, size=12)
    s.cell(row=2, column=1, value=inst["cuando"]).font = Font(italic=True, size=9)
    for i, (k, v) in enumerate([
            ("Estudio", ESTUDIO), ("Título", ctx["titulo"]),
            ("Revista", ctx["revista"]), ("Año", ctx["anio"]),
            ("Diseño adjudicado", "cohorte prospectiva (brazo B); el brazo A es serie de casos"),
            ("Brazos", "; ".join("%s: %s, n=%s" % (b["arm_id"], b["study_design"], b["n_arm"])
                                 for b in ctx["brazos"]))], start=4):
        s.cell(row=i, column=1, value=k).font = negrita
        c = s.cell(row=i, column=2, value=v)
        c.fill = gris
        c.alignment = arriba
    s.column_dimensions["A"].width = 16
    s.column_dimensions["B"].width = 46
    s.column_dimensions["C"].width = 26
    s.column_dimensions["D"].width = 60
    s.column_dimensions["E"].width = 46

    fila = 11
    for j, n in enumerate(["Dominio", "Qué evalúa", "Juicio",
                           "Frase del artículo en que os apoyáis", "Nota"], start=1):
        c = s.cell(row=fila, column=j, value=n)
        c.font, c.fill, c.alignment = negrita, cab, arriba
    dv = DataValidation(type="list",
                        formula1='"%s"' % ",".join(RI.JUICIO_ROBINS),
                        allow_blank=True)
    dv.error = "Escoja una de las cinco categorías de ROBINS-I."
    s.add_data_validation(dv)

    for k, it in enumerate(inst["items"]):
        r = fila + 1 + k
        s.cell(row=r, column=1, value=it["codigo"]).font = negrita
        s.cell(row=r, column=2, value=it["texto_es"]).alignment = arriba
        for col in (3, 4, 5):
            s.cell(row=r, column=col).fill = ojo
            s.cell(row=r, column=col).alignment = arriba
        dv.add(s.cell(row=r, column=3))
        s.row_dimensions[r].height = 40
    rg = fila + 1 + len(inst["items"])
    s.cell(row=rg, column=1, value="GLOBAL").font = negrita
    s.cell(row=rg, column=2, value="Juicio global del estudio").alignment = arriba
    for col in (3, 4, 5):
        s.cell(row=rg, column=col).fill = ojo
    dv.add(s.cell(row=rg, column=3))
    s.row_dimensions[rg].height = 40
    s.freeze_panes = "A%d" % (fila + 1)

    fi = wb.create_sheet("Firma")
    fi.column_dimensions["A"].width = 44
    fi.column_dimensions["B"].width = 52
    fi.cell(row=1, column=1, value="Firma de los dos revisores").font = negrita
    fi.cell(row=2, column=1,
            value="La evaluación es por consenso: los dos con el artículo delante y un solo juicio acordado.")
    for i, k in enumerate(["Revisor 1 (nombre completo)",
                           "Revisor 2 (nombre completo)",
                           "Fecha (AAAA-MM-DD)",
                           "¿Leísteis el artículo completo los dos?"], start=4):
        fi.cell(row=i, column=1, value=k).font = negrita
        fi.cell(row=i, column=2, value="").fill = ojo

    wb.save(CUADERNO)
    print("%d dominios + juicio global para %s" % (len(inst["items"]), ESTUDIO))
    print("cuaderno: %s" % CUADERNO)


if __name__ == "__main__":
    main()
