"""Construye el conjunto de extracción definitivo: un valor por casilla.

DE DÓNDE SALE CADA VALOR

Hasta ahora había tres ficheros y ninguno era «la extracción»: el cuaderno de
D. Valdiviezo, el de N. Trelles, y la lista de desacuerdos con sus resoluciones.
Este script los funde en uno, con una regla explícita por caso:

  los dos coinciden        -> ese valor
  discrepan y hay consenso -> el valor que firmaron los dos revisores
  discrepan y NO hay consenso -> vacío, y la casilla queda marcada ABIERTA
  solo uno rellenó         -> ese valor, marcado SIN SEGUNDA LECTURA
  ninguno rellenó          -> vacío

Las dos últimas reglas importan tanto como las otras. Una casilla que solo
leyó un revisor no es equivalente a una que leyeron los dos y en la que
coincidieron, y el fichero lo dice en vez de igualarlas: cada casilla lleva su
procedencia en una columna paralela. Quien reporte una cifra desde aquí puede
--y debe-- decir cuántas de las casillas que la componen tuvieron doble lectura.

QUÉ NO HACE

No decide nada que los revisores no hayan decidido. Las 14 casillas sin
consenso salen vacías, no rellenas con la respuesta más frecuente ni con la del
revisor más completo. Y no evalúa riesgo de sesgo: eso exige leer los artículos
y es un juicio humano que este canal no puede emitir.

Salida:
    revision_sistematica/extraccion/extraccion_adjudicada.csv
    revision_sistematica/extraccion/extraccion_adjudicada_procedencia.csv
    quality_reports/extraccion_adjudicada.json

Uso:
    python scripts/build_adjudicated_dataset.py
"""
import collections
import csv
import json
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from extraction_schema import CATEGORICOS, normaliza  # noqa: E402

ROOT = pathlib.Path(__file__).resolve().parent.parent
EXTR = ROOT / "revision_sistematica" / "extraccion"
A = EXTR / "extraccion_danny_valdiviezo.xlsx"
B = EXTR / "extraccion_nataly_trelles.xlsx"
CONFLICTOS = EXTR / "extraction_conflicts.csv"
SALIDA = EXTR / "extraccion_adjudicada.csv"
PROCEDENCIA = EXTR / "extraccion_adjudicada_procedencia.csv"
RESUMEN = ROOT / "quality_reports" / "extraccion_adjudicada.json"

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass


# El emparejamiento lo hace compare_extractions con su propia clave (la columna
# «N.o», que trae los EST-nnn y nadie edita). Se importa en vez de reescribirlo:
# dos lectores distintos del mismo cuaderno acabarian discrepando, y el fichero
# de conflictos esta escrito con las claves de ese, no de este.
from compare_extractions import cargar as lee_cuaderno  # noqa: E402


def lee(ruta):
    """{(EST-nnn, brazo): {campo: valor}}, con las casillas vacias fuera."""
    import warnings
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        crudo = lee_cuaderno(ruta)
    return {k: {c: str(v).strip() for c, v in d.items()
                if v is not None and str(v).strip()}
            for k, d in crudo.items()}


def main():
    if not (A.exists() and B.exists()):
        print("faltan los cuadernos de extracción")
        return 1
    a, b = lee(A), lee(B)

    # Las resoluciones firmadas. Las cerradas por regla sin firma conjunta NO
    # cuentan: su valor no lo acordó nadie, asi que su casilla queda abierta.
    SIN_FIRMA = "SIN firma conjunta"
    consenso, abiertos = {}, set()
    for r in csv.DictReader(open(CONFLICTOS, encoding="utf-8")):
        clave = (r["study_id"], r["arm_id"], r["campo"])
        val = (r.get("resolucion") or "").strip()
        if val and SIN_FIRMA not in (r.get("resuelto_por") or ""):
            consenso[clave] = val
        else:
            abiertos.add(clave)

    # study_id y arm_id son la clave, no un campo extraido: si entran en la
    # lista, el bucle pisa las columnas de identificador del fichero de
    # procedencia con la palabra «acuerdo» y las filas dejan de poder
    # localizarse.
    CLAVE = {"study_id", "arm_id", "id_provisional"}
    campos = sorted({c for d in list(a.values()) + list(b.values())
                     for c in d if c not in CLAVE})
    claves = sorted(set(a) | set(b))

    filas, procs = [], []
    cuenta = collections.Counter()
    por_campo = collections.defaultdict(collections.Counter)
    for k in claves:
        da, db = a.get(k, {}), b.get(k, {})
        fila = {"study_id": k[0], "arm_id": k[1]}
        proc = {"study_id": k[0], "arm_id": k[1]}
        for campo in campos:
            va, vb = da.get(campo), db.get(campo)
            ck = (k[0], k[1], campo)
            if va and vb:
                # Se compara con el MISMO normalizador que uso el comparador:
                # «other (intravesical)» y «other», o «fago solo» y «phage
                # monotherapy», son la misma respuesta. Comparar en crudo
                # inventaba 64 desacuerdos que nadie tuvo, y habria dejado
                # vacias 64 casillas que si tienen dato.
                na, nb = normaliza(campo, va), normaliza(campo, vb)
                if na == nb:
                    valor, origen = (na if na is not None else va), "acuerdo"
                elif ck in consenso:
                    valor, origen = consenso[ck], "consenso"
                else:
                    valor, origen = "", "ABIERTO"
            elif va or vb:
                valor, origen = (va or vb), "sin segunda lectura"
            else:
                valor, origen = "", "vacio"
            fila[campo], proc[campo] = valor, origen
            cuenta[origen] += 1
            por_campo[campo][origen] += 1
        filas.append(fila)
        procs.append(proc)

    cab = ["study_id", "arm_id"] + campos
    for ruta, datos in ((SALIDA, filas), (PROCEDENCIA, procs)):
        with open(ruta, "w", encoding="utf-8", newline="") as fh:
            w = csv.DictWriter(fh, fieldnames=cab)
            w.writeheader()
            w.writerows(datos)

    # Cuando los dos revisores coinciden en un valor que NO esta en el
    # vocabulario, coinciden en algo que el esquema no admite y el valor sale
    # tal cual. No se corrige aqui --nadie lo ha acordado-- pero se informa:
    # una casilla fuera de vocabulario en el conjunto definitivo es un dato que
    # no se puede agregar, y callarlo lo haria parecer agregable.
    fuera = collections.defaultdict(collections.Counter)
    for f in filas:
        for campo, ops in CATEGORICOS.items():
            v = (f.get(campo) or "").strip()
            if v and v not in ops:
                fuera[campo][v] += 1
    if fuera:
        print()
        print("  FUERA DEL VOCABULARIO (los dos coincidieron en un valor que el")
        print("  esquema no admite; no se corrige, se informa):")
        for campo, c in sorted(fuera.items()):
            for v, n in c.most_common():
                print("    %-24s %-24r %3d" % (campo, v, n))

    total = sum(cuenta.values())
    llenas = total - cuenta["vacio"]
    doble = cuenta["acuerdo"] + cuenta["consenso"]
    S = {
        "filas": len(filas),
        "estudios": len({k[0] for k in claves}),
        "campos": len(campos),
        "casillas_totales": total,
        "casillas_con_dato": llenas,
        "por_acuerdo": cuenta["acuerdo"],
        "por_consenso": cuenta["consenso"],
        "sin_segunda_lectura": cuenta["sin segunda lectura"],
        "abiertas": cuenta["ABIERTO"],
        "doble_lectura": doble,
        "doble_lectura_pct": round(100.0 * doble / max(1, llenas), 1),
        "fuera_de_vocabulario": sum(sum(c.values()) for c in fuera.values()),
    }
    RESUMEN.write_text(json.dumps(S, indent=2, ensure_ascii=False), encoding="utf-8")

    print("escrito %s" % SALIDA.name)
    print("  %d filas de brazo sobre %d estudios, %d campos"
          % (S["filas"], S["estudios"], S["campos"]))
    print()
    print("  procedencia de las %s casillas con dato:" % f"{llenas:,}".replace(",", " "))
    print("    los dos coincidieron        %5d" % S["por_acuerdo"])
    print("    resuelto por consenso       %5d" % S["por_consenso"])
    print("    solo lo leyó un revisor     %5d" % S["sin_segunda_lectura"])
    print("    abiertas (salen vacías)     %5d" % S["abiertas"])
    print("    -> con doble lectura        %5d  (%.1f %%)"
          % (doble, S["doble_lectura_pct"]))
    print()
    print("  por campo, las que menos doble lectura tienen:")
    orden = sorted(campos, key=lambda c: (por_campo[c]["acuerdo"] + por_campo[c]["consenso"]))
    for campo in orden[:8]:
        c = por_campo[campo]
        con = c["acuerdo"] + c["consenso"]
        print("    %-30s doble %3d | solo uno %3d | abiertas %2d"
              % (campo, con, c["sin segunda lectura"], c["ABIERTO"]))
    return 0


if __name__ == "__main__":
    sys.exit(main())
