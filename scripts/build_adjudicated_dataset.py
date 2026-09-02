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

No decide nada que los revisores no hayan decidido. Las casillas sin consenso
salen vacías --el script dice cuántas al terminar-- y no se rellenan con la
respuesta más frecuente ni con la del revisor más completo. Y no evalúa riesgo de sesgo: eso exige leer los artículos
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
from extraction_schema import CAMPOS, CATEGORICOS, normaliza  # noqa: E402

ROOT = pathlib.Path(__file__).resolve().parent.parent
EXTR = ROOT / "revision_sistematica" / "extraccion"
A = EXTR / "extraccion_danny_valdiviezo.xlsx"
B = EXTR / "extraccion_nataly_trelles.xlsx"
CONFLICTOS = EXTR / "extraction_conflicts.csv"
# Correcciones posteriores a la adjudicacion. Son casillas YA CERRADAS --por
# acuerdo de los dos o por consenso firmado-- que el texto completo contradice
# literalmente. No se editan en el CSV de salida, que es un derivado: se
# declaran aqui, con la cita que las sostiene y la firma de quien las asume, y
# el constructor las aplica en la ultima capa. Asi los cuadernos siguen
# diciendo lo que los revisores escribieron, y la columna de procedencia
# distingue una correccion de un acuerdo. Ver
# quality_reports/decisions/2026-09-01_revision-uno-por-uno-de-los-textos-completos.md
CORRECCIONES = EXTR / "correcciones_tras_texto_completo.csv"
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

    # Solo las variables del esquema. El formulario trae ademas ocho columnas
    # de navegacion ya rellenas --Nº, Pos., titulo, revista, año, tipo, como
    # encontrarlo, abrir articulo-- que nadie extrae: estan para que el revisor
    # localice el articulo. Tratarlas como datos extraidos inflaba el recuento
    # de casillas y el porcentaje de doble lectura, y producia una casilla
    # «abierta» de mas que el fichero de conflictos no tiene.
    #
    # study_id y arm_id son la clave, no un campo: si entran en la lista, el
    # bucle pisa las columnas de identificador del fichero de procedencia.
    # Las correcciones firmadas. Una fila sin firmante NO se aplica: la firma
    # es lo que convierte una lectura en una decision, igual que en
    # ingest_adjudications.py.
    correcciones, sin_firma = {}, 0
    if CORRECCIONES.exists():
        for r in csv.DictReader(open(CORRECCIONES, encoding="utf-8")):
            if not (r.get("firmado_por") or "").strip():
                sin_firma += 1
                continue
            correcciones[(r["study_id"], r["arm_id"], r["campo"])] = \
                (r.get("valor_corregido") or "").strip()
    if sin_firma:
        print(f"  aviso: {sin_firma} correcciones sin firmar, NO aplicadas")

    CLAVE = {"study_id", "arm_id", "id_provisional"}
    campos = sorted({c for d in list(a.values()) + list(b.values())
                     for c in d if c in CAMPOS and c not in CLAVE})
    mobiliario = sorted({c for d in list(a.values()) + list(b.values())
                         for c in d if c not in CAMPOS and c not in CLAVE})
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
                    # Se NORMALIZA PARA COMPARAR y se GUARDA lo que se debe
                    # guardar, que no es lo mismo. En un categórico el valor
                    # canónico es el dato: «fago solo» y «phage monotherapy»
                    # tienen que salir iguales o la columna no se puede
                    # agrupar. En texto libre y en números, normalizar
                    # DESTRUYE: «Bélgica» salía como «belgica» en el fichero
                    # que se entrega, y son 392 celdas.
                    valor = na if campo in CATEGORICOS else va
                    origen = "acuerdo"
                elif ck in consenso:
                    valor, origen = consenso[ck], "consenso"
                else:
                    valor, origen = "", "ABIERTO"
            elif va or vb:
                # Tambien se normaliza. Si no, la misma respuesta sale en
                # ingles cuando la leyeron dos y en castellano cuando la leyo
                # uno, y la columna deja de poder agruparse.
                crudo = va or vb
                nn = normaliza(campo, crudo)
                valor = nn if (campo in CATEGORICOS and nn is not None) else crudo
                origen = "sin segunda lectura"
            else:
                valor, origen = "", "vacio"
            # Ultima capa: una correccion firmada pisa lo que hubiera. Se
            # etiqueta aparte y NO cuenta como doble lectura, porque no lo es:
            # la firma la pone un revisor, no los dos.
            if ck in correcciones:
                valor = correcciones[ck]
                origen = "corregido contra el texto (una firma)"
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
    proc_por_clave = {(r["study_id"], r["arm_id"]): r for r in procs}
    for f in filas:
        pr = proc_por_clave[(f["study_id"], f["arm_id"])]
        for campo, ops in CATEGORICOS.items():
            v = (f.get(campo) or "").strip()
            # El aviso dice «los dos coincidieron», asi que solo puede contar
            # celdas que leyeron los dos. Una que leyo uno solo es otra cosa y
            # se informa aparte.
            if v and v not in ops and pr.get(campo) in ("acuerdo", "consenso"):
                fuera[campo][v] += 1
    if fuera:
        print()
        print("  FUERA DEL VOCABULARIO (los dos coincidieron en un valor que el")
        print("  esquema no admite; no se corrige, se informa):")
        for campo, c in sorted(fuera.items()):
            for v, n in c.most_common():
                print("    %-24s %-24r %3d" % (campo, v, n))

    total = sum(cuenta.values())
    # Una casilla ABIERTA sale vacia del CSV igual que una «vacio»: contarla
    # como rellena inflaba el denominador del porcentaje de doble lectura.
    llenas = total - cuenta["vacio"] - cuenta["ABIERTO"]
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
        "columnas_de_navegacion_descartadas": len(mobiliario),
    }
    RESUMEN.write_text(json.dumps(S, indent=2, ensure_ascii=False), encoding="utf-8")

    print("escrito %s" % SALIDA.name)
    print("  %d filas de brazo sobre %d estudios, %d campos del esquema"
          % (S["filas"], S["estudios"], S["campos"]))
    if mobiliario:
        print("  %d columnas de navegación descartadas (no son datos extraídos): %s"
              % (len(mobiliario), ", ".join(mobiliario)))
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
