# -*- coding: utf-8 -*-
"""Los escalares que la auditoría del 2026-09-16 obligó a medir.

POR QUE VAN APARTE Y LUEGO SE FUNDEN. `build_synthesis_scalars.py` describe el
corpus. Estas cifras describen lo que la auditoría encontró *dentro* de él: el
embudo de la proporción agrupada sin el filtro de diseño comparativo, cuántos
brazos tienen comparador extraído, qué dice el artículo cuando el resumen
calla, y de cuántas fuentes depende cada estudio incluido. Se calculan aquí,
se escriben en el mismo `synthesis_scalars.json` y así el comprobador de
afirmaciones puede anclarlas sin cambiar de fichero.

El script es idempotente: vuelve a calcular todo cada vez y no acumula.

SALIDA
    quality_reports/synthesis_scalars.json   (claves añadidas)
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


def leer(p, enc="utf-8"):
    with open(p, encoding=enc, newline="") as fh:
        return list(csv.DictReader(fh))


def main():
    S = json.loads((QR / "synthesis_scalars.json").read_text(encoding="utf-8"))
    t6 = leer(QR / "tabla6_brazo_a_brazo.csv", enc="utf-8-sig")
    t3 = leer(QR / "tabla3_completitud.csv", enc="utf-8-sig")
    rob = leer(RS / "riesgo_sesgo" / "riesgo_sesgo_comparativos_adjudicado.csv", enc="utf-8-sig")
    excl = {r["study_id"] for r in leer(RS / "cribado" / "exclusiones_tras_texto_completo.csv")}
    adj = [r for r in leer(RS / "extraccion" / "extraccion_adjudicada.csv")
           if r["study_id"] not in excl]
    grupos = leer(RS / "cribado" / "study_groups.csv")
    corpus = {r["record_id"]: r for r in leer(RS / "cribado" / "screening_corpus_all.csv")}
    solap = leer(QR / "solapamiento_candidatos.csv", enc="utf-8-sig")
    enlace = leer(QR / "brazo_informe.csv", enc="utf-8-sig")

    # ---- embudo de la proporción descriptiva: SIN el filtro de diseño
    # comparativo, que no es un requisito para agrupar proporciones.
    pasos = [("numerador y denominador coherentes", ("numerador_valido", "denominador_valido")),
             ("definición operativa del éxito", ("definicion_operativa",)),
             ("desenlace atribuible a P. aeruginosa", ("atribuible_a_P_aeruginosa",)),
             ("administración terapéutica, no profiláctica", ("terapeutica_no_profilactica",)),
             ("reporta una proporción, no un tiempo", ("proporcion_no_tiempo",))]
    vivos, embudo = list(t6), [{"filtro": "brazos extraídos", "brazos": len(t6),
                                "estudios": len({r["study_id"] for r in t6})}]
    for nombre, grupo in pasos:
        vivos = [r for r in vivos if all(r[k] == "cumple" for k in grupo)]
        embudo.append({"filtro": nombre, "brazos": len(vivos),
                       "estudios": len({r["study_id"] for r in vivos})})
    S["embudo_proporcion"] = embudo
    S["brazos_agrupables"] = len(vivos)
    S["estudios_agrupables"] = len({r["study_id"] for r in vivos})
    S["brazos_agrupables_n1"] = sum(1 for r in vivos if (r["N_brazo"] or "").strip() == "1")
    S["brazos_agrupables_n1_pct"] = round(
        100.0 * S["brazos_agrupables_n1"] / S["brazos_agrupables"], 1)

    # ---- comparador: NINGUN brazo extraído es un brazo de control. La
    # modalidad solo toma tres valores y los tres son exposición al fago.
    modos = collections.Counter(r["modality"] for r in adj)
    S["modalidades_extraidas"] = dict(modos)
    S["brazos_con_comparador_extraido"] = sum(
        1 for r in adj if "control" in r["modality"].lower()
        or "placebo" in r["modality"].lower()
        or "standard" in r["modality"].lower())

    # ---- denominadores de uno, medidos sobre la extracción adjudicada y no
    # inferidos del diseño que declara el resumen. Hoy coinciden en 42 con los
    # reportes de caso declarados, y son dos poblaciones distintas.
    por = collections.defaultdict(list)
    for r in adj:
        n = (r["n_arm"] or "").strip()
        por[r["study_id"]].append(int(n) if n.isdigit() else None)
    S["estudios_denominador_uno"] = sum(
        1 for v in por.values() if len(v) == 1 and v[0] == 1)
    S["estudios_denominador_desconocido"] = sum(
        1 for v in por.values() if any(x is None for x in v))

    # ---- Tabla 3: lo que dice el artículo cuando el resumen calla
    for f in t3:
        c = f["campo"]
        S["t3_%s_declarado" % c] = int(f["declarado_texto_completo"])
        S["t3_%s_no_clasificable" % c] = int(f["declarado_no_clasificable"])
        S["t3_%s_silencio" % c] = int(f["no_declarado_texto_completo"])
        S["t3_%s_sin_texto" % c] = int(f["texto_no_recuperado"])
    con_texto = int(t3[0]["total"]) - int(t3[0]["texto_no_recuperado"])
    S["t3_con_texto"] = con_texto
    S["t3_clase_declarada_pct"] = round(
        100.0 * S["t3_resistance_class_declarado"] / con_texto, 1)

    # ---- juicios: los 90 no son todos de dominio
    S["juicios_globales"] = sum(1 for r in rob if r["item"] == "GLOBAL")
    S["juicios_de_dominio"] = len(rob) - S["juicios_globales"]
    S["celdas_tabla5"] = len(rob)
    inst = collections.defaultdict(set)
    for r in rob:
        inst[r["instrumento"]].add(r["study_id"])
    S["dominios_rob2"] = 5
    S["dominios_robins"] = 7
    S["juicios_rob2"] = len(inst["rob2"]) * S["dominios_rob2"]
    S["juicios_robins"] = len(inst["robins"]) * S["dominios_robins"]
    # los escalones del embudo descriptivo, uno a uno, para poder anclarlos
    for k, paso in zip(("numerador", "definicion", "atribuible", "terapeutica",
                        "proporcion"), embudo[1:]):
        S["embudo_prop_" + k] = paso["brazos"]
        S["embudo_prop_%s_estudios" % k] = paso["estudios"]

    # ---- LAS CATORCE CIFRAS DE LA AUDITORIA DE CIERRE (2026-09-20)
    import re as _re
    import unicodedata as _ud

    # 1 y 2. juicios: los que heredan el peor dominio, y los que no son juicio
    ORDEN = {"robins": ["bajo riesgo de sesgo", "riesgo moderado", "riesgo grave",
                        "riesgo critico"],
             "rob2": ["bajo riesgo de sesgo", "algunas preocupaciones",
                      "alto riesgo de sesgo"]}

    def _k(v):
        v = _ud.normalize("NFKD", (v or "").lower())
        return "".join(c for c in v if not _ud.combining(c)).strip()

    por_est = collections.defaultdict(dict)
    for r in rob:
        por_est[(r["study_id"], r["instrumento"])][r["item"]] = r["valor"]
    heredan, discord = 0, []
    for (e, i), d in por_est.items():
        doms = {x: v for x, v in d.items() if x != "GLOBAL"}
        sininfo = [x for x, v in doms.items() if "sin informacion" in _k(v)]
        graves = [x for x, v in doms.items() if _k(v) in ("riesgo grave", "riesgo critico")]
        esperado = ("sin informacion" if (sininfo and not graves) else
                    max((_k(v) for v in doms.values() if _k(v) in ORDEN[i]),
                        key=lambda x: ORDEN[i].index(x), default=""))
        if _k(d["GLOBAL"]) == esperado:
            heredan += 1
        else:
            discord.append(e)
    S["globales_heredan_peor"] = heredan
    S["globales_discordantes"] = len(discord)
    S["globales_discordantes_ids"] = sorted(discord)
    S["juicios_sin_informacion"] = sum(
        1 for r in rob if r["item"] != "GLOBAL" and "sin informacion" in _k(r["valor"]))
    S["juicios_con_veredicto"] = S["juicios_de_dominio"] - S["juicios_sin_informacion"]

    # 3. reportes y series entre los estudios leídos
    pdfs = {q.stem for q in (RS / "textos_completos" / "pdf").iterdir()
            if q.suffix.lower() in (".pdf", ".docx")}
    _web = RS / "textos_completos" / "texto_html"
    if _web.exists():
        pdfs |= {q.stem for q in _web.glob("*.txt")}
    COMPARA = {"RCT", "non-randomised trial", "retrospective cohort",
               "prospective cohort"}
    dis = collections.defaultdict(set)
    for r in adj:
        if r["study_design"] and r["study_design"] != "NA":
            dis[r["study_id"]].add(r["study_design"])
    leidos = {e for e in dis if e in pdfs}
    S["comparativos_con_texto"] = len([e for e in leidos if dis[e] & COMPARA])
    S["casos_y_series_leidos"] = len(leidos) - S["comparativos_con_texto"]

    # 4. la clase de resistencia, separando lo que está por debajo del umbral
    clase = collections.defaultdict(set)
    for r in adj:
        if r["study_id"] in pdfs and r["resistance_class"]:
            clase[r["study_id"]].add(r["resistance_class"])
    S["t3_clase_mdr_xdr_pdr"] = sum(
        1 for v in clase.values() if v & {"MDR", "XDR", "PDR"})
    S["t3_clase_bajo_umbral"] = sum(
        1 for v in clase.values()
        if "below-MDR-threshold" in v and not (v & {"MDR", "XDR", "PDR"}))
    S["brazos_bajo_umbral"] = sum(
        1 for r in adj if r["resistance_class"] == "below-MDR-threshold")

    # 5. el marco del recribado, separado por etapa
    S["validacion_marco_titulo"] = S["excluidos_titulo"]
    S["validacion_marco_resumen"] = S["excluidos_resumen"]

    # 6. cuántos brazos aporta cada comparativo
    comp = sorted(e for e, v in dis.items() if v & COMPARA)
    aporta = collections.Counter()
    for r in adj:
        if r["study_id"] in comp and r["study_design"] in COMPARA:
            aporta[r["study_id"]] += 1
    S["comparativos_un_brazo"] = sum(1 for v in aporta.values() if v == 1)
    S["comparativos_varios_brazos"] = sum(1 for v in aporta.values() if v > 1)
    S["brazos_del_comparativo_mayor"] = max(aporta.values()) if aporta else 0

    # 12. las tres clases de apoyo de los juicios
    juicios = leer(QR / "pendiente1_juicios.csv", enc="utf-8-sig")
    S["citas_literales"] = sum(
        1 for r in juicios if r["cita_que_lo_respalda"] != "[DATO FALTANTE]"
        and _re.search(r"[\"“”]", r["cita_que_lo_respalda"]))
    S["juicios_sin_frase"] = sum(
        1 for r in juicios if r["cita_que_lo_respalda"] == "[DATO FALTANTE]")
    S["notas_del_revisor"] = (len(juicios) - S["citas_literales"]
                              - S["juicios_sin_frase"])

    # 8. quién resolvió cada desacuerdo de extracción
    confl = leer(RS / "extraccion" / "extraction_conflicts.csv")
    S["conflictos_resueltos_por_los_dos"] = sum(
        1 for r in confl if " Y " in (r["resuelto_por"] or "").upper())
    S["conflictos_resueltos_por_uno"] = sum(
        1 for r in confl if (r["resuelto_por"] or "").upper().strip()
        in ("DANNY VALDIVIEZO", "NATALY TRELLES"))

    # 10 y 13. el solapamiento, medido
    sol = leer(QR / "pendiente2_solapamiento.csv", enc="utf-8-sig")
    S["pares_solapamiento_examinados"] = len(sol)
    S["pares_solapamiento_confirmados"] = sum(
        1 for r in sol if r["veredicto"].startswith("SOLAPAMIENTO"))
    S["pares_solapamiento_sin_leer"] = sum(
        1 for r in sol if r["veredicto"].startswith("SIN LEER"))
    conf = [r for r in sol if r["veredicto"].startswith("SOLAPAMIENTO")]
    S["estudios_con_paciente_compartido"] = len(
        {x for r in conf for x in (r["estudio_1"], r["estudio_2"])})
    # El del Berlin Heart aparece en DOS pares y es un solo paciente: se cuenta
    # por la clave estable, no por la fila.
    # una clave puede valer por mas de un paciente: EST-164 aporta dos
    claves = {}
    for r in conf:
        if r["clave_del_paciente"] in ("ninguno", "[DATO FALTANTE]"):
            continue
        claves[r["clave_del_paciente"]] = int(r.get("pacientes_de_esa_clave") or 1)
    S["claves_de_paciente_duplicado"] = len(claves)
    S["pacientes_duplicados_confirmados"] = sum(claves.values())

    # ---- la declaración de EST-108, leída de su propio texto y no tecleada
    _t108 = RS / "textos_completos" / "texto_cache" / "EST-108.txt"
    if _t108.exists():
        _t = _re.sub(r"\s+", " ", _t108.read_text(encoding="utf-8", errors="replace"))
        # LAS DOS COLUMNAS PARTEN LA FRASE. En el PDF sale como «Twenty-seven
        # of the 100 BT tal (QAMH), KU Leuven and Sciensano (...) cases/patients
        # were previously reported6,13-26»: el sujeto en una columna y el verbo
        # en la otra. Se buscan las dos mitades y se exige que esten cerca.
        _m = _re.search(r"(\w+[- ]?\w*) of the (\d+) BT", _t, _re.I)
        if _m and not _re.search(r"cases/patients were previously reported",
                                 _t[_m.end():_m.end() + 260], _re.I):
            _m = None
        if _m:
            _pal = {"twenty-seven": 27, "twentyseven": 27}
            _n = _pal.get(_m.group(1).lower().replace(" ", "-"))
            if _n is None and _m.group(1).isdigit():
                _n = int(_m.group(1))
            if _n is not None:
                S["est108_previamente_publicados"] = _n
                S["est108_casos"] = int(_m.group(2))
                S["est108_frase"] = ("«%s ... cases/patients were "
                                     "previously reported»" % _m.group(0))

    # ---- de cuántas fuentes depende cada estudio incluido
    fuentes = collections.defaultdict(set)
    for g in grupos:
        e = "EST-%03d" % int(g["estudio"])
        if e in excl:
            continue
        for f in (corpus.get(g["record_id"], {}).get("sources") or "").split(";"):
            if f.strip():
                fuentes[e].add(f.strip())
    una = [e for e, v in fuentes.items() if len(v) == 1]
    S["estudios_una_sola_fuente"] = len(una)
    S["estudios_una_sola_fuente_pct"] = round(100.0 * len(una) / len(fuentes), 1)
    S["una_sola_fuente_por_fuente"] = dict(collections.Counter(
        sorted(list(fuentes[e])[0] for e in una)).most_common())

    # ---- solapamiento y enlace brazo-informe
    S["solapamiento_pares_examinados"] = len(solap)
    S["solapamiento_textos_examinados"] = len(
        {r["study_id"] for r in enlace if r["documento_leido"] != "sin texto"})
    S["brazos_con_informe_identificado"] = len(enlace)
    S["brazos_informe_por_lectura"] = sum(
        1 for r in enlace if r["via"].startswith("título"))

    (QR / "synthesis_scalars.json").write_text(
        json.dumps(S, ensure_ascii=False, indent=2), encoding="utf-8", newline="\n")

    print("escalares de auditoría fundidos en synthesis_scalars.json")
    print("  embudo de la proporción descriptiva:")
    for p in embudo:
        print("    %-46s %3d brazos  %3d estudios" % (p["filtro"], p["brazos"], p["estudios"]))
    print("  brazos con comparador extraído: %d" % S["brazos_con_comparador_extraido"])
    print("  clase de resistencia sobre los %d con texto: %d declarada, %d no clasificable, %d en silencio"
          % (con_texto, S["t3_resistance_class_declarado"],
             S["t3_resistance_class_no_clasificable"], S["t3_resistance_class_silencio"]))
    print("  juicios: %d de dominio + %d globales = %d"
          % (S["juicios_de_dominio"], S["juicios_globales"], S["celdas_tabla5"]))
    print("  estudios hallados por una sola fuente: %d (%.1f %%)"
          % (S["estudios_una_sola_fuente"], S["estudios_una_sola_fuente_pct"]))


if __name__ == "__main__":
    main()
