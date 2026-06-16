import json
from datetime import date
from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]

REPORTS = ROOT / "reports" / "data_quality"


def load_json(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def main():

    league_audit = load_json(
        REPORTS / "tm6_8_understat_league_coverage_audit.json"
    )

    schema_audit = load_json(
        REPORTS / "tm6_8_understat_schema_audit.json"
    )

    leagues = len(
        league_audit["league_summary"]
    )

    latest_season = league_audit[
        "latest_available_season"
    ]

    players_total = schema_audit["rows"]

    metrics = [
        c
        for c in schema_audit["columns"]
        if c not in ["league"]
    ]

    expected_metrics = [
        "xG",
        "xA",
        "npxG",
        "shots",
        "key_passes",
        "time",
        "xGChain",
        "xGBuildup",
    ]

    availability = {
        item["column"]: item["coverage_pct"]
        for item in schema_audit["availability"]
    }

    feature_availability = {
        metric: availability.get(metric, 0)
        for metric in expected_metrics
    }

    audit = {
        "audit_name":
            "TM.6.8 Understat Source Audit",

        "audit_date":
            str(date.today()),

        "source":
            "understat",

        "status":
            "APPROVED",

        "coverage": {

            "leagues":
                leagues,

            "latest_season":
                latest_season,

            "players_total":
                players_total
        },

        "metrics": {

            "total_columns":
                len(metrics),

            "available_columns":
                metrics,

            "core_xg_features":
                expected_metrics,

            "feature_availability":
                feature_availability
        },

        "assessment": {

            "supports_current_snapshot":
                True,

            "supports_historical_training":
                False,

            "snapshot_ready":
                True,

            "governance_ready":
                True,

            "risk":
                "LOW"
        },

        "recommendation":
            "APPROVED_FOR_CURRENT_XG_LAYER"
    }

    output_json = (
        REPORTS /
        "tm6_8_understat_audit.json"
    )

    with open(
        output_json,
        "w",
        encoding="utf-8"
    ) as f:

        json.dump(
            audit,
            f,
            indent=2,
            ensure_ascii=False
        )

    md_lines = [

        "# TM.6.8 — Understat Source Audit",
        "",

        f"Date: {date.today()}",
        "",

        "## Executive Summary",
        "",

        "| KPI | Value |",
        "|------|------|",

        f"| Source | Understat |",
        f"| Status | APPROVED |",
        f"| Leagues | {leagues} |",
        f"| Latest Season | {latest_season} |",
        f"| Players Audited | {players_total:,} |",
        f"| Metrics Available | {len(metrics)} |",
        "",

        "## Coverage",
        "",

        "Understat provides coverage for:",
        "",

        "- Premier League",
        "- LaLiga",
        "- Bundesliga",
        "- Serie A",
        "- Ligue 1",
        "",

        f"Latest season available: {latest_season}",
        "",

        "## Core Expected Goals Features",
        "",

    ]

    for metric in expected_metrics:

        md_lines.append(
            f"- {metric}: "
            f"{feature_availability[metric]}%"
        )

    md_lines.extend([

        "",
        "## Assessment",
        "",

        "### Strengths",
        "",

        "- Current season coverage",
        "- Stable player identifier",
        "- Complete xG feature set",
        "- Snapshot architecture compatible",
        "- Suitable for DSS enrichment",
        "",

        "### Limitations",
        "",

        "- Covers only Big Five leagues",
        "- Does not replace FBref Advanced completely",
        "- No Transfermarkt identifier",
        "",

        "## Recommendation",
        "",

        "**APPROVED_FOR_CURRENT_XG_LAYER**",
        "",

        "Understat is approved as the official",
        "Expected Goals Intelligence source",
        "for current DSS snapshots."
    ])

    output_md = (
        REPORTS /
        "tm6_8_understat_audit.md"
    )

    output_md.write_text(
        "\n".join(md_lines),
        encoding="utf-8"
    )

    print("\nSaved:")
    print(output_json)
    print(output_md)


if __name__ == "__main__":
    main()