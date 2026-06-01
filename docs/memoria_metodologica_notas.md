
# Notas metodológicas para memoria TFM

## Objetivo del documento

Este documento centraliza decisiones metodológicas, justificaciones técnicas, resultados experimentales y conclusiones derivadas del desarrollo del sistema analítico para la identificación de jugadores infravalorados en el mercado de fichajes europeo.

Su propósito es servir como base para la redacción final de la memoria académica, manteniendo trazabilidad entre hipótesis, implementación, evaluación y decisiones adoptadas.

---

# Metodología general

El proyecto sigue una adaptación de CRISP‑DM:

1. Comprensión de negocio
2. Comprensión de datos
3. Preparación de datos
4. Modelización
5. Evaluación
6. Despliegue

La ejecución fue iterativa:

```text
Hipótesis
↓
Implementación
↓
Evaluación experimental
↓
Aceptación / rechazo
↓
Aprendizaje
↓
Nueva iteración
```

---

# Sprint 1 — Normalización contextual

## Hipótesis

La normalización por posición y competición podría mejorar la capacidad predictiva.

## Variables añadidas

- goals_per90_pos_z
- assists_per90_pos_z
- goals_position_percentile
- assists_position_percentile

Agrupación:

```text
[position_group, league]
```

## Resultados

| Modelo | RMSE | MAE | R² |
|---|---:|---:|---:|
| Baseline OLS |1.0035|0.8130|0.4160|
| Advanced OLS |1.0065|0.8166|0.4148|

## Conclusión

Hipótesis rechazada.

La señal ya parecía parcialmente capturada por efectos fijos.

---

# Sprint 2 — Growth Features

## Hipótesis

El mercado incorpora señales de trayectoria y crecimiento futuro.

## Variables

- market_value_growth_prev
- delta_log_market_value_prev
- age_squared
- career_year
- breakout_indicator

## Resultados

| Modelo | RMSE | MAE | R² |
|---|---:|---:|---:|
| Baseline OLS |1.0035|0.8130|0.4160|
| Growth OLS |0.9046|0.7278|0.5255|

## Conclusión

Hipótesis aceptada.

El mercado no valora únicamente rendimiento actual.

---

# Sprint 3 — Índices compuestos

## Hipótesis

La agregación de métricas futbolísticas podría mejorar rendimiento predictivo.

## Índices

- finishing_index
- playmaking_index
- progression_index
- defensive_index

## Resultados

| Modelo | RMSE | MAE | R² |
|---|---:|---:|---:|
| Growth OLS |0.9046|0.7278|0.5255|
| Growth + índices |0.9046|0.7278|0.5255|

## Conclusión

Hipótesis parcialmente aceptada.

Mayor utilidad interpretativa que predictiva.

---

# Sprint 4 — Machine Learning

## Hipótesis

Modelos no lineales podrían superar OLS.

## Resultados baseline

| Modelo | RMSE | MAE | R² |
|---|---:|---:|---:|
| Random Forest |1.0481|0.8527|0.3599|
| XGBoost |1.0943|0.8801|0.3022|
| LightGBM |1.1078|0.8936|0.2848|

Conclusión:

Hipótesis rechazada para configuración baseline.

---

# Sprint 4B — ML Pipeline mejorado

## Mejoras introducidas

- validación temporal
- preprocessing robusto
- imputación
- One‑Hot Encoding
- RandomizedSearchCV
- MLflow

## Resultados

| Modelo | RMSE | MAE | R² |
|---|---:|---:|---:|
| Growth OLS |0.9046|0.7278|0.5255|
| Tuned XGBoost |0.8753|0.7004|0.5536|

## Conclusión

Hipótesis aceptada.

La mejora existe, aunque moderada.

---

# Sprint 4C — Explainability

## Implementación

- SHAP global
- SHAP local
- importancia de variables
- reportes por jugador

## Conclusión

El sistema deja de responder:

```text
¿Qué jugador aparece infravalorado?
```

para responder:

```text
¿Por qué aparece infravalorado?
```

---

# Sprint 5 — Scoring multicriterio

Arquitectura:

```text
Predicción
↓
Inefficiency Score
↓
Growth Score
↓
Confidence Score
↓
Opportunity Score
↓
Rankings
```

## Fórmula

```python
opportunity_score=(
0.55*inefficiency_score_z+
0.25*growth_score_z+
0.20*confidence_score_z
)
```

Resultados:

| Métrica | Valor |
|---|---:|
| Observaciones scoreadas |1138|
| Targets prioritarios |53|
| Alta prioridad |376|

---

# Sprint 6 — Validación de negocio

## Precision@K

|K|Precision@K|
|---:|---:|
|10|0.90|
|20|0.90|
|50|0.90|
|100|0.85|

## Evaluación añadida

- ranking diagnostics
- ROI simulation
- análisis por liga
- análisis por posición

---

# Sprint 8 — Reserved

## Contexto

Durante la revisión académica intermedia se redefinió la hoja de ruta del proyecto.

Las funcionalidades inicialmente previstas para Sprint 8 fueron absorbidas posteriormente dentro de Sprint 9 con el objetivo de construir una capa única y coherente de soporte a decisiones.

Esto evitó duplicidades entre componentes de visualización, ranking y validación de negocio.

## Decisión metodológica

Se optó por consolidar todos los desarrollos relacionados con consumo de resultados, priorización y apoyo a decisiones dentro de un único sprint de Decision Support.

## Conclusión

Sprint reservado y no ejecutado como fase independiente.

---

# Sprint 9.1 — Executive Scouting Layer

## Objetivo

Transformar el ranking analítico en una herramienta operativa de scouting mediante filtros ejecutivos y segmentación dinámica del universo de jugadores.

## Implementación

Se desarrolló una nueva capa de exploración compuesta por:

- filtros ejecutivos de scouting
- presets de búsqueda
- segmentación por edad
- segmentación por minutos
- segmentación por liga
- segmentación por posición
- segmentación por Opportunity Score
- segmentación por Confidence Score

## Presets implementados

### Exploración completa

Permite analizar la totalidad del universo modelado.

### Perfiles accionables

Filtra jugadores jóvenes con suficiente volumen competitivo y señal estadística robusta.

### Jóvenes élite

Orienta la búsqueda hacia perfiles de máximo potencial futuro.

### Alto upside

Prioriza jugadores con mayor diferencial estimado respecto a su valor actual.

## Resultado

La capa analítica deja de producir únicamente rankings estáticos y permite construir shortlists dinámicas adaptadas a distintos contextos deportivos.

## Conclusión

Sprint 9.1 constituye la transición desde un sistema de scoring hacia una herramienta interactiva de scouting.

---

# Sprint 9.2 — Executive Dashboard & Decision Support Layer

## Objetivo

Construir una capa de Visual Analytics orientada a departamentos de scouting y dirección deportiva.

La finalidad es transformar los resultados analíticos en información accionable para la toma de decisiones.

## Implementación

Se rediseñó completamente la experiencia visual del sistema incorporando:

- matriz Coste vs Upside
- segmentación estratégica de oportunidades
- indicadores ejecutivos
- síntesis automática de hallazgos
- priorización visual de candidatos

## Matriz estratégica Coste vs Upside

Cada jugador se representa mediante una burbuja donde:

```text
Eje X → valor de mercado actual
Eje Y → upside estimado
Tamaño → Opportunity Score
Color → prioridad scouting
```

## Segmentación estratégica

La matriz divide automáticamente el mercado en cuatro zonas:

| Zona                  | Interpretación                            |
| --------------------- | ----------------------------------------- |
| Comprar / priorizar   | Bajo coste y alto upside                  |
| Oportunidades premium | Alto upside con mayor coste               |
| Seguimiento           | Perfiles interesantes para monitorización |
| Menor prioridad       | Menor relación coste-potencial            |

## Hallazgos ejecutivos

Se incorporó una capa de síntesis automática basada en:

* candidatos prioritarios
* oportunidades premium
* Opportunity Score medio
* upside agregado identificado
* liga dominante

## Resultado

La arquitectura evoluciona desde:

```text
Predicción
↓
Scoring
↓
Ranking
```

hacia:

```text
Predicción
↓
Scoring
↓
Ranking
↓
Visual Analytics
↓
Decision Support
↓
Scouting
```

## Conclusión

Sprint 9.2 representa la primera implementación completa de un sistema DSS (Decision Support System) aplicado al mercado de fichajes.

---

# Conclusión metodológica global

La evolución del proyecto muestra una transición progresiva desde:

```text
Predicción de valor de mercado
```

hacia:

```text
Sistema DSS (Decision Support System) para identificación de talento infravalorado.
```

La evolución metodológica siguió cinco etapas principales:

1. Integración y normalización de datos
2. Modelización econométrica
3. Modelización mediante Machine Learning
4. Construcción de un sistema multicriterio de scoring
5. Desarrollo de una capa de soporte a decisiones

Contribuciones principales:

- integración multi-fuente FBref + Transfermarkt
- matching jerárquico reproducible
- panel longitudinal jugador-temporada
- comparación econometría vs Machine Learning
- explainability mediante SHAP
- scoring multicriterio
- validación de negocio mediante Precision@K
- dashboard ejecutivo para scouting
- sistema DSS aplicado al mercado de fichajes

La principal conclusión metodológica es que el valor generado no proviene únicamente de la capacidad predictiva del modelo, sino de la combinación entre conocimiento de dominio, ingeniería de variables, interpretabilidad y traducción de resultados analíticos a decisiones deportivas accionables.
