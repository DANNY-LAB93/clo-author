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
MANUSCRITO = ROOT / "paper" / "manuscrito_JSR_final.md"

# El bloque del manuscrito que este guion posee, delimitado por su encabezado y
# por el pie de la Tabla 5. Lo de en medio se reescribe entero; el pie y todo lo
# que viene despues no se tocan.
MARCA_INI = "### Riesgo de sesgo"
MARCA_FIN = "**Tabla 5.**"

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
            titulo[(inst["clave"], it["codigo"], "en")] = it["texto_en"]
    return orden, titulo


def juicios():
    """{(estudio, instrumento, item): valor} de lo adjudicado, si lo hay."""
    if not ADJUDICADO.exists():
        return {}
    with open(ADJUDICADO, encoding="utf-8-sig", newline="") as fh:
        return {(r["study_id"], r["instrumento"], r["item"]): r["valor"].strip()
                for r in csv.DictReader(fh) if r["valor"].strip()}


def procedencias():
    """Cuántos juicios salieron por acuerdo y cuántos por consenso firmado."""
    if not ADJUDICADO.exists():
        return collections.Counter()
    with open(ADJUDICADO, encoding="utf-8-sig", newline="") as fh:
        return collections.Counter(r["procedencia"].strip()
                                   for r in csv.DictReader(fh)
                                   if r["valor"].strip())


# NINGUNA CIFRA TECLEADA AQUI. La version anterior llevaba tres dentro del
# texto --«El duodécimo», «los 11 ensayos» y «los 71 con texto obtenido»-- y
# las tres se volvieron falsas el mismo dia, al cambiar la regla de diseño por
# estudio. Ahora todas entran por el diccionario que arma `main()`.
ALCANCE = (
    "El diseño adjudicado sobre el artículo identifica **%(comp)d estudios con "
    "grupo de comparación**, de los cuales **%(ev)d son evaluables**: %(rob2)d "
    "ensayos aleatorizados con RoB 2 y %(robins)d ensayos no aleatorizados y "
    "cohortes con ROBINS-I. %(sin_texto_frase)s; no reciben un juicio de riesgo "
    "alto por esa razón, porque no evaluar y evaluar mal no son lo mismo. Ese "
    "conjunto de %(ev)d estudios no es el mismo que los %(t2)d ensayos que "
    "cuenta la Tabla 2: aquella clasifica por lo que el resumen declara sobre "
    "los %(extraibles)d estudios recuperables y no incluye las cohortes, "
    "mientras que esta evaluación clasifica por lo que se leyó en el artículo "
    "de los %(con_texto)d con texto obtenido y sí las incluye. La Tabla 5 lleva "
    "%(celdas)d juicios de dominio%(recoge)s.")

AVISO = (
    "**[PENDIENTE — no enviar el manuscrito con esta nota. Los %d juicios de "
    "dominio de los %d estudios comparativos aún no han sido emitidos por los "
    "dos revisores. La Tabla 5 y el párrafo que la resume se generan desde la "
    "evaluación adjudicada en cuanto lo estén.]**")

# El orden va de menos a mas riesgo. Se usa para decir cual es el dominio que
# concentra los juicios desfavorables sin tener que elegirlo a mano.
GRAVEDAD = {
    "Bajo riesgo de sesgo": 0, "Algunas preocupaciones": 1,
    "Riesgo moderado": 1, "Alto riesgo de sesgo": 2, "Riesgo grave": 2,
    "Riesgo crítico": 3, "Sin información para juzgar": 1,
}


# Como se nombra cada juicio dentro de la frase. El nombre literal del
# instrumento ("Bajo riesgo de sesgo") no encaja en una enumeracion.
EN_PROSA = {
    "Bajo riesgo de sesgo": "de bajo riesgo",
    "Algunas preocupaciones": "de algunas preocupaciones",
    "Alto riesgo de sesgo": "de alto riesgo",
    "Riesgo moderado": "de riesgo moderado",
    "Riesgo grave": "de riesgo grave",
    "Riesgo crítico": "de riesgo crítico",
    "Sin información para juzgar": "sin información para juzgar",
}


def _enumera(trozos, y=" y "):
    """['a', 'b', 'c'] -> 'a, b y c'. El conector tambien tiene idioma."""
    if len(trozos) == 1:
        return trozos[0]
    return ", ".join(trozos[:-1]) + y + trozos[-1]


EN_PROSA_EN = {
    "Bajo riesgo de sesgo": "low risk",
    "Algunas preocupaciones": "some concerns",
    "Alto riesgo de sesgo": "high risk",
    "Riesgo moderado": "moderate risk",
    "Riesgo grave": "serious risk",
    "Riesgo crítico": "critical risk",
    "Sin información para juzgar": "no information",
}

FRASES = {
    "es": {"global": "De los %d estudios evaluados con %s, el juicio global es %s.",
           "en_n": "%s en %d",
           "peor": "El dominio que más juicios desfavorables concentra en %s%s es «%s», con %d de %d.",
           "coletilla": " —alto riesgo en RoB 2; grave o crítico en ROBINS-I—",
           "consenso": ("Los %d juicios se emitieron en una evaluación única acordada "
                        "entre los dos autores; al no haber dos lecturas independientes, "
                        "no se reporta concordancia entre revisores."),
           "duplicado": ("Los dos revisores coincidieron en %d de los %d juicios y "
                         "resolvieron los %d restantes por consenso.")},
    "en": {"global": "Of the %d studies assessed with %s, the overall judgement is %s.",
           "en_n": "%s in %d",
           "peor": "The domain concentrating most unfavourable judgements%s in %s is “%s”, in %d of %d.",
           "coletilla": " —high risk under RoB 2; serious or critical under ROBINS-I—",
           "consenso": ("The %d judgements were issued in a single assessment agreed "
                        "between the two authors; with no two independent readings, no "
                        "inter-reviewer agreement is reported."),
           "duplicado": ("The two reviewers agreed on %d of the %d judgements and "
                         "resolved the remaining %d by consensus.")},
}


def resumen_prosa(evaluables, orden, titulo, J, proc, idioma="es"):
    """El párrafo de Resultados, escrito desde los juicios adjudicados.

    No se redacta a mano en el manuscrito por la misma razón que el resto de las
    cifras: si mañana se readjudica un dominio, la prosa tiene que moverse con
    él o deja de ser verdad. Los juicios se enumeran de menor a mayor riesgo,
    que es el orden en que los define el instrumento, y no por frecuencia.
    """
    F = FRASES[idioma]
    ETQ = EN_PROSA if idioma == "es" else EN_PROSA_EN
    frases, dicho_desfavorable = [], False
    for clave, nombre in (("rob2", "RoB 2"), ("robins", "ROBINS-I")):
        estudios = [c for c in evaluables if c["instrumento"] == clave]
        if not estudios:
            continue
        glob = collections.Counter(
            J.get((c["study_id"], clave, "GLOBAL"), "") for c in estudios)
        glob.pop("", None)
        if not glob:
            continue
        ordenados = sorted(glob.items(), key=lambda kv: GRAVEDAD.get(kv[0], 9))
        frases.append(F["global"] % (len(estudios), nombre,
                      _enumera([F["en_n"] % (ETQ.get(j, j), n)
                                for j, n in ordenados],
                               " y " if idioma == "es" else " and ")))
        # El dominio que mas peso tiene en ese juicio, dicho por su nombre.
        peor, peor_n = None, 0
        for cod in orden[clave]:
            n = sum(1 for c in estudios
                    if GRAVEDAD.get(J.get((c["study_id"], clave, cod), ""), 0) >= 2)
            if n > peor_n:
                peor_n = n
                peor = titulo[(clave, cod) if idioma == "es"
                              else (clave, cod, "en")]
        if peor and peor_n:
            # La aclaracion de que cuenta como desfavorable se da UNA vez, la
            # primera; repetirla en el segundo instrumento sobra.
            coletilla = "" if dicho_desfavorable else F["coletilla"]
            dicho_desfavorable = True
            orden_args = ((nombre, coletilla) if idioma == "es"
                          else (coletilla, nombre))
            frases.append(F["peor"] % (orden_args[0], orden_args[1],
                                       peor[0].lower() + peor[1:],
                                       peor_n, len(estudios)))
    ac, co = proc.get("acuerdo", 0), proc.get("consenso", 0)
    if co and not ac:
        # Ruta de consenso: un solo cuaderno acordado. Decir aqui "coincidieron
        # en 0 y resolvieron 82 por consenso" seria describir una doble lectura
        # que no existio. La ausencia de concordancia entre revisores no se
        # disimula: se enuncia, y Limitaciones la recoge.
        frases.append(F["consenso"] % co)
    elif ac or co:
        frases.append(F["duplicado"] % (ac, ac + co, co))
    return " ".join(frases)


def escribe_manuscrito(estado, evaluables, orden, titulo, J):
    """Deja el bloque de Resultados diciendo lo que los ficheros sostienen.

    Se escribe SIEMPRE, esté completa la evaluación o no: mientras falte un
    juicio deja el aviso, y en cuanto no falte ninguno lo sustituye por el
    párrafo de resultados. Así el manuscrito no puede quedarse afirmando una
    evaluación que no existe ni arrastrando un aviso que ya sobra.
    """
    if not MANUSCRITO.exists():
        return
    s = MANUSCRITO.read_text(encoding="utf-8")
    ini, fin = s.find(MARCA_INI), s.find(MARCA_FIN)
    if ini < 0 or fin < 0 or fin < ini:
        print("AVISO: no encuentro el bloque de riesgo de sesgo en %s; "
              "la tabla se escribió, el manuscrito no." % MANUSCRITO.name)
        return
    import json as _json
    _S = _json.loads((ROOT / "quality_reports" / "synthesis_scalars.json")
                     .read_text(encoding="utf-8"))
    _n = estado["sin_texto_completo"]
    _ids = ", ".join(estado.get("sin_texto_completo_ids", []))
    if _n == 1:
        _frase = ("El restante no tiene texto completo y no se evalúa (%s)" % _ids)
    else:
        _frase = ("Los %d restantes no tienen texto completo y no se evalúan "
                  "(%s)" % (_n, _ids))
    alcance = ALCANCE % {"comp": estado["comparativos_adjudicados"],
                         "ev": estado["evaluables"],
                         "celdas": estado["celdas_totales"],
                         "recoge": ("" if estado["completa"]
                                    else ", todavía sin emitir"),
                         "rob2": estado["por_instrumento"].get("RoB 2", 0),
                         "robins": estado["por_instrumento"].get("ROBINS-I", 0),
                         "sin_texto_frase": _frase,
                         "t2": _S["estudios_comparativos"],
                         "extraibles": _S["estudios_extraibles"],
                         "con_texto": _S["texto_completo_obtenido"]}
    if estado["completa"]:
        segundo = resumen_prosa(evaluables, orden, titulo, J,
                                procedencias())
    else:
        segundo = AVISO % (estado["celdas_pendientes"], estado["evaluables"])
    nuevo = "%s\n\n%s\n\n%s\n\n" % (MARCA_INI, alcance, segundo)
    MANUSCRITO.write_text(s[:ini] + nuevo + s[fin:], encoding="utf-8")
    print("bloque de riesgo de sesgo reescrito en %s (%s)"
          % (MANUSCRITO.name, "resultados" if estado["completa"] else "aviso"))
    escribe_otros(estado)


def escribe_seccion_37(estado, evaluables, orden, titulo, J, proc):
    """La §3.7 del maestro y de su traducción: existe solo si hay juicios.

    Los Resultados del maestro acababan en 3.6, sin riesgo de sesgo en ninguna
    parte. Al completarse la evaluación, la §2.7 y el ítem 18 de la lista PRISMA
    empezaron los dos a remitir a una «sección 3.7» inexistente. Se escribe
    cuando hay algo que reportar y se retira cuando no: una sección de
    resultados vacía contradiría a la §2.7, que dice que la revisión no reporta
    riesgo de sesgo mientras falte un juicio.
    """
    import rob_bloques as RB
    prosa = resumen_prosa(evaluables, orden, titulo, J, proc)
    ctx = {"ev": estado["evaluables"], "celdas": estado["celdas_totales"],
           "prosa": prosa,
           "prosa_en": resumen_prosa(evaluables, orden, titulo, J, proc, "en")}
    for rel, marca, plantilla in RB.SEC37:
        p = ROOT / rel
        if not p.exists():
            continue
        s = p.read_text(encoding="utf-8")
        cab = plantilla.split("\n", 1)[0]
        # Se retira la que hubiera, y se vuelve a poner si toca. Asi el guion
        # es idempotente y el paso de HECHO a PENDIENTE tambien limpia.
        i = s.find(cab)
        if i >= 0:
            j = s.find(marca, i)
            if j > i:
                s = s[:i] + s[j:]
        if estado["completa"]:
            j = s.find(marca)
            if j < 0:
                print("AVISO: no encuentro «%s» en %s" % (marca, p.name))
                continue
            s = s[:j] + (plantilla % ctx) + s[j:]
        p.write_text(s, encoding="utf-8")
        print("   §3.7 %s en %s" % ("escrita" if estado["completa"] else "retirada",
                                    p.name))


def reconcilia_escalares(estado):
    """Los escalares del consenso no pueden decir mas que el CSV adjudicado.

    El 5 de septiembre un ensayo dejo `rob_comparativos_scalars.json` con 82
    juicios y la firma "PRUEBA A y PRUEBA B", y ese fichero se commiteo: el CSV
    del que sale estaba vacio y nadie lo comprobaba. Un fichero derivado que
    sobrevive a sus datos es peor que uno que falta, porque parece bueno.
    """
    esc = ROOT / "quality_reports" / "rob_comparativos_scalars.json"
    if not esc.exists():
        return
    try:
        S = json.loads(esc.read_text(encoding="utf-8"))
    except ValueError:
        return
    dice = int(S.get("respuestas_por_acuerdo", 0) or 0) +         int(S.get("respuestas_por_consenso", 0) or 0)
    if dice <= estado["celdas_con_juicio"]:
        return
    esc.write_text(json.dumps({
        "modo": "sin evaluar",
        "evaluados": 0,
        "celdas_con_juicio": estado["celdas_con_juicio"],
        "celdas_pendientes": estado["celdas_pendientes"],
        "nota": ("Regenerado por build_rob_table.py: el fichero afirmaba %d "
                 "juicios que el CSV adjudicado no tiene. Lo escribe "
                 "ingest_rob.py cuando hay evaluación firmada." % dice),
    }, ensure_ascii=False, indent=2), encoding="utf-8")
    print("AVISO: %s afirmaba %d juicios y el CSV tiene %d. Regenerado."
          % (esc.name, dice, estado["celdas_con_juicio"]))


def escribe_otros(estado):
    """El maestro y su traducción dicen lo mismo, y cambian a la vez.

    Se quedaron atrás una vez: el de la revista ya declaraba una evaluación por
    consenso en curso y estos dos seguían diciendo que no se había hecho
    ninguna. Los tres viajan en el mismo sobre.
    """
    import rob_bloques as RB
    ctx = {"comp": estado["comparativos_adjudicados"],
           "ev": estado["evaluables"],
           "celdas": estado["celdas_totales"],
           "faltan": estado["celdas_pendientes"],
           "brazos": 103}
    # Metodos del propio manuscrito de la revista: mismo mecanismo.
    met = ROOT / "paper" / "manuscrito_JSR_final.md"
    s = met.read_text(encoding="utf-8")
    i, j = s.find(RB.JSR_MET_INI), s.find(RB.JSR_MET_FIN)
    if i >= 0 and j > i:
        cuerpo = (RB.JSR_MET % dict(
            ctx, estado=(RB.JSR_MET_HECHO if estado["completa"]
                         else RB.JSR_MET_PENDIENTE % ctx)))
        met.write_text(s[:i] + RB.JSR_MET_INI + "\n\n" + cuerpo + "\n\n" + s[j:],
                       encoding="utf-8")
        print("   Métodos de %s" % met.name)
    else:
        print("AVISO: no encuentro el bloque de Métodos en %s" % met.name)

    for rel, ini, fin, comun, pendiente, hecho in RB.BLOQUES:
        p = ROOT / rel
        if not p.exists():
            continue
        s = p.read_text(encoding="utf-8")
        i, j = s.find(ini), s.find(fin)
        if i < 0 or j < 0 or j < i:
            print("AVISO: no encuentro el bloque 2.7 en %s" % p.name)
            continue
        cuerpo = (comun + (hecho if estado["completa"] else pendiente)) % ctx
        s = s[:i] + "%s\n\n%s\n\n" % (ini, cuerpo) + s[j:]
        for rel2, viejo, nuevo in RB.LIMITACION:
            if rel2 == rel and viejo in s:
                s = s.replace(viejo, nuevo, 1)
        p.write_text(s, encoding="utf-8")
        print("   y en %s" % p.name)


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

    proc = procedencias()
    estado = {
        # Como se emitieron los juicios. El manuscrito y el resumen redactan
        # distinto segun esto, y no puede deducirse del numero de celdas.
        "modo": ("consenso" if proc.get("consenso") and not proc.get("acuerdo")
                 else "duplicado"),
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
    reconcilia_escalares(estado)
    escribe_manuscrito(estado, evaluables, orden, titulo, J)
    escribe_seccion_37(estado, evaluables, orden, titulo, J, proc)

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
