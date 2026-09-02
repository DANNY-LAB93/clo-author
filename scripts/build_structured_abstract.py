"""Compone el resumen estructurado del manuscrito a partir de los escalares.

Ninguna cifra se teclea: cada una entra por su nombre desde
`quality_reports/synthesis_scalars.json` y `quality_reports/outcome_scalars.json`,
igual que el resto del manuscrito. Si el corpus cambia, el resumen cambia con él
y no hay que acordarse de tocarlo.

Las normas de Journal of Science and Research (revistas.utb.edu.ec/index.php/sr,
consultadas el 2026-09-02) fijan el resumen en 250 palabras como maximo y entre
tres y cinco palabras clave, en español y en ingles.

CUIDADO CON EL RECUENTO. La primera version de este guion contaba 246 palabras
donde Word cuenta 256, porque descartaba los tokens sin letras ni digitos: las
cinco etiquetas ("Introduccion.", "Objetivo."...) y los cinco signos "%" sueltos.
Word cuenta como palabra todo token separado por espacios, y es el recuento de
Word el que mira la revista. Ahora se cuenta asi.

La revista no exige que el resumen lleve etiquetas; pide que establezca objetivo,
metodologia, resultados y conclusiones. Se generan las dos formas: la etiquetada
(que es la que pidio D.V.) y la de parrafo corrido, que es como aparecen los
resumenes publicados en la revista.

Salidas:
    paper/resumen_estructurado.md          -- las cuatro versiones, para pegar
    paper/manuscrito_JSR_final.md          -- se le reemplaza el resumen

Uso:
    python scripts/build_structured_abstract.py
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
MANUSCRITO = ROOT / "paper" / "manuscrito_JSR_final.md"
SALIDA = ROOT / "paper" / "resumen_estructurado.md"
TOPE = 250          # palabras, norma de la revista, contadas como cuenta Word
MIN_CLAVE, MAX_CLAVE = 3, 5


def escalares():
    def carga(n):
        d = json.loads((ROOT / "quality_reports" / n).read_text(encoding="utf-8"))
        return d.get("escalares", d)
    return carga("synthesis_scalars.json"), carga("outcome_scalars.json")


def mil(n):
    """23057 -> '23 057'. Espacio fino, que es lo que pide la norma en español."""
    return "{:,}".format(int(n)).replace(",", " ")


def dec_es(x):
    return ("%.1f" % float(x)).replace(".", ",")


def dec_en(x):
    return "%.1f" % float(x)


def textos(S, O):
    D = O["definicion_exito"]
    c = dict(
        registros=mil(S["registros_identificados"]),
        unicos=mil(S["informes_unicos"]),
        informes=S["informes_a_texto_completo"],
        evaluados=S["estudios_antes_de_releer"],
        excluidos=S["estudios_excluidos_tras_texto_completo"],
        leidos_fuera=S["excluidos_entre_los_leidos"],
        sin_texto_fuera=S["excluidos_sin_texto_completo"],
        estudios=S["estudios"],
        extraibles=S["estudios_extraibles"],
        con_texto=S["texto_completo_obtenido"],
        anio_min=S["anio_min"],
        anio_max=S["anio_max"],
        fuentes="ocho",
        fuentes_may="Ocho",
        brazos=O["brazos"],
        sin_def=D["sin_definicion_operativa"],
        firmados=S["extraccion_conflictos_firmados"],
        desacuerdos=S["extraccion_desacuerdos"],
    )
    es = dict(c, recuperacion=dec_es(S["texto_completo_pct"]),
              casos=dec_es(S["casos_unicos_pct"]),
              comparativos=dec_es(S["estudios_comparativos_pct"]),
              sin_clase=dec_es(S["sin_clase_util_pct"]),
              sin_def_pct=dec_es(D["sin_definicion_pct"]))
    en = dict(c, recuperacion=dec_en(S["texto_completo_pct"]),
              casos=dec_en(S["casos_unicos_pct"]),
              comparativos=dec_en(S["estudios_comparativos_pct"]),
              sin_clase=dec_en(S["sin_clase_util_pct"]),
              sin_def_pct=dec_en(D["sin_definicion_pct"]))

    # El tercer elemento, cuando esta, es la version para parrafo corrido: sin la
    # etiqueta delante, "Delimitar..." y "Revision sistematica..." se quedan sin
    # verbo principal y dejan de ser frases.
    ES = [
        ("Introducción",
         "Varias síntesis recientes agregan los desenlaces de la fagoterapia en "
         "*Pseudomonas aeruginosa* resistente en proporciones globales de éxito, "
         "presuponiendo una agregabilidad no examinada."),
        ("Objetivo",
         "Delimitar la evidencia clínica disponible y determinar si su estructura "
         "y su reporte admiten una síntesis cuantitativa de eficacia.",
         "Este trabajo delimita la evidencia clínica disponible y determina si su "
         "estructura y su reporte admiten una síntesis cuantitativa de eficacia."),
        ("Metodología",
         "Revisión sistemática conforme a PRISMA 2020, en dos corrientes: bases "
         "bibliográficas y registros de ensayos. {fuentes_may} fuentes, "
         "con ventana {anio_min}-{anio_max} donde la interfaz la admite. La unidad "
         "de inclusión fue el estudio, no el informe. Extracción por duplicado e "
         "independiente, con {firmados} de {desacuerdos} desacuerdos adjudicados "
         "por consenso. No se evaluó el riesgo de sesgo ni la certeza de la "
         "evidencia.",
         "Se realizó una revisión sistemática conforme a PRISMA 2020, en dos "
         "corrientes: bases bibliográficas y registros de ensayos. Se interrogaron "
         "{fuentes} fuentes, con ventana {anio_min}-{anio_max} donde la interfaz la "
         "admite. La unidad de inclusión fue el estudio, no el informe. Extracción "
         "por duplicado e independiente, con {firmados} de {desacuerdos} "
         "desacuerdos adjudicados por consenso. No se evaluó el riesgo de sesgo ni "
         "la certeza de la evidencia."),
        ("Resultados",
         "De {registros} registros quedaron {unicos} informes únicos; {informes} "
         "informes formaron {evaluados} estudios evaluados para elegibilidad, de "
         "los que {excluidos} se excluyeron: {leidos_fuera} al leer el artículo y "
         "{sin_texto_fuera} sin poder leerlo. Quedan {estudios} estudios, "
         "{extraibles} con publicación recuperable y {con_texto} con texto "
         "obtenido ({recuperacion} %). De esos {extraibles}, "
         "el {casos} % son reportes de caso único y el {comparativos} % tiene "
         "diseño comparativo; la categoría de resistencia no puede asignarse en el "
         "{sin_clase} %. En {sin_def} de los {brazos} brazos extraídos "
         "({sin_def_pct} %) no consta una definición operativa de éxito clínico. "
         "Ningún brazo reúne los requisitos aritméticos de una proporción agrupada "
         "y los de elegibilidad."),
        ("Conclusiones",
         "El cuerpo de evidencia es amplio y, a la vez, estructuralmente "
         "inadecuado para una síntesis cuantitativa de eficacia. Las proporciones de "
         "las síntesis previas descansan sobre supuestos que estos "
         "datos no verifican."),
    ]
    EN = [
        ("Introduction",
         "Several recent syntheses pool phage therapy outcomes in resistant "
         "*Pseudomonas aeruginosa* into overall success proportions, presupposing "
         "an aggregability that has not been examined."),
        ("Objective",
         "To delimit the available clinical evidence and to determine whether its "
         "structure and reporting admit a quantitative synthesis of efficacy.",
         "This work delimits the available clinical evidence and determines whether "
         "its structure and reporting admit a quantitative synthesis of efficacy."),
        ("Methodology",
         "Systematic review following PRISMA 2020, with separate streams for "
         "bibliographic databases and trial registries. Eight sources were queried "
         "with a {anio_min}-{anio_max} window where the interface allows it. The "
         "unit of inclusion was the study, not the report. Extraction was in "
         "duplicate and independent, with {firmados} of {desacuerdos} disagreements "
         "adjudicated by consensus. Risk of bias and certainty of evidence were "
         "not assessed.",
         "A systematic review was conducted following PRISMA 2020, with separate "
         "streams for bibliographic databases and trial registries. Eight sources "
         "were queried with a {anio_min}-{anio_max} window where the interface "
         "allows it. The unit of inclusion was the study, not the report. Data were "
         "extracted in duplicate and independently, with {firmados} of "
         "{desacuerdos} disagreements adjudicated by consensus. Risk of bias and "
         "certainty of evidence were not assessed."),
        ("Results",
         "From {registros} records, {unicos} unique reports remained; {informes} "
         "reports formed {evaluados} studies assessed for eligibility, of which "
         "{excluidos} were excluded: {leidos_fuera} on reading the article and "
         "{sin_texto_fuera} without being able to read it. {estudios} studies "
         "remain, {extraibles} with a retrievable publication and {con_texto} with "
         "the text obtained ({recuperacion} %). Of those {extraibles}, {casos} % are single case "
         "reports and {comparativos} % have a comparative design; resistance "
         "category cannot be assigned in {sin_clase} %. In {sin_def} of the "
         "{brazos} extracted arms ({sin_def_pct} %) no operational definition of "
         "clinical success is on record. No arm meets the arithmetic requirements "
         "of a pooled proportion together with those of eligibility."),
        ("Conclusions",
         "The evidence base is broad and, at the same time, structurally unsuited "
         "to a quantitative synthesis of efficacy. The overall proportions of "
         "previous syntheses rest on assumptions that these data do not verify."),
    ]

    def arma(bloques, ctx):
        return [(b[0], b[1].format(**ctx), (b[2] if len(b) > 2 else b[1]).format(**ctx))
                for b in bloques]
    return arma(ES, es), arma(EN, en)


CLAVE_ES = ["bacteriófagos", "fagoterapia", "*Pseudomonas aeruginosa*",
            "farmacorresistencia bacteriana múltiple", "revisión sistemática"]
CLAVE_EN = ["bacteriophages", "phage therapy", "*Pseudomonas aeruginosa*",
            "multiple bacterial drug resistance", "systematic review"]


def palabras(t):
    """Como cuenta Word: todo token separado por espacios.

    Incluye las etiquetas ("Resultados.") y los signos "%" sueltos, que es
    justamente lo que la primera version de este guion se dejaba fuera. El
    marcado de negrita y cursiva no llega al .docx, asi que se quita antes.
    """
    return len(t.replace("**", "").replace("*", "").split())


def etiquetado(bloques):
    return "\n\n".join("**%s.** %s" % (b[0], b[1]) for b in bloques)


def corrido(bloques):
    return " ".join(b[2] for b in bloques)


def main():
    S, O = escalares()
    es, en = textos(S, O)
    versiones = [
        ("Resumen estructurado (español)", etiquetado(es), es),
        ("Structured abstract (English)", etiquetado(en), en),
        ("Resumen en párrafo corrido (español)", corrido(es), es),
        ("Abstract as a single paragraph (English)", corrido(en), en),
    ]

    fallos = []
    for nombre, t, bloques in versiones:
        n = palabras(t)
        print("%-42s %3d palabras  %s" % (nombre, n, "OK" if n <= TOPE else "SE PASA"))
        if n > TOPE:
            # Se dice donde esta el peso, para saber por donde recortar.
            reparto = "  ".join("%s %d" % (b[0][:4], palabras(b[1])) for b in bloques)
            fallos.append("%s: %d palabras, el tope es %d. Reparto: %s"
                          % (nombre, n, TOPE, reparto))
    for nombre, cl in (("español", CLAVE_ES), ("inglés", CLAVE_EN)):
        if not MIN_CLAVE <= len(cl) <= MAX_CLAVE:
            fallos.append("palabras clave en %s: %d, la revista pide entre %d y %d"
                          % (nombre, len(cl), MIN_CLAVE, MAX_CLAVE))
    if fallos:
        raise SystemExit("NO SE ESCRIBE NADA:\n  " + "\n  ".join(fallos))

    cuerpo = ["# Resumen estructurado", "",
              "Generado por `scripts/build_structured_abstract.py` desde los escalares.",
              "No editar a mano: se regenera y se pierde el cambio.", "",
              "Normas de la revista comprobadas aquí: resumen de %d palabras como "
              "máximo —contadas como las cuenta Word, etiquetas y signos «%%» "
              "incluidos—, entre %d y %d palabras clave, en los dos idiomas."
              % (TOPE, MIN_CLAVE, MAX_CLAVE), ""]
    for nombre, t, _ in versiones:
        cl = CLAVE_EN if ("English" in nombre or "Abstract" in nombre) else CLAVE_ES
        eti = "Keywords" if cl is CLAVE_EN else "Palabras clave"
        cuerpo += ["## %s — %d palabras" % (nombre, palabras(t)), "", t, "",
                   "**%s:** %s." % (eti, "; ".join(cl)), ""]
    SALIDA.write_text("\n".join(cuerpo), encoding="utf-8")
    print("escrito %s" % SALIDA.relative_to(ROOT))

    # El manuscrito lleva la version etiquetada, que es la que pidio D.V.
    m = MANUSCRITO.read_text(encoding="utf-8")
    nuevo = ("## RESUMEN\n\n%s\n\n**Palabras clave:** %s.\n\n"
             "## ABSTRACT\n\n%s\n\n**Keywords:** %s.\n\n"
             % (etiquetado(es), "; ".join(CLAVE_ES),
                etiquetado(en), "; ".join(CLAVE_EN)))
    i, j = m.find("## RESUMEN"), m.find("## INTRODUCCIÓN")
    if i < 0 or j < 0:
        raise SystemExit("no encuentro el resumen dentro del manuscrito")
    fin = m.rfind("---", i, j)
    MANUSCRITO.write_text(m[:i] + nuevo + m[fin:], encoding="utf-8")
    print("resumen reemplazado dentro de %s" % MANUSCRITO.name)


if __name__ == "__main__":
    main()
