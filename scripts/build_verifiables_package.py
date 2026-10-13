"""Genera el paquete de verificables que un editor exige antes de publicar.

QUE ES UN VERIFICABLE. No es un anexo decorativo: es el documento que permite a
un revisor comprobar una afirmacion del manuscrito sin fiarse de ella. Por eso
cada archivo de aqui responde a un item concreto de PRISMA 2020 o a un requisito
del ICMJE, y el indice dice a cual.

FORMATO. Word para lo que el editor lee y anota (listas, ecuaciones, informes).
Excel para lo que el revisor filtra y ordena (listados de estudios, registros de
decision). PDF para las figuras, que ya salen vectoriales del generador.

SALIDA
    verificables revisión sistemática/
"""
import collections
import csv
import datetime
import json
import pathlib
import re
import shutil
import sys

from docx import Document
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.shared import Pt, Cm, RGBColor

ROOT = pathlib.Path(__file__).resolve().parent.parent
RS = ROOT / "revision_sistematica"
OUT = ROOT / "verificables revisión sistemática"
csv.field_size_limit(200_000_000)
try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass


def leer(p):
    with open(p, encoding="utf-8", newline="") as fh:
        return list(csv.DictReader(fh))


MESES = ("enero", "febrero", "marzo", "abril", "mayo", "junio", "julio",
         "agosto", "septiembre", "octubre", "noviembre", "diciembre")


def fecha_larga():
    """La fecha de HOY, no la que alguien tecleo un dia.

    El subtitulo de S1 decia «Estado a 11 de agosto de 2026» y ahi se quedo
    mientras el anexo se regeneraba: entre esa fecha y el 14 de septiembre
    entraron las 29 exclusiones tras leer los textos completos, el riesgo de
    sesgo firmado y dos cambios de titulo. Una lista de comprobacion que viaja
    a la revista fechada un mes antes de lo que declara es peor que una sin
    fecha, porque parece comprobada.
    """
    h = datetime.date.today()
    return "%d de %s de %d" % (h.day, MESES[h.month - 1], h.year)


def fecha_es(iso):
    """«2026-08-04» -> «4 de agosto de 2026». Para fechas que salen de un registro."""
    a, m, d = (int(x) for x in iso[:10].split("-"))
    return "%d de %s de %d" % (d, MESES[m - 1], a)


def miles(n):
    """13917 -> «13 917», con espacio duro, como en el manuscrito."""
    return "{:,}".format(int(n)).replace(",", " ")


def vocabulario_de_motivos():
    """Cuándo se escribieron los motivos de exclusión de la etapa de título en
    texto libre y desde cuándo con los códigos del vocabulario cerrado.

    Se calcula sobre el registro solo-anexar porque S1 y S19 decían
    «vocabulario cerrado fijado por los autores antes del cribado», y el
    registro lo desmiente: las exclusiones del primer día llevan el motivo en
    texto libre y los códigos aparecen después. Devuelve los días y el número
    de exclusiones en texto libre.
    """
    sys.path.insert(0, str(ROOT / "scripts"))
    from exclusion_codes import CODES
    textos = set(CODES.values())
    libre, codificado = collections.Counter(), collections.Counter()
    for r in leer(RS / "cribado" / "screening_stage2_pool_decisions.csv"):
        if r["verdict"] != "EXCLUDE":
            continue
        dia = (r.get("decided_at") or "")[:10]
        (codificado if r["reason"] in textos else libre)[dia] += 1
    if not libre or not codificado:
        raise SystemExit("S1/S19: el registro de título ya no mezcla motivos en "
                         "texto libre y codificados; revisa la redacción.")
    if max(libre) >= min(codificado):
        raise SystemExit("S1/S19: hay motivos en texto libre después del primer "
                         "día codificado (%s); la frase «desde el ... se usaron "
                         "los códigos» ya no se sostiene." % min(codificado))
    return {"dias_libre": sorted(libre), "n_libre": sum(libre.values()),
            "primer_dia_codigos": min(codificado)}


def auditoria_controles(S):
    """La auditoría de controles positivos, recalculada desde los datos.

    S6 tenía la tabla tecleada («40 | 40» en las tres etapas) y decía que el
    conjunto tenía 40 estudios: tiene 42 y 40 son comprobables por PMID. Aquí
    se rehace como la hacen screen_stage1_all_sources.py, screen_stage2_pool.py
    y screen_stage3_pool.py --por PMID y a nivel de estudio: un control pasa la
    etapa si conserva al menos un informe-- y se sigue a cada control hasta el
    corpus vigente, que la auditoría del cribado no hace.
    """
    idx = collections.defaultdict(set)
    for l in (ROOT / "quality_reports" / "corpus_identifier_index.txt").read_text(
            encoding="utf-8").splitlines():
        if l.strip() and not l.startswith("#"):
            i, _, s = l.partition("\t")
            idx[s.strip()].add(i.strip().lower())

    def ids_de(r):
        out = set()
        for c, pre in (("pmid", "pmid:"), ("doi", "doi:"), ("nct", "nct:")):
            for v in re.split(r"[;,\s]+", r.get(c) or ""):
                if v.strip():
                    out.add(pre + v.strip().lower())
        return out

    corpus = {r["record_id"]: ids_de(r)
              for r in leer(RS / "cribado" / "screening_corpus_all.csv")}
    registros_de = collections.defaultdict(set)
    for rid, ids in corpus.items():
        for i in ids:
            registros_de[i].add(rid)

    # Las tres etapas. El registro es solo-anexar: vale la última fila de cada
    # registro. Las filas de idioma del 11-08-2026 (decided_by «... idioma ...»)
    # corrigen filas anteriores de la etapa 3; quitándolas se obtiene el estado
    # anterior a la enmienda.
    pasa1 = {r["record_id"] for r in leer(RS / "cribado" / "screening_stage1_all.csv")
             if r["stage1"] != "EXCLUDED"}
    ult2, ult3, ult3_antes = {}, {}, {}
    for r in leer(RS / "cribado" / "screening_stage2_pool_decisions.csv"):
        ult2[r["record_id"]] = r
    for r in leer(RS / "cribado" / "screening_stage3_pool_decisions.csv"):
        ult3[r["record_id"]] = r
        if "idioma" not in r["decided_by"]:
            ult3_antes[r["record_id"]] = r
    pasa2 = {k for k, r in ult2.items() if r["verdict"] == "ADVANCE"}
    pasa3 = {k for k, r in ult3.items() if r["verdict"] == "FULLTEXT"}
    pasa3_antes = {k for k, r in ult3_antes.items() if r["verdict"] == "FULLTEXT"}

    comprobables = sorted(s for s, v in idx.items()
                          if any(i.startswith("pmid:") for i in v))
    etapas = collections.Counter()
    perdidos_enmienda, perdidos_otros, decision_enmienda = [], [], {}
    for s in comprobables:
        recs = set().union(*(registros_de.get(i, set())
                             for i in idx[s] if i.startswith("pmid:")))
        e1 = recs & pasa1
        e2 = e1 & pasa2
        etapas["e1"] += bool(e1)
        etapas["e2"] += bool(e2)
        etapas["e3_antes"] += bool(e2 & pasa3_antes)
        etapas["e3"] += bool(e2 & pasa3)
        if e2 & pasa3_antes and not e2 & pasa3:
            perdidos_enmienda.append(s)
            # la fila del registro que lo excluyó, para citarla tal cual
            decision_enmienda[s] = ult3[sorted(e2 & pasa3_antes)[0]]
        elif not e2 & pasa3:
            perdidos_otros.append(s)

    # Cada control, hasta el corpus vigente: los estudios de study_groups
    # menos las exclusiones tras el texto completo.
    grupos = leer(RS / "cribado" / "study_groups.csv")
    ids_est = collections.defaultdict(set)
    for g in grupos:
        ids_est["EST-%03d" % int(g["estudio"])] |= corpus.get(g["record_id"], set())
    excl = {r["study_id"]: r
            for r in leer(RS / "cribado" / "exclusiones_tras_texto_completo.csv")}
    estado = {}
    for s, v in sorted(idx.items()):
        est = sorted(e for e, ids in ids_est.items() if ids & v)
        dentro = [e for e in est if e not in excl]
        estado[s] = {"estudios": est, "en_corpus": bool(dentro),
                     "pmid": any(i.startswith("pmid:") for i in v),
                     "exclusion": [excl[e] for e in est if e in excl]}

    A = {"fijados": sorted(idx), "comprobables": comprobables,
         "sin_pmid": sorted(s for s in idx if s not in comprobables),
         "etapas": etapas, "perdidos_enmienda": perdidos_enmienda,
         "decision_enmienda": decision_enmienda,
         "perdidos_otros": perdidos_otros, "estado": estado,
         "en_corpus": sum(1 for e in estado.values() if e["en_corpus"])}
    # Las mismas tres cifras salen de build_auditoria_scalars.py y van al
    # manuscrito: si este recálculo no las reproduce, S6 contradiría al texto.
    for clave, valor in (("controles_fijados", len(A["fijados"])),
                         ("controles_comprobables_pmid", len(comprobables)),
                         ("controles_en_corpus", A["en_corpus"])):
        if S[clave] != valor:
            raise SystemExit("S6: %s es %s en los escalares y %s recalculado aquí."
                             % (clave, S[clave], valor))
    return A


def doc_nuevo(titulo, subtitulo=""):
    d = Document()
    est = d.styles["Normal"]
    est.font.name = "Calibri"
    est.font.size = Pt(10.5)
    for s in d.sections:
        s.top_margin = s.bottom_margin = Cm(2)
        s.left_margin = s.right_margin = Cm(2.2)
    h = d.add_heading(titulo, level=0)
    h.alignment = WD_ALIGN_PARAGRAPH.LEFT
    if subtitulo:
        p = d.add_paragraph(subtitulo)
        p.runs[0].italic = True
        p.runs[0].font.size = Pt(9.5)
    return d


def tabla(d, cabecera, filas, anchos=None):
    t = d.add_table(rows=1, cols=len(cabecera))
    t.style = "Light Grid Accent 1"
    for i, c in enumerate(cabecera):
        cel = t.rows[0].cells[i]
        cel.text = ""
        r = cel.paragraphs[0].add_run(str(c))
        r.bold = True
        r.font.size = Pt(9)
    for f in filas:
        cs = t.add_row().cells
        for i, v in enumerate(f):
            cs[i].text = ""
            r = cs[i].paragraphs[0].add_run("" if v is None else str(v))
            r.font.size = Pt(9)
    if anchos:
        for fila in t.rows:
            for i, w in enumerate(anchos):
                fila.cells[i].width = Cm(w)
    d.add_paragraph()
    return t


def nota(d, texto):
    p = d.add_paragraph()
    r = p.add_run(texto)
    r.font.size = Pt(8.5)
    r.italic = True
    r.font.color.rgb = RGBColor(0x44, 0x44, 0x44)


def estado_riesgo_de_sesgo(S):
    """Los items 11 y 18 de PRISMA, redactados desde el canal.

    Devuelve {item: (veredicto, texto)}. Si el fichero de estado no existe
    todavia, se dice eso y no se inventa un veredicto.
    """
    import json as _json
    p = ROOT / "quality_reports" / "rob_tabla_estado.json"
    if not p.exists():
        sin = ("NO CUMPLE", "No se ha evaluado. Ver §2.7.")
        return {"11": sin, "18": sin}
    R = _json.loads(p.read_text(encoding="utf-8"))
    # CORREGIDO EL 2026-10-08. Decia «POR CONSENSO entre los dos autores, no
    # por duplicado independiente» sin decir de donde salio el consenso: los
    # dos cuadernos no son independientes (el registro del 2026-09-05 concluye
    # que uno salio del otro), el cuaderno de consenso lo genero el canal con
    # los juicios coincidentes ya puestos, y los desacuerdos fueron todos hacia
    # el cuaderno de D.V. Las cifras salen de los escalares de concordancia.
    if S["rob_resueltos_hacia_r1"] == S["rob_desacuerdos"]:
        hacia = ("los %d desacuerdos se resolvieron hacia el cuaderno de D.V."
                 % S["rob_desacuerdos"])
    else:
        hacia = ("de los %d desacuerdos, %d se resolvieron hacia el cuaderno "
                 "de D.V." % (S["rob_desacuerdos"], S["rob_resueltos_hacia_r1"]))
    alcance = ("%d de los %d estudios con diseño comparativo adjudicado sobre "
               "el artículo (RoB 2 en los aleatorizados, ROBINS-I en los no "
               "aleatorizados y las cohortes), a nivel de dominio. Se declaró "
               "evaluación por consenso. Hubo dos cuadernos, uno a nombre de "
               "cada autor, sin independencia acreditada: compartían %s "
               "caracteres de notas idénticas, y el registro del 5 de "
               "septiembre de 2026 concluye que un cuaderno salió del otro. El "
               "canal que escribió el modelo de lenguaje generó el cuaderno de "
               "consenso con los juicios coincidentes precargados y los "
               "discrepantes en blanco; lo firmaron los dos autores el 9 de "
               "septiembre de 2026, y %s La concordancia (%s de %s juicios, "
               "kappa %s) no mide dos evaluaciones independientes. Los reportes "
               "y series de casos no se evalúan con instrumento formal, por "
               "decisión: §2.7 dice por qué. "
               % (R["evaluables"], R["comparativos_adjudicados"],
                  miles(S["rob_notas_identicas_caracteres"]), hacia,
                  S["rob_acuerdo_bruto"], S["rob_juicios_comparables"],
                  str(S["rob_kappa"]).replace(".", ",")))
    # Decia ademas «El estudio comparativo restante no tiene texto completo y
    # no se evalua» a continuacion de «9 de los 9»: una contradiccion en la
    # misma casilla. La frase sale ahora de sin_texto_completo y solo aparece
    # si hay alguno.
    sin_texto = R.get("sin_texto_completo", 0)
    resto = ("%d %s sin texto completo no se %s. " % (
        sin_texto,
        "estudio comparativo" if sin_texto == 1 else "estudios comparativos",
        "evalúa" if sin_texto == 1 else "evalúan") if sin_texto else "")
    if R.get("completa"):
        return {
            "11": ("CUMPLE", alcance + resto + "La limitación consta en §4.4"),
            "18": ("CUMPLE", "Tabla de dominios con los %d juicios, estudio "
                   "por estudio, en §3.7" % R["celdas_totales"]),
        }
    return {
        "11": ("PARCIAL", alcance + resto + "La evaluación está EN CURSO: faltan %d de "
               "los %d juicios. §2.7 lo declara" % (R["celdas_pendientes"],
                                                    R["celdas_totales"])),
        "18": ("NO CUMPLE", "Los juicios por estudio aún no están emitidos "
               "(faltan %d de %d). No se sustituyen por ningún indicador "
               "derivado del diseño. §2.7 y §4.4"
               % (R["celdas_pendientes"], R["celdas_totales"])),
    }


# ---------------------------------------------------------------- documentos
def v1_prisma(S):
    """Lista de comprobacion PRISMA 2020, item por item.

    Los items 11 y 18 (riesgo de sesgo) NO se redactan aqui: salen de
    `rob_tabla_estado.json`, que es el mismo fichero del que sale el
    manuscrito. Estuvieron escritos a mano diciendo "no se ha realizado"
    mientras el manuscrito ya declaraba una evaluacion en curso, y una lista
    PRISMA que contradice a su propio manuscrito es peor que no adjuntarla.

    Se marca CUMPLE / PARCIAL / NO CUMPLE y se dice donde mirar. Marcar todo
    como cumplido es la forma mas rapida de perder la confianza del editor: los
    items que esta revision no cumple, si los hay, se declaran como tales.
    """
    ROB = estado_riesgo_de_sesgo(S)
    VOC = vocabulario_de_motivos()
    CTRL = auditoria_controles(S)
    # PRISMA 16b. Decia que las exclusiones a texto completo llevaban «cada
    # una ... la frase del articulo que lo sostiene», y no es asi: las NOPDF y
    # NOREC no tienen articulo, otras filas solo traen el motivo, y EST-205 se
    # decidio sobre la indexacion de SciELO sin leer el texto. Se cuenta aqui,
    # fila a fila, sobre el mismo fichero que S16.
    EX = leer(RS / "cribado" / "exclusiones_tras_texto_completo.csv")
    if len(EX) != S["estudios_excluidos_tras_texto_completo"]:
        raise SystemExit("S1: %d exclusiones en el fichero y %d en los escalares."
                         % (len(EX), S["estudios_excluidos_tras_texto_completo"]))
    sin_articulo = collections.Counter(r["codigo"] for r in EX
                                       if r["codigo"] in ("NOPDF", "NOREC"))
    sin_cita = [r for r in EX
                if not (r["cita_del_texto"] or "").strip()
                or (r["cita_del_texto"] or "").strip().startswith("(")]
    sin_cita_resto = [r for r in sin_cita if r["codigo"] not in sin_articulo]
    solo_uno = sorted(r["study_id"] for r in EX if " y " not in r["decidido_por"])
    est205 = [r for r in EX if r["study_id"] == "EST-205"]
    if not (est205 and est205[0]["codigo"] == "REV"
            and est205[0]["cita_del_texto"].startswith("SciELO")):
        raise SystemExit("S1: EST-205 ya no es la exclusion REV decidida sobre la "
                         "indexacion de SciELO; revisa la frase del item 16b.")
    con_cita = len(EX) - len(sin_cita)
    # Las fechas de NOREC, para el item 24c: la enmienda se adopto para un
    # estudio y se aplico despues a otros. Si aparece otra fecha, la frase del
    # item ya no la cuenta y hay que reescribirla.
    norec_fecha = collections.Counter(r["fecha"][:10] for r in EX
                                      if r["codigo"] == "NOREC")
    if set(norec_fecha) != {"2026-09-02", "2026-10-06"}:
        raise SystemExit("S1: NOREC tiene fechas %s; revisa el item 24c."
                         % sorted(norec_fecha))
    d = doc_nuevo("S1. Lista de comprobación PRISMA 2020",
                  "Fagoterapia en Pseudomonas aeruginosa multirresistente. "
                  "Estado a %s." % fecha_larga())
    # A DONDE APUNTAN LAS REFERENCIAS. La columna "dónde mirar" usa la
    # numeracion del informe extendido (§2.1 a §4.4), que NO viaja en el sobre
    # de la revista: alli va el manuscrito con secciones sin numerar. Un editor
    # que siga "§2.7" no encuentra nada. La correspondencia se declara aqui, en
    # vez de dejar 27 remisiones colgando.
    d.add_heading("Cómo leer la columna «dónde mirar»", level=2)
    d.add_paragraph(
        "Las remisiones §1 a §4.4 corresponden al informe extendido. En el "
        "manuscrito enviado a la revista, cuyas secciones no van numeradas, "
        "equivalen a:")
    for a, b in (("§1", "INTRODUCCIÓN"),
                 ("§2.1", "METODOLOGÍA › Protocolo y reporte"),
                 ("§2.2", "METODOLOGÍA › Criterios de elegibilidad (Tabla 1)"),
                 ("§2.3", "METODOLOGÍA › Fuentes de información y estrategia de búsqueda"),
                 ("§2.4", "METODOLOGÍA › Selección de los estudios"),
                 ("§2.6", "METODOLOGÍA › Extracción de datos"),
                 ("§2.7", "METODOLOGÍA › Evaluación del riesgo de sesgo"),
                 ("§2.8", "METODOLOGÍA › Síntesis"),
                 ("§2.9", "METODOLOGÍA › Enmiendas al protocolo"),
                 ("§3.1 y §3.1.1", "RESULTADOS › Selección de los estudios (Figura 1)"),
                 ("§3.3", "RESULTADOS › Características del cuerpo de evidencia (Tabla 2)"),
                 ("§3.5", "RESULTADOS › Reporte de los desenlaces (Tabla 4)"),
                 ("§3.6", "RESULTADOS › Viabilidad de la síntesis cuantitativa (Tabla 6)"),
                 ("§4, §4.3 y §4.4", "DISCUSIÓN Y CONCLUSIONES")):
        d.add_paragraph("%s  →  %s" % (a, b), style="List Bullet")
    d.add_paragraph(
        "Las tablas también se renumeran entre los dos documentos: la Tabla 1 "
        "del manuscrito de la revista es la de criterios de elegibilidad, y la "
        "de características del corpus es allí la Tabla 2.")
    ITEMS = [
        ("1", "Título", "Identifica el informe como revisión sistemática", "CUMPLE", "Título"),
        ("2", "Resumen estructurado", "Ver lista PRISMA for Abstracts", "CUMPLE", "Resumen"),
        ("3", "Justificación", "Base racional en el contexto de lo conocido", "CUMPLE", "§1"),
        ("4", "Objetivos", "Pregunta explícita", "CUMPLE", "§1, último párrafo"),
        ("5", "Criterios de elegibilidad", "Y cómo se agruparon los estudios", "CUMPLE",
         "§2.2, incluido el criterio de idioma (inglés o español), verificado "
         "informe por informe en S9 y sobre el texto completo en S10"),
        # CORREGIDO EL 2026-10-08. Estaba en CUMPLE, y no hay fecha de ejecucion
        # por fuente: la ejecucion de Scopus cuya exportacion entro al corpus no
        # tiene fecha registrada.
        ("6", "Fuentes de información", "Todas, con fecha de la última búsqueda", "PARCIAL",
         "§2.3 y S2. No hay fecha de ejecución por fuente. Las ejecuciones "
         "documentadas son del 3 y el 4 de agosto de 2026, y la exportación de "
         "BVS se incorporó al corpus el 10 de agosto; la ejecución de Scopus "
         "cuya exportación entró al corpus no tiene fecha registrada (el "
         "fichero de su brazo B se terminó de escribir el 5 de agosto)"),
        ("7", "Estrategia de búsqueda", "Literal, para cada base y registro", "CUMPLE", "§2.3 y S2"),
        # CORREGIDO EL 2026-10-08. Decia «un vocabulario cerrado fijado por los
        # autores» (el registro muestra el primer dia en texto libre y no consta
        # que los autores fijaran los codigos antes), y daba como hecho, con un
        # añadido («antes de agruparlos en estudios»), lo que es una declaracion
        # de D.V.: la agrupacion la propuso un guion del modelo.
        ("8", "Proceso de selección", "Cuántos revisores, cómo trabajaron", "PARCIAL",
         "§2.4; la etapa 1 aplica reglas deterministas, y las decisiones "
         "registro a registro de las etapas 2 y 3 las emitió un modelo de "
         "lenguaje (Claude Opus 5) como revisor único, sin duplicación. El "
         "vocabulario de motivos no se fijó antes de empezar: el %s "
         % fecha_es(VOC["dias_libre"][0]) +
         "(primer día de cribado de títulos) el modelo escribió los motivos en "
         "texto libre, y los códigos, cuya redacción procede de esos textos, se "
         "usaron desde el %s; no consta que los autores los fijaran antes. Ese "
         % fecha_es(VOC["primer_dia_codigos"]) +
         "primer día se añadieron además, a mitad de lote, dos reglas que "
         "concretan los criterios: endolisinas aisladas fuera (intervención) e "
         "informes veterinarios fuera (población). D.V. fue el único revisor "
         "humano. Según declara D.V. (8 de octubre de 2026), examinó uno a uno "
         "los informes que superaron el cribado; ese examen no quedó "
         "registrado. Lo que el modelo excluyó no lo releyó ningún humano, "
         "salvo la muestra de %s del recribado (S19). Declarado en §2.4 y como "
         % S["validacion_muestra"] +
         "primera limitación en §4.4; el registro completo, con modelo y marca "
         "de tiempo por decisión, está en S3"),
        ("9", "Proceso de extracción", "Cuántos revisores, herramientas", "CUMPLE",
         "§2.6; extracción por duplicado (%d de %d "
         % (S["extraccion_estudios_ambos"], S["extraccion_estudios_r1"]) +
         "estudios), con la concordancia medida antes de resolver y %d de %d "
         % (S["extraccion_conflictos_firmados"], S["extraccion_desacuerdos"]) +
         "desacuerdos adjudicados; el registro anota a los dos revisores en %d "
         % S["conflictos_resueltos_por_los_dos"] +
         "y a uno solo en %d, y %d se cerraron por una regla mecánica sin "
         % (S["conflictos_resueltos_por_uno"], S["extraccion_cerrados_por_regla"]) +
         "firma conjunta. La independencia de las dos extracciones no está " +
         "acreditada: la columna de texto libre que localiza cada dato coincide "
         "entre los dos cuadernos en %d de %d filas, erratas incluidas. S11 y "
         % (S["extraccion_localizacion_identicas"],
            S["extraccion_localizacion_comparables"]) +
         "S12 aportan el rastro"),
        ("10a", "Variables de desenlace", "Lista y definiciones", "PARCIAL",
         "§2.2 las lista; S4 no contiene definiciones de desenlace porque "
         "ningún resumen del corpus las declara. Las definiciones de los "
         "textos completos leídos se discuten en §3.5 y §3.6"),
        ("10b", "Otras variables", "Lista y definiciones", "CUMPLE", "S4"),
        ("11", "Riesgo de sesgo", "Herramienta, cuántos revisores", ROB["11"][0],
         ROB["11"][1]),
        ("12", "Medidas del efecto", "Para cada desenlace", "NO APLICA",
         "Este informe no presenta estimaciones de efecto. §3.5 mide la completitud con que se reportan los desenlaces; §3.6 explica por qué no se agregan"),
        ("13a-f", "Métodos de síntesis", "Incluida la decisión de no agrupar", "CUMPLE",
         "§2.8 y §3.6, con la justificación de por qué no se agrupa"),
        # Desde NOPDF (2026-10-06) el corpus no tiene fichas de registro sin
        # publicacion, y la plantilla decia «§4.3 documenta 0 de 65 estudios
        # registrados sin publicación». §4.3 cuenta las que el criterio saco.
        ("14", "Sesgo de publicación", "Métodos de evaluación", "PARCIAL",
         ("§4.3 documenta %d de %d estudios registrados sin publicación; no se "
          % (S["estudios_solo_registro"], S["estudios"])
          if S["estudios_solo_registro"] else
          "§4.3 documenta que %d de los %d estudios que llegaron al criterio del "
          "texto completo eran solo fichas de registro, sin publicación "
          "localizable; el criterio los saca del corpus, no del campo. No se "
          % (S["criterio_texto_nopdf_fichas"], S["estudios_antes_de_nopdf"])) +
         "aplicaron pruebas estadísticas por no haber síntesis cuantitativa"),
        ("15", "Certeza de la evidencia", "GRADE u otro", "NO APLICA",
         "§2.7: GRADE califica la certeza de una estimación agrupada y este "
         "informe no presenta ninguna. §3.5 y la Tabla 6 muestran que, tras "
         "aplicar los criterios de elegibilidad de §2.2, NINGÚN brazo del "
         "corpus podría entrar en una proporción agrupada de éxito clínico"),
        ("16a", "Selección de estudios", "Flujo con números", "CUMPLE", "§3.1 y Figura 1"),
        # CORREGIDO EL 2026-10-08: ver el recuento de EX arriba. Decia ademas
        # que S3 trae los motivos «de las etapas 1 a 3 con vocabulario
        # cerrado»: S3 trae las etapas 2 y 3, y el primer dia en texto libre.
        ("16b", "Excluidos en texto completo", "Con motivos", "CUMPLE",
         "§3.1.1 y S16: %d estudios que el cribado había admitido se "
         % len(EX) +
         "excluyeron en la fase de texto completo, cada uno con su código de "
         "motivo. %d (NOPDF) y %d (NOREC) se excluyeron porque no se consiguió "
         % (sin_articulo["NOPDF"], sin_articulo["NOREC"]) +
         "o no se pudo leer el artículo, no porque se haya comprobado que "
         "incumplen los criterios, y no llevan cita; otros %d llevan solo el "
         % len(sin_cita_resto) +
         "motivo. Los %d restantes llevan la frase del texto leído (artículo o "
         % con_cita +
         "ficha de registro) que sostiene la exclusión, salvo EST-205 (REV), "
         "decidido sobre la indexación de SciELO sin leer el texto. Las "
         "firmaron los dos autores salvo %d, que firmó D.V. solo (%s). El "
         % (len(solo_uno), " y ".join(solo_uno)) +
         "modelo leyó los textos completos y propuso, con su cita, las "
         "exclusiones que se apoyan en ellos. S3 recoge además los motivos de "
         "las etapas 2 y 3 tal como se escribieron"),
        ("17", "Características de los estudios", "De cada uno", "CUMPLE",
         "Tabla 1, y listado completo en S5"),
        ("18", "Riesgo de sesgo por estudio", "", ROB["18"][0], ROB["18"][1]),
        ("19", "Resultados de los estudios", "", "PARCIAL",
         "§3.5 y las Tablas 5 y 6 reportan la COMPLETITUD con que cada estudio "
         "declara los cinco desenlaces, no sus estimaciones de efecto. El "
         "dato brazo a brazo se aporta en S14, y la procedencia de cada "
         "casilla en S15"),
        ("20a-d", "Resultados de la síntesis", "", "CUMPLE",
         "§3.3 a §3.6; la síntesis es de estructura y de completitud de "
         "reporte, no de eficacia, y §3.6 razona por qué no puede ser otra"),
        ("21", "Sesgos de publicación", "", "PARCIAL", "§4.3"),
        ("22", "Certeza de la evidencia", "", "NO APLICA",
         "No hay estimación agrupada cuya certeza calificar; ver §2.7 y §3.5"),
        ("23a-d", "Discusión", "Interpretación, limitaciones, implicaciones", "CUMPLE", "§4"),
        ("24a", "Registro", "Número o declaración de no registro", "CUMPLE (declarado)",
         "§2.1 declara explícitamente que NO está registrada"),
        ("24b", "Protocolo", "Dónde consultarlo", "PARCIAL",
         "Repositorio del proyecto; no depositado en registro público"),
        # CORREGIDO EL 2026-10-08. Decia «una enmienda declarada»: las
        # enmiendas de elegibilidad posteriores al cribado son varias, todas
        # declaradas. El control positivo perdido sale de auditoria_controles.
        # (2026-10-12: decia ademas «declaradas con su fecha», y el manuscrito
        # no fecha la entrada de los codigos IDI, PRO e INT; las fechas que si
        # constan van con cada enmienda.)
        ("24c", "Enmiendas", "", "CUMPLE (enmiendas declaradas)",
         "Todas posteriores al cribado y declaradas (§2.9 y §3.1.1): la "
         "restricción de idioma a inglés y español (11-08-2026), con su "
         "impacto medido: %d estudios eliminados, %d de ellos comparativos y "
         % (S["estudios_eliminados_por_idioma"], S["comparativos_perdidos_por_idioma"]) +
         "%d del conjunto de control positivo; NOREC, adoptado el 02-09-2026 "
         % len(CTRL["perdidos_enmienda"]) +
         "para %d estudio y aplicado el 06-10-2026 a %d más, y ampliado ese "
         % (norec_fecha["2026-09-02"], norec_fecha["2026-10-06"]) +
         "mismo día a NOPDF, que excluye todo estudio sin el artículo completo "
         "(%d estudios); NOORG (14-09-2026, fichas de "
         % S["excluidos_texto_completo_NOPDF"] +
         "registro que no declaran el organismo; %d estudios), y los códigos "
         % S["excluidos_texto_completo_NOORG"] +
         "IDI, PRO e INT, añadidos después del vocabulario original. El "
         "registro de decisiones es solo-anexar y permite reconstruir el "
         "corpus previo"),
        ("25", "Apoyo económico", "", "CUMPLE", "Declaraciones"),
        ("26", "Conflictos de interés", "", "CUMPLE", "Declaraciones"),
        ("27", "Disponibilidad de datos y código", "", "CUMPLE", "Declaraciones y S3–S6"),
    ]
    tabla(d, ["Ítem", "Elemento", "Qué exige", "Estado", "Dónde está"],
          [(a, b, c, e, f) for a, b, c, e, f in ITEMS],
          [1.4, 3.2, 3.8, 2.4, 6.2])
    # El recuento agrupaba por la PRIMERA PALABRA del veredicto, y "NO CUMPLE"
    # y "NO APLICA" empiezan las dos por "NO": los items que no aplican se le
    # presentaban al editor como incumplidos, y la fila "NO APLICA" salia
    # siempre en cero. Se agrupa por el veredicto entero, normalizando solo el
    # parentesis de "CUMPLE (declarado)".
    est = collections.Counter(i[3].split(" (")[0] for i in ITEMS)
    d.add_heading("Resumen del estado", level=2)
    for k in ("CUMPLE", "PARCIAL", "NO CUMPLE", "NO APLICA"):
        n = est.get(k, 0)
        if n:
            d.add_paragraph("%s: %d ítems" % (k, n), style="List Bullet")
    # CORREGIDO EL 2026-10-08. La nota decia «Los ítems marcados NO CUMPLE
    # dependen todos de la extracción por duplicado, que está en curso»: la
    # extraccion y su adjudicacion estan cerradas, y hoy ningun item esta en NO
    # CUMPLE. Solo se escribe si hay alguno, y sin atribuirle una causa.
    if est.get("NO CUMPLE"):
        nota(d, "Los ítems marcados NO CUMPLE se declaran como limitación en "
                "§4.4 del manuscrito en lugar de presentarse como cumplidos.")
    d.save(OUT / "S1_lista_PRISMA_2020.docx")


def v2_busquedas(S):
    # CORREGIDO EL 2026-10-08. El subtitulo prometia la sintaxis «con fecha de
    # ejecucion» de cada fuente y daba «ejecutadas entre el 3 y el 10 de
    # agosto»: no hay fecha de ejecucion por fuente, el 10 de agosto es cuando
    # la exportacion de BVS entro al corpus, y la ejecucion de Scopus cuya
    # exportacion entro al corpus no tiene fecha registrada.
    d = doc_nuevo("S2. Estrategias de búsqueda",
                  "Sintaxis literal por fuente y número de resultados. No hay "
                  "fecha de ejecución por fuente: las ejecuciones documentadas "
                  "son del 3 y el 4 de agosto de 2026, y la exportación de BVS "
                  "se incorporó al corpus el 10 de agosto; la ejecución de "
                  "Scopus cuya exportación entró al corpus no tiene fecha "
                  "registrada (el fichero de su brazo B se terminó de escribir "
                  "el 5 de agosto).")
    # La autoría de la búsqueda se declara aquí y no solo en el manuscrito:
    # este anexo es el que un revisor abre para comprobar la reproducibilidad,
    # y es donde la pregunta "¿quién la hizo?" se plantea de forma natural.
    # CORREGIDA EL 2026-10-08, dos veces. Primero decia que el modelo no genero
    # ni ejecuto las ecuaciones. Despues, que «las diseñó D. Valdiviezo con la
    # asistencia del modelo ... y las ejecutó D. Valdiviezo», como un hecho,
    # y que los recuentos de PubMed y de ClinicalTrials.gov se cuadraron con
    # la interfaz. Lo que hay es una declaracion de D.V. del 8 de octubre, unos
    # commits del 3 de agosto redactados por el modelo que narran la ejecucion
    # en primera persona, y un cuadre con la interfaz que solo consta para
    # ClinicalTrials.gov.
    # «la sección 2.4» es numeración del informe extendido; el manuscrito de la
    # revista, que viaja con este anexo, no numera sus secciones.
    nota(d, "Según declara D.V. (8 de octubre de 2026), diseñó estas ecuaciones "
            "con la participación del modelo de lenguaje cuya intervención se "
            "declara en la selección de los estudios (§2.4 del informe "
            "extendido) y en la declaración de uso de inteligencia artificial "
            "del manuscrito, y las ejecutó en cada interfaz con la "
            "guía del modelo. Los mensajes de los commits del 3 de agosto de "
            "2026, que redactó el modelo, narran esa ejecución en primera "
            "persona. Los registros de PubMed y de ClinicalTrials.gov que "
            "entraron al corpus los descargaron por API guiones escritos por el "
            "modelo; solo los recuentos de ClinicalTrials.gov se cuadraron con "
            "los de la interfaz.")
    man = json.loads((RS / "busqueda" / "sources.json").read_text(encoding="utf-8"))
    REG = {"ClinicalTrials.gov", "EudraCT", "CTIS"}
    # «registros_por_fuente» cuenta registros recuperados, no informes: la
    # columna decia «Informes en el corpus».
    d.add_heading("Corriente 1. Bases bibliográficas", level=2)
    tabla(d, ["Fuente", "Registros en el corpus", "Archivo de exportación"],
          [(k, miles(S["registros_por_fuente"].get(k, 0)), pathlib.Path(v).name)
           for k, v in man.items() if k not in REG], [5.0, 4.0, 7.0])
    d.add_heading("Corriente 2. Registros de ensayos", level=2)
    tabla(d, ["Fuente", "Registros en el corpus", "Archivo de exportación"],
          [(k, miles(S["registros_por_fuente"].get(k, 0)), pathlib.Path(v).name)
           for k, v in man.items() if k in REG], [5.0, 4.0, 7.0])
    fuente = ROOT / "quality_reports" / "ecuaciones_busqueda_final.md"
    if fuente.exists():
        # CORREGIDO EL 2026-10-08. Se copiaba el documento de trabajo ENTERO,
        # incluidas sus secciones 4 a 6 del 4 de agosto («Recuento
        # consolidado» con Scopus sin exportar y 10 414 unicos, «Qué falta» y
        # «Qué declarar en Métodos», que decia «Un solo revisor en cribado y
        # extracción»). Las contradice el corpus final. Se copian solo las
        # secciones 1 a 3 (bases y ecuaciones), y se corta en «## 4.».
        #
        # La copia, ademas, deshacia la sintaxis literal: los «#1 ... #9» del
        # gestor de CENTRAL salian como titulos sin la almohadilla, los
        # bloques de codigo dejaban las comillas invertidas a la vista y las
        # tablas con el numero de resultados se saltaban. Ahora el codigo va
        # tal cual, en monoespaciado, y las tablas se copian como tablas.
        d.add_heading("Ecuaciones literales", level=2)
        nota(d, "Copia de las secciones 1 a 3 de quality_reports/"
                "ecuaciones_busqueda_final.md, el documento de trabajo de las "
                "búsquedas, cuyo inventario de bases se verificó por última vez "
                "el 4 de agosto de 2026. Los recuentos son los que anota ese "
                "documento, y sus avisos de estado («pendiente», «sin probar») "
                "son de ese documento de trabajo, no el estado final: lo que "
                "entró al corpus es lo de las dos tablas de arriba, según el "
                "manifiesto de fuentes. ProQuest se interrogó, pero no se "
                "exportó y no forma parte del corpus. Las secciones de recuento "
                "consolidado, tareas pendientes y redacción de Métodos de ese "
                "documento no se copian: eran notas de trabajo del 4 de agosto "
                "y las contradice el corpus final. En la regla R1, los «%d "
                "estudios incluidos» de la validación previa son los %d "
                "controles positivos con PMID, de los %d fijados (S6): las "
                "ecuaciones se diseñaron para recuperarlos."
                % (S["controles_comprobables_pmid"], S["controles_comprobables_pmid"],
                   S["controles_fijados"]))
        # La frase de R1 se lee, sin esa aclaracion, como si el conjunto de
        # control tuviera 40 estudios. Si el documento de trabajo deja de decir
        # «de 40 estudios incluidos», la aclaracion sobra y hay que revisarla.
        if ("de %d estudios incluidos" % S["controles_comprobables_pmid"]
                not in fuente.read_text(encoding="utf-8")):
            raise SystemExit("S2: la regla R1 de %s ya no habla de «%d estudios "
                             "incluidos»; revisa la aclaración de la nota."
                             % (fuente.name, S["controles_comprobables_pmid"]))
        lineas = fuente.read_text(encoding="utf-8").split("\n")
        corte = next((i for i, l in enumerate(lineas)
                      if l.startswith("## 4.")), None)
        if corte is None:
            raise SystemExit("S2: no encuentro «## 4.» en %s; sin ese corte se "
                             "copiarian las notas de trabajo del 4 de agosto."
                             % fuente.name)
        en_codigo, filas_tabla = False, []

        def sin_marcas(t):
            t = t.replace("**", "")
            # cursiva de Markdown (*texto*), sin tocar comodines como phage*
            return re.sub(r"(?<![\w`*])\*(?=\S)([^*`]+?)(?<=\S)\*(?![\w*])", r"\1", t)

        def volcar_tabla():
            filas = [[sin_marcas(c.strip()) for c in f.strip().strip("|").split("|")]
                     for f in filas_tabla
                     if not re.fullmatch(r"\|?[\s|:-]+\|?", f.strip())]
            if filas:
                n = len(filas[0])
                tabla(d, filas[0], [(f + [""] * n)[:n] for f in filas[1:]])
            filas_tabla.clear()

        for linea in lineas[:corte]:
            l = linea.rstrip()
            if l.startswith("```"):
                en_codigo = not en_codigo
                continue
            if en_codigo:
                # literal: ni titulos, ni marcas, ni espacios recortados
                p = d.add_paragraph()
                r = p.add_run(l)
                r.font.name = "Consolas"
                r.font.size = Pt(8.5)
                p.paragraph_format.space_after = Pt(0)
                continue
            if l.startswith("|"):
                filas_tabla.append(l)
                continue
            if filas_tabla:
                volcar_tabla()
            if not l.strip() or l.strip() in (">", "---"):
                continue
            if l.startswith("#"):
                t = l.lstrip("#").strip().replace("*", "")
                # Los titulos de la seccion 3 llevaban el estado del 4 de
                # agosto («— contada, pendiente de exportar»): se quita, porque
                # en un titulo se lee como el estado actual.
                if re.match(r"3\.\d", t):
                    t = t.split(" — ")[0]
                d.add_heading(t, level=3)
                continue
            t = sin_marcas(l[2:] if l.startswith("> ") else l)
            p = d.add_paragraph(t)
            p.runs[0].font.size = Pt(9)
        if filas_tabla:
            volcar_tabla()
    nota(d, "El manifiesto de fuentes (sources.json) es la única declaración de "
            "qué exportaciones entran en el corpus. Una comprobación automática "
            "falla si alguna fuente declarada no aparece representada.")
    d.save(OUT / "S2_estrategias_de_busqueda.docx")


def v5_listado(S):
    """Listado de los estudios incluidos. En Excel porque se filtra y se ordena."""
    grupos = leer(RS / "cribado" / "study_groups.csv")
    pre = {p["id_provisional"]: p for p in
           leer(RS / "extraccion" / "pre_extraccion_desde_resumen.csv")}
# El texto completo no siempre llega en PDF: el manuscrito de autor de
# PhagoBurn esta depositado en ORBi como .docx. Contar solo *.pdf lo
# dejaba fuera del recuento aunque estuviera en disco y fuera legible.
    # El texto completo puede llegar como PDF, como manuscrito de autor en
    # .docx o como el texto integro de la pagina del editor cuando este
    # sirve el articulo en HTML y bloquea la descarga automatica del PDF.
    # Las tres formas son el mismo dato para quien va a extraer.
    pdfs = {q.stem for q in (RS / "textos_completos" / "pdf").iterdir()
            if q.suffix.lower() in (".pdf", ".docx")}
    web = RS / "textos_completos" / "texto_html"
    if web.exists():
        pdfs |= {q.stem for q in web.glob("*.txt")}
    # Los 22 excluidos al releer el texto completo no van en S5: S5 es el
    # cuerpo de evidencia. Van en S16, con su codigo, su motivo y la cita del
    # articulo que los desmiente, que es lo que pide PRISMA 16b.
    p_ex = RS / "cribado" / "exclusiones_tras_texto_completo.csv"
    fuera_ft = ({r["study_id"] for r in leer(p_ex)} if p_ex.exists() else set())
    reps = {"EST-%03d" % int(g["estudio"]): g for g in grupos
            if g["informe_para_extraer"] == "SI"
            and "EST-%03d" % int(g["estudio"]) not in fuera_ft}
    filas = []
    for eid in sorted(reps):
        g, p = reps[eid], pre.get(eid, {})
        filas.append([eid, g["situacion"], g["anio"], g["revista"], g["titulo"],
                      g["informes_del_estudio"],
                      p.get("study_design", ""), p.get("n_arm", ""),
                      p.get("geographic_source", ""),
                      "sí" if eid in pdfs else "no", g["clave"]])
    # El numero va en el nombre y por tanto SE CALCULA: dejarlo escrito hizo
    # que el fichero siguiera diciendo 219 cuando ya contenia 185.
    for viejo in OUT.glob("S5_listado_*_estudios.*"):
        viejo.unlink()
    with open(OUT / ("S5_listado_%d_estudios.csv" % len(filas)), "w",
              encoding="utf-8-sig", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(["id", "situacion", "anio", "revista", "titulo",
                    "n_informes", "diseno", "n_brazo", "procedencia",
                    "texto_completo", "clave_de_estudio"])
        w.writerows(filas)
    return len(filas)


def v6_auditoria(S):
    """S6: la auditoría de controles positivos, calculada y no tecleada.

    CORREGIDO EL 2026-10-08. Decia que se fijaron «40 estudios», con la tabla
    «40 | 40» escrita a mano en las tres etapas. Se fijaron 42 y la
    comprobación automática, que busca por PMID, alcanzaba a 40. Tampoco
    decía de dónde salió el conjunto (un metaanálisis exploratorio hecho con
    asistencia de modelos de lenguaje) ni que las ecuaciones se diseñaron
    para recuperarlo, de modo que la auditoría prueba la selección y no la
    búsqueda; ni qué fue de los controles después del cribado.
    """
    A = auditoria_controles(S)
    n_fij, n_comp = len(A["fijados"]), len(A["comprobables"])
    E = A["etapas"]
    if A["perdidos_enmienda"] != ["Ronit2024"]:
        raise SystemExit("S6: la enmienda de idioma se lleva ahora %s; el párrafo "
                         "sobre Ronit et al. (2024) ya no se sostiene."
                         % A["perdidos_enmienda"])

    def bonito(clave):
        # «Leitner2021» -> «Leitner 2021»; las claves sin año, o con un sufijo
        # tras el año («Li2025_biliary»), quedan igual: salía «Li 2025_biliary»
        return re.sub(r"(?<=[A-Za-z])(\d{4})$", r" \1", clave)

    def lista(xs):
        xs = list(xs)
        return xs[0] if len(xs) == 1 else ", ".join(xs[:-1]) + " y " + xs[-1]

    d = doc_nuevo("S6. Auditoría de controles positivos",
                  "Comprobación, sobre los %d controles comprobables por PMID de "
                  "los %d fijados antes del cribado, de que la selección no "
                  "perdió ninguno sin un motivo declarado." % (n_comp, n_fij))
    d.add_heading("Qué es el conjunto de control y qué puede probar", level=2)
    d.add_paragraph(
        "Antes de iniciar el cribado se fijó un conjunto de %d estudios "
        "conocidos como elegibles, procedentes del metaanálisis exploratorio de "
        "julio de 2026, que se hizo con asistencia de modelos de lenguaje. La "
        "comprobación automática los busca por PMID y alcanzaba a %d de ellos; "
        "%s sin PMID (%s) %s fuera de ella."
        % (n_fij, n_comp,
           "el único" if len(A["sin_pmid"]) == 1 else "los %d" % len(A["sin_pmid"]),
           lista(bonito(s) for s in A["sin_pmid"]),
           "queda" if len(A["sin_pmid"]) == 1 else "quedan"))
    d.add_paragraph(
        "Las ecuaciones de búsqueda se diseñaron para recuperar este conjunto "
        "(S2). Por eso la auditoría no mide la sensibilidad de la búsqueda: que "
        "la búsqueda encuentre los controles es una condición con la que se "
        "diseñó, no una prueba. Lo que sí acota es lo que pierde la selección: "
        "después de cada etapa de cribado se comprueba que ninguno de los "
        "controles comprobables haya perdido todos sus informes.")
    d.add_paragraph(
        "La comprobación opera sobre el estudio y no sobre el informe. Excluir "
        "una fe de erratas o una ficha de registro duplicada de un estudio "
        "incluido es legítimo; perder el estudio entero no lo es. Una auditoría "
        "por informe daría falsos positivos en el primer caso y dejaría de "
        "distinguir el segundo.")

    d.add_heading("Resultado por etapa", level=2)

    def veredicto(n, perdidos_declarados=0):
        if n == n_comp:
            return "SUPERADA"
        if n + perdidos_declarados == n_comp:
            return "PÉRDIDA DECLARADA (%d)" % perdidos_declarados
        return "FALLO"

    filas = [("Etapa 1 (reglas explícitas)", n_comp, E["e1"], veredicto(E["e1"])),
             ("Etapa 2 (título)", n_comp, E["e2"], veredicto(E["e2"])),
             ("Etapa 3 (resumen), antes de la enmienda de idioma", n_comp,
              E["e3_antes"], veredicto(E["e3_antes"])),
             ("Etapa 3 (resumen), tras la enmienda de idioma del 11 de agosto "
              "de 2026", n_comp, E["e3"],
              veredicto(E["e3"], len(A["perdidos_enmienda"])))]
    if any(f[3] == "FALLO" for f in filas):
        print("  AVISO S6: la auditoría de controles falla en alguna etapa: %s"
              % A["perdidos_otros"])
    tabla(d, ["Etapa", "Controles comprobables", "Conservan informe", "Veredicto"],
          filas, [6.0, 3.6, 3.6, 3.0])
    nota(d, "Recalculado en cada pasada desde los registros de cribado "
            "(screening_stage1_all.csv y los registros solo-anexar de las "
            "etapas 2 y 3) y desde quality_reports/corpus_identifier_index.txt, "
            "por PMID y a nivel de estudio, como la auditoría del canal.")

    d.add_heading("Pérdida por la enmienda de idioma", level=2)
    d.add_paragraph(
        "La restricción a inglés y español, adoptada el 11 de agosto de 2026 con "
        "el cribado ya cerrado, excluyó en la etapa de resumen a %d de los %d "
        "controles comprobables: Ronit et al. (2024), un caso de fagoterapia en "
        "prótesis vascular infectada por P. aeruginosa publicado en danés en "
        "Ugeskrift for Læger. No es un fallo del cribado, porque el estudio se "
        "identificó y se clasificó correctamente, sino el precio del criterio. "
        "Hasta esa enmienda, la auditoría pasaba %d de %d en las tres etapas."
        % (len(A["perdidos_enmienda"]), n_comp,
           min(E["e1"], E["e2"], E["e3_antes"]), n_comp))
    d.add_paragraph(
        "La auditoría distingue las dos situaciones. Una pérdida por una "
        "enmienda declarada se informa pero no detiene el canal; una pérdida sin "
        "motivo declarado sigue siendo un fallo que lo detiene. Confundirlas "
        "arruina la auditoría en cualquiera de los dos sentidos: si falla "
        "siempre se acaba ignorando, y si pasa siempre deja de detectar el error "
        "que existe para detectar.")

    # Lo que la auditoría del cribado no mira: qué fue de cada control después.
    # Todo sale de corpus_identifier_index.txt, study_groups.csv y
    # exclusiones_tras_texto_completo.csv; nada se escribe a mano.
    fuera = {s: e for s, e in A["estado"].items() if not e["en_corpus"]}
    tras = {s: e for s, e in fuera.items() if e["exclusion"]}
    por_codigo = collections.defaultdict(list)
    for s, e in sorted(tras.items()):
        por_codigo[e["exclusion"][0]["codigo"]].append(s)
    en_cribado = [s for s in fuera if s not in tras]
    if sorted(en_cribado) != sorted(A["perdidos_enmienda"]):
        raise SystemExit("S6: salieron del corpus durante el cribado %s, y la "
                         "enmienda de idioma explica %s." % (en_cribado,
                                                            A["perdidos_enmienda"]))
    if set(por_codigo) - {"NOPDF", "NOREC"}:
        raise SystemExit("S6: hay controles excluidos tras el texto completo con "
                         "códigos %s; la frase sobre NOPDF y NOREC no los cubre."
                         % sorted(set(por_codigo) - {"NOPDF", "NOREC"}))
    d.add_heading("Lo que pasó después del cribado", level=2)
    d.add_paragraph(
        "La auditoría del cribado no sigue a los controles más allá de la etapa "
        "de resumen. Hoy siguen en el corpus %d de los %d fijados. Salieron %d: "
        "%d en la etapa de resumen, por la enmienda de idioma, y %d después del "
        "cribado, en la fase de texto completo. %s NOPDF y NOREC excluyen "
        "porque no se consiguió o no se pudo leer el artículo, no porque se haya "
        "comprobado que el estudio incumple los criterios (S16)."
        % (A["en_corpus"], n_fij, len(fuera), len(en_cribado), len(tras),
           " ".join("Por %s, %d: %s." % (
               k, len(v), lista("%s (%s)" % (bonito(s), ", ".join(tras[s]["estudios"]))
                                for s in v))
               for k, v in sorted(por_codigo.items(), key=lambda kv: -len(kv[1])))))
    sys.path.insert(0, str(ROOT / "scripts"))
    from exclusion_codes import code_for
    filas = []
    for s, e in sorted(fuera.items()):
        if e["exclusion"]:
            x = e["exclusion"][0]
            filas.append((bonito(s), ", ".join(e["estudios"]),
                          "Fase de texto completo", x["codigo"],
                          x["decidido_por"], x["fecha"][:10]))
        else:
            # la fila del registro solo-anexar, tal cual: quién y cuándo
            r = A["decision_enmienda"][s]
            filas.append((bonito(s), "—", "Etapa de resumen (enmienda de idioma)",
                          code_for(r["reason"]) or "—", r["decided_by"],
                          r["decided_at"][:10]))
    tabla(d, ["Control", "Estudio", "Cuándo salió", "Código", "Decidido por", "Fecha"],
          filas, [3.0, 2.0, 3.6, 1.6, 3.6, 2.2])

    # Aqui va la clave tal como esta en corpus_identifier_index.txt, para que
    # se pueda buscar en el fichero.
    d.add_heading("Estado de los %d controles" % n_fij, level=2)
    tabla(d, ["Clave del control", "Comprobable por PMID", "Estudio",
              "En el corpus vigente"],
          [(s, "sí" if e["pmid"] else "no",
            ", ".join(e["estudios"]) or "—", "sí" if e["en_corpus"] else "no")
           for s, e in sorted(A["estado"].items())], [4.0, 3.2, 3.0, 3.6])

    d.add_heading("Incidencia detectada y corregida", level=2)
    d.add_paragraph(
        "En una ejecución intermedia la auditoría falló: una regla de exclusión "
        "mal calibrada eliminaba todos los informes de un estudio incluido. La "
        "regla se corrigió antes de continuar. El fallo y su corrección constan "
        "en el registro del proyecto (commit 39b2291, 4 de agosto de 2026: un "
        "lote de títulos que emitió el modelo excluyó a Ronit 2024 porque su "
        "título en PubMed era «[Not Available]»; la corrección se añadió como "
        "fila nueva del registro solo-anexar). Se informa aquí porque una "
        "auditoría que solo se reporta cuando pasa no demuestra nada.")
    # La nota decia solo que el conjunto se fijo antes del cribado. Es cierto,
    # pero callaba que con el mismo conjunto se diseñaron las ecuaciones.
    nota(d, "El conjunto de control se fijó antes del cribado: elegirlo después "
            "de ver los resultados lo convertiría en una descripción del "
            "resultado en vez de en una prueba. Pero con él se diseñaron también "
            "las ecuaciones de búsqueda, de modo que prueba lo que pierde la "
            "selección, no la sensibilidad de la búsqueda.")
    d.save(OUT / "S6_auditoria_controles_positivos.docx")



def v18_evidencia_sesgo(S):
    """S18: un juicio por fila, con la frase FIRMADA en que se apoya.

    LO QUE ENVIABA ANTES, Y POR QUE ESTABA MAL. Este anexo copiaba
    `evidencia_por_dominio.csv`: 229 frases del articulo agrupadas por cubo
    tematico (CONFUSION, MEDICION, y tambien CONFLICTOS y CASO, que no son
    dominios de ninguna herramienta). Era una cosecha mecanica para BUSCAR,
    no la justificacion de un juicio. Un arbitro que quisiera discrepar del
    juicio D4 de EST-070 encontraba un monton de frases del articulo y ninguna
    razon. Ademas D1 y D2 de ROBINS-I comparten cubo, de modo que ni siquiera
    era atribuible por dominio.

    Lo que envia ahora: `pendiente1_juicios.csv`, una fila por juicio, con la
    frase que los dos revisores escribieron en la columna «¿En que frase te
    apoyaste?» del cuaderno de consenso. 79 de los 90 la tienen; los 11 sin
    ella son juicios globales y llevan [DATO FALTANTE].
    """
    origen = ROOT / "quality_reports" / "pendiente1_juicios.csv"
    if origen.exists():
        destino = OUT / "S18_cada_juicio_con_su_frase.csv"
        shutil.copy2(origen, destino)
        filas = leer_bom(destino)
        sin = sum(1 for r in filas if r["cita_que_lo_respalda"].startswith("[DATO"))
        print("  S18 %d juicios, %d con frase firmada, %d sin ella (todos globales)"
              % (len(filas), len(filas) - sin, sin))
        # la cosecha tematica se conserva aparte: sirve para buscar, no para
        # respaldar, y decirlo es parte del anexo
        viejo = OUT / "S18_evidencia_por_dominio.csv"
        if viejo.exists():
            viejo.rename(OUT / "S18b_frases_cosechadas_por_tema.csv")
        for q in OUT.glob("S18_evidencia_por_dominio.xlsx"):
            q.unlink()
        return
    print("  AVISO: no hay pendiente1_juicios.csv; corre scripts/audita_pendientes.py")
    _v18_antiguo(S)


def _v18_antiguo(S):
    """S18: la frase del articulo en que se apoya cada juicio de riesgo de sesgo.

    La Tabla 5 da los 90 juicios, pero un juicio sin la cita que lo sostiene no
    es comprobable: un arbitro no puede discrepar de un «riesgo grave» si no ve
    en que parte del articulo se leyo. El fichero existia desde el principio en
    revision_sistematica/riesgo_sesgo/ y no viajaba; la auditoria del
    2026-09-16 lo senalo.
    """
    origen = RS / "riesgo_sesgo" / "evidencia_por_dominio.csv"
    if not origen.exists():
        print("  AVISO: no hay evidencia_por_dominio.csv")
        return
    # Un estudio que salio del corpus se lleva sus juicios: el anexo publica lo
    # que sostiene la Tabla 5, y la Tabla 5 ya no lo tiene. El fichero de
    # riesgo de sesgo si lo conserva, porque ahi se juzgo de verdad.
    fuera = {r["study_id"] for r in
             leer(RS / "cribado" / "exclusiones_tras_texto_completo.csv")}
    evaluados = {r["study_id"] for r in
                 leer_bom(RS / "riesgo_sesgo" / "riesgo_sesgo_comparativos_adjudicado.csv")
                 if r["study_id"] not in fuera}
    filas = [r for r in leer_bom(origen) if r["study_id"] in evaluados]
    destino = OUT / "S18_evidencia_por_dominio.csv"
    with open(destino, "w", encoding="utf-8-sig", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(filas[0].keys()))
        w.writeheader()
        w.writerows(filas)
    print("  S18 %d frases de apoyo, de los %d estudios evaluados"
          % (len(filas), len(evaluados)))


def leer_bom(p):
    with open(p, encoding="utf-8-sig", newline="") as fh:
        return list(csv.DictReader(fh))


def v19_cribado_modelo(S):
    """S19: el cribado con modelo de lenguaje, documentado hasta donde se puede.

    POR QUE. Un arbitro pidio doce cosas sobre este cribado --modelo, version,
    fecha, prompt, configuracion, regla para respuestas ambiguas, tratamiento
    de errores, ficheros de entrada y salida, que decidio el modelo, que
    verificaron los autores, si se releyeron los excluidos y si la validacion
    fue estratificada--. Este anexo responde a las que constan en el registro y
    marca [DATO FALTANTE] en las que no. Ninguna se rellena de memoria.
    """
    import collections
    d2 = leer(RS / "cribado" / "screening_stage2_pool_decisions.csv")
    d3 = leer(RS / "cribado" / "screening_stage3_pool_decisions.csv")
    quien = collections.Counter(r.get("decided_by", "") for r in d2 + d3)
    fechas = sorted({(r.get("decided_at") or "")[:10] for r in d2 + d3 if r.get("decided_at")})
    VOC = vocabulario_de_motivos()
    corpus = {r["record_id"] for r in leer(RS / "cribado" / "screening_corpus_all.csv")}

    def coma(x):
        return str(x).replace(".", ",")

    # CORREGIDO EL 2026-10-08. Decia «495 en la de resumen» como si fueran 495
    # decisiones. El registro es solo-anexar: 495 filas sobre 460 registros, y
    # las filas de mas son las correcciones de idioma, que sustituyen a una
    # fila anterior. Se cuenta aqui y se contrasta con el escalar.
    vigentes3 = len({r["record_id"] for r in d3})
    if vigentes3 != S["decisiones_resumen"]:
        raise SystemExit("S19: %d registros decididos en resumen y %d en los "
                         "escalares." % (vigentes3, S["decisiones_resumen"]))
    vistos, repetidas = set(), []
    for r in d3:
        if r["record_id"] in vistos:
            repetidas.append(r)
        vistos.add(r["record_id"])
    dias_rep = sorted({r["decided_at"][:10] for r in repetidas})
    if not all("idioma" in r["decided_by"] for r in repetidas) or len(dias_rep) != 1:
        raise SystemExit("S19: las filas repetidas de la etapa de resumen ya no "
                         "son solo las correcciones de idioma de un día.")
    fuera2 = sum(1 for r in d2 if r["record_id"] not in corpus)

    d = doc_nuevo("S19. Cribado con modelo de lenguaje",
                  "Lo que consta en el registro, y lo que no consta")
    d.add_heading("Lo que el registro documenta", level=2)
    for k, v in (
            ("Modelo y versión", "Claude Opus 5 (Anthropic), identificador «claude-opus-5», "
             "tal como queda escrito en la columna decided_by de cada decisión"),
            # 2026-10-12. Decia «así consta en cada fila del registro», y no
            # todas las filas lo dicen con esas palabras: 77 de la etapa de
            # resumen llevan otra etiqueta (desglose al final). Lo que sí
            # consta en cada fila es que la emitió el modelo.
            ("Revisor", "el modelo, como revisor único y sin duplicación. Cada fila "
             "del registro lo nombra como emisor en la columna decided_by, con la "
             "etiqueta que se transcribe al final de este anexo. Lo que el modelo "
             "excluyó no lo releyó ningún humano, salvo la muestra del recribado "
             "(abajo)"),
            ("Fechas de uso", "del %s al %s" % (fecha_es(fechas[0]), fecha_es(fechas[-1]))
             if fechas else "[DATO FALTANTE]"),
            ("Decisiones emitidas por el modelo",
             "en la etapa de título, %s filas, una por registro (%d de esos registros "
             "ya no están en el corpus vigente); en la de resumen, %s filas en el "
             "registro solo-anexar, que son %s decisiones vigentes: las %d filas de "
             "idioma del %s corrigen filas anteriores. Cada fila lleva su motivo y su "
             "marca de tiempo"
             % (miles(len(d2)), fuera2, miles(len(d3)), miles(vigentes3),
                len(repetidas), fecha_es(dias_rep[0]))),
            # main() añade a S3 la columna en_corpus_actual: «sin reelaborar»
            # a secas no era exacto.
            ("Ficheros de entrada y salida",
             "entrada: revision_sistematica/cribado/screening_corpus_all.csv; salida: los "
             "anexos S3, que son el registro original sin reelaborar, con una sola "
             "columna añadida (en_corpus_actual)"),
            # CORREGIDO EL 2026-10-08. Decia «cerrado y fijado por los autores
            # antes del cribado». El registro lo desmiente: ver
            # vocabulario_de_motivos(). Y remitia a «la Tabla 1», que en el
            # informe extendido es la de caracteristicas del corpus.
            ("Vocabulario de motivos",
             "no se fijó antes de empezar. Las decisiones del primer día de cribado "
             "de títulos (%s) llevan el motivo en texto libre (%s exclusiones); los "
             "códigos del vocabulario cerrado, cuya redacción procede de esos textos, "
             "se usaron desde el %s, y las exclusiones del primer día se asignaron "
             "después a un código (exclusion_codes.code_for). No consta que los "
             "autores fijaran los códigos antes de empezar. Ese mismo %s se añadieron "
             "a mitad de lote dos reglas que concretan los criterios: endolisinas "
             "aisladas fuera (intervención) e informes veterinarios fuera "
             "(población). El vocabulario se publica en scripts/exclusion_codes.py y "
             "en la tabla de motivos de exclusión por etapa del informe extendido "
             "(Tabla 4)"
             % (fecha_es(VOC["dias_libre"][0]), miles(VOC["n_libre"]),
                fecha_es(VOC["primer_dia_codigos"]), fecha_es(VOC["dias_libre"][0]))),
            # Decia «recribado ciego ... 0 falsos negativos» sin decir que en la
            # primera pasada D.V. marco registros como incluibles y los
            # reclasifico despues al contrastarlos con los criterios.
            ("Validación del error de exclusión",
             "recribado en Rayyan, a ciegas, por un solo revisor (D.V.), de %s de "
             "los %s registros excluidos en las etapas de título y resumen. En la "
             "primera pasada, sin los criterios a la vista, D.V. marcó %s como "
             "incluibles y, al contrastarlos con los criterios, los reclasificó como "
             "excluidos: %s falsos negativos de %s (%s %%; IC 95 %% exacto, 0,00 a "
             "%s %%)"
             % (S["validacion_muestra"], miles(S["validacion_marco"]),
                S["validacion_primera_pasada_incluidos"],
                S["validacion_falsos_negativos"], S["validacion_muestra"],
                coma(S["validacion_tasa_pct"]), coma(S["validacion_ic_sup_pct"])))):
        pp = d.add_paragraph()
        pp.add_run(k + ". ").bold = True
        # tras el punto del rotulo va mayuscula, y cada entrada cierra con punto
        pp.add_run(v[0].upper() + v[1:] + ("" if v.endswith(".") else "."))

    # CORREGIDO EL 2026-10-08. Bajo «Lo que el registro documenta» habia una
    # entrada «Decisiones verificadas por los autores. D. Valdiviezo examino uno
    # a uno contra los criterios los informes que superaron el cribado». Es una
    # declaracion de D.V. del 8 de octubre, no algo que el registro documente;
    # no la hicieron «los autores», y «contra los criterios» no esta en lo que
    # D.V. declaro. Va aqui, con la redaccion de la declaracion.
    faltan = ["[DATO FALTANTE] El texto literal e íntegro de la instrucción con "
              "que se aplicaron los criterios registro a registro. Lo que sí consta "
              "son los criterios de elegibilidad, las dos reglas añadidas el %s a "
              "mitad de lote y, desde el %s, el vocabulario de motivos (arriba)."
              % (fecha_es(VOC["dias_libre"][0]), fecha_es(VOC["primer_dia_codigos"])),
              "[DATO FALTANTE] Los parámetros de generación (temperatura, longitud "
              "máxima, semilla).",
              "[DATO FALTANTE] La regla escrita para respuestas ambiguas y el "
              "tratamiento de los errores de llamada. En la práctica, el pozo de "
              "título avanzó por defecto a lectura de resumen cuando la decisión no "
              "era clara, pero esa regla no se escribió antes.",
              "[DATO FALTANTE] Estratificación de la muestra de validación por fuente "
              "y por motivo de exclusión. La muestra de %s se tomó al azar sobre el "
              "marco entero, sin estratificar." % S["validacion_muestra"]]
    d.add_heading("Lo que el registro NO documenta", level=2)
    d.add_paragraph(
        "Las %d cosas siguientes no quedaron guardadas y no se reconstruyen a "
        "posteriori: escribirlas ahora de memoria sería inventarlas." % len(faltan))
    for t in faltan:
        d.add_paragraph(t, style="List Bullet")
    pp = d.add_paragraph()
    pp.add_run("Examen de lo que superó el cribado (declaración de D.V.). ").bold = True
    pp.add_run("Según declara D.V. (8 de octubre de 2026), examinó uno a uno los "
               "informes que superaron el cribado; ese examen no quedó registrado. "
               "La agrupación de esos informes en estudios (S5) la propuso un guion "
               "escrito por el modelo.")

    # El titulo y la frase llevaban «0 de 350» y «350 extracciones» tecleados.
    d.add_heading("Cómo debe leerse el %s de %s"
                  % (S["validacion_falsos_negativos"], S["validacion_muestra"]), level=2)
    d.add_paragraph(
        "La tasa observada de falsos negativos es del %s %%, pero la tasa real no se "
        "conoce: con %s registros recribados y %s falsos negativos, el intervalo "
        "exacto llega al %s %%, que sobre el marco de %s registros admite hasta %s "
        "perdidos. La cifra acota el error; no lo elimina."
        % (coma(S["validacion_tasa_pct"]), S["validacion_muestra"],
           S["validacion_falsos_negativos"], coma(S["validacion_ic_sup_pct"]),
           miles(S["validacion_marco"]), S["validacion_cota_estudios"]))
    d.add_heading("Quién emitió cada fila del registro", level=2)
    for k, v in quien.most_common():
        d.add_paragraph("%s — %s %s" % (k or "sin declarar", miles(v),
                                        "fila" if v == 1 else "filas"),
                        style="List Bullet")
    d.save(OUT / "S19_cribado_con_modelo_de_lenguaje.docx")
    print("  S19 cribado con modelo: %d filas de %d emisores"
          % (len(d2) + len(d3), len(quien)))


def v20_brazo_informe(S):
    """S20: de que informe salio cada brazo, y con que prueba."""
    origen = ROOT / "quality_reports" / "brazo_informe.csv"
    if not origen.exists():
        print("  AVISO: no hay brazo_informe.csv; corre scripts/build_brazo_informe.py")
        return
    shutil.copy2(origen, OUT / "S20_de_que_informe_salio_cada_brazo.csv")
    print("  S20 %d brazos con su informe de origen" % len(leer_bom(origen)))


def v21_solapamiento(S):
    """S21: el examen de solapamiento de pacientes entre estudios.

    Hasta el 2026-10-01 copiaba `solapamiento_candidatos.csv`, que es lo que
    propone el DETECTOR: sin veredicto, sin pacientes y sin los pares que solo
    encontro la lectura. El manuscrito remitia a este anexo para el desglose
    de lo confirmado y lo descartado, y el desglose no viajaba. Ahora viaja
    `pendiente2_solapamiento.csv`: cada par examinado, con su veredicto, sus
    pacientes y la frase firmada.
    """
    origen = ROOT / "quality_reports" / "pendiente2_solapamiento.csv"
    if not origen.exists():
        print("  AVISO: no hay pendiente2_solapamiento.csv; corre "
              "scripts/audita_pendientes.py")
        return
    shutil.copy2(origen, OUT / "S21_solapamiento_de_pacientes.csv")
    print("  S21 %d pares examinados de solapamiento" % len(leer_bom(origen)))


def v23_clase_verificada(S):
    """S23: la clase de resistencia comprobada contra el articulo, estudio a estudio.

    La lectura firmada por los dos autores el 2026-09-30, con su texto intacto
    y, al lado, como la codifico `ingest_lectura_firmada.py` y que cambio en la
    extraccion. Lo que quedo abierto va en su columna, no escondido.
    """
    origen = RS / "lectura_pendiente" / "lectura_resistencia_firmada.csv"
    if not origen.exists():
        print("  AVISO: no hay lectura_resistencia_firmada.csv; corre "
              "scripts/ingest_lectura_firmada.py --escribir")
        return
    shutil.copy2(origen, OUT / "S23_clase_de_resistencia_comprobada.csv")
    print("  S23 %d estudios con la clase comprobada contra el artículo"
          % len(leer_bom(origen)))


def v24_comparativos(S):
    """S24: los comparativos reextraidos: comparador, tiempo cero, estimando."""
    origen = RS / "lectura_pendiente" / "lectura_comparativos_firmada.csv"
    if not origen.exists():
        print("  AVISO: no hay lectura_comparativos_firmada.csv; corre "
              "scripts/ingest_lectura_firmada.py --escribir")
        return
    shutil.copy2(origen, OUT / "S24_comparativos_reextraidos.csv")
    print("  S24 %d comparativos reextraídos" % len(leer_bom(origen)))


def v22_completitud(S):
    """S22: la Tabla 3 con las cuatro situaciones, en fichero."""
    origen = ROOT / "quality_reports" / "tabla3_completitud.csv"
    if not origen.exists():
        print("  AVISO: no hay tabla3_completitud.csv; corre "
              "scripts/build_tabla3_completitud.py")
        return
    shutil.copy2(origen, OUT / "S22_completitud_resumen_frente_a_texto.csv")
    print("  S22 completitud en el resumen frente al texto completo")


def v17_tabla6(S):
    """S17: la Tabla 6 desglosada brazo a brazo.

    La Tabla 6 del manuscrito es un embudo y solo dice cuantos brazos quedan en
    cada paso. Un arbitro que quiera discrepar necesita ver POR QUE cae cada
    uno, y sobre todo distinguir los que caen porque el articulo calla de los
    que caen porque esta revision no pudo leerlo. Lo escribe
    `build_tabla6_brazos.py`, que aborta si su desglose no reproduce el embudo
    publicado.
    """
    origen = ROOT / "quality_reports" / "tabla6_brazo_a_brazo.csv"
    if not origen.exists():
        print("  AVISO: no hay tabla6_brazo_a_brazo.csv; corre "
              "scripts/build_tabla6_brazos.py")
        return
    destino = OUT / "S17_tabla6_brazo_a_brazo.csv"
    shutil.copy2(origen, destino)
    filas = leer(destino)
    print("  S17 %d brazos con su requisito de caida" % len(filas))


def v16_exclusiones(S):
    """S16: los estudios excluidos al leer el texto completo, con su motivo.

    Es lo que pide PRISMA 16b, y es el anexo que permite a un revisor
    discrepar: cada fila lleva el codigo de motivo, la explicacion y, cuando
    hay texto leido, la frase que sostiene la exclusion. Sin la cita, la lista
    seria una afirmacion; con ella, es comprobable.

    (2026-10-08: decia que CADA fila lleva «la frase del articulo». No: las
    NOPDF y NOREC no tienen articulo, cuatro filas solo traen el motivo y
    EST-205 cita la indexacion de SciELO. El recuento esta en el item 16b de S1.)
    """
    fuente = RS / "cribado" / "exclusiones_tras_texto_completo.csv"
    if not fuente.exists():
        return
    sys.path.insert(0, str(ROOT / "scripts"))
    from exclusion_codes import CODES
    filas = leer(fuente)
    destino = OUT / "S16_excluidos_tras_leer_el_texto_completo.csv"
    cab = ["study_id", "codigo", "que_significa_el_codigo", "motivo",
           "cita_del_texto", "titulo", "decidido_por", "fecha"]
    with open(destino, "w", encoding="utf-8-sig", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=cab)
        w.writeheader()
        for r in filas:
            r["que_significa_el_codigo"] = CODES.get(r["codigo"], "")
            w.writerow({c: r.get(c, "") for c in cab})
    if len(filas) != S["estudios_excluidos_tras_texto_completo"]:
        raise SystemExit(
            "S16: el anexo trae %d exclusiones y el manuscrito declara %d."
            % (len(filas), S["estudios_excluidos_tras_texto_completo"]))
    import collections as _c
    c = _c.Counter(r["codigo"] for r in filas)
    print("  S16 %d estudios excluidos al releer: %s"
          % (len(filas), ", ".join("%s %d" % kv for kv in c.most_common())))

def v9_idioma(S):
    """S9 sellado con el estado final de cada informe, no con el intermedio.

    `idioma_verificacion.csv` es la salida del comprobador de idioma, que juzga
    sobre el resumen. Un informe puede pasar esa prueba y quedar excluido
    despues al leer el texto completo. Aqui se cruza con el corpus final y con
    las decisiones de cribado, para que el anexo diga en que quedo cada uno.
    """
    fuente = RS / "cribado" / "idioma_verificacion.csv"
    if not fuente.exists():
        return
    filas = list(csv.DictReader(open(fuente, encoding="utf-8-sig")))
    grupos = list(csv.DictReader(
        open(RS / "cribado" / "study_groups.csv", encoding="utf-8-sig")))

    # `study_groups` es la foto que dejo el cribado y NO se filtra: sigue
    # teniendo los 22 estudios que salieron despues, al leer los textos
    # completos. Aqui hay que descontarlos, o S9 declara 233 informes incluidos
    # sobre un corpus de 201. Cada uno se lleva su motivo real, no un generico.
    p_ex = RS / "cribado" / "exclusiones_tras_texto_completo.csv"
    excl_est, motivo_ft = set(), {}
    if p_ex.exists():
        for r in csv.DictReader(open(p_ex, encoding="utf-8")):
            excl_est.add(r["study_id"])
            motivo_ft[r["study_id"]] = "%s: %s" % (r["codigo"], r["motivo"])
    fuera_ft = {g["record_id"]: motivo_ft["EST-%03d" % int(g["estudio"])]
                for g in grupos if "EST-%03d" % int(g["estudio"]) in excl_est}
    incluidos = {g["record_id"] for g in grupos
                 if g["record_id"] not in fuera_ft}

    # El motivo de la exclusion se toma de la ultima decision que la nombre, no
    # se redacta aqui: el registro de cribado es la fuente y es solo-anexar.
    motivo = {}
    for etapa in ("screening_stage3_pool_decisions.csv",
                  "screening_stage2_pool_decisions.csv"):
        p = RS / "cribado" / etapa
        if not p.exists():
            continue
        for r in csv.DictReader(open(p, encoding="utf-8-sig")):
            if r.get("verdict") == "EXCLUDE":
                motivo[r["record_id"]] = r.get("reason", "")

    cab = list(filas[0]) + ["estado_final", "motivo_de_la_exclusion"]
    fuera = 0
    for r in filas:
        dentro = r["record_id"] in incluidos
        r["estado_final"] = "INCLUIDO" if dentro else "EXCLUIDO DESPUES"
        r["motivo_de_la_exclusion"] = "" if dentro else fuera_ft.get(
            r["record_id"],
            motivo.get(r["record_id"], "excluido en el cribado; ver S3"))
        fuera += 0 if dentro else 1

    destino = OUT / "S9_idioma_por_informe_y_clase_de_evidencia.csv"
    with open(destino, "w", encoding="utf-8", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=cab)
        w.writeheader()
        w.writerows(filas)

    n = len(filas) - fuera
    if n != S["informes_agrupados"]:
        raise SystemExit(
            "S9: quedan %d informes INCLUIDO y el corpus tiene %d. El anexo "
            "que prueba el criterio de idioma no cuadra con el manuscrito."
            % (n, S["informes_agrupados"]))
    print("  S9  %d informes incluidos + %d excluidos despues, con su motivo"
          % (n, fuera))


def del_manuscrito(marca, que_es):
    """Un párrafo del manuscrito autoritativo, copiado literal.

    Ninguna declaración del anexo se redacta aquí. Se leen porque las versiones
    paralelas divergen y siempre en la misma dirección: la del anexo salía más
    suave. La de IA decía que el modelo dio «asistencia en la programación» del
    cribado cuando fue él quien emitió las decisiones, y que los autores
    «verificaron todo el contenido» cuando el manuscrito dice que los registros
    excluidos no los releyó nadie. La de CRediT decía «PENDIENTE DE COMPLETAR»
    cuando el manuscrito ya repartía las categorías entre los dos autores.
    """
    md = (ROOT / "paper" / "manuscrito_revision_sistematica.md").read_text(
        encoding="utf-8")
    i = md.find(marca)
    if i < 0:
        raise SystemExit(
            "S7: no encuentro «%s» en el manuscrito. %s sale de ahí y no se "
            "redacta en este script; si la sección se renombró, actualiza la "
            "marca." % (marca, que_es))
    texto = md[i + len(marca):].split("\n\n")[0].strip()
    # El .docx no lleva marcado Markdown: los asteriscos quedarian a la vista.
    return texto.replace("**", "")


def v7_declaraciones(S):
    d = doc_nuevo("S7. Declaraciones y requisitos del ICMJE",
                  "Documento de acompañamiento al envío.")
    for tit, txt in [
        ("Financiación",
         "Esta revisión no recibió financiación específica de agencias "
         "públicas, comerciales o sin ánimo de lucro."),
        ("Conflictos de interés",
         "Los autores declaran no tener conflictos de interés. Cada autor debe "
         "adjuntar además el formulario ICMJE Disclosure of Interest firmado."),
        # Tampoco esta se redacta aqui: el manuscrito ya reparte las categorias
        # entre los dos autores y el anexo seguia diciendo «PENDIENTE DE
        # COMPLETAR». Un comite que abra los dos documentos ve la contradiccion.
        ("Contribución de los autores (CRediT)",
         del_manuscrito("**Contribución de los autores (CRediT).**",
                        "la contribución de los autores")),
        ("Registro del protocolo",
         "PENDIENTE. La revisión no está registrada en PROSPERO ni en OSF. El "
         "manuscrito declara la ausencia de forma explícita en §2.1. Si se "
         "registra antes del envío, debe sustituirse esa declaración por el "
         "número de registro; no debe declararse un registro retrospectivo como "
         "si fuera prospectivo."),
        ("Disponibilidad de datos y código",
         "El corpus de cribado, los registros de decisión completos, el "
         "formulario de extracción y todo el código del canal están disponibles "
         "en el repositorio del proyecto. Los registros de decisión son "
         "solo-anexar y conservan cada corrección junto con la decisión "
         "original."),
        # Esta declaracion NO se redacta aqui: se copia literal del manuscrito.
        # La version que habia decia «asistencia en la programacion del canal de
        # cribado» y «los autores revisaron y verificaron todo el contenido».
        # Las dos cosas suavizaban lo que el manuscrito declara: que el modelo
        # emitio las decisiones como revisor unico, y que los registros que
        # excluyo no los releyo ningun humano. Es justo la declaracion que un
        # comite mira primero, y tener dos versiones distintas de ella en el
        # mismo envio es peor que no adjuntarla.
        ("Uso de inteligencia artificial",
         del_manuscrito("**Uso de inteligencia artificial.**",
                        "la declaración de uso de IA")),
        ("Ética y consentimiento",
         "No aplica: la revisión se basa en literatura publicada y en registros "
         "públicos de ensayos, sin datos individuales de pacientes."),
    ]:
        d.add_heading(tit, level=2)
        d.add_paragraph(txt)
    d.save(OUT / "S7_declaraciones_ICMJE.docx")


def main():
    OUT.mkdir(exist_ok=True)
    S = json.loads((ROOT / "quality_reports" / "synthesis_scalars.json")
                   .read_text(encoding="utf-8"))
    print("paquete de verificables:")
    v1_prisma(S)
    print("  S1  lista PRISMA 2020")
    v2_busquedas(S)
    print("  S2  estrategias de busqueda")
    # S3: registro de decisiones, tal cual, porque su valor es ser el original
    for origen, destino in (
            ("cribado/screening_stage2_pool_decisions.csv",
             "S3_decisiones_etapa2_titulo.csv"),
            ("cribado/screening_stage3_pool_decisions.csv",
             "S3_decisiones_etapa3_resumen.csv"),
            ("extraccion/pre_extraccion_desde_resumen.csv",
             "S4_pre_extraccion_desde_resumen.csv"),
            ("textos_completos/fulltext_identifiers.csv",
             "S8_recuperacion_texto_completo.csv"),
            ("cribado/idioma_texto_completo.csv",
             "S10_idioma_verificado_sobre_texto_completo.csv")):
        p = RS / origen
        if p.exists():
            shutil.copy2(p, OUT / destino)

    # S9: la prueba del criterio de idioma, informe por informe. Se copiaba tal
    # cual y salia con 234 filas, todas ADMITIDO, cuando los informes incluidos
    # son 233. La fila de mas es R56334c0408: el comprobador leyo su resumen,
    # que esta en ingles, y lo admitio; el cuerpo del articulo esta en ruso y se
    # excluyo despues, al abrir la web del editor. El fichero se escribio antes
    # de esa exclusion y nunca se actualizo.
    #
    # No se borra la fila. Es el caso que el manuscrito usa para argumentar que
    # el idioma no se puede dar por sabido desde los metadatos ni desde el
    # resumen, y borrarla escondería precisamente eso. Se sella con el estado
    # final y su motivo, de modo que S9 cuadre con los 233 del manuscrito y el
    # lector vea por que hay una fila mas.
    # S14 y S15. Un arbitro no podia comprobar NADA de la seccion 3.5 ni de las
    # tablas 5 y 6: el paquete solo llevaba la pre-extraccion desde resumenes
    # (S4), y esas cifras salen de la extraccion adjudicada, que no viajaba.
    # Publicar una cifra cuyo fichero no se aporta es pedir que se crea.
    for origen, destino in (
            ("extraccion/extraccion_adjudicada.csv",
             "S14_extraccion_adjudicada.csv"),
            ("extraccion/extraccion_adjudicada_procedencia.csv",
             "S15_procedencia_de_cada_casilla.csv")):
        q = RS / origen
        if q.exists():
            shutil.copy2(q, OUT / destino)
            print("  %-4s %s" % (destino[:3], destino))

    v9_idioma(S)
    v16_exclusiones(S)
    v17_tabla6(S)
    v18_evidencia_sesgo(S)
    v19_cribado_modelo(S)
    v20_brazo_informe(S)
    v21_solapamiento(S)
    v22_completitud(S)
    v23_clase_verificada(S)
    v24_comparativos(S)

    # S4 se copiaba tal cual y no permitia reproducir la Tabla 2: tiene 159
    # filas -- el corpus anterior a la enmienda de idioma -- mientras la tabla
    # usa 124, y su columna `study_id` esta vacia en las 159, de modo que no hay
    # forma de saber que fila pertenece al corpus actual. No se borran las 35
    # filas sobrantes, que son rastro de la enmienda: se anade la columna que
    # permite filtrarlas, y se retira la columna vacia que solo confunde.
    s4 = OUT / "S4_pre_extraccion_desde_resumen.csv"
    if s4.exists():
        filas = leer(s4)
        # Que estudios siguen en el corpus se decide con la misma fuente que
        # S5, `study_groups.csv` menos las exclusiones tras el texto completo.
        # Antes salia de quality_reports/orden_de_extraccion.csv, que es una
        # foto del 2026-08-09: hoy los dos conjuntos coinciden exactamente en
        # los mismos 95 estudios, pero la foto no se mueve cuando el corpus si,
        # y el dia que dejen de coincidir el anexo mentiria sin avisar.
        vivos = {"EST-%03d" % int(g["estudio"])
                 for g in leer(RS / "cribado" / "study_groups.csv")
                 if g["informe_para_extraer"] == "SI"
                 and g["situacion"] in ("extraible", "solo-resumen")}
        p_ex = RS / "cribado" / "exclusiones_tras_texto_completo.csv"
        if p_ex.exists():
            vivos -= {r["study_id"] for r in leer(p_ex)}
        campos = [c for c in filas[0] if c != "study_id"] + ["en_corpus_actual"]
        for f in filas:
            f.pop("study_id", None)
            f["en_corpus_actual"] = "si" if f.get("id_provisional") in vivos else "no"
        with open(s4, "w", encoding="utf-8", newline="") as fh:
            w = csv.DictWriter(fh, fieldnames=campos)
            w.writeheader()
            w.writerows(filas)
        n = sum(1 for f in filas if f["en_corpus_actual"] == "si")
        print("  S4  %d filas, %d en el corpus actual (Tabla 2 se reproduce "
              "filtrando en_corpus_actual = si)" % (len(filas), n))
    # S3 se copiaba tal cual y sale con 13 917 decisiones de titulo mientras el
    # manuscrito declara 13 894. Las 23 de mas son decisiones sobre registros de
    # una version anterior del corpus, y el registro es solo-anexar, asi que se
    # conservan. Pero sin marcarlas, un arbitro cuenta y encuentra una
    # discrepancia que no puede explicar: es el mismo defecto que tenia S9.
    corpus = {r["record_id"] for r in
              leer(RS / "cribado" / "screening_corpus_all.csv")}
    for nombre in ("S3_decisiones_etapa2_titulo.csv",
                   "S3_decisiones_etapa3_resumen.csv"):
        ruta = OUT / nombre
        if not ruta.exists():
            continue
        filas = leer(ruta)
        if not filas or "en_corpus_actual" in filas[0]:
            continue
        cab = list(filas[0]) + ["en_corpus_actual"]
        fuera = 0
        for r in filas:
            dentro = r["record_id"] in corpus
            r["en_corpus_actual"] = "si" if dentro else "no"
            fuera += 0 if dentro else 1
        with open(ruta, "w", encoding="utf-8", newline="") as fh:
            w = csv.DictWriter(fh, fieldnames=cab)
            w.writeheader()
            w.writerows(filas)
        # filas, no decisiones: en la etapa de resumen las correcciones de
        # idioma son filas de mas sobre el mismo registro (ver S19)
        print("  S3  %-38s %5d filas, %d fuera del corpus actual"
              % (nombre, len(filas), fuera))
    print("  S4  pre-extraccion desde resumen")
    n = v5_listado(S)
    print("  S5  listado de %d estudios" % n)
    v6_auditoria(S)
    print("  S6  auditoria de controles positivos")
    v7_declaraciones(S)
    print("  S7  declaraciones ICMJE")
    print("  S8  registro de recuperacion de texto completo")
    print("  S9  idioma por informe, con clase de evidencia")
    print("  S10 idioma verificado sobre el texto completo")
    # figuras y tablas, ya listas
    fig = OUT / "figuras y tablas"
    fig.mkdir(exist_ok=True)
    for p in (ROOT / "paper" / "figuras").glob("*.pdf"):
        shutil.copy2(p, fig / p.name)
    for p in (ROOT / "paper" / "tablas").glob("*.csv"):
        shutil.copy2(p, fig / p.name)
    print("  figuras (PDF vectorial) y tablas (CSV)")

    # S11-S13 se construyen aqui y no aparte. Vivieron cinco dias como fichero
    # suelto y se quedaron viejos: el paquete anunciaba 169 desacuerdos y una
    # kappa de 0,38 cuando el manuscrito ya decia 575 y 0,57. Un anexo que hay
    # que acordarse de regenerar acaba contradiciendo al articulo que acompana.
    # Van despues de S5 porque S12 lo lee para saber que estudios tienen texto.
    import build_extraction_verifiables
    build_extraction_verifiables.main()

    print("\nescrito en %s" % OUT)
    return 0


if __name__ == "__main__":
    sys.exit(main())
