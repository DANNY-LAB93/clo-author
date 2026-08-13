"""Pone al día las cifras del manuscrito que el canal ha recalculado.

POR QUÉ NO ES UN BUSCAR-Y-REEMPLAZAR

Dos cifras del manuscrito no se pueden tocar aunque coincidan con las que
cambian:

  · «el corpus pasó de 159 a 124 estudios» es historia de la enmienda de idioma.
    El 159 es correcto ahí y seguirá siéndolo siempre.
  · «no consta el ámbito de patógeno en el 52,4 %» es otro escalar
    (`sin_ambito_de_patogeno_pct`), que casualmente valía lo mismo que el
    porcentaje de recuperación antes de que este subiera. Cambiar los dos a la
    vez metería un error donde no lo había.

Por eso cada reemplazo lleva su contexto completo y se exige que aparezca
EXACTAMENTE UNA VEZ. Si aparece cero veces, el manuscrito ya cambió y hay que
revisar la regla; si aparece dos, el contexto no es bastante específico. En
ambos casos el script falla en vez de escribir.

EL COMPROBADOR NO BASTA

`check_manuscript_numbers.py` da por buena cualquier cifra que coincida con
algún escalar, sea o no el escalar que le toca. Por eso dejó pasar el «65»:
existe `sin_ambito_de_patogeno = 65`. Este script hace lo que aquel no puede,
que es mirar la frase.

Uso:
    python scripts/sync_manuscript_numbers.py [--escribir]
"""
import argparse
import json
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
ES = ROOT / "paper" / "manuscrito_revision_sistematica.md"
EN = ROOT / "paper" / "manuscript_systematic_review_en.md"
ESCALARES = ROOT / "quality_reports" / "synthesis_scalars.json"

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

# (archivo, texto viejo, texto nuevo, qué escalar lo respalda)
CAMBIOS = [
    (ES, "el texto completo de 65 estudios (52,4 %)",
         "el texto completo de 67 estudios (54,0 %)",
         "texto_completo_obtenido / texto_completo_pct"),
    (ES, "desde el resumen de los 159 estudios con publicación recuperable, realizada",
         "desde el resumen de los 124 estudios con publicación recuperable, realizada",
         "estudios_extraibles"),
    (ES, "**65 de los 124 estudios recuperables (52,4 %)**",
         "**67 de los 124 estudios recuperables (54,0 %)**",
         "texto_completo_obtenido / texto_completo_pct"),
    (ES, "Los 59 restantes requieren préstamo interbibliotecario",
         "Los 57 restantes requieren préstamo interbibliotecario",
         "texto_completo_no_obtenido"),
    (ES, "el texto completo se obtuvo para el 52,4 % de los estudios recuperables",
         "el texto completo se obtuvo para el 54,0 % de los estudios recuperables",
         "texto_completo_pct"),
    (ES, "**Tabla 1.** Características del cuerpo de evidencia recuperable (n = 159 estudios).",
         "**Tabla 1.** Características del cuerpo de evidencia recuperable (n = 124 estudios).",
         "estudios_extraibles"),
    (ES, "**Figura 2. Composición del cuerpo de evidencia recuperable (n = 159 estudios).**",
         "**Figura 2. Composición del cuerpo de evidencia recuperable (n = 124 estudios).**",
         "estudios_extraibles"),
    (ES, "*Fuente.* Pre-extracción sistemática desde el resumen de los 159 estudios con publicación recuperable.",
         "*Fuente.* Pre-extracción sistemática desde el resumen de los 124 estudios con publicación recuperable.",
         "estudios_extraibles"),

    (EN, "Full text was obtained for 65 studies (52.4 %)",
         "Full text was obtained for 67 studies (54.0 %)",
         "texto_completo_obtenido / texto_completo_pct"),
    (EN, "from the abstracts of the 159 studies with a retrievable publication, performed",
         "from the abstracts of the 124 studies with a retrievable publication, performed",
         "estudios_extraibles"),
    (EN, "**65 of the 124 retrievable studies (52.4 %)**",
         "**67 of the 124 retrievable studies (54.0 %)**",
         "texto_completo_obtenido / texto_completo_pct"),
    (EN, "The remaining 59 require interlibrary loan",
         "The remaining 57 require interlibrary loan",
         "texto_completo_no_obtenido"),
    (EN, "full text was obtained for 52.4 % of the retrievable studies",
         "full text was obtained for 54.0 % of the retrievable studies",
         "texto_completo_pct"),
    (EN, "**Table 1.** Characteristics of the retrievable evidence base (n = 159 studies).",
         "**Table 1.** Characteristics of the retrievable evidence base (n = 124 studies).",
         "estudios_extraibles"),
    (EN, "**Figure 2. Composition of the retrievable evidence base (n = 159 studies).**",
         "**Figure 2. Composition of the retrievable evidence base (n = 124 studies).**",
         "estudios_extraibles"),
    (EN, "*Source.* Systematic pre-extraction from the abstracts of the 159 studies with a retrievable publication.",
         "*Source.* Systematic pre-extraction from the abstracts of the 124 studies with a retrievable publication.",
         "estudios_extraibles"),
]

# Frases que NO se tocan. Se comprueba que sigan intactas después de escribir:
# si un reemplazo las hubiera pisado, el script lo dice.
INTOCABLES = [
    (ES, "de 159 a 124 estudios con publicación recuperable"),
    (ES, "no consta en el **52,4 %**"),
    (EN, "from 159 to 124 studies with a retrievable publication"),
    (EN, "is not stated in **52.4 %**"),
]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--escribir", action="store_true")
    args = ap.parse_args()

    esc = json.load(open(ESCALARES, encoding="utf-8"))
    print("escalares que mandan:")
    for k in ("texto_completo_obtenido", "texto_completo_no_obtenido",
              "texto_completo_pct", "estudios_extraibles"):
        print(f"   {k:30} {esc.get(k)}")
    print()

    texto = {ES: ES.read_text(encoding="utf-8"), EN: EN.read_text(encoding="utf-8")}
    fallos = []
    for archivo, viejo, nuevo, respaldo in CAMBIOS:
        n = texto[archivo].count(viejo)
        if n != 1:
            fallos.append(f"{archivo.name}: {n} apariciones de {viejo[:58]!r}")
            continue
        texto[archivo] = texto[archivo].replace(viejo, nuevo)
        print(f"  {archivo.name[:22]:24} {viejo[:46]:48} -> {nuevo[:34]}")

    for archivo, frase in INTOCABLES:
        if frase not in texto[archivo]:
            fallos.append(f"{archivo.name}: se perdió una frase intocable: {frase!r}")

    if fallos:
        print("\nFALLOS, no se ha escrito nada:")
        for f in fallos:
            print("   " + f)
        sys.exit(1)

    print(f"\n{len(CAMBIOS)} reemplazos, todos únicos. Frases intocables, intactas.")
    if not args.escribir:
        print("(ensayo: añade --escribir)")
        return
    for archivo, t in texto.items():
        archivo.write_text(t, encoding="utf-8")
        print(f"escrito {archivo}")


if __name__ == "__main__":
    main()
