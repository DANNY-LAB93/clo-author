"""Reescribe en el manuscrito las cifras que el canal ha recalculado.

POR QUÉ ES GENÉRICO Y NO UNA LISTA DE REEMPLAZOS

La primera versión llevaba los pares viejo->nuevo escritos a mano. Funcionó una
vez y envejeció al día siguiente: en cuanto entraron dos PDF más, el «65» que
buscaba ya era «67» y el script no encontraba nada que cambiar. Un arreglador
que hay que arreglar cada vez no sirve.

Ahora lee las mismas afirmaciones que vigila `check_manuscript_claims.py`. Cada
una es una frase con los escalares entre llaves. El script la busca en el
manuscrito con los números convertidos en comodines, y si lo que encuentra no
coincide con lo que dicen los escalares de hoy, la reescribe.

Comprobador y arreglador comparten tabla a propósito: si vigilaran listas
distintas, una podría dar por bueno lo que la otra deja sin tocar.

LO QUE SIGUE SIN HACER, Y ES DELIBERADO

Cambia cifras dentro de frases conocidas. No cambia afirmaciones. Si el corpus
crece y una frase pasa a ser falsa por su contenido -- «los cuatro ensayos de
referencia siguen sin leerse», cuando ya se leyeron dos -- eso lo tiene que
reescribir una persona. El script no sabe distinguir un número obsoleto de un
argumento obsoleto, y fingir que sí sería peor que no intentarlo.

Uso:
    python scripts/sync_manuscript_numbers.py [--escribir]
"""
import argparse
import json
import pathlib
import re
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from check_manuscript_claims import (AFIRMACIONES, ES, EN, JSR, ESCALARES,
                                     formatea, valor_de)

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--escribir", action="store_true")
    args = ap.parse_args()

    esc = json.load(open(ESCALARES, encoding="utf-8"))
    # Este script comparte la lista de afirmaciones con check_manuscript_claims,
    # asi que tiene que aplanar los escalares de desenlace igual que aquel. Si
    # no, revienta con KeyError en cuanto una afirmacion cita uno.
    oc = ESCALARES.parent / "outcome_scalars.json"
    if oc.exists():
        O = json.load(open(oc, encoding="utf-8"))
        for k, v in O.items():
            if not isinstance(v, (dict, list)):
                esc["desenlace_" + k] = v
        for campo, d in O["desenlaces"].items():
            for k, v in d.items():
                esc["desenlace_%s_%s" % (campo, k)] = v
        for k, v in O["definicion_exito"].items():
            esc["definicion_" + k] = v
    # Y lo mismo con el riesgo de sesgo, por la misma razon y con el mismo
    # aplanado que hace `check_manuscript_claims`. El aviso de arriba se
    # escribio para los desenlaces y se cumplio al pie de la letra en cuanto
    # llegaron los anclajes de sesgo: `sesgo_comparativos_adjudicados`
    # reventaba el reparador justo cuando el comprobador pedia repararlo.
    rb = ESCALARES.parent / "rob_tabla_estado.json"
    if rb.exists():
        R = json.load(open(rb, encoding="utf-8"))
        for k, v in R.items():
            if not isinstance(v, (dict, list)):
                esc["sesgo_" + k] = v
        for k, v in R.get("por_instrumento", {}).items():
            esc["sesgo_instrumento_%s" % k.replace(" ", "").replace("-", "")] = v
    # Los tres manuscritos. El de JSR se anadio al comprobador el 2026-09-02 y
    # no aqui, asi que sincronizar reventaba con un KeyError en cuanto una
    # afirmacion suya quedaba desactualizada.
    textos = {ES: ES.read_text(encoding="utf-8"), EN: EN.read_text(encoding="utf-8"),
              JSR: JSR.read_text(encoding="utf-8")}

    cambios, fallos = [], []
    for entrada in AFIRMACIONES:
        archivo, plantilla = entrada[0], entrada[1]
        veces = entrada[2] if len(entrada) > 2 else 1
        # El idioma lo declara la propia afirmacion cuando lo trae, porque el
        # manuscrito de JSR lleva los dos dentro. Deducirlo del fichero escribio
        # el abstract ingles con decimales espanoles --"75,8 %" en vez de
        # "75.8 %"-- y lo dejo corrupto hasta que el comprobador lo canto.
        ingles = entrada[3] if len(entrada) > 3 else (archivo is EN)
        claves = re.findall(r"\{(\w+)\}", plantilla)
        esperado = plantilla.format(**{c: valor_de(esc, c, ingles) for c in claves})

        # molde con los números convertidos en comodines
        # El separador de millares del manuscrito no siempre es el mismo
        # caracter: hay espacio fino (U+2009), fino sin salto (U+202F), duro
        # (U+00A0) y normal, segun quien tecleara la frase. El comodin los cubre
        # todos; olvidar uno hace que la frase "no aparezca" y el arreglador
        # calle en vez de arreglar.
        # El molde se arma desde la PLANTILLA, partiendo por los huecos, y no
        # buscando los valores dentro del texto ya escapado.
        #
        # Por que importa: el comodin se escribia como r"[\d\u00a0\u2009...]+",
        # con los escapes literales dentro del patron. Un escalar de UN SOLO
        # DIGITO \u2014por ejemplo 9\u2014 encontraba su "9" dentro de "\u2009", que forma
        # parte del comodin ya insertado, y lo partia en "\u200". El patron
        # quedaba corrupto y `re` fallaba con "incomplete escape". Cualquier
        # escalar de un digito rompia el sincronizador entero.
        #
        # Partiendo la plantilla no se toca ningun valor, y el comodin lleva los
        # espacios como caracteres de verdad y no como escapes con digitos.
        # EL COMODIN NO PUEDE COMERSE LA PUNTUACION. Escrito como una clase
        # "[\d espacios . ,]+" era voraz: en una plantilla que EMPIEZA por un
        # hueco --\u00ab{estudios} studies remain...\u00bb-- el comodin empezaba a casar
        # en el punto de la frase anterior y se tragaba \u00ab. \u00bb, de modo que al
        # sustituir desaparecia el final de la oracion. Asi nacio
        # \u00abwithout being able to read it155 studies remain\u00bb, que viajo en el
        # resumen en ingles hasta que alguien lo leyo.
        #
        # Ahora describe UN NUMERO: digitos, grupos de millar separados por
        # cualquiera de los cuatro espacios que el manuscrito usa, y una parte
        # decimal opcional. Ni un punto ni una coma sueltos al final.
        espacio = "\u00a0\u2009\u202f "
        comodin = r"\d+(?:[" + espacio + r"]\d{3})*(?:[.,]\d+)?"
        # Un hueco «{letras_*}» no casa contra un numero sino contra una
        # palabra: la seccion 3.1.1 escribe «Veinticuatro» y no «24».
        palabra = r"[A-Za-z\u00c1\u00c9\u00cd\u00d3\u00da\u00d1\u00e1\u00e9\u00ed\u00f3\u00fa\u00f1-]+(?: y [a-z\u00e1\u00e9\u00ed\u00f3\u00fa]+)?"
        # Y uno «{lista_*}» o «{coma_*}», contra una lista de identificadores.
        ident = r"EST-\d{3}(?: [A-Z])?"
        lista = ident + r"(?:(?:, | y | and )" + ident + r")*"
        partes = re.split(r"\{(\w+)\}", plantilla)
        molde = "".join(
            re.escape(p) if i % 2 == 0
            else (palabra if p.startswith("letras_")
                  else lista if p.startswith(("lista_", "coma_"))
                  # un «*_desglose» es una frase armada por el canal («4 solo
                  # PubMed y 2 solo...»): casa hasta la raya que la cierra.
                  else r"\d+ solo [^\n—]+" if p.endswith("_desglose") else comodin)
            for i, p in enumerate(partes))
        halladas = [m.group(0) for m in re.finditer(molde, textos[archivo])]

        if not halladas:
            fallos.append(f"{archivo.name}: no encuentro la frase «{esperado[:62]}»")
            continue
        if len(halladas) != veces:
            fallos.append(f"{archivo.name}: la frase aparece {len(halladas)} veces "
                          f"y se esperaban {veces}: «{esperado[:52]}»")
            continue
        # Los millares se escriben con espacio fino, duro o normal segun quien
        # tecleara la frase. Comparar sin normalizar marcaria como obsoleta una
        # cifra correcta escrita con otro espacio.
        igual = lambda s: re.sub("[    ]", " ", s)
        for h in halladas:
            if igual(h) != igual(esperado):
                textos[archivo] = textos[archivo].replace(h, esperado)
                cambios.append((archivo.name, h.strip(), esperado.strip()))

    if fallos:
        print("FALLOS, no se ha escrito nada:")
        for f in fallos:
            print("   " + f)
        return 1

    if not cambios:
        print("todas las cifras del manuscrito ya coinciden con los escalares")
        return 0

    print(f"cifras desactualizadas: {len(cambios)}")
    for arch, viejo, nuevo in cambios:
        print(f"\n   {arch}")
        print(f"      dice  : {viejo[:96]}")
        print(f"      debe  : {nuevo[:96]}")

    if not args.escribir:
        print("\n(ensayo: añade --escribir)")
        return 0
    for archivo, t in textos.items():
        archivo.write_text(t, encoding="utf-8")
    print(f"\nescritos los dos manuscritos")
    return 0


if __name__ == "__main__":
    sys.exit(main())
