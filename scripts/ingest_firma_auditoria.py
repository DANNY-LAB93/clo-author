# -*- coding: utf-8 -*-
"""Ingiere las nueve decisiones firmadas de la auditoria del 2026-09-16.

QUE COMPRUEBA ANTES DE TOCAR NADA

El cuaderno no se toma al pie de la letra. Antes de escribir se verifica:

  · que las dos firmas estan puestas y con el nombre completo;
  · que la casilla de lectura de los articulos dice que si;
  · que las nueve hojas traen decision, porque una hoja en blanco no es una
    decision sino una hoja en blanco;
  · que el valor que hay HOY en el fichero es el que la hoja dice que hay. Si
    alguien lo cambio por otro camino, esa decision NO se ingiere: una firma
    sobre un valor distinto del que se enseño no es una firma sobre este dato.

QUE NO HACE

No edita `extraccion_adjudicada.csv`, que es un DERIVADO: lo rehace
`build_adjudicated_dataset.py` desde los dos cuadernos y se lleva por delante
cualquier cosa escrita ahi. Las cuatro correcciones de extraccion entran donde
entraron las quince del 2026-09-01: una fila en
`correcciones_tras_texto_completo.csv` con el valor anterior, el corregido, la
cita que lo sostiene y las dos firmas. Los cuadernos siguen diciendo lo que
cada revisor escribio.

EST-063 sale del corpus como salieron los otros 46: por una fila en
`exclusiones_tras_texto_completo.csv` con su codigo, su cita y su firma. Sus
ocho juicios de riesgo de sesgo se quedan en su fichero, que es el registro de
lo que se juzgo de verdad; lo que cambia es que el canal deja de contarlos,
igual que `study_groups` conserva a los excluidos del cribado.

Tampoco toca el manuscrito. Las cifras salen de los escalares y los escalares
salen de estos ficheros: se rehacen corriendo el canal.

Uso:
    python scripts/ingest_firma_auditoria.py              # informe, no escribe
    python scripts/ingest_firma_auditoria.py --escribir
"""
import csv
import datetime
import pathlib
import sys

from openpyxl import load_workbook

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

ROOT = pathlib.Path(__file__).resolve().parent.parent
RS = ROOT / "revision_sistematica"
EXTR = RS / "extraccion" / "extraccion_adjudicada.csv"
CORR = RS / "extraccion" / "correcciones_tras_texto_completo.csv"
ROB = RS / "riesgo_sesgo" / "riesgo_sesgo_comparativos_adjudicado.csv"
EXCL = RS / "cribado" / "exclusiones_tras_texto_completo.csv"
CUADERNO = pathlib.Path.home() / "Desktop" / "FIRMAR_auditoria_2026-09-16.xlsx"

FECHA = "2026-09-22"
FIRMA = "Danny Javier Valdiviezo Verdugo y Nataly Elizabeth Trelles Avila"
DE_LA_AUDITORIA = "corregido por la auditoria, dos firmas (%s)" % FECHA

# La definicion que EST-003 da de sus propios desenlaces, copiada de su
# seccion «Outcome definitions». La que habia era de EST-008 y hablaba de un
# producto -- BX004-A -- que no aparece ni una vez en EST-003.
DEF_003 = ("Recovery which was defined as no clinical signs of infection "
           "detected by physical examinations or PET/MRI imaging and negative "
           "microbiological cultures from site of infection; Remission defined "
           "as no clinical signs of infection or no imaging findings that "
           "suggest an active infection is present, however bacterial cultures "
           "were not obtained during the entire follow-up period.")

MOTIVO_063 = ("Protocolo de ensayo sin resultados. Estructura de protocolo de "
              "BMJ Open (INTRODUCTION / METHODS AND ANALYSIS / Ethics and "
              "dissemination) y 71 apariciones de «will be», el mismo criterio "
              "con que se excluyeron EST-035, EST-052, EST-083 y EST-122. La "
              "nota firmada del dominio D5 ya lo decia: «Es un protocolo; aun "
              "no hay resultados.» Firmado por los dos revisores el %s."
              % FECHA)
CITA_063 = ("This study is designed to provide pilot data pertaining to safety "
            "and tolerability in children and thus allow for larger, dosing or "
            "placebo trial studies that will fulfil Australian legislation.")
TITULO_063 = ("Single-arm, open-labelled, safety and tolerability of "
              "intrabronchial and nebulised bacteriophage treatment in children "
              "with cystic fibrosis and Pseudomonas aeruginosa.")

# ---------------------------------------------------------------------------
# Lo que cada hoja cambia. `esperado` es el valor que la hoja enseño; si el
# fichero ya no lo tiene, la decision no se ingiere.
# ---------------------------------------------------------------------------
CITA_DEF_003 = ("Recovery which was defined as no clinical signs of infection "
                "detected by physical examinations or PET/MRI imaging and "
                "negative microbiological cultures from site of infection")
MOT_DEF_003 = ("La definicion atribuida a EST-003 describe el cocktail BX004-A, "
               "que es el producto de EST-008 y no aparece ni una vez en "
               "EST-003. Se sustituye por la que el propio articulo da en su "
               "seccion «Outcome definitions».")

EXTRACCION = [
    # hoja, study_id, arm_id, campo, esperado, procedencia_esperada, nuevo,
    # cita, motivo
    (2, "EST-003", "A", "clinical_success_definition", None, "consenso",
     DEF_003, CITA_DEF_003, MOT_DEF_003),
    (2, "EST-003", "B", "clinical_success_definition", None, "consenso",
     DEF_003, CITA_DEF_003, MOT_DEF_003),
    (2, "EST-003", "C", "clinical_success_definition", None, "consenso",
     DEF_003, CITA_DEF_003, MOT_DEF_003),
    (2, "EST-003", "D", "clinical_success_definition", None, "consenso",
     DEF_003, CITA_DEF_003, MOT_DEF_003),
    (2, "EST-003", "E", "clinical_success_definition", None, "consenso",
     DEF_003, CITA_DEF_003, MOT_DEF_003),
    (2, "EST-003", "A", "clinical_success_n", "13", "consenso", "NA",
     "Based on the data presented, there was an 86.6% cure/remission rate "
     "(13 out of 15).",
     "El 13 es el numerador de la serie entera --13 de 15 pacientes-- y no el "
     "de un brazo de un paciente. Sin numerador propio del brazo, NA."),
    (4, "EST-077", "A", "adverse_event_n", "5", "consenso", "NA",
     "Four patients received five separate courses of antibiotic and phage "
     "combination therapy.",
     "El 5 son los ciclos de tratamiento, no eventos adversos: cuatro "
     "pacientes recibieron cinco ciclos. El articulo no usa «adverse» ni una "
     "vez, aunque si describe una retirada por sospecha de reaccion "
     "inflamatoria o alergica el dia 51."),
    (8, "EST-021", "A", "n_arm", "27", "consenso", "13",
     "27 patients were recruited and randomly assigned to receive phage "
     "therapy (n=13) or standard of care (n=14).",
     "El 27 es el ensayo entero. El brazo de fagos son 13. El denominador del "
     "exito clinico queda en 13 y la poblacion mITT de 12 se declara en nota, "
     "por decision de los autores del %s: la ficha de extraccion no tiene "
     "denominador propio del desenlace." % FECHA),
    (8, "EST-021", "A", "mortality_n", "0", "acuerdo", "1",
     "One participant in each group died after follow-up and the deaths were "
     "determined to not be related to treatment.",
     "El 0 contradice al articulo: murio un paciente en cada grupo."),
]

RIESGO = [
    # hoja, study_id, item, esperado, nuevo
    (1, "EST-021", "GLOBAL", "Bajo riesgo de sesgo", "Algunas preocupaciones"),
    (7, "EST-063", "GLOBAL", "Riesgo moderado", "Sin información para juzgar"),
    (7, "EST-116", "GLOBAL", "Riesgo moderado", "Sin información para juzgar"),
]


def leer(p, enc="utf-8-sig"):
    with open(p, encoding=enc, newline="") as f:
        r = list(csv.DictReader(f))
        return r, list(r[0].keys())


def escribir(p, filas, cols, enc="utf-8"):
    with open(p, "w", encoding=enc, newline="") as f:
        w = csv.DictWriter(f, fieldnames=cols)
        w.writeheader()
        w.writerows(filas)


def celda(ws, etiqueta):
    for f in ws.iter_rows(values_only=True):
        if f and f[0] and str(f[0]).strip().lower().startswith(etiqueta):
            return "" if len(f) < 2 or f[1] is None else str(f[1]).strip()
    return ""


def firmas_o_muere(wb):
    ws = wb["Firma"]
    d = {}
    for f in ws.iter_rows(values_only=True):
        if f and f[0]:
            d[str(f[0]).strip()] = "" if len(f) < 2 or f[1] is None else str(f[1]).strip()
    r1 = d.get("Revisor 1 (nombre completo)", "")
    r2 = d.get("Revisor 2 (nombre completo)", "")
    leido = d.get("¿Habéis leído los artículos citados en cada hoja?", "")
    faltan = []
    if len(r1.split()) < 3:
        faltan.append("el nombre completo del revisor 1")
    if len(r2.split()) < 3:
        faltan.append("el nombre completo del revisor 2")
    if leido.strip().lower() not in ("si", "sí", "s", "yes"):
        faltan.append("la confirmacion de que se leyeron los articulos")
    if faltan:
        raise SystemExit("NO SE INGIERE. Falta: %s." % "; ".join(faltan))
    print("Firmado por %s y %s. Articulos leidos: %s." % (r1, r2, leido))
    return r1, r2


def decisiones_o_muere(wb):
    """Las nueve hojas tienen que traer decision y frase."""
    hojas = [h for h in wb.sheetnames if h[0].isdigit()]
    vacias = []
    for h in hojas:
        ws = wb[h]
        if not celda(ws, "vuestra decisi"):
            vacias.append("%s: sin decision" % h)
        if not celda(ws, "frase en que os apoy"):
            vacias.append("%s: sin frase de apoyo" % h)
    if vacias:
        raise SystemExit("NO SE INGIERE. %s" % " | ".join(vacias))
    print("Las %d hojas traen decision y frase de apoyo." % len(hojas))
    return hojas


def main():
    esc = "--escribir" in sys.argv
    if not CUADERNO.exists():
        raise SystemExit("No esta el cuaderno: %s" % CUADERNO)
    wb = load_workbook(CUADERNO, data_only=True)
    firmas_o_muere(wb)
    decisiones_o_muere(wb)
    print()

    hechos, parados = [], []

    # ---- 1. la extraccion, por la capa de correcciones --------------------
    filas, cols = leer(EXTR)
    idx = {(r["study_id"], r["arm_id"]): r for r in filas}
    prfil, _ = leer(RS / "extraccion" / "extraccion_adjudicada_procedencia.csv")
    pridx = {(r["study_id"], r["arm_id"]): r for r in prfil}
    cfil, ccols = leer(CORR)
    ya = {(r["study_id"], r["arm_id"], r["campo"]) for r in cfil}
    nuevas = 0
    for hoja, est, brazo, campo, esperado, proc_esp, nuevo, cita, motivo in EXTRACCION:
        clave = (est, brazo, campo)
        if clave in ya:
            hechos.append("hoja %d: %s %s %s ya tenia correccion" % (hoja, est, brazo, campo))
            continue
        r = idx.get((est, brazo))
        if r is None:
            parados.append("hoja %d: no existe %s %s" % (hoja, est, brazo))
            continue
        hoy = (r[campo] or "").strip()
        proc_hoy = (pridx[(est, brazo)][campo] or "").strip()
        if esperado is not None and hoy != esperado:
            parados.append("hoja %d: %s %s %s vale «%s» y la hoja enseño «%s»"
                           % (hoja, est, brazo, campo, hoy, esperado))
            continue
        if proc_hoy != proc_esp:
            parados.append("hoja %d: %s %s %s viene de «%s», no de «%s»"
                           % (hoja, est, brazo, campo, proc_hoy, proc_esp))
            continue
        cfil.append({"study_id": est, "arm_id": brazo, "campo": campo,
                     "valor_anterior": hoy, "procedencia_anterior": proc_hoy,
                     "valor_corregido": nuevo, "cita_literal": cita,
                     "motivo": motivo,
                     "firmado_por": "Danny_Valdiviezo; nataly trelles",
                     "fecha": "%s; %s" % (FECHA, FECHA)})
        nuevas += 1
        hechos.append("hoja %d: %s %s %s  %s -> %s  (correccion firmada)"
                      % (hoja, est, brazo, campo, hoy[:36] or "(vacio)",
                         nuevo[:36]))
    if esc and nuevas:
        escribir(CORR, cfil, ccols)

    # ---- 2. el riesgo de sesgo ---------------------------------------------
    rfilas, rcols = leer(ROB)
    for hoja, est, item, esperado, nuevo in RIESGO:
        tocada = False
        for r in rfilas:
            if r["study_id"] == est and r["item"] == item:
                hoy = (r["valor"] or "").strip()
                if hoy == nuevo:
                    hechos.append("hoja %d: %s %s ya estaba en «%s»"
                                  % (hoja, est, item, nuevo))
                elif hoy != esperado:
                    parados.append("hoja %d: %s %s vale «%s» y la hoja enseño "
                                   "«%s»" % (hoja, est, item, hoy, esperado))
                else:
                    r["valor"] = nuevo
                    r["procedencia"] = DE_LA_AUDITORIA
                    r["firmado_por"] = FIRMA
                    r["fecha"] = FECHA
                    hechos.append("hoja %d: %s %s  %s -> %s"
                                  % (hoja, est, item, hoy, nuevo))
                tocada = True
        if not tocada:
            parados.append("hoja %d: no existe el juicio %s %s"
                           % (hoja, est, item))
    if esc:
        escribir(ROB, rfilas, rcols, enc="utf-8-sig")

    # ---- 3. la exclusion de EST-063 ----------------------------------------
    efilas, ecols = leer(EXCL, enc="utf-8")
    if any(r["study_id"] == "EST-063" for r in efilas):
        hechos.append("hoja 5: EST-063 ya estaba excluido")
    else:
        efilas.append({"study_id": "EST-063", "codigo": "PRO",
                       "motivo": MOTIVO_063, "cita_del_texto": CITA_063,
                       "titulo": TITULO_063,
                       "decidido_por": "D. Valdiviezo y N. Trelles",
                       "fecha": FECHA})
        hechos.append("hoja 5: EST-063 excluido con codigo PRO "
                      "(exclusiones %d -> %d)" % (len(efilas) - 1, len(efilas)))
        if esc:
            escribir(EXCL, efilas, ecols)

    # ---- informe -----------------------------------------------------------
    print("APLICADO" if esc else "LO QUE SE APLICARIA (nada escrito todavia)")
    for h in hechos:
        print("  · %s" % h)
    if parados:
        print("\nNO INGERIDO, porque el fichero ya no tiene el valor que la "
              "hoja enseño:")
        for p in parados:
            print("  · %s" % p)
    print("\nHojas 3, 6 y 9 no cambian ningun dato: son la redaccion del "
          "manuscrito.")
    if esc:
        print("\nAhora hay que rehacer los escalares:")
        print("  python scripts/build_synthesis_scalars.py   (y el resto del "
              "canal, en orden)")
    else:
        print("\nNada escrito. Para escribir: --escribir")
    return 1 if parados else 0


if __name__ == "__main__":
    sys.exit(main())
