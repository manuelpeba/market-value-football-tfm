import pandas as pd

from src.utils.paths import (
    TABLES_DIR,
)


def build_model_comparison_table():

    ols_path = (
        TABLES_DIR
        / "ols_model_metrics.csv"
    )

    ml_path = (
        TABLES_DIR
        / "ml_model_metrics.csv"
    )

    ols_df = pd.read_csv(ols_path)
    ml_df = pd.read_csv(ml_path)

    comparison_df = pd.concat(
        [ols_df, ml_df],
        ignore_index=True,
    )

    comparison_df = comparison_df.sort_values(
        by="R2",
        ascending=False,
    ).reset_index(drop=True)

    output_path = (
        TABLES_DIR
        / "model_comparison.csv"
    )

    comparison_df.to_csv(
        output_path,
        index=False,
    )

    print("\nModel comparison:")
    print(comparison_df)

    print(f"\nSaved: {output_path}")

    return comparison_df


if __name__ == "__main__":
    build_model_comparison_table()