# Market Value Dynamics and Inefficiency in European Football Transfers

TFM - Master Data Science

## Objetivo

Construir un sistema analítico para identificar jugadores infravalorados en el mercado europeo mediante la estimación del valor de mercado esperado y su potencial de crecimiento futuro.

## Unidad de análisis

Jugador-temporada.

## Fuentes de datos previstas

- Transfermarkt: valor de mercado, edad, club, posición, historial de traspasos.
- FBref: métricas de rendimiento por jugador y temporada.
- Understat: xG, xA y métricas ofensivas avanzadas.
- StatsBomb Open Data: eventos avanzados, uso complementario.

## Estructura del proyecto

- data/raw: datos originales.
- data/interim: datos transformados intermedios.
- data/processed: dataset final de modelización.
- notebooks: análisis exploratorio.
- src: código reutilizable.
- reports: gráficos, tablas y resultados.
- docs: documentación metodológica y decisiones.

## Output esperado

- Inefficiency Score.
- Growth Score.
- Confidence Score.
- Ranking de jugadores infravalorados.
