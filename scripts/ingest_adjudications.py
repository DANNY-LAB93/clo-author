"""Vuelca en extraction_conflicts.csv lo que los dos revisores firmaron.

QUÉ ES ESTO Y QUÉ NO ES

`ADJUDICACION_conflictos.xlsx` es el cuaderno donde D. Valdiviezo y N. Trelles
resolvieron por consenso los desacuerdos entre sus dos extracciones. Cada fila
resuelta lleva el valor acordado, quién lo firmó y la fecha. Este script las
copia al fichero de conflictos, que es lo que lee el canal.

`merge_adjudications.py` NO sirve para esto: está escrito para el flujo anterior,
en el que un tercer lector proponía resoluciones en JSON y las volcaba en
`hoja_de_consenso.csv` sin firmarlas. Aquí las firmas ya existen.

LA PARTE DELICADA: NORMALIZAR SIN INVENTAR

Los revisores rellenaron el cuaderno en castellano y el esquema está en inglés,
así que hay que traducir. Traducir no es decidir: `Intravenosa` y `IV` son la
misma respuesta escrita en dos idiomas. Pero la frontera es fina, y este script
la trata como una frontera:

  · solo normaliza lo que está en la tabla EQUIVALENCIAS, entrada por entrada,
    cada una con su motivo escrito al lado;
  · cualquier otro valor que no esté en el vocabulario del esquema se RECHAZA y
    se informa, con su fila. No se aproxima al valor más parecido;
  · una fila sin firmante no se ingiere. La firma es lo que convierte una
    respuesta en un consenso, y sin ella el dato no es lo que declara ser.

EL CASO «no derivable»

Ese valor no pertenece al esquema: lo metí yo en los desplegables del cuaderno
al construirlo, y los revisores lo eligieron de buena fe. Donde el esquema tiene
un hueco con ese mismo significado se traduce a él, porque significan lo mismo:

  dtr_status  ->  not-derivable   (el propio esquema lo tiene, literal)
  route       ->  NA              (el registro de decisiones del 11 de agosto
  modality    ->  NA               define NA como «un hueco: significa que no
                                   lo sabemos», que es exactamente esto)

Donde el esquema NO tiene ese hueco --`study_design` y `extraction_status`, que
no admiten «no lo sé»-- la fila se queda sin ingerir y se informa. Elegir por
ellos entre `other` y `PARTIAL` sería inventar una respuesta que nadie dio.

Uso:
    python scripts/ingest_adjudications.py            # informe, no escribe
    python scripts/ingest_adjudications.py --escribir
"""
import argparse
import collections
import csv
import datetime
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from extraction_schema import CATEGORICOS  # noqa: E402

ROOT = pathlib.Path(__file__).resolve().parent.parent
EXTR = ROOT / "revision_sistematica" / "extraccion"
CUADERNO = EXTR / "ADJUDICACION_conflictos.xlsx"
CONFLICTOS = EXTR / "extraction_conflicts.csv"

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

# Traducciones literales, una a una, con el motivo. NADA se anade aqui sin que
# las dos formas signifiquen lo mismo; si hay que pensarlo, no va en esta tabla.
EQUIVALENCIAS = {
    ("dtr_status", "NO"): ("no", "solo mayusculas"),
    ("dtr_status", "Si"): ("yes", "castellano"),
    ("dtr_status", "SI"): ("yes", "castellano"),
    ("dtr_status", "no derivable"): ("not-derivable", "el esquema lo tiene literal"),
    ("route", "Intravenosa"): ("IV", "castellano"),
    ("route", "intravenosa"): ("IV", "castellano"),
    ("route", "topica/local"): ("topical/local", "castellano"),
    ("route", "no derivable"): ("NA", "NA es «no lo sabemos» en este esquema"),
    ("modality", "no derivable"): ("NA", "NA es «no lo sabemos» en este esquema"),
}

# Campos que piden un recuento. Un «SI» aqui contesta a otra pregunta.
NUMERICOS = {
    "n_arm", "clinical_success_n", "microbio_eradication_n", "mortality_n",
    "adverse_event_n", "resistance_emergence_n", "los_days", "publication_year",
}


def normaliza(campo, valor):
    """(valor_final, nota) o (None, motivo del rechazo)."""
    v = str(valor).strip()
    if not v:
        return None, "vacío"
    if (campo, v) in EQUIVALENCIAS:
        nuevo, razon = EQUIVALENCIAS[(campo, v)]
        return nuevo, "«%s» -> «%s» (%s)" % (v, nuevo, razon)
    ops = CATEGORICOS.get(campo)
    if ops:
        if v in ops:
            return v, ""
        return None, ("«%s» no está en el vocabulario de %s (admite: %s)"
                      % (v, campo, ", ".join(ops)))
    if campo in NUMERICOS:
        if v.upper() in ("NA", "NR"):
            return v.upper(), ("«%s» -> «%s»" % (v, v.upper())) if v != v.upper() else ""
        if not v.replace(".", "", 1).isdigit():
            return None, "«%s» no es un recuento y %s pide uno" % (v, campo)
    return v, ""


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--escribir", action="store_true",
                    help="sin esto solo informa, no toca el CSV")
    # Un segundo cuaderno con el mismo formato de diez columnas. Lo escribe
    # `make_firma_pendientes.py` y solo lleva los desacuerdos que seguian
    # abiertos: el grande tiene 574 filas y los pendientes no se ven ahi.
    ap.add_argument("--cuaderno", default=None,
                    help="ruta de otro cuaderno con la hoja «Desacuerdos» "
                         "(por defecto, %s)" % CUADERNO.name)
    args = ap.parse_args()

    cuaderno = pathlib.Path(args.cuaderno) if args.cuaderno else CUADERNO
    if not cuaderno.exists():
        print("no existe %s" % cuaderno)
        return 1
    import openpyxl

    libro = openpyxl.load_workbook(cuaderno, data_only=True)
    if "Desacuerdos" not in libro.sheetnames:
        print("%s no tiene una hoja «Desacuerdos»; tiene %s"
              % (cuaderno.name, ", ".join(libro.sheetnames)))
        return 1
    # La firma vive en su propia hoja en el cuaderno de pendientes. Si esta y
    # falta algun nombre o la fecha, no se ingiere: es la misma regla que
    # aplica `ingest_rob.py --consenso`, y por el mismo motivo.
    if "Firma" in libro.sheetnames:
        f = libro["Firma"]
        faltan = [f.cell(i, 1).value or "?" for i in (5, 6, 7)
                  if not str(f.cell(i, 2).value or "").strip()]
        if faltan:
            print("la hoja «Firma» de %s esta incompleta: falta %s"
                  % (cuaderno.name, ", ".join(faltan)))
            print("sin los dos nombres y la fecha, «consenso» es una palabra")
            return 1
    print("leyendo %s" % cuaderno.name)
    h = libro["Desacuerdos"]
    filas = list(h.iter_rows(min_row=2, values_only=True))
    # Columnas del cuaderno: 0 estudio, 1 brazo, 6 acordado, 7 quien, 8 fecha,
    # 9 campo interno. El orden lo fija build_adjudication_workbook.py.
    firmadas, sin_firma, sin_resolver, rechazadas, traducciones = {}, [], [], [], []
    for f in filas:
        est, brazo, acordado, quien, fecha, campo = f[0], f[1], f[6], f[7], f[8], f[9]
        clave = (est, brazo, campo)
        if acordado in (None, "") or not str(acordado).strip():
            sin_resolver.append((clave, "sin valor acordado"))
            continue
        if quien in (None, "") or not str(quien).strip():
            # Una resolucion sin firma no es un consenso: es una opinion.
            sin_firma.append((clave, str(acordado)[:40]))
            continue
        valor, nota = normaliza(campo, acordado)
        if valor is None:
            rechazadas.append((clave, nota))
            continue
        if nota:
            traducciones.append((clave, nota))
        f_txt = (fecha.date().isoformat()
                 if isinstance(fecha, datetime.datetime) else str(fecha)[:10])
        firmadas[clave] = (valor, str(quien).strip(), f_txt)

    # ---- volcado sobre el fichero de conflictos ---------------------------
    conf = list(csv.DictReader(open(CONFLICTOS, encoding="utf-8")))
    cab = list(conf[0])
    nuevas = pisadas = 0
    for r in conf:
        clave = (r["study_id"], r["arm_id"], r["campo"])
        if clave not in firmadas:
            continue
        valor, quien, fecha = firmadas[clave]
        previo = (r.get("resolucion") or "").strip()
        if previo and previo != valor:
            # Las dos filas de journal_tier se cerraron por una regla mecanica
            # sobre una comparacion superada; el consenso las pisa, y eso es lo
            # que queremos, pero que quede dicho.
            pisadas += 1
            print("  pisa una resolución anterior: %s %s «%s» -> «%s»"
                  % (r["study_id"], r["campo"], previo, valor))
        if not previo:
            nuevas += 1
        r["resolucion"], r["resuelto_por"], r["fecha"] = valor, quien, fecha

    # Las dos filas de journal_tier se cerraron antes, aplicando una regla
    # mecanica («casilla en blanco en un metadato objetivo») sobre una
    # comparacion que despues quedo superada. Al rehacerla las dos casillas
    # estaban llenas y discrepaban, asi que la regla dejo de corresponder pero
    # el texto de procedencia se quedo escrito, y dice algo que el fichero no
    # sostiene. No se borra la resolucion --sigue siendo el valor que se uso--
    # pero su procedencia pasa a decir la verdad, que es que nadie la firmo.
    VIEJA = "R2 casilla en blanco en metadato del registro"
    corregidas = 0
    for r in conf:
        if VIEJA in (r.get("resuelto_por") or "") and \
                (r["valor_Danny_Valdiviezo"] or "").strip() and \
                (r["valor_Nataly_Trelles"] or "").strip():
            r["resuelto_por"] = ("cerrado por regla mecánica sobre una comparación "
                                 "superada; SIN firma conjunta de los dos revisores")
            corregidas += 1

    en_csv = {(r["study_id"], r["arm_id"], r["campo"]) for r in conf}
    huerfanas = [k for k in firmadas if k not in en_csv]

    # ---- informe -----------------------------------------------------------
    print()
    print("cuaderno: %d filas" % len(filas))
    print("  firmadas y aptas para ingerir   %4d" % len(firmadas))
    print("  traducidas al vocabulario       %4d" % len(traducciones))
    print("  sin firmante                    %4d" % len(sin_firma))
    print("  sin valor acordado              %4d" % len(sin_resolver))
    print("  RECHAZADAS                      %4d" % len(rechazadas))
    if corregidas:
        print("  procedencias falsas corregidas  %4d" % corregidas)
    if huerfanas:
        print("  firmadas que no están en el CSV %4d" % len(huerfanas))

    if traducciones:
        print()
        print("traducciones aplicadas (%d):" % len(traducciones))
        for razon, n in collections.Counter(t[1] for t in traducciones).most_common():
            print("   %3d x  %s" % (n, razon))

    for titulo, lista in (("RECHAZADAS: no se ingieren", rechazadas),
                          ("Sin firmante: no se ingieren", sin_firma),
                          ("Sin valor acordado", sin_resolver)):
        if not lista:
            continue
        print()
        print("%s (%d):" % (titulo, len(lista)))
        for (est, brazo, campo), motivo in lista:
            print("   %-9s %-3s %-26s %s" % (est, brazo, campo, motivo))

    print()
    if not args.escribir:
        print("informe solamente. Repite con --escribir para volcarlo.")
        return 0

    with open(CONFLICTOS, "w", encoding="utf-8", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=cab)
        w.writeheader()
        w.writerows(conf)
    total = sum(1 for r in conf if (r.get("resolucion") or "").strip())
    print("escrito %s" % CONFLICTOS.name)
    print("  %d resoluciones nuevas, %d pisadas" % (nuevas, pisadas))
    print("  el fichero queda con %d de %d desacuerdos firmados"
          % (total, len(conf)))
    print()
    print("Ahora: build_synthesis_scalars.py y luego el paquete.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
