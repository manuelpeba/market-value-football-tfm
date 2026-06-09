# 📌 PROJECT STATUS

![Architecture](https://img.shields.io/badge/Architecture-Modular-success)
![Validation](https://img.shields.io/badge/Validation-Temporal-important)
![Modeling](https://img.shields.io/badge/Modeling-OLS%20%2B%20ML-blue)
![Matching](https://img.shields.io/badge/Matching-75.97%25-yellow)
![Coverage](https://img.shields.io/badge/Coverage-11%20Leagues-success)
![Tracking](https://img.shields.io/badge/Experiment%20Tracking-MLflow-success)
![Dashboard](https://img.shields.io/badge/Dashboard-Streamlit-success)
![DSS](https://img.shields.io/badge/System-Decision%20Support-success)
![Version](https://img.shields.io/badge/version-v1.2.1-blue)

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

La versión actual incorpora los resultados consolidados de:

```text id="8v7i6m"
Sprint 13A — Multi-League Expansion

Sprint 13B — Advanced Data Expansion
```

Sprint 13A amplió la cobertura competitiva del sistema desde siete hasta once ligas europeas, incrementando el dataset modelizable desde 3.916 hasta 5.527 observaciones jugador-temporada y proporcionando una validación explícita de la capacidad de generalización de la metodología.

Sobre esta nueva base de datos ampliada, Sprint 13B evaluó el impacto de incorporar métricas avanzadas derivadas de FBref mediante la construcción de nuevas variables sintéticas orientadas a capturar dimensiones futbolísticas complejas relacionadas con finalización, disponibilidad competitiva y actividad defensiva.

Las variables incorporadas fueron:

* finishing_index_v2
* availability_index
* defensive_activity_index

Los resultados obtenidos muestran que estas nuevas variables mejoran simultáneamente el rendimiento de los modelos econométricos y de Machine Learning, aportando evidencia favorable sobre el valor incremental de las métricas avanzadas para la estimación del valor de mercado.

Principales contribuciones de Sprint 13A y Sprint 13B:

* ampliación de cobertura a 11 ligas europeas;
* procesamiento de 43.591 observaciones procedentes de FBref;
* auditoría sistemática de matching por liga y temporada;
* validación externa de la metodología;
* integración de métricas avanzadas de rendimiento;
* validación transversal multi-modelo;
* mejora empírica de la capacidad predictiva;
* fortalecimiento de la robustez metodológica del sistema.

La versión actual representa la evolución desde un sistema de estimación de valor de mercado hacia una plataforma DSS completa orientada a scouting, recruitment y soporte avanzado a decisiones deportivas.

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

### Modelos oficiales (v1.2.1)

| Capa             | Modelo oficial     |
| ---------------- | ------------------ |
| Econometría      | Growth OLS v13B    |
| Machine Learning | Tuned XGBoost v13B |

---

### Sprint 13B — Evaluación econométrica

| Modelo                |     R² |
| --------------------- | -----: |
| M_A_v13A_base_spec_FE | 0.4505 |
| M_B_v13B_advanced_FE  | 0.4549 |

Resultado:

```text id="7lfk9x"
ΔR² = +0.0044
```

Mejoras observadas:

* mejora de MAE;
* mejora de RMSE;
* mejora de AIC;
* mejora de BIC.

Conclusión:

Las métricas avanzadas aportan capacidad explicativa incremental dentro de la especificación econométrica.

---

### Sprint 13B — Evaluación Machine Learning

Comparación entre:

```text id="h5e5in"
Feature Set A (v13A)

vs

Feature Set B (v13B)
```

Resultados principales:

| Modelo               | Mejora observada |
| -------------------- | ---------------: |
| XGBoost              |          +0.0096 |
| Random Forest        |          +0.0097 |
| HistGradientBoosting |          +0.0144 |
| LightGBM             |          +0.0291 |

Hallazgo principal:

Todas las arquitecturas evaluadas mejoran simultáneamente tras incorporar las nuevas variables.

Este comportamiento reduce el riesgo de dependencia de una única arquitectura y aporta robustez adicional a los resultados obtenidos.

---

### Variable avanzada más relevante

Los análisis de importancia de variables realizados durante Sprint 13B identifican:

```text id="pbvprn"
finishing_index_v2
```

como la variable avanzada con mayor relevancia predictiva agregada.

Este resultado constituye el principal hallazgo analítico de Sprint 13B.

---

### Estado actual de modelización

```text id="j7fj72"
Growth OLS v13B
↓
Benchmark interpretable

Tuned XGBoost v13B
↓
Modelo productivo
```

La arquitectura mantiene la separación entre interpretabilidad econométrica y capacidad predictiva avanzada.

---

## Evaluación de negocio

| Métrica       | Valor |
| ------------- | ----: |
| Precision@10  |   90% |
| Precision@20  |   90% |
| Precision@50  |   90% |
| Precision@100 |   85% |

Los resultados obtenidos continúan respaldando la utilidad operativa del sistema para procesos de scouting y priorización de oportunidades de mercado.

---

## Estado general del proyecto

```text id="g0s5mz"
Sprint 13A — COMPLETADO

Sprint 13B — COMPLETADO

Release v1.2.1 — ACTIVE

Sprint 14 — SIGUIENTE FASE
```
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
* Evaluación de cobertura por competición.
* Diagnóstico de representatividad del universo analizado.

### Data Preparation

* Matching FBref ↔ Transfermarkt.
* Feature Engineering.
* Construcción del panel longitudinal.
* Control de leakage.
* Expansión multi-liga parametrizada.
* Construcción de métricas avanzadas derivadas de FBref.
* Desarrollo de Composite Football Indices v2.

### Modeling

* Econometric Pipeline.
* Machine Learning Pipeline.
* Experiment Tracking.
* Explainability.
* Validación multi-liga.
* Evaluación de métricas avanzadas.
* Comparación Feature Set A vs Feature Set B.

### Evaluation

* Validación temporal.
* Evaluación predictiva.
* Evaluación orientada a negocio.
* Validación externa.
* Evaluación incremental de nuevas variables.
* Comparación transversal multi-modelo.

### Deployment

* Dashboard interactivo.
* Recruitment Intelligence.
* Decision Support System.
* Modelos productivos v13B.
* Integración DSS.
* Internacionalización EN/ES.

---

## Estado actual

```text id="e6e9aw"
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
Decision Support System
↓
Multi-League Expansion
↓
Advanced Data Expansion
↓
External Validity Assessment
```

La metodología ha superado satisfactoriamente las fases de ampliación competitiva y enriquecimiento analítico, consolidando una arquitectura reproducible y validada sobre múltiples entornos competitivos.

---

# 🏗️ Arquitectura actual

```text id="k5m9nk"
Raw Sources
↓
Feature Engineering
↓
Advanced Metrics Layer
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

| Componente                    | Estado |
| ----------------------------- | ------ |
| Data Pipelines                | ✅      |
| Matching Pipeline             | ✅      |
| Feature Engineering           | ✅      |
| Advanced Feature Engineering  | ✅      |
| Econometric Pipeline          | ✅      |
| Machine Learning Pipeline     | ✅      |
| MLflow Tracking               | ✅      |
| Explainability                | ✅      |
| Opportunity Score             | ✅      |
| Risk Framework                | ✅      |
| Dashboard DSS                 | ✅      |
| Recruitment Intelligence      | ✅      |
| Internationalization EN/ES    | ✅      |
| Multi-League Expansion        | ✅      |
| External Validity Assessment  | ✅      |
| League Coverage Diagnostics   | ✅      |
| Multi-League Benchmarking     | ✅      |
| Advanced Metrics Integration  | ✅      |
| Composite Football Indices v2 | ✅      |

---

# ⚙️ Capacidades implementadas

## Estimación de valor de mercado

La plataforma estima el valor esperado de un jugador utilizando modelos econométricos y algoritmos de Machine Learning entrenados sobre datos históricos procedentes de múltiples competiciones europeas.

La arquitectura combina interpretabilidad econométrica y capacidad predictiva avanzada para capturar los principales determinantes del valor de mercado profesional.

---

## Advanced Football Metrics Layer

Sprint 13B incorpora una nueva capa analítica destinada a capturar dimensiones futbolísticas que no estaban completamente representadas en versiones anteriores del sistema.

Variables productivas incorporadas:

* finishing_index_v2
* availability_index
* defensive_activity_index

Estas variables amplían la capacidad descriptiva del sistema sin modificar la arquitectura conceptual del proyecto.

---

## Opportunity Detection

Identificación automática de jugadores potencialmente infravalorados mediante comparación entre:

```text id="72cgcu"
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

## Decision Support System

La plataforma integra todas las capas anteriores dentro de un entorno único de soporte a decisiones deportivas.

El sistema permite evolucionar desde la identificación de oportunidades individuales hasta procesos estructurados de scouting y recruitment soportados por evidencia cuantitativa reproducible.

---

# 🔄 Evolución funcional

## Sprint 7

Executive Dashboard

```text id="m1h9o5"
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

```text id="zb5wb5"
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

### Contribuciones

* ampliación de cobertura competitiva;
* parametrización reproducible de pipelines;
* auditoría de matching por liga;
* auditoría de matching por temporada;
* validación temporal multi-liga;
* validación externa de la metodología.

Sprint 13A constituye la primera validación empírica de la robustez metodológica fuera del universo competitivo original.

---

## Sprint 13A.1

Coverage Audit & External Validation

### Objetivo

Validar empíricamente la robustez de la metodología tras la expansión desde siete hasta once ligas europeas.

### Resultados

| Dataset  | R² Tuned XGBoost |
| -------- | ---------------: |
| 7 ligas  |           0.5414 |
| 11 ligas |           0.5664 |

### Contribuciones

* auditoría sistemática de cobertura;
* evaluación explícita de validez externa;
* evidencia de capacidad de generalización;
* mejora simultánea de cobertura y rendimiento predictivo.

---

## Sprint 13B

Advanced Data Expansion

### Objetivo

Evaluar si la incorporación de métricas avanzadas derivadas de FBref mejora la capacidad predictiva de los modelos de valoración de mercado.

### Variables incorporadas

* finishing_index_v2
* availability_index
* defensive_activity_index

### Resultados econométricos

| Modelo                |     R² |
| --------------------- | -----: |
| M_A_v13A_base_spec_FE | 0.4505 |
| M_B_v13B_advanced_FE  | 0.4549 |

Resultado:

```text id="d3cln9"
ΔR² = +0.0044
```

---

### Resultados Machine Learning

| Modelo               | Mejora observada |
| -------------------- | ---------------: |
| XGBoost              |          +0.0096 |
| Random Forest        |          +0.0097 |
| HistGradientBoosting |          +0.0144 |
| LightGBM             |          +0.0291 |

---

### Hallazgo principal

Todas las arquitecturas evaluadas mejoran simultáneamente tras incorporar las nuevas variables.

Este comportamiento reduce el riesgo de dependencia de una única familia de modelos y fortalece la robustez metodológica de los resultados obtenidos.

---

### Principal contribución analítica

Los análisis de importancia de variables identifican:

```text id="ecp8pd"
finishing_index_v2
```

como la variable avanzada con mayor relevancia predictiva agregada.

---

### Contribuciones

* Advanced Football Metrics Integration.
* Composite Football Indices v2.
* Advanced Feature Engineering.
* Validación transversal multi-modelo.
* Promoción de nuevas variables productivas.
* Mejora consistente de la capacidad explicativa.

### Resultado metodológico

La hipótesis de Sprint 13B queda validada.

Las métricas avanzadas derivadas de FBref aportan señal predictiva adicional tanto en econometría como en Machine Learning y pasan a formar parte de la arquitectura productiva del proyecto.

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
* Integración de métricas avanzadas derivadas de FBref.
* Composite Football Indices v2 promovidos a producción.
* Validación transversal multi-modelo.

---

## Predictivos

### Econometría

#### Benchmark oficial

```text id="r0kq4f"
Growth OLS v13B
```

Resultados Sprint 13B:

| Modelo                |     R² |
| --------------------- | -----: |
| M_A_v13A_base_spec_FE | 0.4505 |
| M_B_v13B_advanced_FE  | 0.4549 |

Resultado:

```text id="h0zqlm"
ΔR² = +0.0044
```

Adicionalmente se observan mejoras en:

* RMSE.
* MAE.
* AIC.
* BIC.

---

### Machine Learning

#### Modelo productivo oficial

```text id="w4f0gh"
Tuned XGBoost v13B
```

Resultados Sprint 13B:

| Modelo               | Mejora observada |
| -------------------- | ---------------: |
| XGBoost              |          +0.0096 |
| Random Forest        |          +0.0097 |
| HistGradientBoosting |          +0.0144 |
| LightGBM             |          +0.0291 |

---

### Hallazgo principal

La incorporación de métricas avanzadas produce mejoras simultáneas en todas las arquitecturas evaluadas.

Este resultado constituye una evidencia especialmente relevante porque:

* reduce el riesgo de dependencia de una única arquitectura;
* fortalece la robustez metodológica;
* incrementa la confianza en la validez de los resultados obtenidos.

---

## Variable avanzada más relevante

Los análisis de importancia de variables realizados durante Sprint 13B identifican:

```text id="3hzw4r"
finishing_index_v2
```

como la variable avanzada con mayor capacidad explicativa agregada.

Este resultado representa la principal contribución analítica de Sprint 13B.

---

## Validez externa

Sprint 13A aporta evidencia empírica de que el sistema mantiene e incluso mejora su rendimiento al incorporar:

* ligas principales;
* ligas secundarias;
* mercados de distinto nivel competitivo;
* estructuras competitivas heterogéneas;
* perfiles de desarrollo diversos.

La metodología demuestra capacidad de generalización más allá del universo competitivo original.

---

## Negocio

* Opportunity Detection validado.
* Precision@K elevada.
* Recruitment Intelligence integrada.
* Decision Support System operativo.
* Explainability integrada.
* Arquitectura reproducible y escalable.

---

# ⚖️ Trade-offs metodológicos

## Interpretabilidad vs rendimiento

```text id="z1xw56"
Econometría
+
Machine Learning
+
Explainable AI
```

La coexistencia de modelos econométricos y algoritmos avanzados de Machine Learning permite combinar:

* capacidad explicativa;
* robustez metodológica;
* precisión predictiva.

---

## Cobertura vs calidad

La expansión competitiva desarrollada durante Sprint 13A se realizó manteniendo criterios estrictos de matching y control de calidad.

Los resultados observados muestran que el incremento de cobertura añade señal útil sin deteriorar la consistencia metodológica.

---

## Complejidad vs robustez

Sprint 13B incorpora nuevas variables avanzadas sin alterar la arquitectura conceptual del sistema.

La mejora simultánea observada en múltiples modelos sugiere que la complejidad adicional introducida genera valor predictivo real y no únicamente sobreajuste.

---

# ⚠️ Limitaciones actuales

## Datos

* Dependencia de Transfermarkt para valor de mercado.
* Menor cobertura en determinadas ligas secundarias.
* Cobertura desigual entre competiciones.
* Posibles limitaciones derivadas de Transfermarkt-Kaggle.
* Ausencia de tracking data.
* Ausencia de event data avanzado.
* Ausencia de información contractual completa.
* Ausencia de información salarial.

---

## Modelización

* Posible drift temporal.
* Dependencia de variables observables.
* Limitaciones inherentes al valor de mercado como proxy económico.
* Necesidad de recalibración periódica de modelos.

---

## Arquitectura

Durante Sprint 13B se identificó una separación estructural entre:

```text id="q3v6wh"
Modeling Pipeline
≠
Scoring Pipeline
```

El pipeline histórico de scoring requiere variables enriquecidas adicionales no presentes actualmente en la capa productiva de predicción.

Por este motivo, la integración completa entre:

```text id="n52s95"
Predictions v13B
↓
Scoring Dataset v13B
↓
Growth Score
↓
Confidence Score
↓
Opportunity Score
↓
Risk Score
↓
Rankings v13B
```

queda documentada como trabajo futuro independiente.

Esta limitación no afecta a:

* los resultados econométricos;
* los resultados de Machine Learning;
* la validación de la hipótesis principal de Sprint 13B.

---

## Producto

* Ausencia de API pública.
* Ausencia de generación automática de informes.
* Dependencia de ejecución local mediante Streamlit.

---

# 🛣️ Roadmap

## TM.1 — Transfermarkt Coverage Audit

Estado:

```text id="5w7h2m"
Backlog
```

Objetivo:

Determinar si las limitaciones de cobertura observadas durante Sprint 13A proceden principalmente de:

* Transfermarkt-Kaggle.
* Transfermarkt original.
* Pipeline de extracción.
* Disponibilidad histórica de determinadas competiciones.

Contribución esperada:

* diagnóstico definitivo de cobertura;
* estimación del techo teórico de matching;
* identificación de oportunidades de mejora.

---

## TM.2 — Scoring & Ranking Integration v13B

Estado:

```text id="a0v8hx"
Backlog prioritario
```

Objetivo:

Reconstruir la integración completa entre la nueva capa de modelización v13B y el sistema histórico de scoring.

Flujo objetivo:

```text id="eyyr4o"
Predictions v13B
↓
Scoring Dataset v13B
↓
Growth Score
↓
Confidence Score
↓
Opportunity Score
↓
Risk Score
↓
Rankings v13B
↓
Stability Analysis
```

Justificación:

La integración no afecta a la validación de Sprint 13B pero constituye la evolución natural necesaria para alinear completamente la capa predictiva con la capa DSS.

---

## Sprint 14 — Transfer Strategy Enhancement

Estado:

```text id="yow0rd"
Próxima fase principal
```

Objetivo:

Expandir el sistema desde la identificación de oportunidades individuales hacia la recomendación de estrategias completas de captación.

Pregunta objetivo:

```text id="q8yct8"
¿Qué combinación de jugadores
maximiza el valor esperado
bajo restricciones reales
de presupuesto y riesgo?
```

Líneas de trabajo previstas:

* Transfer Strategy Engine.
* Portfolio Optimization.
* Scenario Simulation.
* Strategic Recruitment.
* Decision Science aplicada al mercado de fichajes.

Contribución esperada:

Integrar scouting, valoración económica, riesgo y optimización dentro de una misma arquitectura de soporte a decisiones.

---

## Investigación futura

### Modelización

* TabPFN.
* CatBoost.
* Ensemble Learning.
* Comparación con modelos fundacionales para datos tabulares.

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
* Success Probability Models.

### Sports Economics

* Simulación económica de carteras de fichajes.
* Optimización multiobjetivo.
* Valoración dinámica de activos deportivos.
* Modelización avanzada de ROI.

---

# 🏁 Conclusión

La versión:

```text id="0l0n8k"
v1.2.1 — Advanced Data Expansion
```

representa la consolidación de una arquitectura integral de Football Analytics orientada a scouting, recruitment y soporte avanzado a decisiones deportivas.

La combinación de:

```text id="tqt3x3"
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

permite transformar grandes volúmenes de datos futbolísticos en recomendaciones accionables para departamentos deportivos profesionales.

La evolución metodológica del proyecto puede resumirse mediante:

```text id="h2j0d1"
Predicción
↓
Player Intelligence
↓
Recruitment Intelligence
↓
Decision Support System
```

Sprint 13A aporta una contribución especialmente relevante al demostrar que la ampliación del universo competitivo mejora simultáneamente cobertura, representatividad y rendimiento predictivo.

Sprint 13B aporta una segunda contribución metodológica fundamental al demostrar que las métricas avanzadas derivadas de FBref contienen información económicamente relevante para explicar el valor de mercado de futbolistas profesionales.

Los resultados obtenidos muestran que:

```text id="w9r1v3"
Sprint 13A
→ fortalece la validez externa

Sprint 13B
→ fortalece la capacidad explicativa
```

reforzando simultáneamente la robustez metodológica y el valor analítico de la plataforma.

La hipótesis principal de Sprint 13B queda validada.

Las variables:

* finishing_index_v2
* availability_index
* defensive_activity_index

aportan mejoras consistentes tanto en econometría como en Machine Learning y pasan a formar parte de la arquitectura productiva del proyecto.

El resultado final es una plataforma reproducible, interpretable y orientada a negocio capaz de conectar analítica deportiva avanzada con procesos reales de scouting, recruitment y toma de decisiones dentro del fútbol profesional.

La siguiente fase de desarrollo corresponderá a:

```text id="8ebq5m"
Sprint 14
↓
Transfer Strategy Enhancement
```

centrada en extender el sistema desde la identificación de oportunidades hacia la optimización estratégica de decisiones de fichaje.
