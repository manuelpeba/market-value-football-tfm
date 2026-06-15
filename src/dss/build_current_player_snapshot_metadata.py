from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import pandas as pd

ROOT = Path(__file__).resolve().parents[2] if "src" in Path(__file__).parts else Path.cwd()

DEFAULT_SNAPSHOT = ROOT / "data" / "processed" / "current_player_snapshot.parquet"
DEFAULT_SNAPSHOT_AUDIT = ROOT / "data" / "processed" / "current_player_snapshot_audit.json"
DEFAULT_APPLY_SUMMARY = ROOT / "reports" / "data_quality" / "current_snapshot_apply" / "current_snapshot_apply_summary.json"
DEFAULT_OUTPUT = ROOT / "data" / "processed" / "current_player_snapshot_metadata.json"


def read_json(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def to_iso_date(value: Any) -> str | None:
    if value is None or pd.isna(value):
        return None
    ts = pd.to_datetime(value, errors="coerce")
    if pd.isna(ts):
        return str(value)
    return ts.date().isoformat()


def find_apply_record(summary: Any, token: str) -> dict[str, Any]:
    """Find a dataset record in different possible summary structures."""
    if not summary:
        return {}

    candidates: list[dict[str, Any]] = []

    if isinstance(summary, list):
        candidates.extend([x for x in summary if isinstance(x, dict)])

    elif isinstance(summary, dict):
        if isinstance(summary.get("results"), list):
            candidates.extend([x for x in summary["results"] if isinstance(x, dict)])
        if isinstance(summary.get("datasets"), list):
            candidates.extend([x for x in summary["datasets"] if isinstance(x, dict)])

        for value in summary.values():
            if isinstance(value, dict):
                candidates.append(value)
            elif isinstance(value, list):
                candidates.extend([x for x in value if isinstance(x, dict)])

    token_l = token.lower()
    for item in candidates:
        path = str(
            item.get("path", "")
            or item.get("dataset", "")
            or item.get("name", "")
        ).lower()
        if token_l in path:
            return item

    return {}

def get_pct(record: dict[str, Any]) -> float | None:
    for key in ["matched_pct", "coverage_pct", "match_pct"]:
        if key in record and pd.notna(record[key]):
            return round(float(record[key]), 2)
    rows = record.get("rows")
    matched = record.get("matched_total")
    if rows and matched is not None:
        return round(float(matched) / float(rows) * 100, 2)
    return None


def build_metadata(
    snapshot_path: Path,
    snapshot_audit_path: Path,
    apply_summary_path: Path,
    output_path: Path,
    snapshot_version: str,
    source: str,
) -> dict[str, Any]:
    if not snapshot_path.exists():
        raise FileNotFoundError(f"Snapshot not found: {snapshot_path}")

    snapshot = pd.read_parquet(snapshot_path)
    snapshot_audit = read_json(snapshot_audit_path)
    apply_summary = read_json(apply_summary_path)

    latest_valuation_date = None
    if "current_valuation_date" in snapshot.columns:
        latest_valuation_date = to_iso_date(snapshot["current_valuation_date"].max())
    elif "tm_current_valuation_date" in snapshot.columns:
        latest_valuation_date = to_iso_date(snapshot["tm_current_valuation_date"].max())

    players_total = int(snapshot["player_id_tm"].nunique()) if "player_id_tm" in snapshot.columns else int(len(snapshot))
    leagues_total = int(snapshot["current_league"].nunique()) if "current_league" in snapshot.columns else None
    leagues = sorted(snapshot["current_league"].dropna().astype(str).unique().tolist()) if "current_league" in snapshot.columns else []

    homonym_names = snapshot_audit.get("homonym_names")
    if homonym_names is None and "is_homonym_name" in snapshot.columns:
        homonym_names = int(snapshot.loc[snapshot["is_homonym_name"].fillna(False), "player_name_key"].nunique()) if "player_name_key" in snapshot.columns else int(snapshot["is_homonym_name"].fillna(False).sum())

    dss_record = find_apply_record(apply_summary, "global_prospect_universe")
    contract_record = find_apply_record(apply_summary, "contract_intelligence")
    portfolio_record = find_apply_record(apply_summary, "transfer_portfolio")

    metadata = {
        "snapshot_version": snapshot_version,
        "snapshot_date": datetime.now(timezone.utc).date().isoformat(),
        "generated_at_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "source": source,
        "snapshot_path": str(snapshot_path.relative_to(ROOT) if snapshot_path.is_absolute() and ROOT in snapshot_path.parents else snapshot_path),
        "latest_valuation_date": latest_valuation_date,
        "players_total": players_total,
        "leagues_total": leagues_total,
        "leagues": leagues,
        "market_value_min": int(pd.to_numeric(snapshot.get("current_market_value_eur"), errors="coerce").min()) if "current_market_value_eur" in snapshot.columns else None,
        "market_value_max": int(pd.to_numeric(snapshot.get("current_market_value_eur"), errors="coerce").max()) if "current_market_value_eur" in snapshot.columns else None,
        "homonym_names": int(homonym_names) if homonym_names is not None else None,
        "match_key": "player_id_tm",
        "fallback_match_key": "player_name_norm_unique_only",
        "coverage": {
            "dss_pct": get_pct(dss_record),
            "contract_pct": get_pct(contract_record),
            "portfolio_pct": get_pct(portfolio_record),
        },
        "matched_rows": {
            "dss": dss_record.get("matched_total"),
            "contract": contract_record.get("matched_total"),
            "portfolio": portfolio_record.get("matched_total"),
        },
        "unmatched_rows": {
            "dss": dss_record.get("unmatched"),
            "contract": contract_record.get("unmatched"),
            "portfolio": portfolio_record.get("unmatched"),
        },
        "source_files": {
            "snapshot_audit": str(snapshot_audit_path),
            "apply_summary": str(apply_summary_path),
        },
        "governance_note": (
            "Historical player-season values remain unchanged. Current club, league and market value "
            "are provided by current_player_snapshot and should be interpreted as current market context."
        ),
    }

    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", encoding="utf-8") as f:
        json.dump(metadata, f, indent=2, ensure_ascii=False)

    return metadata


def main() -> None:
    parser = argparse.ArgumentParser(description="Build metadata for current_player_snapshot governance layer.")
    parser.add_argument("--snapshot", default=str(DEFAULT_SNAPSHOT))
    parser.add_argument("--snapshot-audit", default=str(DEFAULT_SNAPSHOT_AUDIT))
    parser.add_argument("--apply-summary", default=str(DEFAULT_APPLY_SUMMARY))
    parser.add_argument("--output", default=str(DEFAULT_OUTPUT))
    parser.add_argument("--snapshot-version", default="v1.0.0")
    parser.add_argument("--source", default="transfermarkt_features_v13a")
    args = parser.parse_args()

    metadata = build_metadata(
        snapshot_path=Path(args.snapshot),
        snapshot_audit_path=Path(args.snapshot_audit),
        apply_summary_path=Path(args.apply_summary),
        output_path=Path(args.output),
        snapshot_version=args.snapshot_version,
        source=args.source,
    )

    print("=" * 100)
    print("CURRENT PLAYER SNAPSHOT METADATA")
    print("=" * 100)
    print(json.dumps(metadata, indent=2, ensure_ascii=False))
    print(f"\n[OK] Metadata: {Path(args.output).resolve()}")


if __name__ == "__main__":
    main()
