"""Genera en PDF los verificables de la doble extracción, y la guía del paquete.

QUÉ AÑADE Y POR QUÉ

El paquete cubría búsqueda, cribado, idioma y recuperación. La extracción por
duplicado no tenía verificable propio, y es la parte que un revisor mira con más
detalle: si dos personas leen los mismos artículos y no coinciden, la pregunta
inmediata es cuánto no coincidieron, en qué, y cómo se resolvió.

  S11  Concordancia entre las dos extracciones independientes, variable a
       variable, con la kappa donde es informativa y la advertencia donde no.
  S12  Cómo se resolvió cada desacuerdo: qué se resolvió por regla, qué se
       dirimió leyendo el artículo, y qué no se puede resolver todavía.
  S13  Las reglas de extracción de desenlaces, con la corrección documentada.
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


def desde_markdown(ruta, st, saltar_hasta=None):
    """Renderiza un .md del proyecto, opcionalmente desde un encabezado dado."""
    md = ruta.read_text(encoding="utf-8")
    if saltar_hasta:
        i = md.find(saltar_hasta)
        if i > 0:
            md = md[i:]
    fuera, lineas, i = [], md.split("\n"), 0
    while i < len(lineas):
        s = lineas[i].strip()
        if not s or (set(s) <= set("-") and len(s) > 2):
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
        elif s.startswith(("- ", "* ")):
            fuera.append(Paragraph(inline(s[2:], SIN_CITAS), st["lista"],
                                   bulletText="•"))
        elif s.startswith("> "):
            fuera.append(Paragraph(inline(s[2:], SIN_CITAS), st["nota"]))
        else:
            fuera.append(Paragraph(inline(s, SIN_CITAS), st["cuerpo"]))
        i += 1
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
    cuerpo = [Paragraph("S11. Concordancia entre las dos extracciones independientes",
                        st["titulo"])]
    cuerpo.append(Paragraph(
        "Los dos revisores extrajeron los mismos estudios por separado y sin verse. "
        "Este anexo es la medida de cuánto coincidieron, antes de resolver nada. Se "
        "reporta tal como salió, porque una concordancia alta declarada después de "
        "consensuar no mide nada.", st["cuerpo"]))
    cuerpo += desde_markdown(ACUERDO, st, saltar_hasta="| |")
    documento(dest, "S11 · Concordancia entre extractores").build(cuerpo)
    return dest


# ------------------------------------------------------------------- S12
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
    # declara; meterlas en el mismo saco que las 559 que los dos revisores
    # firmaron infla la cifra en dos y es justo lo que este anexo existe para
    # no hacer. El mismo corte que usa build_synthesis_scalars.
    SIN_FIRMA = "SIN firma conjunta"
    cerrados = [r for r in todos if (r.get("resolucion") or "").strip()]
    firmados = [r for r in cerrados
                if SIN_FIRMA not in (r.get("resuelto_por") or "")]
    por_regla = [r for r in cerrados if r not in firmados]
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

    c = [Paragraph("S12. C\u00f3mo se resuelve cada desacuerdo", st["titulo"])]
    c.append(Paragraph(
        "La comparaci\u00f3n de las dos extracciones independientes devolvi\u00f3 "
        "<b>%d desacuerdos</b>. Se reparten en %d de las %d filas de brazo "
        "comparadas, sobre %d estudios. "
        "De ellos, <b>%d est\u00e1n firmados por los dos revisores</b>, %d se cerraron "
        "por una regla y sin firma conjunta, y %d siguen pendientes. "
        "Este anexo dice d\u00f3nde est\u00e1 cada uno, con qu\u00e9 instrumento "
        "se resuelven y qu\u00e9 no se puede resolver todav\u00eda. El fichero completo, "
        "desacuerdo a desacuerdo, es "
        "<font face='Courier' size='8.5'>extraction_conflicts.csv</font>."
        % (len(todos), len({(r["study_id"], r["arm_id"]) for r in todos}),
           comparadas, len({r["study_id"] for r in todos}),
           len(firmados), len(por_regla), len(pend)),
        st["cuerpo"]))

    c.append(Paragraph("D\u00f3nde est\u00e1 cada desacuerdo", st["h1"]))
    c.append(cuadro(st, [
        ["Firmados por los dos revisores", str(len(firmados)),
         "Resueltos por consenso, con qui\u00e9n lo resolvi\u00f3 y cu\u00e1ndo"],
        ["Cerrados por regla, sin firma conjunta", str(len(por_regla)),
         "Ver m\u00e1s abajo. No cuentan como adjudicados"],
        ["Pendientes, con el art\u00edculo en mano", str(len(con_texto)),
         "En %d estudios cuyo texto completo est\u00e1 recuperado. Se dirimen "
         "abriendo el art\u00edculo" % len({r["study_id"] for r in con_texto})],
        ["Pendientes, sin texto completo", str(len(sin_texto)),
         "En %d estudios que no tenemos. No los resuelve nadie discutiendo: se "
         "resuelven consiguiendo el art\u00edculo"
         % len({r["study_id"] for r in sin_texto})],
    ], ["Situaci\u00f3n", "n", "Qu\u00e9 significa"],
        [6.2 * cm, 1.3 * cm, ANCHO - 7.5 * cm]))

    c.append(Paragraph("Con qu\u00e9 se resuelven", st["h1"]))
    c.append(Paragraph(
        "Los %d pendientes se trabajan sobre "
        "<font face='Courier' size='8.5'>ADJUDICACION_conflictos.xlsx</font>, que "
        "presenta el mismo contenido ordenado <b>por estudio</b> y no por variable: "
        "quien adjudica abre un art\u00edculo y resuelve todo lo suyo antes de pasar al "
        "siguiente, en vez de saltar de un PDF a otro. Cada fila muestra la pregunta "
        "literal que se le hizo al revisor junto a las dos respuestas, y las "
        "variables categ\u00f3ricas llevan desplegable con su vocabulario cerrado, de modo "
        "que el consenso no puede escribir un valor que el esquema no admite."
        % len(pend), st["cuerpo"]))
    c.append(Paragraph(
        "%d de los %d est\u00e1n marcados como prioritarios: son los campos que deciden "
        "si el art\u00edculo puede llegar a reportar desenlaces. El resto no cambia "
        "ninguna cifra de las que el manuscrito publica hoy."
        % (n_pri, len(pend)), st["cuerpo"]))
    c.append(Paragraph(
        "Las tres columnas que cierran cada fila \u2014valor acordado, qui\u00e9n lo resolvi\u00f3 y "
        "fecha\u2014 van vac\u00edas y las firman los dos revisores. El cuaderno no propone "
        "resoluciones: un documento que sugiere la respuesta y luego pide "
        "confirmarla no produce un consenso, produce un asentimiento.", st["nota"]))

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
    c.append(Paragraph(
        "Los %d desacuerdos cerrados sin firma conjunta est\u00e1n los dos en "
        "<font face='Courier' size='8.5'>journal_tier</font>, un metadato del "
        "registro bibliogr\u00e1fico que se comprueba fuera del art\u00edculo. <b>No son "
        "casillas en blanco:</b> los dos revisores rellenaron el campo y "
        "escribieron valores distintos (%s), y ambos se cerraron con el valor de "
        "la segunda revisora." % (len(por_regla), detalle), st["cuerpo"]))
    c.append(Paragraph(
        "Se cerraron aplicando una regla mec\u00e1nica \u2014casilla vac\u00eda en un metadato "
        "objetivo\u2014 sobre una comparaci\u00f3n que despu\u00e9s qued\u00f3 superada. Al rehacer "
        "la comparaci\u00f3n, la casilla dej\u00f3 de estar vac\u00eda y la regla dej\u00f3 de "
        "corresponder, pero la resoluci\u00f3n qued\u00f3 escrita. Constan aqu\u00ed como lo "
        "que son: <b>dos discrepancias de valor cerradas sin firma conjunta de "
        "los dos revisores</b>, pendientes de pasar por el mismo consenso que "
        "las dem\u00e1s. Ning\u00fan desacuerdo sobre el contenido de un art\u00edculo se ha "
        "resuelto por regla.", st["nota"]))

    c.append(Paragraph("Qu\u00e9 NO se resuelve por regla", st["h1"]))
    c.append(Paragraph(
        "Una casilla en blanco en un campo de desenlace no se rellena con el valor "
        "del otro revisor. El esquema de extracci\u00f3n distingue tres estados que no son "
        "intercambiables: vac\u00edo significa que no se contest\u00f3, <b>NA</b> que el art\u00edculo "
        "no lo notifica, y <b>0</b> que el art\u00edculo dice que fueron cero. Dar por bueno "
        "el n\u00famero del \u00fanico que contest\u00f3 convertir\u00eda la doble extracci\u00f3n en simple, "
        "que es justamente lo que este dise\u00f1o quiere evitar.", st["cuerpo"]))
    c.append(Paragraph(
        "Dos valores que parec\u00edan erratas tampoco se corrigieron solos: "
        "<font face='Courier' size='8.5'>'2 meses'</font> en d\u00edas de estancia es un "
        "problema de unidad, y <font face='Courier' size='8.5'>'Si'</font> en un campo "
        "que pide un recuento es una respuesta a otra pregunta. Ambos se enviaron a "
        "consenso y ambos motivaron cerrar el vocabulario del formulario.", st["cuerpo"]))

    c.append(Paragraph("Desacuerdos pendientes por variable", st["h1"]))
    porc = collections.Counter(r["campo"] for r in pend)
    c.append(cuadro(st, [[k, str(v), "S\u00ed" if k in PRIORITARIOS else ""]
                         for k, v in porc.most_common(14)],
                    ["Variable", "Pendientes", "Prioritaria"],
                    [ANCHO - 6.4 * cm, 3.2 * cm, 3.2 * cm]))
    c.append(Paragraph(
        "La lista completa de %d variables est\u00e1 en el fichero de conflictos; aqu\u00ed van "
        "las %d que m\u00e1s acumulan." % (len(porc), min(14, len(porc))), st["nota"]))

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
    siguen = sum(1 for r in hoja
                 if (r["study_id"], r["arm_id"], r["campo"]) in vivos)
    c.append(Paragraph(
        "<font face='Courier' size='8.5'>hoja_de_consenso.csv</font> conserva un "
        "triaje anterior de %d filas, con citas literales del art\u00edculo, su "
        "localizaci\u00f3n exacta y una segunda lectura encargada de refutar cada "
        "propuesta. Ese trabajo se hizo sobre una comparaci\u00f3n que despu\u00e9s qued\u00f3 "
        "superada: el comparador contaba como desacuerdo toda casilla que un revisor "
        "hab\u00eda rellenado y el otro no, y la segunda extracci\u00f3n a\u00fan estaba a medias. "
        "Hoy <b>%d de aquellas %d filas siguen siendo desacuerdos</b> y %d ya no lo "
        "son." % (len(hoja), siguen, len(hoja), len(hoja) - siguen), st["cuerpo"]))
    c.append(Paragraph(
        "El fichero se conserva porque el registro es solo-anexar y porque sus citas "
        "siguen sirviendo para adjudicar las filas que s\u00ed contin\u00faan abiertas. Lo que "
        "no es, es una tabla de resoluciones del conjunto actual, y este anexo no lo "
        "presenta como tal.", st["nota"]))

    documento(dest, "S12 \u00b7 Resoluci\u00f3n de conflictos").build(c)
    return dest


# ------------------------------------------------------------------- S13
def s13(st):
    dest = OUT / "S13_reglas_de_extraccion_de_desenlaces.pdf"
    c = [Paragraph("S13. Reglas de extracción de desenlaces", st["titulo"])]
    c.append(Paragraph(
        "La concordancia más baja de toda la extracción se dio en erradicación "
        "microbiológica. Al mirar los desacuerdos uno a uno, la causa no era el "
        "descuido de ningún revisor: era que el campo admitía dos lecturas legítimas. "
        "Este anexo documenta la regla que se fijó, la corrección que sufrió al "
        "probarla contra los artículos, y las dos columnas que hubo que añadir al "
        "formulario. Se incluye porque una definición de desenlace que cambia a mitad "
        "de una revisión es exactamente lo que un lector necesita poder auditar.",
        st["cuerpo"]))
    c += desde_markdown(REGLA_NUEVA, st, saltar_hasta="## Por qué hubo que corregirla")
    c.append(Paragraph("Antecedente: la versión que se corrigió", st["h1"]))
    c.append(Paragraph(
        "La primera versión de la regla, del 11 de agosto de 2026, se conserva íntegra "
        "en el repositorio del proyecto. Sus reglas sobre definición de éxito clínico y "
        "sobre la distinción entre casilla vacía, NA y cero siguen vigentes sin cambios; "
        "solo se corrigió la regla de erradicación. El registro de decisiones es "
        "solo-anexar: la corrección forma parte del rastro y no lo sustituye.",
        st["cuerpo"]))
    c += desde_markdown(REGLA_VIEJA, st, saltar_hasta="## Regla 2")
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
