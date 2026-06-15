"""
TM.6.7 — Current Performance Snapshot (FBref)

Builds a governed latest-performance layer from FBref-derived processed datasets.

Outputs:
- reports/data_quality/tm6_7_fbref_current_performance_audit.json
- reports/data_quality/tm6_7_fbref_current_performance_audit.csv
- data/processed/current_performance_snapshot.parquet
- data/processed/current_performance_snapshot.csv
- data/processed/current_performance_snapshot_metadata.json
- reports/data_quality/current_performance_snapshot_health_report.json
- reports/data_quality/current_performance_snapshot_health_report.md
- reports/data_quality/current_performance_snapshot_apply/current_performance_snapshot_apply_summary.json

Methodological rule:
- This script never overwrites historical player-season variables.
- Current/latest-performance columns are written with current_* names.
- Existing season-context columns are preserved and, when useful, copied to season_context_*.
"""

from __future__ import annotations

import argparse
import json
import re
import shutil
import unicodedata
from dataclasses import dataclass
from datetime import date, datetime
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd

SNAPSHOT_VERSION = "v1.0.0"
SPRINT = "TM.6.7"
GOVERNANCE_NOTE = (
    "Current performance snapshot is a latest-available FBref layer for DSS context. "
    "It must not be used to overwrite historical player-season training variables."
)

SOURCE_CANDIDATES = [
    "player_season_modeling_v13b_productive_candidate.parquet",
    "player_season_modeling_v13b_advanced.parquet",
    "player_role_dss.parquet",
    "player_role_features_advanced.parquet",
    "player_season_modeling_v13a.parquet",
    "fbref_features_v13a.parquet",
]

TARGET_DATASETS = {
    "dss": "reports/dss/global_prospect_universe.csv",
    "portfolio": "reports/strategy/transfer_portfolio_dataset.csv",
    "contract": "reports/tm3_contract_intelligence/contract_intelligence_dataset.csv",
}

PERFORMANCE_FEATURE_MAP = {
    "current_minutes": ["minutes_played", "minutes", "Playing Time_Min", "Min", "min"],
    "current_goals": ["goals", "Standard_Gls", "Gls"],
    "current_assists": ["assists", "Standard_Ast", "Ast"],
    "current_xg": ["xg", "Expected_xG", "Performance_xG", "xG"],
    "current_xag": ["xag", "Expected_xAG", "xAG"],
    "current_npxg": ["npxg", "Expected_npxG", "npxG"],
    "current_progressive_passes": ["progressive_passes", "PrgP", "Passing_PrgP"],
    "current_progressive_carries": ["progressive_carries", "PrgC", "Carries_PrgC"],
    "current_key_passes": ["key_passes", "KP", "Passing_KP"],
    "current_sca": ["sca", "SCA", "SCA_SCA"],
    "current_gca": ["gca", "GCA", "GCA_GCA"],
    "current_aerials_won": ["aerials_won", "Aerial Duels_Won", "Aerials_Won"],
    "current_availability_index": ["availability_index"],
    "current_finishing_index": ["finishing_index_v2", "finishing_index"],
    "current_defensive_activity_index": ["defensive_activity_index"],
}

DEF_ACTION_CANDIDATES = [
    "tackles", "Tackles_Tkl", "interceptions", "Int", "blocks", "Blocks_Blocks",
    "tackles_per90", "interceptions_per90", "blocks_per90"
]

ID_COL_CANDIDATES = ["player_id_tm", "tm_player_id", "player_id"]
NAME_COL_CANDIDATES = ["player_name_fbref", "player_name", "player", "name"]
TEAM_COL_CANDIDATES = ["team", "club", "squad", "current_team"]
LEAGUE_COL_CANDIDATES = ["league", "competition", "comp"]
SEASON_COL_CANDIDATES = ["season", "season_name", "Season"]
ROLE_COL_CANDIDATES = ["primary_role", "current_role", "role", "role_label"]


def find_project_root() -> Path:
    current = Path(__file__).resolve()
    for candidate in [current.parent, *current.parents]:
        if (candidate / "data" / "processed").exists() or (candidate / "reports").exists():
            return candidate
    return Path.cwd()


def normalize_name(value: Any) -> str:
    if pd.isna(value):
        return ""
    text = str(value).strip().lower()
    text = unicodedata.normalize("NFKD", text).encode("ascii", "ignore").decode("ascii")
    text = re.sub(r"[^a-z0-9 ]+", " ", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text


def season_start_year(value: Any) -> int | None:
    if pd.isna(value):
        return None
    text = str(value)
    matches = re.findall(r"(20\d{2}|19\d{2}|\d{4})", text)
    if matches:
        return int(matches[0])
    short = re.findall(r"(\d{2})(\d{2})", text)
    if short:
        return int("20" + short[0][0])
    return None


def pick_col(df: pd.DataFrame, candidates: list[str]) -> str | None:
    lower_map = {c.lower(): c for c in df.columns}
    for candidate in candidates:
        if candidate in df.columns:
            return candidate
        if candidate.lower() in lower_map:
            return lower_map[candidate.lower()]
    return None


def first_existing(df: pd.DataFrame, candidates: list[str]) -> pd.Series:
    for col in candidates:
        if col in df.columns:
            return df[col]
    return pd.Series([np.nan] * len(df), index=df.index)


def safe_num(s: pd.Series) -> pd.Series:
    return pd.to_numeric(s, errors="coerce")


def latest_source(processed_path: Path) -> Path:
    for name in SOURCE_CANDIDATES:
        path = processed_path / name
        if path.exists():
            return path
    available = sorted(processed_path.glob("*.parquet"))
    raise FileNotFoundError(
        "No FBref/modeling parquet source found. Checked: "
        + ", ".join(SOURCE_CANDIDATES)
        + f". Available parquet files: {[p.name for p in available]}"
    )


def read_source(path: Path) -> pd.DataFrame:
    if path.suffix.lower() == ".parquet":
        return pd.read_parquet(path)
    if path.suffix.lower() == ".csv":
        return pd.read_csv(path)
    raise ValueError(f"Unsupported source format: {path}")


def audit_fbref_source(df: pd.DataFrame, source_path: Path, reports_path: Path) -> dict[str, Any]:
    season_col = pick_col(df, SEASON_COL_CANDIDATES)
    league_col = pick_col(df, LEAGUE_COL_CANDIDATES)
    team_col = pick_col(df, TEAM_COL_CANDIDATES)
    name_col = pick_col(df, NAME_COL_CANDIDATES)
    id_col = pick_col(df, ID_COL_CANDIDATES)

    work = df.copy()
    if season_col:
        work["_season_start_year"] = work[season_col].map(season_start_year)
        latest_season_value = work.sort_values("_season_start_year", na_position="first")[season_col].dropna().iloc[-1] if work[season_col].notna().any() else None
    else:
        latest_season_value = None

    key_cols = [c for c in [name_col, season_col, team_col] if c]
    dup_count = int(work.duplicated(key_cols).sum()) if key_cols else None

    advanced_cols = []
    for cols in PERFORMANCE_FEATURE_MAP.values():
        advanced_cols.extend([c for c in cols if c in df.columns])
    advanced_cols = sorted(set(advanced_cols))

    missing_rows = []
    for col in df.columns:
        na = int(df[col].isna().sum())
        missing_rows.append({
            "column": col,
            "missing_count": na,
            "missing_pct": round(100 * na / max(len(df), 1), 4),
            "dtype": str(df[col].dtype),
        })
    missing_df = pd.DataFrame(missing_rows).sort_values(["missing_pct", "column"], ascending=[False, True])

    audit = {
        "sprint": SPRINT,
        "audit_date": date.today().isoformat(),
        "source_dataset": str(source_path.as_posix()),
        "rows": int(len(df)),
        "columns_total": int(df.shape[1]),
        "columns": list(map(str, df.columns)),
        "id_column": id_col,
        "name_column": name_col,
        "season_column": season_col,
        "team_column": team_col,
        "league_column": league_col,
        "seasons_available": sorted(map(str, df[season_col].dropna().unique())) if season_col else [],
        "latest_performance_season": str(latest_season_value) if latest_season_value is not None else None,
        "leagues_total": int(df[league_col].dropna().nunique()) if league_col else None,
        "leagues": sorted(map(str, df[league_col].dropna().unique())) if league_col else [],
        "players_unique_by_id": int(df[id_col].dropna().nunique()) if id_col else None,
        "players_unique_by_name": int(df[name_col].dropna().nunique()) if name_col else None,
        "duplicate_player_season_team_rows": dup_count,
        "available_performance_features": advanced_cols,
        "feature_availability": {
            out_col: next((c for c in candidates if c in df.columns), None)
            for out_col, candidates in PERFORMANCE_FEATURE_MAP.items()
        },
        "missingness_top_30": missing_df.head(30).to_dict(orient="records"),
        "key_stability": {
            "has_player_id_tm": bool(id_col == "player_id_tm"),
            "has_any_id": bool(id_col),
            "has_normalizable_name": bool(name_col),
            "has_season": bool(season_col),
            "has_team": bool(team_col),
            "has_league": bool(league_col),
        },
    }

    reports_path.mkdir(parents=True, exist_ok=True)
    (reports_path / "tm6_7_fbref_current_performance_audit.json").write_text(
        json.dumps(audit, indent=2, ensure_ascii=False), encoding="utf-8"
    )
    missing_df.to_csv(reports_path / "tm6_7_fbref_current_performance_audit.csv", index=False)
    return audit


def build_snapshot(df: pd.DataFrame, source_path: Path, processed_path: Path) -> pd.DataFrame:
    id_col = pick_col(df, ID_COL_CANDIDATES)
    name_col = pick_col(df, NAME_COL_CANDIDATES)
    team_col = pick_col(df, TEAM_COL_CANDIDATES)
    league_col = pick_col(df, LEAGUE_COL_CANDIDATES)
    season_col = pick_col(df, SEASON_COL_CANDIDATES)
    role_col = pick_col(df, ROLE_COL_CANDIDATES)

    if not name_col or not season_col:
        raise ValueError("Cannot build snapshot without a player name column and a season column.")

    work = df.copy()
    work["_season_start_year"] = work[season_col].map(season_start_year)
    latest_year = work["_season_start_year"].max()
    latest = work[work["_season_start_year"] == latest_year].copy()

    # Deduplicate at player level. Keep the row with the highest minutes where available.
    minutes_source = first_existing(latest, PERFORMANCE_FEATURE_MAP["current_minutes"])
    latest["_minutes_sort"] = safe_num(minutes_source).fillna(-1)
    latest["player_name_norm"] = latest[name_col].map(normalize_name)

    sort_cols = ["player_name_norm", "_minutes_sort"]
    if id_col:
        sort_cols = [id_col, "_minutes_sort"]
    latest = latest.sort_values(sort_cols, ascending=[True, False])
    dedup_key = id_col if id_col else "player_name_norm"
    latest = latest.drop_duplicates(subset=[dedup_key], keep="first")

    snap = pd.DataFrame(index=latest.index)
    snap["player_id_tm"] = latest[id_col] if id_col else np.nan
    snap["player_name_fbref"] = latest[name_col]
    snap["player_name_norm"] = latest["player_name_norm"]
    snap["current_performance_season"] = latest[season_col]
    snap["current_performance_team"] = latest[team_col] if team_col else np.nan
    snap["current_performance_league"] = latest[league_col] if league_col else np.nan

    for out_col, candidates in PERFORMANCE_FEATURE_MAP.items():
        snap[out_col] = first_existing(latest, candidates)

    def_action_existing = [c for c in DEF_ACTION_CANDIDATES if c in latest.columns]
    if def_action_existing:
        snap["current_defensive_actions"] = latest[def_action_existing].apply(pd.to_numeric, errors="coerce").sum(axis=1, min_count=1)
    else:
        snap["current_defensive_actions"] = np.nan

    snap["current_role"] = latest[role_col] if role_col else np.nan
    snap["snapshot_date"] = date.today().isoformat()
    snap["source_dataset"] = source_path.name

    preferred_order = [
        "player_id_tm", "player_name_fbref", "player_name_norm",
        "current_performance_season", "current_performance_team", "current_performance_league",
        "current_minutes", "current_goals", "current_assists", "current_xg", "current_xag", "current_npxg",
        "current_progressive_passes", "current_progressive_carries", "current_key_passes",
        "current_sca", "current_gca", "current_defensive_actions", "current_aerials_won",
        "current_availability_index", "current_finishing_index", "current_defensive_activity_index",
        "current_role", "snapshot_date", "source_dataset",
    ]
    snap = snap[[c for c in preferred_order if c in snap.columns]]

    processed_path.mkdir(parents=True, exist_ok=True)
    snap.to_parquet(processed_path / "current_performance_snapshot.parquet", index=False)
    snap.to_csv(processed_path / "current_performance_snapshot.csv", index=False)
    return snap


def add_season_context_columns(df: pd.DataFrame) -> pd.DataFrame:
    out = df.copy()
    context_map = {
        "minutes_played": "season_context_minutes",
        "minutes": "season_context_minutes",
        "team": "season_context_team",
        "club": "season_context_team",
        "league": "season_context_league",
    }
    for src, dst in context_map.items():
        if src in out.columns and dst not in out.columns:
            out[dst] = out[src]
    return out


def apply_snapshot_to_dataset(dataset_path: Path, snapshot: pd.DataFrame, dry_run: bool = False) -> dict[str, Any]:
    if not dataset_path.exists():
        return {"dataset": str(dataset_path), "exists": False}

    target = pd.read_csv(dataset_path)
    target = add_season_context_columns(target)

    if "player_name_norm" not in target.columns:
        name_col = pick_col(target, NAME_COL_CANDIDATES)
        if name_col:
            target["player_name_norm"] = target[name_col].map(normalize_name)

    snap = snapshot.copy()
    snap_id = snap[snap["player_id_tm"].notna()].drop_duplicates("player_id_tm") if "player_id_tm" in snap.columns else pd.DataFrame()
    snap_name_counts = snap["player_name_norm"].value_counts(dropna=True) if "player_name_norm" in snap.columns else pd.Series(dtype=int)
    unique_names = set(snap_name_counts[snap_name_counts == 1].index)
    snap_name = snap[snap["player_name_norm"].isin(unique_names)].drop_duplicates("player_name_norm") if "player_name_norm" in snap.columns else pd.DataFrame()

    current_cols = [c for c in snapshot.columns if c.startswith("current_") or c in ["snapshot_date", "source_dataset"]]
    before_cols = set(target.columns)
    result = target.copy()
    result["performance_snapshot_match_key"] = "unmatched"

    matched_id = pd.Series(False, index=result.index)
    if "player_id_tm" in result.columns and not snap_id.empty:
        merge_cols = ["player_id_tm"] + current_cols
        merged = result[["player_id_tm"]].merge(snap_id[merge_cols], on="player_id_tm", how="left", indicator=True)
        matched_id = merged["_merge"].eq("both")
        for col in current_cols:
            result.loc[matched_id, col] = merged.loc[matched_id, col].values
        result.loc[matched_id, "performance_snapshot_match_key"] = "player_id_tm"

    matched_name = pd.Series(False, index=result.index)
    if "player_name_norm" in result.columns and not snap_name.empty:
        remaining = ~matched_id
        merged_name = result.loc[remaining, ["player_name_norm"]].merge(
            snap_name[["player_name_norm"] + current_cols], on="player_name_norm", how="left", indicator=True
        )
        matched_name_idx = result.loc[remaining].index[merged_name["_merge"].eq("both").to_numpy()]
        matched_name.loc[matched_name_idx] = True
        for col in current_cols:
            result.loc[matched_name_idx, col] = merged_name.loc[merged_name["_merge"].eq("both"), col].values
        result.loc[matched_name_idx, "performance_snapshot_match_key"] = "player_name_norm_unique"

    matched_total = int((matched_id | matched_name).sum())
    coverage = round(100 * matched_total / max(len(result), 1), 4)

    backup_path = dataset_path.with_suffix(dataset_path.suffix + f".tm6_7_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}")
    if not dry_run:
        shutil.copy2(dataset_path, backup_path)
        result.to_csv(dataset_path, index=False)

    return {
        "dataset": str(dataset_path),
        "exists": True,
        "rows": int(len(result)),
        "matched_total": matched_total,
        "matched_by_player_id_tm": int(matched_id.sum()),
        "matched_by_player_name_norm_unique": int(matched_name.sum()),
        "coverage_pct": coverage,
        "new_columns": sorted(set(result.columns) - before_cols),
        "backup_path": str(backup_path) if not dry_run else None,
    }


def build_metadata(snapshot: pd.DataFrame, source_path: Path, apply_summary: dict[str, Any], processed_path: Path) -> dict[str, Any]:
    coverage = {k: v.get("coverage_pct") for k, v in apply_summary.get("datasets", {}).items() if v.get("exists")}
    feature_groups = {
        "volume": ["current_minutes", "current_availability_index"],
        "attacking_output": ["current_goals", "current_assists", "current_xg", "current_xag", "current_npxg", "current_finishing_index"],
        "progression_creation": ["current_progressive_passes", "current_progressive_carries", "current_key_passes", "current_sca", "current_gca"],
        "defensive_aerial": ["current_defensive_actions", "current_defensive_activity_index", "current_aerials_won"],
        "role_context": ["current_role"],
    }
    metadata = {
        "snapshot_version": SNAPSHOT_VERSION,
        "snapshot_date": date.today().isoformat(),
        "source": source_path.name,
        "latest_performance_season": str(snapshot["current_performance_season"].dropna().iloc[0]) if "current_performance_season" in snapshot.columns and snapshot["current_performance_season"].notna().any() else None,
        "players_total": int(len(snapshot)),
        "leagues_total": int(snapshot["current_performance_league"].dropna().nunique()) if "current_performance_league" in snapshot.columns else None,
        "coverage_dss_pct": coverage.get("dss"),
        "coverage_contract_pct": coverage.get("contract"),
        "coverage_portfolio_pct": coverage.get("portfolio"),
        "match_key": "player_id_tm",
        "fallback_match_key": "player_name_norm_unique_only",
        "feature_groups": feature_groups,
        "governance_note": GOVERNANCE_NOTE,
    }
    (processed_path / "current_performance_snapshot_metadata.json").write_text(
        json.dumps(metadata, indent=2, ensure_ascii=False), encoding="utf-8"
    )
    return metadata


def build_health_report(snapshot: pd.DataFrame, metadata: dict[str, Any], apply_summary: dict[str, Any], reports_path: Path) -> dict[str, Any]:
    key_features = [
        "current_minutes", "current_goals", "current_assists", "current_xg", "current_xag",
        "current_progressive_passes", "current_progressive_carries", "current_key_passes",
        "current_sca", "current_gca", "current_defensive_actions", "current_availability_index",
        "current_finishing_index", "current_defensive_activity_index",
    ]
    feature_availability = {}
    missingness = {}
    for col in key_features:
        if col in snapshot.columns:
            non_null = int(snapshot[col].notna().sum())
            feature_availability[col] = round(100 * non_null / max(len(snapshot), 1), 4)
            missingness[col] = round(100 - feature_availability[col], 4)
        else:
            feature_availability[col] = 0.0
            missingness[col] = 100.0

    coverage_values = [v.get("coverage_pct", 0) for v in apply_summary.get("datasets", {}).values() if v.get("exists")]
    coverage_score = min(100.0, np.mean(coverage_values) if coverage_values else 0.0)
    feature_score = np.mean(list(feature_availability.values())) if feature_availability else 0.0

    latest = metadata.get("latest_performance_season")
    latest_year = season_start_year(latest)
    current_year = date.today().year
    # Football seasons: a latest season starting previous calendar year can still be current/acceptable.
    staleness_years = None if latest_year is None else max(0, current_year - latest_year)
    if staleness_years is None:
        staleness_score = 50
        staleness_status = "YELLOW"
    elif staleness_years <= 1:
        staleness_score = 100
        staleness_status = "GREEN"
    elif staleness_years == 2:
        staleness_score = 70
        staleness_status = "YELLOW"
    else:
        staleness_score = 35
        staleness_status = "RED"

    homonym_count = int(snapshot["player_name_norm"].duplicated(keep=False).sum()) if "player_name_norm" in snapshot.columns else 0
    homonym_rate = round(100 * homonym_count / max(len(snapshot), 1), 4)
    homonym_score = max(0, 100 - homonym_rate * 2)

    score = round(0.35 * coverage_score + 0.25 * feature_score + 0.25 * staleness_score + 0.15 * homonym_score, 2)
    status = "GREEN" if score >= 85 else "YELLOW" if score >= 70 else "RED"

    report = {
        "snapshot_version": metadata.get("snapshot_version"),
        "snapshot_date": metadata.get("snapshot_date"),
        "latest_performance_season": latest,
        "players_total": metadata.get("players_total"),
        "leagues_total": metadata.get("leagues_total"),
        "coverage": {k: v for k, v in apply_summary.get("datasets", {}).items()},
        "coverage_score": round(float(coverage_score), 2),
        "staleness": {
            "latest_performance_season": latest,
            "staleness_years": staleness_years,
            "status": staleness_status,
            "score": staleness_score,
        },
        "missingness": missingness,
        "feature_availability": feature_availability,
        "homonym_risk": {
            "homonym_rows": homonym_count,
            "homonym_rate_pct": homonym_rate,
            "score": round(float(homonym_score), 2),
        },
        "status": status,
        "score": score,
        "governance_note": GOVERNANCE_NOTE,
    }

    reports_path.mkdir(parents=True, exist_ok=True)
    (reports_path / "current_performance_snapshot_health_report.json").write_text(
        json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8"
    )
    md = f"""# TM.6.7 — Current Performance Snapshot Health Report

| Metric | Value |
|---|---:|
| Status | {status} |
| Score | {score} |
| Snapshot date | {metadata.get('snapshot_date')} |
| Latest performance season | {latest} |
| Players | {metadata.get('players_total')} |
| Leagues | {metadata.get('leagues_total')} |
| Coverage score | {round(float(coverage_score), 2)} |
| Feature availability score | {round(float(feature_score), 2)} |
| Homonym rate | {homonym_rate}% |

## Governance note

{GOVERNANCE_NOTE}

## Dataset coverage

"""
    for name, item in apply_summary.get("datasets", {}).items():
        md += f"- **{name}**: {item.get('coverage_pct', 'N/A')}% ({item.get('matched_total', 0)}/{item.get('rows', 0)})\n"
    md += "\n## Key feature availability\n\n"
    for col, val in feature_availability.items():
        md += f"- **{col}**: {val}%\n"
    (reports_path / "current_performance_snapshot_health_report.md").write_text(md, encoding="utf-8")
    return report


def validate_guardrails(health: dict[str, Any], min_score: float, min_coverage: float) -> tuple[bool, list[str]]:
    errors = []
    if health.get("score", 0) < min_score:
        errors.append(f"Health score below guardrail: {health.get('score')} < {min_score}")
    for name, item in health.get("coverage", {}).items():
        if item.get("exists") and item.get("coverage_pct", 0) < min_coverage:
            errors.append(f"Coverage below guardrail for {name}: {item.get('coverage_pct')} < {min_coverage}")
    return len(errors) == 0, errors


def run(dry_run: bool = False, min_score: float = 70.0, min_coverage: float = 60.0) -> dict[str, Any]:
    root = find_project_root()
    processed_path = root / "data" / "processed"
    reports_path = root / "reports" / "data_quality"
    source_path = latest_source(processed_path)

    df = read_source(source_path)
    audit = audit_fbref_source(df, source_path, reports_path)
    snapshot = build_snapshot(df, source_path, processed_path)

    apply_dir = reports_path / "current_performance_snapshot_apply"
    apply_dir.mkdir(parents=True, exist_ok=True)
    dataset_summaries = {}
    for name, rel_path in TARGET_DATASETS.items():
        dataset_summaries[name] = apply_snapshot_to_dataset(root / rel_path, snapshot, dry_run=dry_run)

    apply_summary = {
        "sprint": SPRINT,
        "run_date": date.today().isoformat(),
        "dry_run": dry_run,
        "snapshot_rows": int(len(snapshot)),
        "datasets": dataset_summaries,
    }
    (apply_dir / "current_performance_snapshot_apply_summary.json").write_text(
        json.dumps(apply_summary, indent=2, ensure_ascii=False), encoding="utf-8"
    )

    metadata = build_metadata(snapshot, source_path, apply_summary, processed_path)
    health = build_health_report(snapshot, metadata, apply_summary, reports_path)
    passed, errors = validate_guardrails(health, min_score=min_score, min_coverage=min_coverage)

    result = {
        "status": "PASSED" if passed else "FAILED",
        "guardrail_errors": errors,
        "audit": audit,
        "metadata": metadata,
        "health": health,
        "apply_summary": apply_summary,
    }
    if not passed:
        raise SystemExit(json.dumps(result, indent=2, ensure_ascii=False))
    return result


def main() -> None:
    parser = argparse.ArgumentParser(description="Run TM.6.7 current performance snapshot refresh.")
    parser.add_argument("--dry-run", action="store_true", help="Do not overwrite target DSS CSV files.")
    parser.add_argument("--min-score", type=float, default=70.0, help="Minimum health score required to pass.")
    parser.add_argument("--min-coverage", type=float, default=60.0, help="Minimum dataset coverage percentage required to pass.")
    args = parser.parse_args()
    result = run(dry_run=args.dry_run, min_score=args.min_score, min_coverage=args.min_coverage)
    print(json.dumps({
        "status": result["status"],
        "snapshot": result["metadata"],
        "health_score": result["health"].get("score"),
        "health_status": result["health"].get("status"),
    }, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
