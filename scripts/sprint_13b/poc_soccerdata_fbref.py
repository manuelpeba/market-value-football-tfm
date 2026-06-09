from pathlib import Path
import pandas as pd
import soccerdata as sd


OUT_DIR = Path("data/raw/fbref/sprint_13b/soccerdata")
REPORT_DIR = Path("reports/sprint_13b")

OUT_DIR.mkdir(parents=True, exist_ok=True)
REPORT_DIR.mkdir(parents=True, exist_ok=True)

LEAGUES = ["ENG-Premier League"]
SEASONS = ["2025-2026"]

STAT_TYPES = [
    "standard",
    "shooting",
    "playing_time",
    "misc",
    "passing",
    "passing_types",
    "gca",
    "defense",
    "possession",
]

rows = []

for stat_type in STAT_TYPES:
    print(f"\n=== Testing stat_type={stat_type} ===")

    try:
        fbref = sd.FBref(
            leagues=LEAGUES,
            seasons=SEASONS,
        )

        df = fbref.read_player_season_stats(stat_type=stat_type)

        out_path = OUT_DIR / f"fbref_{stat_type}_premier_league_2025_2026.parquet"
        df.to_parquet(out_path, index=True)

        rows.append(
            {
                "source": "soccerdata",
                "league": "premier_league",
                "season": "2025_2026",
                "stat_type": stat_type,
                "status": "ok",
                "rows": len(df),
                "columns": len(df.columns),
                "output_path": str(out_path),
                "error": "",
            }
        )

        print(f"OK: {df.shape} -> {out_path}")
        print(df.head(2))

    except Exception as exc:
        rows.append(
            {
                "source": "soccerdata",
                "league": "premier_league",
                "season": "2025_2026",
                "stat_type": stat_type,
                "status": "error",
                "rows": None,
                "columns": None,
                "output_path": "",
                "error": repr(exc),
            }
        )

        print(f"ERROR {stat_type}: {repr(exc)}")

audit = pd.DataFrame(rows)
audit_path = REPORT_DIR / "poc_soccerdata_fbref_results.csv"
audit.to_csv(audit_path, index=False, encoding="utf-8-sig")

print("\nSaved:", audit_path)
print(audit)