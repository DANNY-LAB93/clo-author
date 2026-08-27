"""Convierte el CSV de conflictos en un cuaderno que se pueda usar.

EL PROBLEMA

`extraction_conflicts.csv` tiene 575 filas y columnas como `clinical_success_definition`
y `arm_id`. Es correcto y es ilegible: nadie adjudica 575 desacuerdos leyendo
nombres de variable en inglés y valores como `na`. Un documento que hay que
descifrar antes de usarlo no se usa.

QUE HACE ESTE

El mismo contenido, ordenado para trabajar:

  · una portada que dice qué hay que hacer, en cuatro líneas
  · los desacuerdos agrupados POR ESTUDIO, no por variable, porque quien
    adjudica tiene el artículo delante y resuelve todo lo de ese artículo de una
    vez en vez de saltar de un PDF a otro
  · la pregunta que se le hizo al revisor, literal, junto a las dos respuestas
  · desplegables con las opciones válidas en las variables categóricas, para que
    la resolución no invente un valor que el esquema no admite
  · una columna de prioridad: los campos que deciden si el viraje a desenlaces
    es viable van marcados, para poder resolver solo esos si no hay tiempo

QUE NO HACE

No propone resoluciones. Las tres columnas que importan van vacías: las firman
los dos revisores. Un cuaderno que sugiere la respuesta y luego pide que la
confirmes no produce un consenso, produce un asentimiento.

Uso:
    python scripts/build_adjudication_workbook.py
"""
import csv
import datetime
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from extraction_schema import CAMPO_DE_ETIQUETA, CATEGORICOS, PREGUNTA

ROOT = pathlib.Path(__file__).resolve().parent.parent
EXTR = ROOT / "revision_sistematica" / "extraccion"
CONF = EXTR / "extraction_conflicts.csv"
SALIDA = EXTR / "ADJUDICACION_conflictos.xlsx"

csv.field_size_limit(200_000_000)
try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

# Los campos que deciden si el articulo puede virar a desenlaces. Si no hay
# tiempo para los 575, estos son los que cambian algo.
PRIORITARIOS = {
    "dtr_status", "clinical_success_n", "clinical_success_definition",
    "microbio_eradication_n", "mortality_n", "adverse_event_n",
    "resistance_emergence_n", "n_arm",
}


def etiqueta(campo):
    inv = {v: k for k, v in CAMPO_DE_ETIQUETA.items()}
    return inv.get(campo, campo)


def main():
    if not CONF.exists():
        print("no existe %s" % CONF)
        return 1
    import openpyxl
    from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
    from openpyxl.worksheet.datavalidation import DataValidation

    filas = list(csv.DictReader(open(CONF, encoding="utf-8")))
    col_a = next(c for c in filas[0] if c.startswith("valor_") and "Danny" in c)
    col_b = next(c for c in filas[0] if c.startswith("valor_") and c != col_a)
    nom_a = col_a.replace("valor_", "").replace("_", " ")
    nom_b = col_b.replace("valor_", "").replace("_", " ")

    pend = [r for r in filas if not (r.get("resolucion") or "").strip()]
    # Por estudio, y dentro del estudio los prioritarios primero: quien adjudica
    # abre un PDF y resuelve todo lo de ese articulo antes de pasar al siguiente.
    pend.sort(key=lambda r: (r["study_id"], r["campo"] not in PRIORITARIOS, r["campo"]))

    wb = openpyxl.Workbook()
    AZUL = PatternFill("solid", fgColor="1F4E79")
    GRIS = PatternFill("solid", fgColor="F2F2F2")
    AMAR = PatternFill("solid", fgColor="FFF2CC")
    VERDE = PatternFill("solid", fgColor="E2EFDA")
    borde = Border(*[Side(style="thin", color="BFBFBF")] * 4)

    # ---- portada -----------------------------------------------------------
    p = wb.active
    p.title = "Empieza aquí"
    p.column_dimensions["A"].width = 108
    lineas = [
        ("Resolución de desacuerdos entre las dos extracciones", 16, True, "1F4E79"),
        ("", 11, False, None),
        ("Hay %d desacuerdos por resolver, sobre %d estudios." % (len(pend), len({r["study_id"] for r in pend})), 12, True, None),
        ("Cada fila es una casilla donde %s y %s pusieron cosas distintas." % (nom_a, nom_b), 11, False, None),
        ("", 11, False, None),
        ("QUÉ HAY QUE HACER", 13, True, "1F4E79"),
        ("", 11, False, None),
        ("Abre la hoja «Desacuerdos». Están agrupados por estudio, así que puedes abrir", 11, False, None),
        ("un artículo y resolver todo lo suyo antes de pasar al siguiente.", 11, False, None),
        ("", 11, False, None),
        ("En cada fila rellena las tres columnas amarillas:", 11, False, None),
        ("      Valor acordado  ·  Quién lo resolvió  ·  Fecha", 11, True, None),
        ("", 11, False, None),
        ("No hace falta elegir entre las dos respuestas: si al releer el artículo veis que", 11, False, None),
        ("ninguna era correcta, poned la tercera. Lo que cuenta es lo que dice el texto.", 11, False, None),
        ("", 11, False, None),
        ("SI NO HAY TIEMPO PARA TODO", 13, True, "1F4E79"),
        ("", 11, False, None),
        ("Las filas marcadas «Sí» en la columna Prioritario son las que deciden si el", 11, False, None),
        ("artículo puede llegar a reportar desenlaces. Son %d de %d." % (sum(1 for r in pend if r["campo"] in PRIORITARIOS), len(pend)), 11, False, None),
        ("El resto no cambia ninguna cifra de lo que el manuscrito publica hoy.", 11, False, None),
        ("", 11, False, None),
        ("CUANDO TERMINÉIS", 13, True, "1F4E79"),
        ("", 11, False, None),
        ("Guardad el fichero y avisad. El canal recoge las resoluciones y la cifra del", 11, False, None),
        ("manuscrito se actualiza sola; nadie tiene que editar el texto a mano.", 11, False, None),
        ("", 11, False, None),
        ("Generado el %s desde extraction_conflicts.csv" % datetime.date.today().isoformat(), 9, False, "808080"),
    ]
    for i, (txt, tam, neg, color) in enumerate(lineas, start=1):
        c = p.cell(row=i, column=1, value=txt)
        c.font = Font(size=tam, bold=neg, color=color or "000000")
        c.alignment = Alignment(wrap_text=False, vertical="center")

    # ---- desacuerdos -------------------------------------------------------
    h = wb.create_sheet("Desacuerdos")
    cab = ["Estudio", "Brazo", "Prioritario", "Qué se preguntó",
           "Respuesta de %s" % nom_a, "Respuesta de %s" % nom_b,
           "Valor acordado", "Quién lo resolvió", "Fecha", "campo_interno"]
    h.append(cab)
    for j, c in enumerate(h[1], start=1):
        c.fill, c.font = AZUL, Font(color="FFFFFF", bold=True, size=11)
        c.alignment = Alignment(wrap_text=True, vertical="center")
        c.border = borde
    h.row_dimensions[1].height = 34
    for col, w in zip("ABCDEFGHIJ", (11, 7, 11, 46, 34, 34, 30, 20, 13, 26)):
        h.column_dimensions[col].width = w
    h.freeze_panes = "A2"

    est_previo = None
    for r in pend:
        pri = "Sí" if r["campo"] in PRIORITARIOS else ""
        h.append([r["study_id"], r["arm_id"], pri,
                  PREGUNTA.get(r["campo"], etiqueta(r["campo"])),
                  r[col_a], r[col_b], "", "", "", r["campo"]])
        f = h.max_row
        nuevo = r["study_id"] != est_previo
        est_previo = r["study_id"]
        for j in range(1, 11):
            cel = h.cell(row=f, column=j)
            cel.border = borde
            cel.alignment = Alignment(wrap_text=True, vertical="top")
            if j in (7, 8, 9):
                cel.fill = AMAR
            elif nuevo:
                cel.fill = GRIS
        if pri:
            h.cell(row=f, column=3).fill = VERDE
            h.cell(row=f, column=3).font = Font(bold=True, color="375623")

    # Desplegables: la resolucion de una variable categorica solo puede tomar
    # uno de sus valores. Sin esto, el consenso puede escribir un valor que el
    # esquema no admite y el error no aparece hasta que algo falla aguas abajo.
    cats = dict(CATEGORICOS) if not isinstance(CATEGORICOS, dict) else CATEGORICOS
    porcampo = {}
    for i, r in enumerate(pend, start=2):
        porcampo.setdefault(r["campo"], []).append(i)
    for campo, filas_c in porcampo.items():
        ops = cats.get(campo)
        if not ops:
            continue
        lista = ",".join(list(ops) + ["no derivable"])
        if len(lista) > 250:
            continue
        dv = DataValidation(type="list", formula1='"%s"' % lista, allow_blank=True)
        dv.error = "Ese valor no está en el vocabulario de esta variable."
        h.add_data_validation(dv)
        for f in filas_c:
            dv.add(h.cell(row=f, column=7))

    h.auto_filter.ref = "A1:J%d" % h.max_row
    h.column_dimensions["J"].hidden = True

    wb.save(SALIDA)
    print("escrito %s" % SALIDA)
    print("  %d desacuerdos por resolver, sobre %d estudios"
          % (len(pend), len({r["study_id"] for r in pend})))
    print("  %d marcados prioritarios" % sum(1 for r in pend if r["campo"] in PRIORITARIOS))
    print("  %d variables con desplegable" % len([c for c in porcampo if cats.get(c)]))
    return 0


if __name__ == "__main__":
    sys.exit(main())
