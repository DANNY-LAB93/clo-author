"""Ingiere las dos evaluaciones y lo que se firmó, y produce el juicio final.

DE DÓNDE SALE CADA VALOR. Donde los dos revisores coincidieron, ese es el valor,
y la procedencia es «acuerdo». Donde discreparon, el valor es el que firmaron en
`riesgo_sesgo_conflictos.csv` y la procedencia es «consenso». No hay tercera vía:
un desacuerdo sin firma NO se ingiere y sale listado. La firma es lo que
convierte una respuesta en un consenso; sin ella el dato no es lo que declara ser.

QUÉ SE PUBLICA Y QUÉ NO. Los escalares que salen de aquí solo cuentan los
estudios con juicio completo. Un estudio a medio evaluar no se reparte entre
categorías ni se cuenta como «sin información»: se cuenta como pendiente, que es
lo que es.

LOS 24 SIN TEXTO NO ENTRAN EN NINGÚN PORCENTAJE. No son «riesgo alto» ni
«sin información»: no se evaluaron. Van en su propio escalar, y el manuscrito
tiene que decir que la evaluación cubre 71 de 95 y que la fracción que falta
concentra 6 de los 11 estudios comparativos. Repartirlos entre las categorías
haría parecer completa una evaluación que no lo es.

USO
    python scripts/ingest_rob.py
"""
import argparse
import collections
import csv
import json
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from compare_rob import CONFLICTOS, CONFLICTOS_SIMPLE, lee_libro
from rob_instruments import (INSTRUMENTOS, SIMPLIFICADOS, NO_EVALUABLE,
                             PENDIENTE)

ROOT = pathlib.Path(__file__).resolve().parent.parent
DEST = ROOT / "revision_sistematica" / "riesgo_sesgo"
SALIDA = DEST / "riesgo_sesgo_adjudicado.csv"
SALIDA_SIMPLE = DEST / "riesgo_sesgo_comparativos_adjudicado.csv"
ESCALARES = ROOT / "quality_reports" / "rob_scalars.json"
ESCALARES_SIMPLE = ROOT / "quality_reports" / "rob_comparativos_scalars.json"

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass


CONSENSO = DEST / "riesgo_sesgo_comparativos_consenso.xlsx"


def ingiere_consenso(salida_p, escalares_p):
    """Un solo cuaderno acordado entre los dos autores, con su firma.

    No hay concordancia que medir aqui y no se finge que la haya: la
    procedencia de cada juicio es «consenso», sin excepcion, y el manuscrito
    declara evaluacion por consenso y no por duplicado independiente.

    Se exige la firma por la misma razon que en la ruta de dos cuadernos: sin
    los dos nombres, «acordado entre los autores» es una afirmacion que nadie
    ha hecho. Y se exigen los 82 juicios completos, porque una tabla a medias
    publicada como completa es peor que no tenerla.
    """
    import openpyxl
    if not CONSENSO.exists():
        raise SystemExit("falta %s. Genéralo con make_rob_consensus.py"
                         % CONSENSO.name)
    wb = openpyxl.load_workbook(CONSENSO, data_only=True)
    if "Firma" not in wb.sheetnames:
        raise SystemExit("el cuaderno no tiene hoja «Firma»; regenéralo.")
    fw = wb["Firma"]
    quien = [str(fw.cell(row=r, column=2).value or "").strip() for r in (5, 6)]
    fecha = str(fw.cell(row=7, column=2).value or "").strip()[:10]
    faltan_firma = [q for q in quien if not q]
    if faltan_firma or not fecha:
        raise SystemExit(
            "NO SE INGIERE: falta la firma en la hoja «Firma» de %s.\n"
            "  nombres: %s\n  fecha: %s\n"
            "Sin los dos nombres y la fecha, «acordado entre los autores» no lo "
            "ha afirmado nadie." % (CONSENSO.name,
                                    " / ".join(q or "(vacío)" for q in quien),
                                    fecha or "(vacía)"))

    V = lee_libro(CONSENSO, SIMPLIFICADOS)
    vacias = sorted(k for k, v in V.items() if not v)
    if vacias:
        raise SystemExit(
            "NO SE INGIERE: quedan %d juicios sin decidir.\n  %s%s"
            % (len(vacias),
               ", ".join("%s %s" % (k[0], k[2]) for k in vacias[:8]),
               " …" if len(vacias) > 8 else ""))

    filas = [{"study_id": s, "instrumento": inst, "item": cod, "valor": v,
              "procedencia": "consenso", "firmado_por": " y ".join(quien),
              "fecha": fecha}
             for (s, inst, cod), v in sorted(V.items())]

    cols = ["study_id", "instrumento", "item", "valor", "procedencia",
            "firmado_por", "fecha"]
    DEST.mkdir(parents=True, exist_ok=True)
    with open(salida_p, "w", encoding="utf-8-sig", newline="") as fh:
        w = csv.DictWriter(fh, cols)
        w.writeheader()
        w.writerows(filas)

    n_items = {i["clave"]: len(i["items"]) for i in SIMPLIFICADOS}
    por_estudio = collections.defaultdict(dict)
    for f in filas:
        por_estudio[(f["study_id"], f["instrumento"])][f["item"]] = f["valor"]
    completos = {k: d["GLOBAL"] for k, d in por_estudio.items()
                 if d.get("GLOBAL")
                 and sum(1 for c, v in d.items() if c != "GLOBAL" and v)
                 >= n_items.get(k[1], 0)}
    S = {
        "modo": "consenso",
        "evaluados": len(completos),
        "a_medias": len(por_estudio) - len(completos),
        "no_evaluables_sin_texto": 1,
        "respuestas_por_acuerdo": 0,
        "respuestas_por_consenso": len(filas),
        "desacuerdos_abiertos": 0,
        "resoluciones_sin_firma": 0,
        "sin_segunda_lectura": 0,
        "firmado_por": " y ".join(quien),
        "fecha": fecha,
        "juicio_global": dict(collections.Counter(completos.values())),
        "evaluados_por_instrumento": dict(
            collections.Counter(inst for _, inst in completos)),
    }
    escalares_p.write_text(json.dumps(S, ensure_ascii=False, indent=2),
                           encoding="utf-8")
    print("escrito %s  (%d juicios, todos por consenso)"
          % (salida_p.relative_to(ROOT), len(filas)))
    print("   acordado por %s el %s" % (" y ".join(quien), fecha))
    print("estudios con juicio completo: %d" % len(completos))
    for j, n in collections.Counter(completos.values()).most_common():
        print("   %-34s %3d" % (j, n))
    print("escrito %s" % escalares_p.relative_to(ROOT))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--a", default=str(DEST / "riesgo_sesgo_danny_valdiviezo.xlsx"))
    ap.add_argument("--b", default=None)
    ap.add_argument("--simplificado", action="store_true",
                    help="los formularios por dominio de los comparativos")
    ap.add_argument("--consenso", action="store_true",
                    help="el cuaderno único acordado entre los dos autores")
    args = ap.parse_args()
    if args.consenso:
        return ingiere_consenso(SALIDA_SIMPLE, ESCALARES_SIMPLE)
    instrumentos = SIMPLIFICADOS if args.simplificado else INSTRUMENTOS
    conflictos_p = CONFLICTOS_SIMPLE if args.simplificado else CONFLICTOS
    salida_p = SALIDA_SIMPLE if args.simplificado else SALIDA
    escalares_p = ESCALARES_SIMPLE if args.simplificado else ESCALARES
    if args.simplificado and args.a == str(DEST / 'riesgo_sesgo_danny_valdiviezo.xlsx'):
        args.a = str(DEST / 'riesgo_sesgo_comparativos_danny_valdiviezo.xlsx')
    if args.b is None:
        args.b = str(DEST / ('riesgo_sesgo_comparativos_nataly_trelles.xlsx'
                             if args.simplificado
                             else 'riesgo_sesgo_nataly_trelles.xlsx'))
    pa, pb = pathlib.Path(args.a), pathlib.Path(args.b)
    for p in (pa, pb):
        if not p.exists():
            raise SystemExit("falta %s. Genéralo con make_rob_forms.py" % p.name)
    A, B = lee_libro(pa, instrumentos), lee_libro(pb, instrumentos)

    firmado, sin_firma = {}, []
    if conflictos_p.exists():
        with open(conflictos_p, encoding="utf-8-sig", newline="") as fh:
            for r in csv.DictReader(fh):
                k = (r["study_id"], r["instrumento"], r["item"])
                res = (r.get("resolucion") or "").strip()
                quien = (r.get("resuelto_por") or "").strip()
                if res and quien:
                    firmado[k] = r
                elif res:
                    # Lo peligroso no es el hueco: es el valor escrito sin
                    # firmar. Parece resuelto y no lo esta.
                    sin_firma.append(k)

    filas, abiertos, sin_pareja = [], [], []
    for k in sorted(set(A) | set(B)):
        s, inst, cod = k
        va, vb = A.get(k, ""), B.get(k, "")
        if not va and not vb:
            continue
        if not va or not vb:
            # Solo contesto uno. No es un desacuerdo que firmar: le falta la
            # segunda lectura, y son cosas distintas.
            sin_pareja.append(k)
            continue
        if va == vb:
            filas.append({"study_id": s, "instrumento": inst, "item": cod,
                          "valor": va, "procedencia": "acuerdo",
                          "firmado_por": "", "fecha": ""})
        elif k in firmado:
            r = firmado[k]
            filas.append({"study_id": s, "instrumento": inst, "item": cod,
                          "valor": r["resolucion"].strip(),
                          "procedencia": "consenso",
                          "firmado_por": r.get("resuelto_por", ""),
                          "fecha": r.get("fecha", "")})
        else:
            abiertos.append(k)

    DEST.mkdir(parents=True, exist_ok=True)
    cols = ["study_id", "instrumento", "item", "valor", "procedencia",
            "firmado_por", "fecha"]
    with open(salida_p, "w", encoding="utf-8-sig", newline="") as fh:
        w = csv.DictWriter(fh, cols)
        w.writeheader()
        w.writerows(filas)

    # ---- escalares -------------------------------------------------------
    # Un estudio cuenta como evaluado solo si tiene TODAS las preguntas de su
    # instrumento resueltas. A medio evaluar no es una categoria de riesgo.
    n_items = {i["clave"]: len(i["items"]) for i in instrumentos}
    por_estudio = collections.defaultdict(dict)
    for f in filas:
        por_estudio[(f["study_id"], f["instrumento"])][f["item"]] = f["valor"]

    completos, parciales = {}, 0
    for (s, inst), d in por_estudio.items():
        respondidas = sum(1 for c, v in d.items() if c != "GLOBAL" and v)
        if respondidas >= n_items.get(inst, 0) and d.get("GLOBAL"):
            completos[(s, inst)] = d["GLOBAL"]
        else:
            parciales += 1

    juicios = collections.Counter(completos.values())
    por_inst = collections.Counter(inst for _, inst in completos)

    S = {
        "evaluados": len(completos),
        "a_medias": parciales,
        "no_evaluables_sin_texto": 24,
        "respuestas_por_acuerdo": sum(1 for f in filas if f["procedencia"] == "acuerdo"),
        "respuestas_por_consenso": sum(1 for f in filas if f["procedencia"] == "consenso"),
        "desacuerdos_abiertos": len(abiertos),
        "resoluciones_sin_firma": len(sin_firma),
        "sin_segunda_lectura": len(sin_pareja),
        "juicio_global": dict(juicios),
        "evaluados_por_instrumento": dict(por_inst),
    }
    escalares_p.write_text(json.dumps(S, ensure_ascii=False, indent=2), encoding="utf-8")

    print("escrito %s  (%d respuestas)" % (salida_p.relative_to(ROOT), len(filas)))
    print("   por acuerdo   %4d" % S["respuestas_por_acuerdo"])
    print("   por consenso  %4d" % S["respuestas_por_consenso"])
    print("   desacuerdos sin firmar   %4d  <- NO entran" % len(abiertos))
    print("   sin segunda lectura      %4d  <- solo contestó uno" % len(sin_pareja))
    if sin_firma:
        print("   %d con valor escrito y SIN FIRMA, no ingeridas:" % len(sin_firma))
        for k in sin_firma[:5]:
            print("      %s %s %s" % k)
    print()
    print("estudios con juicio completo: %d   a medias: %d" % (len(completos), parciales))
    for j, n in juicios.most_common():
        print("   %-34s %3d" % (j, n))
    if not completos:
        print("   (todavía ninguno: los formularios están en blanco)")
    print("escrito %s" % escalares_p.relative_to(ROOT))


if __name__ == "__main__":
    main()
