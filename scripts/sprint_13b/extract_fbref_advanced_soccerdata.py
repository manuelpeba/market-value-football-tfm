from pathlib import Path
import time
import pandas as pd
import soccerdata as sd

RAW_DIR = Path("data/raw/fbref/sprint_13b/soccerdata")
REPORT_DIR = Path("reports/sprint_13b")
RAW_DIR.mkdir(parents=True, exist_ok=True)
REPORT_DIR.mkdir(parents=True, exist_ok=True)

LEAGUES = [
    "ENG-Premier League",
    "ESP-La Liga",
    "GER-Bundesliga",
    "ITA-Serie A",
    "FRA-Ligue 1",
    "NED-Eredivisie",
    "POR-Primeira Liga",
    "ENG-Championship",
    "BEL-Belgian Pro League",
    "AUT-Austrian Bundesliga",
    "ESP-Segunda División",
]

SEASONS = [
    "2019-2020",
    "2020-2021",
    "2021-2022",
    "2022-2023",
    "2023-2024",
    "2024-2025",
    "2025-2026",
]

STAT_TYPES = ["shooting", "playing_time", "misc"]

def slug(value: str) -> str:
    return (
        value.lower()
        .replace(" ", "_")
        .replace("-", "_")
        .replace(".", "")
        .replace("ü", "u")
        .replace("ó", "o")
        .replace("í", "i")
        .replace("á", "a")
        .replace("é", "e")
        .replace("ñ", "n")
    )

rows = []

for league in LEAGUES:
    for season in SEASONS:
        for stat_type in STAT_TYPES:
            league_slug = slug(league.split("-", 1)[1])
            season_slug = season.replace("-", "_")

            out_dir = RAW_DIR / stat_type
            out_dir.mkdir(parents=True, exist_ok=True)

            out_path = out_dir / f"fbref_{stat_type}_{league_slug}_{season_slug}.parquet"

            print(f"\n=== {league} | {season} | {stat_type} ===")

            if out_path.exists():
                print(f"SKIP existing: {out_path}")
                rows.append({
                    "source": "soccerdata",
                    "league": league,
                    "season": season,
                    "stat_type": stat_type,
                    "status": "skipped_existing",
                    "rows": None,
                    "columns": None,
                    "output_path": str(out_path),
                    "error": "",
                })
                continue

            try:
                fbref = sd.FBref(
                    leagues=[league],
                    seasons=[season],
                )

                df = fbref.read_player_season_stats(stat_type=stat_type)
                df.to_parquet(out_path, index=True)

                rows.append({
                    "source": "soccerdata",
                    "league": league,
                    "season": season,
                    "stat_type": stat_type,
                    "status": "ok",
                    "rows": len(df),
                    "columns": len(df.columns),
                    "output_path": str(out_path),
                    "error": "",
                })

                print(f"OK: {df.shape} -> {out_path}")

                time.sleep(8)

            except Exception as exc:
                rows.append({
                    "source": "soccerdata",
                    "league": league,
                    "season": season,
                    "stat_type": stat_type,
                    "status": "error",
                    "rows": None,
                    "columns": None,
                    "output_path": "",
                    "error": repr(exc),
                })

                print(f"ERROR: {repr(exc)}")
                time.sleep(8)

audit = pd.DataFrame(rows)
audit_path = REPORT_DIR / "fbref_advanced_extraction_audit.csv"
audit.to_csv(audit_path, index=False, encoding="utf-8-sig")

print("\nSaved audit:", audit_path)
print(audit["status"].value_counts(dropna=False))