# 📊 Decisiones de Modelización

## Objetivo

Este documento recoge las principales decisiones metodológicas adoptadas durante el desarrollo del sistema y su evolución hasta la release:

```text
v1.4.0 — Contract Intelligence Layer
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
* Recruitment Analytics.
* Contract Intelligence.

---

# 🧠 Filosofía metodológica

El proyecto adopta una arquitectura híbrida donde la precisión predictiva no constituye el objetivo final.

La finalidad última consiste en generar decisiones deportivas de mayor calidad mediante la integración de modelización predictiva, evaluación de oportunidades, inteligencia de recruitment, contexto contractual y optimización estratégica.

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
Contract Intelligence
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

En este sentido, TM.3 refuerza la transición desde un sistema de detección de oportunidades hacia una plataforma DSS capaz de incorporar contexto negociador y contractual en procesos de recruitment profesional.

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

## Decisión sobre variables contractuales

Las variables contractuales incorporadas en Sprint TM.3 no se integran dentro de la especificación econométrica oficial.

Decisión:

```text
Contract Intelligence
=
DSS Layer
≠
Historical Modeling Feature
```

Justificación:

* la información contractual disponible procede de un snapshot operativo;
* no existe serie histórica contractual completa y homogénea para todo el panel jugador-temporada;
* incorporar contratos al dataset histórico podría introducir temporal leakage;
* el objetivo de TM.3 es mejorar la toma de decisiones DSS, no reestimar el valor de mercado esperado;
* los modelos econométricos mantienen su función como benchmark interpretable de valoración.

Por tanto, la capa econométrica oficial permanece inalterada tras TM.3.

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

Sprint TM.3 no modifica este modelo. Su contribución se sitúa aguas abajo, en la capa de Decision Support System.

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

## Decisión sobre variables contractuales

Las variables contractuales de Sprint TM.3 no se incorporan al modelo Machine Learning productivo.

Decisión:

```text
Tuned XGBoost v13B
permanece como modelo productivo oficial
sin reentrenamiento contractual
```

Justificación:

* TM.3 no busca mejorar métricas predictivas del valor de mercado;
* la variable contractual disponible pertenece a un snapshot operacional 2025-2026;
* utilizar esta información como predictor histórico podría contaminar la validación temporal;
* la capa contractual se utiliza para enriquecer rankings DSS y no para alterar predicciones de mercado;
* se preserva la comparabilidad de resultados con Sprint 13B y TM.2.

Por tanto, Sprint TM.3 no modifica:

* modelos Machine Learning;
* features de entrenamiento;
* validación temporal;
* métricas productivas;
* artefactos MLflow.

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

## Relación con Sprint TM.3

Sprint TM.3 no reabre la validación externa de modelos porque no modifica la capa predictiva.

La validez de TM.3 se evalúa desde una perspectiva DSS:

* cobertura contractual;
* consistencia de integración;
* ausencia de duplicados;
* coherencia de rankings;
* utilidad operativa para recruitment.

La capa contractual amplía la explotación de los resultados sobre el universo DSS, pero no altera la evidencia predictiva obtenida en Sprint 13A.1 y Sprint 13B.

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

## Relación con Sprint TM.3

Sprint TM.3 no modifica la explainability del modelo predictivo porque la información contractual no entra en el entrenamiento.

La interpretación contractual se sitúa en una capa posterior:

```text
Model Explainability
↓
Opportunity Interpretation
↓
Contract Intelligence
↓
Recruitment Decision
```

Esto permite separar dos planos:

* explicación del valor de mercado esperado;
* explicación de la oportunidad negociadora.

---

## Decisión final

Las recomendaciones generadas por la plataforma deben ser:

```text
Predictivas
+
Interpretables
+
Defendibles
+
Operativamente accionables
```

especialmente en contextos profesionales de scouting, recruitment, negociación contractual y toma de decisiones deportivas.

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

TM.3
↓
Contract Intelligence Layer
```

La modelización deja de perseguir exclusivamente la estimación de valor de mercado para convertirse en una herramienta de apoyo a decisiones deportivas bajo restricciones reales de club.

La incorporación de TM.3 añade una nueva dimensión de decisión relacionada con negociación contractual, leverage de mercado y timing de adquisición.

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

# 📌 MD-015 — Contract Intelligence Layer (Sprint TM.3)

## Problema identificado

Hasta Sprint TM.2 la plataforma era capaz de responder:

```text
¿Qué jugadores parecen infravalorados?
```

y

```text
¿Qué jugadores presentan mejor relación
entre oportunidad y riesgo?
```

Sin embargo, seguía existiendo una limitación operativa importante.

Dos jugadores con Opportunity Score similar pueden presentar condiciones de negociación radicalmente distintas debido a su situación contractual.

Pregunta metodológica:

```text
¿Cómo incorporar contexto contractual
sin comprometer la integridad de la
modelización histórica?
```

---

## Decisión metodológica principal

Implementar una nueva capa:

```text
Contract Intelligence Layer
```

situada entre:

```text
Recruitment Intelligence
↓
Contract Intelligence
↓
Transfer Strategy Engine
```

La nueva capa opera exclusivamente sobre el universo DSS.

---

## Decisión sobre integración de datos

Fuente utilizada:

```text
Transfermarkt
```

Variable contractual disponible:

```text
contract_expiration_date
```

Cobertura obtenida:

```text
95.90%
```

sobre el universo DSS.

---

## Decisión sobre modelización

Las variables contractuales no se incorporan:

* al panel histórico;
* a la econometría;
* al Machine Learning productivo;
* a los experimentos de validación externa.

Justificación:

```text
Evitar temporal leakage
```

La información contractual disponible representa un snapshot operativo y no una serie histórica completa.

Incorporarla dentro de la modelización podría introducir información futura respecto a observaciones históricas.

---

## Decisión sobre arquitectura

Contract Intelligence se implementa como:

```text
DSS Layer
```

y no como:

```text
Modeling Layer
```

Esto permite:

* preservar comparabilidad histórica;
* mantener reproducibilidad experimental;
* evitar reestimaciones innecesarias;
* enriquecer el proceso de recruitment.

---

## Variables implementadas

* contract_expiration_date
* contract_months_remaining
* contract_years_remaining
* contract_expiring_12m
* contract_critical_zone
* free_agent_horizon
* negotiation_leverage_score
* contract_opportunity_score
* contract_status

---

## Contract Opportunity Score

Objetivo:

```text
Cuantificar atractivo contractual
independientemente de la calidad deportiva
del jugador.
```

Dimensiones consideradas:

* proximidad a expiración;
* leverage negociador;
* horizonte de agente libre;
* criticidad contractual.

---

## Recruitment Contract Score

Objetivo:

```text
Combinar oportunidad deportiva
y oportunidad contractual
en una única métrica operativa.
```

Implementación:

```python
0.70 * opportunity_score +
0.30 * contract_opportunity_score
```

---

## Justificación de pesos

| Componente                 | Peso |
| -------------------------- | ---- |
| Opportunity Score          | 70%  |
| Contract Opportunity Score | 30%  |

Principio metodológico:

```text
La calidad deportiva
debe seguir siendo
la señal dominante.
```

La capa contractual complementa la decisión, pero no sustituye la lógica principal de detección de oportunidades.

---

## Decisión sobre Risk Score

Risk Score no se incorpora al Recruitment Contract Score.

Justificación:

* cobertura parcial;
* disponibilidad no homogénea;
* necesidad de mantener consistencia sobre todo el universo DSS.

Esta decisión permite calcular rankings contractuales sobre prácticamente todos los jugadores enriquecidos.

---

## Outputs generados

```text
contract_intelligence_dataset.csv
top_contract_opportunities.csv
top_recruitment_contract_targets.csv
```

---

## Resultado

La arquitectura evoluciona desde:

```text
Opportunity-Based Recruitment
```

hacia:

```text
Opportunity-Based Recruitment
+
Contract-Aware Recruitment
```

aportando una dimensión adicional de decisión alineada con procesos reales de scouting y negociación.

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

---

# 🏁 Conclusión metodológica

La evolución del proyecto puede resumirse mediante:

```text
Market Value Prediction
↓
Opportunity Detection
↓
Risk Assessment
↓
Player Intelligence
↓
Recruitment Intelligence
↓
Contract Intelligence
↓
Transfer Strategy Engine
↓
Portfolio Optimization
↓
Decision Support System
```

La principal decisión metodológica adoptada durante TM.3 consiste en separar explícitamente:

```text
Modelización histórica
≠
Inteligencia contractual operativa
```

preservando la validez científica de los modelos mientras se incrementa significativamente la utilidad práctica del DSS.

La versión v1.4.0 representa la arquitectura metodológica más completa desarrollada durante el proyecto y constituye la base para futuras extensiones relacionadas con UEFA Intelligence, National Team Layer, CatBoost, TabPFN y Health Intelligence.
