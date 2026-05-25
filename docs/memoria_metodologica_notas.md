
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

# Conclusión metodológica global

La evolución del proyecto muestra una transición progresiva desde:

```text
Predicción de valor de mercado
```

hacia:

```text
Sistema analítico reproducible para soporte a decisiones de scouting
```

Contribuciones principales:

- integración multi‑fuente
- matching jerárquico
- panel longitudinal jugador‑temporada
- arquitectura modular reproducible
- comparación econometría vs ML
- explainability mediante SHAP
- scoring multicriterio
- evaluación estadística y de negocio

La principal conclusión metodológica es que la mejora incremental no provino únicamente de algoritmos más complejos, sino de una combinación de:

- conocimiento del dominio
- ingeniería de variables
- validación temporal
- interpretabilidad
- traducción a negocio
