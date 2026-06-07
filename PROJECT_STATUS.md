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

La versión actual incorpora **Sprint 13A — Multi-League Expansion**, una ampliación de cobertura competitiva orientada a evaluar la validez externa de la metodología en ecosistemas futbolísticos distintos.

Sprint 13A no modifica los modelos predictivos, el scoring multicriterio, la explainability ni la lógica de recruitment implementada previamente.

Su principal contribución consiste en:

* ampliar la cobertura a 11 ligas europeas;
* procesar 43.591 observaciones procedentes de FBref;
* parametrizar los pipelines para generar artefactos reproducibles versionados;
* auditar la calidad de matching por liga y temporada;
* evaluar limitaciones de cobertura en fuentes de mercado.

La versión actual representa la evolución desde un sistema predictivo de valoración de mercado hacia una plataforma DSS orientada a procesos reales de captación, optimización y planificación estratégica de fichajes.

---

# 📊 Estado actual

## Dataset

| Métrica                        |                 Valor |
| ------------------------------ | --------------------: |
| Observaciones FBref procesadas |                43.591 |
| Cobertura temporal             | 2019-2020 → 2025-2026 |
| Temporadas                     |                     7 |
| Ligas                          |                    11 |
| Combinaciones liga-temporada   |                    77 |
| Match Rate global              |                75,97% |

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
| External Validity Audit      | ✅      |
| League Coverage Diagnostics  | ✅      |

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

## Sprint 13A

Multi-League Expansion

Objetivo:

Evaluar la generalización de la metodología a ecosistemas competitivos distintos mediante una ampliación de cobertura y una auditoría sistemática de calidad de matching.

Nuevas ligas incorporadas:

* Championship.
* Belgian Pro League.
* Austrian Bundesliga.
* Spanish Segunda División.

Resultados:

| Métrica                      |  Valor |
| ---------------------------- | -----: |
| Ligas                        |     11 |
| Temporadas                   |      7 |
| Combinaciones liga-temporada |     77 |
| Observaciones FBref          | 43.591 |
| Match Rate global            | 75,97% |

Contribuciones:

* ampliación de cobertura competitiva;
* parametrización reproducible de pipelines;
* auditoría de matching por liga;
* auditoría de matching por liga-temporada;
* evaluación de validez externa.

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
* 77 combinaciones liga-temporada.
* Pipeline reproducible y parametrizable.
* Tracking experimental mediante MLflow.
* Diagnóstico sistemático de calidad de matching.

---

## Predictivos

* Growth OLS como benchmark interpretable.
* Tuned XGBoost como modelo productivo.
* R² superior a 0.54 en el modelo final.
* Rendimiento predictivo mantenido tras la expansión de cobertura.

---

## Validez externa

* Generalización evaluada en ligas principales y secundarias.
* Incorporación de mercados con estructuras competitivas distintas.
* Diagnóstico de cobertura por liga.
* Evidencia de limitaciones de cobertura en Transfermarkt-Kaggle para determinadas ligas secundarias y temporadas recientes.

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
Explainability
```

permitiendo equilibrar capacidad predictiva y justificación analítica.

---

## Cobertura vs calidad

El proyecto prioriza calidad del matching y consistencia temporal frente a maximizar cobertura.

La expansión a nuevas ligas incrementa la representatividad del universo analizado, aunque introduce retos adicionales de cobertura y disponibilidad de datos.

---

# ⚠️ Limitaciones actuales

## Datos

* Dependencia de Transfermarkt para valor de mercado.
* Menor cobertura en determinadas ligas secundarias.
* Menor cobertura en temporadas recientes para algunas competiciones.
* Posibles limitaciones de cobertura en Transfermarkt-Kaggle.
* Ausencia de tracking data y datos event-based avanzados.

---

## Modelización

* Posible drift temporal.
* Dependencia de variables observables.
* Limitaciones inherentes a la estimación de valor de mercado como proxy de valoración económica.

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

* Transfermarkt-Kaggle.
* Transfermarkt como fuente original.
* Pipeline de extracción.

Esta investigación no forma parte de Sprint 13A.

---

## Sprint 13B

Advanced Data Expansion

Objetivo:

Incrementar la profundidad analítica del sistema mediante la incorporación de métricas avanzadas de rendimiento y nuevas fuentes de datos futbolísticos.

Líneas de trabajo previstas:

### FBref Advanced Metrics

Incorporación de variables procedentes de tablas avanzadas de FBref:

* Shooting
* Passing
* Pass Types
* Goal & Shot Creation
* Possession
* Defensive Actions
* Playing Time

Objetivos:

* enriquecer el Feature Engineering;
* mejorar capacidad predictiva;
* fortalecer la capa de Player Intelligence;
* ampliar el Positional Benchmarking.

---

### Understat Integration

Incorporación de métricas basadas en expected goals.

Variables previstas:

* xG
* xA
* xGChain
* xGBuildup

Objetivos:

* capturar calidad de acciones ofensivas;
* mejorar evaluación de talento emergente;
* incorporar señal independiente de la producción observada.

---

### Expected Contributions Layer

Nueva familia de indicadores orientados a medir contribución subyacente.

Ejemplos:

* Finishing Efficiency
* Chance Creation Efficiency
* xG Overperformance
* xA Contribution

---

### Advanced Scouting Intelligence

Mejoras previstas:

* radar multicriterio ampliado;
* benchmarking avanzado;
* comparación de perfiles tácticos;
* evaluación ofensiva basada en xG/xA.

---

### Contribución esperada

Sprint 13B ampliará la riqueza informativa del sistema manteniendo intacta la arquitectura DSS desarrollada en releases anteriores.

La combinación de FBref avanzado y Understat permitirá evolucionar desde métricas descriptivas hacia indicadores más próximos al rendimiento subyacente y al potencial futuro del jugador.

---

## Investigación futura

* Incorporación de TabPFN.
* Incorporación de CatBoost.
* Nuevas fuentes de datos deportivas.
* FBref avanzado.
* Understat.
* Métricas xG/xA.
* Tracking data.
* Optimización multiobjetivo.
* Simulación económica de carteras.
* Evaluación causal de decisiones de fichaje.

---

# 🏁 Conclusión

La versión:

```text
v1.2.0 — Multi-League Expansion
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

Sprint 13A amplía la cobertura competitiva del proyecto desde siete hasta once ligas europeas y aporta evidencia inicial sobre la validez externa de la metodología, sin modificar la arquitectura analítica, los modelos predictivos ni la lógica DSS desarrollada en releases anteriores.

La plataforma ya no se limita a detectar oportunidades de mercado, sino que permite apoyar decisiones estratégicas de fichajes bajo restricciones reales de presupuesto, riesgo y necesidades deportivas.
