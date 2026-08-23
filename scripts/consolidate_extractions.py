"""Consolida varios cuadernos de extracción de un mismo revisor en uno solo.

EL PROBLEMA QUE RESUELVE

Un revisor acaba con varias copias de su cuaderno: la que descargó, la que
reenvió, la que guardó con otro nombre. Algunas son el mismo fichero y otras son
pasadas distintas del mismo trabajo, y de fuera no se distinguen.

LO QUE HACE, Y LO QUE SE NIEGA A HACER

Une celda a celda. Donde solo un fichero tiene valor, lo toma. Donde dos tienen
el MISMO valor, lo toma. Donde dos tienen valores DISTINTOS **no elige**: deja la
celda con el valor del fichero más reciente y anota el conflicto en una hoja
aparte, con lo que dice cada fichero.

Elegir en silencio sería fabricar un consenso que no existe. Un cuaderno
consolidado que oculta que dos pasadas discrepaban en `dtr_status` o en
`microbio_eradication_n` es peor que tres cuadernos sueltos: parece resuelto.

Uso:
    python scripts/consolidate_extractions.py salida.xlsx entrada1.xlsx entrada2.xlsx ...

Los ficheros se ordenan por fecha de modificación; el más reciente gana los
conflictos, y todos quedan listados.
"""
import pathlib
import shutil
import sys
import warnings

warnings.filterwarnings("ignore")
import openpyxl  # noqa: E402

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from extraction_schema import CAMPO_DE_ETIQUETA, CAMPOS, CLAVE  # noqa: E402

CAMPOS_DATO = [c for c in CAMPOS if c not in CLAVE]

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass


def abre(ruta):
    wb = openpyxl.load_workbook(ruta)
    ws = wb["Extraccion"] if "Extraccion" in wb.sheetnames else wb.active
    hdr = [(c.value or "") for c in ws[1]]
    col_id = next(i for i, h in enumerate(hdr) if str(h).strip().startswith("N"))
    idx = {CAMPO_DE_ETIQUETA[str(h).strip()]: i
           for i, h in enumerate(hdr) if CAMPO_DE_ETIQUETA.get(str(h).strip())}
    return wb, ws, col_id, idx


def es_formula(v):
    """Una celda calculada por Excel, no tecleada por el revisor.

    `journal_tier` es un VLOOKUP contra la hoja de revistas. Su texto lleva la
    fila dentro (`VLOOKUP(D44,...)`), asi que dos copias del mismo cuaderno con
    filas insertadas discrepan en TODAS estas celdas sin que nadie haya
    extraido nada distinto. Y copiarla de un fichero a otro escribiria una
    referencia a la fila equivocada, que es peor que no copiar nada.
    """
    return isinstance(v, str) and v.startswith("=")


def celdas(ruta):
    """{(estudio, brazo, campo): valor} con las celdas que tienen dato."""
    _, ws, col_id, idx = abre(ruta)
    out = {}
    for fila in ws.iter_rows(min_row=2):
        v = [c.value for c in fila]
        if not v[col_id]:
            continue
        eid = str(v[col_id]).strip()
        arm = str(v[idx["arm_id"]] or "A").strip() if "arm_id" in idx else "A"
        for c in CAMPOS_DATO:
            if c in idx and v[idx[c]] not in (None, "")                     and not es_formula(v[idx[c]]):
                out[(eid, arm, c)] = str(v[idx[c]]).strip()
    return out


def main():
    if len(sys.argv) < 4:
        print(__doc__)
        return 2
    salida = pathlib.Path(sys.argv[1])
    entradas = [pathlib.Path(p) for p in sys.argv[2:]]
    faltan = [p for p in entradas if not p.exists()]
    if faltan:
        print("no existen: %s" % ", ".join(str(p) for p in faltan))
        return 1

    # el más reciente al final: gana los conflictos. Se desempata por nombre
    # para que el orden sea determinista: dos ficheros guardados en el mismo
    # minuto ordenados al azar hacen que los conflictos se cuenten dos veces y
    # que el valor ganador dependa del sistema de ficheros.
    entradas.sort(key=lambda p: (p.stat().st_mtime, p.name))
    datos = [(p, celdas(p)) for p in entradas]

    # Copias idénticas: un revisor acaba con el mismo cuaderno guardado con dos
    # nombres. Contarlas dos veces infla los conflictos y no aporta nada.
    unicos, descartados = [], []
    for p, d in datos:
        # Copia redundante: sus celdas caben dentro de otro fichero SIN ninguna
        # discrepancia. Un cuaderno reguardado con otro nombre suele diferir en
        # una celda suelta, así que exigir identidad exacta no lo detecta y los
        # conflictos se cuentan por partida doble.
        def redundante(e, d):
            return all(k in e and e[k] == v for k, v in d.items())
        gemelo = next((q for q, e in unicos if redundante(e, d)), None)
        if gemelo is None:
            for i, (q, e) in enumerate(unicos):
                if redundante(d, e):          # el nuevo contiene al anterior
                    descartados.append((q, p))
                    unicos[i] = (p, d)
                    gemelo = "reemplaza"
                    break
            if gemelo == "reemplaza":
                continue
        if gemelo is not None:
            descartados.append((p, gemelo))
        else:
            unicos.append((p, d))
    for p, d in unicos:
        print("  %-46s %4d celdas" % (p.name[:46], len(d)))
    for p, gemelo in descartados:
        print("  %-46s copia idéntica de %s, se omite"
              % (p.name[:46], gemelo.name[:30]))
    datos = unicos

    fusion, origen, conflictos = {}, {}, []
    for p, d in datos:
        for k, v in d.items():
            if k in fusion and fusion[k] != v:
                conflictos.append((k, origen[k], fusion[k], p.name, v))
            fusion[k] = v
            origen[k] = p.name

    # se escribe sobre una copia del fichero más completo, para conservar las
    # hojas de instrucciones, listas y diccionario que el formulario lleva
    base = max(datos, key=lambda x: len(x[1]))[0]
    shutil.copy2(base, salida)
    wb, ws, col_id, idx = abre(salida)

    escritas, calculadas = 0, []
    for fila in ws.iter_rows(min_row=2):
        v = [c.value for c in fila]
        if not v[col_id]:
            continue
        eid = str(v[col_id]).strip()
        arm = str(v[idx["arm_id"]] or "A").strip() if "arm_id" in idx else "A"
        for c in CAMPOS_DATO:
            if c not in idx:
                continue
            valor = fusion.get((eid, arm, c))
            if es_formula(fila[idx[c]].value):
                # La hoja la recalcula sola. Se anota igualmente: descartar un
                # valor en silencio es justo lo que no debe hacer un
                # consolidador, aunque el descarte sea el acierto.
                if fusion.get((eid, arm, c)) is not None:
                    calculadas.append((eid, c, fusion[(eid, arm, c)]))
                continue
            if valor is not None and str(fila[idx[c]].value or "").strip() != valor:
                fila[idx[c]].value = valor
                escritas += 1

    if "Conflictos" in wb.sheetnames:
        del wb["Conflictos"]
    hc = wb.create_sheet("Conflictos")
    hc.append(["Estudio", "Brazo", "Campo", "Fichero A", "Valor A",
               "Fichero B", "Valor B", "Cuál vale", "Quién lo resolvió"])
    for (eid, arm, c), fa, va, fb, vb in conflictos:
        hc.append([eid, arm, c, fa, va, fb, vb, "", ""])
    for i, ancho in enumerate([11, 7, 30, 32, 40, 32, 40, 22, 22], start=1):
        hc.column_dimensions[chr(64 + i)].width = ancho

    wb.save(salida)
    print()
    print("celdas únicas consolidadas : %d" % len(fusion))
    print("celdas reescritas en la hoja: %d" % escritas)
    print("CONFLICTOS a resolver       : %d  (hoja «Conflictos»)" % len(conflictos))
    if calculadas:
        campos = sorted({c for _, c, _ in calculadas})
        print("celdas NO copiadas por ser columna calculada: %d (%s)."
              % (len(calculadas), ", ".join(campos)))
        print("  La hoja las recalcula desde la de Revistas; copiarlas "
              "romperia el VLOOKUP.")
    print()
    print("escrito %s" % salida)
    print("En los conflictos se dejó el valor del fichero más reciente, pero NINGUNO")
    print("está resuelto: los revisores deben rellenar «Cuál vale» en esa hoja.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
