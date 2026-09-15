"""El cuaderno para firmar los desacuerdos de extracción que siguen abiertos.

QUE PROBLEMA RESUELVE. De los 541 desacuerdos entre las dos extracciones,
todos menos un puñado estan firmados. Los que quedan bloquean lo unico que el
informe editorial pone como reparo para ir a revision por pares, y estan
repartidos por un cuaderno de 574 filas donde no se ven. Aqui salen solos.

POR QUE LOS DESPLEGABLES IMPORTAN. `study_design` NO admite «NA». Su
vocabulario son siete valores en ingles y el esquema no tiene hueco para «no
lo se»; `ingest_adjudications.py` lo dice y RECHAZA cualquier otra cosa en vez
de aproximarla. Ocho de los diez desacuerdos de diseño existen justamente
porque un revisor puso NA. Si se firman escribiendo a mano, el ingestor los
rechaza y hay que repetir la sesion; con el desplegable no puede pasar.

EL FORMATO ES EL DEL CUADERNO GRANDE --diez columnas, en el mismo orden-- para
que `ingest_adjudications.py --cuaderno` lo lea sin traducir nada.

QUE NO HACE. No propone valores. Las casillas de decision salen VACIAS: si el
guion sugiriera el valor mas frecuente o el del revisor mas completo estaria
decidiendo el, y eso es exactamente lo que el conjunto adjudicado se niega a
hacer con estas casillas.

Salida:
    revision_sistematica/extraccion/FIRMAR_pendientes.xlsx

Uso:
    python scripts/make_firma_pendientes.py
    # se rellena a mano, entre los dos, y luego:
    python scripts/ingest_adjudications.py --cuaderno revision_sistematica/extraccion/FIRMAR_pendientes.xlsx
"""
import csv
import pathlib
import sys

try:
    import openpyxl
    from openpyxl.comments import Comment
    from openpyxl.styles import Alignment, Font, PatternFill
    from openpyxl.utils import get_column_letter
    from openpyxl.worksheet.datavalidation import DataValidation
except ImportError:
    raise SystemExit("hace falta openpyxl: python -m pip install openpyxl")

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from extraction_schema import CATEGORICOS

ROOT = pathlib.Path(__file__).resolve().parent.parent
CONFLICTOS = ROOT / "revision_sistematica" / "extraccion" / "extraction_conflicts.csv"
SALIDA = ROOT / "revision_sistematica" / "extraccion" / "FIRMAR_pendientes.xlsx"

CAB = PatternFill("solid", fgColor="D9D9D9")
FIJO = PatternFill("solid", fgColor="EDEDED")
DECIDIR = PatternFill("solid", fgColor="FFD966")
FIRMA = PatternFill("solid", fgColor="FFF2CC")
EJEMPLO = PatternFill("solid", fgColor="E2EFDA")

COLUMNAS = ["Estudio", "Brazo", "Prioritario", "Qué se preguntó",
            "Respuesta de Danny Valdiviezo", "Respuesta de Nataly Trelles",
            "Valor acordado", "Quién lo resolvió", "Fecha", "campo_interno"]

# Lo que el ingestor acepta en cada campo, y de donde sale. Para los numericos
# no hay lista cerrada: un recuento, 0, o NA.
NUMERICOS = {"adverse_event_n", "microbio_eradication_n", "clinical_success_n",
             "mortality_n", "resistance_emergence_n", "n_arm", "los_days"}

AYUDA = {
    "study_design": (
        "Lo que el artículo ES, no lo que dice ser. Un «estudio» de un solo "
        "paciente es un case report.\n\n"
        "OJO: este campo NO admite NA. El esquema no tiene hueco para «no lo "
        "sé», y el ingestor rechaza cualquier valor que no esté en la lista. "
        "Si de verdad no se puede decidir, hay que mirar el artículo otra vez: "
        "el diseño siempre es uno de los siete."),
    "extraction_status": (
        "COMPLETE si se sacó todo lo que el artículo daba. PARTIAL si faltó "
        "algo pero lo extraído es utilizable. EXTRACTION_INCOMPLETE si la "
        "extracción se quedó a medias."),
    "adverse_event_n": (
        "Cuántos pacientes tuvieron algún evento adverso.\n\n"
        "  · un número = el artículo lo dice o permite contarlo\n"
        "  · 0 = el artículo dice que no hubo ninguno\n"
        "  · NA = no lo reporta ni permite deducirlo\n\n"
        "Cero notificados se escribe 0, no NA: no significan lo mismo."),
    "microbio_eradication_n": (
        "Pacientes con cultivo de control NEGATIVO para el organismo diana, "
        "del mismo sitio, después de terminar la fagoterapia.\n\n"
        "  · un número = se hizo cultivo y salió negativo en esos\n"
        "  · 0 = se hizo cultivo y siguió positivo en todos\n"
        "  · NA = no se hizo, o no se reporta, cultivo de control\n\n"
        "La regla entera está en quality_reports/decisions/"
        "2026-08-12_erradicacion-regla-corregida.md"),
}

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass


def abiertos():
    with open(CONFLICTOS, encoding="utf-8-sig", newline="") as fh:
        filas = list(csv.DictReader(fh))
    ab = [r for r in filas if not (r.get("resolucion") or "").strip()]
    # Primero los que comparten campo, para poder decidirlos de corrido: diez
    # veces la misma pregunta se contesta mejor seguida que salteada.
    ab.sort(key=lambda r: (r["campo"], r["study_id"]))
    return len(filas), ab


def hoja_portada(wb, ab, total):
    ws = wb.create_sheet("Empieza aquí")
    ws.column_dimensions["A"].width = 26
    ws.column_dimensions["B"].width = 94
    fila = [1]

    def linea(a, b="", negrita=False, relleno=None):
        ws.cell(fila[0], 1, a).font = Font(bold=True, size=11)
        c = ws.cell(fila[0], 2, b)
        c.alignment = Alignment(wrap_text=True, vertical="top")
        if negrita:
            c.font = Font(bold=True)
        if relleno:
            ws.cell(fila[0], 1).fill = relleno
            c.fill = relleno
        ws.row_dimensions[fila[0]].height = max(15, 13 * (1 + len(b) // 90))
        fila[0] += 1

    linea("Qué es esto", "Los %d desacuerdos de extracción que siguen sin firmar, de los "
                         "%d que hubo en total. Los demás ya están cerrados por consenso."
          % (len(ab), total), negrita=True)
    linea("", "")
    linea("Cómo se rellena",
          "En la hoja «Desacuerdos», una fila por desacuerdo. Las columnas grises son "
          "contexto y no se tocan. En la columna amarilla «Valor acordado» se elige del "
          "desplegable —o se escribe el número, en los campos que piden recuento—, y se "
          "ponen quién lo resolvió y la fecha.")
    linea("", "Pasa el ratón por encima de la celda «Qué se preguntó»: lleva la regla "
              "completa del campo en un comentario.")
    linea("", "")
    linea("Lo que NO hace este cuaderno",
          "No propone valores. Las casillas de decisión salen vacías a propósito. Si el "
          "guion sugiriera «el valor más frecuente» o «el del revisor que rellenó más», "
          "estaría decidiendo él, que es justo lo que el conjunto adjudicado se niega a "
          "hacer con estas casillas.")
    linea("", "")
    linea("Aviso sobre el diseño",
          "«study_design» NO admite NA. Son siete valores y el esquema no tiene hueco "
          "para «no lo sé»; el ingestor rechaza cualquier otra cosa en vez de "
          "aproximarla. Ocho de los desacuerdos de diseño existen precisamente porque "
          "un revisor puso NA. Por eso hay desplegable: para que no vuelva a pasar.",
          negrita=True)
    linea("", "")

    # --------- EL EJEMPLO, que es lo que se pidio ---------
    linea("EJEMPLO", "Así queda una fila bien rellenada. Esto es una MUESTRA: no se "
                     "ingiere, vive solo en esta hoja.", negrita=True, relleno=EJEMPLO)
    fila[0] += 1
    cab = fila[0]
    for j, c in enumerate(["Columna", "Qué se escribe en el ejemplo"], start=1):
        cel = ws.cell(cab, j, c)
        cel.font, cel.fill = Font(bold=True), CAB
    fila[0] += 1
    for a, b in [
        ("Estudio", "EST-098   (viene puesto, no se toca)"),
        ("Brazo", "A   (viene puesto, no se toca)"),
        ("Qué se preguntó", "Diseño del estudio   (viene puesto)"),
        ("Respuesta de Danny Valdiviezo", "NA   (viene puesta)"),
        ("Respuesta de Nataly Trelles", "serie de casos   (viene puesta)"),
        ("→ Valor acordado", "case series      ← del desplegable, EN INGLÉS"),
        ("→ Quién lo resolvió", "DANNY VALDIVIEZO Y NATALY TRELLES"),
        ("→ Fecha", "2026-09-15"),
    ]:
        ws.cell(fila[0], 1, a).alignment = Alignment(vertical="top")
        c = ws.cell(fila[0], 2, b)
        c.alignment = Alignment(wrap_text=True, vertical="top")
        if a.startswith("→"):
            ws.cell(fila[0], 1).fill = DECIDIR
            c.fill = DECIDIR
            c.font = Font(bold=True)
        else:
            ws.cell(fila[0], 1).fill = FIJO
            c.fill = FIJO
        fila[0] += 1
    fila[0] += 1
    linea("Por qué «case series»",
          "Nataly leyó el artículo y anotó «serie de casos»; Danny dejó la casilla en "
          "NA, que no es una respuesta distinta sino una casilla sin rellenar. Al "
          "sentarse los dos, se comprueba en el artículo cuántos pacientes hay: si son "
          "varios, es case series; si es uno, case report. La firma va con los DOS "
          "nombres porque lo que convierte una respuesta en consenso es que los dos la "
          "hayan mirado.")
    linea("", "")
    linea("Después de firmar",
          "python scripts/ingest_adjudications.py --cuaderno "
          "revision_sistematica/extraccion/FIRMAR_pendientes.xlsx")
    linea("", "El ingestor rechaza toda fila sin firmante, e informa de cualquier valor "
              "que no esté en el vocabulario en vez de aproximarlo al más parecido.")


def hoja_firma(wb):
    ws = wb.create_sheet("Firma")
    ws.column_dimensions["A"].width = 34
    ws.column_dimensions["B"].width = 46
    ws["A1"] = "Firma del consenso"
    ws["A1"].font = Font(bold=True, size=13)
    ws["A3"] = ("Sin los dos nombres y la fecha, «consenso» es una palabra. "
                "El ingestor no acepta una fila sin firmante.")
    ws["A3"].alignment = Alignment(wrap_text=True)
    ws.merge_cells("A3:B3")
    for i, (a, b) in enumerate([("Primer revisor", "DANNY VALDIVIEZO"),
                                ("Segunda revisora", "NATALY TRELLES"),
                                ("Fecha de la sesión", "")], start=5):
        ws.cell(i, 1, a).font = Font(bold=True)
        c = ws.cell(i, 2, b)
        c.fill = FIRMA
    ws.cell(7, 2).comment = Comment("AAAA-MM-DD, el día en que os sentasteis.", "firma")


def main():
    if SALIDA.exists():
        raise SystemExit("ya existe %s. Si quieres uno nuevo, muevelo o borralo "
                         "antes: sobrescribirlo tiraria lo que ya este firmado."
                         % SALIDA.name)
    total, ab = abiertos()
    if not ab:
        print("no queda ningun desacuerdo sin firmar; no hay nada que hacer")
        return 0

    wb = openpyxl.Workbook()
    wb.remove(wb.active)
    hoja_portada(wb, ab, total)

    ws = wb.create_sheet("Desacuerdos")
    for j, c in enumerate(COLUMNAS, start=1):
        cel = ws.cell(1, j, c)
        cel.font, cel.fill = Font(bold=True), CAB
        cel.alignment = Alignment(wrap_text=True, vertical="center")
    for j, w in enumerate([11, 7, 11, 34, 30, 30, 26, 30, 13, 24], start=1):
        ws.column_dimensions[get_column_letter(j)].width = w
    ws.freeze_panes = "A2"

    # Un desplegable por campo categorico, anclado a las filas de ese campo.
    listas = {}
    for i, r in enumerate(ab, start=2):
        campo = r["campo"]
        vals = [r["study_id"], r["arm_id"] or "A", "Sí",
                campo, r["valor_Danny_Valdiviezo"] or "(vacío)",
                r["valor_Nataly_Trelles"] or "(vacío)", None, None, None, campo]
        for j, v in enumerate(vals, start=1):
            cel = ws.cell(i, j, v)
            cel.alignment = Alignment(wrap_text=True, vertical="top")
            cel.fill = DECIDIR if j in (7, 8, 9) else FIJO
        if campo in AYUDA:
            ws.cell(i, 4).comment = Comment(AYUDA[campo][:2000], "consenso")
        ops = CATEGORICOS.get(campo)
        if ops:
            clave = campo
            if clave not in listas:
                dv = DataValidation(type="list", allow_blank=True,
                                    formula1='"%s"' % ",".join(ops),
                                    showErrorMessage=True)
                dv.error = ("Ese valor no está en el vocabulario de %s. El ingestor "
                            "lo rechazaría. Admite: %s" % (campo, ", ".join(ops)))
                ws.add_data_validation(dv)
                listas[clave] = dv
            listas[clave].add(ws.cell(i, 7))
        elif campo in NUMERICOS:
            ws.cell(i, 7).comment = Comment(
                "Un recuento, 0, o NA. Cero notificados es 0, no NA.", "consenso")

    hoja_firma(wb)
    wb.save(SALIDA)
    import collections
    print("escrito %s" % SALIDA.relative_to(ROOT))
    print("  %d desacuerdos sin firmar, de %d" % (len(ab), total))
    for k, v in collections.Counter(r["campo"] for r in ab).most_common():
        ops = CATEGORICOS.get(k)
        print("     %-24s %2d   %s" % (k, v, "desplegable: " + ", ".join(ops) if ops
                                       else "número, 0 o NA"))
    print("  falta la firma de los dos en la hoja «Firma»")
    return 0


if __name__ == "__main__":
    sys.exit(main())
