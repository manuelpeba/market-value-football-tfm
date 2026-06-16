import json
from datetime import date, datetime
from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]

SNAPSHOT_PATH = ROOT / "data" / "processed" / "current_player_snapshot.parquet"
METADATA_PATH = ROOT / "data" / "processed" / "current_player_snapshot_metadata.json"
HEALTH_PATH = ROOT / "reports" / "data_quality" / "snapshot_health_report.json"


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8")) if path.exists() else {}


def write_json(path: Path, payload: dict) -> None:
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")


def main():
    df = pd.read_parquet(SNAPSHOT_PATH)
    metadata = load_json(METADATA_PATH)
    health = load_json(HEALTH_PATH)

    latest_valuation_date = pd.to_datetime(
        df["current_valuation_date"], errors="coerce"
    ).max().date().isoformat()

    players_total = int(df["player_id_tm"].nunique())
    leagues_total = int(df["current_league"].nunique())

    homonym_names = int(
        df.loc[df["is_homonym_name"] == True, "player_name_norm"].nunique()
    )

    valuation_age_days = (
        date.today() - datetime.strptime(latest_valuation_date, "%Y-%m-%d").date()
    ).days

    health.setdefault("snapshot", {})
    health["snapshot"].update(
        {
            "snapshot_version": metadata.get("snapshot_version", "v1.0.0"),
            "snapshot_date": metadata.get("snapshot_date"),
            "latest_valuation_date": latest_valuation_date,
            "match_key": metadata.get("match_key", "player_id_tm"),
            "fallback_match_key": metadata.get("fallback_match_key", "player_name_norm_unique_only"),
            "source": metadata.get("source", "transfermarkt_features_v13a"),
            "players_total": players_total,
            "leagues_total": leagues_total,
        }
    )

    health.setdefault("freshness", {})
    health["freshness"].update(
        {
            "latest_valuation_date": latest_valuation_date,
            "valuation_age_days": valuation_age_days,
        }
    )

    health.setdefault("quality", {})
    health["quality"].update(
        {
            "homonym_names": homonym_names,
        }
    )

    health["players_total"] = players_total
    health["leagues_total"] = leagues_total
    health["latest_valuation_date"] = latest_valuation_date
    health["metadata_resynced_at_utc"] = metadata.get("generated_at_utc")

    write_json(HEALTH_PATH, health)

    print("Nested snapshot health report fixed")
    print(f"players_total: {players_total:,}")
    print(f"latest_valuation_date: {latest_valuation_date}")
    print(f"homonym_names: {homonym_names}")
    print(f"valuation_age_days: {valuation_age_days}")


if __name__ == "__main__":
    main()