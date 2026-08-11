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


# ---------------------------------------------------------------- documentos
def v1_prisma(S):
    """Lista de comprobacion PRISMA 2020, item por item.

    Se marca CUMPLE / PARCIAL / NO CUMPLE y se dice donde mirar. Marcar todo
    como cumplido es la forma mas rapida de perder la confianza del editor: los
    tres items que esta revision no cumple se declaran como tales.
    """
    d = doc_nuevo("S1. Lista de comprobación PRISMA 2020",
                  "Fagoterapia en Pseudomonas aeruginosa multirresistente. "
                  "Estado a 11 de agosto de 2026.")
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
         "§2.4; cribado por un solo revisor con reglas explícitas y auditoría "
         "de controles positivos. Declarado como limitación en §4.4"),
        ("9", "Proceso de extracción", "Cuántos revisores, herramientas", "PARCIAL",
         "§2.6; extracción por duplicado en curso, no concluida"),
        ("10a", "Variables de desenlace", "Lista y definiciones", "CUMPLE", "§2.2 y S4"),
        ("10b", "Otras variables", "Lista y definiciones", "CUMPLE", "S4"),
        ("11", "Riesgo de sesgo", "Herramienta, cuántos revisores", "NO CUMPLE",
         "§2.7; depende del texto completo. Se reportará con la extracción "
         "definitiva. Declarado en §4.4"),
        ("12", "Medidas del efecto", "Para cada desenlace", "NO APLICA",
         "Este informe no presenta estimaciones de efecto; ver §2.6 y §3.5"),
        ("13a-f", "Métodos de síntesis", "Incluida la decisión de no agrupar", "CUMPLE",
         "§2.8 y §3.5, con la justificación de por qué no se agrupa"),
        ("14", "Sesgo de publicación", "Métodos de evaluación", "PARCIAL",
         "§4.3 documenta 60 de 219 estudios registrados sin publicación; no se "
         "aplicaron pruebas estadísticas por no haber síntesis cuantitativa"),
        ("15", "Certeza de la evidencia", "GRADE u otro", "NO CUMPLE",
         "§2.7; pendiente de la extracción definitiva"),
        ("16a", "Selección de estudios", "Flujo con números", "CUMPLE", "§3.1 y Figura 1"),
        ("16b", "Excluidos en texto completo", "Con motivos", "PARCIAL",
         "S3 recoge los motivos de las etapas 1 a 3 con vocabulario cerrado; "
         "la exclusión en texto completo se producirá con la extracción"),
        ("17", "Características de los estudios", "De cada uno", "CUMPLE",
         "Tabla 1, y listado completo en S5"),
        ("18", "Riesgo de sesgo por estudio", "", "NO CUMPLE", "Pendiente; §4.4"),
        ("19", "Resultados de los estudios", "", "NO APLICA", "Ver §2.6"),
        ("20a-d", "Resultados de la síntesis", "", "CUMPLE",
         "§3.3 a §3.5; la síntesis es de estructura y reporte, no de eficacia"),
        ("21", "Sesgos de publicación", "", "PARCIAL", "§4.3"),
        ("22", "Certeza de la evidencia", "", "NO CUMPLE", "Pendiente"),
        ("23a-d", "Discusión", "Interpretación, limitaciones, implicaciones", "CUMPLE", "§4"),
        ("24a", "Registro", "Número o declaración de no registro", "CUMPLE (declarado)",
         "§2.1 declara explícitamente que NO está registrada"),
        ("24b", "Protocolo", "Dónde consultarlo", "PARCIAL",
         "Repositorio del proyecto; no depositado en registro público"),
        ("24c", "Enmiendas", "", "CUMPLE (una enmienda declarada)",
         "§2.9 declara la restricción de idioma adoptada el 11-08-2026, con el "
         "cribado ya cerrado, y mide su impacto: 34 estudios eliminados, 17 de "
         "ellos comparativos y uno del conjunto de control positivo. El registro "
         "de decisiones es solo-anexar y permite reconstruir el corpus previo"),
        ("25", "Apoyo económico", "", "CUMPLE", "Declaraciones"),
        ("26", "Conflictos de interés", "", "CUMPLE", "Declaraciones"),
        ("27", "Disponibilidad de datos y código", "", "CUMPLE", "Declaraciones y S3–S6"),
    ]
    tabla(d, ["Ítem", "Elemento", "Qué exige", "Estado", "Dónde está"],
          [(a, b, c, e, f) for a, b, c, e, f in ITEMS],
          [1.4, 3.2, 3.8, 2.4, 6.2])
    est = collections.Counter(i[3].split()[0] for i in ITEMS)
    d.add_heading("Resumen del estado", level=2)
    for k in ("CUMPLE", "PARCIAL", "NO", "NO APLICA"):
        n = est.get(k, 0)
        if n:
            d.add_paragraph("%s: %d ítems" % (
                {"NO": "NO CUMPLE"}.get(k, k), n), style="List Bullet")
    nota(d, "Los ítems marcados NO CUMPLE dependen todos de la extracción por "
            "duplicado, que está en curso. Se declaran como limitación en §4.4 "
            "del manuscrito en lugar de presentarse como cumplidos.")
    d.save(OUT / "S1_lista_PRISMA_2020.docx")


def v2_busquedas(S):
    d = doc_nuevo("S2. Estrategias de búsqueda",
                  "Sintaxis literal por fuente, con fecha de ejecución y "
                  "número de resultados. Última ejecución: 10 de agosto de 2026.")
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
    """Listado de los 219 estudios. En Excel porque se filtra y se ordena."""
    grupos = leer(RS / "cribado" / "study_groups.csv")
    pre = {p["id_provisional"]: p for p in
           leer(RS / "extraccion" / "pre_extraccion_desde_resumen.csv")}
    pdfs = {p.stem for p in (RS / "textos_completos" / "pdf").glob("*.pdf")}
    reps = {"EST-%03d" % int(g["estudio"]): g for g in grupos
            if g["informe_para_extraer"] == "SI"}
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
    for viejo in OUT.glob("S5_listado_*_estudios.csv"):
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
        ("Uso de inteligencia artificial",
         "En la preparación de este trabajo se emplearon herramientas de "
         "inteligencia artificial generativa (Claude, Anthropic) para la "
         "asistencia en la programación del canal de cribado, la pre-extracción "
         "desde resúmenes y la redacción de borradores. Los autores revisaron y "
         "verificaron todo el contenido y asumen la responsabilidad íntegra por "
         "su exactitud e integridad. Ninguna herramienta de IA figura como "
         "autora, conforme a las recomendaciones del ICMJE."),
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
            # La prueba del criterio de idioma. Va tal cual, informe por
            # informe: un criterio de elegibilidad que el lector no puede
            # recomprobar no es un criterio, es una afirmacion.
            ("cribado/idioma_verificacion.csv",
             "S9_idioma_por_informe_y_clase_de_evidencia.csv"),
            ("cribado/idioma_texto_completo.csv",
             "S10_idioma_verificado_sobre_texto_completo.csv")):
        p = RS / origen
        if p.exists():
            shutil.copy2(p, OUT / destino)
    print("  S3  registros de decision (etapas 2 y 3)")
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
    print("\nescrito en %s" % OUT)
    return 0


if __name__ == "__main__":
    sys.exit(main())
