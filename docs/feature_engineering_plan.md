# 🧪 Plan de Feature Engineering

<div align="center">

![Feature Engineering](https://img.shields.io/badge/Feature%20Engineering-Advanced-blue)
![Sports Analytics](https://img.shields.io/badge/Sports%20Analytics-Football-success)
![Modeling](https://img.shields.io/badge/Modeling-Econometrics%20%2B%20ML-orange)
![Scoring](https://img.shields.io/badge/Scoring-Engine-success)
![Evaluation](https://img.shields.io/badge/Evaluation-Business%20Validation-purple)
![Tracking](https://img.shields.io/badge/Tracking-MLflow-success)

</div>

---

# 📑 Tabla de contenidos

- [🧠 Objetivo](#-objetivo)
- [⚙️ Filosofía](#️-filosofía)
- [📊 Estado actual](#-estado-actual)
- [⚽ Features actuales](#-features-actuales)
- [📈 Features derivadas](#-features-derivadas)
- [🚀 Growth features](#-growth-features)
- [🧩 Composite football indices](#-composite-football-indices)
- [🎯 Variables derivadas para scoring — Sprint 5](#-variables-derivadas-para-scoring--sprint-5)
- [📊 Variables de evaluación y negocio — Sprint 6](#-variables-de-evaluación-y-negocio--sprint-6)
- [🔄 Feature tracking](#-feature-tracking)
- [🛡️ Prevención de leakage](#️-prevención-de-leakage)
- [⚖️ Trade-offs](#️-trade-offs)
- [🚀 Roadmap](#-roadmap)
- [🧠 Conclusión](#-conclusión)

---

# 🧠 Objetivo

Este documento describe la estrategia de feature engineering implementada y futura dentro del sistema analítico de identificación de jugadores infravalorados en el mercado de fichajes europeo.

El objetivo no es únicamente aumentar el rendimiento predictivo de los modelos, sino construir una capa de variables coherente con el dominio futbolístico, trazable metodológicamente y útil para la toma de decisiones de scouting.

Objetivos principales:

- aumentar señal predictiva
- mantener interpretabilidad
- garantizar validez temporal
- evitar leakage
- soportar scoring cuantitativo
- facilitar rankings accionables
- conectar predicción, evaluación y negocio

---

# ⚙️ Filosofía

Principio central:

```text
incrementar señal
sin aumentar complejidad innecesaria
```

Decisión metodológica:

Priorizar:

- robustez
- interpretabilidad
- coherencia futbolística
- reproducibilidad
- trazabilidad experimental
- utilidad real para scouting

El feature engineering se concibe como una capa de traducción entre el rendimiento deportivo observado y la señal económica que el modelo intenta capturar.

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
- variables de ranking
- métricas de validación de negocio
- outputs de simulación ROI

Resultado observado:

```text
el principal cuello de botella ya no es el modelo,
sino la riqueza y estabilidad del signal disponible
```

La evolución del proyecto ha demostrado que modelos más complejos solo aportan valor cuando las variables incorporan información diferencial sobre rendimiento, trayectoria, contexto y potencial futuro.

---

# ⚽ Features actuales

## Producción ofensiva

- `goals_per90`
- `assists_per90`
- `shots_per90`
- `g_a_per90`

## Volumen competitivo

- `minutes_played`
- `log_minutes_played`
- `starts`
- `nineties`

## Contexto

- `age`
- `league`
- `season`
- `position_group`

## Defensivas

- `tackles_per90`
- `interceptions_per90`
- `blocks_per90`

## Calidad y matching

- `matching_confidence`
- `matching_method`
- `club_score`
- `age_diff`

Estas variables no representan rendimiento deportivo puro, pero son relevantes para evaluar la fiabilidad de las observaciones y alimentar la capa de `confidence_score`.

---

# 📈 Features derivadas

Transformaciones principales:

| Variable | Tipo | Uso |
|---|---|---|
| `log_market_value_eur` | target transform | modelización |
| `log_minutes_played` | log transform | modelización |
| `age_squared` | nonlinear age | trayectoria |
| `career_year` | experiencia | growth |
| `breakout_indicator` | explosión temprana | growth/scouting |

## Justificación

El valor de mercado presenta una distribución altamente asimétrica, por lo que la transformación logarítmica permite estabilizar la varianza, reducir el impacto de outliers y mejorar la interpretación relativa de los errores.

La edad y la trayectoria se modelan de forma no lineal porque el mercado no valora igual un rendimiento elevado a los 18 años que a los 23. En jugadores jóvenes, la edad contiene información sobre potencial, madurez competitiva y margen de revalorización.

---

# 🚀 Growth Features

Variables implementadas:

| Variable | Objetivo |
|---|---|
| `market_value_growth_prev` | crecimiento histórico |
| `delta_log_market_value_prev` | evolución relativa |
| `breakout_indicator` | detección temprana |
| `growth_index` | potencial |
| `career_year` | experiencia |

Resultados observados:

| Modelo | R² |
|---|---:|
| Baseline OLS | 0.4160 |
| Growth OLS | 0.5255 |

Interpretación:

Las variables temporales aportan señal significativa porque el mercado de fichajes no descuenta únicamente rendimiento presente, sino también expectativas de evolución futura.

La mejora del modelo Growth OLS frente al baseline confirma que el valor de mercado incorpora dinámicas longitudinales y señales de progresión profesional.

---

# 🧩 Composite Football Indices

Índices implementados:

- `finishing_index`
- `playmaking_index`
- `growth_index`
- `experience_index`

Uso actual:

- scouting
- explainability
- rankings
- reporting
- análisis descriptivo

No utilizados en:

```text
modelo predictivo final
```

debido a redundancia informativa con variables base y de crecimiento.

## Decisión metodológica

Aunque los índices compuestos no mejoraron el rendimiento predictivo, se mantienen como variables de interpretación. En un contexto de scouting, estos índices permiten explicar perfiles de jugador de forma más intuitiva que una lista extensa de variables individuales.

Su valor principal está en la traducción del output técnico a lenguaje de negocio deportivo.

---

# 🎯 Variables derivadas para scoring — Sprint 5

Sprint 5 incorpora una capa de variables derivadas exclusivamente orientada a scouting.

Estas variables no se utilizan como inputs del modelo predictivo base, sino como outputs construidos a partir de predicciones, valor observado, trayectoria y fiabilidad.

## Inefficiency variables

| Variable | Descripción |
|---|---|
| `predicted_market_value_eur` | valor estimado por el modelo |
| `market_value_gap_eur` | diferencia entre valor estimado y observado |
| `market_value_gap_pct` | gap porcentual relativo |
| `inefficiency_score` | señal de infravaloración |
| `inefficiency_score_z` | señal normalizada |

Interpretación:

```text
inefficiency_score > 0  → posible jugador infravalorado
inefficiency_score < 0  → posible jugador sobrevalorado
```

## Growth variables

| Variable | Descripción |
|---|---|
| `growth_score` | potencial de crecimiento |
| `growth_score_z` | potencial normalizado |

## Confidence variables

| Variable | Descripción |
|---|---|
| `confidence_score` | fiabilidad global de la recomendación |
| `confidence_score_z` | fiabilidad normalizada |

Componentes:

- `matching_confidence`
- `minutes_reliability`
- `feature_completeness`
- `temporal_stability`

## Opportunity variables

| Variable | Descripción |
|---|---|
| `opportunity_score` | score multicriterio final |
| `opportunity_rank` | ranking global |
| `opportunity_tier` | nivel de prioridad |

Fórmula conceptual:

```python
opportunity_score = (
    0.55 * inefficiency_score_z
    + 0.25 * growth_score_z
    + 0.20 * confidence_score_z
)
```

## Rol dentro del sistema

Sprint 5 transforma el sistema desde una lógica puramente predictiva hacia una lógica de decisión:

```text
predicción
↓
inefficiency score
↓
growth score
↓
confidence score
↓
opportunity score
↓
rankings
```

---

# 📊 Variables de evaluación y negocio — Sprint 6

Sprint 6 incorpora una capa de validación posterior al scoring. Esta fase no crea features predictivas para el modelo base, sino variables y métricas derivadas para evaluar si los rankings generados tienen utilidad real desde una perspectiva de scouting y negocio.

## Objetivo del Sprint 6

Validar si el sistema de scoring produce rankings útiles, estables y económicamente interpretables.

La pregunta deja de ser únicamente:

```text
¿predice bien el valor de mercado?
```

y pasa a ser:

```text
¿ordena correctamente jugadores con potencial de oportunidad?
```

---

## Ranking diagnostics

Variables y outputs generados:

| Output | Objetivo |
|---|---|
| `ranking_summary.csv` | resumen global de rankings |
| `ranking_by_league.csv` | diagnóstico por liga |
| `ranking_by_position.csv` | diagnóstico por posición |
| `ranking_score_correlations.csv` | correlaciones entre scores |
| `ranking_tier_summary.csv` | distribución por niveles de prioridad |

Uso metodológico:

- detectar sesgos por liga
- detectar sesgos por posición
- validar coherencia interna del Opportunity Score
- comprobar concentración excesiva de rankings
- auditar estabilidad de señales

---

## Precision@K

Variables de evaluación:

| Variable | Descripción |
|---|---|
| `k` | tamaño del top ranking evaluado |
| `players` | número de jugadores considerados |
| `true_positive` | jugadores con señal positiva posterior |
| `precision_at_k` | proporción de aciertos en el top K |

Resultados actuales:

| K | Precision@K |
|---:|---:|
| 10 | 0.90 |
| 20 | 0.90 |
| 50 | 0.90 |
| 100 | 0.85 |

Interpretación:

El sistema mantiene una precisión elevada en los primeros tramos del ranking. Esto sugiere que el Opportunity Score concentra perfiles con evolución positiva y no se limita a ordenar ruido estadístico.

Advertencia metodológica:

Precision@K debe interpretarse como validación preliminar de ranking. No implica causalidad ni garantiza rentabilidad real, ya que depende de proxies longitudinales disponibles en el dataset.

---

## ROI simulation

Variables derivadas:

| Variable | Descripción |
|---|---|
| `expected_profit_eur` | beneficio esperado estimado |
| `expected_roi_pct` | retorno esperado porcentual |
| `risk_adjusted_profit_eur` | beneficio ajustado por riesgo |
| `risk_adjusted_roi_pct` | ROI ajustado por riesgo |
| `positive_roi_rate` | proporción de operaciones potencialmente positivas |

Hipótesis conservadora adoptada:

```python
realization_factor = 0.5

assumed_sell_price_eur = (
    market_value_eur
    + (predicted_market_value_eur - market_value_eur) * realization_factor
)
```

Justificación:

El valor estimado por el modelo no debe interpretarse como precio garantizado de venta. El mercado real incorpora costes de transacción, incertidumbre contractual, riesgo deportivo, negociación, liquidez limitada y variabilidad temporal.

Por ello, Sprint 6 aplica una hipótesis conservadora en la que solo una parte del upside estimado se materializa.

---

## Business features derivadas

Estas variables no se incorporan al entrenamiento, pero sí al análisis de negocio:

- `expected_profit_eur`
- `expected_roi_pct`
- `risk_adjusted_profit_eur`
- `risk_adjusted_roi_pct`
- `positive_roi_rate`
- `transfer_strategy_segment`
- `ranking_tier`
- `is_top_k`
- `is_scouting_shortlist`

## Decisión metodológica

Las variables de Sprint 6 pertenecen a la capa de evaluación y puesta en valor, no al dataset de entrenamiento.

Esto preserva la separación entre:

| Capa | Función |
|---|---|
| Features predictivas | estimar valor esperado |
| Scores | transformar predicción en señal de scouting |
| Ranking diagnostics | validar ordenación |
| Business metrics | evaluar utilidad económica potencial |

---

# 🔄 Feature tracking

MLflow registra:

- feature set
- transformaciones
- grupos de variables
- métricas predictivas
- feature importance
- parámetros de scoring
- outputs de evaluación
- artefactos de ranking

Sprint 6 amplía la trazabilidad del sistema porque permite registrar no solo métricas de modelo, sino también métricas de utilidad de ranking y negocio.

Esto resulta clave para justificar decisiones ante un tribunal o ante un stakeholder deportivo: el sistema no se evalúa únicamente por RMSE, sino por su capacidad para priorizar oportunidades.

---

# 🛡️ Prevención de leakage

Variables excluidas del entrenamiento predictivo:

- `market_value_next_eur`
- `future_minutes`
- `predicted_market_value_eur`
- `market_value_gap_eur`
- `market_value_gap_pct`
- `inefficiency_score`
- `growth_score`
- `confidence_score`
- `opportunity_score`
- `opportunity_rank`
- `ranking_tier`
- `expected_profit_eur`
- `expected_roi_pct`
- `positive_roi_rate`
- rankings

Principio:

```text
toda feature predictiva debe existir
en el momento real de decisión
```

## Separación crítica

Las variables de Sprint 5 y Sprint 6 son outputs derivados, no inputs de entrenamiento.

Esto evita que el modelo aprenda información generada por sí mismo o información posterior al momento de decisión.

---

# ⚖️ Trade-offs

| Trade-off | Decisión |
|---|---|
| muchas features vs interpretabilidad | equilibrio |
| complejidad vs estabilidad | modularización |
| precisión vs explicabilidad | arquitectura híbrida |
| señal deportiva vs ruido muestral | filtros y confidence score |
| ranking agresivo vs recomendación fiable | Opportunity Score multicriterio |
| ROI optimista vs prudencia de negocio | realization factor conservador |
| métricas técnicas vs utilidad real | añadir Precision@K y ROI simulation |

---

# 🚀 Roadmap

## Alta prioridad

- xG
- xA
- métricas defensivas avanzadas
- rolling metrics
- progression metrics
- estabilidad temporal de rankings
- robustness checks por liga y posición

## Media prioridad

- eventos StatsBomb
- métricas tácticas
- context features
- league strength adjustment
- team strength adjustment
- age curves por posición

## Futuro

- embeddings
- modelos específicos por posición
- similar players engine
- scouting reports automáticos
- dashboard Streamlit
- API de scoring
- retraining continuo

---

# 🧠 Conclusión

El feature engineering representa actualmente el mayor potencial de mejora del sistema.

Los sprints anteriores demostraron que:

- la normalización contextual por posición y liga no mejoró el rendimiento predictivo de forma directa
- las variables temporales y de crecimiento sí aportaron señal relevante
- los índices compuestos aportan valor interpretativo aunque no mejoren métricas
- el scoring multicriterio permite transformar predicciones en rankings accionables

Sprint 5 añadió una nueva capa de variables derivadas que convierte señales predictivas en señales de scouting:

```text
predicción
↓
scoring
↓
rankings
↓
decisión
```

Sprint 6 completa esta evolución incorporando validación de ranking y evaluación de negocio:

```text
rankings
↓
Precision@K
↓
ROI simulation
↓
validación de negocio
```

La arquitectura resultante ya no se limita a estimar valores de mercado, sino que construye un sistema analítico completo para priorizar oportunidades, evaluar su fiabilidad y traducirlas a una lógica de decisión propia de un departamento de Football Analytics profesional.
