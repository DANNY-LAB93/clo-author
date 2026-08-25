"""Saca una muestra aleatoria de los registros excluidos, para recribar en Rayyan.

QUE PROBLEMA RESUELVE

El cribado de titulo y resumen lo condujo un solo revisor humano y las decisiones
registro a registro las emitio un modelo. Los registros que el modelo excluyo no
volvio a leerlos nadie, de modo que **el falso negativo no esta medido**. La
auditoria de controles positivos lo acota solo sobre los 40 estudios que ya se
conocian de antemano, que es justo la parte facil.

Recribar los 13 434 excluidos a mano no es viable. Una muestra aleatoria si:
cribada a ciegas del veredicto del modelo, convierte «no se midio» en una tasa
con intervalo de confianza.

QUE NO ARREGLA

Nada, por si solo. Produce el fichero para que una persona lo cribe. Si la
muestra se cribara viendo lo que el modelo decidio, o con las sugerencias de IA
de Rayyan activadas, no mediria nada: mediria el acuerdo de alguien consigo
mismo. Por eso la salida NO lleva el veredicto ni el motivo, y la
correspondencia se guarda aparte.

COMO SE USA EL RESULTADO

  1. Importar `muestra_rayyan.csv` en Rayyan como revision nueva.
  2. Cribar los N registros por titulo y resumen, con los mismos criterios.
  3. Exportar las decisiones y cotejarlas con `clave_muestra.csv`.
  4. Los que Rayyan incluye y el modelo excluyo son los falsos negativos.

Uso:
    python scripts/build_rayyan_validation_sample.py [n] [--semilla N]
"""
import argparse
import csv
import pathlib
import random
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
CRIBADO = ROOT / "revision_sistematica" / "cribado"
SALIDA = ROOT / "revision_sistematica" / "validacion_rayyan"

csv.field_size_limit(200_000_000)
try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass


def leer(p):
    with open(p, encoding="utf-8", newline="") as fh:
        return list(csv.DictReader(fh))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("n", nargs="?", type=int, default=350,
                    help="tamano de la muestra (por defecto 350)")
    ap.add_argument("--semilla", type=int, default=20260823,
                    help="semilla del muestreo; fijarla hace la muestra reproducible")
    args = ap.parse_args()

    corpus = {r["record_id"]: r for r in leer(CRIBADO / "screening_corpus_all.csv")}
    dec2 = leer(CRIBADO / "screening_stage2_pool_decisions.csv")
    dec3 = leer(CRIBADO / "screening_stage3_pool_decisions.csv")

    # El marco de muestreo son los excluidos QUE SIGUEN EN EL CORPUS ACTUAL. El
    # fichero de decisiones conserva filas de una version anterior -- el canal ya
    # lo avisa -- y muestrear sobre ellas mediria el error de un corpus que ya no
    # existe.
    excluidos = [(r["record_id"], "titulo") for r in dec2
                 if r["verdict"] == "EXCLUDE" and r["record_id"] in corpus]
    excluidos += [(r["record_id"], "resumen") for r in dec3
                  if r["verdict"] == "EXCLUDE" and r["record_id"] in corpus]

    vistos, marco = set(), []
    for rid, etapa in excluidos:
        if rid not in vistos:
            vistos.add(rid)
            marco.append((rid, etapa))

    if args.n > len(marco):
        print("la muestra pedida (%d) supera el marco (%d)" % (args.n, len(marco)))
        return 1

    rng = random.Random(args.semilla)
    muestra = rng.sample(marco, args.n)
    muestra.sort(key=lambda x: x[0])

    SALIDA.mkdir(parents=True, exist_ok=True)

    # Fichero para Rayyan. SIN veredicto ni motivo: quien cribe no debe saber
    # que decidio el modelo, o la medicion no vale nada.
    cab = ["key", "title", "authors", "journal", "year", "abstract", "doi", "pmid"]
    with open(SALIDA / "muestra_rayyan.csv", "w", encoding="utf-8-sig",
              newline="") as fh:
        w = csv.writer(fh)
        w.writerow(cab)
        for rid, _ in muestra:
            r = corpus[rid]
            w.writerow([rid, r.get("title", ""), "", r.get("journal", ""),
                        r.get("year", ""), r.get("abstract", ""),
                        r.get("doi", ""), r.get("pmid", "")])

    # La clave, que se guarda y NO se mira hasta despues de cribar.
    porque = {r["record_id"]: (r["verdict"], r.get("reason", ""))
              for r in dec2 + dec3}
    with open(SALIDA / "clave_muestra.csv", "w", encoding="utf-8-sig",
              newline="") as fh:
        w = csv.writer(fh)
        w.writerow(["key", "etapa", "verdict_modelo", "motivo_modelo"])
        for rid, etapa in muestra:
            v, m = porque.get(rid, ("", ""))
            w.writerow([rid, etapa, v, m])

    # Cota superior del 95 % si la muestra sale sin ningun error: la regla de
    # tres, 1 - 0.05^(1/n). Se imprime para que nadie tenga que fiarse.
    cota = 1 - 0.05 ** (1.0 / args.n)
    print("marco de muestreo (excluidos en el corpus actual): %d" % len(marco))
    print("muestra                                          : %d" % args.n)
    print("semilla                                          : %d" % args.semilla)
    print()
    print("si la muestra sale con CERO exclusiones erroneas, la cota superior")
    print("del 95 %% para la tasa de falso negativo es %.2f %%, que sobre el marco" % (100 * cota))
    print("son hasta %d registros." % round(cota * len(marco)))
    print()
    print("escrito en %s" % SALIDA)
    print("  muestra_rayyan.csv   importar en Rayyan; NO lleva el veredicto")
    print("  clave_muestra.csv    NO abrir hasta terminar de cribar")
    return 0


if __name__ == "__main__":
    sys.exit(main())
