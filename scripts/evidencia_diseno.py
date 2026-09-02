"""¿Es este documento un estudio clínico con pacientes, o es otra cosa?

Un protocolo de ensayo, un modelo in vitro y una revisión narrativa pueden
llevar la palabra «phage» y el nombre del patógeno en cada página sin aportar
ni un desenlace en un paciente. El cribado por título y resumen no siempre los
separa, y en la extracción acaban con un `study_design` que los hace parecer
estudios.

Este script no dictamina: marca las señales y las pone delante, con la frase
donde aparecen, para que se lea.

Uso:
    python scripts/evidencia_diseno.py [EST-001 ...]
"""
import pathlib
import re
import sys

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

CACHE = (pathlib.Path(__file__).resolve().parent.parent
         / "revision_sistematica" / "textos_completos" / "texto_cache")

SENAL = {
    "PROTOCOLO": r"protocol version|protocol number|SPIRIT (?:20\d\d|checklist)|"
                 r"\{1[0-9][a-z]?\}|informed consent will be|will be randomi[sz]ed|"
                 r"statistical analysis plan|this protocol describes",
    "IN-VITRO": r"hollow[- ]fib|time[- ]kill|multiplicity of infection|\bMOI\b|"
                r"bacterial lawn|spot assay|checkerboard|log cfu/mL reduction",
    "ANIMAL": r"\bmurine\b|\bmice\b|\brats?\b|galleria|zebrafish|rabbit model|"
              r"animal model",
    "REVISION": r"we searched (?:PubMed|MEDLINE|Embase)|this (?:narrative |scoping "
                r"|systematic )?review (?:summari|aims|examines)|search strategy was",
    "PACIENTES": r"patients? (?:were|was) (?:treated|enrolled|admitted|included)|"
                 r"we (?:treated|report a|present a) (?:case|patient)|"
                 r"a \d+[- ]year[- ]old",
}


def main():
    ids = sys.argv[1:] or sorted(p.stem for p in CACHE.glob("EST-*.txt"))
    for s in ids:
        p = CACHE / f"{s}.txt"
        if not p.exists():
            continue
        t = re.sub(r"\s+", " ", p.read_text(encoding="utf-8"))
        hit = {k: len(re.findall(v, t, re.I)) for k, v in SENAL.items()}
        raras = [k for k in ("PROTOCOLO", "IN-VITRO", "ANIMAL", "REVISION") if hit[k]]
        if not raras:
            continue
        marca = " ".join(f"{k}={hit[k]}" for k in raras)
        print(f"\n### {s}   {marca}   PACIENTES={hit['PACIENTES']}")
        print(f"    {t[:150].strip()}")
        for k in raras:
            m = re.search(SENAL[k], t, re.I)
            if m:
                print(f"    [{k}] ...{t[max(0,m.start()-120):m.start()+160].strip()}...")


if __name__ == "__main__":
    main()
