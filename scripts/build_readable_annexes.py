"""Convierte los anexos del paquete en cuadernos que un revisor pueda leer.

EL PROBLEMA

Los anexos se exportan como CSV con los nombres internos del canal:
`record_id`, `verdict`, `decided_by`, `pathogen_scope`, `extraction_status`. Un
revisor que abre S3 encuentra 13 917 filas de `EXCLUDE` y `ADVANCE` sin saber
qué es una fila, cuántas debería haber, ni qué significa la columna. El fichero
es correcto y no comunica nada.

QUE HACE

Por cada CSV del paquete escribe un .xlsx con dos hojas:

  «Léeme»       qué es este anexo, cuántas filas tiene, qué significa cada
                columna, y a qué sección del manuscrito corresponde
  los datos     con las cabeceras en castellano, los códigos traducidos, la
                primera fila congelada y filtros puestos

QUE NO HACE

No toca los CSV. Se conservan tal cual, con sus nombres internos, porque son la
copia reproducible: quien quiera reejecutar el canal necesita las claves que el
canal usa, no una traducción. El .xlsx es para leer; el .csv es para verificar.
Un paquete que solo trae la versión bonita pierde la trazabilidad, y uno que
solo trae la cruda no la comunica.

Uso:
    python scripts/build_readable_annexes.py
"""
import csv
import datetime
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
PAQ = ROOT / "verificables revisión sistemática"
csv.field_size_limit(200_000_000)
try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

# Qué es cada anexo, en una frase que un revisor entienda sin abrir el fichero.
QUE_ES = {
    "S3_decisiones_etapa2_titulo": (
        "Toda decisión de cribado por TÍTULO, una por fila, con su motivo y su marca de tiempo.",
        "Sección 2.4. El registro es solo-anexar: una corrección es una fila nueva y ambas permanecen."),
    "S3_decisiones_etapa3_resumen": (
        "Toda decisión de cribado por RESUMEN, una por fila, con su motivo y su marca de tiempo.",
        "Sección 2.4. Solo llegan aquí los registros que superaron el cribado por título."),
    # Decia «la fuente de TODA cifra que el artículo publica» y no decia quien
    # la emitio. Las dos cosas eran falsas o faltaban: la emitio el modelo, y
    # la sección 3.5 y la tabla 5 salen de la extraccion adjudicada (S14), no
    # de aqui.
    "S4_pre_extraccion_desde_resumen": (
        "La pre-extracción desde el resumen, emitida por el modelo de lenguaje "
        "(Claude Opus 5); fuente de las cifras estructurales (secciones 3.1 a 3.4).",
        "Sección 2.6. Cada fila va marcada PARCIAL: describe lo que el resumen declara, no el texto completo. "
        "Los desenlaces (sección 3.5, tabla 5) salen de la extracción adjudicada, S14."),
    # La clave llevaba el recuento de un corpus viejo y no casaba con el
    # fichero: S5 salia con la Léeme generica. Ahora se busca sin recuento.
    "S5_listado": (
        "Los estudios del corpus tras agrupar los informes, con su situación y si se obtuvo el texto completo.",
        "Sección 3.1. La unidad es el estudio, no el informe: un mismo estudio puede tener varios informes."),
    # Decia «Cómo se localizó cada texto completo, o por qué no se pudo» y
    # «Explica el sesgo de recuperación que el artículo mide». S8 no es eso: es
    # la vía resuelta de los informes sin DOI editorial (fulltext_identifiers),
    # y desde NOPDF (2026-10-06) la recuperación es del 100 % por construcción.
    # Se alinea con la descripción del índice (build_editorial_report).
    "S8_recuperacion_texto_completo": (
        "La vía de recuperación resuelta para cada informe sin DOI editorial "
        "(resúmenes de congreso, fichas de registro y algunos artículos): el "
        "identificador que se resolvió y cómo. No es el registro de los intentos "
        "de obtener cada texto completo.",
        "Sección 3.2."),
    "S9_idioma_por_informe_y_clase_de_evidencia": (
        "El idioma de cada informe y de dónde se determinó, informe a informe.",
        "Sección 2.9. Sostiene la enmienda de idioma y su impacto medido."),
    "S10_idioma_verificado_sobre_texto_completo": (
        "El idioma comprobado sobre el PDF, no sobre lo que declaraba la base de datos.",
        "Sección 2.9. El nombre de la revista no determina el idioma del artículo."),
    "S21_solapamiento_de_pacientes": (
        "Cada par de estudios que podía describir a los mismos pacientes, con el veredicto "
        "tras leer los dos artículos y los pacientes que comparten, una clave por persona.",
        # Decia «limitación séptima»: al añadir la limitación del cribado por
        # el modelo pasó a ser la octava en el maestro, y en el manuscrito de
        # la revista es otra. Se remite por su asunto, sin ordinal.
        "Sección 4.4, en la limitación sobre pacientes descritos en más de un "
        "estudio. Un paciente que sale en tres pares tiene la misma "
        "clave en los tres y se cuenta una vez."),
    "S23_clase_de_resistencia_comprobada": (
        "La clase de resistencia de cada estudio con texto completo, comprobada contra el "
        "antibiograma del artículo, con la conclusión firmada por los dos autores.",
        "Sección 3.4. La columna «queda abierto» dice lo que la lectura no resolvió y no "
        "se cambió en la extracción."),
    "S24_comparativos_reextraidos": (
        "Los estudios con diseño comparativo, reextraídos: qué comparan, desde cuándo, "
        "hasta cuándo y si hay un contraste para P. aeruginosa.",
        "Sección 3.7. «Grupo sin fago» y «contraste para P. aeruginosa» son la "
        "codificación del texto firmado que va al lado."),
    # S15 y S18b salian con el texto por defecto, «Anexo del material
    # suplementario.», y en S15 nadie explicaba las etiquetas: el lector tenia
    # que adivinar que «consenso» (la etiqueta de entonces) cubria tambien
    # casillas que el registro atribuye a un unico responsable.
    "S15_procedencia_de_cada_casilla": (
        "De dónde salió cada casilla de la extracción adjudicada (S14): el mismo "
        "cuadro, una fila por brazo y una columna por variable, con la etiqueta de "
        "procedencia en lugar del valor.",
        # Decia que «con doble lectura» contaba tambien las «corregidas con dos
        # firmas». No es el calculo: build_outcome_scalars.DOBLE cuenta acuerdo
        # y las tres «adjudicada ...», y ninguna corregida. main() lo comprueba
        # contra DOBLE antes de escribirlo (DOBLE_DE_LA_TABLA, abajo).
        "Sección 2.6 y tabla 5, cuyo «con doble lectura» cuenta las casillas con "
        "acuerdo o adjudicadas, por uno o por los dos; las corregidas contra el "
        "texto no cuentan, tampoco las de dos firmas. Cada etiqueta se explica "
        "abajo."),
    "S18b_frases_cosechadas_por_tema": (
        "Las frases de cada artículo que el modelo de lenguaje (Claude Opus 5) "
        "localizó de forma automática, buscando expresiones, para cada dominio o "
        "tema de riesgo de sesgo, y que puso como comentario en las casillas de los "
        "formularios. Sirven para buscar en el artículo, no para sostener un juicio.",
        "Sección 2.7. Lo que sostiene cada juicio está en S18. Un tema sin frases "
        "quiere decir que el buscador no encontró la expresión, no que el artículo "
        "no trate el asunto."),
}

# Lo que significa cada etiqueta de un anexo cuyas casillas son etiquetas y no
# datos. El recuento de cada una se cuenta en el propio CSV al escribir el
# Léeme, no se teclea. Si el CSV trae una etiqueta que no esta aqui, el guion
# se para: un Léeme que no explica una de sus etiquetas es justo el defecto
# que esto corrige.
ETIQUETAS_DE = {
    # Las tres «adjudicada ...» eran una sola, «consenso», hasta el 2026-10-08
    # (build_adjudicated_dataset.py). La columna resuelto_por del registro de
    # adjudicacion anota a los dos revisores en pocas filas y un unico
    # responsable en el resto; la etiqueta dice lo que anota, no mas.
    "S15_procedencia_de_cada_casilla": [
        ("acuerdo", "Los dos revisores escribieron el mismo valor, una vez "
                    "normalizado el vocabulario."),
        # «Solo estas constan como consenso» chocaba con la etiqueta
        # «corregido por consenso contra el texto» de la misma hoja; esa
        # etiqueta es ahora «corregido contra el texto (dos firmas)», y la
        # frase se acota a las adjudicadas: una casilla adjudicada por los dos
        # que despues se corrigio lleva la etiqueta de la correccion.
        ("adjudicada por los dos",
         "Los dos revisores discreparon; el valor es el del registro de "
         "adjudicación (extraction_conflicts.csv), que anota como responsables a "
         "los dos. Entre las casillas adjudicadas, solo estas constan como "
         "consenso."),
        ("adjudicada por uno (D.V.)",
         "Los dos revisores discreparon; el valor es el del registro de "
         "adjudicación, que anota un único responsable: D.V."),
        ("adjudicada por uno (N.T.)",
         "Los dos revisores discreparon; el valor es el del registro de "
         "adjudicación, que anota un único responsable: N.T."),
        # Se llamaba «corregido por consenso contra el texto» hasta el
        # 2026-10-13 (build_adjudicated_dataset.CORR_DOS). Ahora dice cuantas
        # firmas lleva, simetrica con la de una firma.
        ("corregido contra el texto (dos firmas)",
         "Casilla ya cerrada que una corrección posterior, con su cita literal y "
         "la firma de los dos autores, cambió contra el texto completo "
         "(correcciones_tras_texto_completo.csv). Las correcciones de modalidad las "
         "propuso el modelo de lenguaje tras leer los textos. No cuenta como "
         "doble lectura en la tabla 5."),
        ("corregido contra el texto (una firma)",
         "Lo mismo, con la firma de un solo autor; no cuenta como doble lectura. "
         "Entre ellas están las casillas del tercer paciente de EST-121, que "
         "extrajo el modelo de lenguaje y firmó solo D.V."),
        ("sin segunda lectura",
         "Solo un revisor rellenó la casilla; no cuenta como doble lectura."),
        ("ABIERTO",
         "Los dos discreparon y el desacuerdo no está adjudicado; la casilla sale "
         "vacía en S14. Así queda también un desacuerdo que se cerró por una "
         "regla mecánica, sin firma conjunta: su valor no lo firmó nadie."),
        ("vacio", "Ninguno de los dos rellenó la casilla."),
    ],
}
NOTA_ETIQUETAS = {
    "S15_procedencia_de_cada_casilla": (
        "Una casilla adjudicada que después se corrigió contra el texto lleva la "
        "etiqueta de la corrección; por eso las casillas «adjudicada» son menos "
        "que los desacuerdos adjudicados del registro. Que el registro anote un "
        "único responsable dice quién firmó, no cuántos leyeron: la casilla la "
        "leyeron los dos, y por eso discreparon."),
}

# Las etiquetas que la Léeme de S15 dice que cuentan como doble lectura en la
# tabla 5. La frase la escribe QUE_ES; esto la ata al calculo: si
# build_outcome_scalars.DOBLE cambia, el guion se para en vez de publicar una
# descripcion que ya no es la del calculo.
DOBLE_DE_LA_TABLA = {"acuerdo", "adjudicada por los dos",
                     "adjudicada por uno (D.V.)", "adjudicada por uno (N.T.)"}

# Las Léeme remiten a la numeracion del informe extendido (el maestro). El
# manuscrito de la revista no numera las secciones y numera las tablas de otro
# modo, y estos .xlsx viajan tambien en el sobre de la revista. Decia «el
# manuscrito enviado a la revista»: no se ha enviado, y enviarlo o no lo
# deciden los autores.
NUMERACION = ("Las secciones y tablas que se citan son las del informe extendido "
              "(manuscrito maestro). En el manuscrito preparado para la revista "
              "las secciones no van numeradas")
NUMERACION_TABLA5 = "; allí la tabla 5 (desenlaces) es la Tabla 4"


def numeracion(donde):
    """La advertencia de numeracion, con la equivalencia de la tabla 5 solo
    donde la Léeme la cita."""
    return NUMERACION + (NUMERACION_TABLA5 if "tabla 5" in donde else "") + "."


def alcance_s18b(datos, cab):
    """Qué estudios trae S18b frente a los que tienen juicio en S18.

    S18b llegó a traer frases de tres estudios sin juicio en S18 (EST-055,
    EST-063 y EST-132, en el consejo del 2026-10-13). El filtro a los estudios
    con juicio en S18 se hace en build_verifiables_package; la Léeme lo dice,
    y lo dice leyendo los dos CSV, de modo que no puede afirmar un filtro que
    no se hizo: si quedan estudios sin juicio, los nombra.
    """
    s18 = PAQ / "S18_cada_juicio_con_su_frase.csv"
    if "study_id" not in cab or not s18.exists():
        return ""
    i = cab.index("study_id")
    propios = {f[i] for f in datos if len(f) > i and f[i].strip()}
    with open(s18, encoding="utf-8-sig", newline="") as fh:
        con_juicio = {r["estudio"] for r in csv.DictReader(fh)}
    fuera = sorted(propios - con_juicio)
    if not fuera:
        return (" Solo trae los %d estudios que tienen juicio en S18; las frases "
                "cosechadas para cualquier otro estudio no se incluyen."
                % len(propios))
    return (" Trae %d estudios; %d de ellos (%s) no tienen juicio en S18."
            % (len(propios), len(fuera), ", ".join(fuera)))

# Cabeceras. Lo que el canal llama X, un revisor lo entiende como Y.
ETIQUETA = {
    "record_id": "Identificador del informe", "id": "Identificador",
    "id_provisional": "Identificador del estudio", "estudio": "Estudio",
    "arm_id": "Brazo", "orden": "Orden", "verdict": "Decisión",
    "reason": "Motivo", "decided_by": "Quién decidió", "decided_at": "Cuándo",
    "corriente": "Corriente (base o registro)", "titulo": "Título",
    "revista": "Revista", "anio": "Año", "situacion": "Situación",
    "n_informes": "Informes del estudio", "diseno": "Diseño",
    "n_brazo": "Pacientes en el brazo", "procedencia": "País",
    "texto_completo": "¿Texto completo obtenido?", "clave_de_estudio": "Clave del estudio",
    "tipo": "Tipo de informe", "identificador_resuelto": "Identificador resuelto",
    "via": "Cómo se localizó", "nota": "Nota", "duplicado_interno": "Duplicado interno",
    "fuentes": "Fuentes que lo aportaron", "paginas": "Páginas", "palabras": "Palabras",
    "idioma_texto_completo": "Idioma del texto completo", "confianza": "Confianza",
    "evidencia": "Evidencia", "idioma_previo": "Idioma declarado antes",
    "coincide": "¿Coinciden?", "idioma_declarado": "Idioma declarado",
    "fuente_declarado": "De dónde sale el idioma declarado",
    "idioma_del_texto": "Idioma del texto", "clase_de_evidencia": "Clase de evidencia",
    "prueba": "Prueba", "estado": "Estado",
    "caracteres_de_resumen": "Caracteres del resumen",
    "titulo_alternativo": "Título alternativo",
    "pathogen_scope": "¿Solo P. aeruginosa o mixto?",
    "resistance_class": "Clase de resistencia",
    "resistance_class_source": "De dónde sale la clase",
    "dtr_status": "¿Cumple criterio DTR?", "route": "Vía de administración",
    "modality": "¿Fago solo o con antibiótico?", "study_design": "Diseño del estudio",
    "extraction_status": "Estado de la extracción", "n_arm": "Pacientes en el brazo",
    "en_corpus_actual": "¿Sigue en el corpus?", "study_id": "Estudio",
    "estado_final": "¿Quedó incluido al final?",
    "motivo_de_la_exclusion": "Por qué se excluyó",
    "campo": "Variable", "resolucion": "Valor acordado",
    "resuelto_por": "Quién lo resolvió", "fecha": "Fecha",
}

# Códigos internos -> castellano. Solo donde el código no se entiende solo.
VALOR = {
    "EXCLUDE": "excluido", "ADVANCE": "pasa a resumen", "FULLTEXT": "pasa a texto completo",
    "Pseudomonas-only": "solo P. aeruginosa",
    "mixed-pathogen-with-Pseudomonas-subgroup": "mixto, con subgrupo separable",
    "not-classifiable": "no clasificable", "below-MDR-threshold": "por debajo de MDR",
    "author-reported": "declarado por el autor",
    "independently-verified": "verificado de forma independiente",
    "yes": "sí", "no": "no", "not-derivable": "no derivable",
    "PARTIAL": "parcial", "COMPLETE": "completa",
    "extraible": "extraíble", "solo-registro": "solo ficha de registro",
    "solo-resumen": "solo resumen",
    "case report": "reporte de caso único", "case series": "serie de casos",
    "RCT": "ensayo aleatorizado", "non-randomised trial": "ensayo no aleatorizado",
    "prospective cohort": "cohorte prospectiva",
    "retrospective cohort": "cohorte retrospectiva",
    "base": "base bibliográfica", "registro": "registro de ensayos",
    # Vias y modalidades. Se traducen porque son de las columnas que un revisor
    # lee primero; los identificadores de ensayo y los DOI NO se tocan, que son
    # claves y traducirlas seria destruirlas.
    "phage+antibiotic combination": "fago + antibiótico",
    "phage monotherapy": "fago en monoterapia",
    "topical/local": "tópica o local", "inhaled/nebulized": "inhalada o nebulizada",
    "IV": "intravenosa", "oral": "oral", "intravenous": "intravenosa",
    "other": "otra", "unknown": "no consta", "none": "ninguno",
    "no-latino": "no latino",
    "INCLUIDO": "incluido", "EXCLUIDO DESPUES": "excluido después",
    "ADMITIDO": "admitido",
}


def main():
    if not PAQ.exists():
        print("no existe %s" % PAQ)
        return 1
    import openpyxl
    from openpyxl.styles import Font, PatternFill, Alignment
    from openpyxl.utils import get_column_letter

    AZUL = PatternFill("solid", fgColor="1F4E79")
    hechos = 0

    for csvf in sorted(PAQ.glob("S*.csv")):
        clave = csvf.stem
        # Solo para buscar la descripción: el nombre del fichero no se toca.
        busca = "S5_listado" if clave.startswith("S5_listado_") else clave
        with open(csvf, encoding="utf-8-sig", newline="") as fh:
            filas = list(csv.reader(fh))
        if not filas:
            continue
        cab, datos = filas[0], filas[1:]
        que, donde = QUE_ES.get(busca, ("Anexo del material suplementario.", ""))
        if clave == "S18b_frases_cosechadas_por_tema":
            que += alcance_s18b(datos, cab)
        if clave == "S15_procedencia_de_cada_casilla":
            from build_outcome_scalars import DOBLE
            if set(DOBLE) != DOBLE_DE_LA_TABLA:
                raise SystemExit(
                    "La Léeme de S15 dice que la doble lectura de la tabla 5 "
                    "cuenta %s, y build_outcome_scalars.DOBLE cuenta %s. "
                    "Corrige la frase de QUE_ES y DOBLE_DE_LA_TABLA."
                    % (sorted(DOBLE_DE_LA_TABLA), sorted(DOBLE)))

        wb = openpyxl.Workbook()

        # ---- Léeme ---------------------------------------------------------
        p = wb.active
        p.title = "Léeme"
        p.column_dimensions["A"].width = 42
        p.column_dimensions["B"].width = 74
        lineas = [
            (clave.replace("_", " "), 15, True),
            ("", 11, False),
            ("Qué es", 12, True), (que, 11, False),
            ("", 11, False),
            ("Dónde se usa", 12, True), (donde, 11, False),
        ] + ([(numeracion(donde), 10, False)] if donde else []) + [
            ("", 11, False),
            ("Cuántas filas", 12, True), ("%d filas de datos" % len(datos), 11, False),
            ("", 11, False),
            ("Qué significa cada columna", 12, True),
        ]
        f = 1
        for txt, tam, neg in lineas:
            c = p.cell(row=f, column=1, value=txt)
            c.font = Font(size=tam, bold=neg, color="1F4E79" if neg and tam >= 12 else "000000")
            c.alignment = Alignment(wrap_text=True, vertical="top")
            f += 1
        for col in cab:
            p.cell(row=f, column=1, value=ETIQUETA.get(col, col)).font = Font(bold=True, size=10)
            p.cell(row=f, column=2, value="columna interna: %s" % col).font = Font(size=10, color="808080")
            f += 1
        if clave in ETIQUETAS_DE:
            # Las casillas de datos son etiquetas: se cuentan aqui, sobre las
            # columnas que no son la clave del brazo.
            ids = {i for i, c in enumerate(cab) if c in ("study_id", "arm_id")}
            cuenta = {}
            for fila in datos:
                for i, v in enumerate(fila):
                    if i not in ids:
                        cuenta[v] = cuenta.get(v, 0) + 1
            explicadas = dict(ETIQUETAS_DE[clave])
            sobran = sorted(set(cuenta) - set(explicadas))
            if sobran:
                raise SystemExit("%s: etiquetas sin explicar en el Léeme: %s. "
                                 "Añádelas a ETIQUETAS_DE." % (clave, sobran))
            f += 1
            c = p.cell(row=f, column=1, value="Qué significa cada etiqueta")
            c.font = Font(size=12, bold=True, color="1F4E79")
            f += 1
            for etiqueta, sentido in ETIQUETAS_DE[clave]:
                c = p.cell(row=f, column=1, value="%s (%d casillas)"
                           % (etiqueta, cuenta.get(etiqueta, 0)))
                c.font = Font(bold=True, size=10)
                c.alignment = Alignment(wrap_text=True, vertical="top")
                c = p.cell(row=f, column=2, value=sentido)
                c.font = Font(size=10)
                c.alignment = Alignment(wrap_text=True, vertical="top")
                f += 1
            if clave in NOTA_ETIQUETAS:
                c = p.cell(row=f, column=2, value=NOTA_ETIQUETAS[clave])
                c.font = Font(size=10, italic=True)
                c.alignment = Alignment(wrap_text=True, vertical="top")
                f += 1
        f += 1
        p.cell(row=f, column=1, value="El CSV con los nombres internos acompaña a este fichero: "
               "es la copia reproducible.").font = Font(size=10, italic=True)
        p.cell(row=f + 2, column=1,
               value="Generado el %s" % datetime.date.today().isoformat()).font = Font(size=9, color="808080")

        # ---- datos ---------------------------------------------------------
        h = wb.create_sheet("Datos")
        h.append([ETIQUETA.get(c, c) for c in cab])
        for c in h[1]:
            c.fill, c.font = AZUL, Font(color="FFFFFF", bold=True, size=10)
            c.alignment = Alignment(wrap_text=True, vertical="center")
        h.row_dimensions[1].height = 30
        for fila in datos:
            h.append([VALOR.get((v or "").strip(), v) for v in fila])
        h.freeze_panes = "A2"
        h.auto_filter.ref = "A1:%s%d" % (get_column_letter(len(cab)), h.max_row)
        for i, col in enumerate(cab, start=1):
            ancho = 46 if col in ("titulo", "reason", "evidencia", "nota",
                                  "titulo_alternativo", "via", "motivo_de_la_exclusion") else 20
            h.column_dimensions[get_column_letter(i)].width = ancho

        sal = PAQ / (clave + ".xlsx")
        wb.save(sal)
        hechos += 1
        print("  %-48s %6d filas" % (sal.name[:48], len(datos)))

    print()
    print("%d anexos convertidos. Los CSV se conservan intactos." % hechos)
    return 0


if __name__ == "__main__":
    sys.exit(main())
