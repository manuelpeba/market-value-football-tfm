# 🔄 Referencia de pipelines

::: {align="center"}
![Pipelines](https://img.shields.io/badge/Pipelines-Reproducible-success)
![Validation](https://img.shields.io/badge/Validation-Temporal-blue)
![Tracking](https://img.shields.io/badge/Tracking-MLflow-orange)
![Scouting](https://img.shields.io/badge/Scouting-Scoring%20Engine-success)
![Business](https://img.shields.io/badge/Business-Evaluation-purple)
![Status](https://img.shields.io/badge/Status-v0.7.0--Business--Validation-brightgreen)
:::

------------------------------------------------------------------------

# 🧠 Objetivo

Este documento describe los pipelines implementados, sus
responsabilidades, inputs, outputs y relaciones entre componentes.

Su objetivo es garantizar reproducibilidad experimental y trazabilidad
completa del sistema analítico.

------------------------------------------------------------------------

# 📊 Estado actual

  Pipeline                        Estado
  ----------------------------- --------
  Data ingestion                      ✅
  Feature engineering                 ✅
  Matching                            ✅
  Modeling dataset                    ✅
  Econometric modeling                ✅
  Machine Learning                    ✅
  Explainability                      ✅
  Scoring Engine                      ✅
  Ranking Engine                      ✅
  Evaluation & Business Layer         ✅

------------------------------------------------------------------------

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

I --> J[Evaluation]

J --> K[Business Outputs]

F --> L[MLflow]
G --> L
```

------------------------------------------------------------------------

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

------------------------------------------------------------------------

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

------------------------------------------------------------------------

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

------------------------------------------------------------------------

# 🚀 Evolución futura

-   Dashboard Streamlit
-   API scoring
-   Understat integration
-   Auto scouting reports
-   Continuous retraining
