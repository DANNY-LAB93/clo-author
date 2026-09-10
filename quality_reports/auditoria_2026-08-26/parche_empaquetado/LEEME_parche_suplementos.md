# Parche: copia de material suplementario al paquete de envío

Añade a `scripts/build_jsr_submission.py` el paso de copia de anexos que no existía, más
una comprobación de cobertura que avisa si el manuscrito cita un anexo que no viajó.

## Qué contiene

| Fichero | Uso |
|---|---|
| `parche_suplementos.diff` | Parche unificado contra la versión del 23-08 del script |
| `build_jsr_submission_parcheado.py` | El script completo ya parcheado, si prefieres sustituir el fichero |

## Cómo aplicarlo

Desde `clo-author/`, con el parche:

```bash
python -m patch parche_suplementos.diff        # o: patch -p1 < parche_suplementos.diff
python scripts/build_jsr_submission.py
```

O sustituyendo el fichero directamente:

```bash
cp build_jsr_submission_parcheado.py scripts/build_jsr_submission.py
python scripts/build_jsr_submission.py
```

## Qué cambia

Dos añadidos, ninguna modificación ni borrado de lo que ya había. Los pasos de manuscrito,
figuras y tablas quedan intactos.

1. **Constante `SUPLEMENTOS` y lista blanca `PATRON_ANEXO`** (tras la línea 35). El patrón
   admite todo fichero cuyo nombre empiece por `S<dígito>_` o por `00_`.

2. **Bloque de copia a `destino/suplementos/`** (tras la línea 410), seguido de la
   comprobación de cobertura.

## Por qué lista blanca y no lista de exclusión

La carpeta de verificables contiene 21 ficheros y una subcarpeta, y solo 17 de esos ficheros
son material suplementario. Los otros cuatro son renderizados del propio manuscrito
—`manuscrito_es.docx`, `manuscript_en.docx` y sus dos PDF— que viajan en el paquete por su
canal propio; la subcarpeta `figuras y tablas` duplica lo que ya se copia.

Una lista de exclusión habría que mantenerla cada vez que aparezca un fichero nuevo en la
carpeta, y el modo de fallo sería silencioso: un renderizado nuevo se colaría en el paquete
sin que nadie lo note. Con inclusión por patrón, un anexo nuevo entra solo y cualquier otra
cosa queda fuera por defecto.

## Verificación hecha antes de entregarlo

Ejecutado contra un destino de prueba, sin tocar la carpeta de envío:

- **17 ficheros copiados**: los 14 anexos en 15 ficheros (S3 son dos), más el índice y la
  guía del material suplementario.
- **5 excluidos**: los cuatro renderizados del manuscrito y la subcarpeta.
- **Cobertura completa**: los anexos citados en el manuscrito son S0 a S13, y los presentes
  tras el parche son S0 a S13. Sin faltas y sin sobrantes.
- **Sintaxis validada** y los dos pasos previos del script verificados como intactos.
- **El parche no contiene ninguna operación de borrado.**

Sobre la comprobación de cobertura: la expresión que detecta anexos citados está acotada a
dos dígitos. Sin esa restricción, un código de tres o más cifras en el título de una
referencia bibliográfica se leería como anexo inexistente y produciría un aviso falso. Con
la restricción, el recuento sobre el manuscrito actual devuelve solo códigos entre S0 y S13.

## Advertencia de orden

**Este parche no debe aplicarse todavía.** Añadir los anexos al paquete hoy metería en el
envío `S11_concordancia_entre_extractores.pdf` y `S12_resolucion_de_conflictos.pdf` con
cifras desactualizadas, según los bloqueantes 1 y 2 y el punto 4 de
`CORRECCIONES_PENDIENTES.md`. El orden correcto es regenerar el cálculo de concordancia,
corregir la fuente de la estratificación de conflictos, regenerar S11 y S12, y solo después
aplicar este parche y reejecutar el script.
