"""Reúne, para cada texto completo, la evidencia sobre QUÉ se administró.

No dictamina. Un script no puede decidir si un artículo describe fago solo o
fago con antibiótico: sólo puede poner delante las frases donde eso se dice,
para que lo decida quien lee. La versión anterior de esta comprobación sí
dictaminaba, con una ventana de 130 caracteres, y se equivocó en 2 de 11.

Saca tres bloques por estudio:
  ANTIBIOTICO  frases donde aparece un antibiótico junto al fago
  SOLO         frases donde se afirma monoterapia o ausencia de antibiótico
  NO-FAGO      menciones de endolisina, lisina u otro derivado que NO es un fago

Uso:
    python scripts/evidencia_intervencion.py [EST-001 EST-002 ...]
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

ATB = (r"meropenem|imipenem|ceftazidime|cefepime|colistin|colisti|polymyxin|"
       r"piperacillin|tazobactam|ciprofloxacin|levofloxacin|amikacin|tobramycin|"
       r"gentamicin|aztreonam|ceftolozane|avibactam|vancomycin|linezolid|"
       r"daptomycin|rifampic|rifampin|antibiotic|antimicrobial therapy|antibacterial")
COMBO = (r"in combination|combined with|concomitant|concurrent|adjunct|"
         r"alongside|together with|plus |co-administ|added to|in addition to")
SOLO = (r"monotherap|phage alone|bacteriophage alone|without antibiotic|"
        r"no antibiotic|antibiotic-free|sole therapy|as the only|discontinu\w+ "
        r"antibiotic|ceased antibiotic|stopped antibiotic")
NOFAGO = r"endolysin|endolisin|\blysin\b|lysins|depolymerase|phage-derived protein"
FAGO = r"phage|bacteriophag|fago"


def frases(t):
    t = re.sub(r"\s+", " ", t)
    return re.split(r"(?<=[.;])\s+", t)


def rec(s, pat, extra=None, n=4):
    out = []
    for f in s:
        if len(f) < 25 or len(f) > 420:
            continue
        if re.search(pat, f, re.I) and (extra is None or re.search(extra, f, re.I)):
            out.append(f.strip())
        if len(out) >= n:
            break
    return out


def main():
    ids = sys.argv[1:] or sorted(p.stem for p in CACHE.glob("EST-*.txt"))
    for s in ids:
        p = CACHE / f"{s}.txt"
        if not p.exists():
            print(f"\n### {s}  --- SIN TEXTO COMPLETO")
            continue
        f = frases(p.read_text(encoding="utf-8"))
        a = rec(f, ATB, FAGO, 3) or rec(f, COMBO, ATB, 2) or rec(f, ATB, None, 2)
        so = rec(f, SOLO, None, 2)
        nf = rec(f, NOFAGO, None, 2)
        print(f"\n### {s}")
        for et, xs in (("ATB ", a), ("SOLO", so), ("NOFG", nf)):
            for x in xs:
                print(f"  {et} | {x[:300]}")
        if not (a or so or nf):
            print("  (ninguna frase de intervención localizada)")


if __name__ == "__main__":
    main()
