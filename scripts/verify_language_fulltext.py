"""Verifica el idioma sobre el TEXTO COMPLETO de cada PDF recuperado.

POR QUE HACE FALTA. El titulo y el resumen indexados pueden estar en ingles
mientras el articulo esta en otra lengua: es exactamente lo que hacen las
revistas rusas bilingues y lo que PubMed produce al traducir titulos. Si el
criterio de elegibilidad dice "informes en ingles o espanol", la prueba tiene
que hacerse sobre el texto que el revisor va a leer y del que va a extraer, no
sobre los metadatos.

QUE MIDE. Sobre las paginas centrales del PDF, no la primera: la portada suele
llevar cabecera de revista, filiaciones y palabras clave en ingles aunque el
cuerpo este en otro idioma, y analizarla sola daria ingles siempre.

QUE HACE CON EL RESULTADO. No decide por su cuenta. Contrasta con la
determinacion previa y REPORTA las discrepancias, que es donde esta el valor:
un PDF que resulta estar en ruso cuando los metadatos decian ingles es un
hallazgo, y silenciarlo seria peor que no comprobar nada.

USO
    python scripts/verify_language_fulltext.py            # todos los PDFs
    python scripts/verify_language_fulltext.py --limite 20  # por tandas

SALIDA
    revision_sistematica/cribado/idioma_texto_completo.csv
"""
import argparse
import collections
import csv
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
RS = ROOT / "revision_sistematica"
CRIB = RS / "cribado"
PDFS = RS / "textos_completos" / "pdf"
OUT = CRIB / "idioma_texto_completo.csv"
csv.field_size_limit(200_000_000)
try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

sys.path.insert(0, str(ROOT / "scripts"))
from verify_language_eligibility import identifica, ADMITIDOS  # noqa: E402


def leer(p):
    with open(p, encoding="utf-8", newline="") as fh:
        return list(csv.DictReader(fh))


def texto_del_pdf(ruta, max_paginas=8):
    """Texto de las paginas centrales, saltando portada y bibliografia.

    La portada de un articulo lleva titulo, filiaciones y palabras clave que
    muchas revistas publican en ingles aunque el cuerpo no lo este. Empezar por
    ella daria ingles en practicamente todo. Se toma desde la segunda pagina y
    se dejan fuera las ultimas, que suelen ser referencias.
    """
    from pypdf import PdfReader
    lector = PdfReader(str(ruta))
    n = len(lector.pages)
    if n == 0:
        return "", 0
    inicio = 1 if n >= 3 else 0
    fin = max(inicio + 1, n - 1 if n >= 4 else n)
    trozos = []
    for i in range(inicio, min(fin, inicio + max_paginas)):
        try:
            trozos.append(lector.pages[i].extract_text() or "")
        except Exception:
            pass
    return "\n".join(trozos), n


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--limite", type=int, default=0,
                    help="verificar solo los N primeros aun sin verificar")
    args = ap.parse_args()

    grupos = leer(CRIB / "study_groups.csv")
    reps = {"EST-%03d" % int(g["estudio"]): g for g in grupos
            if g["informe_para_extraer"] == "SI"}
    previo = {r["id"]: r for r in leer(OUT)} if OUT.exists() else {}
    verif = {r["record_id"]: r for r in
             leer(CRIB / "idioma_verificacion.csv")} \
        if (CRIB / "idioma_verificacion.csv").exists() else {}

    pendientes = sorted(p for p in PDFS.glob("*.pdf")
                        if p.stem not in previo)
    if args.limite:
        pendientes = pendientes[:args.limite]

    filas = list(previo.values())
    nuevos = 0
    for ruta in pendientes:
        eid = ruta.stem
        g = reps.get(eid, {})
        try:
            texto, n_pag = texto_del_pdf(ruta)
        except Exception as e:
            filas.append({"id": eid, "paginas": 0, "palabras": 0,
                          "idioma_texto_completo": "(ilegible)",
                          "confianza": "error", "evidencia": type(e).__name__,
                          "idioma_previo": verif.get(g.get("record_id", ""), {})
                          .get("idioma_del_texto", ""),
                          "coincide": "", "revista": g.get("revista", ""),
                          "titulo": " ".join((g.get("titulo") or "").split())[:90]})
            nuevos += 1
            continue
        det, conf, ev = identifica(texto)
        prev = verif.get(g.get("record_id", ""), {}).get("idioma_del_texto", "")
        filas.append({
            "id": eid, "paginas": n_pag,
            "palabras": len(re.findall(r"[A-Za-z]+", texto)),
            "idioma_texto_completo": det or "(indeterminado)",
            "confianza": conf, "evidencia": ev[:110],
            "idioma_previo": prev or "(sin dato)",
            "coincide": "si" if (det and prev and det == prev) else
                        ("" if not prev else "NO"),
            "revista": g.get("revista", ""),
            "titulo": " ".join((g.get("titulo") or "").split())[:90],
        })
        nuevos += 1

    filas.sort(key=lambda f: f["id"])
    with open(OUT, "w", encoding="utf-8", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(filas[0].keys()))
        w.writeheader()
        w.writerows(filas)

    total = len(list(PDFS.glob("*.pdf")))
    print("PDFs verificados : %d de %d  (nuevos en esta tanda: %d)"
          % (len(filas), total, nuevos))
    print("\nidioma del texto completo:")
    for k, v in collections.Counter(f["idioma_texto_completo"]
                                    for f in filas).most_common():
        marca = "" if k in ADMITIDOS else "   <-- revisar"
        print("   %-18s %3d%s" % (k, v, marca))

    problemas = [f for f in filas
                 if f["idioma_texto_completo"] not in ADMITIDOS
                 and f["confianza"] == "probado"]
    discrepan = [f for f in filas if f["coincide"] == "NO"]
    if problemas:
        print("\nTEXTO COMPLETO EN LENGUA NO ADMITIDA (%d):" % len(problemas))
        for f in problemas:
            print("   %s [%s] %-32s %s" % (f["id"], f["idioma_texto_completo"],
                                           f["revista"][:32], f["titulo"][:52]))
    if discrepan:
        print("\nDISCREPAN metadatos y texto completo (%d):" % len(discrepan))
        for f in discrepan:
            print("   %s  metadatos=%-6s texto completo=%-6s  %s"
                  % (f["id"], f["idioma_previo"], f["idioma_texto_completo"],
                     f["titulo"][:48]))
    ilegibles = [f for f in filas if f["confianza"] in ("error", "insuficiente")]
    if ilegibles:
        print("\nsin texto extraible o insuficiente (%d): %s"
              % (len(ilegibles), " ".join(f["id"] for f in ilegibles[:20])))
    print("\nescrito %s" % OUT)
    print("PENDIENTES: %d" % (total - len(filas)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
