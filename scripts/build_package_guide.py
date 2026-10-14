"""Guía del material suplementario: qué contesta cada fichero del paquete.

POR QUÉ HACE FALTA

Un paquete de catorce anexos sin guía obliga al revisor a abrirlos uno por uno
para averiguar cuál responde a su duda. Este PDF es el mapa: para cada fichero
dice qué contiene, qué pregunta permite contestar y qué formato tiene, y agrupa
los anexos por la etapa de la revisión que documentan.

El inventario se lee del disco, no de una lista escrita a mano. Si un anexo
desaparece o cambia de tamaño, la guía lo refleja al reejecutar; y si aparece un
fichero que nadie ha descrito, la guía lo dice en lugar de callarlo.

Uso:
    python scripts/build_package_guide.py
"""
import ast
import csv
import json
import pathlib
import re
import sys

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.platypus import Paragraph, Spacer

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from build_manuscript_pdf import estilos, inline  # noqa: E402
from build_extraction_verifiables import ANCHO, SIN_CITAS, cuadro, documento  # noqa: E402
# La misma cuenta de S16 que escribe la lista de anexos de los manuscritos: la
# guía y la lista no pueden describir el anexo con cifras distintas. Lo mismo
# para S10 y para la numeración de tablas y secciones, leída de los manuscritos.
from build_lista_anexos import citas_s16, de_las_citadas, numeracion, s10  # noqa: E402

ROOT = pathlib.Path(__file__).resolve().parent.parent
OUT = ROOT / "verificables revisión sistemática"

# La guia describia «los 90 juicios de riesgo de sesgo» con una cifra tecleada,
# y se volvio falsa el 2026-09-22 al salir EST-063 del corpus. Ahora entra por
# el escalar, como todo lo demas.
_S = json.loads((ROOT / "quality_reports" / "synthesis_scalars.json")
                .read_text(encoding="utf-8"))
_S16 = citas_s16(_S)
# Desacuerdos de extracción que siguen sin adjudicar. Cambia la forma de varias
# frases, no solo una cifra: con 0 no se puede decir «no ha concluido».
_PENDIENTES = _S["extraccion_conflictos_sin_firmar"]

# LA NUMERACIÓN. La guía decía «la sección 3.5 y las tablas 5 y 6», «la tabla
# 7», «la sección 3.6», con la numeración del maestro, y viaja en el sobre con
# el manuscrito de la revista, que no numera los apartados y numera las tablas
# de otro modo: allí la «tabla 5» es la de riesgo de sesgo. Ahora cada número
# se lee de los dos manuscritos y la guía da los dos.
_N = numeracion()
_D, _F, _R = _N["desenlaces"], _N["embudo"], _N["riesgo"]


def _apartado(tema):
    """«el apartado «X» de RESULTADOS»: el equivalente de una sección del
    maestro en el manuscrito de la revista, que no numera los apartados."""
    t = _N[tema]
    return "el apartado «%s» de %s" % (t["apartado_revista"],
                                       t["capitulo_revista"])


def _extendido_en_el_sobre():
    """(carpeta, fichero) con que el sobre de la revista lleva el informe
    extendido, leídos del generador del sobre sin ejecutarlo; None si no se
    encuentran.

    La guía viaja en suplementos/ y remitía al PDF maestro, que no va ahí: en
    el sobre el informe extendido va aparte (build_jsr_submission.py, tupla
    LECTURA y carpeta leer_dst). Se lee del generador para que la guía no
    nombre un fichero que el sobre ya no lleve."""
    try:
        arbol = ast.parse((ROOT / "scripts" / "build_jsr_submission.py")
                          .read_text(encoding="utf-8"))
    except (OSError, SyntaxError):
        return None
    carpeta = fichero = None
    for nodo in ast.walk(arbol):
        if not isinstance(nodo, ast.Assign):
            continue
        nombres = {t.id for t in nodo.targets if isinstance(t, ast.Name)}
        if "LECTURA" in nombres:
            try:
                for f, que in ast.literal_eval(nodo.value):
                    if "informe extendido" in que:
                        fichero = f
            except (ValueError, TypeError):
                pass
        v = nodo.value
        if ("leer_dst" in nombres and isinstance(v, ast.BinOp)
                and isinstance(v.op, ast.Div)
                and isinstance(v.right, ast.Constant)):
            carpeta = v.right.value
    return (carpeta, fichero) if carpeta and fichero else None


def _nota_numeracion():
    """La nota del principio: qué numeración usa la guía y la equivalencia de
    las tablas que cita, ordenada como en el manuscrito de la revista."""
    nombres = {"desenlaces": "de desenlaces", "riesgo": "de riesgo de sesgo",
               "embudo": "del embudo de agregabilidad"}
    orden = sorted(_N, key=lambda k: _N[k]["tabla_revista"])
    trozos = []
    for i, k in enumerate(orden):
        t = _N[k]
        igual = "también " if t["tabla_revista"] == t["tabla_maestro"] else ""
        if i == 0:
            trozos.append("la tabla %s es la Tabla %d (en el informe extendido, "
                          "%sla %d)" % (nombres[k], t["tabla_revista"], igual,
                                        t["tabla_maestro"]))
        else:
            trozos.append("la %s, la Tabla %d (%sla %d)" % (
                nombres[k], t["tabla_revista"], igual, t["tabla_maestro"]))
    lista = (("; ".join(trozos[:-1]) + ", y " + trozos[-1])
             if len(trozos) > 1 else trozos[0])
    # Remitía al PDF maestro como si estuviera al lado, y en el sobre de la
    # revista no va en suplementos/, donde viaja esta guía.
    sobre = _extendido_en_el_sobre()
    if sobre:
        donde = ("; en el sobre de la revista no va en suplementos/, sino en "
                 "%s/, como %s" % sobre)
    else:
        print("  AVISO: no se encuentra en build_jsr_submission.py cómo viaja "
              "el informe extendido en el sobre; la nota no lo dice")
        donde = ""
    return ("<b>Numeración.</b> Esta guía cita secciones y tablas con la "
            "numeración del informe extendido (el manuscrito maestro: "
            "manuscrito_revision_sistematica.pdf y manuscrito_es.docx en este "
            "paquete%s), que es de referencia y no el fichero de envío. El "
            "manuscrito que se envía a la revista (manuscrito_JSR_final.docx) no "
            "numera las secciones y numera las tablas de otro modo: allí %s. "
            "Donde la guía cita una sección o una tabla, da también su "
            "equivalente en el manuscrito de la revista." % (donde, lista))


def _s10_es_la_del_cuerpo():
    """S10 tiene que ser la comprobación sobre el cuerpo que describe la guía.

    Hasta el 2026-10-13 S10 era una copia del fichero del 13-ago-2026, anterior
    a esa comprobación y con 80 filas que no eran el corpus. La guía describe
    ahora la del cuerpo (quality_reports/idioma_cuerpo_pdf.csv), así que se
    niega a escribirse si S10 no tiene una fila por estudio comprobado."""
    hallados = sorted(OUT.glob("S10_*.csv"))
    if len(hallados) != 1:
        return  # la tabla lo dirá como NO ENCONTRADO
    with open(hallados[0], encoding="utf-8-sig", newline="") as fh:
        n = sum(1 for _ in csv.reader(fh)) - 1
    if n != _S["idioma_cuerpo_comprobados"]:
        raise SystemExit(
            "NO SE ESCRIBE LA GUÍA: %s tiene %d filas y la comprobación del "
            "idioma sobre el cuerpo (idioma_cuerpo_comprobados) cubre %d "
            "estudios. La guía lo describiría como lo que no es; rehaz S10 con "
            "build_verifiables_package.py." % (hallados[0].name, n,
                                                _S["idioma_cuerpo_comprobados"]))


def _enumera(nums):
    """[1, 2] -> «1 y 2»; [1..7] -> «1 a 7»; si hay huecos, los enumera."""
    nums = sorted(nums)
    if len(nums) == 1:
        return "%d" % nums[0]
    if len(nums) > 2 and nums == list(range(nums[0], nums[-1] + 1)):
        return "%d a %d" % (nums[0], nums[-1])
    return ", ".join("%d" % n for n in nums[:-1]) + " y %d" % nums[-1]


def _figuras_y_tablas():
    """Qué hay de verdad en «figuras y tablas», leído del disco.

    Decía «las cuatro tablas del manuscrito» con la cifra tecleada, y la
    carpeta trae siete tablas numeradas y la de criterios: se quedó vieja en
    cuanto el manuscrito ganó tablas, sin que nada fallara."""
    d = OUT / "figuras y tablas"
    if not d.is_dir():
        return "Figuras y tablas del manuscrito."

    def numeros(patron, comodin):
        ms = (re.match(patron, p.name) for p in d.glob(comodin))
        return [int(m.group(1)) for m in ms if m]

    figs = numeros(r"figura_(\d+)_", "figura_*.pdf")
    tabs = numeros(r"tabla_(\d+)_", "tabla_*.csv")
    partes = []
    if figs:
        partes.append(("Figura %s" if len(figs) == 1 else "Figuras %s")
                      % _enumera(figs) + " en PDF vectorial")
    if tabs:
        # «Del manuscrito» no decía de cuál: los ficheros llevan el número de
        # la tabla en el informe extendido (tabla_7_riesgo_sesgo), no en el de
        # la revista.
        partes.append(("la tabla %s" if len(tabs) == 1 else "las tablas %s")
                      % _enumera(tabs) + " del informe extendido en CSV, con "
                      "su numeración")
    texto = ", y ".join(partes) if partes else "Figuras y tablas del manuscrito"
    if list(d.glob("tabla_criterios*.csv")):
        texto += ", más la tabla de criterios de elegibilidad"
    return texto[0].upper() + texto[1:] + "."


# Qué es cada anexo y qué deja comprobar. El orden es el del paquete.
CATALOGO = [
    ("Manuscrito", [
        # Decía «El documento que se envía, en su forma final». No es el que se
        # envía (a la revista va manuscrito_JSR_final.docx) y «forma final» no
        # se sostiene mientras N.T. no haya aprobado por escrito la versión
        # final.
        ("manuscrito_revision_sistematica.pdf", "Manuscrito maestro (informe "
         "extendido) maquetado en español, con las citas numeradas y la lista "
         "de referencias.",
         "Informe extendido, de referencia; no es el fichero de envío. Es el "
         "que numera secciones y tablas, y su numeración es la que usa esta "
         "guía."),
        # Decía «La versión para revistas de habla inglesa», que la presentaba
        # como un fichero de envío; es la traducción del maestro y no va en el
        # sobre de la revista.
        ("manuscript_systematic_review_en.pdf", "El mismo, en inglés.",
         "La versión en inglés del informe extendido, de referencia; no es un "
         "fichero de envío."),
        # «Para las revistas que exigen .docx» invitaba a tomarlo por el fichero
        # que se sube, y la revista de destino pide Word: el que se sube es
        # manuscrito_JSR_final.docx.
        ("manuscrito_es.docx", "Manuscrito maestro en Word, español.",
         "La versión editable del informe extendido; tampoco es el fichero de "
         "envío."),
        ("manuscript_en.docx", "Manuscrito maestro en Word, inglés.",
         "Igual, en inglés."),
        # Decía «Informe editorial» sin decir quién lo escribió. Lo redactó el
        # modelo de lenguaje haciendo de editor de revista (docstring de
        # build_editorial_report.py), y así podía tomarse por la valoración de
        # una persona.
        # Por patrón: el nombre del fichero («informe editorial») está en
        # discusión y la guía no debe darlo por NO ENCONTRADO si cambia.
        ("S0_*.docx", "Evaluación previa del manuscrito que "
         "redactó el modelo de lenguaje en el papel de un editor de revista; no "
         "es una evaluación editorial externa.",
         "Si alguna decisión metodológica se tomó después de ver los resultados."),
    ]),
    # Se llamaba «Protocolo y reporte», y el paquete no lleva ningún protocolo.
    # S1 no da páginas: da el estado de cada ítem y la sección donde se cumple.
    ("Reporte y declaraciones", [
        ("S1_lista_PRISMA_2020.docx", "Lista PRISMA 2020, ítem por ítem, con su "
         "estado y la sección del informe extendido donde se cumple, y la "
         "equivalencia de esas secciones en el manuscrito de la revista.",
         "Si el reporte cumple PRISMA sin buscarlo a mano."),
        ("S7_declaraciones_ICMJE.docx", "Autoría según CRediT, conflictos de interés, "
         "financiación y uso de IA.", "Quién hizo qué y con qué financiación."),
    ]),
    ("Búsqueda", [
        # Prometía «con fecha» de cada búsqueda y no hay fecha por fuente: la
        # ejecución de Scopus cuya exportación entró al corpus no la tiene
        # registrada. «Ocho» iba además tecleado.
        ("S2_estrategias_de_busqueda.docx", "La cadena de búsqueda literal de cada "
         "una de las %d fuentes, con su número de registros."
         % _S["fuentes_distintas_n"],
         "Si la búsqueda es reproducible: se copia y se reejecuta."),
    ]),
    ("Cribado", [
        # «Con su motivo codificado» no vale para todas las filas: las del
        # primer día, y algunas de la etapa de resumen, van en texto libre. Y
        # no decía quién emitió las decisiones.
        # «Para cada registro» callaba que S3 lleva el cribado vigente: la
        # primera pasada del 4-ago-2026 sobre el brazo A de PubMed no está.
        ("S3_decisiones_etapa2_titulo.xlsx + .csv", "Decisión de cribado por título de "
         "cada registro en el cribado vigente, con su motivo, quién la emitió "
         "(el modelo de lenguaje, como revisor único) y su marca de tiempo. La "
         "primera pasada del 4 de agosto de 2026 sobre el brazo A de PubMed, "
         "que el cribado del pozo sustituyó, consta en el repositorio y no en S3.",
         "Por qué se excluyó cualquier registro concreto."),
        ("S3_decisiones_etapa3_resumen.xlsx + .csv", "Lo mismo en la lectura de resumen.",
         "Por qué un estudio no llegó a texto completo."),
        # Decía «40 estudios», tecleado: se fijaron 42 y la comprobación por
        # PMID alcanza a 40. Y no decía que el conjunto procede de una revisión
        # hecha con modelos de lenguaje ni que las ecuaciones se diseñaron para
        # recuperarlo, que es lo que limita lo que la auditoría puede afirmar.
        ("S6_auditoria_controles_positivos.docx", "Auditoría del cribado, tras "
         "cada etapa, contra los %d estudios fijados antes del cribado como "
         "elegibles conocidos, procedentes del metaanálisis exploratorio de julio "
         "de 2026, hecho con asistencia de modelos de lenguaje. La comprobación "
         "automática alcanza a los %d que tienen PMID."
         % (_S["controles_fijados"], _S["controles_comprobables_pmid"]),
         "Si el cribado perdió alguno de los controles comprobables. No mide la "
         "sensibilidad de la búsqueda: las ecuaciones se diseñaron para "
         "recuperarlos."),
    ]),
    ("Idioma", [
        ("S9_idioma_por_informe_y_clase_de_evidencia.xlsx + .csv", "Idioma de cada informe y "
         "clase de evidencia que aportaba.",
         "Qué se perdió al restringir a inglés y español."),
        # Decía «Verificación del idioma sobre el texto completo del PDF»
        # cuando S10 era una copia del 13-ago-2026, anterior a la comprobación
        # sobre el cuerpo de los estudios del corpus (6-oct-2026). S10 se rehace
        # ahora desde quality_reports/idioma_cuerpo_pdf.csv y se describe con
        # la misma frase que la lista de anexos; _s10_es_la_del_cuerpo() para
        # la guía si el fichero no es ese. Por patrón, por si cambia de nombre.
        ("S10_*.xlsx + .csv", s10(_S, False),
         "Si el idioma de cada estudio del corpus se comprobó sobre el cuerpo "
         "del artículo o se dio por bueno a partir de los metadatos."),
    ]),
    ("Corpus y recuperación", [
        ("S5_listado_*_estudios.xlsx + .csv", "Los estudios incluidos, con sus informes "
         "agrupados.", "Qué estudios componen el cuerpo de evidencia."),
        # Decía que todos llevan «la frase del artículo que lo sostiene» y que
        # «el texto completo desmintió» a todos. Los NOPDF salieron por no tener
        # el artículo, no porque el texto los desmintiera, y ni ellos ni los
        # NOREC tienen frase que citar.
        ("S16_excluidos_tras_leer_el_texto_completo.xlsx + .csv",
         "Los %d estudios que el cribado admitió y que salieron después, con su "
         "código de motivo y quién firmó la exclusión. %d llevan la cita en que "
         "se apoya; los %d sin el artículo completo (NOPDF) y los %d sin texto "
         "que se pudiera leer (NOREC) no tienen nada que citar%s"
         % (_S["estudios_excluidos_tras_texto_completo"], _S16["s16_con_cita"],
            _S["excluidos_texto_completo_NOPDF"],
            _S["excluidos_texto_completo_NOREC"],
            (", y %d más %s sin cita." % (_S16["s16_sin_cita_otros"],
                                          "van" if _S16["s16_sin_cita_otros"] > 1
                                          else "va"))
            if _S16["s16_sin_cita_otros"] else ".")
         # No todas las citas son del artículo: las de las fichas de registro
         # citan la ficha y la de EST-205, la indexación de SciELO.
         + de_las_citadas(_S16, False),
         "Por qué salió cada uno y, cuando hay cita, tenerla delante para poder "
         "discrepar (PRISMA 16b)."),
        # Decía «Qué se intentó para conseguir cada texto completo y con qué
        # resultado» y prometía mostrar «si el sesgo de recuperación se
        # documentó o se ocultó». S8 no es eso: es fulltext_identifiers.csv
        # (resolve_fulltext_ids.py, agosto de 2026), la vía resuelta para cada
        # informe sin DOI editorial, PMID ni NCT, sin los intentos de descarga
        # ni su resultado. Misma descripción que la lista de anexos.
        ("S8_recuperacion_texto_completo.xlsx + .csv", "Vía de recuperación "
         "resuelta en agosto de 2026 para cada informe que pasó a texto completo "
         "sin DOI editorial, PMID ni NCT: el identificador del registro o el "
         "código de protocolo, el DOI localizado, el ensayo ya identificado del "
         "que es informe o la cita por la que buscarlo.",
         # «Por qué vía se buscó» afirmaba una búsqueda que S8 no registra:
         # resolve_fulltext_ids.py deja escrito por dónde había que buscar
         # cada informe, no que se buscara ni con qué resultado.
         "Por qué vía había que buscar el texto de cada informe que no traía "
         "DOI editorial, PMID ni NCT. No registra los intentos de descarga ni "
         "su resultado: los estudios que se quedaron sin el artículo completo "
         "están en S16 (NOPDF)."),
        ("S20_de_que_informe_salio_cada_brazo.xlsx + .csv", "Cada brazo extraído con el "
         "informe del que salió, y con qué prueba se estableció el vínculo: el título "
         "localizado dentro del documento leído, el informe único del estudio o el único "
         "artículo del grupo.",
         "Dónde mirar para comprobar cualquier dato de cualquier brazo (PRISMA 10)."),
        ("S21_solapamiento_de_pacientes.xlsx + .csv", "Los %d pares de estudios que "
         "podían describir a los mismos pacientes, con la señal que los marcó, el "
         "veredicto tras leer los dos artículos, los pacientes compartidos y la frase "
         "firmada en que se apoya." % _S["pares_solapamiento_examinados"],
         "Si el corpus cuenta a algún paciente dos veces, y cuál."),
    ]),
    ("Extracción", [
        ("S4_pre_extraccion_desde_resumen.xlsx + .csv", "Pre-extracción desde el resumen, "
         "que emitió el modelo de lenguaje, marcada como parcial en cada registro.",
         "De dónde salen las cifras de estructura del corpus."),
        ("S22_completitud_resumen_frente_a_texto.xlsx + .csv", "Para cada variable de "
         "estratificación, cuántos estudios la declaran en el texto completo, cuántos la "
         "mencionan sin poder clasificarla, cuántos callan y de cuántos no hay texto.",
         "Separar la ausencia en el resumen de la ausencia en el estudio."),
        ("S23_clase_de_resistencia_comprobada.xlsx + .csv", "La clase de resistencia de "
         "los %d estudios que tenían texto completo, comprobada contra el antibiograma: la "
         "conclusión firmada, la frase o la tabla en que se apoya, cómo se codificó y qué "
         "cambió en la extracción." % _S["lectura_clase_estudios_leidos"],
         "Comprobar si un paciente es multirresistente sin fiarse de la etiqueta del autor."),
        ("S24_comparativos_reextraidos.xlsx + .csv", "Los %d estudios con diseño "
         "comparativo, reextraídos: comparador, asignación, tiempo cero, tiempo de "
         "evaluación, cointervenciones, pérdidas, estimando y si hay un contraste para "
         "P. aeruginosa." % _S["comparativos_reextraidos_leidos"],
         "Ver qué comparan de verdad los estudios que se llaman comparativos."),
        # «La Tabla 6» iba tecleada y sin decir de qué manuscrito.
        ("S17_tabla6_brazo_a_brazo.xlsx + .csv", "La Tabla %d del informe "
         "extendido desglosada (%s la Tabla %d en el manuscrito de la revista): "
         "los siete requisitos, brazo a brazo, con el primero que falla y por qué."
         % (_F["tabla_maestro"],
            "también" if _F["tabla_revista"] == _F["tabla_maestro"] else "es",
            _F["tabla_revista"]),
         "Comprobar el embudo de agregabilidad sin fiarse del recuento."),
        # «Qué verificaron los autores» repartía entre los dos un examen que,
        # según declara D.V. (8 de octubre de 2026), hizo D.V. y que no quedó
        # registrado.
        ("S19_cribado_con_modelo_de_lenguaje.docx", "Qué modelo emitió las decisiones de "
         "cribado, cuándo, sobre qué ficheros, qué examinó D.V., según su declaración, "
         "y qué no quedó registrado, marcado como dato faltante.",
         "Juzgar el procedimiento de cribado, incluido lo que no se puede reconstruir."),
        # Nombraba «S18_evidencia_por_dominio», que no existe: la guía lo daba
        # por NO ENCONTRADO y listaba el S18 real como fichero sin describir.
        # Decía además que cada juicio tiene «la frase del artículo en que se
        # apoya», y en algunos el cuaderno no registra apoyo alguno.
        ("S18_cada_juicio_con_su_frase.xlsx + .csv", "Cada uno de los %d juicios "
         "de riesgo de sesgo, con lo que lo sostiene en el cuaderno firmado: una "
         "cita literal en %d, una nota sin cita en %d y nada en %d, marcados como "
         "dato faltante."
         % (_S["celdas_tabla5"], _S["citas_literales"], _S["notas_del_revisor"],
            _S["juicios_sin_frase"]),
         "Discrepar de un juicio concreto teniendo delante lo que lo sostiene, o "
         "ver que no consta nada."),
        # S18b no estaba descrito: salía como fichero huérfano.
        ("S18b_frases_cosechadas_por_tema.xlsx + .csv", "Las frases de cada "
         "artículo que el modelo de lenguaje localizó de forma automática para "
         "cada dominio de riesgo de sesgo, y que puso como comentario en las "
         "casillas de los formularios.",
         "Qué tenían delante los revisores al juzgar cada dominio. Acompañan a "
         "los juicios; lo que sostiene cada uno está en S18."),
        # Decía «en todas las filas», sin cifra: son las filas comparables, y el
        # recuento sale del escalar.
        ("S11_concordancia_entre_extractores.pdf", "Concordancia entre las dos "
         "extracciones, variable a variable, antes de resolver nada. Su "
         "independencia no está acreditada: una columna de texto libre coincide "
         "carácter por carácter entre los dos cuadernos en %d de las %d filas "
         "comparables, erratas incluidas."
         % (_S["extraccion_localizacion_identicas"],
            _S["extraccion_localizacion_comparables"]),
         "Cuánto coinciden los dos cuadernos, y por qué no mide dos lecturas "
         "independientes."),
        # Hablaba de desacuerdos «pendientes de conseguirlo» cuando ya no queda
        # ninguno, y no decía quién adjudicó. «Según el registro»: lo comprobado
        # es el responsable que anota resuelto_por, no cómo se tomó la decisión.
        ("S12_resolucion_de_conflictos.pdf", "Cómo se cerraron los %d "
         "desacuerdos: adjudicados, según el registro, por los dos revisores (%d) "
         "o por uno solo (%d), o cerrados por una regla mecánica, sin firma "
         "conjunta (%d)%s"
         % (_S["extraccion_desacuerdos"], _S["conflictos_resueltos_por_los_dos"],
            _S["conflictos_resueltos_por_uno"], _S["extraccion_cerrados_por_regla"],
            "; %d siguen sin adjudicar." % _PENDIENTES if _PENDIENTES else "."),
         "Si los desacuerdos se adjudicaron o se taparon, y quién los adjudicó "
         "según el registro."),
        # «Tras resolver los desacuerdos por consenso» y «la resolvieron por
        # consenso» eran falsos: el registro anota a los dos revisores solo en
        # una parte de los desacuerdos y a uno solo en el resto. Las etiquetas
        # son las de S15 tras separar quién adjudicó.
        # «La sección 3.5 y las tablas 5 y 6» eran del maestro, tecleadas, y en
        # el manuscrito de la revista la de desenlaces es otra tabla.
        ("S14_extraccion_adjudicada.csv", "La extracción definitiva: un valor por "
         "casilla, brazo a brazo, tras la adjudicación de los desacuerdos.",
         "Toda cifra de la sección %s y de las tablas %d y %d del informe "
         "extendido (en el manuscrito de la revista, %s y las tablas %d y %d)."
         % (_D["seccion_maestro"], _D["tabla_maestro"], _F["tabla_maestro"],
            _apartado("desenlaces"), _D["tabla_revista"], _F["tabla_revista"])),
        ("S15_procedencia_de_cada_casilla.csv", "Para cada casilla de S14, de "
         "dónde sale su valor: acuerdo, adjudicada por los dos, adjudicada por "
         "uno, corregida contra el texto, una sola lectura o abierta.",
         "Cuánta doble lectura hay detrás de cada cifra, y cuántas casillas "
         "adjudicó, según el registro, una sola persona."),
        # No decía quién las redactó; la lista de anexos sí. Misma redacción.
        ("S13_reglas_de_extraccion_de_desenlaces.pdf", "Definición de erradicación "
         "microbiológica y de éxito clínico, con su corrección documentada. Las "
         "redactó el modelo de lenguaje; según declara D.V., las decidieron los "
         "dos autores, y el registro del 12 de agosto de 2026 las dejó como "
         "propuesta sin ratificar.",
         "Si la definición de desenlace cambió, cuándo y por qué."),
    ]),
    ("Figuras y tablas", [
        ("figuras y tablas", _figuras_y_tablas(),
         "Los datos exactos que hay detrás de cada figura y de cada tabla."),
    ]),
]

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass


def tamano(p):
    if p.is_dir():
        return f"{sum(1 for _ in p.iterdir())} ficheros"
    kb = p.stat().st_size / 1024
    if p.suffix == ".csv":
        try:
            n = sum(1 for _ in csv.reader(open(p, encoding="utf-8-sig"))) - 1
            return f"{n:,} filas".replace(",", " ")
        except Exception:
            pass
    return f"{kb:,.0f} KB".replace(",", " ")


def main():
    st = estilos()
    S = json.loads((ROOT / "quality_reports" / "synthesis_scalars.json")
                   .read_text(encoding="utf-8"))
    dest = OUT / "00_GUIA_DEL_MATERIAL_SUPLEMENTARIO.pdf"
    _s10_es_la_del_cuerpo()

    c = [Paragraph("Guía del material suplementario", st["titulo"])]
    c.append(Paragraph(
        "Fagoterapia en infecciones por <i>Pseudomonas aeruginosa</i> multirresistente: "
        "revisión sistemática de la literatura clínica y la completitud de su reporte",
        st["autores"]))
    c.append(Spacer(1, 10))
    # Decía «el rastro completo», y no lo es: S19 señala lo que no quedó
    # registrado (el examen que declara D.V. de lo que superó el cribado).
    # Tampoco todo lo registrado viaja: la primera pasada del cribado (4-ago-
    # 2026, brazo A de PubMed), que el cribado del pozo sustituyó, está en el
    # repositorio y no en S3. Se dice en vez de dar el paquete por el rastro
    # entero.
    c.append(Paragraph(
        "Este paquete contiene el rastro registrado de la revisión vigente: qué se "
        "buscó, qué se excluyó y por qué, qué no se pudo conseguir, y en qué no "
        "coincidieron los dos revisores; lo que no quedó registrado se señala como "
        "tal (S19), y lo que se sustituyó y no viaja, como la primera pasada del "
        "cribado, se indica donde corresponde (S3). Está "
        "ordenado por la etapa que documenta. Cada entrada dice qué contiene el "
        "fichero y qué pregunta permite contestar, para que no haga falta abrirlos "
        "todos.", st["cuerpo"]))
    # La guía viaja con el manuscrito de la revista y cita la numeración del
    # maestro: lo dice al principio, con la equivalencia leída de los dos.
    c.append(Paragraph(_nota_numeracion(), st["cuerpo"]))
    # Decía «ningún dato se transcribió a mano», y la extracción y los juicios
    # de riesgo de sesgo los emitieron los autores en sus cuadernos (así lo dice
    # la declaración de uso de IA). Y no decía quién escribió el canal. La
    # versión siguiente, «Ninguna cifra de este paquete se copió a mano», seguía
    # sin sostenerse: los valores de los cuadernos de extracción (pacientes,
    # éxitos, eventos) son cifras que se pasaron a mano desde los artículos. Lo
    # que no se teclea son los recuentos y porcentajes que el canal calcula.
    c.append(Paragraph(
        "Los ficheros en <b>CSV</b> son datos, pensados para abrirse en una hoja de "
        "cálculo y filtrarse; los que están en <b>PDF</b> o <b>Word</b> son documentos "
        "para leer. Ningún recuento ni porcentaje de este paquete se tecleó al "
        "escribirlo: los calcula, a partir de los registros de decisión y de los "
        "cuadernos de extracción y de riesgo de sesgo, el canal de código que "
        "escribió y ejecutó el modelo de lenguaje, el mismo que produce las cifras "
        "del manuscrito, y se regeneran reejecutándolo.", st["nota"]))

    descritos = set()
    for seccion, entradas in CATALOGO:
        filas = []
        for nombre, que_es, para_que in entradas:
            # Un anexo de datos son DOS ficheros: el .xlsx que se lee y el .csv
            # reproducible. La entrada los nombra juntos, asi que hay que
            # resolver los dos y marcar los dos como descritos; si no, la
            # comprobacion de cobertura los da por huerfanos y la guia acaba
            # avisando de que no describe ficheros que si describe.
            partes = [x.strip() for x in nombre.split("+")]
            # Un anexo cuyo nombre lleva el recuento dentro --S5-- cambia de
            # nombre cada vez que cambia el corpus. Teclearlo aqui es la misma
            # trampa que el propio S5 evita calculandolo: se resuelve por
            # patron, y si no aparece ninguno la guia lo dira como NO ENCONTRADO.
            # Vale igual para S0 y S10, que se resuelven por patrón. Si falta
            # el .xlsx pero está el .csv (el .xlsx lo escribe después
            # build_readable_annexes.py), la raíz se toma del .csv: así la guía
            # dice cuál falta en vez de dar el .csv por huérfano.
            if "*" in partes[0]:
                patron = partes[0]
                raiz_patron, ext = patron.rsplit(".", 1)
                hallados = sorted(OUT.glob(patron)) or sorted(
                    p for x in partes[1:] if x.startswith(".")
                    for p in OUT.glob(raiz_patron + x))
                if hallados:
                    partes[0] = hallados[0].stem + "." + ext
                    nombre = nombre.replace(raiz_patron, hallados[0].stem)
            raiz = partes[0].rsplit(".", 1)[0]
            reales = []
            for x in partes:
                # "S3_algo.xlsx" ya es un nombre; ".csv" es solo la extension
                # del mismo anexo y hay que pegarla a la raiz.
                reales.append(x if not x.startswith(".") else raiz + x)
            for x in reales:
                descritos.add(x)
            faltan = [x for x in reales if not (OUT / x).exists()]
            if faltan:
                filas.append([f"<b>{nombre}</b>", "NO ENCONTRADO: %s" % ", ".join(faltan),
                              "—", "—"])
                continue
            tam = tamano(OUT / reales[0])
            filas.append([nombre, que_es, para_que, tam])
        c.append(Paragraph(seccion, st["h1"]))
        c.append(cuadro(st, filas,
                        ["Fichero", "Qué contiene", "Qué permite comprobar", "Tamaño"],
                        [4.6 * cm, 4.6 * cm, ANCHO - 12.0 * cm, 2.8 * cm]))

    huerfanos = sorted(p.name for p in OUT.iterdir()
                       if p.name not in descritos
                       and not p.name.startswith("00_")
                       and p.suffix.lower() in (".csv", ".pdf", ".docx"))
    if huerfanos:
        c.append(Paragraph("Ficheros del paquete que esta guía no describe", st["h1"]))
        c.append(Paragraph(
            "Aparecen aquí para que la guía no dé por completo lo que no lo está: "
            + ", ".join(huerfanos) + ".", st["nota"]))

    c.append(Paragraph("Advertencia sobre el alcance de esta revisión", st["h1"]))
    # DECÍA «Lo que no ha concluido es la adjudicación por consenso de los
    # desacuerdos: 0 de los 541 siguen sin firmar. Por eso este informe no
    # presenta estimaciones de eficacia, ni riesgo de sesgo, ni certeza GRADE
    # [...] y ninguna cifra publicada depende de los cuadernos de extracción».
    # Era falso entero: con 0 pendientes la adjudicación SÍ ha concluido; no fue
    # «por consenso» (el registro anota a los dos revisores solo en una parte y
    # a uno solo en el resto); el manuscrito SÍ presenta riesgo de sesgo (sección
    # 3.7, tabla 7), y la sección 3.5 y las tablas 5 y 6 salen de la extracción
    # adjudicada, que es la fusión de los dos cuadernos. Ahora hay dos
    # redacciones, según queden o no desacuerdos sin adjudicar, y todas las
    # cifras salen de los escalares. Del riesgo de sesgo, lo que sale de la
    # extracción adjudicada es el DISEÑO que decide qué estudios se evalúan
    # (make_rob_forms.py lee study_design de extraccion_adjudicada.csv); los
    # juicios se emitieron en cuadernos propios (sección 2.7), y así se dice:
    # escribir que «salen de la extracción» sería atribuirles otro origen.
    e = {"ambos": S["extraccion_estudios_ambos"], "r1": S["extraccion_estudios_r1"],
         "loc_id": S["extraccion_localizacion_identicas"],
         "loc_comp": S["extraccion_localizacion_comparables"],
         "desac": S["extraccion_desacuerdos"],
         "adj": S["extraccion_conflictos_firmados"],
         "dos": S["conflictos_resueltos_por_los_dos"],
         "uno": S["conflictos_resueltos_por_uno"],
         "regla": S["extraccion_cerrados_por_regla"],
         "pend": S["extraccion_conflictos_sin_firmar"],
         "rob": S["celdas_tabla5"], "ev": S["rob_estudios_evaluables"],
         "rob2": S["rob_estudios_con_dos_lecturas"],
         "rob1": S["rob_estudios_con_una_lectura"],
         "rob_des": S["rob_desacuerdos"], "rob_dv": S["rob_resueltos_hacia_r1"]}
    # Si las partes no suman el todo, la advertencia diría algo que no cuadra.
    # Mejor no escribirla.
    if (e["adj"] + e["regla"] + e["pend"] != e["desac"]
            or e["dos"] + e["uno"] != e["adj"]
            or e["rob2"] + e["rob1"] != e["ev"]):
        raise SystemExit("NO SE ESCRIBE LA GUÍA: los escalares de adjudicación o "
                         "de riesgo de sesgo no suman: %r" % e)
    indep = ("sin independencia acreditada: la columna de texto libre que localiza "
             "cada dato coincide carácter por carácter entre los dos cuadernos en "
             "%(loc_id)d de las %(loc_comp)d filas comparables (S11)" % e)
    if e["pend"]:
        p1 = ("La extracción por duplicado <b>está completa</b>: los dos revisores "
              "extrajeron %(ambos)d de los %(r1)d estudios, " % e + indep
              + ". Lo que <b>no ha concluido</b> es la adjudicación de los "
              "desacuerdos: de los %(desac)d, %(pend)d siguen sin adjudicar, y esas "
              "casillas salen vacías de la extracción adjudicada (S14) y figuran "
              "como abiertas en S15; no se rellenan con una conjetura. De los "
              "%(adj)d adjudicados, el registro anota a los dos revisores en "
              "%(dos)d, los únicos que constan como consenso, y a uno solo en "
              "%(uno)d; %(regla)d se cerraron por una regla mecánica, sin firma "
              "conjunta (S12)." % e)
    else:
        p1 = ("La extracción por duplicado y la adjudicación de sus desacuerdos "
              "<b>están cerradas</b>. Los dos revisores extrajeron %(ambos)d de los "
              "%(r1)d estudios, " % e + indep
              + ". De los %(desac)d desacuerdos, %(adj)d están adjudicados: el "
              "registro anota a los dos revisores en %(dos)d, los únicos que "
              "constan como consenso, y a uno solo en %(uno)d. Los %(regla)d "
              "restantes se cerraron por una regla mecánica, sin firma conjunta "
              "(S12)." % e)
    c.append(Paragraph(p1, st["cuerpo"]))
    una = ("" if not e["rob1"] else
           " El estudio restante tiene una sola lectura." if e["rob1"] == 1 else
           " Los %(rob1)d restantes tienen una sola lectura." % e)
    # «La sección 3.5 y las tablas 5 y 6», «la sección 3.7 y la tabla 7» y
    # «(sección 3.6)» iban tecleadas con la numeración del maestro; leídas
    # junto al manuscrito de la revista mandaban a tablas equivocadas.
    c.append(Paragraph(
        "De esa extracción adjudicada (S14) salen la sección %s y las tablas %d "
        "y %d del informe extendido (en el manuscrito de la revista, %s y las "
        "tablas %d y %d), y el diseño que decide qué estudios se evalúan en "
        "riesgo de sesgo%s. Los %d juicios de riesgo de sesgo (S18; sección %s "
        "y tabla %d del informe extendido, y en la revista, %s y la Tabla %d) "
        "se emitieron en cuadernos aparte: en %d de los %d estudios "
        "evaluables hubo dos, uno a nombre de cada autor, cuya independencia "
        "tampoco está acreditada, y se cerraron en un cuaderno de consenso que el "
        "modelo de lenguaje generó con los juicios coincidentes precargados y que "
        "firmaron los dos autores; de los %d juicios en que los dos cuadernos "
        "discrepaban, %s se resolvieron hacia el de D.V.%s"
        % (_D["seccion_maestro"], _D["tabla_maestro"], _F["tabla_maestro"],
           _apartado("desenlaces"), _D["tabla_revista"], _F["tabla_revista"],
           ", de modo que esas cifras pueden cambiar cuando se adjudique lo "
           "pendiente" if e["pend"] else "",
           e["rob"], _R["seccion_maestro"], _R["tabla_maestro"],
           _apartado("riesgo"), _R["tabla_revista"],
           e["rob2"], e["ev"], e["rob_des"],
           "los %d" % e["rob_dv"] if e["rob_dv"] == e["rob_des"] else
           "%d" % e["rob_dv"], una),
        st["cuerpo"]))
    c.append(Paragraph(
        "GRADE no se aplica: califica la certeza de una estimación agrupada, y el "
        "manuscrito no presenta ninguna (sección %s del informe extendido; en la "
        "revista, %s)." % (_F["seccion_maestro"], _apartado("embudo")),
        st["cuerpo"]))
    # Decía que S11 a S13 muestran «qué estudios no se pueden adjudicar todavía
    # porque no se ha conseguido su texto completo»: hoy no queda ninguno.
    c.append(Paragraph(
        "Los anexos S11 a S15 documentan ese proceso sin suavizarlo: cuánto "
        "coincidían los dos cuadernos antes de resolver nada y por qué esa "
        "concordancia no mide dos lecturas independientes (S11), cómo se cerraron "
        "los desacuerdos%s (S12), las reglas de desenlace (S13), el valor final "
        "de cada casilla (S14) y de dónde sale (S15).%s"
        % ((", quién los adjudicó según el registro y cuáles siguen sin adjudicar",
            " Se incluyen porque el estado real de una adjudicación en marcha es "
            "información que el lector necesita, y no algo que deba esperar a "
            "estar resuelto para poder auditarse.")
           if e["pend"] else (" y quién los adjudicó según el registro", "")),
        st["cuerpo"]))

    documento(dest, "Guía del material suplementario").build(c)
    print(f"  {dest.name:52} {dest.stat().st_size // 1024} KB")
    if huerfanos:
        print(f"  aviso: {len(huerfanos)} ficheros sin describir -> {huerfanos}")


if __name__ == "__main__":
    main()
