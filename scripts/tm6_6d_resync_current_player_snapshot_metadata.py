import json
from datetime import date, datetime, timezone
from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]

SNAPSHOT_PATH = ROOT / "data" / "processed" / "current_player_snapshot.parquet"
METADATA_PATH = ROOT / "data" / "processed" / "current_player_snapshot_metadata.json"
HEALTH_PATH = ROOT / "reports" / "data_quality" / "snapshot_health_report.json"


def load_json(path: Path) -> dict:
    if not path.exists():
        return {}
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")


def main():
    df = pd.read_parquet(SNAPSHOT_PATH)

    metadata = load_json(METADATA_PATH)
    health = load_json(HEALTH_PATH)

    valuation_col = "current_valuation_date"
    league_col = "current_league"
    value_col = "current_market_value_eur"

    latest_valuation = (
        pd.to_datetime(df[valuation_col], errors="coerce").max().date().isoformat()
        if valuation_col in df.columns
        else None
    )

    leagues = (
        sorted(df[league_col].dropna().astype(str).unique().tolist())
        if league_col in df.columns
        else []
    )

    market_value_min = (
        int(pd.to_numeric(df[value_col], errors="coerce").min())
        if value_col in df.columns
        else None
    )

    market_value_max = (
        int(pd.to_numeric(df[value_col], errors="coerce").max())
        if value_col in df.columns
        else None
    )

    homonym_names = (
        int(df.loc[df.get("is_homonym_name", False) == True, "player_name_norm"].nunique())
        if "is_homonym_name" in df.columns and "player_name_norm" in df.columns
        else metadata.get("homonym_names")
    )

    metadata.update(
        {
            "snapshot_version": metadata.get("snapshot_version", "v1.0.0"),
            "snapshot_date": metadata.get("snapshot_date", str(date.today())),
            "generated_at_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
            "source": metadata.get("source", "transfermarkt_features_v13a"),
            "snapshot_path": "data\\processed\\current_player_snapshot.parquet",
            "latest_valuation_date": latest_valuation,
            "players_total": int(df["player_id_tm"].nunique()) if "player_id_tm" in df.columns else int(len(df)),
            "leagues_total": int(len(leagues)),
            "leagues": leagues,
            "market_value_min": market_value_min,
            "market_value_max": market_value_max,
            "homonym_names": homonym_names,
            "match_key": metadata.get("match_key", "player_id_tm"),
            "fallback_match_key": metadata.get("fallback_match_key", "player_name_norm_unique_only"),
            "governance_note": metadata.get(
                "governance_note",
                "Historical player-season values remain unchanged. Current club, league and market value are provided by current_player_snapshot and should be interpreted as current market context.",
            ),
        }
    )

    if health:
        freshness = health.get("freshness", {})
        freshness["latest_valuation_date"] = latest_valuation
        freshness["valuation_age_days"] = (
            (date.today() - datetime.strptime(latest_valuation, "%Y-%m-%d").date()).days
            if latest_valuation
            else None
        )
        health["freshness"] = freshness

        health["players_total"] = metadata["players_total"]
        health["leagues_total"] = metadata["leagues_total"]
        health["latest_valuation_date"] = latest_valuation
        health["metadata_resynced_at_utc"] = metadata["generated_at_utc"]

    write_json(METADATA_PATH, metadata)
    write_json(HEALTH_PATH, health)

    print("\nTM.6.6D Metadata Resynchronization")
    print("===================================")
    print(f"Snapshot rows: {len(df):,}")
    print(f"Players total: {metadata['players_total']:,}")
    print(f"Leagues total: {metadata['leagues_total']}")
    print(f"Latest valuation date: {metadata['latest_valuation_date']}")
    print(f"Homonym names: {metadata['homonym_names']}")
    print("\nUpdated:")
    print(METADATA_PATH)
    print(HEALTH_PATH)


if __name__ == "__main__":
    main()