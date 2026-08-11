"""Esquema compartido de extracción: campos, vocabularios y normalización.

Un solo sitio define qué campos se extraen, qué valores admite cada uno y cómo
se normaliza un valor antes de medir concordancia. Los dos scripts que forman
la doble extracción -- el que genera los formularios y el que los compara --
leen de aquí, para que el formulario no pueda ofrecer un valor que el
comparador no sepa puntuar.

POR QUÉ NORMALIZAR ANTES DE MEDIR. `route` tiene 23 valores distintos en el
corpus, pero casi todos son `other (...)` con el paréntesis redactado de otra
forma. Comparados literalmente, dos revisores que codificaron ambos "otra vía"
contarían como desacuerdo por escribir el paréntesis distinto, y la kappa
saldría hundida por un artefacto de redacción. La concordancia se mide sobre la
categoría; el texto literal se conserva y se muestra en la lista de conflictos.
"""
import re

# Campos que identifican la fila. No se puntúan: son la clave de emparejamiento.
CLAVE = ["study_id", "arm_id"]

# Categóricos con vocabulario cerrado -> kappa de Cohen.
CATEGORICOS = {
    "pathogen_scope": ["Pseudomonas-only", "mixed-pathogen-with-Pseudomonas-subgroup"],
    "resistance_class": ["MDR", "XDR", "PDR", "below-MDR-threshold", "not-classifiable"],
    "resistance_class_source": ["author-reported", "independently-verified",
                                "not-classifiable"],
    "dtr_status": ["yes", "no", "not-derivable"],
    "route": ["IV", "inhaled/nebulized", "topical/local", "oral", "intravesical",
              "intra-articular", "other", "NA"],
    "modality": ["phage monotherapy", "phage+antibiotic combination",
                 "phage+other", "NA"],
    "study_design": ["RCT", "case report", "case series", "retrospective cohort",
                     "prospective cohort", "non-randomised trial", "other"],
    "extraction_status": ["COMPLETE", "PARTIAL", "EXTRACTION_INCOMPLETE"],
}

# Numéricos -> concordancia exacta y diferencia absoluta. "NA" es un valor
# legítimo: significa "no notificado", que es distinto de cero y no debe
# convertirse en cero al comparar.
NUMERICOS = ["n_arm", "clinical_success_n", "adverse_event_n",
             "microbio_eradication_n", "mortality_n", "los_days",
             "resistance_emergence_n", "publication_year"]

# Texto libre -> no se puntúa; se lista para revisión visual. Son justamente los
# campos donde dos redacciones distintas pueden decir lo mismo.
TEXTO = ["clinical_success_definition", "journal_tier", "geographic_source",
         "extraction_citation", "incomplete_reason"]

CAMPOS = CLAVE + list(CATEGORICOS) + NUMERICOS + TEXTO


def normaliza(campo, valor):
    """Valor comparable: recorta el paréntesis explicativo y unifica may/min.

    Devuelve None cuando la celda está vacía, para poder distinguir "no
    contestado" de "contestado NA", que no son lo mismo: lo primero es una
    laguna del formulario y lo segundo una decisión del revisor.
    """
    v = (valor or "").strip()
    if not v:
        return None
    if campo in CATEGORICOS:
        v = re.sub(r"\s*\(.*\)\s*$", "", v).strip()   # "other (intravesical)" -> "other"
        v = v.lower()
        # Un formulario en español y otro en inglés tienen que poder compararse:
        # ambos se llevan al valor canónico antes de medir nada.
        if v in VALOR_DE_ES:
            return VALOR_DE_ES[v]
        for canon in CATEGORICOS[campo]:
            if canon.lower() == v:
                return canon
        # cualquier variante no prevista de "other ..." cae en la categoría other
        if v.startswith("other"):
            return "other"
        return v
    if campo in NUMERICOS:
        if v.upper() in ("NA", "N/A", "NR", "-"):
            return "NA"
        try:
            f = float(v.replace(",", "."))
            return str(int(f)) if f == int(f) else str(f)
        except ValueError:
            return v.lower()
    return v.lower()


# ---------------------------------------------------------------------------
# CAPA DE TRADUCCIÓN
#
# El formulario se rellena en español; el dato canónico sigue en inglés. No es
# capricho: `metaanalisis/datos/phage_therapy_extraction_dataset.csv`, los scripts de
# análisis y el manuscrito usan esos nombres, y traducir el almacén rompería
# todo lo que hay aguas abajo. Se traduce en la entrada y en la salida, y el
# comparador acepta indistintamente un formulario en español o en inglés.
# La etiqueta es lo que LEE la persona; el campo canónico es lo que guarda el
# dataset. Un encabezado como `ambito_patogeno` es de programador y obliga a
# consultar un instructivo aparte cada vez; una pregunta en español se contesta
# sin salir de la celda.
ETIQUETAS = {
    "study_id": "Id del estudio (Autor+Año)",
    "arm_id": "Brazo",
    "n_arm": "Pacientes en este brazo",
    "pathogen_scope": "¿Solo P. aeruginosa o mixto?",
    "resistance_class": "Clase de resistencia",
    "resistance_class_source": "¿De dónde sale esa clase?",
    "dtr_status": "¿Cumple criterio DTR?",
    "route": "Vía de administración",
    "modality": "¿Fago solo o con antibiótico?",
    "study_design": "Diseño del estudio",
    "extraction_status": "Estado de esta extracción",
    "clinical_success_n": "Éxito clínico (nº pacientes)",
    "adverse_event_n": "Eventos adversos (nº)",
    "microbio_eradication_n": "Erradicación microbiológica (nº)",
    "mortality_n": "Fallecidos (nº)",
    "los_days": "Estancia hospitalaria (días)",
    "resistance_emergence_n": "Aparición de resistencia al fago (nº)",
    "publication_year": "Año de publicación",
    "clinical_success_definition": "¿Cómo define el AUTOR el éxito clínico?",
    "journal_tier": "Nivel de la revista",
    "geographic_source": "País del estudio",
    "extraction_citation": "¿Dónde viste estos datos?",
    "incomplete_reason": "Si algo quedó incompleto, ¿por qué?",
}

# Ayuda que se muestra al pasar el ratón por el encabezado y en el Diccionario.
PREGUNTA = {
    "study_id": "Apellido del primer autor pegado al año: Tkhilaishvili2020. Sin espacios ni tildes.",
    "arm_id": "A si el estudio da un solo grupo de datos. Si separa desenlaces por clase de resistencia, usa A, B, C.",
    "n_arm": "Cuántos pacientes hay en ESTE brazo, no en todo el estudio.",
    "pathogen_scope": "Solo Pseudomonas si todos los pacientes tenían P. aeruginosa. Mixto si había otras bacterias PERO el artículo permite separar los de Pseudomonas.",
    "resistance_class": "MDR, XDR o PDR según Magiorakos. Si el antibiograma no alcanza para clasificar, pon 'no clasificable'.",
    "resistance_class_source": "¿Lo dice el autor y lo aceptaste, o lo verificaste tú con el antibiograma? Importa para el riesgo de sesgo.",
    "dtr_status": (
        "Difficult-to-Treat Resistance (Kadri 2018, PMID 30052813). NO es MDR con otro nombre: "
        "pregunta si se agotaron los antibióticos de PRIMERA LÍNEA (carbapenémicos, otros "
        "betalactámicos, fluoroquinolonas). Los de RESERVA -- colistina, aminoglucósidos, "
        "tigeciclina -- y los posteriores a 2018 -- ceftazidima-avibactam, cefiderocol -- NO "
        "cuentan: son aquello a lo que el DTR obliga a recurrir.\n"
        "SÍ: el artículo documenta sensibilidad SOLO a agentes de reserva.\n"
        "NO: basta UN agente de primera línea sensible documentado.\n"
        "NO DERIVABLE: el resto.\n"
        "Ojo: esta revisión ya definió mal este campo una vez (exigía 'todos los "
        "betalactámicos', más estricto que Kadri) y fabricó no-derivabilidad. Si duda entre "
        "'no' y 'no derivable', mire si hay UN solo agente de primera línea sensible."),
    "route": "Por dónde se administró el fago. Si fueron varias vías, elige 'otra' y explica en el paréntesis.",
    "modality": "¿El fago fue solo, o junto con antibióticos?",
    "study_design": "Lo que el artículo ES, no lo que dice ser. Un 'estudio' de un paciente es un caso clínico.",
    "extraction_status": "COMPLETA si sacaste todo lo que el artículo daba. PARCIAL o INCOMPLETA si te faltó algo, y explícalo en la última columna.",
    "clinical_success_n": "Cuántos pacientes de este brazo mejoraron, según la definición del propio autor. Si no lo reporta, NA.",
    "adverse_event_n": "Cuántos pacientes tuvieron algún evento adverso. Cero notificados se escribe 0, no NA.",
    "microbio_eradication_n": "En cuántos desapareció la bacteria en cultivo.",
    "mortality_n": "Cuántos fallecieron durante el seguimiento.",
    "los_days": "Días de hospitalización. Casi ningún caso clínico lo reporta: NA es lo normal aquí.",
    "resistance_emergence_n": "En cuántos apareció resistencia al fago durante el tratamiento.",
    "publication_year": "Año del artículo.",
    "clinical_success_definition": "COPIA la definición del autor, no escribas la tuya. Es lo que después permite ver si todos midieron lo mismo.",
    "journal_tier": "Nombre de la revista, y si es de alto o medio impacto: 'alto (Nature Microbiology)'.",
    "geographic_source": "País y ciudad si consta: 'Alemania (Berlín)'.",
    "extraction_citation": "Página, tabla o figura de donde sacaste los números: 'p.3 Results, Tabla 2'. Obligatorio para cualquier cifra.",
    "incomplete_reason": "Qué faltó y por qué. NA si no faltó nada.",
}

CAMPO_DE_ETIQUETA = {v: k for k, v in ETIQUETAS.items()}

VALORES_ES = {
    "Pseudomonas-only": "solo Pseudomonas",
    "mixed-pathogen-with-Pseudomonas-subgroup": "mixto con subgrupo de Pseudomonas",
    "below-MDR-threshold": "por debajo del umbral MDR",
    "not-classifiable": "no clasificable",
    "author-reported": "declarado por el autor",
    "independently-verified": "verificado de forma independiente",
    "yes": "si", "no": "no", "not-derivable": "no derivable",
    "inhaled/nebulized": "inhalada/nebulizada",
    "topical/local": "topica/local",
    "oral": "oral", "intravesical": "intravesical",
    "intra-articular": "intraarticular",
    "other": "otra", "IV": "IV", "NA": "NA",
    "phage monotherapy": "fago en monoterapia",
    "phage+antibiotic combination": "fago + antibiotico",
    "phage+other": "fago + otro",
    "RCT": "ECA", "case report": "caso clinico", "case series": "serie de casos",
    "retrospective cohort": "cohorte retrospectiva",
    "prospective cohort": "cohorte prospectiva",
    "non-randomised trial": "ensayo no aleatorizado",
    "COMPLETE": "COMPLETA", "PARTIAL": "PARCIAL",
    "EXTRACTION_INCOMPLETE": "INCOMPLETA",
}
# `other` traduce a "otra" en via_administracion y a "otro" en diseno_estudio;
# ambas formas tienen que volver a la misma categoría canónica.
VALOR_DE_ES = {v.lower(): k for k, v in VALORES_ES.items()}
VALOR_DE_ES["otro"] = "other"
VALOR_DE_ES["sí"] = "yes"


def valores_es(campo):
    """Vocabulario cerrado del campo, en español, para el desplegable."""
    return [VALORES_ES.get(v, v) for v in CATEGORICOS.get(campo, [])]


def a_canonico(campo, valor):
    """Traduce un valor escrito en español al canónico inglés.

    Tolera el paréntesis explicativo: 'otra (instilación intravesical)' vuelve
    como 'other', que es la categoría con la que se mide la concordancia.
    """
    v = (valor or "").strip()
    if not v:
        return v
    base = re.sub(r"\s*\(.*\)\s*$", "", v).strip().lower()
    return VALOR_DE_ES.get(base, v)
