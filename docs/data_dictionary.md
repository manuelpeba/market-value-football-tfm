````md
# 📚 Diccionario de datos

<div align="center">

![Dataset](https://img.shields.io/badge/Dataset-Player%20Season-orange)
![Modeling](https://img.shields.io/badge/Modeling-Econometrics%20%2B%20ML-blue)
![Validation](https://img.shields.io/badge/Validation-Temporal-important)
![Tracking](https://img.shields.io/badge/Tracking-MLflow-success)
![Config](https://img.shields.io/badge/Configuration-Centralized-purple)

</div>

---

# 📑 Tabla de contenidos

- [🧠 Objetivo del documento](#-objetivo-del-documento)
- [🏗️ Unidad de análisis](#️-unidad-de-análisis)
- [📦 Datasets principales](#-datasets-principales)
- [📂 Arquitectura de datos](#-arquitectura-de-datos)
- [🎯 Variables objetivo](#-variables-objetivo)
- [📊 Variables identificadoras](#-variables-identificadoras)
- [👤 Variables demográficas](#-variables-demográficas)
- [🏟️ Variables contextuales](#️-variables-contextuales)
- [⚽ Variables de rendimiento ofensivo](#-variables-de-rendimiento-ofensivo)
- [🛡️ Variables defensivas](#️-variables-defensivas)
- [⏱️ Variables de volumen de juego](#️-variables-de-volumen-de-juego)
- [📈 Variables derivadas](#-variables-derivadas)
- [🔗 Variables de matching](#-variables-de-matching)
- [📊 Variables de modelización](#-variables-de-modelización)
- [💡 Variables de scoring](#-variables-de-scoring)
- [🧪 Variables experimentales y tracking](#-variables-experimentales-y-tracking)
- [⚙️ Variables de configuración](#️-variables-de-configuración)
- [📤 Outputs generados](#-outputs-generados)
- [🛡️ Variables excluidas por leakage](#️-variables-excluidas-por-leakage)
- [📉 Limitaciones actuales](#-limitaciones-actuales)
- [🚀 Variables previstas futuras](#-variables-previstas-futuras)

---

# 🧠 Objetivo del documento

Este documento describe las principales variables utilizadas en el sistema analítico para:

- integración de fuentes
- feature engineering
- modelización econométrica
- Machine Learning
- scoring cuantitativo
- experiment tracking
- validación temporal

El objetivo es garantizar:

- transparencia metodológica
- interpretabilidad
- trazabilidad analítica
- reproducibilidad
- coherencia semántica entre pipelines

---

# 🏗️ Unidad de análisis

La unidad de análisis utilizada es:

```text
Jugador – Temporada
```

Cada observación representa:

* rendimiento deportivo
* contexto competitivo
* características demográficas
* valor de mercado

de un jugador en una temporada concreta.

---

# 📦 Datasets principales

| Dataset                | Ruta                                            |
| ---------------------- | ----------------------------------------------- |
| FBref features         | `data/processed/fbref_features.parquet`         |
| Transfermarkt features | `data/processed/transfermarkt_features.parquet` |
| Player-season panel    | `data/processed/player_season_panel.parquet`    |
| Modeling dataset       | `data/processed/player_season_modeling.parquet` |

---

# 📂 Arquitectura de datos

```text
raw data
→ processed features
→ player-season panel
→ modeling dataset
→ predictions
→ scoring outputs
→ reports
→ MLflow tracking
```

---

# 🎯 Variables objetivo

## market_value_eur

| Campo  | Valor                  |
| ------ | ---------------------- |
| Tipo   | Numérica continua      |
| Fuente | Transfermarkt          |
| Unidad | Euros                  |
| Uso    | Valor de mercado bruto |

### Descripción

Valor de mercado observado del jugador según Transfermarkt.

---

## log_market_value_eur

| Campo          | Valor                       |
| -------------- | --------------------------- |
| Tipo           | Numérica continua           |
| Transformación | Log natural                 |
| Uso            | Variable objetivo principal |

### Descripción

Transformación logarítmica del valor de mercado utilizada en modelización econométrica y ML.

### Justificación

La transformación reduce:

* asimetría
* heterocedasticidad
* impacto de outliers

---

# 📊 Variables identificadoras

## player_name

| Campo | Valor                 |
| ----- | --------------------- |
| Tipo  | String                |
| Uso   | Identificación visual |

### Descripción

Nombre original del jugador.

---

## player_name_normalized

| Campo | Valor    |
| ----- | -------- |
| Tipo  | String   |
| Uso   | Matching |

### Descripción

Versión normalizada utilizada en matching multi-fuente.

### Transformaciones

* lowercase
* eliminación de acentos
* limpieza de caracteres especiales

---

## player_id

| Campo | Valor                 |
| ----- | --------------------- |
| Tipo  | String                |
| Uso   | Identificador interno |

### Descripción

Identificador interno utilizado durante integración y pipelines.

---

## season

| Campo   | Valor             |
| ------- | ----------------- |
| Tipo    | String            |
| Ejemplo | `2024-2025`       |
| Uso     | Contexto temporal |

---

# 👤 Variables demográficas

## age

| Campo  | Valor             |
| ------ | ----------------- |
| Tipo   | Numérica          |
| Unidad | Años              |
| Uso    | Feature principal |

### Descripción

Edad del jugador durante la temporada.

---

## birth_year

| Campo | Valor      |
| ----- | ---------- |
| Tipo  | Numérica   |
| Uso   | Validación |

### Descripción

Año de nacimiento cuando está disponible.

---

# 🏟️ Variables contextuales

## league

| Campo | Valor        |
| ----- | ------------ |
| Tipo  | Categórica   |
| Uso   | Fixed effect |

### Valores principales

* Premier League
* LaLiga
* Bundesliga
* Serie A
* Ligue 1
* Eredivisie
* Liga Portugal

---

## club

| Campo | Valor               |
| ----- | ------------------- |
| Tipo  | String              |
| Uso   | Matching y contexto |

---

## position

| Campo | Valor                  |
| ----- | ---------------------- |
| Tipo  | String                 |
| Uso   | Clasificación original |

---

## position_group

| Campo | Valor        |
| ----- | ------------ |
| Tipo  | Categórica   |
| Uso   | Fixed effect |

### Valores

* GK
* DEF
* MID
* ATT

---

# ⚽ Variables de rendimiento ofensivo

## goals

| Campo | Valor               |
| ----- | ------------------- |
| Tipo  | Numérica            |
| Uso   | Producción ofensiva |

---

## assists

| Campo | Valor               |
| ----- | ------------------- |
| Tipo  | Numérica            |
| Uso   | Producción ofensiva |

---

## goals_per90

| Campo | Valor             |
| ----- | ----------------- |
| Tipo  | Numérica          |
| Uso   | Feature principal |

### Descripción

Goles anotados por 90 minutos.

---

## assists_per90

| Campo | Valor             |
| ----- | ----------------- |
| Tipo  | Numérica          |
| Uso   | Feature principal |

### Descripción

Asistencias por 90 minutos.

---

## g_a_per90

| Campo | Valor                        |
| ----- | ---------------------------- |
| Tipo  | Numérica                     |
| Uso   | Producción ofensiva agregada |

### Descripción

Contribuciones ofensivas totales por 90 minutos.

---

## shots_per90

| Campo | Valor              |
| ----- | ------------------ |
| Tipo  | Numérica           |
| Uso   | Potencial ofensivo |

---

# 🛡️ Variables defensivas

## tackles_per90

| Campo | Valor                 |
| ----- | --------------------- |
| Tipo  | Numérica              |
| Uso   | Rendimiento defensivo |

---

## interceptions_per90

| Campo | Valor                 |
| ----- | --------------------- |
| Tipo  | Numérica              |
| Uso   | Rendimiento defensivo |

---

## blocks_per90

| Campo | Valor                 |
| ----- | --------------------- |
| Tipo  | Numérica              |
| Uso   | Rendimiento defensivo |

---

## aerial_duels_won_pct

| Campo  | Valor         |
| ------ | ------------- |
| Tipo   | Numérica      |
| Unidad | Porcentaje    |
| Uso    | Dominio aéreo |

---

# ⏱️ Variables de volumen de juego

## minutes_played

| Campo  | Valor             |
| ------ | ----------------- |
| Tipo   | Numérica          |
| Unidad | Minutos           |
| Uso    | Feature principal |

---

## log_minutes_played

| Campo          | Valor        |
| -------------- | ------------ |
| Tipo           | Numérica     |
| Transformación | Log natural  |
| Uso            | Modelización |

---

## starts

| Campo | Valor         |
| ----- | ------------- |
| Tipo  | Numérica      |
| Uso   | Participación |

---

## nineties

| Campo | Valor                |
| ----- | -------------------- |
| Tipo  | Numérica             |
| Uso   | Normalización por 90 |

---

# 📈 Variables derivadas

## market_value_growth_1y

| Campo | Valor           |
| ----- | --------------- |
| Tipo  | Numérica        |
| Uso   | Growth analysis |

### Descripción

Cambio absoluto anual en valor de mercado.

---

## delta_log_market_value_1y

| Campo | Valor              |
| ----- | ------------------ |
| Tipo  | Numérica           |
| Uso   | Evolución relativa |

### Descripción

Variación logarítmica anual del valor de mercado.

---

## market_value_prev_eur

| Campo | Valor     |
| ----- | --------- |
| Tipo  | Numérica  |
| Uso   | Histórico |

---

## market_value_next_eur

| Campo | Valor                   |
| ----- | ----------------------- |
| Tipo  | Numérica                |
| Uso   | Evaluación longitudinal |

---

# 🔗 Variables de matching

## matching_status

| Campo | Valor                |
| ----- | -------------------- |
| Tipo  | Boolean / categórica |
| Uso   | Auditoría            |

---

## matching_method

| Campo | Valor            |
| ----- | ---------------- |
| Tipo  | Categórica       |
| Uso   | Calidad matching |

### Valores

* exact_age_validated
* exact_age_club_validated
* fuzzy_age_club_validated

---

## matching_confidence

| Campo | Valor           |
| ----- | --------------- |
| Tipo  | Numérica        |
| Rango | 0–1             |
| Uso   | Control calidad |

---

## age_diff

| Campo | Valor               |
| ----- | ------------------- |
| Tipo  | Numérica            |
| Uso   | Validación matching |

---

## club_score

| Campo | Valor            |
| ----- | ---------------- |
| Tipo  | Numérica         |
| Uso   | Similaridad club |

---

# 📊 Variables de modelización

## target_variable

| Campo        | Valor                  |
| ------------ | ---------------------- |
| Valor actual | `log_market_value_eur` |

---

## modeling_split

| Campo | Valor    |
| ----- | -------- |
| Tipo  | Temporal |

### Configuración actual

| Split | Temporadas            |
| ----- | --------------------- |
| Train | 2019-2020 → 2023-2024 |
| Test  | 2024-2025             |

---

## fixed_effects

| Campo | Valor            |
| ----- | ---------------- |
| Tipo  | Lista categórica |

### Variables

* league
* season
* position_group

---

# 💡 Variables de scoring

## predicted_market_value_eur

| Campo | Valor                |
| ----- | -------------------- |
| Tipo  | Numérica             |
| Uso   | Predicción principal |

---

## predicted_log_market_value

| Campo | Valor                 |
| ----- | --------------------- |
| Tipo  | Numérica              |
| Uso   | Predicción modelizada |

---

## market_value_gap_eur

| Campo | Valor                |
| ----- | -------------------- |
| Tipo  | Numérica             |
| Uso   | Diferencial absoluto |

---

## market_value_gap_pct

| Campo  | Valor      |
| ------ | ---------- |
| Tipo   | Numérica   |
| Unidad | Porcentaje |

---

## inefficiency_score

| Campo | Valor            |
| ----- | ---------------- |
| Tipo  | Numérica         |
| Uso   | Ranking scouting |

### Fórmula conceptual

```python
inefficiency_score =
valor_estimado - valor_observado
```

---

## confidence_score

| Campo | Valor         |
| ----- | ------------- |
| Tipo  | Numérica      |
| Uso   | Calidad señal |

### Componentes previstos

* matching confidence
* estabilidad temporal
* completitud de features
* volumen de juego

---

## opportunity_score

| Campo  | Valor    |
| ------ | -------- |
| Tipo   | Numérica |
| Estado | Previsto |

### Fórmula conceptual prevista

```python
Opportunity Score =
inefficiency_score +
growth_score +
confidence_score
```

---

# 🧪 Variables experimentales y tracking

## experiment_id

| Campo | Valor           |
| ----- | --------------- |
| Tipo  | String          |
| Uso   | Tracking MLflow |

---

## run_id

| Campo | Valor                |
| ----- | -------------------- |
| Tipo  | String               |
| Uso   | Identificador MLflow |

---

## model_name

| Campo | Valor               |
| ----- | ------------------- |
| Tipo  | String              |
| Uso   | Comparación modelos |

---

## model_version

| Campo | Valor        |
| ----- | ------------ |
| Tipo  | String       |
| Uso   | Trazabilidad |

---

## training_timestamp

| Campo | Valor                  |
| ----- | ---------------------- |
| Tipo  | Datetime               |
| Uso   | Auditoría experimental |

---

## experiment_metrics

| Campo | Valor             |
| ----- | ----------------- |
| Tipo  | JSON / estructura |
| Uso   | Tracking          |

### Métricas registradas

* RMSE
* MAE
* R²

---

# ⚙️ Variables de configuración

## MIN_AGE

| Campo | Valor          |
| ----- | -------------- |
| Tipo  | Numérica       |
| Uso   | Filtro dataset |

---

## MAX_AGE

| Campo | Valor          |
| ----- | -------------- |
| Tipo  | Numérica       |
| Uso   | Filtro dataset |

---

## MIN_MINUTES

| Campo | Valor          |
| ----- | -------------- |
| Tipo  | Numérica       |
| Uso   | Filtro dataset |

---

## MAX_AGE_DIFF

| Campo | Valor    |
| ----- | -------- |
| Tipo  | Numérica |
| Uso   | Matching |

---

## MIN_CLUB_SCORE

| Campo | Valor    |
| ----- | -------- |
| Tipo  | Numérica |
| Uso   | Matching |

---

## FUZZY_THRESHOLD

| Campo | Valor    |
| ----- | -------- |
| Tipo  | Numérica |
| Uso   | Matching |

---

# 📤 Outputs generados

## Reports

| Output       | Ruta                         |
| ------------ | ---------------------------- |
| Rankings     | `reports/rankings/`          |
| Métricas     | `reports/tables/`            |
| Diagnósticos | `reports/model_diagnostics/` |

---

## Artifacts

| Output             | Ruta                            |
| ------------------ | ------------------------------- |
| Modelos            | `artifacts/models/`             |
| Predicciones       | `artifacts/predictions/`        |
| Feature importance | `artifacts/feature_importance/` |

---

## MLflow

| Output              | Ruta      |
| ------------------- | --------- |
| Runs experimentales | `mlruns/` |
| Parámetros          | `mlruns/` |
| Métricas            | `mlruns/` |
| Artefactos          | `mlruns/` |

---

# 🛡️ Variables excluidas por leakage

Las siguientes variables no pueden utilizarse como inputs predictivos:

| Variable                   | Razón              |
| -------------------------- | ------------------ |
| market_value_next_eur      | Información futura |
| delta_log_market_value_1y  | Leakage temporal   |
| predicted_market_value_eur | Output derivado    |
| inefficiency_score         | Output derivado    |
| rankings                   | Output derivado    |

---

# 📉 Limitaciones actuales

## Feature engineering

Todavía faltan variables relevantes como:

* z-scores posicionales
* percentiles
* progression metrics
* rolling metrics
* métricas avanzadas defensivas

---

## Cobertura contextual

Pendiente integrar:

* xG
* xA
* métricas Understat
* eventos StatsBomb

---

## Dataset size

El tamaño actual del dataset limita parcialmente:

* modelos muy complejos
* modelización altamente segmentada
* deep learning

---

# 🚀 Variables previstas futuras

## Progression metrics

Variables previstas:

* delta_minutes_yoy
* delta_goals_per90_yoy
* delta_assists_per90_yoy

---

## Positional normalization

Variables previstas:

* goals_per90_pos_z
* assists_per90_pos_z
* progression_index_pos_z

---

## Explainability

Variables previstas:

* shap_global_importance
* shap_player_contribution

---

## Stability metrics

Variables previstas:

* ranking_stability_score
* temporal_consistency_score

---

# 🧠 Conclusión

El diccionario de datos refleja una arquitectura orientada a:

* reproducibilidad
* interpretabilidad
* trazabilidad
* analytics engineering
* scouting cuantitativo

Actualmente el sistema ya integra:

* variables deportivas
* variables contextuales
* variables de matching
* variables derivadas
* variables de scoring
* tracking experimental
* configuración centralizada

La evolución futura del sistema dependerá principalmente de enriquecer el feature set con variables más avanzadas y señales longitudinales que incrementen la capacidad predictiva del modelo.
