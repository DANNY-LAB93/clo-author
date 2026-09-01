"""Genera las cuatro tablas del manuscrito desde el canal, no a mano.

Cada tabla sale en Markdown (para el manuscrito de trabajo) y en CSV (para el
paquete de verificables y para importarla a Word sin retecleo). Las notas al pie
van en el fichero, no dentro de la tabla, conforme al estandar del proyecto.

SALIDA
    paper/tablas/tabla_N_*.md   y   .csv
"""
import collections
import csv
import json
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
RS = ROOT / "revision_sistematica"
OUT = ROOT / "paper" / "tablas"
csv.field_size_limit(200_000_000)
try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

ES_DISENO = {
    "case report": "Reporte de caso único",
    "case series": "Serie de casos",
    "prospective cohort": "Cohorte prospectiva",
    "retrospective cohort": "Cohorte retrospectiva",
    "RCT": "Ensayo aleatorizado",
    "non-randomised trial": "Ensayo no aleatorizado",
    "no declarado": "No declarado en el resumen",
}
COMPARATIVOS = {"RCT", "non-randomised trial"}
# Los codigos se leen del vocabulario, no se copian: una copia se queda
# desfasada en cuanto se anade un codigo, y la tabla del manuscrito dejaria
# de sumar sin que nada avise.
import sys as _sys, pathlib as _pl
_sys.path.insert(0, str(_pl.Path(__file__).resolve().parent))
from exclusion_codes import CODES as _CODES
CODIGOS = dict(_CODES)
CODIGOS['ORG'] = 'Organismo distinto de *P. aeruginosa*, sin subgrupo separable'
CODIGOS['IDI'] = 'Informe no redactado en inglés ni en español (enmienda)'


def leer(p):
    with open(p, encoding="utf-8", newline="") as fh:
        return list(csv.DictReader(fh))


def escribe(nombre, cabecera, filas, titulo, nota):
    OUT.mkdir(parents=True, exist_ok=True)
    md = ["**%s**" % titulo, "",
          "| " + " | ".join(cabecera) + " |",
          "|" + "|".join("---" for _ in cabecera) + "|"]
    for f in filas:
        md.append("| " + " | ".join(str(x) for x in f) + " |")
    md += ["", "*Nota.* " + nota]
    (OUT / (nombre + ".md")).write_text("\n".join(md) + "\n",
                                        encoding="utf-8", newline="\n")
    with open(OUT / (nombre + ".csv"), "w", encoding="utf-8-sig",
              newline="") as fh:
        w = csv.writer(fh)
        w.writerow(cabecera)
        w.writerows(filas)
    print("  %-34s %d filas" % (nombre, len(filas)))


def main():
    S = json.loads((ROOT / "quality_reports" / "synthesis_scalars.json")
                   .read_text(encoding="utf-8"))
    grupos = leer(RS / "cribado" / "study_groups.csv")
    pre = {p["id_provisional"]: p for p in
           leer(RS / "extraccion" / "pre_extraccion_desde_resumen.csv")}
# El texto completo no siempre llega en PDF: el manuscrito de autor de
# PhagoBurn esta depositado en ORBi como .docx. Contar solo *.pdf lo
# dejaba fuera del recuento aunque estuviera en disco y fuera legible.
    # El texto completo puede llegar como PDF, como manuscrito de autor en
    # .docx o como el texto integro de la pagina del editor cuando este
    # sirve el articulo en HTML y bloquea la descarga automatica del PDF.
    # Las tres formas son el mismo dato para quien va a extraer.
    pdfs = {q.stem for q in (RS / "textos_completos" / "pdf").iterdir()
            if q.suffix.lower() in (".pdf", ".docx")}
    web = RS / "textos_completos" / "texto_html"
    if web.exists():
        pdfs |= {q.stem for q in web.glob("*.txt")}
    reps = {"EST-%03d" % int(g["estudio"]): g for g in grupos
            if g["informe_para_extraer"] == "SI"}
    extr = {k for k, g in reps.items()
            if g["situacion"] in ("extraible", "solo-resumen")}
    n = len(extr)
    pc = lambda x: "%.1f" % (100.0 * x / n)

    print("tablas del manuscrito:")

    # ---- Tabla 1: caracteristicas -----------------------------------------
    filas = [["Periodo de publicación", "%d–%d" % (S["anio_min"], S["anio_max"]), "—"],
             ["Publicados desde 2020", S["publicados_desde_2020"],
              S["publicados_desde_2020_pct"]],
             ["", "", ""],
             ["**Diseño**", "", ""]]
    for k, v in S["disenos"].items():
        filas.append([ES_DISENO.get(k, k), v, pc(v)])
    filas += [["", "", ""],
              ["**Diseños comparativos (total)**", S["estudios_comparativos"],
               S["estudios_comparativos_pct"]],
              ["", "", ""],
              ["**Procedencia declarada**", "", ""]]
    # Se listan TODOS los paises declarados, no los ocho primeros. Cortar por
    # los ocho dejaba fuera a India e Israel, empatados a 2 con Ucrania, que si
    # aparecia: el desempate lo decidia el orden del diccionario y no un
    # criterio, y la tabla no avisaba de que faltaba nada.
    # Los paises con dos o mas estudios, uno por fila; los que aparecen una
    # sola vez se agrupan y se DICE cuantos son. Listar veinte filas de las que
    # once valen 1 no informa, y callarse esas once seria truncar otra vez.
    decl = sorted(((k, v) for k, v in S["procedencia"].items()
                   if k != "no declarada"), key=lambda x: (-x[1], x[0]))
    for k, v in [x for x in decl if x[1] >= 2]:
        filas.append([k, v, pc(v)])
    sueltos = [x for x in decl if x[1] < 2]
    if sueltos:
        filas.append(["Otros %d países, un estudio cada uno" % len(sueltos),
                      len(sueltos), pc(len(sueltos))])
    filas.append(["No declarada en el resumen", S["procedencia_no_declarada"],
                  S["procedencia_no_declarada_pct"]])
    escribe("tabla_1_caracteristicas", ["Característica", "n", "%"], filas,
            "Tabla 1. Características del cuerpo de evidencia recuperable "
            "(n = %d estudios)." % n,
            "Porcentajes sobre los %d estudios con publicación recuperable. El "
            "diseño procede de la pre-extracción sistemática desde el resumen; "
            "«No declarado» significa que el resumen no permite reconocer el "
            "diseño, no que el estudio carezca de él. Fuente: canal de cribado "
            "del proyecto, ejecución del 10 de agosto de 2026." % n)

    # ---- Tabla 2: completitud del reporte ---------------------------------
    filas = []
    for campo, etiqueta in (
            ("sin_clase_de_resistencia", "Clase de resistencia (MDR/XDR/PDR)"),
            ("sin_ambito_de_patogeno", "Ámbito de patógeno (solo *P. aeruginosa* o mixto)"),
            ("sin_via_de_administracion", "Vía de administración del fago"),
            ("sin_modalidad", "Modalidad (monoterapia o combinada)"),
            ("sin_criterio_dtr", "Criterio DTR (*difficult-to-treat resistance*)")):
        filas.append([etiqueta, n - S[campo], "%.1f" % (100 - S[campo + "_pct"]),
                      S[campo], S[campo + "_pct"]])
    escribe("tabla_2_completitud", ["Variable", "Declara (n)", "Declara (%)",
                                    "No declara (n)", "No declara (%)"], filas,
            "Tabla 2. Completitud del reporte en las variables críticas para la "
            "estratificación (n = %d estudios)." % n,
            "Medido sobre el resumen indexado, que es lo que alimenta las bases "
            "bibliográficas y las revisiones automatizadas. Una variable puede "
            "constar en el texto completo y no en el resumen; la extracción por "
            "duplicado, ya adjudicada, mide esa distinción para los desenlaces "
            "en la Tabla 5. Esta tabla se "
            "reproduce desde el anexo S4 filtrando en_corpus_actual = sí: el "
            "anexo conserva además las filas que la enmienda de idioma dejó "
            "fuera, para que la enmienda pueda auditarse.")

    # ---- Tabla 3: sesgo de recuperacion ------------------------------------
    con, sin_ = extr & pdfs, extr - pdfs

    def perfil(conj):
        d = collections.Counter((pre.get(k, {}).get("study_design")
                                 or "no declarado") for k in conj)
        comp = sum(v for k, v in d.items() if k in COMPARATIVOS)
        pac = 0
        for k in conj:
            try:
                pac += int(pre.get(k, {}).get("n_arm") or 0)
            except ValueError:
                pass
        return d, comp, pac

    dc, cc, pcn = perfil(con)
    ds, cs, psn = perfil(sin_)
    filas = [["Estudios", len(con), len(sin_)],
             ["Diseños comparativos", cc, cs],
             ["Comparativos (% de la columna)",
              "%.1f" % (100.0 * cc / len(con)), "%.1f" % (100.0 * cs / len(sin_))],
             ["Reportes de caso único", dc["case report"], ds["case report"]],
             ["Ensayos aleatorizados", dc["RCT"], ds["RCT"]],
             # Millar fino, como el resto del manuscrito: escribia «1044»
             # en una tabla donde arriba pone «17 129».
             ["Pacientes declarados (suma de n por brazo)",
              f"{pcn:,}".replace(",", " "),
              f"{psn:,}".replace(",", " ")]]
    escribe("tabla_3_sesgo_recuperacion",
            ["", "Con texto completo", "Sin texto completo"], filas,
            "Tabla 3. Comparación entre los estudios con y sin texto completo "
            "obtenido.",
            # La nota se DERIVA de la tabla. Antes afirmaba que la fracción no
            # obtenida declaraba más pacientes que la obtenida: cuando el
            # corpus crecio la direccion se invirtio y la nota siguio diciendo
            # lo mismo, contradiciendo a la tabla que encabeza. Una nota que
            # asegura una direccion sin mirarla es una cifra tecleada a mano
            # disfrazada de prosa.
            "La fracción no obtenida no es una muestra aleatoria: concentra el "
            "%.1f %% de los estudios comparativos (%.1f %% de esa fracción, "
            "frente al %.1f %% de la obtenida) y declara %s pacientes que la "
            "obtenida (%s frente a %s). Cualquier síntesis limitada a lo "
            "descargable heredaría esa asimetría."
            % (S["comparativos_sin_texto_pct"],
               100.0 * cs / max(1, len(sin_)),
               100.0 * cc / max(1, len(con)),
               "más" if f"{psn:,}".replace(",", " ") > f"{pcn:,}".replace(",", " ") else "menos", f"{psn:,}".replace(",", " "), f"{pcn:,}".replace(",", " ")))

    # ---- Tabla 4: motivos de exclusion -------------------------------------
    filas = []
    for cod, desc in CODIGOS.items():
        t = S["exclusiones_titulo"].get(cod, 0)
        r = S["exclusiones_resumen"].get(cod, 0)
        filas.append([cod, desc, t, r, t + r])
    filas.append(["", "**Total**", S["excluidos_titulo"], S["excluidos_resumen"],
                  S["excluidos_titulo"] + S["excluidos_resumen"]])
    escribe("tabla_4_exclusiones", ["Código", "Motivo", "Por título",
                                    "Por resumen", "Total"], filas,
            "Tabla 4. Motivos de exclusión por etapa, con el vocabulario cerrado.",
            "Los seis primeros códigos se fijaron antes de iniciar el cribado. Un "
            "motivo que no encaje en ellos no recibe otro improvisado sobre la "
            "marcha: el registro avanza a la etapa siguiente para lectura "
            "humana. IDI es una ENMIENDA posterior al protocolo, incorporada el "
            "11 de agosto de 2026 y aplicada solo en la etapa de resumen; su "
            "adopción y su impacto se declaran en Métodos y en Limitaciones. El "
            "registro de decisiones es solo-anexar y conserva el texto literal "
            "escrito al decidir, del que se deriva el código.")

    # ---- Tabla 5: que reporta el corpus en cada desenlace -------------------
    # Primera tabla del manuscrito que sale de los cuadernos de extraccion y no
    # del cribado. Puede hacerse porque la adjudicacion esta firmada; hasta el
    # 26 de agosto no habia un valor unico por casilla que citar.
    oc = ROOT / "quality_reports" / "outcome_scalars.json"
    if oc.exists():
        O = json.loads(oc.read_text(encoding="utf-8"))
        filas = []
        for campo, d in O["desenlaces"].items():
            filas.append([
                d["nombre"].capitalize(),
                d["con_numerador_y_denominador"],
                "%.1f" % d["pct_de_los_brazos"],
                "%.1f" % d["pct_de_los_legibles"],
                "%.1f" % d["doble_lectura_pct"],
            ])
        nota = (
            "La tabla mide COMPLETITUD DE REPORTE, no eficacia: un numerador sin "
            "denominador no es una proporción. Se dan DOS denominadores porque "
            "miden cosas distintas: sobre los %d brazos extraídos, y sobre los %d "
            "cuyo estudio tiene texto completo recuperado. La diferencia entre "
            "ambos no es silencio de la literatura sino hueco documental nuestro: "
            "de un artículo que no se ha podido leer no se puede afirmar que "
            "calle. «Con doble lectura» es el porcentaje de esas casillas en que "
            "los dos revisores coincidieron o resolvieron por consenso; el resto "
            "lo leyó un solo revisor, y en la fila de emergencia de resistencia "
            "esas casillas las rellenó siempre el mismo. "
            % (O["brazos"], O["brazos_legibles"]))
        if O.get("campos_del_esquema_no_extraidos"):
            nota += (
                "La fila de erradicación usa el tamaño del brazo como denominador: "
                "el esquema declara además %s, que se añadieron después de "
                "repartir los formularios y nunca llegaron a extraerse, de modo "
                "que no consta a cuántos pacientes se les hizo cultivo de control. "
                "El denominador real es por tanto menor o igual que el usado. "
                % " y ".join("`%s`" % c for c in O["campos_del_esquema_no_extraidos"]))
        nota += (
            "El diseño solo puede clasificarse en %d de los %d brazos (%d con un "
            "«NA» que los dos revisores acordaron y %d con la casilla aún "
            "abierta), de modo que los recuentos por diseño son suelos: de esos "
            "%d, %d son comparativos, y solo %d reúnen a la vez diseño "
            "comparativo, numerador, denominador y una definición operativa del "
            "éxito clínico. Dos brazos reportan un numerador mayor que su "
            "denominador y se señalan como error de reporte. «Comparativo» "
            "describe lo que el estudio es, no lo que hay en este fichero: la "
            "extracción se hizo por brazo y se extrajo el de fago, de modo que "
            "el conjunto no contiene los brazos de control."
            % (O["brazos_con_diseno"], O["brazos"], O["diseno_na_acordado"],
               O["diseno_abierto"], O["brazos_con_diseno"],
               O["brazos_comparativos"], O["brazos_agregables_exito_clinico"]))
        escribe("tabla_5_desenlaces",
                ["Desenlace", "Con numerador y denominador",
                 "%% de los %d brazos" % O["brazos"],
                 "%% de los %d con texto completo" % O["brazos_legibles"],
                 "% con doble lectura"], filas,
                "Tabla 5. Completitud de reporte de los cinco desenlaces "
                "declarados, sobre los %d brazos de la extracción adjudicada."
                % O["brazos"], nota)

    print("escritas en %s" % OUT)
    return 0


if __name__ == "__main__":
    sys.exit(main())
