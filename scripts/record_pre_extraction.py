"""Registra la pre-extracción hecha desde el RESUMEN, no desde el texto completo.

QUÉ ES Y QUÉ NO ES. No es una extracción y no es un tercer revisor. Es lo que el
resumen del registro bibliográfico permite afirmar, anotado con esa procedencia,
para que Danny y Nataly lleguen al texto completo sabiendo qué buscar. Todo lo
que el resumen no sostiene se queda vacío: la casilla vacía es el resultado
honesto, no un hueco que rellenar.

POR QUÉ NO ENTRA EN LA CONCORDANCIA. `compare_extractions.py` mide acuerdo entre
dos lecturas independientes. Dos lecturas del MISMO resumen no son
independientes, y una de ellas no ha visto el artículo. Meter esto ahí daría una
kappa alta que no mide fiabilidad sino redundancia -- y lo parecería. Por eso se
escribe en su propio archivo, con `extraction_status` siempre PARCIAL y la cita
diciendo de dónde salió.

CUÁNDO PUEDE MIRARSE. Después de que ambos revisores cierren su formulario. Si
se abre antes, la extracción deja de ser ciega y la concordancia se vuelve
decorativa.

FORMATO DEL LOTE (TSV, una línea por brazo):
    id_provisional \\t campo=valor \\t campo=valor ...
    EST-001  pathogen_scope=Pseudomonas-only  study_design=case report  n_arm=1

USO
    python scripts/record_pre_extraction.py --lote lote01.tsv
    python scripts/record_pre_extraction.py --estado
"""
import argparse
import collections
import csv
import datetime
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from extraction_schema import CAMPOS, CATEGORICOS, NUMERICOS, normaliza

ROOT = pathlib.Path(__file__).resolve().parent.parent
GRUPOS = ROOT / "revision_sistematica" / "cribado" / "study_groups.csv"
OUT = ROOT / "revision_sistematica" / "extraccion" / "pre_extraccion_desde_resumen.csv"

CITA = "Resumen del registro bibliográfico; texto completo NO consultado"
COLS = (["id_provisional", "arm_id"] + [c for c in CAMPOS if c != "arm_id"] +
        ["alerta_microbiologia", "alerta_revision", "registrado_en"])

csv.field_size_limit(200_000_000)
try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass


def universo():
    with open(GRUPOS, encoding="utf-8", newline="") as fh:
        return {"EST-%03d" % int(g["estudio"])
                for g in csv.DictReader(fh)
                if g["informe_para_extraer"] == "SI"
                and g["situacion"] in ("extraible", "solo-resumen")}


def cargar():
    if not OUT.exists():
        return {}
    with open(OUT, encoding="utf-8", newline="") as fh:
        return {(r["id_provisional"], r["arm_id"]): r for r in csv.DictReader(fh)}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--lote")
    ap.add_argument("--estado", action="store_true")
    args = ap.parse_args()

    ids = universo()
    hecho = cargar()

    if args.lote:
        stamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
        filas = []
        for linea in pathlib.Path(args.lote).read_text(encoding="utf-8").splitlines():
            if not linea.strip() or linea.lstrip().startswith("#"):
                continue
            partes = [p for p in linea.split("\t") if p.strip()]
            eid = partes[0].strip()
            if eid not in ids:
                sys.exit("%s no está entre los estudios a extraer" % eid)
            fila = {c: "" for c in COLS}
            fila["id_provisional"] = eid
            fila["arm_id"] = "A"
            for par in partes[1:]:
                if "=" not in par:
                    sys.exit("par sin '=' en %s: %r" % (eid, par))
                campo, valor = par.split("=", 1)
                campo, valor = campo.strip(), valor.strip()
                if campo not in COLS:
                    sys.exit("campo desconocido en %s: %r" % (eid, campo))
                # El vocabulario se valida contra el mismo esquema que el
                # formulario humano: si un valor no normaliza a una categoría
                # conocida, es un error de tecleo, no una categoría nueva.
                if campo in CATEGORICOS:
                    n = normaliza(campo, valor)
                    if n not in CATEGORICOS[campo]:
                        sys.exit("valor fuera del vocabulario en %s, %s: %r"
                                 % (eid, campo, valor))
                    valor = n
                if campo in NUMERICOS and normaliza(campo, valor) is None:
                    sys.exit("valor numérico ilegible en %s, %s: %r" % (eid, campo, valor))
                fila[campo] = valor
            fila["extraction_citation"] = CITA
            fila["extraction_status"] = "PARTIAL"   # nunca COMPLETE: falta el texto
            fila["registrado_en"] = stamp
            filas.append(fila)

        nuevo = not OUT.exists()
        OUT.parent.mkdir(parents=True, exist_ok=True)
        with open(OUT, "a", encoding="utf-8", newline="") as fh:
            w = csv.DictWriter(fh, fieldnames=COLS)
            if nuevo:
                w.writeheader()
            w.writerows(filas)
        print("registrados %d estudios" % len(filas))
        hecho = cargar()

    n = len({k[0] for k in hecho})
    print("\npre-extracción desde resumen")
    print("  estudios          : %d de %d (%.0f%%)" % (n, len(ids), 100.0 * n / len(ids)))
    print("  pendientes        : %d" % (len(ids) - n))
    if hecho:
        llenos = collections.Counter()
        for r in hecho.values():
            for c in CAMPOS:
                if (r.get(c) or "").strip():
                    llenos[c] += 1
        print("\n  campos con dato (de %d estudios):" % n)
        for c, k in llenos.most_common():
            if c not in ("extraction_citation", "extraction_status"):
                print("    %-30s %3d  (%.0f%%)" % (c, k, 100.0 * k / n))
        al = sum(1 for r in hecho.values()
                 if (r.get("alerta_microbiologia") or r.get("alerta_revision") or "").strip())
        print("\n  estudios con alguna alerta: %d" % al)


if __name__ == "__main__":
    main()
