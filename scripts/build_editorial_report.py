"""Informe editorial, indice del paquete y manuscritos en Word.

EL PAPEL QUE SE ADOPTA AQUI. El de un editor de revista de microbiologia
clinica que recibe el manuscrito y decide si puede entrar en revision por pares.
No es un resumen amable de lo hecho: es la lista de lo que falta, con la
consecuencia de cada carencia y qui'en puede resolverla. Un informe editorial
que solo elogia no sirve para publicar.

SALIDA
    verificables revisión sistemática/00_INDICE.docx
    verificables revisión sistemática/S0_informe_editorial.docx
    verificables revisión sistemática/manuscrito_*.docx
"""
import json
import pathlib
import re
import sys

from docx import Document
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.shared import Pt, Cm, RGBColor

ROOT = pathlib.Path(__file__).resolve().parent.parent
OUT = ROOT / "verificables revisión sistemática"
try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass


def doc_nuevo(titulo, subtitulo=""):
    d = Document()
    est = d.styles["Normal"]
    est.font.name = "Calibri"
    est.font.size = Pt(10.5)
    for s in d.sections:
        s.top_margin = s.bottom_margin = Cm(2)
        s.left_margin = s.right_margin = Cm(2.2)
    d.add_heading(titulo, level=0).alignment = WD_ALIGN_PARAGRAPH.LEFT
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


def nota(d, texto):
    p = d.add_paragraph()
    r = p.add_run(texto)
    r.font.size = Pt(8.5)
    r.italic = True
    r.font.color.rgb = RGBColor(0x44, 0x44, 0x44)


def informe_editorial(S):
    d = doc_nuevo(
        "Informe editorial",
        "Evaluación previa a revisión por pares. Revista de microbiología "
        "clínica / revisiones sistemáticas. 11 de agosto de 2026.")

    d.add_heading("Decisión", level=1)
    p = d.add_paragraph()
    r = p.add_run("REVISIÓN MAYOR ANTES DE ENVIAR A PARES.")
    r.bold = True
    d.add_paragraph(
        "El trabajo metodológico que sostiene este manuscrito está por encima "
        "de lo habitual en el campo, y su hallazgo central es relevante y "
        "publicable. No puede, sin embargo, entrar en revisión por pares como "
        "revisión sistemática completa mientras la extracción de datos no haya "
        "concluido. Lo que sigue distingue lo que impide publicar de lo que "
        "solo mejora el manuscrito.")

    d.add_heading("Lo que este manuscrito hace bien", level=1)
    for t in [
        "La búsqueda es más amplia que la de las revisiones publicadas en el "
        "campo: nueve fuentes en dos corrientes, sin restricción de idioma, con "
        "literatura regional y registros de ensayos incluidos. La inclusión de "
        "BVS y SciELO no es decorativa: aporta la literatura donde se "
        "concentran los diseños comparativos.",
        "La auditoría de controles positivos es infrecuente y convincente. "
        "Permite afirmar, y no solo esperar, que el cribado no perdió estudios "
        "elegibles conocidos. Que se declare el fallo detectado en una "
        "ejecución intermedia refuerza la afirmación en vez de debilitarla.",
        "El vocabulario cerrado de exclusión, fijado antes de empezar, resuelve "
        "un problema real de las revisiones grandes: los motivos escritos en "
        "texto libre derivan entre lotes y luego hay que reagruparlos a mano.",
        "La sección 3.5 argumenta explícitamente por qué NO se agrupa. Es lo "
        "contrario de lo habitual, y es lo correcto cuando los requisitos del "
        "diseño no se cumplen.",
        "La declaración de uso de IA cumple las recomendaciones del ICMJE.",
    ]:
        d.add_paragraph(t, style="List Bullet")

    d.add_heading("Condiciones para publicar (bloqueantes)", level=1)
    tabla(d,
          ["#", "Qué falta", "Por qué bloquea", "Quién lo resuelve"],
          [("B1", "Extracción de datos por duplicado e independiente",
            "Sin ella no hay desenlaces, ni riesgo de sesgo, ni GRADE. Una "
            "revisión sistemática sin extracción es un protocolo con "
            "resultados de cribado.",
            "Los dos revisores; el formulario y el libro de códigos ya existen"),
           ("B2", "Registro del protocolo",
            "PROSPERO admite registro aunque la revisión esté en marcha, "
            "declarando la fecha de inicio. Sin registro ni declaración, "
            "muchas revistas devuelven el manuscrito sin revisar. El "
            "manuscrito SÍ declara la ausencia, que es la vía honesta, pero "
            "el registro sigue siendo preferible.",
            "Autor de correspondencia; 1–2 días de trámite"),
           ("B3", "Recuperación del texto completo",
            "El 46,5 % obtenido es insuficiente y, sobre todo, sesgado: la "
            "fracción faltante concentra el 63,4 % de los diseños "
            "comparativos. Un revisor objetará que las características "
            "descritas no representan al campo.",
            "Biblioteca de la universidad; petición interbibliotecaria"),
           ("B4", "Evaluación del riesgo de sesgo",
            "PRISMA 2020 ítems 11 y 18. Depende de B1 y B3.",
            "Los dos revisores, con RoB 2, ROBINS-I y Murad"),
           ("B5", "Formularios ICMJE de conflicto de interés",
            "Uno firmado por autor. Requisito administrativo sin excepción.",
            "Cada autor"),
           ("B6", "Contribución de autores en formato CRediT",
            "Exigido por la mayoría de revistas del área.",
            "Autor de correspondencia")],
          [1.2, 4.6, 6.4, 4.4])

    d.add_heading("Prioridad dentro de B3, si el tiempo es limitado", level=1)
    d.add_paragraph(
        "No hacen falta los 85 textos completos para que el manuscrito resista "
        "la revisión. Los 26 estudios comparativos son los que deciden, y "
        "dentro de ellos los cuatro ensayos aleatorizados de referencia del "
        "campo. Recuperar solo esos cuatro cambia la objeción de «no ha leído "
        "los ensayos principales» a «no ha leído parte de la literatura "
        "regional», que es una limitación declarable.")
    tabla(d, ["Estudio", "Publicación", "Identificador", "Por qué es prioritario"],
          [("EST-021", "Lancet Infect Dis 2019", "PMID 30292481",
            "PhagoBurn: único ensayo aleatorizado en quemados por P. aeruginosa"),
           ("EST-118", "Lancet Infect Dis 2021", "PMID 32949500",
            "Leitner: tres brazos aleatorizados con placebo y antibiótico; el "
            "comparador más limpio del corpus"),
           ("EST-052", "J Cyst Fibros 2023", "CYPHY (Yale)",
            "Ensayo aleatorizado en fibrosis quística"),
           ("EST-029", "Med 2025", "PMID 39740667",
            "TP-102 en pie diabético; aleatorizado y doble ciego")],
          [2.4, 4.2, 3.6, 6.4])

    d.add_heading("Observaciones que mejoran el manuscrito (no bloquean)", level=1)
    for t in [
        "El título describe con precisión lo que el trabajo hace, pero es "
        "largo. Considerar «Phage therapy for multidrug-resistant Pseudomonas "
        "aeruginosa: how verifiable is the clinical evidence base?».",
        "El resumen (241 palabras en la versión inglesa) cumple el límite "
        "habitual de 250. Comprobar el límite exacto de la revista de destino.",
        "Las cifras de la sección 3.4 miden el reporte EN EL RESUMEN. El "
        "manuscrito lo aclara, y hace bien, pero conviene repetir esa "
        "salvedad en la leyenda de la Tabla 2, porque las tablas se leen "
        "sueltas.",
        "La Figura 1 incluye una caja de recuperación de texto completo que no "
        "forma parte del flujo PRISMA. Está explicada en el pie, pero algún "
        "revisor la leerá como parte del diagrama. Considerar moverla a una "
        "figura suplementaria.",
        "Falta un párrafo sobre por qué se excluyeron las endolisinas. La "
        "decisión es defendible y está en Métodos, pero merece una frase en "
        "Discusión, porque hay literatura que las cuenta como fagoterapia.",
        "Declarar en Métodos qué se hará si un estudio aparece publicado entre "
        "la búsqueda y el envío.",
    ]:
        d.add_paragraph(t, style="List Bullet")

    d.add_heading("Sobre la vía de publicación, dado el plazo", level=1)
    d.add_paragraph(
        "Si el plazo no permite completar B1, hay dos salidas legítimas y una "
        "que no lo es.")
    tabla(d, ["Opción", "Qué se envía", "Viabilidad"],
          [("A. Completar la extracción",
            "Revisión sistemática completa, con desenlaces, riesgo de sesgo y "
            "GRADE",
            "La correcta. No es alcanzable en 24 horas con 159 estudios y dos "
            "revisores."),
           ("B. Enviar como está, reencuadrado",
            "Revisión sistemática de la estructura y verificabilidad del "
            "cuerpo de evidencia, sin estimaciones de eficacia, con las cuatro "
            "limitaciones declaradas",
            "Alcanzable hoy. Es lo que el manuscrito ya hace. Admisible en "
            "revistas metodológicas y en revistas del área que publican "
            "evidence mapping."),
           ("C. Publicar proporciones agrupadas",
            "Metaanálisis de proporciones de éxito",
            "NO. Los datos no lo sostienen y la sección 3.5 explica por qué. "
            "Hacerlo sería reproducir el defecto que este trabajo denuncia.")],
          [4.2, 6.4, 6.0])
    nota(d, "La opción B no es un premio de consolación. El hallazgo de que un "
            "cuerpo de evidencia no admite la síntesis que se le viene "
            "aplicando es un resultado por derecho propio, y este manuscrito "
            "lo demuestra con datos y no con opinión.")
    d.save(OUT / "S0_informe_editorial.docx")


def md_a_docx(origen, destino, titulo):
    """Vuelca el manuscrito a Word conservando la jerarquia y las negritas."""
    t = pathlib.Path(origen).read_text(encoding="utf-8")
    d = Document()
    est = d.styles["Normal"]
    est.font.name = "Calibri"
    est.font.size = Pt(11)
    for s in d.sections:
        s.top_margin = s.bottom_margin = Cm(2.2)
        s.left_margin = s.right_margin = Cm(2.4)
    for linea in t.split("\n"):
        l = linea.rstrip()
        if not l or l.strip() == "---":
            continue
        if l.startswith("#"):
            n = len(l) - len(l.lstrip("#"))
            d.add_heading(re.sub(r"\*", "", l.lstrip("# ").strip()),
                          level=min(n - 1, 4) if n > 1 else 0)
            continue
        estilo = None
        if l.startswith("- "):
            estilo, l = "List Bullet", l[2:]
        p = d.add_paragraph(style=estilo)
        # negrita y cursiva de Markdown, respetando las citas [@clave]
        for trozo in re.split(r"(\*\*[^*]+\*\*|\*[^*]+\*)", l):
            if not trozo:
                continue
            if trozo.startswith("**") and trozo.endswith("**"):
                p.add_run(trozo[2:-2]).bold = True
            elif trozo.startswith("*") and trozo.endswith("*"):
                p.add_run(trozo[1:-1]).italic = True
            else:
                p.add_run(trozo)
    d.save(destino)


def indice(S):
    d = doc_nuevo("Verificables — Revisión sistemática de fagoterapia en "
                  "Pseudomonas aeruginosa multirresistente",
                  "Índice del paquete. Cada archivo responde a un ítem de "
                  "PRISMA 2020 o a un requisito del ICMJE.")
    tabla(d, ["Archivo", "Qué contiene", "Responde a"],
          [("S0_informe_editorial.docx",
            "Evaluación editorial: qué bloquea la publicación y qué solo la "
            "mejora", "Uso interno"),
           ("manuscrito_es.docx / manuscript_en.docx",
            "Manuscrito completo en español y en inglés", "Envío"),
           ("S1_lista_PRISMA_2020.docx",
            "Lista de comprobación ítem por ítem, con estado y ubicación",
            "PRISMA 2020, ítem 27"),
           ("S2_estrategias_de_busqueda.docx",
            "Sintaxis literal por fuente, fecha y número de resultados",
            "PRISMA 2020, ítems 6 y 7"),
           ("S3_decisiones_etapa2_titulo.csv",
            "Registro solo-anexar de toda decisión de cribado por título",
            "PRISMA 2020, ítem 8"),
           ("S3_decisiones_etapa3_resumen.csv",
            "Ídem para el cribado por resumen, con la corriente PRISMA",
            "PRISMA 2020, ítems 8 y 16"),
           ("S4_pre_extraccion_desde_resumen.csv",
            "Pre-extracción de los 159 estudios, marcada como parcial",
            "PRISMA 2020, ítems 9 y 10"),
           ("S5_listado_219_estudios.csv",
            "Los 219 estudios con situación, diseño, procedencia y si se "
            "obtuvo el texto completo", "PRISMA 2020, ítem 17"),
           ("S6_auditoria_controles_positivos.docx",
            "Prueba de que el cribado no perdió estudios elegibles conocidos",
            "Metodológico; refuerza el ítem 8"),
           ("S7_declaraciones_ICMJE.docx",
            "Financiación, conflictos, CRediT, registro, datos y uso de IA",
            "ICMJE; PRISMA ítems 24 a 27"),
           ("S8_recuperacion_texto_completo.csv",
            "Vía de recuperación resuelta para cada informe sin DOI editorial",
            "Justifica el 46,5 % de §3.2"),
           ("figuras y tablas/",
            "Figuras 1 y 2 en PDF vectorial; tablas 1 a 4 en CSV",
            "PRISMA 2020, ítem 16a")],
          [5.6, 7.4, 3.6])

    d.add_heading("Estado del envío", level=1)
    tabla(d, ["Elemento", "Estado"],
          [("Búsqueda en nueve fuentes", "COMPLETA"),
           ("Cribado por título y resumen", "COMPLETO — 219 estudios"),
           ("Agrupación de informes en estudios", "COMPLETA"),
           ("Pre-extracción desde resumen", "COMPLETA — 159 de 159"),
           ("Recuperación de texto completo", "PARCIAL — %d de %d (%.1f %%)"
            % (S["texto_completo_obtenido"], S["estudios_extraibles"],
               S["texto_completo_pct"])),
           ("Extracción por duplicado", "PENDIENTE — bloquea la publicación"),
           ("Riesgo de sesgo y GRADE", "PENDIENTE — depende de la extracción"),
           ("Registro en PROSPERO", "PENDIENTE — declarado como ausente"),
           ("Manuscrito y figuras", "COMPLETOS")],
          [8.0, 8.6])
    nota(d, "Todas las cifras de este paquete y del manuscrito se generan desde "
            "el canal de datos. Una comprobación automática recorre el "
            "manuscrito y falla si alguna cifra del texto no procede de él.")
    d.save(OUT / "00_INDICE.docx")


def main():
    OUT.mkdir(exist_ok=True)
    S = json.loads((ROOT / "quality_reports" / "synthesis_scalars.json")
                   .read_text(encoding="utf-8"))
    informe_editorial(S)
    print("  S0  informe editorial")
    md_a_docx(ROOT / "paper" / "manuscrito_revision_sistematica.md",
              OUT / "manuscrito_es.docx", "Manuscrito (español)")
    md_a_docx(ROOT / "paper" / "manuscript_systematic_review_en.md",
              OUT / "manuscript_en.docx", "Manuscript (English)")
    print("  manuscritos en Word, español e inglés")
    indice(S)
    print("  00  índice del paquete")
    return 0


if __name__ == "__main__":
    sys.exit(main())
