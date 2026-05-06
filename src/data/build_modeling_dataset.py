from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]

INPUT_PATH = ROOT / "data/processed/player_season_panel.parquet"
OUTPUT_PATH = ROOT / "data/processed/player_season_modeling.parquet"

MIN_SEASON = 2020
MAX_SEASON = 2023

MIN_AGE = 18
MAX_AGE = 23

MIN_MINUTES = 300
MIN_MATCHING_CONFIDENCE = 0.90
MAX_AGE_DIFF = 1.5
MIN_MARKET_VALUE_EUR = 500_000


def get_or_create_modeling_columns(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()

    if "season_x" in df.columns and "season" not in df.columns:
        df = df.rename(columns={"season_x": "season"})
    elif "season_fbref" in df.columns and "season" not in df.columns:
        df = df.rename(columns={"season_fbref": "season"})

    if "season" not in df.columns:
        raise KeyError(f"No season column found. Available columns: {df.columns.tolist()}")

    if "season_start_year_fbref" in df.columns:
        df["season_start_year"] = df["season_start_year_fbref"]
    elif "season_start_year_tm" in df.columns:
        df["season_start_year"] = df["season_start_year_tm"]
    elif "season_start_year" in df.columns:
        df["season_start_year"] = df["season_start_year"]
    else:
        df["season_start_year"] = df["season"].astype(str).str[:4].astype(int)

    if "age_tm" in df.columns:
        df["age"] = df["age_tm"]
    elif "age_fbref" in df.columns:
        df["age"] = df["age_fbref"]
    elif "age" not in df.columns:
        raise KeyError("No age column found.")

    if "age_diff" not in df.columns:
        if "age_fbref" in df.columns and "age_tm" in df.columns:
            df["age_diff"] = (df["age_fbref"] - df["age_tm"]).abs()
        else:
            df["age_diff"] = pd.NA

    if "position_group" not in df.columns:
        if "position_group_tm" in df.columns:
            df["position_group"] = df["position_group_tm"]
        elif "position_group_fbref" in df.columns:
            df["position_group"] = df["position_group_fbref"]
        else:
            df["position_group"] = "UNK"

    if "player_name_fbref" not in df.columns:
        raise KeyError("No player_name_fbref column found.")

    return df


def build_modeling_dataset() -> pd.DataFrame:
    print("Loading panel...")
    df = pd.read_parquet(INPUT_PATH)
    df = get_or_create_modeling_columns(df)

    initial_rows = len(df)

    df = df[df["matching_status"] == True].copy()
    after_matched = len(df)

    df = df[df["age_diff"].notna()]
    df = df[df["age_diff"] <= MAX_AGE_DIFF]
    after_age_validation = len(df)

    if "matching_confidence" in df.columns:
        df = df[df["matching_confidence"] >= MIN_MATCHING_CONFIDENCE]
    after_confidence = len(df)

    df = df[
        (df["season_start_year"] >= MIN_SEASON) &
        (df["season_start_year"] <= MAX_SEASON)
    ]
    after_season = len(df)

    df = df[
        (df["age"] >= MIN_AGE) &
        (df["age"] <= MAX_AGE)
    ]
    after_age_filter = len(df)

    df = df[df["minutes_played"] >= MIN_MINUTES]
    after_minutes = len(df)

    df = df[df["market_value_eur"].notna()]
    df = df[df["log_market_value_eur"].notna()]
    df = df[df["market_value_eur"] >= MIN_MARKET_VALUE_EUR]
    after_target = len(df)

    df = df[df["position_group"].notna()]
    df = df[df["position_group"] != "UNK"]
    after_position = len(df)

    dedup_cols = ["player_name_fbref", "season"]
    if "club" in df.columns:
        dedup_cols.append("club")

    sort_cols = [
        col for col in ["matching_confidence", "club_score", "minutes_played", "market_value_eur"]
        if col in df.columns
    ]

    df = df.sort_values(
        by=sort_cols,
        ascending=[False] * len(sort_cols)
    )

    df = df.drop_duplicates(subset=dedup_cols)

    final_rows = len(df)

    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    df.to_parquet(OUTPUT_PATH, index=False)

    print("\nModeling dataset construido")
    print(f"Initial rows: {initial_rows:,}")
    print(f"After matched only: {after_matched:,}")
    print(f"After age validation: {after_age_validation:,}")
    print(f"After confidence filter: {after_confidence:,}")
    print(f"After season filter: {after_season:,}")
    print(f"After age filter: {after_age_filter:,}")
    print(f"After minutes filter: {after_minutes:,}")
    print(f"After target filter: {after_target:,}")
    print(f"After position filter: {after_position:,}")
    print(f"Final rows: {final_rows:,}")
    print(f"Players: {df['player_name_fbref'].nunique():,}")
    print(f"Seasons: {df['season'].min()} - {df['season'].max()}")
    print(f"Output: {OUTPUT_PATH}")

    print("\nMatching methods:")
    print(df["matching_method"].value_counts(dropna=False))

    print("\nAge diff summary:")
    print(df["age_diff"].describe())

    if "club_score" in df.columns:
        print("\nClub score summary:")
        print(df["club_score"].describe())

    print("\nMarket value summary:")
    print(df["market_value_eur"].describe())

    print("\nPosition groups:")
    print(df["position_group"].value_counts())

    if "league" in df.columns:
        print("\nLeagues:")
        print(df["league"].value_counts())

    return df


if __name__ == "__main__":
    build_modeling_dataset()