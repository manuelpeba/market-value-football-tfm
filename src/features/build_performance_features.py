from pathlib import Path
import argparse
import numpy as np
import pandas as pd


ROOT = Path(__file__).resolve().parents[2]


PERFORMANCE_COLUMNS = [
    "goals_per90",
    "assists_per90",
    "shots_per90",
    "progressive_passes_per90",
    "progressive_carries_per90",
    "tackles_per90",
    "interceptions_per90",
]


def load_dataset(path: str | Path) -> pd.DataFrame:
    path = Path(path)

    if not path.is_absolute():
        path = ROOT / path

    if path.suffix == ".parquet":
        return pd.read_parquet(path)

    if path.suffix == ".csv":
        return pd.read_csv(path)

    raise ValueError(f"Unsupported file format: {path.suffix}")


def get_league_column(df: pd.DataFrame) -> str:
    if "league" in df.columns:
        return "league"
    if "league_tm" in df.columns:
        return "league_tm"
    if "league_fbref" in df.columns:
        return "league_fbref"

    raise KeyError(
        "No league column found. Expected one of: league, league_tm, league_fbref"
    )


def safe_zscore(series: pd.Series) -> pd.Series:
    mean = series.mean()
    std = series.std(ddof=0)

    if pd.isna(std) or std == 0:
        return pd.Series(0.0, index=series.index)

    return (series - mean) / std


def add_group_zscores(
    df: pd.DataFrame,
    columns: list[str],
    group_cols: list[str],
) -> pd.DataFrame:
    df = df.copy()

    for col in columns:
        if col not in df.columns:
            print(f"Warning: column not found and skipped: {col}")
            continue

        z_col = f"z_{col}"

        df[z_col] = (
            df.groupby(group_cols, dropna=False)[col]
            .transform(safe_zscore)
        )

    return df


def add_performance_indexes(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()

    df["finishing_index"] = df[
        [
            "z_goals_per90",
            "z_shots_per90",
        ]
    ].mean(axis=1)

    df["playmaking_index"] = df[
        [
            "z_assists_per90",
            "z_progressive_passes_per90",
        ]
    ].mean(axis=1)

    df["progression_index"] = df[
        [
            "z_progressive_passes_per90",
            "z_progressive_carries_per90",
        ]
    ].mean(axis=1)

    df["defensive_index"] = df[
        [
            "z_tackles_per90",
            "z_interceptions_per90",
        ]
    ].mean(axis=1)

    return df


def add_minutes_flags(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()

    if "minutes_played" not in df.columns:
        raise KeyError("Missing required column: minutes_played")

    df["minutes_bucket"] = pd.cut(
        df["minutes_played"],
        bins=[-np.inf, 450, 900, 1800, np.inf],
        labels=["low", "medium", "high", "very_high"],
    )

    df["is_low_minutes"] = df["minutes_played"] < 900

    return df


def build_performance_features(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()

    league_col = get_league_column(df)

    df = add_group_zscores(
        df=df,
        columns=PERFORMANCE_COLUMNS,
        group_cols=["position_group", league_col],
    )

    df = add_performance_indexes(df)
    df = add_minutes_flags(df)

    return df


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--input",
        default="data/processed/player_season_panel.parquet",
    )
    parser.add_argument(
        "--output",
        default="data/processed/player_season_features.parquet",
    )
    args = parser.parse_args()

    df = load_dataset(args.input)
    features = build_performance_features(df)

    output_path = ROOT / args.output
    output_path.parent.mkdir(parents=True, exist_ok=True)
    features.to_parquet(output_path, index=False)

    print("Performance feature engineering completed")
    print(f"Rows: {len(features):,}")
    print(f"Columns: {len(features.columns):,}")
    print(f"Output: {output_path}")

    created_columns = [
        col for col in features.columns
        if col.startswith("z_") or col.endswith("_index")
    ]

    print("\nCreated feature columns:")
    for col in created_columns:
        print(f"- {col}")


if __name__ == "__main__":
    main()