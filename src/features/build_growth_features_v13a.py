from pathlib import Path
import logging

import mlflow
import numpy as np
import pandas as pd


INPUT_PATH = Path(
    "data/processed/player_season_modeling_advanced_v13a.parquet"
)

OUTPUT_PATH = Path(
    "data/processed/player_season_modeling_growth_v13a.parquet"
)

MLFLOW_URI = "sqlite:///reports/sprint_13a1/xgboost/mlflow_v13a1.db"

EXPERIMENT_NAME = "sprint_13a1_growth_features"


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
)

logger = logging.getLogger(__name__)


def resolve_player_id_column(df: pd.DataFrame) -> str:
    candidates = [
        "player_id",
        "player_id_tm",
        "player_name",
        "player_name_fbref",
        "player_name_tm",
    ]

    for col in candidates:
        if col in df.columns:
            logger.info("Using player identifier column: %s", col)
            return col

    raise KeyError(
        "No valid player identifier column found. "
        f"Available columns: {df.columns.tolist()}"
    )


def resolve_season_column(df: pd.DataFrame) -> str:
    candidates = [
        "season_start_year",
        "season_start_year_fbref",
        "season_start_year_tm",
        "season",
    ]

    for col in candidates:
        if col in df.columns:
            logger.info("Using season column: %s", col)
            return col

    raise KeyError(
        "No valid season column found. "
        f"Available columns: {df.columns.tolist()}"
    )


def create_growth_features(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()

    player_col = resolve_player_id_column(df)
    season_col = resolve_season_column(df)

    required_cols = [
        player_col,
        season_col,
        "market_value_eur",
        "age",
    ]

    missing = [col for col in required_cols if col not in df.columns]

    if missing:
        raise KeyError(
            f"Missing required columns for growth features: {missing}"
        )

    logger.info("Sorting panel by %s and %s...", player_col, season_col)

    df = df.sort_values(
        by=[
            player_col,
            season_col,
        ]
    ).copy()

    logger.info("Creating lag market value feature...")

    if "market_value_prev_eur" not in df.columns:
        df["market_value_prev_eur"] = (
            df.groupby(player_col)["market_value_eur"]
            .shift(1)
        )

    logger.info("Creating historical market growth features...")

    df["market_value_growth_prev"] = (
        (
            df["market_value_eur"]
            - df["market_value_prev_eur"]
        )
        / df["market_value_prev_eur"]
    )

    df["delta_log_market_value_prev"] = (
        np.log1p(df["market_value_eur"])
        - np.log1p(df["market_value_prev_eur"])
    )

    logger.info("Creating age curve features...")

    df["age_squared"] = df["age"] ** 2

    logger.info("Creating career progression feature...")

    df["career_year"] = (
        df.groupby(player_col)
        .cumcount()
        + 1
    )

    logger.info("Creating breakout indicator...")

    if "minutes_played" in df.columns:
        df["breakout_indicator"] = (
            (df["career_year"] <= 2)
            & (df["minutes_played"] >= 900)
            & (df["market_value_growth_prev"] > 0.25)
        ).astype(int)
    else:
        df["breakout_indicator"] = np.nan

    return df


def main() -> None:
    mlflow.set_tracking_uri(MLFLOW_URI)
    mlflow.set_experiment(EXPERIMENT_NAME)

    logger.info("Loading dataset...")

    if not INPUT_PATH.exists():
        raise FileNotFoundError(f"Input dataset not found: {INPUT_PATH}")

    df = pd.read_parquet(INPUT_PATH)

    initial_cols = len(df.columns)
    initial_rows = len(df)

    df = create_growth_features(df)

    created_features = [
        "market_value_growth_prev",
        "delta_log_market_value_prev",
        "age_squared",
        "career_year",
        "breakout_indicator",
    ]

    OUTPUT_PATH.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    df.to_parquet(
        OUTPUT_PATH,
        index=False,
    )

    with mlflow.start_run(run_name="growth_features"):

        mlflow.log_param("pipeline", "build_growth_features")
        mlflow.log_param("input_path", str(INPUT_PATH))
        mlflow.log_param("output_path", str(OUTPUT_PATH))
        mlflow.log_param("created_features", ",".join(created_features))

        mlflow.log_metric("rows", initial_rows)
        mlflow.log_metric("initial_columns", initial_cols)
        mlflow.log_metric("final_columns", len(df.columns))
        mlflow.log_metric("created_features_count", len(created_features))

        for feature in created_features:
            if feature in df.columns:
                mlflow.log_metric(
                    f"missing_rate_{feature}",
                    float(df[feature].isna().mean()),
                )

        mlflow.log_artifact(str(OUTPUT_PATH))

    logger.info("Saved to %s", OUTPUT_PATH)
    logger.info("Created features: %s", created_features)


if __name__ == "__main__":
    main()