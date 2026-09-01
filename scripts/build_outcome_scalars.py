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

# Los diseños que, POR SU ETIQUETA, incluyen un grupo de comparacion. El filtro
# mira lo que el estudio ES, no lo que hay en este conjunto: el formulario se
# rellena por brazo y los revisores extrajeron el brazo de fago, asi que de los
# 24 brazos comparativos solo 5 pertenecen a un estudio con mas de un brazo
# extraido, y ninguno de los tres agregables tiene aqui su comparador.
#
# Para una proporcion de un solo brazo eso basta --una proporcion no necesita
# control--, pero no basta para nada que se llame «comparado con que». Se
# declara en la nota de la tabla 5 en vez de dejar que la etiqueta prometa mas
# de lo que el fichero contiene.
# «Comparativo» significaba DOS cosas en el mismo articulo: la Tabla 1 y la
# 3.3 contaban solo ensayos (23 estudios) y la Tabla 5 contaba ademas cohortes
# (24 brazos). Un lector que ve 23 y 24 supone que son el mismo conjunto, y no
# lo son: 13 son ensayos y 11 son cohortes. Se separan los dos sentidos y se
# publican los dos, con su nombre.
ENSAYOS = {"RCT", "non-randomised trial"}
COHORTES = {"prospective cohort", "retrospective cohort"}
COMPARATIVOS = ENSAYOS | COHORTES

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

    # Un brazo de un estudio sin texto completo no pudo extraerse. Contarlo
    # como «no reporta el desenlace» confunde el silencio del articulo con
    # nuestro propio hueco documental.
    s5f = sorted((ROOT / "verificables revisión sistemática").glob(
        "S5_listado_*_estudios.csv"))
    tiene_texto = {}
    if s5f:
        for r in csv.DictReader(open(s5f[0], encoding="utf-8-sig")):
            tiene_texto[r["id"]] = r["texto_completo"].strip().lower().startswith(("s", "y"))
    legibles = [r for r in filas if tiene_texto.get(r["study_id"], False)]

    S = {}
    S["brazos"] = len(filas)
    S["brazos_legibles"] = len(legibles)
    S["brazos_sin_texto_completo"] = len(filas) - len(legibles)
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
        leg = [r for r in usable if tiene_texto.get(r["study_id"], False)]
        S["desenlaces"][campo] = {
            "nombre": nombre,
            "brazos_que_lo_reportan": len(tiene),
            "con_numerador_y_denominador": len(usable),
            "pct_de_los_brazos": round(100.0 * len(usable) / max(1, len(filas)), 1),
            # El mismo recuento sobre los brazos que SI se pudieron leer. La
            # diferencia entre los dos porcentajes es el hueco documental, no
            # el silencio de la literatura.
            "en_brazos_legibles": len(leg),
            "pct_de_los_legibles": round(100.0 * len(leg) / max(1, len(legibles)), 1),
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
        # Las otras cinco filas de la Tabla 5 llevan doble denominador y esta
        # no lo llevaba, siendo la que sostiene el hallazgo. Sobre los brazos
        # que si se pudieron leer la cifra baja del 67,4 % al 58,4 %.
        "sin_definicion_en_legibles": sum(
            1 for r in legibles if sin_definicion(r.get("clinical_success_definition"))),
        "sin_definicion_legibles_pct": round(
            100.0 * sum(1 for r in legibles
                        if sin_definicion(r.get("clinical_success_definition")))
            / max(1, len(legibles)), 1),
    }

    # ---- lo que el formulario nunca llego a preguntar -----------------------
    # `microbio_eradication_denom` y `microbio_eradication_sustained` estan en el
    # esquema y NO en los cuadernos: se anadieron despues de repartirlos. Sin el
    # primero, la fila de erradicacion usa n_arm como denominador, que
    # sobreestima --no a todos los pacientes se les hace cultivo de control--.
    # Se declara aqui para que la tabla pueda decirlo.
    presentes = set()
    for r in filas:
        presentes |= {k for k, v in r.items() if (v or "").strip()}
    S["campos_del_esquema_no_extraidos"] = sorted(
        c for c in ("microbio_eradication_denom", "microbio_eradication_sustained")
        if c not in presentes)

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
    # «No clasificable» junta dos situaciones distintas: un «NA» que los dos
    # revisores acordaron --el articulo no permite reconocer el diseño-- y una
    # casilla que sigue abierta --no lo hemos resuelto--. La primera habla del
    # articulo; la segunda, de nosotros.
    acordado_na = abierto = 0
    for r in filas:
        v = normaliza("study_design", r.get("study_design"))
        if v in CATEGORICOS["study_design"]:
            continue
        if proc.get((r["study_id"], r["arm_id"]), {}).get("study_design") == "ABIERTO":
            abierto += 1
        else:
            acordado_na += 1
    S["diseno_na_acordado"] = acordado_na
    S["diseno_abierto"] = abierto
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
    # ---- EL EMBUDO, con los criterios de 2.2 --------------------------------
    # Cada paso quita brazos por una razon nombrada, y el fichero guarda cuantos
    # quedan tras cada uno. Los dos ultimos filtros los trajeron los arbitros:
    # un desenlace que el articulo no separa por patogeno no es atribuible a
    # P. aeruginosa, y un estudio de profilaxis no mide lo mismo que uno de
    # tratamiento. Ninguno de los dos es un juicio de este script: el primero
    # sale de lo que los revisores anotaron, el segundo del titulo del articulo.
    import re as _re
    s5t = {}
    if s5f:
        for r in csv.DictReader(open(s5f[0], encoding="utf-8-sig")):
            s5t[r["id"]] = r.get("titulo", "")

    def separable(r):
        return "no separa" not in (r.get("incomplete_reason") or "").lower()

    def terapeutica(r):
        return not _re.search(r"\bprevent|\bprophyla|\bprofilax",
                              s5t.get(r["study_id"], ""), _re.I)

    paso = []
    c = filas
    paso.append(("brazos extraídos", len(c)))
    c = [r for r in c if normaliza("study_design", r.get("study_design")) in COMPARATIVOS]
    paso.append(("diseño comparativo", len(c)))
    c = [r for r in c if es_numero(r.get("clinical_success_n"))
         and es_numero(r.get("n_arm"))
         and float(r["clinical_success_n"]) <= float(r["n_arm"])]
    paso.append(("numerador y denominador coherentes", len(c)))
    c = [r for r in c if not sin_definicion(r.get("clinical_success_definition"))]
    paso.append(("definición operativa del éxito", len(c)))
    c = [r for r in c if separable(r)]
    paso.append(("desenlace atribuible a P. aeruginosa", len(c)))
    c = [r for r in c if terapeutica(r)]
    paso.append(("administración terapéutica, no profiláctica", len(c)))
    # El ultimo paso no es automatico: que un desenlace principal sea un tiempo
    # y no una proporcion se lee en el articulo, no en una casilla. PhagoBurn
    # (EST-021) lo es, y esta citado en 3.6.
    TIEMPO = {"EST-021"}
    c = [r for r in c if r["study_id"] not in TIEMPO]
    paso.append(("reporta una proporción, no un tiempo", len(c)))

    S["embudo"] = [{"filtro": k, "quedan": v} for k, v in paso]
    S["brazos_agregables_final"] = len(c)
    S["brazos_agregables_final_ids"] = [r["study_id"] for r in c]
    S["brazos_ensayo"] = sum(
        1 for r in filas
        if normaliza("study_design", r.get("study_design")) in ENSAYOS)
    S["brazos_cohorte"] = sum(
        1 for r in filas
        if normaliza("study_design", r.get("study_design")) in COHORTES)

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
    print("  %-34s %6s %9s %11s %9s"
          % ("desenlace", "n+N", "% de 132", "%% de %d leg." % len(legibles),
             "doble lect."))
    for campo, _ in DESENLACES:
        d = S["desenlaces"][campo]
        print("  %-34s %6d %8.1f %% %10.1f %% %7.1f %%"
              % (d["nombre"], d["con_numerador_y_denominador"],
                 d["pct_de_los_brazos"], d["pct_de_los_legibles"],
                 d["doble_lectura_pct"]))
    if S["campos_del_esquema_no_extraidos"]:
        print()
        print("  CAMPOS DEL ESQUEMA QUE NUNCA SE EXTRAJERON: %s"
              % ", ".join(S["campos_del_esquema_no_extraidos"]))
        print("    -> la fila de erradicación usa n_arm como denominador")
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
    print("  %d brazos con diseño clasificable; %d sin él (%d «NA» acordado, "
          "%d abiertos)"
          % (S["brazos_con_diseno"], S["diseno_no_clasificable"],
             S["diseno_na_acordado"], S["diseno_abierto"]))
    print("  brazos comparativos: %d, en %d estudios"
          % (S["brazos_comparativos"], S["estudios_comparativos_extraidos"]))
    print()
    print("  EL EMBUDO, con los criterios de §2.2")
    for x in S["embudo"]:
        print("    %-44s %3d" % (x["filtro"], x["quedan"]))
    print()
    print("  BRAZOS QUE REÚNEN LOS CUATRO REQUISITOS: %d"
          % S["brazos_agregables_exito_clinico"])
    for a in S["agregables_detalle"]:
        print("    %-9s %-22s %s/%s  %s"
              % (a["study_id"], a["diseno"], a["n"], a["N"], a["definicion"][:52]))
    return 0


if __name__ == "__main__":
    sys.exit(main())
