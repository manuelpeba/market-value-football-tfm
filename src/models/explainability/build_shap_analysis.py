from pathlib import Path

import joblib
import matplotlib.pyplot as plt
import pandas as pd
import shap
import numpy as np


ROOT = Path(__file__).resolve().parents[3]

MODEL_PATH = (
    ROOT
    / "artifacts"
    / "models"
    / "hist_gradient_boosting.joblib"
)

DATA_PATH = (
    ROOT
    / "data"
    / "processed"
    / "player_season_modeling.parquet"
)

OUTPUT_TABLE = (
    ROOT
    / "reports"
    / "tables"
    / "explainability"
    / "shap_global_importance.csv"
)

OUTPUT_SUMMARY = (
    ROOT
    / "reports"
    / "figures"
    / "explainability"
    / "shap_summary.png"
)

TARGET = "log_market_value_eur"


def load_model():
    if not MODEL_PATH.exists():
        raise FileNotFoundError(f"Model not found: {MODEL_PATH}")

    return joblib.load(MODEL_PATH)


def load_data():
    if not DATA_PATH.exists():
        raise FileNotFoundError(f"Dataset not found: {DATA_PATH}")

    return pd.read_parquet(DATA_PATH)


def build_feature_matrix(df: pd.DataFrame) -> tuple[pd.DataFrame, list[str]]:
    """
    Build a SHAP-compatible feature matrix.

    SHAP TreeExplainer requires numeric inputs for this model.
    Datetime, object, category and boolean columns are excluded here.
    """

    numeric_cols = (
        df
        .select_dtypes(
            include=[
                "int64",
                "float64",
                "int32",
                "float32",
            ]
        )
        .columns
        .tolist()
    )

    features = [
        col
        for col in numeric_cols
        if col != TARGET
    ]

    if not features:
        raise ValueError("No numeric features found for SHAP analysis.")

    X = df[features].copy()
    X = X.replace([float("inf"), float("-inf")], pd.NA)
    X = X.fillna(0)

    return X, features


def calculate_shap_importance(model, X: pd.DataFrame, features: list[str]):

    explainer = shap.Explainer(model)

    shap_values = explainer(X)

    shap_matrix = np.asarray(
        getattr(shap_values, "values")
    )

    importance = pd.DataFrame(
        {
            "feature": features,
            "importance": np.abs(
                shap_matrix
            ).mean(axis=0)
        }
    )

    importance = (
        importance
        .sort_values(
            by="importance",
            ascending=False
        )
        .reset_index(drop=True)
    )

    return importance, shap_values


def save_outputs(
    importance: pd.DataFrame,
    shap_values,
    X: pd.DataFrame,
) -> None:
    OUTPUT_TABLE.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_SUMMARY.parent.mkdir(parents=True, exist_ok=True)

    importance.to_csv(OUTPUT_TABLE, index=False)

    plt.figure()

    shap.summary_plot(
        shap_values,
        X,
        show=False,
    )

    plt.tight_layout()

    plt.savefig(
        OUTPUT_SUMMARY,
        dpi=300,
        bbox_inches="tight",
    )

    plt.close()


def main() -> None:
    print("Loading model...")
    model = load_model()

    print("Loading data...")
    df = load_data()

    print("Building numeric feature matrix...")
    X, features = build_feature_matrix(df)

    print(f"Features used: {len(features)}")
    print(features[:15])

    print("Calculating SHAP values...")
    importance, shap_values = calculate_shap_importance(
        model=model,
        X=X,
        features=features,
    )

    print("Saving outputs...")
    save_outputs(
        importance=importance,
        shap_values=shap_values,
        X=X,
    )

    print("\nDone")
    print(f"Output table: {OUTPUT_TABLE}")
    print(f"Output figure: {OUTPUT_SUMMARY}")

    print("\nTop 10 SHAP features:")
    print(importance.head(10))


if __name__ == "__main__":
    main()