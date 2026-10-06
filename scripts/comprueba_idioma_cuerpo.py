# -*- coding: utf-8 -*-
"""El idioma del CUERPO de cada PDF del corpus vigente, sin navegador ni metadatos.

El corpus solo admite estudios redactados en ingles o en espanol. El
2026-10-06 se comprobo que 18 de los 65 PDF del corpus nunca habian pasado por
la comprobacion del cuerpo (`verify_language_fulltext.py` corrio antes de que
se consiguieran). Este guion la rehace sobre todos, cada vez.

Como: palabras vacias de ingles, espanol, portugues, frances, aleman, italiano,
polaco y danes sobre el texto del PDF, y la fraccion de cirilico y de CJK. Es
una deteccion mecanica: un PDF con mas de un 5 % de cirilico o de CJK se marca
para mirarlo pagina a pagina (EST-075 lo tiene: su pagina 1 es el resumen ruso
que exige la revista; el cuerpo, paginas 2 a 5, esta en ingles).

Salida:
    quality_reports/idioma_cuerpo_pdf.csv

Uso:
    python scripts/comprueba_idioma_cuerpo.py
"""
import collections
import csv
import pathlib
import re
import sys
import unicodedata

try:
    import pymupdf
except ImportError:
    import fitz as pymupdf

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

ROOT = pathlib.Path(__file__).resolve().parent.parent
RS = ROOT / "revision_sistematica"
SALIDA = ROOT / "quality_reports" / "idioma_cuerpo_pdf.csv"

VACIAS = {
    "eng": "the of and in to was with for is were that by on as from at this".split(),
    "spa": "de la el en y los las del se con por una para que fue es".split(),
    "por": "de da do em e os as dos das com uma para que foi não".split(),
    "fra": "de la le et les des du en une est dans pour que avec par".split(),
    "deu": "der die und das den mit von ist im des nicht eine wurde".split(),
    "ita": "di il la e che del della per con una sono nel gli".split(),
    "pol": "i w z na się do nie jest oraz że przez od".split(),
    "dan": "og i at det en er til med på af den for som".split(),
}


def leer(p):
    with open(p, encoding="utf-8-sig", newline="") as fh:
        return list(csv.DictReader(fh))


def main():
    fuera = {r["study_id"] for r in leer(RS / "cribado" / "exclusiones_tras_texto_completo.csv")}
    corpus = {"EST-%03d" % int(g["estudio"]) for g in leer(RS / "cribado" / "study_groups.csv")} - fuera
    filas = []
    for p in sorted((RS / "textos_completos" / "pdf").glob("EST-*.pdf")):
        if p.stem not in corpus:
            continue
        with pymupdf.open(p) as d:
            t = " ".join(pg.get_text() for pg in d)
        letras = [c for c in t if c.isalpha()]
        cir = sum(1 for c in letras if "CYRILLIC" in unicodedata.name(c, ""))
        cjk = sum(1 for c in letras if "CJK" in unicodedata.name(c, ""))
        pal = re.findall(r"[a-záéíóúñüàèìòùçãõąćęłńśźżäöåæø]+", t.lower())
        cuenta, n = collections.Counter(pal), max(1, len(pal))
        punt = {l: sum(cuenta[w] for w in ws) / n for l, ws in VACIAS.items()}
        mejor = max(punt, key=punt.get)
        fc, fk = cir / max(1, len(letras)), cjk / max(1, len(letras))
        filas.append({"study_id": p.stem, "idioma_del_cuerpo": mejor,
                      "frecuencia_palabras_vacias": round(punt[mejor], 3),
                      "segundo_idioma": round(sorted(punt.values())[-2], 3),
                      "fraccion_cirilico": round(fc, 3), "fraccion_cjk": round(fk, 3),
                      "palabras": len(pal),
                      "mirar_a_mano": "si" if (fc > 0.05 or fk > 0.05 or mejor not in ("eng", "spa"))
                      else ""})
    with open(SALIDA, "w", encoding="utf-8-sig", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(filas[0].keys()))
        w.writeheader()
        w.writerows(filas)
    c = collections.Counter(f["idioma_del_cuerpo"] for f in filas)
    print("PDF del corpus: %d; idioma del cuerpo: %s" % (len(filas), dict(c)))
    for f in filas:
        if f["mirar_a_mano"]:
            print("  mirar a mano: %s (%s, cirílico %.2f)" % (f["study_id"], f["idioma_del_cuerpo"],
                                                            f["fraccion_cirilico"]))
    fuera_de_criterio = [f["study_id"] for f in filas if f["idioma_del_cuerpo"] not in ("eng", "spa")]
    if fuera_de_criterio:
        print("ATENCIÓN: cuerpo en otro idioma: %s" % ", ".join(fuera_de_criterio))
    print("escrito %s" % SALIDA.relative_to(ROOT))


if __name__ == "__main__":
    main()
