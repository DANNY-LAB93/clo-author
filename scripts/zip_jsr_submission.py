# -*- coding: utf-8 -*-
"""Comprime el sobre de Journal of Science and Research en un solo .zip.

ENTRADA   ~/Escritorio/Envio_JSR_Fagoterapia_Pseudomonas/   (lo escribe build_jsr_submission.py)
SALIDA    ~/Escritorio/Envio_JSR_Fagoterapia_Pseudomonas.zip

QUE COMPRUEBA ANTES DE COMPRIMIR

  1. Que el sobre no esta caduco: si el manuscrito del sobre es mas viejo que
     el manuscrito fuente o que los escalares, para. Un .zip es lo que se
     manda por correo, y comprimir una version vieja es la forma mas facil de
     enviar cifras que ya no son las del canal.
  2. Que el manuscrito, la carta, el LEEME y las cuatro carpetas estan.

QUE COMPRUEBA DESPUES

  Reabre el .zip y compara, uno por uno, la lista de ficheros y su tamano
  contra la carpeta. Si falta algo o no cuadra un byte, borra el .zip y sale
  con error: mas vale ningun .zip que uno incompleto que parece completo.

Uso:
    python scripts/zip_jsr_submission.py [carpeta_del_sobre]
"""
import pathlib
import sys
import zipfile

ROOT = pathlib.Path(__file__).resolve().parent.parent
SOBRE = pathlib.Path.home() / "Desktop" / "Envio_JSR_Fagoterapia_Pseudomonas"
FUENTE = ROOT / "paper" / "manuscrito_JSR_final.md"
ESCALARES = ROOT / "quality_reports" / "synthesis_scalars.json"

IMPRESCINDIBLES = ("manuscrito_JSR_final.docx", "carta_de_presentacion.docx",
                   "LEEME_ANTES_DE_ENVIAR.md")
CARPETAS = ("suplementos", "tablas", "figuras", "para_leer")

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass


def tamano(n):
    for u in ("B", "KB", "MB"):
        if n < 1024 or u == "MB":
            return "%.1f %s" % (n, u) if u != "B" else "%d B" % n
        n /= 1024.0


def main():
    sobre = pathlib.Path(sys.argv[1]) if len(sys.argv) > 1 else SOBRE
    if not sobre.is_dir():
        raise SystemExit("no encuentro el sobre en %s. Corre antes "
                         "scripts/build_jsr_submission.py" % sobre)

    faltan = [n for n in IMPRESCINDIBLES if not (sobre / n).exists()]
    faltan += [n for n in CARPETAS if not (sobre / n).is_dir()]
    if faltan:
        raise SystemExit("al sobre le falta: %s" % ", ".join(faltan))

    # --- el sobre no puede ser mas viejo que lo que dice contener ---
    doc = (sobre / "manuscrito_JSR_final.docx").stat().st_mtime
    viejo = [p.name for p in (FUENTE, ESCALARES)
             if p.exists() and p.stat().st_mtime > doc]
    if viejo:
        raise SystemExit(
            "el sobre esta caduco: %s se modifico DESPUES que el manuscrito "
            "del sobre. Corre scripts/build_jsr_submission.py y vuelve a "
            "intentarlo." % " y ".join(viejo))

    ficheros = sorted(p for p in sobre.rglob("*") if p.is_file())
    destino = sobre.with_suffix(".zip")
    if destino.exists():
        destino.unlink()

    # La raiz del .zip es la propia carpeta: al descomprimir sale el sobre
    # entero y no cuarenta ficheros sueltos en el Escritorio.
    with zipfile.ZipFile(destino, "w", zipfile.ZIP_DEFLATED, compresslevel=9) as z:
        for p in ficheros:
            z.write(p, pathlib.Path(sobre.name) / p.relative_to(sobre))

    # --- se reabre y se compara, fichero a fichero ---
    with zipfile.ZipFile(destino) as z:
        dentro = {i.filename: i.file_size for i in z.infolist()}
        malo = z.testzip()
    problemas = []
    if malo:
        problemas.append("fichero corrupto dentro del zip: %s" % malo)
    for p in ficheros:
        clave = (pathlib.Path(sobre.name) / p.relative_to(sobre)).as_posix()
        if clave not in dentro:
            problemas.append("falta en el zip: %s" % clave)
        elif dentro[clave] != p.stat().st_size:
            problemas.append("tamano distinto: %s" % clave)
    if problemas:
        destino.unlink()
        print("EL ZIP NO SE ESCRIBE. Problemas:", file=sys.stderr)
        for x in problemas:
            print("  " + x, file=sys.stderr)
        raise SystemExit(1)

    print("sobre comprimido y comprobado fichero a fichero")
    for c in CARPETAS:
        n = sum(1 for p in ficheros if p.parent.name == c)
        print("  %-14s %d ficheros" % (c + "/", n))
    sueltos = [p.name for p in ficheros if p.parent == sobre]
    print("  %-14s %s" % ("en la raiz:", ", ".join(sorted(sueltos))))
    print("\n  %d ficheros, %s comprimidos en %s"
          % (len(ficheros), tamano(destino.stat().st_size), tamano(
              sum(p.stat().st_size for p in ficheros))))
    print("\nescrito %s" % destino)


if __name__ == "__main__":
    main()
