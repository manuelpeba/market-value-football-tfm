# Schema Decisions

## Unidad de análisis

La unidad de análisis será jugador-temporada.

Cada fila representa el rendimiento, contexto y valor de mercado de un jugador en una temporada determinada.

## Clave primaria

La clave primaria del dataset final será:

- player_id
- season

## Identificador de jugador

Se utilizará un player_id interno para evitar dependencia exclusiva de identificadores externos.

Los identificadores de Transfermarkt, FBref y Understat se almacenarán como claves externas.

## Target principal

El target principal será:

- log_market_value_eur

Derivado de:

- market_value_eur

## Target secundario

El target dinámico será:

- delta_log_market_value_1y

Derivado de:

- market_value_eur en t
- market_value_eur en t+1

## Fuentes principales

- Transfermarkt: mercado y características del jugador.
- FBref: rendimiento deportivo.
- Understat: métricas ofensivas esperadas.
- StatsBomb Open Data: fuente complementaria no core.

## Reglas iniciales de inclusión

- Jugadores con registros identificables en al menos mercado y rendimiento.
- Temporadas con información suficiente de minutos y valor de mercado.
- Se mantendrá trazabilidad de registros excluidos.

## Riesgos principales

- Matching incorrecto entre fuentes.
- Cambios de club dentro de una temporada.
- Diferencias de nombres entre fuentes.
- Cobertura desigual por liga y temporada.
- Sesgo del valor de mercado por liga, club y exposición mediática.
