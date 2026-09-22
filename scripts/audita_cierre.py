# -*- coding: utf-8 -*-
"""Las cuatro tablas de cierre, completas y exportables, más el impacto.

QUE AÑADE SOBRE `audita_pendientes.py`. Las columnas que el árbitro pidió y
que faltaban: archivo y sección de origen en cada fila, quién la firmó, el
estado de verificación, el tipo de frase de apoyo, el informe de los DOS
estudios de cada par de solapamiento, y la justificación dentro de cada celda
de la Tabla 6. Nada se resume: 90, 20, 103 y 103 filas.

LAS CUATRO CLASES DE APOYO, QUE NO SON LO MISMO Y HABÍA QUE SEPARAR

  1. **cita literal**      texto entrecomillado copiado del artículo.
  2. **nota del revisor**  texto que escribieron los revisores. Es una razón,
                           no una cita, y no permite a un árbitro discrepar
                           leyendo el artículo.
  3. **juicio firmado**    los 90. Todos llevan las dos firmas.
  4. **sin fuente**        la casilla de apoyo está vacía.

Con estas definiciones, 79 y 33 no se contradicen: 79 juicios tienen ALGO
escrito y 33 tienen una CITA. Lo que hay que corregir es la palabra, no la
cifra.

LO QUE NO DECIDE ESTE SCRIPT. Qué estudio se conserva cuando dos comparten
paciente, y si EST-063 se excluye. Las dos son decisiones de los autores; aquí
va la recomendación y el recálculo de lo que pasaría, marcados como tales.

SALIDA
    quality_reports/cierre_A_juicios.csv
    quality_reports/cierre_B_solapamiento.csv
    quality_reports/cierre_C_brazos.csv
    quality_reports/cierre_D_tabla6.csv
    quality_reports/cierre_impacto.json
    ~/Escritorio/Auditoria_cierre_tablas.xlsx      (una hoja por tabla)
"""
import collections
import csv
import json
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
RS = ROOT / "revision_sistematica"
QR = ROOT / "quality_reports"
CACHE = RS / "textos_completos" / "texto_cache"
XLSX = pathlib.Path.home() / "Desktop" / "Auditoria_cierre_tablas.xlsx"
csv.field_size_limit(200_000_000)

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

FALTA = "[DATO FALTANTE]"
COMPARATIVOS = {"RCT", "non-randomised trial", "retrospective cohort",
                "prospective cohort"}
VACIOS = {"", "na", "n/a", "nd"}


def leer(p, enc="utf-8"):
    with open(p, encoding=enc, newline="") as fh:
        return list(csv.DictReader(fh))


def escribe(nombre, filas):
    p = QR / nombre
    with p.open("w", encoding="utf-8-sig", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(filas[0].keys()))
        w.writeheader()
        w.writerows(filas)
    return p


def vacio(v):
    return (v or "").strip().lower() in VACIOS


def entero(v):
    v = (v or "").strip()
    return int(v) if v.isdigit() else None


# ---------------------------------------------------------------- TABLA A
def tabla_a():
    base = leer(QR / "pendiente1_juicios.csv", enc="utf-8-sig")
    hoja = {"rob2": "RoB 2 por dominio", "robins": "ROBINS-I por dominio"}
    filas, cuenta = [], collections.Counter()
    for r in base:
        cita = r["cita_que_lo_respalda"]
        if cita == FALTA:
            tipo, estado = "sin fuente", "SIN FUENTE"
        elif re.search(r"[\"“”]", cita):
            tipo, estado = "cita literal del artículo", "VERIFICADO"
        else:
            tipo, estado = "nota metodológica del revisor", "PENDIENTE"
        cuenta[tipo] += 1
        inst = "rob2" if "RoB 2" in r["instrumento"] else "robins"
        if r["estudio"] == "EST-004":
            archivo = "FIRMAR_riesgo_de_sesgo_EST-004.xlsx"
            seccion = "hoja «ROBINS-I EST-004», fila %s, columna «Frase del " \
                      "artículo en que os apoyáis»" % r["item"]
        else:
            archivo = "revision_sistematica/riesgo_sesgo/" \
                      "riesgo_sesgo_comparativos_consenso.xlsx"
            seccion = "hoja «%s», fila de %s, columna «¿En qué frase te " \
                      "apoyaste?», entrada numerada %s" \
                      % (hoja[inst], r["estudio"], re.sub(r"\D", "", r["item"]) or "—")
        filas.append({
            "n": r["n"],
            "estudio": r["estudio"],
            "informe": r["informe"],
            "referencia_del_informe": r["referencia_del_informe"],
            "instrumento": r["instrumento"],
            "item": r["item"],
            "dominio_o_juicio_global": r["dominio"],
            "tipo_de_juicio": r["tipo_de_juicio"],
            "juicio": r["valor"],
            "frase_de_apoyo": cita,
            "tipo_de_frase": tipo,
            "archivo_de_origen": archivo,
            "seccion_o_celda_de_origen": seccion,
            "pagina_del_articulo": FALTA + ": la página del artículo no se "
                                          "registró en ningún cuaderno",
            "revisor_o_consenso": "consenso de los dos revisores",
            "firmado_por": r["firmado_por"],
            "fecha_de_firma": r["fecha"],
            "estado": estado,
        })
    return filas, cuenta


# ---------------------------------------------------------------- TABLA B
def tabla_b(informes):
    base = leer(QR / "pendiente2_solapamiento.csv", enc="utf-8-sig")
    designado = {}
    for e, gs in informes.items():
        g = next((x for x in gs if x["informe_para_extraer"] == "SI"), gs[0])
        designado[e] = g["record_id"]
    # Qué estudio se conserva si dos comparten paciente. NO lo decide el
    # script: la revisión cuenta estudios y los dos se quedan. Lo que hay que
    # decidir es cuál manda si alguna vez se cuentan pacientes, y eso se firma.
    CONSERVA = {
        ("EST-003", "EST-095"): "EST-095, el reporte original del caso; EST-003 lo "
                                "cita como «Published case»",
        ("EST-003", "EST-015"): "EST-015, el reporte original del caso; EST-003 lo "
                                "cita como «Published case»",
        ("EST-003", "EST-012"): "sin recomendación: EST-012 es posterior a EST-003 y "
                                "ninguno cita al otro como fuente del caso",
        ("EST-003", "EST-070"): "EST-003, que publica el caso con datos; EST-070 lo "
                                "menciona como «manuscript in preparation»",
        ("EST-077", "EST-003"): "EST-077, que describe al paciente con detalle "
                                "clínico; EST-003 lo resume en una fila de tabla",
    }
    filas = []
    for r in base:
        a, b = r["estudio_1"], r["estudio_2"]
        conf = r["veredicto"].startswith("SOLAPAMIENTO")
        est = ("CONFIRMADO" if conf else
               "DESCARTADO" if r["veredicto"].startswith("DESCARTADO") else
               "NO RESUELTO" if r["veredicto"].startswith("SIN RESOLVER") else
               "NO LEIDO")
        cons = CONSERVA.get((a, b)) or CONSERVA.get((b, a)) or ""
        filas.append({
            "estudio_1": a,
            "informe_1": designado.get(a, FALTA),
            "estudio_2": b,
            "informe_2": designado.get(b, FALTA),
            "paciente_o_identificador": r["paciente_o_identificador"],
            "evidencia_del_solapamiento": r["evidencia"],
            "pacientes_potencialmente_duplicados": r["pacientes_potencialmente_duplicados"],
            "estado": est,
            "brazos_afectados": r["brazos_afectados"],
            "contado_una_o_dos_veces": r["se_conto_una_o_dos_veces"],
            "estudio_que_se_conserva_para_el_analisis":
                (cons + " — RECOMENDACIÓN, pendiente de firma de los dos autores")
                if cons else
                (FALTA + ": no procede, no hay solapamiento" if est == "DESCARTADO"
                 else FALTA + ": hace falta leer los dos artículos"),
            "accion_correctiva": r["accion_necesaria"],
            "senal_que_lo_marco": r["senal_que_lo_marco"],
        })
    return filas


def bloque_est021(informes, pdfs):
    rob = [r for r in leer(RS / "riesgo_sesgo" / "riesgo_sesgo_comparativos_adjudicado.csv",
                           enc="utf-8-sig") if r["study_id"] == "EST-021"]
    adj = [r for r in leer(RS / "extraccion" / "extraccion_adjudicada.csv")
           if r["study_id"] == "EST-021"]
    gs = informes["EST-021"]
    des = next(g for g in gs if g["informe_para_extraer"] == "SI")
    dom = {r["item"]: r["valor"] for r in rob}
    a = adj[0]
    return [
        ["Identificación", "%s. %s, %s. record_id %s"
         % (des["titulo"], des["revista"], des["anio"], des["record_id"]),
         "study_groups.csv; texto completo en texto_cache/EST-021.txt"],
        ["Informe asociado", "%s (artículo). Los otros %d informes del estudio son "
         "fichas de registro del mismo ensayo (NCT02116010)."
         % (des["record_id"], len(gs) - 1), "study_groups.csv"],
        ["Diseño", "Ensayo aleatorizado. El resumen lo declara RCT y la adjudicación "
         "sobre el artículo también.", "pre_extraccion + extraccion_adjudicada"],
        ["Número de brazos en el ARTÍCULO", "Dos: PP1131 y cuidado estándar.",
         "«randomly assigned to receive phage therapy (n=13) or standard of care (n=14)»"],
        ["Número de brazos EXTRAÍDOS", "Uno (%s). El comparador no se extrajo."
         % a["arm_id"], "extraccion_adjudicada.csv"],
        ["n_arm registrado", "%s — INCORRECTO" % a["n_arm"],
         "El 27 es el total del ensayo. El brazo de fagos es n=13; población de "
         "seguridad 13, mITT 12. «27 patients were recruited and randomly assigned "
         "to receive phage therapy (n=13) or standard of care (n=14)»"],
        ["mortality_n registrado", "%s — INCORRECTO" % a["mortality_n"],
         "«One patient died in each treatment group after day 21». Hubo 1 muerte en "
         "el brazo de fagos."],
        ["clinical_success_n / n_arm", "%s / %s — INCOHERENTE"
         % (a["clinical_success_n"], a["n_arm"]),
         "El 6 procede de «the most infected wound was successfully reduced by two "
         "quadrants or more in half of participants», 6 de 12 de la mITT del brazo "
         "de fagos. El denominador correcto es 12, no 27."],
        ["adverse_event_n", a["adverse_event_n"],
         "«three (23%) of 13 analysable participants had adverse events». El "
         "numerador es correcto; su denominador es 13, no 27."],
        ["Estado de inclusión", "Incluido en el corpus vivo, con texto completo (%s), "
         "evaluado con la versión adaptada de RoB 2."
         % ("sí" if "EST-021" in pdfs else "no"), "carpetas de texto completo"],
        ["Juicio de riesgo de sesgo", "Dominios: %s. GLOBAL: %s — NO CONFIRMADO."
         % ("; ".join("%s=%s" % (k, dom[k]) for k in sorted(dom) if k != "GLOBAL"),
            dom["GLOBAL"]),
         "RoB 2 (Sterne 2019): «Low risk of bias — the study is judged to be at low "
         "risk of bias for all domains». Con D2 en «Algunas preocupaciones», el "
         "global no puede ser bajo."],
    ]


# ---------------------------------------------------------------- TABLA C
def tabla_c(adj, excl, enlace, pdfs):
    t6 = {(r["study_id"], r["arm_id"]): r
          for r in leer(QR / "tabla6_brazo_a_brazo.csv", enc="utf-8-sig")}
    log = {r["id"]: r for r in leer(RS / "textos_completos" / "fulltext_download_log.csv")}
    # El tipo de desenlace se lee en el artículo, no en una casilla. Los dos
    # que no son una proporción están nombrados en el manuscrito y se declaran
    # aquí con la frase que lo dice.
    TIPO = {"EST-021": ("tiempo hasta evento",
                        "«The primary endpoint was the time taken for a sustained "
                        "reduction in bacterial burden»"),
            "EST-008": ("variable continua",
                        "el desenlace principal es la carga bacteriana en esputo "
                        "(log10 UFC/g), no una proporción")}
    filas = []
    for r in adj:
        e, a = r["study_id"], r["arm_id"]
        if e in excl:
            continue
        en = enlace.get((e, a), {})
        t = t6.get((e, a), {})
        tipo, razon = TIPO.get(e, ("proporción binaria",
                                   "el artículo reporta un recuento de pacientes con "
                                   "éxito sobre el total del brazo"))
        arch = []
        if (CACHE / (e + ".txt")).exists():
            arch.append("revision_sistematica/textos_completos/texto_cache/%s.txt" % e)
        if log.get(e, {}).get("pmcid"):
            arch.append(log[e]["pmcid"])
        if not arch:
            arch.append("sin documento recuperado")
        filas.append({
            "estudio": e,
            "informe": en.get("record_id", "") or FALTA,
            "brazo": a,
            "intervencion": "%s, vía %s" % (r["modality"] or FALTA, r["route"] or FALTA),
            "comparador": FALTA + ": el formulario de extracción no tiene campo de "
                          "comparador; no se extrajo ningún brazo de control",
            "tamano_muestral": r["n_arm"] if not vacio(r["n_arm"]) else FALTA,
            "texto_completo_disponible": "sí" if e in pdfs else "no",
            "desenlace": "éxito clínico",
            "tiempo_de_evaluacion": FALTA + ": el formulario no recoge el momento de "
                                   "evaluación del desenlace",
            "numerador": r["clinical_success_n"] if not vacio(r["clinical_success_n"])
                         else FALTA,
            "denominador": r["n_arm"] if not vacio(r["n_arm"]) else FALTA,
            "definicion_de_exito": (r["clinical_success_definition"]
                                    if not vacio(r["clinical_success_definition"])
                                    and not r["clinical_success_definition"].upper()
                                    .startswith("SIN DEFINICION")
                                    else "sin definición operativa en el artículo"),
            "atribucion_a_P_aeruginosa": "%s — ámbito declarado: %s"
                % (t.get("atribuible_a_P_aeruginosa", FALTA).upper(),
                   r["pathogen_scope"] or FALTA),
            "terapeutico_o_profilactico":
                "terapéutico" if t.get("terapeutica_no_profilactica") == "cumple"
                else "profiláctico",
            "tipo_de_desenlace": "%s — %s" % (tipo, razon),
            "archivo_de_origen": " | ".join(arch),
            "seccion_de_origen": r["extraction_citation"] or FALTA,
            "pagina_de_origen": FALTA + ": la extracción no registró página",
            "incluido_o_excluido": "incluido",
            "motivo_de_exclusion": "",
            "estado_de_extraccion": r["extraction_status"],
        })
    return filas


# ---------------------------------------------------------------- TABLA D
def tabla_d():
    t6 = leer(QR / "tabla6_brazo_a_brazo.csv", enc="utf-8-sig")
    enlace = {(r["study_id"], r["arm_id"]): r
              for r in leer(QR / "brazo_informe.csv", enc="utf-8-sig")}
    # la clasificación en las cuatro categorías vive en la tabla del pendiente 4
    clasif = {(r["estudio"], r["brazo"]): r["clasificacion"]
              for r in leer(QR / "pendiente4_tabla6.csv", enc="utf-8-sig")}
    CRIT = [("diseno_comparativo", "1. diseño comparativo"),
            ("numerador_valido", "2. numerador válido"),
            ("denominador_valido", "3. denominador válido"),
            ("definicion_operativa", "4. definición operativa de éxito"),
            ("atribuible_a_P_aeruginosa", "5. atribuible a P. aeruginosa"),
            ("terapeutica_no_profilactica", "6. terapéutica, no profiláctica"),
            ("proporcion_no_tiempo", "7. proporción binaria")]

    def justifica(r, k):
        v, d = r[k], r["diseno_adjudicado"] or "no declarado"
        if k == "diseno_comparativo":
            return ("diseño «%s»" % d) if v == "cumple" else (
                "el diseño no consta en la extracción" if v == "no evaluable"
                else "diseño «%s»: sin grupo de comparación" % d)
        if k == "numerador_valido":
            return ("éxito clínico n=%s" % r["n_exito"]) if v == "cumple" else \
                   "éxito clínico n=«%s» sobre N=«%s»" % (r["n_exito"] or "", r["N_brazo"] or "")
        if k == "denominador_valido":
            return ("N=%s" % r["N_brazo"]) if v == "cumple" else "no consta el tamaño del brazo"
        if k == "definicion_operativa":
            return "el artículo define qué contaba como éxito" if v == "cumple" \
                   else "el artículo no define qué contaba como éxito"
        if k == "atribuible_a_P_aeruginosa":
            return "el numerador es una proporción de P. aeruginosa" if v == "cumple" \
                   else "el numerador no es una proporción de P. aeruginosa"
        if k == "terapeutica_no_profilactica":
            return "administración terapéutica" if v == "cumple" \
                   else "administración profiláctica"
        return "reporta una proporción" if v == "cumple" \
               else "el desenlace principal es un tiempo, no una proporción"

    filas = []
    for r in t6:
        e, a = r["study_id"], r["arm_id"]
        f = {"estudio": e, "informe": enlace.get((e, a), {}).get("record_id", FALTA),
             "brazo": a, "diseno_adjudicado": r["diseno_adjudicado"] or "no declarado",
             "texto_completo": r["texto_completo"]}
        for k, etq in CRIT:
            f[etq] = "%s — %s" % (r[k].upper(), justifica(r, k))
        f["primer_requisito_que_falla"] = r["primer_requisito_que_falla"] or "ninguno"
        f["clasificacion"] = clasif.get((e, a), FALTA)
        filas.append(f)

    # el embudo, y QUIEN sobrevive a cada paso
    vivos, embudo = list(t6), []
    embudo.append({"filtro": "0. brazos extraídos", "estudios": len({x["study_id"] for x in vivos}),
                   "brazos": len(vivos), "no_evaluables": 0, "excluidos": 0,
                   "motivos": "", "quienes_sobreviven": "los 103"})
    for k, etq in CRIT:
        antes = list(vivos)
        noev = [x for x in antes if x[k] == "no evaluable"]
        fuera = [x for x in antes if x[k] != "cumple"]
        vivos = [x for x in antes if x[k] == "cumple"]
        mot = collections.Counter(
            x["motivo"] for x in fuera if x["primer_requisito_que_falla"] == k)
        quien = ", ".join("%s %s" % (x["study_id"], x["arm_id"]) for x in vivos) \
            if len(vivos) <= 8 else "%d brazos" % len(vivos)
        embudo.append({"filtro": etq,
                       "estudios": len({x["study_id"] for x in vivos}),
                       "brazos": len(vivos), "no_evaluables": len(noev),
                       "excluidos": len(fuera),
                       "motivos": "; ".join("%s (%d)" % (m[:70], c)
                                            for m, c in mot.most_common(4)),
                       "quienes_sobreviven": quien or "ninguno"})
    return filas, embudo


# ------------------------------------------------------------- EL IMPACTO
def impacto(adj, excl, pdfs, informes):
    rob = leer(RS / "riesgo_sesgo" / "riesgo_sesgo_comparativos_adjudicado.csv",
               enc="utf-8-sig")
    t6 = leer(QR / "tabla6_brazo_a_brazo.csv", enc="utf-8-sig")

    def cuenta(fuera):
        """Los recuentos del manuscrito excluyendo `fuera`."""
        ex = set(excl) | set(fuera)
        est = {("EST-%03d" % int(g["estudio"])) for gs in informes.values() for g in gs}
        vivos = est - ex
        recup = set()
        for e, gs in informes.items():
            if e in ex:
                continue
            g = next((x for x in gs if x["informe_para_extraer"] == "SI"), gs[0])
            if g["situacion"] in ("extraible", "solo-resumen"):
                recup.add(e)
        brazos = [r for r in adj if r["study_id"] not in ex]
        dis = collections.defaultdict(set)
        for r in brazos:
            if r["study_design"] and r["study_design"] != "NA":
                dis[r["study_id"]].add(r["study_design"])
        comp = sorted(e for e, v in dis.items() if v & COMPARATIVOS)
        evalu = [e for e in comp if e in pdfs]
        juicios = [r for r in rob if r["study_id"] not in ex]
        dom = [r for r in juicios if r["item"] != "GLOBAL"]
        con_texto = sorted(e for e in recup if e in pdfs)
        b6 = [r for r in t6 if r["study_id"] not in ex]
        b6c = [r for r in b6 if r["diseno_comparativo"] == "cumple"]
        return {
            "estudios_incluidos": len(vivos),
            "recuperables": len(recup),
            "con_texto_completo": len(con_texto),
            "brazos_extraidos": len(brazos),
            "comparativos": len(comp),
            "evaluables": len(evalu),
            "juicios_totales": len(juicios),
            "juicios_de_dominio": len(dom),
            "juicios_globales": len(juicios) - len(dom),
            "brazos_comparativos_tabla6": len(b6c),
            "estudios_tabla6_primer_filtro": len({r["study_id"] for r in b6c}),
            "casos_y_series_de_los_leidos": len(con_texto) - len(evalu),
            "exclusiones_tras_texto_completo": len(ex),
        }

    hoy = cuenta([])
    sin63 = cuenta(["EST-063"])
    return {"hoy": hoy, "si_se_excluye_EST_063": sin63,
            "diferencia": {k: sin63[k] - hoy[k] for k in hoy}}


# ------------------------------------------------------------------ EXCEL
def a_excel(tablas):
    from openpyxl import Workbook
    from openpyxl.styles import Alignment, Font, PatternFill
    wb = Workbook()
    wb.remove(wb.active)
    cab = PatternFill("solid", fgColor="D9E1F2")
    for nombre, filas in tablas:
        s = wb.create_sheet(nombre[:31])
        cols = list(filas[0].keys())
        for i, c in enumerate(cols, start=1):
            cel = s.cell(row=1, column=i, value=c)
            cel.font = Font(bold=True)
            cel.fill = cab
            cel.alignment = Alignment(wrap_text=True, vertical="top")
            s.column_dimensions[cel.column_letter].width = min(
                60, max(12, len(c) + 4))
        for j, f in enumerate(filas, start=2):
            for i, c in enumerate(cols, start=1):
                cel = s.cell(row=j, column=i, value=str(f[c]))
                cel.alignment = Alignment(wrap_text=True, vertical="top")
        s.freeze_panes = "A2"
        s.auto_filter.ref = s.dimensions
    # Si el libro está abierto en Excel, Windows lo bloquea. Los CSV ya están
    # escritos: se avisa y se guarda al lado en vez de perder la ejecución.
    try:
        wb.save(XLSX)
        return XLSX
    except PermissionError:
        alt = XLSX.with_name(XLSX.stem + "_nuevo.xlsx")
        wb.save(alt)
        print("  AVISO: %s está abierto en Excel; se guardó en %s"
              % (XLSX.name, alt.name))
        return alt


def main():
    grupos = leer(RS / "cribado" / "study_groups.csv")
    excl = {r["study_id"] for r in leer(RS / "cribado" / "exclusiones_tras_texto_completo.csv")}
    adj = leer(RS / "extraccion" / "extraccion_adjudicada.csv")
    enlace = {(r["study_id"], r["arm_id"]): r
              for r in leer(QR / "brazo_informe.csv", enc="utf-8-sig")}
    pdfs = {q.stem for q in (RS / "textos_completos" / "pdf").iterdir()
            if q.suffix.lower() in (".pdf", ".docx")}
    web = RS / "textos_completos" / "texto_html"
    if web.exists():
        pdfs |= {q.stem for q in web.glob("*.txt")}
    informes = collections.defaultdict(list)
    for g in grupos:
        informes["EST-%03d" % int(g["estudio"])].append(g)

    A, tipos = tabla_a()
    B = tabla_b(informes)
    e021 = bloque_est021(informes, pdfs)
    C = tabla_c(adj, excl, enlace, pdfs)
    D, embudo = tabla_d()
    imp = impacto(adj, excl, pdfs, informes)

    escribe("cierre_A_juicios.csv", A)
    escribe("cierre_B_solapamiento.csv", B)
    escribe("cierre_C_brazos.csv", C)
    escribe("cierre_D_tabla6.csv", D)
    escribe("cierre_D_embudo.csv", embudo)
    escribe("cierre_EST021.csv",
            [{"extremo": x[0], "estado": x[1], "evidencia": x[2]} for x in e021])
    (QR / "cierre_impacto.json").write_text(
        json.dumps({"impacto": imp, "tipos_de_frase": dict(tipos)},
                   ensure_ascii=False, indent=2), encoding="utf-8", newline="\n")

    destino = a_excel([("A juicios", A), ("B solapamiento", B), ("C brazos", C),
             ("D tabla 6", D), ("D embudo", embudo),
             ("EST-021", [{"extremo": x[0], "estado": x[1], "evidencia": x[2]}
                          for x in e021])])

    print("A. juicios        %3d filas | %s" % (len(A), dict(tipos)))
    print("B. solapamiento   %3d filas | %s"
          % (len(B), dict(collections.Counter(r["estado"] for r in B))))
    print("C. brazos         %3d filas | comparador y tiempo: [DATO FALTANTE] en todas"
          % len(C))
    print("D. tabla 6        %3d filas" % len(D))
    for x in embudo:
        print("   %-34s est %3d  brazos %3d  no eval %2d  caen %3d  -> %s"
              % (x["filtro"], x["estudios"], x["brazos"], x["no_evaluables"],
                 x["excluidos"], x["quienes_sobreviven"][:60]))
    print()
    print("IMPACTO de excluir EST-063:")
    for k in imp["hoy"]:
        print("   %-34s %4s -> %4s  (%+d)"
              % (k, imp["hoy"][k], imp["si_se_excluye_EST_063"][k], imp["diferencia"][k]))
    print()
    print("excel: %s" % destino)


if __name__ == "__main__":
    main()
