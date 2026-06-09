# 📊 Decisiones de Modelización

## Objetivo

Este documento recoge las decisiones metodológicas adoptadas durante el desarrollo del sistema y su evolución hasta la release:

```text
v1.2.1 — Advanced Data Expansion
```

El objetivo es justificar las decisiones desde una perspectiva:

* Econométrica.
* Machine Learning.
* Explainability.
* Feature Engineering.
* Evaluación de negocio.
* Football Analytics.
* Validación externa.
* Decision Support Systems.

---

# 🧠 Filosofía de modelización

El proyecto adopta una arquitectura híbrida donde la precisión predictiva no constituye el objetivo final.

La finalidad última es generar recomendaciones accionables para scouting, recruitment y toma de decisiones deportivas.

Arquitectura conceptual:

```text
Modelización
↓
Evaluación
↓
Scoring
↓
Player Intelligence
↓
Recruitment Intelligence
↓
Decision Support System
↓
External Validation
↓
Advanced Data Expansion
```

Principio metodológico:

```text
Maximizar utilidad para scouting
y no únicamente métricas predictivas
```

---

# 📈 Decisiones econométricas

## Estrategia metodológica

La capa econométrica actúa como benchmark interpretable de toda la arquitectura.

Su función principal es:

```text
Explicar
antes de
predecir
```

---

## Modelo oficial

Modelo productivo actual:

```python
log_market_value_eur ~
age +
log_minutes_played +
goals_per90 +
assists_per90 +
growth variables +
advanced football indices +
league FE +
position FE +
season FE
```

---

## Decisiones adoptadas

* Transformación logarítmica del target.
* Efectos fijos por liga.
* Efectos fijos por posición.
* Efectos fijos por temporada.
* Covarianza robusta HC3.
* Validación temporal estricta.
* Inclusión de variables longitudinales.
* Inclusión de métricas avanzadas Sprint 13B.

---

## Modelo oficial

```text
Growth OLS v13B
```

Rol metodológico:

```text
Benchmark interpretable
```

---

## Resultados Sprint 13B

Comparación principal:

| Modelo                |     R² |
| --------------------- | -----: |
| M_A_v13A_base_spec_FE | 0.4505 |
| M_B_v13B_advanced_FE  | 0.4549 |

Resultado:

```text
ΔR² = +0.0044
```

Mejoras adicionales:

* MAE
* RMSE
* AIC
* BIC

---

## Decisión final

Las variables avanzadas aportan capacidad explicativa incremental.

Por tanto:

```text
Growth OLS v13B
=
Benchmark econométrico oficial
```

---

# 🤖 Decisiones de Machine Learning

## Modelos evaluados

Durante el proyecto se evaluaron:

* Random Forest
* HistGradientBoosting
* LightGBM
* XGBoost

---

## Diseño experimental

El pipeline incorpora:

* Validación temporal.
* ColumnTransformer.
* Imputación robusta.
* Escalado.
* Codificación categórica.
* RandomizedSearchCV.
* MLflow.
* Persistencia reproducible.

---

## Evaluación Sprint 13B

Comparación:

```text
Feature Set A (v13A)

vs

Feature Set B (v13B)
```

Resultados:

| Modelo               | Mejora observada |
| -------------------- | ---------------: |
| XGBoost              |          +0.0096 |
| Random Forest        |          +0.0097 |
| HistGradientBoosting |          +0.0144 |
| LightGBM             |          +0.0291 |

---

## Hallazgo metodológico

Todas las arquitecturas mejoran simultáneamente tras incorporar:

* finishing_index_v2
* availability_index
* defensive_activity_index

Este comportamiento reduce el riesgo de dependencia de una única familia de modelos.

---

## Modelo productivo oficial

```text
Tuned XGBoost v13B
```

Rol:

```text
Predicción operativa
```

---

## Justificación

* Mejor equilibrio global entre rendimiento y estabilidad.
* Compatibilidad completa con SHAP.
* Excelente comportamiento out-of-sample.
* Robustez frente a la expansión multi-liga.
* Mejora tras incorporación de métricas avanzadas.

---

## Decisión final

```text
Growth OLS v13B
↓
Interpretabilidad

Tuned XGBoost v13B
↓
Producción
```

La arquitectura mantiene deliberadamente la coexistencia de econometría y Machine Learning.

---

# 🌍 Decisiones de validez externa

## Problema identificado

Hasta Sprint 13A la metodología había sido validada sobre un universo limitado de competiciones.

Pregunta metodológica:

```text
¿La metodología generaliza
más allá del universo original?
```

---

## Diseño experimental

Expansión desde:

```text
7 ligas
↓
11 ligas
```

Nuevas competiciones:

* Championship
* Belgian Pro League
* Austrian Bundesliga
* Segunda División de España

---

## Resultado

Comparación principal:

| Dataset  | R² Tuned XGBoost |
| -------- | ---------------: |
| 7 ligas  |           0.5414 |
| 11 ligas |           0.5664 |

---

## Decisión

La expansión multi-liga queda incorporada permanentemente al proyecto.

Motivos:

* mejora cobertura;
* mejora representatividad;
* mejora capacidad predictiva;
* fortalece validez externa.

---

# 🔍 Explainability

## Decisión principal

```text
SHAP = mecanismo oficial de interpretación
```

---

## Explainability global

Permite identificar:

* Feature Importance.
* SHAP Importance.
* Summary Plots.

Objetivo:

```text
¿Qué variables explican el valor de mercado?
```

---

## Explainability local

Permite explicar:

* drivers positivos;
* drivers negativos;
* estimaciones individuales.

Objetivo:

```text
¿Por qué este jugador aparece
infravalorado?
```

---

## Sprint 13B — Explainability de métricas avanzadas

La incorporación de nuevas variables permitió evaluar explícitamente su contribución.

Resultado principal:

```text
finishing_index_v2
```

aparece como la variable avanzada con mayor relevancia predictiva agregada.

---

## Decisión

Las recomendaciones generadas por el sistema deben ser:

```text
Predictivas
+
Interpretables
+
Defendibles
```

especialmente dentro de contextos profesionales de scouting y recruitment.

# 🎯 Decisiones sobre scoring

Sprint 5 introduce una capa específica para transformar predicciones en señales accionables.

Arquitectura conceptual:

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
Risk Score
```

El objetivo deja de ser únicamente:

```text
¿Qué valor tendrá un jugador?
```

para responder:

```text
¿Qué jugador merece ser analizado?
```

---

## Inefficiency Score

Captura desviaciones entre:

```text
Valor esperado
vs
Valor observado
```

Interpretación:

```text
Mispricing potencial
```

---

## Growth Score

Captura:

* potencial de crecimiento;
* trayectoria reciente;
* revalorización observada;
* señal longitudinal.

---

## Confidence Score

Captura:

* calidad de matching;
* robustez de datos;
* estabilidad de observaciones;
* fiabilidad analítica.

---

## Opportunity Score

Implementación conceptual:

```python
0.55 * inefficiency_score_z +
0.25 * growth_score_z +
0.20 * confidence_score_z
```

---

## Decisión metodológica

Priorizar simultáneamente:

```text
Infravaloración
+
Potencial
+
Robustez
```

en lugar de utilizar únicamente diferencias entre valor observado y valor esperado.

---

# ⚠️ Risk Framework

Introducido durante Sprint 10.

Problema identificado:

```text
Alta oportunidad
≠
Recomendación segura
```

---

## Decisión

Incorporar explícitamente:

```text
Risk Score
```

como dimensión independiente.

---

## Objetivo

Cuantificar incertidumbre asociada a cada recomendación.

---

## Resultado

```text
Opportunity Score
+
Risk Score
=
Priorización más realista
```

La arquitectura evoluciona desde una lógica puramente ofensiva de upside hacia una lógica riesgo-retorno.

---

# ⚽ Player Intelligence

Introducida durante Sprint 10.

Problema identificado:

```text
Ranking
≠
Comprensión del jugador
```

---

## Decisión

Incorporar:

* Player Radar
* Positional Benchmarking
* Scouting Narrative

---

## Objetivo

Transformar rankings analíticos en perfiles interpretables.

---

## Resultado

```text
Player Intelligence Layer
```

Esta capa constituye la transición desde analítica descriptiva hacia inteligencia deportiva aplicada.

---

# 🎯 Recruitment Intelligence

Introducida durante Sprint 11.

Problema identificado:

```text
Análisis individual
≠
Proceso real de recruitment
```

---

## Decisión

Incorporar:

* Recruitment Board
* Candidate Selection System
* Comparative Player Analysis
* Executive Scouting Workflow

---

## Resultado

```text
Recruitment Intelligence Layer
```

La plataforma deja de responder únicamente a preguntas analíticas y comienza a soportar procesos reales de captación de talento.

---

# 🖥️ Decision Support System

Consolidado durante Sprint 12.

Problema identificado:

```text
Capacidad analítica
≠
Adopción por usuarios finales
```

---

## Decisión

Incorporar:

* Global Search Engine
* UX Redesign
* Search Suggestions
* Active Filters Context
* Internationalization EN/ES
* Executive Workflow

---

## Resultado

```text
Decision Support System
```

La arquitectura se consolida como plataforma DSS orientada a scouting y recruitment.

---

# 📊 Decisiones de evaluación

El proyecto adopta una visión más amplia que la evaluación predictiva tradicional.

---

## Métricas técnicas

* RMSE
* MAE
* R²

---

## Métricas de negocio

* Precision@K
* Positive ROI Rate
* Ranking Quality
* Prioritization Metrics

---

## Decisión metodológica

```text
Un modelo útil
no es únicamente
el que predice mejor

sino el que genera
mejores decisiones
```

---

## Resultados actuales

|   K | Precision@K |
| --: | ----------: |
|  10 |        0.90 |
|  20 |        0.90 |
|  50 |        0.90 |
| 100 |        0.85 |

Estos resultados continúan respaldando la utilidad operativa de la metodología.

---

# 🔄 Historical Evaluation Layer

Objetivo:

Separar evaluación metodológica de explotación operativa.

---

## Funciones

* Comparación de modelos.
* Validación temporal.
* Backtesting.
* Evaluación académica.
* Validación externa.

---

## Contribución

```text
Evaluación histórica
≠
Scouting operativo
```

Esta separación se consolida definitivamente durante Sprint 10.3 y permanece vigente en la arquitectura actual.

---

# ⚖️ Trade-offs metodológicos

| Trade-off                            | Decisión                |
| ------------------------------------ | ----------------------- |
| Interpretabilidad vs precisión       | OLS + XGBoost           |
| Econometría vs ML                    | Arquitectura híbrida    |
| Cobertura vs matching estricto       | Priorizar calidad       |
| Complejidad vs reproducibilidad      | Modularización          |
| Métrica técnica vs utilidad          | Precision@K             |
| Ranking automático vs scout          | Sistema de apoyo        |
| Evaluación histórica vs operación    | Separación explícita    |
| Expansión multi-liga vs consistencia | Validación externa      |
| Nuevas variables vs sobreajuste      | Validación multi-modelo |
| Precisión vs explicabilidad          | SHAP                    |

---

# 🛡️ Prevención de leakage

Controles implementados:

* validación temporal;
* separación train/test;
* exclusión de variables futuras;
* scoring posterior a predicción;
* persistencia independiente;
* separación Historical Evaluation Layer / Current Scouting Layer.

---

## Principio

```text
Toda variable utilizada como input
debe existir en el momento real
de la decisión.
```

---

# ⚠️ Decisión sobre integración de scoring v13B

Durante Sprint 13B se intentó integrar la nueva capa de modelización dentro del pipeline histórico de scoring.

---

## Hallazgo

Se identifica una separación estructural entre:

```text
Modeling Pipeline
≠
Scoring Pipeline
```

---

## Situación observada

El pipeline histórico requiere variables enriquecidas como:

* market_value_growth_prev
* delta_log_market_value_prev
* growth_index
* career_year
* breakout_indicator
* matching_confidence

Mientras que la capa productiva v13B genera principalmente:

* predicted_log_market_value_ml
* predicted_market_value_ml_eur
* inefficiency_score_ml

---

## Decisión

No integrar esta capa dentro de Sprint 13B.

Justificación:

1. No afecta a la hipótesis principal.
2. No altera resultados econométricos.
3. No altera resultados de Machine Learning.
4. Constituye un trabajo de integración independiente.
5. Presenta menor prioridad estratégica que Sprint 14.

---

## Backlog asociado

```text
TM.2 — Scoring & Ranking Integration v13B
```

---

# ⚠️ Limitaciones actuales

## Datos

* Dependencia de Transfermarkt.
* Ausencia de datos salariales.
* Ausencia de datos contractuales.
* Ausencia de tracking data.
* Ausencia de event data avanzado.

---

## Modelización

* Heterogeneidad estructural entre posiciones.
* Posible drift temporal.
* Sensibilidad a cambios estructurales del mercado.
* Dependencia parcial de variables observables.

---

## Evaluación

* Precision@K basada en proxies.
* Ausencia de transferencias observadas.
* Limitaciones históricas de disponibilidad de datos.

---

## Arquitectura

La integración completa entre modelización y scoring permanece pendiente mediante:

```text
TM.2
```

aunque no afecta a la validez metodológica de Sprint 13B.

---

# 🛣️ Roadmap

## TM.1 — Transfermarkt Coverage Audit

Objetivo:

* diagnosticar limitaciones de cobertura;
* estimar techo teórico de matching;
* mejorar integración de datos.

---

## TM.2 — Scoring & Ranking Integration v13B

Objetivo:

```text
Predictions v13B
↓
Scoring Dataset v13B
↓
Opportunity Framework v13B
↓
Rankings v13B
↓
Stability Analysis
```

---

## Sprint 14 — Transfer Strategy Enhancement

Próxima fase principal del proyecto.

Objetivo:

```text
¿Qué combinación de jugadores
maximiza valor esperado
bajo restricciones reales
de presupuesto y riesgo?
```

Líneas de trabajo:

* Transfer Strategy Engine.
* Portfolio Optimization.
* Scenario Simulation.
* Strategic Recruitment.

---

## Investigación futura

### Modelización

* TabPFN.
* CatBoost.
* Ensemble Learning.

### Datos

* Nuevas métricas avanzadas FBref.
* Event Data avanzado.
* Tracking Data.
* Información contractual.
* Datos salariales.

### Football Analytics

* Similarity Engine.
* Career Trajectory Modeling.
* Club Development Intelligence.

---

# 🏁 Conclusión

La principal evolución metodológica del proyecto consiste en transformar una arquitectura centrada en predicción hacia una arquitectura orientada a decisión.

```text
Predicción
↓
Scoring
↓
Player Intelligence
↓
Recruitment Intelligence
↓
Decision Support System
↓
External Validation
↓
Advanced Data Expansion
```

Las decisiones metodológicas más relevantes pueden resumirse en:

### Sprint 2

Las variables longitudinales constituyen una señal fundamental para explicar valor de mercado.

### Sprint 4B

Machine Learning supera consistentemente al benchmark econométrico.

### Sprint 10.3

La separación entre evaluación histórica y scouting operativo mejora la coherencia metodológica.

### Sprint 13A

La expansión multi-liga fortalece la validez externa de la metodología.

### Sprint 13B

Las métricas avanzadas derivadas de FBref aportan capacidad explicativa incremental consistente.

---

## Estado actual

Modelos oficiales:

```text
Growth OLS v13B
↓
Benchmark interpretable

Tuned XGBoost v13B
↓
Modelo productivo
```

---

## Resultado metodológico

La hipótesis principal de Sprint 13B queda validada.

Las variables:

* finishing_index_v2
* availability_index
* defensive_activity_index

aportan mejoras consistentes tanto en econometría como en Machine Learning y pasan a formar parte de la arquitectura productiva oficial.

La release:

```text
v1.2.1 — Advanced Data Expansion
```

consolida una plataforma reproducible, interpretable y orientada a negocio capaz de conectar Football Analytics, Machine Learning y Sports Economics con procesos reales de scouting, recruitment y soporte avanzado a decisiones deportivas.
