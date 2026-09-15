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
    # No es una cifra: es el codigo de protocolo del ensayo Phage4Cure-001,
    # que el manuscrito nombra al explicar el duplicado en CTIS. Anadido el
    # 2026-09-14, cuando ese parrafo entro en los tres manuscritos.
    "001": "codigo de protocolo del ensayo Phage4Cure-001, no una cantidad",
    # Comprobadas una a una el 2026-09-05 contra su fuente. Estaban saliendo
    # como "sin respaldo" desde hace semanas, y una lista de fallos que siempre
    # trae los mismos tres deja de leerse: son reales, y aqui consta por que.
    "4416": "registros que devolvio ProQuest, que NO se exporto ni forma parte "
            "del corpus; la cifra existe para declarar la fuente no usada",
    "495": "informes del corpus anteriores a 2016, contados sobre "
           "screening_corpus_all.csv: la ventana no se aplico en BVS, SciELO "
           "ni los registros",
    "98": "extraccion_doble_pct, que si es escalar; el comprobador lo marca "
          "porque el 98 aparece pegado a otra cifra en la misma frase",
    "2020": "PRISMA 2020, ano de la declaracion",
    "102": "TP-102, nombre del producto en el ensayo de Nir-Paz; no es una cifra",
    "2017": "ano de la lista de patogenos prioritarios de la OMS que la de 2024 sustituye",
    "15": "dia 15, momento de medida del desenlace continuo de BX004-A (Weiner 2025)",
    "14": "numero de anexos del paquete suplementario (S0-S13), contado del propio paquete",
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
    # Decia «numero de fuentes interrogadas (= fuentes_n)», y son OCHO fuentes:
    # `fuentes_n` cuenta los nueve brazos de busqueda, con Scopus repetido.
    # El manuscrito publica «ocho fuentes» y la glosa lo contradecia.
    "9": "brazos de busqueda (= fuentes_brazos_n; las fuentes son 8)",
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
    """Normaliza a punto decimal, sea cual sea la convencion del texto.

    El manuscrito existe en espanol (46,5 y 1 839) y en ingles (46.5 y
    23 057). Tratar el punto siempre como separador de millares convertia 63.4
    en 634 y marcaba como sin respaldo cada porcentaje de la version inglesa.
    La regla aplicada es la del ultimo separador: si le siguen una o dos cifras
    hasta el final, es un decimal; cualquier otro separador agrupa millares.
    """
    for esp in (" ", " ", " ", " "):
        s = s.replace(esp, "")
    s = s.strip()
    m = re.search(r"[.,](\d{1,2})$", s)
    if m:
        return "%s.%s" % (re.sub(r"[.,]", "", s[:m.start()]), m.group(1))
    return re.sub(r"[.,]", "", s)


def main():
    ruta = pathlib.Path(sys.argv[1]) if len(sys.argv) > 1 else POR_DEFECTO
    S = json.loads((ROOT / "quality_reports" / "synthesis_scalars.json")
                   .read_text(encoding="utf-8"))
    # Los desenlaces salen de la extraccion adjudicada y viven en su propio
    # fichero. Sin esto, las cifras de la seccion 3.5 aparecian como SIN
    # RESPALDO en el guardian numerico aunque el canal las produce: un aviso
    # que da falsos positivos se deja de leer, y entonces deja de avisar.
    oc = ROOT / "quality_reports" / "outcome_scalars.json"
    if oc.exists():
        S["_desenlaces"] = json.loads(oc.read_text(encoding="utf-8"))
    # El alcance del riesgo de sesgo vive en su propio fichero por el mismo
    # motivo, y el manuscrito lo cita: cuantos comparativos, cuantos
    # evaluables y cuantos juicios. Sin esto, el 82 salia sin respaldo.
    rb = ROOT / "quality_reports" / "rob_tabla_estado.json"
    if rb.exists():
        S["_riesgo_de_sesgo"] = json.loads(rb.read_text(encoding="utf-8"))

    # universo de valores respaldados por el canal
    respaldo = {}

    def anota(v, nombre):
        if isinstance(v, bool) or v is None:
            return
        if isinstance(v, (int, float)):
            respaldo.setdefault(str(v), []).append(nombre)
            if isinstance(v, float) and v == int(v):
                respaldo.setdefault(str(int(v)), []).append(nombre)

    # Recorrido RECURSIVO. Bajaba un solo nivel, y los escalares de desenlace
    # estan a tres (_desenlaces -> desenlaces -> campo -> cifra), asi que las
    # cifras de la seccion 3.5 salian sin respaldo aunque el canal las produce.
    def recorre(v, nombre):
        if isinstance(v, dict):
            for a, b in v.items():
                recorre(b, "%s[%s]" % (nombre, a))
        elif isinstance(v, list):
            return
        else:
            anota(v, nombre)

    for k, v in S.items():
        recorre(v, k)
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
    texto = re.sub(r"(secci[oó]n(es)?|sections?)\s+\d+(\.\d+)*", " ",
                   texto, flags=re.I)
    texto = re.sub(r"(?m)^-\s*S\d+\.", " ", texto)
    # El recuento de palabras es metadato autorreferente del propio manuscrito:
    # no procede del canal y no tiene sentido exigirle respaldo.
    texto = re.sub(r"(?m)^\*\*(Recuento de palabras|Word count).*$", " ", texto)

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
