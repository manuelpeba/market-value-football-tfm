# 🔄 Referencia de pipelines

::: {align="center"}
![Pipelines](https://img.shields.io/badge/Pipelines-Reproducible-success)
![Validation](https://img.shields.io/badge/Validation-Temporal-blue)
![Tracking](https://img.shields.io/badge/Tracking-MLflow-orange)
![Scouting](https://img.shields.io/badge/Scouting-Scoring%20Engine-success)
![Business](https://img.shields.io/badge/Business-Evaluation-purple)
![Dashboard](https://img.shields.io/badge/Dashboard-Streamlit-success)
![Explainability](https://img.shields.io/badge/Explainability-SHAP-success)
![Status](https://img.shields.io/badge/Status-v0.8.0--Executive--Dashboard-brightgreen)
![DecisionSupport](https://img.shields.io/badge/Decision%20Support-System-success)
![VisualAnalytics](https://img.shields.io/badge/Visual%20Analytics-Executive-success)
:::

---

# 🧠 Objetivo

Este documento describe los pipelines implementados, sus
responsabilidades, inputs, outputs y relaciones entre componentes.

Su objetivo es garantizar reproducibilidad experimental y trazabilidad
completa del sistema analítico.

---

# 📊 Estado actual

| Pipeline | Estado |
|----------|----------|
| Data ingestion | ✅ |
| Feature engineering | ✅ |
| Matching | ✅ |
| Modeling dataset | ✅ |
| Econometric modeling | ✅ |
| Machine Learning | ✅ |
| Explainability | ✅ |
| Scoring Engine | ✅ |
| Ranking Engine | ✅ |
| Evaluation & Business Layer | ✅ |
| Dashboard Scouting | ✅ |
| Visual Analytics | ✅ |
| Decision Support Layer | ✅ |

---

# 🏗️ Pipeline global

``` mermaid
flowchart TD

A[Raw Sources]
--> B[Feature Engineering]

B --> C[Matching]

C --> D[Player Season Panel]

D --> E[Modeling Dataset]

E --> F[Econometric Pipeline]
E --> G[Machine Learning Pipeline]

F --> H[Scoring Engine]
G --> H

H --> I[Ranking Engine]

I --> J[Explainability]

J --> K[Executive Dashboard]

K --> L[Visual Analytics]

L --> M[Decision Support]

M --> N[Scouting Intelligence]

F --> O[MLflow]
G --> O
```

---

# 🤖 Machine Learning Pipeline

Pipeline principal:

``` text
src/models/machine_learning/train_ml_tuned.py
```

Modelos:

-   Tuned Random Forest
-   Tuned XGBoost
-   Tuned LightGBM
-   HistGradientBoosting

Modelo seleccionado:

``` text
Tuned XGBoost
R² = 0.5536
RMSE = 0.8753
MAE = 0.7004
```

---

# 🎯 Scoring Pipeline

``` text
Predictions
 ↓
build_inefficiency_score.py
 ↓
build_growth_score.py
 ↓
build_confidence_score.py
 ↓
build_opportunity_score.py
 ↓
generate_rankings.py
```

Outputs:

``` text
reports/rankings/

scouting_shortlist.csv
top_undervalued_global.csv
top_undervalued_by_league.csv
top_undervalued_by_position.csv
top_high_potential.csv
top_low_risk.csv
```

---

# 📈 Evaluation Pipeline

``` text
src/models/evaluation/

build_ranking_diagnostics.py
build_roi_simulation.py
build_precision_at_k.py
```

Outputs:

``` text
reports/model_diagnostics/
reports/business/
reports/evaluation/
```

Métricas:

-   Precision@K
-   Expected ROI
-   Positive ROI rate
-   Risk-adjusted profit

Resultados actuales:

  K       Precision@K
  ----- -------------
  10             0.90
  20             0.90
  50             0.90
  100            0.85

---

# 🖥️ Executive Dashboard Pipeline

Pipeline principal:

```text
dashboard/
streamlit_app.py
```

Objetivo:

Transformar predicciones, rankings y señales de scouting en una herramienta de apoyo a decisiones para departamentos deportivos.

---

## Sprint 9.1 — Executive Scouting Filters

Capacidades:

* presets de scouting
* filtros ejecutivos
* shortlist dinámica
* universo modelado visible
* métricas de cobertura
* filtros activos visibles

Variables:

* Liga
* Posición
* Edad
* Opportunity Score
* Confidence Score

---

## Sprint 9.2 — Visual Analytics

### Coste actual vs Upside estimado

Matriz estratégica basada en:

* valor de mercado actual
* gap de mercado estimado
* Opportunity Score
* tier de oportunidad

Representación:

```text
Eje X → Coste actual
Eje Y → Upside estimado
Tamaño → Opportunity Score
Color → Prioridad scouting
```

### Segmentación estratégica

* Comprar / priorizar
* Oportunidades premium
* Seguimiento
* Menor prioridad

### Hallazgos ejecutivos

* candidatos prioritarios
* oportunidades premium
* score oportunidad medio
* upside agregado
* liga dominante

### Top 5 destacados

Identificación automática de oportunidades prioritarias.

---

## Informe individual

* Opportunity Score
* Growth Score
* Confidence Score
* Valor estimado
* Gap de mercado
* Recomendación analítica

---

## Explainability

* SHAP local
* drivers positivos
* drivers negativos
* explicación ejecutiva

Resultado:

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
↓
Scouting Intelligence
```

---

### Sprint 10 — Advanced Player Intelligence

- radar avanzado de jugador
- comparador jugador vs jugador
- comparador jugador vs percentil de liga
- scouting cards descargables
- exportación PDF de perfiles

### Sprint 11 — Advanced Explainability

- SHAP por posición
- SHAP por liga
- explicación avanzada de rankings
- estabilidad de rankings

### Sprint 12 — Advanced Feature Engineering

- progression metrics
- carrying metrics
- passing value metrics
- percentiles avanzados
- normalización por liga

### Roadmap técnico

- API scoring
- Understat integration
- Continuous retraining
- Business Validation Layer

## Conclusión

La arquitectura de pipelines implementada permite recorrer de forma reproducible todo el ciclo analítico:

```text
Raw Data
↓
Feature Engineering
↓
Matching
↓
Modeling
↓
Scoring
↓
Ranking
↓
Explainability
↓
Visual Analytics
↓
Decision Support
↓
Scouting Intelligence
```

Tras la incorporación del Executive Dashboard (Sprint 9), el sistema deja de ser únicamente un conjunto de pipelines de modelización para convertirse en una plataforma integrada de Football Analytics orientada a identificación, priorización y justificación de oportunidades de mercado.

