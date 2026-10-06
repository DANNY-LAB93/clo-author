# -*- coding: utf-8 -*-
"""La frase de la procedencia geografica, escrita desde los datos en los tres manuscritos.

POR QUE EXISTE

El reparto por pais iba tecleado. El maestro y el ingles decian todavia el
2026-10-06 «Rusia (7 estudios), Polonia y Georgia (6 cada una), Alemania (4)…
e India, Iran e Israel (2 cada una). No consta en 76 estudios», que es un
corpus anterior a la enmienda de idioma: Iran no esta en ningun estudio del
corpus vigente. El de la revista se corrigio una vez y se anclo solo el «No
consta en N de los M»; el reparto por pais siguio tecleado y volvio a quedarse
atras en cuanto salieron estudios. Un ancla no sirve para una lista de paises
que cambia de forma; esta frase la reescribe el canal entero, como el bloque
de riesgo de sesgo.

Lee `procedencia` de `synthesis_scalars.json`. Agrupa los paises por numero de
estudios; los origenes de un solo estudio se cuentan, no se enumeran.

Uso:
    python scripts/escribe_procedencia.py
"""
import json
import pathlib
import re
import sys

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

ROOT = pathlib.Path(__file__).resolve().parent.parent
ES = ROOT / "paper" / "manuscrito_revision_sistematica.md"
EN = ROOT / "paper" / "manuscript_systematic_review_en.md"
JSR = ROOT / "paper" / "manuscrito_JSR_final.md"

EN_NOMBRE = {"Georgia": "Georgia", "Polonia": "Poland", "Estados Unidos": "the United States",
             "Francia": "France", "Alemania": "Germany", "Bélgica": "Belgium",
             "España": "Spain", "Israel": "Israel", "Rusia": "Russia", "India": "India",
             "Italia": "Italy", "Japón": "Japan", "Reino Unido": "the United Kingdom",
             "Ucrania": "Ukraine", "China": "China", "Irán": "Iran"}
NO_DECLARADA = "no declarada"


def y(v, ingles):
    return (", ".join(v[:-1]) + (" and " if ingles else " y ") + v[-1]) if len(v) > 1 else v[0]


def frases(S):
    proc = {k: v for k, v in S["procedencia"].items() if k != NO_DECLARADA}
    grupos = {}
    for pais, n in proc.items():
        grupos.setdefault(n, []).append(pais)
    trozos_es, trozos_en, sueltos = [], [], 0
    for n in sorted(grupos, reverse=True):
        if n == 1:
            sueltos = len(grupos[n])
            continue
        es = sorted(grupos[n])
        en = sorted(EN_NOMBRE.get(p, p) for p in grupos[n])
        if not trozos_es:
            trozos_es.append("%s (%d estudios%s)" % (y(es, False), n, " cada una" if len(es) > 1 else ""))
            trozos_en.append("%s (%d studies%s)" % (y(en, True), n, " each" if len(en) > 1 else ""))
        else:
            trozos_es.append("%s (%d%s)" % (y(es, False), n, " cada una" if len(es) > 1 else ""))
            trozos_en.append("%s (%d%s)" % (y(en, True), n, " each" if len(en) > 1 else ""))
    if sueltos:
        trozos_es.append("y otros %d orígenes con un estudio cada uno" % sueltos)
        trozos_en.append("and %d other origins with one study each" % sueltos)
    no = S["procedencia"].get(NO_DECLARADA, 0)
    tot = S["estudios_extraibles"]
    es = ("se reparte entre %s. No consta en %d de los %d estudios."
          % (", ".join(trozos_es), no, tot))
    en = ("is spread across %s. It is not stated in %d of the %d studies."
          % (", ".join(trozos_en), no, tot))
    return es, en


def main():
    S = json.load(open(ROOT / "quality_reports" / "synthesis_scalars.json", encoding="utf-8"))
    suma = sum(S["procedencia"].values())
    if suma != S["estudios_extraibles"]:
        raise SystemExit("la procedencia suma %d y hay %d estudios extraíbles"
                         % (suma, S["estudios_extraibles"]))
    es, en = frases(S)
    rusia = S["procedencia"].get("Rusia", 0)
    cambios = {
        ES: [(r"(La procedencia geográfica, cuando consta, )se reparte entre [^\n]*?No consta en [^.]*\.",
              r"\g<1>" + es),
             (r"—de \d+ estudios a \d+— es efecto directo del criterio de idioma y no de la búsqueda\.",
              "—de %d estudios a %d— se debe sobre todo al criterio de idioma, no a la búsqueda."
              % (S["rusos_antes_de_la_enmienda"], rusia))],
        JSR: [(r"(La procedencia, cuando consta, )se reparte entre [^\n]*?No consta en [^.]*\.",
               r"\g<1>" + es)],
        EN: [(r"(Where stated, geographic origin )is spread across [^\n]*?It is not stated in [^.]*\.",
              r"\g<1>" + en),
             (r"from \d+ studies to \d+, is a direct effect of the language criterion and not of the search\.",
              "from %d studies to %d, is mainly an effect of the language criterion, not of the search."
              % (S["rusos_antes_de_la_enmienda"], rusia))],
    }
    # Las dos frases de la caida rusa ya reescritas no casan con el patron
    # viejo; se aceptan tambien en su forma nueva para que el guion sea
    # idempotente.
    nuevas = {
        ES: r"—de \d+ estudios a \d+— se debe sobre todo al criterio de idioma, no a la búsqueda\.",
        EN: r"from \d+ studies to \d+, is mainly an effect of the language criterion, not of the search\.",
    }
    for p, cs in cambios.items():
        t = p.read_text(encoding="utf-8")
        for i, (patron, nuevo) in enumerate(cs):
            n = len(re.findall(patron, t))
            if n == 0 and i == 1 and p in nuevas:
                patron = nuevas[p]
                n = len(re.findall(patron, t))
            if n != 1:
                raise SystemExit("%s: el patrón aparece %d veces: %s" % (p.name, n, patron[:60]))
            t = re.sub(patron, nuevo if "\\g<1>" in nuevo else nuevo.replace("\\", "\\\\"), t)
        p.write_text(t, encoding="utf-8")
    print("procedencia escrita en los tres manuscritos:")
    print("  ES: ..." + es[:150])
    print("  EN: ..." + en[:150])


if __name__ == "__main__":
    main()
