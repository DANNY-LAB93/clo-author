# -*- coding: utf-8 -*-
"""Tabla 3: la completitud, separando el silencio del resumen del del artículo.

POR QUE SE REHIZO. La Tabla 3 medía la completitud SOLO sobre el resumen y el
manuscrito concluía de ahí que «la clase de resistencia no puede asignarse en
el 75,8 % de los estudios». Sobre el resumen es cierto; sobre el estudio no se
sabe, porque el resumen que calla puede tener un artículo que lo dice. Un
árbitro lo señaló y tiene razón: **ausencia en el resumen no es ausencia en el
estudio**, y presentarlas juntas confunde un hueco documental con una
propiedad de la literatura.

LAS CUATRO CATEGORIAS, EXCLUYENTES ENTRE SI, SOBRE LOS 95 RECUPERABLES

  1. declarado en el texto completo
  2. declarado pero no clasificable --el artículo dice «multirresistente» sin
     dar el antibiograma que permita decidir entre MDR, XDR y PDR--
  3. no declarado en el texto completo --silencio del artículo, que sí es una
     propiedad del estudio--
  4. texto completo no recuperado --no sabemos, y no se puede contar como
     silencio del estudio sin mentir--

La columna del resumen se conserva aparte, porque la afirmación sobre lo que
las bases indexan sigue siendo válida y es la que sostiene el argumento sobre
el cribado automatizado.

SALIDA
    quality_reports/tabla3_completitud.csv
    quality_reports/tabla3_completitud.json
"""
import collections
import csv
import json
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
RS = ROOT / "revision_sistematica"
QR = ROOT / "quality_reports"
csv.field_size_limit(200_000_000)

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

VARIABLES = [
    ("resistance_class", "Clase de resistencia (MDR/XDR/PDR)"),
    ("route", "Vía de administración"),
    ("pathogen_scope", "Ámbito de patógeno"),
    ("modality", "Modalidad (monoterapia o combinación)"),
    ("dtr_status", "Criterio DTR"),
]
# Valores que significan «lo dice pero no se puede clasificar», y valores que
# significan «no lo dice». Se declaran aquí y no se adivinan por parecido.
NO_CLASIFICABLE = {"not-classifiable", "not-derivable"}
SILENCIO = {"", "na", "n/a", "no declarado", "no declarada", "none", "nd"}


def leer(p, enc="utf-8"):
    with open(p, encoding=enc, newline="") as fh:
        return list(csv.DictReader(fh))


def valor_de_estudio(filas, campo):
    """Un estudio puede tener varios brazos: vale el primer valor con
    contenido. Si todos callan, calla el estudio."""
    clasif, no_clasif = [], False
    for f in filas:
        v = (f.get(campo) or "").strip()
        if v.lower() in SILENCIO:
            continue
        if v in NO_CLASIFICABLE:
            no_clasif = True
            continue
        clasif.append(v)
    if clasif:
        return clasif[0]
    return "NO_CLASIFICABLE" if no_clasif else ""


def main():
    grupos = leer(RS / "cribado" / "study_groups.csv")
    excl = {r["study_id"] for r in leer(RS / "cribado" / "exclusiones_tras_texto_completo.csv")}
    adj = leer(RS / "extraccion" / "extraccion_adjudicada.csv")
    pre = leer(RS / "extraccion" / "pre_extraccion_desde_resumen.csv")

    pdfs = {q.stem for q in (RS / "textos_completos" / "pdf").iterdir()
            if q.suffix.lower() in (".pdf", ".docx")}
    web = RS / "textos_completos" / "texto_html"
    if web.exists():
        pdfs |= {q.stem for q in web.glob("*.txt")}

    recuperables = []
    for g in grupos:
        eid = "EST-%03d" % int(g["estudio"])
        if eid in excl or g["informe_para_extraer"] != "SI":
            continue
        if g["situacion"] in ("extraible", "solo-resumen"):
            recuperables.append(eid)
    recuperables = sorted(set(recuperables))

    por_est = collections.defaultdict(list)
    for r in adj:
        por_est[r["study_id"]].append(r)
    por_pre = collections.defaultdict(list)
    for r in pre:
        por_pre[r["id_provisional"]].append(r)

    filas, resumen = [], {}
    for campo, titulo in VARIABLES:
        c = collections.Counter()
        for eid in recuperables:
            if eid not in pdfs:
                c["texto completo no recuperado"] += 1
                continue
            v = valor_de_estudio(por_est.get(eid, []), campo)
            if v == "NO_CLASIFICABLE":
                c["declarado pero no clasificable"] += 1
            elif v:
                c["declarado en el texto completo"] += 1
            else:
                c["no declarado en el texto completo"] += 1
        # y lo que decía el resumen, sobre los mismos 95
        cr = sum(1 for eid in recuperables
                 if not valor_de_estudio(por_pre.get(eid, []), campo)
                 or valor_de_estudio(por_pre.get(eid, []), campo) == "NO_CLASIFICABLE")
        n = len(recuperables)
        fila = {
            "variable": titulo,
            "campo": campo,
            "declarado_texto_completo": c["declarado en el texto completo"],
            "declarado_no_clasificable": c["declarado pero no clasificable"],
            "no_declarado_texto_completo": c["no declarado en el texto completo"],
            "texto_no_recuperado": c["texto completo no recuperado"],
            "total": n,
            "no_asignable_en_el_resumen": cr,
            "no_asignable_en_el_resumen_pct": round(100.0 * cr / n, 1),
            "silencio_del_articulo_pct": round(
                100.0 * c["no declarado en el texto completo"] / n, 1),
        }
        assert (fila["declarado_texto_completo"] + fila["declarado_no_clasificable"]
                + fila["no_declarado_texto_completo"] + fila["texto_no_recuperado"]) == n, campo
        filas.append(fila)
        resumen[campo] = fila

    salida = QR / "tabla3_completitud.csv"
    with salida.open("w", encoding="utf-8-sig", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(filas[0].keys()))
        w.writeheader()
        w.writerows(filas)
    (QR / "tabla3_completitud.json").write_text(
        json.dumps({"n_recuperables": len(recuperables),
                    "con_texto": sum(1 for e in recuperables if e in pdfs),
                    "variables": resumen}, ensure_ascii=False, indent=2),
        encoding="utf-8", newline="\n")

    print("Tabla 3 sobre %d estudios recuperables (%d con texto) -> %s"
          % (len(recuperables), sum(1 for e in recuperables if e in pdfs), salida.name))
    print("  %-38s %5s %5s %5s %5s | resumen" % ("variable", "decl", "n.cl", "sil", "s/txt"))
    for f in filas:
        print("  %-38s %5d %5d %5d %5d | %s %%"
              % (f["variable"][:38], f["declarado_texto_completo"],
                 f["declarado_no_clasificable"], f["no_declarado_texto_completo"],
                 f["texto_no_recuperado"], f["no_asignable_en_el_resumen_pct"]))


if __name__ == "__main__":
    main()
