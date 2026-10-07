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
    # Los estudios excluidos al examinar el articulo no forman parte del
    # corpus, y las tablas tienen que contarlos fuera igual que los
    # escalares. Sin este filtro, las columnas de recuento sumaban 124 --el
    # corpus anterior-- mientras los porcentajes, que vienen de los
    # escalares, ya eran sobre 95: la tabla se contradecia a si misma.
    p_ex = RS / "cribado" / "exclusiones_tras_texto_completo.csv"
    fuera = set()
    if p_ex.exists():
        with open(p_ex, encoding="utf-8", newline="") as fh:
            fuera = {r["study_id"] for r in csv.DictReader(fh)}
    reps = {"EST-%03d" % int(g["estudio"]): g for g in grupos
            if g["informe_para_extraer"] == "SI"
            and "EST-%03d" % int(g["estudio"]) not in fuera}
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
    # CUATRO SITUACIONES, NO DOS. Hasta el 2026-09-16 esta tabla medía solo el
    # resumen y de ahí se concluía que la variable «no puede asignarse» en el
    # estudio. No es lo mismo: de los 71 artículos leídos, ninguno calla sobre
    # la clase de resistencia. La ausencia está en el resumen. Las cuatro
    # columnas del texto completo se excluyen entre sí y suman el corpus.
    filas = []
    # Desde el 2026-10-06 todo el corpus tiene texto completo (seccion 2.9): la
    # columna «Texto completo no recuperado» seria una columna de ceros.
    todo_texto = S.get("texto_completo_no_obtenido", 0) == 0
    for campo, resumen, etiqueta in (
            ("resistance_class", "sin_clase_de_resistencia", "Clase de resistencia (MDR/XDR/PDR)"),
            ("pathogen_scope", "sin_ambito_de_patogeno", "Ámbito de patógeno (solo *P. aeruginosa* o mixto)"),
            ("route", "sin_via_de_administracion", "Vía de administración del fago"),
            ("modality", "sin_modalidad", "Modalidad (monoterapia o combinada)"),
            ("dtr_status", "sin_criterio_dtr", "Criterio DTR (*difficult-to-treat resistance*)")):
        filas.append([etiqueta,
                      "%d (%s %%)" % (S[resumen], S[resumen + "_pct"]),
                      S["t3_%s_declarado" % campo],
                      S["t3_%s_no_clasificable" % campo],
                      S["t3_%s_silencio" % campo]]
                     + ([] if todo_texto else [S["t3_%s_sin_texto" % campo]]))
    if todo_texto:
        escribe("tabla_2_completitud",
                ["Variable", "No asignable en el resumen",
                 "Declarado en el texto completo", "Declarado pero no clasificable",
                 "No declarado en el texto completo"],
                filas,
                "Tabla 3. Completitud del reporte en las variables de "
                "estratificación, en el resumen y en el texto completo "
                "(n = %d estudios, todos con texto completo)." % n,
                "La segunda columna mide el RESUMEN indexado, que es lo que "
                "alimenta las bases bibliográficas y las revisiones automatizadas. "
                "Las tres siguientes miden el TEXTO COMPLETO, se excluyen entre sí "
                "y suman %d: todos los estudios del corpus tienen el artículo "
                "completo (sección 2.9). «Declarado pero no clasificable» significa "
                "que el artículo nombra la variable en términos que no permiten "
                "asignar una categoría: «multirresistente» sin el antibiograma que "
                "decida entre MDR, XDR y PDR. La columna del resumen se reproduce "
                "desde el anexo S4 filtrando en_corpus_actual = sí; las del texto "
                "completo, desde la extracción adjudicada (anexo S14)." % n)
    else:
        escribe("tabla_2_completitud",
            ["Variable", "No asignable en el resumen",
             "Declarado en el texto completo", "Declarado pero no clasificable",
             "No declarado en el texto completo", "Texto completo no recuperado"],
            filas,
            "Tabla 3. Completitud del reporte en las variables de "
            "estratificación, en el resumen y en el texto completo "
            "(n = %d estudios recuperables, %d con texto obtenido)."
            % (n, S["t3_con_texto"]),
            "La segunda columna mide el RESUMEN indexado, que es lo que "
            "alimenta las bases bibliográficas y las revisiones automatizadas. "
            "Las cuatro siguientes miden el TEXTO COMPLETO, se excluyen entre "
            "sí y suman %d. «Declarado pero no clasificable» significa que el "
            "artículo nombra la variable en términos que no permiten asignar "
            "una categoría: «multirresistente» sin el antibiograma que decida "
            "entre MDR, XDR y PDR. «Texto completo no recuperado» no es "
            "silencio del estudio: de esos %d artículos no sabemos lo que "
            "dicen. La columna del resumen se reproduce desde el anexo S4 "
            "filtrando en_corpus_actual = sí; las del texto completo, desde la "
            "extracción adjudicada (anexo S14)."
            % (n, S["t3_resistance_class_sin_texto"]))

    # ---- Tabla 3: lo que el criterio del texto completo deja fuera ----------
    # Hasta el 2026-10-06 comparaba los estudios con y sin texto completo
    # DENTRO del corpus. Desde la ampliacion de NOREC (codigo NOPDF, firmada
    # por los dos) no queda ninguno sin texto: la comparacion es ahora entre lo
    # que se incluye y lo que el criterio excluyo por no tener el articulo.
    # Las fichas de registro no tienen diseno extraido del resumen y se
    # cuentan aparte, en la nota.
    con = extr & pdfs
    with open(RS / "cribado" / "exclusiones_tras_texto_completo.csv", encoding="utf-8",
              newline="") as fh:
        _cod = {r["study_id"]: r["codigo"] for r in csv.DictReader(fh)}
    _sit = {"EST-%03d" % int(g["estudio"]): g["situacion"] for g in grupos
            if g["informe_para_extraer"] == "SI"}
    sin_ = {e for e, c in _cod.items() if c in ("NOREC", "NOPDF")
            and _sit.get(e) in ("extraible", "solo-resumen")}

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
    mil = lambda x: f"{x:,}".replace(",", " ")
    filas = [["Estudios", len(con), len(sin_)],
             ["Diseños comparativos", cc, cs],
             ["Comparativos (% de la columna)",
              "%.1f" % (100.0 * cc / max(1, len(con))), "%.1f" % (100.0 * cs / max(1, len(sin_)))],
             ["Reportes de caso único", dc["case report"], ds["case report"]],
             ["Ensayos aleatorizados", dc["RCT"], ds["RCT"]],
             ["Pacientes declarados (suma de n por brazo)", mil(pcn), mil(psn)]]
    escribe("tabla_3_sesgo_recuperacion",
            ["", "Incluidos (texto completo leído)",
             "Excluidos por no tener el texto completo"], filas,
            "Tabla 3. Lo que el criterio del texto completo deja fuera: estudios "
            "incluidos frente a los excluidos por no disponer del PDF del artículo.",
            # La nota se DERIVA de la tabla, como antes: una nota que asegura
            # una direccion sin mirarla es una cifra tecleada disfrazada.
            "La columna de excluidos reúne los artículos cuyo texto no se obtuvo y "
            "los resúmenes de congreso (códigos NOREC y NOPDF); el diseño sale del "
            "resumen. Además se excluyeron %d fichas de registro sin artículo, que no "
            "tienen diseño extraído. Lo excluido no es una muestra aleatoria: "
            "concentra el %.1f %% de los diseños comparativos (%.1f %% de esa "
            "columna, frente al %.1f %% de la de incluidos) y declara %s pacientes "
            "(%s frente a %s). Es el efecto del criterio, y se declara como tal."
            % (S["criterio_texto_fichas"], S["criterio_texto_comparativos_pct"],
               100.0 * cs / max(1, len(sin_)), 100.0 * cc / max(1, len(con)),
               "más" if psn > pcn else "menos", mil(psn), mil(pcn)))

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
        # Desde el 2026-10-06 todos los brazos son de estudios con texto
        # completo (seccion 2.9): la columna «% de los brazos legibles» repetia
        # la anterior cifra por cifra.
        dos_denominadores = O["brazos_legibles"] != O["brazos"]
        for campo, d in O["desenlaces"].items():
            filas.append([
                d["nombre"].capitalize(),
                d["con_numerador_y_denominador"],
                "%.1f" % d["pct_de_los_brazos"]]
                + (["%.1f" % d["pct_de_los_legibles"]] if dos_denominadores else [])
                + ["%.1f" % d["doble_lectura_pct"]])
        if dos_denominadores:
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
        else:
            nota = (
                "La tabla mide COMPLETITUD DE REPORTE, no eficacia: un numerador sin "
                "denominador no es una proporción. Los %d brazos pertenecen a "
                "estudios con el artículo completo leído (sección 2.9), de modo que "
                "un desenlace que no consta es un desenlace que el artículo no "
                "reporta. «Con doble lectura» es el porcentaje de esas casillas en "
                "que los dos revisores coincidieron o resolvieron por consenso; el "
                "resto lo leyó un solo revisor, y en la fila de emergencia de "
                "resistencia esas casillas las rellenó siempre el mismo. "
                % O["brazos"])
        if O.get("campos_del_esquema_no_extraidos"):
            nota += (
                "La fila de erradicación usa el tamaño del brazo como denominador: "
                "el esquema declara además %s, que se añadieron después de "
                "repartir los formularios y nunca llegaron a extraerse, de modo "
                "que no consta a cuántos pacientes se les hizo cultivo de control. "
                "El denominador real es por tanto menor o igual que el usado. "
                % " y ".join("`%s`" % c for c in O["campos_del_esquema_no_extraidos"]))
        if O["brazos_con_diseno"] == O["brazos"]:
            nota += (
                "El diseño consta en los %d brazos: %d son comparativos, y solo %d "
                "reúnen a la vez diseño comparativo, numerador, denominador y una "
                "definición operativa del éxito clínico. "
                % (O["brazos"], O["brazos_comparativos"],
                   O["brazos_agregables_exito_clinico"]))
        else:
            nota += (
                "El diseño solo puede clasificarse en %d de los %d brazos (%d con un "
                "«NA» que los dos revisores acordaron y %d con la casilla aún "
                "abierta), de modo que los recuentos por diseño son suelos: de esos "
                "%d, %d son comparativos, y solo %d reúnen a la vez diseño "
                "comparativo, numerador, denominador y una definición operativa del "
                "éxito clínico. "
                % (O["brazos_con_diseno"], O["brazos"], O["diseno_na_acordado"],
                   O["diseno_abierto"], O["brazos_con_diseno"],
                   O["brazos_comparativos"], O["brazos_agregables_exito_clinico"]))
        nota += (
            "Dos brazos reportan un numerador mayor que su "
            "denominador y se señalan como error de reporte. «Comparativo» "
            "describe lo que el estudio es, no lo que hay en este fichero: la "
            "extracción se hizo por brazo y se extrajo el de fago, de modo que "
            "el conjunto no contiene los brazos de control.")
        escribe("tabla_5_desenlaces",
                ["Desenlace", "Con numerador y denominador",
                 "%% de los %d brazos" % O["brazos"]]
                # «con texto completo» se leia como estudios o como textos,
                # y son BRAZOS. Solo se da si difiere del total.
                + (["%% de los %d brazos legibles" % O["brazos_legibles"]]
                   if dos_denominadores else [])
                + ["% con doble lectura"], filas,
                "Tabla 5. Completitud de reporte de los cinco desenlaces "
                "declarados, sobre los %d brazos de la extracción adjudicada."
                % O["brazos"], nota)

    # ---- Tabla 6: el embudo -------------------------------------------------
    # Cada fila quita brazos por una razon nombrada. Los dos ultimos filtros
    # son los criterios de elegibilidad del propio articulo (§2.2), que hasta
    # ahora no se aplicaban a este cruce: sin ellos el embudo paraba en 3.
    if oc.exists():
        # DOS EMBUDOS, DOS PREGUNTAS. El de la izquierda incluye el diseño
        # comparativo y responde a «¿había un contraste utilizable?». El de la
        # derecha lo omite --agrupar proporciones no exige diseño comparativo--
        # y responde a «¿había proporciones agrupables?». Presentar solo el
        # primero hacía pasar por imposibilidad aritmética lo que es una
        # decisión clínica y estadística.
        prop = {x["filtro"]: x for x in S["embudo_proporcion"]}
        filas = []
        for x in O["embudo"]:
            f = x["filtro"]
            pr = prop.get(f)
            filas.append([f[:1].upper() + f[1:], x["quedan"],
                          "%d (%d estudios)" % (pr["brazos"], pr["estudios"])
                          if pr else "no se aplica"])
        escribe("tabla_6_embudo",
                ["Requisito acumulado", "Efecto comparativo: brazos que quedan",
                 "Proporción descriptiva: brazos que quedan"],
                filas,
                "Tabla 6. Brazos que sobreviven a cada requisito de una "
                "proporción agrupada de éxito clínico (n = %d brazos "
                "extraídos)." % O["brazos"],
                "Cada fila aplica el requisito de esa fila Y todos los "
                "anteriores. **Las dos últimas columnas responden a preguntas "
                "distintas.** La primera exige además diseño comparativo y "
                "responde a si el corpus sostiene un efecto comparativo; la "
                "segunda omite ese requisito, porque agrupar proporciones no lo "
                "exige, y responde a si sostiene una proporción descriptiva. "
                "Los criterios de elegibilidad de la sección 2.2 son los dos "
                "penúltimos: el desenlace tiene que poder atribuirse a "
                "*P. aeruginosa* --la extracción anota cuándo el artículo no "
                "separa los patógenos-- y la administración tiene que ser "
                "terapéutica, no profiláctica. El último se lee en el artículo "
                "y no en una casilla: PhagoBurn reporta el tiempo hasta una "
                "reducción sostenida de carga bacteriana, no una proporción. "
                "Ningún brazo reúne los siete requisitos; %d brazos de %d "
                "estudios reúnen los seis de la proporción descriptiva, y %d de "
                "esos %d tienen un denominador de un solo paciente."
                % (S["brazos_agrupables"], S["estudios_agrupables"],
                   S["brazos_agrupables_n1"], S["brazos_agrupables"]))

    print("escritas en %s" % OUT)
    return 0


if __name__ == "__main__":
    sys.exit(main())
