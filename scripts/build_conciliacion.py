# -*- coding: utf-8 -*-
"""Tabla de conciliación informe → estudio → brazo → desenlace.

POR QUE EXISTE. El manuscrito imprime ocho recuentos que parecen decir lo
mismo y no lo dicen: 11 diseños comparativos en la Tabla 2, 14 estudios con
grupo de comparación en Resultados, 11 evaluables en la Tabla 5, 18 brazos en
el primer filtro de la Tabla 6, 130 filas de brazo comparadas entre los dos
extractores, 103 brazos extraídos, 79 brazos legibles y 71 estudios con texto.
Un árbitro que los cruce sin una tabla que los concilie encuentra ocho cifras
que no cuadran. Este script produce esa tabla y, con ella, la conciliación
aritmética de las ocho.

SALIDA
    quality_reports/conciliacion_estudio_brazo.csv    una fila por estudio
    quality_reports/conciliacion_recuentos.md         las ocho cifras, cuadradas
"""
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

# Diseños que cuentan como comparativos. La Tabla 2 clasifica sobre lo que
# declara el RESUMEN y no incluye cohortes; la evaluación de riesgo de sesgo
# clasifica sobre lo ADJUDICADO en el artículo y sí las incluye. Los dos
# criterios son legítimos y dan cifras distintas: la tabla lo hace visible.
ENSAYOS = {"RCT", "non-randomised trial"}
COHORTES = {"prospective cohort", "retrospective cohort"}


def leer(p, enc="utf-8"):
    with open(p, encoding=enc, newline="") as fh:
        return list(csv.DictReader(fh))


def main():
    grupos = leer(RS / "cribado" / "study_groups.csv")
    excl = {r["study_id"]: r for r in leer(RS / "cribado" / "exclusiones_tras_texto_completo.csv")}
    pre = {r["id_provisional"]: r for r in leer(RS / "extraccion" / "pre_extraccion_desde_resumen.csv")}
    adj = leer(RS / "extraccion" / "extraccion_adjudicada.csv")
    # lleva BOM: la primera clave sale como "﻿study_id"
    rob = leer(RS / "riesgo_sesgo" / "riesgo_sesgo_comparativos_adjudicado.csv",
               enc="utf-8-sig")
    # Las «filas comparadas» NO son las del fichero de conflictos: ese solo
    # guarda las que tuvieron al menos un desacuerdo. Las comparadas son las que
    # estaban en los dos cuadernos, y las cuenta `compare_extractions.py`.
    conc = json.loads((QR / "extraction_agreement.json").read_text(encoding="utf-8"))

    pdfs = {q.stem for q in (RS / "textos_completos" / "pdf").iterdir()
            if q.suffix.lower() in (".pdf", ".docx")}
    web = RS / "textos_completos" / "texto_html"
    if web.exists():
        pdfs |= {q.stem for q in web.glob("*.txt")}

    # informes por estudio, y situación
    info = {}
    for g in grupos:
        eid = "EST-%03d" % int(g["estudio"])
        d = info.setdefault(eid, {"informes": 0, "tipos": set(), "situacion": g["situacion"],
                                  "titulo": g["titulo"]})
        d["informes"] += 1
        d["tipos"].add(g["tipo_informe"])

    brazos = {}
    for r in adj:
        brazos.setdefault(r["study_id"], []).append(r)

    rob_ids = {r["study_id"] for r in rob}

    campos = ["study_id", "informes", "tipos_de_informe", "situacion",
              "diseno_declarado_resumen", "diseno_adjudicado", "grupo_comparador",
              "brazos_extraidos", "texto_completo", "en_tabla_2", "en_tabla_5",
              "aporta_brazos_a_tabla_6", "motivo_de_exclusion", "titulo"]
    filas = []
    for eid in sorted(info):
        d = info[eid]
        ex = excl.get(eid)
        bs = brazos.get(eid, [])
        adjudicado = sorted({b["study_design"] for b in bs if b["study_design"]})
        dec = (pre.get(eid) or {}).get("study_design", "")
        if adjudicado:
            comp = ("sí" if any(x in ENSAYOS | COHORTES for x in adjudicado)
                    else "no")
        else:
            comp = "no evaluable"
        filas.append({
            "study_id": eid,
            "informes": d["informes"],
            "tipos_de_informe": "; ".join(sorted(d["tipos"])),
            "situacion": d["situacion"],
            "diseno_declarado_resumen": dec,
            "diseno_adjudicado": "; ".join(adjudicado),
            "grupo_comparador": comp,
            "brazos_extraidos": len(bs),
            "texto_completo": "sí" if eid in pdfs else "no",
            "en_tabla_2": "no" if ex else ("sí" if d["situacion"] in ("extraible", "solo-resumen") else "no"),
            "en_tabla_5": "sí" if eid in rob_ids else "no",
            "aporta_brazos_a_tabla_6": "sí" if (bs and not ex) else "no",
            "motivo_de_exclusion": ("%s — %s" % (ex["codigo"], ex["motivo"][:90])) if ex else "",
            "titulo": d["titulo"][:110],
        })

    salida = QR / "conciliacion_estudio_brazo.csv"
    with salida.open("w", encoding="utf-8-sig", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=campos)
        w.writeheader()
        w.writerows(filas)

    # ------------------------------------------------ las ocho cifras
    vivos = [f for f in filas if not f["motivo_de_exclusion"]]
    t2 = [f for f in vivos if f["en_tabla_2"] == "sí"]
    t2_comp = [f for f in t2 if f["diseno_declarado_resumen"] in ENSAYOS]
    # DOS REGLAS, DOS CIFRAS, Y LA DIFERENCIA ES UN ESTUDIO. `make_rob_forms.
    # corpus()` asigna al estudio el diseño del PRIMER brazo que encuentra y
    # descarta los demas; contar «comparativo si CUALQUIER brazo lo es» da uno
    # mas. El estudio en discordia es EST-004, cuyo brazo A es serie de casos y
    # cuyo brazo B es cohorte prospectiva. Las dos cifras se publican aqui
    # porque la eleccion entre ellas es una decision de los autores, no del
    # canal, y esta abierta.
    adj_comp = [f for f in vivos if f["grupo_comparador"] == "sí"]
    adj_comp_primero = [f for f in vivos
                        if (f["diseno_adjudicado"].split("; ") or [""])[0] in ENSAYOS | COHORTES]
    discordia = sorted(set(f["study_id"] for f in adj_comp)
                       - set(f["study_id"] for f in adj_comp_primero))
    t5 = [f for f in filas if f["en_tabla_5"] == "sí"]
    brazos_vivos = [b for eid, bs in brazos.items() if eid not in excl for b in bs]
    brazos_comp = [b for b in brazos_vivos if b["study_design"] in ENSAYOS | COHORTES]
    brazos_leg = [b for b in brazos_vivos if b["study_id"] in pdfs]
    con_texto = [f for f in vivos if f["texto_completo"] == "sí"]

    L = ["# Conciliación de los ocho recuentos", "",
         "Generado por `scripts/build_conciliacion.py`. Cada cifra sale de contar la",
         "tabla `conciliacion_estudio_brazo.csv`, no de los escalares.", "",
         "| Cifra del manuscrito | Valor | Unidad | Poblacion sobre la que se cuenta |",
         "|---|---|---|---|",
         "| Diseños comparativos, Tabla 2 | %d | estudios | de los %d recuperables, clasificados por el diseño **que declara el resumen**; NO incluye cohortes |" % (len(t2_comp), len(t2)),
         "| Estudios con grupo de comparación, Resultados | %d | estudios | del corpus vivo, por el diseño **adjudicado sobre el artículo**; SÍ incluye cohortes. Regla del canal: manda el PRIMER brazo |" % len(adj_comp_primero),
         "| ídem, si cuenta **cualquier** brazo comparativo | %d | estudios | la diferencia es %s, con un brazo serie de casos y otro cohorte prospectiva. **Decisión abierta** |" % (len(adj_comp), ", ".join(discordia) or "ninguno"),
         "| Comparativos evaluables, Tabla 5 | %d | estudios | los %d anteriores **que tienen texto completo** |" % (len(t5), len(adj_comp_primero)),
         "| Primer filtro de la Tabla 6 | %d | **brazos** | brazos de esos estudios comparativos; un estudio aporta más de un brazo |" % len(brazos_comp),
         "| Filas de brazo comparadas | %d | **filas** | brazos presentes en los DOS cuadernos (A tenía %d, B tenía %d), **incluidos los de estudios excluidos después** |" % (conc["filas_comparadas"], conc["filas_a"], conc["filas_b"]),
         "| Filas adjudicadas en total | %d | **filas** | el cuaderno adjudicado entero; %d pertenecen a estudios excluidos más tarde, y %d − %d = %d |" % (len(adj), len(adj) - len(brazos_vivos), len(adj), len(adj) - len(brazos_vivos), len(brazos_vivos)),
         "| Brazos extraídos | %d | **brazos** | todos los brazos del corpus vivo |" % len(brazos_vivos),
         "| Brazos legibles | %d | **brazos** | los anteriores cuyo estudio tiene texto completo |" % len(brazos_leg),
         "| Estudios con texto obtenido | %d | estudios | del corpus vivo |" % len(con_texto),
         "",
         "## Las tres confusiones que la tabla deshace", "",
         "1. **Estudio ≠ brazo.** Tres de las ocho cifras cuentan brazos y cinco cuentan",
         "   estudios. Los %d brazos del primer filtro de la Tabla 6 salen de los %d" % (len(brazos_comp), len(adj_comp)),
         "   estudios comparativos, no de otra población.",
         "2. **Diseño declarado ≠ diseño adjudicado.** La Tabla 2 clasifica por el resumen",
         "   sobre los %d recuperables; la evaluación de riesgo de sesgo clasifica por el" % len(t2),
         "   artículo sobre el corpus vivo. Que las dos den %d y %d no es contradicción:" % (len(t2_comp), len(adj_comp)),
         "   son criterios distintos, y la diferencia son las cohortes, que el resumen no",
         "   cuenta como comparativas y el artículo sí.",
         "3. **El corpus de hoy ≠ el corpus que se comparó.** Las %d filas de brazo son un" % conc["filas_comparadas"],
         "   recuento histórico del trabajo de los dos extractores e incluyen estudios",
         "   excluidos después. El puente es el cuaderno adjudicado: %d filas en total," % len(adj),
         "   de las que %d pertenecen a estudios excluidos más tarde, y quedan %d." % (len(adj) - len(brazos_vivos), len(brazos_vivos)),
         "",
         "## Lo que esta tabla NO cierra", "",
         "**%s.** La regla que el canal usa para asignar un diseño a un estudio con" % (", ".join(discordia) or "Ninguno"),
         "brazos de diseño distinto es «manda el primer brazo», y es arbitraria. Con esa",
         "regla hay %d estudios con grupo de comparación; contando cualquier brazo" % len(adj_comp_primero),
         "comparativo hay %d, y el evaluable pasaría de %d a %d, porque ese estudio tiene" % (len(adj_comp), len(t5), len(t5) + len(discordia)),
         "texto completo. Es una decisión de los autores y está abierta.",
         ""]
    (QR / "conciliacion_recuentos.md").write_text("\n".join(L), encoding="utf-8", newline="\n")

    print("conciliación de %d estudios -> %s" % (len(filas), salida.name))
    for l in L[5:14]:
        print("  " + l)


if __name__ == "__main__":
    main()
