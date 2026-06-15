from __future__ import annotations

import argparse
import json
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2] if "src" in Path(__file__).resolve().parts else Path.cwd()
DEFAULT_REGISTRY_DIR = ROOT / "data" / "processed" / "snapshot_registry"
DEFAULT_METADATA = ROOT / "data" / "processed" / "current_player_snapshot_metadata.json"
DEFAULT_HEALTH = ROOT / "reports" / "data_quality" / "snapshot_health_report.json"
DEFAULT_SNAPSHOT_DIR = ROOT / "data" / "processed"
OFFICIAL_FILES = [
    "current_player_snapshot.csv",
    "current_player_snapshot.parquet",
    "current_player_snapshot_audit.json",
    "current_player_snapshot_homonyms.csv",
]


def rel(path: Path) -> str:
    try:
        return str(path.relative_to(ROOT))
    except Exception:
        return str(path)


def now_utc() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def read_json(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    with path.open("r", encoding="utf-8") as f:
        data = json.load(f)
    return data if isinstance(data, dict) else {"results": data}


def write_json(path: Path, data: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")


def parse_date_safe(value: Any) -> str:
    if value is None:
        return ""
    return str(value)[:10]


def record_from_current(
    registry_dir: Path,
    snapshot_dir: Path,
    metadata_path: Path,
    health_path: Path,
    status: str,
    reason: str,
) -> dict[str, Any]:
    meta = read_json(metadata_path)
    health = read_json(health_path)
    if not meta:
        raise FileNotFoundError(f"Metadata not found or empty: {metadata_path}")

    files = {}
    for name in OFFICIAL_FILES:
        p = snapshot_dir / name
        if p.exists():
            files[name] = rel(p)

    record = {
        "registry_record_type": "current_player_snapshot_approved_record",
        "created_at_utc": now_utc(),
        "status": status,
        "approval_reason": reason,
        "snapshot_version": meta.get("snapshot_version", "v1.0.0"),
        "snapshot_date": meta.get("snapshot_date"),
        "source": meta.get("source"),
        "latest_valuation_date": meta.get("latest_valuation_date"),
        "players_total": meta.get("players_total"),
        "leagues_total": meta.get("leagues_total"),
        "leagues": meta.get("leagues", []),
        "homonym_names": meta.get("homonym_names"),
        "match_key": meta.get("match_key", "player_id_tm"),
        "fallback_match_key": meta.get("fallback_match_key"),
        "coverage": meta.get("coverage", {}),
        "matched_rows": meta.get("matched_rows", {}),
        "unmatched_rows": meta.get("unmatched_rows", {}),
        "snapshot_status": health.get("snapshot_status"),
        "snapshot_score": health.get("snapshot_score"),
        "files": files,
        "metadata_path": rel(metadata_path),
        "health_report_path": rel(health_path),
    }
    return record


def seed_baseline_good(registry_dir: Path) -> dict[str, Any]:
    """Seed the best known approved baseline from TM.6.6c QA evidence.

    This is intentionally explicit: it protects the project from comparing new
    candidates against an already degraded current snapshot.
    """
    record = {
        "registry_record_type": "current_player_snapshot_approved_record",
        "created_at_utc": now_utc(),
        "status": "approved",
        "approval_reason": "TM.6.6c approved baseline before accidental refresh degradation.",
        "snapshot_version": "v1.0.0",
        "snapshot_date": "2026-06-15",
        "source": "transfermarkt_features_v13a",
        "latest_valuation_date": "2026-03-27",
        "players_total": 17510,
        "leagues_total": 9,
        "homonym_names": 512,
        "match_key": "player_id_tm",
        "fallback_match_key": "player_name_norm_unique_only",
        "coverage": {
            "dss_pct": 91.68,
            "contract_pct": 91.68,
            "portfolio_pct": 89.95,
        },
        "matched_rows": {
            "dss": 694,
            "contract": 694,
            "portfolio": 5584,
        },
        "unmatched_rows": {
            "dss": 63,
            "contract": 63,
            "portfolio": 624,
        },
        "snapshot_status": "GREEN",
        "snapshot_score": 96.42,
        "files": {},
        "governance_note": "Baseline registry record created to prevent future snapshot refreshes from being validated against an already degraded current snapshot.",
    }
    save_record(registry_dir, record)
    return record


def save_record(registry_dir: Path, record: dict[str, Any]) -> Path:
    registry_dir.mkdir(parents=True, exist_ok=True)
    date_token = parse_date_safe(record.get("latest_valuation_date")) or "unknown_date"
    players = record.get("players_total", "unknown_players")
    created = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
    path = registry_dir / f"approved_snapshot_{date_token}_{players}_{created}.json"
    write_json(path, record)
    latest = registry_dir / "latest_approved_snapshot.json"
    write_json(latest, record)
    return path


def load_records(registry_dir: Path) -> list[dict[str, Any]]:
    records = []
    if not registry_dir.exists():
        return records
    for p in registry_dir.glob("approved_snapshot_*.json"):
        r = read_json(p)
        if r:
            r["registry_path"] = rel(p)
            records.append(r)
    return records


def best_record(registry_dir: Path) -> dict[str, Any]:
    records = load_records(registry_dir)
    if not records:
        latest = read_json(registry_dir / "latest_approved_snapshot.json")
        return latest

    def key(r: dict[str, Any]) -> tuple[str, int, float]:
        return (
            str(r.get("latest_valuation_date", "")),
            int(float(r.get("players_total") or 0)),
            float(r.get("snapshot_score") or 0),
        )

    return sorted(records, key=key, reverse=True)[0]


def scan_snapshot_candidates(search_root: Path) -> list[dict[str, Any]]:
    candidates: list[dict[str, Any]] = []
    for audit in search_root.rglob("current_player_snapshot_audit.json"):
        data = read_json(audit)
        if not data:
            continue
        directory = audit.parent
        candidates.append({
            "audit_path": rel(audit),
            "directory": rel(directory),
            "players_total": data.get("players_unique") or data.get("rows"),
            "latest_valuation_date": data.get("current_valuation_date_max"),
            "leagues_total": data.get("leagues_unique"),
            "homonym_names": data.get("homonym_names"),
            "has_parquet": (directory / "current_player_snapshot.parquet").exists(),
            "has_csv": (directory / "current_player_snapshot.csv").exists(),
        })
    return sorted(
        candidates,
        key=lambda x: (str(x.get("latest_valuation_date") or ""), int(float(x.get("players_total") or 0))),
        reverse=True,
    )


def restore_from_directory(source_dir: Path, target_dir: Path) -> dict[str, Any]:
    if not source_dir.exists():
        raise FileNotFoundError(f"Source snapshot directory not found: {source_dir}")
    target_dir.mkdir(parents=True, exist_ok=True)
    copied = []
    for name in OFFICIAL_FILES:
        src = source_dir / name
        dst = target_dir / name
        if src.exists():
            shutil.copy2(src, dst)
            copied.append({"source": rel(src), "destination": rel(dst)})
    if not copied:
        raise FileNotFoundError(f"No official snapshot files found in: {source_dir}")
    return {"status": "ok", "source_dir": rel(source_dir), "target_dir": rel(target_dir), "copied": copied}


def main() -> None:
    parser = argparse.ArgumentParser(description="TM.6.6c.3 Snapshot Registry & Baseline Protection")
    sub = parser.add_subparsers(dest="command", required=True)

    p_seed = sub.add_parser("seed-baseline-good", help="Create approved registry baseline from known good TM.6.6c metrics.")
    p_seed.add_argument("--registry-dir", default=str(DEFAULT_REGISTRY_DIR.relative_to(ROOT)))

    p_approve = sub.add_parser("approve-current", help="Approve current official snapshot and register it.")
    p_approve.add_argument("--registry-dir", default=str(DEFAULT_REGISTRY_DIR.relative_to(ROOT)))
    p_approve.add_argument("--snapshot-dir", default=str(DEFAULT_SNAPSHOT_DIR.relative_to(ROOT)))
    p_approve.add_argument("--metadata", default=str(DEFAULT_METADATA.relative_to(ROOT)))
    p_approve.add_argument("--health", default=str(DEFAULT_HEALTH.relative_to(ROOT)))
    p_approve.add_argument("--reason", default="Manual approval after QA.")
    p_approve.add_argument("--status", default="approved")

    p_best = sub.add_parser("best", help="Print best approved snapshot baseline.")
    p_best.add_argument("--registry-dir", default=str(DEFAULT_REGISTRY_DIR.relative_to(ROOT)))

    p_scan = sub.add_parser("scan", help="Scan repository for snapshot backups/candidates.")
    p_scan.add_argument("--search-root", default=".")
    p_scan.add_argument("--out", default="reports/data_quality/snapshot_refresh/snapshot_registry_scan.json")

    p_restore = sub.add_parser("restore", help="Restore official snapshot files from a source directory.")
    p_restore.add_argument("--source-dir", required=True)
    p_restore.add_argument("--target-dir", default=str(DEFAULT_SNAPSHOT_DIR.relative_to(ROOT)))

    args = parser.parse_args()

    if args.command == "seed-baseline-good":
        registry_dir = ROOT / args.registry_dir
        record = seed_baseline_good(registry_dir)
        print(json.dumps(record, indent=2, ensure_ascii=False))
        print(f"\n[OK] Registry baseline: {registry_dir / 'latest_approved_snapshot.json'}")

    elif args.command == "approve-current":
        registry_dir = ROOT / args.registry_dir
        record = record_from_current(
            registry_dir=registry_dir,
            snapshot_dir=ROOT / args.snapshot_dir,
            metadata_path=ROOT / args.metadata,
            health_path=ROOT / args.health,
            status=args.status,
            reason=args.reason,
        )
        path = save_record(registry_dir, record)
        print(json.dumps(record, indent=2, ensure_ascii=False))
        print(f"\n[OK] Approved registry record: {path}")

    elif args.command == "best":
        record = best_record(ROOT / args.registry_dir)
        print(json.dumps(record, indent=2, ensure_ascii=False))

    elif args.command == "scan":
        candidates = scan_snapshot_candidates(ROOT / args.search_root)
        out = ROOT / args.out
        write_json(out, {"candidates": candidates})
        print(json.dumps({"candidates": candidates[:30], "total": len(candidates), "out": rel(out)}, indent=2, ensure_ascii=False))

    elif args.command == "restore":
        result = restore_from_directory(ROOT / args.source_dir, ROOT / args.target_dir)
        print(json.dumps(result, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
