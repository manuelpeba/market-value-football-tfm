# 📌 PROJECT STATUS

![Architecture](https://img.shields.io/badge/Architecture-Modular-success)
![Validation](https://img.shields.io/badge/Validation-Temporal-important)
![Modeling](https://img.shields.io/badge/Modeling-OLS%20%2B%20ML-blue)
![Matching](https://img.shields.io/badge/Matching-88%25-brightgreen)
![Tracking](https://img.shields.io/badge/Experiment%20Tracking-MLflow-success)
![Dashboard](https://img.shields.io/badge/Dashboard-Streamlit-success)
![DSS](https://img.shields.io/badge/System-Decision%20Support-success)
![Version](https://img.shields.io/badge/version-v1.1.0-blue)

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

La versión actual representa la evolución desde un sistema predictivo de valoración de mercado hacia una plataforma DSS orientada a procesos reales de captación y optimización de fichajes.

---

# 📊 Estado actual

## Dataset

| Métrica                  |                 Valor |
| ------------------------ | --------------------: |
| Observaciones integradas |                24.194 |
| Observaciones modelables |                 3.916 |
| Jugadores únicos         |                 2.136 |
| Cobertura temporal       | 2019-2020 → 2025-2026 |
| Ligas                    |                     7 |
| Match Rate               |                   88% |

---

## Modelización

| Modelo        |     R² |
| ------------- | -----: |
| Growth OLS    | 0.5258 |
| Tuned XGBoost | 0.5414 |

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

### Data Preparation

* Matching FBref ↔ Transfermarkt.
* Feature Engineering.
* Construcción del panel longitudinal.
* Control de leakage.

### Modeling

* Econometric Pipeline.
* Machine Learning Pipeline.
* Experiment Tracking.
* Explainability.

### Evaluation

* Validación temporal.
* Evaluación predictiva.
* Evaluación orientada a negocio.

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
Recruitment Intelligence
↓
Transfer Strategy Engine
↓
Portfolio Optimization
↓
Decision Support System
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

---

# ⚙️ Capacidades implementadas

## Estimación de valor de mercado

La plataforma estima el valor esperado de un jugador utilizando modelos econométricos y Machine Learning entrenados sobre datos históricos.

---

## Opportunity Detection

Identificación automática de jugadores potencialmente infravalorados mediante comparación entre:

```text
Predicted Market Value
vs
Observed Market Value
```

---

## Risk Assessment

Evaluación del riesgo asociado a cada recomendación mediante:

* Risk Score.
* Risk Category.
* Opportunity vs Risk Matrix.

---

## Recruitment Intelligence

Funcionalidades incorporadas durante Sprint 11:

* Recruitment Board.
* Comparative Player Analysis.
* Candidate Selection System.
* Executive Scouting Workflow.
* Global Search Engine.
* Executive UX Layer.

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

* Match Rate del 88%.
* Dataset longitudinal multi-fuente.
* Pipeline reproducible.
* Tracking experimental completo.

## Predictivos

* Growth OLS como benchmark interpretable.
* Tuned XGBoost como modelo productivo.

## Negocio

* Opportunity Detection validado.
* Precision@K elevada.
* Recruitment Intelligence integrada.
* Portfolio Optimization operativa.
* Strategic Recruitment Engine funcional.

---

# ⚖️ Trade-offs metodológicos

## Interpretabilidad vs rendimiento

```text
Econometría
+
Machine Learning
+
Explainability
```

permitiendo equilibrar capacidad predictiva y justificación analítica.

---

## Cobertura vs calidad

El proyecto prioriza calidad del matching y consistencia temporal frente a maximizar cobertura.

---

# ⚠️ Limitaciones actuales

## Datos

* Dependencia de Transfermarkt para valor de mercado.
* Cobertura limitada a siete ligas europeas.

## Modelización

* Posible drift temporal.
* Dependencia de variables observables.

## Producto

* Ausencia de API de scoring.
* Ausencia de generación automática de informes PDF.

---

# 🛣️ Roadmap

## Sprint 13 — Multi-League Expansion

Ligas candidatas:

* Championship.
* Segunda División española.
* Belgian Pro League.
* Austrian Bundesliga.
* Danish Superliga.

Objetivo:

Ampliar la capacidad de detección de ineficiencias de mercado fuera de las principales ligas europeas.

---

## Sprint 15 — Advanced Recruitment Intelligence

Líneas futuras:

* Benchmarking avanzado.
* Comparación posicional enriquecida.
* Radar multicriterio ampliado.
* Explicabilidad avanzada.

---

## Sprint 16 — Transfer Replacement Engine

Líneas futuras:

* Replacement Analysis.
* Similarity Matching.
* Budget-Constrained Replacements.
* Tactical Compatibility.

---

## Investigación futura

* Incorporación de TabPFN.
* Incorporación de CatBoost.
* Nuevas fuentes de datos deportivas.
* Métricas avanzadas de FBref.
* Tracking data.
* Optimización multiobjetivo.
* Simulación económica de carteras.

---

# 🏁 Conclusión

La versión:

```text
v1.1.0 — Strategic Recruitment & Decision Support System
```

consolida la evolución del proyecto desde un sistema de predicción de valor de mercado hacia una plataforma integral de Football Analytics orientada a scouting, recruitment y soporte a decisiones deportivas.

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

permite transformar datos futbolísticos en recomendaciones accionables para departamentos deportivos profesionales.

La evolución metodológica puede resumirse mediante:

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

La plataforma ya no se limita a detectar oportunidades de mercado, sino que permite apoyar decisiones estratégicas de fichajes bajo restricciones reales de presupuesto, riesgo y necesidades deportivas.


