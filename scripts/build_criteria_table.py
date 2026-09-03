"""Construye la tabla de criterios de inclusion y exclusion, a dos columnas.

D.V. pidio el formato de dos columnas enfrentadas --"Criterios de inclusion" /
"Criterios de exclusion"-- en lugar de la tabla por dominios (Poblacion,
Intervencion, Comparador...) que llevaba el manuscrito.

Se conserva la etiqueta PICO al principio de cada fila de inclusion. El formato
de dos columnas por si solo pierde la estructura PICO que PRISMA 2020 espera ver
en los criterios de elegibilidad, y perderla seria un motivo de comentario del
revisor; con la etiqueta delante se tienen las dos cosas.

Cada fila de exclusion lleva su codigo del vocabulario cerrado
(`scripts/exclusion_codes.py`), que es el mismo con el que se cuentan las
exclusiones en el diagrama PRISMA y en el anexo S16. Asi la tabla de criterios y
la de recuentos hablan el mismo idioma.

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
        ("Población", "Pacientes humanos con infección por *Pseudomonas aeruginosa* "
                      "clasificada como MDR, XDR o PDR según Magiorakos et al., o descrita "
                      "en términos que impliquen esas categorías."),
        ("Población", "Estudios con varios patógenos, cuando el subgrupo de "
                      "*P. aeruginosa* es separable."),
        ("Intervención", "Administración terapéutica de bacteriófagos líticos, por "
                         "cualquier vía."),
        ("Intervención", "Fagoterapia sola o combinada con antimicrobianos."),
        ("Comparador", "No se exigió comparador: se admitieron estudios de un solo brazo."),
        ("Desenlaces", "Estudios que reporten éxito clínico, erradicación microbiológica, "
                       "mortalidad, eventos adversos o emergencia de resistencia al fago, "
                       "según la definición de cada estudio."),
        ("Diseños", "Ensayos aleatorizados y no aleatorizados, cohortes, series de casos "
                    "y reportes de caso, con pacientes tratados."),
        ("Idioma", "Informes redactados en español o en inglés."),
        ("Periodo", "Publicaciones de %s a %s, donde la interfaz de búsqueda lo admite."
                    % (a, b)),
    ]
    exclusion = [
        ("ORG", "Organismo distinto de *P. aeruginosa*, sin subgrupo separable."),
        ("VET", "Aislados o infección veterinaria, no humana."),
        ("INT", "Endolisinas u otros derivados administrados sin la partícula viral."),
        ("OFF", "Estudios que no evalúan fagoterapia en pacientes: encuestas, "
                "epidemiología, prensa u otra terapia."),
        ("LAB", "Trabajo de laboratorio, preclínico o de modelización, sin pacientes "
                "tratados."),
        ("REV", "Revisiones narrativas y comentarios, sin datos primarios propios."),
        ("SEC", "Síntesis secundarias: revisiones sistemáticas y revisiones de alcance."),
        ("PRO", "Protocolos de estudio: declaran lo que se hará, sin resultados."),
        ("IDI", "Informes redactados en un idioma distinto del español o el inglés."),
        ("NOREC", "Estudios cuyo texto completo no se pudo recuperar, de modo que los "
                  "criterios no pudieron verificarse contra el artículo."),
    ]
    inc = ["**%s.** %s" % (e, t) for e, t in inclusion]
    exc = ["**%s.** %s" % (c, t) for c, t in exclusion]
    # Se enfrentan fila a fila; la columna corta se rellena en blanco, como en
    # la tabla que sirvio de modelo.
    n = max(len(inc), len(exc))
    inc += [""] * (n - len(inc))
    exc += [""] * (n - len(exc))
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
    pie = ("**Tabla 1.** Criterios de inclusión y exclusión de los estudios. Las "
           "filas de inclusión llevan delante el dominio PICO al que responden; las "
           "de exclusión, el código del vocabulario cerrado con el que se contabilizan "
           "en el diagrama PRISMA (Figura 1) y en el anexo de exclusiones.\n\n")
    MANUSCRITO.write_text(m[:ini] + pie + "\n".join(md) + "\n\n" + m[fin:],
                          encoding="utf-8")
    print("Tabla 1 del manuscrito reemplazada por el formato a dos columnas")


if __name__ == "__main__":
    main()
