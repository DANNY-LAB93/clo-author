"""Resuelve por regla los conflictos que no necesitan criterio, y estratifica el resto.

De los 169 conflictos que dejó `compare_extractions.py`, una parte no son
desacuerdos: son casillas en blanco y un error de tecleo. Llevar eso a una
reunión de consenso es gastar el único recurso escaso que hay, que es el rato
en que los dos revisores miran el mismo artículo a la vez.

LO QUE ESTE SCRIPT SE PERMITE RESOLVER SOLO, Y POR QUÉ

  R1. Error de tecleo contra un vocabulario cerrado. El valor no está en el
      vocabulario, está a un carácter de distancia de exactamente una entrada,
      y **el otro revisor escribió justamente esa entrada**. Esa última
      condición es la que lo hace seguro: no se adivina qué quiso poner nadie,
      se constata que el otro lo escribió bien de forma independiente.

  R2. Casilla en blanco en un metadato objetivo (`journal_tier`,
      `publication_year`). Son datos del registro bibliográfico, no lecturas
      del artículo: se comprueban fuera y no admiten dos interpretaciones. Un
      blanco ahí es una omisión, no una postura.

LO QUE NO SE PERMITE, AUNQUE PAREZCA MECÁNICO

  Un blanco en un campo de desenlace NO se rellena con el valor del otro. El
  propio esquema distingue vacío, `NA` y `0`: vacío es "no lo contestó", `NA`
  es "el artículo no lo dice" y `0` es "el artículo dice que ninguno". Dar por
  bueno el número del único que contestó convierte una doble extracción en una
  simple, que es exactamente lo que la revisión promete no hacer.

  Un valor fuera de vocabulario sin gemelo tampoco se corrige. `'2 meses'` en
  `los_days` es un problema de unidad y `'Si'` en `resistance_emergence_n` es
  alguien contestando sí/no donde se pide un recuento. Ambos se dejan al
  consenso, y ambos son señal de que el formulario admite texto donde debería
  cerrar la opción.

LO QUE HACE CON EL RESTO

  Lo estratifica en tres bloques, porque no se atacan igual:

  A. Sin artículo. El estudio no tiene texto completo. No es dirimible por
     nadie: primero hay que conseguir el artículo.
  B. Bloqueado por definición. Toca erradicación o éxito clínico, cuya regla
     sigue en PROPUESTA. Resolverlos antes de confirmarla es decidir dos veces.
  C. Dirimible. Hay artículo y la regla no está en disputa: se resuelve
     leyendo, y ahí sí hace falta el consenso.

Uso:
    python scripts/resolve_mechanical_conflicts.py [--fecha AAAA-MM-DD] [--escribir]

Sin `--escribir` no toca nada: enseña lo que haría.
"""
import argparse
import csv
import datetime
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from extraction_schema import CATEGORICOS, NUMERICOS, normaliza

ROOT = pathlib.Path(__file__).resolve().parent.parent
CONFLICTOS = ROOT / "revision_sistematica" / "extraccion" / "extraction_conflicts.csv"
ORDEN = ROOT / "quality_reports" / "orden_de_extraccion.csv"
HOJA = ROOT / "revision_sistematica" / "extraccion" / "hoja_de_consenso.csv"

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

# `journal_tier` es texto libre en el esquema, pero de hecho tiene vocabulario
# cerrado: son los cuatro niveles que el proyecto ya decidió. Se declara aquí
# para poder aplicarle R1 sin tocar el esquema compartido.
VOCABULARIO_EXTRA = {"journal_tier": ["alto", "medio", "bajo", "solo registro"]}

# Metadatos del registro, no lecturas del artículo. Solo estos admiten R2.
METADATO_OBJETIVO = ["journal_tier", "publication_year"]

# Campos que la regla en PROPUESTA redefine. Ver
# quality_reports/decisions/2026-08-11_definicion-erradicacion-y-exito.md
CAMPOS_BLOQUEADOS = ["microbio_eradication_n", "clinical_success_n",
                     "clinical_success_definition"]


def distancia_uno(a, b):
    """¿Se pasa de `a` a `b` con una sola inserción, borrado o sustitución?"""
    a, b = a.lower(), b.lower()
    if abs(len(a) - len(b)) > 1:
        return False
    if a == b:
        return False
    if len(a) == len(b):
        return sum(x != y for x, y in zip(a, b)) == 1
    corto, largo = (a, b) if len(a) < len(b) else (b, a)
    for i in range(len(largo)):
        if largo[:i] + largo[i + 1:] == corto:
            return True
    return False


def vocabulario(campo):
    if campo in CATEGORICOS:
        return CATEGORICOS[campo]
    return VOCABULARIO_EXTRA.get(campo, [])


def aplica_r1(campo, propio, ajeno):
    """Devuelve el valor corregido si `propio` es un tecleo de `ajeno`.

    Exige que `ajeno` sea una entrada legítima del vocabulario: si los dos
    escribieron algo raro, no hay nada que constatar y no se toca.
    """
    voc = vocabulario(campo)
    if not voc or not propio or not ajeno:
        return None
    if propio.strip().lower() in [v.lower() for v in voc]:
        return None                                   # `propio` ya es válido
    candidatos = [v for v in voc if distancia_uno(propio.strip(), v)]
    if len(candidatos) != 1:
        return None
    if ajeno.strip().lower() != candidatos[0].lower():
        return None                                   # el otro no lo confirma
    return candidatos[0]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--fecha", default=datetime.date.today().isoformat(),
                    help="fecha que se estampa en las resoluciones automáticas")
    ap.add_argument("--escribir", action="store_true",
                    help="sin esto, no modifica ningún archivo")
    args = ap.parse_args()

    filas = list(csv.DictReader(open(CONFLICTOS, encoding="utf-8")))
    orden = {r["id"]: r for r in csv.DictReader(open(ORDEN, encoding="utf-8-sig"))}
    tiene_texto = {k: (v.get("texto_completo") == "si") for k, v in orden.items()}

    resueltas, consenso = [], []
    contador = {"R1": 0, "R2": 0, "A": 0, "B": 0, "C": 0, "ya_resuelto": 0}

    for r in filas:
        campo = r["campo"]
        d = r["valor_Danny_Valdiviezo"].strip()
        n = r["valor_Nataly_Trelles"].strip()

        if r.get("resolucion", "").strip():
            contador["ya_resuelto"] += 1
            resueltas.append(r)
            continue

        # --- R1: tecleo confirmado por el otro revisor ---
        corregido = aplica_r1(campo, d, n) or aplica_r1(campo, n, d)
        if corregido:
            r["resolucion"] = corregido
            r["resuelto_por"] = "R1 error de tecleo, confirmado por el otro revisor"
            r["fecha"] = args.fecha
            contador["R1"] += 1
            resueltas.append(r)
            continue

        # --- R2: blanco en metadato objetivo ---
        if campo in METADATO_OBJETIVO and bool(d) != bool(n):
            r["resolucion"] = d or n
            r["resuelto_por"] = ("R2 casilla en blanco en metadato del registro; "
                                 "valor del revisor que lo cumplimentó")
            r["fecha"] = args.fecha
            contador["R2"] += 1
            resueltas.append(r)
            continue

        # --- estratificación del resto ---
        if not tiene_texto.get(r["study_id"], False):
            bloque, motivo = "A", "sin artículo: no dirimible hasta conseguir el texto completo"
        elif campo in CAMPOS_BLOQUEADOS:
            bloque, motivo = "B", "bloqueado por la regla de erradicación/éxito en PROPUESTA"
        else:
            bloque, motivo = "C", "dirimible leyendo el artículo"
        contador[bloque] += 1
        consenso.append({
            "bloque": bloque, "motivo": motivo,
            "study_id": r["study_id"], "arm_id": r["arm_id"], "campo": campo,
            "tipo": ("numérico" if campo in NUMERICOS
                     else "categórico" if campo in CATEGORICOS else "texto"),
            "valor_Danny_Valdiviezo": d or "(en blanco)",
            "valor_Nataly_Trelles": n or "(en blanco)",
            "evidencia": "", "resolucion_propuesta": "", "razon": "",
            "resolucion": "", "resuelto_por": "", "fecha": "",
        })
        resueltas.append(r)

    print(f"conflictos leídos: {len(filas)}")
    print(f"  resueltos por regla: {contador['R1'] + contador['R2']}"
          f"  (R1 tecleo: {contador['R1']}, R2 blanco en metadato: {contador['R2']})")
    print(f"  ya venían resueltos: {contador['ya_resuelto']}")
    print(f"  a la hoja de consenso: {len(consenso)}")
    print(f"     bloque A sin artículo:        {contador['A']}")
    print(f"     bloque B bloqueado por regla: {contador['B']}")
    print(f"     bloque C dirimible leyendo:   {contador['C']}")

    if not args.escribir:
        print("\n(ensayo: no se ha escrito nada; añade --escribir)")
        return

    with open(CONFLICTOS, "w", encoding="utf-8", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(filas[0].keys()))
        w.writeheader()
        w.writerows(resueltas)
    orden_bloque = {"C": 0, "B": 1, "A": 2}
    consenso.sort(key=lambda x: (orden_bloque[x["bloque"]], x["study_id"],
                                 x["arm_id"], x["campo"]))
    with open(HOJA, "w", encoding="utf-8", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(consenso[0].keys()))
        w.writeheader()
        w.writerows(consenso)
    print(f"\nescrito {CONFLICTOS}")
    print(f"escrito {HOJA}")


if __name__ == "__main__":
    main()
