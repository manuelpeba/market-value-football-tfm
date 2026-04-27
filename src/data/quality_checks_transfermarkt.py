from pathlib import Path
import pandas as pd
import argparse


ROOT = Path(__file__).resolve().parents[2]


def load_dataset(path: Path) -> pd.DataFrame:
    if path.suffix == ".csv":
        return pd.read_csv(path)
    if path.suffix == ".parquet":
        return pd.read_parquet(path)
    raise ValueError("Unsupported format")


def check_duplicates(df: pd.DataFrame):
    dup = df.duplicated(subset=["player_name", "season"]).sum()
    print(f"Duplicates (player_name + season): {dup}")


def check_market_value(df: pd.DataFrame):
    negative = (df["market_value_eur"] <= 0).sum()
    print(f"Invalid market values (<=0): {negative}")


def check_age(df: pd.DataFrame):
    invalid = df[(df["age"] < 15) | (df["age"] > 45)].shape[0]
    print(f"Invalid ages: {invalid}")


def check_missing(df: pd.DataFrame):
    print("\nMissing values:")
    print(df.isna().sum())


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True)
    args = parser.parse_args()

    df = load_dataset(ROOT / args.input)

    print("=== DATA QUALITY REPORT ===\n")

    check_duplicates(df)
    check_market_value(df)
    check_age(df)
    check_missing(df)


if __name__ == "__main__":
    main()
