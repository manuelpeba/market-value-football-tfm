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
-   Explainability layer
-   Visual Analytics layer
-   Decision Support layer
-   Business layer

---

## Evolución arquitectónica por sprints

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

---

### Sprint 9 --- Executive Dashboard & Decision Support System

Nueva evolución de la capa:

`dashboard/`

Componente principal:

`streamlit_app.py`

Objetivo:

Transformar el dashboard inicial en una herramienta de soporte a decisiones orientada a scouting profesional.

---

#### Sprint 9.1 --- Executive Scouting Filters

Capacidades incorporadas:

* presets de scouting
* filtros ejecutivos automáticos
* universo modelado visible
* shortlist dinámica
* filtros activos visibles
* segmentación avanzada

Variables de segmentación:

* Liga
* Posición
* Edad
* Opportunity Score
* Confidence Score

Resultado:

El dashboard evoluciona desde una visualización estática hacia una herramienta interactiva de exploración del mercado.

---

#### Sprint 9.2 --- Visual Analytics & Opportunity Matrix

Nuevos componentes:

##### Coste actual vs Upside estimado

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

##### Segmentación estratégica

Zonas automáticas:

* Comprar / priorizar
* Oportunidades premium
* Seguimiento
* Menor prioridad

##### Executive Insights

Nueva capa de síntesis:

* candidatos prioritarios
* oportunidades premium
* score oportunidad medio
* upside agregado
* liga dominante

##### Top 5 destacados

Identificación automática de las mejores oportunidades dentro de los filtros activos.

Resultado arquitectónico:

```text
Predictions
↓
Scoring Engine
↓
Ranking Engine
↓
Visual Analytics
↓
Decision Support
↓
Scouting Intelligence
```

---

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
→ Econometric Layer
→ Machine Learning Layer
→ Scoring Engine
→ Ranking Engine
→ Explainability
→ Visual Analytics
→ Decision Support
→ Scouting Intelligence

---

## Conclusión

## Conclusión

La arquitectura actual implementa una cadena completa de valor analítico aplicada al mercado de fichajes:

```text
Datos
↓
Feature Engineering
↓
Modelización
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

La evolución arquitectónica desarrollada entre los Sprints 5 y 9 transforma el proyecto desde un sistema de predicción de valor de mercado hacia una plataforma de Football Analytics orientada a identificación, priorización y justificación de oportunidades de mercado.

La incorporación de la capa de Visual Analytics y Decision Support constituye la principal evolución funcional del proyecto, permitiendo convertir predicciones y rankings en recomendaciones accionables para procesos reales de scouting profesional.

