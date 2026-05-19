from __future__ import annotations

import argparse
import logging
from pathlib import Path
from typing import Iterable

import numpy as np
import pandas as pd

try:
    import mlflow
except ImportError:
    mlflow = None


ROOT = Path(__file__).resolve().parents[2]

DEFAULT_INPUT_PATH = ROOT / "data" / "processed" / "player_season_modeling.parquet"
DEFAULT_OUTPUT_PATH = ROOT / "data" / "processed" / "player_season_modeling_advanced.parquet"
DEFAULT_LOG_PATH = ROOT / "logs" / "build_advanced_features.log"

MLFLOW_TRACKING_URI = "sqlite:///artifacts/metadata/mlflow.db"
MLFLOW_EXPERIMENT_NAME = "market-value-football-tfm"

GROUP_COLS = ["position_group", "league"]

Z_SCORE_FEATURES = [
    "goals_per90",
    "assists_per90",
    "shots_per90",
]

PERCENTILE_FEATURES = [
    "goals_per90",
    "assists_per90",
]


def setup_logging(log_path: Path = DEFAULT_LOG_PATH) -> logging.Logger:
    log_path.parent.mkdir(parents=True, exist_ok=True)

    logger = logging.getLogger("build_advanced_features")
    logger.setLevel(logging.INFO)
    logger.handlers.clear()

    formatter = logging.Formatter(
        fmt="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    file_handler = logging.FileHandler(log_path, encoding="utf-8")
    file_handler.setFormatter(formatter)

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger


def validate_required_columns(df: pd.DataFrame, required_cols: Iterable[str]) -> None:
    missing = [col for col in required_cols if col not in df.columns]

    if missing:
        raise KeyError(
            "Missing required columns for advanced feature engineering: "
            f"{missing}. Available columns: {df.columns.tolist()}"
        )


def add_groupwise_z_scores(
    df: pd.DataFrame,
    features: Iterable[str],
    group_cols: list[str],
    logger: logging.Logger,
) -> pd.DataFrame:
    df = df.copy()

    for feature in features:
        output_col = f"{feature.replace('_per90', '')}_per90_pos_z"

        if feature not in df.columns:
            logger.warning(
                "Feature '%s' not found. Creating '%s' as NaN to keep schema stable.",
                feature,
                output_col,
            )
            df[output_col] = np.nan
            continue

        group_mean = df.groupby(group_cols)[feature].transform("mean")
        group_std = df.groupby(group_cols)[feature].transform("std").replace(0, np.nan)

        df[output_col] = (df[feature] - group_mean) / group_std

        logger.info(
            "Created z-score feature: %s grouped by %s",
            output_col,
            group_cols,
        )

    return df


def add_groupwise_percentiles(
    df: pd.DataFrame,
    features: Iterable[str],
    group_cols: list[str],
    logger: logging.Logger,
) -> pd.DataFrame:
    df = df.copy()

    for feature in features:
        output_col = f"{feature.replace('_per90', '')}_position_percentile"

        if feature not in df.columns:
            logger.warning(
                "Feature '%s' not found. Creating '%s' as NaN to keep schema stable.",
                feature,
                output_col,
            )
            df[output_col] = np.nan
            continue

        df[output_col] = (
            df.groupby(group_cols)[feature]
            .rank(method="average", pct=True)
        )

        logger.info(
            "Created percentile feature: %s grouped by %s",
            output_col,
            group_cols,
        )

    return df


def log_to_mlflow(
    df: pd.DataFrame,
    input_path: Path,
    output_path: Path,
    log_path: Path,
    initial_cols: int,
    created_features: list[str],
    logger: logging.Logger,
) -> None:
    if mlflow is None:
        logger.warning("MLflow is not installed. Skipping MLflow tracking.")
        return

    mlflow.set_tracking_uri(MLFLOW_TRACKING_URI)
    mlflow.set_experiment(MLFLOW_EXPERIMENT_NAME)

    with mlflow.start_run(run_name="build_advanced_features_positional_normalization"):
        mlflow.log_param("pipeline", "build_advanced_features")
        mlflow.log_param("feature_block", "positional_normalization")
        mlflow.log_param("input_path", str(input_path))
        mlflow.log_param("output_path", str(output_path))
        mlflow.log_param("group_cols", ",".join(GROUP_COLS))
        mlflow.log_param("z_score_features", ",".join(Z_SCORE_FEATURES))
        mlflow.log_param("percentile_features", ",".join(PERCENTILE_FEATURES))

        mlflow.log_metric("rows", len(df))
        mlflow.log_metric("initial_columns", initial_cols)
        mlflow.log_metric("final_columns", len(df.columns))
        mlflow.log_metric("created_features_count", len(created_features))
        mlflow.log_metric("missing_values_created_features", int(df[created_features].isna().sum().sum()))

        for feature in created_features:
            missing_rate = float(df[feature].isna().mean())
            mlflow.log_metric(f"missing_rate_{feature}", missing_rate)

        if output_path.exists():
            mlflow.log_artifact(str(output_path))

        if log_path.exists():
            mlflow.log_artifact(str(log_path))


def build_advanced_features(
    input_path: Path = DEFAULT_INPUT_PATH,
    output_path: Path = DEFAULT_OUTPUT_PATH,
    log_path: Path = DEFAULT_LOG_PATH,
    use_mlflow: bool = True,
) -> pd.DataFrame:
    logger = setup_logging(log_path)

    logger.info("Loading modeling dataset from: %s", input_path)

    if not input_path.exists():
        raise FileNotFoundError(f"Input dataset not found: {input_path}")

    df = pd.read_parquet(input_path)

    validate_required_columns(
        df,
        required_cols=[
            "position_group",
            "league",
            "goals_per90",
            "assists_per90",
        ],
    )

    initial_rows = len(df)
    initial_cols = len(df.columns)

    logger.info("Initial rows: %s", f"{initial_rows:,}")
    logger.info("Initial columns: %s", f"{initial_cols:,}")

    df = add_groupwise_z_scores(
        df=df,
        features=Z_SCORE_FEATURES,
        group_cols=GROUP_COLS,
        logger=logger,
    )

    df = add_groupwise_percentiles(
        df=df,
        features=PERCENTILE_FEATURES,
        group_cols=GROUP_COLS,
        logger=logger,
    )

    created_features = [
        "goals_per90_pos_z",
        "assists_per90_pos_z",
        "shots_per90_pos_z",
        "goals_position_percentile",
        "assists_position_percentile",
    ]

    available_created_features = [col for col in created_features if col in df.columns]

    output_path.parent.mkdir(parents=True, exist_ok=True)
    df.to_parquet(output_path, index=False)

    logger.info("Advanced feature dataset created")
    logger.info("Final rows: %s", f"{len(df):,}")
    logger.info("Final columns: %s", f"{len(df.columns):,}")
    logger.info("Created features: %s", available_created_features)
    logger.info("Output path: %s", output_path)

    if use_mlflow:
        log_to_mlflow(
            df=df,
            input_path=input_path,
            output_path=output_path,
            log_path=log_path,
            initial_cols=initial_cols,
            created_features=available_created_features,
            logger=logger,
        )

    return df


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Build advanced positional normalization features."
    )

    parser.add_argument(
        "--input",
        default=str(DEFAULT_INPUT_PATH),
        help="Input modeling dataset parquet path.",
    )

    parser.add_argument(
        "--output",
        default=str(DEFAULT_OUTPUT_PATH),
        help="Output advanced modeling dataset parquet path.",
    )

    parser.add_argument(
        "--log-path",
        default=str(DEFAULT_LOG_PATH),
        help="Log file path.",
    )

    parser.add_argument(
        "--no-mlflow",
        action="store_true",
        help="Disable MLflow tracking.",
    )

    return parser.parse_args()


def main() -> None:
    args = parse_args()

    build_advanced_features(
        input_path=Path(args.input),
        output_path=Path(args.output),
        log_path=Path(args.log_path),
        use_mlflow=not args.no_mlflow,
    )


if __name__ == "__main__":
    main()