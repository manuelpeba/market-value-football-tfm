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

---

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

---

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

---

### Sprint 7 --- Scouting Dashboard & Decision Support Layer

Nueva capa:

`dashboard/`

Componente principal:

`streamlit_app.py`

Objetivo:

Transformar rankings, métricas y predicciones en una herramienta operativa para departamentos de scouting y dirección deportiva.

Capacidades incorporadas:

#### Executive KPIs

- Precision@K
- % oportunidades rentables
- cobertura analítica
- tamaño de shortlist

#### Bubble Chart Coste vs Upside

- Opportunity Score visual
- tiers de oportunidad
- top oportunidades destacadas
- filtros interactivos

#### Ranking interactivo

- paginación
- filtros por liga
- posición
- club
- temporada

#### Informe individual

- valor mercado actual
- valor estimado
- gap de mercado
- Opportunity Score
- Growth Score
- Confidence Score

#### Explainability integrada

- SHAP local
- drivers positivos
- drivers negativos
- explicación de predicciones

Resultado arquitectónico:

Predictions
↓
Scoring Engine
↓
Ranking Engine
↓
Explainability
↓
Scouting Dashboard
↓
Decision Support


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

---

## Arquitectura final

Raw Data
→ Feature Engineering
→ Matching
→ Modeling Dataset
→ OLS / ML
→ Scoring Engine
→ Ranking Engine
→ Explainability
→ Scouting Dashboard
→ Decision Support

---

## Conclusión

La arquitectura actual incorpora una cadena completa de valor analítico:

Datos
→ Modelización
→ Scoring
→ Ranking
→ Explainability
→ Dashboard
→ Decisión deportiva

La incorporación del Dashboard Scouting durante Sprint 7 transforma el proyecto desde una plataforma analítica hacia un sistema de soporte a decisiones de Football Analytics profesional.
