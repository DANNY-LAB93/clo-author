"""Construye la tabla de criterios de inclusion y exclusion, a dos columnas.

D.V. pidio dos columnas enfrentadas --"Criterios de inclusion" y "Criterios de
exclusion"-- en lugar de la tabla por dominios (Poblacion, Intervencion,
Comparador...) que llevaba el manuscrito, y corrigio una primera version que
encabezaba cada fila con su dominio PICO: los criterios describen QUE ARTICULOS
entran y cuales no, no la pregunta PICO. Cada fila es ahora una frase sobre el
documento.

FICHAS DE REGISTRO Y RESUMENES DE CONGRESO. La tabla anterior no decia nada de
ellos, y sin embargo 60 de los 155 estudios del corpus existen unicamente como
ficha de registro de ensayo y 3 solo como resumen de congreso: 63 de 155,
admitidos de hecho pero no declarados en ningun criterio. Se declara ahora.

No confundir esa fila con el codigo PRO. PRO excluye ARTICULOS DE PROTOCOLO
publicados en revista (EST-035, EST-052, EST-083, EST-122; el de CYPHY tiene 223
ocurrencias de "will be"), que son un informe que anuncia lo que se hara. Una
ficha de registro es otra cosa: es el rastro del ensayo en la corriente de
registros que PRISMA 2020 obliga a separar, y se contabiliza como estudio
identificado aunque no aporte resultados. Las dos filas lo dicen expresamente,
porque juntas parecen contradecirse.

LOS CODIGOS NO SE IMPRIMEN. Cada motivo de exclusion lleva en el codigo fuente su
codigo del vocabulario cerrado (`scripts/exclusion_codes.py`) --ORG, VET, LAB...
el mismo con el que se cuentan las exclusiones en el diagrama PRISMA y en el
anexo S16--, pero la tabla sale sin ellos: D.V. los quito el 2026-09-03. Se
conserva el par motivo-codigo aqui porque es lo unico que ata cada fila de esta
tabla con su recuento; si alguien vuelve a quererlos visibles, basta con volver a
concatenarlos en `filas()`.

La ventana de publicacion no se teclea: sale de los escalares.

Salidas:
    paper/tablas/tabla_criterios_inclusion_exclusion.md
    paper/tablas/tabla_criterios_inclusion_exclusion.csv
    paper/manuscrito_JSR_final.md   -- se le reemplaza la Tabla 1

Uso:
    python scripts/build_criteria_table.py
"""
import csv
import json
import pathlib
import sys

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

ROOT = pathlib.Path(__file__).resolve().parent.parent
MANUSCRITO = ROOT / "paper" / "manuscrito_JSR_final.md"
TABLAS = ROOT / "paper" / "tablas"
BASE = "tabla_criterios_inclusion_exclusion"


def ventana():
    d = json.loads((ROOT / "quality_reports" / "synthesis_scalars.json")
                   .read_text(encoding="utf-8"))
    d = d.get("escalares", d)
    return d["anio_min"], d["anio_max"]


def filas():
    a, b = ventana()
    inclusion = [
        "Artículos originales publicados entre %s y %s, donde la interfaz de "
        "búsqueda permitió aplicar el filtro." % (a, b),
        "Artículos redactados en español o en inglés.",
        "Artículos nacionales e internacionales, incluida la literatura regional "
        "indexada en BVS y SciELO.",
        "Artículos originales que reporten el uso terapéutico de bacteriófagos "
        "líticos en pacientes humanos con infección por *Pseudomonas aeruginosa* "
        "multirresistente (MDR), extremadamente resistente (XDR) o panresistente "
        "(PDR), según Magiorakos et al., o descrita en términos que impliquen esas "
        "categorías.",
        "Artículos en los que el bacteriófago se administre solo o combinado con "
        "antimicrobianos, por cualquier vía.",
        "Artículos sobre varios patógenos, cuando los datos de *P. aeruginosa* "
        "pueden separarse del resto.",
        "Ensayos clínicos aleatorizados y no aleatorizados, estudios de cohorte, "
        "series de casos y reportes de caso que describan pacientes tratados.",
        "Artículos que informen al menos uno de los desenlaces de interés: éxito "
        "clínico, erradicación microbiológica, mortalidad, eventos adversos o "
        "emergencia de resistencia al fago.",
        "Fichas de registro de ensayos clínicos y resúmenes de congreso que cumplan "
        "lo anterior, contabilizados como estudios identificados aunque no aporten "
        "resultados publicados.",
    ]
    exclusion = [
        ("Artículos publicados fuera del período de estudio.", None),
        ("Estudios publicados en un idioma diferente del español o el inglés.", "IDI"),
        ("Estudios sobre un organismo distinto de *P. aeruginosa* cuando sus datos "
         "no pueden separarse del resto.", "ORG"),
        ("Estudios en animales o sobre aislados veterinarios.", "VET"),
        ("Estudios de laboratorio, preclínicos o de modelización, sin pacientes "
         "tratados.", "LAB"),
        ("Artículos de revisión bibliográfica, editoriales y comentarios sin datos "
         "primarios propios.", "REV"),
        ("Revisiones sistemáticas y revisiones de alcance.", "SEC"),
        ("Artículos que no evalúan fagoterapia en pacientes: encuestas, estudios "
         "epidemiológicos, notas de prensa u otra terapia.", "OFF"),
        ("Estudios en los que la intervención no es un bacteriófago, como "
         "endolisinas u otros derivados administrados sin la partícula viral.", "INT"),
        ("Artículos de protocolo publicados en revista, que declaran lo que se hará "
         "sin presentar resultados.", "PRO"),
        ("Estudios cuyo texto completo no se pudo recuperar, de modo que los "
         "criterios no pudieron verificarse contra el artículo.", "NOREC"),
    ]
    # El codigo NO se imprime: D.V. lo quito de la tabla el 2026-09-03. Se
    # conserva junto a cada motivo porque es lo que ata esta fila con el recuento
    # del diagrama PRISMA y con el anexo de exclusiones, y sin el par aqui esa
    # correspondencia solo vive en la cabeza de quien escribio la tabla.
    exc = [t for t, _ in exclusion]
    # Se enfrentan fila a fila; la columna corta se rellena en blanco, como en
    # la tabla que sirvio de modelo.
    n = max(len(inclusion), len(exc))
    inc = inclusion + [""] * (n - len(inclusion))
    exc = exc + [""] * (n - len(exc))
    return list(zip(inc, exc))


CABECERA = ("Criterios de inclusión", "Criterios de exclusión")


def main():
    f = filas()
    TABLAS.mkdir(parents=True, exist_ok=True)

    md = ["| %s | %s |" % CABECERA, "|---|---|"]
    md += ["| %s | %s |" % (i, e) for i, e in f]
    (TABLAS / (BASE + ".md")).write_text("\n".join(md) + "\n", encoding="utf-8")

    with open(TABLAS / (BASE + ".csv"), "w", encoding="utf-8-sig", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(CABECERA)
        for i, e in f:
            w.writerow([i.replace("**", "").replace("*", ""),
                        e.replace("**", "").replace("*", "")])
    print("escritas %s.md y %s.csv  (%d filas)" % (BASE, BASE, len(f)))

    # Sustituye la Tabla 1 dentro del manuscrito, pie incluido.
    m = MANUSCRITO.read_text(encoding="utf-8")
    ini = m.find("**Tabla 1.")
    if ini < 0:
        raise SystemExit("no encuentro la Tabla 1 en el manuscrito")
    fin = m.find("**Tabla 2.", ini)
    if fin < 0:
        raise SystemExit("no encuentro donde acaba la Tabla 1")
    pie = "**Tabla 1.** Criterios de inclusión y exclusión de los artículos.\n\n"
    MANUSCRITO.write_text(m[:ini] + pie + "\n".join(md) + "\n\n" + m[fin:],
                          encoding="utf-8")
    print("Tabla 1 del manuscrito reemplazada por el formato a dos columnas")


if __name__ == "__main__":
    main()
