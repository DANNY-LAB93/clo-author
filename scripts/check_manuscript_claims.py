"""Ata cada cifra reportada a su frase, y falla si la frase se quedó atrás.

EL AGUJERO QUE CIERRA

`check_manuscript_numbers.py` comprueba que toda cifra del manuscrito coincida
con ALGÚN escalar del canal. Es necesario y no es suficiente: el 2026-08-13 el
manuscrito decía que se había obtenido el texto completo de 65 estudios cuando
ya eran 67, y el comprobador lo dio por bueno porque existe otro escalar,
`sin_ambito_de_patogeno`, que vale 65. La cifra estaba mal y pasaba por la
puerta de al lado.

La diferencia es de qué se comprueba. Aquel comprueba pertenencia a un conjunto;
este comprueba que UNA frase concreta lleva EL escalar que le toca. Si el corpus
cambia y la prosa no, aquí salta.

CÓMO SE AÑADE UNA AFIRMACIÓN

Una entrada por frase, con los escalares entre llaves. El formato de los números
se aplica solo: miles con espacio fino, decimales con coma en español y con
punto en inglés, tal como los escribe el manuscrito.

Falla también si una frase aparece más de una vez: dos apariciones significan
que hay dos sitios que actualizar y solo se comprobaría uno.

Uso:
    python scripts/check_manuscript_claims.py
"""
import json
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
ES = ROOT / "paper" / "manuscrito_revision_sistematica.md"
EN = ROOT / "paper" / "manuscript_systematic_review_en.md"
ESCALARES = ROOT / "quality_reports" / "synthesis_scalars.json"

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

# Frases que deben estar, con el escalar que manda en cada hueco.
AFIRMACIONES = [
    # ---- periodo del corpus. No hubo filtro de fecha en la busqueda: el
    # rango es el resultado, no una restriccion, y por eso se ancla.

    (ES, "De {registros_identificados} registros, publicados entre {anio_min} y {anio_max}, quedaron {informes_unicos} informes únicos."),
    (ES, "Pasaron a texto completo {informes_a_texto_completo}, agrupados en {estudios} estudios; {estudios_extraibles} de ellos tienen publicación recuperable."),
    (ES, "Se obtuvo el texto completo de {texto_completo_obtenido} estudios ({texto_completo_pct} %)"),
    (ES, "**{texto_completo_obtenido} de los {estudios_extraibles} estudios recuperables ({texto_completo_pct} %)**"),
    (ES, "Los {texto_completo_no_obtenido} restantes requieren préstamo interbibliotecario"),
    (ES, "el texto completo se obtuvo para el {texto_completo_pct} % de los estudios recuperables"),
    (ES, "El criterio de idioma eliminó {estudios_eliminados_por_idioma} estudios"),
    (ES, "la fracción restante concentra el {comparativos_sin_texto_pct} % de los diseños comparativos"),
    (ES, "Contiene {comparativos_sin_texto} de los {estudios_comparativos} estudios comparativos, el **{comparativos_sin_texto_pct} %**"),
    # La n aparece en dos leyendas, Tabla 1 y Figura 2. Se declaran las dos
    # apariciones a propósito: si un día solo se actualiza una, esto salta.
    (ES, "recuperable (n = {estudios_extraibles} estudios)", 2),
    # Los seis motivos de exclusion por titulo. Se anclan porque esta frase
    # imprimia el desglose del conjunto sin restringir mientras su total salia
    # del conjunto restringido: sumaban 13 456 bajo un total de 13 434.
    (ES, "trabajo de laboratorio o preclínico ({excluidos_titulo_LAB}), organismo distinto sin subgrupo separable ({excluidos_titulo_ORG}), revisión o comentario sin datos primarios ({excluidos_titulo_REV}), no evalúa fagoterapia en pacientes ({excluidos_titulo_OFF}), ámbito veterinario ({excluidos_titulo_VET}) y síntesis secundaria ({excluidos_titulo_SEC})"),
    # Las decisiones que emitio el modelo. Se anclan porque al escribirlas a
    # mano se colo un recuento que duplicaba las filas de la enmienda.
    (ES, "{decisiones_titulo} decisiones de título y {decisiones_resumen} de resumen"),
    (ES, "no puede asignarse en el **{sin_clase_util_pct} %** de los estudios: el {sin_clase_de_resistencia_pct} % no la menciona en absoluto y un {clase_mencionada_no_clasificable_pct} % adicional"),
    (ES, "resumen {palabras_resumen_es};"),
    (ES, "texto principal {palabras_cuerpo_es}."),

    (EN, "From {registros_identificados} records, published between {anio_min} and {anio_max}, {informes_unicos} unique reports remained."),
    (EN, "Full-text assessment covered {informes_a_texto_completo} reports, which grouped into {estudios} studies; {estudios_extraibles} of these have a retrievable publication."),
    (EN, "Full text was obtained for {texto_completo_obtenido} studies ({texto_completo_pct} %)"),
    (EN, "**{texto_completo_obtenido} of the {estudios_extraibles} retrievable studies ({texto_completo_pct} %)**"),
    (EN, "The remaining {texto_completo_no_obtenido} require interlibrary loan"),
    (EN, "full text was obtained for {texto_completo_pct} % of the retrievable studies"),
    (EN, "The language criterion removed {estudios_eliminados_por_idioma} studies"),
    (EN, "the remaining fraction concentrates {comparativos_sin_texto_pct} % of the comparative designs"),
    (EN, "It contains {comparativos_sin_texto} of the {estudios_comparativos} comparative studies, **{comparativos_sin_texto_pct} %**"),
    (EN, "base (n = {estudios_extraibles} studies)", 2),
    (EN, "{decisiones_titulo} title decisions and {decisiones_resumen} abstract decisions"),
    (EN, "{decisiones_titulo} title decisions and {decisiones_resumen} abstract decisions"),
    (EN, "cannot be assigned in **{sin_clase_util_pct} %** of studies: {sin_clase_de_resistencia_pct} % do not mention it at all and a further {clase_mencionada_no_clasificable_pct} %"),
    (EN, "abstract {palabras_resumen_en};"),
    (EN, "main text {palabras_cuerpo_en}."),
]


SIN_MILLAR = {"anio_min", "anio_max"}


def formatea(valor, ingles, clave=None):
    """Como los escribe el manuscrito: miles con espacio, decimal con coma o punto."""
    if isinstance(valor, float):
        s = f"{valor:.1f}"
        return s if ingles else s.replace(".", ",")
    if clave in SIN_MILLAR:
        # Un anio no lleva separador de millar: «2 016» no es un anio, es una
        # cantidad. Agruparlo convierte 2016 en algo que ningun lector reconoce.
        return str(valor)
    if isinstance(valor, str):
        # Escalares ya formateados en origen, como la kappa ("0.30"), que
        # lleva dos decimales por convencion y no uno. Solo se ajusta el
        # separador decimal al idioma; el de millar no aplica.
        return valor if ingles else valor.replace(".", ",")
    s = f"{valor:,}".replace(",", " ")          # espacio duro de millar
    return s


def main():
    esc = json.load(open(ESCALARES, encoding="utf-8"))
    textos = {ES: ES.read_text(encoding="utf-8"), EN: EN.read_text(encoding="utf-8")}
    # el manuscrito usa espacio normal o fino indistintamente; se normaliza
    normal = {k: re.sub(r"[   ]", " ", v) for k, v in textos.items()}

    fallos, ok = [], 0
    for entrada in AFIRMACIONES:
        archivo, plantilla = entrada[0], entrada[1]
        veces = entrada[2] if len(entrada) > 2 else 1
        ingles = archivo is EN
        claves = re.findall(r"\{(\w+)\}", plantilla)
        faltan = [c for c in claves if c not in esc]
        if faltan:
            fallos.append(f"{archivo.name}: escalar inexistente {faltan} en «{plantilla[:56]}…»")
            continue
        esperado = plantilla.format(**{c: formatea(esc[c], ingles, c) for c in claves})
        esperado_n = re.sub(r"[   ]", " ", esperado)
        n = normal[archivo].count(esperado_n)
        if n == veces:
            ok += 1
            continue
        if n == 0:
            # ¿está la frase con otro número? Se localiza para poder decirlo.
            molde = re.escape(esperado_n)
            for c in claves:
                molde = molde.replace(re.escape(formatea(esc[c], ingles, c)),
                                      r"([\d  .,]+)")
            hallado = re.search(molde, normal[archivo])
            detalle = (f" -- el manuscrito dice «{hallado.group(0)[:80]}»"
                       if hallado else " -- la frase no aparece en absoluto")
            fallos.append(f"{archivo.name}: DESACTUALIZADA «{esperado_n[:70]}»{detalle}")
        else:
            fallos.append(f"{archivo.name}: la frase aparece {n} veces y se "
                          f"esperaban {veces}: «{esperado_n[:60]}». Si el cambio es "
                          f"legítimo, actualiza el recuento en AFIRMACIONES.")

    print(f"afirmaciones ancladas : {len(AFIRMACIONES)}")
    print(f"al día                : {ok}")
    if not fallos:
        print("\ncada cifra reportada lleva el escalar que le toca")
        return 0
    print(f"\nDESAJUSTES ({len(fallos)}):")
    for f in fallos:
        print("   " + f)
    print("\nArréglalo con: python scripts/sync_manuscript_numbers.py --escribir")
    return 1


if __name__ == "__main__":
    sys.exit(main())
