"""Vuelve a preguntar, hoy, si cada texto completo que falta se puede conseguir.

POR QUÉ HACE FALTA

`abiertos_pendientes.csv` es una foto de agosto: 24 de los 31 que faltan salen
como `closed` y con la acción «préstamo interbibliotecario». Esa foto envejece
--un artículo entra en PMC, un autor deposita el manuscrito, un embargo vence--
y ya se demostró que puede equivocarse: EST-207 figuraba como cerrado y su
texto se consiguió por el DOI en un minuto.

Este script no descarga nada. Pregunta a Europe PMC, estudio por estudio, y
deja por escrito lo que hay HOY: si está indexado, si tiene texto completo en
la propia Europe PMC, si es de acceso abierto y qué enlaces libres declara.
Decidir qué se pide y a quién es de los revisores.

No se envía ningún dato personal: la consulta es el DOI o el título.

Salida:
    revision_sistematica/textos_completos/disponibilidad_hoy.csv

Uso:
    python scripts/recheck_fulltext_availability.py
"""
import csv
import json
import pathlib
import re
import sys
import time
import urllib.parse
import urllib.request

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

ROOT = pathlib.Path(__file__).resolve().parent.parent
RS = ROOT / "revision_sistematica"
OUT = RS / "textos_completos" / "disponibilidad_hoy.csv"
API = "https://www.ebi.ac.uk/europepmc/webservices/rest/search"
# Un agente identificable es cortesia basica con una API publica y gratuita.
UA = "clo-author-systematic-review/1.0 (academic use; contact via repository)"


def consulta(q, intentos=3):
    url = API + "?" + urllib.parse.urlencode(
        {"query": q, "format": "json", "resultType": "core", "pageSize": 1})
    for i in range(intentos):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": UA})
            with urllib.request.urlopen(req, timeout=25) as r:
                return json.loads(r.read().decode("utf-8"))
        except Exception as e:
            if i == intentos - 1:
                return {"__error__": str(e)}
            time.sleep(2 * (i + 1))
    return {}


def primero(d):
    try:
        return d["resultList"]["result"][0]
    except Exception:
        return {}


def main():
    s5f = sorted((ROOT / "verificables revisión sistemática").glob(
        "S5_listado_*_estudios.csv"))
    if not s5f:
        print("no encuentro S5. Corre build_verifiables_package.py antes.")
        return 1
    s5 = list(csv.DictReader(open(s5f[0], encoding="utf-8-sig")))
    falta = [r for r in s5
             if r["situacion"] in ("extraible", "solo-resumen")
             and r["texto_completo"].strip().lower().startswith("n")]

    ap = {}
    p_ap = RS / "textos_completos" / "abiertos_pendientes.csv"
    if p_ap.exists():
        ap = {r["id"]: r for r in csv.DictReader(
            open(p_ap, encoding="utf-8-sig"))}

    filas = []
    for i, r in enumerate(falta, 1):
        a = ap.get(r["id"], {})
        m = re.search(r"10\.[^\s]+", a.get("enlace", ""))
        doi = m.group(0) if m else ""
        # Por DOI cuando lo hay; si no, por titulo entrecomillado, que es lo
        # unico que identifica el articulo sin inventar nada.
        q = ('DOI:"%s"' % doi) if doi else ('TITLE:"%s"'
                                            % r["titulo"].rstrip(".").replace('"', ""))
        res = primero(consulta(q))
        err = res.get("__error__", "")
        libre = []
        for u in (res.get("fullTextUrlList", {}) or {}).get("fullTextUrl", []):
            if u.get("availability") in ("Free", "Open access"):
                libre.append(u.get("url", ""))
        fila = {
            "study_id": r["id"], "diseno": r["diseno"],
            "estado_agosto": a.get("estado_oa", ""),
            "doi": doi,
            "encontrado": "sí" if res and not err else "no",
            "pmid": res.get("pmid", ""), "pmcid": res.get("pmcid", ""),
            "en_europepmc": res.get("inEPMC", ""),
            "acceso_abierto": res.get("isOpenAccess", ""),
            "tiene_pdf": res.get("hasPDF", ""),
            "enlaces_libres": " | ".join(dict.fromkeys(libre))[:400],
            "titulo": r["titulo"][:120],
            "error": err[:80],
        }
        filas.append(fila)
        marca = ("ABIERTO" if fila["acceso_abierto"] == "Y"
                 else "en EPMC" if fila["en_europepmc"] == "Y"
                 else "libre" if libre else "-")
        print("  [%2d/%d] %s %-20s %-8s %s" % (
            i, len(falta), r["id"], (r["diseno"] or "")[:20], marca,
            fila["pmcid"] or fila["pmid"] or ""), flush=True)
        time.sleep(0.4)

    with open(OUT, "w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, list(filas[0].keys()))
        w.writeheader()
        w.writerows(filas)

    ganables = [f for f in filas
                if f["acceso_abierto"] == "Y" or f["en_europepmc"] == "Y"
                or f["enlaces_libres"]]
    print("\n%d estudios sin texto completo" % len(filas))
    print("  con alguna via libre HOY: %d" % len(ganables))
    for f in ganables:
        print("    %s  %-20s %s" % (f["study_id"], (f["diseno"] or "")[:20],
                                    (f["enlaces_libres"] or f["pmcid"])[:90]))
    print("\nescrito %s" % OUT.name)


if __name__ == "__main__":
    main()
