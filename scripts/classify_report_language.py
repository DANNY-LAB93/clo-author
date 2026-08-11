"""Determina el idioma de cada informe que paso a texto completo.

POR QUE NO SE DEDUCE DEL NOMBRE DE LA REVISTA. Adivinar el idioma por el titulo
de la revista falla en los dos sentidos: Pirogov Russian Journal of Surgery
publica en ingles, y una revista con nombre ingles puede publicar el articulo en
otro idioma. Un criterio de elegibilidad no puede apoyarse en una conjetura, asi
que el idioma se toma del campo `language` que declara Europe PMC, que es el
mismo dato que PubMed archiva en LA y que un revisor puede comprobar.

CUANDO NO HAY DATO, SE INCLUYE. Si el registro no esta en Europe PMC y las
senales del propio registro no bastan, el informe se marca `dudoso` y NO se
excluye. Excluir por una suposicion es peor que incluir de mas: lo segundo se
ve en el listado y lo primero desaparece sin dejar rastro.

SALIDA
    revision_sistematica/cribado/idioma_informes.csv
    (cache en revision_sistematica/cribado/.idioma_cache.json)
"""
import csv
import json
import pathlib
import re
import sys
import time
import urllib.parse
import urllib.request

ROOT = pathlib.Path(__file__).resolve().parent.parent
RS = ROOT / "revision_sistematica"
CRIB = RS / "cribado"
CACHE = CRIB / ".idioma_cache.json"
OUT = CRIB / "idioma_informes.csv"
csv.field_size_limit(200_000_000)
try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

ELEGIBLES = {"eng", "spa"}
CIRILICO = re.compile(r"[Ѐ-ӿ]")

# Revistas que publican una version integra en ingles ademas de la original.
# Se comprueban a mano y se listan aqui porque el campo `language` de la fuente
# recoge el idioma del articulo indexado, no la existencia de una traduccion
# oficial. Cada entrada dice donde se comprobo.
BILINGUES = {
    "pirogov russian journal of surgery":
        "Khirurgiya. Zhurnal im. N.I. Pirogova: version inglesa integra en "
        "mediasphera.ru",
    "russian journal of infection and immunity":
        "publica cada articulo en ruso y en ingles (iimmun.ru)",
}


def leer(p):
    with open(p, encoding="utf-8", newline="") as fh:
        return list(csv.DictReader(fh))


def idioma_de_las_fuentes():
    """Indice de idioma construido desde las exportaciones crudas.

    Europe PMC solo conoce lo que esta indexado en PubMed o PMC, y 139 de los
    268 informes no lo estan: fichas de registro, resumenes de congreso y
    registros que solo vienen de Scopus o de las bases regionales. Esos SI
    declaran el idioma en su propia exportacion -- Scopus en la columna
    "Language of Original Document" y los RIS en la etiqueta LA -- asi que el
    dato existe y solo hay que ir a buscarlo donde esta.
    """
    sys.path.insert(0, str(ROOT / "scripts"))
    from deduplicate_sources import load, keys_for, norm_title

    ISO = {"english": "eng", "spanish": "spa", "portuguese": "por",
           "russian": "rus", "german": "ger", "french": "fre",
           "en": "eng", "es": "spa", "pt": "por", "ru": "rus",
           "de": "ger", "fr": "fre", "ja": "jpn", "japanese": "jpn"}

    por_id, por_titulo = {}, {}
    man = json.loads((RS / "busqueda" / "sources.json").read_text(encoding="utf-8"))
    for etiqueta, rel in man.items():
        p = ROOT / rel
        if not p.exists():
            continue
        for r in load(p):
            crudo = ""
            for campo in ("language", "la", "language of original document"):
                if r.get(campo):
                    crudo = r[campo]
                    break
            if not crudo:
                continue
            iso = ISO.get(crudo.strip().lower(), crudo.strip().lower()[:3])
            _, ids = keys_for(r)
            for i in ids:
                por_id.setdefault(i, (iso, etiqueta))
            t = norm_title(r.get("title", ""))
            if t:
                por_titulo.setdefault(t, (iso, etiqueta))
    return por_id, por_titulo


def consulta_epmc(clave):
    u = ("https://www.ebi.ac.uk/europepmc/webservices/rest/search?query=%s"
         "&resultType=core&format=json&pageSize=1"
         % urllib.parse.quote(clave))
    with urllib.request.urlopen(u, timeout=30) as fh:
        r = json.load(fh)["resultList"]["result"]
    return r[0] if r else None


def main():
    grupos = leer(CRIB / "study_groups.csv")
    pool = {p["record_id"]: p for p in
            leer(CRIB / "screening_stage2_priorizado.csv")}
    cache = json.loads(CACHE.read_text(encoding="utf-8")) if CACHE.exists() else {}
    sys.path.insert(0, str(ROOT / "scripts"))
    from deduplicate_sources import norm_title
    fuente_id, fuente_titulo = idioma_de_las_fuentes()

    filas = []
    consultados = 0
    for g in grupos:
        rid = g["record_id"]
        p = pool.get(rid, {})
        pmid = (p.get("pmid") or "").strip()
        doi = (p.get("doi") or "").strip()
        idioma, via = "", ""

        if rid in cache:
            idioma, via = cache[rid]["idioma"], cache[rid]["via"]
        else:
            clave = ("EXT_ID:%s" % pmid if pmid
                     else ('DOI:"%s"' % doi if doi and
                           not doi.lower().startswith("10.1002/central/") else ""))
            if clave:
                try:
                    r = consulta_epmc(clave)
                    consultados += 1
                    time.sleep(0.12)
                    if r and r.get("language"):
                        idioma, via = r["language"].lower(), "Europe PMC (campo language)"
                except Exception as e:
                    via = "consulta fallida: %s" % type(e).__name__
            cache[rid] = {"idioma": idioma, "via": via}

        titulo = g["titulo"] or ""
        revista = (g["revista"] or "")

        # Segunda fuente: el idioma que declara la exportacion de origen
        if not idioma:
            claves = [x.strip() for x in (p.get("identifiers") or "").split(";")
                      if x.strip()]
            for i in claves:
                if i in fuente_id:
                    idioma, etq = fuente_id[i]
                    via = "exportacion de %s (campo de idioma)" % etq
                    break
        if not idioma:
            hit = fuente_titulo.get(norm_title(titulo))
            if hit:
                idioma, etq = hit
                via = "exportacion de %s, emparejado por titulo" % etq

        # Senales propias del registro, solo cuando ninguna fuente da el dato
        if not idioma:
            if CIRILICO.search(titulo + revista):
                idioma, via = "rus", "caracteres cirilicos en el propio registro"
            elif titulo.strip().startswith("["):
                idioma, via = "no-eng", "titulo entre corchetes: original no ingles"

        # Fuentes que publican en ingles por construccion. Ni los registros de
        # ensayos ni Cochrane CENTRAL traen etiqueta de idioma, y quedarian los
        # 107 como "sin dato", que haria inoperante el criterio. Pero el dato no
        # falta: ClinicalTrials.gov, EudraCT y CTIS publican su ficha en ingles,
        # y CENTRAL indexa titulo y resumen en ingles. Se resuelve por la fuente
        # y se deja constancia de que se resolvio asi, no por el campo.
        fuentes = {x.strip() for x in (p.get("sources") or "").split(";")
                   if x.strip()}
        if not idioma and fuentes:
            if fuentes <= {"ClinicalTrials.gov", "EudraCT", "CTIS"}:
                idioma = "eng"
                via = "ficha de registro de ensayo: el registro publica en ingles"
            elif fuentes <= {"Cochrane CENTRAL"}:
                idioma = "eng"
                via = "Cochrane CENTRAL indexa titulo y resumen en ingles"

        # Version oficial en ingles disponible
        bil = ""
        for k, nota in BILINGUES.items():
            if revista.lower().startswith(k):
                bil = nota
                break

        if idioma in ELEGIBLES:
            veredicto = "elegible"
        elif bil:
            veredicto = "elegible"
        elif idioma:
            veredicto = "excluir"
        else:
            veredicto = "dudoso"

        filas.append({
            "record_id": rid, "estudio": g["estudio"],
            "idioma": idioma or "(sin dato)", "fuente_del_idioma": via or "(ninguna)",
            "version_inglesa": bil, "veredicto": veredicto,
            "pmid": pmid, "revista": revista,
            "titulo": " ".join(titulo.split())[:120],
        })

    CACHE.write_text(json.dumps(cache, ensure_ascii=False, indent=1),
                     encoding="utf-8")
    with open(OUT, "w", encoding="utf-8", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(filas[0].keys()))
        w.writeheader()
        w.writerows(filas)

    import collections
    print("informes clasificados : %d  (consultas nuevas: %d)"
          % (len(filas), consultados))
    print("\nidioma declarado:")
    for k, v in collections.Counter(f["idioma"] for f in filas).most_common():
        print("   %-14s %3d" % (k, v))
    print("\nveredicto:")
    for k, v in collections.Counter(f["veredicto"] for f in filas).most_common():
        print("   %-14s %3d" % (k, v))
    n_bil = sum(1 for f in filas if f["version_inglesa"])
    print("\nrescatados por tener version oficial en ingles: %d" % n_bil)
    print("escrito %s" % OUT)
    return 0


if __name__ == "__main__":
    sys.exit(main())
