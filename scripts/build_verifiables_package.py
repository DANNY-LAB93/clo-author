"""Genera el paquete de verificables que un editor exige antes de publicar.

QUE ES UN VERIFICABLE. No es un anexo decorativo: es el documento que permite a
un revisor comprobar una afirmacion del manuscrito sin fiarse de ella. Por eso
cada archivo de aqui responde a un item concreto de PRISMA 2020 o a un requisito
del ICMJE, y el indice dice a cual.

FORMATO. Word para lo que el editor lee y anota (listas, ecuaciones, informes).
Excel para lo que el revisor filtra y ordena (listados de estudios, registros de
decision). PDF para las figuras, que ya salen vectoriales del generador.

SALIDA
    verificables revisión sistemática/
"""
import collections
import csv
import datetime
import json
import pathlib
import shutil
import sys

from docx import Document
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.shared import Pt, Cm, RGBColor

ROOT = pathlib.Path(__file__).resolve().parent.parent
RS = ROOT / "revision_sistematica"
OUT = ROOT / "verificables revisión sistemática"
csv.field_size_limit(200_000_000)
try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass


def leer(p):
    with open(p, encoding="utf-8", newline="") as fh:
        return list(csv.DictReader(fh))


MESES = ("enero", "febrero", "marzo", "abril", "mayo", "junio", "julio",
         "agosto", "septiembre", "octubre", "noviembre", "diciembre")


def fecha_larga():
    """La fecha de HOY, no la que alguien tecleo un dia.

    El subtitulo de S1 decia «Estado a 11 de agosto de 2026» y ahi se quedo
    mientras el anexo se regeneraba: entre esa fecha y el 14 de septiembre
    entraron las 29 exclusiones tras leer los textos completos, el riesgo de
    sesgo firmado y dos cambios de titulo. Una lista de comprobacion que viaja
    a la revista fechada un mes antes de lo que declara es peor que una sin
    fecha, porque parece comprobada.
    """
    h = datetime.date.today()
    return "%d de %s de %d" % (h.day, MESES[h.month - 1], h.year)


def doc_nuevo(titulo, subtitulo=""):
    d = Document()
    est = d.styles["Normal"]
    est.font.name = "Calibri"
    est.font.size = Pt(10.5)
    for s in d.sections:
        s.top_margin = s.bottom_margin = Cm(2)
        s.left_margin = s.right_margin = Cm(2.2)
    h = d.add_heading(titulo, level=0)
    h.alignment = WD_ALIGN_PARAGRAPH.LEFT
    if subtitulo:
        p = d.add_paragraph(subtitulo)
        p.runs[0].italic = True
        p.runs[0].font.size = Pt(9.5)
    return d


def tabla(d, cabecera, filas, anchos=None):
    t = d.add_table(rows=1, cols=len(cabecera))
    t.style = "Light Grid Accent 1"
    for i, c in enumerate(cabecera):
        cel = t.rows[0].cells[i]
        cel.text = ""
        r = cel.paragraphs[0].add_run(str(c))
        r.bold = True
        r.font.size = Pt(9)
    for f in filas:
        cs = t.add_row().cells
        for i, v in enumerate(f):
            cs[i].text = ""
            r = cs[i].paragraphs[0].add_run("" if v is None else str(v))
            r.font.size = Pt(9)
    if anchos:
        for fila in t.rows:
            for i, w in enumerate(anchos):
                fila.cells[i].width = Cm(w)
    d.add_paragraph()
    return t


def nota(d, texto):
    p = d.add_paragraph()
    r = p.add_run(texto)
    r.font.size = Pt(8.5)
    r.italic = True
    r.font.color.rgb = RGBColor(0x44, 0x44, 0x44)


def estado_riesgo_de_sesgo():
    """Los items 11 y 18 de PRISMA, redactados desde el canal.

    Devuelve {item: (veredicto, texto)}. Si el fichero de estado no existe
    todavia, se dice eso y no se inventa un veredicto.
    """
    import json as _json
    p = ROOT / "quality_reports" / "rob_tabla_estado.json"
    if not p.exists():
        sin = ("NO CUMPLE", "No se ha evaluado. Ver §2.7.")
        return {"11": sin, "18": sin}
    R = _json.loads(p.read_text(encoding="utf-8"))
    alcance = ("%d de los %d estudios con diseño comparativo adjudicado sobre "
               "el artículo (RoB 2 en los aleatorizados, ROBINS-I en los no "
               "aleatorizados y las cohortes), a nivel de dominio y POR "
               "CONSENSO entre los dos autores, no por duplicado "
               "independiente. Los reportes y series de casos no se evalúan "
               "con instrumento formal, por decisión: §2.7 dice por qué. "
               % (R["evaluables"], R["comparativos_adjudicados"]))
    if R.get("completa"):
        return {
            "11": ("CUMPLE", alcance + "El estudio comparativo restante no "
                   "tiene texto completo y no se evalúa. La limitación consta "
                   "en §4.4"),
            "18": ("CUMPLE", "Tabla de dominios con los %d juicios, estudio "
                   "por estudio, en §3.7" % R["celdas_totales"]),
        }
    return {
        "11": ("PARCIAL", alcance + "La evaluación está EN CURSO: faltan %d de "
               "los %d juicios. §2.7 lo declara" % (R["celdas_pendientes"],
                                                    R["celdas_totales"])),
        "18": ("NO CUMPLE", "Los juicios por estudio aún no están emitidos "
               "(faltan %d de %d). No se sustituyen por ningún indicador "
               "derivado del diseño. §2.7 y §4.4"
               % (R["celdas_pendientes"], R["celdas_totales"])),
    }


# ---------------------------------------------------------------- documentos
def v1_prisma(S):
    """Lista de comprobacion PRISMA 2020, item por item.

    Los items 11 y 18 (riesgo de sesgo) NO se redactan aqui: salen de
    `rob_tabla_estado.json`, que es el mismo fichero del que sale el
    manuscrito. Estuvieron escritos a mano diciendo "no se ha realizado"
    mientras el manuscrito ya declaraba una evaluacion en curso, y una lista
    PRISMA que contradice a su propio manuscrito es peor que no adjuntarla.

    Se marca CUMPLE / PARCIAL / NO CUMPLE y se dice donde mirar. Marcar todo
    como cumplido es la forma mas rapida de perder la confianza del editor: los
    tres items que esta revision no cumple se declaran como tales.
    """
    ROB = estado_riesgo_de_sesgo()
    d = doc_nuevo("S1. Lista de comprobación PRISMA 2020",
                  "Fagoterapia en Pseudomonas aeruginosa multirresistente. "
                  "Estado a %s." % fecha_larga())
    # A DONDE APUNTAN LAS REFERENCIAS. La columna "dónde mirar" usa la
    # numeracion del informe extendido (§2.1 a §4.4), que NO viaja en el sobre
    # de la revista: alli va el manuscrito con secciones sin numerar. Un editor
    # que siga "§2.7" no encuentra nada. La correspondencia se declara aqui, en
    # vez de dejar 27 remisiones colgando.
    d.add_heading("Cómo leer la columna «dónde mirar»", level=2)
    d.add_paragraph(
        "Las remisiones §1 a §4.4 corresponden al informe extendido. En el "
        "manuscrito enviado a la revista, cuyas secciones no van numeradas, "
        "equivalen a:")
    for a, b in (("§1", "INTRODUCCIÓN"),
                 ("§2.1", "METODOLOGÍA › Protocolo y reporte"),
                 ("§2.2", "METODOLOGÍA › Criterios de elegibilidad (Tabla 1)"),
                 ("§2.3", "METODOLOGÍA › Fuentes de información y estrategia de búsqueda"),
                 ("§2.4", "METODOLOGÍA › Selección de los estudios"),
                 ("§2.6", "METODOLOGÍA › Extracción de datos"),
                 ("§2.7", "METODOLOGÍA › Evaluación del riesgo de sesgo"),
                 ("§2.8", "METODOLOGÍA › Síntesis"),
                 ("§2.9", "METODOLOGÍA › Enmiendas al protocolo"),
                 ("§3.1 y §3.1.1", "RESULTADOS › Selección de los estudios (Figura 1)"),
                 ("§3.3", "RESULTADOS › Características del cuerpo de evidencia (Tabla 2)"),
                 ("§3.5", "RESULTADOS › Reporte de los desenlaces (Tabla 4)"),
                 ("§3.6", "RESULTADOS › Viabilidad de la síntesis cuantitativa (Tabla 6)"),
                 ("§4, §4.3 y §4.4", "DISCUSIÓN Y CONCLUSIONES")):
        d.add_paragraph("%s  →  %s" % (a, b), style="List Bullet")
    d.add_paragraph(
        "Las tablas también se renumeran entre los dos documentos: la Tabla 1 "
        "del manuscrito de la revista es la de criterios de elegibilidad, y la "
        "de características del corpus es allí la Tabla 2.")
    ITEMS = [
        ("1", "Título", "Identifica el informe como revisión sistemática", "CUMPLE", "Título"),
        ("2", "Resumen estructurado", "Ver lista PRISMA for Abstracts", "CUMPLE", "Resumen"),
        ("3", "Justificación", "Base racional en el contexto de lo conocido", "CUMPLE", "§1"),
        ("4", "Objetivos", "Pregunta explícita", "CUMPLE", "§1, último párrafo"),
        ("5", "Criterios de elegibilidad", "Y cómo se agruparon los estudios", "CUMPLE",
         "§2.2, incluido el criterio de idioma (inglés o español), verificado "
         "informe por informe en S9 y sobre el texto completo en S10"),
        ("6", "Fuentes de información", "Todas, con fecha de la última búsqueda", "CUMPLE", "§2.3"),
        ("7", "Estrategia de búsqueda", "Literal, para cada base y registro", "CUMPLE", "§2.3 y S2"),
        ("8", "Proceso de selección", "Cuántos revisores, cómo trabajaron", "PARCIAL",
         "§2.4; la etapa 1 aplica reglas deterministas y las etapas 2 y 3 las "
         "emitió un modelo de lenguaje (Claude Opus 5) como revisor único, sin "
         "duplicación independiente, aplicando criterios y un vocabulario "
         "cerrado fijados de antemano por los autores. Los informes que "
         "superaron el cribado los revisaron los autores uno a uno antes de "
         "agruparlos en estudios (S5). Lo no revisado es lo que el modelo "
         "excluyó. Declarado en §2.4 y como limitación en §4.4; el registro "
         "completo, con modelo y marca de tiempo por decisión, está en S3"),
        ("9", "Proceso de extracción", "Cuántos revisores, herramientas", "CUMPLE",
         "§2.6; extracción por duplicado e independiente completa (%d de %d "
         % (S["extraccion_estudios_ambos"], S["extraccion_estudios_r1"]) +
         "estudios), con la concordancia medida antes de resolver y %d de %d "
         % (S["extraccion_conflictos_firmados"], S["extraccion_desacuerdos"]) +
         "desacuerdos adjudicados por consenso. S11 y S12 aportan el rastro"),
        ("10a", "Variables de desenlace", "Lista y definiciones", "PARCIAL",
         "§2.2 las lista; S4 no contiene definiciones de desenlace porque "
         "ningún resumen del corpus las declara. Las definiciones de los "
         "textos completos leídos se discuten en §3.5 y §3.6"),
        ("10b", "Otras variables", "Lista y definiciones", "CUMPLE", "S4"),
        ("11", "Riesgo de sesgo", "Herramienta, cuántos revisores", ROB["11"][0],
         ROB["11"][1]),
        ("12", "Medidas del efecto", "Para cada desenlace", "NO APLICA",
         "Este informe no presenta estimaciones de efecto. §3.5 mide la completitud con que se reportan los desenlaces; §3.6 explica por qué no se agregan"),
        ("13a-f", "Métodos de síntesis", "Incluida la decisión de no agrupar", "CUMPLE",
         "§2.8 y §3.6, con la justificación de por qué no se agrupa"),
        ("14", "Sesgo de publicación", "Métodos de evaluación", "PARCIAL",
         "§4.3 documenta %d de %d estudios registrados sin publicación; no se "
         % (S["estudios_solo_registro"], S["estudios"]) +
         "aplicaron pruebas estadísticas por no haber síntesis cuantitativa"),
        ("15", "Certeza de la evidencia", "GRADE u otro", "NO APLICA",
         "§2.7: GRADE califica la certeza de una estimación agrupada y este "
         "informe no presenta ninguna. §3.5 y la Tabla 6 muestran que, tras "
         "aplicar los criterios de elegibilidad de §2.2, NINGÚN brazo del "
         "corpus podría entrar en una proporción agrupada de éxito clínico"),
        ("16a", "Selección de estudios", "Flujo con números", "CUMPLE", "§3.1 y Figura 1"),
        ("16b", "Excluidos en texto completo", "Con motivos", "CUMPLE",
         "§3.1.1 y S16: %d estudios que el cribado había admitido se "
         % S["estudios_excluidos_tras_texto_completo"] +
         "excluyeron al leer su texto completo, cada uno con su código de "
         "motivo y la frase del artículo que lo sostiene. S3 recoge además "
         "los motivos de las etapas 1 a 3 con vocabulario cerrado"),
        ("17", "Características de los estudios", "De cada uno", "CUMPLE",
         "Tabla 1, y listado completo en S5"),
        ("18", "Riesgo de sesgo por estudio", "", ROB["18"][0], ROB["18"][1]),
        ("19", "Resultados de los estudios", "", "PARCIAL",
         "§3.5 y las Tablas 5 y 6 reportan la COMPLETITUD con que cada estudio "
         "declara los cinco desenlaces, no sus estimaciones de efecto. El "
         "dato brazo a brazo se aporta en S14, y la procedencia de cada "
         "casilla en S15"),
        ("20a-d", "Resultados de la síntesis", "", "CUMPLE",
         "§3.3 a §3.6; la síntesis es de estructura y de completitud de "
         "reporte, no de eficacia, y §3.6 razona por qué no puede ser otra"),
        ("21", "Sesgos de publicación", "", "PARCIAL", "§4.3"),
        ("22", "Certeza de la evidencia", "", "NO APLICA",
         "No hay estimación agrupada cuya certeza calificar; ver §2.7 y §3.5"),
        ("23a-d", "Discusión", "Interpretación, limitaciones, implicaciones", "CUMPLE", "§4"),
        ("24a", "Registro", "Número o declaración de no registro", "CUMPLE (declarado)",
         "§2.1 declara explícitamente que NO está registrada"),
        ("24b", "Protocolo", "Dónde consultarlo", "PARCIAL",
         "Repositorio del proyecto; no depositado en registro público"),
        ("24c", "Enmiendas", "", "CUMPLE (una enmienda declarada)",
         "§2.9 declara la restricción de idioma adoptada el 11-08-2026, con el "
         "cribado ya cerrado, y mide su impacto: %d estudios eliminados, %d de "
         % (S["estudios_eliminados_por_idioma"], S["comparativos_perdidos_por_idioma"]) +
         "ellos comparativos y uno del conjunto de control positivo. El registro "
         "de decisiones es solo-anexar y permite reconstruir el corpus previo"),
        ("25", "Apoyo económico", "", "CUMPLE", "Declaraciones"),
        ("26", "Conflictos de interés", "", "CUMPLE", "Declaraciones"),
        ("27", "Disponibilidad de datos y código", "", "CUMPLE", "Declaraciones y S3–S6"),
    ]
    tabla(d, ["Ítem", "Elemento", "Qué exige", "Estado", "Dónde está"],
          [(a, b, c, e, f) for a, b, c, e, f in ITEMS],
          [1.4, 3.2, 3.8, 2.4, 6.2])
    # El recuento agrupaba por la PRIMERA PALABRA del veredicto, y "NO CUMPLE"
    # y "NO APLICA" empiezan las dos por "NO": los items que no aplican se le
    # presentaban al editor como incumplidos, y la fila "NO APLICA" salia
    # siempre en cero. Se agrupa por el veredicto entero, normalizando solo el
    # parentesis de "CUMPLE (declarado)".
    est = collections.Counter(i[3].split(" (")[0] for i in ITEMS)
    d.add_heading("Resumen del estado", level=2)
    for k in ("CUMPLE", "PARCIAL", "NO CUMPLE", "NO APLICA"):
        n = est.get(k, 0)
        if n:
            d.add_paragraph("%s: %d ítems" % (k, n), style="List Bullet")
    nota(d, "Los ítems marcados NO CUMPLE dependen todos de la extracción por "
            "duplicado, que está en curso. Se declaran como limitación en §4.4 "
            "del manuscrito en lugar de presentarse como cumplidos.")
    d.save(OUT / "S1_lista_PRISMA_2020.docx")


def v2_busquedas(S):
    d = doc_nuevo("S2. Estrategias de búsqueda",
                  "Sintaxis literal por fuente, con fecha de ejecución y "
                  "número de resultados. Última ejecución: 10 de agosto de 2026.")
    # La autoría de la búsqueda se declara aquí y no solo en el manuscrito:
    # este anexo es el que un revisor abre para comprobar la reproducibilidad,
    # y es donde la pregunta "¿quién la hizo?" se plantea de forma natural.
    nota(d, "Estas ecuaciones las diseñó y ejecutó D. Valdiviezo, autor de la "
            "revisión, interrogando cada interfaz directamente. No las generó ni "
            "las ejecutó el modelo de lenguaje que sí emitió las decisiones de "
            "cribado por título y resumen, cuya intervención se declara en la "
            "sección 2.4 del manuscrito y en la declaración de uso de "
            "inteligencia artificial.")
    man = json.loads((RS / "busqueda" / "sources.json").read_text(encoding="utf-8"))
    REG = {"ClinicalTrials.gov", "EudraCT", "CTIS"}
    d.add_heading("Corriente 1. Bases bibliográficas", level=2)
    tabla(d, ["Fuente", "Informes en el corpus", "Archivo de exportación"],
          [(k, S["registros_por_fuente"].get(k, 0), pathlib.Path(v).name)
           for k, v in man.items() if k not in REG], [5.0, 4.0, 7.0])
    d.add_heading("Corriente 2. Registros de ensayos", level=2)
    tabla(d, ["Fuente", "Informes en el corpus", "Archivo de exportación"],
          [(k, S["registros_por_fuente"].get(k, 0), pathlib.Path(v).name)
           for k, v in man.items() if k in REG], [5.0, 4.0, 7.0])
    fuente = ROOT / "quality_reports" / "ecuaciones_busqueda_final.md"
    if fuente.exists():
        d.add_heading("Ecuaciones literales", level=2)
        for linea in fuente.read_text(encoding="utf-8").split("\n"):
            l = linea.rstrip()
            if not l:
                continue
            if l.startswith("#"):
                d.add_heading(l.lstrip("# ").strip(), level=3)
            elif l.startswith(("|", "---")):
                continue
            else:
                p = d.add_paragraph(l)
                p.runs[0].font.size = Pt(9)
    nota(d, "El manifiesto de fuentes (sources.json) es la única declaración de "
            "qué exportaciones entran en el corpus. Una comprobación automática "
            "falla si alguna fuente declarada no aparece representada.")
    d.save(OUT / "S2_estrategias_de_busqueda.docx")


def v5_listado(S):
    """Listado de los estudios incluidos. En Excel porque se filtra y se ordena."""
    grupos = leer(RS / "cribado" / "study_groups.csv")
    pre = {p["id_provisional"]: p for p in
           leer(RS / "extraccion" / "pre_extraccion_desde_resumen.csv")}
# El texto completo no siempre llega en PDF: el manuscrito de autor de
# PhagoBurn esta depositado en ORBi como .docx. Contar solo *.pdf lo
# dejaba fuera del recuento aunque estuviera en disco y fuera legible.
    # El texto completo puede llegar como PDF, como manuscrito de autor en
    # .docx o como el texto integro de la pagina del editor cuando este
    # sirve el articulo en HTML y bloquea la descarga automatica del PDF.
    # Las tres formas son el mismo dato para quien va a extraer.
    pdfs = {q.stem for q in (RS / "textos_completos" / "pdf").iterdir()
            if q.suffix.lower() in (".pdf", ".docx")}
    web = RS / "textos_completos" / "texto_html"
    if web.exists():
        pdfs |= {q.stem for q in web.glob("*.txt")}
    # Los 22 excluidos al releer el texto completo no van en S5: S5 es el
    # cuerpo de evidencia. Van en S16, con su codigo, su motivo y la cita del
    # articulo que los desmiente, que es lo que pide PRISMA 16b.
    p_ex = RS / "cribado" / "exclusiones_tras_texto_completo.csv"
    fuera_ft = ({r["study_id"] for r in leer(p_ex)} if p_ex.exists() else set())
    reps = {"EST-%03d" % int(g["estudio"]): g for g in grupos
            if g["informe_para_extraer"] == "SI"
            and "EST-%03d" % int(g["estudio"]) not in fuera_ft}
    filas = []
    for eid in sorted(reps):
        g, p = reps[eid], pre.get(eid, {})
        filas.append([eid, g["situacion"], g["anio"], g["revista"], g["titulo"],
                      g["informes_del_estudio"],
                      p.get("study_design", ""), p.get("n_arm", ""),
                      p.get("geographic_source", ""),
                      "sí" if eid in pdfs else "no", g["clave"]])
    # El numero va en el nombre y por tanto SE CALCULA: dejarlo escrito hizo
    # que el fichero siguiera diciendo 219 cuando ya contenia 185.
    for viejo in OUT.glob("S5_listado_*_estudios.*"):
        viejo.unlink()
    with open(OUT / ("S5_listado_%d_estudios.csv" % len(filas)), "w",
              encoding="utf-8-sig", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(["id", "situacion", "anio", "revista", "titulo",
                    "n_informes", "diseno", "n_brazo", "procedencia",
                    "texto_completo", "clave_de_estudio"])
        w.writerows(filas)
    return len(filas)


def v6_auditoria(S):
    d = doc_nuevo("S6. Auditoría de controles positivos",
                  "Comprobación de que el cribado no perdió ningún estudio "
                  "conocido a priori como elegible.")
    d.add_heading("Qué comprueba y por qué a nivel de estudio", level=2)
    d.add_paragraph(
        "Antes de iniciar el cribado se fijó un conjunto de 40 estudios "
        "identificados en una revisión exploratoria previa y conocidos como "
        "elegibles. Después de cada etapa se comprueba que ninguno de ellos "
        "haya perdido todos sus informes.")
    d.add_paragraph(
        "La comprobación opera sobre el estudio y no sobre el informe. Excluir "
        "una fe de erratas o una ficha de registro duplicada de un estudio "
        "incluido es legítimo; perder el estudio entero no lo es. Una auditoría "
        "por informe daría falsos positivos en el primer caso y dejaría de "
        "distinguir el segundo.")
    d.add_heading("Resultado", level=2)
    tabla(d, ["Etapa", "Estudios de control", "Conservan informe", "Veredicto"],
          [("Etapa 1 (reglas explícitas)", 40, 40, "SUPERADA"),
           ("Etapa 2 (título)", 40, 40, "SUPERADA"),
           ("Etapa 3 (resumen)", 40, 40, "SUPERADA")], [6.0, 3.6, 3.6, 3.0])
    d.add_heading("Perdida por la enmienda de idioma", level=2)
    d.add_paragraph(
        "La restriccion a ingles y espanol, adoptada el 11 de agosto de 2026 con "
        "el cribado ya cerrado, elimina uno de los 40 estudios de control: "
        "Ronit et al. (2024), un caso de fagoterapia en protesis vascular "
        "infectada por P. aeruginosa publicado en danes en Ugeskrift for Laeger. "
        "No es un fallo del cribado, porque el estudio se identifico y se "
        "clasifico correctamente, sino el precio del criterio.")
    d.add_paragraph(
        "La auditoria distingue ahora las dos situaciones. Una perdida por una "
        "enmienda declarada se informa pero no detiene el canal; una perdida sin "
        "motivo declarado sigue siendo un fallo que lo detiene. Confundirlas "
        "arruina la auditoria en cualquiera de los dos sentidos: si falla "
        "siempre se acaba ignorando, y si pasa siempre deja de detectar el error "
        "que existe para detectar.")

    d.add_heading("Incidencia detectada y corregida", level=2)
    d.add_paragraph(
        "En una ejecución intermedia la auditoría falló: una regla de exclusión "
        "mal calibrada eliminaba todos los informes de un estudio incluido. La "
        "regla se corrigió antes de continuar. El fallo y su corrección constan "
        "en el registro del proyecto. Se informa aquí porque una auditoría que "
        "solo se reporta cuando pasa no demuestra nada.")
    nota(d, "El conjunto de control se fijó ANTES del cribado. Elegirlo después "
            "de ver los resultados lo convertiría en una descripción del "
            "resultado en vez de en una prueba.")
    d.save(OUT / "S6_auditoria_controles_positivos.docx")



def v16_exclusiones(S):
    """S16: los estudios excluidos al leer el texto completo, con su motivo.

    Es lo que pide PRISMA 16b, y es el anexo que permite a un revisor
    discrepar: cada fila lleva el codigo de motivo, la explicacion y **la frase
    del articulo** que sostiene la exclusion. Sin la cita, la lista seria una
    afirmacion; con ella, es comprobable.
    """
    fuente = RS / "cribado" / "exclusiones_tras_texto_completo.csv"
    if not fuente.exists():
        return
    sys.path.insert(0, str(ROOT / "scripts"))
    from exclusion_codes import CODES
    filas = leer(fuente)
    destino = OUT / "S16_excluidos_tras_leer_el_texto_completo.csv"
    cab = ["study_id", "codigo", "que_significa_el_codigo", "motivo",
           "cita_del_texto", "titulo", "decidido_por", "fecha"]
    with open(destino, "w", encoding="utf-8-sig", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=cab)
        w.writeheader()
        for r in filas:
            r["que_significa_el_codigo"] = CODES.get(r["codigo"], "")
            w.writerow({c: r.get(c, "") for c in cab})
    if len(filas) != S["estudios_excluidos_tras_texto_completo"]:
        raise SystemExit(
            "S16: el anexo trae %d exclusiones y el manuscrito declara %d."
            % (len(filas), S["estudios_excluidos_tras_texto_completo"]))
    import collections as _c
    c = _c.Counter(r["codigo"] for r in filas)
    print("  S16 %d estudios excluidos al releer: %s"
          % (len(filas), ", ".join("%s %d" % kv for kv in c.most_common())))

def v9_idioma(S):
    """S9 sellado con el estado final de cada informe, no con el intermedio.

    `idioma_verificacion.csv` es la salida del comprobador de idioma, que juzga
    sobre el resumen. Un informe puede pasar esa prueba y quedar excluido
    despues al leer el texto completo. Aqui se cruza con el corpus final y con
    las decisiones de cribado, para que el anexo diga en que quedo cada uno.
    """
    fuente = RS / "cribado" / "idioma_verificacion.csv"
    if not fuente.exists():
        return
    filas = list(csv.DictReader(open(fuente, encoding="utf-8-sig")))
    grupos = list(csv.DictReader(
        open(RS / "cribado" / "study_groups.csv", encoding="utf-8-sig")))

    # `study_groups` es la foto que dejo el cribado y NO se filtra: sigue
    # teniendo los 22 estudios que salieron despues, al leer los textos
    # completos. Aqui hay que descontarlos, o S9 declara 233 informes incluidos
    # sobre un corpus de 201. Cada uno se lleva su motivo real, no un generico.
    p_ex = RS / "cribado" / "exclusiones_tras_texto_completo.csv"
    excl_est, motivo_ft = set(), {}
    if p_ex.exists():
        for r in csv.DictReader(open(p_ex, encoding="utf-8")):
            excl_est.add(r["study_id"])
            motivo_ft[r["study_id"]] = "%s: %s" % (r["codigo"], r["motivo"])
    fuera_ft = {g["record_id"]: motivo_ft["EST-%03d" % int(g["estudio"])]
                for g in grupos if "EST-%03d" % int(g["estudio"]) in excl_est}
    incluidos = {g["record_id"] for g in grupos
                 if g["record_id"] not in fuera_ft}

    # El motivo de la exclusion se toma de la ultima decision que la nombre, no
    # se redacta aqui: el registro de cribado es la fuente y es solo-anexar.
    motivo = {}
    for etapa in ("screening_stage3_pool_decisions.csv",
                  "screening_stage2_pool_decisions.csv"):
        p = RS / "cribado" / etapa
        if not p.exists():
            continue
        for r in csv.DictReader(open(p, encoding="utf-8-sig")):
            if r.get("verdict") == "EXCLUDE":
                motivo[r["record_id"]] = r.get("reason", "")

    cab = list(filas[0]) + ["estado_final", "motivo_de_la_exclusion"]
    fuera = 0
    for r in filas:
        dentro = r["record_id"] in incluidos
        r["estado_final"] = "INCLUIDO" if dentro else "EXCLUIDO DESPUES"
        r["motivo_de_la_exclusion"] = "" if dentro else fuera_ft.get(
            r["record_id"],
            motivo.get(r["record_id"], "excluido en el cribado; ver S3"))
        fuera += 0 if dentro else 1

    destino = OUT / "S9_idioma_por_informe_y_clase_de_evidencia.csv"
    with open(destino, "w", encoding="utf-8", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=cab)
        w.writeheader()
        w.writerows(filas)

    n = len(filas) - fuera
    if n != S["informes_agrupados"]:
        raise SystemExit(
            "S9: quedan %d informes INCLUIDO y el corpus tiene %d. El anexo "
            "que prueba el criterio de idioma no cuadra con el manuscrito."
            % (n, S["informes_agrupados"]))
    print("  S9  %d informes incluidos + %d excluidos despues, con su motivo"
          % (n, fuera))


def declaracion_ia():
    """La declaración de uso de IA, tomada literal del manuscrito autoritativo.

    Se lee en vez de reescribirse porque las dos versiones que existían habían
    divergido, y la del anexo era la suave: decía que el modelo dio «asistencia
    en la programación» del cribado cuando fue él quien emitió las decisiones,
    y que los autores «verificaron todo el contenido» cuando el manuscrito dice
    que los registros excluidos no los releyó nadie.
    """
    md = (ROOT / "paper" / "manuscrito_revision_sistematica.md").read_text(
        encoding="utf-8")
    marca = "**Uso de inteligencia artificial.**"
    i = md.find(marca)
    if i < 0:
        raise SystemExit(
            "S7: no encuentro «%s» en el manuscrito. La declaración de uso de "
            "IA sale de ahí y no se redacta en este script; si la sección se "
            "renombró, actualiza la marca." % marca)
    texto = md[i + len(marca):].split("\n\n")[0].strip()
    # El .docx no lleva marcado Markdown: los asteriscos quedarian a la vista.
    return texto.replace("**", "")


def v7_declaraciones(S):
    d = doc_nuevo("S7. Declaraciones y requisitos del ICMJE",
                  "Documento de acompañamiento al envío.")
    for tit, txt in [
        ("Financiación",
         "Esta revisión no recibió financiación específica de agencias "
         "públicas, comerciales o sin ánimo de lucro."),
        ("Conflictos de interés",
         "Los autores declaran no tener conflictos de interés. Cada autor debe "
         "adjuntar además el formulario ICMJE Disclosure of Interest firmado."),
        ("Contribución de los autores (CRediT)",
         "PENDIENTE DE COMPLETAR antes del envío. Debe asignar a cada autor las "
         "categorías CRediT que le correspondan: conceptualización, curación de "
         "datos, análisis formal, investigación, metodología, software, "
         "validación, visualización, redacción del borrador original, y "
         "redacción con revisión y edición."),
        ("Registro del protocolo",
         "PENDIENTE. La revisión no está registrada en PROSPERO ni en OSF. El "
         "manuscrito declara la ausencia de forma explícita en §2.1. Si se "
         "registra antes del envío, debe sustituirse esa declaración por el "
         "número de registro; no debe declararse un registro retrospectivo como "
         "si fuera prospectivo."),
        ("Disponibilidad de datos y código",
         "El corpus de cribado, los registros de decisión completos, el "
         "formulario de extracción y todo el código del canal están disponibles "
         "en el repositorio del proyecto. Los registros de decisión son "
         "solo-anexar y conservan cada corrección junto con la decisión "
         "original."),
        # Esta declaracion NO se redacta aqui: se copia literal del manuscrito.
        # La version que habia decia «asistencia en la programacion del canal de
        # cribado» y «los autores revisaron y verificaron todo el contenido».
        # Las dos cosas suavizaban lo que el manuscrito declara: que el modelo
        # emitio las decisiones como revisor unico, y que los registros que
        # excluyo no los releyo ningun humano. Es justo la declaracion que un
        # comite mira primero, y tener dos versiones distintas de ella en el
        # mismo envio es peor que no adjuntarla.
        ("Uso de inteligencia artificial", declaracion_ia()),
        ("Ética y consentimiento",
         "No aplica: la revisión se basa en literatura publicada y en registros "
         "públicos de ensayos, sin datos individuales de pacientes."),
    ]:
        d.add_heading(tit, level=2)
        d.add_paragraph(txt)
    d.save(OUT / "S7_declaraciones_ICMJE.docx")


def main():
    OUT.mkdir(exist_ok=True)
    S = json.loads((ROOT / "quality_reports" / "synthesis_scalars.json")
                   .read_text(encoding="utf-8"))
    print("paquete de verificables:")
    v1_prisma(S)
    print("  S1  lista PRISMA 2020")
    v2_busquedas(S)
    print("  S2  estrategias de busqueda")
    # S3: registro de decisiones, tal cual, porque su valor es ser el original
    for origen, destino in (
            ("cribado/screening_stage2_pool_decisions.csv",
             "S3_decisiones_etapa2_titulo.csv"),
            ("cribado/screening_stage3_pool_decisions.csv",
             "S3_decisiones_etapa3_resumen.csv"),
            ("extraccion/pre_extraccion_desde_resumen.csv",
             "S4_pre_extraccion_desde_resumen.csv"),
            ("textos_completos/fulltext_identifiers.csv",
             "S8_recuperacion_texto_completo.csv"),
            ("cribado/idioma_texto_completo.csv",
             "S10_idioma_verificado_sobre_texto_completo.csv")):
        p = RS / origen
        if p.exists():
            shutil.copy2(p, OUT / destino)

    # S9: la prueba del criterio de idioma, informe por informe. Se copiaba tal
    # cual y salia con 234 filas, todas ADMITIDO, cuando los informes incluidos
    # son 233. La fila de mas es R56334c0408: el comprobador leyo su resumen,
    # que esta en ingles, y lo admitio; el cuerpo del articulo esta en ruso y se
    # excluyo despues, al abrir la web del editor. El fichero se escribio antes
    # de esa exclusion y nunca se actualizo.
    #
    # No se borra la fila. Es el caso que el manuscrito usa para argumentar que
    # el idioma no se puede dar por sabido desde los metadatos ni desde el
    # resumen, y borrarla escondería precisamente eso. Se sella con el estado
    # final y su motivo, de modo que S9 cuadre con los 233 del manuscrito y el
    # lector vea por que hay una fila mas.
    # S14 y S15. Un arbitro no podia comprobar NADA de la seccion 3.5 ni de las
    # tablas 5 y 6: el paquete solo llevaba la pre-extraccion desde resumenes
    # (S4), y esas cifras salen de la extraccion adjudicada, que no viajaba.
    # Publicar una cifra cuyo fichero no se aporta es pedir que se crea.
    for origen, destino in (
            ("extraccion/extraccion_adjudicada.csv",
             "S14_extraccion_adjudicada.csv"),
            ("extraccion/extraccion_adjudicada_procedencia.csv",
             "S15_procedencia_de_cada_casilla.csv")):
        q = RS / origen
        if q.exists():
            shutil.copy2(q, OUT / destino)
            print("  %-4s %s" % (destino[:3], destino))

    v9_idioma(S)
    v16_exclusiones(S)

    # S4 se copiaba tal cual y no permitia reproducir la Tabla 2: tiene 159
    # filas -- el corpus anterior a la enmienda de idioma -- mientras la tabla
    # usa 124, y su columna `study_id` esta vacia en las 159, de modo que no hay
    # forma de saber que fila pertenece al corpus actual. No se borran las 35
    # filas sobrantes, que son rastro de la enmienda: se anade la columna que
    # permite filtrarlas, y se retira la columna vacia que solo confunde.
    s4 = OUT / "S4_pre_extraccion_desde_resumen.csv"
    if s4.exists():
        filas = leer(s4)
        # el fichero lleva BOM, asi que la primera clave sale como "﻿id"
        with open(ROOT / "quality_reports" / "orden_de_extraccion.csv",
                  encoding="utf-8-sig", newline="") as fh:
            vivos = {r["id"] for r in csv.DictReader(fh)}
        p_ex = RS / "cribado" / "exclusiones_tras_texto_completo.csv"
        if p_ex.exists():
            vivos -= {r["study_id"] for r in leer(p_ex)}
        campos = [c for c in filas[0] if c != "study_id"] + ["en_corpus_actual"]
        for f in filas:
            f.pop("study_id", None)
            f["en_corpus_actual"] = "si" if f.get("id_provisional") in vivos else "no"
        with open(s4, "w", encoding="utf-8", newline="") as fh:
            w = csv.DictWriter(fh, fieldnames=campos)
            w.writeheader()
            w.writerows(filas)
        n = sum(1 for f in filas if f["en_corpus_actual"] == "si")
        print("  S4  %d filas, %d en el corpus actual (Tabla 2 se reproduce "
              "filtrando en_corpus_actual = si)" % (len(filas), n))
    # S3 se copiaba tal cual y sale con 13 917 decisiones de titulo mientras el
    # manuscrito declara 13 894. Las 23 de mas son decisiones sobre registros de
    # una version anterior del corpus, y el registro es solo-anexar, asi que se
    # conservan. Pero sin marcarlas, un arbitro cuenta y encuentra una
    # discrepancia que no puede explicar: es el mismo defecto que tenia S9.
    corpus = {r["record_id"] for r in
              leer(RS / "cribado" / "screening_corpus_all.csv")}
    for nombre in ("S3_decisiones_etapa2_titulo.csv",
                   "S3_decisiones_etapa3_resumen.csv"):
        ruta = OUT / nombre
        if not ruta.exists():
            continue
        filas = leer(ruta)
        if not filas or "en_corpus_actual" in filas[0]:
            continue
        cab = list(filas[0]) + ["en_corpus_actual"]
        fuera = 0
        for r in filas:
            dentro = r["record_id"] in corpus
            r["en_corpus_actual"] = "si" if dentro else "no"
            fuera += 0 if dentro else 1
        with open(ruta, "w", encoding="utf-8", newline="") as fh:
            w = csv.DictWriter(fh, fieldnames=cab)
            w.writeheader()
            w.writerows(filas)
        print("  S3  %-38s %5d decisiones, %d fuera del corpus actual"
              % (nombre, len(filas), fuera))
    print("  S4  pre-extraccion desde resumen")
    n = v5_listado(S)
    print("  S5  listado de %d estudios" % n)
    v6_auditoria(S)
    print("  S6  auditoria de controles positivos")
    v7_declaraciones(S)
    print("  S7  declaraciones ICMJE")
    print("  S8  registro de recuperacion de texto completo")
    print("  S9  idioma por informe, con clase de evidencia")
    print("  S10 idioma verificado sobre el texto completo")
    # figuras y tablas, ya listas
    fig = OUT / "figuras y tablas"
    fig.mkdir(exist_ok=True)
    for p in (ROOT / "paper" / "figuras").glob("*.pdf"):
        shutil.copy2(p, fig / p.name)
    for p in (ROOT / "paper" / "tablas").glob("*.csv"):
        shutil.copy2(p, fig / p.name)
    print("  figuras (PDF vectorial) y tablas (CSV)")

    # S11-S13 se construyen aqui y no aparte. Vivieron cinco dias como fichero
    # suelto y se quedaron viejos: el paquete anunciaba 169 desacuerdos y una
    # kappa de 0,38 cuando el manuscrito ya decia 575 y 0,57. Un anexo que hay
    # que acordarse de regenerar acaba contradiciendo al articulo que acompana.
    # Van despues de S5 porque S12 lo lee para saber que estudios tienen texto.
    import build_extraction_verifiables
    build_extraction_verifiables.main()

    print("\nescrito en %s" % OUT)
    return 0


if __name__ == "__main__":
    sys.exit(main())
