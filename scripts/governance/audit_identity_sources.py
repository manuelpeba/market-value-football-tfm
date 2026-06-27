from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
PROCESSED = ROOT / "data" / "processed"

FILES = [
    "current_player_snapshot.parquet",
    "player_season_modeling_v13a.parquet",
    "player_season_modeling_v13b.parquet",
    "player_season_panel_v13a.parquet",
    "fbref_features_v13a.parquet",
    "transfermarkt_features_v13a.parquet",
]

TARGET_COLUMNS = [
    "player_id_tm",
    "player_name_tm",
    "club",
    "current_club",
    "league",
    "current_league",
    "age",
    "current_age",
    "position",
    "current_position",
    "position_group",
    "nationality",
    "market_value_eur",
    "current_market_value_eur",
    "valuation_date",
]

for file in FILES:

    path = PROCESSED / file

    print("\n" + "=" * 90)
    print(file)

    if not path.exists():
        print("NOT FOUND")
        continue

    df = pd.read_parquet(path)

    print(f"rows: {len(df):,}")
    print()

    available = [c for c in TARGET_COLUMNS if c in df.columns]

    if not available:
        print("No identity columns")
        continue

    summary = []

    for c in available:

        non_null = df[c].notna().sum()

        summary.append({
            "column": c,
            "non_null": non_null,
            "coverage_%": round(non_null / len(df) * 100, 2)
        })

    print(pd.DataFrame(summary).to_string(index=False))