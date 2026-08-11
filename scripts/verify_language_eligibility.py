"""Prueba, informe por informe, que todo lo incluido esta en ingles o espanol.

POR QUE NO BASTA EL CAMPO DECLARADO. El campo `language` cubre lo que esta
indexado en PubMed o en Scopus, pero 107 de los informes son fichas de registro
y registros de Cochrane CENTRAL, que no traen ese campo. Darlos por ingleses
"porque esas fuentes publican en ingles" es una inferencia razonable y NO es una
prueba: si un solo registro llegara en otro idioma, nada lo detectaria.

QUE HACE ESTE SCRIPT. Determina el idioma del TEXTO que de verdad se leeria
--titulo mas resumen-- de forma independiente del campo declarado, y contrasta
las dos determinaciones. Cualquier desacuerdo se reporta. Un informe solo queda
dentro si su texto es demostrablemente ingles o espanol.

COMO IDENTIFICA EL IDIOMA. Primero por alfabeto: cirilico, griego, arabe, hebreo
o CJK descartan de inmediato. Despues, sobre alfabeto latino, por frecuencia de
palabras funcionales, que son las que ninguna lengua puede evitar y que ningun
tecnicismo comparte. Se exige margen sobre la segunda candidata: si ingles y
neerlandes empatan, el informe no esta probado y se marca como tal en vez de
adjudicarse al que gane por un voto.

CODIGO DE SALIDA. 1 si algun informe incluido no queda probado. Es deliberado:
un criterio de elegibilidad que no se puede comprobar no es un criterio.

SALIDA
    revision_sistematica/cribado/idioma_verificacion.csv
"""
import collections
import csv
import json
import pathlib
import re
import sys
import unicodedata

ROOT = pathlib.Path(__file__).resolve().parent.parent
RS = ROOT / "revision_sistematica"
CRIB = RS / "cribado"
OUT = CRIB / "idioma_verificacion.csv"
csv.field_size_limit(200_000_000)
try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

ADMITIDOS = {"eng", "spa"}

# Alfabetos que por si solos descartan ingles y espanol.
ESCRITURAS = [
    ("cirilico", re.compile(r"[Ѐ-ӿ]")),
    ("griego", re.compile(r"[Ͱ-Ͽ]")),
    ("arabe", re.compile(r"[؀-ۿ]")),
    ("hebreo", re.compile(r"[֐-׿]")),
    ("CJK", re.compile(r"[぀-ヿ一-鿿가-힯]")),
]

# Palabras funcionales. No se eligen por ser frecuentes en abstracto, sino por
# ser imposibles de evitar al escribir una frase y por no coincidir entre
# lenguas: "the" no existe en espanol, "de" no funciona como articulo en ingles.
PERFILES = {
    "eng": """the of and in to a for with was were is are that this these those
              were been has have had not but their its from by on at we our
              study patients treatment results conclusion""".split(),
    "spa": """el la los las de del y en un una para con que se fue fueron es son
              este esta estos estas su sus por no pero desde al como
              estudio pacientes tratamiento resultados conclusiones""".split(),
    "por": """o a os as de do da dos das e em um uma para com que se foi foram
              este esta estes estas seu seus pelo pela nao mas
              estudo pacientes tratamento resultados conclusoes""".split(),
    "fre": """le la les des du de et en un une pour avec que qui est sont ete
              cette ces leur leurs par ne pas dans au aux
              etude patients traitement resultats""".split(),
    "deu": """der die das den dem des und in ein eine fur mit von zu ist sind
              war waren nicht auch bei auf als aus dass
              studie patienten behandlung ergebnisse""".split(),
    "ita": """il lo la i gli le di del della e in un una per con che si e sono
              stato stati questa questi loro non ma da al
              studio pazienti trattamento risultati""".split(),
    "nld": """de het een van en in te dat die deze voor met op zijn was waren
              niet maar door bij aan als uit ook
              onderzoek patienten behandeling resultaten""".split(),
    "dan": """og i at det en den af til er var for med som pa de ikke men
              have har blev fra ved om
              undersogelse patienter behandling resultater""".split(),
}


# Palabras que aparecen en un unico perfil. Son las unicas que distinguen: si
# "for" esta en ingles y en danes, contarla en ambos no separa nada y en un
# texto corto puede invertir el resultado.
_todas = collections.Counter(w for stops in PERFILES.values() for w in set(stops))
EXCLUSIVAS = {lang: frozenset(w for w in set(stops) if _todas[w] == 1)
              for lang, stops in PERFILES.items()}

# Politicas de idioma verificables de los registros de ensayos. No es una
# suposicion sobre la fuente: es la norma publicada del registro, y por eso
# constituye evidencia citable para una ficha cuyo titulo es demasiado corto
# para analizarlo.
REGISTROS = {
    "ClinicalTrials.gov":
        "42 CFR 11 y la politica de la NLM exigen que el registro se presente "
        "en ingles",
    "EudraCT":
        "el registro publico de la EMA se publica en ingles",
    "CTIS":
        "el Reglamento (UE) 536/2014 fija el ingles para la parte I del "
        "expediente publico",
}


def sin_tildes(t):
    t = unicodedata.normalize("NFKD", t or "")
    return "".join(c for c in t if not unicodedata.combining(c))


ALTERNO = re.compile(r"\s*;\s*\[[^\]]*\]\s*$")


def parte_titulo(t):
    """Separa el titulo principal del alternativo que va entre corchetes.

    PubMed y Scopus archivan `Titulo en ingles; [Titulo original]`. Analizar la
    cadena entera hace que el alfabeto del titulo alternativo decida por el
    informe entero, que es justo lo contrario de lo que interesa: lo que hay que
    determinar es en que idioma se puede LEER el informe.
    """
    t = t or ""
    m = ALTERNO.search(t)
    return (t[:m.start()].strip(), m.group(0).strip(" ;[]")) if m else (t.strip(), "")


def identifica(texto):
    """(idioma, confianza, evidencia). confianza: 'probado' | 'insuficiente'."""
    # El alfabeto tiene que DOMINAR, no solo aparecer. Contar tres caracteres
    # sueltos marcaba como no latinos nueve articulos de Nature Communications
    # y Scientific Reports: cualquier texto de microbiologia lleva alfa, beta,
    # mu y delta en unidades, cepas y nombres de genes. Se compara contra las
    # letras latinas del mismo texto.
    latinas = len(re.findall(r"[A-Za-z]", texto or ""))
    for nombre, pat in ESCRITURAS:
        hits = len(pat.findall(texto or ""))
        if hits >= 12 and hits > 0.20 * max(latinas, 1):
            return ("no-latino", "probado",
                    "alfabeto %s dominante: %d caracteres frente a %d latinas"
                    % (nombre, hits, latinas))

    palabras = re.findall(r"[a-z]+", sin_tildes(texto).lower())
    if len(palabras) < 12:
        return ("", "insuficiente",
                "solo %d palabras de texto: no hay base para decidir"
                % len(palabras))

    cuenta = collections.Counter(palabras)
    marcador = {}
    for lang, stops in PERFILES.items():
        # SOLO palabras EXCLUSIVAS de esa lengua. Puntuar con el perfil entero
        # hizo que "Individual Patient Expanded Access for AB-PA01" saliera
        # danes: "for" y "pa" estan en los dos perfiles y en un titulo corto
        # deciden por si solos. Una palabra que comparten dos lenguas no aporta
        # informacion para distinguirlas y no debe puntuar en ninguna.
        marcador[lang] = sum(cuenta[w] for w in EXCLUSIVAS[lang]) \
            / float(len(palabras))

    orden = sorted(marcador.items(), key=lambda kv: -kv[1])
    (mejor, m1), (segundo, m2) = orden[0], orden[1]
    # Margen exigido: la primera debe superar a la segunda con holgura, y
    # alcanzar un minimo absoluto. Sin el margen, un resumen tecnico corto en
    # neerlandes puede ganar en ingles por dos preposiciones compartidas.
    if m1 < 0.06:
        return (mejor, "insuficiente",
                "densidad de palabras funcionales demasiado baja (%.3f)" % m1)
    if m1 < m2 * 1.6:
        return (mejor, "insuficiente",
                "%s %.3f frente a %s %.3f: margen escaso"
                % (mejor, m1, segundo, m2))
    encontradas = [w for w in PERFILES[mejor] if cuenta[w]][:8]
    return (mejor, "probado",
            "%s %.3f frente a %s %.3f; palabras: %s"
            % (mejor, m1, segundo, m2, " ".join(encontradas)))


def leer(p):
    with open(p, encoding="utf-8", newline="") as fh:
        return list(csv.DictReader(fh))


def main():
    grupos = leer(CRIB / "study_groups.csv")
    pool = {p["record_id"]: p for p in
            leer(CRIB / "screening_stage2_priorizado.csv")}
    declarado = {r["record_id"]: r for r in leer(CRIB / "idioma_informes.csv")}

    filas, sin_probar, discrepan = [], [], []
    for g in grupos:
        rid = g["record_id"]
        p = pool.get(rid, {})
        d = declarado.get(rid, {})
        dec = d.get("idioma", "")
        principal, alterno = parte_titulo(p.get("title", ""))
        resumen = p.get("abstract", "") or ""
        # Se analiza lo que de verdad se leeria: el titulo principal y el
        # resumen indexado, sin el titulo alternativo entre corchetes.
        det, confianza, evidencia = identifica("%s %s" % (principal, resumen))
        fuentes = {x.strip() for x in (p.get("sources") or "").split(";")
                   if x.strip()}

        # ---- clases de evidencia, de la mas fuerte a la mas debil ----
        if confianza == "probado" and det in ADMITIDOS:
            clase = "A. texto probado"
            prueba = evidencia
            elegible = True
        elif (confianza == "probado" and det not in ADMITIDOS
                and dec not in ADMITIDOS):
            clase = "E. texto probado en lengua no admitida"
            prueba = evidencia
            elegible = False
        elif fuentes and fuentes <= set(REGISTROS):
            # Antes que el campo declarado: para una ficha de registro, el campo
            # "eng" lo puso este mismo canal a partir de la fuente, asi que
            # citarlo seria circular. La norma del registro si es comprobable.
            clase = "D. politica de idioma del registro"
            prueba = "; ".join(REGISTROS[f] for f in sorted(fuentes))
            elegible = True
        elif dec in ADMITIDOS:
            clase = "B. campo de idioma de la fuente"
            prueba = "%s declara %s; texto insuficiente para corroborar (%s)"                 % (d.get("fuente_del_idioma", "?"), dec, evidencia)
            elegible = True
        elif False:
            clase = "D. politica de idioma del registro"
            prueba = "; ".join(REGISTROS[f] for f in sorted(fuentes))
            elegible = True
        elif dec and dec not in ADMITIDOS and len(resumen) >= 400 and                 identifica(resumen)[0] == "eng" and                 identifica(resumen)[1] == "probado" and not                 (p.get("title", "") or "").strip().startswith("["):
            # El original no esta en lengua admitida, pero el informe SI se
            # puede leer en ingles: titulo principal en ingles (no entre
            # corchetes, que es como se marca una traduccion de cortesia) y
            # resumen integro en ingles. La elegibilidad se refiere al idioma
            # en que el informe puede leerse y extraerse, no al del manuscrito
            # original.
            clase = "C. version en ingles disponible"
            prueba = ("original en %s, pero titulo principal en ingles sin "
                      "corchetes y resumen integro en ingles de %d caracteres"
                      % (dec, len(resumen)))
            elegible = True
        else:
            clase = "E. sin prueba"
            prueba = evidencia
            elegible = False

        estado = "ADMITIDO" if elegible else "NO ADMITIDO"
        if not elegible:
            sin_probar.append((rid, g, clase, prueba))
        if (confianza == "probado" and dec in ADMITIDOS and det in ADMITIDOS
                and det != dec):
            discrepan.append((rid, dec, det, g["titulo"][:60]))

        filas.append({
            "record_id": rid, "estudio": g["estudio"],
            "idioma_declarado": dec or "(sin dato)",
            "fuente_declarado": d.get("fuente_del_idioma", ""),
            "idioma_del_texto": det or "(indeterminado)",
            "clase_de_evidencia": clase, "prueba": prueba,
            "estado": estado,
            "caracteres_de_resumen": len(resumen),
            "titulo_alternativo": alterno[:60],
            "revista": g["revista"],
            "titulo": " ".join(principal.split())[:110],
        })

    with open(OUT, "w", encoding="utf-8", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(filas[0].keys()))
        w.writeheader()
        w.writerows(filas)

    print("informes incluidos verificados : %d" % len(filas))
    print("\nestado:")
    for k, v in collections.Counter(f["estado"] for f in filas).most_common():
        print("   %-46s %3d" % (k, v))
    print("\nidioma determinado sobre el propio texto:")
    for k, v in collections.Counter(f["idioma_del_texto"]
                                    for f in filas).most_common():
        print("   %-18s %3d" % (k, v))

    if discrepan:
        print("\nDISCREPANCIAS entre el campo declarado y el texto (%d):"
              % len(discrepan))
        for rid, dec, det, tit in discrepan:
            print("   %s declarado=%s texto=%s  %s" % (rid, dec, det, tit))

    if sin_probar:
        print("\nNO PROBADOS (%d). Cada uno necesita decision explicita:"
              % len(sin_probar))
        for rid, g, estado, ev in sin_probar[:40]:
            print("   %s [%s] %s\n        %-36s %s"
                  % (rid, estado, ev[:66], (g["revista"] or "(sin revista)")[:36],
                     " ".join(g["titulo"].split())[:58]))
        if len(sin_probar) > 40:
            print("   ... y %d mas" % (len(sin_probar) - 40))

    print("\nescrito %s" % OUT)
    return 1 if sin_probar else 0


if __name__ == "__main__":
    sys.exit(main())
