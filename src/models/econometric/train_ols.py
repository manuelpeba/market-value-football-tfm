from pathlib import Path
import logging

import mlflow
import numpy as np
import pandas as pd
import statsmodels.formula.api as smf
from sklearn.metrics import (
    mean_absolute_error,
    mean_squared_error,
    r2_score,
)

from src.models.econometric.specifications import (
    OLS_MODEL_SPECS,
    FIXED_EFFECTS,
    ECONOMETRIC_TARGET,
)


# ==========================================================
# CONFIG
# ==========================================================

INPUT_DATA = Path(
    "data/processed/player_season_modeling_indices.parquet"
)

MLFLOW_URI = (
    "sqlite:///artifacts/metadata/mlflow.db"
)

EXPERIMENT_NAME = (
    "market-value-model-comparison"
)


# ==========================================================
# LOGGING
# ==========================================================

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)

logger = logging.getLogger(__name__)


# ==========================================================
# HELPERS
# ==========================================================

def ensure_modeling_columns(
    df: pd.DataFrame
) -> pd.DataFrame:

    df = df.copy()

    if "log_minutes_played" not in df.columns:

        if "minutes_played" not in df.columns:

            raise KeyError(
                "Neither 'log_minutes_played' "
                "nor 'minutes_played' found."
            )

        logger.info(
            "Creating log_minutes_played..."
        )

        df["log_minutes_played"] = np.log1p(
            df["minutes_played"]
        )

    return df


def build_formula(
    features: list[str]
):

    numeric = " + ".join(
        features
    )

    fixed = " + ".join(
        [
            f"C({f})"
            for f in FIXED_EFFECTS
        ]
    )

    formula = f"""
    {ECONOMETRIC_TARGET}
    ~
    {numeric}
    +
    {fixed}
    """

    return formula


def evaluate(
    y_true,
    y_pred
):

    return {

        "rmse":
        np.sqrt(
            mean_squared_error(
                y_true,
                y_pred
            )
        ),

        "mae":
        mean_absolute_error(
            y_true,
            y_pred
        ),

        "r2":
        r2_score(
            y_true,
            y_pred
        )
    }


# ==========================================================
# MODEL EXECUTION
# ==========================================================

def run_model(
    name: str,
    features: list[str],
    df: pd.DataFrame
):

    logger.info(
        f"Running: {name}"
    )

    cols = (
        features
        +
        FIXED_EFFECTS
        +
        [ECONOMETRIC_TARGET]
    )

    model_df = (

        df[
            cols
        ]

        .dropna()

    )

    logger.info(
        f"Rows after NA removal: {len(model_df):,}"
    )

    formula = build_formula(
        features
    )

    logger.info(
        f"Formula:\n{formula}"
    )

    model = smf.ols(
        formula=formula,
        data=model_df
    ).fit(
        cov_type="HC3"
    )

    pred = model.predict(
        model_df
    )

    metrics = evaluate(
        model_df[
            ECONOMETRIC_TARGET
        ],
        pred
    )

    with mlflow.start_run(
        run_name=name
    ):

        mlflow.log_param(
            "model",
            name
        )

        mlflow.log_param(
            "features",
            ",".join(
                features
            )
        )

        mlflow.log_metric(
            "rows",
            len(model_df)
        )

        for k, v in metrics.items():

            mlflow.log_metric(
                k,
                v
            )

        summary_path = (
            Path(
                "artifacts/models"
            )
            /
            f"{name}_summary.txt"
        )

        summary_path.parent.mkdir(
            parents=True,
            exist_ok=True
        )

        with open(
            summary_path,
            "w",
            encoding="utf-8"
        ) as f:

            f.write(
                model.summary().as_text()
            )

        mlflow.log_artifact(
            str(summary_path)
        )

    print("\n")
    print("=" * 60)
    print(name)
    print("=" * 60)

    for k, v in metrics.items():

        print(
            f"{k}: {v:.4f}"
        )


# ==========================================================
# MAIN
# ==========================================================

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

    logger.info(
        f"Rows: {len(df):,}"
    )

    logger.info(
        f"Columns: {len(df.columns)}"
    )

    df = ensure_modeling_columns(
        df
    )

    for model_name, spec in OLS_MODEL_SPECS.items():

        run_model(
            name=model_name,
            features=spec[
                "features"
            ],
            df=df
        )

    logger.info(
        "Training finished."
    )


if __name__ == "__main__":
    main()