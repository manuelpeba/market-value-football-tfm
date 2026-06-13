"""
TM.6.4.2b — Attacking Calibration

Objective
---------
Recalibrate the tactical position taxonomy produced in TM.6.4.1 without
modifying clustering, UMAP, KMeans or the Role Labeling Engine.

Inputs
------
- data/processed/player_role_features_advanced.parquet
- data/processed/player_position_taxonomy.parquet
- data/processed/player_role_labels.parquet (optional, for context only)

Outputs
-------
- data/processed/player_position_taxonomy_v2b.parquet
- reports/roles/position_taxonomy_distribution_v2b.csv
- reports/roles/position_taxonomy_validation_v2b.csv
- reports/roles/position_taxonomy_representatives_v2b.csv
- reports/roles/position_taxonomy_purity_v2b.csv

Design principles
-----------------
- Quality of tactical classification before algorithmic complexity.
- Functional scores for ambiguous families only:
    ATT: W vs CF
    MID: DM vs CM vs AM
- Defensive taxonomy is preserved unless high-confidence evidence exists.
- Reproducible deterministic rules.
"""

from __future__ import annotations

import argparse
import json
import math
import re
import unicodedata
from pathlib import Path
from typing import Iterable

import numpy as np
import pandas as pd


VALID_TAXONOMY = ["GK", "CB", "FB", "DM", "CM", "AM", "W", "CF"]
FIELD_PLAYERS = ["CB", "FB", "DM", "CM", "AM", "W", "CF"]
MID_FAMILY = ["DM", "CM", "AM"]
ATT_FAMILY = ["W", "CF"]

VALIDATION_PLAYERS = {
    "CB": ["Bastoni", "Van Dijk", "Rúben Dias"],
    "FB": ["Hakimi", "Frimpong", "Theo Hernández"],
    "DM": ["Rodri", "Zubimendi", "Caicedo", "Ugarte"],
    "CM": ["Vitinha", "Modric", "Bruno Guimarães"],
    "AM": ["Pedri", "Wirtz", "Bellingham"],
    "W": ["Vinicius", "Saka", "Nico Williams", "Rafael Leão", "Kvaratskhelia"],
    "CF": ["Haaland", "Kane", "Isak", "Gyokeres"],
}

ALIASES = {
    "player": ["player", "player_name", "name"],
    "team": ["team", "club", "squad"],
    "season": ["season", "season_name"],
    "position_taxonomy": ["position_taxonomy", "position_taxonomy_v1", "taxonomy_position"],
    "position_confidence": ["position_confidence", "taxonomy_confidence", "confidence"],
    "pos": ["pos", "pos_", "position", "position_original"],
    "position_group": ["position_group", "pos_group", "base_position_group"],
    "minutes": ["minutes_played", "Playing Time_Min", "Min", "minutes", "playing_time_min"],
    "xg": ["xg", "Expected_xG", "expected_xg", "xG", "npxg", "Expected_npxG"],
    "shots": ["shots", "Shooting_Sh", "standard_Sh", "sh", "shots_total"],
    "shots_on_target": ["shots_on_target", "Shooting_SoT", "sot", "shots_on_target_total"],
    "touches_box": ["touches_box", "Touches_Att Pen", "Possession_Touches_Att Pen", "touches_att_pen", "touches_penalty_area"],
    "carries_box": ["carries_box", "Carries_CPA", "Possession_Carries_CPA", "carries_into_penalty_area"],
    "progressive_carries": ["progressive_carries", "Carries_PrgC", "Possession_Carries_PrgC", "prgc"],
    "progressive_receipts": ["progressive_receipts", "Receiving_PrgR", "Possession_Receiving_PrgR", "prgr"],
    "creation_index_role": ["creation_index_role", "creation_index", "playmaking_index", "playmaking_index_role"],
    "defending_index_role": ["defending_index_role", "defensive_activity_index", "defensive_index", "defensive_index_role"],
    "progression_index_role": ["progression_index_role", "progression_index", "progressive_index_role"],
    "touches_att_third": ["touches_att_third", "Touches_Att 3rd", "Possession_Touches_Att 3rd", "touches_att_3rd"],
    "progressive_passes": ["progressive_passes", "Passing_PrgP", "PrgP", "progressive_passes_total"],
    "key_passes": ["key_passes", "Passing_KP", "KP", "passes_key"],
    "sca": ["sca", "GCA_SCA", "SCA_SCA", "shot_creating_actions"],
    "gca": ["gca", "GCA_GCA", "goal_creating_actions"],
}


def normalize_text(value: object) -> str:
    if pd.isna(value):
        return ""
    text = str(value).strip().lower()
    text = unicodedata.normalize("NFKD", text)
    text = "".join(ch for ch in text if not unicodedata.combining(ch))
    text = re.sub(r"[^a-z0-9 ]+", " ", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text


def find_col(df: pd.DataFrame, canonical: str, required: bool = False) -> str | None:
    candidates = ALIASES.get(canonical, [canonical])
    lower_map = {str(c).lower(): c for c in df.columns}
    for cand in candidates:
        if cand in df.columns:
            return cand
        if cand.lower() in lower_map:
            return lower_map[cand.lower()]
    if required:
        raise KeyError(f"Required column not found for '{canonical}'. Candidates: {candidates}")
    return None


def numeric_series(df: pd.DataFrame, canonical: str) -> pd.Series:
    col = find_col(df, canonical, required=False)
    if col is None:
        return pd.Series(0.0, index=df.index, name=canonical)
    return pd.to_numeric(df[col], errors="coerce").replace([np.inf, -np.inf], np.nan).fillna(0.0)


def safe_minmax(s: pd.Series) -> pd.Series:
    s = pd.to_numeric(s, errors="coerce").replace([np.inf, -np.inf], np.nan)
    if s.notna().sum() == 0:
        return pd.Series(0.5, index=s.index)
    lo, hi = s.quantile(0.02), s.quantile(0.98)
    if not np.isfinite(lo) or not np.isfinite(hi) or hi <= lo:
        return pd.Series(0.5, index=s.index)
    out = (s.clip(lo, hi) - lo) / (hi - lo)
    return out.fillna(0.5).clip(0, 1)


def add_scaled(df: pd.DataFrame, canonical_cols: Iterable[str]) -> pd.DataFrame:
    out = df.copy()
    for c in canonical_cols:
        out[f"_s_{c}"] = safe_minmax(numeric_series(out, c))
    return out


def softmax_conf(scores: pd.DataFrame, labels: list[str]) -> pd.Series:
    arr = scores[labels].to_numpy(dtype=float)
    arr = np.nan_to_num(arr, nan=0.0, posinf=0.0, neginf=0.0)
    top = np.partition(arr, -1, axis=1)[:, -1]
    second = np.partition(arr, -2, axis=1)[:, -2] if arr.shape[1] > 1 else np.zeros(len(arr))
    margin = top - second
    conf = 55 + 45 * safe_minmax(pd.Series(margin, index=scores.index))
    return conf.clip(50, 100).round(1)


def base_group_from_taxonomy(tax: str) -> str:
    if tax == "GK":
        return "GK"
    if tax in {"CB", "FB"}:
        return "DEF"
    if tax in {"DM", "CM", "AM"}:
        return "MID"
    if tax in {"W", "CF"}:
        return "ATT"
    return "UNK"


def infer_group(row: pd.Series) -> str:
    tax = row.get("position_taxonomy_v1", row.get("position_taxonomy", ""))
    grp = base_group_from_taxonomy(str(tax))
    if grp != "UNK":
        return grp
    pos = str(row.get("pos", "")).upper()
    if "GK" in pos:
        return "GK"
    if any(x in pos for x in ["DF", "CB", "LB", "RB", "WB"]):
        return "DEF"
    if any(x in pos for x in ["MF", "DM", "CM", "AM"]):
        return "MID"
    if any(x in pos for x in ["FW", "LW", "RW", "CF", "ST"]):
        return "ATT"
    return "UNK"


def load_inputs(root: Path) -> pd.DataFrame:
    features_path = root / "data" / "processed" / "player_role_features_advanced.parquet"
    taxonomy_path = root / "data" / "processed" / "player_position_taxonomy.parquet"

    if not features_path.exists():
        raise FileNotFoundError(f"Missing input: {features_path}")
    if not taxonomy_path.exists():
        raise FileNotFoundError(f"Missing input: {taxonomy_path}")

    features = pd.read_parquet(features_path)
    tax = pd.read_parquet(taxonomy_path)

    for canonical in ["player", "team", "season"]:
        fcol = find_col(features, canonical, required=True)
        tcol = find_col(tax, canonical, required=True)
        if fcol != canonical:
            features = features.rename(columns={fcol: canonical})
        if tcol != canonical:
            tax = tax.rename(columns={tcol: canonical})

    tax_col = find_col(tax, "position_taxonomy", required=True)
    if tax_col != "position_taxonomy":
        tax = tax.rename(columns={tax_col: "position_taxonomy"})
    tax = tax.rename(columns={"position_taxonomy": "position_taxonomy_v1"})

    conf_col = find_col(tax, "position_confidence", required=False)
    if conf_col and conf_col != "position_confidence":
        tax = tax.rename(columns={conf_col: "position_confidence_v1"})
    elif conf_col == "position_confidence":
        tax = tax.rename(columns={"position_confidence": "position_confidence_v1"})
    else:
        tax["position_confidence_v1"] = 75.0

    keep_tax = ["player", "team", "season", "position_taxonomy_v1", "position_confidence_v1"]
    df = features.merge(tax[keep_tax], on=["player", "team", "season"], how="left")

    pos_col = find_col(df, "pos", required=False)
    if pos_col and pos_col != "pos":
        df = df.rename(columns={pos_col: "pos"})
    elif "pos" not in df.columns:
        df["pos"] = ""

    df["position_taxonomy_v1"] = df["position_taxonomy_v1"].fillna("UNK")
    df["position_family"] = df.apply(infer_group, axis=1)
    return df


def calibrate_taxonomy(df: pd.DataFrame) -> pd.DataFrame:
    feature_cols = [
        "xg", "shots", "shots_on_target", "touches_box", "carries_box",
        "progressive_carries", "progressive_receipts", "creation_index_role",
        "defending_index_role", "progression_index_role", "touches_att_third",
        "progressive_passes", "key_passes", "sca", "gca",
    ]
    df = add_scaled(df, feature_cols)

    # ATT functional scores — TM.6.4.2b calibration
    # Objective: separate wide ball-carrying creators from central finishers.
    # Creation is intentionally excluded from CF_score because players like Kane
    # create heavily while remaining functionally central strikers.
    finisher_signal = (df["_s_xg"] + df["_s_shots_on_target"]) / 2
    finisher_bonus = (finisher_signal > finisher_signal.quantile(0.75)).astype(float) * 0.05
    central_striker_bonus = (
        (df["_s_shots"] > 0.60) & (df["_s_touches_box"] > 0.60)
    ).astype(float) * 0.08

    df["_score_CF"] = (
        0.35 * df["_s_xg"]
        + 0.25 * df["_s_shots"]
        + 0.20 * df["_s_shots_on_target"]
        + 0.20 * df["_s_touches_box"]
        + finisher_bonus
        + central_striker_bonus
    )
    df["_score_W"] = (
        0.35 * df["_s_progressive_carries"]
        + 0.30 * df["_s_carries_box"]
        + 0.25 * df["_s_progressive_receipts"]
        + 0.10 * df["_s_creation_index_role"]
    )

    # MID functional scores
    attack_load = (df["_s_touches_att_third"] + df["_s_touches_box"] + df["_s_sca"] + df["_s_gca"]) / 4
    balance = 1 - (df["_s_defending_index_role"] - df["_s_creation_index_role"]).abs()
    df["_score_DM"] = (
        0.44 * df["_s_defending_index_role"]
        + 0.24 * df["_s_progression_index_role"]
        + 0.18 * df["_s_progressive_passes"]
        + 0.14 * (1 - attack_load)
    )
    df["_score_CM"] = (
        0.34 * df["_s_progression_index_role"]
        + 0.25 * df["_s_progressive_passes"]
        + 0.17 * df["_s_defending_index_role"]
        + 0.14 * df["_s_creation_index_role"]
        + 0.10 * balance
    )
    df["_score_AM"] = (
        0.35 * df["_s_creation_index_role"]
        + 0.25 * df["_s_key_passes"]
        + 0.20 * df["_s_sca"]
        + 0.20 * df["_s_gca"]
    )

    # Preserve non-ambiguous families. Only recalibrate ATT and MID.
    df["position_taxonomy"] = df["position_taxonomy_v1"].where(df["position_taxonomy_v1"].isin(VALID_TAXONOMY), "UNK")
    df["position_confidence"] = pd.to_numeric(df["position_confidence_v1"], errors="coerce").fillna(75.0)

    att_mask = df["position_family"].eq("ATT") | df["position_taxonomy_v1"].isin(ATT_FAMILY)
    mid_mask = df["position_family"].eq("MID") | df["position_taxonomy_v1"].isin(MID_FAMILY)

    att_scores = df.loc[att_mask, ["_score_W", "_score_CF"]].rename(columns={"_score_W": "W", "_score_CF": "CF"})
    if len(att_scores):
        df.loc[att_mask, "position_taxonomy"] = att_scores.idxmax(axis=1)
        df.loc[att_mask, "position_confidence"] = softmax_conf(att_scores, ATT_FAMILY)

    mid_scores = df.loc[mid_mask, ["_score_DM", "_score_CM", "_score_AM"]].rename(
        columns={"_score_DM": "DM", "_score_CM": "CM", "_score_AM": "AM"}
    )
    if len(mid_scores):
        df.loc[mid_mask, "position_taxonomy"] = mid_scores.idxmax(axis=1)
        df.loc[mid_mask, "position_confidence"] = softmax_conf(mid_scores, MID_FAMILY)

    # Conservative fallback for unknowns.
    df.loc[~df["position_taxonomy"].isin(VALID_TAXONOMY), "position_taxonomy"] = df.loc[
        ~df["position_taxonomy"].isin(VALID_TAXONOMY), "position_taxonomy_v1"
    ]
    df["position_confidence"] = pd.to_numeric(df["position_confidence"], errors="coerce").fillna(70).clip(0, 100).round(1)
    return df


def compute_purity(df: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for tax in FIELD_PLAYERS:
        sub = df[df["position_taxonomy"].eq(tax)].copy()
        if sub.empty:
            rows.append({"position_taxonomy": tax, "n": 0, "position_purity_score": np.nan})
            continue

        if tax in ATT_FAMILY:
            own = sub[f"_score_{tax}"]
            other = sub[[f"_score_{x}" for x in ATT_FAMILY if x != tax]].max(axis=1)
            margin = own - other
            family_conf = safe_minmax(margin)
        elif tax in MID_FAMILY:
            own = sub[f"_score_{tax}"]
            other = sub[[f"_score_{x}" for x in MID_FAMILY if x != tax]].max(axis=1)
            margin = own - other
            family_conf = safe_minmax(margin)
        else:
            margin = pd.Series(np.nan, index=sub.index)
            family_conf = pd.to_numeric(sub["position_confidence"], errors="coerce").fillna(75) / 100

        purity = float((100 * family_conf).mean())
        rows.append(
            {
                "position_taxonomy": tax,
                "n": int(len(sub)),
                "share_pct": round(100 * len(sub) / max(len(df), 1), 2),
                "avg_position_confidence": round(float(sub["position_confidence"].mean()), 2),
                "avg_functional_margin": round(float(pd.to_numeric(margin, errors="coerce").mean()), 4)
                if margin.notna().any()
                else np.nan,
                "position_purity_score": round(purity, 2),
            }
        )
    return pd.DataFrame(rows)


def representatives(df: pd.DataFrame, n: int = 15) -> pd.DataFrame:
    rep = df[df["position_taxonomy"].isin(FIELD_PLAYERS)].copy()
    rep = rep.sort_values(["position_taxonomy", "position_confidence"], ascending=[True, False])
    cols = ["player", "team", "season", "position_taxonomy", "position_confidence"]
    optional = ["position_taxonomy_v1", "_score_DM", "_score_CM", "_score_AM", "_score_W", "_score_CF"]
    cols += [c for c in optional if c in rep.columns]
    return rep.groupby("position_taxonomy", group_keys=False).head(n)[cols]


ATTACKING_AUDIT_PLAYERS = {
    "W": {
        "Vinicius": ["vinicius junior", "vinicius júnior", "vinicius jr"],
        "Saka": ["bukayo saka"],
        "Nico Williams": ["nico williams"],
        "Leão": ["rafael leao", "rafael leão"],
        "Kvaratskhelia": ["khvicha kvaratskhelia", "kvaratskhelia"],
    },
    "CF": {
        "Haaland": ["erling haaland"],
        "Kane": ["harry kane"],
        "Isak": ["alexander isak"],
        "Gyokeres": ["viktor gyokeres", "viktor gyökeres", "gyokeres", "gyökeres"],
    },
}


def strict_alias_mask(player_norm: pd.Series, aliases: list[str]) -> pd.Series:
    """Exact semantic audit mask.

    Avoids false positives such as:
    - Saka matching Wan-Bissaka
    - Rodri matching Rodriguez
    - Vinicius matching Carlos Vinicius or Vinicius Souza when auditing Vinicius Junior
    """
    mask = pd.Series(False, index=player_norm.index)
    for alias in aliases:
        norm_alias = normalize_text(alias)
        if not norm_alias:
            continue
        # Exact full-name match or exact alias token sequence bounded by word boundaries.
        pattern = rf"(^|\s){re.escape(norm_alias)}($|\s)"
        mask = mask | player_norm.str.fullmatch(re.escape(norm_alias), na=False) | player_norm.str.contains(pattern, na=False, regex=True)
    return mask


def attacking_audit_report(df: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    rows = []
    df = df.copy()
    df["_player_norm"] = df["player"].map(normalize_text)
    for expected, player_map in ATTACKING_AUDIT_PLAYERS.items():
        for audit_name, aliases in player_map.items():
            sub = df.loc[strict_alias_mask(df["_player_norm"], aliases)].copy()
            if sub.empty:
                rows.append(
                    {
                        "audit_player": audit_name,
                        "expected_taxonomy": expected,
                        "observations_found": 0,
                        "assigned_taxonomies": "NOT_FOUND",
                        "success_rate_pct": np.nan,
                        "avg_confidence": np.nan,
                        "status": "NOT_FOUND",
                        "sample_rows": "",
                    }
                )
                continue
            success = sub["position_taxonomy"].eq(expected)
            rows.append(
                {
                    "audit_player": audit_name,
                    "expected_taxonomy": expected,
                    "observations_found": int(len(sub)),
                    "assigned_taxonomies": ", ".join(
                        f"{k}:{v}" for k, v in sub["position_taxonomy"].value_counts().to_dict().items()
                    ),
                    "success_rate_pct": round(100 * float(success.mean()), 1),
                    "avg_confidence": round(float(sub["position_confidence"].mean()), 1),
                    "status": "PASS" if 100 * float(success.mean()) >= 80 else "REVIEW",
                    "sample_rows": " | ".join(
                        sub[["player", "team", "season", "position_taxonomy"]]
                        .head(8)
                        .astype(str)
                        .agg(" - ".join, axis=1)
                        .tolist()
                    ),
                }
            )
    detail = pd.DataFrame(rows)
    found = detail[detail["observations_found"].fillna(0).astype(float) > 0].copy()
    overall = pd.DataFrame(
        [
            {
                "audit_scope": "ATT",
                "players_found": int(len(found)),
                "players_expected": int(sum(len(v) for v in ATTACKING_AUDIT_PLAYERS.values())),
                "avg_success_rate_pct_found_players": round(float(found["success_rate_pct"].mean()), 1) if len(found) else np.nan,
                "min_success_rate_pct_found_players": round(float(found["success_rate_pct"].min()), 1) if len(found) else np.nan,
                "players_pass_80pct": int((found["success_rate_pct"] >= 80).sum()) if len(found) else 0,
                "closure_threshold_pct": 80.0,
                "closure_status": "PASS" if len(found) > 0 and (found["success_rate_pct"] >= 80).all() else "REVIEW",
                "note": "NOT_FOUND players are reported but excluded from the threshold because they are outside current data coverage.",
            }
        ]
    )
    return detail, overall


def validation_report(df: pd.DataFrame) -> pd.DataFrame:
    rows = []
    df = df.copy()
    df["_player_norm"] = df["player"].map(normalize_text)
    for expected, players in VALIDATION_PLAYERS.items():
        for target in players:
            target_norm = normalize_text(target)
            mask = df["_player_norm"].str.contains(re.escape(target_norm), na=False)
            sub = df.loc[mask].copy()
            if sub.empty:
                rows.append(
                    {
                        "audit_player": target,
                        "expected_taxonomy": expected,
                        "observations_found": 0,
                        "assigned_taxonomies": "NOT_FOUND",
                        "success_rate_pct": np.nan,
                        "status": "NOT_FOUND",
                    }
                )
                continue
            success = sub["position_taxonomy"].eq(expected)
            rows.append(
                {
                    "audit_player": target,
                    "expected_taxonomy": expected,
                    "observations_found": int(len(sub)),
                    "assigned_taxonomies": ", ".join(
                        f"{k}:{v}" for k, v in sub["position_taxonomy"].value_counts().to_dict().items()
                    ),
                    "success_rate_pct": round(100 * float(success.mean()), 1),
                    "avg_confidence": round(float(sub["position_confidence"].mean()), 1),
                    "status": "PASS" if success.all() else "REVIEW",
                    "sample_rows": " | ".join(
                        sub[["player", "team", "season", "position_taxonomy"]]
                        .head(5)
                        .astype(str)
                        .agg(" - ".join, axis=1)
                        .tolist()
                    ),
                }
            )
    return pd.DataFrame(rows)


def distribution(df: pd.DataFrame) -> pd.DataFrame:
    out = (
        df["position_taxonomy"]
        .value_counts(dropna=False)
        .rename_axis("position_taxonomy")
        .reset_index(name="n")
    )
    out["share_pct"] = (100 * out["n"] / max(len(df), 1)).round(2)
    order = {v: i for i, v in enumerate(VALID_TAXONOMY)}
    out["_order"] = out["position_taxonomy"].map(order).fillna(99)
    return out.sort_values("_order").drop(columns="_order")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", default=".", help="Project root path")
    parser.add_argument("--min-minutes", type=float, default=0.0, help="Optional minimum minutes filter for reports only")
    args = parser.parse_args()

    root = Path(args.root).resolve()
    processed = root / "data" / "processed"
    reports = root / "reports" / "roles"
    processed.mkdir(parents=True, exist_ok=True)
    reports.mkdir(parents=True, exist_ok=True)

    df = load_inputs(root)
    calibrated = calibrate_taxonomy(df)

    output_cols = ["player", "team", "season", "position_taxonomy", "position_confidence"]
    output = calibrated[output_cols].copy()
    output.to_parquet(processed / "player_position_taxonomy_v2b.parquet", index=False)
    # Also update the canonical v2 artifact so downstream TM.6.5 can consume the stabilized taxonomy by default.
    output.to_parquet(processed / "player_position_taxonomy_v2.parquet", index=False)

    report_df = calibrated.copy()
    min_col = find_col(report_df, "minutes", required=False)
    if args.min_minutes > 0 and min_col is not None:
        report_df = report_df[pd.to_numeric(report_df[min_col], errors="coerce").fillna(0) >= args.min_minutes]

    distribution(report_df).to_csv(reports / "position_taxonomy_distribution_v2b.csv", index=False)
    validation_report(report_df).to_csv(reports / "position_taxonomy_validation_v2b.csv", index=False)
    att_detail, att_summary = attacking_audit_report(report_df)
    att_detail.to_csv(reports / "position_taxonomy_attacking_audit_v2b.csv", index=False)
    att_summary.to_csv(reports / "position_taxonomy_attacking_audit_summary_v2b.csv", index=False)
    representatives(report_df).to_csv(reports / "position_taxonomy_representatives_v2b.csv", index=False)
    compute_purity(report_df).to_csv(reports / "position_taxonomy_purity_v2b.csv", index=False)

    summary = {
        "rows": int(len(output)),
        "distribution": distribution(report_df).to_dict(orient="records"),
        "outputs": [
            str(processed / "player_position_taxonomy_v2b.parquet"),
            str(reports / "position_taxonomy_distribution_v2b.csv"),
            str(reports / "position_taxonomy_validation_v2b.csv"),
            str(reports / "position_taxonomy_attacking_audit_v2b.csv"),
            str(reports / "position_taxonomy_attacking_audit_summary_v2b.csv"),
            str(reports / "position_taxonomy_representatives_v2b.csv"),
            str(reports / "position_taxonomy_purity_v2b.csv"),
        ],
    }
    print(json.dumps(summary, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
