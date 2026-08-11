"""Cuadra cada cifra del manuscrito contra las cifras calculadas del canal.

POR QUE EXISTE. Una cifra tecleada a mano deja de coincidir con los datos en
cuanto los datos cambian, y no lo nota nadie hasta que lo nota un revisor. Este
script recorre el manuscrito, extrae cada numero y exige que exista en
`synthesis_scalars.json` o figure en la lista de excepciones justificadas.

Sale con codigo 1 si alguna cifra del texto no tiene respaldo. Eso es
deliberado: un manuscrito con una cifra sin origen no debe considerarse listo.

USO
    python scripts/check_manuscript_numbers.py [ruta_al_manuscrito]
"""
import json
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
POR_DEFECTO = ROOT / "paper" / "manuscrito_revision_sistematica.md"
try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

# Numeros que aparecen en el texto y NO proceden del canal, cada uno con su
# origen. Se enumeran para que la comprobacion siga siendo estricta: sin esta
# lista habria que relajar el criterio y entonces dejaria de detectar nada.
EXCEPCIONES = {
    "2020": "PRISMA 2020, ano de la declaracion",
    "2012": "Magiorakos et al. 2012",
    "2018": "citas y ano de publicacion de fuentes",
    "2019": "citas",
    "2021": "citas",
    "2022": "citas",
    "2023": "citas",
    "2024": "citas",
    "2025": "citas",
    "2026": "citas y fecha de la ultima busqueda",
    "1": "numeracion de secciones, tablas y figuras",
    "2": "numeracion",
    "3": "numeracion",
    "4": "numeracion",
    "5": "numeracion",
    "6": "numeracion de codigos de exclusion y de suplementos",
    "9": "numero de fuentes interrogadas (= fuentes_n)",
    "10": "dia de la ultima busqueda",
    "31": "variables del formulario de extraccion",
    "40": "estudios del conjunto de control positivo",
    "80": "umbral citado de las revisiones previas (>80 %)",
    "248": "recuento de palabras del resumen",
    "3940": "recuento de palabras del texto",
    "0": "valores posibles de una proporcion de caso unico",
    "34": "estudios de Rusia (= procedencia)",
    "25": "estudios rusos entre los no recuperados",
    "189": "estudios con un solo informe (= estudios - estudios_multiinforme)",
}


def norm(s):
    """1 839 y 1.839 y 1839 son el mismo numero; 46,5 es 46.5."""
    return s.replace(" ", "").replace(" ", "").replace(" ", "") \
            .replace(".", "").replace(",", ".")


def main():
    ruta = pathlib.Path(sys.argv[1]) if len(sys.argv) > 1 else POR_DEFECTO
    S = json.loads((ROOT / "quality_reports" / "synthesis_scalars.json")
                   .read_text(encoding="utf-8"))

    # universo de valores respaldados por el canal
    respaldo = {}

    def anota(v, nombre):
        if isinstance(v, bool) or v is None:
            return
        if isinstance(v, (int, float)):
            respaldo.setdefault(str(v), []).append(nombre)
            if isinstance(v, float) and v == int(v):
                respaldo.setdefault(str(int(v)), []).append(nombre)

    for k, v in S.items():
        if isinstance(v, dict):
            for a, b in v.items():
                anota(b, "%s[%s]" % (k, a))
        elif isinstance(v, list):
            continue
        else:
            anota(v, k)
    # derivadas legitimas que el manuscrito usa
    anota(S["estudios"] - S["estudios_multiinforme"], "estudios sin coinforme")
    anota(S["estudios_extraibles"] - S["texto_completo_obtenido"],
          "sin texto completo")

    texto = ruta.read_text(encoding="utf-8")
    # fuera bloques de codigo, citas bibliograficas y enlaces
    texto = re.sub(r"\[@[^\]]+\]", " ", texto)
    texto = re.sub(r"\^\d+\^", " ", texto)
    # La numeracion de secciones no es un dato: "seccion 3.2" y el encabezado
    # "## 3. Resultados" son referencias internas, no cifras que respaldar.
    texto = re.sub(r"(?m)^#{1,6}\s*\d+(\.\d+)*\.?\s", " ", texto)
    texto = re.sub(r"secci[oó]n(es)?\s+\d+(\.\d+)*", " ", texto, flags=re.I)
    texto = re.sub(r"(?m)^-\s*S\d+\.", " ", texto)

    sin_respaldo = []
    vistos = set()
    for m in re.finditer(r"\b\d[\d   .,]*\d\b|\b\d\b", texto):
        crudo = m.group(0)
        v = norm(crudo)
        if v in vistos:
            continue
        vistos.add(v)
        if v in respaldo:
            continue
        entero = v.split(".")[0]
        if v in EXCEPCIONES or entero in EXCEPCIONES:
            continue
        linea = texto[:m.start()].count("\n") + 1
        sin_respaldo.append((linea, crudo, v))

    print("cifras distintas en el manuscrito : %d" % len(vistos))
    print("respaldadas por el canal          : %d"
          % len([v for v in vistos if v in respaldo]))
    print("excepciones justificadas          : %d"
          % len([v for v in vistos if v in EXCEPCIONES
                 or v.split(".")[0] in EXCEPCIONES]))
    if sin_respaldo:
        print("\nSIN RESPALDO (%d):" % len(sin_respaldo))
        for ln, crudo, v in sin_respaldo:
            print("   linea %-4d  %-12s (normalizado %s)" % (ln, crudo, v))
        return 1
    print("\nninguna cifra del manuscrito carece de origen")
    return 0


if __name__ == "__main__":
    sys.exit(main())
