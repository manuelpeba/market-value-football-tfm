# Data Dictionary

## Dataset principal: `player_season_modeling.parquet`

Unidad de análisis:

```text
Jugador–temporada
```

El dataset final de modelización integra información de mercado procedente de Transfermarkt con métricas de rendimiento deportivo procedentes de FBref.

Su objetivo es servir como tablón analítico para estimar el valor de mercado esperado de los jugadores y construir scores de ineficiencia de mercado.

---

## 1. Identificación del registro

| Variable | Tipo esperado | Descripción | Fuente | Uso |
|---|---:|---|---|---|
| `player_id` | string / int | Identificador interno del jugador cuando está disponible | Transfermarkt / interna | Identificación |
| `player_name` | string | Nombre del jugador | FBref / Transfermarkt | Identificación y reporting |
| `player_name_norm` | string | Nombre normalizado para matching | Interna | Matching |
| `season` | string | Temporada deportiva, por ejemplo `2022-2023` | FBref / Transfermarkt | Panel temporal |
| `league` | string | Competición o liga | FBref | Fixed effect / segmentación |
| `club` | string | Club del jugador en la temporada | FBref / Transfermarkt | Matching / contexto |
| `club_norm` | string | Club normalizado para matching | Interna | Matching |

---

## 2. Variables demográficas y contextuales

| Variable | Tipo esperado | Descripción | Fuente | Uso |
|---|---:|---|---|---|
| `age` | float | Edad del jugador en la temporada | Transfermarkt / FBref | Variable explicativa |
| `position` | string | Posición específica original | FBref / Transfermarkt | Contexto deportivo |
| `position_group` | category | Grupo posicional: `GK`, `DEF`, `MID`, `ATT` | Interna | Fixed effect / segmentación |
| `nationality` | string | Nacionalidad principal del jugador | Transfermarkt | Contexto / futura extensión |

---

## 3. Variables de mercado

| Variable | Tipo esperado | Descripción | Fuente | Uso |
|---|---:|---|---|---|
| `market_value_eur` | float | Valor de mercado observado en euros | Transfermarkt | Target original |
| `log_market_value_eur` | float | Logaritmo natural del valor de mercado | Derivada | Target econométrico |
| `market_value_prev_eur` | float | Valor de mercado observado en temporada anterior | Derivada | Growth model futuro |
| `market_value_next_eur` | float | Valor de mercado observado en temporada posterior | Derivada | Growth model futuro |
| `market_value_growth_1y` | float | Crecimiento porcentual del valor de mercado a un año | Derivada | Growth Score futuro |
| `delta_log_market_value_1y` | float | Diferencia logarítmica del valor de mercado a un año | Derivada | Growth model futuro |

### Nota metodológica

`market_value_eur` representa una estimación pública de valor de mercado, no necesariamente un precio real de transferencia. Por ello, el modelo estima discrepancias relativas al mercado observado, no plusvalías garantizadas.

---

## 4. Variables de rendimiento deportivo

| Variable | Tipo esperado | Descripción | Fuente | Uso |
|---|---:|---|---|---|
| `minutes_played` | float / int | Minutos jugados en la temporada | FBref | Variable explicativa principal |
| `goals_per90` | float | Goles por 90 minutos | FBref | Producción ofensiva |
| `assists_per90` | float | Asistencias por 90 minutos | FBref | Producción ofensiva / creación |
| `shots_per90` | float | Tiros por 90 minutos | FBref | Finalización |
| `progressive_passes_per90` | float | Pases progresivos por 90 minutos | FBref | Progresión |
| `progressive_carries_per90` | float | Conducciones progresivas por 90 minutos | FBref | Progresión |
| `tackles_per90` | float | Entradas por 90 minutos | FBref | Rendimiento defensivo |
| `interceptions_per90` | float | Intercepciones por 90 minutos | FBref | Rendimiento defensivo |
| `xg_per90` | float | Expected Goals por 90 minutos | Understat / FBref | Extensión futura |
| `xa_per90` | float | Expected Assists por 90 minutos | Understat / FBref | Extensión futura |

---

## 5. Variables normalizadas e índices derivados

Estas variables se construyen para mejorar la comparabilidad entre jugadores de distintas posiciones y ligas.

### 5.1 Z-scores contextuales

| Variable | Tipo esperado | Descripción | Fuente | Uso |
|---|---:|---|---|---|
| `z_goals_per90` | float | Z-score de goles por 90 dentro de grupo contextual | Derivada | Feature engineering |
| `z_assists_per90` | float | Z-score de asistencias por 90 | Derivada | Feature engineering |
| `z_shots_per90` | float | Z-score de tiros por 90 | Derivada | Feature engineering |
| `z_progressive_passes_per90` | float | Z-score de pases progresivos | Derivada | Feature engineering |
| `z_progressive_carries_per90` | float | Z-score de conducciones progresivas | Derivada | Feature engineering |
| `z_tackles_per90` | float | Z-score de entradas | Derivada | Feature engineering |
| `z_interceptions_per90` | float | Z-score de intercepciones | Derivada | Feature engineering |

Agrupación usada:

```text
position_group + league
```

---

### 5.2 Índices deportivos

| Variable | Tipo esperado | Descripción | Fuente | Uso |
|---|---:|---|---|---|
| `finishing_index` | float | Índice agregado de finalización | Derivada | Feature engineering |
| `playmaking_index` | float | Índice agregado de creación | Derivada | Feature engineering |
| `progression_index` | float | Índice agregado de progresión | Derivada | Feature engineering |
| `defensive_index` | float | Índice agregado defensivo | Derivada | Feature engineering |

Construcción conceptual:

```text
finishing_index   = mean(z_goals_per90, z_shots_per90)
playmaking_index  = mean(z_assists_per90, z_progressive_passes_per90)
progression_index = mean(z_progressive_passes_per90, z_progressive_carries_per90)
defensive_index   = mean(z_tackles_per90, z_interceptions_per90)
```

---

## 6. Variables de control de minutos

| Variable | Tipo esperado | Descripción | Fuente | Uso |
|---|---:|---|---|---|
| `minutes_bucket` | category | Segmento de minutos: `low`, `medium`, `high`, `very_high` | Derivada | Control / segmentación |
| `is_low_minutes` | bool | Indicador de jugador con menos de 900 minutos | Derivada | Control de fiabilidad |

---

## 7. Variables de matching y calidad

| Variable | Tipo esperado | Descripción | Fuente | Uso |
|---|---:|---|---|---|
| `matching_method` | string | Método de matching utilizado | Interna | Trazabilidad |
| `matching_confidence` | float | Confianza del matching | Interna | Confidence Score |
| `age_diff` | float | Diferencia absoluta de edad entre fuentes | Interna | Validación del matching |
| `club_score` | float | Similitud entre nombres de club | Interna | Validación del matching |
| `matching_status` | string | Estado del matching cuando está disponible | Interna | Calidad |

Valores principales de `matching_method`:

```text
exact_age_club_validated
fuzzy_age_club_validated
```

Resultados actuales del panel:

```text
exact_age_club_validated: 6,107
fuzzy_age_club_validated: 74
unmatched / NaN: 5,599
```

---

## 8. Variables del modelo econométrico

Variables utilizadas actualmente en `03_econometric_model.ipynb`.

### 8.1 Target

| Variable | Tipo esperado | Descripción |
|---|---:|---|
| `log_market_value_eur` | float | Variable dependiente del modelo OLS |

### 8.2 Variables explicativas base

| Variable | Tipo esperado | Descripción |
|---|---:|---|
| `minutes_played` | float | Exposición competitiva |
| `goals_per90` | float | Producción goleadora |
| `assists_per90` | float | Producción creativa |
| `age` | float | Edad del jugador |

### 8.3 Fixed Effects

Variables categóricas codificadas mediante dummies:

| Variable original | Descripción |
|---|---|
| `league` | Efectos fijos de liga |
| `season` | Efectos fijos de temporada |
| `position_group` | Efectos fijos de posición |

Ejemplos de columnas dummy generadas:

```text
league_Eredivisie
league_LaLiga
league_Liga Portugal
league_Ligue 1
league_Premier League
league_Serie A
season_2021-2022
season_2022-2023
season_2023-2024
position_group_DEF
position_group_GK
position_group_MID
```

---

## 9. Variables de predicción y scoring

Generadas en el notebook `03_econometric_model.ipynb`.

| Variable | Tipo esperado | Descripción | Interpretación |
|---|---:|---|---|
| `predicted_log_market_value` | float | Valor de mercado estimado en escala logarítmica | Predicción del modelo |
| `predicted_market_value_eur` | float | Valor de mercado estimado en euros | `exp(predicted_log_market_value)` |
| `residual_observed_minus_predicted` | float | Residuo econométrico clásico | Observado - predicho |
| `inefficiency_score` | float | Score de infravaloración | Predicho - observado |
| `inefficiency_score_z` | float | Inefficiency Score estandarizado | Comparabilidad |
| `market_value_gap_eur` | float | Diferencia monetaria entre valor esperado y observado | Positivo = posible oportunidad |
| `market_value_gap_pct` | float | Gap relativo respecto al valor observado | Positivo = posible oportunidad |
| `confidence_score` | float | Fiabilidad de la estimación según matching | 0-1 aproximadamente |
| `opportunity_score` | float | Score final inicial de oportunidad | Inefficiency ajustado por confianza |

---

## 10. Definiciones críticas de scoring

### Residuo econométrico

```text
residual_observed_minus_predicted = observed_log_market_value - predicted_log_market_value
```

### Inefficiency Score

```text
inefficiency_score = predicted_log_market_value - observed_log_market_value
```

Interpretación:

```text
inefficiency_score > 0 → valor esperado superior al observado → potencial infravaloración
inefficiency_score < 0 → valor observado superior al esperado → potencial sobrevaloración
```

### Market Value Gap

```text
market_value_gap_eur = predicted_market_value_eur - market_value_eur
market_value_gap_pct = market_value_gap_eur / market_value_eur
```

Interpretación:

```text
market_value_gap_eur > 0 → potencial oportunidad de mercado
market_value_gap_eur < 0 → potencial sobrevaloración
```

---

## 11. Outputs analíticos esperados

Los outputs se almacenan o se prevé almacenarlos en:

```text
data/outputs/
```

Tablas principales:

| Output | Descripción |
|---|---|
| `model_metrics` | Métricas MAE, RMSE, R² y R² ajustado |
| `coefficient_table` | Coeficientes OLS con errores robustos HC3 |
| `vif_table` | Diagnóstico de multicolinealidad |
| `undervalued_ranking` | Ranking de jugadores potencialmente infravalorados |
| `overvalued_ranking` | Ranking de jugadores potencialmente sobrevalorados |
| `league_summary` | Resumen de scores por liga |
| `position_summary` | Resumen de scores por posición |

---

## 12. Métricas actuales del modelo OLS

Resultados del notebook `03_econometric_model.ipynb`:

| Métrica | Valor |
|---|---:|
| `MAE_log` | 0.6363 |
| `RMSE_log` | 0.7964 |
| `R2` | 0.6481 |
| `Adj_R2` | 0.6424 |
| `N_obs` | 1,012 |
| `N_features` | 17 |

---

## 13. Observaciones metodológicas

- El target se modeliza en escala logarítmica para reducir asimetría y mejorar la interpretación porcentual de coeficientes.
- El modelo econométrico actual prioriza interpretabilidad sobre máxima capacidad predictiva.
- Las variables de scoring no deben interpretarse como recomendaciones automáticas de fichaje.
- Los rankings son herramientas de priorización para revisión posterior por scouting experto.
- Los residuos pueden reflejar ineficiencias, pero también variables omitidas como contrato, salario, lesiones, reputación, agente o potencial percibido.

---

## 14. Próximas variables a incorporar

### Rendimiento avanzado

- `xg_per90`
- `xa_per90`
- `shot_creating_actions_per90`
- `key_passes_per90`
- `touches_attacking_third_per90`
- `touches_box_per90`

### Contexto de club y liga

- fuerza relativa de la liga
- nivel económico del club
- clasificación del equipo
- competición europea

### Mercado y contrato

- duración contractual
- historial de transferencias
- nacionalidad
- internacionalidades
- salario si estuviera disponible

### Salud y disponibilidad

- lesiones
- partidos perdidos
- continuidad competitiva

---

## 15. Estado de uso por notebook

| Notebook | Dataset principal | Estado |
|---|---|---|
| `01_data_understanding.ipynb` | `player_season_modeling.parquet` | Completado |
| `02_econometric_baseline.ipynb` | `player_season_modeling.parquet` | Completado |
| `03_econometric_model.ipynb` | `player_season_modeling.parquet` | Completado |
| `04_machine_learning_model.ipynb` | Pendiente | Próximo paso |
