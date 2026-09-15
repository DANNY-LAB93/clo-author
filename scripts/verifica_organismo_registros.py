# -*- coding: utf-8 -*-
"""Lectura, una por una, de las 29 fichas de registro cuyo titulo, resumen y
MeSH no permitian saber que organismo se trata.

Las fichas completas estan en disco, bajadas por `fetch_registros.py`:
  revision_sistematica/textos_completos/registros/<NCT>.json        (ClinicalTrials.gov API v2)
  revision_sistematica/textos_completos/registros/CTIS_<id>.json    (CTIS public API)

Este script NO decide. Hace tres cosas:
  1. Para cada estudio, recupera del JSON la frase literal que sostiene la
     lectura. Si la frase no esta donde se dice que esta, aborta sin escribir.
  2. Escribe la tabla de evidencia.
  3. Escribe el cuaderno para firmar. Excluir un estudio es un acto de autoria:
     hasta que las dos firmas esten, no se toca el corpus.

VEREDICTOS
  CUMPLE          la ficha nombra P. aeruginosa entre los organismos de la
                  poblacion que se va a tratar.
  NO CUMPLE       la ficha exige otro organismo, o el estudio incumple otro
                  criterio de inclusion; los datos no se pueden separar.
  INDETERMINADO   la ficha no permite saberlo. No se excluye: se declara.
"""
import csv
import json
import pathlib
import re
import sys

RAIZ = pathlib.Path(__file__).resolve().parents[1]
FICHAS = RAIZ / "revision_sistematica" / "textos_completos" / "registros"
ENTRADA = RAIZ / "quality_reports" / "registros_sin_organismo.json"
TABLA = RAIZ / "quality_reports" / "registros_organismo_verificado.csv"
CUADERNO = pathlib.Path.home() / "Desktop" / "FIRMAR_organismo_de_los_registros.xlsx"

# est -> (veredicto, codigo, campo del JSON, clave literal a buscar en ese campo)
# El "campo" es el nombre de la clave dentro de la ficha; la "clave" es el texto
# que debe aparecer en ella. La frase que se cita se EXTRAE del JSON, no se teclea.
LECTURA = {
    # --- la ficha nombra P. aeruginosa entre los organismos tratados ---
    "EST-025": ("CUMPLE", "", "detailedDescription", "Pseudomonas aeruginosa"),
    "EST-026": ("CUMPLE", "", "detailedDescription", "Pseudomonas aeruginosa"),
    "EST-066": ("CUMPLE", "", "briefSummary", "P. aeruginosa"),
    "EST-097": ("CUMPLE", "", "eligibilityCriteria", "P. aeruginosa"),
    "EST-107": ("CUMPLE", "", "detailedDescription", "Pseudomonas aeruginosa"),
    "EST-112": ("CUMPLE", "", "eligibilityCriteria", "Pseudomonas aeruginosa"),
    "EST-114": ("CUMPLE", "", "eligibilityCriteria", "P. aeruginosa"),
    "EST-153": ("CUMPLE", "", "eligibilityCriteria", "Pseudomonas aeruginosa"),
    "EST-186": ("CUMPLE", "", "medicalCondition", "Pseudomonas"),
    "EST-187": ("CUMPLE", "", "medicalCondition", "Pseudomonas"),
    "EST-191": ("CUMPLE", "", "fullTitle", "Pseudomonas aeruginosa"),
    "EST-215": ("CUMPLE", "", "eligibilityCriteria", "P. aeruginosa"),

    # --- la ficha exige explicitamente OTRO organismo ---
    "EST-072": ("NO CUMPLE", "ORG", "eligibilityCriteria", "Monobacterial Infection due to S. aureus"),
    "EST-138": ("NO CUMPLE", "ORG", "publicTitle", "infected by Staphylococcus aureus"),
    "EST-150": ("NO CUMPLE", "ORG", "officialTitle", "Staphylococcus Epidermidis"),
    "EST-182": ("NO CUMPLE", "ORG", "officialTitle", "Fluoroquinolone-Resistant Escherichia Coli"),
    "EST-204": ("NO CUMPLE", "ORG", "officialTitle", "ETEC and EPEC Induced Diarrhea in Children"),
    "EST-210": ("NO CUMPLE", "ORG", "eligibilityCriteria", "E. coli present in feces sample"),
    "EST-216": ("NO CUMPLE", "ORG", "briefSummary", "Enterobacterium"),
    "EST-218": ("NO CUMPLE", "ORG", "briefSummary", "nontuberculous mycobacterial infections"),

    # --- incumplen otro criterio, no el del organismo ---
    "EST-211": ("NO CUMPLE", "OFF", "briefSummary", "investigate if certain bacteria are correlated"),
    "EST-213": ("NO CUMPLE", "OFF", "briefSummary", "help scientists and clinicians discover answers"),

    # --- la ficha no permite saberlo ---
    "EST-087": ("INDETERMINADO", "", "eligibilityCriteria", "severe infection treated with bacteriophage"),
    "EST-141": ("INDETERMINADO", "", "eligibilityCriteria", "children diagnosed with acute tonsillitis"),
    "EST-148": ("INDETERMINADO", "", "eligibilityCriteria", "recurrent chronic urinary tract infections"),
    "EST-192": ("INDETERMINADO", "", "eligibilityCriteria", "invasive mechanical ventilation"),
    "EST-203": ("INDETERMINADO", "", "eligibilityCriteria", "must have evidence of hemosiderosis"),
    "EST-209": ("INDETERMINADO", "", "eligibilityCriteria", "treated by phagotherapy and having had an adverse event"),
    "EST-214": ("INDETERMINADO", "", "eligibilityCriteria", "serious infection treated at CRIOAc Lyon by phage therapy"),
}

# lo que se sospecha que es el mismo ensayo registrado dos veces
DUP_A, DUP_B = "EST-186", "EST-187"
DUP_TEXTO = ("Phage4Cure-001 aparece en CTIS con dos identificadores "
             "(2023-507203-55-00 y 2022-503145-22-00). Puede ser un unico ensayo contado dos veces.")

CTIS = {  # est -> identificador CTIS, para los cuatro que no son NCT
    "EST-138": "2022-500541-24-00",
    "EST-186": "2023-507203-55-00",
    "EST-187": "2022-503145-22-00",
    "EST-191": "2024-519856-94-00",
}
URL_NCT = "https://clinicaltrials.gov/study/%s"
URL_CTIS = "https://euclinicaltrials.eu/ctis-public/view/%s"


def busca_campo(nodo, campo, salida):
    """Todos los valores de texto guardados bajo esa clave, a cualquier profundidad."""
    if isinstance(nodo, dict):
        for k, v in nodo.items():
            if k == campo and isinstance(v, str):
                salida.append(v)
            else:
                busca_campo(v, campo, salida)
    elif isinstance(nodo, list):
        for v in nodo:
            busca_campo(v, campo, salida)
    return salida


def frase(texto, clave, margen=200):
    """La frase literal de la ficha alrededor de la clave. Sin retocar."""
    i = texto.lower().find(clave.lower())
    ini = max(0, i - margen)
    fin = min(len(texto), i + len(clave) + margen)
    trozo = re.sub(r"\s+", " ", texto[ini:fin]).strip()
    return ("..." if ini else "") + trozo + ("..." if fin < len(texto) else "")


def main():
    pendientes = json.loads(ENTRADA.read_text(encoding="utf-8"))
    if len(pendientes) != len(LECTURA):
        raise SystemExit("hay %d fichas pendientes y %d lecturas; no cuadran"
                         % (len(pendientes), len(LECTURA)))

    filas, faltan = [], []
    for reg in pendientes:
        est = reg["est"]
        veredicto, codigo, campo, clave = LECTURA[est]
        if est in CTIS:
            archivo = FICHAS / ("CTIS_%s.json" % CTIS[est])
            registro, ident, url = "CTIS", CTIS[est], URL_CTIS % CTIS[est]
        else:
            archivo = FICHAS / ("%s.json" % reg["nct"])
            registro, ident, url = "ClinicalTrials.gov", reg["nct"], URL_NCT % reg["nct"]
        if not archivo.exists():
            raise SystemExit("falta la ficha en disco: %s" % archivo)
        ficha = json.loads(archivo.read_text(encoding="utf-8"))

        candidatos = [t for t in busca_campo(ficha, campo, []) if clave.lower() in t.lower()]
        if not candidatos:
            faltan.append("%s: no aparece en el campo %s de %s" % (est, campo, archivo.name))
            continue
        filas.append({
            "study_id": est,
            "registro": registro,
            "identificador": ident,
            "veredicto_propuesto": veredicto,
            "codigo": codigo,
            "campo_de_la_ficha": campo,
            "frase_literal_de_la_ficha": frase(candidatos[0], clave),
            "url": url,
            "titulo_en_el_corpus": reg["titulo"],
        })

    if faltan:
        print("La evidencia declarada no esta en la ficha. No se escribe nada:", file=sys.stderr)
        for f in faltan:
            print("  " + f, file=sys.stderr)
        raise SystemExit(1)

    with TABLA.open("w", newline="", encoding="utf-8-sig") as f:
        w = csv.DictWriter(f, fieldnames=list(filas[0].keys()))
        w.writeheader()
        w.writerows(filas)

    cuenta = {}
    for f in filas:
        cuenta[f["veredicto_propuesto"]] = cuenta.get(f["veredicto_propuesto"], 0) + 1
    print("%d fichas leidas contra su registro" % len(filas))
    for k in ("CUMPLE", "NO CUMPLE", "INDETERMINADO"):
        print("  %-14s %d" % (k, cuenta.get(k, 0)))
    print("tabla de evidencia: %s" % TABLA)
    escribe_cuaderno(filas)
    print("cuaderno para firmar: %s" % CUADERNO)


def escribe_cuaderno(filas):
    from openpyxl import Workbook
    from openpyxl.styles import Alignment, Font, PatternFill
    from openpyxl.worksheet.datavalidation import DataValidation

    negrita = Font(bold=True)
    cab = PatternFill("solid", fgColor="D9E1F2")
    ojo = PatternFill("solid", fgColor="FCE4D6")
    arriba = Alignment(vertical="top", wrap_text=True)

    wb = Workbook()

    h = wb.active
    h.title = "Empieza aqui"
    h.column_dimensions["A"].width = 118
    texto = [
        ("Que es esto", True),
        ("", False),
        ("29 de los 155 estudios del corpus son fichas de registro cuyo titulo, resumen y MeSH no decian que", False),
        ("organismo se trata. Se bajo la ficha completa de cada una -25 de ClinicalTrials.gov y 4 del registro", False),
        ("europeo CTIS- y se leyo una por una. Las fichas quedaron en disco, en", False),
        ("revision_sistematica/textos_completos/registros/, y la frase que sostiene cada lectura esta en la hoja", False),
        ("'Fichas', copiada literal del registro.", False),
        ("", False),
        ("Lo que hay que decidir", True),
        ("", False),
        ("Excluir un estudio del corpus es un acto de autoria, no una operacion del canal. Nada de esto se ha", False),
        ("aplicado. La hoja 'Fichas' trae una propuesta por estudio; ustedes la confirman o la cambian en la", False),
        ("columna 'decision_firmada', y firman en la hoja 'Firma'. Hasta que esten las dos firmas, el corpus", False),
        ("sigue en 155 estudios.", False),
        ("", False),
        ("Que significa cada veredicto", True),
        ("", False),
        ("CUMPLE           la ficha nombra P. aeruginosa entre los organismos de la poblacion que se va a tratar.", False),
        ("NO CUMPLE        la ficha exige otro organismo (codigo ORG), o el estudio incumple otro criterio (OFF).", False),
        ("INDETERMINADO    la ficha no permite saberlo. La propuesta NO es excluirlo: es dejarlo y declararlo.", False),
        ("", False),
        ("Lo que cuesta cada si", True),
        ("", False),
        ("Cada NO CUMPLE que firmen saca un estudio del corpus y mueve cifras ya escritas en el manuscrito: el", False),
        ("total de estudios, el diagrama PRISMA, la tabla 4 de exclusiones y los porcentajes que se calculan", False),
        ("sobre el total. Por eso no se aplica solo. Despues de firmar, el canal se vuelve a correr entero.", False),
        ("", False),
        ("Ejemplo de como se rellena", True),
        ("", False),
        ("  study_id             EST-204", False),
        ("  veredicto_propuesto  NO CUMPLE", False),
        ("  frase_literal        ...Effect of an Orally-fed Escherichia Coli (E. Coli) Phage in the Management", False),
        ("                       of ETEC and EPEC Induced Diarrhea in Children...", False),
        ("  decision_firmada     NO CUMPLE        <- se escoge del desplegable", False),
        ("  comentario           Ensayo de E. coli en ninos con diarrea en Bangladesh, patrocinado por Nestle.", False),
        ("                       No hay datos de P. aeruginosa que separar.", False),
        ("", False),
        ("Si no estan de acuerdo con una propuesta, escojan otra cosa en 'decision_firmada' y digan por que en", False),
        ("'comentario'. Un desacuerdo razonado vale exactamente lo mismo que una confirmacion.", False),
    ]
    for i, (t, b) in enumerate(texto, start=1):
        c = h.cell(row=i, column=1, value=t)
        if b:
            c.font = negrita

    s = wb.create_sheet("Fichas")
    cols = ["study_id", "registro", "identificador", "veredicto_propuesto", "codigo",
            "campo_de_la_ficha", "frase_literal_de_la_ficha", "url", "titulo_en_el_corpus",
            "decision_firmada", "comentario"]
    anchos = [11, 17, 20, 20, 8, 20, 78, 46, 60, 20, 46]
    for j, (n, a) in enumerate(zip(cols, anchos), start=1):
        c = s.cell(row=1, column=j, value=n)
        c.font = negrita
        c.fill = cab
        c.alignment = arriba
        s.column_dimensions[c.column_letter].width = a
    orden = {"NO CUMPLE": 0, "INDETERMINADO": 1, "CUMPLE": 2}
    ordenadas = sorted(filas, key=lambda x: (orden[x["veredicto_propuesto"]], x["study_id"]))
    for i, f in enumerate(ordenadas, start=2):
        for j, n in enumerate(cols, start=1):
            c = s.cell(row=i, column=j, value=f.get(n, ""))
            c.alignment = arriba
            if n == "decision_firmada":
                c.fill = ojo
        s.row_dimensions[i].height = 58
    dv = DataValidation(type="list", formula1='"CUMPLE,NO CUMPLE,INDETERMINADO"', allow_blank=True)
    dv.error = "Escoja una de las tres."
    s.add_data_validation(dv)
    dv.add("J2:J%d" % (len(filas) + 1))
    s.freeze_panes = "A2"

    d = wb.create_sheet("Duplicado")
    d.column_dimensions["A"].width = 112
    lineas = [
        "Una cosa mas, que no es una exclusion por organismo",
        "",
        DUP_TEXTO,
        "",
        "Las dos fichas cumplen el criterio del organismo: las dos dicen 'Pseudomonas colonization'. Lo que hay",
        "que decidir es si %s y %s son el mismo ensayo. Si lo son, uno de los dos no es un" % (DUP_A, DUP_B),
        "estudio nuevo sino un informe mas del mismo, y el corpus baja en uno por duplicacion, no por criterio.",
        "",
        "Son el mismo ensayo?  (escriban SI o NO, y quien lo comprobo)",
        "",
        "    respuesta:",
        "    comprobado por:",
    ]
    for i, t in enumerate(lineas, start=1):
        c = d.cell(row=i, column=1, value=t)
        if i == 1:
            c.font = negrita

    fi = wb.create_sheet("Firma")
    fi.column_dimensions["A"].width = 46
    fi.column_dimensions["B"].width = 52
    fi.cell(row=1, column=1, value="Firma de los dos revisores").font = negrita
    fi.cell(row=2, column=1, value="Sin las dos firmas y la fecha, nada de esto se aplica al corpus.")
    campos = [
        "Revisor 1 (nombre completo)",
        "Revisor 2 (nombre completo)",
        "Fecha (AAAA-MM-DD)",
        "",
        "Leyeron las dos la frase literal de cada ficha?",
        "Abrieron alguna ficha en el registro, en el navegador?",
        "Cuales?",
    ]
    for i, k in enumerate(campos, start=4):
        if not k:
            continue
        fi.cell(row=i, column=1, value=k).font = negrita
        fi.cell(row=i, column=2, value="").fill = ojo
    wb.save(CUADERNO)


if __name__ == "__main__":
    main()
