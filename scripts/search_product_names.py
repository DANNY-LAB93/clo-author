"""Search PubMed for phage PRODUCT and PROGRAMME names, and diff against the corpus.

WHY. Case reports of phage therapy routinely name the preparation rather than the
technique. The executed equations carry only `pyophage`, `intestiphage` and
`phage cocktail`, and the corpus contains direct proof that this is not enough:
the OMKO1 case (Chan 2018, MDR P. aeruginosa aortic Dacron graft infection) is an
INCLUDED study that no executed query ever retrieved -- it entered through a
manual landmark screen at peer review. A search that misses a canonical case of
its own corpus has a systematic gap, not bad luck.

This runs the product-name block as its own arm and reports which PMIDs are new
relative to revision_sistematica/busqueda/screening_pubmed_union.csv, so the marginal contribution is
measured rather than assumed.

USAGE
    python scripts/search_product_names.py
    python scripts/search_product_names.py --window "2016"[dp]:"2026"[dp]
"""
import argparse
import csv
import json
import pathlib
import time
import urllib.parse
import urllib.request

ROOT = pathlib.Path(__file__).resolve().parent.parent
CORPUS = ROOT / "revision_sistematica" / "busqueda" / "screening_pubmed_union.csv"
OUT = ROOT / "quality_reports" / "product_name_search.md"
EUTILS = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/"

csv.field_size_limit(10_000_000)

# Named preparations, programmes and trial names. Grouped so the report can say
# which family produced which record.
PRODUCTS = {
    # LPS-5 QUEDA FUERA a proposito. PubMed rompe el guion y empareja "LPS" con
    # "5", de modo que '"LPS-5"[tiab]' devuelve la literatura de lipopolisacarido
    # -- 885 registros, entre ellos "acute lung injury via TLR4" y estudios de
    # polifenoles. Incluirlo anadia 396 falsos nuevos, cuatro veces el rendimiento
    # real de todo el bloque. Cualquier codigo corto con guion corre el mismo
    # riesgo y debe comprobarse antes de anadirlo.
    "cocteles nominados": [
        "OMKO1", "AB-PA01", "AP-PA02", "BFC-1", "BFC1", "PP1131",
        "BX004", "TP-102", "TP-122", "PASA16", "phiYY",
    ],
    "preparados comerciales georgianos/rusos": [
        "Pyophage", "Intestiphage", "Fersisi", "PYO bacteriophage",
        "Sextaphage", "Piobacteriophage", "polyvalent pyobacteriophage",
    ],
    "programas y ensayos": [
        "PhagoBurn", "PhagoDAIR", "Phage4Cure", "CYPHY", "SWARM-Pa",
        "PHAGEinLYON", "Eliava",
    ],
    "descriptores de practica": [
        "personalised bacteriophage", "personalized bacteriophage",
        "phage-antibiotic synergy", "magistral phage", "phage steering",
    ],
}


def eutils(endpoint, params, retries=4):
    params.setdefault("tool", "clo-author-sr")
    params.setdefault("email", "dvchiqui@gmail.com")
    params.setdefault("retmode", "json")
    url = EUTILS + endpoint + "?" + urllib.parse.urlencode(params)
    for attempt in range(retries):
        try:
            with urllib.request.urlopen(url, timeout=120) as r:
                return json.loads(r.read())
        except Exception:
            if attempt == retries - 1:
                raise
            time.sleep(3 * (attempt + 1))


def search(term, window):
    """One product name, title/abstract only, inside the review window."""
    q = '("%s"[tiab]) AND %s' % (term, window)
    d = eutils("esearch.fcgi", {"db": "pubmed", "term": q, "retmax": 500})
    res = d.get("esearchresult", {})
    return set(res.get("idlist", [])), int(res.get("count", 0))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--window", default='("2016"[dp] : "2026"[dp])')
    args = ap.parse_args()

    with open(CORPUS, encoding="utf-8", newline="") as fh:
        have = {r["pmid"] for r in csv.DictReader(fh)}
    print("corpus actual: %d PMID\n" % len(have))

    rows, all_new = [], {}
    for family, terms in PRODUCTS.items():
        for term in terms:
            ids, count = search(term, args.window)
            new = ids - have
            rows.append((family, term, count, len(new)))
            for p in new:
                all_new.setdefault(p, []).append(term)
            print("  %-32s %4d hits  %3d nuevos" % (term, count, len(new)))
            time.sleep(0.4)                    # NCBI: <=3 peticiones/segundo

    print("\nPMID nuevos, unicos: %d" % len(all_new))

    L = ["# Búsqueda por nombre de producto — contribución marginal", "",
         "Generado por `scripts/search_product_names.py`.", "",
         "**Por qué existe.** Los reportes de caso nombran el preparado, no la",
         "técnica. La prueba está dentro del propio corpus: el caso **OMKO1**",
         "(Chan 2018) es un estudio **incluido** que ninguna consulta ejecutada",
         "recuperó; entró por un cribado manual de casos emblemáticos en la revisión",
         "por pares.", "",
         "Cada término se busca en `[tiab]` dentro de la ventana %s." % args.window,
         "«Nuevos» significa PMID ausentes del corpus de %d registros." % len(have),
         "", "| Familia | Término | Registros | Nuevos |", "|---|---|---|---|"]
    for fam, term, count, n_new in rows:
        mark = " **%d**" % n_new if n_new else " 0"
        L.append("| %s | `%s` | %d |%s |" % (fam, term, count, mark))

    L += ["", "**PMID nuevos únicos: %d**" % len(all_new), ""]
    if all_new:
        L += ["| PMID | Recuperado por | PubMed |", "|---|---|---|"]
        for p, terms in sorted(all_new.items()):
            L.append("| %s | %s | https://pubmed.ncbi.nlm.nih.gov/%s/ |"
                     % (p, ", ".join(sorted(set(terms))), p))
        L += ["", "Estos registros entran al cribado por la vía normal; ninguno se",
              "incluye por haber sido recuperado así."]
    else:
        L.append("Ningún registro nuevo: el bloque de nombres de producto queda")
        L.append("subsumido por las ecuaciones ya ejecutadas.")

    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text("\n".join(L) + "\n", encoding="utf-8", newline="\n")
    print("wrote", OUT)


if __name__ == "__main__":
    main()
