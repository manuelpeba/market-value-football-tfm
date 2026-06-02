# 📚 Diccionario de Datos

## Objetivo

Este documento describe las variables utilizadas en la versión v1.0.0 — Scouting Intelligence Platform.

Su objetivo es garantizar:

- trazabilidad
- reproducibilidad
- interpretabilidad
- coherencia semántica
- gobernanza de datos

---

# Unidad de análisis

```text
Jugador – Temporada
```

Cada observación representa:

- rendimiento deportivo
- contexto competitivo
- características demográficas
- valoración de mercado

de un jugador en una temporada concreta.

---

# Datasets principales

| Dataset | Ruta |
|----------|------|
| FBref features | data/processed/fbref_features.parquet |
| Transfermarkt features | data/processed/transfermarkt_features.parquet |
| Player Season Panel | data/processed/player_season_panel.parquet |
| Modeling Dataset | data/processed/player_season_modeling.parquet |

---

# Arquitectura de datos

```text
Raw Sources
↓
Features
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
Dashboard
```

---

# Dataset actual

| Métrica | Valor |
|----------|----------:|
| Observaciones | 3.916 |
| Jugadores únicos | 2.136 |
| Cobertura temporal | 2019-2020 → 2025-2026 |

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

- reducción de asimetría
- reducción de heterocedasticidad
- mayor estabilidad estadística

---

# Variables identificadoras

## player_name

Nombre original del jugador.

## player_name_normalized

Versión normalizada utilizada para matching.

## player_id

Identificador interno.

## season

Temporada.

Ejemplo:

```text
2025-2026
```

---

# Variables demográficas

## age

Edad del jugador.

## birth_year

Año de nacimiento.

---

# Variables contextuales

## league

Valores:

- Premier League
- LaLiga
- Bundesliga
- Serie A
- Ligue 1
- Eredivisie
- Liga Portugal

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

## assists

Asistencias.

## goals_per90

Goles por 90 minutos.

## assists_per90

Asistencias por 90 minutos.

## g_a_per90

Contribuciones ofensivas por 90.

---

# Variables defensivas

Actualmente limitadas en el dataset operativo.

Variables disponibles:

## tackles_per90

Entradas por 90.

## interceptions_per90

Intercepciones por 90.

## blocks_per90

Bloqueos por 90.

## aerial_duels_won_pct

Porcentaje de duelos aéreos ganados.

---

# Variables de volumen

## minutes_played

Minutos disputados.

## log_minutes_played

Transformación logarítmica.

## starts

Titularidades.

## nineties

Partidos equivalentes completos.

---

# Variables derivadas

## market_value_prev_eur

Valor de mercado previo.

## market_value_next_eur

Valor futuro.

Uso:

```text
Evaluación longitudinal
```

---

## market_value_growth_1y

Variación anual absoluta.

---

## delta_log_market_value_1y

Variación logarítmica anual.

---

# Variables de matching

## matching_status

Estado del matching.

## matching_method

Valores:

- exact_age_validated
- exact_age_club_validated
- fuzzy_age_club_validated

## matching_confidence

Rango:

```text
0 → 1
```

## age_diff

Diferencia de edad.

## club_score

Similitud entre clubes.

---

# Variables de modelización

## target_variable

```text
log_market_value_eur
```

---

## modeling_split

Configuración actual:

| Split | Temporadas |
|----------|------------|
| Train | 2019-2020 → 2024-2025 |
| Scouting | 2025-2026 |

---

## fixed_effects

Variables:

- league
- season
- position_group

---

# Variables de scoring

Introducidas progresivamente entre Sprint 5 y Sprint 10.

---

## predicted_market_value_eur

Valor de mercado estimado.

---

## predicted_log_market_value

Predicción en escala logarítmica.

---

## market_value_gap_eur

Diferencia absoluta entre valor esperado y observado.

---

## market_value_gap_pct

Diferencia porcentual.

---

## inefficiency_score

Objetivo:

```text
Detección de infravaloración
```

---

## growth_score

Objetivo:

```text
Capturar potencial futuro
```

---

## confidence_score

Objetivo:

```text
Capturar robustez analítica
```

---

## opportunity_score

Score principal de priorización.

Implementación conceptual:

```python
0.55 * inefficiency_score_z +
0.25 * growth_score_z +
0.20 * confidence_score_z
```

---

# Sprint 10 — Nuevas variables

Sprint 10 incorpora una nueva capa analítica.

---

## risk_score

Nueva métrica introducida en Sprint 10.3.

Objetivo:

```text
Cuantificar incertidumbre
```

Interpretación:

| Nivel | Significado |
|----------|-------------|
| Bajo | Perfil estable |
| Medio | Riesgo moderado |
| Alto | Riesgo elevado |

---

## risk_level

Categoría derivada.

Valores:

```text
Low
Medium
High
```

---

## risk_adjusted_opportunity_score

Opportunity Score ajustada por riesgo.

Uso:

```text
Priorización operativa
```

---

# Player Intelligence Variables

Introducidas en Sprint 10.1.

---

## radar_percentile

Percentil de una métrica frente al benchmark.

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
Promedio
Bajo
```

---

# Variables de tracking

## experiment_id

Identificador MLflow.

## run_id

Identificador de ejecución.

## model_name

Nombre del modelo.

## model_version

Versión del modelo.

## training_timestamp

Fecha de entrenamiento.

---

# Outputs operativos

## Historical Evaluation Layer

Artefactos:

```text
tuned_xgboost_test_predictions.csv
tuned_xgboost_full_predictions.csv
```

---

## Current Scouting Layer

Artefactos:

```text
tuned_xgboost_predictions.csv
scoring_dataset.csv
scouting_shortlist.csv
scouting_shortlist_with_risk.csv
```

---

## Player Intelligence Layer

Artefactos:

```text
player radar
benchmarking
scouting narrative
```

---

# Variables excluidas por leakage

No pueden utilizarse como inputs:

- market_value_next_eur
- delta_log_market_value_1y
- predicted_market_value_eur
- inefficiency_score
- opportunity_score
- risk_score
- rankings derivados

Principio:

```text
Toda variable predictiva debe existir
en el momento real de la decisión.
```

---

# Limitaciones actuales

## Datos

Pendiente:

- Understat
- xG
- xA
- salarios
- contratos

---

## FBref avanzado

Auditado durante Sprint 10.2.

Tablas evaluadas:

- Shooting
- Defense
- Misc
- Playing Time
- Passing
- Possession
- Goal & Shot Creation

Resultado:

```text
Viabilidad confirmada para futuras integraciones
```

---

# Variables previstas futuras

## Sprint 11

Advanced Football Radar

Variables previstas:

- shots_per90
- shots_on_target_per90
- tackles_won_per90
- interceptions_per90
- blocks_per90
- fouls_drawn_per90
- crosses_per90

---

## Sprint 12

Understat Integration

Variables previstas:

- xG
- xA
- xG_per90
- xA_per90

---

# Conclusión

El diccionario de datos refleja la evolución del proyecto desde una arquitectura centrada en modelización hacia una plataforma completa de Scouting Intelligence.

La principal ampliación introducida en Sprint 10 es la incorporación de:

- Risk Framework
- Current Scouting Layer
- Player Intelligence Layer
- Positional Benchmarking

permitiendo transformar variables deportivas y económicas en recomendaciones operativas para scouting profesional.
