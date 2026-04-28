from pathlib import Path
import pandas as pd
import numpy as np
import argparse
import hashlib


ROOT = Path(__file__).resolve().parents[2]


def load_dataset(path: Path) -> pd.DataFrame:
    if path.suffix == ".csv":
        return pd.read_csv(path)
    elif path.suffix == ".parquet":
        return pd.read_parquet(path)
    else:
        raise ValueError("Unsupported format")


def generate_player_id(name: str) -> str:
    return hashlib.md5(name.encode()).hexdigest()


def extract_season_year(season: str) -> int:
    return int(season.split("-")[0])


def map_position_group(position: str) -> str:
    position = position.lower()

    if "goalkeeper" in position:
        return "GK"
    if "back" in position or "defender" in position:
        return "DEF"
    if "midfield" in position:
        return "MID"
    if "forward" in position or "wing" in position:
        return "ATT"

    return "UNK"


def build_features(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()

    # player_id
    df["player_id"] = df["player_name"].apply(generate_player_id)

    # season_year
    df["season_start_year"] = df["season"].apply(extract_season_year)

    # position_group
    df["position_group"] = df["position"].apply(map_position_group)

    # log market value
    df["log_market_value_eur"] = np.log(df["market_value_eur"])

    return df


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True)
    parser.add_argument(
        "--output",
        default="data/processed/transfermarkt_features.parquet"
    )
    args = parser.parse_args()

    input_path = ROOT / args.input
    output_path = ROOT / args.output

    df = load_dataset(input_path)
    df_features = build_features(df)

    output_path.parent.mkdir(parents=True, exist_ok=True)
    df_features.to_parquet(output_path, index=False)

    print("Feature engineering completed")
    print(f"Rows: {len(df_features):,}")
    print(f"Columns: {len(df_features.columns):,}")
    print(f"Output: {output_path}")


if __name__ == "__main__":
    main()
