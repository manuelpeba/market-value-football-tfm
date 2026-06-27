from __future__ import annotations

import argparse
import json
import re
import unicodedata
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]

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


def first_available(df: pd.DataFrame, candidates: list[str]) -> pd.Series:
    out = pd.Series(pd.NA, index=df.index, dtype="object")
    for col in candidates:
        if col in df.columns:
            out = out.fillna(df[col])
    return out


def resolve_input_path(input_path: str | Path) -> Path:
    path = Path(input_path)
    if not path.is_absolute():
        path = ROOT / path
    if not path.exists():
        raise FileNotFoundError(f"Transfermarkt features file not found: {path}")
    return path


def build_snapshot(input_path: str | Path, scope: str = "productive") -> pd.DataFrame:
    input_path = resolve_input_path(input_path)
    tm = pd.read_parquet(input_path).copy()

    required = [
        "player_id_tm",
        "market_value_eur",
        "valuation_date",
    ]
    missing = [c for c in required if c not in tm.columns]
    if missing:
        raise ValueError(f"Missing required columns in {input_path}: {missing}")

    tm["current_valuation_date"] = pd.to_datetime(tm["valuation_date"], errors="coerce")
    tm["current_market_value_eur"] = pd.to_numeric(tm["market_value_eur"], errors="coerce")

    tm = tm[tm["player_id_tm"].notna()].copy()
    tm = tm[tm["current_valuation_date"].notna()].copy()
    tm = tm[tm["current_market_value_eur"].notna()].copy()
    tm = tm[tm["current_market_value_eur"] > 0].copy()

    latest = (
        tm.sort_values(
            ["player_id_tm", "current_valuation_date", "current_market_value_eur"],
            ascending=[True, False, False],
        )
        .drop_duplicates("player_id_tm", keep="first")
        .copy()
    )

    latest["player_name_tm"] = first_available(latest, ["player_name_tm", "name", "player_name"])
    latest["player_name_tm"] = latest["player_name_tm"].astype("string")
    latest["player_name_norm"] = latest["player_name_tm"].map(normalize_key)

    latest["current_club"] = first_available(
        latest,
        [
            "current_club_name_tm",
            "current_club_name",
            "current_club",
            "club",
            "season_context_club",
        ],
    )

    latest["current_club_id"] = first_available(
        latest,
        [
            "current_club_id_tm",
            "current_club_id",
            "club_id",
        ],
    )

    latest["current_competition_id"] = first_available(
        latest,
        [
            "competition_id_tm",
            "current_club_domestic_competition_id",
            "player_club_domestic_competition_id",
            "current_competition_id",
        ],
    )

    latest["current_league"] = latest["current_competition_id"].map(COMPETITION_TO_LEAGUE)
    if "current_league" in tm.columns:
        latest["current_league"] = latest["current_league"].fillna(latest["current_league"])

    latest["current_season"] = latest["current_valuation_date"].apply(season_from_date)

    if "date_of_birth" in latest.columns:
        latest["current_age"] = calculate_age(latest["date_of_birth"], latest["current_valuation_date"])
    else:
        latest["current_age"] = pd.to_numeric(first_available(latest, ["age_tm", "age"]), errors="coerce")

    latest["current_position"] = first_available(latest, ["position", "sub_position"])
    latest["current_position_group"] = first_available(latest, ["position_group", "position_group_tm"])
    latest["nationality"] = first_available(latest, ["nationality", "country_of_citizenship"])
    latest["current_club_norm"] = latest["current_club"].map(normalize_key)

    homonym_counts = latest.groupby("player_name_norm", dropna=False)["player_id_tm"].transform("nunique")
    latest["homonym_group_size"] = homonym_counts.astype("Int64")
    latest["is_homonym_name"] = latest["homonym_group_size"].fillna(0).astype(int) > 1
    latest["identity_resolution_status"] = np.where(
        latest["is_homonym_name"],
        "PLAYER_ID_REQUIRED_HOMONYM",
        "UNIQUE_NAME_FALLBACK_ALLOWED",
    )

    latest["identity_primary_key"] = "player_id_tm"
    latest["snapshot_source"] = "transfermarkt_features_v13a_latest_valuation"
    latest["identity_quality_status"] = "OK"

    critical = [
        "player_id_tm",
        "player_name_tm",
        "current_club",
        "current_league",
        "current_market_value_eur",
        "current_valuation_date",
        "current_age",
    ]
    for col in critical:
        bad = latest[col].isna() | (latest[col].astype(str).str.strip() == "")
        latest.loc[bad, "identity_quality_status"] = "INCOMPLETE"

    out_cols = [
        "player_id_tm",
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
        "nationality",
        "current_position",
        "current_position_group",
        "sub_position",
        "foot",
        "height_in_cm",
        "homonym_group_size",
        "is_homonym_name",
        "identity_resolution_status",
        "identity_primary_key",
        "snapshot_source",
        "identity_quality_status",
    ]
    out_cols = [c for c in out_cols if c in latest.columns]
    snapshot = latest[out_cols].copy()

    if scope == "productive":
        snapshot = snapshot[snapshot["current_league"].isin(PRODUCTIVE_LEAGUES)].copy()
    elif scope != "full":
        raise ValueError("scope must be 'productive' or 'full'")

    snapshot["current_market_value_eur"] = snapshot["current_market_value_eur"].round().astype("Int64")

    return snapshot.sort_values(
        ["current_league", "current_market_value_eur"],
        ascending=[True, False],
    ).reset_index(drop=True)


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
        "missing_current_club": int(snapshot["current_club"].isna().sum()),
        "missing_current_age": int(snapshot["current_age"].isna().sum()),
        "missing_current_position": int(snapshot.get("current_position", pd.Series(index=snapshot.index)).isna().sum()),
        "identity_ok_pct": round(float(snapshot["identity_quality_status"].eq("OK").mean() * 100), 2),
        "homonym_names": int(snapshot.loc[snapshot["is_homonym_name"], "player_name_norm"].nunique()),
        "leagues": sorted(snapshot["current_league"].dropna().unique().tolist()),
        "snapshot_source": "transfermarkt_features_v13a_latest_valuation",
    }

    audit_path.write_text(json.dumps(audit, indent=2, ensure_ascii=False), encoding="utf-8")

    homonyms = snapshot[snapshot["is_homonym_name"]].copy()
    if not homonyms.empty:
        homonyms.to_csv(homonyms_path, index=False, encoding="utf-8")

    print("=" * 100)
    print("CURRENT PLAYER SNAPSHOT BUILD — SNAPSHOT AUTHORITY")
    print("=" * 100)
    print(json.dumps(audit, indent=2, ensure_ascii=False))
    print(f"\n[OK] CSV:     {csv_path}")
    print(f"[OK] Parquet: {parquet_path}")
    print(f"[OK] Audit:   {audit_path}")
    if not homonyms.empty:
        print(f"[REVIEW] Homonyms: {homonyms_path}")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", default="data/processed/transfermarkt_features_v13a.parquet")
    parser.add_argument("--output-dir", default="data/processed")
    parser.add_argument("--scope", default="productive", choices=["productive", "full"])
    args = parser.parse_args()

    snapshot = build_snapshot(args.input, scope=args.scope)
    write_outputs(snapshot, args.output_dir)


if __name__ == "__main__":
    main()
