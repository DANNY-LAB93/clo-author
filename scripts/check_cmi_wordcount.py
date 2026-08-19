"""Mide el manuscrito contra el limite de Clinical Microbiology and Infection.

LIMITES, leidos de la guia de autores de CMI el 2026-08-03 y conservados desde
entonces en el repositorio:

    revision sistematica, texto principal   3 500 palabras
    resumen estructurado                      300 palabras
    lista PRISMA 2020                         obligatoria al enviar

POR QUE ESTE SCRIPT SE REESCRIBIO

La version anterior contaba `paper/main_cmi.tex`, que se elimino con la ruta
LaTeX el 2026-08-12. Desde entonces fallaba al abrirlo, es decir, llevaba dias
sin comprobar nada mientras aparentaba ser el guardian del limite. Un limite
duro que nadie mide es un rechazo editorial esperando su turno.

QUE CUENTA Y QUE NO

CMI cuenta el texto principal: de la Introduccion al final de las Conclusiones.
Quedan fuera la portada, el resumen, las palabras clave, las declaraciones, las
referencias, y las tablas y figuras con sus leyendas. Las claves de cita
(`[@Autor2020]`) no son palabras del texto y tampoco cuentan; en el PDF final
son un superindice.

Ademas del total, informa el reparto por seccion. Saber que sobran cuatrocientas
palabras no ayuda; saber en que seccion estan, si.

Uso:
    python scripts/check_cmi_wordcount.py
"""
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
ES = ROOT / "paper" / "manuscrito_revision_sistematica.md"
EN = ROOT / "paper" / "manuscript_systematic_review_en.md"

LIMITE_CUERPO = 3500
LIMITE_RESUMEN = 300

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass


def palabras(texto):
    t = re.sub(r"\[@[^\]]+\]", " ", texto)          # claves de cita
    t = re.sub(r"[*_`#|>]", " ", t)                 # marcas de Markdown
    return len([w for w in re.split(r"\s+", t) if w.strip(" .,;:()-")])


def secciones(cuerpo):
    """Reparto por seccion de nivel 2, en orden de aparicion."""
    cortes = [(m.start(), m.group(1).strip())
              for m in re.finditer(r"(?m)^##\s+(.+)$", cuerpo)]
    fuera = []
    for n, (ini, titulo) in enumerate(cortes):
        fin = cortes[n + 1][0] if n + 1 < len(cortes) else len(cuerpo)
        fuera.append((titulo, palabras(cuerpo[ini:fin])))
    return fuera


def mide(ruta, ini_resumen, ini_cuerpo, fin_cuerpo):
    doc = ruta.read_text(encoding="utf-8")
    resumen = doc.split(ini_resumen)[1].split(ini_cuerpo)[0]
    cuerpo = doc.split(ini_cuerpo)[1]
    for corte in fin_cuerpo:
        cuerpo = cuerpo.split(corte)[0]
    return palabras(resumen), palabras(cuerpo), secciones(ini_cuerpo + cuerpo)


def informe(nombre, res, cue, secs):
    print(f"--- {nombre} ---")
    estado_r = "cabe" if res <= LIMITE_RESUMEN else f"SE PASA en {res - LIMITE_RESUMEN}"
    estado_c = "cabe" if cue <= LIMITE_CUERPO else f"SE PASA en {cue - LIMITE_CUERPO}"
    print(f"  resumen        {res:5} / {LIMITE_RESUMEN}   {estado_r}")
    print(f"  texto principal{cue:5} / {LIMITE_CUERPO}   {estado_c}")
    if cue > LIMITE_CUERPO:
        print("  reparto por seccion, de mayor a menor:")
        for titulo, n in sorted(secs, key=lambda x: -x[1]):
            print(f"     {n:5}  {titulo[:56]}")
    print()
    return cue <= LIMITE_CUERPO and res <= LIMITE_RESUMEN


def main():
    ok = True
    ok &= informe("español", *mide(ES, "## Resumen", "## 1. Introducci",
                                   ("## Declaraciones",)))
    if EN.exists():
        ok &= informe("inglés", *mide(EN, "## Abstract", "## 1. Introduction",
                                      ("## Declarations", "## Declaraciones")))
    if ok:
        print("dentro de los limites de CMI")
        return 0
    print("FUERA DE LIMITE: CMI devuelve el manuscrito sin mandarlo a revision.")
    return 1


if __name__ == "__main__":
    sys.exit(main())
