"""Closed vocabulary for stage-2 exclusion reasons.

WHY A CLOSED LIST. Free-text reasons written batch by batch drift: the same
decision came out as "trabajo de laboratorio o modelizacion" in one batch and
"trabajo de laboratorio, preclinico o de modelizacion" in the next, and the
counts then split across two rows that mean one thing. PRISMA asks for exclusions
grouped by reason, so the grouping has to be stable or it has to be redone by
hand at the end -- which is how transcription errors get in.

SIX CODES, AND NO MORE. If a record does not fit one of these, it does not get a
seventh code invented for it on the spot: it advances to stage 3, where a human
reads the abstract. A new code is a change to the protocol and is added here
deliberately, not mid-batch.

THE ORIGINAL WORDING IS NOT DESTROYED. Normalisation adds a code alongside the
text that was actually written at decision time; it never rewrites the log. A
reader can always see both what was decided and how it was phrased.
"""

CODES = {
    "ORG": "Organismo distinto de P. aeruginosa, sin subgrupo separable",
    "REV": "Revision narrativa o comentario, sin datos primarios propios",
    "SEC": "Sintesis secundaria (revision sistematica o scoping)",
    "LAB": "Trabajo de laboratorio, preclinico o de modelizacion; sin pacientes tratados",
    "VET": "Aislados o infeccion veterinaria, no humana",
    "OFF": "No evalua fagoterapia en pacientes (encuesta, epidemiologia, prensa, otra terapia)",
}

# Patrones que mapean el texto libre ya registrado a su codigo. Se evaluan en
# orden; el primero que coincide gana. Deliberadamente estrictos: cualquier
# motivo que no coincida se reporta en vez de asignarse a una categoria por
# defecto, porque una asignacion silenciosa es indistinguible de un error.
PATTERNS = [
    # Frases en ingles heredadas del brazo de etapa 3 indexado por PMID. Van
    # primero por una razon concreta: "narrative or systematic review with no
    # primary patient data" es una disyuncion -- el revisor no distinguio el
    # diseno, y lo decisivo fue la ausencia de datos primarios propios. Agrupa
    # en REV, no en SEC, porque SEC afirma que el registro ES una sintesis
    # secundaria y aqui eso no consta. Sin esta precedencia, el patron generico
    # "systematic review" se lo llevaria a SEC e inflaria ese recuento con
    # registros cuyo diseno nunca se determino.
    ("REV", r"narrative (or systematic )?review|commentary"),
    ("ORG", r"not P\. aeruginosa"),
    ("SEC", r"systematic review|scoping review|meta-analysis"),
    ("VET", r"veterinari|equina|animal, no humana"),
    ("SEC", r"sintesis secundaria|revision sistematica|scoping"),
    ("REV", r"revision|comentario"),
    ("LAB", r"laboratorio|preclinic|modelizacion"),
    ("OFF", r"no evalua fagoterapia|encuesta|prensa"),
    ("ORG", r"organismo distinto|E\. coli|Achromobacter|Klebsiella|Acinetobacter|"
            r"Mycobacterium|Enterococcus|MRSA|Staphylococcus|Burkholderia|Shigella|"
            r"Stenotrophomonas|Enterobacteriaceae|Enterobacter"),
]


def code_for(reason):
    """Devuelve el codigo, o None si el texto no corresponde a ninguno."""
    import re
    r = (reason or "").lower()
    for code, pat in PATTERNS:
        if re.search(pat, r, re.I):
            return code
    return None
