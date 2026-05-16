from pathlib import Path

import numpy as np
import pandas as pd

from src.models.econometric.train_ols import train_ols_model
from src.models.evaluation.metrics import regression_metrics
from src.models.scoring.inefficiency import add_inefficiency_scores
from src.models.scoring.rankings import (
    get_undervalued_players,
    get_overvalued_players,
)

from src.utils.paths import (
    PROCESSED_DATA_DIR,
    TABLES_DIR,
    RANKINGS_DIR,
)

from src.utils.dataset_versioning import version_dataset
from src.utils.experiment_tracking import setup_mlflow, log_experiment


INPUT_PATH = PROCESSED_DATA_DIR / "player_season_modeling.parquet"

DATASET_NAME = "player_season_modeling"
DATASET_VERSION = "v1" # Actualizar manualmente cuando cambie el esquema o las features del dataset

EXPERIMENT_NAME = "market_value_modeling"
MODEL_NAME = "OLS_final_temporal"

TRAIN_MAX_SEASON_START_YEAR = 2023
TEST_SEASON_START_YEAR = 2024


def run_ols_pipeline():
    print("Versioning dataset...")

    dataset_metadata_path = version_dataset(
        dataset_path=INPUT_PATH,
        dataset_name=DATASET_NAME,
        logical_version=DATASET_VERSION,
        pipeline_name="run_ols_pipeline",
    )

    print("\nLoading modeling dataset...")

    df = pd.read_parquet(INPUT_PATH)

    df["log_minutes_played"] = np.log1p(df["minutes_played"])

    print(f"Rows: {len(df):,}")

    print("\nCreating temporal split...")

    train_df = df[
        df["season_start_year"] <= TRAIN_MAX_SEASON_START_YEAR
    ].copy()

    test_df = df[
        df["season_start_year"] == TEST_SEASON_START_YEAR
    ].copy()

    if train_df.empty:
        raise ValueError("Train dataset is empty after temporal split.")

    if test_df.empty:
        raise ValueError("Test dataset is empty after temporal split.")

    print(f"Train rows: {len(train_df):,}")
    print(f"Test rows: {len(test_df):,}")

    print("\nTraining OLS model...")

    model = train_ols_model(
    train_df,
    include_season_fe=False,
    )

    print("Generating test predictions...")

    test_df["predicted_log_market_value"] = model.predict(test_df)

    metrics = regression_metrics(
        y_true=test_df["log_market_value_eur"],
        y_pred=test_df["predicted_log_market_value"],
        model_name=MODEL_NAME,
    )

    print("\nOut-of-sample metrics:")
    print(metrics)

    TABLES_DIR.mkdir(parents=True, exist_ok=True)

    metrics_df = pd.DataFrame([metrics])

    metrics_output_path = TABLES_DIR / "ols_model_metrics.csv"

    metrics_df.to_csv(metrics_output_path, index=False)

    print(f"\nSaved metrics: {metrics_output_path}")

    print("\nComputing inefficiency scores on test set...")

    test_df = add_inefficiency_scores(test_df)

    undervalued = get_undervalued_players(test_df)
    overvalued = get_overvalued_players(test_df)

    RANKINGS_DIR.mkdir(parents=True, exist_ok=True)

    undervalued_output = RANKINGS_DIR / "ols_undervalued.csv"
    overvalued_output = RANKINGS_DIR / "ols_overvalued.csv"

    undervalued.to_csv(undervalued_output, index=False)
    overvalued.to_csv(overvalued_output, index=False)

    print(f"\nSaved undervalued ranking: {undervalued_output}")
    print(f"Saved overvalued ranking: {overvalued_output}")

    print("\nLogging experiment to MLflow...")

    setup_mlflow(EXPERIMENT_NAME)

    params = {
        "model_type": "OLS",
        "covariance_type": "HC3",
        "target": "log_market_value_eur",
        "dataset_version": DATASET_VERSION,
        "train_max_season_start_year": TRAIN_MAX_SEASON_START_YEAR,
        "test_season_start_year": TEST_SEASON_START_YEAR,
        "train_rows": len(train_df),
        "test_rows": len(test_df),
        "features": (
            "age, log_minutes_played, goals_per90, assists_per90, "
            "league FE, position FE"
        ),
        "season_fe": False,
        "season_fe_note": (
            "Disabled for temporal validation because test season is unseen during training."
        ),
    }

    tags = {
        "stage": "econometric_baseline",
        "framework": "statsmodels",
        "validation": "temporal_split",
        "train_period": "2019-2020_to_2023-2024",
        "test_period": "2024-2025",
        "pipeline": "run_ols_pipeline",
    }

    artifacts = [
        str(metrics_output_path),
        str(undervalued_output),
        str(overvalued_output),
    ]

    metric_values = {
        key: float(value)
        for key, value in metrics.items()
        if key != "model"
    }

    log_experiment(
        model_name=MODEL_NAME,
        dataset_metadata_path=dataset_metadata_path,
        metrics=metric_values,
        params=params,
        tags=tags,
        artifacts=artifacts,
    )

    print("\nTop undervalued:")

    print(
        undervalued[
            [
                "player_name_fbref",
                "inefficiency_score",
            ]
        ].head()
    )

    return {
        "model": model,
        "train_dataset": train_df,
        "test_dataset": test_df,
        "metrics": metrics_df,
        "undervalued": undervalued,
        "overvalued": overvalued,
        "dataset_metadata_path": Path(dataset_metadata_path),
    }


if __name__ == "__main__":
    run_ols_pipeline()