# -*- coding: utf-8 -*-
"""Adenda al cuaderno del 2026-10-01: dos decisiones que solo tienen una firma.

El 2026-10-03, al revisar el cuaderno firmado, D. Valdiviezo respondio en el chat:

  · EST-132: EXCLUIR con ORG. La hoja 1, firmada por los dos, decia MANTENER,
    y la frase que la sostenia es la composicion del coctel empirico: el
    articulo no dice cuantos pacientes tenian P. aeruginosa ni desglosa por
    organismo (lo firmasteis en la hoja 7 del 30-sep).
  · EST-106: MANTENER y declararlo. La hoja 3 lo corrigio a «por debajo del
    umbral» y, como es un caso unico, quedo como EST-053/057/088 sin que nadie
    hubiera firmado su permanencia.

Excluir un estudio es un acto de autoria y lo firman los dos; por eso no se
aplica con una sola respuesta. `ingest_firma_lectura.py` lee esta adenda cuando
lleva las dos firmas, y hasta entonces el manuscrito dice lo que dice el
cuaderno.

SALIDA
    ~/Desktop/FIRMAR_adenda_lectura_2026-10-03.xlsx
"""
import pathlib
import sys

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

CUADERNO = pathlib.Path.home() / "Desktop" / "FIRMAR_adenda_lectura_2026-10-03.xlsx"

FILAS = [
    ("EST-132",
     "MANTENER en el corpus (hoja 1). Por qué: «pseudomonas derivable del brazo». Frase: "
     "«a mixture of bacteriophages against isolates most commonly found in the ICU, such as "
     "Escherichia coli, Pseudomonas aeruginosa,»",
     "EXCLUIR con el código ORG (respuesta de D. Valdiviezo del 3 de octubre)",
     "La frase es la composición del cóctel empírico que se aplicó hasta tener el fago "
     "personalizado (p. 2). El artículo no dice cuántos pacientes tenían P. aeruginosa ni "
     "desglosa por organismo, y el criterio de población exige un subgrupo separable. Si sale: "
     "deja de ser uno de los 4 con grupo de comparación y sus juicios RoB 2 salen de la Tabla 7.",
     ["EXCLUIR con el código ORG", "MANTENER en el corpus"]),
    ("EST-106",
     "Corregir a «below-MDR-threshold» (hoja 3)",
     "MANTENER y declararlo, como EST-001, EST-053, EST-057, EST-088 y EST-094 "
     "(respuesta de D. Valdiviezo del 3 de octubre)",
     "Es un caso único: con la clase corregida, su único paciente no es multirresistente. "
     "Los otros cinco en esa situación se mantienen por decisión firmada.",
     ["MANTENER y declararlo; como los demás", "EXCLUIR"]),
]


def main():
    from openpyxl import Workbook, load_workbook
    from openpyxl.styles import Alignment, Font, PatternFill
    from openpyxl.worksheet.datavalidation import DataValidation

    if CUADERNO.exists():
        wb = load_workbook(CUADERNO)
        if any(c.value not in (None, "") for ws in wb.worksheets for row in ws.iter_rows()
               for c in row if c.fill and str(c.fill.fgColor.rgb).endswith("FCE4D6")):
            raise SystemExit("NO SE ESCRIBE: la adenda ya tiene respuestas.")

    negrita, grande = Font(bold=True), Font(bold=True, size=13)
    blanca, azul = Font(bold=True, color="FFFFFF"), PatternFill("solid", fgColor="44546A")
    ojo = PatternFill("solid", fgColor="FCE4D6")
    arriba = Alignment(vertical="top", wrap_text=True)

    wb = Workbook()
    s = wb.active
    s.title = "Adenda"
    s.cell(row=1, column=1, value="Dos decisiones con una sola firma: hacen falta las dos").font = grande
    cab = ["Estudio", "Lo que firmasteis el 1 de octubre", "Lo que se propone ahora",
           "Por qué y qué cambia", "Vuestra decisión", "Por qué"]
    for j, (c, w) in enumerate(zip(cab, [10, 48, 40, 64, 30, 40]), start=1):
        x = s.cell(row=3, column=j, value=c)
        x.font, x.fill, x.alignment = blanca, azul, arriba
        s.column_dimensions[x.column_letter].width = w
    for i, (e, antes, ahora, porque, ops) in enumerate(FILAS, start=4):
        for j, v in enumerate([e, antes, ahora, porque], start=1):
            s.cell(row=i, column=j, value=v).alignment = arriba
        for j in (5, 6):
            s.cell(row=i, column=j).fill = ojo
            s.cell(row=i, column=j).alignment = arriba
        dv = DataValidation(type="list", allow_blank=True, formula1='"%s"' % ",".join(ops))
        s.add_data_validation(dv)
        dv.add(s.cell(row=i, column=5))
        s.row_dimensions[i].height = 120

    fi = wb.create_sheet("Firma")
    fi.column_dimensions["A"].width = 46
    fi.column_dimensions["B"].width = 54
    fi.cell(row=1, column=1, value="Firma de los dos autores").font = negrita
    fi.cell(row=2, column=1, value="Se firman juntas o no se firma ninguna.")
    for i, k in enumerate(["Revisor 1 (nombre completo)", "Revisor 2 (nombre completo)",
                           "Fecha (AAAA-MM-DD)",
                           "¿Habéis leído los artículos citados en cada hoja?"], start=4):
        fi.cell(row=i, column=1, value=k).font = negrita
        fi.cell(row=i, column=2, value="").fill = ojo
    wb.save(CUADERNO)
    print("adenda: %s (%d decisiones)" % (CUADERNO, len(FILAS)))


if __name__ == "__main__":
    main()
