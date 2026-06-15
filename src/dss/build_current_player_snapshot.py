from __future__ import annotations

import argparse
import json
import re
import unicodedata
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2] if "src" in Path(__file__).parts else Path.cwd()

COMPETITION_TO_LEAGUE = {
    "GB1": "Premier League",
    "ES1": "LaLiga",
    "L1": "Bundesliga",
    "IT1": "Serie A",
    "FR1": "Ligue 1",
    "NL1": "Eredivisie",
    "PO1": "Liga Portugal",
    "BE1": "Belgian Pro League",
    "A1": "Austrian Bundesliga",
}

PRODUCTIVE_LEAGUES = set(COMPETITION_TO_LEAGUE.values())


def normalize_key(value: object) -> str:
    if pd.isna(value):
        return ""
    text = str(value).strip().lower()
    text = unicodedata.normalize("NFKD", text)
    text = "".join(ch for ch in text if not unicodedata.combining(ch))
    text = re.sub(r"[^a-z0-9 ]+", " ", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text


def season_from_date(date: pd.Timestamp) -> str | pd.NA:
    if pd.isna(date):
        return pd.NA
    year = int(date.year)
    return f"{year}-{year + 1}" if int(date.month) >= 7 else f"{year - 1}-{year}"


def calculate_age(date_of_birth: pd.Series, ref_date: pd.Series) -> pd.Series:
    dob = pd.to_datetime(date_of_birth, errors="coerce")
    ref = pd.to_datetime(ref_date, errors="coerce")
    return ((ref - dob).dt.days / 365.25).round(2)


def resolve_tm_raw_dir(raw_dir: str | Path) -> Path:
    raw_dir = Path(raw_dir)
    if not raw_dir.is_absolute():
        raw_dir = ROOT / raw_dir
    if not raw_dir.exists():
        raise FileNotFoundError(f"Transfermarkt raw directory not found: {raw_dir}")
    for required in ["players.csv", "player_valuations.csv"]:
        if not (raw_dir / required).exists():
            raise FileNotFoundError(f"Missing {required} in {raw_dir}")
    return raw_dir


def build_snapshot(raw_dir: str | Path, scope: str = "productive") -> pd.DataFrame:
    raw_dir = resolve_tm_raw_dir(raw_dir)
    players = pd.read_csv(raw_dir / "players.csv")
    valuations = pd.read_csv(raw_dir / "player_valuations.csv")

    valuations = valuations.copy()
    valuations["current_valuation_date"] = pd.to_datetime(valuations["date"], errors="coerce")
    valuations = valuations[valuations["current_valuation_date"].notna()].copy()
    valuations = valuations[valuations["market_value_in_eur"].notna()].copy()
    valuations = valuations[valuations["market_value_in_eur"] > 0].copy()

    latest_val = (
        valuations.sort_values(["player_id", "current_valuation_date"], ascending=[True, False])
        .drop_duplicates("player_id", keep="first")
        .copy()
    )

    keep_player_cols = [
        "player_id",
        "name",
        "date_of_birth",
        "country_of_citizenship",
        "position",
        "sub_position",
        "foot",
        "height_in_cm",
        "current_club_id",
        "current_club_name",
        "current_club_domestic_competition_id",
    ]
    keep_player_cols = [c for c in keep_player_cols if c in players.columns]
    players = players[keep_player_cols].copy()

    snap = latest_val.merge(players, on="player_id", how="left", suffixes=("_valuation", "_player"))

    # Prefer valuation-time club/competition, because it reflects the club at the latest value date.
    snap["current_club"] = snap.get("current_club_name_valuation", pd.Series(index=snap.index, dtype="object"))
    snap["current_club"] = snap["current_club"].fillna(snap.get("current_club_name_player", pd.Series(index=snap.index, dtype="object")))

    snap["current_club_id"] = snap.get("current_club_id_valuation", pd.Series(index=snap.index, dtype="object"))
    snap["current_club_id"] = snap["current_club_id"].fillna(snap.get("current_club_id_player", pd.Series(index=snap.index, dtype="object")))

    snap["current_competition_id"] = snap.get(
        "player_club_domestic_competition_id", pd.Series(index=snap.index, dtype="object")
    )
    if "current_club_domestic_competition_id" in snap.columns:
        snap["current_competition_id"] = snap["current_competition_id"].fillna(
            snap["current_club_domestic_competition_id"]
        )

    snap["current_league"] = snap["current_competition_id"].map(COMPETITION_TO_LEAGUE)
    snap["current_market_value_eur"] = snap["market_value_in_eur"].astype("Int64")
    snap["current_season"] = snap["current_valuation_date"].apply(season_from_date)

    if "date_of_birth" in snap.columns:
        snap["current_age"] = calculate_age(snap["date_of_birth"], snap["current_valuation_date"])
    else:
        snap["current_age"] = np.nan

    snap["player_name_tm"] = snap["name"].astype("string")
    snap["player_name_norm"] = snap["player_name_tm"].map(normalize_key)
    snap["current_club_norm"] = snap["current_club"].map(normalize_key)

    homonym_counts = snap.groupby("player_name_norm", dropna=False)["player_id"].transform("nunique")
    snap["homonym_group_size"] = homonym_counts.astype("Int64")
    snap["is_homonym_name"] = snap["homonym_group_size"].fillna(0).astype(int) > 1
    snap["identity_resolution_status"] = np.where(
        snap["is_homonym_name"],
        "PLAYER_ID_REQUIRED_HOMONYM",
        "UNIQUE_NAME_FALLBACK_ALLOWED",
    )
    snap["identity_primary_key"] = "player_id_tm"
    snap["snapshot_source"] = "transfermarkt_kaggle_player_scores_latest_valuation"

    out_cols = [
        "player_id",
        "player_name_tm",
        "player_name_norm",
        "current_club",
        "current_club_norm",
        "current_club_id",
        "current_competition_id",
        "current_league",
        "current_season",
        "current_market_value_eur",
        "current_valuation_date",
        "current_age",
        "date_of_birth",
        "country_of_citizenship",
        "position",
        "sub_position",
        "foot",
        "height_in_cm",
        "homonym_group_size",
        "is_homonym_name",
        "identity_resolution_status",
        "identity_primary_key",
        "snapshot_source",
    ]
    out_cols = [c for c in out_cols if c in snap.columns]
    snap = snap[out_cols].copy().rename(columns={"player_id": "player_id_tm"})

    if scope == "productive":
        snap = snap[snap["current_league"].isin(PRODUCTIVE_LEAGUES)].copy()
    elif scope != "full":
        raise ValueError("scope must be 'productive' or 'full'")

    return snap.sort_values(["current_league", "current_market_value_eur"], ascending=[True, False]).reset_index(drop=True)


def write_outputs(snapshot: pd.DataFrame, output_dir: str | Path) -> None:
    output_dir = Path(output_dir)
    if not output_dir.is_absolute():
        output_dir = ROOT / output_dir
    output_dir.mkdir(parents=True, exist_ok=True)

    csv_path = output_dir / "current_player_snapshot.csv"
    parquet_path = output_dir / "current_player_snapshot.parquet"
    audit_path = output_dir / "current_player_snapshot_audit.json"
    homonyms_path = output_dir / "current_player_snapshot_homonyms.csv"

    snapshot.to_csv(csv_path, index=False, encoding="utf-8")
    snapshot.to_parquet(parquet_path, index=False)

    audit = {
        "rows": int(len(snapshot)),
        "players_unique": int(snapshot["player_id_tm"].nunique()),
        "leagues_unique": int(snapshot["current_league"].nunique(dropna=True)),
        "current_valuation_date_min": str(pd.to_datetime(snapshot["current_valuation_date"]).min().date()),
        "current_valuation_date_max": str(pd.to_datetime(snapshot["current_valuation_date"]).max().date()),
        "market_value_min": int(snapshot["current_market_value_eur"].min()),
        "market_value_max": int(snapshot["current_market_value_eur"].max()),
        "homonym_names": int(snapshot.loc[snapshot["is_homonym_name"], "player_name_norm"].nunique()),
        "leagues": sorted(snapshot["current_league"].dropna().unique().tolist()),
    }
    audit_path.write_text(json.dumps(audit, indent=2, ensure_ascii=False), encoding="utf-8")

    homonyms = snapshot[snapshot["is_homonym_name"]].copy()
    if not homonyms.empty:
        homonyms.to_csv(homonyms_path, index=False, encoding="utf-8")

    print("=" * 100)
    print("CURRENT PLAYER SNAPSHOT BUILD")
    print("=" * 100)
    print(json.dumps(audit, indent=2, ensure_ascii=False))
    print(f"\n[OK] CSV:     {csv_path}")
    print(f"[OK] Parquet: {parquet_path}")
    print(f"[OK] Audit:   {audit_path}")
    if not homonyms.empty:
        print(f"[REVIEW] Homonyms: {homonyms_path}")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--raw-dir", default="data/raw/transfermarkt/kaggle_player_scores")
    parser.add_argument("--output-dir", default="data/processed")
    parser.add_argument("--scope", choices=["productive", "full"], default="productive")
    args = parser.parse_args()

    snapshot = build_snapshot(args.raw_dir, args.scope)
    write_outputs(snapshot, args.output_dir)


if __name__ == "__main__":
    main()
