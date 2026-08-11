"""Arma el paquete de peticiones para lo que no se pudo descargar en abierto.

QUÉ RESUELVE. Cuando las dos pasadas de acceso abierto terminan, queda un resto
de pago. Ese resto no se consigue con más código: se pide. Este script prepara
las tres vías que sí funcionan, cada una con el material listo para usar, para
que nadie tenga que rearmar la lista a mano.

  1. Acceso institucional -- lista con DOI para probar desde la red de la
     universidad o su VPN. Es lo primero, y suele resolver la mitad.
  2. Préstamo interbibliotecario -- CSV con los campos que pide una biblioteca.
  3. Petición a los autores -- correo redactado por artículo. En fagoterapia el
     campo es pequeño y los autores de casos clínicos suelen responder.

LO QUE NO ENTRA EN LA LISTA. Los resúmenes de congreso y los estudios que solo
existen como resumen: ahí no hay texto completo que pedir, y pedirlo sería
perseguir algo que no se publicó nunca. Salen marcados aparte.

USO
    python scripts/build_request_package.py
"""
import csv
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
GRUPOS = ROOT / "revision_sistematica" / "cribado" / "study_groups.csv"
POOL = ROOT / "revision_sistematica" / "cribado" / "screening_stage2_priorizado.csv"
PDFS = ROOT / "revision_sistematica" / "textos_completos" / "pdf"
DEST = ROOT / "revision_sistematica" / "extraccion"

csv.field_size_limit(200_000_000)
try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

CORREO = """Asunto: Solicitud de copia de su artículo para una revisión sistemática

Estimado/a autor/a:

Estoy realizando una revisión sistemática y metaanálisis sobre fagoterapia en
infecciones por Pseudomonas aeruginosa multirresistente (Universidad Católica de
Cuenca, Ecuador). Su artículo cumple los criterios de inclusión:

  {titulo}
  {revista} ({anio}){doi}

No tengo acceso institucional a esa revista. ¿Sería tan amable de enviarme una
copia del texto completo? La usaría únicamente para extraer los datos de
desenlace del estudio, que se citarán en la revisión.

Si dispone de datos a nivel de paciente sobre desenlace clínico, erradicación
microbiológica o eventos adversos que no aparezcan en el artículo, le agradecería
también esa información.

Muchas gracias por su tiempo.

Danny Valdiviezo
Universidad Católica de Cuenca
"""


def main():
    with open(POOL, encoding="utf-8", newline="") as fh:
        pool = {p["record_id"]: p for p in csv.DictReader(fh)}
    with open(GRUPOS, encoding="utf-8", newline="") as fh:
        fuentes = sorted([g for g in csv.DictReader(fh)
                          if g["informe_para_extraer"] == "SI"
                          and g["situacion"] in ("extraible", "solo-resumen")],
                         key=lambda g: int(g["estudio"]))

    tengo = {p.stem for p in PDFS.glob("*.pdf")} if PDFS.exists() else set()
    faltan, sin_texto = [], []
    for g in fuentes:
        eid = "EST-%03d" % int(g["estudio"])
        if eid in tengo:
            continue
        rec = pool[g["record_id"]]
        fila = {"id": eid, "titulo": " ".join(rec["title"].split()),
                "revista": rec["journal"], "anio": rec["year"],
                "doi": rec["doi"] if not rec["doi"].startswith("10.1002/central/") else "",
                "pmid": rec["pmid"], "tipo": g["tipo_informe"]}
        # Un resumen de congreso no tiene texto completo que pedir: lo que se
        # publicó ES el resumen. Pedirlo por préstamo hace perder el tiempo a la
        # biblioteca y al que lo pide.
        (sin_texto if g["tipo_informe"] != "articulo" else faltan).append(fila)

    DEST.mkdir(parents=True, exist_ok=True)
    campos = ["id", "titulo", "revista", "anio", "doi", "pmid", "tipo"]

    with open(DEST / "peticion_biblioteca.csv", "w", encoding="utf-8", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=campos)
        w.writeheader()
        w.writerows(faltan)

    with open(DEST / "sin_texto_completo_que_pedir.csv", "w", encoding="utf-8", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=campos)
        w.writeheader()
        w.writerows(sin_texto)

    with open(DEST / "correos_a_autores.txt", "w", encoding="utf-8") as fh:
        for f in faltan:
            fh.write("=" * 78 + "\n" + f["id"] + "\n" + "=" * 78 + "\n")
            fh.write(CORREO.format(
                titulo=f["titulo"], revista=f["revista"], anio=f["anio"],
                doi="\n  doi: " + f["doi"] if f["doi"] else ""))
            fh.write("\n\n")

    print("PDFs conseguidos            : %d de %d" % (len(tengo), len(fuentes)))
    print("Artículos por pedir         : %d" % len(faltan))
    print("Sin texto completo que pedir: %d  (resúmenes y fichas)" % len(sin_texto))
    print("\nescritos en revision_sistematica/extraccion/:")
    print("  peticion_biblioteca.csv")
    print("  correos_a_autores.txt")
    print("  sin_texto_completo_que_pedir.csv")


if __name__ == "__main__":
    main()
