from __future__ import annotations

import json
from datetime import date, datetime, timezone
from pathlib import Path
from typing import Any

import pandas as pd

ROOT = Path(__file__).resolve().parents[2]

METADATA_PATH = ROOT / "data" / "processed" / "current_player_snapshot_metadata.json"
OUTPUT_DIR = ROOT / "reports" / "data_quality"
OUTPUT_JSON = OUTPUT_DIR / "snapshot_health_report.json"
OUTPUT_MD = OUTPUT_DIR / "snapshot_health_report.md"


def read_json(path: Path) -> dict[str, Any]:
    if not path.exists():
        raise FileNotFoundError(f"Missing input file: {path}")
    with path.open("r", encoding="utf-8") as f:
        data = json.load(f)
    if not isinstance(data, dict):
        raise ValueError(f"Expected JSON object in {path}")
    return data


def parse_date(value: Any) -> date | None:
    if value is None or value == "":
        return None
    ts = pd.to_datetime(value, errors="coerce", utc=False)
    if pd.isna(ts):
        return None
    return ts.date()


def days_since(value: Any, today: date) -> int | None:
    parsed = parse_date(value)
    if parsed is None:
        return None
    return int((today - parsed).days)


def status_rank(status: str) -> int:
    return {"GREEN": 0, "YELLOW": 1, "RED": 2}.get(status, 2)


def combine_status(*statuses: str) -> str:
    return max(statuses, key=status_rank)


def freshness_status(valuation_age_days: int | None) -> str:
    if valuation_age_days is None:
        return "RED"
    if valuation_age_days <= 120:
        return "GREEN"
    if valuation_age_days <= 180:
        return "YELLOW"
    return "RED"


def freshness_score(valuation_age_days: int | None) -> float:
    if valuation_age_days is None:
        return 0.0
    if valuation_age_days <= 120:
        return 100.0
    if valuation_age_days <= 180:
        # Linearly decay from 100 to 80 between 120 and 180 days.
        return round(100 - ((valuation_age_days - 120) / 60) * 20, 2)
    if valuation_age_days <= 365:
        # Linearly decay from 80 to 40 between 180 and 365 days.
        return round(80 - ((valuation_age_days - 180) / 185) * 40, 2)
    return 40.0


def coverage_status(dss_pct: float | None, portfolio_pct: float | None) -> str:
    dss = dss_pct if dss_pct is not None else 0.0
    portfolio = portfolio_pct if portfolio_pct is not None else 0.0
    if dss >= 90 and portfolio >= 85:
        return "GREEN"
    if dss >= 85 and portfolio >= 80:
        return "YELLOW"
    return "RED"


def coverage_score(dss_pct: float | None, contract_pct: float | None, portfolio_pct: float | None) -> float:
    vals = [v for v in [dss_pct, contract_pct, portfolio_pct] if v is not None]
    if not vals:
        return 0.0
    # Weighted toward DSS/Contract because they drive player-facing trust.
    dss = dss_pct if dss_pct is not None else 0.0
    contract = contract_pct if contract_pct is not None else 0.0
    portfolio = portfolio_pct if portfolio_pct is not None else 0.0
    return round(0.40 * dss + 0.30 * contract + 0.30 * portfolio, 2)


def quality_status(homonym_names: int | None) -> str:
    if homonym_names is None:
        return "RED"
    if homonym_names <= 1000:
        return "GREEN"
    if homonym_names <= 2000:
        return "YELLOW"
    return "RED"


def quality_score(homonym_names: int | None) -> float:
    if homonym_names is None:
        return 0.0
    if homonym_names <= 500:
        return 100.0
    if homonym_names <= 1000:
        return round(100 - ((homonym_names - 500) / 500) * 10, 2)
    if homonym_names <= 2000:
        return round(90 - ((homonym_names - 1000) / 1000) * 30, 2)
    return 50.0


def safe_float(value: Any) -> float | None:
    if value is None:
        return None
    try:
        if pd.isna(value):
            return None
        return float(value)
    except Exception:
        return None


def build_report(metadata: dict[str, Any]) -> dict[str, Any]:
    today = datetime.now(timezone.utc).date()
    coverage = metadata.get("coverage", {}) if isinstance(metadata.get("coverage"), dict) else {}
    unmatched = metadata.get("unmatched_rows", {}) if isinstance(metadata.get("unmatched_rows"), dict) else {}
    matched = metadata.get("matched_rows", {}) if isinstance(metadata.get("matched_rows"), dict) else {}

    snapshot_age = days_since(metadata.get("snapshot_date"), today)
    valuation_age = days_since(metadata.get("latest_valuation_date"), today)

    dss_pct = safe_float(coverage.get("dss_pct"))
    contract_pct = safe_float(coverage.get("contract_pct"))
    portfolio_pct = safe_float(coverage.get("portfolio_pct"))
    homonyms = metadata.get("homonym_names")
    try:
        homonyms_int = int(homonyms) if homonyms is not None else None
    except Exception:
        homonyms_int = None

    f_status = freshness_status(valuation_age)
    f_score = freshness_score(valuation_age)

    c_status = coverage_status(dss_pct, portfolio_pct)
    c_score = coverage_score(dss_pct, contract_pct, portfolio_pct)

    q_status = quality_status(homonyms_int)
    q_score = quality_score(homonyms_int)

    snapshot_score = round(0.40 * f_score + 0.40 * c_score + 0.20 * q_score, 2)
    calculated_status = combine_status(f_status, c_status, q_status)

    # Score can only downgrade the global status, never upgrade hard-rule failures.
    score_status = "GREEN" if snapshot_score >= 95 else "YELLOW" if snapshot_score >= 80 else "RED"
    snapshot_status = combine_status(calculated_status, score_status)

    action_required = snapshot_status == "RED"
    refresh_recommended = f_status in {"YELLOW", "RED"}

    warnings: list[str] = []
    if f_status != "GREEN":
        warnings.append("Latest valuation date is becoming stale; refresh should be evaluated.")
    if c_status != "GREEN":
        warnings.append("Snapshot coverage is below preferred production threshold.")
    if q_status != "GREEN":
        warnings.append("Homonym load is high; identity resolution review is recommended.")
    if not warnings:
        warnings.append("No action required under current governance thresholds.")

    return {
        "snapshot_status": snapshot_status,
        "snapshot_score": snapshot_score,
        "generated_at_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "metadata_source": str(METADATA_PATH.relative_to(ROOT)),
        "snapshot": {
            "snapshot_version": metadata.get("snapshot_version"),
            "snapshot_date": metadata.get("snapshot_date"),
            "source": metadata.get("source"),
            "latest_valuation_date": metadata.get("latest_valuation_date"),
            "players_total": metadata.get("players_total"),
            "leagues_total": metadata.get("leagues_total"),
            "match_key": metadata.get("match_key"),
            "fallback_match_key": metadata.get("fallback_match_key"),
        },
        "freshness": {
            "snapshot_age_days": snapshot_age,
            "valuation_age_days": valuation_age,
            "score": f_score,
            "status": f_status,
            "thresholds": {
                "green_max_valuation_age_days": 120,
                "yellow_max_valuation_age_days": 180,
            },
        },
        "coverage": {
            "dss_pct": dss_pct,
            "contract_pct": contract_pct,
            "portfolio_pct": portfolio_pct,
            "matched_rows": matched,
            "unmatched_rows": unmatched,
            "score": c_score,
            "status": c_status,
            "thresholds": {
                "green_min_dss_pct": 90,
                "green_min_portfolio_pct": 85,
                "yellow_min_dss_pct": 85,
                "yellow_min_portfolio_pct": 80,
            },
        },
        "quality": {
            "homonym_names": homonyms_int,
            "score": q_score,
            "status": q_status,
            "thresholds": {
                "green_max_homonym_names": 1000,
                "yellow_max_homonym_names": 2000,
            },
        },
        "recommendation": {
            "action_required": action_required,
            "refresh_recommended": refresh_recommended,
            "next_action": (
                "Investigate source freshness / coverage before product release."
                if action_required
                else "Evaluate refresh cadence before the next release cycle."
                if refresh_recommended
                else "No action required. Continue standard monthly monitoring."
            ),
        },
        "warnings": warnings,
        "governance_note": metadata.get("governance_note"),
    }


def write_markdown(report: dict[str, Any], path: Path) -> None:
    snapshot = report["snapshot"]
    freshness = report["freshness"]
    coverage = report["coverage"]
    quality = report["quality"]
    rec = report["recommendation"]

    md = f"""# Snapshot Health Report

**Status:** {report['snapshot_status']}  
**Snapshot Score:** {report['snapshot_score']}/100  
**Generated at UTC:** {report['generated_at_utc']}

## Snapshot

| Field | Value |
|---|---:|
| Snapshot version | {snapshot.get('snapshot_version')} |
| Snapshot date | {snapshot.get('snapshot_date')} |
| Source | {snapshot.get('source')} |
| Latest valuation date | {snapshot.get('latest_valuation_date')} |
| Players total | {snapshot.get('players_total')} |
| Leagues total | {snapshot.get('leagues_total')} |
| Match key | {snapshot.get('match_key')} |
| Fallback match key | {snapshot.get('fallback_match_key')} |

## Freshness

| Metric | Value |
|---|---:|
| Snapshot age days | {freshness.get('snapshot_age_days')} |
| Valuation age days | {freshness.get('valuation_age_days')} |
| Freshness score | {freshness.get('score')} |
| Freshness status | {freshness.get('status')} |

## Coverage

| Dataset | Coverage | Matched | Unmatched |
|---|---:|---:|---:|
| DSS | {coverage.get('dss_pct')}% | {coverage.get('matched_rows', {}).get('dss')} | {coverage.get('unmatched_rows', {}).get('dss')} |
| Contract Intelligence | {coverage.get('contract_pct')}% | {coverage.get('matched_rows', {}).get('contract')} | {coverage.get('unmatched_rows', {}).get('contract')} |
| Portfolio | {coverage.get('portfolio_pct')}% | {coverage.get('matched_rows', {}).get('portfolio')} | {coverage.get('unmatched_rows', {}).get('portfolio')} |

**Coverage score:** {coverage.get('score')}  
**Coverage status:** {coverage.get('status')}

## Quality

| Metric | Value |
|---|---:|
| Homonym names | {quality.get('homonym_names')} |
| Quality score | {quality.get('score')} |
| Quality status | {quality.get('status')} |

## Recommendation

| Field | Value |
|---|---|
| Action required | {rec.get('action_required')} |
| Refresh recommended | {rec.get('refresh_recommended')} |
| Next action | {rec.get('next_action')} |

## Governance Note

{report.get('governance_note') or ''}
"""
    path.write_text(md, encoding="utf-8")


def main() -> None:
    metadata = read_json(METADATA_PATH)
    report = build_report(metadata)

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    OUTPUT_JSON.write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8")
    write_markdown(report, OUTPUT_MD)

    print("=" * 100)
    print("SNAPSHOT HEALTH REPORT")
    print("=" * 100)
    print(json.dumps(report, indent=2, ensure_ascii=False))
    print(f"\n[OK] JSON: {OUTPUT_JSON}")
    print(f"[OK] MD:   {OUTPUT_MD}")


if __name__ == "__main__":
    main()
