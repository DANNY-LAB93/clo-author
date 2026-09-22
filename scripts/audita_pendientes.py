# -*- coding: utf-8 -*-
"""Las cuatro tablas de la auditoría final: juicios, solapamiento, brazos y Tabla 6.

POR QUE EXISTE. Un árbitro pidió cuatro cosas, una fila por unidad y sin
inventar nada: los 90 juicios con su cita, el solapamiento de pacientes con
EST-021 aparte, los 103 brazos con su trazabilidad completa, y la Tabla 6 con
CUMPLE / NO CUMPLE / NO EVALUABLE por criterio. Cada tabla se construye aquí
desde los ficheros firmados, y donde el dato no existe se escribe
[DATO FALTANTE] con el nombre de lo que haría falta.

DE DONDE SALE LA CITA DE CADA JUICIO. Del cuaderno de consenso firmado el
2026-09-09, columna «¿En qué frase te apoyaste?», que trae una entrada
numerada por dominio; y del cuaderno de EST-004, firmado aparte, que trae
además la del juicio global. **No** de `evidencia_por_dominio.csv`, que es una
cosecha mecánica de frases candidatas por cubo temático: sirve para buscar, no
para respaldar un juicio concreto, y ROBINS-I D1 y D2 comparten cubo.

SALIDA
    quality_reports/pendiente1_juicios.csv
    quality_reports/pendiente2_solapamiento.csv
    quality_reports/pendiente3_brazos.csv
    quality_reports/pendiente4_tabla6.csv
    quality_reports/pendiente4_embudo.csv
    quality_reports/auditoria_pendientes.json
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
CONSENSO = RS / "riesgo_sesgo" / "riesgo_sesgo_comparativos_consenso.xlsx"
EST004 = pathlib.Path.home() / "Desktop" / "FIRMAR_riesgo_de_sesgo_EST-004.xlsx"
csv.field_size_limit(200_000_000)

sys.path.insert(0, str(ROOT / "scripts"))
import rob_instruments as RI  # noqa: E402

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

FALTA = "[DATO FALTANTE]"
COMPARATIVOS = {"RCT", "non-randomised trial", "retrospective cohort",
                "prospective cohort"}


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


# ---------------------------------------------------------------- contexto
def contexto():
    grupos = leer(RS / "cribado" / "study_groups.csv")
    excl = {r["study_id"]: r for r in
            leer(RS / "cribado" / "exclusiones_tras_texto_completo.csv")}
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
    return grupos, excl, adj, enlace, pdfs, informes


# ------------------------------------------------- 1. LOS NOVENTA JUICIOS
def frases_firmadas():
    """Una frase por dominio, tal como la escribieron los dos revisores."""
    from openpyxl import load_workbook
    out = {}
    wb = load_workbook(CONSENSO, data_only=True)
    for hoja, col in (("RoB 2 por dominio", 12), ("ROBINS-I por dominio", 14)):
        for fila in wb[hoja].iter_rows(min_row=4, values_only=True):
            if not fila or not fila[0]:
                continue
            texto = fila[col - 1] or ""
            trozos = re.split(r"(?m)^\s*(\d+)[.)]\s*\t?", texto)
            for num, cuerpo in zip(trozos[1::2], trozos[2::2]):
                out[(str(fila[0]).strip(), int(num))] = " ".join(cuerpo.split())
    # EST-004 se firmó aparte y su cuaderno SÍ trae la frase del juicio global
    if EST004.exists():
        s = load_workbook(EST004, data_only=True)["ROBINS-I EST-004"]
        for fila in s.iter_rows(min_row=12, values_only=True):
            cod = str(fila[0]).strip() if fila and fila[0] else ""
            if not cod or not fila[3]:
                continue
            out[("EST-004", cod)] = " ".join(str(fila[3]).split())
    return out


def tabla_juicios(enlace, informes):
    # Los juicios de un estudio que salio del corpus no cuentan: EST-063 se
    # excluyo como protocolo el 2026-09-22 y se llevo sus ocho.
    _fuera = {r["study_id"] for r in
              leer(RS / "cribado" / "exclusiones_tras_texto_completo.csv")}
    rob = [r for r in leer(RS / "riesgo_sesgo"
                           / "riesgo_sesgo_comparativos_adjudicado.csv",
                           enc="utf-8-sig")
           if r["study_id"] not in _fuera]
    frases = frases_firmadas()
    nombre = {}
    for i in RI.SIMPLIFICADOS:
        for it in i["items"]:
            nombre[(i["clave"], it["codigo"])] = it["texto_es"]
    titulo = {}
    for e, gs in informes.items():
        g = next((x for x in gs if x["informe_para_extraer"] == "SI"), gs[0])
        titulo[e] = (g["record_id"], g["revista"], g["anio"], g["titulo"])

    filas, sin_cita = [], []
    for n, r in enumerate(sorted(rob, key=lambda x: (x["study_id"], x["item"] == "GLOBAL",
                                                     x["item"])), start=1):
        e, inst, item = r["study_id"], r["instrumento"], r["item"]
        es_global = item == "GLOBAL"
        if e == "EST-004":
            cita = frases.get((e, item), "")
            fuente = "cuaderno FIRMAR_riesgo_de_sesgo_EST-004.xlsx, firmado 2026-09-17"
        else:
            clave = None if es_global else int(re.sub(r"\D", "", item))
            cita = frases.get((e, clave), "") if clave else ""
            fuente = ("riesgo_sesgo_comparativos_consenso.xlsx, columna «¿En qué "
                      "frase te apoyaste?», firmado 2026-09-09")
        if not cita:
            sin_cita.append("%s %s" % (e, item))
        rec, revista, anio, tit = titulo.get(e, ("", "", "", ""))
        filas.append({
            "n": n,
            "estudio": e,
            "informe": rec,
            "referencia_del_informe": "%s (%s, %s)" % (tit[:70], revista, anio),
            "instrumento": {"rob2": "RoB 2 (adaptado)", "robins": "ROBINS-I"}[inst],
            "item": item,
            "dominio": "Juicio global del estudio" if es_global
                       else nombre.get((inst, item), item),
            "tipo_de_juicio": "global" if es_global else "dominio",
            "valor": r["valor"],
            "fuente_documental": fuente,
            "cita_que_lo_respalda": cita or FALTA,
            "firmado_por": r["firmado_por"],
            "fecha": r["fecha"],
        })
    return filas, sin_cita, rob


# ------------------------------------- 2. SOLAPAMIENTO Y EST-021, APARTE
def tabla_solapamiento():
    """Una fila por par examinado. Lo confirmado se separa de lo descartado."""
    cand = leer(QR / "solapamiento_candidatos.csv", enc="utf-8-sig")
    # Lo que la lectura resolvió, con la frase que lo resuelve. Las dos
    # entradas se escriben aquí porque son juicios de lectura, no del script,
    # y el script no puede producirlos: lo que sí hace es no dejar ningún par
    # candidato fuera de la tabla.
    COMUN = ("EST-108 (Pirnay et al., Nat Microbiol 2024) declara literalmente: "
             "«Twenty-seven of the 100 BT cases/patients were previously "
             "reported6,13–26». Su referencia %s es %s, que es este estudio. Los "
             "pacientes de este estudio están, por tanto, dentro de los 100 de "
             "EST-108.")
    LEIDO = {
        ("EST-077", "EST-003"): dict(
            clave_del_paciente="P1 nina 10 anos, Berlin Heart EXCOR",
            paciente="caso 3 de EST-077 = caso 3 de la Tabla 4 de EST-003",
            evidencia="EST-077: «A 10-year-old female with a genetic cardiomyopathy… "
                      "placement of a Berlin Heart Excor VAD in January 2019… recurrent "
                      "and almost persistent P. aeruginosa bacteremia»; «Two patients "
                      "(Cases 3, 4) were treated at the Schnieder Children's Hospital "
                      "(Petach Tikva, Israel)»; «PASA16 (used in Cases 3 and 4)». "
                      "EST-003, Tabla 4, caso 3: «bacteremia 10/F prostheticdevice MDR "
                      "i.v.,49days … deceased … prosthetic device infection (Berlin "
                      "heart EXCOR)». Coinciden edad, sexo, dispositivo, organismo, "
                      "preparado y país.",
            n_duplicados="1 confirmado; el caso 4 de EST-077 (52/M, Sheba) no aparece "
                         "en la Tabla 4 de EST-003 y queda sin resolver",
            veredicto="SOLAPAMIENTO CONFIRMADO POR LECTURA",
            accion="Declararlo en Resultados y en Limitaciones. No fusionar ni excluir: "
                   "son dos publicaciones distintas y el corpus cuenta estudios. La "
                   "revisión no publica proporción agrupada, de modo que no hay ninguna "
                   "cifra que corregir."),
        ("EST-003", "EST-095"): dict(
            clave_del_paciente="P2 nino 7 anos, infeccion osteoarticular",
            paciente="caso 4 de la Tabla 4 de EST-003 = el nino de EST-095",
            evidencia="La Tabla 4 de EST-003 trae una columna «Published case» y en el caso 4 "
                      "dice «Khatami et al.25». EST-095 es Khatami A et al., «Bacterial lysis, "
                      "autophagy and innate immune responses during adjunctive phage therapy "
                      "in a child», EMBO Mol Med 2021, «osteoarticular infection in a 7-year-old "
                      "child». EST-003 caso 4: «osteomyelitis 7/F surgical debridement XDR "
                      "i.v.,14days ... remission ... Khatami et al.». Coinciden edad, sexo, foco, "
                      "resistencia y duracion.",
            n_duplicados="1", veredicto="SOLAPAMIENTO CONFIRMADO POR LECTURA",
            accion="Declararlo. Lo declara el propio EST-003 en su tabla; no hizo falta "
                   "deducirlo."),
        ("EST-003", "EST-015"): dict(
            clave_del_paciente="P3 varon 25 anos, osteomielitis craneal",
            paciente="caso 9 de la Tabla 4 de EST-003 = el paciente de EST-015",
            evidencia="Columna «Published case» del caso 9 de EST-003: «Simner et al.26». "
                      "EST-015 es Simner PJ et al., «Combination of phage therapy and "
                      "cefiderocol to successfully treat Pseudomonas aeruginosa cranial "
                      "osteomyelitis», JAC-AMR 2022: «a 25-year-old male who experienced an "
                      "accidental electrocution resulting in exposed calvarium». EST-003 caso 9: "
                      "«osteomyelitis 25/M debrided cranial bone and scalp tissue XDR i.v.,30days "
                      "... cefiderocol ... recovery ... Simner et al.».",
            n_duplicados="1", veredicto="SOLAPAMIENTO CONFIRMADO POR LECTURA",
            accion="Declararlo. Tambien lo declara EST-003 en su propia tabla."),
        ("EST-003", "EST-012"): dict(
            clave_del_paciente="P4 varon 96 anos, infeccion protesica",
            paciente="caso 10 de la Tabla 4 de EST-003 = el paciente de EST-012",
            evidencia="EST-012 (Nat Commun 2026): «A 96-year-old male with multiple "
                      "comorbidities including heart failure presented with a chronic "
                      "multidrug-resistant Pseudomonas aeruginosa infection» en protesis, "
                      "tratado con «two bacteriophages (PASA16 and F83)». EST-003 caso 10: "
                      "«prosthetic joint infection 96/M synovial fluid ... IA and i.v., 10 days, "
                      "2 cycles ... PaWRA02Phi83». Coinciden edad, sexo, foco y los dos fagos.",
            n_duplicados="1", veredicto="SOLAPAMIENTO CONFIRMADO POR LECTURA",
            accion="Declararlo. EST-003 no lo marca como publicado porque EST-012 salio despues."),
        ("EST-003", "EST-070"): dict(
            clave_del_paciente="P1 nina 10 anos, Berlin Heart EXCOR",
            paciente="la misma nina del Berlin Heart, por tercera vez",
            evidencia="EST-070 (Onallah, Hazan, Nir-Paz; Israeli Phage Therapy Center, OFID 2023): "
                      "«Additional 2 failure included 1 pediatric case with persistent infection "
                      "of her Berlin heart (manuscript in preparation)». Es la misma paciente que "
                      "el caso 3 de EST-003 y el caso 3 de EST-077.",
            n_duplicados="1 (la misma ya contada con EST-077)",
            veredicto="SOLAPAMIENTO CONFIRMADO POR LECTURA",
            accion="Esta paciente esta en TRES estudios del corpus: EST-003, EST-070 y EST-077."),
        ("EST-049", "EST-061"): dict(
            paciente="[DATO FALTANTE]",
            evidencia="Los dos son receptores de trasplante pulmonar tratados con AB-PA01 en "
                      "UCSD. EST-049 declara «institutional review board 200163», el mismo IRB "
                      "que EST-077 cita para sus casos de UCSD; EST-061 es «Early clinical "
                      "experience of bacteriophage therapy in 3 lung transplant recipients» "
                      "(AJT 2019, UCSD). EST-049 podria ser uno de esos tres o uno posterior. "
                      "La lectura no lo resuelve con lo que los dos articulos dicen.",
            n_duplicados="[DATO FALTANTE]",
            veredicto="SIN RESOLVER: leido y no concluyente",
            accion="Hace falta la descripcion de los tres pacientes de EST-061 con edad y fecha, "
                   "que el articulo no da en el texto recuperado."),
        ("EST-108", "EST-010"): dict(
            clave_del_paciente="P5 infección espinal panresistente",
            paciente="referencia 20 de EST-108 = EST-010",
            evidencia="%s" % (COMUN % ("20", "«Ferry, T. et al. Personalized bacteriophage "
                      "therapy to treat pandrug-resistant spinal Pseudomonas aeruginosa "
                      "infection»")),
            n_duplicados="1", veredicto="SOLAPAMIENTO CONFIRMADO POR LECTURA",
            accion="Declararlo. El brazo A de EST-010 es además uno de los 21 que "
                   "sobreviven al embudo de la proporción descriptiva."),
        ("EST-108", "EST-016"): dict(
            clave_del_paciente="P6 varón de 21 años, osteomielitis femoral, Riga",
            paciente="referencia 21 de EST-108 = EST-016",
            evidencia="%s EST-108 reporta 2 pacientes de Letonia y lleva a la Universidad "
                      "Stradins de Riga en su lista de autores, que es la institución de "
                      "EST-016." % (COMUN % ("21", "«Racenis, K. et al. Use of phage "
                      "cocktail BFC 1.10 in combination with ceftazidime-avibactam»")),
            n_duplicados="1", veredicto="SOLAPAMIENTO CONFIRMADO POR LECTURA",
            accion="Declararlo. El brazo A de EST-016 es además uno de los 21 que "
                   "sobreviven al embudo de la proporción descriptiva."),
        ("EST-108", "EST-046"): dict(
            clave_del_paciente="P7 septicemia sensible solo a colistina",
            paciente="referencia 15 de EST-108 = EST-046",
            evidencia="%s" % (COMUN % ("15", "«Jennes, S. et al. Use of bacteriophages in "
                      "the treatment of colistin-only-sensitive Pseudomonas aeruginosa "
                      "septicaemia»")),
            n_duplicados="1", veredicto="SOLAPAMIENTO CONFIRMADO POR LECTURA",
            accion="Declararlo."),
        ("EST-108", "EST-062"): dict(
            clave_del_paciente="P8 paciente pediátrica, Bruselas, cóctel BFC-1",
            paciente="referencia 17 de EST-108 = EST-062",
            evidencia="%s" % (COMUN % ("17", "«Van Nieuwenhuyse, B. et al. Bacteriophage-"
                      "antibiotic combination therapy against extensively drug-resistant "
                      "Pseudomonas aeruginosa»")),
            n_duplicados="1", veredicto="SOLAPAMIENTO CONFIRMADO POR LECTURA",
            accion="Declararlo. Los dos son del Queen Astrid Military Hospital, que "
                   "coordina el consorcio de EST-108."),
        ("EST-108", "EST-124"): dict(
            clave_del_paciente="P9 paciente de Racenis 2023",
            paciente="referencia 25 de EST-108 = EST-124",
            evidencia="%s" % (COMUN % ("25", "«Racenis, K. et al. Successful bacteriophage-"
                      "antibiotic combination therapy against multidrug-resistant "
                      "Pseudomonas»")),
            n_duplicados="1", veredicto="SOLAPAMIENTO CONFIRMADO POR LECTURA",
            accion="Declararlo."),
        ("EST-108", "EST-164"): dict(
            clave_del_paciente="P10 y P11, dos pacientes musculoesqueléticos, Lovaina",
            n_pacientes=2,
            paciente="referencia 19 de EST-108 = EST-164",
            evidencia="%s EST-164 aporta 2 pacientes." % (COMUN % ("19", "«Onsea, J. et "
                      "al. Bacteriophage application for difficult-to-treat "
                      "musculoskeletal infections: development of a standardized "
                      "protocol»")),
            n_duplicados="2", veredicto="SOLAPAMIENTO CONFIRMADO POR LECTURA",
            accion="Declararlo. KU Leuven forma parte del consorcio de EST-108."),
        ("EST-108", "EST-034"): dict(
            clave_del_paciente="ninguno",
            paciente="ninguno",
            evidencia="EST-034 es una serie de un solo centro de Estados Unidos (Open "
                      "Forum Infect Dis 2020) y EST-108 es el consorcio belga. EST-108 la "
                      "cita en la discusión, no entre las referencias 6 y 13-26 de sus "
                      "casos ya publicados.",
            n_duplicados="0", veredicto="DESCARTADO POR LECTURA",
            accion="Ninguna."),
        ("EST-108", "EST-044"): dict(
            clave_del_paciente="ninguno",
            paciente="ninguno",
            evidencia="EST-044 se publicó en 2026 y EST-108 en 2024: un caso de 2026 no "
                      "puede estar entre los «previously reported» de 2024. La cita va en "
                      "el otro sentido.",
            n_duplicados="0", veredicto="DESCARTADO POR LECTURA",
            accion="Ninguna."),
        ("EST-012", "EST-026"): dict(
            paciente="ninguno",
            evidencia="EST-012 nombra NCT05269134 —el registro de EST-026— en su "
                      "discusión: «These include a Phase 2 study for chronic salvage PJI "
                      "(PhageBank, NCT05269134) and a phase 2 study for acute PJI cases "
                      "(GLORIA, NCT06605651). These studies had challenges with "
                      "enrollment…». Lo cita como ensayo que fracasó en reclutar, no "
                      "como aquel en que se trató a su paciente.",
            n_duplicados="0",
            veredicto="DESCARTADO POR LECTURA",
            accion="Ninguna."),
    }
    pac, brazos = {}, collections.defaultdict(list)
    for r in leer(RS / "extraccion" / "extraccion_adjudicada.csv"):
        brazos[r["study_id"]].append(r["arm_id"])
        n = (r["n_arm"] or "").strip()
        pac[r["study_id"]] = pac.get(r["study_id"], 0) + (int(n) if n.isdigit() else 0)

    filas = []
    for r in cand:
        a, b = r["estudio_a"], r["estudio_b"]
        d = LEIDO.get((a, b)) or LEIDO.get((b, a))
        filas.append({
            "estudio_1": a, "estudio_2": b,
            "clave_del_paciente": (d.get("clave_del_paciente", "") if d else "") or FALTA,
            "pacientes_de_esa_clave": (d.get("n_pacientes", 1) if d else ""),
            "paciente_o_identificador": d["paciente"] if d else FALTA,
            "senal_que_lo_marco": r["fuerza"],
            "evidencia": d["evidencia"] if d else (r["fragmento"][:280] or
                                                   "producto en común: " + r["producto_comun"]),
            "pacientes_potencialmente_duplicados": d["n_duplicados"] if d else FALTA,
            "brazos_afectados": "%s: %s | %s: %s" % (a, ",".join(brazos.get(a, [])) or "—",
                                                     b, ",".join(brazos.get(b, [])) or "—"),
            "se_conto_una_o_dos_veces": ("dos veces, como dos estudios"
                                         if d and d["veredicto"].startswith("SOLAPA")
                                         else ("una vez" if d else FALTA)),
            "veredicto": d["veredicto"] if d else "SIN LEER: candidato por producto y país",
            "accion_necesaria": d["accion"] if d else
                                "Leer los dos artículos y comparar las descripciones de "
                                "paciente. No se ha hecho.",
        })
    # Los pares que la LECTURA encontro y el detector NO propuso. Se anaden
    # explicitamente: si solo se publicaran los candidatos del heuristico, la
    # tabla diria que el examen cubrio lo que en realidad se le escapo.
    ya = {(f["estudio_1"], f["estudio_2"]) for f in filas}
    ya |= {(b, a) for a, b in ya}
    for (a, b), d in LEIDO.items():
        if (a, b) in ya:
            continue
        filas.append({
            "estudio_1": a, "estudio_2": b,
            "clave_del_paciente": d.get("clave_del_paciente", "") or FALTA,
            "pacientes_de_esa_clave": d.get("n_pacientes", 1),
            "paciente_o_identificador": d["paciente"],
            "senal_que_lo_marco": "NO lo marco el detector: lo encontro la lectura",
            "evidencia": d["evidencia"],
            "pacientes_potencialmente_duplicados": d["n_duplicados"],
            "brazos_afectados": "%s: %s | %s: %s" % (a, ",".join(brazos.get(a, [])) or "—",
                                                     b, ",".join(brazos.get(b, [])) or "—"),
            "se_conto_una_o_dos_veces": ("dos veces, como dos estudios"
                                         if d["veredicto"].startswith("SOLAPA") else "una vez"),
            "veredicto": d["veredicto"],
            "accion_necesaria": d["accion"],
        })

    filas.sort(key=lambda f: (0 if f["veredicto"].startswith("SOLAPAMIENTO") else
                              1 if f["veredicto"].startswith("DESCARTADO") else 2,
                              f["estudio_1"]))
    return filas


def bloque_est021(informes, pdfs):
    """EST-021 por separado: qué está confirmado y qué falta para cerrarlo."""
    rob = [r for r in leer(RS / "riesgo_sesgo" / "riesgo_sesgo_comparativos_adjudicado.csv",
                           enc="utf-8-sig") if r["study_id"] == "EST-021"]
    adj = [r for r in leer(RS / "extraccion" / "extraccion_adjudicada.csv")
           if r["study_id"] == "EST-021"]
    gs = informes["EST-021"]
    des = next(g for g in gs if g["informe_para_extraer"] == "SI")
    dom = {r["item"]: r["valor"] for r in rob}
    orden = ["Bajo riesgo de sesgo", "Algunas preocupaciones", "Alto riesgo de sesgo"]
    peor = max((v for k, v in dom.items() if k != "GLOBAL"),
               key=lambda v: orden.index(v) if v in orden else -1)
    return {
        "identificacion": "CONFIRMADA: %s, %s %s, %s"
                          % (des["titulo"][:80], des["revista"], des["anio"],
                             des["record_id"]),
        "diseno": "CONFIRMADO: ECA. Declarado RCT en el resumen y adjudicado RCT "
                  "sobre el artículo; los dos coinciden.",
        "informes": "CONFIRMADO: %d informes, de los cuales el designado para extraer "
                    "es %s (artículo); los otros %d son fichas de registro "
                    "(NCT02116010)." % (len(gs), des["record_id"], len(gs) - 1),
        "brazos": "CONFIRMADO: %d brazo extraído (%s), n=%s. El artículo tiene dos "
                  "grupos —PP1131 y cuidado estándar— y **solo se extrajo el expuesto**."
                  % (len(adj), adj[0]["arm_id"], adj[0]["n_arm"]),
        "inclusion": "CONFIRMADA: en el corpus vivo, con texto completo (%s) y "
                     "evaluado con RoB 2 adaptado."
                     % ("sí" if "EST-021" in pdfs else "no"),
        "juicio": "NO CONFIRMADO. Dominios: %s. Peor dominio: «%s». Juicio global "
                  "firmado: «%s». RoB 2 no admite bajo riesgo global con un dominio "
                  "en algunas preocupaciones."
                  % ("; ".join("%s=%s" % (k, dom[k]) for k in sorted(dom) if k != "GLOBAL"),
                     peor, dom["GLOBAL"]),
        "que_falta": "La decisión firmada de los dos autores en la hoja 1 de "
                     "~/Escritorio/FIRMAR_auditoria_2026-09-16.xlsx: corregir el global "
                     "a «Algunas preocupaciones», o mantenerlo y declarar en Métodos por "
                     "qué se apartan de la regla del instrumento. Ningún documento "
                     "adicional del estudio hace falta: el dato es el juicio, no el "
                     "artículo.",
        "comparador_no_extraido": "El comparador de EST-021 es «standard of care a thick "
                                  "cream» según su propio texto; no se extrajo como "
                                  "brazo, de modo que el contraste no está en los datos.",
    }


# ------------------------------------------------- 3. LOS CIENTO TRES BRAZOS
def tabla_brazos(adj, excl, enlace, pdfs):
    t6 = {(r["study_id"], r["arm_id"]): r
          for r in leer(QR / "tabla6_brazo_a_brazo.csv", enc="utf-8-sig")}
    log = {r["id"]: r for r in leer(RS / "textos_completos" / "fulltext_download_log.csv")}
    filas, sin_traza = [], []
    for r in adj:
        e, a = r["study_id"], r["arm_id"]
        if e in excl:
            continue
        en = enlace.get((e, a), {})
        con_texto = e in pdfs
        fuente = []
        if (CACHE / (e + ".txt")).exists():
            fuente.append("revision_sistematica/textos_completos/texto_cache/%s.txt" % e)
        if log.get(e, {}).get("pmcid"):
            fuente.append(log[e]["pmcid"])
        if en.get("identificadores"):
            fuente.append(en["identificadores"])
        fila = {
            "estudio": e,
            "informe": en.get("record_id", "") or FALTA,
            "brazo": a,
            "intervencion": "%s, vía %s" % (r["modality"] or FALTA, r["route"] or FALTA),
            "comparador": FALTA + ": el formulario de extracción no tiene campo de "
                          "comparador y no se extrajo ningún brazo de control",
            "tamano_muestral": r["n_arm"] if (r["n_arm"] or "").strip() not in ("", "NA")
                               else FALTA,
            "texto_completo": "sí" if con_texto else "no",
            "desenlace": "éxito clínico" + (" (definido: %s)" % r["clinical_success_definition"][:70]
                                            if r["clinical_success_definition"].strip().upper()
                                            not in ("NA", "", "SIN DEFINICION OPERATIVA")
                                            else " (sin definición operativa)"),
            "tiempo_de_evaluacion": FALTA + ": variable no recogida en el formulario",
            "numerador": r["clinical_success_n"] if (r["clinical_success_n"] or "").strip()
                         not in ("", "NA", "Na") else FALTA,
            "denominador": r["n_arm"] if (r["n_arm"] or "").strip() not in ("", "NA")
                           else FALTA,
            "vinculo_con_el_archivo_fuente": " | ".join(fuente) or "sin texto obtenido",
            "incluido_o_excluido": "incluido",
            "motivo_de_exclusion": "",
            "estado_de_extraccion": r["extraction_status"],
            "via_del_vinculo_con_el_informe": en.get("via", "") or FALTA,
        }
        if not en.get("record_id"):
            sin_traza.append("%s%s sin informe" % (e, a))
        filas.append(fila)
    # los brazos de estudios excluidos, para que la tabla explique el 132 - 29
    fuera = []
    for r in adj:
        if r["study_id"] in excl:
            ex = excl[r["study_id"]]
            fuera.append({"estudio": r["study_id"], "brazo": r["arm_id"],
                          "motivo": "%s — %s" % (ex["codigo"], ex["motivo"][:80])})
    return filas, fuera, sin_traza


# ------------------------------------------------------ 4. LA TABLA 6 FINAL
def tabla6_final(pdfs):
    t6 = leer(QR / "tabla6_brazo_a_brazo.csv", enc="utf-8-sig")
    CRIT = [("diseno_comparativo", "1. diseño comparativo"),
            ("numerador_valido", "2. numerador válido"),
            ("denominador_valido", "3. denominador válido"),
            ("definicion_operativa", "4. definición operativa de éxito"),
            ("atribuible_a_P_aeruginosa", "5. atribuible a P. aeruginosa"),
            ("terapeutica_no_profilactica", "6. terapéutica, no profiláctica"),
            ("proporcion_no_tiempo", "7. proporción, no tiempo")]
    filas = []
    for r in t6:
        f = {"estudio": r["study_id"], "brazo": r["arm_id"],
             "diseno_adjudicado": r["diseno_adjudicado"] or "no declarado",
             "texto_completo": r["texto_completo"]}
        for k, etq in CRIT:
            f[etq] = r[k].upper()
        f["primer_requisito_que_falla"] = r["primer_requisito_que_falla"]
        f["motivo"] = r["motivo"]
        f["clasificacion"] = clasifica(r)
        filas.append(f)

    # el embudo, en el ORDEN PUBLICADO, con las cuatro cuentas por escalón
    embudo, vivos = [], list(t6)
    embudo.append({"filtro": "0. brazos extraídos", "brazos": len(vivos),
                   "estudios": len({r["study_id"] for r in vivos}),
                   "no_evaluables": 0, "excluidos_en_este_paso": 0, "motivos": ""})
    for k, etq in CRIT:
        antes = list(vivos)
        noev = [r for r in antes if r[k] == "no evaluable"]
        fuera = [r for r in antes if r[k] != "cumple"]
        vivos = [r for r in antes if r[k] == "cumple"]
        mot = collections.Counter(r["motivo"] for r in fuera if r["primer_requisito_que_falla"] == k)
        embudo.append({
            "filtro": etq,
            "brazos": len(vivos),
            "estudios": len({r["study_id"] for r in vivos}),
            "no_evaluables": len(noev),
            "excluidos_en_este_paso": len(fuera),
            "motivos": "; ".join("%s (%d)" % (m[:60], n) for m, n in mot.most_common(3)),
        })
    return filas, embudo


def clasifica(r):
    """Las cuatro categorías que el árbitro pidió distinguir."""
    comp = r["diseno_comparativo"] == "cumple"
    datos = r["numerador_valido"] == "cumple" and r["denominador_valido"] == "cumple"
    if r["diseno_comparativo"] == "no evaluable":
        return "brazo no evaluable: el diseño no consta"
    if comp and datos:
        return ("estudio clasificado como comparativo, con datos descriptivos; "
                "contraste causal NO utilizable: no se extrajo brazo comparador")
    if comp:
        return ("estudio clasificado como comparativo, sin datos descriptivos "
                "utilizables")
    if datos:
        return "brazo con datos descriptivos, sin diseño comparativo"
    return "brazo sin datos descriptivos ni diseño comparativo"


def main():
    grupos, excl, adj, enlace, pdfs, informes = contexto()

    juicios, sin_cita, rob = tabla_juicios(enlace, informes)
    p1 = escribe("pendiente1_juicios.csv", juicios)

    solap = tabla_solapamiento()
    p2 = escribe("pendiente2_solapamiento.csv", solap)
    est021 = bloque_est021(informes, pdfs)

    brazos, fuera, sin_traza = tabla_brazos(adj, excl, enlace, pdfs)
    p3 = escribe("pendiente3_brazos.csv", brazos)

    t6, embudo = tabla6_final(pdfs)
    p4 = escribe("pendiente4_tabla6.csv", t6)
    p5 = escribe("pendiente4_embudo.csv", embudo)

    # ---- comprobaciones que el árbitro pidió explícitamente
    inst = collections.Counter()
    for r in rob:
        if r["item"] != "GLOBAL":
            inst[r["instrumento"]] += 1
    est_inst = collections.defaultdict(set)
    for r in rob:
        est_inst[r["instrumento"]].add(r["study_id"])
    dom = sum(1 for r in rob if r["item"] != "GLOBAL")
    glob = sum(1 for r in rob if r["item"] == "GLOBAL")
    dup = [k for k, v in collections.Counter(
        (f["estudio"], f["brazo"]) for f in brazos).items() if v > 1]
    un_estudio = all(f["informe"] != FALTA for f in brazos)

    resumen = {
        "juicios": {
            "total": len(rob), "de_dominio": dom, "globales": glob,
            "rob2_estudios": len(est_inst["rob2"]), "rob2_dominios": 5,
            "robins_estudios": len(est_inst["robins"]), "robins_dominios": 7,
            "calculo": "%d x 5 = %d ; %d x 7 = %d ; %d + %d = %d de dominio ; "
                       "+ %d globales = %d"
                       % (len(est_inst["rob2"]), len(est_inst["rob2"]) * 5,
                          len(est_inst["robins"]), len(est_inst["robins"]) * 7,
                          len(est_inst["rob2"]) * 5, len(est_inst["robins"]) * 7,
                          dom, glob, len(rob)),
            "reproduce": len(est_inst["rob2"]) * 5 + len(est_inst["robins"]) * 7 == dom
                         and dom + glob == len(rob),
            "sin_cita": sin_cita,
            "con_cita": len(rob) - len(sin_cita),
        },
        "solapamiento": {
            "pares_examinados": len(solap),
            "confirmados": sum(1 for f in solap if f["veredicto"].startswith("SOLAPAMIENTO")),
            "descartados": sum(1 for f in solap if f["veredicto"].startswith("DESCARTADO")),
            "sin_leer": sum(1 for f in solap if f["veredicto"].startswith("SIN LEER")),
        },
        "est021": est021,
        "brazos": {
            "total": len(brazos), "esperado": 103,
            "duplicados": dup,
            "todos_con_informe": un_estudio,
            "sin_trazabilidad": sin_traza,
            "sin_comparador": len(brazos),
            "sin_tiempo_de_evaluacion": len(brazos),
            "brazos_de_estudios_excluidos": len(fuera),
        },
        "embudo": embudo,
    }
    (QR / "auditoria_pendientes.json").write_text(
        json.dumps(resumen, ensure_ascii=False, indent=2), encoding="utf-8", newline="\n")

    print("1. juicios      %3d filas -> %s" % (len(juicios), p1.name))
    print("   %s" % resumen["juicios"]["calculo"])
    print("   reproduce: %s | con cita: %d | sin cita: %d %s"
          % (resumen["juicios"]["reproduce"], resumen["juicios"]["con_cita"],
             len(sin_cita), sin_cita[:3]))
    print("2. solapamiento %3d pares -> %s  (%d confirmado, %d descartado, %d sin leer)"
          % (len(solap), p2.name, resumen["solapamiento"]["confirmados"],
             resumen["solapamiento"]["descartados"], resumen["solapamiento"]["sin_leer"]))
    print("3. brazos       %3d filas -> %s  (duplicados: %d | sin informe: %d)"
          % (len(brazos), p3.name, len(dup), len(sin_traza)))
    print("4. tabla 6      %3d filas -> %s" % (len(t6), p4.name))
    for e in embudo:
        print("   %-34s brazos %3d  estudios %3d  no evaluables %2d  caen %3d"
              % (e["filtro"], e["brazos"], e["estudios"], e["no_evaluables"],
                 e["excluidos_en_este_paso"]))


if __name__ == "__main__":
    main()
