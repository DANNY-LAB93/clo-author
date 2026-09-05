"""Construye la tabla de riesgo de sesgo de los estudios comparativos.

QUE ENTRA. Solo `riesgo_sesgo_comparativos_adjudicado.csv`, que es lo que sale
del ingestor: valores por acuerdo de los dos revisores o por consenso firmado.
Nada mas. Si un juicio no esta ahi, aqui sale como pendiente; no se deduce, no
se rellena con el juicio de otro dominio ni se promedia.

EL ALCANCE NO LO DECIDE ESTE GUION. Los estudios y su instrumento salen de
`make_rob_forms.corpus()`, que asigna el instrumento por el diseño adjudicado
sobre el texto completo --no por el diseño que declara el resumen--. Por eso el
alcance de esta tabla (11 evaluables) no coincide con los 11 comparativos que la
Tabla 2 cuenta desde el resumen: son dos medidas distintas y el manuscrito lo
dice.

UNA TABLA, DOS INSTRUMENTOS. RoB 2 tiene cinco dominios y ROBINS-I siete, y no
significan lo mismo. Se comparten las columnas D1-D7 por concision, y el pie
declara que dominio es cada una en cada instrumento. Las dos ultimas columnas de
un ECA salen "n. a." porque RoB 2 no tiene esos dominios, no porque falte el
juicio.

Salidas:
    paper/tablas/tabla_7_riesgo_sesgo.csv
    paper/tablas/tabla_7_riesgo_sesgo.md
    quality_reports/rob_tabla_estado.json   -- cuantos juicios hay y cuantos faltan

Uso:
    python scripts/build_rob_table.py
"""
import csv
import collections
import json
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from make_rob_forms import corpus
from rob_instruments import COMPARATIVOS, NO_EVALUABLE, PENDIENTE, SIMPLIFICADOS

ROOT = pathlib.Path(__file__).resolve().parent.parent
ADJUDICADO = (ROOT / "revision_sistematica" / "riesgo_sesgo"
              / "riesgo_sesgo_comparativos_adjudicado.csv")
TABLAS = ROOT / "paper" / "tablas"
ESTADO = ROOT / "quality_reports" / "rob_tabla_estado.json"

PENDIENTE_CELDA = "pendiente"
NO_APLICA = "n. a."

# Como se abrevia cada juicio en la tabla. El nombre largo no cabe en una
# celda y la abreviatura se declara en el pie.
CORTO = {
    "Bajo riesgo de sesgo": "Bajo",
    "Algunas preocupaciones": "Algunas preocupaciones",
    "Alto riesgo de sesgo": "Alto",
    "Riesgo moderado": "Moderado",
    "Riesgo grave": "Grave",
    "Riesgo crítico": "Crítico",
    "Sin información para juzgar": "Sin información",
}

NOMBRE = {"rob2": "RoB 2", "robins": "ROBINS-I"}

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass


def dominios():
    """{clave: [codigos en orden]} y {(clave, codigo): titulo del dominio}."""
    orden, titulo = {}, {}
    for inst in SIMPLIFICADOS:
        orden[inst["clave"]] = [it["codigo"] for it in inst["items"]]
        for it in inst["items"]:
            titulo[(inst["clave"], it["codigo"])] = it["texto_es"]
    return orden, titulo


def juicios():
    """{(estudio, instrumento, item): valor} de lo adjudicado, si lo hay."""
    if not ADJUDICADO.exists():
        return {}
    with open(ADJUDICADO, encoding="utf-8-sig", newline="") as fh:
        return {(r["study_id"], r["instrumento"], r["item"]): r["valor"].strip()
                for r in csv.DictReader(fh) if r["valor"].strip()}


def main():
    orden, titulo = dominios()
    J = juicios()
    filas_corpus = [c for c in corpus() if c["diseno"] in COMPARATIVOS]
    evaluables = [c for c in filas_corpus
                  if c["instrumento"] not in (NO_EVALUABLE, PENDIENTE)]
    sin_texto = [c for c in filas_corpus if c["instrumento"] == NO_EVALUABLE]

    ancho = max(len(v) for v in orden.values())
    cab = (["Estudio", "Diseño", "Herramienta"]
           + ["D%d" % (i + 1) for i in range(ancho)] + ["Juicio global"])

    filas, faltan, puestos = [], 0, 0
    for c in sorted(evaluables, key=lambda x: (x["instrumento"], x["study_id"])):
        clave = c["instrumento"]
        cel = []
        for i in range(ancho):
            cods = orden[clave]
            if i >= len(cods):
                cel.append(NO_APLICA)
                continue
            v = J.get((c["study_id"], clave, cods[i]), "")
            if v:
                puestos += 1
            else:
                faltan += 1
            cel.append(CORTO.get(v, v) if v else PENDIENTE_CELDA)
        g = J.get((c["study_id"], clave, "GLOBAL"), "")
        if g:
            puestos += 1
        else:
            faltan += 1
        filas.append([c["study_id"], c["diseno"], NOMBRE[clave]] + cel
                     + [CORTO.get(g, g) if g else PENDIENTE_CELDA])

    TABLAS.mkdir(parents=True, exist_ok=True)
    with open(TABLAS / "tabla_7_riesgo_sesgo.csv", "w", encoding="utf-8-sig",
              newline="") as fh:
        w = csv.writer(fh)
        w.writerow(cab)
        w.writerows(filas)
    md = ["| " + " | ".join(cab) + " |",
          "|" + "|".join(["---"] * len(cab)) + "|"]
    md += ["| " + " | ".join(f) + " |" for f in filas]
    (TABLAS / "tabla_7_riesgo_sesgo.md").write_text("\n".join(md) + "\n",
                                                    encoding="utf-8")

    estado = {
        "comparativos_adjudicados": len(filas_corpus),
        "evaluables": len(evaluables),
        "sin_texto_completo": len(sin_texto),
        "sin_texto_completo_ids": sorted(c["study_id"] for c in sin_texto),
        "por_instrumento": dict(collections.Counter(
            NOMBRE[c["instrumento"]] for c in evaluables)),
        "celdas_totales": puestos + faltan,
        "celdas_con_juicio": puestos,
        "celdas_pendientes": faltan,
        "completa": faltan == 0,
        "dominios": {NOMBRE[k]: [titulo[(k, c)] for c in v]
                     for k, v in orden.items()},
    }
    ESTADO.write_text(json.dumps(estado, ensure_ascii=False, indent=2),
                      encoding="utf-8")

    print("comparativos con diseño adjudicado: %d  (evaluables %d, sin texto %d)"
          % (len(filas_corpus), len(evaluables), len(sin_texto)))
    for k, v in estado["por_instrumento"].items():
        print("   %-10s %d estudios" % (k, v))
    print("celdas con juicio: %d de %d" % (puestos, puestos + faltan))
    if faltan:
        # No se escribe nada en el manuscrito mientras falte un juicio. Una
        # tabla a medias publicada como completa es peor que no tenerla.
        print()
        print("LA TABLA NO ESTA COMPLETA. Faltan %d juicios." % faltan)
        print("Los rellenan D. Valdiviezo y N. Trelles en sus formularios:")
        print("   python scripts/make_rob_forms.py --simplificado   (ya generados)")
        print("   python scripts/compare_rob.py --simplificado")
        print("   python scripts/ingest_rob.py --simplificado")
        print("   python scripts/build_rob_table.py")
    print("escrito %s" % (TABLAS / "tabla_7_riesgo_sesgo.csv").relative_to(ROOT))


if __name__ == "__main__":
    main()
