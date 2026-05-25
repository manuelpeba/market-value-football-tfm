# Arquitectura del Sistema

## Estado actual

Arquitectura modular basada en CRISP-DM adaptado con:

-   Data ingestion
-   Feature engineering
-   Matching multi-fuente
-   Dataset jugador-temporada
-   Econometric layer
-   Machine Learning layer
-   Scoring layer
-   Evaluation layer
-   Business layer

------------------------------------------------------------------------

## Actualización Sprint 5--6

### Sprint 5 --- Scoring Engine

Nueva capa:

`src/models/scoring/`

Módulos:

-   build_inefficiency_score.py
-   build_growth_score.py
-   build_confidence_score.py
-   build_opportunity_score.py
-   generate_rankings.py

Flujo:

Predictions ↓ Inefficiency Score ↓ Growth Score ↓ Confidence Score ↓
Opportunity Score ↓ Automated Rankings

Outputs:

-   top_undervalued_global.csv
-   top_undervalued_by_league.csv
-   top_undervalued_by_position.csv
-   top_high_potential.csv
-   top_low_risk.csv
-   scouting_shortlist.csv

------------------------------------------------------------------------

### Sprint 6 --- Validation & Business Evaluation

Nueva capa:

`src/models/evaluation/`

Módulos:

-   build_ranking_diagnostics.py
-   build_roi_simulation.py
-   build_precision_at_k.py

Outputs:

reports/model_diagnostics/

-   ranking_summary.csv
-   ranking_by_league.csv
-   ranking_by_position.csv
-   ranking_score_correlations.csv
-   ranking_tier_summary.csv

reports/business/

-   roi_simulation.csv
-   roi_global_summary.csv
-   transfer_strategy_analysis.csv
-   roi_scouting_shortlist.csv

reports/evaluation/

-   precision_at_k.csv

------------------------------------------------------------------------

## Métricas de negocio

### Precision@K

-   Precision@10 = 0.90
-   Precision@20 = 0.90
-   Precision@50 = 0.90
-   Precision@100 = 0.85

### ROI Simulation

Indicadores:

-   expected_profit_eur
-   expected_roi_pct
-   risk_adjusted_profit
-   positive_roi_rate

------------------------------------------------------------------------

## Arquitectura final

Raw Data → Feature Engineering → Matching → Modeling Dataset → OLS / ML
→ Scoring Engine → Automated Rankings → Evaluation → Business Outputs

------------------------------------------------------------------------

## Conclusión

La arquitectura actual ya incorpora una capa de decisión de scouting y
una capa de validación de negocio, acercando el proyecto a un entorno de
Football Analytics profesional.
