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
    return (carga("synthesis_scalars.json"), carga("outcome_scalars.json"),
            carga("rob_tabla_estado.json"))


def mil(n):
    """23057 -> '23 057'. Espacio fino, que es lo que pide la norma en español."""
    return "{:,}".format(int(n)).replace(",", " ")


def dec_es(x):
    return ("%.1f" % float(x)).replace(".", ",")


def dec_en(x):
    return "%.1f" % float(x)


def sesgo(R):
    """La frase de riesgo de sesgo, en las dos formas que puede ser verdad.

    Mientras falte un juicio en `rob_tabla_estado.json` el resumen NO puede
    decir que la evaluación se hizo. Se redacta la forma pendiente, que es
    fea a propósito: se ve desde lejos y desaparece sola en cuanto los dos
    revisores cierran los formularios y se vuelve a ejecutar el guion.
    """
    n = R["evaluables"]
    if R["completa"] and R.get("modo") == "consenso":
        # El resumen tiene que decir POR CONSENSO. Omitirlo dejaria al lector
        # suponer duplicado independiente, que es lo normal en una revision
        # sistematica y no es lo que se hizo.
        return ("El riesgo de sesgo se evaluó por consenso, por dominios, en "
                "los %d comparativos (RoB 2, ROBINS-I); no "
                "se aplicó GRADE." % n,
                "Risk of bias was assessed by consensus, by domain, in the %d "
                "comparative studies (RoB 2, ROBINS-I); GRADE "
                "was not applied." % n)
    if R["completa"]:
        return ("El riesgo de sesgo se evaluó por dominios en los %d "
                "comparativos (RoB 2, ROBINS-I); no se "
                "aplicó GRADE." % n,
                "Risk of bias was assessed by domain in the %d comparative "
                "studies (RoB 2, ROBINS-I); GRADE was not "
                "applied." % n)
    return ("El riesgo de sesgo por dominios de los %d comparativos "
            "(RoB 2, ROBINS-I) está en evaluación; no se aplicó "
            "GRADE." % n,
            "Domain-level risk-of-bias assessment of the %d comparative "
            "studies (RoB 2, ROBINS-I) is under way; GRADE was "
            "not applied." % n)


def textos(S, O, R):
    D = O["definicion_exito"]
    sesgo_es, sesgo_en = sesgo(R)
    c = dict(
        registros=mil(S["registros_identificados"]),
        unicos=mil(S["informes_unicos"]),
        informes=S["informes_a_texto_completo"],
        evaluados=S["estudios_antes_de_releer"],
        excluidos=S["estudios_excluidos_tras_texto_completo"],
        leidos_fuera=S["excluidos_entre_los_leidos"],
        sin_texto_fuera=S["excluidos_sin_poder_leer_nada"],
        ficha_fuera=S["excluidos_sobre_la_ficha_de_registro"],
        nopdf=S["excluidos_texto_completo_NOPDF"],
        comp_fuera=S["criterio_texto_comparativos"],
        comp_antes=S["criterio_texto_comparativos_antes"],
        estudios=S["estudios"],
        extraibles=S["estudios_extraibles"],
        con_texto=S["texto_completo_obtenido"],
        # La VENTANA de busqueda, no el recorrido del corpus (ver
        # build_synthesis_scalars: dejaron de coincidir el 2026-10-06).
        anio_min=S["ventana_desde"],
        anio_max=S["ventana_hasta"],
        fuentes="ocho",
        fuentes_may="Ocho",
        brazos=O["brazos"],
        sin_def=D["sin_definicion_operativa"],
        firmados=S["extraccion_conflictos_firmados"],
        desacuerdos=S["extraccion_desacuerdos"],
        # los brazos que si reunen los seis requisitos que una proporcion
        # descriptiva exige, y cuantos de ellos son de un solo paciente
        agrupables=S["brazos_agrupables"],
        n1=S["brazos_agrupables_n1"],
        sesgo_es=sesgo_es,
        sesgo_en=sesgo_en,
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
         "sin examinar su agregabilidad."),
        ("Objetivo",
         "Delimitar la evidencia clínica disponible y determinar si su estructura "
         "y reporte admiten una síntesis cuantitativa de eficacia.",
         "Este trabajo delimita esa evidencia y determina si su estructura y "
         "reporte admiten una síntesis cuantitativa de eficacia."),
        ("Metodología",
         "Revisión sistemática conforme a PRISMA 2020, en dos corrientes: bases "
         "bibliográficas y registros de ensayos. {fuentes_may} fuentes, "
         "con ventana {anio_min}-{anio_max} donde la interfaz la admite. La unidad "
         "de inclusión fue el estudio, con artículo completo (criterio añadido tras la extracción). Extracción por duplicado e "
         "independiente, con {firmados} de {desacuerdos} desacuerdos adjudicados "
         "por consenso. {sesgo_es}",
         "Revisión sistemática conforme a PRISMA 2020 sobre {fuentes} fuentes "
         "—bases bibliográficas y registros de ensayos—, con ventana "
         "{anio_min}-{anio_max} donde la interfaz la admite. La unidad de inclusión fue el estudio, con artículo completo (criterio añadido tras la extracción). Extracción "
         "por duplicado e independiente, con {firmados} de {desacuerdos} "
         "desacuerdos adjudicados. {sesgo_es}"),
        ("Resultados",
         "De {registros} registros quedaron {unicos} informes únicos; {informes} "
         "informes formaron {evaluados} estudios evaluados para elegibilidad, de "
         "los que {excluidos} se excluyeron, {nopdf} por no disponer del artículo "
         "completo. Quedan {estudios} estudios, todos leídos a texto completo; "
         "exigirlo dejó fuera {comp_fuera} de {comp_antes} diseños comparativos. De ellos, "
         "el {casos} % son reportes de caso único y el {comparativos} % tiene "
         "diseño comparativo según el resumen; la categoría de resistencia no puede asignarse desde "
         "el resumen en el {sin_clase} %. En {sin_def} de {brazos} brazos extraídos "
         "({sin_def_pct} %) no consta una definición operativa de éxito clínico. "
         # PhagoBurn cumple los aritmeticos y los de elegibilidad y cae por la
         # metrica (mide un tiempo): «aritmeticos y de elegibilidad» a secas
         # era falso para ese brazo.
         "Ningún brazo reúne a la vez los requisitos aritméticos, los de "
         "elegibilidad y la métrica de una proporción agrupada."),
        ("Conclusiones",
         "El cuerpo de evidencia es amplio pero inadecuado para una síntesis "
         "cuantitativa de eficacia: las proporciones publicadas descansan sobre "
         "supuestos que estos datos no verifican."),
    ]
    EN = [
        ("Introduction",
         "Several recent syntheses pool phage therapy outcomes in resistant "
         "*Pseudomonas aeruginosa* into overall success proportions without "
         "examining their aggregability."),
        ("Objective",
         "To delimit the available evidence and determine whether its structure "
         "and reporting admit a quantitative synthesis of efficacy.",
         "This work delimits that evidence and determines whether its structure "
         "and reporting admit a quantitative synthesis of efficacy."),
        ("Methodology",
         "Systematic review following PRISMA 2020, with separate streams for "
         "bibliographic databases and trial registries. Eight sources were queried "
         "with a {anio_min}-{anio_max} window where the interface allows it. The "
         "unit of inclusion was the study, with its full article (a criterion added after extraction). Extraction was in "
         "duplicate and independent, with {firmados} of {desacuerdos} disagreements "
         "adjudicated. {sesgo_en}",
         "A PRISMA 2020 systematic review across eight sources —bibliographic "
         "databases and trial registries—, with a {anio_min}-{anio_max} window "
         "where the interface allows it. The "
         "unit of inclusion was the study, with its full article (a criterion added after extraction). Data were extracted in "
         "duplicate and independently, with {firmados} of {desacuerdos} "
         "disagreements adjudicated. {sesgo_en}"),
        ("Results",
         "From {registros} records, {unicos} unique reports remained; {informes} "
         "reports formed {evaluados} studies assessed for eligibility, of which "
         "{excluidos} were excluded, {nopdf} for lacking the full article. {estudios} "
         "studies remain, all read in full text; requiring it left out {comp_fuera} of "
         "{comp_antes} comparative designs. Of these, {casos} % are single case "
         "reports and {comparativos} % have a comparative design by abstract; resistance "
         "category cannot be assigned from the abstract in {sin_clase} %. In "
         "{sin_def} of the "
         "{brazos} extracted arms ({sin_def_pct} %) no operational definition of "
         "clinical success is on record. No arm meets all seven requirements of a "
         "pooled proportion; of the {agrupables} meeting the other six, {n1} have "
         "a single-patient denominator."),
        ("Conclusions",
         "The evidence base is broad but unsuited to a quantitative synthesis of "
         "efficacy: the published proportions rest on assumptions that these data "
         "do not verify."),
    ]

    def arma(bloques, ctx):
        return [(b[0], b[1].format(**ctx), (b[2] if len(b) > 2 else b[1]).format(**ctx))
                for b in bloques]
    return arma(ES, es), arma(EN, en)


# Las palabras clave van EMPAREJADAS y el orden se calcula, no se teclea. Las
# normas de JSR --leidas en revistas.utb.edu.ec el 14 de septiembre de 2026--
# piden dos cosas a la vez: que las castellanas vayan en orden alfabetico y que
# «las keywords deben estar escritas en el orden de las palabras clave», o sea
# en el orden del castellano, no en el suyo propio. Escritas como dos listas
# sueltas se descolocaban: «farmacorresistencia» iba detras de «Pseudomonas».
PARES_CLAVE = [
    ("bacteriófagos", "bacteriophages"),
    ("fagoterapia", "phage therapy"),
    ("farmacorresistencia bacteriana múltiple", "multiple bacterial drug resistance"),
    ("*Pseudomonas aeruginosa*", "*Pseudomonas aeruginosa*"),
    ("revisión sistemática", "systematic review"),
]


def _orden(par):
    """Alfabetico por la voz castellana, ignorando tildes y los asteriscos."""
    s = par[0].strip("*").lower()
    for a, b in zip("áéíóúü", "aeiouu"):
        s = s.replace(a, b)
    return s


CLAVE_ES = [es for es, _ in sorted(PARES_CLAVE, key=_orden)]
CLAVE_EN = [en for _, en in sorted(PARES_CLAVE, key=_orden)]


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
    S, O, R = escalares()
    es, en = textos(S, O, R)
    versiones = [
        ("Resumen estructurado (español)", etiquetado(es), es),
        ("Structured abstract (English)", etiquetado(en), en),
        ("Resumen en párrafo corrido (español)", corrido(es), es),
        ("Abstract as a single paragraph (English)", corrido(en), en),
    ]

    fallos = []
    for nombre, t, bloques in versiones:
        n = palabras(t)
        # Solo el parrafo corrido entra en el manuscrito; la etiquetada se
        # guarda aparte. Sus cinco etiquetas cuentan cinco palabras, y
        # bloquear el envio por ellas dejaba el resumen sin actualizar.
        manda = "corrido" in nombre or "single paragraph" in nombre
        print("%-42s %3d palabras  %s%s"
              % (nombre, n, "OK" if n <= TOPE else "SE PASA",
                 "" if manda else "  (no se envía)"))
        if n > TOPE and manda:
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

    # El manuscrito lleva la version de PARRAFO CORRIDO: la revista no publica
    # resumenes con subsecciones internas, y asi es como aparecen los suyos.
    # La version etiquetada se conserva en `resumen_estructurado.md` por si
    # hace falta para otro destino.
    m = MANUSCRITO.read_text(encoding="utf-8")
    nuevo = ("## RESUMEN\n\n%s\n\n**Palabras clave:** %s.\n\n"
             "## ABSTRACT\n\n%s\n\n**Keywords:** %s.\n\n"
             % (corrido(es), "; ".join(CLAVE_ES),
                corrido(en), "; ".join(CLAVE_EN)))
    i, j = m.find("## RESUMEN"), m.find("## INTRODUCCIÓN")
    if i < 0 or j < 0:
        raise SystemExit("no encuentro el resumen dentro del manuscrito")
    fin = m.rfind("---", i, j)
    MANUSCRITO.write_text(m[:i] + nuevo + m[fin:], encoding="utf-8")
    print("resumen reemplazado dentro de %s" % MANUSCRITO.name)


if __name__ == "__main__":
    main()
