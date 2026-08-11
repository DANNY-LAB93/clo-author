# Cribado asistido — validación

Generado por `scripts/assisted_title_screen.py`.

El clasificador propone una decisión con la misma rúbrica que produjo
las decisiones manuales, y se mide contra ellas. **La única cifra que
decide si puede usarse es el recall sobre ADVANCE**: cuántos registros
que un humano mandó a leer serían descartados por la máquina. El valor
aceptable es cero, no «alto».

Nótese por qué la exactitud no sirve: el 66% del pozo cribado es
excluible, así que un clasificador que respondiera siempre EXCLUDE
acertaría esa proporción sin ser de ninguna utilidad.

| | |
|---|---|
| Registros de validación | 550 |
| ADVANCE manuales | 188 |
| **Perdidos por la máquina** | **8** |
| **Recall sobre ADVANCE** | **95.7%** |
| Estudios ya incluidos perdidos | 1 |
| Mandados a leer de más | 273 |
| Reducción de lectura | 17.6% |

**Veredicto: NO apto para excluir; solo puede ordenar.**

## Registros que la máquina habría perdido

| Posición | Título |
|---|---|
| 112 | Mapping the clinical use of inhaled bacteriophages in respiratory infections caused by multidrug-resistant pat |
| 131 | Case report: Local bacteriophage therapy for fracture-related infection with polymicrobial multi-resistant bac |
| 138 | Bacteriophage Therapy in Intensive Care Units: A Targeted Strategy to Combat Multidrug-Resistant Infections –  |
| 147 | Phage Therapy for Hospital-Acquired Respiratory Bacterial Infections: A Review; [Fagoterapia para infecciones  |
| 189 | Clinical application of customized and non-customized bacteriophage therapy in patients with refractory/resist |
| 276 | The effects of different doses of inhaled bacteriophage therapy for Pseudomonas aeruginosa pulmonary infection |
| 348 | Antibacterial efficacy of lytic phages against multidrug-resistant Pseudomonas aeruginosa infections in bacter |
| 392 | The Potential Utility of Phage Therapy in the Treatment of Periprosthetic Infection Caused by Multidrug-Resist |
