# -*- coding: utf-8 -*-
"""De qué informe salió cada brazo, y con qué prueba se sabe.

POR QUE EXISTE. La auditoría del 2026-09-16 encontró que la extracción
registra el ESTUDIO al que pertenece cada brazo pero no el INFORME. Con 31
estudios que tienen más de un informe --artículo, ficha de registro, resúmenes
de congreso--, «EST-008 brazo A» no dice cuál de los once documentos se leyó
para rellenarlo, y un árbitro que quiera comprobar una cifra no sabe dónde
mirar. El ítem 10 de PRISMA pide exactamente eso: de dónde salió cada dato.

COMO SE ESTABLECE EL VINCULO, EN ORDEN DE FUERZA

  1. «título localizado en el texto leído». El título del informe designado
     aparece literalmente en el documento que se descargó y se leyó. Es la
     prueba más fuerte: el documento que está en la caché ES ese informe, y la
     frase que lo demuestra se guarda en la columna de evidencia.
  2. «informe único». El estudio tiene un solo informe. El vínculo no se
     deduce: no hay otra posibilidad.
  3. «único artículo del grupo». El estudio tiene varios informes pero uno solo
     es un artículo, y los demás son fichas de registro o resúmenes de
     congreso, que no fueron la fuente de la extracción. Se declara como
     inferencia, no como lectura.
  4. «sin resolver». Todo lo demás. Va al fichero de pendientes y NO se
     inventa.

LO QUE ESTE SCRIPT NO HACE. No afirma que el dato concreto de una casilla
salga de una página concreta. Afirma de qué documento salió el brazo. La
trazabilidad hasta la frase es la columna `extraction_citation`, que ya existe.

SALIDA
    quality_reports/brazo_informe.csv
    quality_reports/brazo_informe_pendiente.json
"""
import csv
import json
import pathlib
import re
import sys
import unicodedata

ROOT = pathlib.Path(__file__).resolve().parent.parent
RS = ROOT / "revision_sistematica"
QR = ROOT / "quality_reports"
CACHE = RS / "textos_completos" / "texto_cache"
csv.field_size_limit(200_000_000)

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass


def leer(p, enc="utf-8"):
    with open(p, encoding=enc, newline="") as fh:
        return list(csv.DictReader(fh))


def plano(t):
    """Sin espacios, sin acentos, en minúscula: el texto de un PDF llega con
    las palabras pegadas («Ceftazidimewasappliedfor8weeks») y con los espacios
    puestos donde no van, de modo que buscar sobre el texto tal cual falla."""
    t = unicodedata.normalize("NFKD", t.lower())
    t = "".join(c for c in t if not unicodedata.combining(c))
    return re.sub(r"[^a-z0-9]", "", t)


def ventana(texto, aplanado, indice, i, n):
    """Devuelve el fragmento original que corresponde al tramo [i, i+n) del
    texto aplanado, con un poco de contexto a cada lado."""
    a = indice[max(0, i - 8)]
    b = indice[min(len(indice) - 1, i + n + 8)]
    return re.sub(r"\s+", " ", texto[a:b]).strip()


def mapa(texto):
    ap, idx = [], []
    for k, c in enumerate(unicodedata.normalize("NFKD", texto.lower())):
        if unicodedata.combining(c):
            continue
        if re.match(r"[a-z0-9]", c):
            ap.append(c)
            idx.append(k)
    idx.append(len(texto))
    return "".join(ap), idx


def main():
    grupos = leer(RS / "cribado" / "study_groups.csv")
    excl = {r["study_id"] for r in leer(RS / "cribado" / "exclusiones_tras_texto_completo.csv")}
    adj = leer(RS / "extraccion" / "extraccion_adjudicada.csv")
    corpus = {r["record_id"]: r for r in leer(RS / "cribado" / "screening_corpus_all.csv")}
    log = {r["id"]: r for r in leer(RS / "textos_completos" / "fulltext_download_log.csv")}

    informes = {}
    for g in grupos:
        informes.setdefault("EST-%03d" % int(g["estudio"]), []).append(g)

    filas, pendientes = [], []
    contador = {}
    for r in adj:
        eid = r["study_id"]
        if eid in excl:
            continue
        grupo = informes.get(eid, [])
        designado = next((g for g in grupo if g["informe_para_extraer"] == "SI"), None)
        if designado is None:
            pendientes.append({"study_id": eid, "arm_id": r["arm_id"],
                               "motivo": "el estudio no tiene informe designado"})
            continue
        rc = corpus.get(designado["record_id"], {})
        ids = [x for x in ("pmid:" + (rc.get("pmid") or ""),
                           "doi:" + (rc.get("doi") or ""),
                           "nct:" + (rc.get("nct") or ""))
               if not x.endswith(":")]

        via, evidencia = "", ""
        p = CACHE / (eid + ".txt")
        if p.exists():
            texto = p.read_text(encoding="utf-8", errors="replace")
            ap, idx = mapa(texto)
            clave = plano(designado["titulo"])[:60]
            if clave and clave in ap:
                via = "título localizado en el texto leído"
                evidencia = ventana(texto, ap, idx, ap.index(clave), len(clave))
        if not via:
            if len(grupo) == 1:
                via = "informe único"
                evidencia = "el estudio tiene un solo informe; no hay otra procedencia posible"
            else:
                arts = [g for g in grupo if g["tipo_informe"] == "articulo"]
                if len(arts) == 1 and arts[0]["record_id"] == designado["record_id"]:
                    via = "único artículo del grupo"
                    evidencia = ("de los %d informes del estudio, %d son fichas de registro o "
                                 "resúmenes de congreso y uno solo es artículo"
                                 % (len(grupo), len(grupo) - 1))
                elif len(arts) > 1 and all(
                        plano(a["titulo"])[:50] == plano(arts[0]["titulo"])[:50] for a in arts):
                    via = "artículos con el mismo título"
                    evidencia = ("los %d artículos del grupo llevan el mismo título: son el "
                                 "mismo documento indizado dos veces" % len(arts))
                else:
                    via = "sin resolver"
                    evidencia = ""
                    pendientes.append({
                        "study_id": eid, "arm_id": r["arm_id"],
                        "motivo": "%d informes, %d artículos, y el título designado no aparece "
                                  "en el texto leído" % (len(grupo), len(arts))})

        contador[via] = contador.get(via, 0) + 1
        filas.append({
            "study_id": eid,
            "arm_id": r["arm_id"],
            "record_id": designado["record_id"],
            "tipo_informe": designado["tipo_informe"],
            "identificadores": "; ".join(ids),
            "informes_del_estudio": len(grupo),
            # El log de descarga no cubre los textos que se consiguieron por
            # otra vía; decir «sin texto» de uno que sí está en la caché sería
            # falso, así que la caché manda sobre el log cuando el log calla.
            "documento_leido": (log.get(eid, {}).get("pmcid")
                                or log.get(eid, {}).get("url", "")[:90]
                                or ("texto_cache/%s.txt" % eid if p.exists() else "sin texto")),
            "via": via,
            "evidencia": evidencia[:300],
            "cita_de_extraccion": r["extraction_citation"][:200],
            "titulo_del_informe": designado["titulo"][:140],
        })

    salida = QR / "brazo_informe.csv"
    with salida.open("w", encoding="utf-8-sig", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(filas[0].keys()))
        w.writeheader()
        w.writerows(filas)

    est = {}
    for f in filas:
        est.setdefault(f["study_id"], set()).add(f["record_id"])
    multi = sorted(e for e, v in est.items() if len(v) > 1)

    (QR / "brazo_informe_pendiente.json").write_text(json.dumps({
        "generado_por": "scripts/build_brazo_informe.py",
        "brazos": len(filas),
        "estudios": len(est),
        "por_via": contador,
        "sin_resolver": [p for p in pendientes],
        "estudios_con_mas_de_un_informe_de_origen": multi,
    }, ensure_ascii=False, indent=2), encoding="utf-8", newline="\n")

    print("%d brazos de %d estudios -> %s" % (len(filas), len(est), salida.name))
    for k, v in sorted(contador.items(), key=lambda kv: -kv[1]):
        print("  %-38s %3d" % (k, v))
    if pendientes:
        print("  SIN RESOLVER: %d" % len(pendientes))
        for p in pendientes[:10]:
            print("    %s%s  %s" % (p["study_id"], p.get("arm_id", ""), p["motivo"]))


if __name__ == "__main__":
    main()
