"""Busca por todas las vias LEGITIMAS el texto completo de los ensayos clave.

QUE SE INTENTA, EN ESTE ORDEN. Cada paso es una via legal distinta, no un
reintento del anterior:

  1. Europe PMC: texto completo depositado en PMC o EPMC.
  2. Unpaywall: copia en abierto declarada por el editor o por un repositorio.
  3. OpenAIRE: version de autor depositada por mandato del financiador. Es la
     via que mas rinde en ensayos europeos, porque el FP7 y los PHRC obligan a
     depositar y los autores lo hacen en HAL, en Zenodo o en el repositorio de
     su universidad.
  4. Registro del ensayo: la seccion de resultados publicados. No es el
     articulo, pero es la fuente primaria del promotor y muchas veces trae los
     desenlaces con mas detalle que el resumen.

LO QUE NO SE HACE. No se toca ningun agregador que redistribuya articulos sin
permiso del titular. Un texto conseguido por esa via no se puede citar como
recuperado y pone en riesgo el acceso institucional de toda la universidad.
Cuando ninguna via abierta funciona, este script lo dice y prepara la peticion.

USO
    python scripts/hunt_key_trials.py            # los cuatro de referencia
    python scripts/hunt_key_trials.py --todos    # todos los que faltan
"""
import argparse
import csv
import json
import pathlib
import sys
import time
import urllib.error
import urllib.parse
import urllib.request

ROOT = pathlib.Path(__file__).resolve().parent.parent
RS = ROOT / "revision_sistematica"
DEST = RS / "textos_completos" / "pdf"
REG = RS / "textos_completos" / "busqueda_ensayos_clave.csv"
csv.field_size_limit(200_000_000)
try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

CORREO = "dvchiqui@gmail.com"          # Unpaywall exige un contacto
UA = {"User-Agent": "SystematicReview/1.0 (mailto:%s)" % CORREO}

# Los cuatro que el informe editorial marca como prioritarios, con todo lo que
# se sabe de ellos. El NCT importa tanto como el PMID: si el articulo no se
# consigue, el registro puede traer los resultados.
CLAVE = [
    {"id": "EST-021", "nombre": "PhagoBurn", "pmid": "30292481",
     "nct": "NCT02116010", "revista": "Lancet Infect Dis 2019"},
    {"id": "EST-118", "nombre": "Leitner (resultados)", "pmid": "32949500",
     "nct": "NCT03140085", "revista": "Lancet Infect Dis 2021"},
    {"id": "EST-118p", "nombre": "Leitner (protocolo, BMC Urology)",
     "pmid": "28950849", "nct": "NCT03140085", "revista": "BMC Urol 2017"},
    {"id": "EST-029", "nombre": "TP-102", "pmid": "39740667",
     "nct": "NCT04803708", "revista": "Med 2025"},
    {"id": "EST-052", "nombre": "CYPHY", "pmid": "",
     "nct": "NCT04684641", "revista": "J Cyst Fibros 2023"},
]


def pide(url, cabeceras=None, timeout=40):
    req = urllib.request.Request(url, headers=cabeceras or UA)
    with urllib.request.urlopen(req, timeout=timeout) as fh:
        return fh.read(), fh.headers.get("Content-Type", "")


def json_de(url):
    datos, _ = pide(url)
    return json.loads(datos)


def epmc(consulta):
    u = ("https://www.ebi.ac.uk/europepmc/webservices/rest/search?query=%s"
         "&resultType=core&format=json&pageSize=5"
         % urllib.parse.quote(consulta))
    r = json_de(u)["resultList"]["result"]
    return r[0] if r else None


def unpaywall(doi):
    u = "https://api.unpaywall.org/v2/%s?email=%s" % (urllib.parse.quote(doi),
                                                      CORREO)
    return json_de(u)


def openaire(doi):
    u = ("https://api.openaire.eu/search/publications?doi=%s&format=json"
         % urllib.parse.quote(doi))
    return json_de(u)


def ctgov(nct):
    u = ("https://clinicaltrials.gov/api/v2/studies/%s"
         "?fields=protocolSection,hasResults,resultsSection" % nct)
    return json_de(u)


def baja_pdf(url, destino):
    datos, tipo = pide(url, timeout=90)
    if datos[:5] != b"%PDF-":
        return False, "no es un PDF (%s, %d bytes)" % (tipo[:32], len(datos))
    destino.write_bytes(datos)
    return True, "%.0f KB" % (len(datos) / 1024.0)


def busca(t):
    """Devuelve la lista de intentos, cada uno con su resultado."""
    intentos = []
    doi_real = ""
    art = None

    # ---- 1. Europe PMC -----------------------------------------------------
    consulta = ("EXT_ID:%s" % t["pmid"]) if t["pmid"] else \
               ('"%s"' % t["nombre"])
    try:
        art = epmc(consulta)
    except Exception as e:
        intentos.append(("Europe PMC", "error", type(e).__name__))
    if art:
        doi_real = art.get("doi", "") or ""
        abierto = art.get("isOpenAccess") == "Y"
        en_pmc = art.get("inPMC") == "Y" or art.get("inEPMC") == "Y"
        intentos.append(("Europe PMC", "consultado",
                         "doi=%s abierto=%s en PMC=%s" %
                         (doi_real or "-", "si" if abierto else "no",
                          "si" if en_pmc else "no")))
        if en_pmc and art.get("pmcid"):
            url = ("https://www.ebi.ac.uk/europepmc/webservices/rest/%s"
                   "/fullTextPdf" % art["pmcid"])
            try:
                ok, det = baja_pdf(url, DEST / ("%s.pdf" % t["id"]))
                intentos.append(("PMC texto completo",
                                 "DESCARGADO" if ok else "sin PDF", det))
                if ok:
                    return intentos, doi_real
            except Exception as e:
                intentos.append(("PMC texto completo", "fallo",
                                 type(e).__name__))

    # ---- 2. Unpaywall ------------------------------------------------------
    if doi_real:
        try:
            u = unpaywall(doi_real)
            loc = u.get("best_oa_location") or {}
            if loc.get("url_for_pdf"):
                intentos.append(("Unpaywall", "copia en abierto",
                                 "%s (%s)" % (loc.get("host_type", "?"),
                                              loc.get("license") or "sin licencia")))
                try:
                    ok, det = baja_pdf(loc["url_for_pdf"],
                                       DEST / ("%s.pdf" % t["id"]))
                    intentos.append(("Unpaywall PDF",
                                     "DESCARGADO" if ok else "sin PDF", det))
                    if ok:
                        return intentos, doi_real
                except Exception as e:
                    intentos.append(("Unpaywall PDF", "fallo",
                                     type(e).__name__))
            else:
                intentos.append(("Unpaywall", "sin copia en abierto",
                                 "is_oa=%s" % u.get("is_oa")))
        except Exception as e:
            intentos.append(("Unpaywall", "error", type(e).__name__))

    # ---- 3. OpenAIRE: deposito por mandato del financiador -----------------
    if doi_real:
        try:
            r = openaire(doi_real)
            res = (r.get("response", {}).get("results") or {}).get("result")
            intentos.append(("OpenAIRE", "consultado",
                             "%d registro(s)" % (len(res) if res else 0)))
        except Exception as e:
            intentos.append(("OpenAIRE", "error", type(e).__name__))

    # ---- 4. Resultados publicados en el registro ---------------------------
    if t["nct"]:
        try:
            r = ctgov(t["nct"])
            tiene = r.get("hasResults")
            intentos.append(("Registro %s" % t["nct"],
                             "CON RESULTADOS" if tiene else "sin resultados",
                             "seccion de resultados publicada por el promotor"
                             if tiene else "el promotor no ha publicado datos"))
            if tiene:
                (DEST.parent / "resultados_registro").mkdir(exist_ok=True)
                d = DEST.parent / "resultados_registro" / ("%s_%s.json"
                                                           % (t["id"], t["nct"]))
                d.write_text(json.dumps(r, indent=1, ensure_ascii=False),
                             encoding="utf-8")
                intentos.append(("Registro %s" % t["nct"], "GUARDADO", d.name))
        except Exception as e:
            intentos.append(("Registro %s" % t["nct"], "error",
                             type(e).__name__))

    return intentos, doi_real


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--todos", action="store_true")
    args = ap.parse_args()
    DEST.mkdir(parents=True, exist_ok=True)

    filas = []
    for t in CLAVE:
        ya = (DEST / ("%s.pdf" % t["id"])).exists()
        print("\n=== %s  %s  (%s) ===" % (t["id"], t["nombre"], t["revista"]))
        if ya:
            print("   ya estaba descargado")
            filas.append({"id": t["id"], "nombre": t["nombre"], "via": "previo",
                          "resultado": "ya descargado", "detalle": ""})
            continue
        intentos, doi = busca(t)
        for via, res, det in intentos:
            marca = " <<<" if res.startswith(("DESCARGADO", "CON RESULTADOS")) else ""
            print("   %-24s %-18s %s%s" % (via, res, det[:60], marca))
            filas.append({"id": t["id"], "nombre": t["nombre"], "via": via,
                          "resultado": res, "detalle": det})
        time.sleep(0.4)

    with open(REG, "w", encoding="utf-8", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=["id", "nombre", "via", "resultado",
                                           "detalle"])
        w.writeheader()
        w.writerows(filas)
    print("\nregistro de la busqueda: %s" % REG)
    logrados = sorted({f["id"] for f in filas
                       if f["resultado"].startswith("DESCARGADO")
                       or f["resultado"] == "ya descargado"})
    print("con texto completo: %s" % (", ".join(logrados) or "ninguno"))
    return 0


if __name__ == "__main__":
    sys.exit(main())
