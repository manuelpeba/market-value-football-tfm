import json
from datetime import date, datetime
from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]

PROCESSED = ROOT / "data" / "processed"
REPORTS = ROOT / "reports" / "data_quality"

SNAPSHOT_PATH = PROCESSED / "current_xg_snapshot.parquet"
METADATA_PATH = PROCESSED / "current_xg_snapshot_metadata.json"
MATCHING_AUDIT_PATH = REPORTS / "tm6_8_understat_matching_audit.json"

OUT_REPORT_JSON = REPORTS / "current_xg_snapshot_health_report.json"
OUT_REPORT_MD = REPORTS / "current_xg_snapshot_health_report.md"
OUT_SCORE_JSON = REPORTS / "current_xg_snapshot_health_score.json"
OUT_SCORE_MD = REPORTS / "current_xg_snapshot_health_score.md"

CRITICAL_FEATURES = [
    "current_xg",
    "current_xa",
    "current_npxg",
    "current_xg_per90",
    "current_xa_per90",
    "current_expected_contribution",
    "current_expected_contribution_per90",
]


WEIGHTS = {
    "coverage": 0.40,
    "freshness": 0.30,
    "feature_availability": 0.20,
    "governance": 0.10,
}


def load_json(path: Path) -> dict:
    if not path.exists():
        return {}
    return json.loads(path.read_text(encoding="utf-8"))


def score_status(score: float) -> str:
    if score >= 90:
        return "GREEN"
    if score >= 75:
        return "YELLOW"
    return "RED"


def freshness_score(snapshot_date: str) -> tuple[int, int, str]:
    parsed = datetime.strptime(snapshot_date, "%Y-%m-%d").date()
    age_days = (date.today() - parsed).days

    if age_days <= 30:
        return age_days, 100, "GREEN"
    if age_days <= 90:
        return age_days, 80, "YELLOW"
    return age_days, 50, "RED"


def main():
    REPORTS.mkdir(parents=True, exist_ok=True)

    if not SNAPSHOT_PATH.exists():
        raise FileNotFoundError(f"Missing snapshot: {SNAPSHOT_PATH}")

    snapshot = pd.read_parquet(SNAPSHOT_PATH)
    metadata = load_json(METADATA_PATH)
    matching_audit = load_json(MATCHING_AUDIT_PATH)

    rows = len(snapshot)
    players = snapshot["understat_player_id"].nunique()
    leagues = snapshot["league"].nunique()

    matching_results = {
        item["dataset"]: item
        for item in matching_audit.get("results", [])
    }

    dss_big5 = matching_results.get("DSS", {}).get("coverage_big5_pct", 0)
    portfolio_big5 = matching_results.get("Portfolio", {}).get("coverage_big5_pct", 0)
    contract_big5 = matching_results.get("Contract", {}).get("coverage_big5_pct", 0)

    coverage_score = round((dss_big5 + portfolio_big5 + contract_big5) / 3, 2)

    snapshot_date = str(snapshot["snapshot_date"].dropna().iloc[0])
    age_days, freshness_points, freshness_status = freshness_score(snapshot_date)

    feature_availability = {}
    for feature in CRITICAL_FEATURES:
        if feature not in snapshot.columns:
            feature_availability[feature] = 0.0
        else:
            feature_availability[feature] = round(snapshot[feature].notna().mean() * 100, 2)

    feature_score = round(sum(feature_availability.values()) / len(feature_availability), 2)

    governance_checks = {
        "snapshot_path_exists": SNAPSHOT_PATH.exists(),
        "metadata_path_exists": METADATA_PATH.exists(),
        "snapshot_version_present": "snapshot_version" in snapshot.columns,
        "snapshot_date_present": "snapshot_date" in snapshot.columns,
        "source_present": "source" in snapshot.columns,
        "understat_player_id_present": "understat_player_id" in snapshot.columns,
    }

    governance_score = round(sum(governance_checks.values()) / len(governance_checks) * 100, 2)

    duplicate_name_groups = (
        snapshot.groupby(["player_name_norm", "league"])
        .size()
        .reset_index(name="n")
    )
    duplicate_name_groups = duplicate_name_groups[duplicate_name_groups["n"] > 1]

    homonym_groups = int(len(duplicate_name_groups))
    homonym_rows = int(duplicate_name_groups["n"].sum()) if homonym_groups else 0
    homonym_risk_pct = round(homonym_rows / rows * 100, 2) if rows else 0

    score_components = {
        "coverage": {
            "raw_score": coverage_score,
            "weight": WEIGHTS["coverage"],
            "weighted_score": round(coverage_score * WEIGHTS["coverage"], 2),
            "inputs": {
                "dss_big5_pct": dss_big5,
                "portfolio_big5_pct": portfolio_big5,
                "contract_big5_pct": contract_big5,
            },
        },
        "freshness": {
            "raw_score": freshness_points,
            "weight": WEIGHTS["freshness"],
            "weighted_score": round(freshness_points * WEIGHTS["freshness"], 2),
            "inputs": {
                "snapshot_age_days": age_days,
                "freshness_status": freshness_status,
            },
        },
        "feature_availability": {
            "raw_score": feature_score,
            "weight": WEIGHTS["feature_availability"],
            "weighted_score": round(feature_score * WEIGHTS["feature_availability"], 2),
            "inputs": feature_availability,
        },
        "governance": {
            "raw_score": governance_score,
            "weight": WEIGHTS["governance"],
            "weighted_score": round(governance_score * WEIGHTS["governance"], 2),
            "inputs": governance_checks,
        },
    }

    health_score = round(
        sum(component["weighted_score"] for component in score_components.values()),
        2,
    )

    status = score_status(health_score)

    health_score_document = {
        "snapshot_name": "current_xg_snapshot",
        "score_name": "current_xg_snapshot_health_score",
        "report_date": str(date.today()),
        "snapshot_date": snapshot_date,
        "health_score": health_score,
        "status": status,
        "weights": WEIGHTS,
        "components": score_components,
        "thresholds": {
            "GREEN": ">= 90",
            "YELLOW": "75-89",
            "RED": "< 75",
        },
        "interpretation": (
            "The score is a weighted operational health indicator for the current xG snapshot. "
            "Coverage is intentionally limited to Big Five eligible rows because Understat does not cover non-Big Five leagues."
        ),
    }

    health_report = {
        "snapshot_name": "current_xg_snapshot",
        "snapshot_status": status,
        "health_score": health_score,
        "report_date": str(date.today()),
        "snapshot_date": snapshot_date,
        "source": "understat",
        "snapshot_version": metadata.get("snapshot_version", None),
        "season": metadata.get("season", None),
        "coverage": {
            "score": coverage_score,
            "dss_big5_pct": dss_big5,
            "portfolio_big5_pct": portfolio_big5,
            "contract_big5_pct": contract_big5,
        },
        "freshness": {
            "snapshot_age_days": age_days,
            "score": freshness_points,
            "status": freshness_status,
        },
        "feature_availability": {
            "score": feature_score,
            "features": feature_availability,
        },
        "identity": {
            "rows": int(rows),
            "unique_understat_players": int(players),
            "leagues": int(leagues),
            "homonym_groups": homonym_groups,
            "homonym_rows": homonym_rows,
            "homonym_risk_pct": homonym_risk_pct,
        },
        "governance": {
            "score": governance_score,
            "checks": governance_checks,
            "governance_note": metadata.get("governance_note", ""),
        },
        "health_score_file": str(OUT_SCORE_JSON),
        "recommendation": (
            "APPROVED_FOR_DSS_ENRICHMENT"
            if status in ["GREEN", "YELLOW"]
            else "NOT_APPROVED"
        ),
    }

    OUT_REPORT_JSON.write_text(
        json.dumps(health_report, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )

    OUT_SCORE_JSON.write_text(
        json.dumps(health_score_document, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )

    report_md = [
        "# TM.6.8d — Current xG Snapshot Health Report",
        "",
        f"Report date: {date.today()}",
        "",
        "## Executive Summary",
        "",
        "| KPI | Value |",
        "|---|---:|",
        f"| Status | {status} |",
        f"| Health Score | {health_score} |",
        f"| Snapshot Date | {snapshot_date} |",
        f"| Snapshot Age Days | {age_days} |",
        f"| Rows | {rows:,} |",
        f"| Unique Understat Players | {players:,} |",
        f"| Leagues | {leagues} |",
        f"| DSS Big 5 Coverage | {dss_big5}% |",
        f"| Portfolio Big 5 Coverage | {portfolio_big5}% |",
        f"| Contract Big 5 Coverage | {contract_big5}% |",
        "",
        "## Recommendation",
        "",
        f"**{health_report['recommendation']}**",
        "",
        "The current xG snapshot is approved as a governed current performance layer. "
        "It must remain separated from historical modeling datasets unless a future temporal validation protocol is explicitly implemented.",
    ]

    score_md = [
        "# TM.6.8d — Current xG Snapshot Health Score",
        "",
        f"Report date: {date.today()}",
        "",
        "## Score Summary",
        "",
        "| Component | Raw Score | Weight | Weighted Score |",
        "|---|---:|---:|---:|",
    ]

    for name, component in score_components.items():
        score_md.append(
            f"| {name} | {component['raw_score']} | "
            f"{component['weight']} | {component['weighted_score']} |"
        )

    score_md.extend(
        [
            "",
            f"Final health score: **{health_score}**",
            "",
            f"Status: **{status}**",
            "",
            "## Thresholds",
            "",
            "| Status | Rule |",
            "|---|---:|",
            "| GREEN | >= 90 |",
            "| YELLOW | 75-89 |",
            "| RED | < 75 |",
            "",
            "## Interpretation",
            "",
            "Coverage is calculated only on Big Five eligible rows because Understat does not cover non-Big Five leagues. "
            "The score therefore evaluates whether the snapshot is healthy for the specific scope it is designed to cover.",
        ]
    )

    OUT_REPORT_MD.write_text("\n".join(report_md), encoding="utf-8")
    OUT_SCORE_MD.write_text("\n".join(score_md), encoding="utf-8")

    print("\nSaved:")
    print(OUT_REPORT_JSON)
    print(OUT_REPORT_MD)
    print(OUT_SCORE_JSON)
    print(OUT_SCORE_MD)

    print("\nHealth summary:")
    print(f"Status: {status}")
    print(f"Health score: {health_score}")
    print(f"Coverage score: {coverage_score}")
    print(f"Freshness score: {freshness_points}")
    print(f"Feature score: {feature_score}")
    print(f"Governance score: {governance_score}")


if __name__ == "__main__":
    main()