"""Baja de ClinicalTrials.gov la ficha completa de cada registro del corpus
cuyo titulo, resumen y MeSH no permiten saber el organismo.

Entrada : quality_reports/registros_sin_organismo.json
Salida  : revision_sistematica/textos_completos/registros/<NCT>.json  (ficha entera)
          quality_reports/registros_organismo_declarado.csv           (lo leible)

No decide nada: baja y extrae. La decision de si el estudio cumple el criterio
de organismo la firman los autores sobre lo que aqui queda escrito en disco.
"""
import csv
import json
import pathlib
import re
import time
import urllib.error
import urllib.request

RAIZ = pathlib.Path(__file__).resolve().parents[1]
ENTRADA = RAIZ / "quality_reports" / "registros_sin_organismo.json"
FICHAS = RAIZ / "revision_sistematica" / "textos_completos" / "registros"
SALIDA = RAIZ / "quality_reports" / "registros_organismo_declarado.csv"
API = "https://clinicaltrials.gov/api/v2/studies/%s?format=json"

# lo que buscamos en el texto entero de la ficha
PSEUDOMONAS = re.compile(r"pseudomonas|\bP\.\s*aeruginosa\b|aeruginosa", re.I)
OTROS = {
    "Staphylococcus aureus": r"staphylococc|S\.\s*aureus|\bMRSA\b",
    "Escherichia coli": r"escherichia|E\.\s*coli|\bETEC\b|\bEPEC\b|\bExPEC\b",
    "Klebsiella": r"klebsiella",
    "Acinetobacter": r"acinetobacter",
    "Enterococcus": r"enterococc|\bVRE\b",
    "Mycobacterium": r"mycobacter|\bNTM\b",
    "Streptococcus": r"streptococc",
    "Salmonella": r"salmonella",
    "Shigella": r"shigella",
    "Clostridioides": r"clostridi",
}


def baja(nct):
    ficha = FICHAS / ("%s.json" % nct)
    if ficha.exists():
        return json.loads(ficha.read_text(encoding="utf-8"))
    for intento in range(3):
        try:
            crudo = urllib.request.urlopen(API % nct, timeout=45).read()
            break
        except urllib.error.HTTPError as e:
            if e.code == 404:
                return None
            time.sleep(2 + intento * 3)
        except Exception:
            time.sleep(2 + intento * 3)
    else:
        raise SystemExit("no se pudo bajar %s" % nct)
    ficha.write_bytes(crudo)
    return json.loads(crudo)


def texto(nodo, acc):
    if isinstance(nodo, dict):
        for v in nodo.values():
            texto(v, acc)
    elif isinstance(nodo, list):
        for v in nodo:
            texto(v, acc)
    elif isinstance(nodo, str):
        acc.append(nodo)
    return acc


def campo(d, *ruta, defecto=""):
    for p in ruta:
        if not isinstance(d, dict):
            return defecto
        d = d.get(p, {})
    return d if d not in ({}, None) else defecto


def main():
    pendientes = json.loads(ENTRADA.read_text(encoding="utf-8"))
    filas = []
    for reg in pendientes:
        nct = reg["nct"]
        if not re.fullmatch(r"NCT\d{8}", nct):
            filas.append({
                "est": reg["est"], "nct": nct, "en_ctgov": "no es un NCT",
                "titulo_oficial": reg["titulo"], "condiciones": "", "intervenciones": "",
                "menciona_pseudomonas": "", "otros_organismos": "", "estado": "",
                "patrocinador": "", "pais": "",
            })
            continue
        d = baja(nct)
        if d is None:
            filas.append({
                "est": reg["est"], "nct": nct, "en_ctgov": "404 no existe",
                "titulo_oficial": reg["titulo"], "condiciones": "", "intervenciones": "",
                "menciona_pseudomonas": "", "otros_organismos": "", "estado": "",
                "patrocinador": "", "pais": "",
            })
            continue
        p = d.get("protocolSection", {})
        todo = " \n".join(texto(d, []))
        otros = sorted(n for n, pat in OTROS.items() if re.search(pat, todo, re.I))
        paises = sorted({
            loc.get("country", "")
            for loc in campo(p, "contactsLocationsModule", "locations", defecto=[]) or []
            if loc.get("country")
        })
        filas.append({
            "est": reg["est"],
            "nct": nct,
            "en_ctgov": "si",
            "titulo_oficial": campo(p, "identificationModule", "officialTitle")
                              or campo(p, "identificationModule", "briefTitle"),
            "condiciones": "; ".join(campo(p, "conditionsModule", "conditions", defecto=[]) or []),
            "intervenciones": "; ".join(
                i.get("name", "") for i in campo(p, "armsInterventionsModule", "interventions", defecto=[]) or []
            ),
            "menciona_pseudomonas": "si" if PSEUDOMONAS.search(todo) else "NO",
            "otros_organismos": "; ".join(otros),
            "estado": campo(p, "statusModule", "overallStatus"),
            "patrocinador": campo(p, "sponsorCollaboratorsModule", "leadSponsor", "name"),
            "pais": "; ".join(paises),
        })
        print("%s %s %s" % (reg["est"], nct, filas[-1]["menciona_pseudomonas"]))

    with SALIDA.open("w", newline="", encoding="utf-8-sig") as f:
        w = csv.DictWriter(f, fieldnames=list(filas[0].keys()))
        w.writeheader()
        w.writerows(filas)
    sin = [f for f in filas if f["menciona_pseudomonas"] == "NO"]
    print("\nfichas bajadas en %s" % FICHAS)
    print("%d de %d fichas no nombran Pseudomonas en ninguna parte" % (len(sin), len(filas)))


if __name__ == "__main__":
    main()
