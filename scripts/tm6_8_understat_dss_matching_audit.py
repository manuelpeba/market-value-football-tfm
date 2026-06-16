import json
import re
import unicodedata
from datetime import date
from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]

PROCESSED = ROOT / "data" / "processed"
REPORTS = ROOT / "reports" / "data_quality"

DSS_PATH = ROOT / "reports" / "dss" / "global_prospect_universe.csv"
PORTFOLIO_PATH = ROOT / "reports" / "strategy" / "transfer_portfolio_dataset.csv"
CONTRACT_PATH = ROOT / "reports" / "tm3_contract_intelligence" / "contract_intelligence_dataset.csv"

XG_SNAPSHOT_PATH = PROCESSED / "current_xg_snapshot.parquet"

REPORTS.mkdir(parents=True, exist_ok=True)


LEAGUE_MAP = {
    "ENG-Premier League": "Premier League",
    "ESP-La Liga": "LaLiga",
    "GER-Bundesliga": "Bundesliga",
    "ITA-Serie A": "Serie A",
    "FRA-Ligue 1": "Ligue 1",
    "Premier League": "Premier League",
    "LaLiga": "LaLiga",
    "La Liga": "LaLiga",
    "Bundesliga": "Bundesliga",
    "Serie A": "Serie A",
    "Ligue 1": "Ligue 1",
    "England": "Premier League",
    "Spain": "LaLiga",
    "Germany": "Bundesliga",
    "Italy": "Serie A",
    "France": "Ligue 1",
    "ENG": "Premier League",
    "ESP": "LaLiga",
    "GER": "Bundesliga",
    "ITA": "Serie A",
    "FRA": "Ligue 1",
}


def normalize_name(value: str) -> str:
    if pd.isna(value):
        return ""

    value = str(value).strip().lower()
    value = unicodedata.normalize("NFKD", value)
    value = "".join(c for c in value if not unicodedata.combining(c))
    value = re.sub(r"[^a-z0-9\s-]", " ", value)
    value = re.sub(r"\s+", " ", value).strip()

    return value


def infer_columns(df: pd.DataFrame):
    player_candidates = [
        "player_name_norm",
        "player_name_fbref",
        "player_name_tm",
        "player",
        "player_name",
        "name",
    ]

    league_candidates = [
        "display_league",
        "current_league",
        "season_context_league",
        "league",
    ]

    player_col = next((c for c in player_candidates if c in df.columns), None)
    league_col = next((c for c in league_candidates if c in df.columns), None)

    if player_col is None:
        raise ValueError(f"No player column found. Columns: {df.columns.tolist()}")

    if league_col is None:
        raise ValueError(f"No league column found. Columns: {df.columns.tolist()}")

    return player_col, league_col


def prepare_target(df: pd.DataFrame, dataset_name: str) -> pd.DataFrame:
    player_col, league_col = infer_columns(df)

    out = df.copy()
    out["_dataset"] = dataset_name
    out["_player_col"] = player_col
    out["_league_col"] = league_col

    if player_col == "player_name_norm":
        out["player_name_norm"] = out[player_col].fillna("").astype(str)
    else:
        out["player_name_norm"] = out[player_col].apply(normalize_name)

    out["league_normalized"] = (
        out[league_col]
        .astype(str)
        .map(LEAGUE_MAP)
        .fillna(out[league_col].astype(str))
    )

    return out


def audit_dataset(dataset_name: str, path: Path, xg: pd.DataFrame) -> tuple[dict, pd.DataFrame]:
    if not path.exists():
        return {
            "dataset": dataset_name,
            "path": str(path),
            "status": "MISSING_FILE",
            "rows_total": 0,
            "rows_big5": 0,
            "matched_rows": 0,
            "coverage_big5_pct": 0,
            "coverage_total_pct": 0,
            "unmatched_big5": 0,
        }, pd.DataFrame()

    df = pd.read_csv(path)
    target = prepare_target(df, dataset_name)

    big5_leagues = set(xg["league"].dropna().unique())

    target_big5 = target[
        target["league_normalized"].isin(big5_leagues)
    ].copy()

    xg_keys = xg[
        [
            "understat_player_id",
            "player_name",
            "player_name_norm",
            "league",
            "team",
            "current_xg",
            "current_xa",
            "current_npxg",
            "current_expected_contribution",
            "current_expected_contribution_per90",
        ]
    ].drop_duplicates(
        subset=["player_name_norm", "league"]
    )

    merged = target_big5.merge(
        xg_keys,
        left_on=["player_name_norm", "league_normalized"],
        right_on=["player_name_norm", "league"],
        how="left",
        suffixes=("", "_understat"),
    )

    matched = int(merged["understat_player_id"].notna().sum())

    result = {
        "dataset": dataset_name,
        "path": str(path),
        "status": "OK",
        "rows_total": int(len(target)),
        "rows_big5": int(len(target_big5)),
        "matched_rows": matched,
        "coverage_big5_pct": round(matched / len(target_big5) * 100, 2) if len(target_big5) else 0,
        "coverage_total_pct": round(matched / len(target) * 100, 2) if len(target) else 0,
        "unmatched_big5": int(len(target_big5) - matched),
        "player_column_used": target["_player_col"].iloc[0] if len(target) else None,
        "league_column_used": target["_league_col"].iloc[0] if len(target) else None,
    }

    unmatched = merged[merged["understat_player_id"].isna()].copy()

    return result, unmatched


def main():
    if not XG_SNAPSHOT_PATH.exists():
        raise FileNotFoundError(f"Missing current_xg_snapshot: {XG_SNAPSHOT_PATH}")

    xg = pd.read_parquet(XG_SNAPSHOT_PATH)

    required_xg_cols = {
        "understat_player_id",
        "player_name",
        "player_name_norm",
        "league",
    }

    missing = required_xg_cols - set(xg.columns)

    if missing:
        raise ValueError(f"Missing required columns in current_xg_snapshot: {sorted(missing)}")

    xg["player_name_norm"] = xg["player_name_norm"].fillna("").astype(str)
    xg["league"] = xg["league"].astype(str)

    datasets = [
        ("DSS", DSS_PATH),
        ("Portfolio", PORTFOLIO_PATH),
        ("Contract", CONTRACT_PATH),
    ]

    results = []
    unmatched_frames = []

    for dataset_name, path in datasets:
        print(f"Auditing {dataset_name}...")

        result, unmatched = audit_dataset(dataset_name, path, xg)
        results.append(result)

        if not unmatched.empty:
            unmatched["_audit_dataset"] = dataset_name
            unmatched_frames.append(unmatched)

        print(result)

    results_df = pd.DataFrame(results)

    json_path = REPORTS / "tm6_8_understat_matching_audit.json"
    csv_path = REPORTS / "tm6_8_understat_matching_audit.csv"
    unmatched_path = REPORTS / "tm6_8_understat_matching_unmatched_big5.csv"
    md_path = REPORTS / "tm6_8_understat_matching_audit.md"

    results_df.to_csv(csv_path, index=False)

    if unmatched_frames:
        unmatched_df = pd.concat(unmatched_frames, ignore_index=True)
        unmatched_df.to_csv(unmatched_path, index=False)
    else:
        unmatched_path.write_text("", encoding="utf-8")

    audit = {
        "audit_name": "TM.6.8c Understat DSS Matching Coverage Audit",
        "audit_date": str(date.today()),
        "source": "understat",
        "snapshot": "current_xg_snapshot",
        "matching_strategy": {
            "primary_current_method": "player_name_norm + league",
            "future_target_method": "player_id_tm + understat_player_id crosswalk",
            "risk_note": (
                "Name-based matching is acceptable for coverage estimation, "
                "but final productive enrichment should use a controlled mapping "
                "layer between player_id_tm and understat_player_id."
            ),
        },
        "results": results,
        "assessment": {
            "status": "PENDING_REVIEW",
            "approval_rule": "APPROVED if DSS Big5 coverage >= 70% and no critical schema issue.",
        },
    }

    json_path.write_text(
        json.dumps(audit, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )

    md_lines = [
        "# TM.6.8c — Understat Matching Strategy & DSS Coverage Audit",
        "",
        f"Audit date: {date.today()}",
        "",
        "## Matching Strategy",
        "",
        "Current audit method:",
        "",
        "```text",
        "player_name_norm + league",
        "```",
        "",
        "Future productive method:",
        "",
        "```text",
        "player_id_tm + understat_player_id crosswalk",
        "```",
        "",
        "## Coverage Results",
        "",
        "| Dataset | Rows Total | Big 5 Rows | Matched Rows | Coverage Big 5 | Coverage Total | Player Col | League Col |",
        "|---|---:|---:|---:|---:|---:|---|---|",
    ]

    for r in results:
        md_lines.append(
            f"| {r['dataset']} | {r['rows_total']} | {r['rows_big5']} | "
            f"{r['matched_rows']} | {r['coverage_big5_pct']}% | "
            f"{r['coverage_total_pct']}% | {r.get('player_column_used')} | {r.get('league_column_used')} |"
        )

    md_lines.extend(
        [
            "",
            "## Governance Note",
            "",
            "This audit uses conservative name + league matching. "
            "It is valid for coverage estimation, but productive DSS enrichment should use "
            "a controlled mapping layer between `player_id_tm` and `understat_player_id`.",
            "",
            "## Output Files",
            "",
            f"- `{csv_path}`",
            f"- `{json_path}`",
            f"- `{unmatched_path}`",
        ]
    )

    md_path.write_text("\n".join(md_lines), encoding="utf-8")

    print("\nSaved:")
    print(csv_path)
    print(json_path)
    print(md_path)
    print(unmatched_path)


if __name__ == "__main__":
    main()