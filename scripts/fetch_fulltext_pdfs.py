"""Descarga los textos completos que están en acceso abierto, por vía legítima.

QUÉ HACE Y QUÉ NO. Consulta Europe PMC, que publica una API REST pensada
exactamente para esto, y baja el PDF solo cuando el registro está marcado como
acceso abierto. No entra en webs de editoriales ni intenta sortear muros de
pago: además de estar prohibido por los términos de uso de Elsevier, Springer y
compañía, la descarga masiva desde una IP institucional acaba con esa IP
bloqueada para todo el mundo en la universidad.

LO QUE NO SE PUEDA BAJAR NO ES UN FALLO DEL SCRIPT. Es el estado real del
acceso, y conviene tenerlo por escrito: sale un listado de lo pendiente para
pedirlo por préstamo interbibliotecario.

Se identifica al descargar, como pide la etiqueta de uso de la API, y espera
entre peticiones. Un script de descarga que no se identifica ni espera es la
razón por la que estos servicios acaban poniendo límites.

SALIDA
    revision_sistematica/textos_completos/pdf/<id_provisional>.pdf
    revision_sistematica/textos_completos/fulltext_download_log.csv

USO
    python scripts/fetch_fulltext_pdfs.py --probe 15    # tantea el rendimiento
    python scripts/fetch_fulltext_pdfs.py               # todo
"""
import argparse
import csv
import json
import pathlib
import sys
import time
import urllib.parse
import urllib.request

ROOT = pathlib.Path(__file__).resolve().parent.parent
GRUPOS = ROOT / "revision_sistematica" / "cribado" / "study_groups.csv"
POOL = ROOT / "revision_sistematica" / "cribado" / "screening_stage2_priorizado.csv"
DEST = ROOT / "revision_sistematica" / "textos_completos" / "pdf"
LOG = ROOT / "revision_sistematica" / "textos_completos" / "fulltext_download_log.csv"

API = "https://www.ebi.ac.uk/europepmc/webservices/rest/search"
UA = ("revision-sistematica-fagoterapia/1.0 "
      "(Universidad Catolica de Cuenca; contacto: dvchiqui@gmail.com)")
PAUSA = 1.0        # segundos entre peticiones

csv.field_size_limit(200_000_000)
try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass


def pedir(url, binario=False, timeout=45):
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return r.read() if binario else json.loads(r.read().decode("utf-8"))


def buscar(doi, pmid):
    """Devuelve (pmcid, url_pdf, es_abierto) o (None, None, False)."""
    consultas = []
    if pmid:
        consultas.append("EXT_ID:%s AND SRC:MED" % pmid)
    if doi:
        consultas.append('DOI:"%s"' % doi)
    for q in consultas:
        url = "%s?%s" % (API, urllib.parse.urlencode(
            {"query": q, "format": "json", "resultType": "core", "pageSize": 1}))
        try:
            d = pedir(url)
        except Exception:
            continue
        res = d.get("resultList", {}).get("result", [])
        if not res:
            continue
        r = res[0]
        abierto = r.get("isOpenAccess") == "Y"
        pmcid = r.get("pmcid")
        pdf = None
        for it in r.get("fullTextUrlList", {}).get("fullTextUrl", []):
            if it.get("documentStyle") == "pdf" and it.get("availability") in (
                    "Open access", "Free"):
                pdf = it.get("url")
                break
        if not pdf and pmcid and abierto:
            pdf = ("https://www.ebi.ac.uk/europepmc/webservices/rest/"
                   "%s/fullTextPDF" % pmcid)
        return pmcid, pdf, abierto
    return None, None, False


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--probe", type=int, default=0,
                    help="probar solo con los N primeros y no guardar nada")
    args = ap.parse_args()

    with open(POOL, encoding="utf-8", newline="") as fh:
        pool = {p["record_id"]: p for p in csv.DictReader(fh)}
    with open(GRUPOS, encoding="utf-8", newline="") as fh:
        fuentes = [g for g in csv.DictReader(fh)
                   if g["informe_para_extraer"] == "SI"
                   and g["situacion"] in ("extraible", "solo-resumen")]
    fuentes.sort(key=lambda g: int(g["estudio"]))
    if args.probe:
        fuentes = fuentes[:args.probe]

    DEST.mkdir(parents=True, exist_ok=True)
    hechos = {p.stem for p in DEST.glob("*.pdf")}
    filas, bajados, ya, cerrados, sin = [], 0, 0, 0, 0

    for g in fuentes:
        eid = "EST-%03d" % int(g["estudio"])
        rec = pool[g["record_id"]]
        doi = (rec["doi"] or "").strip()
        if doi.lower().startswith("10.1002/central/"):
            doi = ""                       # el DOI sustituto de CENTRAL no resuelve
        pmid = (rec["pmid"] or "").strip()

        if eid in hechos:
            ya += 1
            continue
        if not doi and not pmid:
            sin += 1
            filas.append({"id": eid, "estado": "sin identificador consultable",
                          "pmcid": "", "url": "", "revista": rec["journal"][:60]})
            continue

        pmcid, pdf, abierto = buscar(doi, pmid)
        time.sleep(PAUSA)
        if not pdf:
            cerrados += 1
            filas.append({"id": eid,
                          "estado": "sin PDF abierto" + ("" if abierto else " (no es acceso abierto)"),
                          "pmcid": pmcid or "", "url": "", "revista": rec["journal"][:60]})
            continue
        if args.probe:
            bajados += 1
            filas.append({"id": eid, "estado": "descargable", "pmcid": pmcid or "",
                          "url": pdf, "revista": rec["journal"][:60]})
            continue
        try:
            datos = pedir(pdf, binario=True, timeout=90)
            # Un HTML de error pesa poco y empieza por '<'. Guardarlo como PDF
            # dejaría 159 archivos que parecen artículos y no lo son.
            if len(datos) < 20000 or not datos[:5].startswith(b"%PDF"):
                raise ValueError("la respuesta no es un PDF (%d bytes)" % len(datos))
            (DEST / ("%s.pdf" % eid)).write_bytes(datos)
            bajados += 1
            filas.append({"id": eid, "estado": "descargado", "pmcid": pmcid or "",
                          "url": pdf, "revista": rec["journal"][:60]})
        except Exception as e:
            cerrados += 1
            filas.append({"id": eid, "estado": "fallo: %s" % str(e)[:60],
                          "pmcid": pmcid or "", "url": pdf, "revista": rec["journal"][:60]})
        time.sleep(PAUSA)

    if not args.probe and filas:
        nuevo = not LOG.exists()
        with open(LOG, "a", encoding="utf-8", newline="") as fh:
            w = csv.DictWriter(fh, fieldnames=["id", "estado", "pmcid", "url", "revista"])
            if nuevo:
                w.writeheader()
            w.writerows(filas)

    print("estudios mirados        : %d" % len(fuentes))
    print("  ya estaban            : %d" % ya)
    print("  %-20s: %d" % ("descargables" if args.probe else "descargados", bajados))
    print("  sin PDF abierto       : %d" % cerrados)
    print("  sin identificador     : %d" % sin)
    if not args.probe:
        print("\nPDFs en %s: %d" % (DEST, len(list(DEST.glob('*.pdf')))))
        print("registro en %s" % LOG)


if __name__ == "__main__":
    main()
