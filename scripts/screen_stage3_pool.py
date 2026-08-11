"""Etapa 3 (resumen) sobre el pozo priorizado de todas las fuentes.

POR QUE UN RECOLECTOR NUEVO. `screen_stage3_abstracts.py` indexa por PMID y su
pozo es el cribado de etapa 2 antiguo. De los 460 registros que avanzaron por
titulo en el pozo priorizado, 257 no tienen PMID -- CENTRAL, Scopus brazo B y
los registros de ensayos. Indexar por PMID los perderia en silencio, que es
justo el fallo que el cribado por titulo se construyo para evitar. Aqui la
clave es `record_id`, igual que en `screen_stage2_pool.py`.

DOS CORRIENTES, COMO PIDE PRISMA 2020. El diagrama separa "bases de datos" de
"registros" desde la casilla de identificacion. Los 71 registros de ensayos
(ClinicalTrials.gov, CTIS, EudraCT) no tienen resumen: tienen ficha. No pueden
cribarse por resumen ni excluirse por carecer de uno, asi que se contabilizan y
se deciden aparte, sobre la ficha. Un registro que ademas aparece en PubMed,
Scopus, CENTRAL o SciELO NO es corriente de registros: es un informe publicado
cuyo NCT es solo un identificador mas.

LO YA DECIDIDO NO SE VUELVE A DECIDIR. 77 de estos registros ya tienen decision
de resumen en el brazo anterior (`screening_stage3_decisions.csv`, por PMID).
`--seed` los importa con su veredicto y su motivo originales, marcando la
procedencia. Volver a juzgarlos abriria la puerta a contradecir un brazo ya
cerrado sin dejar rastro de cual de las dos decisiones vale.

EL LOG ES SOLO-ANEXAR. Una correccion es una fila nueva que sustituye a la
anterior; ambas quedan. Vocabulario de exclusion cerrado, el mismo de etapa 2,
para que la agrupacion PRISMA por motivo sea estable entre etapas.

USO
    python scripts/screen_stage3_pool.py --seed
    python scripts/screen_stage3_pool.py --status
    python scripts/screen_stage3_pool.py --next 40
    python scripts/screen_stage3_pool.py --registros 40
    python scripts/screen_stage3_pool.py --batch lote.tsv
"""
import argparse
import collections
import csv
import datetime
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from screen_stage1_rules import known_pmids
from exclusion_codes import CODES, code_for

ROOT = pathlib.Path(__file__).resolve().parent.parent
POOL = ROOT / "revision_sistematica" / "cribado" / "screening_stage2_priorizado.csv"
STAGE2 = ROOT / "revision_sistematica" / "cribado" / "screening_stage2_pool_decisions.csv"
STAGE3_PMID = ROOT / "revision_sistematica" / "cribado" / "screening_stage3_decisions.csv"
LOG = ROOT / "revision_sistematica" / "cribado" / "screening_stage3_pool_decisions.csv"

COLS = ["record_id", "orden", "corriente", "verdict", "reason",
        "decided_by", "decided_at"]
VERDICTS = ("FULLTEXT", "EXCLUDE")
REGISTROS = ("ClinicalTrials.gov", "CTIS", "EudraCT", "ICTRP")

csv.field_size_limit(200_000_000)
try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass


def corriente(rec):
    """'registro' solo si TODAS sus fuentes son registros de ensayos."""
    fuentes = [f.strip() for f in rec["sources"].split(";") if f.strip()]
    if not fuentes:
        return "base"
    es_reg = [any(f.startswith(k) for k in REGISTROS) for f in fuentes]
    return "registro" if all(es_reg) else "base"


def load_pool():
    """Los registros que avanzaron por titulo, con su corriente asignada."""
    with open(STAGE2, encoding="utf-8", newline="") as fh:
        stage2 = {d["record_id"]: d for d in csv.DictReader(fh)}
    with open(POOL, encoding="utf-8", newline="") as fh:
        pool = [p for p in csv.DictReader(fh)
                if stage2.get(p["record_id"], {}).get("verdict") == "ADVANCE"]
    for p in pool:
        p["corriente"] = corriente(p)
    return pool


def load_log():
    if not LOG.exists():
        return {}
    with open(LOG, encoding="utf-8", newline="") as fh:
        return {r["record_id"]: r for r in csv.DictReader(fh)}


def append(rows):
    nuevo = not LOG.exists()
    with open(LOG, "a", encoding="utf-8", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=COLS)
        if nuevo:
            w.writeheader()
        w.writerows(rows)


def seed(pool, decided):
    """Importa las decisiones de resumen ya tomadas en el brazo por PMID."""
    if not STAGE3_PMID.exists():
        sys.exit("no existe %s" % STAGE3_PMID)
    with open(STAGE3_PMID, encoding="utf-8", newline="") as fh:
        previo = {r["pmid"]: r for r in csv.DictReader(fh)}
    stamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
    rows = []
    for p in pool:
        pmid = p["pmid"].strip()
        if not pmid or pmid not in previo or p["record_id"] in decided:
            continue
        d = previo[pmid]
        rows.append({
            "record_id": p["record_id"], "orden": p["orden"],
            "corriente": p["corriente"], "verdict": d["verdict"],
            "reason": d["reason"],
            "decided_by": "heredada del brazo por PMID (%s)" % d["decided_by"],
            "decided_at": stamp})
    if not rows:
        print("nada que heredar: ya estaban todas importadas")
        return
    append(rows)
    print("heredadas %d decisiones del brazo por PMID" % len(rows))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--seed", action="store_true")
    ap.add_argument("--status", action="store_true")
    ap.add_argument("--next", type=int, default=0)
    ap.add_argument("--registros", type=int, default=0)
    ap.add_argument("--chars", type=int, default=900)
    ap.add_argument("--batch")
    ap.add_argument("--by", default="claude-opus-5 (revisor unico, sin duplicacion)")
    args = ap.parse_args()

    pool = load_pool()
    by_orden = {r["orden"]: r for r in pool}
    decided = load_log()

    if args.seed:
        seed(pool, decided)
        decided = load_log()

    if args.batch:
        rows, stamp = [], datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
        for line in pathlib.Path(args.batch).read_text(encoding="utf-8").splitlines():
            if not line.strip():
                continue
            orden, verdict, reason = (line.split("\t") + ["", ""])[:3]
            rec = by_orden.get(orden.strip())
            if rec is None:
                sys.exit("posicion %s no esta en el pozo de etapa 3" % orden)
            verdict = verdict.strip().upper()
            if verdict not in VERDICTS:
                sys.exit("veredicto invalido en %s: %s" % (orden, verdict))
            if verdict == "EXCLUDE" and code_for(reason) is None:
                sys.exit("motivo sin codigo del vocabulario cerrado, posicion %s: "
                         "%r -- usa uno de: %s" % (orden, reason, ", ".join(CODES)))
            rows.append({"record_id": rec["record_id"], "orden": orden.strip(),
                         "corriente": rec["corriente"], "verdict": verdict,
                         "reason": reason.strip(), "decided_by": args.by,
                         "decided_at": stamp})
        append(rows)
        print("registradas %d decisiones" % len(rows))
        decided = load_log()

    # ---------------- estado, por corriente ----------------
    for flujo in ("base", "registro"):
        recs = [r for r in pool if r["corriente"] == flujo]
        dec = [decided[r["record_id"]] for r in recs if r["record_id"] in decided]
        ft = sum(1 for d in dec if d["verdict"] == "FULLTEXT")
        etiqueta = ("bases de datos (cribado por resumen)" if flujo == "base"
                    else "registros de ensayos (cribado por ficha)")
        print("\n%s" % etiqueta)
        print("  pozo          : %d" % len(recs))
        print("  decididos     : %d  (texto completo %d / excluidos %d)"
              % (len(dec), ft, len(dec) - ft))
        print("  pendientes    : %d" % (len(recs) - len(dec)))
        sin_ab = sum(1 for r in recs
                     if r["record_id"] not in decided
                     and not (r["abstract"] or "").strip())
        if sin_ab:
            print("  sin resumen   : %d de los pendientes" % sin_ab)

    exc = [d for d in decided.values() if d["verdict"] == "EXCLUDE"]
    if exc:
        codigos, sin_codigo = collections.Counter(), []
        for d in exc:
            c = code_for(d["reason"])
            (sin_codigo.append(d) if c is None else codigos.update([c]))
        print("\nmotivos de exclusion (vocabulario cerrado):")
        for c, desc in CODES.items():
            if codigos[c]:
                print("  %-4s %4d  %s" % (c, codigos[c], desc[:58]))
        if sin_codigo:
            print("\n  AVISO: %d exclusiones sin codigo asignable:" % len(sin_codigo))
            for d in sin_codigo[:5]:
                print("    orden %s: %s" % (d["orden"], d["reason"][:70]))

    # ---------------- auditoria de control positivo ----------------
    known = known_pmids()
    by_study = collections.defaultdict(list)
    for r in pool:
        if r["pmid"] and r["pmid"] in known:
            by_study[known[r["pmid"]]].append(r)
    # El conjunto de control se fijo bajo el protocolo ORIGINAL, que no tenia
    # criterio de idioma. Cuando una enmienda de elegibilidad entra despues, un
    # control positivo puede perderse legitimamente: no es un fallo del cribado,
    # es el precio del criterio nuevo. Las dos cosas se separan porque
    # confundirlas arruina la auditoria en cualquiera de los dos sentidos --
    # fallar siempre la vuelve ruido que se acaba ignorando, y pasar siempre
    # deja de detectar el error que existe para detectar.
    perdidos, por_enmienda = [], []
    for sid, recs in by_study.items():
        filas = [decided.get(x["record_id"], {}) for x in recs]
        estados = [f.get("verdict") for f in filas if f]
        if not estados or not all(e == "EXCLUDE" for e in estados):
            continue
        codigos = {code_for(f.get("reason", "")) for f in filas if f}
        if codigos == {"IDI"}:
            por_enmienda.append((sid, filas[0].get("reason", "")))
        else:
            perdidos.append(sid)
    tocados = sum(1 for recs in by_study.values()
                  if any(x["record_id"] in decided for x in recs))
    print("\nestudios incluidos con algun informe ya decidido: %d de %d"
          % (tocados, len(by_study)))
    if por_enmienda:
        print("\nPERDIDOS POR LA ENMIENDA DE IDIOMA (%d). No es un fallo del "
              "cribado, pero SI es un coste del criterio y debe declararse en "
              "el manuscrito:" % len(por_enmienda))
        for sid, motivo in por_enmienda:
            print("  %-16s %s" % (sid, motivo[:96]))
    if perdidos:
        print("\nFALLO: un estudio incluido pierde todos sus informes por un "
              "motivo que no es una enmienda declarada")
        for sid in perdidos:
            print("  %s" % sid)
        sys.exit("revisa esas decisiones antes de continuar")
    print("auditoria de control positivo: PASS%s"
          % (" (con %d perdidos por la enmienda de idioma)" % len(por_enmienda)
             if por_enmienda else ""))

    # ---------------- listados de trabajo ----------------
    if args.next:
        todo = [r for r in pool if r["corriente"] == "base"
                and r["record_id"] not in decided][:args.next]
        print("\n# siguientes %d resumenes -- FULLTEXT o EXCLUDE" % len(todo))
        for r in todo:
            ab = " ".join((r["abstract"] or "").split()) or "(sin resumen)"
            print("\n%s | %s | %s" % (r["orden"], r["year"],
                                      " ".join(r["title"].split())[:120]))
            print("   %s" % ab[:args.chars])

    if args.registros:
        todo = [r for r in pool if r["corriente"] == "registro"
                and r["record_id"] not in decided][:args.registros]
        print("\n# siguientes %d fichas de registro -- FULLTEXT o EXCLUDE" % len(todo))
        for r in todo:
            print("%s | %-12s | %s | %s" % (r["orden"], r["nct"] or "-", r["year"],
                                            " ".join(r["title"].split())[:110]))


if __name__ == "__main__":
    main()
