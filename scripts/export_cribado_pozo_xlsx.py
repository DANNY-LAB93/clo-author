"""Exporta a un solo libro de Excel todo el cribado del pozo priorizado.

POR QUE. Sin plataforma de cribado, el libro ES el artefacto que revisa una
persona y que pediría un referee. Tiene que llevar TODAS las decisiones, no solo
las que sobrevivieron: un registro de cribado que enseña únicamente lo que pasó
no se puede auditar. Por eso la hoja de etapa 2 trae los 13.509 registros y no
solo los 460 que avanzaron.

`export_screening_xlsx.py` exporta el brazo antiguo indexado por PMID (1.320
registros). Este exporta el pozo completo de todas las fuentes, indexado por
`record_id`, y mantiene separadas las dos corrientes PRISMA 2020 -- bases de
datos y registros de ensayos.

HOJAS
  Resumen              recuento por etapa y corriente, y estado de la auditoría
  Texto_completo       los informes que pasan a texto completo: la lista de trabajo,
                       agrupada por estudio y con columnas vacías para el revisor
  Estudios_repetidos   informes que comparten NCT: varios informes de un mismo ensayo
  Etapa3_resumen       toda decisión por resumen, con motivo y autor
  Etapa3_registros     toda decisión sobre ficha de registro
  Etapa2_titulo        toda decisión por título (13.509 filas)
  Motivos              exclusiones agrupadas por código y etapa
  Controles_positivos  los 40 estudios de control y dónde está cada uno

Es una VISTA, nunca una fuente: se regenera después de cada lote.

USO
    python scripts/export_cribado_pozo_xlsx.py
"""
import collections
import csv
import datetime
import pathlib
import re
import sys

try:
    import openpyxl
    from openpyxl.styles import Alignment, Font, PatternFill
    from openpyxl.utils import get_column_letter
except ImportError:
    raise SystemExit("hace falta openpyxl: python -m pip install openpyxl")

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from screen_stage1_rules import known_pmids
from exclusion_codes import CODES, code_for

ROOT = pathlib.Path(__file__).resolve().parent.parent
POOL = ROOT / "revision_sistematica" / "cribado" / "screening_stage2_priorizado.csv"
S2 = ROOT / "revision_sistematica" / "cribado" / "screening_stage2_pool_decisions.csv"
S3 = ROOT / "revision_sistematica" / "cribado" / "screening_stage3_pool_decisions.csv"
OUT = ROOT / "quality_reports" / "cribado_pozo.xlsx"

csv.field_size_limit(200_000_000)

CAB = PatternFill("solid", fgColor="1F4E79")
CABF = Font(color="FFFFFF", bold=True)
PENDIENTE = PatternFill("solid", fgColor="FFF2CC")   # columnas que rellena el revisor
AVISO = PatternFill("solid", fgColor="FCE4D6")


def norm_titulo(t):
    return re.sub(r"[^a-z0-9]+", "", (t or "").lower())[:80]


def cargar_indice():
    """identificador -> study_id, para saber qué informes ya están extraídos."""
    idx = {}
    ruta = ROOT / "quality_reports" / "corpus_identifier_index.txt"
    for linea in ruta.read_text(encoding="utf-8").splitlines():
        if linea.startswith("#") or "\t" not in linea:
            continue
        ident, sid = linea.split("\t", 1)
        idx[ident.strip().lower()] = sid.strip()
    return idx


def estudio_corpus(rec, idx):
    """Devuelve el study_id si este informe ya pertenece a un estudio extraído.

    Separa los 268 en dos montones muy distintos para quien revisa: los que solo
    hay que confirmar y los que hay que valorar de cero. Sin esta columna, un
    revisor vuelve a leer de principio a fin estudios que ya están extraídos.
    """
    for pref, val in (("doi", rec["doi"]), ("pmid", rec["pmid"]), ("nct", rec["nct"])):
        v = (val or "").strip().lower()
        if v and "%s:%s" % (pref, v) in idx:
            return idx["%s:%s" % (pref, v)]
    return ""


def estado_id(rec, resuelto=None):
    """Qué hace falta para localizar el texto completo de este registro.

    El orden importa. La primera versión comprobaba el DOI antes que nada y, como
    Cochrane CENTRAL asigna un DOI sustituto propio (10.1002/central/...) a todo
    lo que indexa, daba por irrecuperables 35 informes que tenían PMID o NCT
    perfectamente utilizables. Se comprueban primero las vías que sí resuelven.
    """
    doi = (rec["doi"] or "").strip().lower()
    if doi and not doi.startswith("10.1002/central/"):
        return "DOI editorial"
    if (rec["pmid"] or "").strip():
        return "recuperable por PMID"
    if (rec["nct"] or "").strip():
        return "recuperable por NCT (ficha de registro)"
    if resuelto and resuelto.get("identificador_resuelto"):
        return "%s: %s" % (resuelto["tipo"], resuelto["identificador_resuelto"])
    if resuelto:
        return "búsqueda por cita — %s" % resuelto["via"]
    return "SIN IDENTIFICADOR: localización manual"


def cargar_resueltos():
    ruta = ROOT / "revision_sistematica" / "textos_completos" / "fulltext_identifiers.csv"
    if not ruta.exists():
        return {}
    with open(ruta, encoding="utf-8", newline="") as fh:
        return {r["record_id"]: r for r in csv.DictReader(fh)}


def hoja(wb, titulo, cabeceras, filas, anchos, congelar="A2", cols_revisor=()):
    ws = wb.create_sheet(titulo)
    ws.append(cabeceras)
    for c in range(1, len(cabeceras) + 1):
        ws.cell(1, c).fill = CAB
        ws.cell(1, c).font = CABF
        ws.cell(1, c).alignment = Alignment(vertical="center", wrap_text=True)
    for fila in filas:
        ws.append(fila)
    for i, ancho in enumerate(anchos, start=1):
        ws.column_dimensions[get_column_letter(i)].width = ancho
    for c in cols_revisor:
        for r in range(2, ws.max_row + 1):
            ws.cell(r, c).fill = PENDIENTE
    ws.freeze_panes = congelar
    ws.auto_filter.ref = "A1:%s%d" % (get_column_letter(len(cabeceras)), ws.max_row)
    return ws


def main():
    with open(POOL, encoding="utf-8", newline="") as fh:
        pool = list(csv.DictReader(fh))
    por_id = {p["record_id"]: p for p in pool}
    with open(S2, encoding="utf-8", newline="") as fh:
        s2 = {d["record_id"]: d for d in csv.DictReader(fh)}
    with open(S3, encoding="utf-8", newline="") as fh:
        s3 = {d["record_id"]: d for d in csv.DictReader(fh)}

    wb = openpyxl.Workbook()
    wb.remove(wb.active)
    hoy = datetime.date.today().isoformat()

    # ---------- agrupación en estudios ----------
    # La agrupación NO se calcula aquí: la produce group_reports_into_studies.py,
    # que encadena NCT propio -> NCT declarado en el resumen -> atribución
    # razonada -> título. Repetir aquí una versión simplificada fue justo el
    # error que hizo aparecer los siete resúmenes del BX004-A como siete
    # estudios distintos, que es el doble recuento que la agrupación evita.
    ft = [por_id[rid] for rid, d in s3.items()
          if d["verdict"] == "FULLTEXT" and rid in por_id]
    ft.sort(key=lambda r: int(r["orden"]))
    ruta_grupos = ROOT / "revision_sistematica" / "cribado" / "study_groups.csv"
    if not ruta_grupos.exists():
        raise SystemExit("falta study_groups.csv: ejecuta antes "
                         "python scripts/group_reports_into_studies.py")
    with open(ruta_grupos, encoding="utf-8", newline="") as fh:
        gr = {r["record_id"]: r for r in csv.DictReader(fh)}
    clave = {rid: g["clave"] for rid, g in gr.items()}
    grupos = collections.Counter(clave.values())
    orden_grupo = {g["clave"]: int(g["estudio"]) for g in gr.values()}

    # ---------- Resumen ----------
    ws = wb.create_sheet("Resumen")
    ws.append(["Cribado del pozo priorizado -- fagoterapia en P. aeruginosa MDR/XDR/PDR"])
    ws["A1"].font = Font(bold=True, size=13)
    ws.append(["Generado", hoy])
    ws.append(["Fuente", "revision_sistematica/cribado/screening_stage2_pool_decisions.csv + screening_stage3_pool_decisions.csv"])
    ws.append([])

    adv = sum(1 for d in s2.values() if d["verdict"] == "ADVANCE"
              and d["record_id"] in por_id)
    exc2 = sum(1 for rid, d in s2.items() if d["verdict"] == "EXCLUDE" and rid in por_id)
    base = [d for d in s3.values() if d["corriente"] == "base"]
    reg = [d for d in s3.values() if d["corriente"] == "registro"]
    b_ft = sum(1 for d in base if d["verdict"] == "FULLTEXT")
    r_ft = sum(1 for d in reg if d["verdict"] == "FULLTEXT")

    for fila in [
        ["Etapa", "Entran", "Avanzan", "Excluidos"],
        ["2. Cribado por título (pozo completo)", len(pool), adv, exc2],
        ["3a. Resumen -- corriente de bases de datos", len(base), b_ft, len(base) - b_ft],
        ["3b. Ficha -- corriente de registros de ensayos", len(reg), r_ft, len(reg) - r_ft],
        ["Total a texto completo (informes)", "", b_ft + r_ft, ""],
        ["ESTUDIOS distintos (unidad de inclusión)", "", len(orden_grupo), ""],
    ]:
        ws.append(fila)

    idx0 = cargar_indice()
    ya = [r for r in ft if estudio_corpus(r, idx0)]
    ws.append([])
    ws.append(["Reparto de la carga de texto completo"])
    ws.cell(ws.max_row, 1).font = Font(bold=True)
    ws.append(["Informes que ya pertenecen a un estudio extraído", len(ya)])
    ws.append(["  -- estudios distintos que cubren", len({estudio_corpus(r, idx0) for r in ya})])
    ws.append(["Candidatos nuevos por valorar de cero", len(ft) - len(ya)])
    ws.append(["Estudios del corpus sin ningún informe entre los recuperados",
               len(set(idx0.values()) - {estudio_corpus(r, idx0) for r in ya})])
    ws.append([])
    ws.append(["Situación de los estudios (regla: la unidad de inclusión es el estudio)"])
    ws.cell(ws.max_row, 1).font = Font(bold=True)
    sit = collections.Counter()
    for g in gr.values():
        sit[(g["clave"], g["situacion"])] = 1
    cnt = collections.Counter(s for _, s in sit)
    for etiqueta, texto in (
            ("extraible", "con artículo del que extraer"),
            ("solo-resumen", "solo resumen de congreso -> entran en el análisis de sensibilidad"),
            ("solo-registro", "solo ficha de registro -> en curso o sin resultados publicados")):
        ws.append([texto, cnt.get(etiqueta, 0)])
    for c in range(1, 5):
        ws.cell(5, c).fill = CAB
        ws.cell(5, c).font = CABF

    ws.append([])
    known = known_pmids()
    por_estudio = collections.defaultdict(list)
    for p in pool:
        if p["pmid"] and p["pmid"] in known and p["record_id"] in s3:
            por_estudio[known[p["pmid"]]].append(s3[p["record_id"]]["verdict"])
    con_ft = sum(1 for v in por_estudio.values() if "FULLTEXT" in v)
    ws.append(["Auditoría de control positivo"])
    ws.cell(ws.max_row, 1).font = Font(bold=True)
    ws.append(["Estudios de control conocidos", len(por_estudio)])
    ws.append(["Conservan al menos un informe a texto completo", con_ft])
    ws.append(["Resultado", "PASS" if con_ft == len(por_estudio) else "FALLO"])
    if con_ft != len(por_estudio):
        ws.cell(ws.max_row, 2).fill = AVISO
    ws.append([])
    ws.append(["Cómo leer este libro"])
    ws.cell(ws.max_row, 1).font = Font(bold=True)
    for t in [
        "Las columnas en amarillo de la hoja Texto_completo están vacías a propósito: las rellena quien revise.",
        "Etapa2_titulo trae los 13.509 registros, no solo los que avanzaron: un cribado solo es auditable si se ve también lo excluido.",
        "Un mismo ensayo puede aparecer en varias filas (protocolo, congreso, artículo, ficha). La columna 'estudio' los agrupa.",
        "Los motivos usan el vocabulario cerrado de scripts/exclusion_codes.py, idéntico en las dos etapas.",
    ]:
        ws.append([t])
    ws.column_dimensions["A"].width = 62
    for col in "BCD":
        ws.column_dimensions[col].width = 16

    # ---------- Texto_completo ----------
    idx = cargar_indice()
    resueltos = cargar_resueltos()
    filas = []
    for r in ft:
        k = clave[r["record_id"]]
        d = s3[r["record_id"]]
        sid = estudio_corpus(r, idx)
        res = resueltos.get(r["record_id"])
        g = gr[r["record_id"]]
        filas.append([
            orden_grupo[k], grupos[k], g["informe_para_extraer"], g["situacion"],
            g["tipo_informe"], int(r["orden"]),
            sid or "CANDIDATO NUEVO", r["year"], " ".join(r["title"].split()),
            r["journal"], r["doi"], r["pmid"], r["nct"], r["sources"],
            estado_id(r, res), (res or {}).get("duplicado_interno", ""),
            "", "", "", "",
        ])
    ws = hoja(wb, "Texto_completo",
              ["estudio", "informes del estudio", "EXTRAER DE ESTE", "situación",
               "tipo de informe", "orden", "¿ya extraído?", "año", "título",
               "revista", "doi", "pmid", "nct", "fuentes", "cómo recuperarlo",
               "posible duplicado interno",
               "INCLUIR/EXCLUIR", "motivo", "revisor", "fecha"],
              filas,
              [8, 10, 16, 15, 19, 8, 24, 7, 66, 26, 30, 11, 14, 24, 40, 42,
               15, 30, 14, 12],
              cols_revisor=(17, 18, 19, 20))
    verde = PatternFill("solid", fgColor="E2EFDA")
    for r in range(2, ws.max_row + 1):
        if ws.cell(r, 3).value == "SI":
            ws.cell(r, 3).fill = verde
        if ws.cell(r, 4).value in ("solo-resumen", "solo-registro"):
            ws.cell(r, 4).fill = AVISO
        if ws.cell(r, 7).value == "CANDIDATO NUEVO":
            ws.cell(r, 7).fill = AVISO
        if str(ws.cell(r, 15).value or "").startswith(("búsqueda", "SIN")):
            ws.cell(r, 15).fill = AVISO

    # ---------- Recuperacion ----------
    if resueltos:
        filas = []
        for rid, f in resueltos.items():
            filas.append([int(f["orden"]), f["tipo"], f["identificador_resuelto"],
                          f["via"], f["nota"], f["duplicado_interno"],
                          f["anio"], f["titulo"][:170], f["revista"], f["fuentes"]])
        filas.sort(key=lambda x: x[0])
        hoja(wb, "Recuperacion",
             ["orden", "tipo de informe", "identificador recuperado", "vía",
              "nota", "posible duplicado interno", "año", "título", "revista", "fuentes"],
             filas, [8, 26, 24, 42, 46, 42, 7, 74, 28, 20])

    # ---------- Estudios_repetidos ----------
    filas = []
    for r in ft:
        k = clave[r["record_id"]]
        if grupos[k] > 1:
            filas.append([orden_grupo[k], grupos[k], int(r["orden"]),
                          k if not k.startswith("T:") else "(sin NCT: agrupado por título)",
                          r["year"], " ".join(r["title"].split())[:150], r["journal"]])
    filas.sort(key=lambda f: (f[0], f[2]))
    hoja(wb, "Estudios_repetidos",
         ["estudio", "informes", "orden", "clave de agrupación", "año", "título", "revista"],
         filas, [8, 9, 8, 30, 7, 80, 26])

    # ---------- Etapa 3 ----------
    for nombre, corriente in (("Etapa3_resumen", "base"), ("Etapa3_registros", "registro")):
        filas = []
        for rid, d in s3.items():
            if d["corriente"] != corriente or rid not in por_id:
                continue
            r = por_id[rid]
            filas.append([int(d["orden"]), d["verdict"], code_for(d["reason"]) or "",
                          d["reason"], r["year"], " ".join(r["title"].split())[:200],
                          r["doi"], r["pmid"], r["nct"], d["decided_by"], d["decided_at"]])
        filas.sort(key=lambda f: f[0])
        hoja(wb, nombre,
             ["orden", "veredicto", "código", "motivo", "año", "título", "doi",
              "pmid", "nct", "decidido por", "fecha"],
             filas, [8, 11, 8, 46, 7, 78, 28, 11, 14, 34, 17])

    # ---------- Etapa 2 ----------
    filas = []
    for r in pool:
        d = s2.get(r["record_id"])
        if not d:
            continue
        filas.append([int(r["orden"]), d["verdict"],
                      code_for(d["reason"]) or "" if d["verdict"] == "EXCLUDE" else "",
                      d["reason"], r["year"], " ".join(r["title"].split())[:200],
                      r["doi"], r["pmid"], r["sources"]])
    filas.sort(key=lambda f: f[0])
    hoja(wb, "Etapa2_titulo",
         ["orden", "veredicto", "código", "motivo", "año", "título", "doi", "pmid", "fuentes"],
         filas, [8, 11, 8, 46, 7, 78, 28, 11, 26])

    # ---------- Motivos ----------
    filas = []
    for etiqueta, log, filtro in (
            ("2. título", s2, lambda d: d["record_id"] in por_id),
            ("3a. resumen", s3, lambda d: d["corriente"] == "base"),
            ("3b. ficha de registro", s3, lambda d: d["corriente"] == "registro")):
        cnt = collections.Counter()
        for d in log.values():
            if d["verdict"] != "EXCLUDE" or not filtro(d):
                continue
            cnt[code_for(d["reason"]) or "(sin código)"] += 1
        for cod, n in cnt.most_common():
            filas.append([etiqueta, cod, n, CODES.get(cod, "—")])
    hoja(wb, "Motivos", ["etapa", "código", "n", "definición"], filas, [22, 10, 8, 76])

    # ---------- Controles positivos ----------
    filas = []
    for sid in sorted(por_estudio):
        recs = [p for p in pool if p["pmid"] and known.get(p["pmid"]) == sid]
        v2 = {s2[p["record_id"]]["verdict"] for p in recs if p["record_id"] in s2}
        v3 = {s3[p["record_id"]]["verdict"] for p in recs if p["record_id"] in s3}
        filas.append([sid, len(recs), ", ".join(sorted(v2)) or "—",
                      ", ".join(sorted(v3)) or "—",
                      "OK" if "FULLTEXT" in v3 else "REVISAR",
                      ", ".join(str(p["orden"]) for p in recs)])
    hoja(wb, "Controles_positivos",
         ["estudio", "informes en el pozo", "etapa 2", "etapa 3", "estado", "posiciones"],
         filas, [30, 15, 22, 22, 12, 26])
    ws = wb["Controles_positivos"]
    for r in range(2, ws.max_row + 1):
        if ws.cell(r, 5).value != "OK":
            ws.cell(r, 5).fill = AVISO

    wb.save(OUT)
    print("escrito %s" % OUT)
    print("  %d informes a texto completo, en %d estudios distintos"
          % (len(ft), len(orden_grupo)))
    print("  auditoría de control positivo: %s"
          % ("PASS" if con_ft == len(por_estudio) else "FALLO"))


if __name__ == "__main__":
    main()
