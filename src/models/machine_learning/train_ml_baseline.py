from pathlib import Path
import logging

import mlflow
import pandas as pd
import numpy as np

from sklearn.metrics import (
    mean_absolute_error,
    mean_squared_error,
    r2_score,
)

from sklearn.ensemble import (
    RandomForestRegressor,
)

from xgboost import XGBRegressor

from lightgbm import LGBMRegressor


INPUT_DATA = Path(
    "data/processed/player_season_modeling_indices.parquet"
)

MLFLOW_URI = "sqlite:///artifacts/metadata/mlflow.db"

EXPERIMENT_NAME = "market-value-model-comparison"

TARGET = "log_market_value_eur"


FEATURES = [

    "age",
    "age_squared",
    "career_year",

    "log_minutes_played",

    "goals_per90",
    "assists_per90",

    "breakout_indicator",

    "finishing_index",
    "playmaking_index",
    "experience_index",

    "goals_position_percentile",
    "assists_position_percentile",

]


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)

logger = logging.getLogger(__name__)


def evaluate_model(
    y_true,
    y_pred,
):

    rmse = np.sqrt(
        mean_squared_error(
            y_true,
            y_pred
        )
    )

    mae = mean_absolute_error(
        y_true,
        y_pred
    )

    r2 = r2_score(
        y_true,
        y_pred
    )

    return {

        "rmse":rmse,
        "mae":mae,
        "r2":r2

    }


def run_model(
    model,
    model_name,
    X_train,
    X_test,
    y_train,
    y_test,
):

    logger.info(
        "Running %s",
        model_name
    )

    model.fit(
        X_train,
        y_train
    )

    preds = model.predict(
        X_test
    )

    metrics = evaluate_model(
        y_test,
        preds
    )

    print()
    print("="*60)
    print(model_name)
    print("="*60)

    for k,v in metrics.items():

        print(
            f"{k}: {v:.4f}"
        )

    with mlflow.start_run(
        run_name=model_name
    ):

        mlflow.log_param(
            "model",
            model_name
        )

        for k,v in metrics.items():

            mlflow.log_metric(
                k,
                v
            )


def main():

    mlflow.set_tracking_uri(
        MLFLOW_URI
    )

    mlflow.set_experiment(
        EXPERIMENT_NAME
    )

    logger.info(
        "Loading dataset..."
    )

    df = pd.read_parquet(
        INPUT_DATA
    )

    if (
        "log_minutes_played"
        not in df.columns
    ):

        df[
            "log_minutes_played"
        ]=(

            np.log1p(
                df[
                    "minutes_played"
                ]
            )

        )

    TIME_COL = "season_start_year"

    cols = FEATURES + [TARGET, TIME_COL]

    df = df[cols].dropna()

    logger.info(
        "Rows:%s",
        len(df)
    )

    split_year = 2023

    train = df[
        df[TIME_COL] < split_year
    ]

    test = df[
        df[TIME_COL] >= split_year
    ]

    logger.info(
        "Train rows: %s",
        len(train)
    )

    logger.info(
        "Test rows: %s",
        len(test)
    )

    split_year=2023

    train=df[
        df[
            "season_start_year"
        ]<split_year
    ]

    test=df[
        df[
            "season_start_year"
        ]>=split_year
    ]

    X_train=train[
        FEATURES
    ]

    X_test=test[
        FEATURES
    ]

    y_train=train[
        TARGET
    ]

    y_test=test[
        TARGET
    ]

    models={

        "random_forest":

        RandomForestRegressor(
            n_estimators=300,
            random_state=42
        ),

        "xgboost":

        XGBRegressor(
            n_estimators=300,
            random_state=42
        ),

        "lightgbm":

        LGBMRegressor(
            n_estimators=300,
            random_state=42
        )

    }

    for name,model in models.items():

        run_model(
            model,
            name,
            X_train,
            X_test,
            y_train,
            y_test
        )


if __name__=="__main__":
    main()