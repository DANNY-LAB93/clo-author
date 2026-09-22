# -*- coding: utf-8 -*-
"""El fichero firmado de quien tiene grupo de comparacion de verdad.

Uso:
    python scripts/build_grupo_comparacion.py

La etiqueta «comparativo» sale del DISENO adjudicado: una cohorte cuenta como
comparativa aunque no tenga con que comparar. La hoja 6 de la auditoria del
2026-09-16 pregunto como nombrar eso y los dos autores firmaron el 2026-09-22
la respuesta: «15 con diseno comparativo, de los cuales 5 con grupo de
comparacion».

La frase de apoyo de cada estudio NO se teclea: se saca de la entrada 1 del
dominio 1 de su propio cuaderno de consenso.
"""
import csv, pathlib, re, sys
from openpyxl import load_workbook

ROOT = pathlib.Path(__file__).resolve().parent.parent
RS = ROOT / "revision_sistematica"
CONS = RS / "riesgo_sesgo" / "riesgo_sesgo_comparativos_consenso.xlsx"
ADJ = RS / "riesgo_sesgo" / "riesgo_sesgo_comparativos_adjudicado.csv"
EXCL = RS / "cribado" / "exclusiones_tras_texto_completo.csv"
SALIDA = RS / "riesgo_sesgo" / "grupo_de_comparacion_real.csv"

# Lo que los dos autores firmaron en la hoja 6. El «por que» de los cinco que
# SI lo tienen va aqui porque su nota del dominio 1 no lo dice: lo dice el
# articulo, y la hoja lo recoge.
FIRMADO = {
    "EST-004": ("no", ""),
    "EST-070": ("no", ""),
    "EST-096": ("no", ""),
    "EST-116": ("no", ""),
    "EST-146": ("no", ""),
    "EST-152": ("no", ""),
    "EST-063": ("no", ""),
    "EST-008": ("si", "BX004-A frente a placebo"),
    "EST-021": ("si", "PP1131 frente a cuidado estandar"),
    "EST-132": ("si", "convencional frente a convencional + fago"),
    "EST-055": ("si", "el grupo IV recibe furazidina y cefixima SIN bacteriofago"),
    "EST-108": ("si", "compara con y sin antibiotico concomitante DENTRO de los "
                      "tratados con fago; no compara fago contra no fago"),
}


def notas_del_dominio_1():
    """Entrada 1 de las notas de cada estudio, tal cual la escribieron."""
    out = {}
    wb = load_workbook(CONS, data_only=True)
    for hoja in wb.sheetnames:
        for fila in wb[hoja].iter_rows(min_row=2, values_only=True):
            if not fila or not fila[0]:
                continue
            est = str(fila[0]).strip()
            if not re.match(r"^EST-\d+$", est):
                continue
            texto = ""
            for c in fila:
                s = str(c or "")
                if re.search(r"(?m)^\s*1[.)]", s) and len(s) > 40:
                    texto = s
                    break
            if not texto:
                continue
            trozos = re.split(r"(?m)^\s*(\d+)[.)]\s*\t?", texto)
            for num, cuerpo in zip(trozos[1::2], trozos[2::2]):
                if int(num) == 1:
                    out[est] = " ".join(cuerpo.split())
    return out


def nota_de_respaldo(est):
    """EST-004 se evaluo en un cuaderno aparte el 2026-09-17 y su frase sobre la
    ausencia de control esta en el juicio GLOBAL, no en el dominio 1."""
    import csv as _c
    f = RS / "riesgo_sesgo" / "evidencia_por_dominio.csv"
    for r in _c.DictReader(open(f, encoding="utf-8-sig")):
        if r["study_id"] == est and r["dominio"] == "GLOBAL":
            t = r["frase"].split("|| Nota:")[0]
            return " ".join(t.split())
    return ""


notas = notas_del_dominio_1()
fuera = {r["study_id"] for r in csv.DictReader(open(EXCL, encoding="utf-8"))}
evaluables = sorted({r["study_id"] for r in
                     csv.DictReader(open(ADJ, encoding="utf-8-sig"))})

filas, faltan = [], []
for est in evaluables:
    if est not in FIRMADO:
        faltan.append(est)
        continue
    tiene, porque = FIRMADO[est]
    nota = notas.get(est, "") or nota_de_respaldo(est)
    if tiene == "no" and not nota:
        faltan.append("%s (sin nota del dominio 1)" % est)
        continue
    filas.append({
        "study_id": est,
        "en_el_corpus": "no" if est in fuera else "si",
        "tiene_grupo_de_comparacion": tiene,
        "frase_firmada_del_dominio_1": nota,
        "por_que": porque,
        "fuente": "riesgo_sesgo_comparativos_consenso.xlsx, dominio 1, entrada 1",
        "firmado_por": "Danny Javier Valdiviezo Verdugo y Nataly Elizabeth Trelles Avila",
        "fecha": "2026-09-22",
    })

if faltan:
    print("NO SE ESCRIBE. Sin firma de la hoja 6: %s" % ", ".join(faltan))
    sys.exit(1)

with open(SALIDA, "w", encoding="utf-8", newline="") as fh:
    w = csv.DictWriter(fh, fieldnames=list(filas[0].keys()))
    w.writeheader()
    w.writerows(filas)

vivos = [f for f in filas if f["en_el_corpus"] == "si"]
print("escrito %s" % SALIDA.name)
print("  evaluables con juicio : %d  (%d en el corpus)" % (len(filas), len(vivos)))
print("  con grupo real        : %d" % sum(1 for f in vivos if f["tiene_grupo_de_comparacion"] == "si"))
print("  sin grupo real        : %d" % sum(1 for f in vivos if f["tiene_grupo_de_comparacion"] == "no"))
for f in vivos:
    print("    %-9s %-3s %s" % (f["study_id"], f["tiene_grupo_de_comparacion"],
                                (f["frase_firmada_del_dominio_1"] or f["por_que"])[:88]))
