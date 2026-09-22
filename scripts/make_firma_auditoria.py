# -*- coding: utf-8 -*-
"""Los seis hallazgos de la auditoría del 2026-09-16 que hay que firmar.

POR QUE UN CUADERNO. Los seis tocan datos ya firmados --la evaluación de
riesgo de sesgo y la extracción adjudicada-- y ninguno lo puede corregir un
script: son juicios de los autores. Aquí va cada uno con la prueba literal
delante, la pregunta concreta y la casilla para la respuesta.

LOS SEIS

  1. EST-021. El juicio global es «Bajo riesgo de sesgo» y su dominio 2 es
     «Algunas preocupaciones». RoB 2 no permite esa combinación: bajo riesgo
     global exige bajo riesgo en TODOS los dominios. Los otros once estudios
     sí heredan su peor dominio.
  2. EST-003. Su definición de éxito clínico habla del ensayo BX004-A contra
     placebo, y BX004-A no aparece en ninguna parte del artículo de EST-003,
     que es la serie compasiva de PASA16. La definición parece de otro estudio.
  3. EST-003 y EST-077. El caso 3 de EST-077 --niña de 10 años, Berlin Heart
     EXCOR, bacteriemia por P. aeruginosa, PASA16, Israel-- coincide en edad,
     sexo, dispositivo, organismo, fago y país con el caso 3 de la Tabla 4 de
     EST-003. Parece el mismo paciente en dos estudios del corpus.
  4. EST-077. `adverse_event_n` vale 5 y en el texto completo no aparece
     «adverse», ni «side effect», ni «tolerability». Además el artículo dice
     cuatro pacientes y cinco ciclos de tratamiento: puede que el 5 sean los
     ciclos y no los eventos.
  5. EST-063 es un protocolo de BMJ Open --71 «will be», sin resultados-- y los
     otros cuatro protocolos del corpus se excluyeron con el codigo PRO.
  6. Siete de los quince estudios «con grupo de comparacion» no tienen ninguno,
     segun vuestras propias notas del dominio 1.

SALIDA
    ~/Escritorio/FIRMAR_auditoria_2026-09-16.xlsx
"""
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
CUADERNO = pathlib.Path.home() / "Desktop" / "FIRMAR_auditoria_2026-09-16.xlsx"

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

HALLAZGOS = [
    dict(
        clave="EST-021-GLOBAL",
        titulo="EST-021 (PhagoBurn): el juicio global no cuadra con sus dominios",
        que_hay=[
            "D1 proceso de aleatorización ........ Bajo riesgo de sesgo",
            "D2 desviaciones de la intervención .. Algunas preocupaciones",
            "D3 datos de desenlace faltantes ..... Bajo riesgo de sesgo",
            "D4 medición del desenlace ........... Bajo riesgo de sesgo",
            "D5 selección del resultado .......... Bajo riesgo de sesgo",
            "GLOBAL .............................. Bajo riesgo de sesgo",
        ],
        problema=(
            "RoB 2 establece que el juicio global es «bajo riesgo» solo si TODOS los "
            "dominios son de bajo riesgo. Con un dominio en «algunas preocupaciones», "
            "el global no puede ser «bajo riesgo». Los otros once estudios evaluados "
            "sí heredan su peor dominio, de modo que EST-021 es la única excepción."),
        pregunta="¿Qué hacemos con el juicio global de EST-021?",
        opciones=[
            "Corregirlo a «Algunas preocupaciones» (lo que da la regla del instrumento)",
            "Mantener «Bajo riesgo de sesgo» y declarar en Métodos por qué nos apartamos",
        ],
        efecto=("Si se corrige: la frase de Resultados pasa de «bajo riesgo en 2 y algunas "
                "preocupaciones en 1» a «bajo riesgo en 1 y algunas preocupaciones en 2». "
                "No cambia ninguna conclusión."),
    ),
    dict(
        clave="EST-003-DEFINICION",
        titulo="EST-003 (PASA16): la definición de éxito parece de otro estudio",
        que_hay=[
            "clinical_success_definition de los cinco brazos de EST-003:",
            "  «Significant reductions of P. aeruginosa colony forming units (CFU) in",
            "   sputum occurred in the treatment arm compared to placebo, on days 4",
            "   ... of the BX004-A phage cocktail.»",
            "",
            "Comprobado sobre el texto completo de EST-003 (Onallah et al., Med 2023,",
            "serie compasiva de PASA16):",
            "  «BX004» no aparece ninguna vez.",
            "  esa frase no aparece ninguna vez.",
            "BX004-A es el producto de EST-008, que sí lo nombra.",
            "",
            "Lo que EST-003 sí dice de sus desenlaces:",
            "  «Good clinical outcome was documented in 13 out of 15 patients (86.6%).",
            "   Two clinical failures were reported.»",
            "  «Clinical recovery appeared to take place in six cases, and remission was",
            "   seen in an additional seven patients.»",
        ],
        problema=(
            "La definición atribuida a EST-003 no está en EST-003. Además "
            "`clinical_success_n` vale 13 en el brazo A, cuyo `n_arm` es 1: el 13 es el "
            "numerador de la serie entera (13 de 15), no el del brazo."),
        pregunta="¿Cómo se corrige la extracción de EST-003?",
        opciones=[
            "Sustituir la definición por la frase propia del artículo y poner el numerador del brazo A en NA",
            "Dejarlo como está y señalarlo en el manuscrito como error de reporte",
            "Otra cosa: descríbela en la casilla de al lado",
        ],
        efecto=("La Tabla 4 ya declara los dos numeradores imposibles. Si se corrige, el "
                "brazo A de EST-003 deja de contarse entre ellos y la Tabla 6 gana un brazo "
                "en el filtro de numerador."),
    ),
    dict(
        clave="SOLAPAMIENTO-003-077",
        titulo="El mismo paciente en EST-003 y en EST-077",
        que_hay=[
            "EST-077 (Aslam et al., Antimicrob Agents Chemother 2024), caso 3:",
            "  «A 10-year-old female with a genetic cardiomyopathy was admitted with",
            "   cardiogenic shock and underwent placement of a Berlin Heart Excor VAD",
            "   in January 2019... she developed recurrent and almost persistent",
            "   P. aeruginosa bacteremia attributed to endovascular LVAD infection.»",
            "  «Two patients (Cases 3, 4) were treated at the Schnieder Children's",
            "   Hospital (Petach Tikva, Israel) and Sheba Medical Center...»",
            "  «PASA16 (used in Cases 3 and 4)»",
            "",
            "EST-003 (Onallah et al., Med 2023), Tabla 4, caso 3:",
            "  «3 bacteremia 10/F prostheticdevice MDR i.v.,49days BID ... meropenem",
            "   ... elevated LFT >=2ULN, high fever, deceased, failure, 2 months",
            "   ... prosthetic device infection (Berlin heart EXCOR)»",
            "",
            "Coinciden edad, sexo, dispositivo, organismo, fago y país.",
            "EST-077 cita a EST-003 en su lista de referencias (ref. 19).",
        ],
        problema=(
            "Si es el mismo paciente, está contado dos veces en el corpus. La revisión no "
            "publica ninguna estimación agrupada, de modo que no sesga ningún resultado "
            "numérico, pero el corpus no puede presentarse como 137 estudios de pacientes "
            "distintos sin decirlo."),
        pregunta="¿Es el mismo paciente y qué se hace?",
        opciones=[
            "Sí es el mismo: se declara el solapamiento en Resultados y en Limitaciones, y los dos estudios se mantienen",
            "Sí es el mismo: además se marca el brazo de uno de los dos para no contarlo dos veces",
            "No es el mismo: explicad por qué en la casilla de al lado",
            "No se puede decidir con lo que dicen los dos artículos",
        ],
        efecto=("El corpus sigue en 137 estudios en cualquier caso: son dos publicaciones "
                "distintas. Lo que cambia es lo que se puede afirmar sobre pacientes."),
    ),
    dict(
        clave="EST-077-EVENTOS",
        titulo="EST-077: cinco eventos adversos que el artículo no menciona",
        que_hay=[
            "En la extracción adjudicada: adverse_event_n = 5, n_arm = 4.",
            "",
            "En el texto completo de EST-077, buscado entero:",
            "  «adverse» ............ 0 veces",
            "  «side effect» ........ 0 veces",
            "  «tolerability» ....... 0 veces",
            "",
            "Lo que el artículo sí dice:",
            "  «We performed a retrospective review of four patients that underwent",
            "   five separate courses of intravenous (IV) phage therapy»",
            "  «Breakthrough bacteremia occurred frequently (while the organism remained",
            "   susceptible to administered phage) and is an important safety",
            "   consideration.»",
        ],
        problema=(
            "El 5 puede ser el número de CICLOS de tratamiento, no de eventos adversos. "
            "Si lo es, no hay cinco eventos sobre cuatro pacientes: hay cuatro pacientes y "
            "cinco ciclos, y la unidad de análisis del campo está sin declarar."),
        pregunta="¿Qué cuenta realmente adverse_event_n en EST-077?",
        opciones=[
            "Son ciclos de tratamiento, no eventos: el campo se pone en NA",
            "Son eventos adversos contados por episodio y no por paciente: se mantiene y se declara la unidad",
            "Otra cosa: descríbela en la casilla de al lado",
        ],
        efecto=("La Tabla 4 declara hoy «cinco eventos adversos sobre cuatro» como error de "
                "reporte. Según lo que decidáis, esa frase cambia o desaparece."),
    ),
    dict(
        clave="EST-063-PROTOCOLO",
        titulo="EST-063 es un protocolo, y los protocolos se excluyeron",
        que_hay=[
            "EST-063: Singh J et al. «Single-arm, open-labelled, safety and tolerability of",
            "intrabronchial and nebulised bacteriophage treatment in children with cystic",
            "fibrosis and Pseudomonas aeruginosa». BMJ Open Respir Res 2023.",
            "",
            "Su estructura es la de un protocolo de BMJ Open:",
            "  INTRODUCTION / METHODS AND ANALYSIS / Ethics and dissemination",
            "  «This trial is designed as a small, pilot, single-arm, open-label...»",
            "  «Results will be transcribed onto a data collection sheet...»",
            "",
            "El criterio que vosotros mismos usasteis para los cuatro protocolos que SÍ",
            "excluisteis fue contar «will be»:",
            "  EST-035  99 veces  -> excluido PRO",
            "  EST-052 223 veces  -> excluido PRO",
            "  EST-122  80 veces  -> excluido PRO",
            "  EST-083       —     -> excluido PRO",
            "  EST-063  71 veces  -> EN EL CORPUS",
            "",
            "Y vuestra propia nota de riesgo de sesgo, dominio 5, dice:",
            "  «Es un protocolo; aún no hay resultados.»",
        ],
        problema=(
            "Un protocolo no tiene desenlaces, de modo que se le está evaluando el sesgo "
            "por datos faltantes y por medición de desenlaces que no existen. Si se aplica "
            "el mismo criterio que a los otros cuatro, EST-063 se excluye con el código "
            "PRO."),
        pregunta="¿Se excluye EST-063 con el código PRO?",
        opciones=[
            "Sí: se excluye como protocolo; PRO pasa de 4 a 5 exclusiones",
            "No: se mantiene y se explica en Métodos por qué este protocolo sí entra",
            "Otra cosa: descríbela en la casilla de al lado",
        ],
        efecto=("Si se excluye, se mueven: corpus 137 -> 136; recuperables 95 -> 94; con "
                "texto 71 -> 70; brazos 103 -> 102; comparativos 15 -> 14; evaluables "
                "12 -> 11; juicios 90 -> 82; exclusiones 46 -> 47. Es la corrección de "
                "mayor alcance de esta auditoría."),
    ),
    dict(
        clave="COMPARATIVOS-SIN-CONTROL",
        titulo="Siete de los quince «comparativos» no tienen grupo de comparación",
        que_hay=[
            "Vuestras propias notas del dominio 1, firmadas, dicen:",
            "",
            "  EST-004  «there was no control group for comparison»",
            "  EST-063  «Sin grupo comparador (diseño de un solo brazo).»",
            "  EST-070  «Sin grupo control.»",
            "  EST-096  «Sin grupo control. Imposible separar el efecto del fago.»",
            "  EST-116  «No se evalúa un efecto de tratamiento comparativo.»",
            "  EST-146  «Sin grupo control + antibióticos concomitantes frecuentes.»",
            "  EST-152  «Sin grupo control. No se puede separar el efecto del fago.»",
            "",
            "Con grupo de comparación real, cinco:",
            "  EST-008  BX004-A frente a placebo",
            "  EST-021  PP1131 frente a cuidado estándar",
            "  EST-132  terapia convencional frente a convencional + fago",
            "  EST-055  grupo IV recibe furazidina y cefixima SIN bacteriófago",
            "  EST-108  compara con y sin antibiótico concomitante, dentro de los",
            "           tratados con fago; no compara fago contra no fago",
            "",
            "Sin texto completo, tres: EST-029, EST-157, EST-165. No se sabe.",
        ],
        problema=(
            "El manuscrito dice «15 estudios con grupo de comparación». La etiqueta sale "
            "del diseño adjudicado —una cohorte cuenta como comparativa— y vuestras notas "
            "la contradicen en 7 de los 12 que leísteis. La clasificación sirve para "
            "escoger el instrumento de riesgo de sesgo; no para afirmar que hay un "
            "comparador."),
        pregunta="¿Cómo se nombra esto en el manuscrito?",
        opciones=[
            "Mantener los 15 como «clasificados por diseño» y añadir la cifra de los que tienen comparador real",
            "Cambiar la frase a «15 estudios con diseño comparativo, de los cuales 5 con grupo de comparación»",
            "Otra cosa: descríbela en la casilla de al lado",
        ],
        efecto=("No mueve ninguna cifra del embudo ni del riesgo de sesgo. Cambia lo que "
                "el manuscrito AFIRMA sobre esos 15, que hoy es más de lo que las notas "
                "sostienen."),
    ),
]


def main():
    from openpyxl import Workbook
    from openpyxl.styles import Alignment, Font, PatternFill
    from openpyxl.worksheet.datavalidation import DataValidation

    negrita = Font(bold=True)
    grande = Font(bold=True, size=13)
    mono = Font(name="Consolas", size=9)
    cab = PatternFill("solid", fgColor="D9E1F2")
    ojo = PatternFill("solid", fgColor="FCE4D6")
    arriba = Alignment(vertical="top", wrap_text=True)

    wb = Workbook()
    h = wb.active
    h.title = "Empieza aqui"
    h.column_dimensions["A"].width = 106
    texto = [
        ("Seis cosas que encontró la auditoría y que no puede decidir un script", True),
        ("", False),
        ("Ninguna de las cuatro es de estilo. Las cuatro tocan datos que ya firmasteis, y", False),
        ("las cuatro cambian algo de lo que el manuscrito dice. Por eso vienen aquí y no", False),
        ("resueltas: corregir una extracción firmada o un juicio firmado es vuestro.", False),
        ("", False),
        ("  1. EST-021   el juicio global contradice la regla de RoB 2", False),
        ("  2. EST-003   la definición de éxito parece copiada de otro estudio", False),
        ("  3. EST-003 y EST-077   parece el mismo paciente en los dos", False),
        ("  4. EST-077   cinco eventos adversos que el artículo no menciona", False),
        ("  5. EST-063   es un protocolo, y los protocolos se excluyeron", False),
        ("  6. los 15    siete de ellos no tienen grupo de comparación", False),
        ("", False),
        ("Cada hoja trae la prueba literal, la pregunta y las opciones. Escoged una del", False),
        ("desplegable y, si hace falta, explicad en «por qué». Sin las dos firmas de la", False),
        ("última hoja no se ingiere nada.", False),
        ("", False),
        ("Mientras estas seis sigan sin firmar, el manuscrito lleva un aviso de", True),
        ("PENDIENTE en la sección de riesgo de sesgo y el sobre no se puede enviar.", True),
    ]
    for i, (t, b) in enumerate(texto, start=1):
        c = h.cell(row=i, column=1, value=t)
        if b:
            c.font = negrita

    for k, d in enumerate(HALLAZGOS, start=1):
        s = wb.create_sheet("%d. %s" % (k, d["clave"][:25]))
        s.column_dimensions["A"].width = 22
        s.column_dimensions["B"].width = 96
        s.cell(row=1, column=1, value=d["titulo"]).font = grande
        f = 3
        s.cell(row=f, column=1, value="Lo que hay").font = negrita
        for linea in d["que_hay"]:
            s.cell(row=f, column=2, value=linea).font = mono
            f += 1
        f += 1
        s.cell(row=f, column=1, value="El problema").font = negrita
        c = s.cell(row=f, column=2, value=d["problema"])
        c.alignment = arriba
        s.row_dimensions[f].height = 58
        f += 2
        s.cell(row=f, column=1, value="Qué cambia").font = negrita
        c = s.cell(row=f, column=2, value=d["efecto"])
        c.alignment = arriba
        s.row_dimensions[f].height = 46
        f += 2
        s.cell(row=f, column=1, value="LA PREGUNTA").font = negrita
        s.cell(row=f, column=1).fill = cab
        c = s.cell(row=f, column=2, value=d["pregunta"])
        c.font = negrita
        f += 1
        for o in d["opciones"]:
            s.cell(row=f, column=2, value="   · " + o).alignment = arriba
            f += 1
        f += 1
        s.cell(row=f, column=1, value="Vuestra decisión").font = negrita
        celda = s.cell(row=f, column=2)
        celda.fill = ojo
        dv = DataValidation(
            type="list",
            formula1='"%s"' % ",".join(o.replace(",", ";")[:70] for o in d["opciones"]),
            allow_blank=True)
        dv.error = "Escoja una de las opciones de arriba."
        s.add_data_validation(dv)
        dv.add(celda)
        f += 1
        s.cell(row=f, column=1, value="Por qué").font = negrita
        c = s.cell(row=f, column=2)
        c.fill = ojo
        c.alignment = arriba
        s.row_dimensions[f].height = 56
        f += 1
        s.cell(row=f, column=1, value="Frase en que os apoyáis").font = negrita
        c = s.cell(row=f, column=2)
        c.fill = ojo
        c.alignment = arriba
        s.row_dimensions[f].height = 56

    fi = wb.create_sheet("Firma")
    fi.column_dimensions["A"].width = 46
    fi.column_dimensions["B"].width = 54
    fi.cell(row=1, column=1, value="Firma de los dos autores").font = negrita
    fi.cell(row=2, column=1,
            value="Las seis decisiones son de los dos: se firman juntas o no se firma ninguna.")
    for i, k in enumerate(["Revisor 1 (nombre completo)",
                           "Revisor 2 (nombre completo)",
                           "Fecha (AAAA-MM-DD)",
                           "¿Habéis leído los artículos citados en cada hoja?"], start=4):
        fi.cell(row=i, column=1, value=k).font = negrita
        fi.cell(row=i, column=2, value="").fill = ojo

    wb.save(CUADERNO)
    print("%d hallazgos para firmar" % len(HALLAZGOS))
    print("cuaderno: %s" % CUADERNO)


if __name__ == "__main__":
    main()
