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
