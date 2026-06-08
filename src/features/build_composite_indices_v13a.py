from pathlib import Path
import logging

import mlflow
import numpy as np
import pandas as pd


INPUT_PATH = Path(
    "data/processed/player_season_modeling_growth_v13a.parquet"
)

OUTPUT_PATH = Path(
    "data/processed/player_season_modeling_indices_v13a.parquet"
)

MLFLOW_URI = "sqlite:///reports/sprint_13a1/xgboost/mlflow_v13a1.db"

EXPERIMENT_NAME = "sprint_13a1_composite_indices"


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
)

logger = logging.getLogger(__name__)


def zscore(series: pd.Series) -> pd.Series:
    std = series.std()

    if std == 0 or pd.isna(std):
        return pd.Series(
            np.nan,
            index=series.index,
        )

    return (
        series
        - series.mean()
    ) / std


def add_safe_zscore(
    df: pd.DataFrame,
    source_col: str,
    output_col: str,
) -> pd.DataFrame:
    df = df.copy()

    if source_col not in df.columns:
        logger.warning(
            "Column %s not found. Creating %s as NaN.",
            source_col,
            output_col,
        )
        df[output_col] = np.nan
        return df

    df[output_col] = zscore(
        df[source_col]
    )

    logger.info(
        "Created %s from %s.",
        output_col,
        source_col,
    )

    return df


def create_composite_indices(
    df: pd.DataFrame,
) -> pd.DataFrame:
    df = df.copy()

    logger.info(
        "Creating base z-score components..."
    )

    df = add_safe_zscore(
        df,
        "goals_per90",
        "z_goals_per90_global",
    )

    df = add_safe_zscore(
        df,
        "assists_per90",
        "z_assists_per90_global",
    )

    df = add_safe_zscore(
        df,
        "age",
        "z_age_global",
    )

    df = add_safe_zscore(
        df,
        "career_year",
        "z_career_year_global",
    )

    df = add_safe_zscore(
        df,
        "market_value_growth_prev",
        "z_market_value_growth_prev_global",
    )

    df = add_safe_zscore(
        df,
        "delta_log_market_value_prev",
        "z_delta_log_market_value_prev_global",
    )

    logger.info(
        "Creating composite indices..."
    )

    df["finishing_index"] = (
        df[
            [
                "z_goals_per90_global",
                "goals_position_percentile",
            ]
        ]
        .mean(
            axis=1
        )
    )

    df["playmaking_index"] = (
        df[
            [
                "z_assists_per90_global",
                "assists_position_percentile",
            ]
        ]
        .mean(
            axis=1
        )
    )

    df["growth_index"] = (
        df[
            [
                "z_market_value_growth_prev_global",
                "z_delta_log_market_value_prev_global",
                "breakout_indicator",
            ]
        ]
        .mean(
            axis=1
        )
    )

    df["experience_index"] = (
        df[
            [
                "z_career_year_global",
                "z_age_global",
            ]
        ]
        .mean(
            axis=1
        )
    )

    return df


def main() -> None:
    mlflow.set_tracking_uri(
        MLFLOW_URI
    )

    mlflow.set_experiment(
        EXPERIMENT_NAME
    )

    logger.info(
        "Loading dataset..."
    )

    if not INPUT_PATH.exists():
        raise FileNotFoundError(
            f"Input dataset not found: {INPUT_PATH}"
        )

    df = pd.read_parquet(
        INPUT_PATH
    )

    initial_cols = len(
        df.columns
    )

    df = create_composite_indices(
        df
    )

    created_features = [
        "finishing_index",
        "playmaking_index",
        "growth_index",
        "experience_index",
    ]

    OUTPUT_PATH.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    df.to_parquet(
        OUTPUT_PATH,
        index=False,
    )

    with mlflow.start_run(
        run_name="composite_football_indices"
    ):
        mlflow.log_param(
            "pipeline",
            "build_composite_indices"
        )

        mlflow.log_param(
            "input_path",
            str(INPUT_PATH)
        )

        mlflow.log_param(
            "output_path",
            str(OUTPUT_PATH)
        )

        mlflow.log_param(
            "created_features",
            ",".join(
                created_features
            )
        )

        mlflow.log_metric(
            "rows",
            len(df)
        )

        mlflow.log_metric(
            "initial_columns",
            initial_cols
        )

        mlflow.log_metric(
            "final_columns",
            len(df.columns)
        )

        mlflow.log_metric(
            "created_features_count",
            len(created_features)
        )

        for feature in created_features:
            mlflow.log_metric(
                f"missing_rate_{feature}",
                float(
                    df[feature]
                    .isna()
                    .mean()
                ),
            )

        mlflow.log_artifact(
            str(OUTPUT_PATH)
        )

    logger.info(
        "Saved to %s",
        OUTPUT_PATH,
    )

    logger.info(
        "Created features: %s",
        created_features,
    )


if __name__ == "__main__":
    main()