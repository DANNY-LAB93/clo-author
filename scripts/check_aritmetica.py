"""Recalcula la aritmética del manuscrito sin mirar los escalares.

POR QUÉ HACE FALTA OTRO COMPROBADOR. Ya hay dos, y los dos comprueban contra el
canal: `check_manuscript_numbers.py` mira que toda cifra exista en algún
escalar, y `check_manuscript_claims.py` que cada frase lleve EL escalar que le
toca. Los dos dan por buena una cifra que el canal produce.

Este no mira el canal. Lee el manuscrito y **rehace las cuentas**: si el texto
dice «42 de 95 (44,2 %)», divide 42 entre 95 y compara; si dice que un flujo
pasa de 23 057 a 17 129 quitando 5 928, resta. Un escalar puede estar bien
calculado y aun así redactarse mal en la frase --el 68,0 % donde eran 68,9, o
«casi cuatro de cada diez» para un 44,2 %-- y eso solo se ve recalculando.

QUÉ COMPRUEBA
  1. Todo patrón «N de M (P %)» y sus variantes: P = 100·N/M.
  2. Las restas del flujo PRISMA, una a una.
  3. Las sumas declaradas: los 29 excluidos por motivo, los 155 = 132 + 23,
     los 95 = 92 + 3, los 155 = 95 + 60.
  4. Las expresiones de frecuencia («cuatro de cada diez», «uno de cada nueve»)
     contra el porcentaje que dicen glosar, con su dirección: «casi» exige que
     la cifra esté por debajo, «más de» que esté por encima.

Uso:
    python scripts/check_aritmetica.py [ruta_al_manuscrito]
"""
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
POR_DEFECTO = ROOT / "paper" / "manuscrito_JSR_final.md"
TOL = 0.06          # holgura de redondeo sobre un porcentaje con un decimal

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass


def num(s):
    """'23 057' o '74,7' -> float. Espacio fino, duro o normal como millar."""
    return float(re.sub(r"[\s  ]", "", s).replace(",", "."))


def limpia(t):
    """Fuera el marcado, y los espacios de millar a normales."""
    t = t.replace("**", "").replace("*", "")
    return re.sub(r"[  ]", " ", t)


# ---- 1. «N de M (P %)» en todas sus formas ---------------------------------
PATRONES = [
    # "En 69 de los 103 brazos (67,0 %)"  ·  "69 de 103 brazos extraídos (67,0 %)"
    re.compile(r"(\d[\d\s]*) de (?:los |las )?(\d[\d\s]*)[^.()]{0,40}?\(([\d,]+) %\)"),
    # "42 reportes de caso único (44,2 %)" -> el denominador no está en la frase
    # y se resuelve fuera; aquí no se toca.
]


def porcentajes(t):
    fallos = []
    for pat in PATRONES:
        for m in pat.finditer(t):
            n, d, p = num(m.group(1)), num(m.group(2)), num(m.group(3))
            if d == 0:
                continue
            real = 100.0 * n / d
            if abs(real - p) > TOL:
                fallos.append("«%s»  dice %.1f %%, pero %g/%g = %.1f %%"
                              % (m.group(0)[:70], p, n, d, real))
    return fallos


# ---- 2. las restas del flujo ------------------------------------------------
def flujo(t):
    """Cada paso declarado, rehecho. (antes, quitados, despues, etiqueta)."""
    fallos = []
    pasos = [
        (r"aportaron \*?\*?([\d\s]+) registros\*?\*?, de los que se eliminaron "
         r"([\d\s]+) duplicados para dejar \*?\*?([\d\s]+) informes",
         "identificación − duplicados"),
        (r"excluyeron ([\d\s]+); de los ([\d\s]+) t[ií]tulos cribados se "
         r"excluyeron ([\d\s]+) y avanzaron ([\d\s]+)",
         "títulos cribados − excluidos"),
    ]
    m = re.search(pasos[0][0], t)
    if m:
        a, q, d = num(m.group(1)), num(m.group(2)), num(m.group(3))
        if abs(a - q - d) > 0.5:
            fallos.append("%s: %g − %g = %g, el texto dice %g"
                          % (pasos[0][1], a, q, a - q, d))
    m = re.search(pasos[1][0], t)
    if m:
        crib, exc, av = num(m.group(2)), num(m.group(3)), num(m.group(4))
        if abs(crib - exc - av) > 0.5:
            fallos.append("%s: %g − %g = %g, el texto dice %g"
                          % (pasos[1][1], crib, exc, crib - exc, av))
    m = re.search(r"avanzaron ([\d\s]+) a lectura de resumen; de estos se "
                  r"excluyeron ([\d\s]+) y \*?\*?([\d\s]+) informes pasaron", t)
    if m:
        a, e, q = num(m.group(1)), num(m.group(2)), num(m.group(3))
        if abs(a - e - q) > 0.5:
            fallos.append("resumen: %g − %g = %g, el texto dice %g"
                          % (a, e, a - e, q))
    return fallos


# ---- 3. las sumas declaradas ------------------------------------------------
NUM_ES = {"uno": 1, "dos": 2, "tres": 3, "cuatro": 4, "cinco": 5, "seis": 6,
          "siete": 7, "ocho": 8, "nueve": 9, "diez": 10, "once": 11, "doce": 12}


def sumas(t):
    fallos = []
    # los 29 excluidos, enumerados en letra dentro de un solo párrafo
    m = re.search(r"Los (\d+) excluidos en la fase de texto completo se "
                  r"reparten as[ií]:(.+?)\n", t, re.S)
    if m:
        total, cuerpo = int(m.group(1)), m.group(2)
        # El primer sumando va pegado a los dos puntos del encabezado
        # («se reparten así: once no tienen...»), y sin admitir «:» aquí el
        # comprobador se dejaba fuera el mayor de todos y acusaba en falso.
        piezas = re.findall(r"(?:^\s*|[;.:]\s+|\by )(%s|\d+)\s+(?:no|son|"
                            r"quedaron|administran|aportan|se excluy)"
                            % "|".join(NUM_ES), cuerpo, re.I)
        vals = [NUM_ES.get(x.lower(), None) or int(x) for x in piezas]
        if vals and sum(vals) != total:
            fallos.append("los %d excluidos: la enumeración suma %d (%s)"
                          % (total, sum(vals), " + ".join(map(str, vals))))
        elif not vals:
            fallos.append("los %d excluidos: no pude leer la enumeración" % total)
    # 155 = 132 con un informe + 23 con varios
    m = re.search(r"queda en \*?\*?(\d+) estudios\*?\*?[^.]*?: (\d+) con un solo "
                  r"informe y (\d+) con varios", t)
    if m:
        tot, a, b = (int(m.group(i)) for i in (1, 2, 3))
        if a + b != tot:
            fallos.append("estudios: %d + %d = %d, el texto dice %d"
                          % (a, b, a + b, tot))
    # 95 = 92 artículos + 3 solo-resumen ; y 155 = 95 + 60
    m = re.search(r"De los (\d+) estudios, \*?\*?(\d+) tienen publicaci[oó]n "
                  r"recuperable\*?\*?: (\d+) art[ií]culos y (\d+) que solo", t)
    if m:
        tot, rec, art, res = (int(m.group(i)) for i in range(1, 5))
        if art + res != rec:
            fallos.append("recuperables: %d + %d = %d, el texto dice %d"
                          % (art, res, art + res, rec))
        m2 = re.search(r"Los \*?\*?(\d+) restantes son [uú]nicamente fichas", t)
        if m2 and rec + int(m2.group(1)) != tot:
            fallos.append("corpus: %d + %s = %d, el texto dice %d"
                          % (rec, m2.group(1), rec + int(m2.group(1)), tot))
    return fallos


# ---- 4. «cuatro de cada diez» y su dirección --------------------------------
def frecuencias(t):
    """Comprueba la glosa verbal contra el porcentaje que acompaña.

    «Casi X de cada Y» exige estar POR DEBAJO de X/Y; «más de», por encima.
    Es el error que se coló dos veces con el 44,2 % de casos únicos.
    """
    fallos = []
    pat = re.compile(r"(casi|m[aá]s de|solo|s[oó]lo)?\s*(%s) de cada (%s)"
                     % ("|".join(NUM_ES), "|".join(NUM_ES)), re.I)
    for m in pat.finditer(t):
        adv = (m.group(1) or "").lower()
        a, b = NUM_ES[m.group(2).lower()], NUM_ES[m.group(3).lower()]
        frac = 100.0 * a / b
        # el porcentaje al que glosa: el mas cercano en la misma frase
        ini = t.rfind(".", 0, m.start()) + 1
        fin = t.find(".", m.end())
        frase = t[ini:fin if fin > 0 else len(t)]
        cifras = [num(x) for x in re.findall(r"([\d,]+) %", frase)]
        if not cifras:
            continue
        real = min(cifras, key=lambda c: abs(c - frac))
        if abs(real - frac) > 12:      # glosa de otra cosa, no de esta cifra
            continue
        if adv.startswith("casi") and real >= frac:
            fallos.append("«%s» glosa %.1f %%, que NO está por debajo de %.1f %%"
                          % (m.group(0).strip(), real, frac))
        if adv.startswith(("mas de", "más de")) and real <= frac:
            fallos.append("«%s» glosa %.1f %%, que NO está por encima de %.1f %%"
                          % (m.group(0).strip(), real, frac))
    return fallos


def main():
    ruta = pathlib.Path(sys.argv[1]) if len(sys.argv) > 1 else POR_DEFECTO
    t = limpia(ruta.read_text(encoding="utf-8"))
    bloques = [("porcentajes contra su denominador", porcentajes(t)),
               ("restas del flujo PRISMA", flujo(t)),
               ("sumas declaradas", sumas(t)),
               ("glosas de frecuencia", frecuencias(t))]
    total = sum(len(f) for _, f in bloques)
    print("aritmética de %s" % ruta.name)
    for nombre, f in bloques:
        print("  %-36s %s" % (nombre, "OK" if not f else "%d FALLO(S)" % len(f)))
        for x in f:
            print("     - %s" % x)
    print()
    print("la aritmética del manuscrito cuadra" if not total
          else "%d desajuste(s) que rehacer" % total)
    return 1 if total else 0


if __name__ == "__main__":
    sys.exit(main())
