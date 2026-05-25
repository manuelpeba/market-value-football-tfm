# 🧪 Plan de Feature Engineering

<div align="center">

![Feature Engineering](https://img.shields.io/badge/Feature%20Engineering-Advanced-blue)
![Sports Analytics](https://img.shields.io/badge/Sports%20Analytics-Football-success)
![Modeling](https://img.shields.io/badge/Modeling-Econometrics%20%2B%20ML-orange)
![Scoring](https://img.shields.io/badge/Scoring-Engine-success)
![Tracking](https://img.shields.io/badge/Tracking-MLflow-success)

</div>

---

# 📑 Tabla de contenidos

- Objetivo
- Filosofía
- Estado actual
- Features actuales
- Features derivadas
- Variables para scoring
- Growth features
- Composite indices
- Feature tracking
- Prevención de leakage
- Trade-offs
- Roadmap

---

# 🧠 Objetivo

Este documento describe la estrategia de feature engineering implementada y futura.

Objetivos:

- aumentar señal predictiva
- mantener interpretabilidad
- garantizar validez temporal
- soportar scouting cuantitativo

---

# ⚙️ Filosofía

Principio central:

```text
incrementar señal
sin aumentar complejidad innecesaria
```

Decisión:

Priorizar:

- robustez
- interpretabilidad
- coherencia futbolística
- reproducibilidad

---

# 📊 Estado actual

El sistema dispone actualmente de:

- features ofensivas
- contexto competitivo
- volumen de juego
- variables temporales
- variables longitudinales
- índices compuestos
- variables derivadas para scoring

Resultado observado:

```text
el principal cuello de botella ya no es el modelo,
sino la riqueza del signal disponible
```

---

# ⚽ Features actuales

## Producción ofensiva

- goals_per90
- assists_per90
- shots_per90
- g_a_per90

## Volumen

- minutes_played
- log_minutes_played
- starts
- nineties

## Contexto

- age
- league
- season
- position_group

## Defensivas

- tackles_per90
- interceptions_per90
- blocks_per90

---

# 📈 Features derivadas

Transformaciones:

| Variable | Tipo |
|---|---|
| log_market_value_eur | target transform |
| log_minutes_played | log transform |
| age_squared | nonlinear age |
| career_year | trayectoria |
| breakout_indicator | explosión temprana |

---

# 🚀 Growth Features

Variables implementadas:

| Variable | Objetivo |
|---|---|
| market_value_growth_prev | crecimiento histórico |
| delta_log_market_value_prev | evolución relativa |
| breakout_indicator | detección temprana |
| growth_index | potencial |
| career_year | experiencia |

Resultados observados:

| Modelo | R² |
|---|---:|
| Baseline OLS |0.4160|
| Growth OLS |0.5255|

Interpretación:

Las variables temporales aportan señal significativa.

---

# 🧩 Composite Football Indices

Índices implementados:

- finishing_index
- playmaking_index
- growth_index
- experience_index

Uso actual:

- scouting
- explainability
- rankings
- reporting

No utilizados en:

```text
modelo predictivo final
```

debido a redundancia informativa.

---

# 🎯 Variables derivadas para scoring (Sprint 5)

Las siguientes variables se incorporan exclusivamente para la capa de scouting.

## Inefficiency variables

- predicted_market_value_eur
- market_value_gap_eur
- market_value_gap_pct
- inefficiency_score
- inefficiency_score_z

---

## Growth variables

- growth_score
- growth_score_z

---

## Confidence variables

- confidence_score
- confidence_score_z

Componentes:

- matching_confidence
- minutes_reliability
- feature_completeness
- temporal_stability

---

## Opportunity variables

- opportunity_score
- opportunity_rank
- opportunity_tier

---

# 🔄 Feature tracking

MLflow registra:

- feature set
- transformaciones
- grupos de variables
- métricas
- feature importance

---

# 🛡️ Prevención de leakage

Variables excluidas:

- market_value_next_eur
- future_minutes
- predicted_market_value_eur
- opportunity_score
- rankings

Principio:

```text
toda feature debe existir
en el momento real de decisión
```

---

# ⚖️ Trade-offs

| Trade-off | Decisión |
|---|---|
| muchas features vs interpretabilidad | equilibrio |
| complejidad vs estabilidad | modularización |
| precisión vs explicabilidad | arquitectura híbrida |

---

# 🚀 Roadmap

Alta prioridad:

- xG
- xA
- métricas defensivas avanzadas
- rolling metrics
- progression metrics

Media prioridad:

- eventos StatsBomb
- métricas tácticas
- context features

Futuro:

- embeddings
- modelos específicos por posición

---

# 🧠 Conclusión

El feature engineering representa actualmente el mayor potencial de mejora del sistema.

Sprint 5 añade una nueva capa de variables derivadas que transforma señales predictivas en señales accionables de scouting:

```text
predicción
↓
scoring
↓
rankings
↓
decisión
```
