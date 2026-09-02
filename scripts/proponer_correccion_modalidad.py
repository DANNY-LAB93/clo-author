"""Propone, sin firmarlas, las correcciones de `modality` que contradice el PDF.

POR QUÉ NO LAS APLICA

Estos cinco valores no son desacuerdos abiertos: tres los escribieron IGUAL los
dos revisores y dos ya se cerraron por consenso. Cambiarlos desde un script
sería sustituir una decisión firmada por la mía. Lo que hace este fichero es lo
contrario: los deja en `hoja_de_consenso.csv` como un bloque nuevo, con la
frase del artículo que los contradice, la resolución propuesta y las tres
columnas de firma **vacías**. Los firman D. Valdiviezo y N. Trelles, o no se
cambian.

`modality` no alimenta ninguna cifra del manuscrito. Pero la extracción
adjudicada se publica entera como anexo S14, así que un valor equivocado ahí es
un dato publicado equivocado.

Uso:
    python scripts/proponer_correccion_modalidad.py            # informe
    python scripts/proponer_correccion_modalidad.py --escribir
"""
import csv
import pathlib
import sys

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

ROOT = pathlib.Path(__file__).resolve().parent.parent
HOJA = ROOT / "revision_sistematica" / "extraccion" / "hoja_de_consenso.csv"

MOTIVO = ("valor ya cerrado que el texto completo contradice: "
          "hay que reabrirlo y volver a firmarlo")

# Cada entrada lleva la frase LITERAL del artículo. Sin cita no se propone nada.
CORRECCIONES = [
    ("EST-019", "A", "phage+antibiotic combination",
     "phage therapy was proposed as compassionate use, maintaining the "
     "standard-of-care antibiotics during the treatment, as previously reported",
     "Los antibióticos de referencia se MANTUVIERON durante el tratamiento con "
     "fago; el artículo lo dice en la presentación del caso. Además el resumen "
     "abre con «In-house phage preparations were nebulized over 10 days with "
     "standard-of-care antibiotics».",
     "Presentación del caso; y resumen estructurado", "alta"),

    ("EST-038", "A", "phage+antibiotic combination",
     "bacteria, which were targeted by antibiotics as well as by phages, "
     "remained present throughout the years",
     "El propio artículo describe a los pacientes como tratados con las dos "
     "cosas. Es una serie del Eliava Phage Therapy Center sobre persistencia "
     "bacteriana, no un ensayo de fago aislado.",
     "Discusión", "media"),

    ("EST-085", "A", "phage+antibiotic combination",
     "the antibiotic was completely stopped at April 14",
     "Que el antibiótico se retirara en una fecha concreta prueba que se estaba "
     "administrando durante el tratamiento con fago. El pie de la figura 1D "
     "rotula además «the application of phage and antibiotics».",
     "Resultados; pie de la figura 1D", "alta"),

    ("EST-178", "A", "phage+antibiotic combination",
     "Adding of polyvalent bacteriophage contributes to reducing the use of "
     "antibiotics and is recommended in the framework of the strategy of "
     "delayed prescribing of antibiotics",
     "El fago se AÑADE a una estrategia de prescripción diferida de "
     "antibióticos: no sustituye al antibiótico, lo pospone. (Este estudio está "
     "además propuesto para exclusión por población: cero menciones de "
     "P. aeruginosa en todo el artículo.)",
     "Conclusiones", "media"),

    ("EST-118", "A", "NA",
     "(sin texto completo: no hay artículo que leer)",
     "El valor «phage monotherapy» se codificó desde el resumen. El esquema "
     "reserva NA para «no lo sabemos», y esto es exactamente eso. Es un ECA, "
     "así que la casilla importa más que en un caso aislado.",
     "No procede: el texto completo no se ha recuperado", "alta"),
]


def main():
    escribir = "--escribir" in sys.argv
    cols = next(csv.reader(open(HOJA, encoding="utf-8")))
    previas = list(csv.DictReader(open(HOJA, encoding="utf-8")))
    ya = {(r["study_id"], r["arm_id"], r["campo"]) for r in previas}

    filas = []
    for est, brazo, propuesta, cita, razon, donde, conf in CORRECCIONES:
        if (est, brazo, "modality") in ya:
            print(f"  ya estaba en la hoja: {est} {brazo} modality -- no se duplica")
            continue
        f = {c: "" for c in cols}
        f.update({
            "bloque": "D", "motivo": MOTIVO,
            "study_id": est, "arm_id": brazo, "campo": "modality",
            "tipo": "categórico",
            "valor_Danny_Valdiviezo": "phage monotherapy",
            "valor_Nataly_Trelles": "phage monotherapy",
            "evidencia": cita,
            "resolucion_propuesta": propuesta,
            "razon": razon,
            "localizacion": donde,
            "confianza": conf,
        })
        filas.append(f)

    print(f"\n{len(filas)} correcciones propuestas, todas SIN FIRMAR:")
    for f in filas:
        print(f"  {f['study_id']} {f['arm_id']}  "
              f"{f['valor_Danny_Valdiviezo']} -> {f['resolucion_propuesta']}  "
              f"(confianza {f['confianza']})")

    if not escribir:
        print("\n(informe. Añade --escribir para volcarlas en hoja_de_consenso.csv)")
        return
    with open(HOJA, "a", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, cols)
        w.writerows(filas)
    print(f"\nañadidas a {HOJA.name}. Las firman los dos revisores, no este script.")


if __name__ == "__main__":
    main()
