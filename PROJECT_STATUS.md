# 📌 PROJECT STATUS

![Architecture](https://img.shields.io/badge/Architecture-Modular-success)
![Validation](https://img.shields.io/badge/Validation-Temporal-important)
![Modeling](https://img.shields.io/badge/Modeling-OLS%20%2B%20ML-blue)
![Matching](https://img.shields.io/badge/Matching-75.97%25-yellow)
![Coverage](https://img.shields.io/badge/Coverage-11%20Leagues-success)
![Tracking](https://img.shields.io/badge/Experiment%20Tracking-MLflow-success)
![Dashboard](https://img.shields.io/badge/Dashboard-Streamlit-success)
![DSS](https://img.shields.io/badge/System-Decision%20Support-success)
![Version](https://img.shields.io/badge/version-v1.2.0-blue)

---

# 🧠 Resumen ejecutivo

**Market Value Dynamics and Market Inefficiency Detection in Professional Football** desarrolla una plataforma integral de Football Analytics orientada a scouting, recruitment y soporte a decisiones deportivas.

El proyecto integra:

* Econometría aplicada.
* Machine Learning supervisado.
* Explainable AI.
* Opportunity Detection.
* Risk Assessment.
* Recruitment Intelligence.
* Transfer Strategy Engine.
* Portfolio Optimization.
* Decision Support Systems.

La versión actual incorpora **Sprint 13A — Multi-League Expansion**, una ampliación sistemática de cobertura competitiva orientada a evaluar la robustez metodológica y la capacidad de generalización del sistema en ecosistemas futbolísticos heterogéneos.

La expansión desarrollada durante Sprint 13A incrementa la cobertura desde siete hasta once ligas europeas, elevando el dataset modelizable desde 3.916 hasta 5.527 observaciones jugador-temporada (+41,1%).

Los resultados obtenidos muestran que la ampliación de cobertura no solo incrementa la representatividad del universo analizado, sino que mejora simultáneamente el rendimiento predictivo de los modelos econométricos y de Machine Learning.

Principales contribuciones de Sprint 13A:

* ampliación de cobertura a 11 ligas europeas;
* procesamiento de 43.591 observaciones procedentes de FBref;
* auditoría sistemática de matching por liga y temporada;
* validación externa de la metodología;
* mejora empírica del rendimiento predictivo;
* fortalecimiento de la capacidad de generalización del sistema.

La versión actual representa la evolución desde un sistema de estimación de valor de mercado hacia una plataforma DSS completa orientada a scouting, recruitment y optimización estratégica de fichajes.

---

# 📊 Estado actual

## Dataset

| Métrica                        |                 Valor |
| ------------------------------ | --------------------: |
| Observaciones FBref procesadas |                43.591 |
| Dataset modelizable final      |                 5.527 |
| Cobertura temporal             | 2019-2020 → 2025-2026 |
| Temporadas                     |                     7 |
| Ligas                          |                    11 |
| Combinaciones liga-temporada   |                    77 |
| Match Rate global              |                75,97% |

---

## Modelización

### Benchmark principal (Sprint 13A.1)

| Modelo              |       RMSE |        MAE |         R² |
| ------------------- | ---------: | ---------: | ---------: |
| Growth OLS Temporal |     0.8689 |     0.6989 |     0.5496 |
| Tuned XGBoost       | **0.8525** | **0.6834** | **0.5664** |

### Comparación con versión anterior

| Modelo        | Dataset  |         R² |
| ------------- | -------- | ---------: |
| Tuned XGBoost | 7 ligas  |     0.5414 |
| Tuned XGBoost | 11 ligas | **0.5664** |

Resultados observados:

* mejora de RMSE (-4,1%);
* mejora de MAE (-4,0%);
* mejora de R² (+4,6%);
* mejora consistente en todos los algoritmos evaluados.

La evidencia obtenida sugiere que la ampliación multi-liga aporta información adicional relevante para la estimación del valor de mercado y mejora la capacidad de generalización de la arquitectura analítica.

---

## Evaluación de negocio

| Métrica       | Valor |
| ------------- | ----: |
| Precision@10  |   90% |
| Precision@20  |   90% |
| Precision@50  |   90% |
| Precision@100 |   85% |

---

# 📚 Estado CRISP-DM

## Fases completadas

### Business Understanding

* Problema de scouting definido.
* Objetivos de negocio establecidos.
* Marco de ineficiencias de mercado formulado.

### Data Understanding

* Exploración de fuentes.
* Análisis de calidad.
* Cobertura temporal y competitiva.
* Auditoría multi-liga.

### Data Preparation

* Matching FBref ↔ Transfermarkt.
* Feature Engineering.
* Construcción del panel longitudinal.
* Control de leakage.
* Expansión multi-liga parametrizada.

### Modeling

* Econometric Pipeline.
* Machine Learning Pipeline.
* Experiment Tracking.
* Explainability.
* Validación multi-liga.

### Evaluation

* Validación temporal.
* Evaluación predictiva.
* Evaluación orientada a negocio.
* Validación externa.

### Deployment

* Dashboard interactivo.
* Recruitment Intelligence.
* Transfer Strategy Engine.
* Portfolio Optimization.
* Decision Support System.

---

## Estado actual

```text
Econometric Model
↓
Machine Learning
↓
Opportunity Detection
↓
Risk Assessment
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
↓
Multi-League Expansion
↓
External Validity Assessment
```

---

# 🏗️ Arquitectura actual

```text
Raw Sources
↓
Feature Engineering
↓
Matching Layer
↓
Player Season Panel
↓
Modeling Dataset
↓
Econometric Model
↓
Machine Learning Model
↓
Opportunity Detection
↓
Risk Assessment
↓
Recruitment Intelligence
↓
Transfer Strategy Engine
↓
Portfolio Optimization
↓
Decision Support System
```

---

## Componentes implementados

| Componente                   | Estado |
| ---------------------------- | ------ |
| Data Pipelines               | ✅      |
| Matching Pipeline            | ✅      |
| Feature Engineering          | ✅      |
| Econometric Pipeline         | ✅      |
| Machine Learning Pipeline    | ✅      |
| MLflow Tracking              | ✅      |
| Explainability               | ✅      |
| Opportunity Score            | ✅      |
| Risk Framework               | ✅      |
| Dashboard DSS                | ✅      |
| Recruitment Intelligence     | ✅      |
| Transfer Strategy Engine     | ✅      |
| Scenario Simulator           | ✅      |
| Portfolio Optimization       | ✅      |
| Strategic Recruitment Engine | ✅      |
| Internationalization EN/ES   | ✅      |
| Multi-League Expansion       | ✅      |
| External Validity Assessment | ✅      |
| League Coverage Diagnostics  | ✅      |
| Multi-League Benchmarking    | ✅      |

# ⚙️ Capacidades implementadas

## Estimación de valor de mercado

La plataforma estima el valor esperado de un jugador utilizando modelos econométricos y algoritmos de Machine Learning entrenados sobre datos históricos procedentes de múltiples competiciones europeas.

La arquitectura combina interpretabilidad econométrica y capacidad predictiva avanzada para capturar los principales determinantes del valor de mercado profesional.

---

## Opportunity Detection

Identificación automática de jugadores potencialmente infravalorados mediante comparación entre:

```text
Predicted Market Value
vs
Observed Market Value
```

La diferencia entre ambas magnitudes constituye la base del sistema de detección de ineficiencias de mercado.

---

## Risk Assessment

Evaluación del riesgo asociado a cada recomendación mediante:

* Risk Score.
* Risk Category.
* Opportunity vs Risk Matrix.
* Confidence Framework.

La incorporación de esta capa permite priorizar oportunidades no únicamente por upside potencial sino también por robustez y nivel de incertidumbre.

---

## Recruitment Intelligence

Funcionalidades incorporadas durante Sprint 11:

* Recruitment Board.
* Comparative Player Analysis.
* Candidate Selection System.
* Executive Scouting Workflow.
* Global Search Engine.
* Executive UX Layer.

Esta capa transforma rankings analíticos en herramientas operativas para departamentos deportivos.

---

## Transfer Strategy Engine

Funcionalidades incorporadas durante Sprint 14:

### Portfolio Dataset

* Portfolio Cost.
* Future Asset Score.
* ROI Score.
* Executive Decision Score.

### Optimization Engine

* Programación lineal entera.
* Formulación 0-1 Knapsack.
* Optimización bajo restricciones.

### Scenario Simulator

* Conservative.
* Balanced.
* Aggressive.

### Strategic Recruitment Engine

* Configuración de presupuesto.
* Restricciones posicionales.
* Perfil de riesgo.
* Optimización de cartera.
* Comparación de escenarios.
* Selection Rationale.

---

## Decision Support System

La plataforma integra todas las capas anteriores dentro de un entorno único de soporte a decisiones deportivas.

El sistema permite evolucionar desde la identificación de oportunidades individuales hasta la construcción de estrategias completas de fichajes bajo restricciones reales.

---

# 🔄 Evolución funcional

## Sprint 7

Executive Dashboard

```text
Predicción
↓
Scoring
↓
Ranking
↓
Dashboard
```

---

## Sprint 9

Decision Support Layer

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
```

---

## Sprint 10

Player Intelligence Layer

Incorpora:

* Player Radar.
* Positional Benchmarking.
* Opportunity Score.
* Risk Assessment.

---

## Sprint 11

Recruitment Intelligence Layer

Incorpora:

* Recruitment Board.
* Comparative Analysis.
* Candidate Selection.
* Executive Scouting Workflow.
* Global Search Engine.
* UX Refinement.

---

## Sprint 12

Productization & Internationalization Layer

Incorpora:

* Dashboard Productization.
* EN/ES Internationalization.
* Executive UX Layer.
* Consolidación DSS.

---

## Sprint 13A

Multi-League Expansion

### Objetivo

Evaluar la capacidad de generalización del sistema mediante la expansión de cobertura competitiva y la validación de la metodología en contextos futbolísticos heterogéneos.

### Nuevas ligas incorporadas

* Championship
* Belgian Pro League
* Austrian Bundesliga
* Spanish Segunda División

### Resultados estructurales

| Métrica             |  Valor |
| ------------------- | -----: |
| Ligas               |     11 |
| Temporadas          |      7 |
| Liga-temporada      |     77 |
| Observaciones FBref | 43.591 |
| Dataset modelizable |  5.527 |
| Match Rate global   | 75,97% |

### Resultados predictivos

| Modelo              |   RMSE |    MAE |     R² |
| ------------------- | -----: | -----: | -----: |
| Growth OLS Temporal | 0.8689 | 0.6989 | 0.5496 |
| Tuned XGBoost       | 0.8525 | 0.6834 | 0.5664 |

### Contribuciones

* ampliación de cobertura competitiva;
* parametrización reproducible de pipelines;
* auditoría de matching por liga;
* auditoría de matching por temporada;
* validación temporal multi-liga;
* validación externa de la metodología;
* mejora del rendimiento predictivo.

Sprint 13A constituye la primera validación empírica de la robustez de la metodología fuera del universo inicial de ligas.

---

## Sprint 14

Transfer Strategy Engine

Incorpora:

* Portfolio Dataset.
* Optimization Engine.
* Scenario Simulator.
* Strategic Recruitment Engine.
* Portfolio Optimization.

---

# 🎯 Resultados principales

## Técnicos

* Cobertura ampliada a 11 ligas europeas.
* 43.591 observaciones FBref procesadas.
* 5.527 observaciones modelables.
* 77 combinaciones liga-temporada.
* Arquitectura completamente reproducible.
* Tracking experimental mediante MLflow.
* Diagnóstico sistemático de calidad de matching.
* Auditoría multi-liga automatizada.

---

## Predictivos

### Econometría

Growth OLS Temporal:

* RMSE = 0.8689
* MAE = 0.6989
* R² = 0.5496

### Machine Learning

Tuned XGBoost:

* RMSE = 0.8525
* MAE = 0.6834
* R² = 0.5664

### Hallazgo principal

La expansión multi-liga genera simultáneamente:

* mayor cobertura;
* mayor representatividad;
* mejor capacidad predictiva.

Este resultado constituye una evidencia favorable de validez externa para la metodología propuesta.

---

## Validez externa

Sprint 13A aporta evidencia empírica de que el sistema mantiene e incluso mejora su rendimiento al incorporar:

* ligas principales;
* ligas secundarias;
* mercados de distinto nivel competitivo;
* estructuras salariales heterogéneas;
* perfiles de desarrollo distintos.

La metodología demuestra capacidad de generalización más allá del universo inicial de entrenamiento.

---

## Negocio

* Opportunity Detection validado.
* Precision@K elevada.
* Recruitment Intelligence integrada.
* Portfolio Optimization operativa.
* Strategic Recruitment Engine funcional.
* Plataforma DSS plenamente operativa.

---

# ⚖️ Trade-offs metodológicos

## Interpretabilidad vs rendimiento

```text
Econometría
+
Machine Learning
+
Explainable AI
```

La coexistencia de modelos econométricos e inteligencia artificial permite combinar capacidad explicativa y precisión predictiva.

---

## Cobertura vs calidad

La expansión competitiva se ha realizado manteniendo criterios estrictos de matching y control de calidad.

La mejora observada en los modelos sugiere que el incremento de cobertura ha añadido señal útil sin deteriorar la consistencia metodológica.

---

# ⚠️ Limitaciones actuales

## Datos

* Dependencia de Transfermarkt para valor de mercado.
* Menor cobertura en determinadas ligas secundarias.
* Cobertura desigual en temporadas recientes.
* Posibles limitaciones derivadas de Transfermarkt-Kaggle.
* Ausencia de tracking data.
* Ausencia de event data avanzado.

---

## Modelización

* Posible drift temporal.
* Dependencia de variables observables.
* Limitaciones inherentes al valor de mercado como proxy económico.

---

## Producto

* Ausencia de API de scoring.
* Ausencia de generación automática de informes PDF.
* Dependencia de ejecución local mediante Streamlit.

---

# 🛣️ Roadmap

## TM.1 — Transfermarkt Coverage Audit

Estado:

Backlog futuro.

Objetivo:

Determinar si las limitaciones observadas durante Sprint 13A proceden de:

* Transfermarkt-Kaggle;
* Transfermarkt como fuente original;
* pipeline de extracción.

---

## Sprint 13B

Advanced Data Expansion

### Objetivo

Incrementar la profundidad analítica del sistema mediante nuevas métricas de rendimiento y nuevas fuentes de datos.

### FBref Advanced Metrics

Nuevas familias previstas:

* Shooting
* Passing
* Pass Types
* Goal & Shot Creation
* Possession
* Defensive Actions
* Playing Time

### Understat Integration

Variables previstas:

* xG
* xA
* xGChain
* xGBuildup

### Expected Contributions Layer

* Finishing Efficiency
* Chance Creation Efficiency
* xG Overperformance
* xA Contribution

### Impacto esperado

* mejora del Feature Engineering;
* mejora predictiva;
* enriquecimiento de Player Intelligence;
* fortalecimiento del radar y benchmarking posicional.

---

## Investigación futura

* TabPFN.
* CatBoost.
* Understat.
* Métricas avanzadas FBref.
* xG/xA.
* Tracking Data.
* Optimización multiobjetivo.
* Simulación económica avanzada.
* Evaluación causal de decisiones de fichaje.

---

# 🏁 Conclusión

La versión:

```text
v1.2.0 — Multi-League Expansion
```

representa la consolidación de una arquitectura integral de Football Analytics orientada a scouting, recruitment y soporte avanzado a decisiones deportivas.

La combinación de:

```text
Econometría
+
Machine Learning
+
Explainable AI
+
Opportunity Detection
+
Risk Assessment
+
Recruitment Intelligence
+
Transfer Strategy Engine
+
Portfolio Optimization
+
Decision Support System
```

permite transformar grandes volúmenes de datos futbolísticos en recomendaciones accionables para departamentos deportivos profesionales.

La evolución metodológica del proyecto puede resumirse mediante:

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

Sprint 13A aporta una contribución especialmente relevante al demostrar que la ampliación del universo competitivo mejora simultáneamente la cobertura y el rendimiento predictivo.

Los resultados obtenidos sugieren que la metodología propuesta captura patrones estructurales del mercado de fichajes que permanecen estables a través de ligas y contextos competitivos distintos.

La plataforma ya no se limita a identificar oportunidades de mercado, sino que proporciona una infraestructura analítica completa para apoyar decisiones estratégicas de captación, inversión y planificación deportiva bajo restricciones reales.
