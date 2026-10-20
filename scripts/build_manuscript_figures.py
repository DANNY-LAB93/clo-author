"""Dibuja las dos figuras del manuscrito desde las cifras del canal.

Figura 1: diagrama de flujo PRISMA 2020 con las corrientes de bases
bibliograficas y de registros de ensayos separadas, como exige la declaracion.
Figura 2: composicion del cuerpo de evidencia por diseno y por ano.

NINGUNA CIFRA SE TECLEA. Todas salen de synthesis_scalars.json, de modo que una
figura no puede quedar desfasada respecto al texto sin que falle el generador.
Sin titulo dentro de la figura: el titulo va en el pie, en el manuscrito.

SALIDA
    paper/figuras/figura_1_prisma.pdf  y  .png
    paper/figuras/figura_2_composicion.pdf  y  .png
"""
import collections
import csv
import json
import pathlib
import sys

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch

ROOT = pathlib.Path(__file__).resolve().parent.parent
RS = ROOT / "revision_sistematica"
OUT = ROOT / "paper" / "figuras"
csv.field_size_limit(200_000_000)
try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

plt.rcParams.update({
    "font.family": "serif",
    "font.serif": ["DejaVu Serif"],
    "font.size": 8.5,
    "axes.linewidth": 0.7,
})
TINTA = "#1a1a1a"
BORDE = "#555555"
SUAVE = "#f2f2f0"
ACENTO = "#2b5d7d"
NEUTRO = "#b8b8b0"
FINO = " "          # espacio fino, separador de millares tipografico
ALTO_FIG = 9.2


def caja(ax, x, y, w, h, texto, relleno="white", tam=8.0):
    ax.add_patch(FancyBboxPatch(
        (x, y), w, h, boxstyle="round,pad=0.006,rounding_size=0.010",
        linewidth=0.8, edgecolor=BORDE, facecolor=relleno, zorder=2))
    ax.text(x + w / 2, y + h / 2, texto, ha="center", va="center",
            fontsize=tam, color=TINTA, zorder=3, linespacing=1.5)


def flecha(ax, xy1, xy2, estilo=None):
    ax.add_patch(FancyArrowPatch(
        xy1, xy2, arrowstyle="-|>", mutation_scale=8, linewidth=0.8,
        color=BORDE, shrinkA=0, shrinkB=0, zorder=1,
        connectionstyle=estilo) if estilo else FancyArrowPatch(
        xy1, xy2, arrowstyle="-|>", mutation_scale=8, linewidth=0.8,
        color=BORDE, shrinkA=0, shrinkB=0, zorder=1))


def mil(n):
    return f"{n:,}".replace(",", FINO)


# Las fuentes de la corriente de registros de ensayos. Es la misma regla que
# build_synthesis_scalars (REGISTROS): un informe que llega por las dos
# corrientes se asigna a bases. Se comprueba contra sus escalares.
REGISTROS = {"ClinicalTrials.gov", "EudraCT", "CTIS"}


def identificacion_por_corriente(S):
    """Registros identificados en cada corriente, ANTES de deduplicar, y el
    rótulo de fuentes de la caja de bases.

    ESCALAR NUEVO, calculado aquí (no está en synthesis_scalars.json):
    registros_bases = suma de n_source_records de los informes de la corriente
    de bases, sobre screening_corpus_all.csv, el mismo fichero y la misma
    columna de los que build_synthesis_scalars saca registros_identificados.
    Si las dos corrientes no suman registros_identificados, si las fuentes no
    suman fuentes_distintas_n o si la corriente de registros trae duplicados
    (la figura la hace entrar sin pasar por la deduplicación), se para."""
    with open(RS / "cribado" / "screening_corpus_all.csv", encoding="utf-8",
              newline="") as fh:
        corpus = list(csv.DictReader(fh))
    reg_b = reg_r = inf_b = inf_r = 0
    for c in corpus:
        f = {x.strip() for x in c["sources"].split(";") if x.strip()}
        n = int(c["n_source_records"] or 1)
        if f - REGISTROS:
            reg_b, inf_b = reg_b + n, inf_b + 1
        elif f:
            reg_r, inf_r = reg_r + n, inf_r + 1
    nombres = set(S["fuentes_nombres"])
    bases_distintas = S["fuentes_distintas_n"] - S["fuentes_registros_n"]
    fallos = []
    if reg_b + reg_r != S["registros_identificados"]:
        fallos.append("bases %d + registros %d != registros_identificados %d"
                      % (reg_b, reg_r, S["registros_identificados"]))
    if (inf_b, inf_r) != (S["informes_de_bases"], S["informes_de_registros"]):
        fallos.append("informes por corriente (%d, %d) != escalares (%d, %d)"
                      % (inf_b, inf_r, S["informes_de_bases"],
                         S["informes_de_registros"]))
    if len(nombres & REGISTROS) != S["fuentes_registros_n"]:
        fallos.append("REGISTROS no coincide con fuentes_registros_n")
    if S["fuentes_bases_n"] + S["fuentes_registros_n"] != S["fuentes_brazos_n"]:
        fallos.append("brazos de bases + registros != fuentes_brazos_n")
    if reg_r != inf_r:
        fallos.append("la corriente de registros trae %d duplicados y la figura "
                      "no la deduplica" % (reg_r - inf_r))
    if reg_b - inf_b != S["duplicados_eliminados"]:
        fallos.append("duplicados de bases %d != duplicados_eliminados %d"
                      % (reg_b - inf_b, S["duplicados_eliminados"]))
    if fallos:
        raise SystemExit("Figura 1, identificación: " + "; ".join(fallos))
    rotulo = ("%d fuentes, %d brazos de búsqueda"
              % (bases_distintas, S["fuentes_bases_n"])
              if S["fuentes_bases_n"] != bases_distintas
              else "%d fuentes" % bases_distintas)
    return {"registros_bases": reg_b, "registros_registros": reg_r,
            "fuentes_bases_rotulo": rotulo}


def restas_del_flujo(S):
    """Cada caja de excluidos cuelga de la caja que se cribó en ese paso, así
    que la figura afirma «caja − excluidos = caja siguiente». Se comprueba con
    los escalares antes de dibujar, y también que los motivos de cada caja gris
    sumen su total. Si algo no cuadra, se para."""
    pasos = (
        ("registros_identificados", "duplicados_eliminados", "informes_unicos"),
        ("informes_unicos", "excluidos_etapa1", "cribados_por_titulo"),
        ("cribados_por_titulo", "excluidos_titulo", "a_resumen"),
        ("a_resumen", "excluidos_resumen", "informes_a_texto_completo"),
        ("estudios_antes_de_releer", "estudios_excluidos_tras_texto_completo",
         "estudios"),
        ("informes_a_texto_completo", "informes_excluidos_tras_texto_completo",
         "informes_agrupados"))
    fallos = ["%s %d - %s %d != %s %d" % (a, S[a], b, S[b], c, S[c])
              for a, b, c in pasos if S[a] - S[b] != S[c]]
    for total, mot in (("excluidos_titulo", "exclusiones_titulo"),
                       ("excluidos_resumen", "exclusiones_resumen"),
                       ("estudios_excluidos_tras_texto_completo",
                        "exclusiones_tras_texto_completo")):
        if sum(S[mot].values()) != S[total]:
            fallos.append("los motivos de %s suman %d y %s es %d"
                          % (mot, sum(S[mot].values()), total, S[total]))
    if fallos:
        raise SystemExit("Figura 1, restas del flujo: " + "; ".join(fallos))


def figura_prisma(S):
    """Flujo PRISMA 2020 con las dos corrientes de identificacion separadas.

    La altura de cada caja se DERIVA del numero de lineas de su texto. Fijarla a
    mano funciona hasta que un rotulo gana una linea, y entonces el texto
    desborda por arriba y por abajo sin que nada avise: fue lo que paso en el
    primer intento con las dos cajas de motivos de exclusion.
    """
    restas_del_flujo(S)
    fig, ax = plt.subplots(figsize=(7.4, ALTO_FIG))
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis("off")

    def alto(texto, tam=8.0, pad=0.024):
        return (texto.count("\n") + 1) * (tam / 72.0) * 1.5 / ALTO_FIG + pad

    X_IZQ, ANCHO_IZQ = 0.075, 0.435
    X_DER, ANCHO_DER = 0.585, 0.390
    CENTRO = X_IZQ + ANCHO_IZQ / 2
    HUECO = 0.034

    def flujo(y_arriba, texto, tam=8.0):
        """Caja de la columna principal; devuelve su borde inferior."""
        h = alto(texto, tam)
        caja(ax, X_IZQ, y_arriba - h, ANCHO_IZQ, h, texto, "white", tam)
        return y_arriba - h

    # Las cajas de motivos son mas altas que el hueco entre las cajas del
    # flujo, asi que centrarlas sin mas las hace solaparse y el texto de una
    # queda tapado por la siguiente. Se lleva la cota inferior de la ultima y
    # se empuja hacia abajo lo justo cuando haria falta.
    ultimo = [1.0]

    def excluidos(y_centro, texto, tam=7.5, x_origen=None):
        """x_origen: de donde sale el codo; por defecto, el borde derecho de la
        caja del flujo. Con CENTRO sale de la flecha entre dos cajas."""
        h = alto(texto, tam)
        techo = min(y_centro + h / 2, ultimo[0] - 0.010)
        caja(ax, X_DER, techo - h, ANCHO_DER, h, texto, SUAVE, tam)
        ultimo[0] = techo - h
        # Codo dibujado a mano: tramo horizontal, tramo vertical y flecha recta
        # de entrada. Los conectores "angle" de matplotlib no valen cuando los
        # dos extremos son horizontales, porque no hay rectas que cortar.
        y_entrada = techo - h / 2
        medio = (X_IZQ + ANCHO_IZQ + X_DER) / 2
        ax.plot([X_IZQ + ANCHO_IZQ if x_origen is None else x_origen, medio],
                [y_centro, y_centro], color=BORDE, linewidth=0.8, zorder=1)
        if abs(y_entrada - y_centro) > 0.003:
            ax.plot([medio, medio], [y_centro, y_entrada],
                    color=BORDE, linewidth=0.8, zorder=1)
        flecha(ax, (medio, y_entrada), (X_DER, y_entrada))

    def motivos(mot):
        """Dos codigos por linea: seis en columna estiran la caja de mas."""
        it = list(mot.items())
        return "\n".join(
            "        ".join("%s %s" % (k, mil(v)) for k, v in it[i:i + 2])
            for i in range(0, len(it), 2))

    y0 = 0.982

    # --- Identificacion -----------------------------------------------------
    # CORREGIDO EL 2026-10-19 (consejo del 15-oct). La caja de bases ponia
    # registros_identificados (23 057), que es el total de las OCHO fuentes,
    # registros de ensayos incluidos, y «6 fuentes», que cuenta los dos brazos
    # de Scopus; la de registros sumaba aparte sus 134. La figura daba a
    # entender 23 191 registros y 9 fuentes, y el texto dice «Las ocho fuentes
    # aportaron 23 057». Ahora cada caja lleva lo de su corriente
    # (identificacion_por_corriente) y las dos suman lo que dice el texto.
    I = identificacion_por_corriente(S)
    t_bases = ("Registros identificados en bases\nbibliográficas (%s)\n"
               "n = %s registros"
               % (I["fuentes_bases_rotulo"], mil(I["registros_bases"])))
    h = alto(t_bases)
    caja(ax, X_IZQ, y0 - h, ANCHO_IZQ, h, t_bases)
    caja(ax, X_DER, y0 - h, ANCHO_DER, h,
         "Registros identificados en registros\nde ensayos (%d fuentes)\n"
         "n = %s registros"
         % (S["fuentes_registros_n"], mil(I["registros_registros"])))
    y_id = y0 - h

    y = flujo(y_id - HUECO, "Duplicados eliminados\nn = %s"
              % mil(S["duplicados_eliminados"]))
    flecha(ax, (CENTRO, y_id), (CENTRO, y_id - HUECO))

    # --- Cribado ------------------------------------------------------------
    y_cribado_top = y - HUECO
    t_u = "Informes únicos tras deduplicar\nn = %s" % mil(S["informes_unicos"])
    h_u = alto(t_u)
    caja(ax, X_IZQ, y_cribado_top - h_u, ANCHO_IZQ, h_u, t_u)
    flecha(ax, (CENTRO, y), (CENTRO, y_cribado_top))
    # La corriente de registros entra por el lateral: no atraviesa la
    # deduplicacion bibliografica, porque una ficha de registro no tiene DOI
    # con el que colisionar contra un articulo.
    y_med = y_cribado_top - h_u / 2
    flecha(ax, (X_DER + ANCHO_DER / 2, y_id), (X_IZQ + ANCHO_IZQ, y_med),
           "angle,angleA=-90,angleB=180,rad=4")
    y = y_cribado_top - h_u

    # CORREGIDO EL 2026-10-20 (verificacion de exactitud). Cada caja de
    # excluidos colgaba de la caja SIGUIENTE a la que se cribo: la figura
    # decia que de 460 resumenes se excluyeron 13 434. Ahora cada una sale de
    # la caja cribada; la de etapa 1, de la flecha que lleva al cribado de
    # titulos, porque el borde derecho de «Informes unicos» lo ocupa el
    # conector de la corriente de registros.
    excluidos(y - HUECO / 2,
              "Excluidos por reglas explícitas de\netapa 1\nn = %s"
              % mil(S["excluidos_etapa1"]), x_origen=CENTRO)
    t_t = "Títulos cribados\nn = %s" % mil(S["cribados_por_titulo"])
    h_t = alto(t_t)
    caja(ax, X_IZQ, y - HUECO - h_t, ANCHO_IZQ, h_t, t_t)
    flecha(ax, (CENTRO, y), (CENTRO, y - HUECO))
    excluidos(y - HUECO - h_t / 2,
              "Excluidos por título — n = %s\n\n%s"
              % (mil(S["excluidos_titulo"]), motivos(S["exclusiones_titulo"])))
    y = y - HUECO - h_t

    t_r = "Resúmenes evaluados\nn = %d" % S["a_resumen"]
    h_r = alto(t_r)
    caja(ax, X_IZQ, y - HUECO - h_r, ANCHO_IZQ, h_r, t_r)
    flecha(ax, (CENTRO, y), (CENTRO, y - HUECO))
    excluidos(y - HUECO - h_r / 2,
              "Excluidos por resumen — n = %d\n\n%s"
              % (S["excluidos_resumen"], motivos(S["exclusiones_resumen"])))
    y = y - HUECO - h_r

    t_f = ("Informes evaluados a texto completo\nn = %d"
           % S["informes_a_texto_completo"])
    h_f = alto(t_f)
    caja(ax, X_IZQ, y - HUECO - h_f, ANCHO_IZQ, h_f, t_f)
    flecha(ax, (CENTRO, y), (CENTRO, y - HUECO))
    y = y - HUECO - h_f

    # Los informes se agrupan en estudios y AHI se evalua la elegibilidad. Este
    # paso existe porque 22 estudios que el cribado habia admitido no cumplian
    # §2.2. Veintidos se descubrieron leyendo los articulos uno por uno
    # durante la extraccion; cuatro mas, comprobando el idioma del cuerpo
    # en la pagina del editor. Sin esta casilla, del diagrama entraban 233 informes y salian
    # 201 sin que nada explicara los 32 que faltan.
    t_el = ("Estudios evaluados para elegibilidad\nn = %d  (agrupando %d informes)"
            % (S["estudios_antes_de_releer"], S["informes_a_texto_completo"]))
    h_el = alto(t_el)
    caja(ax, X_IZQ, y - HUECO - h_el, ANCHO_IZQ, h_el, t_el)
    flecha(ax, (CENTRO, y), (CENTRO, y - HUECO))
    # Decia «Excluidos al releer el texto completo», y en esta caja estan los
    # NOPDF, sin articulo, y los NOREC, sin texto legible: a esos no los
    # releyo nadie. El rotulo dice la fase, no que se leyeran.
    excluidos(y - HUECO - h_el / 2,
              "Excluidos en la fase de texto completo\n"
              "n = %d estudios (%d informes)\n\n%s"
              % (S["estudios_excluidos_tras_texto_completo"],
                 S["informes_excluidos_tras_texto_completo"],
                 motivos(S["exclusiones_tras_texto_completo"])))
    y = y - HUECO - h_el
    y_cribado_fin = y

    # --- Inclusion ----------------------------------------------------------
    # Desde el 2026-10-06 solo se admiten estudios con el PDF del articulo
    # completo (NOREC ampliado como NOPDF): no queda ninguna ficha de registro
    # y la recuperacion es del 100 % por construccion. La bifurcacion «con
    # publicacion / solo ficha» y la caja del texto obtenido dibujaban un 0 y
    # un 100 % que no informan de nada; se dibujan solo si vuelven a hacerlo.
    solo_texto = (S["estudios_solo_registro"] == 0 and S["texto_completo_no_obtenido"] == 0)
    if solo_texto:
        t_e = ("Estudios incluidos, todos con el\ntexto completo leído\n"
               "n = %d  (agrupando %d informes)" % (S["estudios"], S["informes_agrupados"]))
    else:
        t_e = ("Estudios incluidos\nn = %d  (agrupando %d informes)"
               % (S["estudios"], S["informes_agrupados"]))
    h_e = alto(t_e)
    caja(ax, X_IZQ, y - HUECO - h_e, ANCHO_IZQ, h_e, t_e)
    flecha(ax, (CENTRO, y), (CENTRO, y - HUECO))
    y = y - HUECO - h_e

    if solo_texto:
        y_fin = min(y, ultimo[0])
    else:
        t_a = "Con publicación\nrecuperable\nn = %d" % S["estudios_extraibles"]
        h_a = alto(t_a)
        w = (ANCHO_IZQ - 0.020) / 2
        caja(ax, X_IZQ, y - HUECO - h_a, w, h_a, t_a)
        caja(ax, X_IZQ + w + 0.020, y - HUECO - h_a, w, h_a,
             "Solo ficha de registro\nde ensayo\nn = %d"
             % S["estudios_solo_registro"])
        # Bifurcacion en T: una linea baja, una travesana, y dos flechas que
        # entran verticales.
        y_t = y - HUECO / 2
        c_izq, c_der = X_IZQ + w / 2, X_IZQ + w * 1.5 + 0.020
        ax.plot([CENTRO, CENTRO], [y, y_t], color=BORDE, linewidth=0.8, zorder=1)
        ax.plot([c_izq, c_der], [y_t, y_t], color=BORDE, linewidth=0.8, zorder=1)
        flecha(ax, (c_izq, y_t), (c_izq, y - HUECO))
        flecha(ax, (c_der, y_t), (c_der, y - HUECO))
        h_d = alto("x\nx", 8.0)
        caja(ax, X_DER, y - HUECO - h_a + (h_a - h_d) / 2, ANCHO_DER, h_d,
             "Texto completo obtenido\nn = %d de %d (%.1f %%)"
             % (S["texto_completo_obtenido"], S["estudios_extraibles"],
                S["texto_completo_pct"]), SUAVE)
        y_fin = min(y - HUECO - h_a, ultimo[0])

    # --- bandas de fase -----------------------------------------------------
    for a, b, etiqueta in ((y_cribado_top + 0.006, 0.982, "Identificación"),
                           (y_cribado_fin, y_cribado_top, "Cribado"),
                           (y_fin - 0.006, y_cribado_fin - 0.006, "Inclusión")):
        ax.add_patch(FancyBboxPatch(
            (0.008, a), 0.046, b - a,
            boxstyle="round,pad=0.002,rounding_size=0.007",
            linewidth=0.7, edgecolor=BORDE, facecolor=SUAVE, zorder=0))
        ax.text(0.031, (a + b) / 2, etiqueta, ha="center", va="center",
                rotation=90, fontsize=8.5, color=TINTA)

    # Recorte del lienzo sobrante. Se encoge el rango de datos Y **y** la altura
    # de la figura en la misma proporcion: asi las pulgadas por unidad de dato
    # no cambian y las cajas conservan la altura calculada para su texto.
    inf, sup = y_fin - 0.012, 0.992
    ax.set_ylim(inf, sup)
    fig.set_figheight(ALTO_FIG * (sup - inf))
    fig.subplots_adjust(left=0, right=1, top=1, bottom=0)
    for ext in ("pdf", "png"):
        fig.savefig(OUT / ("figura_1_prisma." + ext), dpi=400,
                    bbox_inches="tight", pad_inches=0.04)
    plt.close(fig)


def figura_composicion(S):
    pre = {}
    with open(RS / "extraccion" / "pre_extraccion_desde_resumen.csv",
              encoding="utf-8", newline="") as fh:
        for r in csv.DictReader(fh):
            pre[r["id_provisional"]] = r

    ES = {"case report": "Reporte de caso único",
          "case series": "Serie de casos",
          "prospective cohort": "Cohorte prospectiva",
          "retrospective cohort": "Cohorte retrospectiva",
          "RCT": "Ensayo aleatorizado",
          "non-randomised trial": "Ensayo no aleatorizado",
          "no declarado": "No declarado"}
    COMP = {"RCT", "non-randomised trial"}

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(7.4, 3.4))

    orden = sorted(S["disenos"].items(), key=lambda kv: kv[1])
    valores = [v for _, v in orden]
    barras = ax1.barh([ES.get(k, k) for k, _ in orden], valores,
                      color=[ACENTO if k in COMP else NEUTRO for k, _ in orden],
                      height=0.66)
    for b, v in zip(barras, valores):
        ax1.text(v + 0.9, b.get_y() + b.get_height() / 2,
                 "%d (%.1f %%)" % (v, 100.0 * v / S["estudios_extraibles"]),
                 va="center", fontsize=7.2, color=TINTA)
    ax1.set_xlim(0, max(valores) * 1.42)
    ax1.set_xlabel("Estudios", fontsize=8)
    ax1.text(0.0, 1.05, "Panel A: diseño", transform=ax1.transAxes,
             fontsize=8.5, fontweight="bold")
    ax1.spines[["top", "right"]].set_visible(False)
    ax1.tick_params(labelsize=7.4)

    anios, comp_anio = collections.Counter(), collections.Counter()
    for p in pre.values():
        a = p.get("publication_year") or ""
        if a.isdigit():
            anios[int(a)] += 1
            if p.get("study_design") in COMP:
                comp_anio[int(a)] += 1
    xs = sorted(anios)
    ax2.bar(xs, [anios[a] for a in xs], color=NEUTRO, width=0.72,
            label="No comparativos")
    ax2.bar(xs, [comp_anio[a] for a in xs], color=ACENTO, width=0.72,
            label="Comparativos")
    ax2.set_xticks(xs)
    ax2.set_xticklabels([str(a) for a in xs], rotation=45, fontsize=7.2)
    ax2.set_ylabel("Estudios", fontsize=8)
    ax2.text(0.0, 1.05, "Panel B: año de publicación", transform=ax2.transAxes,
             fontsize=8.5, fontweight="bold")
    ax2.spines[["top", "right"]].set_visible(False)
    ax2.legend(frameon=False, fontsize=7.2, loc="upper left")
    ax2.tick_params(labelsize=7.4)

    fig.tight_layout(pad=0.7)
    for ext in ("pdf", "png"):
        fig.savefig(OUT / ("figura_2_composicion." + ext), dpi=400,
                    bbox_inches="tight")
    plt.close(fig)


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    S = json.loads((ROOT / "quality_reports" / "synthesis_scalars.json")
                   .read_text(encoding="utf-8"))
    figura_prisma(S)
    print("  figura_1_prisma.pdf / .png")
    figura_composicion(S)
    print("  figura_2_composicion.pdf / .png")
    print("escritas en %s" % OUT)
    return 0


if __name__ == "__main__":
    sys.exit(main())
