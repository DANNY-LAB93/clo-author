"""Resuelve cómo recuperar los informes que pasan a texto completo sin DOI útil.

EL CUELLO DE BOTELLA NO ERA EL QUE PARECÍA. Un primer recuento dijo que 80 de
los 268 informes no se podían descargar automáticamente. Eran 45: la función de
estado comprobaba el DOI sustituto de Cochrane CENTRAL (10.1002/central/...)
ANTES que el PMID, así que marcaba como irrecuperables 35 registros que sí
tenían PMID o NCT. Y de los 45 restantes, 17 llevaban su identificador de
registro dentro del campo `journal`, en la URL de trialsearch.who.int -- es
decir, la mayor parte del problema era de lectura del propio registro, no de
falta de información.

Este script deja por escrito, para cada informe sin DOI editorial, QUÉ hay que
hacer para conseguirlo, y por qué vía. No inventa identificadores: cuando no hay
nada que extraer, lo dice.

SALIDA
    revision_sistematica/textos_completos/fulltext_identifiers.csv

USO
    python scripts/resolve_fulltext_ids.py
"""
import csv
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
POOL = ROOT / "revision_sistematica" / "cribado" / "screening_stage2_priorizado.csv"
S3 = ROOT / "revision_sistematica" / "cribado" / "screening_stage3_pool_decisions.csv"
OUT = ROOT / "revision_sistematica" / "textos_completos" / "fulltext_identifiers.csv"

csv.field_size_limit(200_000_000)
try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

# Códigos de protocolo que estos patrocinadores usan como identificador público
# cuando el registro no trae ni DOI ni NCT. Se extraen del título porque es
# donde CTIS y EudraCT los ponen.
PROTOCOLO = re.compile(
    r"\b(PHRC-[A-Z]/\d{4}/[A-Z0-9\-]+"      # PHRC francés
    r"|Phage4Cure-\d+"                       # Phage4Cure
    r"|BMX-\d+-\d+"                          # BiomX
    r"|[A-Z]{2,6}-\d{2,4}-\d{3,4})\b")       # forma genérica patrocinador-año-nº

STOP = set("a an the of for in on with and or to by at from is are as be study trial".split())

# ---------------------------------------------------------------------------
# ATRIBUCIONES HECHAS A MANO, CON SU JUSTIFICACIÓN
#
# Un resumen de congreso rara vez lleva DOI propio, pero casi siempre es un
# informe de un ensayo que YA está identificado en el pozo. Atribuirlo cierra la
# recuperación sin inventar nada: el texto que se recupera es el del ensayo.
# Cada línea dice en qué se apoya. Las siete primeras no se deducen del parecido
# del título -- se apoyan en que el propio resumen, leído durante el cribado,
# nombra el producto BX004-A.
# Curación a mano, indexada por record_id y NUNCA por posición en el pozo. La
# posición depende del manifiesto de fuentes: al incorporar BVS el pozo pasó de
# 13 509 a 13 894 registros y las posiciones por encima de la primera inserción
# se desplazaron, de modo que estas atribuciones habrían pasado a asignar el NCT
# del BX004-A a informes ajenos. El síntoma fue que el BX004-A y el TP-102 se
# partieron en dos estudios cada uno. El record_id se deriva del contenido y
# sobrevive a cualquier reconstrucción del corpus.
ATRIBUCION = {
    "R55112b0914": ("NCT05010577", "el resumen nombra BX004-A (OFID 2023, IDWeek)"),
    "R28423b4c7c": ("NCT05010577", "el resumen nombra BX004-A (J Cyst Fibros 2023)"),
    "R793249bfc4": ("NCT05010577", "el resumen nombra BX004-A (J Cyst Fibros 2023)"),
    "R7b2a90b3b7": ("NCT05010577", "el resumen nombra BX004-A (Eur Respir J 2023)"),
    "Rc29fe2424c": ("NCT05010577", "el resumen nombra BX004-A (J Cyst Fibros 2024, WS06.06)"),
    "Rc4889b04ba": ("NCT05010577", "el resumen nombra BX004-A (Eur Respir J 2024)"),
    "R71b87ec1f2": ("NCT05010577", "el resumen nombra BX004-A (J Cyst Fibros 2024)"),
    "R3608cade6a": ("NCT05010577", "ficha EudraCT del mismo Ph1b/2a de BX004 nebulizado en FQ"),
    "R9c54b30733": ("NCT04684641", "CYPHY: título idéntico al informe R64f4b4a1a4"),
    "Rcea9abc521": ("NCT04684641", "CYPHY: título idéntico al informe R64f4b4a1a4"),
    "Rdd0e4fa658": ("NCT04684641", "CYPHY: título idéntico al informe R64f4b4a1a4"),
    "Rc27a7629de": ("NCT02116010", "PhagoBurn: único ensayo fase I-II de fagos en quemados por P. aeruginosa"),
    "R36f8e8613e": ("NCT04803708", "el resumen evalúa TP-102 en pie diabético (OFID 2022)"),
    "R326c83d964": ("NCT03140085", "resultados del ECA de Leitner en RTUP; publicado como PMID 28950849"),
    "R35097ad062": ("pmid:30131795", "mismo título que el informe indexado del mismo grupo"),
    "R9d091cf924": ("10.1016/j.jddst.2023.104486", "mismo título que su informe hermano"),
    "Ra4e9fbb2ff": ("10.4103/ijpam.ijpam_1_24", "mismo título que su informe hermano"),
}

# Comprobado contra PubMed el 2026-08-05: no están indexados allí. No es un
# fallo de búsqueda, es que no tienen PMID. Se recuperan por su cita.
SIN_PMID = {
    "Re9fa49ae6d": "Int J Diabetes Dev Ctries 2025",
    "R99c5855b1c": "Pharmaceutisch Weekblad 2025",
    "Raa2e529a17": "Eur Urol Suppl 2016 (informe previo del grupo de Leitner)",
    "Rcb6a2ca7d4": "Jpn J Clin Ophthalmol 2021",
    "R4a198d51c5": "Surgical Chronicles 2016",
    "R95ed8fa775": "Nephrol Dial Transplant 2020 (resumen de congreso)",
    "R9e51826497": "Rev Cubana Angiol Cir Vasc 2017",
}


def real_doi(r):
    d = (r["doi"] or "").strip().lower()
    return bool(d) and not d.startswith("10.1002/central/")


def toks(t):
    return {w for w in re.findall(r"[a-z0-9]+", (t or "").lower())
            if w not in STOP and len(w) > 2}


def clasificar(r):
    """(tipo, identificador, via, nota) para un informe sin DOI editorial."""
    revista = (r["journal"] or "").strip()

    m = re.search(r"TrialID=([^\s&]+)", revista)
    if m:
        tid = m.group(1)
        return ("ficha de registro (ICTRP)", tid,
                "trialsearch.who.int / registro nacional",
                "el identificador venía en el campo journal del propio registro")

    if not revista:
        m = PROTOCOLO.search(r["title"] or "")
        fuente = (r["sources"] or "").strip()
        if m:
            return ("ficha de registro (%s)" % (fuente or "registro"), m.group(1),
                    "portal CTIS / EudraCT por código de protocolo",
                    "código extraído del título")
        return ("ficha de registro (%s)" % (fuente or "registro"), "",
                "portal CTIS / EudraCT por título y patrocinador",
                "SIN código de protocolo en el título: localización manual")

    congreso = "conference" in (r["doctype"] or "").lower()
    tipo = "resumen de congreso" if congreso else "artículo"
    cita = "%s %s" % (revista, r["year"] or "s/f")
    return (tipo, "", "búsqueda por cita: %s" % cita,
            "indexado en Cochrane CENTRAL sin DOI editorial propio"
            if congreso else "publicación sin DOI en el registro")


def main():
    with open(POOL, encoding="utf-8", newline="") as fh:
        pool = list(csv.DictReader(fh))
    por_id = {p["record_id"]: p for p in pool}
    with open(S3, encoding="utf-8", newline="") as fh:
        s3 = {d["record_id"]: d for d in csv.DictReader(fh)}

    ft = [por_id[rid] for rid, d in s3.items()
          if d["verdict"] == "FULLTEXT" and rid in por_id]
    ft.sort(key=lambda r: int(r["orden"]))
    identificados = [r for r in ft if real_doi(r) or r["pmid"].strip() or r["nct"].strip()]
    huerfanos = [r for r in ft if r not in identificados]

    # Duplicado interno: mismo título que un informe YA identificado. Solo se
    # acepta con solapamiento alto; por debajo se deja en blanco antes que
    # arriesgar una atribución falsa, que es el error que ya contaminó el índice
    # de controles positivos de esta revisión.
    idtoks = [(p, toks(p["title"])) for p in identificados]
    filas = []
    for r in huerfanos:
        th = toks(r["title"])
        mejor, sim = None, 0.0
        for p, tp in idtoks:
            if not tp:
                continue
            j = len(th & tp) / len(th | tp)
            if j > sim:
                mejor, sim = p, j
        tipo, ident, via, nota = clasificar(r)
        if not ident and r["record_id"] in ATRIBUCION:
            ident, razon = ATRIBUCION[r["record_id"]]
            via = "informe de un ensayo ya identificado"
            nota = razon
        elif not ident and r["record_id"] in SIN_PMID:
            via = "cita: %s" % SIN_PMID[r["record_id"]]
            nota = ("comprobado contra PubMed el 2026-08-05: no indexado; "
                    "no tiene PMID que buscar")
        dup = ""
        if mejor is not None and sim >= 0.80:
            dup = "duplicado probable de la posición %s (solapamiento %.2f)" % (
                mejor["orden"], sim)
        filas.append({
            "orden": r["orden"], "record_id": r["record_id"], "tipo": tipo,
            "identificador_resuelto": ident, "via": via, "nota": nota,
            "duplicado_interno": dup,
            "titulo": " ".join(r["title"].split()),
            "revista": r["journal"], "anio": r["year"], "fuentes": r["sources"],
        })

    with open(OUT, "w", encoding="utf-8", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(filas[0].keys()))
        w.writeheader()
        w.writerows(filas)

    con = sum(1 for f in filas if f["identificador_resuelto"])
    dup = sum(1 for f in filas if f["duplicado_interno"])
    print("informes a texto completo            : %d" % len(ft))
    print("  con DOI editorial, PMID o NCT      : %d" % len(identificados))
    print("  sin identificador directo          : %d" % len(huerfanos))
    print("     identificador recuperado del registro : %d" % con)
    print("     además, duplicado interno probable    : %d" % dup)
    sin = [f for f in filas if not f["identificador_resuelto"]]
    print("     resueltos por cita verificada        : %d"
          % sum(1 for f in sin if f["via"].startswith("cita:")))
    print("     SIN resolver                         : %d"
          % sum(1 for f in sin if not f["via"].startswith("cita:")))
    print("escrito %s" % OUT)


if __name__ == "__main__":
    main()
