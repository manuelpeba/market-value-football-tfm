from pathlib import Path
import numpy as np
import pandas as pd
import statsmodels.formula.api as smf

from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score


INPUT_DATA = Path("data/processed/player_season_modeling_indices_v13a.parquet")
OUTPUT_DIR = Path("reports/sprint_13a1/ols")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

TARGET = "log_market_value_eur"
TIME_COL = "season_start_year"
SPLIT_YEAR = 2023

GROWTH_OLS_FEATURES = [
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
]

FIXED_EFFECTS = [
    "league",
    "position_group",
]


def ensure_columns(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()

    if "log_minutes_played" not in df.columns:
        if "minutes_played" not in df.columns:
            raise KeyError("Missing both log_minutes_played and minutes_played.")
        df["log_minutes_played"] = np.log1p(df["minutes_played"])

    required = GROWTH_OLS_FEATURES + FIXED_EFFECTS + [TARGET, TIME_COL]
    missing = [col for col in required if col not in df.columns]

    if missing:
        raise KeyError(f"Missing required columns: {missing}")

    return df


def build_formula() -> str:
    numeric = " + ".join(GROWTH_OLS_FEATURES)
    fixed = " + ".join([f"C({col})" for col in FIXED_EFFECTS])

    return f"{TARGET} ~ {numeric} + {fixed}"


def evaluate(y_true: pd.Series, y_pred: np.ndarray) -> dict[str, float]:
    return {
        "rmse": float(np.sqrt(mean_squared_error(y_true, y_pred))),
        "mae": float(mean_absolute_error(y_true, y_pred)),
        "r2": float(r2_score(y_true, y_pred)),
    }


def main() -> None:
    df = pd.read_parquet(INPUT_DATA)
    df = ensure_columns(df)

    model_cols = GROWTH_OLS_FEATURES + FIXED_EFFECTS + [TARGET, TIME_COL]
    model_df = df[model_cols].dropna().copy()

    train = model_df[model_df[TIME_COL] < SPLIT_YEAR].copy()
    test = model_df[model_df[TIME_COL] >= SPLIT_YEAR].copy()

    formula = build_formula()

    model = smf.ols(formula=formula, data=train).fit(cov_type="HC3")

    pred_train = model.predict(train)
    pred_test = model.predict(test)

    train_metrics = evaluate(train[TARGET], pred_train)
    test_metrics = evaluate(test[TARGET], pred_test)

    results = pd.DataFrame(
        [
            {"model": "growth_ols", "dataset": "v13a_11_leagues", "split": "train", **train_metrics},
            {"model": "growth_ols", "dataset": "v13a_11_leagues", "split": "test_temporal", **test_metrics},
        ]
    )

    results_path = OUTPUT_DIR / "growth_ols_temporal_v13a1_metrics.csv"
    summary_path = OUTPUT_DIR / "growth_ols_temporal_v13a1_summary.txt"

    results.to_csv(results_path, index=False)

    with open(summary_path, "w", encoding="utf-8") as f:
        f.write(model.summary().as_text())

    print("=" * 60)
    print("GROWTH OLS TEMPORAL — Sprint 13A.1")
    print("=" * 60)
    print("Input:", INPUT_DATA)
    print("Rows:", len(model_df))
    print("Train rows:", len(train))
    print("Test rows:", len(test))
    print()
    print(results)
    print()
    print("Metrics exported:", results_path)
    print("Summary exported:", summary_path)


if __name__ == "__main__":
    main()
