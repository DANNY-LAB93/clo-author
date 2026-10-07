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
    excl = {r["study_id"] for r in leer(RS / "cribado" / "exclusiones_tras_texto_completo.csv")}
    # Los juicios de un estudio que salio del corpus NO se borran de su fichero
    # --son el registro de lo que se juzgo de verdad-- pero dejan de contarse,
    # igual que `study_groups` conserva a los excluidos del cribado y el canal
    # no los suma. EST-063 salio como protocolo el 2026-09-22 y se lleva sus
    # siete juicios de dominio y su global.
    rob = [r for r in leer(RS / "riesgo_sesgo"
                           / "riesgo_sesgo_comparativos_adjudicado.csv",
                           enc="utf-8-sig")
           if r["study_id"] not in excl]
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

    # ---- por que 7 ensayos en la Tabla 2 y solo 3 con RoB 2 -------------
    # La Tabla 2 clasifica por lo que DECLARA EL RESUMEN sobre los recuperables;
    # RoB 2 se aplica a los que ademas tienen texto completo. El manuscrito
    # daba las dos cifras sin explicar el paso, y un lector atento lo lee como
    # una incoherencia.
    _pre = {r["id_provisional"]: r for r in
            leer(RS / "extraccion" / "pre_extraccion_desde_resumen.csv")}
    _pdfs = {q.stem for q in (RS / "textos_completos" / "pdf").iterdir()}
    _reps = {"EST-%03d" % int(g["estudio"]): g for g in grupos
             if g["informe_para_extraer"] == "SI"}
    _eca = [e for e, g in _reps.items()
            if e not in excl
            and g["situacion"] in ("extraible", "solo-resumen")
            and _pre.get(e, {}).get("study_design") == "RCT"]
    S["ecas_por_resumen"] = len(_eca)
    S["ecas_con_texto"] = sum(1 for e in _eca if e in _pdfs)
    S["ecas_sin_texto"] = len(_eca) - S["ecas_con_texto"]
    S["ecas_sin_texto_ids"] = sorted(e for e in _eca if e not in _pdfs)

    # ---- concordancia entre los dos revisores, ANTES del consenso ------
    # El manuscrito decia que no se podia medir. Se puede: los dos cuadernos
    # individuales existen. `build_concordancia_rob.py` la calcula.
    _c = QR / "concordancia_rob.json"
    if _c.exists():
        S.update(json.loads(_c.read_text(encoding="utf-8")))
        # EST-004 se evaluo en un cuaderno aparte el 2026-09-17 y tiene UNA
        # sola lectura. Decir «los 11 evaluables con doble lectura» seria
        # falso, y la diferencia es justo el estudio que obligo a reabrir la
        # evaluacion el 2026-09-16.
        _est = QR / "rob_tabla_estado.json"
        _ev = (json.loads(_est.read_text(encoding="utf-8"))["evaluables"]
               if _est.exists() else None)
        if _ev is None:
            raise SystemExit("falta rob_tabla_estado.json: corre "
                             "build_rob_table.py antes que este")
        S["rob_estudios_evaluables"] = _ev
        S["rob_estudios_con_una_lectura"] = _ev - S["rob_estudios_con_dos_lecturas"]

    # ---- grupo de comparacion REAL, no etiqueta de diseno --------------
    # La etiqueta «comparativo» sale del diseno adjudicado y una cohorte cuenta
    # como comparativa aunque no tenga con que comparar. Los dos autores
    # firmaron el 2026-09-22 (hoja 6 de la auditoria) que el manuscrito diga
    # las dos cosas: cuantos tienen diseno comparativo y cuantos tienen grupo.
    _g = RS / "riesgo_sesgo" / "grupo_de_comparacion_real.csv"
    if _g.exists():
        _f = [r for r in leer(_g) if r["en_el_corpus"] == "si"]
        S["comparativos_con_grupo_real"] = sum(
            1 for r in _f if r["tiene_grupo_de_comparacion"] == "si")
        S["comparativos_sin_grupo_real"] = sum(
            1 for r in _f if r["tiene_grupo_de_comparacion"] == "no")
        S["comparativos_con_grupo_real_ids"] = sorted(
            r["study_id"] for r in _f if r["tiene_grupo_de_comparacion"] == "si")
        S["comparativos_sin_grupo_real_ids"] = sorted(
            r["study_id"] for r in _f if r["tiene_grupo_de_comparacion"] == "no")

    # ---- y de los que tienen grupo, cual compara fago con NO fago, y cual
    # da un contraste para P. aeruginosa. Lo firmaron los dos autores el
    # 2026-09-30 al reextraer los comparativos (punto 7 del encargo). No
    # contradice la hoja 6: EST-108 SI tiene grupo de comparacion --con y sin
    # antibiotico--, pero los dos brazos reciben fago.
    _c = RS / "lectura_pendiente" / "lectura_comparativos_firmada.csv"
    if _c.exists():
        _l = {r["study_id"]: r for r in leer(_c, enc="utf-8-sig")
              if r["study_id"] not in excl}
        _con = S.get("comparativos_con_grupo_real_ids", [])
        S["comparativos_fago_vs_no_fago_ids"] = sorted(
            e for e in _con if _l.get(e, {}).get("grupo_sin_fago") == "si")
        S["comparativos_fago_vs_no_fago"] = len(S["comparativos_fago_vs_no_fago_ids"])
        S["comparativos_grupo_con_fago_ids"] = sorted(
            e for e in _con if _l.get(e, {}).get("grupo_sin_fago") == "no")
        S["comparativos_contraste_pa_ids"] = sorted(
            e for e, r in _l.items()
            if r["contraste_para_p_aeruginosa"] in ("si", "parcial"))
        S["comparativos_contraste_pa"] = len(S["comparativos_contraste_pa_ids"])
        S["comparativos_contraste_pa_parcial_ids"] = sorted(
            e for e, r in _l.items() if r["contraste_para_p_aeruginosa"] == "parcial")
        S["comparativos_reextraidos"] = len(_l)
        S["comparativos_reextraidos_con_texto"] = sum(
            1 for r in _l.values() if r["grupo_sin_fago"] != "sin texto")
        # Lo que se LEYO, antes de las exclusiones que la propia lectura trajo:
        # los Metodos describen el procedimiento y el anexo S24 lleva las 14 filas.
        _todos_c = leer(_c, enc="utf-8-sig")
        S["comparativos_reextraidos_leidos"] = len(_todos_c)
        S["comparativos_reextraidos_leidos_con_texto"] = sum(
            1 for r in _todos_c if r["grupo_sin_fago"] != "sin texto")

    # ---- la clase de resistencia, comprobada contra el articulo (punto 2).
    # La traduccion del texto firmado a estas categorias esta en
    # `ingest_lectura_firmada.py`, estudio por estudio y con su guarda.
    _r = RS / "lectura_pendiente" / "lectura_resistencia_firmada.csv"
    if _r.exists():
        _v = [r for r in leer(_r, enc="utf-8-sig") if r["study_id"] not in excl]
        _cv = collections.Counter(r["verificacion"] for r in _v)
        S["lectura_clase_estudios"] = len(_v)
        S["lectura_clase_antibiograma"] = _cv["antibiograma"]
        S["lectura_clase_texto"] = _cv["texto"]
        S["lectura_clase_verificables"] = _cv["antibiograma"] + _cv["texto"]
        S["lectura_clase_no_verificable"] = _cv["no verificable"]
        S["lectura_clase_no_aplica"] = _cv["no aplica"]
        S["lectura_clase_no_aplica_ids"] = sorted(
            r["study_id"] for r in _v if r["verificacion"] == "no aplica")

        def _cubo(rel):
            if rel.startswith("coincide"):
                return "coincide"
            if rel.startswith("la declarada no era clasificable"):
                return "antes_no_clasificable"
            if rel.startswith("más grave"):
                return "mas_grave"
            if rel.startswith(("menos grave", "no confirma", "refuta")):
                return "no_se_sostiene"
            return "mixta"
        _ver = [r for r in _v if r["verificacion"] in ("antibiograma", "texto")]
        _cb = collections.Counter(_cubo(r["relacion_con_la_declarada"]) for r in _ver)
        S["lectura_clase_coincide"] = _cb["coincide"]
        S["lectura_clase_antes_no_clasificable"] = _cb["antes_no_clasificable"]
        _anc = [r for r in _ver if _cubo(r["relacion_con_la_declarada"])
                == "antes_no_clasificable"]
        S["lectura_clase_antes_nc_bajo_umbral"] = sum(
            1 for r in _anc if r["clase_verificada_codificada"] == "below-MDR-threshold")
        S["lectura_clase_antes_nc_xdr"] = sum(
            1 for r in _anc if r["clase_verificada_codificada"] == "XDR")
        S["lectura_clase_mas_grave"] = _cb["mas_grave"]
        S["lectura_clase_mas_grave_ids"] = sorted(
            r["study_id"] for r in _ver if _cubo(r["relacion_con_la_declarada"]) == "mas_grave")
        S["lectura_clase_no_se_sostiene"] = _cb["no_se_sostiene"]
        S["lectura_clase_no_se_sostiene_ids"] = sorted(
            r["study_id"] for r in _ver
            if _cubo(r["relacion_con_la_declarada"]) == "no_se_sostiene")
        S["lectura_clase_mixta"] = _cb["mixta"]
        S["lectura_clase_mixta_ids"] = sorted(
            r["study_id"] for r in _ver if _cubo(r["relacion_con_la_declarada"]) == "mixta")
        S["lectura_queda_abierto"] = sum(1 for r in _v if r["queda_abierto"])
        S["lectura_queda_abierto_ids"] = sorted(r["study_id"] for r in _v if r["queda_abierto"])
        _corr = [r for r in leer(RS / "extraccion" / "correcciones_tras_texto_completo.csv")
                 if r["motivo"].startswith("Lectura firmada del 2026-09-30")
                 and r["study_id"] not in excl]
        S["lectura_correcciones"] = len(_corr)
        S["lectura_correcciones_clase"] = sum(
            1 for r in _corr if r["campo"] == "resistance_class")
        S["lectura_correcciones_procedencia"] = sum(
            1 for r in _corr if r["campo"] == "resistance_class_source")
        S["lectura_correcciones_dtr"] = sum(1 for r in _corr if r["campo"] == "dtr_status")

        # ---- lo que los dos autores decidieron el 2026-10-01 sobre lo abierto
        _todos = leer(_r, enc="utf-8-sig")                 # sin filtrar: los 70 leidos
        S["lectura_clase_estudios_leidos"] = len(_todos)
        _sinpa = [r["study_id"] for r in _todos if r["verificacion"] == "no aplica"]
        S["lectura_sin_pa_total"] = len(_sinpa)
        S["lectura_sin_pa_excluidos_ids"] = sorted(e for e in _sinpa if e in excl)
        S["lectura_sin_pa_excluidos"] = len(S["lectura_sin_pa_excluidos_ids"])
        S["lectura_sin_pa_mantenidos_ids"] = sorted(e for e in _sinpa if e not in excl)
        S["lectura_sin_pa_mantenidos"] = len(S["lectura_sin_pa_mantenidos_ids"])
        _dec = RS / "lectura_pendiente" / "decisiones_firmadas_2026-10-01.csv"
        if _dec.exists():
            _d = [r for r in leer(_dec, enc="utf-8-sig") if r["study_id"] not in excl]
            _h1 = [r for r in _d if r["hoja"] in ("1 sin P. aeruginosa", "adenda")
                   and r["decision"] == "mantener"]
            for cod in ("cita", "coctel", "no_diana"):
                S["lectura_sin_pa_%s_ids" % cod] = sorted(
                    r["study_id"] for r in _h1 if r["p_aeruginosa_en_el_articulo"] == cod
                    and r["study_id"] in _sinpa)
            S["lectura_sin_pa_citados_ids"] = [
                next(r["estudio_citado"] for r in _h1 if r["study_id"] == e)
                for e in S["lectura_sin_pa_cita_ids"]]
            S["lectura_dudosos_mantenidos_ids"] = sorted(
                r["study_id"] for r in _h1 if r["study_id"] not in _sinpa)
            _h3 = [r for r in _d if r["hoja"] == "3 clase y DTR"]
            S["lectura_abiertos_resueltos"] = len(_h3)
            S["lectura_abiertos_corregidos_ids"] = sorted(
                r["study_id"] for r in _h3 if "sin cambio" not in r["decision"])
            S["lectura_abiertos_corregidos"] = len(S["lectura_abiertos_corregidos_ids"])
            S["lectura_abiertos_sin_cambio_ids"] = sorted(
                r["study_id"] for r in _h3 if "sin cambio" in r["decision"])
            S["lectura_abiertos_sin_cambio"] = len(S["lectura_abiertos_sin_cambio_ids"])
            _c2 = [r for r in leer(RS / "extraccion" / "correcciones_tras_texto_completo.csv")
                   if r["motivo"].startswith("Decisión firmada del 2026-10-01")
                   and r["study_id"] not in excl]
            S["firma_lectura_correcciones"] = len(_c2)

    # ---- el idioma del CUERPO de cada PDF del corpus (comprueba_idioma_cuerpo.py)
    _ic = QR / "idioma_cuerpo_pdf.csv"
    if _ic.exists():
        _f = leer(_ic, enc="utf-8-sig")
        S["idioma_cuerpo_comprobados"] = len(_f)
        S["idioma_cuerpo_ingles"] = sum(1 for r in _f if r["idioma_del_cuerpo"] == "eng")
        S["idioma_cuerpo_espanol"] = sum(1 for r in _f if r["idioma_del_cuerpo"] == "spa")
        S["idioma_cuerpo_otro"] = sum(1 for r in _f if r["idioma_del_cuerpo"] not in ("eng", "spa"))
    S["idioma_no_verificable_excluidos"] = sum(
        1 for r in leer(RS / "cribado" / "exclusiones_tras_texto_completo.csv")
        if r["codigo"] == "NOREC" and r["motivo"].startswith("Idioma no verificable"))

    # ---- la §3.1.1: lo juzgado sobre el articulo y lo que no tiene texto.
    # «Los 29 anteriores» y «los 31 sin texto completo» iban tecleados.
    S["excluidos_sobre_el_articulo"] = (S["excluidos_por_publicacion"]
                                        - S.get("excluidos_texto_completo_NOREC", 0))
    S["sin_texto_completo_total"] = (S["texto_completo_no_obtenido"]
                                     + S["excluidos_sin_poder_leer_nada"])

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
        # «Sin informacion para juzgar» es como se llama el juicio en los
        # cuadernos; `esperado` lo nombra «sin informacion». Comparadas tal
        # cual, un global CORRECTO salia discordante: EST-116 lo hizo el
        # 2026-09-22, en cuanto se corrigio.
        _glob = _k(d["GLOBAL"])
        if esperado == "sin informacion" and _glob.startswith("sin informacion"):
            _glob = "sin informacion"
        if _glob == esperado:
            heredan += 1
        else:
            discord.append(e)
    S["globales_heredan_peor"] = heredan
    S["globales_discordantes"] = len(discord)
    S["globales_discordantes_ids"] = sorted(discord)
    S["juicios_sin_informacion"] = sum(
        1 for r in rob if r["item"] != "GLOBAL" and "sin informacion" in _k(r["valor"]))
    S["juicios_con_veredicto"] = S["juicios_de_dominio"] - S["juicios_sin_informacion"]
    # Y de quien son, para que el manuscrito pueda nombrarlos sin teclearlos.
    _si = collections.Counter(
        r["study_id"] for r in rob
        if r["item"] != "GLOBAL" and "sin informacion" in _k(r["valor"]))
    _n_es = {1: "un dominio", 2: "dos dominios", 3: "tres dominios",
             4: "cuatro dominios", 5: "cinco dominios", 6: "seis dominios",
             7: "siete dominios"}
    S["juicios_sin_informacion_ids"] = [
        "%s, %s" % (e, _n_es.get(n, "%d dominios" % n))
        for e, n in sorted(_si.items())]

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
    _bajo = [r for r in adj if r["resistance_class"] == "below-MDR-threshold"]
    S["brazos_bajo_umbral"] = len(_bajo)
    S["brazos_bajo_umbral_ids"] = sorted(
        "%s %s" % (r["study_id"], r["arm_id"]) for r in _bajo)
    # Un brazo por debajo del umbral dentro de un estudio que SI incluye
    # multirresistentes es un estrato, y no compromete la elegibilidad del
    # estudio. Un estudio de un solo brazo cuyo unico paciente esta por debajo
    # del umbral, si. Los dos autores firmaron el 2026-09-22 mantenerlos y
    # declararlos; la distincion tiene que salir del dato, no de la prosa.
    _n_brazos = collections.Counter(r["study_id"] for r in adj)
    S["brazos_bajo_umbral_estrato"] = sum(
        1 for r in _bajo if _n_brazos[r["study_id"]] > 1)
    S["bajo_umbral_estudio_entero_ids"] = sorted(
        r["study_id"] for r in _bajo if _n_brazos[r["study_id"]] == 1)
    S["bajo_umbral_estudio_entero"] = len(S["bajo_umbral_estudio_entero_ids"])
    # La firma del 2026-09-22 cubre a EST-001 y EST-094, y a nadie mas. Los
    # que la lectura del 2026-09-30 llevo por debajo del umbral (EST-053,
    # EST-057, EST-088) estan en la misma situacion y sin decision firmada:
    # el manuscrito no puede decir que «se mantienen por decision firmada».
    _f22 = {"EST-001", "EST-094"}
    # Las del 2026-10-01 (hoja 2 del cuaderno de la lectura, y la adenda si
    # llega firmada) salen del fichero de decisiones, no de esta linea.
    _f01 = set()
    _dec = RS / "lectura_pendiente" / "decisiones_firmadas_2026-10-01.csv"
    if _dec.exists():
        _ds = leer(_dec, enc="utf-8-sig")
        _f01 = {r["study_id"] for r in _ds if r["hoja"] != "adenda"
                and r["decision"].startswith("mantener y declarar")}
        _f03 = {r["study_id"] for r in _ds if r["hoja"] == "adenda"
                and r["decision"].startswith("mantener y declarar")}
    else:
        _f03 = set()
    _firmados = _f22 | _f01 | _f03
    S["bajo_umbral_mantenidos_22sep_ids"] = [
        e for e in S["bajo_umbral_estudio_entero_ids"] if e in _f22]
    S["bajo_umbral_mantenidos_01oct_ids"] = [
        e for e in S["bajo_umbral_estudio_entero_ids"] if e in _f01]
    # La adenda del 2026-10-03, firmada por los dos (EST-106).
    S["bajo_umbral_mantenidos_03oct_ids"] = [
        e for e in S["bajo_umbral_estudio_entero_ids"] if e in _f03]
    S["bajo_umbral_mantenidos_por_firma_ids"] = [
        e for e in S["bajo_umbral_estudio_entero_ids"] if e in _firmados]
    S["bajo_umbral_mantenidos_por_firma"] = len(S["bajo_umbral_mantenidos_por_firma_ids"])
    S["bajo_umbral_sin_decision_ids"] = [
        e for e in S["bajo_umbral_estudio_entero_ids"] if e not in _firmados]
    S["bajo_umbral_sin_decision"] = len(S["bajo_umbral_sin_decision_ids"])

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
    # El del Berlin Heart aparece en TRES pares y es un solo paciente: se
    # cuenta por PERSONA, no por fila. Desde la lectura firmada del 2026-09-30
    # cada fila confirmada trae sus pacientes como «P1 ...; P12 ...», una
    # clave por persona; contar las cadenas de la columna, como antes, dio 22
    # donde son 20, porque EST-003 + EST-070 lleva seis personas en una fila.
    claves = set()
    pac_de = collections.defaultdict(set)
    for r in conf:
        ks = _re.findall(r"(?:^|;\s*)(P\d+)\b", r["clave_del_paciente"])
        if not ks:
            raise SystemExit("solapamiento confirmado sin clave de paciente: %s + %s"
                             % (r["estudio_1"], r["estudio_2"]))
        claves.update(ks)
        for e in (r["estudio_1"], r["estudio_2"]):
            pac_de[e].update(ks)
    S["claves_de_paciente_duplicado"] = len(claves)
    S["pacientes_duplicados_confirmados"] = len(claves)
    S["pares_solapamiento_descartados"] = sum(
        1 for r in sol if r["veredicto"].startswith("DESCARTADO"))
    S["pares_solapamiento_sin_resolver"] = sum(
        1 for r in sol if r["veredicto"].startswith("SIN RESOLVER"))
    S["pares_solapamiento_por_lectura"] = sum(
        1 for r in sol if r["senal_que_lo_marco"].startswith("NO lo marco"))
    S["pares_solapamiento_por_detector"] = (S["pares_solapamiento_examinados"]
                                            - S["pares_solapamiento_por_lectura"])
    # Los tres grupos donde se concentra, contados desde los datos.
    S["est003_pacientes_compartidos"] = len(pac_de["EST-003"])
    _p003_070 = set()
    for r in conf:
        if {r["estudio_1"], r["estudio_2"]} == {"EST-003", "EST-070"}:
            _p003_070.update(_re.findall(r"(?:^|;\s*)(P\d+)\b", r["clave_del_paciente"]))
    S["est003_con_est070"] = len(_p003_070)
    S["est034_pacientes_compartidos"] = len(pac_de["EST-034"])
    S["est108_pacientes_compartidos"] = len(pac_de["EST-108"])
    _con108 = sorted({x for r in conf for x in (r["estudio_1"], r["estudio_2"])
                      if "EST-108" in (r["estudio_1"], r["estudio_2"]) and x != "EST-108"})
    # EST-088 salio despues que EST-108: no esta entre sus «previously
    # reported», coincide por infeccion, especies y fagos.
    _cert = {}
    _f = RS / "lectura_pendiente" / "lectura_solapamiento_firmada.csv"
    if _f.exists():
        for r in leer(_f, enc="utf-8-sig"):
            _cert[frozenset((r["estudio_1"], r["estudio_2"]))] = r["certeza"]
    _citados = [e for e in _con108
                if _cert.get(frozenset(("EST-108", e))) != "muy probable"]
    _probables = [e for e in _con108 if e not in _citados]
    S["est108_estudios_citados_en_corpus"] = len(_citados)
    S["est108_estudios_citados_en_corpus_ids"] = _citados
    S["est108_pacientes_citados_en_corpus"] = len(
        set().union(*(pac_de[e] & pac_de["EST-108"] for e in _citados)) if _citados else set())
    S["est108_coincidencias_no_citadas_ids"] = _probables
    S["solapamiento_muy_probable"] = sum(1 for v in _cert.values() if v == "muy probable")

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
                # Y a cuantas referencias remite: «previously reported6,13-26»
                # son la 6 y de la 13 a la 26. El manuscrito decia «quince»
                # en letra, tecleado.
                _r = _re.search(r"previously reported\s*([\d,–\-\s]+)",
                                _t[_m.end():_m.end() + 400])
                if _r:
                    _n_ref = 0
                    for _tr in _re.split(r"\s*,\s*", _r.group(1).strip()):
                        _ab = _re.split(r"\s*[–\-]\s*", _tr)
                        if len(_ab) == 2 and all(x.isdigit() for x in _ab):
                            _n_ref += int(_ab[1]) - int(_ab[0]) + 1
                        elif _tr.isdigit():
                            _n_ref += 1
                    S["est108_referencias_previas"] = _n_ref

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
    # La frase del manuscrito de la revista, armada aqui: estaba tecleada
    # («20 solo Cochrane CENTRAL, 9 solo ClinicalTrials.gov...») y sumaba 40
    # cuando el total anclado al lado ya decia 6.
    def _nombre(f):
        m = _re.match(r"Scopus \(brazo (\w)\)", f)
        return "el brazo %s de Scopus" % m.group(1) if m else f
    _trozos = ["%d solo %s" % (n, _nombre(f))
               for f, n in S["una_sola_fuente_por_fuente"].items()]
    S["una_sola_fuente_desglose"] = (", ".join(_trozos[:-1]) + " y " + _trozos[-1]
                                    if len(_trozos) > 1 else "".join(_trozos))

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
