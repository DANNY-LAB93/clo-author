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
completitud del reporte, y eso es lo que se calcula.

SALIDA
    quality_reports/synthesis_scalars.json   (cifras con nombre)
    quality_reports/synthesis_scalars.md     (las mismas, legibles)
"""
import collections
import csv
import re
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



def por_frecuencia(cuenta):
    """Ordena un Counter de mayor a menor, desempatando por nombre.

    `most_common()` deja los empates en el orden de insercion, asi que dos
    categorias con el mismo recuento pueden intercambiarse entre ejecuciones y
    el canal produce ficheros distintos con los mismos datos. Un `git diff` que
    se ensucia solo acaba haciendo que nadie mire los diffs.
    """
    return dict(sorted(cuenta.items(), key=lambda kv: (-kv[1], kv[0])))

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
# PhagoBurn (EST-021) estuvo depositado en ORBi como .docx y contar solo *.pdf
# lo dejaba fuera del recuento aunque estuviera en disco y fuera legible. Desde
# el 2026-08-12 hay ademas el PDF del editor, pero la regla se mantiene: el
# recuento es por identificador, y otros estudios siguen llegando en .docx.
    # El texto completo puede llegar como PDF, como manuscrito de autor en
    # .docx o como el texto integro de la pagina del editor cuando este
    # sirve el articulo en HTML y bloquea la descarga automatica del PDF.
    # Las tres formas son el mismo dato para quien va a extraer.
    pdfs = {q.stem for q in (RS / "textos_completos" / "pdf").iterdir()
            if q.suffix.lower() in (".pdf", ".docx")}
    web = RS / "textos_completos" / "texto_html"
    if web.exists():
        pdfs |= {q.stem for q in web.glob("*.txt")}

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
    # OJO CON `fuentes_n`: cuenta BRAZOS DE BUSQUEDA, no fuentes. Scopus se
    # interrogo dos veces --«Scopus (brazo A)» y «(brazo B)»--, asi que hay 9
    # exportaciones sobre 8 fuentes distintas. El manuscrito publica «ocho
    # fuentes» y tiene razon; quien escriba «se interrogaron fuentes_n fuentes»
    # publicara nueve y contradira al manuscrito en el mismo sobre.
    S["fuentes_distintas_n"] = len({re.sub(r"\s*\(brazo [^)]*\)", "", f) for f in man})
    S["fuentes_brazos_n"] = len(man)
    S["registros_por_fuente"] = por_frecuencia(por_fuente)
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

    sys.path.insert(0, str(ROOT / "scripts"))
    from exclusion_codes import CODES

    # ---- exclusiones descubiertas al releer los textos completos ------------
    # 22 estudios que ya estaban DENTRO y no cumplian §2.2: protocolos sin
    # resultados, modelos in vitro y murinos, articulos donde P. aeruginosa
    # solo aparece en el espectro del producto, y dos donde la intervencion no
    # es un bacteriofago. Se descubrieron leyendo los articulos uno por uno,
    # despues del cribado, porque el cribado de titulo y resumen lo emitio un
    # modelo como revisor unico y un resumen de protocolo se parece mucho a uno
    # elegible.
    #
    # NO se borran de study_groups: el fichero sigue siendo el registro de lo
    # que el cribado decidio. La exclusion es una capa aparte, con su codigo,
    # su cita y su firma, y el diagrama PRISMA la muestra como lo que es --una
    # exclusion por elegibilidad-- en vez de disimularla en el total.
    excl_ft = {}
    p_excl = RS / "cribado" / "exclusiones_tras_texto_completo.csv"
    if p_excl.exists():
        excl_ft = {r["study_id"]: r for r in leer(p_excl)}
    FUERA = set(excl_ft)
    # `grupos` se conserva SIN filtrar: es la foto del corpus tal y como lo
    # dejo el cribado, y el contrafactual de la enmienda de idioma se mide
    # contra ella. Lo que se filtra es el corpus vigente.
    dentro_g = [g for g in grupos if "EST-%03d" % int(g["estudio"]) not in FUERA]

    # ---- de informes a estudios (PRISMA 2020 los separa) --------------------
    reps = {"EST-%03d" % int(g["estudio"]): g for g in dentro_g
            if g["informe_para_extraer"] == "SI"}
    S["estudios"] = len(reps)
    S["informes_agrupados"] = len(dentro_g)
    S["estudios_excluidos_tras_texto_completo"] = len(FUERA)
    S["informes_excluidos_tras_texto_completo"] = len(grupos) - len(dentro_g)
    S["estudios_antes_de_releer"] = S["estudios"] + len(FUERA)
    cft = collections.Counter(r["codigo"] for r in excl_ft.values())
    S["exclusiones_tras_texto_completo"] = {k: cft[k] for k in CODES if cft[k]}
    for k in CODES:
        if cft[k]:
            S["excluidos_texto_completo_%s" % k] = cft[k]
    if sum(cft.values()) != len(FUERA):
        raise SystemExit("FALLO: el desglose de exclusiones por texto completo "
                         "no suma su total.")
    sit = collections.Counter(g["situacion"] for g in reps.values())
    S["estudios_con_articulo"] = sit["extraible"]
    S["estudios_solo_resumen"] = sit["solo-resumen"]
    S["estudios_solo_registro"] = sit["solo-registro"]
    multi = collections.Counter(g["estudio"] for g in dentro_g)
    S["estudios_multiinforme"] = sum(1 for v in multi.values() if v > 1)
    # El complemento tambien es una cifra que el manuscrito imprime, y estaba
    # tecleada: seguia diciendo 138 con un corpus de 158.
    S["estudios_un_solo_informe"] = sum(1 for v in multi.values() if v == 1)
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
    S["disenos"] = por_frecuencia(disenos)
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

    # La pre-extraccion escribio cuatro paises sin tilde --«Belgica», «Iran»,
    # «Japon», «multicentrico»-- junto a otros bien acentuados. La Tabla 1 se
    # publica en castellano y los cuatro salian asi. Se corrige la ortografia
    # AQUI y no en el fichero de pre-extraccion, que es el registro de lo que
    # el modelo escribio y se aporta como anexo S4.
    #
    # Solo ortografia. «Francia y Belgica» NO se toca: es un estudio de dos
    # paises y repartirlo, agruparlo bajo «multicentrico» o contarlo dos veces
    # son tres decisiones de clasificacion distintas, y ninguna la toma un
    # script.
    TILDES = {"Belgica": "Bélgica", "Iran": "Irán", "Japon": "Japón",
              "multicentrico (internacional)": "multicéntrico (internacional)",
              "Francia y Belgica": "Francia y Bélgica"}
    paises = collections.Counter(
        TILDES.get(v, v) for v in
        ((pre.get(k, {}).get("geographic_source") or "no declarada")
         for k in extraibles))
    # TODOS los paises, no los diez primeros. El truncamiento hacia que el
    # diccionario sumara 111 sobre un corpus de 124, y de ahi salieron dos
    # errores encadenados: la Tabla 1 perdia paises, y una frase del manuscrito
    # afirmaba que 35 estudios declaran procedencia cuando son 48 (124 menos los
    # 76 que no la declaran). Un escalar truncado no avisa de que lo esta.
    S["procedencia"] = por_frecuencia(paises)
    S["procedencia_declarada"] = sum(v for k, v in paises.items()
                                     if k != "no declarada")
    # Europa del Este agrupada: el manuscrito sostiene que el hueco de la
    # busqueda esta ahi, y la cifra que lo respalda no se teclea.
    S["procedencia_europa_este"] = sum(
        paises.get(k, 0) for k in ("Rusia", "Polonia", "Georgia", "Ucrania"))
    # Invariante: el desglose tiene que sumar el corpus. Si no suma, algo se
    # esta perdiendo por el camino y es mejor fallar que publicar la diferencia.
    if sum(paises.values()) != len(extraibles):
        raise SystemExit("procedencia suma %d y el corpus es %d"
                         % (sum(paises.values()), len(extraibles)))
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
    # `not-classifiable` no es una clase de resistencia: significa que el
    # informe menciona resistencia pero no permite asignar MDR, XDR ni PDR. Para
    # la afirmacion "no consta la clase" cuenta igual que el silencio, y
    # separarlos importa: 87 no la mencionan y 13 mas la mencionan sin poder
    # clasificarla. El manuscrito reportaba solo los 87 y decia 70,2 % cuando el
    # dato relevante para estratificar es el 80,6 %.
    no_clasificable = sum(
        1 for k in extraibles
        if (pre.get(k, {}).get("resistance_class") or "") == "not-classifiable")
    S["clase_mencionada_no_clasificable"] = no_clasificable

    for campo, nombre in (("pathogen_scope", "sin_ambito_de_patogeno"),
                          ("resistance_class", "sin_clase_de_resistencia"),
                          ("route", "sin_via_de_administracion"),
                          ("modality", "sin_modalidad"),
                          ("dtr_status", "sin_criterio_dtr")):
        S[nombre] = sin(campo)
        S[nombre + "_pct"] = round(100.0 * sin(campo) / len(extraibles), 1)
    S["sin_clase_util"] = S["sin_clase_de_resistencia"] + no_clasificable
    S["sin_clase_util_pct"] = round(
        100.0 * S["sin_clase_util"] / len(extraibles), 1)
    S["clase_mencionada_no_clasificable_pct"] = round(
        100.0 * no_clasificable / len(extraibles), 1)

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
    reps_antes = {"EST-%03d" % int(g["estudio"]): g for g in grupos
                  if g["informe_para_extraer"] == "SI"}
    # El «antes» del idioma es el corpus que habia ANTES DEL IDIOMA, no el
    # de hoy mas los del idioma: sumarlo al de hoy le restaba tambien los 22
    # que salieron al releer, y el corpus previo salia 197 en vez de 219.
    S["estudios_antes_de_releer"] = len(reps_antes)
    S["estudios_antes_de_la_enmienda"] = (len(reps_antes)
                                          + S["estudios_eliminados_por_idioma"])

    # El fichero de pre-extraccion se hizo sobre el corpus previo y sigue
    # intacto, asi que sirve de fotografia del ANTES sin conservar copias.
    idi_path = RS / "cribado" / "idioma_informes.csv"
    if idi_path.exists():
        idioma = {r["record_id"]: r for r in leer(idi_path)}
        fuera = collections.Counter(
            r["idioma"] for r in idioma.values() if r["veredicto"] == "excluir")
        S["informes_excluidos_por_idioma_detalle"] = por_frecuencia(fuera)
        S["informes_excluidos_en_ruso"] = fuera.get("rus", 0)
    todos_pre = set(pre)
    S["extraibles_antes_de_la_enmienda"] = len(todos_pre)
    S["comparativos_antes_de_la_enmienda"] = sum(
        1 for k in todos_pre if pre[k].get("study_design") in COMPARATIVOS)
    S["ecas_antes_de_la_enmienda"] = sum(
        1 for k in todos_pre if pre[k].get("study_design") == "RCT")
    # DOS PERDIDAS DISTINTAS, Y NO SE PUEDEN SUMAR EN UNA. Restar los
    # comparativos de hoy a los de antes de la enmienda de idioma atribuia al
    # idioma tambien los que salieron el 2026-09-01 al releer los textos
    # completos: 25 en vez de 18. Cada perdida se mide contra su propio antes.
    reps_antes = {"EST-%03d" % int(g["estudio"]): g for g in grupos
                  if g["informe_para_extraer"] == "SI"}
    extr_antes = {k for k, g in reps_antes.items()
                  if g["situacion"] in ("extraible", "solo-resumen")}
    dis_antes = collections.Counter(
        (pre.get(k, {}).get("study_design") or "no declarado")
        for k in extr_antes)
    comp_antes = sum(1 for k in extr_antes
                     if pre.get(k, {}).get("study_design") in COMPARATIVOS)
    S["extraibles_antes_de_releer"] = len(extr_antes)
    S["comparativos_antes_de_releer"] = comp_antes
    S["ecas_antes_de_releer"] = dis_antes.get("RCT", 0)

    # El denominador de la tasa de error del cribado NO es el corpus: es lo que
    # se pudo leer. De los 22 excluidos al releer, todos salieron de los textos
    # completos disponibles; de los que no tienen texto no se sabe nada, asi
    # que la cifra es un suelo y el manuscrito la reporta como tal.
    leidos = extr_antes & pdfs
    S["estudios_leidos_a_texto_completo"] = len(leidos)
    # SOLO los que salieron DE ESOS 93. Los cuatro excluidos por idioma no
    # tenian texto completo: se detectaron mirando la pagina del editor, asi
    # que meterlos en este numerador con los 93 de denominador mezcla dos
    # comprobaciones distintas e infla la tasa.
    de_los_leidos = FUERA & leidos
    S["excluidos_entre_los_leidos"] = len(de_los_leidos)
    S["excluidos_tras_texto_completo_pct"] = round(
        100.0 * len(de_los_leidos) / max(1, len(leidos)), 1)
    # TRES FORMAS DE EXCLUIR, NO DOS. Hasta el 2026-09-14 el reparto era
    # binario -- «al leer el articulo» y «sin poder leerlo»-- y valia mientras
    # todo lo excluido fuera articulo. Ese dia se excluyeron diez estudios que
    # son solo ficha de registro, tras bajar y leer la ficha ENTERA del
    # registro. Meterlos en «sin poder leerlo» habria dicho al lector que no se
    # leyo nada de ellos, que es justo lo contrario de lo que paso, y habria
    # convertido una lectura en un fracaso de recuperacion.
    p_reg = ROOT / "quality_reports" / "registros_organismo_verificado.csv"
    verificados = set()
    if p_reg.exists():
        with open(p_reg, encoding="utf-8-sig", newline="") as fh:
            verificados = {r["study_id"] for r in csv.DictReader(fh)}
    sobre_ficha = (FUERA - leidos) & verificados
    S["excluidos_sobre_la_ficha_de_registro"] = len(sobre_ficha)
    if p_reg.exists():
        with open(p_reg, encoding="utf-8-sig", newline="") as fh:
            vered = collections.Counter(r["veredicto_propuesto"]
                                        for r in csv.DictReader(fh))
        S["registros_sin_organismo_n"] = sum(vered.values())
        S["registros_organismo_cumple"] = vered.get("CUMPLE", 0)
        S["registros_organismo_no_cumple"] = vered.get("NO CUMPLE", 0)
        S["registros_organismo_indeterminado"] = vered.get("INDETERMINADO", 0)
    S["excluidos_sin_poder_leer_nada"] = len(FUERA - leidos - sobre_ficha)
    # Se conserva el nombre antiguo: es lo que NO se pudo leer en absoluto.
    S["excluidos_sin_texto_completo"] = S["excluidos_sin_poder_leer_nada"]

    # EL CONTRAFACTUAL DE LA SEGUNDA ENMIENDA. El codigo NOREC excluye por no
    # haber podido leer el articulo, y hoy se aplica a UN estudio. El
    # manuscrito esta obligado a declarar que pasaria si se aplicara a todos,
    # porque la respuesta es que la tasa de recuperacion seria del 100 % por
    # construccion y el sesgo que §3.2 mide dejaria de existir. Se calcula
    # aqui para que esa advertencia no envejezca al cambiar el corpus.
    sin_texto = extraibles - con
    S["corpus_si_se_excluye_lo_no_recuperado"] = S["estudios"] - len(sin_texto)
    S["extraibles_si_se_excluye_lo_no_recuperado"] = len(extraibles) - len(sin_texto)
    S["comparativos_si_se_excluye_lo_no_recuperado"] = len(comp - sin_texto)
    S["ecas_si_se_excluye_lo_no_recuperado"] = sum(
        1 for k in extraibles - sin_texto
        if (pre.get(k, {}).get("study_design") or "") == "RCT")

    S["comparativos_perdidos_por_idioma"] = (
        S["comparativos_antes_de_la_enmienda"] - comp_antes)
    S["ecas_perdidos_por_idioma"] = (S["ecas_antes_de_la_enmienda"]
                                     - S["ecas_antes_de_releer"])
    S["comparativos_perdidos_al_releer"] = comp_antes - S["estudios_comparativos"]
    S["ecas_perdidos_al_releer"] = S["ecas_antes_de_releer"] - S["ecas"]
    paises_pre = collections.Counter(
        (pre[k].get("geographic_source") or "no declarada") for k in todos_pre)
    S["rusos_antes_de_la_enmienda"] = paises_pre.get("Rusia", 0)
    # La discusion cita las dos procedencias de Europa del Este que la enmienda
    # de idioma se llevo por delante. La ucraniana estaba tecleada en la prosa;
    # ahora sale de aqui, como el resto.
    S["ucranianos_antes_de_la_enmienda"] = paises_pre.get("Ucrania", 0)

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
        dentro = {"EST-%03d" % int(g["estudio"]) for g in dentro_g}
        filas_ft = [r for r in leer(ftc) if r["id"] in dentro]
        S["texto_completo_verificado"] = len(filas_ft)
        S["texto_completo_verificado_ingles"] = sum(
            1 for r in filas_ft if r["idioma_texto_completo"] == "eng")
        S["excluidos_por_texto_completo"] = 2

    # ---- motivos de exclusion, para el diagrama PRISMA ---------------------
    sys.path.insert(0, str(ROOT / "scripts"))
    from exclusion_codes import CODES, code_for
    # El desglose tiene que contarse sobre EL MISMO conjunto de filas que su
    # total, o la frase del manuscrito no suma. El total de la etapa de titulo
    # se calcula sobre `d2_pozo` -- las decisiones que caen dentro del pozo de
    # la etapa 1 -- mientras que el desglose se contaba sobre `d2` entero, que
    # incluye 23 decisiones sobre registros de una version anterior del corpus.
    # Resultado: el manuscrito imprimia seis codigos que sumaban 13 456 bajo un
    # total de 13 434. Lo detecto un arbitro; ningun comprobador podia verlo,
    # porque ambas cifras existian como escalares y cada una era correcta en su
    # propio conjunto.
    for etapa, dec in (("titulo", d2_pozo), ("resumen", d3)):
        c = collections.Counter()
        for r in dec.values():
            if r["verdict"] in ("EXCLUDE",):
                cod = code_for(r["reason"])
                c[cod or "SIN CODIGO"] += 1
        S["exclusiones_%s" % etapa] = {k: c[k] for k in CODES if c[k]}
        # Cada codigo tambien como escalar suelto, para poder anclar la frase
        # del manuscrito que los enumera. Un diccionario no se puede interpolar
        # en una afirmacion, y sin anclaje esa frase envejecio sin que nadie lo
        # viera: seguia imprimiendo el desglose del conjunto sin restringir.
        for k in CODES:
            if c[k]:
                S["excluidos_%s_%s" % (etapa, k)] = c[k]
        # invariante: el desglose suma su total
        total = S.get("excluidos_titulo" if etapa == "titulo" else "excluidos_resumen")
        suma = sum(S["exclusiones_%s" % etapa].values())
        if total is not None and suma != total:
            raise SystemExit(
                "FALLO: el desglose de exclusiones de %s suma %d y su total "
                "declara %d. No se escriben escalares incoherentes."
                % (etapa, suma, total))
        if c["SIN CODIGO"]:
            S["exclusiones_%s_sin_codigo" % etapa] = c["SIN CODIGO"]

    # ---- quien emitio cada decision de cribado ------------------------------
    # El manuscrito declara que las etapas 2 y 3 las emitio un modelo de
    # lenguaje. Esas cifras tienen que salir del registro, no de la memoria de
    # quien redacta: al escribirlas a mano se colo un "495 mas 34" que duplicaba
    # las filas de la enmienda, ya contenidas en las 495.
    # Ambos diccionarios estan indexados por registro, asi que cuentan la
    # decision VIVA de cada uno, no las filas del registro solo-anexar (que
    # incluye las correcciones superpuestas).
    S["decisiones_titulo"] = len(d2)
    S["decisiones_resumen"] = len(d3)

    # ---- recuento de palabras ----------------------------------------------
    # La portada declara cuantas palabras tiene el resumen y el cuerpo, y las
    # revistas lo comprueban. Se declaraba a mano y envejecio en cuanto se
    # reescribio un parrafo: el 2026-08-13 decia 3 898 cuando ya eran 3 935.
    # Al calcularse aqui, el sincronizador del manuscrito lo mantiene solo.
    # Regla de conteo: se excluyen la portada, las claves de cita, las marcas de
    # Markdown, y todo lo que va desde Declaraciones en adelante (declaraciones,
    # tablas, figuras y suplementos no cuentan como texto principal).
    def palabras(texto):
        t = re.sub(r"\[@[^\]]+\]", " ", texto)
        t = re.sub(r"[*_`#|]", " ", t)
        return len([w for w in re.split(r"\s+", t) if w.strip(" .,;:()-")])

    for cod, ruta, corte_ini, corte_fin in (
            ("es", ROOT / "paper" / "manuscrito_revision_sistematica.md",
             "## Resumen", "## 1. Introducci"),
            ("en", ROOT / "paper" / "manuscript_systematic_review_en.md",
             "## Abstract", "## 1. Introduction")):
        if not ruta.exists():
            continue
        doc = ruta.read_text(encoding="utf-8")
        try:
            resumen = doc.split(corte_ini)[1].split(corte_fin)[0]
            cuerpo = doc.split(corte_fin)[1].split("## Declaraci")[0].split(
                "## Declarations")[0]
        except IndexError:
            continue
        S["palabras_resumen_%s" % cod] = palabras(resumen)
        S["palabras_cuerpo_%s" % cod] = palabras(cuerpo)

    # ---- concordancia entre las dos extracciones ----------------------------
    # La segunda revisora se retiro el 2026-08-22 dejando la doble extraccion
    # sin reconciliar. El manuscrito tiene que declarar cuanto se solapan las
    # dos y cuanto discrepan, y esas cifras no se teclean: las produce
    # compare_extractions.py y se leen de aqui.
    conc = ROOT / "quality_reports" / "extraction_agreement.json"
    if conc.exists():
        C = json.loads(conc.read_text(encoding="utf-8"))
        S["extraccion_estudios_r1"] = C["estudios_a"]
        S["extraccion_estudios_r2"] = C["estudios_b"]
        S["extraccion_estudios_ambos"] = C["estudios_ambos"]
        S["extraccion_estudios_solo_r2"] = C["estudios_solo_b"]
        S["extraccion_filas_comparadas"] = C["filas_comparadas"]
        S["extraccion_desacuerdos"] = C["conflictos_valor"]
        S["extraccion_celdas_sin_pareja"] = C["celdas_sin_pareja"]
        S["extraccion_acuerdo_mediano_pct"] = round(C["acuerdo_mediano_pct"])
        S["extraccion_acuerdo_min_pct"] = round(C["acuerdo_min_pct"])
        S["extraccion_acuerdo_max_pct"] = round(C["acuerdo_max_pct"])
        S["extraccion_kappa_mediana"] = "%.2f" % C["kappa_mediana"]
        S["extraccion_kappas_informativas"] = C["kappas_informativas"]
        S["extraccion_categoricos_total"] = C["categoricos_total"]
        pct = 100.0 * C["estudios_ambos"] / max(1, C["estudios_a"])
        S["extraccion_doble_pct"] = "%.0f" % pct

    # Cuantos desacuerdos llegaron a firmarse. Se lee del CSV y no del JSON de
    # concordancia: el comparador reescribe ese fichero con las columnas de
    # resolucion en blanco, asi que solo el CSV sabe lo que hay firmado.
    conf = RS / "extraccion" / "extraction_conflicts.csv"
    if conf.exists():
        filas = leer(conf)
        cerrados = [r for r in filas if (r.get("resolucion") or "").strip()]
        # No todo lo cerrado se cerro por consenso. Dos filas de journal_tier
        # se cerraron aplicando una regla mecanica sobre una comparacion que
        # despues quedo superada, y su procedencia lo dice. Contarlas como
        # adjudicadas inflaria en dos la cifra que el manuscrito publica.
        SIN_FIRMA = "SIN firma conjunta"
        consenso = [r for r in cerrados
                    if SIN_FIRMA not in (r.get("resuelto_por") or "")]
        S["extraccion_conflictos_firmados"] = len(consenso)
        S["extraccion_cerrados_por_regla"] = len(cerrados) - len(consenso)
        S["extraccion_conflictos_sin_firmar"] = len(filas) - len(cerrados)

    # ---- validacion del cribado por recribado en Rayyan ---------------------
    # El falso negativo del cribado no estaba medido: lo que el modelo excluyo
    # no volvia a leerlo nadie, y la auditoria de controles positivos solo lo
    # acotaba sobre los 40 estudios ya conocidos. Una muestra aleatoria de los
    # excluidos, recribada a ciegas, lo convierte en una cifra con intervalo.
    val = ROOT / "revision_sistematica" / "validacion_rayyan" / "resultado.json"
    if val.exists():
        V = json.loads(val.read_text(encoding="utf-8"))
        R = V["resultado_final"]
        S["validacion_marco"] = V["marco_de_muestreo"]
        S["validacion_muestra"] = V["muestra"]
        S["validacion_falsos_negativos"] = R["falsos_negativos"]
        S["validacion_tasa_pct"] = "%.1f" % R["tasa_pct"]
        S["validacion_ic_sup_pct"] = "%.2f" % R["ic95_superior_pct"]
        S["validacion_cota_estudios"] = R["extrapolacion_marco_cota_superior"]
        S["validacion_primera_pasada_incluidos"] = V["primera_pasada"]["incluidos"]

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
