"""
TM.6.6 — Transfermarkt Refresh Pipeline

Objetivo:
- Refrescar raw Transfermarkt Kaggle Player Scores.
- Validar frescura, esquema y cobertura.
- Construir transfermarkt_features_v13c.parquet sin destruir v13a.
- Comparar old vs new.
- Opcionalmente promocionar v13c como artefacto oficial.
- Regenerar current_player_snapshot y aplicar snapshot al DSS.

Uso básico:
python src/data/run_tm6_6_transfermarkt_refresh.py --raw-dir data/raw/transfermarkt/kaggle_player_scores

Descarga Kaggle opcional:
python src/data/run_tm6_6_transfermarkt_refresh.py --download --dataset davidcariboo/player-scores

Promoción controlada:
python src/data/run_tm6_6_transfermarkt_refresh.py --promote
"""

from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import sys
from datetime import datetime
from pathlib import Path
from typing import Any

import pandas as pd

ROOT = Path(__file__).resolve().parents[2]

DEFAULT_RAW_DIR = ROOT / "data" / "raw" / "transfermarkt" / "kaggle_player_scores"
DEFAULT_PROCESSED_DIR = ROOT / "data" / "processed"
DEFAULT_REPORT_DIR = ROOT / "reports" / "data_quality" / "tm6_6_transfermarkt_refresh"

REQUIRED_RAW_FILES = ["player_valuations.csv", "players.csv"]
SCOPE_COMPETITIONS = {
    "GB1": "Premier League",
    "ES1": "LaLiga",
    "L1": "Bundesliga",
    "IT1": "Serie A",
    "FR1": "Ligue 1",
    "NL1": "Eredivisie",
    "PO1": "Liga Portugal",
    "BE1": "Belgian Pro League",
    "A1": "Austrian Bundesliga",
}


def run(cmd: list[str], cwd: Path = ROOT, check: bool = True) -> subprocess.CompletedProcess:
    print("\n$ " + " ".join(cmd))
    return subprocess.run(cmd, cwd=cwd, check=check, text=True)


def now_tag() -> str:
    return datetime.now().strftime("%Y%m%d_%H%M%S")


def rel(path: Path) -> str:
    try:
        return str(path.relative_to(ROOT))
    except ValueError:
        return str(path)


def safe_backup(path: Path, backup_root: Path) -> Path | None:
    if not path.exists():
        return None
    backup_root.mkdir(parents=True, exist_ok=True)
    target = backup_root / path.name
    if path.is_dir():
        shutil.copytree(path, target, dirs_exist_ok=True)
    else:
        shutil.copy2(path, target)
    return target


def download_kaggle(dataset: str, raw_dir: Path, force: bool) -> None:
    raw_dir.mkdir(parents=True, exist_ok=True)
    cmd = ["kaggle", "datasets", "download", "-d", dataset, "-p", str(raw_dir), "--unzip"]
    if force:
        cmd.append("--force")
    try:
        run(cmd)
    except FileNotFoundError as exc:
        raise RuntimeError("Kaggle CLI no está disponible. Instala/configura kaggle o descarga manualmente el dataset.") from exc


def validate_raw(raw_dir: Path) -> tuple[pd.DataFrame, pd.DataFrame, dict[str, Any]]:
    missing = [f for f in REQUIRED_RAW_FILES if not (raw_dir / f).exists()]
    if missing:
        raise FileNotFoundError(f"Faltan ficheros raw en {raw_dir}: {missing}")

    valuations = pd.read_csv(raw_dir / "player_valuations.csv")
    players = pd.read_csv(raw_dir / "players.csv")

    required_valuations = {"player_id", "date", "market_value_in_eur"}
    required_players = {"player_id", "name", "current_club_name"}

    missing_val = sorted(required_valuations - set(valuations.columns))
    missing_players = sorted(required_players - set(players.columns))
    if missing_val or missing_players:
        raise ValueError({"missing_valuation_cols": missing_val, "missing_player_cols": missing_players})

    valuations["date_dt"] = pd.to_datetime(valuations["date"], errors="coerce")
    latest = valuations.sort_values(["player_id", "date_dt"], ascending=[True, False]).drop_duplicates("player_id")

    comp_col = "player_club_domestic_competition_id"
    scope_latest = latest[latest.get(comp_col, pd.Series(index=latest.index, dtype=object)).isin(SCOPE_COMPETITIONS)] if comp_col in latest.columns else latest.iloc[0:0]

    audit = {
        "raw_dir": rel(raw_dir),
        "valuations_rows": int(len(valuations)),
        "players_rows": int(len(players)),
        "valuation_date_min": str(valuations["date_dt"].min().date()) if valuations["date_dt"].notna().any() else None,
        "valuation_date_max": str(valuations["date_dt"].max().date()) if valuations["date_dt"].notna().any() else None,
        "latest_players_total": int(latest["player_id"].nunique()),
        "latest_players_in_9_league_scope": int(scope_latest["player_id"].nunique()),
        "competition_counts_top30": latest[comp_col].value_counts(dropna=False).head(30).to_dict() if comp_col in latest.columns else {},
    }
    return valuations, players, audit


def build_features(raw_dir: Path, output_path: Path) -> pd.DataFrame:
    try:
        from src.data.build_transfermarkt_features import build_transfermarkt_features
    except Exception as exc:
        raise RuntimeError("No se puede importar src.data.build_transfermarkt_features") from exc

    df = build_transfermarkt_features(raw_dir)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    df.to_parquet(output_path, index=False)
    return df


def compare_features(old_path: Path, new_path: Path, report_dir: Path) -> dict[str, Any]:
    if not old_path.exists() or not new_path.exists():
        return {"status": "skipped", "reason": "old_or_new_features_missing"}

    old = pd.read_parquet(old_path)
    new = pd.read_parquet(new_path)

    def latest(df: pd.DataFrame) -> pd.DataFrame:
        d = df.copy()
        d["valuation_date"] = pd.to_datetime(d["valuation_date"], errors="coerce")
        return d.sort_values(["player_id_tm", "valuation_date"], ascending=[True, False]).drop_duplicates("player_id_tm")

    old_l = latest(old)
    new_l = latest(new)

    cols = [
        "player_id_tm", "player_name_tm", "season", "valuation_date", "market_value_eur",
        "current_club_name_tm", "competition_id_tm",
    ]
    cols = [c for c in cols if c in old_l.columns and c in new_l.columns]

    merged = old_l[cols].merge(new_l[cols], on="player_id_tm", how="outer", suffixes=("_old", "_new"))

    if "market_value_eur_old" in merged.columns and "market_value_eur_new" in merged.columns:
        merged["market_value_delta_eur"] = merged["market_value_eur_new"] - merged["market_value_eur_old"]
        merged["market_value_delta_pct"] = merged["market_value_delta_eur"] / merged["market_value_eur_old"].replace(0, pd.NA)
    if "current_club_name_tm_old" in merged.columns and "current_club_name_tm_new" in merged.columns:
        merged["club_changed"] = merged["current_club_name_tm_old"].astype(str) != merged["current_club_name_tm_new"].astype(str)
    if "competition_id_tm_new" in merged.columns:
        merged["new_league_scope"] = merged["competition_id_tm_new"].map(SCOPE_COMPETITIONS)

    report_dir.mkdir(parents=True, exist_ok=True)
    merged.to_csv(report_dir / "transfermarkt_refresh_latest_diff.csv", index=False)

    top_changes = merged.copy()
    if "market_value_delta_eur" in top_changes.columns:
        top_changes = top_changes[top_changes["market_value_delta_eur"].notna()].copy()
        top_changes["abs_delta"] = top_changes["market_value_delta_eur"].abs()
        top_changes.sort_values("abs_delta", ascending=False).head(200).drop(columns=["abs_delta"]).to_csv(
            report_dir / "transfermarkt_refresh_top_market_value_changes.csv", index=False
        )

    club_changes = merged[merged.get("club_changed", False) == True].copy() if "club_changed" in merged.columns else pd.DataFrame()
    club_changes.to_csv(report_dir / "transfermarkt_refresh_club_changes.csv", index=False)

    return {
        "status": "ok",
        "old_rows": int(len(old)),
        "new_rows": int(len(new)),
        "old_latest_players": int(old_l["player_id_tm"].nunique()),
        "new_latest_players": int(new_l["player_id_tm"].nunique()),
        "players_added": int(merged["player_name_tm_old"].isna().sum()) if "player_name_tm_old" in merged.columns else None,
        "players_removed": int(merged["player_name_tm_new"].isna().sum()) if "player_name_tm_new" in merged.columns else None,
        "market_value_changed_rows": int((merged.get("market_value_delta_eur", pd.Series(dtype=float)).fillna(0) != 0).sum()),
        "club_changed_rows": int(merged.get("club_changed", pd.Series(dtype=bool)).fillna(False).sum()),
    }


def promote_feature_artifact(new_path: Path, official_path: Path, backup_root: Path) -> None:
    if official_path.exists():
        safe_backup(official_path, backup_root)
    shutil.copy2(new_path, official_path)


def maybe_run_snapshot_scripts() -> dict[str, Any]:
    build_script = ROOT / "src" / "dss" / "build_current_player_snapshot.py"
    apply_script = ROOT / "src" / "dss" / "apply_current_player_snapshot.py"
    result: dict[str, Any] = {}

    if build_script.exists():
        run([sys.executable, str(build_script.relative_to(ROOT)), "--raw-dir", "data/raw/transfermarkt/kaggle_player_scores", "--output-dir", "data/processed", "--scope", "productive"])
        result["build_current_player_snapshot"] = "ok"
    else:
        result["build_current_player_snapshot"] = "missing_script"

    snapshot_path = ROOT / "data" / "processed" / "current_player_snapshot.parquet"
    if apply_script.exists() and snapshot_path.exists():
        run([sys.executable, str(apply_script.relative_to(ROOT)), "--snapshot", "data/processed/current_player_snapshot.parquet"])
        result["apply_current_player_snapshot"] = "ok"
    else:
        result["apply_current_player_snapshot"] = "missing_script_or_snapshot"

    return result


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--raw-dir", default=str(DEFAULT_RAW_DIR))
    parser.add_argument("--dataset", default="davidcariboo/player-scores")
    parser.add_argument("--download", action="store_true")
    parser.add_argument("--force-download", action="store_true")
    parser.add_argument("--output", default=str(DEFAULT_PROCESSED_DIR / "transfermarkt_features_v13c.parquet"))
    parser.add_argument("--official-output", default=str(DEFAULT_PROCESSED_DIR / "transfermarkt_features_v13a.parquet"))
    parser.add_argument("--report-dir", default=str(DEFAULT_REPORT_DIR))
    parser.add_argument("--promote", action="store_true", help="Sobrescribe el artefacto oficial tras backup")
    parser.add_argument("--run-current-snapshot", action="store_true")
    args = parser.parse_args()

    raw_dir = Path(args.raw_dir)
    if not raw_dir.is_absolute():
        raw_dir = ROOT / raw_dir
    output_path = Path(args.output)
    if not output_path.is_absolute():
        output_path = ROOT / output_path
    official_path = Path(args.official_output)
    if not official_path.is_absolute():
        official_path = ROOT / official_path
    report_dir = Path(args.report_dir)
    if not report_dir.is_absolute():
        report_dir = ROOT / report_dir

    tag = now_tag()
    backup_root = ROOT / "artifacts" / "backups" / "tm6_6_transfermarkt_refresh" / tag
    report_dir.mkdir(parents=True, exist_ok=True)

    print("=" * 100)
    print("TM.6.6 — TRANSFERMARKT REFRESH PIPELINE")
    print("=" * 100)

    if args.download:
        safe_backup(raw_dir, backup_root / "raw_before_download")
        download_kaggle(args.dataset, raw_dir, args.force_download)

    valuations, players, raw_audit = validate_raw(raw_dir)
    (report_dir / "raw_transfermarkt_audit.json").write_text(json.dumps(raw_audit, indent=2, ensure_ascii=False), encoding="utf-8")

    old_features_backup = None
    if official_path.exists():
        old_features_backup = safe_backup(official_path, backup_root / "processed_before_refresh")

    new_features = build_features(raw_dir, output_path)
    new_audit = {
        "new_features_path": rel(output_path),
        "new_features_rows": int(len(new_features)),
        "new_features_players": int(new_features["player_id_tm"].nunique()) if "player_id_tm" in new_features.columns else None,
        "new_features_valuation_date_max": str(pd.to_datetime(new_features["valuation_date"], errors="coerce").max().date()) if "valuation_date" in new_features.columns else None,
    }

    compare = compare_features(official_path, output_path, report_dir)

    if args.promote:
        promote_feature_artifact(output_path, official_path, backup_root / "official_before_promote")
        promoted = True
    else:
        promoted = False

    snapshot_result = maybe_run_snapshot_scripts() if args.run_current_snapshot else {"status": "skipped"}

    summary = {
        "run_tag": tag,
        "raw_audit": raw_audit,
        "new_features_audit": new_audit,
        "old_features_backup": rel(old_features_backup) if old_features_backup else None,
        "comparison": compare,
        "promoted_to_official": promoted,
        "snapshot_result": snapshot_result,
        "reports": {
            "raw_audit": rel(report_dir / "raw_transfermarkt_audit.json"),
            "latest_diff": rel(report_dir / "transfermarkt_refresh_latest_diff.csv"),
            "top_market_value_changes": rel(report_dir / "transfermarkt_refresh_top_market_value_changes.csv"),
            "club_changes": rel(report_dir / "transfermarkt_refresh_club_changes.csv"),
        },
    }
    summary_path = report_dir / "tm6_6_refresh_summary.json"
    summary_path.write_text(json.dumps(summary, indent=2, ensure_ascii=False), encoding="utf-8")

    print("\n" + "=" * 100)
    print("SUMMARY")
    print("=" * 100)
    print(json.dumps(summary, indent=2, ensure_ascii=False))
    print(f"\n[OK] Summary: {summary_path}")


if __name__ == "__main__":
    main()
