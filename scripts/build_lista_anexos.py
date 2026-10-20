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

# El manuscrito de la revista: no numera los apartados y numera las tablas de
# otro modo que el maestro. La lista (en el maestro y el inglés) y la guía
# citan tablas y secciones; sus números se leen de aquí y del maestro.
REVISTA = ROOT / "paper" / "manuscrito_JSR_final.md"

# Cada tabla que citan la lista y la guía, reconocida por su pie, y el apartado
# de resultados que la presenta, reconocido por su título: (patrón del pie,
# patrón del título). Se buscan sin distinguir mayúsculas.
TEMAS = {
    "desenlaces": (r"desenlaces declarados", r"desenlace"),
    "riesgo": (r"^riesgo de sesgo", r"riesgo de sesgo"),
    "embudo": (r"sobreviven a cada requisito", r"viabilidad de la síntesis"),
}


def _pies(texto):
    """{número: pie} de las tablas, leídos de los «**Tabla N.**» del .md."""
    return {int(m.group(1)): m.group(2).strip()
            for m in re.finditer(r"(?m)^\*\*Tabla (\d+)\.\*\*\s*(.+)$", texto)}


def _resultados(texto):
    """(encabezado del capítulo de resultados, [(número o "", título)]) de
    sus apartados ###. La revista no los numera: su número queda vacío."""
    m = re.search(r"(?mi)^## +((?:\d+\.\s*)?resultados)\s*$", texto)
    if not m:
        return "", []
    resto = texto[m.end():]
    fin = re.search(r"(?m)^## ", resto)
    cuerpo = resto[:fin.start()] if fin else resto
    return m.group(1).strip(), [
        (a.group(1) or "", a.group(2).strip())
        for a in re.finditer(r"(?m)^### +(?:(\d+(?:\.\d+)+)\s+)?(.+?)\s*$", cuerpo)]


def _uno(hallados, que, ruta):
    if len(hallados) != 1:
        raise SystemExit("NO SE ESCRIBE: %s aparece %d veces en %s, y su número "
                         "no se puede leer del manuscrito"
                         % (que, len(hallados), ruta.name))
    return hallados[0]


def numeracion():
    """Número de tabla y de sección de cada tema en el maestro, y su
    equivalente en el manuscrito de la revista, leídos de los dos .md.

    Hasta el 2026-10-13 la guía y la lista tecleaban «la sección 3.5 y las
    tablas 5 y 6», «la tabla 7», con la numeración del maestro, y la guía viaja
    con el manuscrito de la revista, donde la de desenlaces es otra tabla y
    los apartados no llevan número. De la revista se da el título del apartado
    y el capítulo en que está («Riesgo de sesgo», de RESULTADOS)."""
    tm = ES.read_text(encoding="utf-8")
    tr = REVISTA.read_text(encoding="utf-8")
    pm, pr = _pies(tm), _pies(tr)
    _, am = _resultados(tm)
    cap_r, ar = _resultados(tr)
    out = {}
    for tema, (pie, titulo) in TEMAS.items():
        out[tema] = {
            "tabla_maestro": _uno(
                [n for n, p in pm.items() if re.search(pie, p, re.I)],
                "la tabla de «%s»" % tema, ES),
            "tabla_revista": _uno(
                [n for n, p in pr.items() if re.search(pie, p, re.I)],
                "la tabla de «%s»" % tema, REVISTA),
            "seccion_maestro": _uno(
                [n for n, t in am if n and re.search(titulo, t, re.I)],
                "el apartado de resultados de «%s»" % tema, ES),
            "apartado_revista": _uno(
                [t for _, t in ar if re.search(titulo, t, re.I)],
                "el apartado de resultados de «%s»" % tema, REVISTA),
            "capitulo_revista": cap_r,
        }
    return out


def comprueba_ingles(N):
    """La lista del inglés cita la sección y las tablas con los números del
    maestro (numeracion() solo lee el maestro y la revista). Si el inglés
    dejara de numerar igual, su lista mandaría a otra tabla sin que nada
    fallara: se comprueba sobre sus propios pies y encabezados."""
    t = EN.read_text(encoding="utf-8")
    pies = {int(m.group(1)): m.group(2) for m in
            re.finditer(r"(?m)^\*\*Table (\d+)\.\*\*\s*(.+)$", t)}
    for tema, patron in (("desenlaces", r"declared outcomes"),
                         ("embudo", r"surviving each requirement")):
        hallados = [n for n, p in pies.items() if re.search(patron, p, re.I)]
        if hallados != [N[tema]["tabla_maestro"]]:
            raise SystemExit("NO SE ESCRIBE: en %s la tabla de «%s» es %s y en "
                             "el maestro la %d" % (EN.name, tema, hallados,
                                                   N[tema]["tabla_maestro"]))
    sec = N["desenlaces"]["seccion_maestro"]
    if not re.search(r"(?mi)^### %s +.*outcome" % re.escape(sec), t):
        raise SystemExit("NO SE ESCRIBE: en %s la sección %s no es la de los "
                         "desenlaces, como en el maestro" % (EN.name, sec))


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
    citadas = [r["cita_del_texto"].strip() for r in filas
               if r["codigo"] not in sin_texto
               and r["cita_del_texto"].strip()
               and not r["cita_del_texto"].strip().startswith("(")]
    con = len(citadas)
    otros = sum(1 for r in filas if r["codigo"] not in sin_texto) - con
    # «Llevan la cita en que se apoya» se leía como una frase del artículo, y
    # no todas lo son: las fichas de registro del 2026-09-14 citan un campo de
    # la ficha («[eligibilityCriteria] ...») y EST-205 cita la indexación de
    # SciELO, sin el texto del artículo. Se cuentan sobre el mismo fichero.
    ficha = sum(1 for c in citadas if c.startswith("["))
    indexacion = sum(1 for c in citadas if c.startswith("SciELO"))
    nopdf = S["excluidos_texto_completo_NOPDF"]
    norec = S["excluidos_texto_completo_NOREC"]
    if (len(filas) != S["estudios_excluidos_tras_texto_completo"]
            or con + otros + nopdf + norec != len(filas)):
        raise SystemExit("S16: %d filas en %s, %d con cita + %d sin cita + %d "
                         "NOPDF + %d NOREC; el escalar dice %d. No cuadra."
                         % (len(filas), EXCLUSIONES.name, con, otros, nopdf,
                            norec, S["estudios_excluidos_tras_texto_completo"]))
    return {"s16_con_cita": con, "s16_sin_cita_otros": otros,
            "s16_cita_ficha": ficha, "s16_cita_indexacion": indexacion}


def de_las_citadas(e, en):
    """Cuántas de las citas de S16 no salen del artículo: la ficha del
    registro y la indexación de SciELO. Vacío si no hay ninguna. La usa
    también la guía del paquete."""
    partes = []
    if e["s16_cita_ficha"]:
        partes.append(("{s16_cita_ficha} quote the registry record" if en else
                       "{s16_cita_ficha} citan la ficha del registro"))
    if e["s16_cita_indexacion"]:
        partes.append(("{s16_cita_indexacion} the SciELO indexing" if en else
                       "{s16_cita_indexacion}, la indexación de SciELO"))
    if not partes:
        return ""
    y = " and " if en else " y "
    return ((" Of those with a quotation, " if en else
             " De las que llevan cita, ") + y.join(partes) + ".").format(**e)


_MESES_ES = ("enero", "febrero", "marzo", "abril", "mayo", "junio", "julio",
             "agosto", "septiembre", "octubre", "noviembre", "diciembre")
_MESES_EN = ("January", "February", "March", "April", "May", "June", "July",
             "August", "September", "October", "November", "December")


def _fechas(isos, en):
    """[«2026-09-01», «2026-09-02»] -> «del 1 y el 2 de septiembre de 2026» /
    «of 1 and 2 September 2026»."""
    def una(i, con_mes=True):
        a, m, d = (int(x) for x in i.split("-"))
        if not con_mes:
            return "%d" % d
        return ("%d %s %d" % (d, _MESES_EN[m - 1], a) if en else
                "%d de %s de %d" % (d, _MESES_ES[m - 1], a))
    isos = sorted(set(isos))
    mismo_mes = len({i[:7] for i in isos}) == 1
    trozos = [una(i, not mismo_mes or k == len(isos) - 1)
              for k, i in enumerate(isos)]
    if en:
        return "of " + (" and ".join(trozos) if len(trozos) < 3 else
                        ", ".join(trozos[:-1]) + " and " + trozos[-1])
    trozos = ["el " + t for t in trozos]
    texto = (" y ".join(trozos) if len(trozos) < 3 else
             ", ".join(trozos[:-1]) + " y " + trozos[-1])
    return "d" + texto  # «del 1 y el 2 ...»


def firmas_s16(e, en):
    """Quién decidió las exclusiones de S16, según la celda «decidido_por».

    La lista decía «quién firmó la exclusión», y 27 filas solo registran la
    orden de D.V. del 1 y el 2 de septiembre de 2026, sin que conste la firma
    de N.T. (registro de decisión del 2026-10-15). Las cifras van por escalar
    (exclusiones_*) y las fechas se leen del fichero del que sale S16; si el
    fichero y los escalares no cuentan lo mismo, se para."""
    with open(EXCLUSIONES, encoding="utf-8-sig", newline="") as fh:
        filas = list(csv.DictReader(fh))
    orden = [r for r in filas if "no consta firma" in r["decidido_por"].lower()]
    resto = [r for r in filas if r not in orden]
    dos = sum(1 for r in resto if " y " in r["decidido_por"])
    solo_dv = sum(1 for r in resto if " y " not in r["decidido_por"]
                  and "valdiviezo" in r["decidido_por"].lower())
    cuenta = {"exclusiones_firmadas_los_dos": dos,
              "exclusiones_firmadas_solo_dv": solo_dv,
              "exclusiones_orden_dv_sin_firma_nt": len(orden)}
    if (any(e.get(k) != v for k, v in cuenta.items())
            or sum(cuenta.values()) != len(filas)):
        raise SystemExit("S16: las firmas de %s (%r, %d filas) no cuadran con "
                         "los escalares exclusiones_*. No se escribe."
                         % (EXCLUSIONES.name, cuenta, len(filas)))
    f = _fechas([r["fecha"][:10] for r in orden], en) if orden else ""
    n2, n1, no = (e["exclusiones_firmadas_los_dos"],
                  e["exclusiones_firmadas_solo_dv"],
                  e["exclusiones_orden_dv_sin_firma_nt"])
    if en:
        partes = ["both authors signed %d" % n2]
        if n1:
            partes.append("D.V. alone signed %d" % n1)
        if no:
            partes.append("%d %s recorded on D.V.'s instruction %s with no "
                          "record of N.T.'s signature"
                          % (no, "were" if no != 1 else "was", f))
        y = ", and " if len(partes) > 2 else " and "
    else:
        partes = ["%d %s los dos autores" % (n2, "las firmaron" if n2 != 1
                                              else "la firmaron")]
        if n1:
            partes.append("%d %s D.V. solo" % (n1, "las firmó" if n1 != 1
                                                else "la firmó"))
        if no:
            partes.append("%d %s por orden de D.V. %s sin que conste la firma "
                          "de N.T." % (no, "se registraron" if no != 1
                                       else "se registró", f))
        y = " y "
    if len(partes) == 1:
        return partes[0]
    return ", ".join(partes[:-1]) + y + partes[-1]


def s21(e, en):
    """S21 y quién firmó sus veredictos. La usa también la guía del paquete.

    Decía «la frase firmada en que se apoya» de los 30 pares, y 2 (EST-108
    con EST-034 y con EST-044) los descartó la lectura del modelo del 22 de
    septiembre de 2026, sin firma: misma redacción que el cuerpo de los
    manuscritos, y sin la segunda frase si un día no queda ninguno."""
    fir, sin = e["pares_solapamiento_firmados"], e["pares_solapamiento_sin_firma"]
    if fir + sin != e["pares_solapamiento_examinados"]:
        raise SystemExit("S21: %d firmados + %d sin firma != %d examinados"
                         % (fir, sin, e["pares_solapamiento_examinados"]))
    if en:
        t = ("The {pares_solapamiento_examinados} pairs of studies that could "
             "describe the same patients, with the signal that flagged them, "
             "the verdict after reading both articles, the patients shared and "
             "the sentence it rests on. ")
        t += ("{pares_solapamiento_firmados} of the {pares_solapamiento_examinados} "
              "verdicts carry the signature of both authors; the other "
              + ("{pares_solapamiento_sin_firma}, rulings-out made by the model's "
                 "reading of 22 September 2026, are not recorded as signed."
                 if sin > 1 else
                 "one, a ruling-out made by the model's reading of 22 September "
                 "2026, is not recorded as signed.")
              if sin else "All verdicts carry the signature of both authors.")
    else:
        t = ("Los {pares_solapamiento_examinados} pares de estudios que podían "
             "describir a los mismos pacientes, con la señal que los marcó, el "
             "veredicto tras leer los dos artículos, los pacientes compartidos "
             "y la frase en que se apoya. ")
        t += ("{pares_solapamiento_firmados} de los "
              "{pares_solapamiento_examinados} veredictos llevan la firma de los "
              "dos autores; "
              + ("los otros {pares_solapamiento_sin_firma}, descartes que hizo "
                 "la lectura del modelo del 22 de septiembre de 2026, no constan "
                 "firmados." if sin > 1 else
                 "el otro, un descarte que hizo la lectura del modelo del 22 de "
                 "septiembre de 2026, no consta firmado.")
              if sin else "Todos los veredictos llevan la firma de los dos "
              "autores.")
    return t.format(**e)


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
    # Decía «quién firmó la exclusión» (en inglés, «who signed»), y 27 filas
    # solo registran la orden de D.V. sin firma de N.T.: ahora se dice quién
    # decidió cada una según el registro (firmas_s16).
    firmas = firmas_s16(e, en)
    firmas += "" if firmas.endswith(".") else "."
    if en:
        t = ("The {estudios_excluidos_tras_texto_completo} studies the screening "
             "admitted that were excluded afterwards, with their reason code and "
             "who decided each exclusion according to the record: "
             + firmas.replace("{", "{{").replace("}", "}}") +
             " {s16_con_cita} carry the quotation that "
             "supports it; the {excluidos_texto_completo_NOPDF} without the full "
             "article (NOPDF) and the {excluidos_texto_completo_NOREC} without "
             "readable text (NOREC) have nothing to quote")
        cola = ((", and {s16_sin_cita_otros} more carry no quotation."
                 if e["s16_sin_cita_otros"] > 1 else
                 ", and {s16_sin_cita_otros} more carries no quotation.")
                if e["s16_sin_cita_otros"] else ".")
        # OJO: lo de arriba es un ancla de check_manuscript_claims.py; el
        # desglose de las citas va DETRÁS, en frase aparte, para no partirla.
        return (t + cola).format(**e) + de_las_citadas(e, True)
    else:
        t = ("Los {estudios_excluidos_tras_texto_completo} estudios que el "
             "cribado admitió y que salieron después, con su código de motivo y "
             "quién decidió cada exclusión según el registro: "
             + firmas.replace("{", "{{").replace("}", "}}") +
             " {s16_con_cita} llevan la cita en que se "
             "apoya; los {excluidos_texto_completo_NOPDF} sin el artículo "
             "completo (NOPDF) y los {excluidos_texto_completo_NOREC} sin texto "
             "que se pudiera leer (NOREC) no tienen nada que citar")
        cola = ((", y {s16_sin_cita_otros} más van sin cita."
                 if e["s16_sin_cita_otros"] > 1 else
                 ", y {s16_sin_cita_otros} más va sin cita.")
                if e["s16_sin_cita_otros"] else ".")
        return (t + cola).format(**e) + de_las_citadas(e, False)


IDIOMA_CUERPO = ROOT / "quality_reports" / "idioma_cuerpo_pdf.csv"


def _a_mano():
    """Cuántos PDF marca comprueba_idioma_cuerpo.py en su columna
    mirar_a_mano, y por qué: (por la fracción de cirílico o CJK, por el idioma
    detectado). Se cuenta sobre el fichero del que sale S10; si un PDF se marca
    con el idioma en inglés o español, el motivo solo puede ser la fracción de
    caracteres (así lo decide ese guion), sin repetir aquí su umbral."""
    with open(IDIOMA_CUERPO, encoding="utf-8-sig", newline="") as fh:
        marcados = [r for r in csv.DictReader(fh) if r["mirar_a_mano"].strip()]
    por_idioma = sum(1 for r in marcados
                     if r["idioma_del_cuerpo"] not in ("eng", "spa"))
    return len(marcados) - por_idioma, por_idioma


def s10(e, en):
    """S10 tal como lo rehace build_verifiables_package.py desde
    quality_reports/idioma_cuerpo_pdf.csv.

    Decía «Verificación del idioma sobre el texto completo del PDF», y S10 era
    una copia del fichero del 13-ago-2026 (idioma_texto_completo.csv), anterior
    a la comprobación sobre el cuerpo del 6-oct-2026 y con estudios que ya no
    están en el corpus. Ahora describe la comprobación sobre el cuerpo, con
    las cifras de sus escalares; si no se comprobaron todos los estudios del
    corpus, la frase lo dice en vez de «cada uno».

    CORREGIDO EL 2026-10-14, sobre la redacción del 13: decía «sobre el texto
    del artículo, no [...] sobre el resumen», y comprueba_idioma_cuerpo.py lee
    el texto de TODO el PDF, resumen incluido; decía «el canal» sin decir que
    el guion lo escribió el modelo (S1 sí lo dice), y callaba los PDF que el
    propio guion marca para mirarlos a mano (EST-075: su primera página es un
    resumen en ruso). Ahora lo dice, con la cuenta sacada del fichero."""
    n, total = e["idioma_cuerpo_comprobados"], e["estudios"]
    reparto = [(e["idioma_cuerpo_ingles"], "in English", "en inglés"),
               (e["idioma_cuerpo_espanol"], "in Spanish", "en español"),
               (e["idioma_cuerpo_otro"], "in another language",
                "en otro idioma")]
    if sum(r[0] for r in reparto) != n:
        raise SystemExit("S10: inglés + español + otro no suman los %d "
                         "estudios comprobados sobre el cuerpo" % n)
    trozos = ["%d %s" % (k, ing if en else esp) for k, ing, esp in reparto if k]
    y = " and " if en else " y "
    lista = (", ".join(trozos[:-1]) + y + trozos[-1]) if len(trozos) > 1 \
        else (trozos[0] if trozos else "")
    por_letras, por_idioma = _a_mano()
    marcados = por_letras + por_idioma
    if en:
        quienes = ("each of the %d studies in the corpus" % n if n == total
                   else "%d of the %d studies in the corpus" % (n, total))
        motivos = [m for k, m in (
            (por_letras, "its share of Cyrillic or CJK characters"),
            (por_idioma, "a detected language other than English or Spanish"))
            if k]
        cola = ("." if not marcados else
                "; the mirar_a_mano ('check by hand') column flags %d PDF%s for "
                "page-by-page review because of %s."
                % (marcados, "" if marcados == 1 else "s", " or ".join(motivos)))
        return ("Language of the body of the PDF of %s: a mechanical detection "
                "over the text of the whole PDF, not over the metadata nor over "
                "the abstract alone, made by a pipeline script written by the "
                "language model, introduced on 6 October 2026 and redone on "
                "every run. It gives %s%s" % (quienes, lista, cola))
    quienes = ("cada uno de los %d estudios del corpus" % n if n == total
               else "%d de los %d estudios del corpus" % (n, total))
    motivos = [m for k, m in (
        (por_letras, "su fracción de caracteres cirílicos o CJK"),
        (por_idioma, "un idioma detectado distinto del inglés y el español"))
        if k]
    cola = ("." if not marcados else
            "; la columna mirar_a_mano marca %d PDF para %s página a página "
            "por %s." % (marcados, "revisarlo" if marcados == 1 else
                         "revisarlos", " o ".join(motivos)))
    return ("Idioma del cuerpo del PDF de %s: una detección mecánica sobre el "
            "texto de todo el PDF, no sobre los metadatos ni solo sobre el "
            "resumen, que hace un guion del canal escrito por el modelo de "
            "lenguaje, introducida el 6 de octubre de 2026 y rehecha en cada "
            "pasada. Da %s%s" % (quienes, lista, cola))


# (codigo, texto es, texto en). Los huecos {x} son escalares. Un texto puede
# ser también una función de los escalares cuando la frase cambia de forma
# según el estado, no solo de cifra (S10, S12, S16).
ANEXOS = [
    # S0 se presentaba como «Informe editorial» sin decir quién lo escribió.
    # Lo redactó el modelo de lenguaje haciendo de editor de revista (lo dice
    # el docstring de build_editorial_report.py) y la declaración de uso de IA
    # le atribuye la redacción de los anexos: un lector podía tomarlo por la
    # valoración de una persona.
    # Después se llamaba «Evaluación previa», y el fichero
    # «S0_informe_editorial.docx»; desde el 2026-10-15 es
    # S0_autoevaluacion_del_modelo.docx y la entrada lo dice igual.
    ("S0", "Autoevaluación del manuscrito que redactó el modelo de lenguaje "
           "(Claude Opus 5) desde el punto de vista de un editor de revista; no "
           "es un informe de un editor ni una revisión externa.",
     "Self-assessment of the manuscript drafted by the language model (Claude "
     "Opus 5) from the standpoint of a journal editor; it is not an editor's "
     "report or an external review."),
    ("S1", "Lista de comprobación PRISMA 2020.",
     "PRISMA 2020 checklist."),
    # Prometía «con fecha» por fuente y no la hay: la ejecución de Scopus cuya
    # exportación entró al corpus no tiene fecha registrada.
    ("S2", "Ecuaciones de búsqueda literales por fuente, con su número de "
           "resultados.",
     "Verbatim search strings by source, with their number of results."),
    # «Motivo codificado» no vale para todas las filas: las del primer día de
    # cribado, y algunas de la etapa de resumen, llevan el motivo en texto libre.
    # «Registro completo» era falso: la primera pasada del modelo, el 4-ago-2026
    # por la mañana sobre el brazo A de PubMed (screening_stage2_decisions.csv y
    # screening_stage3_decisions.csv), no está en S3, que lleva el cribado
    # vigente. Y «cuándo» no vale para las 77 filas de resumen heredadas de esa
    # pasada, que llevan la hora en que se heredaron: lo que hay es su marca de
    # tiempo. Redacción de la hoja de hechos del 13-oct.
    ("S3", "Las decisiones del cribado vigente, en dos ficheros: etapa 2 "
           "(título) y etapa 3 (resumen), cada una con su motivo, quién la "
           "emitió y su marca de tiempo. La primera pasada del 4 de agosto de "
           "2026 sobre el brazo A de PubMed, que el cribado del pozo sustituyó, "
           "consta en el repositorio y no en S3.",
     "The decisions of the screening in force, in two files: stage 2 (title) "
     "and stage 3 (abstract), each with its reason, who issued it and its "
     "timestamp. The first pass of 4 August 2026 over arm A of PubMed, which "
     "the pool screening replaced, is kept in the repository and not in S3."),
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
    # Decía «qué se intentó por cada estudio y con qué resultado», y S8 no es
    # eso: es fulltext_identifiers.csv (resolve_fulltext_ids.py, agosto de
    # 2026), una fila por INFORME que pasó a texto completo sin DOI editorial,
    # PMID ni NCT, con el identificador resuelto y la vía para buscarlo. No
    # registra los intentos de descarga ni su resultado; lo que no se consiguió
    # salió con NOPDF y está en S16.
    ("S8", "Vía de recuperación resuelta en agosto de 2026 para cada informe que "
           "pasó a texto completo sin DOI editorial, PMID ni NCT: el "
           "identificador del registro o el código de protocolo, el DOI "
           "localizado, el ensayo ya identificado del que es informe o la cita "
           "por la que buscarlo. No registra los intentos de descarga ni su "
           "resultado; los estudios que se quedaron sin el artículo completo "
           "están en S16 (NOPDF).",
     "Retrieval route resolved in August 2026 for each report that went to "
     "full text without an editorial DOI, PMID or NCT: the registry identifier "
     "or protocol code, the DOI located, the already identified trial it "
     "reports on, or the citation to search by. It does not record the "
     "download attempts or their outcome; the studies left without the full "
     "article are in S16 (NOPDF)."),
    ("S9", "Idioma por informe, con la clase de evidencia que aportaba.",
     "Language by report, with the class of evidence it provided."),
    ("S10", lambda e: s10(e, False), lambda e: s10(e, True)),
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
    # «La sección 3.5 y las tablas 5 y 6» iban tecleadas: ahora se leen del
    # maestro (numeracion()), en el que está esta lista.
    ("S14", "Extracción adjudicada: un valor por casilla, brazo a brazo, tras la "
            "adjudicación de los desacuerdos. Sostiene la sección "
            "{sec_desenlaces} y las tablas {tab_desenlaces} y {tab_embudo}.",
     "Adjudicated extraction: one value per cell, arm by arm, after the "
     "disagreements were adjudicated. Underpins section {sec_desenlaces} and "
     "Tables {tab_desenlaces} and {tab_embudo}."),
    # Etiquetaba «consenso» toda casilla adjudicada, la firmara una persona o
    # las dos. Son las etiquetas de S15 tras separar quién adjudicó.
    ("S15", "Procedencia de cada casilla de S14: acuerdo, adjudicada por los dos, "
            "adjudicada por uno, corregida contra el texto, una sola lectura o "
            "abierta.",
     "Provenance of every cell in S14: agreement, adjudicated by both "
     "reviewers, adjudicated by one, corrected against the text, single "
     "reading, or open."),
    ("S16", lambda e: s16(e, False), lambda e: s16(e, True)),
    ("S17", "La Tabla {tab_embudo} desglosada: los siete requisitos, brazo a "
            "brazo sobre los {desenlace_brazos} brazos, con el primero que falla "
            "y por qué.",
     "Table {tab_embudo} broken down: the seven requirements, arm by arm over "
     "the {desenlace_brazos} arms, with the first one that fails and why."),
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
    # Decía «la frase firmada en que se apoya» de los 30, y 2 (EST-108 con
    # EST-034 y con EST-044) los descartó la lectura del modelo del 22-sep sin
    # firma: misma redacción que el cuerpo de los manuscritos.
    ("S21", lambda e: s21(e, False), lambda e: s21(e, True)),
    ("S22", "Para cada variable de estratificación, cuántos estudios la declaran "
            "en el texto completo, cuántos la mencionan sin poder clasificarla, "
            "cuántos callan y de cuántos no hay texto.",
     "For each stratification variable, how many studies state it in the full "
     "text, how many mention it without allowing classification, how many are "
     "silent, and how many have no text at all."),
    # «Cómo se codificó» callaba quién: la conclusión la firmaron los autores
    # en texto libre y el valor categórico lo derivó el modelo
    # (ingest_lectura_firmada.py, columna clase_verificada_codificada).
    ("S23", "La clase de resistencia de los {lectura_clase_estudios_leidos} estudios que "
            "tenían texto completo, comprobada contra el antibiograma del artículo: la "
            "conclusión firmada, la frase o la tabla en que se apoya, cómo la "
            "codificó el modelo de lenguaje a partir de esa conclusión y qué "
            "cambió en la extracción.",
     "The resistance class of the {lectura_clase_estudios_leidos} studies that had full "
     "text, checked against the article's antibiogram: the signed conclusion, "
     "the sentence or table it rests on, how the language model coded it from "
     "that conclusion and what changed in the extraction."),
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
    N = numeracion()
    comprueba_ingles(N)
    esc = dict(S, desenlace_brazos=O["brazos"], **citas_s16(S),
               sec_desenlaces=N["desenlaces"]["seccion_maestro"],
               tab_desenlaces=N["desenlaces"]["tabla_maestro"],
               tab_embudo=N["embudo"]["tabla_maestro"])

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
