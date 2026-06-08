from pathlib import Path
from typing import Any, cast
import logging
import warnings

import mlflow
import numpy as np
import pandas as pd

from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestRegressor, HistGradientBoostingRegressor
from sklearn.impute import SimpleImputer
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.model_selection import RandomizedSearchCV
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

from xgboost import XGBRegressor
from lightgbm import LGBMRegressor


warnings.filterwarnings("ignore", message="X does not have valid feature names")


# ==========================================================
# CONFIG
# ==========================================================

ROOT = Path(__file__).resolve().parents[3]

# Sprint 13A.1 experimental multi-league dataset
INPUT_DATA = ROOT / "data/processed/player_season_modeling_indices_v13a.parquet"
EXPERIMENT_DIR = ROOT / "reports" / "sprint_13a1" / "xgboost"

MLFLOW_URI = f"sqlite:///{EXPERIMENT_DIR / 'mlflow_v13a1.db'}"
EXPERIMENT_NAME = "sprint_13a1_multileague_xgboost"

# Isolated experiment outputs to avoid contaminating productive artifacts
EXPERIMENT_DIR = ROOT / "reports" / "sprint_13a1" / "xgboost"

TARGET = "log_market_value_eur"
OBSERVED_MARKET_VALUE = "market_value_eur"
TIME_COL = "season_start_year"
SPLIT_YEAR = 2023

NUMERIC_FEATURES = [
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

CATEGORICAL_FEATURES = [
    "league",
    "season",
    "position_group",
]

FEATURES = NUMERIC_FEATURES + CATEGORICAL_FEATURES

FEATURE_IMPORTANCE_DIR = EXPERIMENT_DIR / "feature_importance"
PREDICTIONS_DIR = EXPERIMENT_DIR / "predictions"
TABLES_DIR = EXPERIMENT_DIR / "tables"

FEATURE_IMPORTANCE_DIR.mkdir(parents=True, exist_ok=True)
PREDICTIONS_DIR.mkdir(parents=True, exist_ok=True)
TABLES_DIR.mkdir(parents=True, exist_ok=True)

# ==========================================================
# LOGGING
# ==========================================================

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
)

logger = logging.getLogger(__name__)


# ==========================================================
# DATA HELPERS
# ==========================================================

def ensure_columns(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()

    if "log_minutes_played" not in df.columns:
        if "minutes_played" not in df.columns:
            raise KeyError("Missing both log_minutes_played and minutes_played.")

        logger.info("Creating log_minutes_played...")
        df["log_minutes_played"] = np.log1p(df["minutes_played"])

    required_cols = FEATURES + [TARGET, TIME_COL, OBSERVED_MARKET_VALUE]

    missing = [col for col in required_cols if col not in df.columns]

    if missing:
        raise KeyError(
            f"Missing required columns: {missing}. "
            f"Available columns: {df.columns.tolist()}"
        )

    return df


def build_preprocessor() -> ColumnTransformer:
    numeric_pipeline = Pipeline(
        steps=[
            ("imputer", SimpleImputer(strategy="median")),
            ("scaler", StandardScaler()),
        ]
    )

    categorical_pipeline = Pipeline(
        steps=[
            ("imputer", SimpleImputer(strategy="most_frequent")),
            (
                "onehot",
                OneHotEncoder(
                    handle_unknown="ignore",
                    sparse_output=False,
                ),
            ),
        ]
    )

    return ColumnTransformer(
        transformers=[
            ("num", numeric_pipeline, NUMERIC_FEATURES),
            ("cat", categorical_pipeline, CATEGORICAL_FEATURES),
        ],
        remainder="drop",
    )


# ==========================================================
# METRICS
# ==========================================================

def evaluate(y_true: pd.Series, y_pred: np.ndarray) -> dict[str, float]:
    return {
        "rmse": float(np.sqrt(mean_squared_error(y_true, y_pred))),
        "mae": float(mean_absolute_error(y_true, y_pred)),
        "r2": float(r2_score(y_true, y_pred)),
    }


# ==========================================================
# FEATURE IMPORTANCE
# ==========================================================

def get_feature_names(preprocessor: ColumnTransformer) -> list[str]:
    cat_pipeline = preprocessor.named_transformers_["cat"]
    cat_encoder = cat_pipeline.named_steps["onehot"]

    categorical_names = list(
        cat_encoder.get_feature_names_out(CATEGORICAL_FEATURES)
    )

    return NUMERIC_FEATURES + categorical_names


def export_feature_importance(
    model_name: str,
    fitted_pipeline: Pipeline,
) -> Path | None:
    model = fitted_pipeline.named_steps["model"]
    preprocessor = fitted_pipeline.named_steps["preprocess"]

    if not hasattr(model, "feature_importances_"):
        return None

    feature_names = get_feature_names(preprocessor)
    importances = model.feature_importances_

    importance_df = (
        pd.DataFrame(
            {
                "feature": feature_names,
                "importance": importances,
            }
        )
        .sort_values("importance", ascending=False)
        .reset_index(drop=True)
    )

    output_path = FEATURE_IMPORTANCE_DIR / f"{model_name}_feature_importance.csv"
    importance_df.to_csv(output_path, index=False)

    return output_path


# ==========================================================
# PREDICTION EXPORT
# ==========================================================

def add_prediction_columns(
    df: pd.DataFrame,
    model_name: str,
    predictions: np.ndarray,
    y_true: pd.Series,
) -> pd.DataFrame:
    predictions_df = df.copy()

    predictions_df["model_name"] = model_name
    predictions_df["predicted_log_market_value"] = predictions
    predictions_df["observed_log_market_value"] = y_true.values
    predictions_df["prediction_error_log"] = (
        predictions_df["observed_log_market_value"]
        - predictions_df["predicted_log_market_value"]
    )

    return predictions_df


def export_test_predictions(
    model_name: str,
    fitted_pipeline: Pipeline,
    test_df: pd.DataFrame,
    X_test: pd.DataFrame,
    y_test: pd.Series,
) -> Path:
    predictions = np.asarray(fitted_pipeline.predict(X_test))

    predictions_df = add_prediction_columns(
        df=test_df,
        model_name=model_name,
        predictions=predictions,
        y_true=y_test,
    )

    output_path = PREDICTIONS_DIR / f"{model_name}_test_predictions.csv"
    predictions_df.to_csv(output_path, index=False)

    logger.info("Test predictions exported: %s", output_path)

    return output_path


def export_full_predictions(
    model_name: str,
    fitted_pipeline: Pipeline,
    df: pd.DataFrame,
    X: pd.DataFrame,
    y: pd.Series,
) -> Path:
    predictions = np.asarray(fitted_pipeline.predict(X))

    predictions_df = add_prediction_columns(
        df=df,
        model_name=model_name,
        predictions=predictions,
        y_true=y,
    )

    full_output_path = PREDICTIONS_DIR / f"{model_name}_full_predictions.csv"
    canonical_output_path = PREDICTIONS_DIR / "tuned_xgboost_predictions.csv"

    latest_season = predictions_df["season"].max()
    scoring_df = predictions_df[
        predictions_df["season"] == latest_season
    ].copy()

    predictions_df.to_csv(full_output_path, index=False)

    if model_name == "tuned_xgboost":
        scoring_df.to_csv(canonical_output_path, index=False)

        logger.info(
            "Canonical scoring predictions exported for season %s: %s",
            latest_season,
            canonical_output_path,
        )

    logger.info("Full historical predictions exported: %s", full_output_path)
    logger.info("Scoring rows: %s", len(scoring_df))
    logger.info("Full rows: %s", len(predictions_df))

    return full_output_path


# ==========================================================
# MODEL EXECUTION
# ==========================================================

def run_tuned_model(
    model_name: str,
    estimator: Any,
    param_distributions: dict[str, list[Any]],
    X_train: pd.DataFrame,
    y_train: pd.Series,
    X_test: pd.DataFrame,
    y_test: pd.Series,
) -> tuple[dict[str, float], Pipeline]:
    logger.info("Running tuned model: %s", model_name)

    pipeline = Pipeline(
        steps=[
            ("preprocess", build_preprocessor()),
            ("model", estimator),
        ]
    )

    search = RandomizedSearchCV(
        estimator=pipeline,
        param_distributions=param_distributions,
        n_iter=12,
        scoring="neg_root_mean_squared_error",
        cv=3,
        random_state=42,
        n_jobs=-1,
        verbose=0,
    )

    search.fit(X_train, y_train)

    best_model: Pipeline = cast(Pipeline, search.best_estimator_)

    preds = np.asarray(best_model.predict(X_test))
    metrics = evaluate(y_test, preds)

    print("\n" + "=" * 60)
    print(model_name)
    print("=" * 60)
    print(f"Best params: {search.best_params_}")

    for key, value in metrics.items():
        print(f"{key}: {value:.4f}")

    with mlflow.start_run(run_name=model_name):
        mlflow.log_param("model_type", model_name)
        mlflow.log_param("target", TARGET)
        mlflow.log_param("split_year", SPLIT_YEAR)
        mlflow.log_param("numeric_features", ",".join(NUMERIC_FEATURES))
        mlflow.log_param("categorical_features", ",".join(CATEGORICAL_FEATURES))
        mlflow.log_param("best_params", str(search.best_params_))

        mlflow.log_metric("train_rows", len(X_train))
        mlflow.log_metric("test_rows", len(X_test))

        for key, value in metrics.items():
            mlflow.log_metric(key, value)

        importance_path = export_feature_importance(
            model_name=model_name,
            fitted_pipeline=best_model,
        )

        if importance_path is not None:
            mlflow.log_artifact(str(importance_path))

    return metrics, best_model


# ==========================================================
# MAIN
# ==========================================================

def main() -> None:
    mlflow.set_tracking_uri(MLFLOW_URI)
    mlflow.set_experiment(EXPERIMENT_NAME)

    logger.info("Loading dataset...")

    if not INPUT_DATA.exists():
        raise FileNotFoundError(f"Input dataset not found: {INPUT_DATA}")

    df = pd.read_parquet(INPUT_DATA)
    df = ensure_columns(df)

    df = df.dropna(subset=[TARGET, TIME_COL]).copy()

    train = df[df[TIME_COL] < SPLIT_YEAR].copy()
    test = df[df[TIME_COL] >= SPLIT_YEAR].copy()

    X_train = train[FEATURES]
    y_train = train[TARGET]

    X_test = test[FEATURES]
    y_test = test[TARGET]

    X_full = df[FEATURES]
    y_full = df[TARGET]

    logger.info("Train rows: %s", len(train))
    logger.info("Test rows: %s", len(test))
    logger.info("Full scoring rows: %s", len(df))

    models: dict[str, tuple[Any, dict[str, list[Any]]]] = {
        "tuned_random_forest": (
            RandomForestRegressor(random_state=42),
            {
                "model__n_estimators": [200, 400, 600],
                "model__max_depth": [4, 6, 8, 12, None],
                "model__min_samples_split": [2, 5, 10],
                "model__min_samples_leaf": [1, 2, 4],
                "model__max_features": ["sqrt", 0.7, 1.0],
            },
        ),
        "tuned_xgboost": (
            XGBRegressor(
                objective="reg:squarederror",
                random_state=42,
                n_jobs=-1,
            ),
            {
                "model__n_estimators": [200, 400, 600],
                "model__max_depth": [2, 3, 4, 5],
                "model__learning_rate": [0.01, 0.03, 0.05, 0.1],
                "model__subsample": [0.7, 0.85, 1.0],
                "model__colsample_bytree": [0.7, 0.85, 1.0],
                "model__reg_lambda": [1, 5, 10],
            },
        ),
        "tuned_lightgbm": (
            LGBMRegressor(
                random_state=42,
                verbosity=-1,
            ),
            {
                "model__n_estimators": [200, 400, 600],
                "model__num_leaves": [15, 31, 63],
                "model__learning_rate": [0.01, 0.03, 0.05, 0.1],
                "model__subsample": [0.7, 0.85, 1.0],
                "model__colsample_bytree": [0.7, 0.85, 1.0],
                "model__reg_lambda": [0, 1, 5, 10],
            },
        ),
        "hist_gradient_boosting": (
            HistGradientBoostingRegressor(random_state=42),
            {
                "model__max_iter": [100, 200, 400],
                "model__learning_rate": [0.01, 0.03, 0.05, 0.1],
                "model__max_leaf_nodes": [15, 31, 63],
                "model__l2_regularization": [0, 0.01, 0.1, 1],
            },
        ),
    }

    results = []
    fitted_models: dict[str, Pipeline] = {}

    for model_name, (estimator, params) in models.items():
        metrics, fitted_model = run_tuned_model(
            model_name=model_name,
            estimator=estimator,
            param_distributions=params,
            X_train=X_train,
            y_train=y_train,
            X_test=X_test,
            y_test=y_test,
        )

        results.append(
            {
                "model": model_name,
                **metrics,
            }
        )

        fitted_models[model_name] = fitted_model

    results_df = (
        pd.DataFrame(results)
        .sort_values("rmse")
        .reset_index(drop=True)
    )

    comparison_output_path = TABLES_DIR / "ml_tuned_model_comparison.csv"
    results_df.to_csv(comparison_output_path, index=False)

    print("\n" + "=" * 60)
    print("TUNED ML COMPARISON")
    print("=" * 60)
    print(results_df)

    best_model_name = str(results_df.iloc[0]["model"])
    best_model = fitted_models[best_model_name]

    test_predictions_output_path = export_test_predictions(
        model_name=best_model_name,
        fitted_pipeline=best_model,
        test_df=test,
        X_test=X_test,
        y_test=y_test,
    )

    full_predictions_output_path = export_full_predictions(
        model_name=best_model_name,
        fitted_pipeline=best_model,
        df=df,
        X=X_full,
        y=y_full,
    )

    with mlflow.start_run(run_name="tuned_ml_comparison_summary"):
        mlflow.log_param("pipeline", "train_ml_tuned")
        mlflow.log_param("target", TARGET)
        mlflow.log_param("split_year", SPLIT_YEAR)
        mlflow.log_param("best_model", best_model_name)

        mlflow.log_metric("models_evaluated", len(results_df))
        mlflow.log_metric("best_rmse", float(results_df.iloc[0]["rmse"]))
        mlflow.log_metric("best_mae", float(results_df.iloc[0]["mae"]))
        mlflow.log_metric("best_r2", float(results_df.iloc[0]["r2"]))

        mlflow.log_artifact(str(comparison_output_path))
        mlflow.log_artifact(str(test_predictions_output_path))
        mlflow.log_artifact(str(full_predictions_output_path))

    logger.info("Best model: %s", best_model_name)
    logger.info("Comparison exported: %s", comparison_output_path)
    logger.info("Test predictions exported: %s", test_predictions_output_path)
    logger.info("Full predictions exported: %s", full_predictions_output_path)


if __name__ == "__main__":
    main()