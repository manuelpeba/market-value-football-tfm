# 📚 Diccionario de Datos

## Objetivo

Este documento describe las variables utilizadas en la versión:

```text
v2.0.0 — DSS Architecture, Data Contracts & Productization
```

Su objetivo es garantizar:

* trazabilidad
* reproducibilidad
* interpretabilidad
* coherencia semántica
* gobernanza de datos
* validez externa
* consistencia metodológica

---

# Unidad de análisis

```text
Jugador – Temporada
```

Cada observación representa:

* rendimiento deportivo
* contexto competitivo
* características demográficas
* valoración de mercado

de un jugador en una temporada concreta.

---

# Arquitectura conceptual

```text
Raw Sources
↓
Feature Engineering
↓
Advanced Metrics Layer
↓
Player Season Panel
↓
Modeling Dataset
↓
Predictions
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
```

La capa:

```text
Advanced Metrics Layer
```

fue incorporada durante Sprint 13B para integrar métricas avanzadas derivadas de FBref dentro del pipeline de modelización.

---

# Datasets principales

| Dataset                 | Ruta                                                                    |
| ----------------------- | ----------------------------------------------------------------------- |
| FBref Features          | data/processed/fbref_features_v13a.parquet                              |
| Transfermarkt Features  | data/processed/transfermarkt_features_v13a.parquet                      |
| Player Season Panel     | data/processed/player_season_panel_v13a.parquet                         |
| Modeling Dataset v13A   | data/processed/player_season_modeling_v13a.parquet                      |
| Advanced Dataset v13B   | data/processed/player_season_modeling_v13b_advanced.parquet             |
| Productive Dataset v13B | data/processed/player_season_modeling_v13b_productive_candidate.parquet |

---

# Dataset actual

## Universo modelizable

| Métrica            |                 Valor |
| ------------------ | --------------------: |
| Observaciones      |                 5.527 |
| Ligas              |                    11 |
| Temporadas         |                     7 |
| Cobertura temporal | 2019-2020 → 2025-2026 |

---

## Cobertura FBref

| Métrica                  |  Valor |
| ------------------------ | -----: |
| Observaciones procesadas | 43.591 |
| Liga-temporada           |     77 |

---

# Variables objetivo

## market_value_eur

Valor de mercado observado según Transfermarkt.

Tipo:

```text
Numérica continua
```

---

## log_market_value_eur

Target principal utilizado en modelización.

Transformación:

```text
log(market_value_eur)
```

Justificación:

* reducción de asimetría;
* reducción de heterocedasticidad;
* estabilidad estadística;
* mejora de capacidad predictiva.

---

# Variables identificadoras

## player_id_tm

Identificador principal Transfermarkt.

---

## player_name

Nombre original del jugador.

---

## player_name_normalized

Versión normalizada utilizada durante el matching.

---

## season

Temporada.

Ejemplo:

```text
2025-2026
```

---

## season_start_year

Año inicial de temporada.

Ejemplo:

```text
2025
```

Uso:

```text
Temporal Validation
```

---

# Variables demográficas

## age

Edad del jugador.

---

## age_squared

Edad al cuadrado.

Objetivo:

Capturar relaciones no lineales asociadas a la curva de edad.

Introducida en Sprint 2.

---

## birth_year

Año de nacimiento.

---

## career_year

Número de temporada observada dentro de la carrera del jugador.

Introducida en Sprint 2.

---

# Variables contextuales

## league

Competición principal.

Valores actuales:

* Premier League
* LaLiga
* Bundesliga
* Serie A
* Ligue 1
* Eredivisie
* Liga Portugal
* Championship
* Belgian Pro League
* Austrian Bundesliga
* Spanish Segunda División

Uso:

```text
Fixed Effects
```

---

## club

Club del jugador.

---

## position

Posición original.

---

## position_group

Valores:

```text
GK
DEF
MID
ATT
```

Uso:

```text
Fixed Effects
```

---

# Variables ofensivas

## goals

Goles.

---

## assists

Asistencias.

---

## goals_per90

Goles por 90 minutos.

---

## assists_per90

Asistencias por 90 minutos.

---

## g_a_per90

Contribuciones ofensivas por 90 minutos.

---

# Variables defensivas

## tackles_per90

Entradas por 90.

---

## interceptions_per90

Intercepciones por 90.

---

## blocks_per90

Bloqueos por 90.

---

## aerial_duels_won_pct

Porcentaje de duelos aéreos ganados.

---

# Variables de volumen

## minutes_played

Minutos disputados.

---

## log_minutes_played

Transformación logarítmica.

Uso:

```text
Feature principal de modelización
```

---

## starts

Titularidades.

---

## nineties

Partidos equivalentes completos.

---

# Variables de matching

## matching_status

Estado final del matching.

---

## matching_method

Valores posibles:

* exact_age_validated
* exact_age_club_validated
* fuzzy_age_club_validated

---

## matching_confidence

Rango:

```text
0 → 1
```

Representa confianza asociada al matching.

---

## age_diff

Diferencia de edad observada entre fuentes.

---

## club_score

Similitud entre clubes.

Utilizada durante validación de matching.

---

# Variables de crecimiento

Introducidas durante Sprint 2.

---

## market_value_prev_eur

Valor de mercado observado en temporada previa.

---

## market_value_growth_prev

Variación relativa respecto a la temporada anterior.

Objetivo:

Capturar dinámica de crecimiento.

---

## delta_log_market_value_prev

Variación logarítmica respecto a la temporada anterior.

Objetivo:

Capturar evolución económica reciente.

---

## breakout_indicator

Indicador de posible explosión deportiva.

Construido a partir de:

* edad
* trayectoria
* crecimiento observado

---

# Variables de normalización posicional

Introducidas durante Sprint 1.

---

## goals_per90_pos_z

Z-score de goles por 90.

Agrupación:

```text
position_group + league
```

---

## assists_per90_pos_z

Z-score de asistencias por 90.

Agrupación:

```text
position_group + league
```

---

## goals_position_percentile

Percentil ofensivo relativo.

---

## assists_position_percentile

Percentil creativo relativo.

---

# Variables compuestas

Introducidas progresivamente entre Sprint 2, Sprint 3 y Sprint 13B.

---

## finishing_index

Índice sintético de capacidad finalizadora.

---

## playmaking_index

Índice sintético de creación de juego.

---

## growth_index

Índice de potencial de crecimiento.

---

## experience_index

Índice de experiencia acumulada.

---

# Advanced Football Indices (Sprint 13B)

## finishing_index_v2

Índice sintético avanzado de capacidad finalizadora.

Origen:

```text
FBref Advanced Metrics
```

Objetivo:

Capturar eficiencia ofensiva y calidad de finalización mediante información agregada procedente de métricas avanzadas.

Resultado:

Variable avanzada con mayor relevancia predictiva agregada durante Sprint 13B.

---

## availability_index

Índice sintético de disponibilidad competitiva.

Origen:

```text
FBref Advanced Metrics
```

Objetivo:

Capturar continuidad competitiva, participación efectiva y disponibilidad del jugador durante la temporada.

---

## defensive_activity_index

Índice sintético de actividad defensiva.

Origen:

```text
FBref Advanced Metrics
```

Objetivo:

Capturar contribución defensiva agregada mediante métricas avanzadas de rendimiento.

---

## Estado actual

Las variables:

* finishing_index_v2
* availability_index
* defensive_activity_index

fueron promovidas a producción tras la validación experimental de Sprint 13B y permanecen en el conjunto oficial de features productivas de la versión v2.0.0.

# Variables de modelización

## target_variable

```text
log_market_value_eur
```

---

## modeling_split

Configuración actual:

| Split            | Temporadas            |
| ---------------- | --------------------- |
| Train            | 2019-2020 → 2024-2025 |
| Current Scouting | 2025-2026             |

La temporada 2025-2026 queda reservada para explotación operativa y no participa en el entrenamiento de modelos productivos.

---

## fixed_effects

Variables utilizadas en modelos econométricos:

* league
* season
* position_group

---

## leakage_columns

Variables explícitamente excluidas del entrenamiento para evitar fuga de información.

Principio:

```text
Toda variable predictiva debe existir
en el momento real de la decisión.
```

---

# Modelos oficiales

## Benchmark econométrico

Modelo oficial:

```text
Growth OLS v13B
```

Rol:

```text
Interpretabilidad
+
Benchmark académico
```

---

## Modelo productivo

Modelo oficial:

```text
Tuned XGBoost v13B
```

Rol:

```text
Predicción operativa
```

---

## Resultados Sprint 13B

### Econometría

| Modelo                |     R² |
| --------------------- | -----: |
| M_A_v13A_base_spec_FE | 0.4505 |
| M_B_v13B_advanced_FE  | 0.4549 |

Resultado:

```text
ΔR² = +0.0044
```

---

### Machine Learning

| Modelo               | Mejora observada |
| -------------------- | ---------------: |
| XGBoost              |          +0.0096 |
| Random Forest        |          +0.0097 |
| HistGradientBoosting |          +0.0144 |
| LightGBM             |          +0.0291 |

Conclusión:

Todas las arquitecturas evaluadas mejoran simultáneamente tras incorporar las nuevas variables avanzadas.

---

# Variables de Scoring

Introducidas progresivamente entre Sprint 5 y Sprint 10.

Estas variables no participan en entrenamiento de modelos.

Su objetivo es transformar predicciones en señales accionables para scouting y recruitment.

---

## predicted_market_value_eur

Valor de mercado estimado por el modelo productivo.

Modelo actual:

```text
Tuned XGBoost v13B
```

---

## predicted_log_market_value

Predicción en escala logarítmica.

Utilizada internamente durante modelización.

---

## market_value_gap_eur

Diferencia absoluta entre:

```text
Valor esperado
-
Valor observado
```

Interpretación:

```text
Mispricing absoluto
```

---

## market_value_gap_pct

Diferencia relativa entre:

```text
Valor esperado
-
Valor observado
```

Interpretación:

```text
Mispricing porcentual
```

---

## inefficiency_score

Objetivo:

```text
Detección de infravaloración
```

Captura desviaciones positivas entre valor esperado y valor observado.

---

## growth_score

Objetivo:

```text
Potencial futuro
```

Integra señales asociadas a:

* edad
* trayectoria
* evolución reciente
* desarrollo deportivo

---

## confidence_score

Objetivo:

```text
Robustez analítica
```

Captura estabilidad y confianza asociada a cada recomendación.

---

## opportunity_score

Score principal de priorización.

Implementación conceptual:

```python
0.55 * inefficiency_score_z +
0.25 * growth_score_z +
0.20 * confidence_score_z
```

Interpretación:

```text
A mayor valor,
mayor atractivo potencial
para scouting.
```

---

# Variables de Riesgo

Introducidas durante Sprint 10.3.

Objetivo:

Separar oportunidad y riesgo.

---

## risk_score

Nueva métrica diseñada para cuantificar incertidumbre asociada a cada recomendación.

Principio:

```text
Alta oportunidad
≠
bajo riesgo
```

---

## risk_level

Clasificación categórica.

Valores:

```text
Low
Medium
High
```

---

## risk_adjusted_opportunity_score

Opportunity Score ajustada por riesgo.

Uso principal:

```text
Priorización ejecutiva
```

---

# Player Intelligence Variables

Introducidas durante Sprint 10.1.

Objetivo:

Transformar rankings en análisis individuales.

---

## radar_percentile

Percentil relativo de una métrica.

Utilizado en:

```text
Player Radar
```

---

## benchmark_group

Universo de comparación.

Valores:

```text
Position
Global
```

---

## scouting_rating

Clasificación cualitativa.

Ejemplos:

```text
Elite
Superior
Average
Below Average
```

---

## player_profile

Clasificación descriptiva generada a partir de métricas deportivas.

Utilizada en scouting reports.

---

# Recruitment Intelligence Variables

Introducidas durante Sprint 11.

Objetivo:

Facilitar procesos reales de captación de talento.

---

## shortlist_status

Estado dentro de Recruitment Board.

---

## candidate_rank

Posición relativa dentro de shortlist.

---

## recruitment_priority

Prioridad asignada por el sistema.

---

## comparative_score

Resultado agregado utilizado en comparativas multi-jugador.

---

# Tracking Variables

Utilizadas para trazabilidad experimental.

---

## experiment_id

Identificador MLflow.

---

## run_id

Identificador de ejecución.

---

## model_name

Modelo utilizado.

Ejemplos:

```text
Growth OLS v13B
Tuned XGBoost v13B
LightGBM
```

---

## model_version

Versión del modelo.

---

## training_timestamp

Fecha de entrenamiento.

---

# Outputs operativos

## Historical Evaluation Layer

Artefactos:

```text
tuned_xgboost_test_predictions.csv
tuned_xgboost_full_predictions.csv
ml_tuned_model_comparison.csv
```

Objetivo:

```text
Validación académica
```

---

## Current Scouting Layer

Artefactos principales:

```text
tuned_xgboost_predictions.csv
```

Objetivo:

```text
Scouting operativo
```

---

## Estado de integración de scoring

Durante Sprint 13B se identificó una separación estructural entre:

```text
Modeling Pipeline
≠
Scoring Pipeline
```

El pipeline histórico de scoring requiere variables enriquecidas adicionales no presentes actualmente en la capa productiva de predicción.

Por este motivo, la integración completa entre:

```text
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

quedó documentada entonces como trabajo independiente y fue completada posteriormente en TM.2.

Backlog asociado:

```text
TM.2 — Scoring & Ranking Integration v13B
```

Esta limitación no afecta a:

* resultados econométricos;
* resultados de Machine Learning;
* validación de la hipótesis principal de Sprint 13B.

---

## Player Intelligence Layer

Artefactos:

```text
Player Radar
Positional Benchmarking
Scouting Narrative
```

---

## Recruitment Intelligence Layer

Artefactos:

```text
Recruitment Board
Candidate Comparison
Shortlist Analysis
```

---

# Coverage Diagnostics Variables

Introducidas durante Sprint 13A.1.

Objetivo:

Auditar cobertura y calidad de integración.

---

## match_rate

Porcentaje de matching válido.

---

## matched_records

Observaciones correctamente emparejadas.

---

## unmatched_records

Observaciones sin correspondencia válida.

---

## coverage_rate

Cobertura efectiva alcanzada por competición o temporada.

---

# Artefactos Sprint 13A.1

Generados automáticamente:

```text
reports/data_quality/

sprint_13a_matching_by_league.csv

sprint_13a_matching_by_league_season.csv

sprint_13a_coverage_summary.md
```

---

# Universo actual

## Cobertura competitiva

Ligas integradas:

* Premier League
* LaLiga
* Bundesliga
* Serie A
* Ligue 1
* Eredivisie
* Liga Portugal
* Championship
* Belgian Pro League
* Austrian Bundesliga
* Spanish Segunda División

---

## Métricas estructurales

| Métrica                        |  Valor |
| ------------------------------ | -----: |
| Observaciones FBref procesadas | 43.591 |
| Dataset modelizable            |  5.527 |
| Ligas                          |     11 |
| Temporadas                     |      7 |
| Liga-temporada                 |     77 |
| Match Rate global              | 75,97% |

---

# Variables excluidas por leakage

No pueden utilizarse como inputs de modelos.

---

## Leakage económico

* market_value_next_eur
* market_value_growth_1y
* delta_log_market_value_1y

---

## Leakage predictivo

* predicted_market_value_eur
* predicted_log_market_value

---

## Leakage de scoring

* inefficiency_score
* growth_score
* confidence_score
* opportunity_score
* risk_score

---

## Leakage operacional

* rankings derivados
* shortlist outputs
* recruitment outputs

---

Principio:

```text
Toda variable predictiva debe existir
en el momento real de la decisión.
```

---

# Limitaciones actuales

## Datos avanzados

Actualmente no se incorporan:

* tracking data
* salarios
* contratos
* event data avanzado
* datos espaciales

---

## Valor de mercado

Transfermarkt incorpora componentes no observables directamente en los datos deportivos:

* reputación
* percepción humana
* contexto mediático
* expectativas de mercado

Por tanto:

```text
Valor de mercado
≠
precio real de transferencia
```

---

## Cobertura

Las ligas secundarias presentan menor cobertura histórica disponible en Transfermarkt-Kaggle.

---

# Conclusión

El diccionario de datos refleja la evolución completa del proyecto desde un sistema de estimación de valor de mercado hacia una plataforma integral de Football Analytics.

La arquitectura actual integra:

* Data Engineering
* Econometrics
* Machine Learning
* Explainability
* Scoring
* Risk Framework
* Player Intelligence
* Recruitment Intelligence
* Decision Support System
* External Validation
* Advanced Football Metrics

Las principales contribuciones metodológicas de la versión:

```text
v2.0.0 — DSS Architecture, Data Contracts & Productization
```

son:

### Sprint 13A

* expansión a 11 ligas;
* validación externa;
* auditoría de cobertura.

### Sprint 13B

* integración de métricas avanzadas FBref;
* Composite Football Indices v2;
* mejora simultánea en econometría y Machine Learning;
* promoción de nuevas variables productivas.

El universo actual:

| Métrica       | Valor |
| ------------- | ----: |
| Observaciones | 5.527 |
| Ligas         |    11 |
| Temporadas    |     7 |

constituye el mayor dataset utilizado por el proyecto hasta la fecha.

La evolución metodológica del sistema puede resumirse mediante:

```text
Performance Data
+
Market Data
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
Decision Support System
↓
External Validation
↓
Advanced Data Expansion
```

lo que consolida la transición desde un proyecto de modelización predictiva hacia una plataforma integral de apoyo a decisiones deportivas basada en datos.

## Extensión semántica v2.0.0

El diccionario se interpreta ahora por contexto:

- `season_*`: verdad histórica utilizada por la autoridad de modelado;
- `current_*_snapshot`: fotografía vigente procedente del snapshot canónico;
- `display_*`: adaptación de presentación derivada del snapshot;
- campos de identidad: resueltos por el Player Registry;
- `risk_score` y derivados: servidos por la Risk Authority.

Los campos `context_changed`, `club_context_changed`, `league_context_changed`, `valuation_context` y `gap_interpretation_status` controlan cuándo un gap histórico puede mostrarse como referencia actual. Véase [data_contract.md](data_contract.md) para las invariantes obligatorias.
