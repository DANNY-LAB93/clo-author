"""Calcula TODAS las cifras que el manuscrito puede citar, y solo esas.

POR QUE EXISTE. Un numero tecleado a mano en la prosa deja de coincidir con los
datos en cuanto los datos cambian, y nadie lo nota: este proyecto ya arrastro un
"73.0%" en Introduccion y Discusion mucho despues de que el valor real fuera
75.0%. Aqui cada cifra sale del canal, se escribe con su nombre, y el manuscrito
la cita por ese nombre.

QUE NO HACE. No inventa una sintesis de eficacia. La extraccion por duplicado de
Danny y Nataly no ha ocurrido, y 85 de los 159 estudios extraibles no tienen
texto completo, asi que ninguna proporcion de exito agrupada seria defendible.
Lo que se puede sostener hoy es la caracterizacion del cuerpo de evidencia y su
verificabilidad, y eso es lo que se calcula.

SALIDA
    quality_reports/synthesis_scalars.json   (cifras con nombre)
    quality_reports/synthesis_scalars.md     (las mismas, legibles)
"""
import collections
import csv
import json
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
RS = ROOT / "revision_sistematica"
csv.field_size_limit(200_000_000)
try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

COMPARATIVOS = {"RCT", "non-randomised trial"}
UN_SOLO_BRAZO = {"case report", "case series", "prospective cohort",
                 "retrospective cohort"}


def leer(p):
    with open(p, encoding="utf-8", newline="") as fh:
        return list(csv.DictReader(fh))


def main():
    corpus = leer(RS / "cribado" / "screening_corpus_all.csv")
    s1 = leer(RS / "cribado" / "screening_stage1_all.csv")
    d2 = {r["record_id"]: r for r in
          leer(RS / "cribado" / "screening_stage2_pool_decisions.csv")}
    d3 = {r["record_id"]: r for r in
          leer(RS / "cribado" / "screening_stage3_pool_decisions.csv")}
    grupos = leer(RS / "cribado" / "study_groups.csv")
    pre = {p["id_provisional"]: p for p in
           leer(RS / "extraccion" / "pre_extraccion_desde_resumen.csv")}
    man = json.loads((RS / "busqueda" / "sources.json").read_text(encoding="utf-8"))
# El texto completo no siempre llega en PDF: el manuscrito de autor de
# PhagoBurn esta depositado en ORBi como .docx. Contar solo *.pdf lo
# dejaba fuera del recuento aunque estuviera en disco y fuera legible.
    pdfs = {q.stem for q in (RS / "textos_completos" / "pdf").iterdir()
            if q.suffix.lower() in (".pdf", ".docx")}

    S = {}

    # ---- identificacion -----------------------------------------------------
    por_fuente = collections.Counter()
    for c in corpus:
        for f in c["sources"].split(";"):
            if f.strip():
                por_fuente[f.strip()] += 1
    # PRISMA 2020 exige separar bases bibliograficas de registros de ensayos:
    # son dos corrientes de identificacion distintas y se cuentan aparte. Un
    # informe que llega por ambas se asigna a bases, porque alli tiene registro
    # bibliografico propio; contarlo dos veces inflaria la identificacion.
    REGISTROS = {"ClinicalTrials.gov", "EudraCT", "CTIS"}
    de_bases = de_registros = 0
    for c in corpus:
        f = {x.strip() for x in c["sources"].split(";") if x.strip()}
        if f - REGISTROS:
            de_bases += 1
        elif f:
            de_registros += 1
    S["informes_de_bases"] = de_bases
    S["informes_de_registros"] = de_registros
    S["fuentes_bases_n"] = len(set(man) - REGISTROS)
    S["fuentes_registros_n"] = len(set(man) & REGISTROS)
    S["fuentes_n"] = len(man)
    S["fuentes_nombres"] = sorted(man)
    S["registros_por_fuente"] = dict(por_fuente.most_common())
    S["informes_unicos"] = len(corpus)

    # ---- cribado ------------------------------------------------------------
    # Registros identificados = filas de origen ANTES de deduplicar. Es la
    # primera casilla del diagrama PRISMA y no coincide con los informes unicos.
    S["registros_identificados"] = sum(
        int(r["n_source_records"] or 1) for r in corpus)
    S["duplicados_eliminados"] = S["registros_identificados"] - len(corpus)
    S["excluidos_etapa1"] = sum(1 for r in s1 if r["stage1"] == "EXCLUDED")
    S["cribados_por_titulo"] = sum(1 for r in s1 if r["stage1"] == "ADVANCE")
    en_pozo = {r["record_id"] for r in s1 if r["stage1"] == "ADVANCE"}
    d2_pozo = {k: v for k, v in d2.items() if k in en_pozo}
    S["excluidos_titulo"] = sum(1 for r in d2_pozo.values()
                                if r["verdict"] == "EXCLUDE")
    S["a_resumen"] = sum(1 for r in d2_pozo.values() if r["verdict"] == "ADVANCE")
    S["excluidos_resumen"] = sum(1 for r in d3.values() if r["verdict"] == "EXCLUDE")
    S["informes_a_texto_completo"] = sum(1 for r in d3.values()
                                         if r["verdict"] == "FULLTEXT")
    S["corriente_bases"] = sum(1 for r in d3.values() if r["corriente"] == "base")
    S["corriente_registros"] = sum(1 for r in d3.values()
                                   if r["corriente"] == "registro")

    # ---- de informes a estudios (PRISMA 2020 los separa) --------------------
    reps = {"EST-%03d" % int(g["estudio"]): g for g in grupos
            if g["informe_para_extraer"] == "SI"}
    S["estudios"] = len(reps)
    S["informes_agrupados"] = len(grupos)
    sit = collections.Counter(g["situacion"] for g in reps.values())
    S["estudios_con_articulo"] = sit["extraible"]
    S["estudios_solo_resumen"] = sit["solo-resumen"]
    S["estudios_solo_registro"] = sit["solo-registro"]
    multi = collections.Counter(g["estudio"] for g in grupos)
    S["estudios_multiinforme"] = sum(1 for v in multi.values() if v > 1)
    S["informes_del_estudio_mayor"] = max(multi.values())

    # ---- recuperacion de texto completo ------------------------------------
    extraibles = {k for k, g in reps.items()
                  if g["situacion"] in ("extraible", "solo-resumen")}
    S["estudios_extraibles"] = len(extraibles)
    con = extraibles & pdfs
    S["texto_completo_obtenido"] = len(con)
    S["texto_completo_no_obtenido"] = len(extraibles - con)
    S["texto_completo_pct"] = round(100.0 * len(con) / len(extraibles), 1)

    # ---- caracterizacion del cuerpo de evidencia ---------------------------
    def n_de(k):
        try:
            return int(pre.get(k, {}).get("n_arm") or 0)
        except ValueError:
            return 0

    disenos = collections.Counter(
        (pre.get(k, {}).get("study_design") or "no declarado")
        for k in extraibles)
    S["disenos"] = dict(disenos.most_common())
    comp = {k for k in extraibles
            if pre.get(k, {}).get("study_design") in COMPARATIVOS}
    S["estudios_comparativos"] = len(comp)
    S["estudios_comparativos_pct"] = round(100.0 * len(comp) / len(extraibles), 1)
    S["ecas"] = disenos.get("RCT", 0)
    S["casos_unicos"] = disenos.get("case report", 0)
    S["casos_unicos_pct"] = round(100.0 * disenos.get("case report", 0)
                                  / len(extraibles), 1)

    # El sesgo de recuperacion, medido y no supuesto: si lo no recuperado se
    # parece a lo recuperado, prescindir de ello cuesta precision; si difiere,
    # cambia la pregunta. Aqui difiere, y por eso la cifra va al manuscrito.
    S["comparativos_sin_texto"] = len(comp - con)
    S["comparativos_sin_texto_pct"] = round(
        100.0 * len(comp - con) / len(comp), 1) if comp else 0.0
    S["pacientes_declarados_con_texto"] = sum(n_de(k) for k in con)
    S["pacientes_declarados_sin_texto"] = sum(n_de(k) for k in extraibles - con)

    paises = collections.Counter(
        (pre.get(k, {}).get("geographic_source") or "no declarada")
        for k in extraibles)
    S["procedencia"] = dict(paises.most_common(10))
    S["procedencia_no_declarada"] = paises.get("no declarada", 0)
    S["procedencia_no_declarada_pct"] = round(
        100.0 * paises.get("no declarada", 0) / len(extraibles), 1)

    anios = [int(pre[k]["publication_year"]) for k in extraibles
             if (pre.get(k, {}).get("publication_year") or "").isdigit()]
    S["anio_min"] = min(anios) if anios else None
    S["anio_max"] = max(anios) if anios else None
    S["publicados_desde_2020"] = sum(1 for a in anios if a >= 2020)
    S["publicados_desde_2020_pct"] = round(
        100.0 * sum(1 for a in anios if a >= 2020) / len(anios), 1) if anios else 0

    # ---- lo que el cuerpo de evidencia NO declara --------------------------
    def sin(campo):
        return sum(1 for k in extraibles if not (pre.get(k, {}).get(campo) or ""))
    for campo, nombre in (("pathogen_scope", "sin_ambito_de_patogeno"),
                          ("resistance_class", "sin_clase_de_resistencia"),
                          ("route", "sin_via_de_administracion"),
                          ("modality", "sin_modalidad"),
                          ("dtr_status", "sin_criterio_dtr")):
        S[nombre] = sin(campo)
        S[nombre + "_pct"] = round(100.0 * sin(campo) / len(extraibles), 1)

    # ---- efecto de la enmienda de idioma -----------------------------------
    # El registro de decisiones es solo-anexar, asi que el estado ANTERIOR a la
    # enmienda se reconstruye del propio registro: basta ignorar las filas cuyo
    # motivo deriva en IDI y quedarse con la decision previa de cada informe.
    # Reconstruirlo asi, en vez de teclear las cifras de memoria, es lo que
    # permite que un revisor rehaga la comparacion sin pedirnos nada.
    sys.path.insert(0, str(ROOT / "scripts"))
    from exclusion_codes import code_for
    crudo3 = leer(RS / "cribado" / "screening_stage3_pool_decisions.csv")
    previo = {}
    for r in crudo3:
        if code_for(r.get("reason", "")) != "IDI":
            previo[r["record_id"]] = r
    ft_previo = {k for k, v in previo.items() if v["verdict"] == "FULLTEXT"}
    idi = {r["record_id"] for r in crudo3 if code_for(r.get("reason", "")) == "IDI"}
    S["enmienda_idioma_informes_excluidos"] = len(idi)

    por_est_prev = collections.defaultdict(set)
    for g in grupos:
        por_est_prev[g["clave"]].add(g["record_id"])
    # los informes excluidos por idioma ya no estan en study_groups; se
    # recuperan del pozo por su clave de estudio reconstruida
    S["informes_a_texto_completo_antes"] = len(ft_previo)
    S["estudios_eliminados_por_idioma"] = len(ft_previo) - len(
        {r for r in ft_previo if r in {g["record_id"] for g in grupos}})
    S["estudios_antes_de_la_enmienda"] = (S["estudios"]
                                          + S["estudios_eliminados_por_idioma"])

    # El fichero de pre-extraccion se hizo sobre el corpus previo y sigue
    # intacto, asi que sirve de fotografia del ANTES sin conservar copias.
    idi_path = RS / "cribado" / "idioma_informes.csv"
    if idi_path.exists():
        idioma = {r["record_id"]: r for r in leer(idi_path)}
        fuera = collections.Counter(
            r["idioma"] for r in idioma.values() if r["veredicto"] == "excluir")
        S["informes_excluidos_por_idioma_detalle"] = dict(fuera.most_common())
        S["informes_excluidos_en_ruso"] = fuera.get("rus", 0)
    todos_pre = set(pre)
    S["extraibles_antes_de_la_enmienda"] = len(todos_pre)
    S["comparativos_antes_de_la_enmienda"] = sum(
        1 for k in todos_pre if pre[k].get("study_design") in COMPARATIVOS)
    S["ecas_antes_de_la_enmienda"] = sum(
        1 for k in todos_pre if pre[k].get("study_design") == "RCT")
    S["comparativos_perdidos_por_idioma"] = (
        S["comparativos_antes_de_la_enmienda"] - S["estudios_comparativos"])
    S["ecas_perdidos_por_idioma"] = (S["ecas_antes_de_la_enmienda"] - S["ecas"])
    paises_pre = collections.Counter(
        (pre[k].get("geographic_source") or "no declarada") for k in todos_pre)
    S["rusos_antes_de_la_enmienda"] = paises_pre.get("Rusia", 0)

    # ---- verificacion de idioma, por clase de evidencia --------------------
    ver = RS / "cribado" / "idioma_verificacion.csv"
    if ver.exists():
        clases = collections.Counter(r["clase_de_evidencia"].split(".")[0]
                                     for r in leer(ver))
        S["idioma_probado_por_texto"] = clases.get("A", 0)
        S["idioma_por_campo_de_fuente"] = clases.get("B", 0)
        S["idioma_por_version_inglesa"] = clases.get("C", 0)
        S["idioma_por_norma_del_registro"] = clases.get("D", 0)
    ftc = RS / "cribado" / "idioma_texto_completo.csv"
    if ftc.exists():
        dentro = {"EST-%03d" % int(g["estudio"]) for g in grupos}
        filas_ft = [r for r in leer(ftc) if r["id"] in dentro]
        S["texto_completo_verificado"] = len(filas_ft)
        S["texto_completo_verificado_ingles"] = sum(
            1 for r in filas_ft if r["idioma_texto_completo"] == "eng")
        S["excluidos_por_texto_completo"] = 2

    # ---- motivos de exclusion, para el diagrama PRISMA ---------------------
    sys.path.insert(0, str(ROOT / "scripts"))
    from exclusion_codes import CODES, code_for
    for etapa, dec in (("titulo", d2), ("resumen", d3)):
        c = collections.Counter()
        for r in dec.values():
            if r["verdict"] in ("EXCLUDE",):
                cod = code_for(r["reason"])
                c[cod or "SIN CODIGO"] += 1
        S["exclusiones_%s" % etapa] = {k: c[k] for k in CODES if c[k]}
        if c["SIN CODIGO"]:
            S["exclusiones_%s_sin_codigo" % etapa] = c["SIN CODIGO"]

    # ---- salida -------------------------------------------------------------
    sal = ROOT / "quality_reports" / "synthesis_scalars.json"
    sal.write_text(json.dumps(S, indent=2, ensure_ascii=False) + "\n",
                   encoding="utf-8")

    L = ["# Cifras del manuscrito", "",
         "Generado por `scripts/build_synthesis_scalars.py`. **Ninguna cifra del",
         "manuscrito se teclea a mano: se cita por su nombre desde esta tabla.**", "",
         "| Nombre | Valor |", "|---|---|"]
    for k, v in S.items():
        if isinstance(v, dict):
            v = "; ".join("%s: %s" % (a, b) for a, b in v.items())
        elif isinstance(v, list):
            v = ", ".join(map(str, v))
        L.append("| `%s` | %s |" % (k, v))
    (ROOT / "quality_reports" / "synthesis_scalars.md").write_text(
        "\n".join(L) + "\n", encoding="utf-8", newline="\n")

    print("cifras calculadas: %d" % len(S))
    for k in ("informes_unicos", "cribados_por_titulo", "informes_a_texto_completo",
              "estudios", "estudios_extraibles", "texto_completo_obtenido",
              "estudios_comparativos", "comparativos_sin_texto_pct"):
        print("   %-32s %s" % (k, S[k]))
    print("escrito %s" % sal)
    return 0


if __name__ == "__main__":
    sys.exit(main())
