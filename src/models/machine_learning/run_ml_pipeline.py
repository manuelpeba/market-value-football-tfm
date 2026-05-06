import pandas as pd

from src.models.machine_learning.pipelines import (
    prepare_ml_dataset,
)

from src.models.machine_learning.train_ml import (
    build_ml_models,
)

from src.models.evaluation.metrics import (
    regression_metrics,
)

from src.utils.paths import (
    PROCESSED_DATA_DIR,
    TABLES_DIR,
)


INPUT_PATH = (
    PROCESSED_DATA_DIR
    / "player_season_modeling.parquet"
)


def run_ml_pipeline():

    print("Loading modeling dataset...")

    df = pd.read_parquet(INPUT_PATH)

    print(f"Rows: {len(df):,}")

    print("\nPreparing ML dataset...")

    X, y, df_model = prepare_ml_dataset(df)

    print(f"Rows after feature preparation: {len(df_model):,}")
    print(f"Features: {X.shape[1]:,}")

    models = build_ml_models()

    results = []

    for model_name, model in models.items():

        print(f"\nTraining {model_name}...")

        model.fit(X, y)

        predictions = model.predict(X)

        metrics = regression_metrics(
            y_true=y,
            y_pred=predictions,
            model_name=model_name,
        )

        results.append(metrics)

        print(metrics)

    metrics_df = pd.DataFrame(results)

    TABLES_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    output_path = TABLES_DIR / "ml_model_metrics.csv"

    metrics_df.to_csv(
        output_path,
        index=False,
    )

    print(f"\nMetrics exported to: {output_path}")

    return {
        "models": models,
        "metrics": metrics_df,
        "X": X,
        "y": y,
        "dataset": df_model,
    }


if __name__ == "__main__":
    run_ml_pipeline()