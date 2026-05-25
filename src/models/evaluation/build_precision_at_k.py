from pathlib import Path
import argparse
import pandas as pd


ROOT = Path(__file__).resolve().parents[3]

DEFAULT_INPUT_PATH = (
    ROOT / "reports" / "rankings" / "scoring_dataset_opportunity.csv"
)

DEFAULT_OUTPUT_DIR = ROOT / "reports" / "evaluation"

K_VALUES = [10, 20, 50, 100]

REQUIRED_COLUMNS = [
    "opportunity_score",
]


def validate_columns(
    df: pd.DataFrame,
    required_columns: list[str],
) -> None:

    missing = [
        c for c in required_columns
        if c not in df.columns
    ]

    if missing:
        raise KeyError(
            f"Missing columns: {missing}"
        )


def create_future_success_label(
    df: pd.DataFrame,
) -> pd.Series:

    if "market_value_growth_1y" in df.columns:

        growth = pd.to_numeric(
            df["market_value_growth_1y"],
            errors="coerce"
        )

        return (growth > 0).astype(int)

    elif "delta_log_market_value_1y" in df.columns:

        growth = pd.to_numeric(
            df["delta_log_market_value_1y"],
            errors="coerce"
        )

        return (growth > 0).astype(int)

    elif "market_value_next_eur" in df.columns and \
         "market_value_eur" in df.columns:

        next_value = pd.to_numeric(
            df["market_value_next_eur"],
            errors="coerce"
        )

        current_value = pd.to_numeric(
            df["market_value_eur"],
            errors="coerce"
        )

        return (
            next_value > current_value
        ).astype(int)

    raise ValueError(
        (
            "No future value variables found. "
            "Expected one of: "
            "market_value_growth_1y, "
            "delta_log_market_value_1y, "
            "market_value_next_eur"
        )
    )


def compute_precision_at_k(
    df: pd.DataFrame,
    k: int,
) -> dict:

    subset = df.head(k)

    positives = subset["future_success"].sum()

    precision = positives / len(subset)

    return {
        "k": k,
        "players": len(subset),
        "true_positive": positives,
        "precision_at_k": precision,
    }


def export_csv(
    df: pd.DataFrame,
    output_path: Path
):

    output_path.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    df.to_csv(
        output_path,
        index=False
    )


def main():

    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--input",
        default=str(DEFAULT_INPUT_PATH),
    )

    parser.add_argument(
        "--output-dir",
        default=str(DEFAULT_OUTPUT_DIR),
    )

    args = parser.parse_args()

    input_path = Path(args.input)
    output_dir = Path(args.output_dir)

    if not input_path.is_absolute():
        input_path = ROOT / input_path

    if not output_dir.is_absolute():
        output_dir = ROOT / output_dir

    df = pd.read_csv(input_path)

    validate_columns(
        df,
        REQUIRED_COLUMNS,
    )

    df["future_success"] = (
        create_future_success_label(df)
    )

    df = (
        df
        .sort_values(
            "opportunity_score",
            ascending=False
        )
        .reset_index(drop=True)
    )

    results = []

    for k in K_VALUES:

        if k > len(df):
            continue

        results.append(
            compute_precision_at_k(
                df,
                k,
            )
        )

    results_df = pd.DataFrame(results)

    output_path = (
        output_dir /
        "precision_at_k.csv"
    )

    export_csv(
        results_df,
        output_path
    )

    print(
        "Precision@K completed"
    )

    print(
        f"Input: {input_path}"
    )

    print(
        f"Output: {output_path}"
    )

    print()
    print(results_df)


if __name__ == "__main__":
    main()