from __future__ import annotations

import argparse
import json
import re
import unicodedata
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2] if "src" in Path(__file__).resolve().parts else Path.cwd()

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
    return re.sub(r"\s+", " ", text).strip()


def first_existing(df: pd.DataFrame, candidates: list[str]) -> str | None:
    for c in candidates:
        if c in df.columns:
            return c
    return None


def value_series(df: pd.DataFrame, candidates: list[str], default: object = np.nan) -> pd.Series:
    c = first_existing(df, candidates)
    if c is None:
        return pd.Series(default, index=df.index)
    return df[c]


def season_from_date(date: pd.Timestamp) -> object:
    if pd.isna(date):
        return pd.NA
    y = int(date.year)
    return f"{y}-{y + 1}" if int(date.month) >= 7 else f"{y - 1}-{y}"


def build_from_features(features_path: Path, scope: str = "productive") -> pd.DataFrame:
    if not features_path.exists():
        raise FileNotFoundError(features_path)
    df = pd.read_parquet(features_path)

    player_id_col = first_existing(df, ["player_id_tm", "player_id"])
    if player_id_col is None:
        raise ValueError("No player id column found. Expected player_id_tm or player_id.")

    date_col = first_existing(df, [
        "current_valuation_date", "valuation_date", "date", "market_value_date", "last_season_date"
    ])
    value_col = first_existing(df, ["current_market_value_eur", "market_value_eur", "market_value_in_eur"])
    if date_col is None or value_col is None:
        raise ValueError(f"Required date/value columns not found. date_col={date_col}, value_col={value_col}")

    work = df.copy()
    work["current_valuation_date"] = pd.to_datetime(work[date_col], errors="coerce")
    work["current_market_value_eur"] = pd.to_numeric(work[value_col], errors="coerce")
    work = work[work[player_id_col].notna()].copy()
    work = work[work["current_valuation_date"].notna()].copy()
    work = work[work["current_market_value_eur"].notna() & (work["current_market_value_eur"] > 0)].copy()

    latest = (
        work.sort_values([player_id_col, "current_valuation_date"], ascending=[True, False])
        .drop_duplicates(player_id_col, keep="first")
        .copy()
    )

    latest["player_id_tm"] = latest[player_id_col]
    latest["player_name_tm"] = value_series(latest, ["player_name_tm", "name", "player_name", "pretty_name"])
    latest["player_name_norm"] = value_series(latest, ["player_name_norm", "player_name_normalized", "name_norm"])
    latest["player_name_norm"] = latest["player_name_norm"].where(
        latest["player_name_norm"].notna(), latest["player_name_tm"].map(normalize_key)
    )

    latest["current_club"] = value_series(latest, [
        "current_club", "current_club_name", "club", "team", "squad", "season_context_club"
    ])
    latest["current_club_id"] = value_series(latest, ["current_club_id", "current_club_id_tm", "club_id", "current_club_id_valuation"])
    latest["current_competition_id"] = value_series(latest, [
        "current_competition_id", "competition_id_tm", "player_club_domestic_competition_id", "current_club_domestic_competition_id"
    ])
    latest["current_league"] = value_series(latest, ["current_league", "league"])
    latest["current_league"] = latest["current_league"].where(
        latest["current_league"].notna(), latest["current_competition_id"].map(COMPETITION_TO_LEAGUE)
    )
    latest["current_season"] = latest["current_valuation_date"].apply(season_from_date)
    latest["current_club_norm"] = latest["current_club"].map(normalize_key)

    latest["date_of_birth"] = value_series(latest, ["date_of_birth", "dob"])
    latest["country_of_citizenship"] = value_series(latest, ["country_of_citizenship", "nationality", "nation"])
    latest["position"] = value_series(latest, ["position", "pos", "pos_"])
    latest["sub_position"] = value_series(latest, ["sub_position"])
    latest["foot"] = value_series(latest, ["foot"])
    latest["height_in_cm"] = value_series(latest, ["height_in_cm", "height"])
    latest["current_age"] = value_series(latest, ["current_age", "age", "age_"])

    homonym_counts = latest.groupby("player_name_norm", dropna=False)["player_id_tm"].transform("nunique")
    latest["homonym_group_size"] = homonym_counts.astype("Int64")
    latest["is_homonym_name"] = latest["homonym_group_size"].fillna(0).astype(int) > 1
    latest["identity_resolution_status"] = np.where(
        latest["is_homonym_name"], "PLAYER_ID_REQUIRED_HOMONYM", "UNIQUE_NAME_FALLBACK_ALLOWED"
    )
    latest["identity_primary_key"] = "player_id_tm"
    latest["snapshot_source"] = "transfermarkt_features_v13a_latest_valuation_restore"

    if scope == "productive":
        latest = latest[latest["current_league"].isin(PRODUCTIVE_LEAGUES)].copy()
    elif scope != "full":
        raise ValueError("scope must be productive or full")

    out_cols = [
        "player_id_tm", "player_name_tm", "player_name_norm", "current_club", "current_club_norm",
        "current_club_id", "current_competition_id", "current_league", "current_season",
        "current_market_value_eur", "current_valuation_date", "current_age", "date_of_birth",
        "country_of_citizenship", "position", "sub_position", "foot", "height_in_cm",
        "homonym_group_size", "is_homonym_name", "identity_resolution_status", "identity_primary_key",
        "snapshot_source",
    ]
    out_cols = [c for c in out_cols if c in latest.columns]
    latest = latest[out_cols].copy()
    latest["current_market_value_eur"] = pd.to_numeric(latest["current_market_value_eur"], errors="coerce").astype("Int64")
    return latest.sort_values(["current_league", "current_market_value_eur"], ascending=[True, False]).reset_index(drop=True)


def write_outputs(snapshot: pd.DataFrame, output_dir: Path) -> dict:
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
    return audit


def main() -> None:
    parser = argparse.ArgumentParser(description="Restore current_player_snapshot from transfermarkt_features_v13a.parquet")
    parser.add_argument("--features", default="data/processed/transfermarkt_features_v13a.parquet")
    parser.add_argument("--output-dir", default="data/processed")
    parser.add_argument("--scope", choices=["productive", "full"], default="productive")
    parser.add_argument("--expect-players", type=int, default=17510)
    parser.add_argument("--expect-latest-date", default="2026-03-27")
    parser.add_argument("--strict", action="store_true")
    args = parser.parse_args()

    features = ROOT / args.features
    output_dir = ROOT / args.output_dir
    snapshot = build_from_features(features, args.scope)
    audit = write_outputs(snapshot, output_dir)

    print("=" * 100)
    print("RESTORE CURRENT PLAYER SNAPSHOT FROM V13A FEATURES")
    print("=" * 100)
    print(json.dumps(audit, indent=2, ensure_ascii=False))

    problems = []
    if args.expect_players and int(audit["players_unique"]) != int(args.expect_players):
        problems.append(f"players_unique expected {args.expect_players}, got {audit['players_unique']}")
    if args.expect_latest_date and str(audit["current_valuation_date_max"]) != str(args.expect_latest_date):
        problems.append(f"latest date expected {args.expect_latest_date}, got {audit['current_valuation_date_max']}")

    if problems:
        print("\n[REVIEW] Restore completed but did not match expected baseline exactly:")
        for p in problems:
            print(f"- {p}")
        if args.strict:
            raise SystemExit(1)
    else:
        print("\n[OK] Restored snapshot matches approved baseline expectations.")


if __name__ == "__main__":
    main()
