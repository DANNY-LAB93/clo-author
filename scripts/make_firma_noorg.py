# -*- coding: utf-8 -*-
"""El cuaderno de lo que quedo abierto al firmar el organismo de las fichas.

Son siete filas y una pregunta:

  - SEIS que los dos revisores firmaron NO CUMPLE cambiando la propuesta
    (decia INDETERMINADO) y sin escribir comentario. No se aplicaron: su motivo
    no es «otro organismo» --ninguna ficha nombra bacteria alguna-- sino «no
    consta el organismo», que no esta en el vocabulario cerrado de exclusion.
    Un codigo nuevo es una ENMIENDA AL PROTOCOLO y se firma aparte.
  - UNA sin decidir, EST-087.
  - Y la confirmacion de como se aplica el duplicado EST-186 / EST-187, que
    N. Trelles ya comprobo que son el mismo ensayo.

Entrada : quality_reports/organismo_pendiente.json
          quality_reports/registros_organismo_verificado.csv
Salida  : ~/Escritorio/FIRMAR_codigo_NOORG_y_duplicado.xlsx
"""
import csv
import json
import pathlib

RAIZ = pathlib.Path(__file__).resolve().parents[1]
PENDIENTE = RAIZ / "quality_reports" / "organismo_pendiente.json"
EVIDENCIA = RAIZ / "quality_reports" / "registros_organismo_verificado.csv"
CUADERNO = pathlib.Path.home() / "Desktop" / "FIRMAR_codigo_NOORG_y_duplicado.xlsx"

CODIGO = "NOORG"
GLOSA = ("La ficha de registro no declara ningun organismo: el criterio de "
         "P. aeruginosa no se puede verificar ni a favor ni en contra")


def main():
    from openpyxl import Workbook
    from openpyxl.styles import Alignment, Font, PatternFill
    from openpyxl.worksheet.datavalidation import DataValidation

    d = json.loads(PENDIENTE.read_text(encoding="utf-8"))
    with EVIDENCIA.open(encoding="utf-8-sig", newline="") as fh:
        ev = {r["study_id"]: r for r in csv.DictReader(fh)}

    abiertas = [x["study_id"] for x in d["firmadas_sin_codigo"]] + d["sin_decidir"]

    negrita = Font(bold=True)
    cab = PatternFill("solid", fgColor="D9E1F2")
    ojo = PatternFill("solid", fgColor="FCE4D6")
    arriba = Alignment(vertical="top", wrap_text=True)
    wb = Workbook()

    h = wb.active
    h.title = "Empieza aqui"
    h.column_dimensions["A"].width = 116
    texto = [
        ("Lo que quedo abierto, y por que no se cerro solo", True),
        ("", False),
        ("Del cuaderno que firmaron el 14 de septiembre se aplicaron DIEZ exclusiones. Las otras siete no,", False),
        ("y no es un descuido del canal: es que faltaba una decision que solo ustedes pueden tomar.", False),
        ("", False),
        ("SEIS las firmaron NO CUMPLE cambiando la propuesta, que decia INDETERMINADO, y sin comentario.", False),
        ("El problema no es que hayan cambiado la propuesta: es POR QUE MOTIVO se excluyen. Los diez que si", False),
        ("se aplicaron fallan porque su ficha EXIGE otro organismo --S. aureus, E. coli, micobacterias--,", False),
        ("y ese motivo ya tiene codigo: ORG. Estos seis no nombran bacteria alguna. No es «otro organismo»,", False),
        ("es «no consta el organismo», y ese motivo NO esta en el vocabulario.", False),
        ("", False),
        ("El vocabulario de exclusion es cerrado a proposito (scripts/exclusion_codes.py): «ningun codigo se", False),
        ("inventa sobre la marcha; un codigo nuevo es una enmienda al protocolo y se declara con su fecha y", False),
        ("su motivo». Asi se anadieron IDI, PRO, INT y NOREC. Por eso hace falta esta segunda firma.", False),
        ("", False),
        ("Lo que se propone", True),
        ("", False),
        ("  Codigo nuevo: %s" % CODIGO, False),
        ("  Significa   : %s." % GLOSA, False),
        ("", False),
        ("Es hermano de NOREC, y conviene verlo asi: los demas codigos excluyen por lo que el estudio DICE;", False),
        ("NOREC excluye por lo que esta revision no pudo LEER, y %s por lo que el registro no DECLARA." % CODIGO, False),
        ("Los tres ultimos son propiedades del proceso, no del estudio, y el manuscrito tiene que decirlo.", False),
        ("", False),
        ("Lo que conviene que sepan antes de firmar", True),
        ("", False),
        ("Estos siete estudios son, justamente, la prueba de lo que el articulo sostiene. El titulo promete", False),
        ("medir si este cuerpo de evidencia se puede verificar y replicar, y «hay fichas de registro cuya", False),
        ("bacteria no consta en ninguna parte» es un resultado, no un estorbo. Si se excluyen, salen del", False),
        ("total y hay que contarlos igualmente en el diagrama PRISMA y en la seccion de exclusiones; si se", False),
        ("quedan, se declaran como lo que son. Las dos salidas son defendibles. La que no lo es, es que no", False),
        ("aparezcan.", False),
        ("", False),
        ("Ejemplo de como se rellena", True),
        ("", False),
        ("  study_id             EST-209", False),
        ("  titulo               Phage Safety Retrospective Cohort Study", False),
        ("  frase_literal        ...patients having had a bone or joint or implant infection treated by", False),
        ("                       phagotherapy and having had an adverse event...", False),
        ("  decision_firmada     EXCLUIR con %s     <- se escoge del desplegable" % CODIGO, False),
        ("  comentario           La ficha no nombra bacteria en ningun campo. Se comprobo tambien en la", False),
        ("                       pagina del registro el 2026-09-15.", False),
        ("", False),
        ("El comentario NO es opcional: PRISMA 16b pide el motivo de cada estudio excluido, uno por uno, y", False),
        ("ese texto es el que se imprime en el anexo S16 que lee el editor. Sin el, la exclusion no entra.", False),
    ]
    for i, (t, b) in enumerate(texto, start=1):
        c = h.cell(row=i, column=1, value=t)
        if b:
            c.font = negrita

    s = wb.create_sheet("Las siete")
    cols = ["study_id", "titulo", "registro", "identificador", "campo_de_la_ficha",
            "frase_literal_de_la_ficha", "url", "lo_que_firmaron_el_14",
            "decision_firmada", "comentario"]
    anchos = [11, 54, 17, 20, 20, 76, 44, 20, 24, 54]
    for j, (n, a) in enumerate(zip(cols, anchos), start=1):
        c = s.cell(row=1, column=j, value=n)
        c.font, c.fill, c.alignment = negrita, cab, arriba
        s.column_dimensions[c.column_letter].width = a
    firmadas = {x["study_id"]: "NO CUMPLE" for x in d["firmadas_sin_codigo"]}
    for i, est in enumerate(abiertas, start=2):
        e = ev[est]
        valores = {
            "study_id": est,
            "titulo": e["titulo_en_el_corpus"],
            "registro": e["registro"],
            "identificador": e["identificador"],
            "campo_de_la_ficha": e["campo_de_la_ficha"],
            "frase_literal_de_la_ficha": e["frase_literal_de_la_ficha"],
            "url": e["url"],
            "lo_que_firmaron_el_14": firmadas.get(est, "(lo dejaron en blanco)"),
            "decision_firmada": "",
            "comentario": "",
        }
        for j, n in enumerate(cols, start=1):
            c = s.cell(row=i, column=j, value=valores[n])
            c.alignment = arriba
            if n in ("decision_firmada", "comentario"):
                c.fill = ojo
        s.row_dimensions[i].height = 62
    dv = DataValidation(
        type="list",
        formula1='"EXCLUIR con %s,SE QUEDA en el corpus"' % CODIGO,
        allow_blank=True)
    dv.error = "Escoja una de las dos."
    s.add_data_validation(dv)
    dv.add("I2:I%d" % (len(abiertas) + 1))
    s.freeze_panes = "A2"

    e = wb.create_sheet("El codigo nuevo")
    e.column_dimensions["A"].width = 40
    e.column_dimensions["B"].width = 74
    e.cell(row=1, column=1, value="Enmienda al protocolo: un codigo mas").font = negrita
    filas = [
        ("Codigo", CODIGO),
        ("Significado", GLOSA),
        ("Por que no vale ORG", "ORG dice «organismo distinto de P. aeruginosa». En estas "
                                "fichas no hay organismo ninguno: afirmar que es «distinto» "
                                "seria afirmar mas de lo comprobado."),
        ("Cuando se decidio", "(fecha)"),
        ("Se acepta el codigo? (SI / NO)", ""),
        ("Si NO, que codigo usar en su lugar", ""),
    ]
    for i, (k, v) in enumerate(filas, start=3):
        e.cell(row=i, column=1, value=k).font = negrita
        c = e.cell(row=i, column=2, value=v)
        c.alignment = arriba
        if not v or v == "(fecha)":
            c.fill = ojo

    dup = wb.create_sheet("El duplicado")
    dup.column_dimensions["A"].width = 40
    dup.column_dimensions["B"].width = 74
    dup.cell(row=1, column=1, value="EST-186 y EST-187: ya confirmaron que son el mismo ensayo").font = negrita
    for i, (k, v) in enumerate([
        ("Lo que respondieron el 14", "si, son el mismo ensayo (comprobado por N. Trelles)"),
        ("Que falta", "decir cual de las dos fichas es la principal. La otra deja de ser "
                      "un estudio y pasa a ser un informe mas de ella; el corpus baja en "
                      "uno por duplicacion, no por criterio, y eso se cuenta distinto en "
                      "el diagrama PRISMA."),
        ("EST-186", "CTIS 2023-507203-55-00 - «A three part... SAD and MD», decision 2023-08-08"),
        ("EST-187", "CTIS 2022-503145-22-00 - «A two part... SAD and MD», decision 2023-07-07"),
        ("Cual es la principal? (EST-186 / EST-187)", ""),
        ("Por que", ""),
    ], start=3):
        dup.cell(row=i, column=1, value=k).font = negrita
        c = dup.cell(row=i, column=2, value=v)
        c.alignment = arriba
        if not v:
            c.fill = ojo

    fi = wb.create_sheet("Firma")
    fi.column_dimensions["A"].width = 46
    fi.column_dimensions["B"].width = 52
    fi.cell(row=1, column=1, value="Firma de los dos revisores").font = negrita
    fi.cell(row=2, column=1,
            value="Sin las dos firmas y la fecha no se aplica nada, ni el codigo nuevo ni las exclusiones.")
    for i, k in enumerate(["Revisor 1 (nombre completo)",
                           "Revisor 2 (nombre completo)",
                           "Fecha (AAAA-MM-DD)"], start=4):
        fi.cell(row=i, column=1, value=k).font = negrita
        fi.cell(row=i, column=2, value="").fill = ojo

    wb.save(CUADERNO)
    print("%d filas abiertas: %s" % (len(abiertas), ", ".join(abiertas)))
    print("cuaderno: %s" % CUADERNO)


if __name__ == "__main__":
    main()
