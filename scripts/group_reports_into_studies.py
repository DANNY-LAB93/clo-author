"""Agrupa los informes recuperados en ESTUDIOS y designa cuál se extrae.

LA REGLA DE PROTOCOLO QUE IMPLEMENTA. La unidad de inclusión es el estudio, no
el informe. Un ensayo puede llegar como protocolo, ficha de registro, varios
resúmenes de congreso y el artículo final; son un estudio con varios informes.
Extraer de más de uno duplicaría los mismos pacientes en el metaanálisis, y el
BX004-A entra en este pozo con SIETE resúmenes de congreso además de su ficha y
su publicación: es el riesgo concreto que esta agrupación evita.

POR QUÉ NO BASTA CON AGRUPAR POR NCT. Los resúmenes de congreso no llevan el
NCT en el registro bibliográfico. La cadena de claves es: NCT propio ->
atribución razonada (`fulltext_identifiers.csv`, escrita a mano y justificada)
-> título normalizado. Sin el paso intermedio, los siete resúmenes del BX004-A
se contaban como siete estudios.

SITUACIÓN DE CADA ESTUDIO, que es lo que decide dónde va en el PRISMA:
  extraible            tiene al menos un artículo del que extraer
  solo-resumen         su única fuente es un resumen de congreso -> se incluye,
                       pero entra en el análisis de sensibilidad que los excluye
  solo-registro        solo hay ficha de registro -> estudio en curso o sin
                       resultados publicados; no se agrupa, se lista aparte

SALIDA
    revision_sistematica/cribado/study_groups.csv

USO
    python scripts/group_reports_into_studies.py
"""
import collections
import csv
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
POOL = ROOT / "revision_sistematica" / "cribado" / "screening_stage2_priorizado.csv"
S3 = ROOT / "revision_sistematica" / "cribado" / "screening_stage3_pool_decisions.csv"
IDS = ROOT / "revision_sistematica" / "textos_completos" / "fulltext_identifiers.csv"
OUT = ROOT / "revision_sistematica" / "cribado" / "study_groups.csv"

csv.field_size_limit(200_000_000)
try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass


def norm(t):
    return re.sub(r"[^a-z0-9]+", "", (t or "").lower())[:80]


def real_doi(r):
    d = (r["doi"] or "").strip().lower()
    return d if d and not d.startswith("10.1002/central/") else ""


def tipo_informe(r):
    dt = (r["doctype"] or "").lower()
    j = (r["journal"] or "").lower()
    if "trial registry record" in dt or "trialsearch" in j:
        return "ficha de registro"
    if not (r["journal"] or "").strip() and r["nct"].strip():
        return "ficha de registro"
    if ("conference" in dt or "meeting" in dt or "supplement" in j
            or re.match(r"^(ws|p|oa)\d", (r["title"] or "").lower())):
        return "resumen de congreso"
    if not (r["journal"] or "").strip():
        return "ficha de registro"
    return "articulo"


# Preferencia de extracción: de dónde se saca el dato cuando un estudio tiene
# varios informes. El artículo manda; la ficha solo si no hay nada más.
RANGO = {"articulo": 0, "resumen de congreso": 1, "ficha de registro": 2}


def main():
    with open(POOL, encoding="utf-8", newline="") as fh:
        pool = list(csv.DictReader(fh))
    por_id = {p["record_id"]: p for p in pool}
    por_orden = {p["orden"]: p for p in pool}
    with open(S3, encoding="utf-8", newline="") as fh:
        s3 = {d["record_id"]: d for d in csv.DictReader(fh)}
    # La atribucion se indexa por record_id, NUNCA por `orden`. La posicion en
    # el pozo depende del manifiesto de fuentes: al incorporar BVS, el pozo paso
    # de 13 509 a 13 894 registros y toda posicion por encima de la primera
    # insercion se desplazo. Una tabla escrita a mano y leida por posicion pasa
    # entonces a atribuir el NCT de un ensayo a otro informe cualquiera sin que
    # nada falle a la vista: partio el BX004-A y el TP-102 en dos estudios cada
    # uno. El record_id se deriva del contenido y sobrevive a la reconstruccion.
    atrib = {}
    if IDS.exists():
        with open(IDS, encoding="utf-8", newline="") as fh:
            for r in csv.DictReader(fh):
                if r["identificador_resuelto"]:
                    atrib[r["record_id"]] = r["identificador_resuelto"]

    ft = [por_id[rid] for rid, d in s3.items()
          if d["verdict"] == "FULLTEXT" and rid in por_id]
    ft.sort(key=lambda r: int(r["orden"]))

    # Un artículo suele declarar su NCT DENTRO del resumen aunque el registro
    # bibliográfico no traiga el campo. Es lo que pasaba con el artículo del
    # BX004-A en Nature Communications (PMID 40593506): sin este rastreo, el
    # ensayo quedaba clasificado como "solo-resumen" teniendo publicación
    # completa, y se habría ido al análisis de sensibilidad que excluye los
    # estudios solo-resumen. Se acepta un NCT del resumen únicamente si ese NCT
    # ya existe como registro propio de otro informe del pozo: así el rastreo
    # solo une informes, nunca inventa un ensayo nuevo.
    ncts_propios = {r["nct"].strip().upper() for r in ft if r["nct"].strip()}
    nct_en_texto = {}
    for r in ft:
        if r["nct"].strip():
            continue
        hallados = {m.upper() for m in
                    re.findall(r"NCT\d{8}", (r["abstract"] or "") + " " + (r["title"] or ""))}
        hallados &= ncts_propios
        if len(hallados) == 1:
            nct_en_texto[r["record_id"]] = hallados.pop()

    # clave de estudio por registro, con la cadena NCT -> atribución -> título
    clave = {}
    for r in ft:
        n = r["nct"].strip().upper() or nct_en_texto.get(r["record_id"], "")
        if n:
            clave[r["record_id"]] = n
            continue
        a = atrib.get(r["record_id"], "")
        if a.startswith("NCT"):
            clave[r["record_id"]] = a
        elif a.startswith("pmid:"):
            clave[r["record_id"]] = a
        elif a.startswith("10."):
            clave[r["record_id"]] = "doi:" + a.lower()
        else:
            clave[r["record_id"]] = "T:" + norm(r["title"])

    # Una atribución a DOI/PMID apunta al informe PADRE; hay que unificar la
    # clave del hijo con la del padre, o quedarían en estudios separados.
    canon = {}
    for r in ft:
        k = clave[r["record_id"]]
        if k.startswith(("doi:", "pmid:")):
            val = k.split(":", 1)[1]
            for p in ft:
                if (real_doi(p) == val) or (p["pmid"].strip() == val):
                    canon[k] = clave[p["record_id"]]
                    break
    for rid, k in list(clave.items()):
        if k in canon:
            clave[rid] = canon[k]

    # los que comparten título normalizado también se unifican
    portitulo = collections.defaultdict(list)
    for r in ft:
        portitulo[norm(r["title"])].append(r["record_id"])
    for _, rids in portitulo.items():
        if len(rids) > 1:
            elegida = sorted(clave[x] for x in rids)[0]
            for x in rids:
                clave[x] = elegida

    grupos = collections.defaultdict(list)
    for r in ft:
        grupos[clave[r["record_id"]]].append(r)

    # NUMERACION ESTABLE. El numero EST-NNN no se reasigna por posicion en cada
    # ejecucion: se conserva el que ya tenia la clave de estudio y solo se
    # inventan numeros para claves nuevas. Al incorporar BVS, el pozo crecio y
    # las posiciones se desplazaron: la numeracion por orden movio doce estudios
    # un puesto, de modo que EST-205 (el articulo cubano) paso a ser EST-194 y
    # los demas corrieron detras. Los numeros ya estan en los cuadernos de
    # extraccion de Danny y de Nataly y en la pre-extraccion desde resumen, asi
    # que renumerar en silencio reasigna el trabajo de dos personas a estudios
    # que no leyeron.
    previo = {}
    if OUT.exists():
        with open(OUT, encoding="utf-8", newline="") as fh:
            for r in csv.DictReader(fh):
                previo.setdefault(r["clave"], int(r["estudio"]))
    siguiente = max(previo.values(), default=0) + 1

    filas = []
    situaciones = collections.Counter()
    nuevos = []
    orden_grupos = sorted(grupos.items(),
                          key=lambda kv: min(int(x["orden"]) for x in kv[1]))
    numero = {}
    for k, recs in orden_grupos:
        if k in previo:
            numero[k] = previo[k]
        else:
            numero[k] = siguiente
            siguiente += 1
            nuevos.append(k)
    n_est = len(orden_grupos)
    for k, recs in orden_grupos:
        tipos = {tipo_informe(r) for r in recs}
        if "articulo" in tipos:
            situacion = "extraible"
        elif "resumen de congreso" in tipos:
            situacion = "solo-resumen"
        else:
            situacion = "solo-registro"
        situaciones[situacion] += 1
        principal = sorted(recs, key=lambda r: (RANGO[tipo_informe(r)],
                                                0 if real_doi(r) or r["pmid"] else 1,
                                                -int(r["year"] or 0)))[0]
        for r in recs:
            filas.append({
                "estudio": numero[k], "clave": k, "situacion": situacion,
                "orden": r["orden"], "record_id": r["record_id"],
                "tipo_informe": tipo_informe(r),
                "informe_para_extraer": "SI" if r is principal else "no",
                "informes_del_estudio": len(recs),
                "anio": r["year"], "revista": r["journal"],
                "titulo": " ".join(r["title"].split()),
            })

    filas.sort(key=lambda f: (f["estudio"], int(f["orden"])))
    with open(OUT, "w", encoding="utf-8", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(filas[0].keys()))
        w.writeheader()
        w.writerows(filas)

    print("informes agrupados : %d" % len(ft))
    if previo:
        print("numeracion conservada de la ejecucion anterior: %d estudios"
              % (n_est - len(nuevos)))
        if nuevos:
            print("numeros nuevos asignados: %d" % len(nuevos))
    print("estudios distintos : %d" % n_est)
    for s, n in situaciones.most_common():
        print("   %-14s %d" % (s, n))
    multi = sum(1 for k, v in grupos.items() if len(v) > 1)
    print("estudios con más de un informe: %d" % multi)
    print("escrito %s" % OUT)


if __name__ == "__main__":
    main()
