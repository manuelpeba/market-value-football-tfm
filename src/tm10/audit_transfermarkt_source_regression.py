import json
from pathlib import Path

import pandas as pd

ROOT = Path(".")


def audit_parquet(path, date_candidates):
    df = pd.read_parquet(path)

    date_col = next(
        (c for c in date_candidates if c in df.columns),
        None
    )

    if date_col:
        df[date_col] = pd.to_datetime(
            df[date_col],
            errors="coerce"
        )

    player_col = None

    if "player_id_tm" in df.columns:
        player_col = "player_id_tm"
    elif "player_id" in df.columns:
        player_col = "player_id"

    return {
        "path": str(path),
        "rows": int(len(df)),
        "players": int(df[player_col].nunique()) if player_col else None,
        "date_column": date_col,
        "date_min": str(df[date_col].min()) if date_col else None,
        "date_max": str(df[date_col].max()) if date_col else None,
    }


def audit_csv(path, date_candidates):
    df = pd.read_csv(path)

    date_col = next(
        (c for c in date_candidates if c in df.columns),
        None
    )

    if date_col:
        df[date_col] = pd.to_datetime(
            df[date_col],
            errors="coerce"
        )

    player_col = None

    if "player_id_tm" in df.columns:
        player_col = "player_id_tm"
    elif "player_id" in df.columns:
        player_col = "player_id"

    return {
        "path": str(path),
        "rows": int(len(df)),
        "players": int(df[player_col].nunique()) if player_col else None,
        "date_column": date_col,
        "date_min": str(df[date_col].min()) if date_col else None,
        "date_max": str(df[date_col].max()) if date_col else None,
    }


processed_source = audit_parquet(
    ROOT / "data/processed/transfermarkt_features_v13a.parquet",
    ["valuation_date", "date"]
)

current_snapshot = audit_parquet(
    ROOT / "data/processed/current_player_snapshot.parquet",
    ["current_valuation_date", "valuation_date", "date"]
)

raw_update = audit_csv(
    ROOT / "data/raw/transfermarkt/update_2025_2026/player_valuations.csv",
    ["valuation_date", "date"]
)

report = {
    "processed_transfermarkt_features": processed_source,
    "current_player_snapshot": current_snapshot,
    "raw_kaggle_update": raw_update,
    "regression_assessment": {
        "status": "SOURCE_REGRESSION_DETECTED",
        "official_source_to_keep": "data/processed/transfermarkt_features_v13a.parquet",
        "raw_update_should_replace_official": False,
        "date_max_processed": processed_source["date_max"],
        "date_max_raw_update": raw_update["date_max"],
        "rows_delta_raw_minus_processed":
            raw_update["rows"] - processed_source["rows"],
        "players_delta_raw_minus_processed":
            raw_update["players"] - processed_source["players"],
    }
}

output_json = (
    ROOT /
    "reports/tm10/transfermarkt_source_regression_audit.json"
)

output_json.write_text(
    json.dumps(
        report,
        indent=2,
        ensure_ascii=False
    ),
    encoding="utf-8"
)

markdown = f"""
# TM.10.0 — Transfermarkt Source Regression Audit

## Resultado

Se detecta una regresión objetiva en la versión más reciente disponible
en:

`data/raw/transfermarkt/update_2025_2026/player_valuations.csv`

| Fuente | Filas | Jugadores | Fecha máxima |
|---------|---------:|---------:|---------|
| transfermarkt_features_v13a.parquet | {processed_source['rows']:,} | {processed_source['players']:,} | {processed_source['date_max']} |
| player_valuations.csv | {raw_update['rows']:,} | {raw_update['players']:,} | {raw_update['date_max']} |

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
"""

output_md = (
    ROOT /
    "reports/tm10/transfermarkt_source_regression_audit.md"
)

output_md.write_text(
    markdown,
    encoding="utf-8"
)

print()
print("==============================================")
print("TM.10.0 SOURCE REGRESSION AUDIT")
print("==============================================")
print()

print(
    f"Processed source date max: "
    f"{processed_source['date_max']}"
)

print(
    f"Raw update date max: "
    f"{raw_update['date_max']}"
)

print()

print(
    f"Processed rows: "
    f"{processed_source['rows']:,}"
)

print(
    f"Raw rows: "
    f"{raw_update['rows']:,}"
)

print()

print(
    f"Processed players: "
    f"{processed_source['players']:,}"
)

print(
    f"Raw players: "
    f"{raw_update['players']:,}"
)

print()
print("Saved:", output_json)
print("Saved:", output_md)