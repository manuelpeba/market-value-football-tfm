import numpy as np
import pandas as pd

from src.models.econometric.train_ols import (
    train_ols_model,
)

from src.models.evaluation.metrics import (
    regression_metrics,
)

from src.models.scoring.inefficiency import (
    add_inefficiency_scores,
)

from src.models.scoring.rankings import (
    get_undervalued_players,
    get_overvalued_players,
)

from src.utils.paths import (
    PROCESSED_DATA_DIR,
    TABLES_DIR,
)


INPUT_PATH = (
    PROCESSED_DATA_DIR
    / "player_season_modeling.parquet"
)


def run_ols_pipeline():

    print("Loading modeling dataset...")

    df = pd.read_parquet(INPUT_PATH)

    df["log_minutes_played"] = np.log1p(
        df["minutes_played"]
    )

    print(f"Rows: {len(df):,}")

    print("\nTraining OLS model...")

    model = train_ols_model(df)

    print("Generating predictions...")

    df["predicted_log_market_value"] = (
        model.predict(df)
    )

    metrics = regression_metrics(
        y_true=df["log_market_value_eur"],
        y_pred=df["predicted_log_market_value"],
        model_name="OLS_final",
    )

    print("\nMetrics:")
    print(metrics)

    TABLES_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    metrics_df = pd.DataFrame([metrics])

    metrics_output_path = (
        TABLES_DIR
        / "ols_model_metrics.csv"
    )

    metrics_df.to_csv(
        metrics_output_path,
        index=False,
    )

    print(f"\nSaved metrics: {metrics_output_path}")

    print("\nComputing inefficiency scores...")

    df = add_inefficiency_scores(df)

    undervalued = get_undervalued_players(df)
    overvalued = get_overvalued_players(df)

    undervalued.to_csv(
        TABLES_DIR / "ols_undervalued.csv",
        index=False,
    )

    overvalued.to_csv(
        TABLES_DIR / "ols_overvalued.csv",
        index=False,
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
        "dataset": df,
        "metrics": metrics_df,
        "undervalued": undervalued,
        "overvalued": overvalued,
    }


if __name__ == "__main__":
    run_ols_pipeline()