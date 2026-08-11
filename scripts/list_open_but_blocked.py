"""Separa lo que esta CERRADO de lo que esta abierto pero bloqueado al robot.

POR QUE IMPORTA LA DISTINCION. Un articulo cerrado necesita prestamo
interbibliotecario: dias de espera y trabajo de biblioteca. Un articulo con
licencia abierta que el editor no sirve a una peticion automatizada necesita
diez segundos y un navegador. Meterlos en la misma lista de "no recuperados"
convierte un problema de diez minutos en uno de dos semanas.

Oxford University Press responde 403 a todo lo que no parezca un navegador, y
ScienceDirect devuelve una pagina con JavaScript en vez del fichero. En ambos
casos el articulo es de acceso abierto y su licencia lo permite; lo que falla es
el canal automatico, no el permiso.

SALIDA
    revision_sistematica/textos_completos/abiertos_pendientes.csv
    quality_reports/descargar_a_mano.md   (lista lista para trabajar)
"""
import collections
import csv
import json
import pathlib
import sys
import time
import urllib.parse
import urllib.request

ROOT = pathlib.Path(__file__).resolve().parent.parent
RS = ROOT / "revision_sistematica"
CRIB = RS / "cribado"
DEST = RS / "textos_completos" / "pdf"
OUT = RS / "textos_completos" / "abiertos_pendientes.csv"
LISTA = ROOT / "quality_reports" / "descargar_a_mano.md"
CACHE = RS / "textos_completos" / ".estado_oa.json"
csv.field_size_limit(200_000_000)
try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

CORREO = "dvchiqui@gmail.com"
UA = {"User-Agent": "SystematicReview/1.0 (mailto:%s)" % CORREO}
ABIERTOS = {"gold", "hybrid", "green", "bronze"}


def leer(p):
    with open(p, encoding="utf-8", newline="") as fh:
        return list(csv.DictReader(fh))


def jason(u, t=40):
    r = urllib.request.Request(u, headers=UA)
    with urllib.request.urlopen(r, timeout=t) as fh:
        return json.load(fh)


def main():
    cache = json.loads(CACHE.read_text(encoding="utf-8")) if CACHE.exists() else {}
    grupos = leer(CRIB / "study_groups.csv")
    pool = {p["record_id"]: p for p in
            leer(CRIB / "screening_stage2_priorizado.csv")}
    pre = {p["id_provisional"]: p for p in
           leer(RS / "extraccion" / "pre_extraccion_desde_resumen.csv")}
    reps = {"EST-%03d" % int(g["estudio"]): g for g in grupos
            if g["informe_para_extraer"] == "SI"}
    extr = {k for k, g in reps.items()
            if g["situacion"] in ("extraible", "solo-resumen")}
    tengo = {q.stem for q in DEST.iterdir()
             if q.suffix.lower() in (".pdf", ".docx")}
    faltan = sorted(extr - tengo)

    COMP = {"RCT", "non-randomised trial"}
    filas = []
    for eid in faltan:
        p = pool[reps[eid]["record_id"]]
        pmid = (p.get("pmid") or "").strip()
        doi = (p.get("doi") or "").strip()
        if doi.lower().startswith("10.1002/central/"):
            doi = ""
        if not doi and pmid:
            k = "doi:%s" % pmid
            if k not in cache:
                try:
                    r = jason("https://www.ebi.ac.uk/europepmc/webservices/rest/"
                              "search?query=EXT_ID:%s&resultType=core&format=json"
                              "&pageSize=1" % pmid)["resultList"]["result"]
                    cache[k] = (r[0].get("doi") or "") if r else ""
                except Exception:
                    cache[k] = ""
                time.sleep(0.15)
            doi = cache[k]

        estado, enlace, licencia = "sin DOI", "", ""
        if doi:
            k = "oa:%s" % doi
            if k not in cache:
                try:
                    u = jason("https://api.unpaywall.org/v2/%s?email=%s"
                              % (urllib.parse.quote(doi), CORREO))
                    mejor = u.get("best_oa_location") or {}
                    cache[k] = {"s": u.get("oa_status") or "closed",
                                "u": mejor.get("url_for_pdf") or mejor.get("url")
                                or ("https://doi.org/%s" % doi),
                                "l": mejor.get("license") or ""}
                except Exception:
                    cache[k] = {"s": "?", "u": "https://doi.org/%s" % doi,
                                "l": ""}
                time.sleep(0.15)
            estado = cache[k]["s"]
            enlace = cache[k]["u"]
            licencia = cache[k]["l"]

        d = pre.get(eid, {})
        filas.append({
            "id": eid,
            "prioridad": "ALTA" if d.get("study_design") in COMP else "normal",
            "estado_oa": estado,
            "accion": ("abrir en el navegador y guardar"
                       if estado in ABIERTOS else
                       ("préstamo interbibliotecario" if estado == "closed"
                        else "localizar a mano")),
            "diseno": d.get("study_design", ""),
            "enlace": enlace,
            "licencia": licencia,
            "revista": (reps[eid]["revista"] or "")[:52],
            "anio": reps[eid]["anio"],
            "titulo": " ".join(reps[eid]["titulo"].split())[:96],
        })

    CACHE.write_text(json.dumps(cache, ensure_ascii=False), encoding="utf-8")
    filas.sort(key=lambda f: (f["prioridad"] != "ALTA",
                              f["estado_oa"] not in ABIERTOS, f["id"]))
    with open(OUT, "w", encoding="utf-8-sig", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(filas[0].keys()))
        w.writeheader()
        w.writerows(filas)

    abiertos = [f for f in filas if f["estado_oa"] in ABIERTOS]
    cerrados = [f for f in filas if f["estado_oa"] == "closed"]
    otros = [f for f in filas if f not in abiertos and f not in cerrados]

    L = ["# Textos completos que faltan, separados por lo que hay que hacer", "",
         "Generado por `scripts/list_open_but_blocked.py`. La distinción no es",
         "cosmética: lo abierto se resuelve con un navegador y unos minutos; lo",
         "cerrado necesita préstamo interbibliotecario y días.", "",
         "## 1. Abiertos — descargar a mano (%d)" % len(abiertos), "",
         "Tienen licencia de acceso abierto. El editor devuelve 403 o una página",
         "con JavaScript a las peticiones automáticas, así que no bajan solos,",
         "pero se abren sin problema en un navegador.", "",
         "| Estudio | Prioridad | Diseño | Revista | Enlace |",
         "|---|---|---|---|---|"]
    for f in abiertos:
        L.append("| %s | %s | %s | %s (%s) | [abrir](%s) |"
                 % (f["id"], f["prioridad"], f["diseno"] or "—",
                    f["revista"], f["anio"], f["enlace"]))
    L += ["", "## 2. Cerrados — préstamo interbibliotecario (%d)" % len(cerrados),
          "", "| Estudio | Prioridad | Diseño | Revista | DOI |", "|---|---|---|---|---|"]
    for f in cerrados:
        L.append("| %s | %s | %s | %s (%s) | %s |"
                 % (f["id"], f["prioridad"], f["diseno"] or "—",
                    f["revista"], f["anio"], f["enlace"]))
    if otros:
        L += ["", "## 3. Sin DOI utilizable — localizar a mano (%d)" % len(otros),
              "", "| Estudio | Revista | Título |", "|---|---|---|"]
        for f in otros:
            L.append("| %s | %s (%s) | %s |"
                     % (f["id"], f["revista"], f["anio"], f["titulo"]))
    LISTA.write_text("\n".join(L) + "\n", encoding="utf-8", newline="\n")

    print("estudios sin texto completo : %d" % len(filas))
    print("\npor estado de acceso abierto:")
    for k, v in collections.Counter(f["estado_oa"] for f in filas).most_common():
        print("   %-10s %3d" % (k, v))
    print("\nABIERTOS, se bajan a mano en minutos : %d  (de ellos comparativos: %d)"
          % (len(abiertos), sum(1 for f in abiertos if f["prioridad"] == "ALTA")))
    print("CERRADOS, requieren peticion         : %d  (de ellos comparativos: %d)"
          % (len(cerrados), sum(1 for f in cerrados if f["prioridad"] == "ALTA")))
    print("\nescrito %s" % LISTA)
    return 0


if __name__ == "__main__":
    sys.exit(main())
