# Data Dictionary

## Dataset final: mart_player_season

Unidad de análisis: jugador-temporada.

Clave primaria:
- player_id
- season

## Identificación

| Variable | Tipo | Descripción | Fuente |
|---|---|---|---|
| player_id | string | Identificador interno único del jugador | Interna |
| season | string | Temporada deportiva | Interna |
| player_name | string | Nombre del jugador | Transfermarkt/FBref |
| birth_date | date | Fecha de nacimiento | Transfermarkt |
| age | integer | Edad del jugador en la temporada | Transfermarkt |
| nationality | string | Nacionalidad principal | Transfermarkt |
| position | string | Posición específica | Transfermarkt/FBref |
| position_group | string | GK/DEF/MID/ATT | Interna |

## Mercado

| Variable | Tipo | Descripción | Fuente |
|---|---|---|---|
| market_value_eur | float | Valor de mercado observado | Transfermarkt |
| log_market_value_eur | float | Logaritmo del valor de mercado | Derivada |
| market_value_prev_eur | float | Valor de mercado temporada anterior | Derivada |
| market_value_next_eur | float | Valor de mercado temporada siguiente | Derivada |
| market_value_growth_1y | float | Crecimiento porcentual a un año | Derivada |
| delta_log_market_value_1y | float | Diferencia logarítmica del valor a un año | Derivada |

## Rendimiento

| Variable | Tipo | Descripción | Fuente |
|---|---|---|---|
| minutes_played | integer | Minutos jugados | FBref |
| goals_per90 | float | Goles por 90 minutos | FBref |
| assists_per90 | float | Asistencias por 90 minutos | FBref |
| xg_per90 | float | Expected goals por 90 | Understat/FBref |
| xa_per90 | float | Expected assists por 90 | Understat/FBref |
| progressive_passes_per90 | float | Pases progresivos por 90 | FBref |
| progressive_carries_per90 | float | Conducciones progresivas por 90 | FBref |
| tackles_per90 | float | Entradas por 90 | FBref |
| interceptions_per90 | float | Intercepciones por 90 | FBref |

## Índices derivados

| Variable | Tipo | Descripción | Fuente |
|---|---|---|---|
| finishing_index | float | Índice agregado de finalización | Derivada |
| playmaking_index | float | Índice agregado de creación | Derivada |
| progression_index | float | Índice agregado de progresión | Derivada |
| defensive_index | float | Índice agregado defensivo | Derivada |

## Calidad

| Variable | Tipo | Descripción | Fuente |
|---|---|---|---|
| data_quality_score | float | Indicador agregado de calidad del registro | Interna |
| matching_confidence | float | Confianza del matching entre fuentes | Interna |
| source_coverage_flag | string | Cobertura disponible por fuente | Interna |