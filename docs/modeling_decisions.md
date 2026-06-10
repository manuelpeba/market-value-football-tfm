# 📊 Decisiones de Modelización

## Objetivo

Este documento recoge las principales decisiones metodológicas adoptadas durante el desarrollo del sistema y su evolución hasta la release:

```text
v1.2.1 — Transfer Strategy Engine
```

Su finalidad es justificar las decisiones desde una perspectiva de:

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

La finalidad última consiste en generar decisiones deportivas de mayor calidad.

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

Principio metodológico principal:

```text
Maximizar utilidad para scouting
antes que optimizar exclusivamente
métricas predictivas
```

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

---

## Modelo oficial

Especificación productiva:

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

Las métricas avanzadas aportan capacidad explicativa incremental.

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

---

## Justificación

* Mejor equilibrio entre rendimiento y estabilidad.
* Compatibilidad completa con SHAP.
* Excelente comportamiento out-of-sample.
* Robustez frente a expansión multi-liga.
* Mejora consistente tras incorporación de métricas avanzadas.

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

La coexistencia deliberada de econometría y Machine Learning constituye una decisión metodológica central del proyecto.

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
* Segunda División de España

---

## Resultado

| Dataset  | R² Tuned XGBoost |
| -------- | ---------------: |
| 7 ligas  |           0.5414 |
| 11 ligas |           0.5664 |

---

## Decisión

La expansión multi-liga queda incorporada permanentemente al sistema.

Motivos:

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

especialmente en contextos profesionales de scouting y recruitment.

---

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

Sprint 14
↓
Transfer Strategy Engine

Sprint 14.1
↓
Portfolio Optimization
+
Player Level Layer
```

La modelización deja de perseguir exclusivamente la estimación de valor de mercado para convertirse en una herramienta de apoyo a decisiones deportivas bajo restricciones reales de club.

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

Problema identificado:

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

---

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

# 📊 Portfolio Optimization

Introducida durante Sprint 14.

---

## Problema identificado

```text
Mejor jugador individual
≠
Mejor cartera de fichajes
```

Una recomendación óptima a nivel individual no garantiza una combinación óptima a nivel colectivo.

---

## Decisión

Implementar optimización mediante:

```text
Binary Integer Programming
(PuLP)
```

---

## Restricciones implementadas

* presupuesto máximo;
* utilización mínima del presupuesto;
* restricciones posicionales;
* número máximo de fichajes;
* escenarios estratégicos.

---

## Justificación

La formulación mediante Programación Entera Binaria permite modelar de forma explícita restricciones reales de toma de decisiones deportivas.

---

## Resultado

La plataforma evoluciona desde:

```text
Player Selection
```

hacia:

```text
Portfolio Selection
```

alineándose con principios clásicos de Portfolio Optimization.

---

# 🏷️ Player Level Layer

Introducida durante Sprint 14.1.

---

## Problema identificado

```text
Alto ROI
≠
Nivel deportivo suficiente
```

Un jugador puede representar una oportunidad financiera atractiva sin cumplir necesariamente el nivel competitivo requerido por el club.

---

## Decisión

Incorporar una capa explícita de segmentación de calidad.

---

## Niveles implementados

* Development Prospect
* Rotation Profile
* First Team Ready
* Key Player Profile
* Elite Target

---

## Objetivo

Permitir restricciones explícitas de calidad mínima dentro de los procesos de optimización.

---

## Resultado

La plataforma incorpora una dimensión adicional de realismo deportivo dentro de la construcción de carteras.

---

# 🖥️ Decision Support System

Consolidado durante Sprint 12 y ampliado durante Sprint 14.

---

## Problema identificado

```text
Capacidad analítica
≠
Adopción por usuarios finales
```

---

## Decisión

Integrar todas las capas analíticas dentro de un entorno único de soporte a decisiones.

---

## Componentes principales

* Executive Dashboard.
* Player Intelligence.
* Recruitment Intelligence.
* Transfer Strategy Engine.
* Portfolio Optimization.
* EN/ES Internationalization.

---

## Resultado

```text
Decision Support System
```

La arquitectura se consolida como plataforma integral para scouting, recruitment y planificación estratégica de fichajes.

---

# 📊 Decisiones de evaluación

El proyecto adopta una visión más amplia que la evaluación predictiva tradicional.

---

## Métricas técnicas

* RMSE.
* MAE.
* R².

---

## Métricas de negocio

* Precision@K.
* Positive ROI Rate.
* Ranking Quality.
* Portfolio Quality.
* Decision Quality.

---

## Principio metodológico

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

Los resultados continúan respaldando la utilidad operativa de la metodología.

---

# ⚖️ Trade-offs metodológicos

| Trade-off                              | Decisión                |
| -------------------------------------- | ----------------------- |
| Interpretabilidad vs precisión         | OLS + XGBoost           |
| Econometría vs ML                      | Arquitectura híbrida    |
| Cobertura vs matching estricto         | Priorizar calidad       |
| Complejidad vs reproducibilidad        | Modularización          |
| Métrica técnica vs utilidad            | Precision@K             |
| Ranking automático vs scout            | Sistema de apoyo        |
| Evaluación histórica vs operación      | Separación explícita    |
| Expansión multi-liga vs consistencia   | Validación externa      |
| Nuevas variables vs sobreajuste        | Validación multi-modelo |
| Precisión vs explicabilidad            | SHAP                    |
| Selección individual vs cartera óptima | Portfolio Optimization  |

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

Durante Sprint 13B se detectó una separación estructural entre:

```text
Modeling Pipeline
≠
Scoring Pipeline
```

---

## Decisión

No abordar la integración completa dentro de Sprint 13B ni Sprint 14.

Justificación:

1. No afecta a la hipótesis principal.
2. No altera resultados econométricos.
3. No altera resultados de Machine Learning.
4. Constituye un trabajo de integración independiente.
5. Presenta menor prioridad estratégica que Portfolio Optimization.

---

## Backlog asociado

```text
TM.2 — Scoring & Ranking Integration v13B
```

---

# ⚠️ Limitaciones actuales

## Datos

* Dependencia de Transfermarkt.
* Ausencia de información contractual.
* Ausencia de información salarial.
* Ausencia de tracking data.
* Ausencia de event data avanzado.

---

## Modelización

* Heterogeneidad estructural entre posiciones.
* Posible drift temporal.
* Dependencia parcial de variables observables.

---

## Optimización

* Optimización monoobjetivo.
* Restricciones simplificadas.
* Ausencia de simulación dinámica de mercado.

---

## Arquitectura

La integración completa entre modelización y scoring permanece pendiente mediante:

```text
TM.2
```

sin afectar a la validez metodológica de los resultados actuales.

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
Risk Framework v13B
↓
Rankings v13B
```

---

## Sprint 15 — Strategic Optimization Refinement

Objetivo:

Refinar la capa de optimización incorporando:

* simplificación de restricciones estratégicas;
* revisión de escenarios;
* optimización multicriterio;
* evolución del perfil de riesgo;
* mejora de simulación estratégica.

---

## Investigación futura

### Modelización

* TabPFN.
* CatBoost.
* Ensemble Learning.

### Datos

* nuevas métricas avanzadas FBref;
* event data;
* tracking data;
* información contractual;
* datos salariales.

### Football Analytics

* Similarity Engine.
* Career Trajectory Modeling.
* Club Development Intelligence.

### Sports Economics

* Dynamic Asset Valuation.
* Multi-Objective Optimization.
* Portfolio Simulation.

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
Transfer Strategy Engine
↓
Portfolio Optimization
↓
Decision Support System
```

Las decisiones metodológicas más relevantes pueden resumirse mediante:

### Sprint 13A

Validación explícita de validez externa mediante expansión multi-liga.

### Sprint 13B

Validación explícita del valor incremental de métricas avanzadas derivadas de rendimiento futbolístico.

### Sprint 14

Incorporación de Decision Science y Operations Research mediante Transfer Strategy Engine y Portfolio Optimization.

### Sprint 14.1

Incorporación de restricciones explícitas de calidad mediante Player Level Layer.

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

La plataforma ha evolucionado desde un sistema de estimación de valor de mercado hacia un DSS capaz de integrar:

* Football Analytics;
* Sports Economics;
* Machine Learning;
* Explainability;
* Recruitment Analytics;
* Portfolio Optimization;
* Decision Science.

La principal aportación de la arquitectura actual consiste en conectar modelos predictivos con procesos reales de toma de decisiones deportivas bajo restricciones operativas reproducibles y cuantificables.
