"""Comprueba, eslabon por eslabon, que el canal PRISMA cuadra.

POR QUE EXISTE. Cada etapa del cribado tiene su propio script y su propia
comprobacion interna, y todas pasaban mientras el canal en conjunto tenia un
agujero: `bvs_non_medline.ris` estaba en disco pero no en el manifiesto, asi que
638 registros buscados y descargados nunca llegaron al corpus. Ninguna
comprobacion local podia verlo, porque desde dentro de cada etapa todo era
consistente. Solo cuadrar la salida de un eslabon contra la entrada del
siguiente lo destapa.

QUE COMPRUEBA. La igualdad, no la mera inclusion. Que el pozo sea un subconjunto
de los que avanzan en etapa 1 no dice nada; lo que hay que exigir es que sea el
mismo conjunto, porque un registro que avanza y no llega al pozo es un registro
perdido en silencio.

FUENTES DECLARADAS FRENTE A FUENTES PRESENTES. La comprobacion que importa y la
que nadie escribe: toda fuente del manifiesto debe aparecer en el corpus con al
menos un informe. Un fichero que no se carga no da error, solo da menos filas.

CODIGO DE SALIDA. 0 si todo cuadra, 1 si hay algun fallo. Los avisos no
detienen: describen desajustes ya explicados por escrito (por ejemplo, las
decisiones tomadas contra una version anterior del corpus).

USO
    python scripts/check_pipeline_coherence.py
"""
import collections
import csv
import json
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
RS = ROOT / "revision_sistematica"
csv.field_size_limit(200_000_000)

BUSQUEDA = RS / "busqueda"
CRIBADO = RS / "cribado"
EXTRACCION = RS / "extraccion"


def leer(p):
    with open(p, encoding="utf-8", newline="") as fh:
        return list(csv.DictReader(fh))


def ultima(filas):
    """El registro de decisiones es solo-anexar: manda la ultima fila."""
    d = {}
    for r in filas:
        d[r["record_id"]] = r
    return d


def main():
    ok, avisos, fallos = [], [], []

    def chk(cond, msg, blando=False):
        (ok if cond else (avisos if blando else fallos)).append(msg)

    corpus = leer(CRIBADO / "screening_corpus_all.csv")
    s1 = leer(CRIBADO / "screening_stage1_all.csv")
    pozo = leer(CRIBADO / "screening_stage2_priorizado.csv")
    d2 = ultima(leer(CRIBADO / "screening_stage2_pool_decisions.csv"))
    d3 = ultima(leer(CRIBADO / "screening_stage3_pool_decisions.csv"))
    grupos = leer(CRIBADO / "study_groups.csv")
    pre_p = EXTRACCION / "pre_extraccion_desde_resumen.csv"
    pre = leer(pre_p) if pre_p.exists() else []

    cid = {c["record_id"] for c in corpus}
    pid = {p["record_id"] for p in pozo}
    av1 = {r["record_id"] for r in s1 if r["stage1"] == "ADVANCE"}

    chk(len(cid) == len(corpus),
        "corpus sin record_id repetidos (%d informes)" % len(corpus))
    chk(len(pid) == len(pozo), "pozo sin record_id repetidos (%d)" % len(pozo))

    # Toda fuente declarada tiene que estar representada. Esta es la
    # comprobacion que habria evitado la omision de BVS.
    man = json.loads((BUSQUEDA / "sources.json").read_text(encoding="utf-8"))
    presentes = collections.Counter()
    for c in corpus:
        for s in c["sources"].split(";"):
            if s.strip():
                presentes[s.strip()] += 1
    faltan = [k for k in man if not presentes[k]]
    chk(not faltan,
        "todas las fuentes del manifiesto estan en el corpus (%d fuentes)"
        % len(man) if not faltan
        else "FUENTES BUSCADAS QUE NO LLEGARON AL CORPUS: %s" % ", ".join(faltan))
    for k, v in man.items():
        chk((ROOT / v).exists(), "fichero de la fuente %s existe" % k)

    chk(pid <= cid, "el pozo esta contenido en el corpus (%d fuera)"
        % len(pid - cid))
    chk(pid == av1, "pozo == ADVANCE de etapa 1 (%d vs %d)" % (len(pid), len(av1)))
    chk(pid <= set(d2), "etapa 2 cubre todo el pozo (%d sin decidir)"
        % len(pid - set(d2)))

    huerf = set(d2) - pid
    chk(not huerf,
        "etapa 2 sin decisiones huerfanas"
        if not huerf else
        "%d decisiones de etapa 2 sobre registros de una version anterior "
        "del corpus (documentado en quality_reports/decisions/)" % len(huerf),
        blando=True)

    av2 = {r for r, f in d2.items() if f["verdict"] == "ADVANCE"} & pid
    chk(set(d3) <= av2, "etapa 3 solo decide lo que avanzo (%d indebidos)"
        % len(set(d3) - av2))
    chk(av2 <= set(d3), "etapa 3 cubre lo avanzado (%d sin decidir)"
        % len(av2 - set(d3)))

    av3 = {r for r, f in d3.items() if f["verdict"] == "FULLTEXT"}
    gid = {g["record_id"] for g in grupos}
    chk(gid == av3, "agrupacion == FULLTEXT de etapa 3 (%d vs %d)"
        % (len(gid), len(av3)))

    est = collections.Counter(g["estudio"] for g in grupos)
    reps = [g for g in grupos if g["informe_para_extraer"] == "SI"]
    rc = collections.Counter(g["estudio"] for g in reps)
    chk(all(v == 1 for v in rc.values()) and set(rc) == set(est),
        "un unico informe representante por estudio (%d estudios)" % len(est))
    chk(sum(est.values()) == len(grupos),
        "los informes por estudio suman las filas de la agrupacion")

    if pre:
        extr = {"EST-%03d" % int(g["estudio"]) for g in reps
                if g["situacion"] in ("extraible", "solo-resumen")}
        ids = {p["id_provisional"] for p in pre}
        # Se exige COBERTURA, no igualdad. La pre-extraccion se hizo sobre 159
        # estudios y la enmienda de idioma excluyo 32 de ellos: esas filas se
        # conservan porque son el registro del trabajo hecho, y exigir igualdad
        # obligaria a borrarlas, que es justo lo que este proyecto no hace.
        chk(extr <= ids, "pre-extraccion cubre los extraibles (%d de %d)"
            % (len(ids & extr), len(extr)))
        sobra = ids - extr
        chk(not sobra,
            "pre-extraccion sin sobrantes"
            if not sobra else
            "%d pre-extracciones de estudios excluidos despues por la enmienda "
            "de idioma; se conservan como registro" % len(sobra), blando=True)
        chk(len(ids) == len(pre), "pre-extraccion sin filas repetidas")
        chk(all(p.get("extraction_status") == "PARTIAL" for p in pre),
            "toda la pre-extraccion sigue marcada PARTIAL")

    chk(not any("<" in c["title"] for c in corpus),
        "ningun titulo del corpus arrastra marcado HTML")

    print("=== CADENA PRISMA ===")
    print("corpus %d -> etapa1 ADVANCE %d -> pozo %d -> etapa2 ADVANCE %d "
          "-> etapa3 FULLTEXT %d -> %d estudios -> %d pre-extraidos"
          % (len(cid), len(av1), len(pid), len(av2), len(av3), len(est),
             len(pre)))
    print("corriente de etapa 3:",
          dict(collections.Counter(f["corriente"] for f in d3.values())))
    print("informes por fuente:", dict(presentes.most_common()))

    print("\n=== OK (%d) ===" % len(ok))
    for m in ok:
        print("  OK    ", m)
    if avisos:
        print("=== AVISOS (%d) ===" % len(avisos))
        for m in avisos:
            print("  AVISO ", m)
    print("=== FALLOS (%d) ===" % len(fallos))
    for m in fallos:
        print("  FALLO ", m)
    return 1 if fallos else 0


if __name__ == "__main__":
    sys.exit(main())
