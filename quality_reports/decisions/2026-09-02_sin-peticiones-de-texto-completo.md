# 2026-09-02 — No se pide ningún texto completo a nadie

**Entrada añadida el 2026-10-08, con fecha del hecho.** La decisión se tomó el 2 de septiembre de 2026, pero hasta hoy solo constaba en el mensaje del commit `d57164b` y en CLAUDE.md. `scripts/exclusion_codes.py` remitía a «la decisión del 2026-09-02», y esta entrada existe para que esa referencia lleve a algún sitio. No cambia nada de lo decidido.

## Qué se decidió

Orden de D. Valdiviezo: no se solicitan textos completos por préstamo interbibliotecario ni a los autores de los estudios.

Se borraron `build_request_package.py` y sus tres salidas: `peticion_biblioteca.csv`, `correos_a_autores.txt` y `sin_texto_completo_que_pedir.csv`. Siguen en el historial de git.

## Qué destapó

Los agradecimientos del manuscrito daban las gracias a la biblioteca por gestionar préstamos interbibliotecarios y a los autores que respondieron a las peticiones. **No se había enviado ninguna petición.** El párrafo se eliminó en las dos lenguas.

## Consecuencia

El hueco de texto completo no se mitigó por ninguna vía adicional. Ese mismo día nació el código NOREC, y el 6 de octubre se amplió a NOPDF.

En el protocolo de la fase definitiva (2026-10-07, sección 13), volver a pedir los textos es una decisión que los autores tienen que tomar antes del depósito.
