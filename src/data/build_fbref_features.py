from pathlib import Path
import re
import pandas as pd
import argparse

from src.data.ingest_fbref import extract_fbref_player_table


ROOT = Path(__file__).resolve().parents[2]

RAW_PATH = ROOT / "data" / "raw" / "fbref" / "standard_html"
DEFAULT_OUTPUT_PATH = ROOT / "data" / "processed" / "fbref_features.parquet"


LEAGUE_MAP = {
    "premier_league": "Premier League",
    "laliga": "LaLiga",
    "bundesliga": "Bundesliga",
    "serie_a": "Serie A",
    "ligue_1": "Ligue 1",
    "eredivisie": "Eredivisie",
    "primeira_liga": "Liga Portugal",

    # Sprint 13A — Multi-League Expansion
    "championship": "Championship",
    "belgian_pro_league": "Belgian Pro League",
    "spanish_segunda": "Spanish Segunda División",
    "austrian_bundesliga": "Austrian Bundesliga",
}


RENAME_MAP = {
    "Unnamed: 1_level_0_Player": "player_name",
    "Unnamed: 3_level_0_Pos": "position",
    "Unnamed: 4_level_0_Squad": "club",
    "Unnamed: 5_level_0_Age": "age",
    "Playing Time_MP": "matches_played",
    "Playing Time_Starts": "starts",
    "Playing Time_Min": "minutes_played",
    "Playing Time_90s": "nineties",
    "Performance_Gls": "goals",
    "Performance_Ast": "assists",
    "Performance_G+A": "g_a",
    "Performance_G-PK": "goals_minus_pk",
    "Performance_PK": "penalties_scored",
    "Performance_PKatt": "penalties_attempted",
    "Performance_CrdY": "yellow_cards",
    "Performance_CrdR": "red_cards",
    "Per 90 Minutes_Gls": "goals_per90",
    "Per 90 Minutes_Ast": "assists_per90",
    "Per 90 Minutes_G+A": "g_a_per90",
    "Per 90 Minutes_G-PK": "goals_minus_pk_per90",
    "Per 90 Minutes_G+A-PK": "g_a_minus_pk_per90",
}


DROP_COLS = [
    "Unnamed: 0_level_0_Rk",
    "Unnamed: 2_level_0_Nation",
    "Unnamed: 6_level_0_Born",
    "Unnamed: 24_level_0_Matches",
]


NUMERIC_COLS = [
    "age",
    "matches_played",
    "starts",
    "minutes_played",
    "nineties",
    "goals",
    "assists",
    "g_a",
    "goals_minus_pk",
    "penalties_scored",
    "penalties_attempted",
    "yellow_cards",
    "red_cards",
    "goals_per90",
    "assists_per90",
    "g_a_per90",
    "goals_minus_pk_per90",
    "g_a_minus_pk_per90",
]


def parse_filename_metadata(filename: str) -> tuple[str, str]:
    pattern = r"(.+?)_(\d{4}-\d{4})_standard\.html"
    match = re.fullmatch(pattern, filename)

    if not match:
        raise ValueError(f"Cannot parse filename: {filename}")

    league_raw = match.group(1)
    season = match.group(2)

    if league_raw not in LEAGUE_MAP:
        raise ValueError(f"Unknown league in filename: {league_raw}")

    league = LEAGUE_MAP[league_raw]

    return league, season


def add_position_group(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()

    def map_position(pos: object) -> str:
        if pd.isna(pos):
            return "UNK"

        pos = str(pos)

        if "GK" in pos:
            return "GK"
        if any(p in pos for p in ["DF", "FB", "CB", "LB", "RB"]):
            return "DEF"
        if any(p in pos for p in ["MF", "DM", "CM", "AM"]):
            return "MID"
        if any(p in pos for p in ["FW", "LW", "RW"]):
            return "ATT"

        return "UNK"

    df["position_group"] = df["position"].apply(map_position)

    return df


def clean_fbref_table(df: pd.DataFrame, league: str, season: str) -> pd.DataFrame:
    df = df.copy()

    df = df.rename(columns=RENAME_MAP)

    df = df.drop(
        columns=[col for col in DROP_COLS if col in df.columns],
        errors="ignore",
    )

    if "player_name" not in df.columns:
        raise KeyError(f"`player_name` not found after renaming. Columns: {df.columns.tolist()}")

    if "club" not in df.columns:
        raise KeyError(f"`club` not found after renaming. Columns: {df.columns.tolist()}")

    df = df[df["player_name"].notna()].copy()
    df = df[df["player_name"] != "Player"].copy()
    df = df[df["club"].notna()].copy()

    df["league"] = league
    df["season"] = season
    df["season_start_year"] = df["season"].str[:4].astype(int)

    for col in NUMERIC_COLS:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")

    df = add_position_group(df)

    keep_cols = [
        "player_name",
        "club",
        "league",
        "season",
        "season_start_year",
        "position",
        "position_group",
        "age",
        "matches_played",
        "starts",
        "minutes_played",
        "nineties",
        "goals",
        "assists",
        "g_a",
        "goals_minus_pk",
        "penalties_scored",
        "penalties_attempted",
        "yellow_cards",
        "red_cards",
        "goals_per90",
        "assists_per90",
        "g_a_per90",
        "goals_minus_pk_per90",
        "g_a_minus_pk_per90",
    ]

    keep_cols = [col for col in keep_cols if col in df.columns]

    df = df[keep_cols].copy()

    return df


def build_fbref_features(output_path: str | Path = DEFAULT_OUTPUT_PATH) -> pd.DataFrame:
    output_path = Path(output_path)

    if not output_path.is_absolute():
        output_path = ROOT / output_path

    all_dfs = []

    html_files = sorted(RAW_PATH.glob("*.html"))

    if not html_files:
        raise FileNotFoundError(f"No HTML files found in {RAW_PATH}")

    for html_file in html_files:
        print(f"Processing: {html_file.relative_to(ROOT)}")

        league, season = parse_filename_metadata(html_file.name)

        raw_df = extract_fbref_player_table(html_file)

        clean_df = clean_fbref_table(
            df=raw_df,
            league=league,
            season=season,
        )

        all_dfs.append(clean_df)

    final_df = pd.concat(all_dfs, ignore_index=True)

    final_df = final_df.drop_duplicates(
        subset=[
            "player_name",
            "club",
            "league",
            "season",
        ]
    ).copy()

    output_path.parent.mkdir(parents=True, exist_ok=True)
    final_df.to_parquet(output_path, index=False)

    print("\nFBref feature build completed")
    print(f"Rows: {len(final_df):,}")
    print(f"Columns: {len(final_df.columns):,}")
    print(f"Output: {output_path}")

    print("\nSeasons:")
    print(final_df["season"].value_counts().sort_index())

    print("\nLeagues:")
    print(final_df["league"].value_counts())

    print("\nPosition groups:")
    print(final_df["position_group"].value_counts(dropna=False))

    print("\nLeague x Season coverage:")
    print(
        final_df.groupby(["league", "season"])
        .size()
        .sort_index()
        )--verbose

    return final_df


def main():
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--output",
        default="data/processed/fbref_features.parquet",
        help="Output path for processed FBref features.",
    )

    args = parser.parse_args()

    build_fbref_features(output_path=args.output)


if __name__ == "__main__":
    main()