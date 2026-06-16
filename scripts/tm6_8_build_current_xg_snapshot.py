import asyncio
import json
import re
import unicodedata
from datetime import date
from pathlib import Path

import aiohttp
import numpy as np
import pandas as pd
from understat import Understat


ROOT = Path(__file__).resolve().parents[1]

PROCESSED = ROOT / "data" / "processed"
REPORTS = ROOT / "reports" / "data_quality"

PROCESSED.mkdir(parents=True, exist_ok=True)
REPORTS.mkdir(parents=True, exist_ok=True)

SNAPSHOT_VERSION = "v1.0.0"
SEASON_START_YEAR = 2025
SEASON_LABEL = "2025-2026"

LEAGUES = {
    "EPL": "Premier League",
    "La liga": "LaLiga",
    "Bundesliga": "Bundesliga",
    "Serie A": "Serie A",
    "Ligue 1": "Ligue 1",
}


def normalize_name(value: str) -> str:
    if pd.isna(value):
        return ""

    value = str(value).strip().lower()

    value = unicodedata.normalize("NFKD", value)
    value = "".join(
        c for c in value
        if not unicodedata.combining(c)
    )

    value = re.sub(r"[^a-z0-9\s-]", " ", value)
    value = re.sub(r"\s+", " ", value).strip()

    return value


def safe_numeric(series):
    return pd.to_numeric(series, errors="coerce")


def per90(numerator, minutes):
    return np.where(
        minutes > 0,
        numerator / minutes * 90,
        np.nan
    )


async def fetch_current_understat():
    dfs = []

    async with aiohttp.ClientSession() as session:
        understat = Understat(session)

        for league_key, league_name in LEAGUES.items():
            print(f"Loading {league_name}...")

            players = await understat.get_league_players(
                league_key,
                SEASON_START_YEAR
            )

            df = pd.DataFrame(players)
            df["league"] = league_name
            df["league_key"] = league_key

            dfs.append(df)

    return pd.concat(dfs, ignore_index=True)


def build_snapshot(raw: pd.DataFrame) -> pd.DataFrame:
    df = raw.copy()

    numeric_cols = [
        "games",
        "time",
        "goals",
        "assists",
        "shots",
        "key_passes",
        "xG",
        "xA",
        "npg",
        "npxG",
        "xGChain",
        "xGBuildup",
        "yellow_cards",
        "red_cards",
    ]

    for col in numeric_cols:
        if col in df.columns:
            df[col] = safe_numeric(df[col])

    out = pd.DataFrame()

    out["understat_player_id"] = df["id"].astype(str)
    out["player_id_tm"] = pd.NA

    out["player_name"] = df["player_name"]
    out["player_name_norm"] = df["player_name"].apply(normalize_name)

    out["season"] = SEASON_LABEL
    out["season_start_year"] = SEASON_START_YEAR

    out["team"] = df["team_title"]
    out["league"] = df["league"]
    out["league_key"] = df["league_key"]
    out["position"] = df["position"]

    out["current_games"] = df["games"]
    out["current_minutes"] = df["time"]
    out["current_goals"] = df["goals"]
    out["current_assists"] = df["assists"]
    out["current_shots"] = df["shots"]
    out["current_key_passes"] = df["key_passes"]

    out["current_npg"] = df["npg"]
    out["current_xg"] = df["xG"]
    out["current_xa"] = df["xA"]
    out["current_npxg"] = df["npxG"]
    out["current_xgchain"] = df["xGChain"]
    out["current_xgbuildup"] = df["xGBuildup"]

    minutes = out["current_minutes"]

    out["current_xg_per90"] = per90(out["current_xg"], minutes)
    out["current_xa_per90"] = per90(out["current_xa"], minutes)
    out["current_npxg_per90"] = per90(out["current_npxg"], minutes)
    out["current_shots_per90"] = per90(out["current_shots"], minutes)
    out["current_key_passes_per90"] = per90(
        out["current_key_passes"],
        minutes
    )

    out["current_expected_contribution"] = (
        out["current_xg"] +
        out["current_xa"]
    )

    out["current_expected_contribution_per90"] = per90(
        out["current_expected_contribution"],
        minutes
    )

    out["current_goals_minus_xg"] = (
        out["current_goals"] -
        out["current_xg"]
    )

    out["current_goals_minus_npxg"] = (
        out["current_npg"] -
        out["current_npxg"]
    )

    out["current_assists_minus_xa"] = (
        out["current_assists"] -
        out["current_xa"]
    )

    out["current_shot_quality"] = np.where(
        out["current_shots"] > 0,
        out["current_xg"] / out["current_shots"],
        np.nan
    )

    out["current_attacking_involvement"] = out["current_xgchain"]
    out["current_buildup_involvement"] = out["current_xgbuildup"]

    out["snapshot_date"] = str(date.today())
    out["source"] = "understat"
    out["snapshot_version"] = SNAPSHOT_VERSION

    preferred_cols = [
        "understat_player_id",
        "player_id_tm",
        "player_name",
        "player_name_norm",
        "season",
        "season_start_year",
        "team",
        "league",
        "league_key",
        "position",
        "current_games",
        "current_minutes",
        "current_goals",
        "current_assists",
        "current_shots",
        "current_key_passes",
        "current_npg",
        "current_xg",
        "current_xa",
        "current_npxg",
        "current_xgchain",
        "current_xgbuildup",
        "current_xg_per90",
        "current_xa_per90",
        "current_npxg_per90",
        "current_shots_per90",
        "current_key_passes_per90",
        "current_expected_contribution",
        "current_expected_contribution_per90",
        "current_goals_minus_xg",
        "current_goals_minus_npxg",
        "current_assists_minus_xa",
        "current_shot_quality",
        "current_attacking_involvement",
        "current_buildup_involvement",
        "snapshot_date",
        "source",
        "snapshot_version",
    ]

    return out[preferred_cols]


def build_metadata(snapshot: pd.DataFrame) -> dict:
    return {
        "snapshot_name": "current_xg_snapshot",
        "snapshot_version": SNAPSHOT_VERSION,
        "snapshot_date": str(date.today()),
        "source": "understat",
        "season": SEASON_LABEL,
        "season_start_year": SEASON_START_YEAR,
        "players_total": int(len(snapshot)),
        "players_unique_understat_id": int(
            snapshot["understat_player_id"].nunique()
        ),
        "leagues_total": int(snapshot["league"].nunique()),
        "leagues": sorted(snapshot["league"].unique().tolist()),
        "features": snapshot.columns.tolist(),
        "governance_note": (
            "Current xG snapshot generated from Understat. "
            "This artifact is a current performance layer and must not be used "
            "to retrain historical market value models without temporal validation."
        ),
    }


async def main():
    raw = await fetch_current_understat()

    snapshot = build_snapshot(raw)

    snapshot_path = PROCESSED / "current_xg_snapshot.parquet"
    metadata_path = PROCESSED / "current_xg_snapshot_metadata.json"

    snapshot.to_parquet(snapshot_path, index=False)

    metadata = build_metadata(snapshot)

    metadata_path.write_text(
        json.dumps(metadata, indent=2, ensure_ascii=False),
        encoding="utf-8"
    )

    print("\nSaved:")
    print(snapshot_path)
    print(metadata_path)

    print("\nSnapshot summary:")
    print(f"Rows: {len(snapshot):,}")
    print(f"Players: {snapshot['understat_player_id'].nunique():,}")
    print(f"Leagues: {snapshot['league'].nunique()}")
    print(f"Season: {SEASON_LABEL}")

    print("\nLeague distribution:")
    print(snapshot["league"].value_counts())


if __name__ == "__main__":
    asyncio.run(main())