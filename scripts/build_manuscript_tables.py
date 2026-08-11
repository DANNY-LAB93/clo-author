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
    pdfs = {q.stem for q in (RS / "textos_completos" / "pdf").iterdir()
            if q.suffix.lower() in (".pdf", ".docx")}
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
    for k, v in list(S["procedencia"].items())[:8]:
        if k != "no declarada":
            filas.append([k, v, pc(v)])
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
            "constar en el texto completo y no en el resumen; esa distinción se "
            "resolverá con la extracción por duplicado en curso.")

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
             ["Pacientes declarados (suma de n por brazo)", pcn, psn]]
    escribe("tabla_3_sesgo_recuperacion",
            ["", "Con texto completo", "Sin texto completo"], filas,
            "Tabla 3. Comparación entre los estudios con y sin texto completo "
            "obtenido.",
            "La fracción no obtenida no es una muestra aleatoria: concentra el "
            "%.1f %% de los estudios comparativos y más pacientes declarados que "
            "la obtenida. Cualquier síntesis limitada a lo descargable heredaría "
            "esa asimetría." % S["comparativos_sin_texto_pct"])

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

    print("escritas en %s" % OUT)
    return 0


if __name__ == "__main__":
    sys.exit(main())
