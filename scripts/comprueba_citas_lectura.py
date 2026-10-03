# -*- coding: utf-8 -*-
"""¿Esta cada frase entrecomillada del cuaderno firmado en su PDF, y en su pagina?

QUE ES Y QUE NO ES

Es una comprobacion MECANICA de cadenas: busca cada «cita» del cuaderno
`lectura_firmada_2026-09-30.xlsx` dentro del texto del PDF del estudio al que
se atribuye, y mira si esta en la pagina que dice el «(p. N)». No es una
revision: no juzga si la cita respalda la conclusion, ni lee las figuras. Lo
que lleva la marca «[imagen]» se transcribio de una figura o una tabla en
imagen y no se puede comprobar asi; se cuenta aparte.

Normaliza antes de comparar (minusculas, sin espacios ni signos, ligaduras
deshechas), porque la extraccion de texto de un PDF pega palabras, parte
columnas y cambia guiones. Si la cita no aparece entera, prueba con sus dos
mitades: una frase partida por una columna sale como «partida», no como
ausente. Lo que sigue sin aparecer se lista para mirarlo a mano.

Salida:
    quality_reports/lectura_citas_comprobadas.csv

Uso:
    python scripts/comprueba_citas_lectura.py
"""
import collections
import csv
import pathlib
import re
import sys
import unicodedata

import openpyxl

try:
    import pymupdf
except ImportError:                      # versiones antiguas
    import fitz as pymupdf

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

ROOT = pathlib.Path(__file__).resolve().parent.parent
RS = ROOT / "revision_sistematica"
PDF = RS / "textos_completos" / "pdf"
FIRMADO = RS / "lectura_pendiente" / "lectura_firmada_2026-09-30.xlsx"
SALIDA = ROOT / "quality_reports" / "lectura_citas_comprobadas.csv"

# La hoja, la columna donde van las citas y de que estudio son.
COLUMNAS = {
    "2 resistencia": ["criterio_o_antibiograma_en_que_te_apoyas"],
    "7 comparativos": ["brazo_control_identificado", "tipo_y_unidad_de_asignacion",
                       "tiempo_cero", "tiempo_de_evaluacion_del_desenlace",
                       "cointervenciones_y_antibiotico_concomitante",
                       "perdidas_y_datos_faltantes", "estimando_reportado",
                       "hay_contraste_extraible"],
    "15 solapamiento": ["frase_en_que_te_apoyas"],
}

LIGADURAS = {"ﬀ": "ff", "ﬁ": "fi", "ﬂ": "fl", "ﬃ": "ffi",
             "ﬄ": "ffl", "ß": "ss"}


def plano(t):
    """Solo letras y cifras, en minuscula y sin tildes."""
    for a, b in LIGADURAS.items():
        t = t.replace(a, b)
    t = unicodedata.normalize("NFKD", t)
    t = "".join(c for c in t if not unicodedata.combining(c))
    return re.sub(r"[^0-9a-z]", "", t.lower())


_paginas = {}


def paginas(est):
    """El texto plano de cada pagina del PDF, empezando en 1."""
    if est not in _paginas:
        p = PDF / ("%s.pdf" % est)
        if not p.exists():
            _paginas[est] = None
        else:
            with pymupdf.open(p) as doc:
                _paginas[est] = [plano(pg.get_text()) for pg in doc]
    return _paginas[est]


def donde(cita, pags):
    """Las paginas donde esta la cita entera; si no, las de sus dos mitades."""
    c = plano(cita)
    # Las celdas de un antibiograma son cortas («CIP R (2) R (2)»): por debajo de
    # cinco caracteres ya no distinguen nada.
    if len(c) < 5:
        return "demasiado corta", []
    enteras = [i + 1 for i, t in enumerate(pags) if c in t]
    if enteras:
        return "entera", enteras
    # A caballo entre dos paginas.
    for i in range(len(pags) - 1):
        if c in pags[i][-len(c) - 5:] + pags[i + 1][:len(c) + 5]:
            return "entera", [i + 1, i + 2]
    # Partida por una columna, una nota o un pie de figura.
    m = len(c) // 2
    a, b = c[:m], c[m:]
    pa = [i + 1 for i, t in enumerate(pags) if a in t]
    pb = [i + 1 for i, t in enumerate(pags) if b in t]
    if pa and pb:
        return "partida", sorted(set(pa) | set(pb))
    # Lo mas largo que si aparece, para decir cuanto falta.
    for frac in (0.75, 0.6, 0.5, 0.4):
        n = int(len(c) * frac)
        for ini in range(0, len(c) - n + 1, max(1, n // 4)):
            trozo = c[ini:ini + n]
            hay = [i + 1 for i, t in enumerate(pags) if trozo in t]
            if hay:
                return "parcial %d %%" % int(frac * 100), hay
    return "no aparece", []


CITA = re.compile(r"(?:(EST-\d{3}):\s*)?«(.+?)»\s*(?:\(p\.\s*([\d–\-–, ]+)\))?", re.S)


def citas_de(celda, est_por_defecto):
    """(estudio, cita, pagina declarada) de cada «...» de la celda."""
    out = []
    for parte in re.split(r"\s\|\s", celda or ""):
        if parte.strip().startswith("[imagen]"):
            out.append((est_por_defecto, None, None, parte.strip()))
            continue
        # «EST-xxx: «...»» en la hoja de solapamiento: el estudio va delante.
        est = est_por_defecto
        m0 = re.match(r"\s*(EST-\d{3}):", parte)
        if m0:
            est = m0.group(1)
        for m in CITA.finditer(parte):
            out.append((m.group(1) or est, m.group(2), m.group(3), None))
    return out


def main():
    wb = openpyxl.load_workbook(FIRMADO, read_only=True)
    filas = []
    for hoja, cols in COLUMNAS.items():
        ws = wb[hoja]
        it = ws.iter_rows(values_only=True)
        cab = list(next(it))
        for row in it:
            d = dict(zip(cab, row))
            if hoja == "15 solapamiento":
                if not d.get("estudio_1"):
                    continue
                fila_id = "%s + %s" % (d["estudio_1"], d["estudio_2"])
                defecto = d["estudio_1"]
            else:
                if not d.get("study_id"):
                    continue
                fila_id = defecto = d["study_id"]
            for col in cols:
                for est, cita, pag, imagen in citas_de(d.get(col), defecto):
                    if imagen:
                        filas.append(dict(hoja=hoja, fila=fila_id, columna=col,
                                          estudio=est, pagina_declarada="",
                                          resultado="imagen: no comprobable como texto",
                                          paginas_halladas="", en_la_pagina_declarada="",
                                          cita=imagen[:400]))
                        continue
                    pags = paginas(est)
                    if pags is None:
                        res, hall = "sin PDF", []
                    else:
                        res, hall = donde(cita, pags)
                    dec = []
                    for x in re.findall(r"\d+", pag or ""):
                        dec.append(int(x))
                    en = ""
                    if dec and hall:
                        en = "si" if set(dec) & set(hall) else "no"
                    filas.append(dict(hoja=hoja, fila=fila_id, columna=col, estudio=est,
                                      pagina_declarada=pag or "", resultado=res,
                                      paginas_halladas=",".join(map(str, hall)),
                                      en_la_pagina_declarada=en, cita=cita[:400]))

    with open(SALIDA, "w", encoding="utf-8-sig", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(filas[0].keys()))
        w.writeheader()
        w.writerows(filas)

    print("citas en el cuaderno firmado: %d" % len(filas))
    por = collections.Counter((f["hoja"], f["resultado"].split(" ")[0]) for f in filas)
    for hoja in COLUMNAS:
        print("  %-16s %s" % (hoja, ", ".join("%s %d" % (r, n) for (h, r), n
                                              in sorted(por.items()) if h == hoja)))
    pag_mal = [f for f in filas if f["en_la_pagina_declarada"] == "no"]
    print("en otra pagina que la declarada: %d" % len(pag_mal))
    print("estudios cuyo PDF se abrio: %d" % sum(1 for v in _paginas.values() if v))
    print()
    raras = [f for f in filas if f["resultado"] not in ("entera", "partida")
             and not f["resultado"].startswith("imagen")]
    if raras:
        print("PARA MIRAR A MANO (%d):" % len(raras))
        for f in raras:
            print("  %-16s %-18s %-8s %-12s «%s»" % (f["hoja"], f["fila"], f["estudio"],
                                                    f["resultado"], f["cita"][:110]))
    print()
    print("escrito %s" % SALIDA.relative_to(ROOT))


if __name__ == "__main__":
    main()
