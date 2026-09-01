"""Qué reporta de verdad el corpus en cada desenlace, sobre la extracción adjudicada.

POR QUÉ ESTE SCRIPT EXISTE

Hasta ahora ninguna cifra del manuscrito dependía de los cuadernos de
extracción: todas salían del cribado y de la pre-extracción desde resúmenes,
porque los desacuerdos entre los dos revisores no estaban resueltos. Ya lo
están, así que por primera vez se puede mirar lo que la extracción dice de los
cinco desenlaces declarados en los criterios de elegibilidad.

QUÉ MIDE, Y QUÉ NO

Mide **completitud de reporte**: en cuántos brazos consta cada desenlace con su
denominador. No estima eficacia. La diferencia no es de prudencia, es de
aritmética: un numerador sin denominador no es una proporción, y una proporción
cuyo numerador cada estudio define a su manera no se puede promediar con las
demás.

Por eso el fichero informa, junto a cada desenlace, cuántos brazos lo reportan
**y** cuántos definen el éxito clínico de forma operativa. Si la segunda cifra
es baja, la primera no habilita una síntesis: habilita describir un problema.

CADA CIFRA LLEVA SU DOBLE LECTURA

`extraccion_adjudicada_procedencia.csv` dice, casilla a casilla, si el valor lo
acordaron los dos revisores, lo resolvieron por consenso, lo escribió uno solo,
o sigue abierto. Toda cifra que salga de aquí se acompaña del porcentaje de sus
casillas que tuvieron doble lectura. Una completitud del 73 % calculada sobre
casillas que leyó una sola persona no es lo mismo que sobre casillas leídas por
dos, y el lector tiene que poder distinguirlas.

Salida:
    quality_reports/outcome_scalars.json

Uso:
    python scripts/build_outcome_scalars.py
"""
import collections
import csv
import json
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from extraction_schema import CATEGORICOS, normaliza  # noqa: E402

ROOT = pathlib.Path(__file__).resolve().parent.parent
EXTR = ROOT / "revision_sistematica" / "extraccion"
DATOS = EXTR / "extraccion_adjudicada.csv"
PROCED = EXTR / "extraccion_adjudicada_procedencia.csv"
SALIDA = ROOT / "quality_reports" / "outcome_scalars.json"

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

DESENLACES = [
    ("clinical_success_n", "éxito clínico"),
    ("microbio_eradication_n", "erradicación microbiológica"),
    ("mortality_n", "mortalidad"),
    ("adverse_event_n", "eventos adversos"),
    ("resistance_emergence_n", "emergencia de resistencia al fago"),
]

# Los diseños que permiten comparar. Sin uno de estos no hay grupo de control y
# ningun desenlace agregado responde a «comparado con que».
COMPARATIVOS = {"RCT", "non-randomised trial",
                "prospective cohort", "retrospective cohort"}

DOBLE = {"acuerdo", "consenso"}


def es_numero(v):
    v = (v or "").strip()
    return v.replace(".", "", 1).isdigit()


def main():
    if not DATOS.exists():
        print("no existe %s. Corre build_adjudicated_dataset.py antes." % DATOS.name)
        return 1
    filas = list(csv.DictReader(open(DATOS, encoding="utf-8")))
    proc = {(r["study_id"], r["arm_id"]): r
            for r in csv.DictReader(open(PROCED, encoding="utf-8"))}

    S = {}
    S["brazos"] = len(filas)
    S["estudios_extraidos"] = len({r["study_id"] for r in filas})
    con_n = [r for r in filas if es_numero(r.get("n_arm"))]
    S["brazos_con_denominador"] = len(con_n)

    # ---- completitud por desenlace ----------------------------------------
    S["desenlaces"] = {}
    for campo, nombre in DESENLACES:
        tiene = [r for r in filas if es_numero(r.get(campo))]
        usable = [r for r in tiene if es_numero(r.get("n_arm"))]
        dobles = sum(1 for r in usable
                     if proc.get((r["study_id"], r["arm_id"]), {}).get(campo) in DOBLE)
        S["desenlaces"][campo] = {
            "nombre": nombre,
            "brazos_que_lo_reportan": len(tiene),
            "con_numerador_y_denominador": len(usable),
            "pct_de_los_brazos": round(100.0 * len(usable) / max(1, len(filas)), 1),
            "de_esos_con_doble_lectura": dobles,
            "doble_lectura_pct": round(100.0 * dobles / max(1, len(usable)), 1),
        }

    # ---- la definicion de exito clinico ------------------------------------
    # El desenlace que las sintesis publicadas agregan es «exito clinico». Si
    # el estudio no lo define, el numerador no nombra nada comparable, y
    # promediarlo con los demas produce una cifra sin referente.
    #
    # «na» NO es una definicion: es el token de dato ausente que declara
    # extraction_schema, y los dos revisores lo escribieron por separado en 20
    # brazos. Contarlo como definicion rebajaba la cifra publicada del 67,4 %
    # al 52,3 %, o sea en la direccion que ablanda el hallazgo.
    SIN = ("SIN DEFINICION OPERATIVA", "SIN DEFINICI\u00d3N OPERATIVA")
    AUSENTE = {"NA", "N/A", "NR", "ND", "-"}

    def sin_definicion(v):
        t = (v or "").strip()
        return (not t) or t.upper() in AUSENTE or any(x in t.upper() for x in SIN)

    # Un brazo cuya extraccion quedo incompleta no permite afirmar que el
    # articulo no define nada: permite afirmar que no se establecio. Son cosas
    # distintas y el manuscrito no puede confundirlas.
    declarada = ausente = incompleta = definidos = 0
    for r in filas:
        t = (r.get("clinical_success_definition") or "").strip()
        inc = (r.get("extraction_status") or "").strip().upper() == "EXTRACTION_INCOMPLETE"
        if not sin_definicion(t):
            definidos += 1
        elif inc:
            incompleta += 1
        elif t and any(x in t.upper() for x in SIN):
            declarada += 1
        else:
            ausente += 1
    sin_def = declarada + ausente + incompleta
    S["definicion_exito"] = {
        "brazos": len(filas),
        "con_definicion_operativa": definidos,
        "sin_definicion_declarada": declarada,
        "campo_ausente": ausente,
        "extraccion_incompleta": incompleta,
        "sin_definicion_operativa": sin_def,
        "sin_definicion_pct": round(100.0 * sin_def / max(1, len(filas)), 1),
        "establecido_que_no_define": declarada + ausente,
        "establecido_pct": round(100.0 * (declarada + ausente) / max(1, len(filas)), 1),
    }

    # ---- aritmetica imposible ----------------------------------------------
    # Un numerador mayor que su denominador no es un dato: es un error que
    # exige volver al articulo. Se cuenta y se nombra en vez de sumarlo a la
    # completitud como si fuera una proporcion valida.
    imposibles = []
    for r in filas:
        N = r.get("n_arm")
        if not es_numero(N):
            continue
        for campo, _ in DESENLACES:
            if es_numero(r.get(campo)) and float(r[campo]) > float(N):
                imposibles.append("%s %s=%s sobre n=%s"
                                  % (r["study_id"], campo, r[campo], N))
    S["aritmetica_imposible"] = len(imposibles)
    S["aritmetica_imposible_detalle"] = imposibles

    # ---- disenos, sobre la extraccion adjudicada ---------------------------
    dis = collections.Counter()
    for r in filas:
        v = normaliza("study_design", r.get("study_design"))
        dis[v if v in CATEGORICOS["study_design"] else "no clasificable"] += 1
    S["disenos"] = dict(sorted(dis.items(), key=lambda kv: (-kv[1], kv[0])))
    S["diseno_no_clasificable"] = dis["no clasificable"]
    S["brazos_con_diseno"] = len(filas) - dis["no clasificable"]
    comp = [r for r in filas
            if normaliza("study_design", r.get("study_design")) in COMPARATIVOS]
    S["brazos_comparativos"] = len(comp)
    S["estudios_comparativos_extraidos"] = len({r["study_id"] for r in comp})

    # El cruce que decide si se puede agregar algo: brazos que a la vez son
    # comparativos, traen numerador y denominador coherentes, y definen el
    # desenlace. Usa el MISMO predicado que arriba; antes solo acertaba por
    # accidente, porque los brazos con «na» no traian numerador.
    agregables = [
        r for r in comp
        if es_numero(r.get("clinical_success_n")) and es_numero(r.get("n_arm"))
        and float(r["clinical_success_n"]) <= float(r["n_arm"])
        and not sin_definicion(r.get("clinical_success_definition"))]
    S["brazos_agregables_exito_clinico"] = len(agregables)
    S["estudios_agregables_exito_clinico"] = len({r["study_id"] for r in agregables})
    S["agregables_detalle"] = [
        {"study_id": r["study_id"], "arm_id": r["arm_id"],
         "diseno": normaliza("study_design", r.get("study_design")),
         "n": r["clinical_success_n"], "N": r["n_arm"],
         "definicion": (r.get("clinical_success_definition") or "")[:160]}
        for r in agregables]

    SALIDA.write_text(json.dumps(S, indent=2, ensure_ascii=False), encoding="utf-8")

    print("escrito %s" % SALIDA.name)
    print("  %d brazos, %d estudios, %d con denominador"
          % (S["brazos"], S["estudios_extraidos"], S["brazos_con_denominador"]))
    print()
    print("  %-34s %6s %7s %9s" % ("desenlace", "n+N", "% brazos", "doble lect."))
    for campo, _ in DESENLACES:
        d = S["desenlaces"][campo]
        print("  %-34s %6d %6.1f %% %7.1f %%"
              % (d["nombre"], d["con_numerador_y_denominador"],
                 d["pct_de_los_brazos"], d["doble_lectura_pct"]))
    e = S["definicion_exito"]
    print()
    print("  definición de éxito clínico, sobre %d brazos:" % e["brazos"])
    print("    con definición operativa            %3d" % e["con_definicion_operativa"])
    print("    el artículo no la da                %3d" % e["sin_definicion_declarada"])
    print("    el campo salió ausente («na»)       %3d" % e["campo_ausente"])
    print("    extracción incompleta, no consta    %3d" % e["extraccion_incompleta"])
    print("    -> SIN definición operativa         %3d  (%.1f %%)"
          % (e["sin_definicion_operativa"], e["sin_definicion_pct"]))
    if S["aritmetica_imposible"]:
        print()
        print("  ARITMÉTICA IMPOSIBLE (numerador > denominador): %d"
              % S["aritmetica_imposible"])
        for x in S["aritmetica_imposible_detalle"]:
            print("    %s" % x)
    print()
    print("  diseños:", ", ".join("%s %d" % (k, v) for k, v in S["disenos"].items()))
    print("  %d brazos con diseño clasificable; %d sin él"
          % (S["brazos_con_diseno"], S["diseno_no_clasificable"]))
    print("  brazos comparativos: %d, en %d estudios"
          % (S["brazos_comparativos"], S["estudios_comparativos_extraidos"]))
    print()
    print("  BRAZOS QUE REÚNEN LOS CUATRO REQUISITOS: %d"
          % S["brazos_agregables_exito_clinico"])
    for a in S["agregables_detalle"]:
        print("    %-9s %-22s %s/%s  %s"
              % (a["study_id"], a["diseno"], a["n"], a["N"], a["definicion"][:52]))
    return 0


if __name__ == "__main__":
    sys.exit(main())
