"""Compara dos extracciones independientes: concordancia y lista de conflictos.

QUÉ CONVIERTE ESTO. "Revisor único" es una limitación que un referee marca de
inmediato. "Doble extracción independiente con resolución de conflictos
documentada" es una frase de Métodos. La diferencia entre las dos no es el
esfuerzo: es tener por escrito quién discrepó en qué y cómo se resolvió.

QUÉ MIDE, Y QUÉ NO
  categóricos  kappa de Cohen + % de acuerdo, sobre el valor NORMALIZADO
  numéricos    % de acuerdo exacto + diferencia absoluta media
  texto libre  no se puntúa: dos redacciones distintas pueden decir lo mismo.
               Se listan para revisión visual, sin fingir una cifra.

DOS TRAMPAS QUE ESTE SCRIPT NO PISA
  1. Kappa no está definida cuando no hay variación: si ambos revisores usaron
     una sola categoría, la kappa sale 0/0. Se informa "no calculable (sin
     variación)" en vez de un 0 que parecería desacuerdo total, o un NaN que
     alguien copiaría a la tabla.
  2. Una fila que solo existe en una de las dos extracciones NO es un desacuerdo
     de valor: es un desacuerdo de cobertura (un revisor vio un brazo que el
     otro no separó). Se cuenta aparte, porque mezclarlo hundiría la kappa
     atribuyendo a discrepancia lo que es una diferencia de granularidad.

USO
    python scripts/compare_extractions.py --a revision_sistematica/extraccion/extraccion_r1.xlsx \\
                                          --b revision_sistematica/extraccion/extraccion_r2.xlsx
    python scripts/compare_extractions.py --a corpus --b revision_sistematica/extraccion/extraccion_r2.xlsx
"""
import argparse
import collections
import csv
import datetime
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from extraction_schema import (CAMPO_DE_ETIQUETA, CATEGORICOS, NUMERICOS,
                               TEXTO, normaliza)

ROOT = pathlib.Path(__file__).resolve().parent.parent
CORPUS = ROOT / "metaanalisis" / "datos" / "phage_therapy_extraction_dataset.csv"
INFORME = ROOT / "quality_reports" / "extraction_agreement.md"
CONFLICTOS = ROOT / "revision_sistematica" / "extraccion" / "extraction_conflicts.csv"

csv.field_size_limit(200_000_000)
try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass


def cargar(ruta):
    """Devuelve {(study_id, arm_id): fila}. Acepta el corpus o un formulario."""
    if ruta == "corpus":
        with open(CORPUS, encoding="utf-8", newline="") as fh:
            return {(r["study_id"].strip(), r["arm_id"].strip().rsplit("_", 1)[-1]): r
                    for r in csv.DictReader(fh)}
    import openpyxl
    wb = openpyxl.load_workbook(ruta, data_only=True)
    ws = wb["Extraccion"] if "Extraccion" in wb.sheetnames else wb.active
    # El formulario viene con encabezados en español ("Vía de administración");
    # el dataset y este comparador trabajan con el nombre canónico. Se traduce
    # al leer, así que un formulario en español y uno en inglés se comparan sin
    # problema -- lo que importa es que ambos acaben en la misma clave.
    cab = [CAMPO_DE_ETIQUETA.get((c.value or "").strip(), (c.value or "").strip())
           for c in ws[1]]
    out = {}
    for fila in ws.iter_rows(min_row=2, values_only=True):
        d = {cab[i]: ("" if v is None else str(v)) for i, v in enumerate(fila) if i < len(cab)}
        # Se empareja por id_provisional, que ambos formularios comparten y
        # nadie edita. Emparejar por study_id fallaría en cuanto un revisor
        # escribiera "Liu 2025" y el otro "Liu2025_perinephric": saldrían como
        # filas exclusivas de cada uno y la kappa se calcularía sobre nada.
        sid = (d.get("Nº") or d.get("id_provisional")
               or d.get("study_id") or "").strip()
        if not sid:
            continue
        out[(sid, (d.get("arm_id") or "A").strip())] = d
    return out


def kappa(pares):
    """Kappa de Cohen. Devuelve (valor|None, motivo si es None)."""
    n = len(pares)
    if n == 0:
        return None, "sin filas comparables"
    cats = sorted({x for p in pares for x in p})
    if len(cats) < 2:
        return None, "no calculable (sin variación: una sola categoría)"
    po = sum(1 for a, b in pares if a == b) / n
    ca = collections.Counter(a for a, _ in pares)
    cb = collections.Counter(b for _, b in pares)
    pe = sum((ca[c] / n) * (cb[c] / n) for c in cats)
    if abs(1 - pe) < 1e-12:
        return None, "no calculable (acuerdo esperado = 1)"
    return (po - pe) / (1 - pe), None


def etiqueta(k):
    if k is None:
        return "—"
    for lim, txt in ((0.81, "casi perfecta"), (0.61, "sustancial"), (0.41, "moderada"),
                     (0.21, "aceptable"), (0.0, "leve")):
        if k >= lim:
            return txt
    return "pobre"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--a", required=True, help="ruta del formulario, o 'corpus'")
    ap.add_argument("--b", required=True)
    ap.add_argument("--nombre-a", default="revisor A")
    ap.add_argument("--nombre-b", default="revisor B")
    args = ap.parse_args()

    A, B = cargar(args.a), cargar(args.b)
    comunes = sorted(set(A) & set(B))
    solo_a, solo_b = sorted(set(A) - set(B)), sorted(set(B) - set(A))

    filas_conf, resumen = [], []
    for campo in list(CATEGORICOS) + NUMERICOS:
        pares, difs = [], []
        for k in comunes:
            va, vb = normaliza(campo, A[k].get(campo)), normaliza(campo, B[k].get(campo))
            if va is None and vb is None:
                continue
            pares.append((va or "(vacío)", vb or "(vacío)"))
            if va != vb:
                filas_conf.append({
                    "study_id": k[0], "arm_id": k[1], "campo": campo,
                    "valor_%s" % args.nombre_a.replace(" ", "_"): (A[k].get(campo) or "").strip(),
                    "valor_%s" % args.nombre_b.replace(" ", "_"): (B[k].get(campo) or "").strip(),
                    "tipo": "categórico" if campo in CATEGORICOS else "numérico",
                    "resolucion": "", "resuelto_por": "", "fecha": "",
                })
            if campo in NUMERICOS and va not in (None, "NA") and vb not in (None, "NA"):
                try:
                    difs.append(abs(float(va) - float(vb)))
                except ValueError:
                    pass
        n = len(pares)
        ac = sum(1 for a, b in pares if a == b)
        if campo in CATEGORICOS:
            k_, motivo = kappa(pares)
            resumen.append((campo, "categórico", n, ac,
                            "%.0f%%" % (100 * ac / n) if n else "—",
                            "%.2f (%s)" % (k_, etiqueta(k_)) if k_ is not None else motivo))
        else:
            md = "%.2f" % (sum(difs) / len(difs)) if difs else "—"
            resumen.append((campo, "numérico", n, ac,
                            "%.0f%%" % (100 * ac / n) if n else "—",
                            "dif. media %s" % md))

    for campo in TEXTO:
        for k in comunes:
            va, vb = normaliza(campo, A[k].get(campo)), normaliza(campo, B[k].get(campo))
            if va != vb and (va or vb):
                filas_conf.append({
                    "study_id": k[0], "arm_id": k[1], "campo": campo,
                    "valor_%s" % args.nombre_a.replace(" ", "_"): (A[k].get(campo) or "").strip()[:300],
                    "valor_%s" % args.nombre_b.replace(" ", "_"): (B[k].get(campo) or "").strip()[:300],
                    "tipo": "texto (no puntuado)", "resolucion": "", "resuelto_por": "", "fecha": "",
                })

    if filas_conf:
        with open(CONFLICTOS, "w", encoding="utf-8", newline="") as fh:
            w = csv.DictWriter(fh, fieldnames=list(filas_conf[0].keys()))
            w.writeheader()
            w.writerows(filas_conf)

    puntuables = [r for r in resumen if r[2] > 0]
    kappas = [float(r[5].split()[0]) for r in resumen
              if r[1] == "categórico" and r[5][0].isdigit()]
    lin = ["# Concordancia entre extracciones independientes", "",
           "Generado el %s por `scripts/compare_extractions.py`." % datetime.date.today().isoformat(),
           "", "| | |", "|---|---:|",
           "| %s | %d filas |" % (args.nombre_a, len(A)),
           "| %s | %d filas |" % (args.nombre_b, len(B)),
           "| Filas comparadas (brazos en ambos) | %d |" % len(comunes),
           "| Solo en %s | %d |" % (args.nombre_a, len(solo_a)),
           "| Solo en %s | %d |" % (args.nombre_b, len(solo_b)),
           "| Conflictos de valor | %d |" % len(filas_conf), ""]
    if kappas:
        lin += ["Kappa mediana de los campos categóricos calculables: **%.2f**." %
                sorted(kappas)[len(kappas) // 2], ""]
    lin += ["## Por variable", "",
            "| variable | tipo | n | acuerdos | % acuerdo | kappa / dispersión |",
            "|---|---|---:|---:|---:|---|"]
    for c, t, n, ac, pc, extra in resumen:
        lin.append("| `%s` | %s | %d | %d | %s | %s |" % (c, t, n, ac, pc, extra))

    if solo_a or solo_b:
        lin += ["", "## Diferencias de cobertura, no de valor", "",
                "Filas presentes en una sola extracción. No entran en la kappa: casi siempre",
                "significan que un revisor separó brazos que el otro agrupó, no que discrepen",
                "sobre un dato.", ""]
        for k in solo_a[:25]:
            lin.append("- solo en %s: `%s` brazo %s" % (args.nombre_a, k[0], k[1]))
        for k in solo_b[:25]:
            lin.append("- solo en %s: `%s` brazo %s" % (args.nombre_b, k[0], k[1]))

    lin += ["", "## Qué hacer ahora", "",
            "1. Abrir `revision_sistematica/extraccion/extraction_conflicts.csv` y resolver fila a fila.",
            "2. Rellenar `resolucion`, `resuelto_por` y `fecha`: el rastro de la resolución",
            "   es lo que permite escribir en Métodos que los desacuerdos se resolvieron por",
            "   consenso, y con qué frecuencia hizo falta.",
            "3. Volcar los valores acordados al dataset de extracción y volver a ejecutar",
            "   este script para dejar constancia de la concordancia previa a la resolución.", ""]
    INFORME.write_text("\n".join(lin), encoding="utf-8")

    print("filas comparadas: %d | conflictos: %d | solo en A: %d | solo en B: %d"
          % (len(comunes), len(filas_conf), len(solo_a), len(solo_b)))
    if kappas:
        print("kappa mediana (categóricos calculables): %.2f" % sorted(kappas)[len(kappas) // 2])
    print("escrito %s" % INFORME)
    if filas_conf:
        print("escrito %s" % CONFLICTOS)


if __name__ == "__main__":
    main()
