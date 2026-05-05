# Fuentes de datos

## Transfermarkt

Uso:
- Target principal: market_value.
- Edad, club, posición, nacionalidad.
- Historial de valores de mercado.
- Historial de transferencias.

Riesgos:
- Valor de mercado estimado, no precio real.
- Posibles sesgos de popularidad, liga, club y nacionalidad.
- Matching complejo con otras fuentes.

## FBref

Uso:
- Métricas de rendimiento por jugador.
- Variables por 90 minutos.
- Estadísticas ofensivas, defensivas y de posesión.

Riesgos:
- Cambios de formato.
- Diferencias de nombres de jugadores.
- Cobertura variable por competición/temporada.

## Understat

Uso:
- xG.
- xA.
- Métricas ofensivas avanzadas.

Riesgos:
- Principalmente orientado a ligas concretas.
- Menor riqueza de variables que FBref.

## StatsBomb Open Data

Uso:
- Enriquecimiento mediante eventos avanzados.

Riesgos:
- Cobertura limitada.
- No debe ser fuente core del dataset final.

## Construcción de Transfermarkt Features

A partir del dataset `davidcariboo/player-scores`, se utiliza como tabla principal `player_valuations.csv`, que contiene registros históricos de valor de mercado por jugador y fecha.

El proceso transforma esta información a nivel jugador-temporada mediante los siguientes pasos:

1. Conversión de `date` a formato temporal.
2. Asignación de cada valoración a una temporada deportiva.
3. Agregación por `player_id` y temporada.
4. Selección del último valor disponible dentro de cada temporada como proxy del valor de mercado observado.
5. Enriquecimiento con información maestra de `players.csv`.
6. Cálculo de `log_market_value_eur`.
7. Generación de variables dinámicas:
   - `market_value_prev_eur`
   - `market_value_next_eur`
   - `market_value_growth_1y`
   - `delta_log_market_value_1y`

El output generado es:

`data/processed/transfermarkt_features.parquet`

## Decisión sobre scraping directo de Transfermarkt

Se descarta el scraping directo complejo de Transfermarkt como fuente principal del proyecto debido a:

- Mayor fragilidad ante cambios HTML.
- Mayor coste de mantenimiento.
- Riesgo de bloqueos o inconsistencias.
- Menor reproducibilidad frente a una fuente estructurada.

No obstante, se mantiene como posible línea futura la creación de un script específico de scraping para actualizar jugadores o competiciones concretas.
