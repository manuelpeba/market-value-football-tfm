from pathlib import Path
import pandas as pd
import soccerdata as sd

OUT_DIR = Path("data/raw/fbref/sprint_13b/soccerdata/team")
REPORT_DIR = Path("reports/sprint_13b")

OUT_DIR.mkdir(parents=True, exist_ok=True)
REPORT_DIR.mkdir(parents=True, exist_ok=True)

fbref = sd.FBref(
    leagues=["ENG-Premier League"],
    seasons=["2025-2026"],
)

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
    print(f"\n=== Team season stat_type={stat_type} ===")
    try:
        df = fbref.read_team_season_stats(stat_type=stat_type)

        out_path = OUT_DIR / f"fbref_team_{stat_type}_premier_league_2025_2026.parquet"
        df.to_parquet(out_path)

        rows.append({
            "level": "team_season",
            "stat_type": stat_type,
            "status": "ok",
            "rows": len(df),
            "columns": len(df.columns),
            "output_path": str(out_path),
            "error": "",
        })

        print(f"OK: {df.shape}")
        print(df.head())

    except Exception as exc:
        rows.append({
            "level": "team_season",
            "stat_type": stat_type,
            "status": "error",
            "rows": None,
            "columns": None,
            "output_path": "",
            "error": repr(exc),
        })

        print(f"ERROR: {repr(exc)}")

audit = pd.DataFrame(rows)
audit_path = REPORT_DIR / "poc_soccerdata_fbref_team_season_results.csv"
audit.to_csv(audit_path, index=False, encoding="utf-8-sig")

print("\nSaved:", audit_path)
print(audit)