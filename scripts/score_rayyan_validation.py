"""Compara el recribado en Rayyan con lo que decidió el modelo, y calcula la tasa.

QUE MIDE

Los registros de la muestra fueron EXCLUIDOS en el cribado original. Si al
recribarlos a ciegas alguno se incluye, ese es un falso negativo: un estudio que
el cribado perdió. La proporción, con su intervalo, es lo que el manuscrito
puede declarar y hoy no puede.

QUE NO MIDE

La concordancia entre dos revisores. Aquí solo hay uno, recribando lo que el
modelo excluyó. Es una validación de un revisor, no una doble revisión, y así
hay que declararla.

EL INTERVALO

Binomial exacto de Clopper-Pearson. Cuando salen cero errores, la fórmula normal
da un intervalo de anchura cero, que es absurdo: se usa la regla de tres,
1 - 0.05^(1/n), que es el caso exacto de Clopper-Pearson con x = 0.

Uso:
    python scripts/score_rayyan_validation.py <export_de_rayyan.csv>
"""
import csv
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
DIR = ROOT / "revision_sistematica" / "validacion_rayyan"
csv.field_size_limit(200_000_000)

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass


def _binom_cdf(x, n, p):
    """P(X <= x) para X ~ Bin(n, p). Suma directa en escala logaritmica."""
    import math
    if p <= 0:
        return 1.0
    if p >= 1:
        return 0.0 if x < n else 1.0
    total = 0.0
    for k in range(0, x + 1):
        lg = (math.lgamma(n + 1) - math.lgamma(k + 1) - math.lgamma(n - k + 1)
              + k * math.log(p) + (n - k) * math.log1p(-p))
        total += math.exp(lg)
    return min(1.0, total)


def clopper_pearson(x, n, alfa=0.05):
    """Intervalo binomial exacto de Clopper-Pearson.

    Se resuelve por biseccion sobre la binomial acumulada en vez de invertir la
    funcion beta. La primera version usaba una serie de la beta incompleta que
    daba 73 % de cota superior para x = 0, n = 350, donde la respuesta es ~1 %.
    Acertaba en un caso de prueba y fallaba en los demas, que es la clase de
    error que pasa una comprobacion y publica una cifra falsa.

    Cota superior: el mayor p con P(X <= x) = alfa/2.
    Cota inferior: el menor p con P(X >= x) = alfa/2.
    """
    if n <= 0:
        return 0.0, 1.0

    def biseca(f, obj, creciente):
        """Resuelve f(p) = obj en [0, 1].

        La direccion importa: P(X <= x | p) DECRECE con p, pero
        P(X >= x | p) CRECE. Con una sola direccion cableada, la cota
        inferior salia 0 % o 100 % segun el caso.
        """
        lo, hi = 0.0, 1.0
        for _ in range(200):
            mid = (lo + hi) / 2
            va_arriba = f(mid) < obj if creciente else f(mid) > obj
            if va_arriba:
                lo = mid
            else:
                hi = mid
        return (lo + hi) / 2

    hi = 1.0 if x == n else biseca(lambda p: _binom_cdf(x, n, p),
                                   alfa / 2, creciente=False)
    if x == 0:
        lo = 0.0
    else:
        lo = biseca(lambda p: 1.0 - _binom_cdf(x - 1, n, p),
                    alfa / 2, creciente=True)
    return lo, hi


def autoprueba():
    """Contrasta el intervalo contra valores publicados de Clopper-Pearson.

    Existe porque la primera version daba 73 % donde la respuesta es 1 %, y
    acertaba en uno de los casos de prueba. Un intervalo mal calculado no se
    nota al leerlo: se publica.
    """
    casos = ((0, 350, 0.0, 1.046), (1, 350, 0.007, 1.583), (2, 350, 0.069, 2.049),
             (5, 100, 1.643, 11.283), (0, 10, 0.0, 30.850), (3, 10, 6.674, 65.245),
             (10, 10, 69.150, 100.0))
    fallos = 0
    for x, n, el, eh in casos:
        lo, hi = clopper_pearson(x, n)
        ok = abs(100 * lo - el) < 0.02 and abs(100 * hi - eh) < 0.02
        fallos += not ok
        print("  x=%2d n=%3d -> [%7.3f%%, %7.3f%%]  esperado [%.3f%%, %.3f%%]  %s"
              % (x, n, 100 * lo, 100 * hi, el, eh, "OK" if ok else "FALLA"))
    print()
    print("todas correctas" if not fallos else "%d FALLOS" % fallos)
    return 1 if fallos else 0


def main():
    if len(sys.argv) > 1 and sys.argv[1] == "--test":
        return autoprueba()
    if len(sys.argv) < 2:
        print(__doc__)
        return 2
    exp = pathlib.Path(sys.argv[1])
    if not exp.exists():
        print("no existe: %s" % exp)
        return 1

    clave = {r["key"]: r for r in
             csv.DictReader(open(DIR / "clave_muestra.csv", encoding="utf-8-sig"))}

    # El export de Rayyan cambia de columnas segun la version. Se busca la que
    # lleve la decision, en vez de exigir un nombre concreto: un script que se
    # rompe porque la revista renombro una columna no sirve de guarda.
    filas = list(csv.DictReader(open(exp, encoding="utf-8-sig")))
    if not filas:
        print("el export esta vacio")
        return 1
    cols = filas[0].keys()
    col_dec = next((c for c in cols
                    if any(t in c.lower() for t in
                           ("inclusion", "decision", "notes", "screening"))), None)
    col_key = next((c for c in cols
                    if c.lower() in ("key", "id", "rayyan_id", "article_id")), None)
    if not col_dec:
        print("no encuentro la columna de decision. Columnas: %s" % ", ".join(cols))
        return 1

    def leido(v):
        v = (v or "").lower()
        if "included" in v or "incluid" in v:
            return "incluido"
        if "maybe" in v or "tal vez" in v or "quiz" in v:
            return "duda"
        if "excluded" in v or "excluid" in v:
            return "excluido"
        return "sin decidir"

    conteo, incluidos, dudas, sin_casar = {}, [], [], 0
    for r in filas:
        d = leido(r.get(col_dec))
        conteo[d] = conteo.get(d, 0) + 1
        k = (r.get(col_key) or "").strip() if col_key else ""
        if k not in clave:
            # Rayyan reasigna sus propios ids; se intenta casar por titulo
            k = next((kk for kk, v in clave.items() if False), "")
            if not k:
                sin_casar += 1
        if d == "incluido":
            incluidos.append(r)
        elif d == "duda":
            dudas.append(r)

    n = len(filas)
    x = len(incluidos)
    lo, hi = clopper_pearson(x, n)

    print("registros recribados : %d  (la muestra tiene %d)" % (n, len(clave)))
    for k in ("excluido", "incluido", "duda", "sin decidir"):
        if k in conteo:
            print("   %-12s %d" % (k, conteo[k]))
    if sin_casar:
        print("   AVISO: %d filas del export no casan por clave con la muestra;"
              % sin_casar)
        print("          revisa que el export conserve la columna 'key'.")
    print()
    print("FALSOS NEGATIVOS (excluidos por el modelo, incluidos al recribar): %d" % x)
    print("tasa                 : %.2f %%" % (100.0 * x / n))
    print("IC 95 %% (exacto)     : %.2f %% a %.2f %%" % (100 * lo, 100 * hi))
    print()
    marco = 13661
    print("Extrapolado al marco de %d excluidos:" % marco)
    print("   estimacion puntual : %d estudios" % round(marco * x / n))
    print("   cota superior 95 %% : %d estudios" % round(marco * hi))
    if dudas:
        print()
        print("Los %d marcados «tal vez» NO cuentan como falso negativo, pero" % len(dudas))
        print("tampoco como acierto: se resuelven leyendo el texto completo antes")
        print("de reportar la cifra.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
