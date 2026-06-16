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

LEAGUES = {
    "EPL": "Premier League",
    "La liga": "LaLiga",
    "Bundesliga": "Bundesliga",
    "Serie A": "Serie A",
    "Ligue 1": "Ligue 1",
}

SEASONS_TO_TEST = list(range(2014, 2027))


async def fetch_league_players(understat, league_key, season):
    try:
        players = await understat.get_league_players(league_key, season)
        return players or []
    except Exception as exc:
        return {"error": str(exc)}


def summarize_players(players):
    if isinstance(players, dict) and "error" in players:
        return {
            "status": "ERROR",
            "players_count": 0,
            "teams_count": 0,
            "metrics_available": [],
            "error": players["error"],
        }

    if not players:
        return {
            "status": "EMPTY",
            "players_count": 0,
            "teams_count": 0,
            "metrics_available": [],
            "error": None,
        }

    df = pd.DataFrame(players)

    team_col = "team_title" if "team_title" in df.columns else None

    return {
        "status": "OK",
        "players_count": int(len(df)),
        "teams_count": int(df[team_col].nunique()) if team_col else None,
        "metrics_available": sorted(df.columns.tolist()),
        "error": None,
    }


async def main():
    rows = []

    async with aiohttp.ClientSession() as session:
        understat = Understat(session)

        for league_key, league_name in LEAGUES.items():
            print(f"\n=== {league_name} ===")

            for season in SEASONS_TO_TEST:
                players = await fetch_league_players(understat, league_key, season)
                summary = summarize_players(players)

                row = {
                    "source": "understat",
                    "league_key": league_key,
                    "league": league_name,
                    "season_start_year": season,
                    "season": f"{season}-{season + 1}",
                    **summary,
                }
                rows.append(row)

                print(
                    f"{league_name} {season}-{season + 1}: "
                    f"{summary['status']} | players={summary['players_count']} | teams={summary['teams_count']}"
                )

    df = pd.DataFrame(rows)

    csv_path = OUT_DIR / "tm6_8_understat_league_coverage_audit.csv"
    json_path = OUT_DIR / "tm6_8_understat_league_coverage_audit.json"
    md_path = OUT_DIR / "tm6_8_understat_league_coverage_audit.md"

    df.to_csv(csv_path, index=False)

    ok_df = df[df["status"].eq("OK")].copy()

    league_summary = (
        ok_df.groupby("league")
        .agg(
            first_season=("season", "min"),
            latest_season=("season", "max"),
            seasons_available=("season", "nunique"),
            max_players=("players_count", "max"),
            latest_players=("players_count", "last"),
            latest_teams=("teams_count", "last"),
        )
        .reset_index()
        .to_dict(orient="records")
    )

    latest_available_season = ok_df["season"].max() if not ok_df.empty else None

    all_metrics = sorted(
        {
            metric
            for metrics in ok_df["metrics_available"].dropna()
            for metric in metrics
        }
    )

    audit = {
        "audit_name": "TM.6.8a.2 Understat League Coverage Audit",
        "audit_date": str(date.today()),
        "source": "understat",
        "leagues_tested": list(LEAGUES.values()),
        "seasons_tested": [f"{s}-{s+1}" for s in SEASONS_TO_TEST],
        "latest_available_season": latest_available_season,
        "league_summary": league_summary,
        "metrics_available": all_metrics,
        "raw_output": str(csv_path),
        "assessment": {
            "current_layer_viability": "PENDING_DSS_MATCHING",
            "notes": [
                "This audit measures source availability only.",
                "DSS viability requires matching coverage against global_prospect_universe.",
            ],
        },
    }

    json_path.write_text(json.dumps(audit, indent=2, ensure_ascii=False), encoding="utf-8")

    md = [
        "# TM.6.8a.2 — Understat League Coverage Audit",
        "",
        f"Audit date: {date.today()}",
        "",
        "## Executive Summary",
        "",
        f"- Source: Understat",
        f"- Leagues tested: {len(LEAGUES)}",
        f"- Seasons tested: {SEASONS_TO_TEST[0]}-{SEASONS_TO_TEST[-1] + 1}",
        f"- Latest available season detected: {latest_available_season}",
        "",
        "## League Coverage",
        "",
        "| League | First Season | Latest Season | Seasons | Max Players | Latest Players | Latest Teams |",
        "|---|---:|---:|---:|---:|---:|---:|",
    ]

    for item in league_summary:
        md.append(
            f"| {item['league']} | {item['first_season']} | {item['latest_season']} | "
            f"{item['seasons_available']} | {item['max_players']} | "
            f"{item['latest_players']} | {item['latest_teams']} |"
        )

    md.extend(
        [
            "",
            "## Metrics Available",
            "",
            ", ".join(all_metrics),
            "",
            "## Assessment",
            "",
            "This audit confirms source-level league and season availability. "
            "Final DSS approval requires matching coverage against DSS, Portfolio and Contract datasets.",
        ]
    )

    md_path.write_text("\n".join(md), encoding="utf-8")

    print("\nSaved:")
    print(csv_path)
    print(json_path)
    print(md_path)


if __name__ == "__main__":
    asyncio.run(main())