"""Busca por vias legitimas el texto completo de los estudios que faltan.

QUE APRENDIO ESTE BUSCADOR DE LOS INTENTOS ANTERIORES. Tres cosas, y las tres
costaron un articulo dado por perdido:

  1. `best_oa_location` no basta. PhagoBurn figuraba como abierto y sin PDF
     porque su unica ubicacion es una pagina de repositorio, no un fichero. Hay
     que recorrer TODAS las ubicaciones y, cuando apuntan a una pagina,
     resolverla: los repositorios declaran el fichero en `citation_pdf_url`.
  2. El texto completo no siempre es un PDF. El manuscrito de autor de
     PhagoBurn esta depositado en .docx. Rechazar todo lo que no empiece por
     %PDF- lo descartaba.
  3. El DOI del corpus suele ser el sustituto de Cochrane CENTRAL
     (10.1002/central/...), que no sirve para consultar a nadie. El DOI
     editorial se resuelve antes por PMID.

VIAS, EN ORDEN. Europe PMC -> Unpaywall (todas las ubicaciones) -> OpenAIRE ->
CORE -> Semantic Scholar -> resultados publicados en el registro del ensayo.
Ninguna redistribuye sin permiso del titular.

USO
    python scripts/hunt_fulltext_openly.py --limite 12
"""
import argparse
import collections
import csv
import json
import pathlib
import re
import sys
import time
import urllib.parse
import urllib.request

ROOT = pathlib.Path(__file__).resolve().parent.parent
RS = ROOT / "revision_sistematica"
CRIB = RS / "cribado"
DEST = RS / "textos_completos" / "pdf"
REG = RS / "textos_completos" / "busqueda_abierta.csv"
CACHE = RS / "textos_completos" / ".busqueda_abierta.json"
csv.field_size_limit(200_000_000)
try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

CORREO = "dvchiqui@gmail.com"
UA = {"User-Agent": "Mozilla/5.0 (compatible; SystematicReview/1.0; +mailto:%s)"
      % CORREO, "Accept": "*/*"}
FIRMAS = {b"%PDF-": ".pdf", b"PK\x03\x04": ".docx"}


def leer(p):
    with open(p, encoding="utf-8", newline="") as fh:
        return list(csv.DictReader(fh))


def trae(url, timeout=60):
    req = urllib.request.Request(url, headers=UA)
    with urllib.request.urlopen(req, timeout=timeout) as fh:
        return fh.read(), fh.headers.get("Content-Type", "")


def jason(url, timeout=45):
    datos, _ = trae(url, timeout)
    return json.loads(datos)


def guarda(datos, eid):
    """Guarda el fichero con la extension que corresponda a su contenido."""
    for firma, ext in FIRMAS.items():
        if datos.startswith(firma):
            d = DEST / ("%s%s" % (eid, ext))
            d.write_bytes(datos)
            return d, "%.0f KB" % (len(datos) / 1024.0)
    return None, "no es un documento (%d bytes, %r)" % (len(datos), datos[:8])


def fichero_de_pagina(url):
    """Un repositorio publica el fichero en la etiqueta citation_pdf_url."""
    try:
        datos, tipo = trae(url, 45)
    except Exception:
        return ""
    if not tipo.startswith("text/"):
        return url
    html = datos.decode("utf-8", "replace")
    m = re.search(r'<meta[^>]+name="citation_pdf_url"[^>]+content="([^"]+)"',
                  html, re.I)
    if m:
        return m.group(1)
    m = re.search(r'href="(/bitstream[^"]+)"', html, re.I)
    if m:
        base = "%s://%s" % urllib.parse.urlparse(url)[:2]
        return urllib.parse.urljoin(url, m.group(1))
    return ""


def intenta(url, eid):
    try:
        datos, _ = trae(url, 90)
    except Exception as e:
        return None, "fallo: %s" % type(e).__name__
    if not any(datos.startswith(f) for f in FIRMAS):
        otra = fichero_de_pagina(url)
        if otra and otra != url:
            try:
                datos, _ = trae(otra, 90)
            except Exception as e:
                return None, "pagina resuelta pero fallo: %s" % type(e).__name__
    return guarda(datos, eid)


def doi_editorial(p, cache, eid):
    """El DOI del corpus puede ser el sustituto de CENTRAL; se busca el real."""
    d = (p.get("doi") or "").strip()
    if d and not d.lower().startswith("10.1002/central/"):
        return d
    pmid = (p.get("pmid") or "").strip()
    if not pmid:
        return ""
    clave = "doi:%s" % pmid
    if clave in cache:
        return cache[clave]
    try:
        r = jason("https://www.ebi.ac.uk/europepmc/webservices/rest/search?"
                  "query=EXT_ID:%s&resultType=core&format=json&pageSize=1" % pmid)
        res = r["resultList"]["result"]
        cache[clave] = (res[0].get("doi") or "") if res else ""
    except Exception:
        cache[clave] = ""
    return cache[clave]


def busca(eid, p, cache):
    vias = []
    pmid = (p.get("pmid") or "").strip()
    nct = (p.get("nct") or "").strip()

    # 1. Europe PMC: deposito en PMC
    if pmid:
        try:
            r = jason("https://www.ebi.ac.uk/europepmc/webservices/rest/search?"
                      "query=EXT_ID:%s&resultType=core&format=json&pageSize=1"
                      % pmid)["resultList"]["result"]
            art = r[0] if r else None
            if art and (art.get("inPMC") == "Y" or art.get("inEPMC") == "Y") \
                    and art.get("pmcid"):
                d, det = intenta("https://www.ebi.ac.uk/europepmc/webservices/"
                                 "rest/%s/fullTextPdf" % art["pmcid"], eid)
                vias.append(("Europe PMC", "OBTENIDO" if d else "sin fichero", det))
                if d:
                    return vias, "Europe PMC (deposito en PMC)"
        except Exception as e:
            vias.append(("Europe PMC", "error", type(e).__name__))

    # 2. Unpaywall: TODAS las ubicaciones, no solo la mejor
    doi = doi_editorial(p, cache, eid)
    if doi:
        try:
            u = jason("https://api.unpaywall.org/v2/%s?email=%s"
                      % (urllib.parse.quote(doi), CORREO))
            locs = u.get("oa_locations") or []
            vias.append(("Unpaywall", "%s (%s)" % (u.get("oa_status"),
                                                   len(locs)), doi))
            for l in locs:
                for campo in ("url_for_pdf", "url"):
                    if not l.get(campo):
                        continue
                    d, det = intenta(l[campo], eid)
                    if d:
                        vias.append(("Unpaywall/%s" % (l.get("host_type") or "?"),
                                     "OBTENIDO", det))
                        return vias, "Unpaywall: %s, %s, %s" % (
                            l.get("host_type"), l.get("version"),
                            l.get("license") or "sin licencia")
        except Exception as e:
            vias.append(("Unpaywall", "error", type(e).__name__))

    # 3. OpenAIRE: deposito por mandato del financiador
    if doi:
        try:
            r = jason("https://api.openaire.eu/search/publications?doi=%s"
                      "&format=json" % urllib.parse.quote(doi))
            blob = json.dumps(r)
            enlaces = [x for x in set(re.findall(r'https?://[^"\\ ]+', blob))
                       if re.search(r"(bitstream|/download|\.pdf)", x, re.I)]
            for x in enlaces[:4]:
                d, det = intenta(x, eid)
                if d:
                    vias.append(("OpenAIRE", "OBTENIDO", det))
                    return vias, "OpenAIRE: repositorio institucional"
            if enlaces:
                vias.append(("OpenAIRE", "%d enlace(s) sin exito" % len(enlaces), ""))
        except Exception as e:
            vias.append(("OpenAIRE", "error", type(e).__name__))

    # 4. Semantic Scholar
    if doi:
        try:
            r = jason("https://api.semanticscholar.org/graph/v1/paper/DOI:%s"
                      "?fields=isOpenAccess,openAccessPdf"
                      % urllib.parse.quote(doi))
            oa = r.get("openAccessPdf") or {}
            if oa.get("url"):
                d, det = intenta(oa["url"], eid)
                if d:
                    vias.append(("Semantic Scholar", "OBTENIDO", det))
                    return vias, "Semantic Scholar: %s" % oa.get("status", "")
        except Exception as e:
            vias.append(("Semantic Scholar", "error", type(e).__name__))

    # 5. Resultados publicados en el registro
    if nct:
        try:
            r = jason("https://clinicaltrials.gov/api/v2/studies/%s"
                      "?fields=protocolSection,hasResults,resultsSection" % nct)
            if r.get("hasResults"):
                carpeta = DEST.parent / "resultados_registro"
                carpeta.mkdir(exist_ok=True)
                (carpeta / ("%s_%s.json" % (eid, nct))).write_text(
                    json.dumps(r, indent=1, ensure_ascii=False), encoding="utf-8")
                vias.append(("Registro %s" % nct, "RESULTADOS", "guardados"))
                return vias, "resultados publicados en el registro %s" % nct
            vias.append(("Registro %s" % nct, "sin resultados", ""))
        except Exception as e:
            vias.append(("Registro %s" % nct, "error", type(e).__name__))

    return vias, ""


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--limite", type=int, default=12)
    args = ap.parse_args()
    DEST.mkdir(parents=True, exist_ok=True)
    cache = json.loads(CACHE.read_text(encoding="utf-8")) if CACHE.exists() else {}

    grupos = leer(CRIB / "study_groups.csv")
    pool = {p["record_id"]: p for p in
            leer(CRIB / "screening_stage2_priorizado.csv")}
    reps = {"EST-%03d" % int(g["estudio"]): g for g in grupos
            if g["informe_para_extraer"] == "SI"}
    extr = {k for k, g in reps.items()
            if g["situacion"] in ("extraible", "solo-resumen")}
    tengo = {q.stem for q in DEST.iterdir()
             if q.suffix.lower() in (".pdf", ".docx")}
    previo = {r["id"]: r for r in leer(REG)} if REG.exists() else {}
    faltan = sorted(k for k in extr - tengo if k not in previo)[:args.limite]

    filas = list(previo.values())
    for eid in faltan:
        p = pool[reps[eid]["record_id"]]
        vias, exito = busca(eid, p, cache)
        estado = "OBTENIDO" if exito else "sin via abierta"
        print("  %s %-16s %s" % (eid, estado, (exito or "; ".join(
            "%s=%s" % (a, b) for a, b, _ in vias[-2:]))[:78]))
        filas.append({"id": eid, "estado": estado, "via": exito,
                      "intentos": " | ".join("%s:%s" % (a, b) for a, b, _ in vias),
                      "revista": reps[eid]["revista"][:60],
                      "titulo": " ".join(reps[eid]["titulo"].split())[:80]})
        time.sleep(0.3)

    CACHE.write_text(json.dumps(cache, ensure_ascii=False), encoding="utf-8")
    if filas:
        with open(REG, "w", encoding="utf-8", newline="") as fh:
            w = csv.DictWriter(fh, fieldnames=["id", "estado", "via",
                                               "intentos", "revista", "titulo"])
            w.writeheader()
            w.writerows(filas)
    tengo = {q.stem for q in DEST.iterdir()
             if q.suffix.lower() in (".pdf", ".docx")}
    print("\ntextos completos: %d de %d extraibles" % (len(extr & tengo), len(extr)))
    vistos = {f["id"] for f in filas}
    print("examinados en total: %d | pendientes: %d"
          % (len(filas), len(extr - tengo - vistos)))
    obt = collections.Counter(f["estado"] for f in filas)
    print("resultado acumulado:", dict(obt))
    return 0


if __name__ == "__main__":
    sys.exit(main())
