from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2] if "src" in Path(__file__).resolve().parts else Path.cwd()

DEFAULT_CONFIG = ROOT / "config" / "snapshot_config.yaml"
DEFAULT_RAW_DIR = ROOT / "data" / "raw" / "transfermarkt" / "kaggle_player_scores"
DEFAULT_OUTPUT_DIR = ROOT / "data" / "processed"
DEFAULT_AUDIT_DIR = ROOT / "reports" / "data_quality" / "current_snapshot_apply"
DEFAULT_REFRESH_DIR = ROOT / "reports" / "data_quality" / "snapshot_refresh"
DEFAULT_HEALTH_REPORT = ROOT / "reports" / "data_quality" / "snapshot_health_report.json"
DEFAULT_METADATA = ROOT / "data" / "processed" / "current_player_snapshot_metadata.json"
DEFAULT_REGISTRY_DIR = ROOT / "data" / "processed" / "snapshot_registry"

OFFICIAL_SNAPSHOT_FILES = [
    "current_player_snapshot.csv",
    "current_player_snapshot.parquet",
    "current_player_snapshot_audit.json",
    "current_player_snapshot_homonyms.csv",
]


# =============================================================================
# Generic IO helpers
# =============================================================================


def now_tag() -> str:
    return datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")


def as_project_path(path: str | Path) -> Path:
    path = Path(path)
    return path if path.is_absolute() else ROOT / path


def rel(path: Path) -> str:
    try:
        return str(path.relative_to(ROOT))
    except Exception:
        return str(path)


def read_json(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    with path.open("r", encoding="utf-8") as f:
        data = json.load(f)
    return data if isinstance(data, dict) else {"results": data}


def read_yaml_light(path: Path) -> dict[str, Any]:
    """Read YAML config when PyYAML exists; otherwise return an empty dict.

    The refresh pipeline works with safe defaults, so YAML remains a governance
    configuration file rather than a hard runtime dependency.
    """
    if not path.exists():
        return {}
    try:
        import yaml  # type: ignore

        with path.open("r", encoding="utf-8") as f:
            data = yaml.safe_load(f)
        return data if isinstance(data, dict) else {}
    except Exception:
        return {}


def parse_date(value: Any) -> datetime | None:
    if value is None:
        return None
    text = str(value).strip()
    if not text or text.lower() in {"nan", "none", "null"}:
        return None
    try:
        return datetime.fromisoformat(text[:10])
    except Exception:
        return None


def require_file(path: Path, label: str) -> None:
    if not path.exists():
        raise FileNotFoundError(f"Missing {label}: {path}")


def run_step(name: str, cmd: list[str], dry_run: bool = False) -> dict[str, Any]:
    print("\n" + "=" * 100)
    print(f"STEP: {name}")
    print("=" * 100)
    print(" ".join(cmd))

    if dry_run:
        return {"step": name, "status": "dry_run", "command": cmd, "returncode": 0}

    completed = subprocess.run(
        cmd,
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
    )

    if completed.stdout:
        print(completed.stdout)
    if completed.stderr:
        print(completed.stderr, file=sys.stderr)

    status = "ok" if completed.returncode == 0 else "failed"
    return {
        "step": name,
        "status": status,
        "command": cmd,
        "returncode": int(completed.returncode),
        "stdout_tail": completed.stdout[-4000:] if completed.stdout else "",
        "stderr_tail": completed.stderr[-4000:] if completed.stderr else "",
    }




def load_best_approved_snapshot_registry(registry_dir: Path) -> dict[str, Any]:
    """Load the best approved snapshot baseline from the registry.

    The registry protects the refresh pipeline from validating new candidates
    against an already-degraded current snapshot. Ranking is intentionally
    conservative: latest valuation date first, then player coverage, then score.
    """
    records: list[dict[str, Any]] = []
    latest = read_json(registry_dir / "latest_approved_snapshot.json")
    if latest:
        latest["registry_path"] = rel(registry_dir / "latest_approved_snapshot.json")
        records.append(latest)
    if registry_dir.exists():
        for path in registry_dir.glob("approved_snapshot_*.json"):
            item = read_json(path)
            if item:
                item["registry_path"] = rel(path)
                records.append(item)

    approved = [r for r in records if str(r.get("status", "approved")).lower() == "approved"]
    if not approved:
        return {}

    def key(record: dict[str, Any]) -> tuple[str, int, float]:
        return (
            str(record.get("latest_valuation_date") or ""),
            as_int(record.get("players_total"), 0),
            as_float(record.get("snapshot_score"), 0.0),
        )

    return sorted(approved, key=key, reverse=True)[0]

# =============================================================================
# Snapshot guardrails
# =============================================================================


def get_nested(data: dict[str, Any], *keys: str, default: Any = None) -> Any:
    current: Any = data
    for key in keys:
        if not isinstance(current, dict) or key not in current:
            return default
        current = current[key]
    return current


def as_float(value: Any, default: float = 0.0) -> float:
    try:
        if value is None or value == "":
            return default
        return float(value)
    except Exception:
        return default


def as_int(value: Any, default: int = 0) -> int:
    try:
        if value is None or value == "":
            return default
        return int(float(value))
    except Exception:
        return default


def snapshot_metrics_from_metadata(metadata: dict[str, Any]) -> dict[str, Any]:
    return {
        "latest_valuation_date": metadata.get("latest_valuation_date"),
        "players_total": metadata.get("players_total"),
        "leagues_total": metadata.get("leagues_total"),
        "homonym_names": metadata.get("homonym_names"),
        "dss_pct": get_nested(metadata, "coverage", "dss_pct"),
        "contract_pct": get_nested(metadata, "coverage", "contract_pct"),
        "portfolio_pct": get_nested(metadata, "coverage", "portfolio_pct"),
    }


def snapshot_metrics_from_audit(audit: dict[str, Any]) -> dict[str, Any]:
    return {
        "latest_valuation_date": audit.get("current_valuation_date_max"),
        "players_total": audit.get("players_unique") or audit.get("rows"),
        "leagues_total": audit.get("leagues_unique"),
        "homonym_names": audit.get("homonym_names"),
        "market_value_min": audit.get("market_value_min"),
        "market_value_max": audit.get("market_value_max"),
        "leagues": audit.get("leagues"),
    }


def default_guardrails(cfg: dict[str, Any]) -> dict[str, Any]:
    raw = cfg.get("guardrails", {}) if isinstance(cfg.get("guardrails"), dict) else {}
    thresholds = cfg.get("thresholds", {}) if isinstance(cfg.get("thresholds"), dict) else {}

    return {
        "enabled": bool(raw.get("enabled", True)),
        "reject_older_valuation_date": bool(raw.get("reject_older_valuation_date", True)),
        "reject_player_count_drop": bool(raw.get("reject_player_count_drop", True)),
        "reject_league_count_drop": bool(raw.get("reject_league_count_drop", True)),
        "max_player_drop_pct": as_float(raw.get("max_player_drop_pct", 0.0), 0.0),
        "min_latest_valuation_date": raw.get("min_latest_valuation_date"),
        "min_players_total": raw.get("min_players_total"),
        "min_leagues_total": raw.get("min_leagues_total", thresholds.get("min_leagues_total", 9)),
        "min_snapshot_score": as_float(raw.get("min_snapshot_score", 90.0), 90.0),
        "min_snapshot_status": raw.get("min_snapshot_status", "GREEN"),
    }


def evaluate_candidate_guardrails(
    baseline_metadata: dict[str, Any],
    candidate_audit: dict[str, Any],
    guardrails: dict[str, Any],
) -> dict[str, Any]:
    """Reject candidate snapshots that degrade the official data layer.

    Candidate validation happens before promotion/apply. This prevents the official
    snapshot, DSS reports and metadata from being overwritten by an older or less
    complete data source.
    """
    baseline = snapshot_metrics_from_metadata(baseline_metadata)
    candidate = snapshot_metrics_from_audit(candidate_audit)
    checks: list[dict[str, Any]] = []

    enabled = bool(guardrails.get("enabled", True))
    accepted = True

    def add_check(name: str, status: str, message: str, severity: str = "error", **extra: Any) -> None:
        nonlocal accepted
        checks.append({"name": name, "status": status, "severity": severity, "message": message, **extra})
        if enabled and severity == "error" and status == "fail":
            accepted = False

    # 1) Latest valuation date must not regress.
    baseline_date = parse_date(baseline.get("latest_valuation_date"))
    candidate_date = parse_date(candidate.get("latest_valuation_date"))
    min_date = parse_date(guardrails.get("min_latest_valuation_date"))

    if guardrails.get("reject_older_valuation_date", True) and baseline_date and candidate_date:
        if candidate_date < baseline_date:
            add_check(
                "valuation_date_regression",
                "fail",
                "Candidate latest valuation date is older than current official snapshot.",
                baseline=str(baseline.get("latest_valuation_date")),
                candidate=str(candidate.get("latest_valuation_date")),
            )
        else:
            add_check(
                "valuation_date_regression",
                "pass",
                "Candidate latest valuation date is not older than current official snapshot.",
                severity="info",
                baseline=str(baseline.get("latest_valuation_date")),
                candidate=str(candidate.get("latest_valuation_date")),
            )

    if min_date and candidate_date:
        if candidate_date < min_date:
            add_check(
                "min_latest_valuation_date",
                "fail",
                "Candidate latest valuation date is below the configured minimum acceptable date.",
                configured_min=str(guardrails.get("min_latest_valuation_date")),
                candidate=str(candidate.get("latest_valuation_date")),
            )
        else:
            add_check(
                "min_latest_valuation_date",
                "pass",
                "Candidate latest valuation date meets configured minimum date.",
                severity="info",
                configured_min=str(guardrails.get("min_latest_valuation_date")),
                candidate=str(candidate.get("latest_valuation_date")),
            )

    # 2) Player coverage must not regress beyond tolerance.
    baseline_players = as_int(baseline.get("players_total"), 0)
    candidate_players = as_int(candidate.get("players_total"), 0)
    max_drop_pct = as_float(guardrails.get("max_player_drop_pct", 0.0), 0.0)
    min_players_total_cfg = guardrails.get("min_players_total")
    min_players_total = as_int(min_players_total_cfg, 0) if min_players_total_cfg is not None else None

    if guardrails.get("reject_player_count_drop", True) and baseline_players and candidate_players:
        allowed_min = int(round(baseline_players * (1 - max_drop_pct / 100.0)))
        if candidate_players < allowed_min:
            add_check(
                "player_coverage_regression",
                "fail",
                "Candidate player coverage is below current official snapshot tolerance.",
                baseline=baseline_players,
                candidate=candidate_players,
                allowed_min=allowed_min,
                max_drop_pct=max_drop_pct,
            )
        else:
            add_check(
                "player_coverage_regression",
                "pass",
                "Candidate player coverage is within tolerance.",
                severity="info",
                baseline=baseline_players,
                candidate=candidate_players,
                allowed_min=allowed_min,
                max_drop_pct=max_drop_pct,
            )

    if min_players_total is not None:
        if candidate_players < min_players_total:
            add_check(
                "min_players_total",
                "fail",
                "Candidate player coverage is below configured minimum.",
                configured_min=min_players_total,
                candidate=candidate_players,
            )
        else:
            add_check(
                "min_players_total",
                "pass",
                "Candidate player coverage meets configured minimum.",
                severity="info",
                configured_min=min_players_total,
                candidate=candidate_players,
            )

    # 3) League scope must not regress.
    baseline_leagues = as_int(baseline.get("leagues_total"), 0)
    candidate_leagues = as_int(candidate.get("leagues_total"), 0)
    min_leagues_total = as_int(guardrails.get("min_leagues_total"), 0)

    if guardrails.get("reject_league_count_drop", True) and baseline_leagues and candidate_leagues:
        if candidate_leagues < baseline_leagues:
            add_check(
                "league_scope_regression",
                "fail",
                "Candidate league scope is smaller than current official snapshot.",
                baseline=baseline_leagues,
                candidate=candidate_leagues,
            )
        else:
            add_check(
                "league_scope_regression",
                "pass",
                "Candidate league scope is not smaller than current official snapshot.",
                severity="info",
                baseline=baseline_leagues,
                candidate=candidate_leagues,
            )

    if min_leagues_total:
        if candidate_leagues < min_leagues_total:
            add_check(
                "min_leagues_total",
                "fail",
                "Candidate league scope is below configured minimum.",
                configured_min=min_leagues_total,
                candidate=candidate_leagues,
            )
        else:
            add_check(
                "min_leagues_total",
                "pass",
                "Candidate league scope meets configured minimum.",
                severity="info",
                configured_min=min_leagues_total,
                candidate=candidate_leagues,
            )

    return {
        "accepted": bool(accepted),
        "enabled": enabled,
        "baseline": baseline,
        "candidate": candidate,
        "guardrails": guardrails,
        "checks": checks,
    }


def backup_official_snapshot(output_dir: Path, refresh_dir: Path, run_id: str) -> Path:
    backup_dir = refresh_dir / f"official_snapshot_before_{run_id}"
    backup_dir.mkdir(parents=True, exist_ok=True)
    for name in OFFICIAL_SNAPSHOT_FILES:
        src = output_dir / name
        if src.exists():
            shutil.copy2(src, backup_dir / name)
    return backup_dir


def promote_candidate_snapshot(candidate_dir: Path, output_dir: Path) -> list[dict[str, str]]:
    output_dir.mkdir(parents=True, exist_ok=True)
    promoted: list[dict[str, str]] = []
    for name in OFFICIAL_SNAPSHOT_FILES:
        src = candidate_dir / name
        dst = output_dir / name
        if src.exists():
            shutil.copy2(src, dst)
            promoted.append({"source": rel(src), "destination": rel(dst)})
    return promoted


# =============================================================================
# Command construction
# =============================================================================


def build_candidate_command(args: argparse.Namespace, candidate_dir: Path) -> tuple[str, list[str]]:
    raw_dir = as_project_path(args.raw_dir or DEFAULT_RAW_DIR)
    return (
        "build_candidate_snapshot",
        [
            sys.executable,
            str(ROOT / "src" / "dss" / "build_current_player_snapshot.py"),
            "--raw-dir",
            rel(raw_dir),
            "--output-dir",
            rel(candidate_dir),
            "--scope",
            args.scope,
        ],
    )


def build_apply_metadata_health_commands(args: argparse.Namespace, cfg: dict[str, Any]) -> list[tuple[str, list[str]]]:
    snapshot_cfg = cfg.get("snapshot", {}) if isinstance(cfg.get("snapshot"), dict) else {}

    output_dir = as_project_path(args.output_dir or DEFAULT_OUTPUT_DIR)
    audit_dir = as_project_path(args.audit_dir or DEFAULT_AUDIT_DIR)
    snapshot_path = output_dir / "current_player_snapshot.parquet"
    snapshot_audit = output_dir / "current_player_snapshot_audit.json"
    apply_summary = audit_dir / "current_snapshot_apply_summary.json"
    metadata_path = as_project_path(args.metadata_output or DEFAULT_METADATA)
    registry_dir = as_project_path(args.registry_dir or DEFAULT_REGISTRY_DIR)

    snapshot_version = args.snapshot_version or snapshot_cfg.get("snapshot_version") or "v1.0.0"
    source = args.source or snapshot_cfg.get("source_dataset") or "transfermarkt_features_v13a"

    commands: list[tuple[str, list[str]]] = []

    if not args.skip_apply:
        apply_cmd = [
            sys.executable,
            str(ROOT / "src" / "dss" / "apply_current_player_snapshot.py"),
            "--snapshot",
            rel(snapshot_path),
            "--audit-dir",
            rel(audit_dir),
        ]
        if args.no_backup:
            apply_cmd.append("--no-backup")
        commands.append(("apply_snapshot", apply_cmd))

    if not args.skip_metadata:
        commands.append(
            (
                "build_metadata",
                [
                    sys.executable,
                    str(ROOT / "src" / "dss" / "build_current_player_snapshot_metadata.py"),
                    "--snapshot",
                    rel(snapshot_path),
                    "--snapshot-audit",
                    rel(snapshot_audit),
                    "--apply-summary",
                    rel(apply_summary),
                    "--output",
                    rel(metadata_path),
                    "--snapshot-version",
                    snapshot_version,
                    "--source",
                    source,
                ],
            )
        )

    if not args.skip_health:
        commands.append(
            (
                "build_health_report",
                [sys.executable, str(ROOT / "src" / "dss" / "build_snapshot_health_report.py")],
            )
        )

    return commands


# =============================================================================
# Main
# =============================================================================


def main() -> None:
    parser = argparse.ArgumentParser(
        description="TM.6.6c official refresh pipeline for current_player_snapshot governance with guardrails."
    )
    parser.add_argument("--config", default=str(DEFAULT_CONFIG))
    parser.add_argument("--raw-dir", default=str(DEFAULT_RAW_DIR.relative_to(ROOT)))
    parser.add_argument("--output-dir", default=str(DEFAULT_OUTPUT_DIR.relative_to(ROOT)))
    parser.add_argument("--audit-dir", default=str(DEFAULT_AUDIT_DIR.relative_to(ROOT)))
    parser.add_argument("--metadata-output", default=str(DEFAULT_METADATA.relative_to(ROOT)))
    parser.add_argument("--registry-dir", default=str(DEFAULT_REGISTRY_DIR.relative_to(ROOT)))
    parser.add_argument("--ignore-registry", action="store_true", help="Use current metadata as baseline instead of the approved snapshot registry. Not recommended.")
    parser.add_argument("--candidate-dir", default="", help="Optional candidate output directory. Defaults to reports/data_quality/snapshot_refresh/candidate_<run_id>.")
    parser.add_argument("--scope", choices=["productive", "full"], default="productive")
    parser.add_argument("--snapshot-version", default="v1.0.0")
    parser.add_argument("--source", default="transfermarkt_features_v13a")
    parser.add_argument("--no-backup", action="store_true", help="Do not backup DSS target files before applying snapshot.")
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--fail-on-warning", action="store_true", help="Exit non-zero when final snapshot status is not GREEN.")
    parser.add_argument("--skip-build", action="store_true")
    parser.add_argument("--skip-apply", action="store_true")
    parser.add_argument("--skip-metadata", action="store_true")
    parser.add_argument("--skip-health", action="store_true")
    parser.add_argument("--disable-guardrails", action="store_true", help="Emergency override. Not recommended for release builds.")
    parser.add_argument("--allow-older-valuation", action="store_true", help="Emergency override for older valuation date guardrail.")
    parser.add_argument("--allow-player-drop", action="store_true", help="Emergency override for player coverage regression guardrail.")
    args = parser.parse_args()

    run_id = now_tag()
    config_path = as_project_path(args.config)
    cfg = read_yaml_light(config_path)
    refresh_dir = DEFAULT_REFRESH_DIR
    refresh_dir.mkdir(parents=True, exist_ok=True)

    output_dir = as_project_path(args.output_dir or DEFAULT_OUTPUT_DIR)
    metadata_path = as_project_path(args.metadata_output or DEFAULT_METADATA)
    registry_dir = as_project_path(args.registry_dir or DEFAULT_REGISTRY_DIR)
    candidate_dir = as_project_path(args.candidate_dir) if args.candidate_dir else refresh_dir / f"candidate_{run_id}"

    guardrails = default_guardrails(cfg)
    if args.disable_guardrails:
        guardrails["enabled"] = False
    if args.allow_older_valuation:
        guardrails["reject_older_valuation_date"] = False
    if args.allow_player_drop:
        guardrails["reject_player_count_drop"] = False

    print("=" * 100)
    print("TM.6.6C — OFFICIAL CURRENT SNAPSHOT REFRESH PIPELINE WITH GUARDRAILS")
    print("=" * 100)
    print(json.dumps({
        "run_id": run_id,
        "root": str(ROOT),
        "config": rel(config_path),
        "scope": args.scope,
        "dry_run": bool(args.dry_run),
        "candidate_dir": rel(candidate_dir),
        "guardrails_enabled": bool(guardrails.get("enabled", True)),
        "registry_dir": rel(registry_dir),
        "ignore_registry": bool(args.ignore_registry),
    }, indent=2, ensure_ascii=False))

    for script_name in [
        "build_current_player_snapshot.py",
        "apply_current_player_snapshot.py",
        "build_current_player_snapshot_metadata.py",
        "build_snapshot_health_report.py",
    ]:
        require_file(ROOT / "src" / "dss" / script_name, script_name)

    current_metadata = read_json(metadata_path)
    registry_baseline = {} if args.ignore_registry else load_best_approved_snapshot_registry(registry_dir)
    baseline_metadata = registry_baseline or current_metadata
    baseline_source = "approved_snapshot_registry" if registry_baseline else "current_metadata"
    baseline_metrics = snapshot_metrics_from_metadata(baseline_metadata)

    print("\n" + "=" * 100)
    print("SNAPSHOT BASELINE")
    print("=" * 100)
    print(json.dumps({
        "baseline_source": baseline_source,
        "latest_valuation_date": baseline_metrics.get("latest_valuation_date"),
        "players_total": baseline_metrics.get("players_total"),
        "leagues_total": baseline_metrics.get("leagues_total"),
        "snapshot_score": baseline_metadata.get("snapshot_score"),
        "registry_path": baseline_metadata.get("registry_path"),
    }, indent=2, ensure_ascii=False))

    results: list[dict[str, Any]] = []
    failed = False
    guardrail_decision: dict[str, Any] = {}
    promoted_files: list[dict[str, str]] = []
    official_backup = ""

    # Build candidate into isolated directory first.
    if not args.skip_build:
        if candidate_dir.exists() and not args.dry_run:
            shutil.rmtree(candidate_dir)
        candidate_dir.mkdir(parents=True, exist_ok=True)
        step_name, command = build_candidate_command(args, candidate_dir)
        result = run_step(step_name, command, dry_run=args.dry_run)
        results.append(result)
        if result["status"] == "failed":
            failed = True
    else:
        candidate_dir = output_dir
        results.append({"step": "build_candidate_snapshot", "status": "skipped", "candidate_dir": rel(candidate_dir)})

    # Guard candidate before promotion and before modifying DSS datasets.
    if not failed and not args.dry_run:
        candidate_audit_path = candidate_dir / "current_player_snapshot_audit.json"
        require_file(candidate_audit_path, "candidate current_player_snapshot_audit.json")
        candidate_audit = read_json(candidate_audit_path)
        guardrail_decision = evaluate_candidate_guardrails(baseline_metadata, candidate_audit, guardrails)

        print("\n" + "=" * 100)
        print("SNAPSHOT REFRESH GUARDRAILS")
        print("=" * 100)
        print(json.dumps(guardrail_decision, indent=2, ensure_ascii=False))

        if not guardrail_decision.get("accepted", False):
            failed = True
            results.append({
                "step": "guardrails",
                "status": "rejected",
                "decision": guardrail_decision,
            })
        else:
            results.append({
                "step": "guardrails",
                "status": "accepted",
                "decision": guardrail_decision,
            })

    # Promote candidate only after guardrails pass.
    if not failed and not args.dry_run and not args.skip_build:
        backup_dir = backup_official_snapshot(output_dir, refresh_dir, run_id)
        official_backup = rel(backup_dir)
        promoted_files = promote_candidate_snapshot(candidate_dir, output_dir)
        print("\n" + "=" * 100)
        print("PROMOTE CANDIDATE SNAPSHOT")
        print("=" * 100)
        print(json.dumps({"backup": official_backup, "promoted_files": promoted_files}, indent=2, ensure_ascii=False))

    # Apply official snapshot and rebuild metadata/health only after promotion.
    if not failed:
        for step_name, command in build_apply_metadata_health_commands(args, cfg):
            result = run_step(step_name, command, dry_run=args.dry_run)
            results.append(result)
            if result["status"] == "failed":
                failed = True
                break

    health = {} if args.dry_run or failed else read_json(DEFAULT_HEALTH_REPORT)
    final_status = health.get("snapshot_status") if isinstance(health, dict) else None
    snapshot_score = health.get("snapshot_score") if isinstance(health, dict) else None

    # Final score/status guardrail after metadata/health report.
    final_guardrail_status = "not_evaluated"
    if not failed and not args.dry_run:
        min_score = as_float(guardrails.get("min_snapshot_score", 90.0), 90.0)
        min_status = str(guardrails.get("min_snapshot_status", "GREEN")).upper()
        status_ok = str(final_status or "").upper() == min_status if min_status else True
        score_ok = as_float(snapshot_score, 0.0) >= min_score
        if status_ok and score_ok:
            final_guardrail_status = "accepted"
        else:
            final_guardrail_status = "rejected"
            failed = True
            results.append({
                "step": "final_health_guardrail",
                "status": "rejected",
                "min_snapshot_status": min_status,
                "final_snapshot_status": final_status,
                "min_snapshot_score": min_score,
                "final_snapshot_score": snapshot_score,
            })

    summary = {
        "run_id": run_id,
        "generated_at_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "pipeline": "TM.6.6c Official Current Snapshot Refresh Pipeline with Guardrails",
        "root": str(ROOT),
        "config_path": rel(config_path),
        "raw_dir": args.raw_dir,
        "candidate_dir": rel(candidate_dir),
        "official_backup": official_backup,
        "scope": args.scope,
        "status": "failed" if failed else "ok",
        "baseline_source": baseline_source,
        "baseline_metrics": baseline_metrics,
        "registry_baseline": registry_baseline,
        "guardrail_decision": guardrail_decision,
        "final_health_guardrail_status": final_guardrail_status,
        "final_snapshot_status": final_status,
        "final_snapshot_score": snapshot_score,
        "promoted_files": promoted_files,
        "steps": results,
        "outputs": {
            "snapshot_csv": "data/processed/current_player_snapshot.csv",
            "snapshot_parquet": "data/processed/current_player_snapshot.parquet",
            "metadata": "data/processed/current_player_snapshot_metadata.json",
            "health_report_json": "reports/data_quality/snapshot_health_report.json",
            "health_report_md": "reports/data_quality/snapshot_health_report.md",
            "apply_summary": "reports/data_quality/current_snapshot_apply/current_snapshot_apply_summary.json",
        },
    }

    summary_path = refresh_dir / f"snapshot_refresh_summary_{run_id}.json"
    latest_path = refresh_dir / "snapshot_refresh_summary_latest.json"
    summary_path.write_text(json.dumps(summary, indent=2, ensure_ascii=False), encoding="utf-8")
    latest_path.write_text(json.dumps(summary, indent=2, ensure_ascii=False), encoding="utf-8")

    print("\n" + "=" * 100)
    print("SNAPSHOT REFRESH SUMMARY")
    print("=" * 100)
    print(json.dumps({
        "status": summary["status"],
        "guardrails": (guardrail_decision or {}).get("accepted"),
        "final_snapshot_status": final_status,
        "final_snapshot_score": snapshot_score,
        "summary": rel(summary_path),
        "latest_summary": rel(latest_path),
    }, indent=2, ensure_ascii=False))

    if failed:
        print("\n[REJECTED] Snapshot refresh was not promoted or failed guardrails.", file=sys.stderr)
        raise SystemExit(1)

    if final_status and final_status != "GREEN":
        msg = f"[WARNING] Snapshot refresh completed with health status {final_status}."
        print("\n" + msg)
        if args.fail_on_warning:
            raise SystemExit(2)
    else:
        print("\n[OK] SNAPSHOT REFRESH SUCCESSFUL — GUARDRAILS PASSED")


if __name__ == "__main__":
    main()
