"""Pone delante las frases del artículo que hablan de cada dominio de sesgo.

NO DICTAMINA, Y ESO ES EL PUNTO. El juicio de riesgo de sesgo lo emiten
D. Valdiviezo y N. Trelles, por duplicado y a ciegas, y el manuscrito lo
reportará como suyo. Este script solo busca dónde el artículo habla de
aleatorización, de cegamiento, de pérdidas o de financiación, y copia la frase
con su contexto. Quien lee decide. Igual que `evidencia_diseno.py` y
`evidencia_intervencion.py`, que tampoco adjudican.

QUÉ SIGNIFICA QUE UN DOMINIO SALGA VACÍO. Que el buscador no encontró la
señal, no que el estudio no la tenga: la expresión puede estar redactada de otra
manera, o el PDF puede haber perdido la sección al extraerse. Un dominio sin
frases es una invitación a leer el artículo, no un "no informa" ya resuelto.
Por eso el informe imprime SIEMPRE los diez dominios, incluso los vacíos.

Los 24 estudios sin texto completo no aparecen aquí porque no hay nada que leer.
Van al formulario marcados como no evaluables.

Uso:
    python scripts/evidencia_riesgo_sesgo.py                # todos los legibles
    python scripts/evidencia_riesgo_sesgo.py EST-021        # uno
    python scripts/evidencia_riesgo_sesgo.py --csv          # a fichero, para el formulario
"""
import csv
import pathlib
import re
import sys

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

ROOT = pathlib.Path(__file__).resolve().parent.parent
CACHE = ROOT / "revision_sistematica" / "textos_completos" / "texto_cache"
SALIDA = ROOT / "revision_sistematica" / "riesgo_sesgo" / "evidencia_por_dominio.csv"

VENTANA = 240      # caracteres de contexto a cada lado
MAX_FRASES = 3     # por dominio y estudio; más satura al que lee

# Un dominio por bloque de preguntas de los cuatro instrumentos. Las expresiones
# son deliberadamente amplias: es peor perder una frase que enseñar una de más,
# porque quien lee descarta en un segundo y no puede recuperar lo que no ve.
DOMINIOS = [
    ("ALEATORIZACION",
     "Secuencia de asignación y ocultamiento (RoB 2, dominio 1)",
     r"randomi[sz](?:ed|ation|ing)|random(?:ly)? (?:assign|allocat)|"
     r"allocation (?:conceal|sequence|ratio)|computer[- ]generated|"
     r"random number|block randomi|stratified randomi|sealed envelope|"
     r"1:1 ratio|permuted block|aleatoriza"),

    ("DESVIACIONES",
     "Desviaciones de la intervención asignada (RoB 2, dominio 2)",
     r"intention[- ]to[- ]treat|\bITT\b|per[- ]protocol|as[- ]treated|"
     r"protocol (?:deviation|violation)|cross(?:ed)?[- ]?over to|"
     r"discontinued (?:treatment|the intervention)|non[- ]adherence|"
     r"compassionate use|salvage (?:therapy|treatment)|off[- ]label"),

    ("CEGAMIENTO",
     "Cegamiento de pacientes, personal y evaluadores (RoB 2 d.2 y d.4)",
     r"\bblind(?:ed|ing)?\b|double[- ]blind|single[- ]blind|open[- ]label|"
     r"unblinded|masked|placebo[- ]controlled|assessor[s]? (?:were|was) "
     r"(?:blind|unaware)|doble ciego|abierto"),

    ("PERDIDAS",
     "Datos de desenlace faltantes (RoB 2, dominio 3)",
     r"lost to follow[- ]up|withdrew|withdrawal|dropout|drop[- ]out|"
     r"discontinued the study|did not complete|missing data|"
     r"available for analysis|excluded from (?:the )?analysis|"
     r"attrition|imputation|last observation carried"),

    ("MEDICION",
     "Medición del desenlace (RoB 2, dominio 4)",
     r"primary (?:end ?point|outcome)|secondary (?:end ?point|outcome)|"
     r"outcome (?:was |were )?(?:defined|assessed|measured|adjudicated)|"
     r"success was defined|defined as (?:the )?(?:resolution|eradication|"
     r"absence|improvement)|criteria for (?:cure|success|response)|"
     r"clinical (?:cure|success|response) was"),

    ("REPORTE",
     "Selección del resultado informado y registro previo (RoB 2, dominio 5)",
     r"registered (?:at|with|on)|clinicaltrials\.gov|NCT\d{8}|EudraCT|"
     r"ISRCTN|trial registration|protocol (?:was )?(?:published|available)|"
     r"statistical analysis plan|pre[- ]?specified|prospectively registered"),

    ("CONFUSION",
     "Confusión y selección de participantes (ROBINS-I, dominios 1 y 2)",
     r"confound(?:ing|er)|adjusted for|multivariable|propensity|"
     r"matched (?:for|on)|comparison group|control group|historical control|"
     r"consecutive patients|eligibility criteria|inclusion criteria"),

    ("CLASIFICACION",
     "Clasificación de la intervención y su medición (ROBINS-I, d.3 y d.6)",
     r"dose|titre|titer|PFU|plaque[- ]forming|route of administration|"
     r"intravenous|nebuli[sz]|topical|instillation|duration of (?:therapy|"
     r"treatment)|administered (?:for|over|during)|concomitant antibiotic|"
     r"phage (?:cocktail|preparation|susceptibility|sensitivity)"),

    ("CASO",
     "Descripción del caso: demografía, historia, diagnóstico, seguimiento (JBI)",
     r"a \d+[- ]year[- ]old|(?:male|female) patient|medical history|"
     r"comorbidit|past history|on admission|physical examination|"
     r"culture (?:grew|yielded|was positive)|susceptibility testing|"
     r"at (?:\d+|one|two|three|six|twelve) (?:day|week|month)s? (?:of )?follow"),

    ("CONFLICTOS",
     "Financiación, conflictos de interés y consentimiento",
     r"conflicts? of interest|competing interests|declare[sd]? no|"
     r"funded by|funding|grant (?:no|number|from)|sponsor|"
     r"informed consent|ethics (?:committee|approval)|institutional review|"
     r"written consent was obtained"),
]


def frases(texto, patron):
    """Las apariciones del patrón, con contexto y sin repetir la misma zona."""
    vistos, salida = [], []
    for m in re.finditer(patron, texto, re.I):
        if any(abs(m.start() - v) < VENTANA for v in vistos):
            continue
        vistos.append(m.start())
        a, b = max(0, m.start() - VENTANA), min(len(texto), m.end() + VENTANA)
        salida.append("..." + texto[a:b].strip() + "...")
        if len(salida) >= MAX_FRASES:
            break
    return salida


def legibles():
    inv = CACHE / "_inventario.csv"
    if not inv.exists():
        return sorted(p.stem for p in CACHE.glob("EST-*.txt"))
    with open(inv, encoding="utf-8-sig", newline="") as fh:
        return [r["study_id"] for r in csv.DictReader(fh)
                if r.get("estado") == "legible"]


def main():
    args = [a for a in sys.argv[1:] if a != "--csv"]
    a_csv = "--csv" in sys.argv
    ids = args or legibles()

    filas = []
    for s in ids:
        p = CACHE / ("%s.txt" % s)
        if not p.exists():
            print("%s: sin texto en la cache, no evaluable" % s)
            continue
        t = re.sub(r"\s+", " ", p.read_text(encoding="utf-8"))
        if not a_csv:
            print("\n" + "=" * 78)
            print("### %s   %d caracteres" % (s, len(t)))
        for clave, titulo, patron in DOMINIOS:
            fs = frases(t, patron)
            if not a_csv:
                print("\n  [%s] %s" % (clave, titulo))
                if not fs:
                    print("      -- sin señal; el artículo puede decirlo de otra "
                          "manera. Léelo antes de marcar «no informa».")
                for f in fs:
                    print("      %s" % f)
            for i, f in enumerate(fs, 1):
                filas.append({"study_id": s, "dominio": clave, "titulo": titulo,
                              "n": i, "frase": f})
            if not fs:
                filas.append({"study_id": s, "dominio": clave, "titulo": titulo,
                              "n": 0, "frase": ""})

    if a_csv:
        SALIDA.parent.mkdir(parents=True, exist_ok=True)
        with open(SALIDA, "w", encoding="utf-8-sig", newline="") as fh:
            w = csv.DictWriter(fh, ["study_id", "dominio", "titulo", "n", "frase"])
            w.writeheader()
            w.writerows(filas)
        con = len({f["study_id"] for f in filas if f["frase"]})
        print("escrito %s" % SALIDA.relative_to(ROOT))
        print("  %d estudios, %d frases, %d dominios por estudio"
              % (con, sum(1 for f in filas if f["frase"]), len(DOMINIOS)))


if __name__ == "__main__":
    main()
