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

**Market Value Dynamics and Market Inefficiency Detection in Professional Football** desarrolla una plataforma integral de Football Analytics orientada a la identificación de jugadores infravalorados en el mercado europeo de fichajes.

El proyecto integra:

* Econometría aplicada.
* Machine Learning supervisado.
* Explainable AI.
* Opportunity Detection.
* Risk Assessment.
* Recruitment Intelligence.
* Decision Support Systems.

La versión actual representa la evolución desde un sistema predictivo de valoración de mercado hacia una plataforma DSS orientada a scouting y recruitment profesional.

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
* Visual Analytics.
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
Decision Support System
```

---

## Componentes implementados

| Componente                 | Estado |
| -------------------------- | ------ |
| Data Pipelines             | ✅      |
| Matching Pipeline          | ✅      |
| Feature Engineering        | ✅      |
| Econometric Pipeline       | ✅      |
| Machine Learning Pipeline  | ✅      |
| MLflow Tracking            | ✅      |
| Explainability             | ✅      |
| Opportunity Score          | ✅      |
| Risk Framework             | ✅      |
| Dashboard DSS              | ✅      |
| Recruitment Intelligence   | ✅      |
| Internationalization EN/ES | ✅      |

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

### Recruitment Board

* Construcción dinámica de shortlists.
* Selección múltiple de candidatos.
* Vista ejecutiva de recruitment.

### Comparative Player Analysis

Comparación simultánea de:

* Opportunity Score.
* Risk Score.
* Confidence Score.
* Market Value.
* Predicted Value.
* Mispricing.

### Candidate Selection System

* Selección multijugador.
* Comparación dinámica.
* Priorización operativa.

---

## Decision Support System

Funcionalidades incorporadas durante Sprint 12:

### Advanced Search Engine

Búsqueda por:

* Jugador.
* Club.
* Liga.
* Posición.

### UX Improvements

* Rediseño de filtros.
* Search Suggestions.
* Search Chips.
* Range Sliders mejorados.

### Internationalization

Dashboard bilingüe:

* Español.
* Inglés.

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

---

## Sprint 12

Productization, UX & Internationalization Layer

Incorpora:

* Advanced Search.
* UX Redesign.
* EN/ES Internationalization.
* Dashboard Productization.

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
* Scouting workflows operativos.
* Recruitment Intelligence integrada.

---

# ⚖️ Trade-offs metodológicos

## Interpretabilidad vs rendimiento

La arquitectura combina:

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
* Segunda División.
* Belgian Pro League.

Objetivo:

Ampliar la capacidad de detección de ineficiencias en mercados de desarrollo de talento.

---

## Sprint 14 — Transfer Strategy Engine

Líneas futuras:

* Replacement Analysis.
* Portfolio Construction.
* Investment Optimization.
* Transfer Strategy Simulation.

---

# 🏁 Conclusión

La versión v1.1.0 consolida la evolución del proyecto desde un sistema de predicción de valor de mercado hacia una plataforma integral de apoyo a decisiones para scouting y recruitment.

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
Decision Support System
```

permite transformar datos futbolísticos en recomendaciones accionables para departamentos deportivos profesionales.

