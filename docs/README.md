# 📚 Documentación Técnica del Proyecto

<div align="center">

![Docs](https://img.shields.io/badge/Docs-Scouting%20Intelligence-blue)
![Architecture](https://img.shields.io/badge/Architecture-Modular-success)
![Methodology](https://img.shields.io/badge/Methodology-CRISP--DM-orange)
![Tracking](https://img.shields.io/badge/Tracking-MLflow-success)
![Version](https://img.shields.io/badge/Version-v1.2.1-purple)
![Status](https://img.shields.io/badge/Status-Advanced%20Data%20Expansion-success)

</div>

---

# 🧠 Objetivo

Esta carpeta contiene la documentación técnica y metodológica de la plataforma desarrollada para el Trabajo Fin de Máster:

```text
Market Value Dynamics and Market Inefficiency Detection
in Professional Football
```

La documentación recoge las decisiones relacionadas con:

* arquitectura;
* datos;
* calidad;
* modelización;
* feature engineering;
* explainability;
* scoring;
* risk assessment;
* player intelligence;
* recruitment intelligence;
* decision support systems;
* validación externa.

Su objetivo no es únicamente describir el código, sino justificar las decisiones metodológicas adoptadas durante la evolución del sistema.

---

# 🚀 Estado actual del proyecto

La plataforma ha evolucionado desde un sistema predictivo centrado en estimación de valor de mercado hacia una solución integral de Football Analytics orientada a scouting profesional.

Estado actual:

```text
Historical Evaluation Layer
↓
Current Scouting Layer
↓
Player Intelligence Layer
↓
Recruitment Intelligence Layer
↓
Decision Support System
↓
External Validation
↓
Advanced Metrics Layer
```

---

## Capacidades actuales

### Data Layer

* integración FBref + Transfermarkt;
* matching jerárquico validado;
* panel longitudinal jugador-temporada;
* expansión multi-liga;
* dataset modelizable reproducible.

---

### Modeling Layer

* econometría aplicada;
* machine learning supervisado;
* validación temporal;
* MLflow;
* evaluación incremental de features.

---

### Scoring Layer

* Inefficiency Score;
* Growth Score;
* Confidence Score;
* Opportunity Score;
* Risk Score.

---

### Player Intelligence Layer

* Player Radar;
* Positional Benchmarking;
* Scouting Narrative;
* Opportunity vs Risk Analysis.

---

### Recruitment Intelligence Layer

* Recruitment Board;
* Candidate Selection;
* Comparative Player Analysis;
* Executive Scouting Workflow.

---

### Decision Support System

* Executive Dashboard;
* Advanced Search Engine;
* Explainability SHAP;
* Rankings interactivos;
* Internationalization EN/ES.

---

# 📊 Estado cuantitativo

| Métrica                        |                 Valor |
| ------------------------------ | --------------------: |
| Observaciones FBref procesadas |                43.591 |
| Dataset modelizable            |                 5.527 |
| Cobertura temporal             | 2019-2020 → 2025-2026 |
| Ligas                          |                    11 |
| Liga-temporada                 |                    77 |
| Modelo econométrico oficial    |       Growth OLS v13B |
| Modelo productivo oficial      |    Tuned XGBoost v13B |

---

## Contribuciones recientes

### Sprint 13A — Multi-League Expansion

* expansión a 11 ligas;
* validación externa;
* auditoría de cobertura;
* generalización multi-liga.

---

### Sprint 13B — Advanced Data Expansion

* integración de métricas avanzadas FBref;
* nuevas variables productivas;
* mejora simultánea en econometría y Machine Learning;
* fortalecimiento de la capacidad explicativa.

---

# 📂 Índice documental

## 🏗️ Arquitectura y sistema

| Documento             | Descripción                                                              |
| --------------------- | ------------------------------------------------------------------------ |
| architecture.md       | Arquitectura global del sistema y evolución metodológica                 |
| pipeline_reference.md | Referencia completa de pipelines y flujos operativos                     |
| schema_decisions.md   | Diseño de datasets, target, unidades de análisis y prevención de leakage |

---

## 📊 Datos

| Documento          | Descripción                                                |
| ------------------ | ---------------------------------------------------------- |
| data_sources.md    | Fuentes de datos, matching e integración multi-fuente      |
| data_quality.md    | Controles de calidad, validaciones y prevención de leakage |
| data_dictionary.md | Diccionario completo de variables y outputs                |

---

## 🤖 Modelización y analítica

| Documento                   | Descripción                                                       |
| --------------------------- | ----------------------------------------------------------------- |
| modeling_decisions.md       | Decisiones metodológicas de econometría, ML, scoring y evaluación |
| feature_engineering_plan.md | Estrategia completa de Feature Engineering                        |

---

# 🧩 Evolución metodológica

La documentación refleja la evolución progresiva del proyecto.

| Sprint       | Contribución principal                |
| ------------ | ------------------------------------- |
| Sprint 1     | Positional Normalization              |
| Sprint 2     | Temporal Dynamics                     |
| Sprint 3     | Composite Football Indices            |
| Sprint 4     | Machine Learning                      |
| Sprint 4C    | Explainability                        |
| Sprint 5     | Scoring Engine                        |
| Sprint 6     | Business Evaluation                   |
| Sprint 7     | Executive Dashboard                   |
| Sprint 9     | Decision Support Layer                |
| Sprint 10    | Player Intelligence + Risk Framework  |
| Sprint 11    | Recruitment Intelligence              |
| Sprint 12    | Productization & Internationalization |
| Sprint 13A   | Multi-League Expansion                |
| Sprint 13A.1 | External Validation & Coverage Audit  |
| Sprint 13B   | Advanced Data Expansion               |

---

# 🔄 Flujo documental recomendado

Para comprender el sistema de forma progresiva se recomienda el siguiente orden:

1. architecture.md
2. pipeline_reference.md
3. schema_decisions.md
4. data_sources.md
5. data_quality.md
6. data_dictionary.md
7. modeling_decisions.md
8. feature_engineering_plan.md

---

# 🧠 Relación entre documentos

```mermaid
flowchart TD

A[architecture.md]
--> B[pipeline_reference.md]

A --> C[schema_decisions.md]

C --> D[data_sources.md]
C --> E[data_quality.md]
C --> F[data_dictionary.md]

D --> G[modeling_decisions.md]
E --> G
F --> G

G --> H[feature_engineering_plan.md]

H --> I[Current Scouting Layer]

I --> J[Player Intelligence Layer]

J --> K[Recruitment Intelligence Layer]

K --> L[Decision Support System]

L --> M[Scouting Intelligence]
```

# 🏗️ Relación con la arquitectura

La documentación sigue la misma estructura conceptual que la arquitectura del sistema.

```text id="h4e2m9"
Raw Sources
↓
Feature Engineering
↓
Advanced Metrics Layer
↓
Modeling Dataset
↓
Econometric & ML Models
↓
Historical Evaluation Layer
↓
Current Scouting Layer
↓
Player Intelligence Layer
↓
Recruitment Intelligence Layer
↓
Decision Support System
```

Cada documento describe una capa específica del sistema y las decisiones metodológicas asociadas.

---

# 📌 Convenciones documentales

## Principios

Todos los documentos deben:

* justificar decisiones;
* documentar trade-offs;
* describir limitaciones;
* explicar impactos metodológicos;
* mantener trazabilidad;
* garantizar reproducibilidad.

---

## Reproducibilidad

La ejecución reproducible reside en:

```text id="n8u7jw"
src/
```

Los notebooks se mantienen como soporte para:

* exploración;
* validación;
* interpretación;
* visualización;
* experimentación controlada.

---

## Tracking experimental

MLflow se utiliza para registrar:

```text id="8m4r5q"
Parámetros
↓
Métricas
↓
Modelos
↓
Artefactos
```

Ubicación:

```text id="z0q4gt"
mlruns/
```

---

## Outputs finales

| Directorio | Función                   |
| ---------- | ------------------------- |
| reports/   | resultados interpretables |
| artifacts/ | modelos y predicciones    |
| mlruns/    | tracking experimental     |
| logs/      | trazabilidad operativa    |

---

# 🚀 Contribuciones metodológicas recientes

## Sprint 13A — Multi-League Expansion

Sprint 13A constituye la principal ampliación de cobertura realizada hasta la fecha.

Principales contribuciones:

* expansión de 7 a 11 ligas;
* incorporación de 4 nuevas competiciones;
* parametrización de pipelines;
* auditoría de cobertura;
* diagnósticos de matching;
* validación externa.

---

### Resultado

| Métrica                        |  Valor |
| ------------------------------ | -----: |
| Observaciones FBref procesadas | 43.591 |
| Dataset modelizable            |  5.527 |
| Ligas                          |     11 |
| Temporadas                     |      7 |
| Liga-temporada                 |     77 |
| Match Rate global              | 75,97% |

---

### Impacto metodológico

Sprint 13A fortalece:

```text id="9hrc9r"
Validez externa
↓
Capacidad de generalización
↓
Representatividad competitiva
```

---

## Sprint 13B — Advanced Data Expansion

Sprint 13B amplía la profundidad analítica del sistema mediante la incorporación de métricas avanzadas derivadas de FBref.

---

### Nuevas variables productivas

* finishing_index_v2
* availability_index
* defensive_activity_index

---

### Resultados econométricos

| Modelo                |     R² |
| --------------------- | -----: |
| M_A_v13A_base_spec_FE | 0.4505 |
| M_B_v13B_advanced_FE  | 0.4549 |

Resultado:

```text id="q8v4md"
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

La variable avanzada con mayor relevancia predictiva agregada es:

```text id="q3gjcc"
finishing_index_v2
```

---

### Impacto metodológico

Sprint 13B fortalece:

```text id="95jzgm"
Capacidad explicativa
↓
Calidad de variables
↓
Robustez predictiva
```

---

# ⚠️ Limitación arquitectónica identificada

Durante Sprint 13B se intentó integrar la nueva capa de modelización dentro del pipeline histórico de scoring.

---

## Hallazgo

Se identifica una separación estructural entre:

```text id="k0vxr7"
Modeling Pipeline
≠
Scoring Pipeline
```

---

## Situación observada

El pipeline histórico de scoring depende de variables enriquecidas adicionales como:

* market_value_growth_prev;
* delta_log_market_value_prev;
* growth_index;
* career_year;
* breakout_indicator;
* matching_confidence.

Mientras que la capa productiva v13B genera principalmente:

* predicted_log_market_value_ml;
* predicted_market_value_ml_eur;
* inefficiency_score_ml.

---

## Decisión metodológica

No integrar esta capa dentro de Sprint 13B.

Motivos:

1. No afecta a la hipótesis principal.
2. No altera resultados econométricos.
3. No altera resultados de Machine Learning.
4. Constituye un trabajo de integración independiente.

---

# 🛣️ Próximas líneas documentales

## TM.1 — Transfermarkt Coverage Audit

Objetivo:

* diagnosticar limitaciones de cobertura;
* estimar techo teórico de matching;
* mejorar integración de datos.

---

## TM.2 — Scoring & Ranking Integration v13B

Objetivo:

```text id="w5m6zn"
Predictions v13B
↓
Scoring Dataset v13B
↓
Opportunity Framework v13B
↓
Risk Framework v13B
↓
Rankings v13B
↓
Stability Analysis
```

---

## Sprint 14 — Transfer Strategy Enhancement

Siguiente fase oficial del proyecto.

Objetivo:

```text id="h1l3ff"
Transformar oportunidades individuales
en estrategias óptimas de fichajes
bajo restricciones reales
de presupuesto y riesgo
```

Líneas previstas:

* Transfer Strategy Engine;
* Portfolio Optimization;
* Scenario Simulation;
* Strategic Recruitment.

---

# 🧠 Conclusión

La documentación refleja la evolución del proyecto desde un sistema académico centrado en modelización hacia una plataforma integral de Football Analytics orientada a scouting profesional, recruitment y soporte avanzado a decisiones deportivas.

La evolución metodológica puede resumirse mediante:

```text id="d8b0jw"
Modelización
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

Las contribuciones más relevantes de la release:

```text id="t6qj2v"
v1.2.1 — Advanced Data Expansion
```

corresponden a:

### Sprint 13A

* ampliación multi-liga;
* validación externa;
* auditoría de cobertura.

### Sprint 13B

* integración de métricas avanzadas;
* validación incremental de variables;
* mejora simultánea en econometría y Machine Learning.

La hipótesis principal de Sprint 13B queda validada.

Las variables:

* finishing_index_v2;
* availability_index;
* defensive_activity_index;

aportan señal predictiva incremental consistente y pasan a formar parte de la arquitectura productiva oficial.

La siguiente evolución natural del proyecto corresponde a:

```text id="mpq4u8"
Sprint 14
↓
Transfer Strategy Enhancement
```

orientada a transformar inteligencia de scouting en estrategias óptimas de construcción de plantilla.
