from pathlib import Path
import argparse
import pandas as pd


ROOT = Path(__file__).resolve().parents[2]


def load_dataset(path: Path) -> pd.DataFrame:
    if path.suffix == ".csv":
        return pd.read_csv(path)
    if path.suffix == ".parquet":
        return pd.read_parquet(path)
    raise ValueError(f"Unsupported file format: {path.suffix}")


def profile_dataset(df: pd.DataFrame) -> pd.DataFrame:
    profile = pd.DataFrame({
        "column": df.columns,
        "dtype": [str(df[col].dtype) for col in df.columns],
        "non_null_count": [df[col].notna().sum() for col in df.columns],
        "null_count": [df[col].isna().sum() for col in df.columns],
        "null_pct": [round(df[col].isna().mean() * 100, 2) for col in df.columns],
        "unique_count": [df[col].nunique(dropna=True) for col in df.columns],
        "sample_values": [
            ", ".join(map(str, df[col].dropna().unique()[:5]))
            for col in df.columns
        ],
    })

    return profile


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--input",
        required=True,
        help="Path to dataset, relative to project root",
    )
    parser.add_argument(
        "--output",
        default="reports/tables/dataset_profile.csv",
        help="Output profile path, relative to project root",
    )

    args = parser.parse_args()

    input_path = ROOT / args.input
    output_path = ROOT / args.output

    df = load_dataset(input_path)
    profile = profile_dataset(df)

    output_path.parent.mkdir(parents=True, exist_ok=True)
    profile.to_csv(output_path, index=False)

    print("Dataset profiling completed")
    print(f"Rows: {len(df):,}")
    print(f"Columns: {len(df.columns):,}")
    print(f"Output: {output_path}")


if __name__ == "__main__":
    main()
