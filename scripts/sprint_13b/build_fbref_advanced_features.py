from pathlib import Path
import re
import unicodedata

import numpy as np
import pandas as pd


RAW_DIR = Path("data/raw/fbref/sprint_13b/soccerdata")
PROCESSED_DIR = Path("data/processed")
REPORT_DIR = Path("reports/sprint_13b")

BASE_MODELING_PATH = PROCESSED_DIR / "player_season_modeling_v13a.parquet"
OUTPUT_PATH = PROCESSED_DIR / "player_season_modeling_v13b_advanced.parquet"
FEATURE_AUDIT_PATH = REPORT_DIR / "fbref_advanced_feature_engineering_audit.csv"

REPORT_DIR.mkdir(parents=True, exist_ok=True)


LEAGUE_MAP = {
    "ENG-Premier League": "Premier League",
    "ESP-La Liga": "LaLiga",
    "GER-Bundesliga": "Bundesliga",
    "ITA-Serie A": "Serie A",
    "FRA-Ligue 1": "Ligue 1",
    "NED-Eredivisie": "Eredivisie",
    "POR-Primeira Liga": "Liga Portugal",
    "ENG-Championship": "Championship",
    "BEL-Belgian Pro League": "Belgian Pro League",
    "AUT-Austrian Bundesliga": "Austrian Bundesliga",
    "ESP-Segunda División": "Spanish Segunda División",
}


def normalize_text(value: object) -> str:
    if pd.isna(value):
        return ""

    value = str(value).strip().lower()
    value = unicodedata.normalize("NFKD", value)
    value = "".join(c for c in value if not unicodedata.combining(c))
    value = re.sub(r"[^a-z0-9]+", " ", value)
    return re.sub(r"\s+", " ", value).strip()


def normalize_season(value: object) -> str:
    value = str(value)

    if re.fullmatch(r"\d{4}-\d{4}", value):
        return value

    if re.fullmatch(r"\d{4}", value):
        return f"20{value[:2]}-20{value[2:]}"

    if re.fullmatch(r"\d{2}\d{2}", value):
        return f"20{value[:2]}-20{value[2:]}"

    return value


def flatten_columns(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()

    if isinstance(df.columns, pd.MultiIndex):
        new_cols = []
        for col in df.columns:
            parts = [str(x) for x in col if str(x) not in ["", "nan", "None"]]
            new_cols.append("_".join(parts))
        df.columns = new_cols
    else:
        df.columns = [str(c) for c in df.columns]

    df.columns = (
        pd.Index(df.columns)
        .str.replace(" ", "_", regex=False)
        .str.replace("/", "_per_", regex=False)
        .str.replace("%", "_pct", regex=False)
        .str.replace("+", "_plus_", regex=False)
        .str.replace("-", "_minus_", regex=False)
        .str.replace(".", "", regex=False)
        .str.replace("__", "_", regex=False)
        .str.lower()
    )

    return df


def read_soccerdata_dataset(dataset: str) -> pd.DataFrame:
    frames = []

    for path in sorted((RAW_DIR / dataset).glob("*.parquet")):
        df = pd.read_parquet(path)

        if isinstance(df.index, pd.MultiIndex):
            df = df.reset_index()
        else:
            df = df.reset_index()

        df = flatten_columns(df)
        df["source_file"] = path.name
        df["advanced_dataset"] = dataset

        frames.append(df)

    if not frames:
        raise FileNotFoundError(f"No parquet files found for dataset={dataset}")

    out = pd.concat(frames, ignore_index=True)

    out["league"] = out["league"].map(LEAGUE_MAP).fillna(out["league"])
    out["season"] = out["season"].apply(normalize_season)

    out["player_name_normalized"] = out["player"].apply(normalize_text)
    out["club_normalized"] = out["team"].apply(normalize_text)

    return out


def select_existing(df: pd.DataFrame, columns: list[str]) -> list[str]:
    return [c for c in columns if c in df.columns]


def aggregate_advanced_features() -> pd.DataFrame:
    shooting = read_soccerdata_dataset("shooting")
    playing_time = read_soccerdata_dataset("playing_time")
    misc = read_soccerdata_dataset("misc")

    key_cols = ["league", "season", "player_name_normalized"]

    shooting_cols = {
        "standard_gls": "adv_goals",
        "standard_sh": "adv_shots",
        "standard_sot": "adv_shots_on_target",
        "standard_sh_per_90": "adv_shots_per90",
        "standard_sot_per_90": "adv_shots_on_target_per90",
    }

    playing_cols = {
        "playing_time_min": "adv_minutes",
        "starts_starts": "adv_starts",
        "starts_compl": "adv_complete_matches",
    }

    misc_cols = {
        "performance_int": "adv_interceptions",
        "performance_tklw": "adv_tackles_won",
    }

    shooting = shooting[key_cols + select_existing(shooting, list(shooting_cols))]
    playing_time = playing_time[key_cols + select_existing(playing_time, list(playing_cols))]
    misc = misc[key_cols + select_existing(misc, list(misc_cols))]

    shooting = shooting.rename(columns=shooting_cols)
    playing_time = playing_time.rename(columns=playing_cols)
    misc = misc.rename(columns=misc_cols)

    adv = (
        shooting
        .merge(playing_time, on=key_cols, how="outer")
        .merge(misc, on=key_cols, how="outer")
    )

    numeric_cols = [c for c in adv.columns if c.startswith("adv_")]

    for col in numeric_cols:
        adv[col] = pd.to_numeric(adv[col], errors="coerce")

    adv = (
        adv
        .groupby(key_cols, as_index=False)[numeric_cols]
        .sum(min_count=1)
    )

    return adv


def add_position_percentile(df: pd.DataFrame, value_col: str, pct_col: str) -> pd.DataFrame:
    df = df.copy()

    if value_col not in df.columns:
        df[pct_col] = np.nan
        return df

    group_cols = ["season", "league", "position_group"]

    df[pct_col] = (
        df
        .groupby(group_cols)[value_col]
        .rank(pct=True)
    )

    return df


def build_indices(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()

    percentile_specs = {
        "goals": "goals_position_pct",
        "adv_shots": "shots_position_pct",
        "adv_shots_on_target": "shots_on_target_position_pct",
        "adv_shots_per90": "shots_per90_position_pct",
        "adv_shots_on_target_per90": "shots_on_target_per90_position_pct",
        "adv_starts": "starts_position_pct",
        "minutes_played": "minutes_position_pct",
        "adv_complete_matches": "complete_matches_position_pct",
        "adv_interceptions": "interceptions_position_pct",
        "adv_tackles_won": "tackles_won_position_pct",
    }

    for value_col, pct_col in percentile_specs.items():
        df = add_position_percentile(df, value_col, pct_col)

    df["finishing_index_v2"] = (
        0.40 * df["goals_position_pct"]
        + 0.20 * df["shots_position_pct"]
        + 0.20 * df["shots_on_target_position_pct"]
        + 0.10 * df["shots_per90_position_pct"]
        + 0.10 * df["shots_on_target_per90_position_pct"]
    )

    df["availability_index"] = (
        0.40 * df["starts_position_pct"]
        + 0.30 * df["minutes_position_pct"]
        + 0.30 * df["complete_matches_position_pct"]
    )

    df["defensive_activity_index"] = (
        0.50 * df["interceptions_position_pct"]
        + 0.50 * df["tackles_won_position_pct"]
    )

    return df


def main() -> None:
    print("Loading base modeling dataset:", BASE_MODELING_PATH)
    base = pd.read_parquet(BASE_MODELING_PATH)

    PLAYER_COL_CANDIDATES = [
        "player_name",
        "player",
        "name",
        "Player",
        "player_name_fbref",
        "player_name_tm",
        "player_tm",
    ]

    player_col = next((c for c in PLAYER_COL_CANDIDATES if c in base.columns), None)

    if player_col is None:
        raise KeyError(
            "No player name column found in base dataset. "
            f"Available columns: {base.columns.tolist()}"
        )

    required_cols = ["league", "season", "position_group"]

    missing_required = [c for c in required_cols if c not in base.columns]

    if missing_required:
        raise KeyError(
            f"Missing required columns in base dataset: {missing_required}. "
            f"Available columns: {base.columns.tolist()}"
        )

    print(f"Using player column: {player_col}")

    base["player_name_normalized"] = base[player_col].apply(normalize_text)

    print("Building advanced feature table...")
    advanced = aggregate_advanced_features()

    print("Advanced rows:", len(advanced))
    print("Advanced columns:", advanced.columns.tolist())

    merge_keys = ["league", "season", "player_name_normalized"]

    before_rows = len(base)

    enriched = base.merge(
        advanced,
        on=merge_keys,
        how="left",
        validate="m:1",
    )

    after_rows = len(enriched)

    if before_rows != after_rows:
        raise RuntimeError(
            f"Row count changed after merge: before={before_rows}, after={after_rows}"
        )

    enriched = build_indices(enriched)

    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    enriched.to_parquet(OUTPUT_PATH, index=False)

    feature_cols = [
        "adv_shots",
        "adv_shots_on_target",
        "adv_shots_per90",
        "adv_shots_on_target_per90",
        "adv_starts",
        "adv_complete_matches",
        "adv_interceptions",
        "adv_tackles_won",
        "finishing_index_v2",
        "availability_index",
        "defensive_activity_index",
    ]

    audit_rows = []

    for col in feature_cols:
        if col not in enriched.columns:
            audit_rows.append({
                "feature": col,
                "exists": False,
                "non_null": 0,
                "coverage_pct": 0,
            })
            continue

        non_null = enriched[col].notna().sum()

        audit_rows.append({
            "feature": col,
            "exists": True,
            "non_null": int(non_null),
            "coverage_pct": round(non_null / len(enriched), 4),
        })

    audit = pd.DataFrame(audit_rows)
    audit.to_csv(FEATURE_AUDIT_PATH, index=False, encoding="utf-8-sig")

    print("\nSaved:")
    print(OUTPUT_PATH)
    print(FEATURE_AUDIT_PATH)

    print("\nFeature audit:")
    print(audit)


if __name__ == "__main__":
    main()