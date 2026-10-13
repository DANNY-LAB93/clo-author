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
import csv
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

# De aquí sale S16 (build_verifiables_package.py lo copia tal cual).
EXCLUSIONES = (ROOT / "revision_sistematica" / "cribado"
               / "exclusiones_tras_texto_completo.csv")


def citas_s16(S):
    """Cuántas de las exclusiones de S16 llevan cita y cuántas no.

    La lista decía que todos llevan «la frase del artículo que lo sostiene»
    y era falso: los NOPDF no tienen artículo, los NOREC no tienen texto que
    se pudiera leer, y unas pocas filas más van sin cita. Se cuenta sobre el
    fichero del que sale S16, no se teclea, y si las cuentas no cuadran con el
    escalar el guion se para en vez de escribir una lista que no suma."""
    with open(EXCLUSIONES, encoding="utf-8-sig", newline="") as fh:
        filas = list(csv.DictReader(fh))
    sin_texto = ("NOPDF", "NOREC")
    con = sum(1 for r in filas if r["codigo"] not in sin_texto
              and r["cita_del_texto"].strip()
              and not r["cita_del_texto"].strip().startswith("("))
    otros = sum(1 for r in filas if r["codigo"] not in sin_texto) - con
    nopdf = S["excluidos_texto_completo_NOPDF"]
    norec = S["excluidos_texto_completo_NOREC"]
    if (len(filas) != S["estudios_excluidos_tras_texto_completo"]
            or con + otros + nopdf + norec != len(filas)):
        raise SystemExit("S16: %d filas en %s, %d con cita + %d sin cita + %d "
                         "NOPDF + %d NOREC; el escalar dice %d. No cuadra."
                         % (len(filas), EXCLUSIONES.name, con, otros, nopdf,
                            norec, S["estudios_excluidos_tras_texto_completo"]))
    return {"s16_con_cita": con, "s16_sin_cita_otros": otros}


def s12(e, en):
    """S12 con dos redacciones, según queden o no desacuerdos sin adjudicar.

    Decía «incluidos los que no pueden dirimirse todavía» cuando ya no quedaba
    ninguno (extraccion_conflictos_sin_firmar = 0), y no decía quién adjudicó:
    el registro anota a los dos revisores solo en una parte."""
    if en:
        t = ("How the {extraccion_desacuerdos} extraction disagreements were "
             "closed and who adjudicated them according to the log: both "
             "reviewers in {conflictos_resueltos_por_los_dos} and a single "
             "reviewer in {conflictos_resueltos_por_uno}; "
             "{extraccion_cerrados_por_regla} were closed by a mechanical rule, "
             "without joint sign-off")
        cola = ("; {extraccion_conflictos_sin_firmar} remain unadjudicated."
                if e["extraccion_conflictos_sin_firmar"] else ".")
    else:
        t = ("Cómo se cerraron los {extraccion_desacuerdos} desacuerdos de "
             "extracción y quién los adjudicó según el registro: los dos "
             "revisores en {conflictos_resueltos_por_los_dos} y uno solo en "
             "{conflictos_resueltos_por_uno}; {extraccion_cerrados_por_regla} se "
             "cerraron por una regla mecánica, sin firma conjunta")
        cola = ("; {extraccion_conflictos_sin_firmar} siguen sin adjudicar."
                if e["extraccion_conflictos_sin_firmar"] else ".")
    return (t + cola).format(**e)


def s16(e, en):
    """S16 separando lo que tiene cita de lo que no puede tenerla."""
    if en:
        t = ("The {estudios_excluidos_tras_texto_completo} studies the screening "
             "admitted that were excluded afterwards, with their reason code and "
             "who signed the exclusion. {s16_con_cita} carry the quotation that "
             "supports it; the {excluidos_texto_completo_NOPDF} without the full "
             "article (NOPDF) and the {excluidos_texto_completo_NOREC} without "
             "readable text (NOREC) have nothing to quote")
        cola = ((", and {s16_sin_cita_otros} more carry no quotation."
                 if e["s16_sin_cita_otros"] > 1 else
                 ", and {s16_sin_cita_otros} more carries no quotation.")
                if e["s16_sin_cita_otros"] else ".")
    else:
        t = ("Los {estudios_excluidos_tras_texto_completo} estudios que el "
             "cribado admitió y que salieron después, con su código de motivo y "
             "quién firmó la exclusión. {s16_con_cita} llevan la cita en que se "
             "apoya; los {excluidos_texto_completo_NOPDF} sin el artículo "
             "completo (NOPDF) y los {excluidos_texto_completo_NOREC} sin texto "
             "que se pudiera leer (NOREC) no tienen nada que citar")
        cola = ((", y {s16_sin_cita_otros} más van sin cita."
                 if e["s16_sin_cita_otros"] > 1 else
                 ", y {s16_sin_cita_otros} más va sin cita.")
                if e["s16_sin_cita_otros"] else ".")
    return (t + cola).format(**e)


# (codigo, texto es, texto en). Los huecos {x} son escalares. Un texto puede
# ser también una función de los escalares cuando la frase cambia de forma
# según el estado, no solo de cifra (S12, S16).
ANEXOS = [
    # S0 se presentaba como «Informe editorial» sin decir quién lo escribió.
    # Lo redactó el modelo de lenguaje haciendo de editor de revista (lo dice
    # el docstring de build_editorial_report.py) y la declaración de uso de IA
    # le atribuye la redacción de los anexos: un lector podía tomarlo por la
    # valoración de una persona.
    ("S0", "Evaluación previa del manuscrito que redactó el modelo de lenguaje "
           "en el papel de un editor de revista; no es una evaluación editorial "
           "externa.",
     "Pre-review assessment of the manuscript drafted by the language model in "
     "the role of a journal editor; it is not an external editorial "
     "assessment."),
    ("S1", "Lista de comprobación PRISMA 2020.",
     "PRISMA 2020 checklist."),
    # Prometía «con fecha» por fuente y no la hay: la ejecución de Scopus cuya
    # exportación entró al corpus no tiene fecha registrada.
    ("S2", "Ecuaciones de búsqueda literales por fuente, con su número de "
           "resultados.",
     "Verbatim search strings by source, with their number of results."),
    # «Motivo codificado» no vale para todas las filas: las del primer día de
    # cribado, y algunas de la etapa de resumen, llevan el motivo en texto libre.
    ("S3", "Registro completo de decisiones de cribado, en dos ficheros: etapa 2 "
           "(título) y etapa 3 (resumen). Cada fila lleva su motivo, quién la "
           "emitió y cuándo.",
     "Full record of screening decisions, in two files: stage 2 (title) and "
     "stage 3 (abstract). Every row carries its reason, who issued it and "
     "when."),
    # No decía quién la emitió: la emitió el modelo de lenguaje (declaración de
    # uso de IA). OJO: «desde el resumen de los {estudios_extraibles} estudios
    # con publicación recuperable» es un ancla de check_manuscript_claims.py,
    # que la exige dos veces en el maestro; no partir esa frase.
    ("S4", "Pre-extracción desde el resumen de los {estudios_extraibles} estudios "
           "con publicación recuperable, emitida por el modelo de lenguaje y "
           "marcada como parcial en cada registro.",
     "Pre-extraction from the abstracts of the {estudios_extraibles} studies "
     "with a retrievable publication, issued by the language model and flagged "
     "as partial in every record."),
    # Decía que S5 lista también los excluidos tras el cribado «con su motivo y
    # su cita», y S5 solo trae los estudios del corpus: los excluidos van en
    # S16 (build_verifiables_package.py lo dice al construir S5). El ancla de
    # check_manuscript_claims.py que fijaba la frase vieja («...agrupados, y de
    # los {estudios_excluidos_tras_texto_completo} excluidos») tiene que pasar a
    # la nueva.
    ("S5", "Listado de los {estudios} estudios del corpus, con su situación y sus "
           "informes agrupados. Los {estudios_excluidos_tras_texto_completo} "
           "excluidos después del cribado están en S16.",
     "Listing of the {estudios} studies in the corpus, with their status and "
     "grouped reports. The {estudios_excluidos_tras_texto_completo} excluded "
     "after screening are in S16."),
    ("S6", "Auditoría del cribado contra los {controles_fijados} controles "
           "positivos fijados antes de empezarlo, {controles_comprobables_pmid} "
           "de ellos comprobables por PMID.",
     "Audit of the screening against the {controles_fijados} positive controls "
     "fixed before it began, {controles_comprobables_pmid} of them checkable by "
     "PMID."),
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
    ("S11", "Concordancia entre las dos extracciones, antes de resolver los "
            "desacuerdos; su independencia no está acreditada.",
     "Agreement between the two extractions, whose independence is not "
     "established, before disagreements "
     "were resolved."),
    ("S12", lambda e: s12(e, False), lambda e: s12(e, True)),
    # No decia quien las redacto. Las redacto el modelo; que las decidieran
    # los dos autores es declaracion de D.V., y el registro no lo respalda.
    ("S13", "Reglas de extracción de desenlaces, con su corrección documentada. "
            "Las redactó el modelo de lenguaje; según declara D.V., las decidieron "
            "los dos autores, y el registro del 12 de agosto de 2026 las dejó como "
            "propuesta sin ratificar.",
     "Outcome extraction rules, with their documented correction. The language "
     "model drafted them; according to D.V., both authors decided them, and the "
     "record of 12 August 2026 left them as an unratified proposal."),
    # «Tras el consenso» era falso: el registro anota a los dos revisores solo
    # en una parte de los desacuerdos, y a uno solo en el resto.
    ("S14", "Extracción adjudicada: un valor por casilla, brazo a brazo, tras la "
            "adjudicación de los desacuerdos. Sostiene la sección 3.5 y las "
            "tablas 5 y 6.",
     "Adjudicated extraction: one value per cell, arm by arm, after the "
     "disagreements were adjudicated. Underpins section 3.5 and Tables 5 and 6."),
    # Etiquetaba «consenso» toda casilla adjudicada, la firmara una persona o
    # las dos. Son las etiquetas de S15 tras separar quién adjudicó.
    ("S15", "Procedencia de cada casilla de S14: acuerdo, adjudicada por los dos, "
            "adjudicada por uno, corregida contra el texto, una sola lectura o "
            "abierta.",
     "Provenance of every cell in S14: agreement, adjudicated by both "
     "reviewers, adjudicated by one, corrected against the text, single "
     "reading, or open."),
    ("S16", lambda e: s16(e, False), lambda e: s16(e, True)),
    ("S17", "La Tabla 6 desglosada: los siete requisitos, brazo a brazo sobre los "
            "{desenlace_brazos} brazos, con el primero que falla y por qué.",
     "Table 6 broken down: the seven requirements, arm by arm over the "
     "{desenlace_brazos} arms, with the first one that fails and why."),
    # Decía «con la frase firmada en que se apoya cada uno», y hay juicios en
    # que el cuaderno no registra apoyo alguno: S18 los marca [DATO FALTANTE].
    # Las tres clases salen de los escalares.
    ("S18", "Los {celdas_tabla5} juicios de riesgo de sesgo, uno por fila, con lo "
            "que sostiene cada uno en el cuaderno firmado: una cita literal en "
            "{citas_literales}, una nota sin cita en {notas_del_revisor} y nada "
            "en {juicios_sin_frase}, marcados como dato faltante.",
     "The {celdas_tabla5} risk-of-bias judgements, one per row, with what "
     "supports each in the signed notebook: a verbatim quotation in "
     "{citas_literales}, a note without a quotation in {notas_del_revisor} and "
     "nothing in {juicios_sin_frase}, flagged as missing data."),
    # No decía quién las «cosechó»: las localizó el modelo de forma automática
    # (evidencia_riesgo_sesgo.py) y las puso como comentario en los formularios.
    ("S18b", "Las frases de cada artículo que el modelo de lenguaje localizó de "
             "forma automática para cada dominio de riesgo de sesgo y puso como "
             "comentario en los formularios; acompañan a lo que sostiene cada "
             "juicio en S18, no lo sustituyen.",
     "The sentences from each article that the language model located "
     "automatically for each risk-of-bias domain and placed as comments in the "
     "forms; they accompany what supports each judgement in S18, they do not "
     "replace it."),
    # «Qué verificaron los autores» repartía entre los dos un examen que, según
    # declara D.V. (8 de octubre de 2026), hizo D.V. y no quedó registrado.
    ("S19", "Qué modelo emitió las decisiones de cribado, cuándo, sobre qué "
            "ficheros, qué examinó D.V., según su declaración, y qué no quedó "
            "registrado, marcado como dato faltante.",
     "Which model issued the screening decisions, when, over which files, what "
     "D.V. examined, according to D.V.'s statement, and what was not recorded, "
     "flagged as missing data."),
    ("S20", "De qué informe salió cada uno de los {desenlace_brazos} brazos, y con "
            "qué prueba se estableció el vínculo.",
     "Which report each of the {desenlace_brazos} arms came from, and with what "
     "evidence the link was established."),
    ("S21", "Los {pares_solapamiento_examinados} pares de estudios que podían "
            "describir a los mismos pacientes, con la señal que los marcó, el "
            "veredicto tras leer los dos artículos, los pacientes compartidos y "
            "la frase firmada en que se apoya.",
     "The {pares_solapamiento_examinados} pairs of studies that could describe "
     "the same patients, with the signal that flagged them, the verdict after "
     "reading both articles, the patients shared and the signed sentence it "
     "rests on."),
    ("S22", "Para cada variable de estratificación, cuántos estudios la declaran "
            "en el texto completo, cuántos la mencionan sin poder clasificarla, "
            "cuántos callan y de cuántos no hay texto.",
     "For each stratification variable, how many studies state it in the full "
     "text, how many mention it without allowing classification, how many are "
     "silent, and how many have no text at all."),
    ("S23", "La clase de resistencia de los {lectura_clase_estudios_leidos} estudios que "
            "tenían texto completo, comprobada contra el antibiograma del artículo: la "
            "conclusión firmada, la frase o la tabla en que se apoya, cómo se "
            "codificó y qué cambió en la extracción.",
     "The resistance class of the {lectura_clase_estudios_leidos} studies that had full "
     "text, checked against the article's antibiogram: the signed conclusion, "
     "the sentence or table it rests on, how it was coded and what changed in "
     "the extraction."),
    ("S24", "Los {comparativos_reextraidos_leidos} estudios con diseño comparativo, "
            "reextraídos: comparador, asignación, tiempo cero, tiempo de "
            "evaluación, cointervenciones, pérdidas, estimando y si hay un "
            "contraste para *P. aeruginosa*.",
     "The {comparativos_reextraidos_leidos} studies with a comparative design, "
     "re-extracted: comparator, allocation, time zero, assessment time, "
     "co-interventions, losses, estimand and whether there is a contrast for "
     "*P. aeruginosa*."),
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
    esc = dict(S, desenlace_brazos=O["brazos"], **citas_s16(S))

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
        lineas = ["- **%s.** %s" % (a[0], a[i_txt](esc) if callable(a[i_txt])
                                    else a[i_txt].format(**esc))
                  for a in ANEXOS]
        cuerpo = "%s\n\n%s\n\n%s\n" % (ini, "\n".join(lineas), cierre)
        ruta.write_text(t[:i] + cuerpo, encoding="utf-8", newline="\n")
        print("%-38s %d anexos" % (ruta.name, len(ANEXOS)))

    print("los %d codigos citados existen en el paquete" % len(citados))


if __name__ == "__main__":
    main()
