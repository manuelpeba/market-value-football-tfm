import json
from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]

snapshot_path = ROOT / "data/processed/current_player_snapshot.parquet"
metadata_path = ROOT / "data/processed/current_player_snapshot_metadata.json"
health_path = ROOT / "reports/data_quality/snapshot_health_report.json"

print("\n==============================")
print("SNAPSHOT")
print("==============================")

df = pd.read_parquet(snapshot_path)

print("rows:", len(df))
print("players:", df["player_id_tm"].nunique())

if "current_league" in df.columns:
    print("leagues:", df["current_league"].nunique())

if "current_valuation_date" in df.columns:
    print(
        "latest valuation:",
        pd.to_datetime(df["current_valuation_date"]).max()
    )

print("\n==============================")
print("METADATA")
print("==============================")

metadata = json.loads(metadata_path.read_text())

for k, v in metadata.items():
    print(k, ":", v)

print("\n==============================")
print("HEALTH REPORT")
print("==============================")

health = json.loads(health_path.read_text())

for k in [
    "snapshot_status",
    "snapshot_score",
]:
    print(k, ":", health.get(k))