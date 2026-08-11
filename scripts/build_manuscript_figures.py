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


def figura_prisma(S):
    """Flujo PRISMA 2020 con las dos corrientes de identificacion separadas.

    La altura de cada caja se DERIVA del numero de lineas de su texto. Fijarla a
    mano funciona hasta que un rotulo gana una linea, y entonces el texto
    desborda por arriba y por abajo sin que nada avise: fue lo que paso en el
    primer intento con las dos cajas de motivos de exclusion.
    """
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

    def excluidos(y_centro, texto, tam=7.5):
        h = alto(texto, tam)
        techo = min(y_centro + h / 2, ultimo[0] - 0.010)
        caja(ax, X_DER, techo - h, ANCHO_DER, h, texto, SUAVE, tam)
        ultimo[0] = techo - h
        # Codo dibujado a mano: tramo horizontal, tramo vertical y flecha recta
        # de entrada. Los conectores "angle" de matplotlib no valen cuando los
        # dos extremos son horizontales, porque no hay rectas que cortar.
        y_entrada = techo - h / 2
        medio = (X_IZQ + ANCHO_IZQ + X_DER) / 2
        ax.plot([X_IZQ + ANCHO_IZQ, medio], [y_centro, y_centro],
                color=BORDE, linewidth=0.8, zorder=1)
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
    t_bases = ("Registros identificados en bases\nbibliográficas (%d fuentes)\n"
               "n = %s registros"
               % (S["fuentes_bases_n"], mil(S["registros_identificados"])))
    h = alto(t_bases)
    caja(ax, X_IZQ, y0 - h, ANCHO_IZQ, h, t_bases)
    caja(ax, X_DER, y0 - h, ANCHO_DER, h,
         "Registros identificados en registros\nde ensayos (%d fuentes)\n"
         "n = %d informes"
         % (S["fuentes_registros_n"], S["informes_de_registros"]))
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

    t_t = "Títulos cribados\nn = %s" % mil(S["cribados_por_titulo"])
    h_t = alto(t_t)
    caja(ax, X_IZQ, y - HUECO - h_t, ANCHO_IZQ, h_t, t_t)
    flecha(ax, (CENTRO, y), (CENTRO, y - HUECO))
    excluidos(y - HUECO - h_t / 2,
              "Excluidos por reglas explícitas de\netapa 1\nn = %s"
              % mil(S["excluidos_etapa1"]))
    y = y - HUECO - h_t

    t_r = "Resúmenes evaluados\nn = %d" % S["a_resumen"]
    h_r = alto(t_r)
    caja(ax, X_IZQ, y - HUECO - h_r, ANCHO_IZQ, h_r, t_r)
    flecha(ax, (CENTRO, y), (CENTRO, y - HUECO))
    excluidos(y - HUECO - h_r / 2,
              "Excluidos por título — n = %s\n\n%s"
              % (mil(S["excluidos_titulo"]), motivos(S["exclusiones_titulo"])))
    y = y - HUECO - h_r

    t_f = ("Informes evaluados a texto completo\nn = %d"
           % S["informes_a_texto_completo"])
    h_f = alto(t_f)
    caja(ax, X_IZQ, y - HUECO - h_f, ANCHO_IZQ, h_f, t_f)
    flecha(ax, (CENTRO, y), (CENTRO, y - HUECO))
    excluidos(y - HUECO - h_f / 2,
              "Excluidos por resumen — n = %d\n\n%s"
              % (S["excluidos_resumen"], motivos(S["exclusiones_resumen"])))
    y = y - HUECO - h_f
    y_cribado_fin = y

    # --- Inclusion ----------------------------------------------------------
    t_e = ("Estudios incluidos\nn = %d  (agrupando %d informes)"
           % (S["estudios"], S["informes_agrupados"]))
    h_e = alto(t_e)
    caja(ax, X_IZQ, y - HUECO - h_e, ANCHO_IZQ, h_e, t_e)
    flecha(ax, (CENTRO, y), (CENTRO, y - HUECO))
    y = y - HUECO - h_e

    t_a = "Con publicación\nrecuperable\nn = %d" % S["estudios_extraibles"]
    h_a = alto(t_a)
    w = (ANCHO_IZQ - 0.020) / 2
    caja(ax, X_IZQ, y - HUECO - h_a, w, h_a, t_a)
    caja(ax, X_IZQ + w + 0.020, y - HUECO - h_a, w, h_a,
         "Solo ficha de registro\nde ensayo\nn = %d"
         % S["estudios_solo_registro"])
    # Bifurcacion en T: una linea baja, una travesana, y dos flechas que
    # entran verticales. Un conector "angle" no sirve aqui porque sus dos
    # extremos son verticales y matplotlib no puede cortar rectas paralelas.
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
