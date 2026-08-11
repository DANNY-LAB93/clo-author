# Etapa 1 — cribado por regla, todas las fuentes

Generado por `scripts/screen_stage1_all_sources.py` sobre el corpus
unificado de 17129 informes deduplicados.

## Aplicabilidad y efecto de cada regla

Una regla que no puede leer su campo devuelve NO APLICABLE y el registro
avanza. Un campo ausente no es un hallazgo negativo.

| Regla | Registros que puede juzgar | Excluye |
|---|---|---|
| `rule_no_title` | 17129 (100.0%) | 4 |
| `rule_non_data_doctype` | 17116 (99.9%) | 554 |
| `rule_animal_not_human_scoped` | 9132 (53.3%) | 130 |
| `rule_phage_as_laboratory_tool` | 17129 (100.0%) | 2547 |
| **Total excluidos** | | **3235** |
| **Pasan a etapa 2** | | **13894** |

## Nota sobre la cobertura de las reglas

`rule_animal_not_human_scoped` depende de MeSH, que solo aporta PubMed:
puede juzgar el 53.3% del corpus. Los registros de Scopus, SciELO y los
registros de ensayos no llevan indexación de especie, así que su
condición humana o preclínica se decide en la etapa 2, leyendo.

`rule_non_data_doctype` combina los tipos de publicación de PubMed con
el vocabulario *Document Type* de Scopus. **Conference Paper no se
excluye**: los resúmenes de congreso son justamente donde aparecen
primero los casos de uso compasivo, y excluirlos por regla contradiría
el argumento de esta revisión sobre el sesgo de publicación.

## Control positivo

41 de los 41 estudios ya incluidos están presentes en el corpus y
**ninguna regla excluye a ninguno**. La comprobación sale con error si
eso deja de cumplirse.
