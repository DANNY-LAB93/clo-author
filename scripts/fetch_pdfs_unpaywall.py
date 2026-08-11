"""Segunda pasada: busca copia legal en abierto de lo que Europe PMC no trajo.

POR QUÉ HACEN FALTA DOS PASADAS. Europe PMC solo conoce lo depositado en PMC.
Unpaywall rastrea además los repositorios institucionales, los servidores de
preprints y las páginas del propio editorial cuando la revista es abierta: para
este corpus eso incluye MDPI (Viruses, Antibiotics), Frontiers, Nature
Communications y Scientific Reports, que son abiertas de origen y no aparecen
necesariamente en PMC.

LÍMITE QUE NO SE CRUZA. Unpaywall devuelve únicamente ubicaciones legales -- es
su razón de ser. Lo que siga sin aparecer está de pago de verdad, y para eso la
respuesta es el acceso institucional de la universidad o el préstamo
interbibliotecario, no un rodeo técnico.

USO
    python scripts/fetch_pdfs_unpaywall.py
"""
import csv
import urllib.parse
import json
import pathlib
import sys
import time
import urllib.request

ROOT = pathlib.Path(__file__).resolve().parent.parent
GRUPOS = ROOT / "revision_sistematica" / "cribado" / "study_groups.csv"
POOL = ROOT / "revision_sistematica" / "cribado" / "screening_stage2_priorizado.csv"
DEST = ROOT / "revision_sistematica" / "textos_completos" / "pdf"
LOG = ROOT / "revision_sistematica" / "textos_completos" / "fulltext_download_log.csv"

EMAIL = "dvchiqui@gmail.com"     # la API lo exige como identificación del uso
UA = "revision-sistematica-fagoterapia/1.0 (Universidad Catolica de Cuenca)"
PAUSA = 0.8

csv.field_size_limit(200_000_000)
try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass


def pedir(url, binario=False, timeout=60):
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return r.read() if binario else json.loads(r.read().decode("utf-8"))


def main():
    with open(POOL, encoding="utf-8", newline="") as fh:
        pool = {p["record_id"]: p for p in csv.DictReader(fh)}
    with open(GRUPOS, encoding="utf-8", newline="") as fh:
        fuentes = sorted([g for g in csv.DictReader(fh)
                          if g["informe_para_extraer"] == "SI"
                          and g["situacion"] in ("extraible", "solo-resumen")],
                         key=lambda g: int(g["estudio"]))

    DEST.mkdir(parents=True, exist_ok=True)
    ya = {p.stem for p in DEST.glob("*.pdf")}
    filas, nuevos, sin_doi, cerrado = [], 0, 0, 0

    for g in fuentes:
        eid = "EST-%03d" % int(g["estudio"])
        if eid in ya:
            continue
        rec = pool[g["record_id"]]
        doi = (rec["doi"] or "").strip()
        if not doi or doi.lower().startswith("10.1002/central/"):
            sin_doi += 1
            continue
        try:
            d = pedir("https://api.unpaywall.org/v2/%s?email=%s"
                      % (urllib.parse.quote(doi), EMAIL))
        except Exception:
            time.sleep(PAUSA)
            continue
        time.sleep(PAUSA)
        loc = d.get("best_oa_location") or {}
        pdf = loc.get("url_for_pdf") or loc.get("url")
        if not d.get("is_oa") or not pdf:
            cerrado += 1
            filas.append({"id": eid, "estado": "sin copia legal en abierto (Unpaywall)",
                          "pmcid": "", "url": "", "revista": rec["journal"][:60]})
            continue
        try:
            datos = pedir(pdf, binario=True, timeout=90)
            if len(datos) < 20000 or not datos[:5].startswith(b"%PDF"):
                raise ValueError("no es un PDF (%d bytes)" % len(datos))
            (DEST / ("%s.pdf" % eid)).write_bytes(datos)
            nuevos += 1
            filas.append({"id": eid, "estado": "descargado (Unpaywall)", "pmcid": "",
                          "url": pdf, "revista": rec["journal"][:60]})
        except Exception as e:
            cerrado += 1
            filas.append({"id": eid, "estado": "abierto pero fallo la descarga: %s" % str(e)[:50],
                          "pmcid": "", "url": pdf, "revista": rec["journal"][:60]})
        time.sleep(PAUSA)

    if filas:
        nuevo = not LOG.exists()
        with open(LOG, "a", encoding="utf-8", newline="") as fh:
            w = csv.DictWriter(fh, fieldnames=["id", "estado", "pmcid", "url", "revista"])
            if nuevo:
                w.writeheader()
            w.writerows(filas)

    print("segunda pasada (Unpaywall)")
    print("  nuevos descargados : %d" % nuevos)
    print("  sin copia abierta  : %d" % cerrado)
    print("  sin DOI utilizable : %d" % sin_doi)
    print("  PDFs totales       : %d de %d" % (len(list(DEST.glob("*.pdf"))), len(fuentes)))


if __name__ == "__main__":
    main()
