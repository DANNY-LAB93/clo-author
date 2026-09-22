# -*- coding: utf-8 -*-
"""Los nueve hallazgos de la auditoría que hay que firmar.

POR QUE UN CUADERNO. Los nueve tocan datos ya firmados --la evaluación de
riesgo de sesgo y la extracción adjudicada-- y ninguno lo puede corregir un
script: son juicios de los autores. Aquí va cada uno con la prueba literal
delante, la pregunta concreta y la casilla para la respuesta.

LOS NUEVE

  1. EST-021. Juicio global «bajo riesgo» con un dominio en «algunas
     preocupaciones». RoB 2 no admite esa combinación.
  2. EST-003. Su definición de éxito describe el ensayo BX004-A y BX004-A no
     aparece en su artículo. Además `clinical_success_n` = 13 sobre n = 1.
  3. Solapamiento. Once pacientes en trece estudios; uno publicado tres
     veces. EST-108 declara que 27 de sus 100 casos ya estaban publicados
     y seis de esas referencias son estudios de este corpus.
  4. EST-077. `adverse_event_n` = 5 y el artículo no dice «adverse» ni una vez.
  5. EST-063. Es un protocolo de BMJ Open y los otros cuatro protocolos del
     corpus se excluyeron con el código PRO.
  6. Los quince «comparativos»: siete no tienen grupo de comparación según
     vuestras propias notas del dominio 1.
  7. EST-063 y EST-116. Dos dominios «sin información» cada uno y juicio global
     «riesgo moderado», que ROBINS-I tampoco admite.
  8. EST-021. `n_arm` = 27 es el ensayo entero y `mortality_n` = 0 contradice
     al artículo.
  9. EST-001 A y EST-094 A. Su único paciente está por debajo del umbral de
     multirresistencia, que es el criterio de población de la revisión.

EL SEGURO. Si alguna casilla de respuesta o de firma ya está rellenada, el
script NO escribe: preguntar dos veces es barato, borrar una firma no.

SALIDA
    ~/Escritorio/FIRMAR_auditoria_2026-09-16.xlsx
"""
import csv
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
RS = ROOT / "revision_sistematica"
QR = ROOT / "quality_reports"
CUADERNO = pathlib.Path.home() / "Desktop" / "FIRMAR_auditoria_2026-09-16.xlsx"
csv.field_size_limit(200_000_000)

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

RESPUESTAS = ("Vuestra decisión", "Por qué", "Frase en que os apoyáis",
              "Revisor 1 (nombre completo)", "Revisor 2 (nombre completo)",
              "Fecha (AAAA-MM-DD)", "¿Habéis leído los artículos citados en cada hoja?")


def leer(p, enc="utf-8"):
    with open(p, encoding=enc, newline="") as fh:
        return list(csv.DictReader(fh))


def ya_contestado():
    """Devuelve las casillas con contenido, para no pisarlas."""
    if not CUADERNO.exists():
        return []
    from openpyxl import load_workbook
    wb = load_workbook(CUADERNO, data_only=True)
    puestas = []
    for n in wb.sheetnames:
        for f in wb[n].iter_rows(values_only=True):
            if (f and f[0] in RESPUESTAS and len(f) > 1
                    and f[1] not in (None, "")):
                puestas.append("%s / %s" % (n, f[0]))
    return puestas


def solapamientos():
    """Los pares confirmados, leídos del fichero y no tecleados."""
    filas = leer(QR / "pendiente2_solapamiento.csv", enc="utf-8-sig")
    return [r for r in filas if r["veredicto"].startswith("SOLAPAMIENTO")]


def bajo_umbral():
    excl = {r["study_id"] for r in leer(RS / "cribado" / "exclusiones_tras_texto_completo.csv")}
    adj = [r for r in leer(RS / "extraccion" / "extraccion_adjudicada.csv")
           if r["study_id"] not in excl]
    por = {}
    for r in adj:
        por.setdefault(r["study_id"], []).append(r)
    solos, estratos = [], []
    for r in adj:
        if r["resistance_class"] != "below-MDR-threshold":
            continue
        otras = {x["resistance_class"] for x in por[r["study_id"]]}
        (estratos if otras & {"MDR", "XDR", "PDR"} else solos).append(r)
    return solos, estratos


def construye():
    conf = solapamientos()
    solos, estratos = bajo_umbral()

    H = []
    H.append(dict(
        clave="EST-021-GLOBAL",
        fuente_frase=["revision_sistematica/textos_completos/pdf/EST-021.pdf  (Jault, Lancet Infect Dis 2019)",
                     "o el manual de RoB 2 (Sterne BMJ 2019) si mantenéis el juicio y os apartáis de la regla"],
        titulo="EST-021 (PhagoBurn): el juicio global no cuadra con sus dominios",
        que_hay=[
            "D1 proceso de aleatorización ........ Bajo riesgo de sesgo",
            "D2 desviaciones de la intervención .. Algunas preocupaciones",
            "D3 datos de desenlace faltantes ..... Bajo riesgo de sesgo",
            "D4 medición del desenlace ........... Bajo riesgo de sesgo",
            "D5 selección del resultado .......... Bajo riesgo de sesgo",
            "GLOBAL .............................. Bajo riesgo de sesgo",
        ],
        problema=(
            "RoB 2 (Sterne 2019) define el juicio global de bajo riesgo como «the "
            "study is judged to be at low risk of bias for all domains». Con un "
            "dominio en «algunas preocupaciones», el global no puede ser bajo. "
            "OJO: no es la única excepción; ver la hoja 7."),
        pregunta="¿Qué hacemos con el juicio global de EST-021?",
        opciones=[
            "Corregirlo a «Algunas preocupaciones» (lo que da la regla del instrumento)",
            "Mantener «Bajo riesgo de sesgo» y declarar en Métodos por qué nos apartamos",
        ],
        efecto=("Si se corrige, la frase de Resultados pasa de «bajo riesgo en 2 y "
                "algunas preocupaciones en 1» a «bajo riesgo en 1 y algunas "
                "preocupaciones en 2». No cambia ninguna conclusión."),
    ))

    H.append(dict(
        clave="EST-003-DEFINICION",
        fuente_frase=["revision_sistematica/textos_completos/pdf/EST-003.pdf  (Onallah, Med 2023). Mirad Resultados y la Tabla 4"],
        titulo="EST-003 (PASA16): la definición de éxito es de otro estudio",
        que_hay=[
            "clinical_success_definition de los cinco brazos de EST-003:",
            "  «Significant reductions of P. aeruginosa colony forming units (CFU)",
            "   in sputum occurred in the treatment arm compared to placebo, on",
            "   days 4 ... of the BX004-A phage cocktail.»",
            "",
            "Comprobado sobre el texto de EST-003 (Onallah, Med 2023, serie",
            "compasiva de PASA16):",
            "  «BX004» no aparece ninguna vez.",
            "  De 12 fragmentos de esa frase, 0 aparecen en el artículo.",
            "BX004-A es el producto de EST-008.",
            "",
            "Lo que EST-003 sí dice de sus desenlaces:",
            "  «Good clinical outcome was documented in 13 out of 15 patients",
            "   (86.6%). Two clinical failures were reported.»",
            "",
            "Y sus numeradores por brazo: A=13 sobre n=1; B=5/5; C=4/5; D=3/4;",
            "E=1/1. Suman 26 éxitos sobre 16 pacientes.",
        ],
        problema=(
            "La definición atribuida a EST-003 no está en EST-003, y el 13 del brazo "
            "A es el numerador de la serie entera (13 de 15), no el de un brazo de un "
            "paciente."),
        pregunta="¿Cómo se corrige la extracción de EST-003?",
        opciones=[
            "Sustituir la definición por la frase propia del artículo y poner el numerador del brazo A en NA",
            "Dejarlo como está y señalarlo en el manuscrito como error de reporte",
            "Otra cosa: descríbela en la casilla de al lado",
        ],
        efecto=("La Tabla 4 ya declara los dos numeradores imposibles. Si se corrige, "
                "el brazo A de EST-003 deja de contarse entre ellos."),
    ))

    pac = {}
    for r in conf:
        pac[r["clave_del_paciente"]] = int(r.get("pacientes_de_esa_clave") or 1)
    est = {x for r in conf for x in (r["estudio_1"], r["estudio_2"])}
    que = ["%d pares confirmados leyendo los artículos. %d pacientes repartidos"
           % (len(conf), sum(pac.values())),
           "entre %d estudios; uno de ellos está publicado TRES veces." % len(est), ""]
    for r in conf:
        que.append("  %s + %s" % (r["estudio_1"], r["estudio_2"]))
        que.append("      %s" % r["clave_del_paciente"])
    que += ["",
            "DOS SERIES LOS CONCENTRAN.",
            "",
            "EST-003 comparte cuatro. Dos de ellos los declara el propio EST-003,",
            "en una columna «Published case» de su Tabla 4 que nadie había leído:",
            "el caso 4 dice «Khatami et al.» (= EST-095) y el caso 9 «Simner et",
            "al.» (= EST-015).",
            "",
            "EST-108 dice literalmente: «Twenty-seven of the 100 BT cases/patients",
            "were previously reported6,13-26». De esas quince referencias, SEIS son",
            "estudios de este corpus: EST-010, EST-016, EST-046, EST-062, EST-124 y",
            "EST-164. Sus siete pacientes están dentro de los 100 de EST-108.",
            "",
            "Quedan 13 pares candidatos SIN LEER."]
    H.append(dict(
        clave="SOLAPAMIENTO",
        fuente_frase=["Los dos PDF de cada par que confirméis, en revision_sistematica/textos_completos/pdf/",
                     "EST-003, EST-010, EST-012, EST-015, EST-016, EST-046, EST-062, EST-070, EST-077, EST-095, EST-108, EST-124 y EST-164"],
        titulo="Once pacientes están en más de un estudio del corpus",
        que_hay=que,
        problema=(
            "El corpus no son 137 conjuntos disjuntos de pacientes. La revisión no "
            "publica ninguna proporción agrupada, de modo que no hay ninguna cifra de "
            "efecto contaminada, pero trece de los estudios comparten pacientes y hay "
            "13 pares más sin comprobar. Dos de los brazos afectados --EST-010 A y "
            "EST-016 A-- están además entre los 21 que sobreviven al embudo de la "
            "proporción descriptiva, junto con EST-003 B a E, EST-012 A y EST-015 A: "
            "ocho de esos 21 brazos son pacientes contados dos veces."),
        pregunta="¿Confirmáis los cinco y qué estudio manda si se cuentan pacientes?",
        opciones=[
            "Confirmamos todos: se declaran en Resultados y en Limitaciones y los dos estudios se mantienen",
            "Confirmamos todos y además marcamos un estudio primario por paciente",
            "No confirmamos alguno: decid cuál y por qué en la casilla de al lado",
        ],
        efecto=("El corpus sigue en 137 estudios: son publicaciones distintas. Lo que "
                "cambia es lo que se puede afirmar sobre pacientes. Los 13 pares sin "
                "leer siguen sin leer y el manuscrito ya lo dice."),
    ))

    H.append(dict(
        clave="EST-077-EVENTOS",
        fuente_frase=["revision_sistematica/textos_completos/pdf/EST-077.pdf  (Aslam, Antimicrob Agents Chemother 2024)"],
        titulo="EST-077: cinco eventos adversos que el artículo no menciona",
        que_hay=[
            "En la extracción adjudicada: adverse_event_n = 5, n_arm = 4.",
            "",
            "Buscado en el texto completo entero:",
            "  «adverse» ............ 0 veces",
            "  «side effect» ........ 0 veces",
            "  «tolerability» ....... 0 veces",
            "",
            "Lo que el artículo sí dice:",
            "  «We performed a retrospective review of four patients that underwent",
            "   five separate courses of intravenous (IV) phage therapy»",
        ],
        problema=(
            "El 5 puede ser el número de CICLOS de tratamiento, no de eventos "
            "adversos. Si lo es, la unidad de análisis del campo está sin declarar."),
        pregunta="¿Qué cuenta realmente adverse_event_n en EST-077?",
        opciones=[
            "Son ciclos de tratamiento, no eventos: el campo se pone en NA",
            "Son eventos contados por episodio y no por paciente: se mantiene y se declara la unidad",
            "Otra cosa: descríbela en la casilla de al lado",
        ],
        efecto="Según lo que decidáis, la frase de la Tabla 4 cambia o desaparece.",
    ))

    H.append(dict(
        clave="EST-063-PROTOCOLO",
        fuente_frase=["revision_sistematica/textos_completos/pdf/EST-063.pdf  (Singh, BMJ Open Respir Res 2023)"],
        titulo="EST-063 es un protocolo, y los protocolos se excluyeron",
        que_hay=[
            "EST-063: Singh J et al. «Single-arm, open-labelled, safety and",
            "tolerability of intrabronchial and nebulised bacteriophage treatment in",
            "children with cystic fibrosis and Pseudomonas aeruginosa».",
            "BMJ Open Respir Res 2023.",
            "",
            "Estructura de protocolo de BMJ Open:",
            "  INTRODUCTION / METHODS AND ANALYSIS / Ethics and dissemination",
            "  «This trial is designed as a small, pilot, single-arm, open-label...»",
            "  «Results will be transcribed onto a data collection sheet...»",
            "",
            "El criterio que usasteis para los cuatro protocolos que SÍ excluisteis",
            "fue contar «will be»:",
            "  EST-035  99 veces  -> excluido PRO",
            "  EST-052 223 veces  -> excluido PRO",
            "  EST-122  80 veces  -> excluido PRO",
            "  EST-083       —     -> excluido PRO",
            "  EST-063  71 veces  -> EN EL CORPUS",
            "",
            "Y vuestra nota firmada del dominio D5 dice:",
            "  «Es un protocolo; aún no hay resultados.»",
        ],
        problema=(
            "Un protocolo no tiene desenlaces, de modo que se le está evaluando el "
            "sesgo por datos faltantes y por medición de desenlaces que no existen."),
        pregunta="¿Se excluye EST-063 con el código PRO?",
        opciones=[
            "Sí: se excluye como protocolo; PRO pasa de 4 a 5 exclusiones",
            "No: se mantiene y se explica en Métodos por qué este protocolo sí entra",
            "Otra cosa: descríbela en la casilla de al lado",
        ],
        efecto=("Si se excluye se mueven trece recuentos: corpus 137 -> 136; "
                "recuperables 95 -> 94; con texto 71 -> 70; brazos 103 -> 102; "
                "comparativos 15 -> 14; evaluables 12 -> 11; juicios 90 -> 82 (78 -> "
                "71 de dominio y 12 -> 11 globales); brazos del primer filtro de la "
                "Tabla 6 18 -> 17; exclusiones 46 -> 47. Los 21 brazos del embudo "
                "descriptivo NO cambian."),
    ))

    H.append(dict(
        clave="COMPARATIVOS-SIN-CONTROL",
        fuente_frase=["Vuestro propio cuaderno de consenso: revision_sistematica/riesgo_sesgo/riesgo_sesgo_comparativos_consenso.xlsx,",
                     "columna «¿En qué frase te apoyaste?», entrada 1 de cada estudio. O los PDF de los siete."],
        titulo="Siete de los quince «comparativos» no tienen grupo de comparación",
        que_hay=[
            "Vuestras propias notas del dominio 1, firmadas:",
            "",
            "  EST-004  «there was no control group for comparison»",
            "  EST-063  «Sin grupo comparador (diseño de un solo brazo).»",
            "  EST-070  «Sin grupo control.»",
            "  EST-096  «Sin grupo control. Imposible separar el efecto del fago.»",
            "  EST-116  «No se evalúa un efecto de tratamiento comparativo.»",
            "  EST-146  «Sin grupo control + antibióticos concomitantes frecuentes.»",
            "  EST-152  «Sin grupo control. No se puede separar el efecto del fago.»",
            "",
            "Con grupo de comparación real, cinco:",
            "  EST-008  BX004-A frente a placebo",
            "  EST-021  PP1131 frente a cuidado estándar",
            "  EST-132  convencional frente a convencional + fago",
            "  EST-055  el grupo IV recibe furazidina y cefixima SIN bacteriófago",
            "  EST-108  compara con y sin antibiótico concomitante DENTRO de los",
            "           tratados con fago; no compara fago contra no fago",
            "",
            "Sin texto completo, tres: EST-029, EST-157, EST-165. No se sabe.",
        ],
        problema=(
            "El manuscrito dice «15 estudios con grupo de comparación». La etiqueta "
            "sale del diseño adjudicado --una cohorte cuenta como comparativa-- y "
            "vuestras notas la contradicen en 7 de los 12 que leísteis."),
        pregunta="¿Cómo se nombra esto en el manuscrito?",
        opciones=[
            "Mantener los 15 como «clasificados por diseño» y añadir cuántos tienen comparador real",
            "Cambiar la frase a «15 con diseño comparativo, de los cuales 5 con grupo de comparación»",
            "Otra cosa: descríbela en la casilla de al lado",
        ],
        efecto=("No mueve ninguna cifra del embudo ni del riesgo de sesgo. Cambia lo "
                "que el manuscrito AFIRMA sobre esos 15."),
    ))

    H.append(dict(
        clave="EST-063-116-GLOBALES",
        fuente_frase=["revision_sistematica/textos_completos/pdf/EST-063.pdf y EST-116.pdf",
                     "o el manual de ROBINS-I (Sterne BMJ 2016) si mantenéis los juicios"],
        titulo="EST-063 y EST-116: dos globales más que no cuadran",
        que_hay=[
            "EST-063          EST-116",
            "  D1 Sin información   D1 Sin información",
            "  D2 Riesgo moderado   D2 Riesgo moderado",
            "  D3 Bajo riesgo       D3 Bajo riesgo",
            "  D4 Riesgo moderado   D4 Sin información",
            "  D5 Sin información   D5 Riesgo moderado",
            "  D6 Riesgo moderado   D6 Riesgo moderado",
            "  D7 Riesgo moderado   D7 Bajo riesgo",
            "  GLOBAL: Riesgo moderado   GLOBAL: Riesgo moderado",
            "",
            "ROBINS-I (Sterne 2016): el juicio global es «No information» cuando hay",
            "uno o más dominios sin información y ninguno grave ni crítico.",
            "",
            "Con estos dos y con EST-021, los juicios globales que no se",
            "corresponden con sus dominios son 3 de 12, no 1.",
        ],
        problema=(
            "Un juicio global de «riesgo moderado» afirma más de lo que los dominios "
            "sostienen: dos de los siete dicen que no hay información para juzgar."),
        pregunta="¿Qué hacemos con los juicios globales de EST-063 y EST-116?",
        opciones=[
            "Corregir los dos a «Sin información para juzgar»",
            "Mantener «Riesgo moderado» en los dos y declarar en Métodos por qué",
            "Decidir uno a uno: explicadlo en la casilla de al lado",
        ],
        efecto=("Si se corrigen, los globales de ROBINS-I pasan de «7 grave y 2 "
                "moderado» a «7 grave y 2 sin información». Si además se excluye "
                "EST-063 (hoja 5), quedan 8 estudios con «7 grave y 1 sin información»."),
    ))

    H.append(dict(
        clave="EST-021-EXTRACCION",
        fuente_frase=["revision_sistematica/textos_completos/pdf/EST-021.pdf. Mirad Findings, la Tabla 2 y el diagrama CONSORT"],
        titulo="EST-021: dos casillas que el artículo desmiente",
        que_hay=[
            "En la extracción adjudicada: n_arm = 27, mortality_n = 0,",
            "clinical_success_n = 6, adverse_event_n = 3.",
            "",
            "Lo que dice el artículo (Jault, Lancet Infect Dis 2019):",
            "  «27 patients were recruited and randomly assigned to receive phage",
            "   therapy (n=13) or standard of care (n=14).»",
            "  «...giving a safety population of 26 patients (PP1131 n=13,",
            "   standard of care n=13)»; mITT 25 (PP1131 n=12).",
            "  «One patient died in each treatment group after day 21.»",
            "  «three (23%) of 13 analysable participants had adverse events»",
            "  «the most infected wound was successfully reduced by two quadrants",
            "   or more in half of participants» -> 6 de 12.",
        ],
        problema=(
            "El 27 es el ensayo entero, no el brazo de fagos. El 0 de mortalidad "
            "contradice al artículo. Y el par 6/27 mezcla un recuento de brazo con el "
            "total del ensayo: la Tabla 6 lo validó como numerador y denominador "
            "correctos, y EST-021 es uno de los cinco brazos que llegan al cuarto "
            "filtro."),
        pregunta="¿Se corrigen las casillas de EST-021?",
        opciones=[
            "Sí: n_arm = 13, mortality_n = 1, y el numerador 6 sobre denominador 12",
            "Sí, pero con otros valores: decidlos en la casilla de al lado",
            "No: explicad por qué en la casilla de al lado",
        ],
        efecto=("Cambia la fila de EST-021 en la Tabla 4 de desenlaces y el par que la "
                "Tabla 6 valida. No cambia el resultado del embudo: EST-021 cae "
                "igualmente en el séptimo requisito, porque su desenlace principal es "
                "un tiempo."),
    ))

    que9 = ["Cuatro brazos tienen resistance_class = «below-MDR-threshold»,",
            "los cuatro con texto leído y extracción COMPLETE.", "",
            "Estudios de un solo brazo, cuyo ÚNICO paciente está por debajo del",
            "umbral de multirresistencia:"]
    for r in solos:
        que9.append("  %s %s  n=%s  fuente de la clase: %s"
                    % (r["study_id"], r["arm_id"], r["n_arm"], r["resistance_class_source"]))
    que9 += ["", "Estratos por clase dentro de estudios que SÍ incluyen MDR:"]
    for r in estratos:
        que9.append("  %s %s  n=%s" % (r["study_id"], r["arm_id"], r["n_arm"]))
    que9 += ["", "EST-003 B es además uno de los 21 brazos que sobreviven al embudo",
             "de la proporción descriptiva."]
    H.append(dict(
        clave="BAJO-UMBRAL-MDR",
        fuente_frase=["revision_sistematica/textos_completos/pdf/EST-001.pdf y EST-094.pdf. Mirad el antibiograma de su paciente"],
        titulo="Dos estudios cuyo único paciente no es multirresistente",
        que_hay=que9,
        problema=(
            "La población de la revisión es «Pseudomonas aeruginosa "
            "multirresistente». Los estratos de EST-003 y EST-108 no son un problema: "
            "el estudio cumple aunque uno de sus estratos no. Los otros dos sí lo son: "
            "son estudios de un paciente, y ese paciente está por debajo del umbral "
            "según vuestra propia codificación."),
        pregunta="¿Qué hacemos con EST-001 y EST-094?",
        opciones=[
            "Excluirlos: no cumplen el criterio de población",
            "Mantenerlos y declarar en Resultados cuántos brazos quedan por debajo del umbral",
            "Revisar la clasificación de resistencia de esos dos artículos antes de decidir",
        ],
        efecto=("Si se excluyen, el corpus baja a 135, los recuperables a 93, los "
                "brazos a 101 y los 21 del embudo descriptivo a 19. Si se mantienen, "
                "hay que decir que 4 de los 103 brazos no cumplen el criterio de "
                "resistencia."),
    ))
    return H


def main():
    from openpyxl import Workbook
    from openpyxl.styles import Alignment, Font, PatternFill
    from openpyxl.worksheet.datavalidation import DataValidation

    puestas = ya_contestado()
    if puestas:
        print("NO SE ESCRIBE: el cuaderno ya tiene respuestas.", file=sys.stderr)
        for x in puestas:
            print("  " + x, file=sys.stderr)
        print("Si de verdad quieres rehacerlo, muévelo o bórralo antes.",
              file=sys.stderr)
        raise SystemExit(1)

    HALLAZGOS = construye()
    negrita = Font(bold=True)
    grande = Font(bold=True, size=13)
    mono = Font(name="Consolas", size=9)
    cab = PatternFill("solid", fgColor="D9E1F2")
    ojo = PatternFill("solid", fgColor="FCE4D6")
    arriba = Alignment(vertical="top", wrap_text=True)

    wb = Workbook()
    h = wb.active
    h.title = "Empieza aqui"
    h.column_dimensions["A"].width = 106
    texto = [("Nueve cosas que encontró la auditoría y que no decide un script", True),
             ("", False),
             ("Ninguna es de estilo. Las nueve tocan datos que ya firmasteis, y las", False),
             ("nueve cambian algo de lo que el manuscrito dice. Por eso vienen aquí y", False),
             ("no resueltas: corregir una extracción firmada o un juicio firmado es", False),
             ("vuestro.", False),
             ("", False)]
    for i, d in enumerate(HALLAZGOS, start=1):
        texto.append(("  %d. %s" % (i, d["titulo"]), False))
    texto += [("", False),
              ("Cada hoja trae la prueba literal, la pregunta y las opciones. Escoged", False),
              ("una del desplegable y, si hace falta, explicad en «por qué». Sin las dos", False),
              ("firmas de la última hoja no se ingiere nada.", False),
              ("", False),
              ("LA CASILLA «FRASE EN QUE OS APOYÁIS».", True),
              ("Va la cita literal del documento que sostiene vuestra decisión, y cada hoja", False),
              ("dice de qué fichero sacarla, en «Sacad la frase de». Los artículos están en", False),
              ("clo-author/revision_sistematica/textos_completos/pdf/, un PDF por estudio.", False),
              ("Si la decisión no se apoya en una cita sino en un razonamiento vuestro,", False),
              ("escribidlo igual pero sin comillas: la auditoría separa las dos cosas y", False),
              ("ninguna de las dos se presenta como la otra.", False),
              ("", False),
              ("Mientras estas nueve sigan sin firmar, el manuscrito lleva avisos de", True),
              ("pendiente y el sobre no se puede enviar.", True)]
    for i, (t, b) in enumerate(texto, start=1):
        c = h.cell(row=i, column=1, value=t)
        if b:
            c.font = negrita

    for k, d in enumerate(HALLAZGOS, start=1):
        s = wb.create_sheet("%d. %s" % (k, d["clave"][:25]))
        s.column_dimensions["A"].width = 22
        s.column_dimensions["B"].width = 96
        s.cell(row=1, column=1, value=d["titulo"]).font = grande
        f = 3
        s.cell(row=f, column=1, value="Lo que hay").font = negrita
        for linea in d["que_hay"]:
            s.cell(row=f, column=2, value=linea).font = mono
            f += 1
        f += 1
        s.cell(row=f, column=1, value="El problema").font = negrita
        s.cell(row=f, column=2, value=d["problema"]).alignment = arriba
        s.row_dimensions[f].height = 62
        f += 2
        s.cell(row=f, column=1, value="Qué cambia").font = negrita
        s.cell(row=f, column=2, value=d["efecto"]).alignment = arriba
        s.row_dimensions[f].height = 62
        f += 2
        s.cell(row=f, column=1, value="LA PREGUNTA").font = negrita
        s.cell(row=f, column=1).fill = cab
        s.cell(row=f, column=2, value=d["pregunta"]).font = negrita
        f += 1
        for o in d["opciones"]:
            s.cell(row=f, column=2, value="   · " + o).alignment = arriba
            f += 1
        f += 1
        s.cell(row=f, column=1, value="Vuestra decisión").font = negrita
        celda = s.cell(row=f, column=2)
        celda.fill = ojo
        dv = DataValidation(
            type="list",
            formula1='"%s"' % ",".join(o.replace(",", ";")[:70] for o in d["opciones"]),
            allow_blank=True)
        dv.error = "Escoja una de las opciones de arriba."
        s.add_data_validation(dv)
        dv.add(celda)
        f += 1
        s.cell(row=f, column=1, value="Por qué").font = negrita
        c = s.cell(row=f, column=2)
        c.fill = ojo
        c.alignment = arriba
        s.row_dimensions[f].height = 56
        f += 2
        # DE DONDE SALE LA FRASE. La casilla se llamaba «Frase en que os
        # apoyáis» y no decía de qué documento: quien la rellena tenía que
        # adivinar qué artículo abrir. Ahora cada hoja nombra el fichero.
        s.cell(row=f, column=1, value="Sacad la frase de").font = negrita
        s.cell(row=f, column=1).fill = cab
        for linea in d["fuente_frase"]:
            s.cell(row=f, column=2, value=linea).font = mono
            f += 1
        s.cell(row=f, column=1, value="Frase en que os apoyáis").font = negrita
        c = s.cell(row=f, column=2)
        c.fill = ojo
        c.alignment = arriba
        s.row_dimensions[f].height = 56
        f += 1

    fi = wb.create_sheet("Firma")
    fi.column_dimensions["A"].width = 46
    fi.column_dimensions["B"].width = 54
    fi.cell(row=1, column=1, value="Firma de los dos autores").font = negrita
    fi.cell(row=2, column=1,
            value="Las nueve decisiones son de los dos: se firman juntas o no se "
                  "firma ninguna.")
    for i, k in enumerate(["Revisor 1 (nombre completo)",
                           "Revisor 2 (nombre completo)",
                           "Fecha (AAAA-MM-DD)",
                           "¿Habéis leído los artículos citados en cada hoja?"], start=4):
        fi.cell(row=i, column=1, value=k).font = negrita
        fi.cell(row=i, column=2, value="").fill = ojo

    wb.save(CUADERNO)
    print("%d hallazgos para firmar" % len(HALLAZGOS))
    for i, d in enumerate(HALLAZGOS, start=1):
        print("  %d. %s" % (i, d["titulo"]))
    print("cuaderno: %s" % CUADERNO)


if __name__ == "__main__":
    main()
