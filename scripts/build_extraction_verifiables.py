"""Genera en PDF los verificables de la doble extracción, y la guía del paquete.

QUÉ AÑADE Y POR QUÉ

El paquete cubría búsqueda, cribado, idioma y recuperación. La extracción por
duplicado no tenía verificable propio, y es la parte que un revisor mira con más
detalle: si dos personas leen los mismos artículos y no coinciden, la pregunta
inmediata es cuánto no coincidieron, en qué, y cómo se resolvió.

  S11  Concordancia entre las dos extracciones, variable a
       variable, con la kappa donde es informativa y la advertencia donde no.
  S12  Cómo se resolvió cada desacuerdo: qué se cerró por regla, qué se
       adjudicó y a quién anota el registro como responsable, y --solo si
       los hay-- qué sigue pendiente.
  S13  Las reglas de extracción de desenlaces, con la corrección documentada
       y con quién las redactó y quién declara haberlas decidido.
  Guía Índice en lengua llana: qué contesta cada fichero.

Todo se calcula desde los ficheros del canal. Ninguna cifra se teclea aquí: si
la hoja de consenso cambia, estos PDF cambian al reejecutar.

Uso:
    python scripts/build_extraction_verifiables.py
"""
import csv
import collections
import json
import pathlib
import re
import sys

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.platypus import (BaseDocTemplate, Frame, PageTemplate,
                                Paragraph, Spacer, Table, TableStyle)

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from build_manuscript_pdf import estilos, inline, tabla_desde_md  # noqa: E402

ROOT = pathlib.Path(__file__).resolve().parent.parent
OUT = ROOT / "verificables revisión sistemática"
HOJA = ROOT / "revision_sistematica" / "extraccion" / "hoja_de_consenso.csv"
CONFLICTOS = ROOT / "revision_sistematica" / "extraccion" / "extraction_conflicts.csv"
PROCEDENCIA = (ROOT / "revision_sistematica" / "extraccion"
               / "extraccion_adjudicada_procedencia.csv")
OUTCOME = ROOT / "quality_reports" / "outcome_scalars.json"
ACUERDO = ROOT / "quality_reports" / "extraction_agreement.md"
ACUERDO_JSON = ROOT / "quality_reports" / "extraction_agreement.json"
REGLA_NUEVA = ROOT / "quality_reports" / "decisions" / "2026-08-12_erradicacion-regla-corregida.md"
REGLA_VIEJA = ROOT / "quality_reports" / "decisions" / "2026-08-11_definicion-erradicacion-y-exito.md"

ANCHO = A4[0] - 4.4 * cm

# Los campos que deciden si el articulo puede reportar desenlaces. Se toma
# del cuaderno de adjudicacion para que no existan dos listas que digan lo
# mismo y puedan divergir.
from build_adjudication_workbook import PRIORITARIOS  # noqa: E402
SIN_CITAS = lambda clave: 0          # noqa: E731  estos anexos no llevan citas

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass


def documento(destino, titulo_pie):
    doc = BaseDocTemplate(str(destino), pagesize=A4,
                          leftMargin=2.2 * cm, rightMargin=2.2 * cm,
                          topMargin=2.0 * cm, bottomMargin=1.8 * cm,
                          title=destino.stem, author="Valdiviezo D, Trelles N")
    marco = Frame(doc.leftMargin, doc.bottomMargin, doc.width, doc.height, id="n")

    def pie(canvas, d):
        canvas.saveState()
        canvas.setFont("Times-Roman", 8)
        canvas.setFillColor(colors.HexColor("#777777"))
        canvas.drawString(2.2 * cm, 1.1 * cm, titulo_pie)
        canvas.drawRightString(A4[0] - 2.2 * cm, 1.1 * cm, str(d.page))
        canvas.restoreState()

    doc.addPageTemplates([PageTemplate(id="n", frames=[marco], onPage=pie)])
    return doc


def desde_markdown(ruta, st, saltar_hasta=None, cortar_en=None, quitar=(),
                   cambios=()):
    """Renderiza un .md del proyecto, opcionalmente desde un encabezado dado
    y hasta otro.

    `quitar`: encabezados cuya seccion entera se omite, hasta el siguiente
    encabezado de su nivel o superior. `cambios`: pares (texto, sustituto) que
    se aplican antes de renderizar, sin que importen los saltos de linea del
    original. Si un texto no aparece se para: el registro cambio, y publicar
    el anexo con la mitad de las correcciones aplicadas seria peor que no
    publicarlo.

    Las lineas seguidas forman un solo parrafo. Antes cada linea del .md salia
    como un parrafo aparte, y una negrita que cruzaba un salto de linea salia
    con los asteriscos a la vista."""
    md = ruta.read_text(encoding="utf-8").replace("\r\n", "\n")
    if saltar_hasta:
        i = md.find(saltar_hasta)
        if i > 0:
            md = md[i:]
    if cortar_en:
        i = md.find(cortar_en)
        if i > 0:
            md = md[:i]
    for viejo, nuevo in cambios:
        patron = r"\s+".join(re.escape(p) for p in viejo.split())
        md, n = re.subn(patron, lambda m, n_=nuevo: n_, md)
        if not n:
            raise SystemExit("%s: no encuentro «%s». El registro cambió y la "
                             "corrección de este anexo ya no aplica; revísala."
                             % (ruta.name, viejo[:70]))
    lineas = md.split("\n")
    if quitar:
        quedan, saltando = [], None
        for ln in lineas:
            s = ln.strip()
            if s.startswith("#"):
                nivel = len(s) - len(s.lstrip("#"))
                if saltando is not None and nivel <= saltando:
                    saltando = None
                if saltando is None and s.startswith(tuple(quitar)):
                    saltando = nivel
            if saltando is None:
                quedan.append(ln)
        lineas = quedan

    def raya(s):
        return set(s) <= set("-") and len(s) > 2

    ESPECIAL = ("|", "#", "- ", "* ", ">")
    fuera, i = [], 0
    while i < len(lineas):
        s = lineas[i].strip()
        if not s or raya(s):
            i += 1
            continue
        if s.startswith("|"):
            bloque = []
            while i < len(lineas) and lineas[i].strip().startswith("|"):
                bloque.append(lineas[i])
                i += 1
            t = tabla_desde_md(bloque, st, SIN_CITAS, ANCHO)
            if t:
                fuera += [Spacer(1, 4), t, Spacer(1, 9)]
            continue
        if s.startswith("#"):
            n = len(s) - len(s.lstrip("#"))
            fuera.append(Paragraph(inline(s.lstrip("#").strip(), SIN_CITAS),
                                   st["h1" if n <= 2 else "h2"]))
            i += 1
            continue
        if s.startswith(">"):
            # Una cita sigue mientras sigan las lineas con «>»; una linea «>»
            # vacia separa parrafos dentro de ella.
            trozos = []
            while i < len(lineas) and lineas[i].strip().startswith(">"):
                t = lineas[i].strip()[1:].strip()
                if t:
                    trozos.append(t)
                elif trozos:
                    fuera.append(Paragraph(inline(" ".join(trozos), SIN_CITAS),
                                           st["nota"]))
                    trozos = []
                i += 1
            if trozos:
                fuera.append(Paragraph(inline(" ".join(trozos), SIN_CITAS),
                                       st["nota"]))
            continue
        if s.startswith(("- ", "* ")):
            # Un punto de lista sigue en las lineas sangradas que vienen debajo.
            texto, i = s[2:], i + 1
            while i < len(lineas):
                sig, ss = lineas[i], lineas[i].strip()
                if not ss or not sig[:1].isspace() or ss.startswith(ESPECIAL):
                    break
                texto, i = texto + " " + ss, i + 1
            fuera.append(Paragraph(inline(texto, SIN_CITAS), st["lista"],
                                   bulletText="•"))
            continue
        trozos, i = [s], i + 1
        while i < len(lineas):
            ss = lineas[i].strip()
            if not ss or raya(ss) or ss.startswith(ESPECIAL):
                break
            trozos, i = trozos + [ss], i + 1
        fuera.append(Paragraph(inline(" ".join(trozos), SIN_CITAS), st["cuerpo"]))
    return fuera


def cuadro(st, filas, cabecera, anchos):
    datos = [[Paragraph(inline(c, SIN_CITAS), st["celdah"]) for c in cabecera]]
    datos += [[Paragraph(inline(str(c), SIN_CITAS), st["celda"]) for c in f]
              for f in filas]
    t = Table(datos, colWidths=anchos, repeatRows=1, hAlign="LEFT")
    t.setStyle(TableStyle([
        ("LINEABOVE", (0, 0), (-1, 0), 0.9, colors.black),
        ("LINEBELOW", (0, 0), (-1, 0), 0.5, colors.black),
        ("LINEBELOW", (0, -1), (-1, -1), 0.9, colors.black),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("TOPPADDING", (0, 0), (-1, -1), 3.5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 3.5),
        ("LEFTPADDING", (0, 0), (-1, -1), 2),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1),
         [colors.white, colors.HexColor("#f6f6f4")]),
    ]))
    return t


# ------------------------------------------------------------------- S11
def s11(st):
    dest = OUT / "S11_concordancia_entre_extractores.pdf"
    S = json.loads((ROOT / "quality_reports" / "synthesis_scalars.json")
                   .read_text(encoding="utf-8"))
    cuerpo = [Paragraph("S11. Concordancia entre las dos extracciones",
                        st["titulo"])]
    # Decia «por separado y sin verse». No se sostiene: la columna de texto
    # libre que localiza cada dato es identica entre los dos cuadernos.
    cuerpo.append(Paragraph(
        "Los dos revisores extrajeron los mismos estudios, cada uno en su "
        "cuaderno. Este anexo mide cuánto coincidieron antes de resolver nada, y "
        "se reporta tal como salió. <b>No mide dos lecturas independientes:</b> "
        "la columna de texto libre que localiza cada dato coincide carácter por "
        "carácter entre los dos cuadernos en %d de las %d filas comparables, con "
        "la misma errata %d veces, en el cuaderno que el segundo revisor entregó "
        "el 26 de agosto de 2026; el 23 de agosto no coincidía en ninguna. Por "
        "eso estas cifras se leen como un máximo."
        % (S["extraccion_localizacion_identicas"],
           S["extraccion_localizacion_comparables"],
           S["extraccion_localizacion_errata_compartida"]), st["cuerpo"]))
    # La lista de tareas del final es del 31-ago, cuando no se habia
    # adjudicado nada, y no va en un anexo: describe trabajo ya hecho.
    cuerpo += desde_markdown(ACUERDO, st, saltar_hasta="| |",
                             cortar_en="## Qué hacer ahora")
    documento(dest, "S11 · Concordancia entre extractores").build(cuerpo)
    return dest


# ------------------------------------------------------------------- S12
def responsable(r):
    """Lo que anota la columna `resuelto_por`, con las iniciales.

    El mismo corte que build_auditoria_scalars: « Y » entre dos nombres son
    los dos; un nombre solo es un unico responsable. Lo que no encaja devuelve
    None y quien lo pida decide: este anexo no adivina quien firmo."""
    rp = (r.get("resuelto_por") or "").upper().strip()
    if " Y " in rp:
        return "los dos revisores"
    return {"DANNY VALDIVIEZO": "D.V.", "NATALY TRELLES": "N.T."}.get(rp)


def iniciales(columna):
    """`valor_Nataly_Trelles` -> «N.T.»: el nombre del revisor va en la
    columna y se descubre, no se teclea."""
    return "".join(p[0].upper() + "." for p in columna.split("_")[1:] if p)


def con_punto(frase):
    """Cierra la frase con punto, salvo que ya acabe en uno: una frase que
    termina en las iniciales de un revisor salia con dos («N.T..»)."""
    return frase if frase.endswith(".") else frase + "."


def s12(st):
    """Como se resuelve cada desacuerdo, con el estado de HOY.

    Este anexo se rehizo el 26 de agosto de 2026. La version anterior describia
    un triaje en tres bloques construido sobre una comparacion que despues
    quedo superada por dos motivos: el comparador contaba como desacuerdo toda
    casilla que un revisor habia rellenado y el otro no, y la segunda revisora
    aun no habia terminado. Presentar aquel reparto como si siguiera vigente
    seria describir un trabajo que ya no corresponde a los ficheros.
    """
    dest = OUT / "S12_resolucion_de_conflictos.pdf"
    todos = list(csv.DictReader(open(CONFLICTOS, encoding="utf-8")))
    comparadas = json.loads(ACUERDO_JSON.read_text(encoding="utf-8"))["filas_comparadas"]
    # Cerrado no es lo mismo que firmado. Dos filas de journal_tier se cerraron
    # por una regla mecanica sobre una comparacion superada y su procedencia lo
    # declara; meterlas en el mismo saco que las adjudicadas infla la cifra en
    # dos y es justo lo que este anexo existe para no hacer. Y adjudicado no es
    # firmado por los dos: el registro anota a uno solo en la mayoria. El mismo corte que usa build_synthesis_scalars.
    SIN_FIRMA = "SIN firma conjunta"
    cerrados = [r for r in todos if (r.get("resolucion") or "").strip()]
    firmados = [r for r in cerrados
                if SIN_FIRMA not in (r.get("resuelto_por") or "")]
    por_regla = [r for r in cerrados if r not in firmados]
    ambos = [r for r in firmados if " Y " in (r.get("resuelto_por") or "").upper()]
    uno = [r for r in firmados if r not in ambos]
    uno_dv = [r for r in uno if responsable(r) == "D.V."]
    uno_nt = [r for r in uno if responsable(r) == "N.T."]
    if len(uno_dv) + len(uno_nt) != len(uno):
        raise SystemExit(
            "S12: %d filas adjudicadas con un responsable que no es D.V., N.T. "
            "ni los dos. Revisa resuelto_por en %s antes de publicar el anexo."
            % (len(uno) - len(uno_dv) - len(uno_nt), CONFLICTOS.name))
    pend = [r for r in todos if not (r.get("resolucion") or "").strip()]
    estudios = {r["study_id"] for r in pend}
    n_pri = sum(1 for r in pend if r["campo"] in PRIORITARIOS)

    # Con el articulo en mano se resuelve leyendo; sin el, no se resuelve
    # discutiendo. La distincion la marca el listado de estudios, no una
    # etiqueta escrita a mano en la hoja de conflictos.
    # El nombre de S5 lleva el recuento dentro y lo calcula quien lo escribe
    # (build_verifiables_package.v5_listado). Teclear aqui el 184 hace que este
    # anexo reviente en cuanto el corpus cambie de tamano, justo en la
    # ejecucion en que mas falta hace que salga bien.
    s5f = sorted(OUT.glob("S5_listado_*_estudios.csv"))
    if not s5f:
        raise SystemExit("S12: no encuentro S5_listado_*_estudios.csv en %s. "
                         "Corre build_verifiables_package.py antes." % OUT.name)
    s5 = list(csv.DictReader(open(s5f[0], encoding="utf-8-sig")))
    tiene = {r["id"]: r["texto_completo"].strip().lower().startswith(("s", "y"))
             for r in s5}
    # Un estudio del fichero de conflictos puede no estar ya en S5 sin que nada
    # este roto: los desacuerdos se resolvieron sobre el corpus de 184, y el
    # 2026-09-01 salieron 22 estudios al leer sus textos completos. Eso NO es
    # un fallo de generacion, es historia. Lo que si seria un fallo es callarlo
    # o dar por hecho que esos estudios tienen texto completo.
    p_ex = ROOT / "revision_sistematica" / "cribado" / "exclusiones_tras_texto_completo.csv"
    salidos = ({r["study_id"] for r in csv.DictReader(open(p_ex, encoding="utf-8"))}
               if p_ex.exists() else set())
    faltan = [i for i in estudios if i not in tiene and i not in salidos]
    if faltan:
        raise SystemExit("S12: %d estudios del fichero de conflictos no estan "
                         "en S5 ni entre los excluidos al releer (%s). "
                         "Regenera S5 antes." % (len(faltan), faltan[:3]))
    fuera_del_corpus = sorted({i for i in estudios if i in salidos})
    # Los que salieron del corpus tenian texto completo --por eso se pudieron
    # desmentir-- asi que su desacuerdo era dirimible; lo que ya no procede es
    # dirimirlo.
    for i in fuera_del_corpus:
        tiene.setdefault(i, True)
    con_texto = [r for r in pend if tiene[r["study_id"]]]
    sin_texto = [r for r in pend if not tiene[r["study_id"]]]

    # Con todo adjudicado, el titulo en presente y las secciones de pendientes
    # describian un trabajo en curso que ya no existe: salian tablas vacias y
    # frases como \u00ab0 de los 0 estan marcados como prioritarios\u00bb. Lo que habla
    # de pendientes solo se escribe si los hay.
    c = [Paragraph("S12. C\u00f3mo se resuelve cada desacuerdo" if pend else
                   "S12. C\u00f3mo se adjudic\u00f3 cada desacuerdo", st["titulo"])]
    # Decia \u00abel registro anota a los dos revisores en %d y a uno solo en %d\u00bb.
    # Lo comprobado es lo que anota la columna resuelto_por, no quien decidio:
    # se dice asi, con el desglose por responsable.
    c.append(Paragraph(
        "La comparaci\u00f3n de las dos extracciones devolvi\u00f3 "
        "<b>%d desacuerdos</b>. Se reparten en %d de las %d filas de brazo "
        "comparadas, sobre %d estudios. "
        "De ellos, <b>%d est\u00e1n adjudicados</b>: el registro anota la firma de "
        "los dos revisores en %d y un \u00fanico responsable en %d (D.V. en %d, "
        "N.T. en %d). Otros %d se cerraron por una regla y sin firma conjunta%s. "
        "Este anexo dice d\u00f3nde est\u00e1 cada uno y con qu\u00e9 instrumento %s. El "
        "fichero completo, desacuerdo a desacuerdo, con el valor adjudicado, "
        "qui\u00e9n consta como responsable y la fecha, es "
        "<font face='Courier' size='8.5'>extraction_conflicts.csv</font>."
        % (len(todos), len({(r["study_id"], r["arm_id"]) for r in todos}),
           comparadas, len({r["study_id"] for r in todos}),
           len(firmados), len(ambos), len(uno), len(uno_dv), len(uno_nt),
           len(por_regla),
           (", y %d siguen pendientes" % len(pend)) if pend else
           ", y no queda ninguno pendiente",
           "se resuelven, y qu\u00e9 no se puede resolver todav\u00eda" if pend else
           "se adjudicaron"),
        st["cuerpo"]))

    c.append(Paragraph("D\u00f3nde est\u00e1 cada desacuerdo", st["h1"]))
    # La fila de los de un solo nombre decia \u00abAdjudicados por un solo revisor
    # ... No son un consenso\u00bb. Eso afirma mas de lo comprobado: que el registro
    # anote un nombre no prueba que no hubiera consenso, prueba que falta la
    # firma de los dos.
    situacion = [
        ["Adjudicados con la firma de los dos", str(len(ambos)),
         "El registro anota a los dos revisores, con la fecha. Solo estos "
         "constan como consenso"],
        ["Adjudicados con un \u00fanico responsable", str(len(uno)),
         "El registro anota un \u00fanico responsable, con la fecha: D.V. en %d y "
         "N.T. en %d" % (len(uno_dv), len(uno_nt))],
        ["Cerrados por regla, sin firma conjunta", str(len(por_regla)),
         "Ver m\u00e1s abajo. No cuentan como adjudicados"],
    ]
    if pend:
        situacion += [
            ["Pendientes, con el art\u00edculo en mano", str(len(con_texto)),
             "En %d estudios cuyo texto completo est\u00e1 recuperado. Se dirimen "
             "abriendo el art\u00edculo" % len({r["study_id"] for r in con_texto})],
            ["Pendientes, sin texto completo", str(len(sin_texto)),
             "En %d estudios sin texto completo recuperado. No los resuelve "
             "nadie discutiendo: se resuelven consiguiendo el art\u00edculo"
             % len({r["study_id"] for r in sin_texto})],
        ]
    c.append(cuadro(st, situacion, ["Situaci\u00f3n", "n", "Qu\u00e9 significa"],
                    [6.2 * cm, 1.3 * cm, ANCHO - 7.5 * cm]))

    c.append(Paragraph("Con qu\u00e9 se resuelven" if pend else
                       "Con qu\u00e9 se adjudicaron", st["h1"]))
    # Con todo adjudicado, «los 0 pendientes se trabajan» describe un trabajo
    # que ya no existe: se cuenta en pasado.
    c.append(Paragraph(
        ("Los %d pendientes se trabajan sobre " % len(pend) if pend else
         "Los desacuerdos se trabajaron sobre ") +
        "<font face='Courier' size='8.5'>ADJUDICACION_conflictos.xlsx</font>, que "
        "presenta el mismo contenido ordenado <b>por estudio</b> y no por variable: "
        "quien adjudica abre un art\u00edculo y resuelve todo lo suyo antes de pasar al "
        "siguiente, en vez de saltar de un PDF a otro. Cada fila muestra la pregunta "
        "literal que se le hizo al revisor junto a las dos respuestas, y las "
        "variables categ\u00f3ricas llevan desplegable con su vocabulario cerrado, de modo "
        "que quien adjudica no puede escribir un valor que el esquema no admite.",
        st["cuerpo"]))
    if pend:
        c.append(Paragraph(
            "%d de los %d est\u00e1n marcados como prioritarios: son los campos que deciden "
            "si el art\u00edculo puede llegar a reportar desenlaces. El resto no cambia "
            "ninguna cifra de las que el manuscrito publica hoy."
            % (n_pri, len(pend)), st["cuerpo"]))
    c.append(Paragraph(
        "Las tres columnas que cierran cada fila \u2014valor acordado, qui\u00e9n lo "
        "resolvi\u00f3 y fecha\u2014 iban vac\u00edas y deb\u00edan firmarlas los dos revisores; en "
        "el registro final, la columna de qui\u00e9n lo resolvi\u00f3 anota un \u00fanico "
        "responsable en %d de las %d filas adjudicadas. El cuaderno no propone "
        "resoluciones: un documento que sugiere la respuesta y luego pide "
        "confirmarla no produce un consenso, produce un asentimiento."
        % (len(uno), len(firmados)), st["nota"]))

    # Este parrafo decia que los desacuerdos firmados eran \u00abcasillas en blanco
    # resueltas con el valor del revisor que la cumplimento\u00bb. Es falso: en las
    # dos filas los dos revisores escribieron, y escribieron cosas distintas.
    # La regla R2 se aplico cuando la comparacion mostraba una casilla vacia; al
    # arreglar el comparador (ca12d6a) los valores cambiaron y la resolucion
    # quedo arrastrada. Ahora el texto se construye leyendo las filas, y la
    # guarda de abajo impide que vuelva a afirmar algo que el fichero no dice.
    c.append(Paragraph("Qu\u00e9 se cerr\u00f3 antes de la adjudicaci\u00f3n, y c\u00f3mo", st["h1"]))
    # Los nombres de las dos columnas de valor llevan dentro el nombre del
    # revisor, asi que se descubren en vez de teclearse.
    col_a, col_b = [k for k in todos[0] if k.startswith("valor_")]
    ambas_llenas = [r for r in por_regla
                    if (r[col_a] or "").strip() and (r[col_b] or "").strip()
                    and (r[col_a] or "").strip() != (r[col_b] or "").strip()]
    if por_regla and len(ambas_llenas) != len(por_regla):
        raise SystemExit(
            "S12: %d de %d filas cerradas por regla no son discrepancias de valor "
            "con las dos casillas llenas. El parrafo que describe como se cerraron "
            "ya no vale para esas filas; reescribelo antes de publicar el anexo."
            % (len(por_regla) - len(ambas_llenas), len(por_regla)))
    detalle = "; ".join(
        "%s %s, \u00ab%s\u00bb frente a \u00ab%s\u00bb, cerrado como \u00ab%s\u00bb"
        % (r["study_id"], r["campo"], r[col_a], r[col_b], r["resolucion"])
        for r in por_regla)
    # Decia \u00abcon el valor de la segunda revisora\u00bb: se calcula de quien era el
    # valor con que se cerro cada fila, y se nombra con las iniciales.
    de_quien = set()
    for r in por_regla:
        res = (r["resolucion"] or "").strip()
        if res == (r[col_b] or "").strip():
            de_quien.add(iniciales(col_b))
        elif res == (r[col_a] or "").strip():
            de_quien.add(iniciales(col_a))
        else:
            de_quien.add(None)
    if len(de_quien) == 1 and None not in de_quien:
        cierre = ("todos se cerraron con el valor que hab\u00eda escrito %s"
                  % de_quien.pop())
    else:
        cierre = "se cerraron con el valor indicado en cada caso"
    c.append(Paragraph(con_punto(
        "Los %d desacuerdos cerrados sin firma conjunta est\u00e1n en "
        "<font face='Courier' size='8.5'>journal_tier</font>, un metadato del "
        "registro bibliogr\u00e1fico que se comprueba fuera del art\u00edculo. <b>No son "
        "casillas en blanco:</b> los dos revisores rellenaron el campo y "
        "escribieron valores distintos (%s), y %s"
        % (len(por_regla), detalle, cierre)), st["cuerpo"]))
    # Decia \u00abpendientes de pasar por la misma adjudicacion que las demas\u00bb,
    # como trabajo por hacer. Lo que se puede afirmar es lo que hace el canal
    # con ellas, y se lee del fichero de procedencia en vez de suponerlo.
    proc = {(r["study_id"], r["arm_id"]): r
            for r in csv.DictReader(open(PROCEDENCIA, encoding="utf-8"))}
    abiertas = sum(1 for r in por_regla
                   if proc.get((r["study_id"], r["arm_id"]), {}).get(r["campo"]) == "ABIERTO")
    c.append(Paragraph(
        "Se cerraron aplicando una regla mec\u00e1nica \u2014casilla vac\u00eda en un metadato "
        "objetivo\u2014 sobre una comparaci\u00f3n que despu\u00e9s qued\u00f3 superada. Al rehacer "
        "la comparaci\u00f3n, la casilla dej\u00f3 de estar vac\u00eda y la regla dej\u00f3 de "
        "corresponder, pero la resoluci\u00f3n qued\u00f3 escrita. Constan aqu\u00ed como lo "
        "que son: <b>discrepancias de valor cerradas sin firma conjunta de "
        "los dos revisores</b>, que no pasaron por la adjudicaci\u00f3n de las "
        "dem\u00e1s%s. Ning\u00fan desacuerdo sobre el contenido de un art\u00edculo se ha "
        "resuelto por regla."
        % ("; por eso la extracci\u00f3n adjudicada (S14) no les da valor y su "
           "procedencia (S15) las marca como abiertas"
           if por_regla and abiertas == len(por_regla) else ""), st["nota"]))

    c.append(Paragraph("Qu\u00e9 NO se resuelve por regla", st["h1"]))
    c.append(Paragraph(
        "Una casilla en blanco en un campo de desenlace no se rellena con el valor "
        "del otro revisor. El esquema de extracci\u00f3n distingue tres estados que no son "
        "intercambiables: vac\u00edo significa que no se contest\u00f3, <b>NA</b> que el art\u00edculo "
        "no lo notifica, y <b>0</b> que el art\u00edculo dice que fueron cero. Dar por bueno "
        "el n\u00famero del \u00fanico que contest\u00f3 convertir\u00eda la doble extracci\u00f3n en simple, "
        "que es justamente lo que este dise\u00f1o quiere evitar.", st["cuerpo"]))
    # Decia \u00abAmbos se enviaron a consenso y ambos motivaron cerrar el
    # vocabulario del formulario\u00bb. Lo primero no se sostiene: el registro
    # anota, para cada uno, un valor adjudicado y un unico responsable. Lo
    # segundo no lo encontre documentado: el commit 774b50c (12-ago) solo los
    # senalaba como indicio de que el formulario admitia texto libre. Ahora la
    # frase se construye leyendo las filas y no afirma lo que no consta.
    def la_fila(campo, valor):
        return [r for r in todos if r["campo"] == campo
                and valor in {(r[col_a] or "").strip(), (r[col_b] or "").strip()}]
    casos = [("'2 meses'", "en d\u00edas de estancia es un problema de unidad",
              la_fila("los_days", "2 meses")),
             ("'Si'", "en un campo que pide un recuento es una respuesta a otra "
              "pregunta", la_fila("resistance_emergence_n", "Si"))]
    if any(len(f) != 1 for _, _, f in casos):
        raise SystemExit(
            "S12: los dos valores que parec\u00edan erratas ya no son una fila cada "
            "uno en %s; el p\u00e1rrafo que los describe no vale. Reescr\u00edbelo."
            % CONFLICTOS.name)
    def como_se_cerro(r):
        if not (r.get("resolucion") or "").strip():
            return "%s, todav\u00eda pendiente" % r["study_id"]
        quien = responsable(r)
        return ("%s se adjudic\u00f3 con el valor \u00ab%s\u00bb (%s)" % (
            r["study_id"], r["resolucion"],
            ("responsables en el registro: %s" % quien)
            if quien == "los dos revisores" else
            ("responsable en el registro: %s" % quien) if quien
            else "el registro no anota un responsable reconocible"))
    c.append(Paragraph(con_punto(
        "Dos valores que parec\u00edan erratas tampoco se corrigieron solos: "
        "<font face='Courier' size='8.5'>%s</font> %s, y "
        "<font face='Courier' size='8.5'>%s</font> %s. Ninguno se cerr\u00f3 por "
        "regla: %s, y %s"
        % (casos[0][0], casos[0][1], casos[1][0], casos[1][1],
           como_se_cerro(casos[0][2][0]), como_se_cerro(casos[1][2][0]))),
        st["cuerpo"]))

    # Con cero pendientes estas dos secciones eran una tabla vacia y un
    # \u00ab0 desacuerdos se concentran en 0 estudios\u00bb. Solo salen si hay algo.
    if pend:
        c.append(Paragraph("Desacuerdos pendientes por variable", st["h1"]))
        porc = collections.Counter(r["campo"] for r in pend)
        c.append(cuadro(st, [[k, str(v), "S\u00ed" if k in PRIORITARIOS else ""]
                             for k, v in porc.most_common(14)],
                        ["Variable", "Pendientes", "Prioritaria"],
                        [ANCHO - 6.4 * cm, 3.2 * cm, 3.2 * cm]))
        c.append(Paragraph(
            "La lista completa de %d variables est\u00e1 en el fichero de conflictos; aqu\u00ed van "
            "las %d que m\u00e1s acumulan." % (len(porc), min(14, len(porc))), st["nota"]))

    if sin_texto:
        c.append(Paragraph("Lo que todav\u00eda no se puede resolver", st["h1"]))
        sinart = collections.Counter(r["study_id"] for r in sin_texto)
        c.append(Paragraph(
            "%d desacuerdos se concentran en %d estudios sin texto completo recuperado. "
            "Ninguno se dirime leyendo, porque no hay qu\u00e9 leer. Figuran aqu\u00ed para que el "
            "lector pueda separar lo que queda por trabajar de lo que queda por conseguir."
            % (len(sin_texto), len(sinart)), st["cuerpo"]))
        c.append(cuadro(st, [[k, str(v)] for k, v in sinart.most_common()],
                        ["Estudio sin texto completo", "Desacuerdos"],
                        [ANCHO - 3.2 * cm, 3.2 * cm]))

    c.append(Paragraph("El rastro anterior, y por qu\u00e9 no se presenta como vigente",
                       st["h1"]))
    hoja = list(csv.DictReader(open(HOJA, encoding="utf-8")))
    vivos = {(r["study_id"], r["arm_id"], r["campo"]) for r in todos}
    # Este parrafo no decia quien hizo el triaje, y lo hizo el modelo: agentes
    # de Claude Opus 5 leyeron los PDF y propusieron cada valor con su cita
    # (commit 0ae7c94, 12-ago) y otros agentes del modelo intentaron refutar
    # esas propuestas (a4f451e y 0605278, 13-ago). Callarlo presentaba como
    # trabajo de los revisores lo que hizo el modelo. Los recuentos salen de
    # la columna `verificacion` de la propia hoja.
    #
    # Y decia que el 12-ago se repartieron en bloques todas las filas de la
    # hoja, todas sobre la comparacion superada. No es asi: el bloque D lo anadio el
    # modelo el 1-sep (bfd0935) con las correcciones de modalidad que propuso
    # tras leer los textos, y no sale de aquella comparacion. Se cuentan aparte.
    tardias = [r for r in hoja if r.get("bloque") == "D"]
    if any(r["campo"] != "modality" for r in tardias):
        raise SystemExit(
            "S12: el bloque D de %s ya no son solo correcciones de modalidad; "
            "el p\u00e1rrafo que lo describe no vale. Reescr\u00edbelo." % HOJA.name)
    del_12 = [r for r in hoja if r not in tardias]
    siguen = sum(1 for r in del_12
                 if (r["study_id"], r["arm_id"], r["campo"]) in vivos)
    propuestas = [r for r in del_12 if (r.get("resolucion_propuesta") or "").strip()]
    verificadas = [r for r in propuestas
                   if (r.get("verificacion") or "").startswith(("aguanta", "REFUTADA"))]
    refutadas = [r for r in verificadas
                 if (r.get("verificacion") or "").startswith("REFUTADA")]
    # Que las del bloque D las firmaron los dos se lee de la capa de
    # correcciones, no se supone.
    CORR = ROOT / "revision_sistematica" / "extraccion" / "correcciones_tras_texto_completo.csv"
    firmas = {(r["study_id"], r["arm_id"], r["campo"]):
              len([x for x in (r.get("firmado_por") or "").split(";") if x.strip()])
              for r in csv.DictReader(open(CORR, encoding="utf-8"))}
    d_dos = all(firmas.get((r["study_id"], r["arm_id"], r["campo"]), 0) > 1
                for r in tardias)
    c.append(Paragraph(
        "<font face='Courier' size='8.5'>hoja_de_consenso.csv</font> conserva un "
        "triaje de %d filas que <b>no hicieron los revisores sino el modelo de "
        "lenguaje (Claude Opus 5)</b>. El 12 de agosto de 2026 el modelo "
        "reparti\u00f3 en bloques %d desacuerdos y, para %d de ellos, agentes del "
        "modelo leyeron el art\u00edculo y propusieron una resoluci\u00f3n con su cita "
        "literal y su localizaci\u00f3n (commits 774b50c y 0ae7c94); una segunda "
        "lectura, tambi\u00e9n del modelo, intent\u00f3 refutar %d de esas propuestas y "
        "tumb\u00f3 %d. Ese trabajo se hizo sobre "
        "una comparaci\u00f3n que despu\u00e9s qued\u00f3 "
        "superada: el comparador contaba como desacuerdo toda casilla que un revisor "
        "hab\u00eda rellenado y el otro no, y la segunda extracci\u00f3n a\u00fan estaba a medias. "
        "Hoy <b>%d de aquellas %d filas figuran tambi\u00e9n en el registro de "
        "desacuerdos vigente</b> y %d ya no."
        % (len(hoja), len(del_12), len(propuestas), len(verificadas),
           len(refutadas), siguen, len(del_12), len(del_12) - siguen)
        + ((" Las otras %d filas (bloque D) las a\u00f1adi\u00f3 el modelo el 1 de "
            "septiembre de 2026: son las correcciones de modalidad que propuso, "
            "con su cita, tras leer los textos completos%s."
            % (len(tardias), ", y que despu\u00e9s firmaron los dos autores (S15 las "
               "marca como corregidas contra el texto)" if d_dos else ""))
           if tardias else ""), st["cuerpo"]))
    # Decia que las citas \u00absiguen sirviendo para adjudicar las filas que si
    # continuan abiertas\u00bb. Con cero abiertas eso describe un uso que ya no
    # existe; y el registro de adjudicacion no tiene columna que diga que se
    # consulto al adjudicar, asi que no se puede afirmar ni negar que esas
    # propuestas se usaran.
    c.append(Paragraph(
        ("El fichero se conserva porque el registro es solo-anexar y porque sus "
         "citas pueden servir para adjudicar las filas que siguen abiertas. "
         if pend else
         "El fichero se conserva porque el registro es solo-anexar. El registro "
         "de adjudicaci\u00f3n no anota qu\u00e9 se consult\u00f3 al adjudicar, as\u00ed que no "
         "consta si esas propuestas se tuvieron a la vista. ") +
        "No es una tabla de resoluciones del conjunto actual, y este anexo no "
        "lo presenta como tal.", st["nota"]))

    documento(dest, "S12 \u00b7 Resoluci\u00f3n de conflictos").build(c)
    return dest


# ------------------------------------------------------------------- S13
def s13(st):
    dest = OUT / "S13_reglas_de_extraccion_de_desenlaces.pdf"
    c = [Paragraph("S13. Reglas de extracción de desenlaces", st["titulo"])]
    # Este anexo no decia quien redacto las reglas ni quien las decidio, y
    # saltar_hasta se comia el «Estado» y la nota del 23-ago del registro. Las
    # redacto el modelo; que las decidieran los dos es una declaracion de D.V.
    # del 8-oct, que el propio registro anota sin respaldarla: no consta la
    # ratificacion por los dos. El estado y la nota se leen del
    # propio registro: si cambian, el anexo se para en vez de citar algo que ya
    # no dice.
    nuevo = REGLA_NUEVA.read_text(encoding="utf-8")
    estado = re.search(r"^\*\*Estado:\*\*\s*(.+?)\s*$", nuevo, re.M)
    if not estado or "PROPUESTA" not in estado.group(1):
        raise SystemExit("S13: el «Estado» de %s ya no es una propuesta; la nota "
                         "de autoría de este anexo no vale. Revísala." % REGLA_NUEVA.name)
    if "Esa confirmación no llegó" not in nuevo:
        raise SystemExit("S13: la nota del 23 de agosto de %s ya no dice que la "
                         "confirmación no llegó; la nota de autoría de este anexo "
                         "no vale. Revísala." % REGLA_NUEVA.name)
    c.append(Paragraph(
        "<b>Quién redactó estas reglas y quién las decidió.</b> Las reglas de "
        "extracción de desenlaces de este anexo, y la columna «Con la regla "
        "corregida» de la tabla que las aplica a las filas de erradicación que "
        "entonces se podían revisar contra el texto, las redactó el modelo de "
        "lenguaje (Claude Opus 5). Según declara D.V. (8 de octubre de 2026), las "
        "decidieron los dos autores. El registro del 12 de agosto de 2026 las dejó "
        "como «%s», y la nota del 23 de agosto de ese registro dice que esa "
        "confirmación no llegó. Lo que sigue reproduce los dos registros de "
        "decisión, del 11 y del 12 de agosto de 2026; se omiten sus listas de "
        "tareas, ya superadas, y se quitan los recuentos de aquellos días que hoy "
        "no valen. La declaración del "
        "uso del modelo en toda la revisión es la del manuscrito (Declaraciones, "
        "«Uso de inteligencia artificial»), que S7 reproduce."
        % estado.group(1).strip(), st["nota"]))
    # Decia «las dos columnas que hubo que añadir al formulario» y nada mas, y
    # el lector entendia que se habian extraido. No: se añadieron despues de
    # repartir los formularios y no llegaron a rellenarse. Se lee del canal.
    O = json.loads(OUTCOME.read_text(encoding="utf-8"))
    sin_extraer = O.get("campos_del_esquema_no_extraidos") or []
    c.append(Paragraph(
        "La concordancia más baja de toda la extracción se dio en erradicación "
        "microbiológica. Al mirar los desacuerdos uno a uno, la causa no era el "
        "descuido de ningún revisor: era que el campo admitía dos lecturas legítimas. "
        "Este anexo documenta la regla que se fijó, la corrección que sufrió al "
        "probarla contra los artículos, y las dos columnas que hubo que añadir al "
        "formulario%s. Se incluye porque una definición de desenlace que cambia a mitad "
        "de una revisión es exactamente lo que un lector necesita poder auditar."
        % ((" (%s, que se añadieron al esquema después de repartir los formularios "
            "y nunca llegaron a extraerse)"
            % " y ".join("<font face='Courier' size='8.5'>%s</font>" % x
                         for x in sin_extraer)) if sin_extraer else ""),
        st["cuerpo"]))
    # Arreglos sobre el borrador del modelo, que se reproducia tal cual:
    # «los cuatro artículos que sí tenemos» hablaba en primera persona y daba
    # una cifra del 12-ago como si fuera de hoy (hoy todo el corpus tiene el
    # articulo); «Con 107 estudios por extraer» y «los 16 ensayos aleatorizados
    # del corpus» eran tambien recuentos de aquel dia. Y se quita la seccion de
    # las filas sin texto completo: decia en presente que EST-003, -007, -013 y
    # -015 no tenian articulo --hoy estan en el corpus con el-- y terminaba en
    # una lista de articulos por conseguir.
    c += desde_markdown(
        REGLA_NUEVA, st, saltar_hasta="## Por qué hubo que corregirla",
        quitar=("## Las otras ocho filas siguen sin poder resolverse",),
        cambios=(
            ("aplicarla después contra los cuatro artículos que sí tenemos,",
             "aplicarla después contra los artículos que entonces se tenían,"),
            ("De las cuatro filas de erradicación que se pueden revisar contra el texto,",
             "De las cuatro filas de erradicación que entonces se podían revisar "
             "contra el texto,"),
            ("## Qué pasa con las cuatro filas que se pueden revisar",
             "## Qué pasa con las cuatro filas que entonces se podían revisar"),
            ("y en los 16 ensayos aleatorizados del corpus:",
             "y en los ensayos aleatorizados:"),
            ("Con 107 estudios por extraer, esa lista abierta",
             "Con la mayor parte de la extracción todavía por hacer, esa lista "
             "abierta"),
        ))
    c.append(Paragraph("Antecedente: la versión que se corrigió", st["h1"]))
    c.append(Paragraph(
        "La primera versión de la regla, del 11 de agosto de 2026, se conserva íntegra "
        "en el repositorio del proyecto. Sus reglas sobre definición de éxito clínico y "
        "sobre la distinción entre casilla vacía, NA y cero siguen vigentes sin cambios; "
        "solo se corrigió la regla de erradicación. El registro de decisiones es "
        "solo-anexar: la corrección forma parte del rastro y no lo sustituye.",
        st["cuerpo"]))
    # «Qué hacer con lo ya extraído» era la lista de tareas del 11-ago («media
    # hora entre los dos», «antes de seguir»): trabajo de aquel dia, no una
    # regla, y no va en un anexo.
    c += desde_markdown(REGLA_VIEJA, st, saltar_hasta="## Regla 2",
                        quitar=("## Qué hacer con lo ya extraído",))
    documento(dest, "S13 · Reglas de extracción de desenlaces").build(c)
    return dest


def main():
    st = estilos()
    OUT.mkdir(parents=True, exist_ok=True)
    for f in (s11, s12, s13):
        d = f(st)
        print(f"  {d.name:52} {d.stat().st_size // 1024} KB")


if __name__ == "__main__":
    main()
