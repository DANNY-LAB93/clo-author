# -*- coding: utf-8 -*-
"""Las diecisiete cifras del manuscrito, recalculadas desde la fuente.

POR QUE EXISTE. Un árbitro pidió auditar cada cifra sin dar ninguna por buena,
y con cinco cosas por cifra: unidad de análisis, denominador, fuente exacta,
cálculo y veredicto. Este script no lee los escalares: vuelve a contar sobre
los ficheros de datos y compara con lo que el manuscrito publica. Si una cifra
no se reproduce, lo dice; no la arregla.

CADA CIFRA TRAE SU CALCULO. La columna «cálculo» no es una glosa: es la
operación que este script ejecutó, escrita con los números que usó, de modo
que se pueda rehacer a mano.

SALIDA
    quality_reports/auditoria_cifras.md
    quality_reports/auditoria_cifras.json
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

ENSAYOS = {"RCT", "non-randomised trial"}
COHORTES = {"prospective cohort", "retrospective cohort"}


def leer(p, enc="utf-8"):
    with open(p, encoding=enc, newline="") as fh:
        return list(csv.DictReader(fh))


# LAS CIFRAS PUBLICADAS QUE ESTE GUION CONTRASTA se actualizaron el
# 2026-09-22, al ingerir las nueve decisiones firmadas de la auditoria del
# 2026-09-16. Once de las diecisiete se movieron a la vez porque EST-063 salio
# del corpus como protocolo. Van escritas a proposito: son lo que el manuscrito
# DICE, y el guion las recuenta desde los ficheros de datos sin mirar
# `synthesis_scalars.json`. Si vuelven a discrepar, el manuscrito esta mal o
# los datos cambiaron, y en los dos casos hay algo que mirar.
def main():
    corpus = leer(RS / "cribado" / "screening_corpus_all.csv")
    grupos = leer(RS / "cribado" / "study_groups.csv")
    excl = {r["study_id"]: r for r in leer(RS / "cribado" / "exclusiones_tras_texto_completo.csv")}
    adj = leer(RS / "extraccion" / "extraccion_adjudicada.csv")
    pre = leer(RS / "extraccion" / "pre_extraccion_desde_resumen.csv")
    # Sin el filtro, un estudio que salio del corpus seguia aportando sus ocho
    # juicios a la Tabla 5. EST-063 salio como protocolo el 2026-09-22.
    rob = [r for r in leer(RS / "riesgo_sesgo"
                           / "riesgo_sesgo_comparativos_adjudicado.csv",
                           enc="utf-8-sig")
           if r["study_id"] not in excl]
    conc = json.loads((QR / "extraction_agreement.json").read_text(encoding="utf-8"))
    S = json.loads((QR / "synthesis_scalars.json").read_text(encoding="utf-8"))

    pdfs = {q.stem for q in (RS / "textos_completos" / "pdf").iterdir()
            if q.suffix.lower() in (".pdf", ".docx")}
    web = RS / "textos_completos" / "texto_html"
    if web.exists():
        pdfs |= {q.stem for q in web.glob("*.txt")}

    estudios = collections.defaultdict(list)
    for g in grupos:
        estudios["EST-%03d" % int(g["estudio"])].append(g)
    vivos = {e: gs for e, gs in estudios.items() if e not in excl}
    brazos_vivos = [r for r in adj if r["study_id"] not in excl]

    # diseño adjudicado por estudio, con la regla firmada el 2026-09-16
    dis = collections.defaultdict(set)
    for r in brazos_vivos:
        if r["study_design"] and r["study_design"] != "NA":
            dis[r["study_id"]].add(r["study_design"])
    comparativos = sorted(e for e, v in dis.items() if v & (ENSAYOS | COHORTES))
    evaluables = sorted(e for e in comparativos if e in pdfs)
    sin_texto = sorted(set(comparativos) - set(evaluables))
    brazos_comp = [r for r in brazos_vivos
                   if r["study_design"] in ENSAYOS | COHORTES]

    rob_items = collections.defaultdict(set)
    for r in rob:
        rob_items[(r["study_id"], r["instrumento"])].add(r["item"])
    n_glob = sum(1 for r in rob if r["item"] == "GLOBAL")
    n_dom = len(rob) - n_glob
    por_inst = collections.Counter(i for (s, i) in rob_items)
    dom_por_inst = {i: len(next(v for (s, j), v in rob_items.items() if j == i) - {"GLOBAL"})
                    for i in por_inst}

    extraibles = [e for e, gs in vivos.items()
                  if gs[0]["situacion"] in ("extraible", "solo-resumen")]
    # `situacion` está en cada informe del grupo; se toma la del designado
    extraibles = []
    solo_registro = []
    for e, gs in vivos.items():
        g = next((x for x in gs if x["informe_para_extraer"] == "SI"), gs[0])
        if g["situacion"] in ("extraible", "solo-resumen"):
            extraibles.append(e)
        if all(x["tipo_informe"] == "ficha de registro" for x in gs):
            solo_registro.append(e)

    suma_fuentes = sum(collections.Counter(
        f.strip() for c in corpus for f in c["sources"].split(";") if f.strip()).values())
    crudos = sum(int(c["n_source_records"] or 1) for c in corpus)

    C = []

    def cifra(nombre, publicada, obtenida, unidad, denom, fuente, calculo, nota=""):
        C.append({"cifra": nombre, "publicada": publicada, "recalculada": obtenida,
                  "unidad": unidad, "denominador": denom, "fuente": fuente,
                  "calculo": calculo,
                  "estado": "consistente" if publicada == obtenida else "CORREGIR",
                  "nota": nota})

    cifra("Registros identificados", 23057, crudos, "registros (filas de exportación)",
          "no aplica: es la primera casilla del diagrama",
          "screening_corpus_all.csv, columna n_source_records",
          "suma de n_source_records sobre los %d informes únicos = %d" % (len(corpus), crudos),
          "la tabla de fuentes del anexo suma %d, que son pares informe×fuente: la "
          "diferencia de %d son registros repetidos DENTRO de una misma fuente, casi "
          "todos de BVS, que agrega dieciséis colecciones"
          % (suma_fuentes, crudos - suma_fuentes))
    cifra("Informes únicos", 17129, len(corpus), "informes", "de los %d registros" % crudos,
          "screening_corpus_all.csv, número de filas",
          "%d registros − %d duplicados = %d" % (crudos, crudos - len(corpus), len(corpus)))
    cifra("Informes a texto completo", 233, len(grupos), "informes",
          "de los %d informes únicos" % len(corpus),
          "study_groups.csv, número de filas",
          "%d filas, una por informe evaluado a texto completo" % len(grupos))
    cifra("Estudios evaluados para elegibilidad", 183, len(estudios), "estudios",
          "de los %d informes" % len(grupos),
          "study_groups.csv, valores distintos de la columna estudio",
          "%d informes agrupados en %d estudios" % (len(grupos), len(estudios)))
    cifra("Estudios incluidos", 136, len(vivos), "estudios",
          "de los %d evaluados" % len(estudios),
          "study_groups.csv menos exclusiones_tras_texto_completo.csv",
          "%d − %d excluidos = %d" % (len(estudios), len(excl), len(vivos)))
    cifra("Informes de los estudios incluidos", 170,
          sum(len(v) for v in vivos.values()), "informes",
          "de los %d informes evaluados" % len(grupos),
          "study_groups.csv, filas cuyo estudio no está excluido",
          "%d − %d informes de estudios excluidos = %d"
          % (len(grupos), len(grupos) - sum(len(v) for v in vivos.values()),
             sum(len(v) for v in vivos.values())))
    cifra("Estudios con publicación recuperable", 94, len(extraibles), "estudios",
          "de los %d incluidos" % len(vivos),
          "study_groups.csv, situación «extraible» o «solo-resumen» del informe designado",
          "%d de %d; los otros %d son solo ficha de registro"
          % (len(extraibles), len(vivos), len(vivos) - len(extraibles)))
    cifra("Estudios con texto obtenido", 70,
          len([e for e in vivos if e in pdfs]), "estudios",
          "de los %d recuperables" % len(extraibles),
          "carpetas textos_completos/pdf y texto_html",
          "%d de %d recuperables = %.1f %%"
          % (len([e for e in vivos if e in pdfs]), len(extraibles),
             100.0 * len([e for e in vivos if e in pdfs]) / len(extraibles)))
    cifra("Estudios solo con ficha de registro", 42, len(solo_registro), "estudios",
          "de los %d incluidos" % len(vivos),
          "study_groups.csv, estudios cuyos informes son todos ficha de registro",
          "%d + %d recuperables = %d incluidos"
          % (len(solo_registro), len(extraibles), len(vivos)))
    cifra("Filas de brazo comparadas", 130, conc["filas_comparadas"], "filas de brazo",
          "brazos presentes en los dos cuadernos de extracción",
          "quality_reports/extraction_agreement.json",
          "cuaderno A %d filas, cuaderno B %d filas, en común %d; es un recuento "
          "histórico e incluye estudios excluidos después"
          % (conc["filas_a"], conc["filas_b"], conc["filas_comparadas"]))
    cifra("Brazos extraídos", 102, len(brazos_vivos), "brazos",
          "de los %d estudios incluidos" % len(vivos),
          "extraccion_adjudicada.csv menos los estudios excluidos",
          "%d filas adjudicadas − %d de estudios excluidos después = %d"
          % (len(adj), len(adj) - len(brazos_vivos), len(brazos_vivos)))
    cifra("Brazos con texto completo", 78,
          len([r for r in brazos_vivos if r["study_id"] in pdfs]), "brazos",
          "de los %d brazos extraídos" % len(brazos_vivos),
          "extraccion_adjudicada.csv cruzado con las carpetas de texto",
          "%d de %d brazos pertenecen a estudios con texto"
          % (len([r for r in brazos_vivos if r["study_id"] in pdfs]), len(brazos_vivos)))
    cifra("Estudios con diseño comparativo", 14, len(comparativos), "estudios",
          "de los %d incluidos" % len(vivos),
          "extraccion_adjudicada.csv, diseño adjudicado; regla firmada el 2026-09-16",
          "estudios con al menos un brazo de diseño %s = %d"
          % ("/".join(sorted(ENSAYOS | COHORTES)), len(comparativos)))
    cifra("Comparativos evaluables", 11, len(evaluables), "estudios",
          "de los %d comparativos" % len(comparativos),
          "los comparativos cuyo estudio tiene texto completo",
          "%d − %d sin texto (%s) = %d"
          % (len(comparativos), len(sin_texto), ", ".join(sin_texto), len(evaluables)))
    cifra("Ensayos en la Tabla 2", 10,
          sum(1 for r in pre if r["id_provisional"] in vivos
              and r["id_provisional"] in extraibles and r["study_design"] in ENSAYOS),
          "estudios", "de los %d recuperables" % len(extraibles),
          "pre_extraccion_desde_resumen.csv, diseño DECLARADO en el resumen",
          "criterio distinto del anterior: clasifica por el resumen y no cuenta cohortes")
    cifra("Brazos con diseño comparativo", 17, len(brazos_comp), "brazos",
          "de los %d brazos extraídos" % len(brazos_vivos),
          "extraccion_adjudicada.csv, brazos cuyo diseño es comparativo",
          "%d brazos aportados por los %d estudios comparativos"
          % (len(brazos_comp), len(comparativos)))
    cifra("Celdas de la Tabla 5", 82, len(rob), "celdas de juicio",
          "de los %d estudios evaluables" % len(evaluables),
          "riesgo_sesgo_comparativos_adjudicado.csv",
          "%d × %d dominios de RoB 2 = %d; %d × %d dominios de ROBINS-I = %d; "
          "%d + %d = %d juicios de dominio; más %d juicios globales, uno por "
          "estudio, = %d celdas"
          % (por_inst["rob2"], dom_por_inst["rob2"], por_inst["rob2"] * dom_por_inst["rob2"],
             por_inst["robins"], dom_por_inst["robins"],
             por_inst["robins"] * dom_por_inst["robins"],
             por_inst["rob2"] * dom_por_inst["rob2"],
             por_inst["robins"] * dom_por_inst["robins"], n_dom, n_glob, len(rob)),
          "el manuscrito las llama «juicios de dominio» y no lo son: %d son de "
          "dominio y %d son globales" % (n_dom, n_glob))

    malas = [c for c in C if c["estado"] == "CORREGIR"]
    L = ["# Auditoría de las diecisiete cifras", "",
         "Generado por `scripts/audita_cifras.py`. Cada cifra se vuelve a contar",
         "sobre los ficheros de datos; ninguna se lee de `synthesis_scalars.json`.", "",
         "**%d de %d cifras se reproducen exactamente.**" % (len(C) - len(malas), len(C)), ""]
    for c in C:
        L += ["## %s — %s" % (c["cifra"], "✔ consistente" if c["estado"] == "consistente"
                              else "✘ CORREGIR"), "",
              "| | |", "|---|---|",
              "| Publicada | %s |" % c["publicada"],
              "| Recalculada | %s |" % c["recalculada"],
              "| Unidad de análisis | %s |" % c["unidad"],
              "| Denominador | %s |" % c["denominador"],
              "| Fuente | `%s` |" % c["fuente"],
              "| Cálculo | %s |" % c["calculo"]]
        if c["nota"]:
            L += ["| Advertencia | %s |" % c["nota"]]
        L += [""]
    (QR / "auditoria_cifras.md").write_text("\n".join(L), encoding="utf-8", newline="\n")
    (QR / "auditoria_cifras.json").write_text(
        json.dumps({"cifras": C, "juicios_de_dominio": n_dom, "juicios_globales": n_glob,
                    "celdas_tabla5": len(rob), "comparativos": comparativos,
                    "evaluables": evaluables, "sin_texto": sin_texto},
                   ensure_ascii=False, indent=2), encoding="utf-8", newline="\n")

    print("%d cifras auditadas; %d se reproducen, %d exigen corrección"
          % (len(C), len(C) - len(malas), len(malas)))
    for c in C:
        print("  %-42s publicada %-7s recalculada %-7s %s"
              % (c["cifra"][:42], c["publicada"], c["recalculada"],
                 "" if c["estado"] == "consistente" else "<-- CORREGIR"))
    print()
    print("Tabla 5: %d juicios de dominio + %d globales = %d celdas"
          % (n_dom, n_glob, len(rob)))


if __name__ == "__main__":
    main()
