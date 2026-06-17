
# TM.10.0 — Transfermarkt Source Regression Audit

## Resultado

Se detecta una regresión objetiva en la versión más reciente disponible
en:

`data/raw/transfermarkt/update_2025_2026/player_valuations.csv`

| Fuente | Filas | Jugadores | Fecha máxima |
|---------|---------:|---------:|---------|
| transfermarkt_features_v13a.parquet | 616,377 | 39,361 | 2026-03-30 00:00:00 |
| player_valuations.csv | 507,815 | 31,507 | 2026-02-27 00:00:00 |

## Decisión

No se reemplaza la fuente oficial actual.

La fuente oficial se mantiene en:

    data/processed/transfermarkt_features_v13a.parquet

El snapshot operativo se mantiene en:

    data/processed/current_player_snapshot.parquet

## Justificación metodológica

Aunque existe una actualización posterior del dataset bruto, la auditoría
muestra menor cobertura temporal y menor volumen de observaciones.

Por tanto, su integración degradaría la calidad del sistema y reduciría la
frescura de la variable económica principal.

## Implicación para TM.10

TM.10 debe evolucionar hacia una capa independiente de actualización de
valores actuales.

Separación recomendada:

    Kaggle = histórico reproducible

    Transfermarkt Current Snapshot = capa operativa actualizada

## Próximo paso

Diseñar TM.10.0:

Transfermarkt Independent Refresh Layer

Objetivo:

Generar snapshots operativos actualizados sin depender de Kaggle para
las actualizaciones periódicas del DSS.
