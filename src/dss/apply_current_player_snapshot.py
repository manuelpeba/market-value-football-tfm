from __future__ import annotations

import argparse
import json
import re
import shutil
import unicodedata
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2] if "src" in Path(__file__).parts else Path.cwd()


def _repo_relative(path: str | Path) -> str:
    """Represent repository files with portable POSIX-style relative paths."""
    resolved = Path(path).resolve()

    try:
        return resolved.relative_to(
            ROOT.resolve()
        ).as_posix()
    except ValueError:
        return resolved.as_posix()

TARGET_FILES = [
    Path("reports/dss/global_prospect_universe.csv"),
    Path("reports/tm3_contract_intelligence/contract_intelligence_dataset.csv"),
    Path("reports/strategy/transfer_portfolio_dataset.csv"),
]


def normalize_key(value: object) -> str:
    if pd.isna(value):
        return ""
    text = str(value).strip().lower()
    text = unicodedata.normalize("NFKD", text)
    text = "".join(ch for ch in text if not unicodedata.combining(ch))
    text = re.sub(r"[^a-z0-9 ]+", " ", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text


def read_table(path: Path) -> pd.DataFrame:
    return pd.read_parquet(path) if path.suffix.lower() == ".parquet" else pd.read_csv(path)


def write_table(df: pd.DataFrame, path: Path) -> None:
    if path.suffix.lower() == ".parquet":
        df.to_parquet(path, index=False)
    else:
        df.to_csv(path, index=False, encoding="utf-8")


def remove_numbered_duplicate_columns(df: pd.DataFrame) -> pd.DataFrame:
    """Drop pandas duplicate-name artifacts such as column.1, column.2."""
    duplicate_suffix = re.compile(r"\.\d+$")
    drop_cols = [c for c in df.columns if duplicate_suffix.search(str(c))]
    if drop_cols:
        df = df.drop(columns=drop_cols)
    if df.columns.duplicated().any():
        df = df.loc[:, ~df.columns.duplicated()].copy()
    return df


def as_series(df: pd.DataFrame, col: str, default=pd.NA) -> pd.Series:
    """Return a single Series even when previous corrupt runs created duplicate columns."""
    if col not in df.columns:
        return pd.Series(default, index=df.index)
    value = df[col]
    if isinstance(value, pd.DataFrame):
        return value.iloc[:, 0]
    return value


def load_snapshot(path: str | Path) -> pd.DataFrame:
    path = Path(path)
    if not path.is_absolute():
        path = ROOT / path
    if not path.exists():
        raise FileNotFoundError(f"current_player_snapshot not found: {path}")

    snap = read_table(path).copy()
    required = {
        "player_id_tm",
        "player_name_tm",
        "player_name_norm",
        "current_club",
        "current_league",
        "current_market_value_eur",
        "current_valuation_date",
    }
    missing = required - set(snap.columns)
    if missing:
        raise ValueError(f"Snapshot missing required columns: {sorted(missing)}")

    snap["player_id_tm"] = pd.to_numeric(snap["player_id_tm"], errors="coerce").astype("Int64")
    snap["player_name_norm"] = snap["player_name_norm"].fillna("").astype(str)
    snap["snapshot_name_unique"] = snap.groupby("player_name_norm")["player_id_tm"].transform("nunique").fillna(0).eq(1)
    snap = snap.drop_duplicates("player_id_tm", keep="first").copy()
    return snap


def standardize_input_identity(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    if "player_id_tm" in df.columns:
        df["player_id_tm"] = pd.to_numeric(df["player_id_tm"], errors="coerce").astype("Int64")
    else:
        df["player_id_tm"] = pd.Series([pd.NA] * len(df), dtype="Int64")

    name_candidates = ["player_name_fbref", "player_name", "player", "name"]
    name_col = next((c for c in name_candidates if c in df.columns), None)
    if name_col is None:
        raise ValueError("No player name column found")
    df["_player_name_source_col"] = name_col
    df["_player_name_norm_join"] = df[name_col].map(normalize_key)
    return df


def preserve_historical_context(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    preserve_map = {
        "club": "season_context_club",
        "club_actual": "season_context_club",
        "team": "season_context_team",
        "league": "season_context_league",
        "season": "season_context_season",
        "age": "season_context_age",
        "market_value_eur": "season_context_market_value_eur",
    }
    for source, target in preserve_map.items():
        if source in df.columns and target not in df.columns:
            df[target] = df[source]
    return df


def build_joined(df: pd.DataFrame, snapshot: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    df = remove_numbered_duplicate_columns(df)
    snapshot = remove_numbered_duplicate_columns(snapshot)
    df = standardize_input_identity(preserve_historical_context(df))
    df = remove_numbered_duplicate_columns(df)

    snap_cols = [
        "player_id_tm",
        "player_name_tm",
        "player_name_norm",
        "current_club",
        "current_league",
        "current_season",
        "current_market_value_eur",
        "current_valuation_date",
        "current_age",
        "current_competition_id",
        "current_club_id",
        "homonym_group_size",
        "is_homonym_name",
        "identity_resolution_status",
        "snapshot_source",
    ]
    snap_cols = [c for c in snap_cols if c in snapshot.columns]

    # TM.8.10 — Snapshot application must be idempotent.
    #
    # Remove values managed by the snapshot before applying the current
    # authority. Otherwise, repeated executions generate columns such as
    # current_age_snapshot and preserve stale current-context values.
    snapshot_value_cols = [
        column
        for column in snap_cols
        if column != "player_id_tm"
    ]

    accidental_snapshot_aliases = [
        f"{column}_snapshot"
        for column in snapshot_value_cols
    ]

    derived_snapshot_cols = [
        "identity_match_method",
        "current_snapshot_applied",
        "identity_review_required",
        "display_club",
        "display_league",
        "display_market_value_eur",
        "club_context_changed",
        "league_context_changed",
        "context_changed",
        "valuation_context",
        "gap_interpretation_status",
    ]

    snapshot_managed_cols = set(
        snapshot_value_cols
        + accidental_snapshot_aliases
        + derived_snapshot_cols
    )

    drop_snapshot_managed_cols = [
        column
        for column in df.columns
        if column in snapshot_managed_cols
    ]

    if drop_snapshot_managed_cols:
        df = df.drop(
            columns=drop_snapshot_managed_cols
        )

    # 1) Primary match by player_id_tm.
    by_id = df.merge(
        snapshot[snap_cols],
        on="player_id_tm",
        how="left",
        suffixes=("", "_snapshot"),
    ).reset_index(drop=True)
    by_id = remove_numbered_duplicate_columns(by_id)
    by_id["identity_match_method"] = np.where(by_id["current_club"].notna(), "player_id_tm", pd.NA)

    # 2) Conservative fallback by unique normalized name only.
    unmatched = by_id["current_club"].isna()
    snapshot_unique_name = snapshot[snapshot["snapshot_name_unique"]].copy()
    name_cols = [c for c in snap_cols if c != "player_id_tm"] + ["player_id_tm"]
    name_fallback = df.loc[unmatched, ["_player_name_norm_join"]].merge(
        snapshot_unique_name[name_cols],
        left_on="_player_name_norm_join",
        right_on="player_name_norm",
        how="left",
        suffixes=("", "_snapshot"),
    )

    if len(name_fallback):
        for col in snap_cols:
            if col == "player_id_tm":
                if "player_id_tm_snapshot" in name_fallback.columns:
                    vals = name_fallback["player_id_tm_snapshot"].to_numpy()
                    by_id.loc[unmatched, "player_id_tm"] = by_id.loc[unmatched, "player_id_tm"].fillna(pd.Series(vals, index=by_id.index[unmatched]).astype("Int64"))
                continue
            if col in name_fallback.columns:
                by_id.loc[unmatched, col] = name_fallback[col].to_numpy()
        by_id.loc[unmatched & by_id["current_club"].notna(), "identity_match_method"] = "unique_name_norm"

    by_id["current_snapshot_applied"] = by_id["current_club"].notna()
    by_id["identity_review_required"] = ~by_id["current_snapshot_applied"]

    # Do NOT overwrite historical market_value_eur.
    # Rebuild current/display authority on every execution.
    by_id["display_club"] = (
        by_id["current_club"]
        .fillna(by_id.get("season_context_club"))
    )

    by_id["display_league"] = (
        by_id["current_league"]
        .fillna(by_id.get("season_context_league"))
    )

    # ==========================================================
    # TM.8.8 — Dataset Governance Contract
    # ==========================================================
    by_id["current_club_snapshot"] = by_id["current_club"]
    by_id["current_league_snapshot"] = by_id["current_league"]

    if "current_market_value_eur" in by_id.columns:
        by_id["current_market_value_eur_snapshot"] = (
            by_id["current_market_value_eur"]
        )
    else:
        by_id["current_market_value_eur_snapshot"] = pd.NA

    current_mv = as_series(
        by_id,
        "current_market_value_eur_snapshot",
    )

    season_mv = as_series(
        by_id,
        "season_context_market_value_eur",
    )

    by_id["display_market_value_eur"] = (
        current_mv.fillna(season_mv)
    )

    season_club = as_series(by_id, "season_context_club").reset_index(drop=True).fillna("").astype(str)
    current_club = as_series(by_id, "current_club_snapshot").reset_index(drop=True).fillna("").astype(str)
    season_league = as_series(by_id, "season_context_league").reset_index(drop=True).fillna("").astype(str)
    current_league = as_series(by_id, "current_league_snapshot").reset_index(drop=True).fillna("").astype(str)

    by_id["club_context_changed"] = season_club.ne(current_club).to_numpy()
    by_id["league_context_changed"] = season_league.ne(current_league).to_numpy()

    by_id["context_changed"] = by_id["club_context_changed"] | by_id["league_context_changed"]

    by_id["valuation_context"] = "CURRENT_SNAPSHOT_FOR_DISPLAY__SEASON_CONTEXT_FOR_MODEL"

    by_id["gap_interpretation_status"] = np.where(
        by_id["context_changed"],
        "CONTEXT_CHANGED_CAUTION",
        "VALID_SAME_CONTEXT",
    )

    diagnostics = pd.DataFrame(
        {
            "rows": [len(by_id)],
            "matched_total": [int(by_id["current_snapshot_applied"].sum())],
            "matched_pct": [round(float(by_id["current_snapshot_applied"].mean() * 100), 2) if len(by_id) else 0.0],
            "matched_by_player_id": [int((by_id["identity_match_method"] == "player_id_tm").sum())],
            "matched_by_unique_name": [int((by_id["identity_match_method"] == "unique_name_norm").sum())],
            "unmatched": [int((~by_id["current_snapshot_applied"]).sum())],
            "homonym_review_rows": [
                int(
                    by_id.get(
                        "is_homonym_name",
                        pd.Series(
                            False,
                            index=by_id.index,
                            dtype="boolean",
                        ),
                    )
                    .astype("boolean")
                    .fillna(False)
                    .sum()
                )
            ],
            "current_leagues": [" | ".join(sorted(by_id["current_league"].dropna().astype(str).unique()))],
        }
    )

    drop_internal = ["_player_name_norm_join", "_player_name_source_col"]
    by_id = by_id.drop(columns=[c for c in drop_internal if c in by_id.columns])
    return by_id, diagnostics


def apply_to_file(path: Path, snapshot: pd.DataFrame, backup: bool, out_dir: Path) -> dict:
    full_path = path if path.is_absolute() else ROOT / path
    if not full_path.exists():
        return {"path": _repo_relative(full_path), "status": "missing"}

    if backup:
        backup_path = full_path.with_suffix(full_path.suffix + ".bak_current_snapshot")
        shutil.copy2(full_path, backup_path)

    df = read_table(full_path)
    updated, diagnostics = build_joined(df, snapshot)
    write_table(updated, full_path)

    out_dir.mkdir(parents=True, exist_ok=True)
    diag_path = out_dir / f"{full_path.stem}_current_snapshot_apply_audit.csv"
    diagnostics.insert(0, "dataset", full_path.stem)
    diagnostics.insert(1, "path", _repo_relative(full_path))
    diagnostics.to_csv(diag_path, index=False, encoding="utf-8")

    return {
        "path": _repo_relative(full_path),
        "status": "ok",
        "rows": int(diagnostics.loc[0, "rows"]),
        "matched_total": int(diagnostics.loc[0, "matched_total"]),
        "matched_pct": float(diagnostics.loc[0, "matched_pct"]),
        "matched_by_player_id": int(diagnostics.loc[0, "matched_by_player_id"]),
        "matched_by_unique_name": int(diagnostics.loc[0, "matched_by_unique_name"]),
        "unmatched": int(diagnostics.loc[0, "unmatched"]),
        "audit": _repo_relative(diag_path),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--snapshot", default="data/processed/current_player_snapshot.parquet")
    parser.add_argument("--audit-dir", default="reports/data_quality/current_snapshot_apply")
    parser.add_argument("--no-backup", action="store_true")
    parser.add_argument("--targets", nargs="*", default=[str(p) for p in TARGET_FILES])
    args = parser.parse_args()

    snapshot = load_snapshot(args.snapshot)
    audit_dir = Path(args.audit_dir)
    if not audit_dir.is_absolute():
        audit_dir = ROOT / audit_dir

    results = []
    print("=" * 100)
    print("APPLY CURRENT PLAYER SNAPSHOT")
    print("=" * 100)
    for target in args.targets:
        result = apply_to_file(Path(target), snapshot, backup=not args.no_backup, out_dir=audit_dir)
        results.append(result)
        print(json.dumps(result, indent=2, ensure_ascii=False))

    summary_path = audit_dir / "current_snapshot_apply_summary.json"
    summary_path.write_text(json.dumps(results, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"\n[OK] Summary: {summary_path}")


if __name__ == "__main__":
    main()
