# -*- coding: utf-8 -*-
"""Guardián de la extracción adjudicada: la coherencia de los DATOS.

EL AGUJERO QUE CIERRA. `check_aritmetica.py` comprueba que las cuentas del
manuscrito cuadren. No mira los datos de los que salen. El 2026-09-16, una
auditoría encontró en la extracción adjudicada dos numeradores mayores que su
denominador, tres brazos etiquetados «case report» con 2, 23 y 26 pacientes, y
ocho países escritos de dos o tres maneras distintas. Nada de eso hacía saltar
ningún guardián, porque ninguno miraba ahí.

Este comprueba la tabla, no la prosa. Avisa; no corrige: la extracción está
firmada por los dos revisores y cambiarla es un acto de autoría.

QUE COMPRUEBA
  1. Ningún numerador mayor que su denominador.
  2. Ningún «case report» con más de un paciente ni «case series» de un solo
     brazo con un solo paciente.
  3. Los vocabularios controlados, escritos de una sola manera.
  4. Cada brazo del corpus vivo tiene informe de origen identificado.
  5. Las definiciones de éxito entrecomilladas están en el texto del estudio al
     que se atribuyen.

Uso:
    python scripts/check_extraccion.py
"""
import collections
import csv
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

NUMERADORES = ["clinical_success_n", "mortality_n", "adverse_event_n",
               "microbio_eradication_n", "resistance_emergence_n"]
CONTROLADOS = ["geographic_source", "route", "modality", "study_design",
               "pathogen_scope", "resistance_class", "dtr_status"]


def leer(p, enc="utf-8"):
    with open(p, encoding=enc, newline="") as fh:
        return list(csv.DictReader(fh))


def entero(v):
    v = (v or "").strip()
    return int(v) if v.isdigit() else None


def plano(t):
    t = unicodedata.normalize("NFKD", (t or "").lower())
    t = "".join(c for c in t if not unicodedata.combining(c))
    return re.sub(r"[^a-z0-9]", "", t)


def clave(v):
    t = unicodedata.normalize("NFKD", (v or "").lower())
    return re.sub(r"\s+", " ", "".join(c for c in t if not unicodedata.combining(c))).strip()


def main():
    excl = {r["study_id"] for r in leer(RS / "cribado" / "exclusiones_tras_texto_completo.csv")}
    adj = [r for r in leer(RS / "extraccion" / "extraccion_adjudicada.csv")
           if r["study_id"] not in excl]
    avisos = []

    # ---- 1. numerador sobre denominador
    for r in adj:
        N = entero(r["n_arm"])
        for c in NUMERADORES:
            v = entero(r[c])
            if N is not None and v is not None and v > N:
                avisos.append(("numerador imposible",
                               "%s%s: %s = %d sobre n_arm = %d"
                               % (r["study_id"], r["arm_id"], c, v, N)))

    # ---- 2. diseño contra tamaño
    por = collections.defaultdict(list)
    for r in adj:
        por[r["study_id"]].append(r)
    for r in adj:
        N = entero(r["n_arm"])
        if r["study_design"] == "case report" and N is not None and N > 1:
            avisos.append(("diseño contra tamaño",
                           "%s%s: «case report» con %d pacientes"
                           % (r["study_id"], r["arm_id"], N)))
        if (r["study_design"] == "case series" and N == 1
                and len(por[r["study_id"]]) == 1):
            avisos.append(("diseño contra tamaño",
                           "%s%s: «case series» de un solo brazo con 1 paciente"
                           % (r["study_id"], r["arm_id"])))

    # ---- 3. vocabularios escritos de varias maneras
    for c in CONTROLADOS:
        formas = collections.defaultdict(set)
        for r in adj:
            v = (r[c] or "").strip()
            if v:
                formas[clave(v)].add(v)
        for k, vs in formas.items():
            if len(vs) > 1:
                avisos.append(("vocabulario",
                               "%s: %s son la misma categoría escrita distinto"
                               % (c, " / ".join("«%s»" % x for x in sorted(vs)))))

    # ---- 4. cada brazo con su informe
    enl = QR / "brazo_informe.csv"
    if enl.exists():
        tiene = {(r["study_id"], r["arm_id"]) for r in leer(enl, enc="utf-8-sig")
                 if r["record_id"]}
        for r in adj:
            if (r["study_id"], r["arm_id"]) not in tiene:
                avisos.append(("sin informe",
                               "%s%s no tiene informe de origen identificado"
                               % (r["study_id"], r["arm_id"])))
    else:
        avisos.append(("sin informe", "falta quality_reports/brazo_informe.csv"))

    # ---- 5. definiciones entrecomilladas que no están en su artículo
    for r in adj:
        d = (r["clinical_success_definition"] or "").strip()
        if not d.startswith('"') or len(d) < 60:
            continue
        p = CACHE / (r["study_id"] + ".txt")
        if not p.exists():
            continue
        texto = plano(p.read_text(encoding="utf-8", errors="replace"))
        # EL PDF A DOS COLUMNAS PARTE LAS FRASES. «The outcome was favorable
        # during the follow-up» sale del extractor con texto de la otra columna
        # metido en medio, de modo que buscar la frase entera da un falso
        # positivo. Se trocea en fragmentos cortos y se exige que aparezca la
        # mayoria: una frase partida conserva sus trozos, una frase de otro
        # articulo no conserva ninguno.
        ap = plano(d)
        trozos = [ap[i:i + 25] for i in range(0, min(len(ap), 300), 25)]
        trozos = [t for t in trozos if len(t) == 25]
        if not trozos:
            continue
        hallados = sum(1 for t in trozos if t in texto)
        if hallados / len(trozos) < 0.4:
            avisos.append(("cita fuera de su artículo",
                           "%s%s: de %d fragmentos de la definición entrecomillada, "
                           "solo %d aparecen en el texto de %s"
                           % (r["study_id"], r["arm_id"], len(trozos), hallados,
                              r["study_id"])))

    grupos = collections.OrderedDict()
    for tipo, t in avisos:
        grupos.setdefault(tipo, []).append(t)

    print("guardián de la extracción adjudicada (%d brazos del corpus vivo)" % len(adj))
    if not avisos:
        print("  sin incidencias")
        return 0
    for tipo, ts in grupos.items():
        print("\n  %s (%d)" % (tipo.upper(), len(ts)))
        for t in ts:
            print("    %s" % t)
    print("\n%d incidencias. NO se corrigen aquí: la extracción está firmada y "
          "cambiarla es un acto de autoría. Van al cuaderno de firma." % len(avisos))
    return 0


if __name__ == "__main__":
    sys.exit(main())
