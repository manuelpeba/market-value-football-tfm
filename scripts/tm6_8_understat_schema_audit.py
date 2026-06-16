import asyncio
import json
from datetime import date
from pathlib import Path

import aiohttp
import pandas as pd
from understat import Understat


ROOT = Path(__file__).resolve().parents[1]

OUT_DIR = ROOT / "reports" / "data_quality"
OUT_DIR.mkdir(parents=True, exist_ok=True)

LEAGUES = [
    "EPL",
    "La liga",
    "Bundesliga",
    "Serie A",
    "Ligue 1",
]

SEASON = 2025


async def main():

    dfs = []

    async with aiohttp.ClientSession() as session:

        understat = Understat(session)

        for league in LEAGUES:

            print(f"Loading {league}...")

            players = await understat.get_league_players(
                league,
                SEASON
            )

            df = pd.DataFrame(players)

            df["league"] = league

            dfs.append(df)

    df = pd.concat(dfs, ignore_index=True)

    print("\n")
    print("=" * 80)
    print("GLOBAL AUDIT")
    print("=" * 80)

    print(f"Rows: {len(df):,}")
    print(f"Columns: {len(df.columns)}")

    columns = sorted(df.columns.tolist())

    print("\nColumns:")
    for col in columns:
        print(col)

    availability = []

    for col in columns:

        non_null = df[col].notna().sum()

        coverage = round(
            non_null / len(df) * 100,
            2
        )

        availability.append(
            {
                "column": col,
                "non_null": int(non_null),
                "coverage_pct": coverage,
            }
        )

    availability_df = pd.DataFrame(availability)

    availability_df = availability_df.sort_values(
        "coverage_pct",
        ascending=False
    )

    print("\n")
    print("=" * 80)
    print("TOP COVERAGE")
    print("=" * 80)

    print(availability_df.head(50))

    json_output = {
        "audit_name": "TM.6.8a.3 Metrics Availability Audit",
        "audit_date": str(date.today()),
        "season": "2025-2026",
        "rows": int(len(df)),
        "columns": columns,
        "availability": availability,
    }

    json_path = (
        OUT_DIR /
        "tm6_8_understat_schema_audit.json"
    )

    json_path.write_text(
        json.dumps(
            json_output,
            indent=2,
            ensure_ascii=False
        ),
        encoding="utf-8"
    )

    availability_df.to_csv(
        OUT_DIR /
        "tm6_8_understat_schema_availability.csv",
        index=False
    )

    print("\nSaved:")
    print(json_path)


if __name__ == "__main__":
    asyncio.run(main())