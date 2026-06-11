# 📊 Decisiones de Modelización

## Objetivo

Este documento recoge las principales decisiones metodológicas adoptadas durante el desarrollo del sistema y su evolución hasta la release:

```text
v1.2.2 — Transfer Strategy Engine + Multi-League DSS Integration
```

Su finalidad es justificar formalmente las decisiones tomadas desde una perspectiva de:

* Econometría aplicada.
* Machine Learning.
* Explainability.
* Feature Engineering.
* Sports Economics.
* Football Analytics.
* Validación externa.
* Decision Science.
* Operations Research.
* Decision Support Systems.

---

# 🧠 Filosofía metodológica

El proyecto adopta una arquitectura híbrida donde la precisión predictiva no constituye el objetivo final.

La finalidad última consiste en generar decisiones deportivas de mayor calidad mediante la integración de modelización predictiva, evaluación de oportunidades y optimización estratégica.

La arquitectura conceptual puede resumirse mediante:

```text
Data
↓
Modeling
↓
Evaluation
↓
Scoring
↓
Player Intelligence
↓
Recruitment Intelligence
↓
Transfer Strategy Engine
↓
Portfolio Optimization
↓
Decision Support System
```

Principio metodológico central:

```text
Maximizar utilidad para scouting
antes que optimizar exclusivamente
métricas predictivas
```

La calidad de una solución no se evalúa únicamente por su capacidad explicativa o predictiva, sino por su capacidad para mejorar procesos reales de toma de decisiones deportivas.

---

# 📈 Decisiones econométricas

## Rol de la econometría

La capa econométrica actúa como benchmark interpretable de toda la arquitectura.

Su función principal es:

```text
Explicar
antes de
predecir
```

La econometría proporciona una referencia interpretable frente a modelos de mayor complejidad y permite validar la coherencia económica y deportiva de los resultados obtenidos.

---

## Especificación oficial

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

Rol:

```text
Benchmark interpretable
```

---

## Resultado Sprint 13B

| Modelo                |     R² |
| --------------------- | -----: |
| M_A_v13A_base_spec_FE | 0.4505 |
| M_B_v13B_advanced_FE  | 0.4549 |

Resultado:

```text
ΔR² = +0.0044
```

---

## Decisión final

Las métricas avanzadas aportan capacidad explicativa incremental sin comprometer la interpretabilidad.

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

Este comportamiento reduce significativamente el riesgo de dependencia de una única familia de modelos.

---

## Modelo productivo oficial

```text
Tuned XGBoost v13B
```

Rol:

```text
Production Prediction Engine
```

Resultado productivo:

```text
RMSE = 0.9639
MAE  = 0.7777
R²   = 0.4453
```

Referencia histórica de validación externa:

```text
Sprint 13A.1
Tuned XGBoost

RMSE = 0.8525
MAE  = 0.6834
R²   = 0.5664
```

Este resultado constituye el mejor rendimiento predictivo alcanzado durante el proyecto y la principal evidencia de capacidad de generalización multi-liga de la metodología desarrollada.

---

## Justificación

* Mejor equilibrio entre rendimiento y estabilidad.
* Compatibilidad completa con SHAP.
* Excelente comportamiento out-of-sample.
* Robustez frente a expansión multi-liga.
* Mejora consistente tras incorporación de métricas avanzadas.

---

## Decisión

La expansión multi-liga queda incorporada permanentemente al sistema.

Justificación:

* mayor cobertura;
* mayor representatividad;
* mejora predictiva;
* fortalecimiento de validez externa.

Resultado principal:

| Dataset  | R² Tuned XGBoost |
| -------- | ---------------: |
| 7 ligas  |           0.5414 |
| 11 ligas |           0.5664 |

La validación externa multi-liga constituye una de las evidencias metodológicas más sólidas del proyecto, demostrando que la ampliación de cobertura no reduce la capacidad predictiva del sistema y permite mejorar su capacidad de generalización.


---

# 🌍 Decisiones de validez externa

## Problema identificado

Hasta Sprint 13A la metodología había sido validada sobre un universo limitado de competiciones.

Pregunta metodológica:

```text
¿La metodología mantiene rendimiento
fuera del universo competitivo original?
```

---

## Diseño experimental

Expansión:

```text
7 ligas
↓
11 ligas
```

Competiciones incorporadas:

* Championship
* Belgian Pro League
* Austrian Bundesliga
* Spanish Segunda División

---

## Resultado

| Dataset  | R² Tuned XGBoost |
| -------- | ---------------: |
| 7 ligas  |           0.5414 |
| 11 ligas |           0.5664 |

---

## Decisión

La expansión multi-liga queda incorporada permanentemente al sistema.

Justificación:

* mayor cobertura;
* mayor representatividad;
* mejora predictiva;
* fortalecimiento de validez externa.

---

# 🔍 Explainability

## Decisión principal

```text
SHAP
=
Mecanismo oficial de interpretación
```

---

## Explainability global

Permite identificar:

* Feature Importance.
* SHAP Importance.
* Summary Plots.

Pregunta objetivo:

```text
¿Qué variables explican
el valor de mercado?
```

---

## Explainability local

Permite explicar:

* drivers positivos;
* drivers negativos;
* estimaciones individuales.

Pregunta objetivo:

```text
¿Por qué este jugador aparece
como oportunidad de mercado?
```

---

## Sprint 13B — Explainability de métricas avanzadas

La incorporación de nuevas variables permitió evaluar explícitamente su contribución.

Hallazgo principal:

```text
finishing_index_v2
```

aparece como la variable avanzada con mayor relevancia predictiva agregada.

---

## Decisión final

Las recomendaciones generadas por la plataforma deben ser:

```text
Predictivas
+
Interpretables
+
Defendibles
```

especialmente en contextos profesionales de scouting, recruitment y toma de decisiones deportivas.

# 🧩 Evolución metodológica

La evolución conceptual del proyecto puede resumirse mediante:

```text
Sprint 4
↓
Predicción

Sprint 10
↓
Player Intelligence

Sprint 11
↓
Recruitment Intelligence

Sprint 13A
↓
Multi-League Expansion

Sprint 13B
↓
Advanced Football Metrics

Sprint 14
↓
Transfer Strategy Engine

Sprint 14.1
↓
Portfolio Optimization
+
Player Level Layer

TM.2
↓
Multi-League DSS Integration
```

La modelización deja de perseguir exclusivamente la estimación de valor de mercado para convertirse en una herramienta de apoyo a decisiones deportivas bajo restricciones reales de club.

---

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

# 📌 MD-014 — Multi-League DSS Consistency (Sprint TM.2)

## Problema identificado

Tras Sprint 13A y Sprint 13B, la cobertura de modelización había sido ampliada a once competiciones europeas.

Sin embargo, parte de la capa DSS seguía operando sobre artefactos heredados construidos sobre la versión anterior de siete ligas.

Situación observada:

```text
Modeling Layer
↓
11 ligas

Scoring / Ranking DSS
↓
7 ligas
```

---

## Decisión metodológica

Implementar una capa explícita de reintegración de variables dentro del pipeline de scoring.

Arquitectura resultante:

```text
Predictions
↓
Scoring Feature Reintegration
↓
Growth Score
↓
Confidence Score
↓
Opportunity Score
↓
Ranking Engine
↓
Transfer Strategy Engine
```

---

## Implementación

La reintegración utiliza claves compuestas:

```text
player_id_tm
+
season
+
league
+
club
```

e incorpora controles explícitos de:

* integridad de filas;
* unicidad de claves;
* validación many-to-one;
* compatibilidad hacia atrás.

---

## Resultado

Cobertura final:

```text
Modeling Layer
↓
11 ligas

Scoring Layer
↓
11 ligas

Opportunity Layer
↓
11 ligas

Ranking Engine
↓
11 ligas

Transfer Strategy Engine
↓
11 ligas

Decision Support System
↓
11 ligas
```

---

## Justificación

La decisión permite:

* mantener reproducibilidad;
* evitar reentrenamientos innecesarios;
* preservar la metodología validada;
* garantizar consistencia arquitectónica de extremo a extremo.

---

## Impacto

Sprint TM.2 no modifica:

* modelos econométricos;
* modelos Machine Learning;
* lógica de scoring;
* métricas de evaluación.

Su contribución consiste exclusivamente en asegurar la propagación completa de la expansión multi-liga hasta la capa operativa DSS.

---

# ⚠️ Risk Framework

Introducido durante Sprint 10.

## Problema identificado

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

## Problema identificado

```text
Ranking
≠
Comprensión del jugador
```

---

## Decisión

Incorporar:

* Player Radar.
* Positional Benchmarking.
* Opportunity vs Risk Matrix.
* Scouting Narrative.

---

## Resultado

```text
Player Intelligence Layer
```

Esta capa constituye la transición desde analítica descriptiva hacia inteligencia deportiva aplicada.

---

# 🎯 Recruitment Intelligence

Introducida durante Sprint 11.

## Problema identificado

```text
Análisis individual
≠
Proceso real de recruitment
```

---

## Decisión

Incorporar:

* Recruitment Board.
* Candidate Selection System.
* Comparative Player Analysis.
* Executive Scouting Workflow.

---

## Resultado

```text
Recruitment Intelligence Layer
```

La plataforma deja de responder únicamente preguntas analíticas y comienza a soportar procesos reales de captación de talento.

---

# 🧠 Transfer Strategy Engine

Introducido durante Sprint 14.

## Problema identificado

Hasta Sprint 13 la plataforma respondía principalmente:

```text
¿Qué jugadores parecen infravalorados?
```

Sin embargo, los departamentos deportivos no fichan jugadores de forma aislada.

Las decisiones reales se producen bajo restricciones simultáneas de:

* presupuesto;
* posiciones necesarias;
* calidad mínima;
* número de incorporaciones;
* perfil estratégico.

---

## Decisión metodológica

Incorporar una nueva capa de optimización estratégica capaz de responder:

```text
¿Qué combinación de jugadores
maximiza el valor esperado
bajo restricciones reales de club?
```

---

## Inputs estratégicos

* Budget.
* Positions Needed.
* Scenario.
* Portfolio Style.
* Maximum Signings.

---

## Outputs estratégicos

* Recommended Portfolio.
* Total Cost.
* Budget Utilization.
* Expected Upside.
* Expected ROI.
* Average Portfolio Score.

---

## Contribución

Sprint 14 introduce formalmente conceptos procedentes de:

* Decision Science.
* Operations Research.
* Strategic Recruitment Analytics.

representando la principal evolución conceptual del proyecto.
