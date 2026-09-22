# -*- coding: utf-8 -*-
"""Escribe la lista de material suplementario en el maestro y en el ingles.

POR QUE EXISTE

Las dos listas estaban escritas a mano y las dos se quedaron cortas: citaban
16 anexos de los 24 que el paquete envia, y la del manuscrito INGLES estaba
ademas redactada EN ESPANOL, salvo dos entradas. Ninguna cifra dentro de ellas
la vigilaba nadie --la del ingles seguia diciendo «los 184 estudios»-- porque
un guardian que solo mira el cuerpo no mira los anexos.

Ahora salen de una sola tabla, con las cifras por nombre desde los escalares, y
se comprueba que cada anexo citado exista de verdad en el paquete.

Uso:
    python scripts/build_lista_anexos.py
"""
import json
import pathlib
import re
import sys

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

ROOT = pathlib.Path(__file__).resolve().parent.parent
PAQUETE = ROOT / "verificables revisión sistemática"
ES = ROOT / "paper" / "manuscrito_revision_sistematica.md"
EN = ROOT / "paper" / "manuscript_systematic_review_en.md"

INI_ES, INI_EN = "## Material suplementario", "## Supplementary material"
CIERRE_ES = ("Los acompaña una guía que explica, fichero a fichero, qué "
             "contiene y qué pregunta permite contestar.")
CIERRE_EN = ("A guide accompanies them explaining, file by file, what each "
             "contains and what question it lets the reader answer.")

# (codigo, texto es, texto en). Los huecos {x} son escalares.
ANEXOS = [
    ("S0", "Informe editorial: qué se decidió, cuándo y con qué fundamento.",
     "Editorial report: what was decided, when, and on what grounds."),
    ("S1", "Lista de comprobación PRISMA 2020.",
     "PRISMA 2020 checklist."),
    ("S2", "Ecuaciones de búsqueda literales por fuente, con fecha y número de "
           "resultados.",
     "Verbatim search strings by source, with date and number of results."),
    ("S3", "Registro completo de decisiones de cribado, en dos ficheros: etapa 2 "
           "(título) y etapa 3 (resumen). Cada fila lleva su motivo codificado, "
           "quién la emitió y cuándo.",
     "Full record of screening decisions, in two files: stage 2 (title) and "
     "stage 3 (abstract). Every row carries its coded reason, who issued it "
     "and when."),
    ("S4", "Pre-extracción desde el resumen de los {estudios_extraibles} estudios "
           "con publicación recuperable, marcada como parcial en cada registro.",
     "Pre-extraction from the abstracts of the {estudios_extraibles} studies "
     "with a retrievable publication, flagged as partial in every record."),
    ("S5", "Listado de los {estudios} estudios con su situación y sus informes "
           "agrupados, y de los {estudios_excluidos_tras_texto_completo} "
           "excluidos tras el cribado, con su motivo y su cita.",
     "Listing of the {estudios} studies with their status and grouped reports, "
     "and of the {estudios_excluidos_tras_texto_completo} excluded after "
     "screening, with their reason and supporting quotation."),
    ("S6", "Auditoría de controles positivos.",
     "Positive-control audit."),
    ("S7", "Declaraciones ICMJE.",
     "ICMJE declarations."),
    ("S8", "Registro de recuperación de texto completo: qué se intentó por cada "
           "estudio y con qué resultado.",
     "Full-text retrieval log: what was attempted for each study and with what "
     "result."),
    ("S9", "Idioma por informe, con la clase de evidencia que aportaba.",
     "Language by report, with the class of evidence it provided."),
    ("S10", "Verificación del idioma sobre el texto completo del PDF, no sobre "
            "los metadatos.",
     "Language verification against the full text of the PDF, not against the "
     "metadata."),
    ("S11", "Concordancia entre las dos extracciones independientes, antes de "
            "resolver los desacuerdos.",
     "Agreement between the two independent extractions, before disagreements "
     "were resolved."),
    ("S12", "Resolución de conflictos de extracción, incluidos los que no pueden "
            "dirimirse todavía.",
     "Resolution of extraction conflicts, including those that cannot yet be "
     "settled."),
    ("S13", "Reglas de extracción de desenlaces, con su corrección documentada.",
     "Outcome extraction rules, with their documented correction."),
    ("S14", "Extracción adjudicada: un valor por casilla, brazo a brazo, tras el "
            "consenso. Sostiene la sección 3.5 y las tablas 5 y 6.",
     "Adjudicated extraction: one value per cell, arm by arm, after consensus. "
     "Underpins section 3.5 and Tables 5 and 6."),
    ("S15", "Procedencia de cada casilla de S14: acuerdo, consenso, una sola "
            "lectura o abierta.",
     "Provenance of every cell in S14: agreement, consensus, single reading, or "
     "still open."),
    ("S16", "Los {estudios_excluidos_tras_texto_completo} estudios que el cribado "
            "admitió y el texto completo desmintió, con su código de motivo y la "
            "frase del artículo que lo sostiene.",
     "The {estudios_excluidos_tras_texto_completo} studies the screening "
     "admitted and the full text contradicted, with their reason code and the "
     "sentence from the article that supports it."),
    ("S17", "La Tabla 6 desglosada: los siete requisitos, brazo a brazo sobre los "
            "{desenlace_brazos} brazos, con el primero que falla y por qué.",
     "Table 6 broken down: the seven requirements, arm by arm over the "
     "{desenlace_brazos} arms, with the first one that fails and why."),
    ("S18", "Los {celdas_tabla5} juicios de riesgo de sesgo, uno por fila, con la "
            "frase firmada en que se apoya cada uno.",
     "The {celdas_tabla5} risk-of-bias judgements, one per row, with the signed "
     "sentence supporting each."),
    ("S18b", "Las frases del artículo cosechadas por tema, que acompañan pero no "
             "sustituyen a la firmada.",
     "Sentences harvested from the articles by theme, which accompany but do "
     "not replace the signed one."),
    ("S19", "Qué modelo emitió las decisiones de cribado, cuándo, sobre qué "
            "ficheros, qué verificaron los autores y qué NO quedó registrado, "
            "marcado como dato faltante.",
     "Which model issued the screening decisions, when, over which files, what "
     "the authors verified and what was NOT recorded, flagged as missing data."),
    ("S20", "De qué informe salió cada uno de los {desenlace_brazos} brazos, y con "
            "qué prueba se estableció el vínculo.",
     "Which report each of the {desenlace_brazos} arms came from, and with what "
     "evidence the link was established."),
    ("S21", "Los pares de estudios que pueden describir a los mismos pacientes, "
            "con la señal que los marcó y la frase literal.",
     "Pairs of studies that may describe the same patients, with the signal "
     "that flagged them and the verbatim sentence."),
    ("S22", "Para cada variable de estratificación, cuántos estudios la declaran "
            "en el texto completo, cuántos la mencionan sin poder clasificarla, "
            "cuántos callan y de cuántos no hay texto.",
     "For each stratification variable, how many studies state it in the full "
     "text, how many mention it without allowing classification, how many are "
     "silent, and how many have no text at all."),
]


def existentes():
    """Los codigos que el paquete envia de verdad."""
    out = set()
    for f in PAQUETE.iterdir():
        m = re.match(r"^(S\d+b?)_", f.name)
        if m:
            out.add(m.group(1))
    return out


def main():
    S = json.loads((ROOT / "quality_reports" / "synthesis_scalars.json")
                   .read_text(encoding="utf-8"))
    O = json.loads((ROOT / "quality_reports" / "outcome_scalars.json")
                   .read_text(encoding="utf-8"))
    esc = dict(S, desenlace_brazos=O["brazos"])

    hay = existentes()
    citados = {a[0] for a in ANEXOS}
    faltan = citados - hay
    sobran = hay - citados
    if faltan:
        raise SystemExit("NO SE ESCRIBE: la lista cita anexos que el paquete no "
                         "tiene: %s" % ", ".join(sorted(faltan)))
    if sobran:
        raise SystemExit("NO SE ESCRIBE: el paquete envia anexos que la lista no "
                         "cita: %s" % ", ".join(sorted(sobran)))

    for ruta, ini, i_txt, cierre in ((ES, INI_ES, 1, CIERRE_ES),
                                     (EN, INI_EN, 2, CIERRE_EN)):
        t = ruta.read_text(encoding="utf-8")
        # Se trunca desde el encabezado, de modo que tiene que aparecer UNA
        # vez y ser la ultima seccion. Si algun dia deja de serlo, esto para
        # en vez de borrar lo que venga detras.
        marca = "\n" + ini
        if t.count(marca) != 1:
            raise SystemExit("«%s» aparece %d veces en %s"
                             % (ini, t.count(marca), ruta.name))
        i = t.index(marca) + 1
        if re.search(r"(?m)^## ", t[i + len(ini):]):
            raise SystemExit("hay secciones despues de «%s» en %s: este guion "
                             "las borraria" % (ini, ruta.name))
        lineas = ["- **%s.** %s" % (a[0], a[i_txt].format(**esc))
                  for a in ANEXOS]
        cuerpo = "%s\n\n%s\n\n%s\n" % (ini, "\n".join(lineas), cierre)
        ruta.write_text(t[:i] + cuerpo, encoding="utf-8", newline="\n")
        print("%-38s %d anexos" % (ruta.name, len(ANEXOS)))

    print("los %d codigos citados existen en el paquete" % len(citados))


if __name__ == "__main__":
    main()
