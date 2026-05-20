from pathlib import Path

import joblib
import numpy as np
import pandas as pd
import shap


ROOT = Path(__file__).resolve().parents[3]

MODEL_PATH = ROOT / "artifacts" / "models" / "hist_gradient_boosting.joblib"
DATA_PATH = ROOT / "data" / "processed" / "player_season_modeling.parquet"

OUTPUT_PATH = (
    ROOT
    / "reports"
    / "scouting_reports"
    / "player_shap_report.csv"
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


def build_feature_matrix(
    df: pd.DataFrame,
    model,
) -> tuple[pd.DataFrame, list[str]]:
    """
    Rebuild the exact feature matrix expected by the trained model.

    The persisted HistGradientBoosting model was trained with one-hot encoded
    league / season / position_group variables. Therefore, the raw modeling
    dataset must be encoded and aligned with model.feature_names_in_.
    """

    if not hasattr(model, "feature_names_in_"):
        raise AttributeError(
            "The model does not contain feature_names_in_. "
            "Cannot reconstruct the exact training feature matrix."
        )

    expected_features = list(model.feature_names_in_)

    df_model = df.copy()

    categorical_cols = [
        col
        for col in ["league", "season", "position_group"]
        if col in df_model.columns
    ]

    df_encoded = pd.get_dummies(
        df_model,
        columns=categorical_cols,
        drop_first=False,
    )

    for col in expected_features:
        if col not in df_encoded.columns:
            df_encoded[col] = 0

    X = df_encoded[expected_features].copy()

    X = X.replace([float("inf"), float("-inf")], pd.NA)
    X = X.fillna(0)

    return X, expected_features


def format_top_features(
    values: np.ndarray,
    features: list[str],
    positive: bool,
) -> str:
    pairs = list(zip(features, values))

    if positive:
        pairs = sorted(
            pairs,
            key=lambda x: x[1],
            reverse=True,
        )
        pairs = [pair for pair in pairs if pair[1] > 0]
    else:
        pairs = sorted(
            pairs,
            key=lambda x: x[1],
        )
        pairs = [pair for pair in pairs if pair[1] < 0]

    top = pairs[:3]

    return "; ".join(
        [
            f"{feature}: {value:.4f}"
            for feature, value in top
        ]
    )


def build_report(
    df: pd.DataFrame,
    X: pd.DataFrame,
    features: list[str],
    model,
) -> pd.DataFrame:
    explainer = shap.Explainer(model)
    shap_values = explainer(X)

    shap_matrix = np.asarray(
        getattr(shap_values, "values")
    )

    predictions = model.predict(X)

    report = df.copy()

    report["predicted_log_market_value"] = predictions
    report["predicted_market_value_eur"] = np.exp(predictions)

    if "market_value_eur" in report.columns:
        report["market_value_gap_eur"] = (
            report["predicted_market_value_eur"]
            - report["market_value_eur"]
        )

    if TARGET in report.columns:
        report["inefficiency_score"] = (
            report["predicted_log_market_value"]
            - report[TARGET]
        )

    report["top_positive_shap_factors"] = [
        format_top_features(
            values=row,
            features=features,
            positive=True,
        )
        for row in shap_matrix
    ]

    report["top_negative_shap_factors"] = [
        format_top_features(
            values=row,
            features=features,
            positive=False,
        )
        for row in shap_matrix
    ]

    preferred_cols = [
        "player_name_fbref",
        "player_name_tm",
        "club",
        "league",
        "season",
        "position_group",
        "age",
        "market_value_eur",
        "predicted_market_value_eur",
        "market_value_gap_eur",
        "inefficiency_score",
        "top_positive_shap_factors",
        "top_negative_shap_factors",
    ]

    cols = [
        col
        for col in preferred_cols
        if col in report.columns
    ]

    report = report[cols].copy()

    if "inefficiency_score" in report.columns:
        report = report.sort_values(
            by="inefficiency_score",
            ascending=False,
        )

    return report


def main() -> None:
    print("Loading model...")
    model = load_model()

    print("Loading data...")
    df = load_data()

    print("Building feature matrix aligned with training columns...")
    X, features = build_feature_matrix(
        df=df,
        model=model,
    )

    print(f"Features used: {len(features)}")
    print(features[:15])

    print("Building player-level SHAP report...")
    report = build_report(
        df=df,
        X=X,
        features=features,
        model=model,
    )

    OUTPUT_PATH.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    report.to_csv(
        OUTPUT_PATH,
        index=False,
    )

    print("\nDone")
    print(f"Output: {OUTPUT_PATH}")

    print("\nTop 10 rows:")
    print(report.head(10))


if __name__ == "__main__":
    main()