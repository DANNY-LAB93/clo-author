"""¿El PDF guardado como EST-nnn.pdf es de verdad el artículo EST-nnn?

POR QUÉ HACE FALTA

El canal daba por recuperado un texto completo con mirar si existía el fichero.
EST-207 tenía un PDF de 4 000 caracteres que resultó ser el final de un
artículo japonés de insuficiencia cardíaca --recuperado por número de página,
597, que casualmente es también la página del artículo correcto--, y aun así
S5 lo declaraba `texto_completo: sí` y entró en el recuento de 93/124.

Un fichero con el nombre correcto no es el artículo correcto. Esto lo comprueba
cotejando el título que S5 declara contra el texto del PDF.

CÓMO COTEJA, Y POR QUÉ NO DE LA MANERA OBVIA

La primera versión buscaba el arranque del título como una cadena seguida
dentro del PDF comprimido. Marcó cuatro y **los cuatro eran falsos**: en un
artículo a dos columnas la extracción entrelaza los bloques, y el título sale
partido --«Development of Host Immune | Observations suggest... | Response to
Bacteriophage»--. EST-105 es peor todavía: es una página de *Research letters*
donde conviven dos cartas y el texto de ambas se mezcla.

Un cotejo que se equivoca en el 100 % de lo que marca no sirve. Así que no se
compara el título como cadena, sino **cuántas de sus palabras distintivas
aparecen** en el texto. El orden deja de importar, y entrelazar columnas deja
de romperlo. Se busca cada palabra dentro del texto comprimido, para que
«Successfulbacteriophagetreatment» siga contando.

Salida:
    revision_sistematica/verificacion_texto_completo/pdf_vs_titulo.csv

Uso:
    python scripts/verificar_pdf_corresponde.py
"""
import csv
import pathlib
import re
import sys
import unicodedata

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

ROOT = pathlib.Path(__file__).resolve().parent.parent
CACHE = ROOT / "revision_sistematica" / "textos_completos" / "texto_cache"
S5 = ROOT / "verificables revisión sistemática" / "S5_listado_184_estudios.csv"
OUT = ROOT / "revision_sistematica" / "verificacion_texto_completo" / "pdf_vs_titulo.csv"

# Palabras de menos de 5 letras no distinguen nada: «the», «for», «due», «with».
MINIMO_PALABRA = 5
# Umbrales. Por debajo de la mitad de las palabras del título, el PDF es
# sospechoso; entre la mitad y el 80 %, hay que mirarlo a mano.
BIEN, DUDA = 0.80, 0.50


def comprime(s):
    s = unicodedata.normalize("NFD", (s or "").lower())
    s = "".join(c for c in s if unicodedata.category(c) != "Mn")
    return re.sub(r"[^a-z0-9]", "", s)


def distintivas(titulo):
    s = unicodedata.normalize("NFD", (titulo or "").lower())
    s = "".join(c for c in s if unicodedata.category(c) != "Mn")
    return [w for w in re.findall(r"[a-z0-9]+", s) if len(w) >= MINIMO_PALABRA]


def main():
    titulos = {r["id"]: r.get("titulo", "")
               for r in csv.DictReader(open(S5, encoding="utf-8-sig"))}
    filas = []
    for p in sorted(CACHE.glob("EST-*.txt")):
        est = p.stem
        tit = titulos.get(est, "")
        pal = distintivas(tit)
        cp = comprime(p.read_text(encoding="utf-8"))
        if not pal:
            estado, frac, faltan = "sin título en S5", "", ""
        else:
            hay = [w for w in pal if w in cp]
            f = len(hay) / len(pal)
            frac = f"{len(hay)}/{len(pal)}"
            faltan = " ".join(w for w in pal if w not in cp)[:80]
            estado = ("coincide" if f >= BIEN
                      else "revisar" if f >= DUDA else "NO COINCIDE")
        filas.append({"study_id": est, "estado": estado,
                      "palabras_del_titulo_halladas": frac,
                      "no_halladas": faltan,
                      "caracteres_pdf": len(cp),
                      "titulo_S5": tit[:120]})

    OUT.parent.mkdir(exist_ok=True)
    with open(OUT, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, list(filas[0].keys()))
        w.writeheader()
        w.writerows(filas)

    from collections import Counter
    c = Counter(x["estado"] for x in filas)
    print(f"{len(filas)} PDF cotejados contra el título que declara S5\n")
    for k, v in c.most_common():
        print(f"  {v:4d}  {k}")
    malos = [x for x in filas if x["estado"] not in ("coincide",)]
    if malos:
        print(f"\nRevisar a mano ({len(malos)}):")
        for x in malos:
            print(f"  {x['study_id']}  {x['estado']:22s} {x['caracteres_pdf']:7d} car."
                  f"  {x['titulo_S5'][:70]}")


if __name__ == "__main__":
    main()
