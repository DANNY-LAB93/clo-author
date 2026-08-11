"""Genera el formulario de extracción CIEGO de un revisor, en español.

CIEGO SIGNIFICA CIEGO. El formulario no lleva ningún valor previo: ni el del
otro revisor, ni el de los 42 estudios que este proyecto ya tiene extraídos.
Prerrellenar aunque fuera "para ahorrar trabajo" destruiría la medida: la
concordancia entre dos revisores solo significa algo si el segundo no vio lo que
puso el primero. Por eso hay estudios ya extraídos en el formulario y aun así
salen en blanco -- ahí la doble extracción es precisamente la verificación.

EN ESPAÑOL, PERO EL DATO CANÓNICO SIGUE EN INGLÉS. Los encabezados son preguntas
en español y los desplegables traen los valores en español, porque quien extrae
lee papers, no código. El almacén (`phage_therapy_extraction_dataset.csv`), los
scripts de análisis y el manuscrito siguen en inglés; la traducción la hace
`extraction_schema.py` al comparar. Traducir el almacén habría roto todo lo que
está aguas abajo.

Una fila por BRAZO, no por estudio. Un brazo es un grupo de pacientes cuyos
desenlaces el artículo permite contar por separado -- en esta revisión suele ser
la clase de resistencia, no el grupo de tratamiento.

USO
    python scripts/make_extraction_forms.py --revisor "Nombre Apellido"
    python scripts/make_extraction_forms.py --revisor "Nombre" --muestra 40 --semilla 7
"""
import argparse
import csv
import datetime
import pathlib
import random
import sys

try:
    import openpyxl
    from openpyxl.comments import Comment
    from openpyxl.styles import Alignment, Font, PatternFill
    from openpyxl.utils import get_column_letter
    from openpyxl.worksheet.datavalidation import DataValidation
except ImportError:
    raise SystemExit("hace falta openpyxl: python -m pip install openpyxl")

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from extraction_schema import (CAMPOS, CATEGORICOS, CLAVE, ETIQUETAS, PREGUNTA,
                               VALORES_ES, valores_es)

ROOT = pathlib.Path(__file__).resolve().parent.parent
GRUPOS = ROOT / "revision_sistematica" / "cribado" / "study_groups.csv"
POOL = ROOT / "revision_sistematica" / "cribado" / "screening_stage2_priorizado.csv"
IDS = ROOT / "revision_sistematica" / "textos_completos" / "fulltext_identifiers.csv"
DEST = ROOT / "revision_sistematica" / "extraccion"

csv.field_size_limit(200_000_000)
try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

CAB = PatternFill("solid", fgColor="1F4E79")
CABF = Font(color="FFFFFF", bold=True)
FIJO = PatternFill("solid", fgColor="EDEDED")     # lo que no se toca
RELLENA = PatternFill("solid", fgColor="FFF2CC")  # lo que rellena el revisor

# Columnas de contexto: identifican el estudio, no se rellenan.
CONTEXTO = [("id_provisional", "Nº", "Clave con la que se cruzan las dos extracciones. NO la modifique."),
            ("orden", "Pos.", "Posición en el pozo cribado."),
            ("titulo", "Título del artículo", ""),
            ("revista", "Revista", ""),
            ("anio", "Año", ""),
            ("tipo_informe", "Tipo", "Artículo, resumen de congreso o ficha de registro."),
            ("como_recuperarlo", "Cómo encontrarlo", "DOI, PMID o identificador de registro."),
            ("enlace", "Abrir artículo", "Clic para abrirlo en el navegador.")]

ANCHOS = {"Nº": 9, "Pos.": 7, "Título del artículo": 58, "Revista": 24, "Año": 6,
          "Tipo": 17, "Cómo encontrarlo": 24, "Abrir artículo": 16,
          "Id del estudio (Autor+Año)": 22, "Brazo": 8,
          "¿Cómo define el AUTOR el éxito clínico?": 42,
          "¿Dónde viste estos datos?": 32,
          "Si algo quedó incompleto, ¿por qué?": 30,
          "Nivel de la revista": 26, "País del estudio": 20}


PAISES = ["Alemania", "Australia", "Bélgica", "Canadá", "China", "Corea del Sur",
          "Dinamarca", "Ecuador", "España", "Estados Unidos", "Francia", "Georgia",
          "India", "Irán", "Israel", "Italia", "Japón", "Letonia", "Países Bajos",
          "Polonia", "Reino Unido", "Rusia", "Singapur", "Suiza", "Turquía",
          "multicéntrico (Europa)", "multicéntrico (internacional)", "otro"]

NIVEL_REVISTA = ["alto", "medio", "bajo", "solo registro"]

# Pares que el emparejamiento automático no puede unir sin volverse peligroso.
# La abreviatura del corpus y el nombre completo del pozo comparten tan pocas
# palabras que aflojar el umbral para capturarlos volvería a colar falsos como
# "Critical Care" -> "Annals of Critical Care". Se nombran a mano, que es más
# largo de escribir y mucho más difícil de equivocar.
# Propuesta de nivel para revistas de circulación internacional reconocible.
# NO se escribe en la columna de decisión: va en una columna aparte marcada como
# propuesta, para que la confirme una persona. Se dejan deliberadamente fuera
# las revistas regionales y en otros idiomas -- rusas, ucranianas, polacas,
# cubana, japonesa, neerlandesa: no las conozco lo bastante, y rellenarlas de
# memoria sería meter una opinión mía disfrazada de dato en un artefacto de la
# revisión. Esas se buscan en Scimago.
PROPUESTA = {
    "the journal of heart and lung transplantation": "alto",
    "the journal of infectious diseases": "alto",
    "nephrology dialysis transplantation": "alto",
    "european journal of cardio-thoracic surgery": "alto",
    "europace": "alto",
    "journal of cystic fibrosis": "alto",
    "international journal of antimicrobial agents": "medio",
    "jac-antimicrobial resistance": "medio",
    "bmj open": "medio",
    "bmj open respiratory research": "medio",
    "frontiers in cellular and infection microbiology": "medio",
    "frontiers in microbiology": "medio",
    "frontiers in pharmacology": "medio",
    "international journal of molecular sciences": "medio",
    "biomedicines": "medio",
    "future microbiology": "medio",
    "virus research": "medio",
    "trials": "medio",
    "journal of chemotherapy": "medio",
    "journal of infection and chemotherapy": "medio",
    "folia microbiologica": "medio",
    "enfermedades infecciosas y microbiologia clinica": "medio",
    "phage: therapy, applications, and research": "medio",
    "current urology": "medio",
    "jaad case reports": "medio",
    "journal of plastic, reconstructive and aesthetic surgery": "medio",
    "journal of drug delivery science and technology": "medio",
    "the international journal of lower extremity wounds": "medio",
    "annals of vascular surgery - brief reports and innovations": "medio",
    "european urology, supplements": "medio",
    "cureus": "bajo",
    "clinical medicine insights: case reports": "bajo",
    "medicine in microecology": "bajo",
    "international journal of diabetes in developing countries": "bajo",
    "international journal of pediatrics and adolescent medicine": "bajo",
    "methods in molecular biology": "no aplica (serie de libros)",
}

ALIAS = {
    "american journal of respiratory and critical care medicine": "alto",
    "american journal of transplantation": "alto",
    "the journal of antimicrobial chemotherapy": "medio",
    "journal of the pediatric infectious diseases society": "medio",
    "evolution, medicine, and public health": "medio",
    "journal of investigative medicine high impact case reports": "medio",
}

# Abreviaturas del corpus -> nombre completo tal como viene en el pozo. El
# corpus escribe "Antimicrob Agents Chemother" y el registro bibliográfico
# "Antimicrobial agents and chemotherapy": sin normalizar, el mismo nivel se
# asignaría dos veces con dos nombres.
def clave_revista(nombre):
    """Clave de comparación entre el nombre del corpus y el del pozo.

    El corpus pega el editorial al título ("Viruses/MDPI", "Med/Cell Press") y
    el registro bibliográfico no. Sin quitarlo, 'Viruses' y 'Viruses/MDPI' son
    revistas distintas y el nivel ya decidido no se reutiliza.
    """
    import re
    n = (nombre or "").lower()
    n = re.split(r"[/(]", n)[0]           # fuera editorial y paréntesis
    n = re.split(r"\s:\s", n)[0]         # fuera "... : official publication of ..."
    n = re.sub(r"[^a-z ]", " ", n)
    fuera = {"the", "of", "and", "journal", "de", "la", "el", "for", "in", "a",
             "an", "official", "publication", "society", "america", "int",
             "international", "j"}
    # Las abreviaturas del corpus son prefijos de la palabra completa
    # ("Infect" de "infectious", "Respir" de "respiratory"), así que se compara
    # por prefijo de 5 letras. Truncar a 6 dejaba "int" y "intern" como tokens
    # distintos y separaba "Int J Infectious Diseases" de "International journal
    # of infectious diseases", que son la misma revista.
    return frozenset(w[:5] for w in n.split() if w and w not in fuera)


def niveles_del_corpus(ruta):
    """Nivel ya asignado a cada revista en el corpus extraído.

    No se inventa ninguno: solo se reutiliza lo que este proyecto ya decidió,
    para que el mismo título no acabe con dos niveles distintos según quién lo
    mire. Las revistas sin nivel previo salen en blanco, que es lo honesto.
    """
    import csv as _csv, re
    if not ruta.exists():
        return {}
    ES = {"high-tier": "alto", "mid-tier": "medio", "low-tier": "bajo",
          "registry-only": "solo registro"}
    out = {}
    with open(ruta, encoding="utf-8", newline="") as fh:
        for r in _csv.DictReader(fh):
            t = (r.get("journal_tier") or "").strip()
            if not t:
                continue
            nivel = ES.get(t.split("(")[0].strip())
            m = re.search(r"\((.*?)\)", t)
            if nivel and m:
                out[clave_revista(m.group(1))] = nivel
    return out


def nivel_para(clave, tabla):
    """Nivel de una revista, aceptando abreviatura o nombre completo.

    El corpus escribe "J Pediatric Infect Dis Soc" y el pozo "Journal of the
    Pediatric Infectious Diseases Society". Ningún emparejamiento exacto une
    esos dos; el de subconjunto sí, y recupera decisiones que este proyecto ya
    había tomado en vez de volver a tomarlas.
    """
    if clave in tabla:
        return tabla[clave]
    for k, v in tabla.items():
        if not k or not clave:
            continue
        # Subconjunto NO basta. {critic, care} está dentro de {annals, critic,
        # care}, así que "Critical Care" (Londres) le pasaba su nivel alto a
        # "Annals of Critical Care", que es una revista rusa distinta, y a
        # "Indian Journal of Critical Care Medicine". Se exige además que
        # coincida la mayor parte del nombre: dos títulos que comparten solo el
        # final genérico no son la misma revista.
        j = len(k & clave) / len(k | clave)
        if j >= 0.75:
            return v
    return ""

MOTIVOS_INCOMPLETO = [
    "NA",
    "texto completo no accesible",
    "el artículo no separa los datos de P. aeruginosa",
    "el artículo no reporta este desenlace",
    "solo resumen de congreso: datos limitados",
    "datos solo del estudio entero, no por brazo",
    "el antibiograma no permite clasificar la resistencia",
    "otro (explicar al lado)",
]


def enlace(rec, recuperado):
    """URL para abrir el artículo. Prioriza lo que resuelve de verdad.

    El DOI de Cochrane CENTRAL (10.1002/central/...) no lleva a ningún editorial,
    así que se salta: entre un enlace que no abre nada y ninguno, ninguno es
    mejor, porque el que no abre hace perder el tiempo dos veces.
    """
    doi = (rec.get("doi") or "").strip()
    if doi and not doi.lower().startswith("10.1002/central/"):
        return "https://doi.org/" + doi
    if (rec.get("pmid") or "").strip():
        return "https://pubmed.ncbi.nlm.nih.gov/%s/" % rec["pmid"].strip()
    if (rec.get("nct") or "").strip():
        return "https://clinicaltrials.gov/study/%s" % rec["nct"].strip()
    revista = (rec.get("journal") or "").strip()
    if revista.startswith("http"):
        return revista                      # ficha del ICTRP: la URL ya viene
    ident = (recuperado or "").strip()
    if ident.upper().startswith("NCT"):
        return "https://clinicaltrials.gov/study/" + ident
    if ident:
        return "https://trialsearch.who.int/?TrialID=" + ident
    return ""


def texto(ws, lineas):
    for linea, negrita in lineas:
        ws.append([linea])
        if negrita:
            ws.cell(ws.max_row, 1).font = Font(bold=True)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--revisor", required=True)
    ap.add_argument("--muestra", type=int, default=0,
                    help="extraer solo una muestra aleatoria de N estudios")
    ap.add_argument("--previo",
                    help="cuaderno anterior de ESTE revisor; su trabajo se "
                         "arrastra al nuevo formulario")
    ap.add_argument("--orden", choices=("prioridad", "pozo"), default="prioridad",
                    help="prioridad = comparativos primero (por defecto)")
    ap.add_argument("--semilla", type=int, default=20260805)
    args = ap.parse_args()

    with open(GRUPOS, encoding="utf-8", newline="") as fh:
        grupos = list(csv.DictReader(fh))
    with open(POOL, encoding="utf-8", newline="") as fh:
        pool = {p["record_id"]: p for p in csv.DictReader(fh)}
    recuperacion = {}
    if IDS.exists():
        with open(IDS, encoding="utf-8", newline="") as fh:
            for r in csv.DictReader(fh):
                recuperacion[r["orden"]] = (r["identificador_resuelto"] or r["via"])

    # Solo los estudios de los que se puede extraer algo. Los que únicamente
    # tienen ficha de registro no se extraen: se listan como estudios en curso.
    fuentes = [g for g in grupos if g["informe_para_extraer"] == "SI"
               and g["situacion"] in ("extraible", "solo-resumen")]
    # ORDEN DE TRABAJO. Por defecto van primero los disenos comparativos, que
    # son los unicos capaces de sostener una afirmacion de eficacia, y dentro de
    # ellos los que ya tienen el texto completo en disco. Extraer por posicion en
    # el pozo gasta las primeras horas en reportes de caso unico, que es lo que
    # menos aporta por hora invertida.
    COMPARATIVOS = {"RCT", "non-randomised trial"}
    SERIES = {"case series", "prospective cohort", "retrospective cohort"}
    pre_ext = {}
    p_pre = DEST / "pre_extraccion_desde_resumen.csv"
    if p_pre.exists():
        with open(p_pre, encoding="utf-8", newline="") as fh:
            pre_ext = {r["id_provisional"]: r for r in csv.DictReader(fh)}
    con_texto = set()
    for sub in ("pdf", "texto_html"):
        d = ROOT / "revision_sistematica" / "textos_completos" / sub
        if d.exists():
            con_texto |= {q.stem for q in d.iterdir()
                          if q.suffix.lower() in (".pdf", ".docx", ".txt")}

    def rango(g):
        eid = "EST-%03d" % int(g["estudio"])
        d = pre_ext.get(eid, {}).get("study_design", "")
        cat = 0 if d in COMPARATIVOS else (1 if d in SERIES else 2)
        return (cat, 0 if eid in con_texto else 1, int(g["orden"]))

    if args.orden == "prioridad":
        fuentes.sort(key=rango)
    else:
        fuentes.sort(key=lambda g: int(g["orden"]))
    if args.muestra and args.muestra < len(fuentes):
        random.Random(args.semilla).shuffle(fuentes)
        fuentes = sorted(fuentes[:args.muestra], key=lambda g: int(g["orden"]))
        muestreo = "muestra aleatoria de %d estudios (semilla %d)" % (args.muestra, args.semilla)
    else:
        muestreo = "los %d estudios extraíbles" % len(fuentes)

    wb = openpyxl.Workbook()

    # ---------------- Instrucciones ----------------
    ws = wb.active
    ws.title = "Instrucciones"
    texto(ws, [
        ("Formulario de extracción — %s" % args.revisor, True),
        ("%s · %s" % (datetime.date.today().isoformat(), muestreo), False),
        ("", False),
        ("Empiece por la hoja Ejemplo. Son dos estudios ya resueltos.", True),
        ("", False),
        ("Lo que no debe hacer", True),
        ("No abra el formulario del otro revisor ni el archivo de extracción del proyecto.", False),
        ("Hay 42 estudios que ya se extrajeron y aun así salen en blanco aquí, a propósito:", False),
        ("la comparación posterior solo mide algo si usted no vio lo que puso el otro.", False),
        ("", False),
        ("Las columnas", True),
        ("Grises (A a G): identifican el estudio. No se tocan. La primera, Nº, es la clave", False),
        ("con la que se cruzan las dos extracciones; si la cambia, se rompe el cruce.", False),
        ("Amarillas: son suyas. Pase el ratón por cada encabezado y sale una nota", False),
        ("explicando qué va en esa columna.", False),
        ("", False),
        ("Una fila por brazo", True),
        ("Un brazo es un grupo de pacientes cuyos desenlaces el artículo permite contar", False),
        ("aparte. Casi siempre eso significa clase de resistencia, no grupo de tratamiento.", False),
        ("Si hay varios: copie la fila entera, péguela debajo, deje el mismo Nº y cambie", False),
        ("el Brazo a B, C… Si el artículo no permite separarlos, una sola fila.", False),
        ("", False),
        ("NA y celda vacía no son lo mismo", True),
        ("NA quiere decir que el artículo no lo reporta. Vacío quiere decir que usted", False),
        ("todavía no lo ha mirado. El programa que compara los distingue.", False),
        ("", False),
        ("Los desplegables admiten texto", True),
        ("Si ninguna opción encaja, escriba encima: otra (instilación intravesical).", False),
        ("Lo que va entre paréntesis no afecta a la concordancia, así que explíquese.", False),
        ("", False),
        ("Al terminar", True),
        ("Guarde el archivo sin cambiarle el nombre y devuélvalo a quien coordina.", False),
    ])
    ws.column_dimensions["A"].width = 100

    # ---------------- Extraccion ----------------
    ws = wb.create_sheet("Extraccion")
    cabeceras = [c[1] for c in CONTEXTO] + [ETIQUETAS[c] for c in CAMPOS]
    campos_col = [None] * len(CONTEXTO) + list(CAMPOS)
    ws.append(cabeceras)
    for i, cab in enumerate(cabeceras, start=1):
        celda = ws.cell(1, i)
        celda.fill, celda.font = CAB, CABF
        celda.alignment = Alignment(vertical="center", wrap_text=True)
        ayuda = (PREGUNTA.get(campos_col[i - 1], "") if campos_col[i - 1]
                 else CONTEXTO[i - 1][2])
        if ayuda:
            celda.comment = Comment(ayuda, "Guía de extracción")
            # El de DTR es largo a propósito: es el campo que esta revisión ya
            # codificó mal una vez, y la nota corta invitaba a repetirlo.
            grande = campos_col[i - 1] == "dtr_status"
            celda.comment.width = 460 if grande else 320
            celda.comment.height = 250 if grande else 110
    ws.row_dimensions[1].height = 46

    # ARRASTRE. Lo que el revisor ya escribio se recupera de su cuaderno
    # anterior y se vuelca en el nuevo. Pedirle que reescriba trece estudios
    # porque el corpus cambio seria una forma segura de perder datos y de que
    # deje de fiarse del formulario. Se indexa por (estudio, brazo), de modo
    # que los estudios con varios brazos conservan cada uno el suyo.
    previo = {}
    if args.previo:
        vw = openpyxl.load_workbook(args.previo, read_only=True, data_only=True)
        vs = vw["Extraccion"]
        vfilas = list(vs.iter_rows(values_only=True))
        vcab = [str(c or "") for c in vfilas[0]]
        for fila in vfilas[1:]:
            if not fila or not fila[0] or not str(fila[0]).startswith("EST-"):
                continue
            eid = str(fila[0]).split()[0].strip()
            d = {vcab[i]: fila[i] for i in range(min(len(fila), len(vcab)))}
            brazo = str(d.get("Brazo", "A") or "A").strip() or "A"
            previo.setdefault(eid, {})[brazo] = d
        print("arrastrando trabajo previo de %d estudios" % len(previo))

    def escribe_fila(g, rec, ident, url, datos=None, brazo="A"):
        fila = ["EST-%03d" % int(g["estudio"]), int(g["orden"]),
                g["titulo"][:180], g["revista"], g["anio"], g["tipo_informe"],
                ident, "abrir" if url else ""]
        for c in CAMPOS:
            if c == "arm_id":
                fila.append(brazo)
            elif datos:
                # OJO CON EL CERO. `valor or ""` borra los ceros, porque en
                # Python 0 es falso: "0 eventos adversos" se convertia en celda
                # vacia y pasaba de ser un dato reportado a parecer un dato que
                # falta. En una revision sistematica eso no es un detalle de
                # formato, es un numerador alterado.
                v = datos.get(ETIQUETAS.get(c, c))
                fila.append("" if v is None else v)
            else:
                fila.append("")
        ws.append(fila)
        if url:
            celda = ws.cell(ws.max_row, 8)
            celda.hyperlink = url
            celda.font = Font(color="0563C1", underline="single")

    for g in fuentes:
        rec = pool[g["record_id"]]
        ident = (rec["doi"] if rec["doi"] and not rec["doi"].startswith("10.1002/central/")
                 else "") or rec["pmid"] or rec["nct"] or recuperacion.get(g["orden"], "")
        url = enlace(rec, recuperacion.get(g["orden"], ""))
        eid = "EST-%03d" % int(g["estudio"])
        if eid in previo:
            for brazo in sorted(previo[eid]):
                escribe_fila(g, rec, ident, url, previo[eid][brazo], brazo)
        else:
            escribe_fila(g, rec, ident, url)

    fin, n_ctx = ws.max_row, len(CONTEXTO)
    for r in range(2, fin + 1):
        for c in range(1, n_ctx + 1):
            ws.cell(r, c).fill = FIJO
        for c in range(n_ctx + 1, len(cabeceras) + 1):
            ws.cell(r, c).fill = RELLENA

    for campo in CATEGORICOS:
        col = get_column_letter(campos_col.index(campo) + 1)
        dv = DataValidation(type="list",
                            formula1='"%s"' % ",".join(valores_es(campo)),
                            allow_blank=True, showDropDown=False)
        # No se bloquea la escritura libre: "otra (…)" tiene que caber. Un
        # formulario que rechaza lo que el revisor de verdad leyó le empuja a
        # forzar el dato dentro de una categoría que no le corresponde.
        ws.add_data_validation(dv)
        dv.add("%s2:%s%d" % (col, col, fin + 80))

    # ---- validaciones de la R en adelante ----
    # Los recuentos NO llevan desplegable: el valor depende del estudio y una
    # lista fija sería falsa. Llevan algo más útil -- un tope: ningún desenlace
    # puede superar el nº de pacientes del brazo. Esa regla habría cazado sola
    # el "éxito clínico = 9 de 1 paciente" que apareció al probar el comparador.
    col_n = get_column_letter(campos_col.index("n_arm") + 1)
    for campo in ("clinical_success_n", "adverse_event_n", "microbio_eradication_n",
                  "mortality_n", "resistance_emergence_n"):
        col = get_column_letter(campos_col.index(campo) + 1)
        dv = DataValidation(
            type="custom",
            formula1='=OR({c}2="NA",AND(ISNUMBER({c}2),{c}2>=0,{c}2<=${n}2))'.format(c=col, n=col_n),
            allow_blank=True, showErrorMessage=True,
            errorTitle="Revise la cifra",
            error="Debe ser un entero entre 0 y el nº de pacientes del brazo, o NA "
                  "si el artículo no lo reporta.")
        ws.add_data_validation(dv)
        dv.add("%s2:%s%d" % (col, col, fin + 80))

    for campo, minimo in (("n_arm", 1), ("los_days", 0)):
        col = get_column_letter(campos_col.index(campo) + 1)
        dv = DataValidation(
            type="custom",
            formula1='=OR({c}2="NA",AND(ISNUMBER({c}2),{c}2>={m}))'.format(c=col, m=minimo),
            allow_blank=True, showErrorMessage=True,
            errorTitle="Revise la cifra",
            error="Un número (mínimo %d) o NA si el artículo no lo reporta." % minimo)
        ws.add_data_validation(dv)
        dv.add("%s2:%s%d" % (col, col, fin + 80))

    col = get_column_letter(campos_col.index("publication_year") + 1)
    dv = DataValidation(type="list", formula1='"%s"' % ",".join(str(a) for a in range(2006, 2027)),
                        allow_blank=True, showDropDown=False)
    ws.add_data_validation(dv)
    dv.add("%s2:%s%d" % (col, col, fin + 80))

    # Las listas largas van en una hoja aparte y se referencian por rango: una
    # lista escrita dentro de la validación no puede pasar de 255 caracteres, y
    # cuando se pasa Excel no avisa -- simplemente no muestra el desplegable.
    # ---- hoja de revistas ----
    # El nivel es un atributo de LA REVISTA, no del estudio. Pedir que se juzgue
    # 159 veces son 102 juicios repetidos (74 revistas aparecen una sola vez) y
    # una fuente segura de desacuerdos que no miden nada sobre la extracción.
    # Se decide una vez por revista, aquí.
    corpus_niveles = niveles_del_corpus(ROOT / "metaanalisis" / "datos" /
                                        "phage_therapy_extraction_dataset.csv")
    revistas = {}
    for g in fuentes:
        nombre = (g["revista"] or "(sin revista)").strip()
        k = clave_revista(nombre)
        if k not in revistas:
            base = nombre.lower().split(" : ")[0].strip()
            revistas[k] = [nombre, 0, ALIAS.get(base) or nivel_para(k, corpus_niveles)]
        revistas[k][1] += 1

    rev = wb.create_sheet("Revistas")
    texto(rev, [
        ("Nivel de cada revista — se decide UNA vez por revista, no por estudio", True),
        ("", False),
        ("Criterio de esta revisión (memo de estrategia, comprobación de falsación nº2):", False),
        ("el nivel es un indicador grueso, solo sirve para comprobar que la revista no", False),
        ("predice el resultado agrupado. No hace falta afinar: basta alto / medio / bajo.", False),
        ("", False),
        ("alto   revista general o de infecciosas de primera línea (Nature Microbiology,", False),
        ("       Lancet Infect Dis, Clinical Infectious Diseases, Nature Communications…)", False),
        ("medio  revista especializada con revisión por pares (Viruses, Antibiotics,", False),
        ("       Antimicrob Agents Chemother, Frontiers…)", False),
        ("bajo   revista local, sin indexación reconocible o sin revisión por pares clara", False),
        ("solo registro   no es una revista: es una ficha de ensayo", False),
        ("", False),
        ("Si duda, búsquela en scimagojr.com: Q1 y Q2 -> alto o medio; Q3, Q4 o sin", False),
        ("cuartil -> bajo. Anote la fuente en la última columna.", False),
        ("", False),
        ("Las que ya traen nivel salen del corpus ya extraído de este proyecto. No las", False),
        ("cambie sin motivo: cambiarlas descuadra los 42 estudios ya codificados.", False),
        ("", False)])
    encabezado = rev.max_row + 1
    rev.append(["Revista", "Estudios", "Nivel", "Propuesta (confirmar)", "Fuente / nota"])
    for c in range(1, 6):
        rev.cell(encabezado, c).fill, rev.cell(encabezado, c).font = CAB, CABF
    for nombre, n, nivel in sorted(revistas.values(), key=lambda x: (-x[1], x[0].lower())):
        base = nombre.lower().split(" : ")[0].split(" (")[0].strip()
        prop = "" if nivel else PROPUESTA.get(base, "")
        nota = ("corpus del proyecto" if nivel
                else "propuesta: confirmar" if prop
                else "buscar en scimagojr.com")
        rev.append([nombre, n, nivel, prop, nota])
        if not nivel:
            rev.cell(rev.max_row, 3).fill = RELLENA
    dv = DataValidation(type="list", formula1='"%s"' % ",".join(NIVEL_REVISTA),
                        allow_blank=True, showDropDown=False)
    rev.add_data_validation(dv)
    dv.add("C%d:C%d" % (encabezado + 1, rev.max_row))
    for c, ancho in (("A", 56), ("B", 10), ("C", 16), ("D", 22), ("E", 26)):
        rev.column_dimensions[c].width = ancho
    rev.freeze_panes = rev.cell(encabezado + 1, 1)
    primera_revista = encabezado + 1

    aux = wb.create_sheet("Listas")
    aux.append(["País", "Nivel de revista", "Motivo si quedó incompleto"])
    for i in range(max(len(PAISES), len(NIVEL_REVISTA), len(MOTIVOS_INCOMPLETO))):
        aux.append([PAISES[i] if i < len(PAISES) else None,
                    NIVEL_REVISTA[i] if i < len(NIVEL_REVISTA) else None,
                    MOTIVOS_INCOMPLETO[i] if i < len(MOTIVOS_INCOMPLETO) else None])
    for c, ancho in (("A", 30), ("B", 20), ("C", 48)):
        aux.column_dimensions[c].width = ancho
    for c in range(1, 4):
        aux.cell(1, c).fill, aux.cell(1, c).font = CAB, CABF

    for campo, columna_aux, n in (("geographic_source", "A", len(PAISES)),
                                  ("incomplete_reason", "C", len(MOTIVOS_INCOMPLETO))):
        col = get_column_letter(campos_col.index(campo) + 1)
        dv = DataValidation(type="list",
                            formula1="=Listas!$%s$2:$%s$%d" % (columna_aux, columna_aux, n + 1),
                            allow_blank=True, showDropDown=False)
        ws.add_data_validation(dv)
        dv.add("%s2:%s%d" % (col, col, fin + 80))

    # El nivel de cada fila se resuelve buscando la revista en la hoja Revistas.
    # Así el revisor no lo teclea 159 veces y, sobre todo, la misma revista no
    # puede acabar con dos niveles distintos en dos filas del mismo archivo.
    # La fila de inicio se toma de la hoja recién construida. Escribirla a mano
    # ya falló una vez: puse 22 cuando los datos empezaban en la 21, y la
    # primera revista de la lista -- la más frecuente -- no se habría encontrado.
    fila_ini = primera_revista
    for r in range(2, fin + 1):
        ws.cell(r, campos_col.index("journal_tier") + 1).value = (
            '=IFERROR(IF(VLOOKUP(D{r},Revistas!$A${i}:$C$400,3,FALSE)=0,"",'
            'VLOOKUP(D{r},Revistas!$A${i}:$C$400,3,FALSE)),"")'.format(r=r, i=fila_ini))

    for i, cab in enumerate(cabeceras, start=1):
        ws.column_dimensions[get_column_letter(i)].width = ANCHOS.get(cab, 18)
    ws.freeze_panes = ws.cell(2, n_ctx + 1)

    # ---------------- Diccionario ----------------
    ws = wb.create_sheet("Diccionario")
    ws.append(["Columna", "Qué se contesta", "Opciones"])
    for c in range(1, 4):
        ws.cell(1, c).fill, ws.cell(1, c).font = CAB, CABF
    for campo in CAMPOS:
        ws.append([ETIQUETAS[campo], PREGUNTA.get(campo, ""),
                   " · ".join(valores_es(campo)) if campo in CATEGORICOS else ""])
    for col, ancho in (("A", 38), ("B", 86), ("C", 52)):
        ws.column_dimensions[col].width = ancho
    for r in range(2, ws.max_row + 1):
        for c in range(1, 4):
            ws.cell(r, c).alignment = Alignment(vertical="top", wrap_text=True)

    # ---------------- Ejemplo ----------------
    # Va DENTRO del libro para que siga estando cuando alguien lo reabra en tres
    # semanas. Son dos estudios reales ya extraídos, elegidos porque enseñan lo
    # que no es evidente: sobre todo que un brazo se separa por clase de
    # resistencia y no por grupo de tratamiento.
    ws = wb.create_sheet("Ejemplo")
    texto(ws, [
        ("Dos ejemplos resueltos", True),
        ("Salen de estudios que ya se extrajeron en este proyecto.", False), ("", False),
        ("EJEMPLO 1 — un solo brazo", True),
        ("Tkhilaishvili 2020. Un paciente con infección de prótesis por P. aeruginosa XDR,", False),
        ("tratado con fago más antibiótico por vía local. Curó.", False), ("", False)])
    ws.append(["Columna", "Qué escribí", "Por qué"])
    for c in range(1, 4):
        ws.cell(ws.max_row, c).fill, ws.cell(ws.max_row, c).font = CAB, CABF
    for campo, valor, nota in [
            ("study_id", "Tkhilaishvili2020", "apellido pegado al año"),
            ("arm_id", "A", "un solo brazo"),
            ("n_arm", "1", "pacientes de este brazo"),
            ("pathogen_scope", VALORES_ES["Pseudomonas-only"], ""),
            ("resistance_class", "XDR", "según el antibiograma"),
            ("resistance_class_source", VALORES_ES["independently-verified"],
             "lo verifiqué yo con Magiorakos; no me fié de la etiqueta del autor"),
            ("dtr_status", VALORES_ES["not-derivable"], "el artículo no da lo necesario"),
            ("route", VALORES_ES["topical/local"], ""),
            ("modality", VALORES_ES["phage+antibiotic combination"], ""),
            ("clinical_success_n", "1", "de 1 paciente"),
            ("clinical_success_definition",
             "Infección erradicada; sin dolor, PCR normal, sin aflojamiento a 10 meses",
             "la definición DEL AUTOR, copiada, no la mía"),
            ("adverse_event_n", "0", "cero notificados; NO es lo mismo que NA"),
            ("microbio_eradication_n", "1", ""),
            ("mortality_n", "0", ""),
            ("los_days", "NA", "el artículo no lo dice"),
            ("resistance_emergence_n", "NA", "el artículo no lo dice"),
            ("study_design", VALORES_ES["case report"], ""),
            ("publication_year", "2020", ""),
            ("journal_tier", "medio (Antimicrob Agents Chemother)", ""),
            ("geographic_source", "Alemania (Berlín)", ""),
            ("extraction_citation", "pp.1-2 Case Presentation; Tabla 1 antibiograma",
             "dónde lo vi; obligatorio para cualquier cifra"),
            ("extraction_status", VALORES_ES["COMPLETE"], ""),
            ("incomplete_reason", "NA", "")]:
        ws.append([ETIQUETAS[campo], valor, nota])
        ws.cell(ws.max_row, 2).fill = RELLENA

    texto(ws, [
        ("", False), ("EJEMPLO 2 — varios brazos", True),
        ("Pirnay 2024, cohorte de 100 casos. Aquí está el error más común:", False),
        ("los brazos NO son grupos de tratamiento, son clases de resistencia.", True),
        ("Todos los pacientes recibieron lo mismo, fago más antibiótico. Lo que separa", False),
        ("las filas es que el artículo permite contar desenlaces aparte en XDR, MDR y PDR.", False),
        ("Se copia la fila tres veces, con el MISMO Nº y el Brazo en A, B y C.", False), ("", False)])
    ws.append(["Brazo", "Clase de resistencia", "Pacientes", "Éxito clínico",
               "Eventos adversos", "Fallecidos"])
    for c in range(1, 7):
        ws.cell(ws.max_row, c).fill, ws.cell(ws.max_row, c).font = CAB, CABF
    for fila in (["A", "XDR", 7, 6, 2, 2], ["B", "MDR", 23, 16, 4, 2],
                 ["C", "PDR", 2, 1, 0, 0]):
        ws.append(fila)
        for c in range(1, 7):
            ws.cell(ws.max_row, c).fill = RELLENA
    texto(ws, [
        ("", False),
        ("El resto de columnas (vía, modalidad, revista, país…) se repite igual en las tres.", False),
        ("Si el artículo NO permite separar por clase de resistencia, no invente brazos:", False),
        ("una sola fila y la clase en 'no clasificable'.", False)])
    for col, ancho in (("A", 34), ("B", 52), ("C", 58)):
        ws.column_dimensions[col].width = ancho

    DEST.mkdir(parents=True, exist_ok=True)
    slug = "".join(ch if ch.isalnum() else "_" for ch in args.revisor).strip("_").lower()
    out = DEST / ("extraccion_%s.xlsx" % slug)
    wb.save(out)
    print("escrito %s" % out)
    print("  %s · %d columnas por rellenar" % (muestreo, len(CAMPOS)))


if __name__ == "__main__":
    main()
