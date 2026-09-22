# -*- coding: utf-8 -*-
"""¿Hay pacientes contados dos veces en el corpus?

POR QUE EXISTE. La auditoría del 2026-09-16 anotó que no se había examinado el
solapamiento de pacientes entre estudios. En esta literatura el riesgo es
concreto y no teórico: los centros que hacen fagoterapia son pocos, un mismo
paciente se publica primero como reporte de caso y después entra en la serie
del centro, y las series grandes recogen casos tratados en otros hospitales con
el mismo producto. Si dos estudios del corpus describen al mismo paciente, ese
paciente pesa dos veces en cualquier recuento.

QUE BUSCA, Y CON QUE FUERZA

  A. **Cita cruzada.** El texto de A nombra a B: por DOI, PMID, NCT o por ocho
     palabras seguidas de su título. Sola, es una señal débil: casi todas las
     citas cruzadas son citas de discusión.
  B. **Marca de publicación previa.** Cerca de esa cita, o en una columna de
     tabla, el artículo dice que un caso ya se publicó: «previously published»,
     «published case», «reported elsewhere», «ya descrito». Se excluye a
     propósito «as previously described», que en estos artículos casi siempre
     introduce un método de laboratorio y no un paciente.
  C. **Mismo producto y mismo país.** Dos estudios que usan el mismo preparado
     en el mismo país y en años que se tocan pueden compartir pacientes aunque
     ninguno lo diga.

Un par con A+B es un candidato firme; con A+C o solo C, un candidato a
comprobar leyendo. El script NO decide: marca, cita la frase y deja la lectura.

SALIDA
    quality_reports/solapamiento_candidatos.csv
    quality_reports/solapamiento_lectura.md   los fragmentos, para leerlos
"""
import csv
import collections
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

# Preparados que aparecen con nombre propio en esta literatura. La lista se
# construyó leyendo los textos, no de memoria: cada entrada aparece al menos
# en un artículo del corpus.
PRODUCTOS = ["PASA16", "BX004", "AB-PA01", "AP-PA02", "PP1131", "Pyophage",
             "Intesti", "Sextaphage", "Phagoburn", "PhagoBurn", "TP-102",
             "BFC-1", "Pyo bacteriophage", "WRAIR", "Biophage-PA", "PhageBank",
             "Phage4Cure", "Navy phage", "IPATH", "Eliava"]

# «as previously described» introduce un método, no un paciente: se excluye.
MARCA = re.compile(
    r"(?<!as )previously (published|reported)"
    r"|published (case|elsewhere|report of this)"
    r"|(case|patient)s? (has|have|was|were) (been )?(previously )?(published|reported)"
    r"|reported (previously |earlier )?elsewhere"
    r"|already (published|reported)"
    r"|ya (publicad|descrit|reportad)"
    r"|publicado previamente"
    r"|same patient|el mismo paciente"
    r"|overlap(ping)? (with|patients|cases)", re.I)

# «N de los M casos ya se habian publicado»: la frase que remite a las
# referencias por numero y que ninguna comprobacion por titulo alcanza.
DECLARA = re.compile(
    r"(were|was|have been|has been) previously (reported|published)"
    r"|previously (reported|published) (in|elsewhere|cases)"
    r"|of the \d+ .{0,40}(cases|patients).{0,40}previously"
    r"|\d+ of (the )?\d+ .{0,30}(cases|patients)", re.I)

VACIAS = set("""the of and in for with a an to on by from at as is are was were this that
these those we our their its be been has have had which who whom using used case cases
patient patients report reports study studies treatment therapy use versus vs new novel""".split())


def sin_acentos(t):
    t = unicodedata.normalize("NFKD", t.lower())
    return "".join(c for c in t if not unicodedata.combining(c))


def plano(t):
    return re.sub(r"[^a-z0-9]", "", sin_acentos(t))


def mapa(texto):
    """Texto aplanado (sin espacios ni signos) y el índice a la posición
    original de cada carácter: los PDF llegan con las palabras pegadas."""
    ap, idx = [], []
    for k, c in enumerate(sin_acentos(texto)):
        if re.match(r"[a-z0-9]", c):
            ap.append(c)
            idx.append(k)
    idx.append(len(texto))
    return "".join(ap), idx


def leer(p, enc="utf-8"):
    with open(p, encoding=enc, newline="") as fh:
        return list(csv.DictReader(fh))


def normaliza_pais(p):
    p = sin_acentos((p or "").strip())
    p = re.sub(r"\s+", " ", p)
    return {"estados unidos": "eeuu", "usa": "eeuu", "eeuu": "eeuu"}.get(p, p)


def clave_titulo(t, n=8):
    """Las n primeras palabras con significado del título, pegadas. Sirve para
    encontrar el título dentro de una lista de referencias de un PDF."""
    ps = [w for w in re.findall(r"[a-z0-9]+", sin_acentos(t)) if w not in VACIAS and len(w) > 2]
    return "".join(ps[:n]) if len(ps) >= n else ""


def main():
    grupos = leer(RS / "cribado" / "study_groups.csv")
    excl = {r["study_id"] for r in leer(RS / "cribado" / "exclusiones_tras_texto_completo.csv")}
    corpus = {r["record_id"]: r for r in leer(RS / "cribado" / "screening_corpus_all.csv")}
    adj = [r for r in leer(RS / "extraccion" / "extraccion_adjudicada.csv")
           if r["study_id"] not in excl]

    est = {}
    for g in grupos:
        eid = "EST-%03d" % int(g["estudio"])
        if eid in excl:
            continue
        d = est.setdefault(eid, {"titulos": [], "ids": set(), "anio": g["anio"],
                                 "revista": g["revista"], "designado": ""})
        d["titulos"].append(g["titulo"])
        if g["informe_para_extraer"] == "SI":
            d["designado"] = g["titulo"]
            d["anio"] = g["anio"]
        rc = corpus.get(g["record_id"], {})
        for k in ("doi", "pmid", "nct"):
            v = (rc.get(k) or "").strip()
            # los DOI de Cochrane CENTRAL son del registro, no del artículo
            if v and len(v) >= 7 and not v.startswith("10.1002/central"):
                d["ids"].add(v)

    pacientes, pais = {}, {}
    for r in adj:
        e = r["study_id"]
        n = r["n_arm"].strip()
        pacientes[e] = pacientes.get(e, 0) + (int(n) if n.isdigit() else 0)
        if e not in pais or pais[e] == "na":
            pais[e] = normaliza_pais(r["geographic_source"])

    textos = {}
    for e in est:
        p = CACHE / (e + ".txt")
        if p.exists():
            t = p.read_text(encoding="utf-8", errors="replace")
            textos[e] = (t,) + mapa(t)

    # ---------------------------------------------------------- A: citas
    citas = collections.defaultdict(list)
    for a, (texto, ap, idx) in textos.items():
        for b, d in est.items():
            if b == a:
                continue
            golpes = []
            for v in d["ids"]:
                # El PDF a dos columnas parte los DOI: «10.1016/» se queda en
                # una columna y «j.medj.2023.07.002» en la otra, de modo que
                # el DOI entero no aparece nunca seguido. El sufijo sí, y es
                # bastante distintivo por sí solo.
                claves = [plano(v)]
                if "/" in v:
                    suf = plano(v.rsplit("/", 1)[1])
                    if len(suf) >= 10:
                        claves.append(suf)
                for k in claves:
                    if k and k in ap:
                        golpes.append((ap.index(k), "identificador " + v))
                        break
            for t in d["titulos"]:
                k = clave_titulo(t, 14)
                if not k:
                    continue
                # EL PDF A DOS COLUMNAS PARTE LOS TITULOS DE LA BIBLIOGRAFIA.
                # La referencia 21 de EST-108 sale asi: «Racenis, K. et al. Use
                # of phage cocktail BFC 1.10 in 41. Rose, T. et al. Experimental
                # phage therapy of burn wound combination with ceftazidime-
                # avibactam...». El titulo entero no aparece nunca seguido; sus
                # trozos si. Exigir el titulo completo dejaba fuera seis
                # estudios que EST-108 declara haber publicado antes.
                trozos = [k[i:i + 20] for i in range(0, len(k), 20)]
                trozos = [x for x in trozos if len(x) == 20]
                hall = [x for x in trozos if x in ap]
                if trozos and len(hall) / len(trozos) >= 0.4:
                    golpes.append((ap.index(hall[0]),
                                   "título (%d de %d trozos)" % (len(hall), len(trozos))))
                    break
            if golpes:
                i, como = min(golpes)
                a0, b0 = idx[max(0, i - 40)], idx[min(len(idx) - 1, i + 120)]
                citas[(a, b)] = [como, re.sub(r"\s+", " ", texto[a0:b0]).strip()]

    # ------------------------------------------------- B: marcas de previa
    marcas = collections.defaultdict(list)
    for a, (texto, ap, idx) in textos.items():
        llano = re.sub(r"\s+", " ", texto)
        for m in MARCA.finditer(llano):
            marcas[a].append(llano[max(0, m.start() - 220):m.start() + 240].strip())
        # columna «Published case» de las tablas de series
        for m in re.finditer(r"publish\s*ed\s*case|published\s*$", llano, re.I):
            frag = llano[max(0, m.start() - 160):m.start() + 200].strip()
            if frag not in marcas[a]:
                marcas[a].append(frag)

    # --------------------------------------- C: mismo producto y mismo país
    # Un producto NOMBRADO TRES VECES O MAS es el que el estudio usa; una o dos
    # menciones son la discusión o la lista de referencias. El umbral es
    # arbitrario y por eso se publica el recuento junto al par, para que quien
    # lea decida si le convence.
    MINIMO = 3
    prod, veces = {}, {}
    for e, (texto, ap, idx) in textos.items():
        cuenta = {p: ap.count(plano(p)) for p in PRODUCTOS}
        veces[e] = cuenta
        prod[e] = {p for p, n in cuenta.items() if n >= MINIMO}

    filas = []
    vistos = set()
    for (a, b), (como, frag) in citas.items():
        mismo_pais = pais.get(a, "na") == pais.get(b, "na") != "na"
        comp = sorted(prod.get(a, set()) & prod.get(b, set()))
        cerca = [f for f in marcas.get(a, [])
                 if clave_titulo(est[b]["designado"])[:20] in plano(f)
                 or any(plano(v) in plano(f) for v in est[b]["ids"])]
        # EL AGUJERO QUE ESTO CIERRA. EST-108 declara «Twenty-seven of the 100
        # BT cases/patients were previously reported6,13-26» y remite a sus
        # referencias por NUMERO. La marca esta, la cita esta, y no se tocan:
        # el numero volado no lleva el titulo al lado. Exigir que la marca
        # nombre a B dejaba fuera los siete pacientes que EST-108 comparte con
        # seis estudios del corpus. Si A declara casos ya publicados y ADEMAS
        # cita a B, el par se marca firme y se lee.
        declara = [f for f in marcas.get(a, []) if DECLARA.search(f)]
        if cerca:
            fuerza = "firme: cita + marca de publicación previa"
        elif declara:
            fuerza = "firme: A declara casos ya publicados y cita a B"
            frag = declara[0]
        elif comp and mismo_pais:
            fuerza = "a comprobar: cita + mismo producto y país"
        elif comp:
            fuerza = "a comprobar: cita + mismo producto"
        else:
            continue
        vistos.add((a, b))
        filas.append({
            "estudio_a": a, "estudio_b": b, "fuerza": fuerza,
            "como_lo_nombra": como,
            "producto_comun": "; ".join("%s (%d/%d menciones)"
                                        % (c, veces.get(a, {}).get(c, 0),
                                           veces.get(b, {}).get(c, 0)) for c in comp),
            "pais_a": pais.get(a, ""), "pais_b": pais.get(b, ""),
            "pacientes_a": pacientes.get(a, 0), "pacientes_b": pacientes.get(b, 0),
            "anio_a": est[a]["anio"], "anio_b": est[b]["anio"],
            "fragmento": (cerca[0] if cerca else frag)[:400],
        })

    # pares sin cita pero con producto y país en común: el residuo honesto
    nombres = sorted(est)
    for i, a in enumerate(nombres):
        for b in nombres[i + 1:]:
            if (a, b) in vistos or (b, a) in vistos:
                continue
            comp = sorted(prod.get(a, set()) & prod.get(b, set()))
            if comp and pais.get(a, "na") == pais.get(b, "na") != "na":
                filas.append({
                    "estudio_a": a, "estudio_b": b,
                    "fuerza": "a comprobar: mismo producto y país, sin cita entre ellos",
                    "como_lo_nombra": "",
                    "producto_comun": "; ".join("%s (%d/%d menciones)"
                                                % (c, veces.get(a, {}).get(c, 0),
                                                   veces.get(b, {}).get(c, 0)) for c in comp),
                    "pais_a": pais.get(a, ""), "pais_b": pais.get(b, ""),
                    "pacientes_a": pacientes.get(a, 0), "pacientes_b": pacientes.get(b, 0),
                    "anio_a": est[a]["anio"], "anio_b": est[b]["anio"],
                    "fragmento": "",
                })

    orden = {"firme": 0, "a comprobar: cita + mismo producto y país": 1}
    filas.sort(key=lambda f: (0 if f["fuerza"].startswith("firme") else 1,
                              f["estudio_a"], f["estudio_b"]))
    salida = QR / "solapamiento_candidatos.csv"
    with salida.open("w", encoding="utf-8-sig", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(filas[0].keys()))
        w.writeheader()
        w.writerows(filas)

    L = ["# Solapamiento de pacientes: lo que hay que leer", "",
         "Generado por `scripts/detecta_solapamiento.py` sobre los %d textos completos"
         % len(textos), "del corpus vivo. Cada fragmento es literal del artículo.", ""]
    for e in sorted(marcas):
        if not marcas[e]:
            continue
        L += ["## %s — %s" % (e, est[e]["designado"][:90]), ""]
        for f in marcas[e][:8]:
            L += ["> " + re.sub(r"\s+", " ", f)[:600], ""]
    (QR / "solapamiento_lectura.md").write_text("\n".join(L), encoding="utf-8", newline="\n")

    firmes = [f for f in filas if f["fuerza"].startswith("firme")]
    print("%d textos examinados; %d pares candidatos -> %s"
          % (len(textos), len(filas), salida.name))
    print("  firmes (cita + marca de publicación previa): %d" % len(firmes))
    for f in firmes:
        print("    %s <-> %s  %s" % (f["estudio_a"], f["estudio_b"], f["producto_comun"]))
    print("  estudios con alguna marca de publicación previa: %d"
          % sum(1 for e in marcas if marcas[e]))


if __name__ == "__main__":
    main()
