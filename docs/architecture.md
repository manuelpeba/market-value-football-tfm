# 🏗️ Arquitectura del Sistema

## Visión general

La arquitectura del proyecto ha evolucionado desde un entorno exploratorio centrado en modelización predictiva hacia una plataforma integral de Football Analytics orientada a scouting profesional, recruitment intelligence y soporte cuantitativo a decisiones deportivas.

La versión actual:

```text
v1.2.2 — Transfer Strategy Engine + Multi-League DSS Integration
```

implementa una arquitectura multicapa capaz de transformar información deportiva y económica procedente de múltiples competiciones europeas en recomendaciones accionables para departamentos deportivos profesionales.

La evolución metodológica del sistema puede resumirse mediante:

```text
Data Engineering
↓
Modeling
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
Sporting Decision
```

La arquitectura integra actualmente conceptos procedentes de:

* Sports Analytics
* Sports Economics
* Econometría aplicada
* Machine Learning supervisado
* Explainable AI
* Decision Science
* Operations Research
* Portfolio Optimization

permitiendo evolucionar desde la identificación de oportunidades individuales hacia la optimización de decisiones de fichaje bajo restricciones reales de club.

---

## Estado actual

| Métrica                        |  Valor |
| ------------------------------ | -----: |
| Observaciones FBref procesadas | 43.591 |
| Dataset modelizable            |  5.527 |
| Ligas                          |     11 |
| Temporadas                     |      7 |
| Combinaciones liga-temporada   |     77 |
| Match Rate global              | 75,97% |

---

## Principios arquitectónicos

La arquitectura se diseña siguiendo los siguientes principios:

* Modularidad.
* Reproducibilidad.
* Trazabilidad experimental.
* Separación de responsabilidades.
* Validación temporal.
* Interpretabilidad.
* Escalabilidad analítica.
* Orientación a negocio.
* Validez externa.
* Generalización multi-liga.
* Optimización bajo restricciones.

---

# 🧩 Arquitectura funcional actual

```mermaid
flowchart TD

A[Raw Sources]
--> B[Feature Engineering]

B --> C[Advanced Metrics Layer]

C --> D[Player-Season Matching]

D --> E[Player-Season Panel]

E --> F[Modeling Dataset]

F --> G[Econometric Pipeline]
F --> H[Machine Learning Pipeline]

G --> I[Model Evaluation]
H --> I

I --> J[Explainability]

H --> K[Operational Predictions]

K --> L[Scoring Feature Reintegration Layer]

L --> M[Opportunity Framework]
L --> N[Risk Framework]

M --> O[Ranking Engine]
N --> O

O --> P[Scouting Layer]

P --> Q[Player Intelligence]

Q --> R[Recruitment Intelligence]

R --> S[Transfer Strategy Engine]

S --> T[Portfolio Optimization]

T --> U[Decision Support System]

U --> V[Sporting Decision]
```

---

## Contribución arquitectónica de Sprint TM.2

Sprint TM.2 introduce una capa explícita de reintegración de variables entre la salida de predicción y el Opportunity Framework.

Objetivo:

```text
Predictions
↓
Scoring Feature Reintegration
↓
Opportunity Framework
↓
Ranking Engine
↓
Transfer Strategy Engine
```

Esta capa garantiza que la expansión multi-liga introducida durante Sprint 13A y Sprint 13B se propague correctamente hasta todas las capas operativas del DSS.

Resultado:

```text
Modeling Layer             → 11 ligas
Scoring Layer              → 11 ligas
Opportunity Layer          → 11 ligas
Transfer Strategy Engine   → 11 ligas
Decision Support System    → 11 ligas
```

La arquitectura elimina así dependencias heredadas de versiones anteriores y asegura consistencia metodológica de extremo a extremo.

---

# 🏛️ Capas arquitectónicas

## 1. Data Layer

Responsable de la adquisición, limpieza y preparación de datos.

### Fuentes

* FBref
* Transfermarkt

### Responsabilidades

* Ingestión.
* Limpieza.
* Estandarización.
* Integración.
* Enriquecimiento.
* Construcción de variables.

### Componentes

```text
src/data/
src/features/
```

---

### Cobertura actual

| Métrica             |  Valor |
| ------------------- | -----: |
| Ligas               |     11 |
| Temporadas          |      7 |
| Observaciones FBref | 43.591 |

---

## 2. Advanced Metrics Layer

Introducida durante Sprint 13B.

### Objetivo

Integrar métricas avanzadas derivadas de FBref dentro de la arquitectura productiva.

### Variables productivas

* finishing_index_v2
* availability_index
* defensive_activity_index

### Resultado metodológico

Las tres variables fueron promovidas a producción tras demostrar mejoras consistentes tanto en econometría como en Machine Learning.

Hallazgo principal:

```text
finishing_index_v2
```

se identifica como la variable avanzada con mayor relevancia predictiva agregada.

---

## 3. Matching Layer

Responsable de la integración entre fuentes.

### Objetivo

```text
FBref ↔ Transfermarkt
```

### Metodología

* Exact Matching.
* Club Validation.
* Age Validation.
* Fuzzy Matching.

### Tecnología

```text
RapidFuzz
```

### Resultado actual

| Métrica           |  Valor |
| ----------------- | -----: |
| Match Rate global | 75,97% |

---

## 4. Modeling Layer

Responsable de la construcción del dataset modelizable y del entrenamiento de modelos predictivos.

### Dataset actual

| Métrica       | Valor |
| ------------- | ----: |
| Observaciones | 5.527 |
| Ligas         |    11 |
| Temporadas    |     7 |

### Modelos oficiales

#### Growth OLS v13B

Benchmark econométrico oficial.

R²:

```text
0.4549
```

#### Tuned XGBoost v13B

Modelo Machine Learning productivo.

Resultado productivo:

```text
RMSE = 0.9639
MAE  = 0.7777
R²   = 0.4453
```

#### Referencia histórica de validación externa

Sprint 13A.1 obtuvo el mejor resultado predictivo alcanzado durante el proyecto:

```text
Tuned XGBoost
RMSE = 0.8525
MAE  = 0.6834
R²   = 0.5664
```

Este resultado constituye la principal evidencia de capacidad de generalización multi-liga de la metodología desarrollada.

### Resultado

La modelización opera actualmente sobre un universo multi-liga de once competiciones europeas y constituye la base de todas las capas posteriores del DSS.


## 5. Opportunity Framework Layer

Introducida durante Sprint 5 y ampliada progresivamente hasta Sprint TM.2.

### Objetivo

Transformar predicciones de valor de mercado en oportunidades accionables de scouting.

La lógica central del sistema se basa en la comparación entre:

```text
Observed Market Value
vs
Expected Market Value
```

permitiendo identificar potenciales ineficiencias de mercado.

---

### Componentes

#### Inefficiency Score

Mide el grado de infravaloración o sobrevaloración relativa.

#### Growth Score

Captura señales de crecimiento y evolución reciente del jugador.

#### Confidence Score

Evalúa la robustez y fiabilidad de la recomendación.

#### Opportunity Score

Combina las dimensiones anteriores en una métrica única orientada a toma de decisiones.

---

### Resultado operativo

Tras Sprint TM.2:

```text
Opportunity Framework
↓
11 ligas integradas
↓
6.208 observaciones elegibles
```

garantizando consistencia con la cobertura de modelización.

---

## 6. Risk Framework Layer

Responsable de la evaluación del riesgo asociado a cada recomendación.

### Objetivo

Complementar el análisis de oportunidad con una medida explícita de incertidumbre.

### Componentes

* Risk Score.
* Risk Category.
* Opportunity vs Risk Matrix.
* Risk-adjusted Opportunity.

### Resultado

La plataforma permite evaluar simultáneamente:

```text
Potencial esperado
+
Nivel de riesgo
```

mejorando la calidad de las decisiones de recruitment.

---

## 7. Ranking Engine Layer

Responsable de transformar Opportunity Framework y Risk Framework en rankings operativos.

### Función principal

```text
Opportunity Framework
+
Risk Framework
↓
Ranking Engine
↓
Scouting Prioritization
```

---

### Outputs principales

#### Global Rankings

Ranking global de oportunidades.

#### Positional Rankings

Rankings específicos por posición.

#### Recruitment Rankings

Rankings orientados a scouting y recruitment.

#### Executive Shortlists

Selección priorizada de candidatos para evaluación ejecutiva.

---

### Sprint TM.2

Sprint TM.2 resolvió una inconsistencia arquitectónica detectada tras la expansión multi-liga.

Situación previa:

```text
Modeling Layer      → 11 ligas
Ranking Engine      → 7 ligas
```

Situación actual:

```text
Modeling Layer      → 11 ligas
Ranking Engine      → 11 ligas
```

Resultado:

Consistencia completa entre modelización y capa operativa.

---

## 8. Player Intelligence Layer

Introducida durante Sprint 10.

### Objetivo

Transformar rankings en análisis individuales de jugadores.

### Componentes

#### Player Radar

Visualización multidimensional del perfil del jugador.

#### Positional Benchmarking

Comparación frente a perfiles equivalentes.

#### Opportunity vs Risk Matrix

Evaluación conjunta de potencial y riesgo.

#### Scouting Narrative

Interpretación automática de fortalezas y debilidades.

### Resultado

La plataforma evoluciona desde rankings descriptivos hacia inteligencia accionable a nivel de jugador.

---

## 9. Recruitment Intelligence Layer

Introducida durante Sprint 11.

### Objetivo

Transformar análisis individuales en procesos estructurados de recruitment.

### Componentes

#### Recruitment Board

Permite:

* construcción de shortlists;
* gestión de candidatos;
* evaluación colectiva.

#### Candidate Selection System

Permite:

* comparación simultánea;
* priorización dinámica;
* evaluación ejecutiva.

#### Comparative Player Analysis

Comparación directa de:

* Opportunity Score.
* Risk Score.
* Confidence Score.
* Market Value.
* Predicted Value.
* Market Mispricing.

---

### Workflow ejecutivo

```text
Opportunity Detection
↓
Filtering
↓
Shortlisting
↓
Comparative Analysis
↓
Recruitment Decision
```

---

## 10. Transfer Strategy Engine

Introducido durante Sprint 14.

### Objetivo

Responder a la pregunta:

```text
¿Qué cartera de fichajes maximiza
el valor esperado bajo restricciones
reales de club?
```

---

### Inputs

* Budget.
* Positions Needed.
* Scenario.
* Portfolio Style.
* Minimum Player Level.
* Maximum Signings.

---

### Outputs

* Recommended Portfolio.
* Total Cost.
* Budget Utilization.
* Expected Upside.
* Expected ROI.
* Average Portfolio Score.

---

### Escenarios implementados

#### Conservative

Prioriza estabilidad y robustez.

#### Balanced

Equilibrio entre upside y riesgo.

#### Aggressive

Maximización de upside esperado.

---

### Estilos de cartera

#### Value Opportunities

Maximización de oportunidades de mercado.

#### Balanced Squad Building

Equilibrio entre concentración y diversificación.

#### Star + Prospects

Combinación de talento consolidado y desarrollo futuro.

---

## 11. Portfolio Optimization Layer

Introducida durante Sprint 14.

### Metodología

```text
Binary Integer Programming
(PuLP)
```

### Restricciones implementadas

* Presupuesto máximo.
* Utilización mínima del presupuesto.
* Restricciones posicionales.
* Número máximo de incorporaciones.
* Nivel mínimo de jugador.
* Escenarios estratégicos.

---

### Player Level Layer (Sprint 14.1)

Niveles implementados:

* Development Prospect
* Rotation Profile
* First Team Ready
* Key Player Profile
* Elite Target

---

### Contribución metodológica

Esta capa introduce formalmente conceptos procedentes de:

* Operations Research.
* Decision Science.
* Portfolio Optimization.
* Strategic Recruitment Analytics.

Representa la principal evolución conceptual del proyecto.

---

## 12. Decision Support System Layer

Consolidada durante Sprint 12 y ampliada durante Sprint 14 y Sprint TM.2.

### Aplicación principal

```text
app/streamlit_app.py
```

### Capacidades actuales

#### Executive Dashboard

Visualización ejecutiva de oportunidades.

#### Player Intelligence

Benchmarking y análisis individual.

#### Recruitment Intelligence

Comparación y selección de candidatos.

#### Transfer Strategy Engine

Construcción de carteras optimizadas.

#### Portfolio Optimization

Simulación estratégica bajo restricciones.

#### Internationalization

Idiomas soportados:

* Español.
* Inglés.

---

### Cobertura DSS actual

```text
Modeling Dataset
↓
Scoring Dataset
↓
Opportunity Framework
↓
Ranking Engine
↓
Transfer Strategy Engine
↓
Decision Support System
```

Cobertura:

```text
11 ligas
77 league-seasons
```

La cobertura competitiva es ahora consistente en todas las capas del sistema.

---

# 🔄 Evolución arquitectónica

| Sprint       | Evolución                             |
| ------------ | ------------------------------------- |
| Sprint 1     | Positional Normalization              |
| Sprint 2     | Temporal Dynamics                     |
| Sprint 3     | Composite Football Indices            |
| Sprint 4     | Machine Learning                      |
| Sprint 4C    | Explainability                        |
| Sprint 5     | Opportunity Framework                 |
| Sprint 6     | Business Evaluation                   |
| Sprint 7     | Executive Dashboard                   |
| Sprint 9     | Decision Support Layer                |
| Sprint 10    | Player Intelligence                   |
| Sprint 11    | Recruitment Intelligence              |
| Sprint 12    | Productization & Internationalization |
| Sprint 13A   | Multi-League Expansion                |
| Sprint 13A.1 | External Validation Layer             |
| Sprint 13B   | Advanced Metrics Layer                |
| Sprint 14    | Transfer Strategy Engine              |
| Sprint 14.1  | Player Level Layer                    |
| TM.2         | Multi-League DSS Integration          |

---

# 🖥️ Arquitectura física

```text
market-value-football-tfm/

├── app/
├── artifacts/
├── config/
├── data/
├── docs/
├── mlruns/
├── notebooks/
├── reports/
│   ├── rankings/
│   ├── strategy/
│   ├── scouting_reports/
│   ├── data_quality/
│   └── sprint_13a1/
│
├── src/
│   ├── data/
│   ├── features/
│   ├── models/
│   ├── strategy/
│   └── utils/
│
└── tests/
```

---

# 🛣️ Roadmap arquitectónico

## TM.1 — Transfermarkt Coverage Audit

Estado:

```text
Backlog
```

Objetivo:

Analizar el techo teórico de matching y las limitaciones estructurales de integración entre FBref y Transfermarkt.

---

## Prioridad alta

### Contract Intelligence Layer

Variables previstas:

* años restantes de contrato;
* expiración contractual;
* proximidad a free agency.

---

### UEFA Club Strength Layer

Variables previstas:

* coeficiente UEFA;
* participaciones europeas;
* rendimiento continental.

---

### National Team Layer

Variables previstas:

* internacionalidades;
* minutos internacionales;
* torneos disputados.

---

## Investigación futura

### Machine Learning

* CatBoost.
* TabPFN.
* Ensemble Learning.

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

La arquitectura ha evolucionado desde un sistema de valoración de mercado hacia una plataforma DSS completa capaz de integrar:

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
Transfer Strategy Engine
↓
Portfolio Optimization
↓
Decision Support System
```

Sprint 13A aporta validez externa mediante expansión multi-liga.

Sprint 13A.1 aporta evidencia explícita de generalización mediante validación externa sobre once competiciones europeas, alcanzando el mejor rendimiento predictivo observado durante el proyecto:

```text
Tuned XGBoost
RMSE = 0.8525
MAE  = 0.6834
R²   = 0.5664
```

Sprint 13B aporta profundidad analítica mediante métricas avanzadas.

Sprint 14 introduce optimización bajo restricciones reales.

Sprint TM.2 garantiza consistencia metodológica de extremo a extremo entre modelización y DSS.

La versión productiva actual opera sobre una arquitectura completamente integrada de once ligas europeas y constituye la base funcional del Decision Support System desarrollado.

La versión actual constituye una arquitectura reproducible, interpretable y orientada a negocio preparada tanto para defensa académica como para evolución hacia una plataforma profesional de scouting y recruitment intelligence.

