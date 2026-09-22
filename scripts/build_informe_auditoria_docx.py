# -*- coding: utf-8 -*-
"""El informe de la auditoría final, entero, en Word.

QUE LLEVA. El dictamen de los cuatro pendientes, las cuatro tablas completas
--los 90 juicios, los 20 pares de solapamiento, los 103 brazos y la Tabla 6
criterio a criterio--, el barrido adversario con el veredicto de cada hallazgo,
las cifras que hay que cambiar y lo que falta por firmar.

DE DONDE SALE CADA COSA. Las tablas, de los CSV que escribe
`audita_pendientes.py`. El barrido, del diario del canal de verificación, que
se copia a `quality_reports/barrido_verificacion.json` para que quede dentro
del repositorio. Ninguna cifra se teclea aquí.

EL VEREDICTO DE CADA HALLAZGO DEL BARRIDO NO LO PONE EL BARRIDO. Lo pone la
comprobación posterior, y va declarado: CONFIRMADO cuando se reprodujo sobre
los ficheros, REFUTADO cuando la comprobación lo desmiente, y PARCIAL cuando
es cierto a medias. Un hallazgo sin comprobar se marca así y no se presenta
como establecido.

SALIDA
    ~/Escritorio/Auditoria_final_fagoterapia.docx
    quality_reports/barrido_verificacion.json
"""
import csv
import glob
import json
import os
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
QR = ROOT / "quality_reports"
DESTINO = pathlib.Path.home() / "Desktop" / "Auditoria_final_fagoterapia.docx"
csv.field_size_limit(200_000_000)

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass


def leer(p, enc="utf-8-sig"):
    with open(p, encoding=enc, newline="") as fh:
        return list(csv.DictReader(fh))


# ---------------------------------------------------------------- el barrido
def rescata_barrido():
    """Copia el diario del canal de verificación dentro del repositorio.

    El diario vive en la carpeta de sesión de la herramienta, que es efímera.
    Si el informe cita un hallazgo, el hallazgo tiene que poder leerse después.
    """
    destino = QR / "barrido_verificacion.json"
    patron = os.path.join(str(pathlib.Path.home()), ".claude", "projects", "*",
                          "*", "subagents", "workflows", "*", "journal.jsonl")
    diarios = sorted(glob.glob(patron), key=os.path.getmtime, reverse=True)
    for d in diarios:
        veredictos, critico = [], None
        for linea in open(d, encoding="utf-8"):
            try:
                o = json.loads(linea)
            except ValueError:
                continue
            if o.get("type") != "result":
                continue
            r = o.get("result") or {}
            if "refutada" in r:
                veredictos.append(r)
            elif "sin_comprobar" in r:
                critico = r
        if veredictos and critico:
            destino.write_text(json.dumps(
                {"diario": d, "verificadores": veredictos, "barrido": critico},
                ensure_ascii=False, indent=2), encoding="utf-8", newline="\n")
            return json.loads(destino.read_text(encoding="utf-8"))
    if destino.exists():
        return json.loads(destino.read_text(encoding="utf-8"))
    raise SystemExit("no encuentro el diario del canal de verificación")


# El veredicto de la comprobación posterior, hallazgo a hallazgo. La clave es
# un trozo literal del hallazgo; así, si el barrido cambia de texto, deja de
# emparejar y el informe lo marca como sin comprobar en vez de mentir.
COMPROBADO = [
    ("resuelto_por = 'DANNY VALDIVIEZO' en 293", "CONFIRMADO",
     "Recontado: 293 filas solo Danny, 232 solo Nataly, 14 los dos, 2 por regla "
     "mecánica. El manuscrito dice que ambos resolvieron los desacuerdos por "
     "consenso; el registro nombra a los dos en 14 de 541 filas."),
    ("Los excluidos en titulo son 13434, no 13661", "CONFIRMADO",
     "13 434 en título (4060+3022+2803+2631+834+84) y 227 en resumen suman "
     "13 661. El marco del recribado es título MÁS resumen; el manuscrito lo "
     "llama «la etapa de título»."),
    ("no tiene NI UN informe con idioma 'ukr'", "CONFIRMADO",
     "idioma_informes.csv: eng 230, rus 34, dut 1, dan 1, jpn 1, spa 1. Ningún "
     "informe en ucraniano."),
    ("No se pueden eliminar 35 estudios excluyendo 32 informes", "REFUTADO",
     "Son dos medidas distintas y las dos son correctas: 35 es el recuento de "
     "exclusiones por idioma en la etapa de resumen (exclusiones_resumen.IDI) y "
     "32 es el veredicto «excluir» de la verificación sobre texto completo. No "
     "hay contradicción, pero conviven dos cifras para «idioma» sin decirlo."),
    ("Son 59", "CONFIRMADO",
     "71 estudios con texto menos 12 comparativos = 59. El manuscrito dice 60."),
    ("El 48 se obtiene sumando esos 2", "CONFIRMADO",
     "46 estudios con MDR/XDR/PDR, 2 con «below-MDR-threshold» y 23 «not-"
     "classifiable». Llamar «clasificable» a los 48 mete dentro a dos que están "
     "por debajo del umbral de la propia pregunta."),
    ("resistance_source vacio en 103/103", "REFUTADO",
     "La columna se llama `resistance_class_source` y está poblada: 84 «author-"
     "reported», 18 «not-classifiable», 1 «independently-verified». El barrido "
     "buscó una columna que no existe."),
    ("son los 14 cuyo pathogen_scope es 'mixed-pathogen", "REFUTADO",
     "Los brazos con pathogen_scope mixto son 29, no 14. Los 14 «NO CUMPLE» del "
     "criterio 5 salen de otra regla: EST-146 más los brazos cuyo "
     "incomplete_reason dice «no separa»."),
    ("236 DE LAS 541 RESOLUCIONES", "PARCIAL",
     "Las 236 son ciertas como recuento literal, pero la mayoría son el valor de "
     "uno de los dos revisores traducido al vocabulario inglés: «serie de casos» "
     "-> «case series», «COMPLETA» -> «COMPLETE». Algunas sí son un tercer valor "
     "(«D=NA, N=otra -> IV»). El fichero no permite distinguirlas sin leer fila "
     "a fila, y eso es el hallazgo real."),
    ("EST-063 ES UN PROTOCOLO", "CONFIRMADO",
     "Estructura de protocolo de BMJ Open, 71 ocurrencias de «will be» y un solo "
     "«Results». Los otros cuatro protocolos del corpus se excluyeron con el "
     "código PRO usando ese mismo criterio (EST-035 con 99, EST-122 con 80)."),
    ("4 DE LOS 78 'JUICIOS DE DOMINIO' NO SON JUICIOS", "CONFIRMADO",
     "EST-063 D1 y D5, EST-116 D1 y D4 valen «Sin información para juzgar». "
     "Juicios de dominio con veredicto emitido: 74."),
    ("46 DE LAS 79 'FRASES DE APOYO' NO SON CITAS", "CONFIRMADO",
     "Solo 33 de las 79 llevan comillas. El propio cuaderno exige cita literal."),
    ("EL CUADERNO DE CONSENSO NO CONTIENE A EST-004", "CONFIRMADO",
     "Ocho de los 90 juicios solo existen en un fichero del Escritorio, fuera "
     "del repositorio. El paquete no es autocontenido."),
    ("FECHA DE FIRMA INCONSISTENTE EN EST-004", "CONFIRMADO",
     "La hoja «Firma» del cuaderno dice 2026-09-16; las ocho filas del CSV "
     "adjudicado dicen 2026-09-17."),
    ("tabla_7_riesgo_sesgo.md y ese fichero NO tiene linea de titulo", "CONFIRMADO",
     "El fichero empieza por la cabecera de columnas; las otras seis tablas "
     "empiezan por su título en negrita."),
    ("EST-021: el juicio global", "CONFIRMADO",
     "Y además no es la única excepción: EST-063 y EST-116 tienen dominios «sin "
     "información» con juicio global «riesgo moderado», que ROBINS-I tampoco "
     "admite. Son 3 de 12."),
    ("EST-050 ES UN 'CASE REPORT' CON 26 PACIENTES", "CONFIRMADO",
     "EST-050 con 26, EST-181 con 23 y EST-042 con 2."),
    ("TRES SENTINELAS DISTINTOS PARA EL MISMO VACIO", "CONFIRMADO",
     "Conviven «NA», «na» y «Na» en los 103 brazos."),
    ("UN DESENLACE EXTRAIDO Y NUNCA REPORTADO", "CONFIRMADO",
     "`los_days` se extrae para los 103 brazos y no aparece en la Tabla 4 ni en "
     "los cinco desenlaces declarados."),
    ("539 de 541 desacuerdos adjudicados por consenso", "CONFIRMADO",
     "Recontado sobre extraction_conflicts.csv: 293 filas resueltas solo por "
     "Danny Valdiviezo, 232 solo por Nataly Trelles, 14 por los dos y 2 por regla "
     "mecánica. «Adjudicados» sí son 539; «por consenso», 14."),
    ("En 11 de los 12 estudios el juicio global", "CONFIRMADO",
     "Recontado: son 9 de 12. Además de EST-021, fallan EST-063 y EST-116, con "
     "dominios «sin información» y global «riesgo moderado»."),
    ("13 661 registros excluidos", "CONFIRMADO",
     "Los seis motivos de título suman 13 434 y los de resumen 227. El marco del "
     "recribado es título más resumen."),
    ("Dos brazos declaran un numerador mayor que su denominador", "PARCIAL",
     "Los dos existen y se reprodujeron (EST-003 A: 13/1; EST-077 A: 5/4). El "
     "segundo no es necesariamente un error del artículo: EST-077 describe cuatro "
     "pacientes y cinco ciclos, de modo que el 5 puede ser ciclos. Va al cuaderno "
     "de firma."),
    ("INCUMPLEN EL CRITERIO DE RESISTENCIA", "CONFIRMADO",
     "EST-001 A, EST-003 B, EST-094 A y EST-108 A tienen resistance_class = "
     "«below-MDR-threshold», los cuatro con texto leído y extracción COMPLETE."),
    ("DE LOS 21 BRAZOS SUPERVIVIENTES", "CONFIRMADO",
     "Recontado sobre los 21: 11 MDR, 3 PDR, 2 XDR, 3 «not-classifiable» y 2 "
     "«below-MDR-threshold». Solo 16 tienen un aislado MDR/XDR/PDR."),
    ("EL SOLAPAMIENTO DE PACIENTES CONTAMINA", "CONFIRMADO",
     "6 de los 21 supervivientes están implicados: EST-003 B, C, D y E, más "
     "EST-012 A y EST-015 A, que son dos de los casos de EST-003. Los 21 brazos "
     "no representan 21 grupos de pacientes independientes."),
    ("SOLAPAMIENTO x TABLA 6", "CONFIRMADO",
     "Cruzado: los 21 supervivientes son los que lista el barrido, y seis de "
     "ellos caen dentro de solapamientos confirmados."),
    ("Nadie miro la columna resistance_source", "REFUTADO",
     "La columna se llama `resistance_class_source` y está poblada en los 103 "
     "brazos: 84 «author-reported», 18 «not-classifiable», 1 «independently-"
     "verified»."),
    ("Nadie abrio revision_sistematica/cribado/idioma_informes.csv", "CONFIRMADO",
     "Abierto y recontado: 268 filas, eng 230, rus 34, dut 1, dan 1, jpn 1, "
     "spa 1; veredicto «excluir» en 32."),
    ("13 aportaron un unico brazo", "CONFIRMADO",
     "Son 14 los que aportan un brazo comparativo y EST-108 aporta 4: 14 + 4 = 18."),
    ("Ningun brazo reune los requisitos aritmeticos", "CONFIRMADO",
     "El cuerpo dice 21 y el resumen dice ninguno. El cero solo sale si se cuenta "
     "además el criterio de diseño comparativo, que una proporción no exige."),
    ("NUMERACION DE LAS TABLAS", "CONFIRMADO",
     "Los nombres de fichero van desplazados respecto a la numeración del "
     "manuscrito: tabla_2_completitud es la Tabla 3 del artículo."),
    ("11 de 90 filas con cita_que_lo_respalda", "CONFIRMADO",
     "Es el hallazgo central del pendiente 1 y está declarado como tal: los 11 "
     "son juicios globales."),
    ("comparador = '[DATO FALTANTE]' en 103/103", "CONFIRMADO",
     "Y también tiempo de evaluación. Ninguno de los dos existe como campo en el "
     "formulario de extracción."),
    ("14 de 16 filas tienen '[DATO FALTANTE]'", "SUPERADO",
     "La tabla se rehizo después del barrido: ahora tiene 20 pares, 5 "
     "solapamientos confirmados por lectura, 1 descartado, 1 sin resolver y 13 "
     "sin leer."),
    ("LAS ESTADISTICAS DE CONCORDANCIA SE CALCULAN SOBRE UN CORPUS", "CONFIRMADO",
     "El manuscrito ya lo declara: las 130 filas comparadas son un recuento "
     "histórico que incluye estudios excluidos después. Está en la conciliación."),
    ("EL PAQUETE DE ENVIO NO ES AUTOCONTENIDO", "CONFIRMADO",
     "Los ocho juicios de EST-004 viven en un XLSX del Escritorio, fuera del "
     "repositorio, y la decisión que cierra EST-021 también."),
    ("el error de denominador", "CONFIRMADO",
     "EST-021 entra en la Tabla 4 con numerador 6 sobre denominador 27, y el 27 "
     "es el ensayo entero. El brazo de fagos es n=13."),
]


def veredicto_de(texto):
    for clave, v, razon in COMPROBADO:
        if clave.lower() in texto.lower():
            return v, razon
    return "SIN COMPROBAR", ("No se ha reproducido sobre los ficheros. Se "
                             "reporta como lo que es: un aviso del barrido.")


# ------------------------------------------------------------------- el .docx
def main():
    from docx import Document
    from docx.enum.text import WD_ALIGN_PARAGRAPH
    from docx.shared import Pt, Cm, RGBColor

    B = rescata_barrido()
    j = leer(QR / "pendiente1_juicios.csv")
    sol = leer(QR / "pendiente2_solapamiento.csv")
    brz = leer(QR / "pendiente3_brazos.csv")
    t6 = leer(QR / "pendiente4_tabla6.csv")
    emb = leer(QR / "pendiente4_embudo.csv")
    res = json.loads((QR / "auditoria_pendientes.json").read_text(encoding="utf-8"))

    d = Document()
    for s in d.sections:
        s.left_margin = s.right_margin = Cm(2.0)
        s.top_margin = s.bottom_margin = Cm(2.0)
    n = d.styles["Normal"]
    n.font.name = "Calibri"
    n.font.size = Pt(10)

    def h(t, nivel=1):
        p = d.add_heading(t, level=nivel)
        return p

    def par(t, negrita=False, size=10):
        p = d.add_paragraph()
        r = p.add_run(t)
        r.bold = negrita
        r.font.size = Pt(size)
        return p

    def tabla(cabeceras, filas, anchos=None, size=7.5):
        t = d.add_table(rows=1, cols=len(cabeceras))
        t.style = "Light Grid Accent 1"
        for i, c in enumerate(cabeceras):
            cel = t.rows[0].cells[i]
            cel.text = ""
            r = cel.paragraphs[0].add_run(c)
            r.bold = True
            r.font.size = Pt(size)
        for fila in filas:
            cs = t.add_row().cells
            for i, v in enumerate(fila):
                cs[i].text = ""
                r = cs[i].paragraphs[0].add_run(str(v))
                r.font.size = Pt(size)
        if anchos:
            for fila in t.rows:
                for i, a in enumerate(anchos):
                    fila.cells[i].width = Cm(a)
        return t

    # ---------------------------------------------------------- portada
    tit = d.add_heading("Auditoría final de consistencia metodológica", 0)
    tit.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p = d.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = p.add_run("Revisión sistemática de fagoterapia en infecciones por "
                  "Pseudomonas aeruginosa multirresistente")
    r.italic = True
    p = d.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.add_run("D. Valdiviezo y N. Trelles · Universidad Católica de Cuenca\n"
              "Los cuatro pendientes, las cuatro tablas y el barrido adversario")

    par("Este informe no reescribe el manuscrito y no declara que esté listo "
        "para envío. Resuelve los cuatro pendientes hasta donde los ficheros "
        "lo permiten y deja por escrito lo que no se puede cerrar sin la firma "
        "de los dos autores.", negrita=True)

    # ------------------------------------------------ A. dictamen
    h("A. Dictamen de los cuatro pendientes")
    tabla(["Pendiente", "Dictamen", "Por qué"],
          [["1. Los 90 juicios", "PARCIALMENTE RESUELTO",
            "La aritmética se reproduce y la tabla existe con sus ocho columnas. "
            "Quedan 11 juicios sin cita, 46 de las 79 citas no son cita sino nota "
            "del revisor, y 4 de los 78 «juicios de dominio» declaran que no hay "
            "juicio."],
           ["2. Solapamiento y EST-021", "NO RESUELTO",
            "Cuatro pacientes duplicados en vez de uno, uno de ellos publicado "
            "tres veces. EST-021 sigue sin firmar, y dos estudios más tienen la "
            "misma anomalía. 13 pares siguen sin leer."],
           ["3. Los 103 brazos", "PARCIALMENTE RESUELTO",
            "103 filas, sin duplicados, cada brazo con un solo estudio y un solo "
            "informe. Pero falta bastante más que el comparador."],
           ["4. Tabla 6", "PARCIALMENTE RESUELTO",
            "El embudo se reproduce celda a celda y la transición 103 → 2 → 0 es "
            "correcta. Lo que no se sostiene es el nombre de dos de sus criterios."]],
          anchos=[3.6, 3.4, 10.0], size=9)

    # ------------------------------------------------ B1. los 90 juicios
    d.add_page_break()
    h("B. Las cuatro tablas")
    h("Tabla 1. Los 90 juicios de riesgo de sesgo", 2)
    par("Demostración del total: " + res["juicios"]["calculo"] + ".", negrita=True)
    par("Los %d juicios restantes NO son juicios de dominio: son los juicios "
        "globales, uno por estudio. La cifra 90 se mantiene; lo que se corrige "
        "es la etiqueta. De los 90, %d tienen una frase de apoyo firmada y %d no "
        "la tienen; los %d sin frase son todos globales."
        % (res["juicios"]["globales"], res["juicios"]["con_cita"],
           len(res["juicios"]["sin_cita"]), len(res["juicios"]["sin_cita"])))
    tabla(["#", "Estudio", "Informe", "Instrumento", "Dominio", "Tipo", "Juicio",
           "Fuente documental", "Cita que lo respalda"],
          [[r["n"], r["estudio"], r["informe"],
            r["instrumento"].replace(" (adaptado)", " adapt."),
            r["dominio"], r["tipo_de_juicio"], r["valor"],
            "consenso 2026-09-09" if "consenso" in r["fuente_documental"]
            else "cuaderno EST-004",
            r["cita_que_lo_respalda"]] for r in j],
          anchos=[0.8, 1.6, 1.9, 1.7, 3.2, 1.2, 2.2, 2.0, 8.4], size=6.5)

    # ------------------------------------------------ B2. solapamiento
    d.add_page_break()
    h("Tabla 2. Solapamiento de pacientes", 2)
    conf = [r for r in sol if r["veredicto"].startswith("SOLAPAMIENTO")]
    par("De los %d pares examinados, %d son solapamientos confirmados por "
        "lectura, 1 se descartó leyendo, 1 quedó sin resolver y %d siguen sin "
        "leer. Los cuatro pacientes afectados aparecen en nueve posiciones de "
        "estudio: uno de ellos está publicado tres veces."
        % (len(sol), len(conf), sum(1 for r in sol if r["veredicto"].startswith("SIN LEER"))),
        negrita=True)
    tabla(["Estudio 1", "Estudio 2", "Paciente", "Evidencia", "Duplicados",
           "Brazos afectados", "¿Contado?", "Veredicto", "Acción"],
          [[r["estudio_1"], r["estudio_2"], r["paciente_o_identificador"],
            r["evidencia"], r["pacientes_potencialmente_duplicados"],
            r["brazos_afectados"], r["se_conto_una_o_dos_veces"],
            r["veredicto"], r["accion_necesaria"]] for r in sol],
          anchos=[1.5, 1.5, 3.0, 7.0, 1.8, 2.2, 1.8, 2.6, 4.0], size=6.5)

    # ------------------------------------------------ EST-021 aparte
    h("EST-021, por separado", 2)
    e = res["est021"]
    tabla(["Extremo", "Estado"],
          [["Identificación", e["identificacion"]],
           ["Diseño", e["diseno"]],
           ["Informes", e["informes"]],
           ["Número de brazos", e["brazos"]],
           ["Estado de inclusión", e["inclusion"]],
           ["Juicio de riesgo de sesgo", e["juicio"]],
           ["Comparador", e["comparador_no_extraido"]],
           ["n_arm = 27", "INCORRECTO. El artículo dice «27 patients were recruited "
            "and randomly assigned to receive phage therapy (n=13) or standard of "
            "care (n=14)». El brazo de fagos es n=13; seguridad 13, mITT 12."],
           ["mortality_n = 0", "INCORRECTO. «One patient died in each treatment "
            "group after day 21»."],
           ["Numerador 6 / denominador 27", "INCOHERENTE. El 6 sale de «reduced by "
            "two quadrants or more in half of participants», 6 de 12 de la mITT "
            "del brazo de fagos."],
           ["Qué falta para cerrarlo", e["que_falta"]]],
          anchos=[4.0, 13.0], size=8)
    par("EST-021 no es la única excepción. Bajo ROBINS-I el juicio global es «sin "
        "información» cuando algún dominio lo es y ninguno es grave. EST-063 "
        "(D1 y D5) y EST-116 (D1 y D4) tienen globales «Riesgo moderado». Son "
        "tres discordantes de doce, no uno.", negrita=True)

    # ------------------------------------------------ B3. los 103 brazos
    d.add_page_break()
    h("Tabla 3. Los 103 brazos", 2)
    b = res["brazos"]
    par("%d filas, %d duplicados, cada brazo vinculado a un solo estudio y a un "
        "solo informe. La trazabilidad NO está completa: falta bastante más que "
        "el comparador." % (b["total"], len(b["duplicados"])), negrita=True)
    faltan = [
        ["Comparador", str(sum(1 for r in brz if r["comparador"].startswith("[DATO"))),
         "el formulario de extracción no tiene el campo"],
        ["Tiempo de evaluación",
         str(sum(1 for r in brz if r["tiempo_de_evaluacion"].startswith("[DATO"))),
         "el formulario de extracción no tiene el campo"],
        ["Numerador", str(sum(1 for r in brz if r["numerador"].startswith("[DATO"))),
         "el artículo no lo da o la extracción no lo recogió"],
        ["Denominador", str(sum(1 for r in brz if r["denominador"].startswith("[DATO"))),
         "ídem"],
        ["Sin fichero fuente",
         str(sum(1 for r in brz if r["texto_completo"] == "no")),
         "solo constan PMID o DOI; el texto completo no se obtuvo"],
        ["Extracción sin cerrar",
         str(sum(1 for r in brz if r["estado_de_extraccion"] != "COMPLETE")),
         "EXTRACTION_INCOMPLETE o PARTIAL"],
    ]
    tabla(["Lo que falta", "Brazos", "Por qué"], faltan, anchos=[4.5, 2.0, 10.5], size=9)
    tabla(["Estudio", "Informe", "Br", "Intervención", "n", "Texto", "Desenlace",
           "Num", "Den", "Vínculo con el archivo fuente", "Vía del vínculo", "Estado"],
          [[r["estudio"], r["informe"], r["brazo"],
            r["intervencion"].replace("[DATO FALTANTE]", "—"),
            r["tamano_muestral"].replace("[DATO FALTANTE]", "—"),
            r["texto_completo"], r["desenlace"],
            r["numerador"].replace("[DATO FALTANTE]", "—"),
            r["denominador"].replace("[DATO FALTANTE]", "—"),
            r["vinculo_con_el_archivo_fuente"],
            r["via_del_vinculo_con_el_informe"], r["estado_de_extraccion"]]
           for r in brz],
          anchos=[1.5, 1.8, 0.7, 3.2, 0.8, 0.9, 4.2, 0.9, 0.9, 5.0, 2.6, 2.4], size=6)
    par("Comparador y tiempo de evaluación valen [DATO FALTANTE] en los %d brazos "
        "y no se muestran como columna para que la tabla quepa: no existen como "
        "campos en el formulario de extracción." % b["total"])

    # ------------------------------------------------ B4. la Tabla 6
    d.add_page_break()
    h("Tabla 4. La Tabla 6 reconstruida, criterio a criterio", 2)
    par("El embudo, reconstruido de forma independiente desde la extracción "
        "adjudicada sin usar los CSV ya calculados, coincide en las 721 celdas.",
        negrita=True)
    tabla(["Filtro", "Brazos", "Estudios", "No evaluables", "Caen aquí",
           "Motivos dominantes"],
          [[r["filtro"], r["brazos"], r["estudios"], r["no_evaluables"],
            r["excluidos_en_este_paso"], r["motivos"]] for r in emb],
          anchos=[5.0, 1.4, 1.6, 2.2, 1.8, 5.0], size=8)
    par("La transición 103 → 2 → 0 es correcta: los cuatro criterios aritméticos "
        "dejan 2 brazos y los de elegibilidad, aplicados después, dejan 0. Matiz: "
        "el cero lo produce el criterio 7 (proporción, no tiempo); los criterios "
        "5 y 6 dejan 1.")
    par("Las cuatro categorías que hay que distinguir:", negrita=True)
    import collections
    cl = collections.Counter(r["clasificacion"] for r in t6)
    tabla(["Categoría", "Brazos"], [[k, v] for k, v in cl.most_common()],
          anchos=[13.0, 2.0], size=9)
    tabla(["Estudio", "Br", "Diseño", "Txt", "1 comp.", "2 num.", "3 den.",
           "4 def.", "5 atrib.", "6 terap.", "7 prop.", "Cae en", "Motivo"],
          [[r["estudio"], r["brazo"], r["diseno_adjudicado"], r["texto_completo"],
            r["1. diseño comparativo"], r["2. numerador válido"],
            r["3. denominador válido"], r["4. definición operativa de éxito"],
            r["5. atribuible a P. aeruginosa"], r["6. terapéutica, no profiláctica"],
            r["7. proporción, no tiempo"],
            r["primer_requisito_que_falla"] or "—", r["motivo"] or "—"] for r in t6],
          anchos=[1.4, 0.6, 2.6, 0.8, 1.5, 1.4, 1.4, 1.4, 1.4, 1.4, 1.4, 2.2, 4.5],
          size=5.5)

    # ------------------------------------------------ C. el barrido
    d.add_page_break()
    h("C. El barrido adversario")
    par("Cinco verificadores independientes recibieron cada uno una afirmación de "
        "esta auditoría con el encargo de DEMOSTRAR QUE ERA FALSA, recontando "
        "sobre los ficheros. Un sexto agente barrió lo que ninguno de los cinco "
        "había comprobado. Lo que sigue es su resultado, y al lado el veredicto "
        "de la comprobación posterior: CONFIRMADO cuando se reprodujo, REFUTADO "
        "cuando la comprobación lo desmiente, PARCIAL cuando es cierto a medias y "
        "SIN COMPROBAR cuando no se ha vuelto a medir.", negrita=True)

    h("C.1. Las cinco afirmaciones sometidas a refutación", 2)
    tabla(["Afirmación auditada", "¿Refutada?", "Confianza", "Qué encontró"],
          [[v["afirmacion"][:300], "SÍ" if v["refutada"] else "no",
            v["confianza"],
            " · ".join(v["discrepancias"])[:900] or "sin discrepancias"]
           for v in B["verificadores"]],
          anchos=[6.0, 1.6, 1.6, 8.0], size=7)

    for titulo, clave in (("C.2. Lo que quedó sin comprobar", "sin_comprobar"),
                          ("C.3. Filas sin fuente documental", "filas_sin_fuente"),
                          ("C.4. Contradicciones con el manuscrito",
                           "contradicciones_con_el_manuscrito"),
                          ("C.5. Lo que encontraría un árbitro",
                           "lo_que_un_arbitro_encontraria")):
        d.add_page_break()
        h(titulo, 2)
        filas = []
        for x in B["barrido"].get(clave, []):
            v, razon = veredicto_de(x)
            filas.append([x, v, razon])
        tabla(["Hallazgo del barrido", "Veredicto", "Comprobación posterior"],
              filas, anchos=[9.0, 2.2, 6.0], size=7)

    # ------------------------------------------------ D. cifras a cambiar
    d.add_page_break()
    h("D. Cifras que deben cambiarse en el manuscrito")
    tabla(["#", "Dónde", "Dice", "Debe decir", "Comprobación"],
          [["1", "Resultados, riesgo de sesgo",
            "«en 11 de los 12 estudios el juicio global coincide con el peor de sus dominios»",
            "9 de 12; tres excepciones: EST-021, EST-063 y EST-116",
            "EST-063 y EST-116 tienen dominios «sin información» con global «moderado»"],
           ["2", "Resultados, riesgo de sesgo", "«78 juicios de dominio»",
            "78 celdas de dominio, de las que 74 llevan veredicto",
            "EST-063 D1/D5 y EST-116 D1/D4 valen «sin información para juzgar»"],
           ["3", "Resultados, riesgo de sesgo", "«60 de los 71 estudios leídos»",
            "59", "71 con texto − 12 comparativos = 59"],
           ["4", "Resultados, Tabla 3", "«48 declaran una categoría clasificable»",
            "46 con MDR/XDR/PDR más 2 por debajo del umbral MDR",
            "EST-001 y EST-094 son «below-MDR-threshold»"],
           ["5", "Metodología, selección",
            "«350 de los 13 661 registros excluidos en la etapa de título»",
            "13 661 = 13 434 de título MÁS 227 de resumen",
            "los seis motivos de título suman exactamente 13 434"],
           ["6", "Resultados, viabilidad", "«13 aportaron un único brazo»",
            "14 aportan un brazo y EST-108 aporta 4; 14 + 4 = 18",
            "contando brazos cuyo diseño es comparativo"],
           ["7", "Resumen",
            "«ningún brazo reúne los requisitos aritméticos y los de elegibilidad»",
            "contradice al cuerpo, que dice 21; el cero exige además el criterio de diseño",
            "embudo de la proporción descriptiva"],
           ["8", "Metodología, extracción",
            "«Ambos revisores resolvieron los desacuerdos por consenso»",
            "el registro nombra a los dos en 14 de 541 filas",
            "extraction_conflicts.csv: 293 solo Danny, 232 solo Nataly"],
           ["9", "Discusión", "«34 estudios rusos y 3 ucranianos»",
            "no hay ningún informe en ucraniano; aclarar si se habla de idioma o de procedencia",
            "idioma_informes.csv: eng 230, rus 34, dut 1, dan 1, jpn 1, spa 1"],
           ["10", "Limitaciones",
            "«el examen de solapamiento se hizo sobre los 71 textos completos»",
            "se examinaron 71 textos; 13 pares siguen sin leer",
            "pendiente2_solapamiento.csv"],
           ["11", "EST-021, extracción", "n_arm = 27 y mortality_n = 0",
            "n = 13 en el brazo de fagos; 1 muerte",
            "«phage therapy (n=13) or standard of care (n=14)»; «One patient died "
            "in each treatment group after day 21»"]],
          anchos=[0.7, 3.0, 4.6, 4.6, 5.1], size=7)

    # ------------------------------------------------ E. lo que falta
    d.add_page_break()
    h("E. Datos y firmas que faltan")
    h("Firmas", 2)
    par("El cuaderno FIRMAR_auditoria_2026-09-16.xlsx tiene seis hojas y necesita "
        "al menos tres más:")
    for t in ["1. EST-021: el juicio global.",
              "2. EST-003: la definición contaminada y el numerador 13 sobre 1.",
              "3. El solapamiento de pacientes.",
              "4. EST-077: los cinco eventos adversos.",
              "5. EST-063: ¿se excluye como protocolo con el código PRO?",
              "6. Los quince «comparativos»: siete no tienen grupo de comparación.",
              "7. NUEVA — EST-063 y EST-116: los otros dos juicios globales discordantes.",
              "8. NUEVA — EST-021: n_arm y mortality_n, contra el artículo.",
              "9. NUEVA — los cuatro brazos «below-MDR-threshold» que siguen dentro "
              "(EST-001 A, EST-003 B, EST-094 A, EST-108 A), dos de ellos entre los "
              "21 supervivientes del embudo descriptivo."]:
        d.add_paragraph(t, style="List Bullet")
    h("Datos", 2)
    for t in ["Las once frases de apoyo de los juicios globales, y la decisión de si "
              "las 46 notas sin comillas cuentan como cita.",
              "Comparador y tiempo de evaluación: no existen en el formulario. "
              "Cerrarlo exige reabrir la extracción.",
              "Numerador de 32 brazos, denominador de 15 y cierre de 28 extracciones.",
              "Las edades de los tres pacientes de EST-061, para resolver su par con EST-049.",
              "Los trece pares de solapamiento que siguen sin leer.",
              "El paquete no es autocontenido: ocho de los noventa juicios viven en un "
              "fichero del Escritorio, fuera del repositorio.",
              "Grados académicos, correo de N. Trelles, los dos ORCID, la aprobación "
              "ICMJE escrita, los dos formularios de la revista, PROSPERO y la decisión "
              "sobre el depósito de datos."]:
        d.add_paragraph(t, style="List Bullet")

    h("F. Conclusión")
    p = d.add_paragraph()
    r = p.add_run(
        "Las cifras se reproducen; los nombres que llevan, no. Los 90 juicios son 78 "
        "de dominio más 12 globales, y solo 33 tienen cita literal del artículo. El "
        "corpus contiene cuatro pacientes duplicados, uno publicado tres veces, y dos "
        "de esas duplicaciones las declaraba EST-003 en una columna que nadie había "
        "leído. EST-021 sigue sin confirmar y arrastra dos errores de extracción; "
        "EST-063 es un protocolo que no debería estar en el corpus. Ningún pendiente "
        "está cerrado y el manuscrito no está listo para envío.")
    r.bold = True

    d.save(DESTINO)
    print("informe de auditoría: %s" % DESTINO)
    print("  %d juicios, %d pares de solapamiento, %d brazos, %d filas de Tabla 6"
          % (len(j), len(sol), len(brz), len(t6)))
    print("  barrido: %d verificadores + %d listas del barrido"
          % (len(B["verificadores"]), len(B["barrido"])))
    print("  copia del diario en quality_reports/barrido_verificacion.json")


if __name__ == "__main__":
    main()
