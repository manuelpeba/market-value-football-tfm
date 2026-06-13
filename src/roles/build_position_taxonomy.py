"""
TM.6.4.1 — Position Taxonomy Resolution

Builds a reproducible, data-driven football position taxonomy from FBref-derived
role features. The model uses pos_ only to define plausible candidate universes,
not as the final label. The final label is inferred from tactical-statistical
profiles.

Outputs
-------
data/processed/player_position_taxonomy.parquet
reports/roles/position_taxonomy_distribution.csv
reports/roles/position_taxonomy_representatives.csv
reports/roles/position_taxonomy_validation.csv

Run
---
python src/roles/build_position_taxonomy.py
"""

from __future__ import annotations

import argparse
import json
import math
import unicodedata
from pathlib import Path
from typing import Dict, Iterable, List, Optional, Sequence, Tuple

import numpy as np
import pandas as pd


TAXONOMIES = ["CB", "FB", "DM", "CM", "AM", "W", "CF"]
REQUIRED_ID_CANDIDATES = {
    "player": ["player", "player_name", "name"],
    "team": ["team", "club", "squad"],
    "season": ["season", "season_start_year", "year"],
    "pos": ["pos_", "position", "positions", "position_group"],
}

ALIASES: Dict[str, Sequence[str]] = {
    # Playing time / identifiers
    "minutes": ["minutes", "Playing Time_Min", "minutes_played", "min", "90s", "nineties"],

    # Creation
    "key_passes": ["key_passes_p90", "KP_p90", "Passing_KP_p90", "KP"],
    "sca": ["sca_p90", "SCA_SCA90", "SCA90", "sca"],
    "gca": ["gca_p90", "GCA_GCA90", "GCA90", "gca"],
    "gca_live": ["gca_live_p90", "GCA_GCA_Live_p90", "GCA_Live"],

    # Progression
    "progressive_passes": ["progressive_passes_p90", "PrgP_p90", "Passing_PrgP_p90", "PrgP"],
    "progressive_carries": ["progressive_carries_p90", "PrgC_p90", "Carries_PrgC_p90", "PrgC"],
    "progressive_receipts": ["progressive_receipts_p90", "PrgR_p90", "Receiving_PrgR_p90", "PrgR"],

    # Finalisation
    "xg": ["xg_p90", "Expected_xG_p90", "xG_p90", "xG"],
    "shots": ["shots_p90", "Standard_Sh_p90", "Sh_p90", "shots"],
    "sot": ["sot_p90", "Standard_SoT_p90", "SoT_p90", "shots_on_target_p90"],
    "g_per_shot": ["g_per_shot", "Standard_G/Sh", "G/Sh"],
    "g_per_sot": ["g_per_sot", "Standard_G/SoT", "G/SoT"],

    # Defence
    "tackles": ["tackles_p90", "Tackles_Tkl_p90", "Tkl_p90", "tackles"],
    "tackles_won": ["tackles_won_p90", "Tackles_TklW_p90", "TklW_p90"],
    "interceptions": ["interceptions_p90", "Int_p90", "interceptions"],
    "recoveries": ["recoveries_p90", "Recov_p90", "recoveries"],
    "blocks": ["blocks_p90", "Blocks_Blocks_p90", "Blocks_p90", "blocks"],
    "clearances": ["clearances_p90", "Clr_p90", "clearances"],
    "aerials_won": ["aerials_won_p90", "Aerial Duels_Won_p90", "Aerials_Won_p90"],
    "aerials_lost": ["aerials_lost_p90", "Aerial Duels_Lost_p90", "Aerials_Lost_p90"],
    "aerials_won_pct": ["aerial_duels_won_pct", "aerials_won_pct", "Aerial Duels_Won%"],

    # Possession / zones
    "touches_att_third": ["touches_att_third_p90", "Touches_Att 3rd_p90", "Att 3rd_p90"],
    "touches_box": ["touches_box_p90", "Touches_Att Pen_p90", "Att Pen_p90", "touches_att_pen_p90"],
    "carries_box": ["carries_box_p90", "Carries_CPA_p90", "CPA_p90", "carries_into_penalty_area_p90"],
    "take_ons": ["take_ons_p90", "Take-Ons_Att_p90", "takeons_p90", "dribbles_attempted_p90"],
    "successful_take_ons": ["successful_take_ons_p90", "Take-Ons_Succ_p90", "dribbles_completed_p90"],

    # Existing synthetic indices when available
    "creation_index": ["creation_index_role", "playmaking_index", "creation_index"],
    "progression_index": ["progression_index_role", "progression_index"],
    "defending_index": ["defending_index_role", "defensive_activity_index", "defending_index"],
    "finishing_index": ["finishing_index_role", "finishing_index_v2", "finishing_index"],
    "duel_index": ["duel_index_role", "duel_index"],
}

KNOWN_VALIDATION = {
    "Bastoni": "CB",
    "Rúben Dias": "CB",
    "Ruben Dias": "CB",
    "Van Dijk": "CB",
    "Hakimi": "FB",
    "Frimpong": "FB",
    "Theo Hernández": "FB",
    "Theo Hernandez": "FB",
    "Caicedo": "DM",
    "Endo": "DM",
    "Ugarte": "DM",
    "Rodri": "DM",       # may be DM/CM depending season, expected as organiser/6 profile
    "Vitinha": "CM",
    "Zubimendi": "DM",
    "Pedri": "AM",
    "Wirtz": "AM",
    "Bellingham": "AM",
    "Vinicius": "W",
    "Vinícius": "W",
    "Saka": "W",
    "Nico Williams": "W",
    "Haaland": "CF",
    "Kane": "CF",
    "Isak": "CF",
}


# ---------------------------------------------------------------------------
# Path / IO helpers
# ---------------------------------------------------------------------------

def find_project_root() -> Path:
    current = Path(__file__).resolve()
    for candidate in [current.parent, *current.parents]:
        if (candidate / "data").exists() or (candidate / "reports").exists():
            return candidate
    return current.parents[2]


def pick_column(df: pd.DataFrame, candidates: Sequence[str], required: bool = False) -> Optional[str]:
    lower_map = {str(c).lower(): c for c in df.columns}
    for c in candidates:
        if c in df.columns:
            return c
        if c.lower() in lower_map:
            return lower_map[c.lower()]
    if required:
        raise KeyError(f"None of the required columns were found: {candidates}")
    return None


def resolve_id_columns(df: pd.DataFrame) -> Dict[str, str]:
    return {
        key: pick_column(df, candidates, required=True)
        for key, candidates in REQUIRED_ID_CANDIDATES.items()
    }


def to_numeric_series(df: pd.DataFrame, canonical_name: str) -> pd.Series:
    col = pick_column(df, ALIASES[canonical_name], required=False)
    if col is None:
        return pd.Series(np.nan, index=df.index, dtype="float64")
    s = pd.to_numeric(df[col], errors="coerce")

    # If a feature is a season total rather than per90, convert when minutes are available.
    minutes_col = pick_column(df, ALIASES["minutes"], required=False)
    if col.lower().endswith("_p90") or "90" in col.lower() or canonical_name in {"g_per_shot", "g_per_sot", "aerials_won_pct"}:
        return s
    if minutes_col is not None and canonical_name not in {"minutes"}:
        mins = pd.to_numeric(df[minutes_col], errors="coerce")
        nineties = mins / 90.0
        return np.where(nineties > 0, s / nineties, np.nan)
    return s


# ---------------------------------------------------------------------------
# Feature construction
# ---------------------------------------------------------------------------

def robust_z(s: pd.Series) -> pd.Series:
    s = pd.to_numeric(s, errors="coerce")
    med = s.median(skipna=True)
    q1 = s.quantile(0.25)
    q3 = s.quantile(0.75)
    iqr = q3 - q1
    if not np.isfinite(iqr) or iqr <= 1e-9:
        std = s.std(skipna=True)
        if not np.isfinite(std) or std <= 1e-9:
            return pd.Series(0.0, index=s.index)
        z = (s - s.mean(skipna=True)) / std
    else:
        z = (s - med) / (iqr / 1.349)
    return z.clip(-3.0, 3.0).fillna(0.0)


def zmean(zdf: pd.DataFrame, cols: Sequence[str], weights: Optional[Sequence[float]] = None) -> pd.Series:
    existing = [c for c in cols if c in zdf.columns]
    if not existing:
        return pd.Series(0.0, index=zdf.index)
    mat = zdf[existing].astype(float)
    if weights is None:
        return mat.mean(axis=1)
    w = np.array(weights[: len(existing)], dtype=float)
    w = w / w.sum() if w.sum() else np.ones(len(existing)) / len(existing)
    return pd.Series(mat.to_numpy() @ w, index=zdf.index)


def build_metric_table(df: pd.DataFrame) -> pd.DataFrame:
    metrics = pd.DataFrame(index=df.index)
    for canonical in ALIASES:
        metrics[canonical] = to_numeric_series(df, canonical)

    # Derived metric: aerial volume + success where available.
    metrics["aerial_profile"] = metrics[["aerials_won", "aerials_won_pct", "duel_index"]].mean(axis=1, skipna=True)

    # Robust standardisation across the observed universe. This keeps the procedure
    # deterministic and avoids leaking manual labels into the taxonomy.
    zdf = pd.DataFrame(index=df.index)
    for c in metrics.columns:
        zdf[c] = robust_z(metrics[c])

    # Tactical dimensions used by the label engine.
    dim = pd.DataFrame(index=df.index)
    dim["def_centrality"] = zmean(zdf, ["clearances", "blocks", "aerial_profile", "duel_index"], [0.35, 0.25, 0.25, 0.15])
    dim["def_mobility"] = zmean(zdf, ["tackles", "tackles_won", "interceptions", "recoveries"], [0.30, 0.20, 0.30, 0.20])
    dim["progression"] = zmean(zdf, ["progressive_passes", "progressive_carries", "progression_index"], [0.40, 0.40, 0.20])
    dim["wide_progression"] = zmean(zdf, ["progressive_carries", "progressive_receipts", "touches_att_third", "take_ons", "successful_take_ons"], [0.28, 0.22, 0.20, 0.18, 0.12])
    dim["creation"] = zmean(zdf, ["key_passes", "sca", "gca", "gca_live", "creation_index"], [0.25, 0.30, 0.20, 0.10, 0.15])
    dim["box_presence"] = zmean(zdf, ["touches_box", "carries_box", "xg", "shots"], [0.25, 0.20, 0.35, 0.20])
    dim["finishing"] = zmean(zdf, ["xg", "shots", "sot", "g_per_shot", "g_per_sot", "finishing_index"], [0.25, 0.18, 0.18, 0.12, 0.12, 0.15])
    dim["attacking_zone"] = zmean(zdf, ["touches_att_third", "touches_box", "carries_box", "progressive_receipts"], [0.25, 0.30, 0.20, 0.25])

    return pd.concat([metrics.add_prefix("raw_"), zdf.add_prefix("z_"), dim], axis=1)


# ---------------------------------------------------------------------------
# Candidate generation and scoring
# ---------------------------------------------------------------------------

def clean_text(x: object) -> str:
    return "" if pd.isna(x) else str(x).strip()


def position_tokens(pos: object) -> List[str]:
    txt = clean_text(pos).upper().replace("-", ",").replace("/", ",").replace(" ", "")
    tokens = [t for t in txt.split(",") if t]
    expanded: List[str] = []
    for t in tokens:
        if t in {"D", "DEF", "DF"}:
            expanded.append("DF")
        elif t in {"M", "MID", "MF"}:
            expanded.append("MF")
        elif t in {"A", "ATT", "FW", "F"}:
            expanded.append("FW")
        elif t == "GK":
            expanded.append("GK")
        else:
            # FBref detailed labels occasionally appear; map conservatively.
            if t in {"CB", "LB", "RB", "LWB", "RWB"}:
                expanded.append("DF")
            elif t in {"DM", "CM", "AM", "LM", "RM"}:
                expanded.append("MF")
            elif t in {"LW", "RW", "ST", "CF"}:
                expanded.append("FW")
    return sorted(set(expanded))


def candidate_taxonomies(tokens: Sequence[str]) -> List[str]:
    s = set(tokens)
    if "GK" in s:
        return []
    if not s:
        return TAXONOMIES.copy()
    candidates: List[str] = []
    if s == {"DF"}:
        candidates = ["CB", "FB"]
    elif s == {"MF"}:
        candidates = ["DM", "CM", "AM"]
    elif s == {"FW"}:
        candidates = ["W", "CF"]
    elif s == {"DF", "MF"}:
        candidates = ["FB", "DM", "CM"]
    elif s == {"MF", "FW"}:
        candidates = ["CM", "AM", "W", "CF"]
    elif s == {"DF", "FW"}:
        candidates = ["FB", "W"]
    else:
        # Very ambiguous rows: all outfield taxonomies remain possible.
        candidates = TAXONOMIES.copy()
    return candidates


def compute_taxonomy_scores(dim: pd.DataFrame) -> pd.DataFrame:
    scores = pd.DataFrame(index=dim.index)

    # CB: central defence, aerial/clearance profile, not high final-third/carry profile.
    scores["CB"] = (
        0.42 * dim["def_centrality"]
        + 0.24 * dim["def_mobility"]
        - 0.18 * dim["wide_progression"]
        - 0.10 * dim["attacking_zone"]
        - 0.06 * dim["finishing"]
    )

    # FB: mobile/wide defender with progression/carrying, but lower pure central-defender signal.
    scores["FB"] = (
        0.26 * dim["def_mobility"]
        + 0.30 * dim["wide_progression"]
        + 0.18 * dim["progression"]
        + 0.12 * dim["creation"]
        - 0.22 * dim["def_centrality"]
        - 0.08 * dim["finishing"]
    )

    # DM: defensive activity + progression from deeper zones, limited box/finalisation.
    scores["DM"] = (
        0.34 * dim["def_mobility"]
        + 0.28 * dim["progression"]
        + 0.12 * dim["def_centrality"]
        - 0.20 * dim["box_presence"]
        - 0.06 * dim["finishing"]
    )

    # CM: balanced organiser/progressor, not overly defensive nor striker-like.
    scores["CM"] = (
        0.34 * dim["progression"]
        + 0.22 * dim["creation"]
        + 0.18 * dim["def_mobility"]
        - 0.12 * dim["def_centrality"]
        - 0.10 * dim["finishing"]
    )

    # AM: creative final-third midfielder, high creation/attacking-zone, not winger/striker dominated.
    scores["AM"] = (
        0.38 * dim["creation"]
        + 0.25 * dim["attacking_zone"]
        + 0.16 * dim["progression"]
        + 0.08 * dim["box_presence"]
        - 0.16 * dim["def_centrality"]
        - 0.10 * dim["def_mobility"]
    )

    # W: wide receiver/carrier/creator; can have box entries but should not look like a pure CF.
    scores["W"] = (
        0.40 * dim["wide_progression"]
        + 0.23 * dim["creation"]
        + 0.17 * dim["attacking_zone"]
        + 0.07 * dim["finishing"]
        - 0.14 * dim["def_centrality"]
        - 0.08 * dim["box_presence"]
    )

    # CF: central finisher with box/xG/shot dominance and lower wide-carry dependency.
    scores["CF"] = (
        0.46 * dim["finishing"]
        + 0.32 * dim["box_presence"]
        + 0.08 * dim["attacking_zone"]
        - 0.18 * dim["wide_progression"]
        - 0.12 * dim["def_mobility"]
    )
    return scores


def masked_softmax(row: pd.Series, allowed: Sequence[str]) -> Tuple[str, float, float, Dict[str, float]]:
    if not allowed:
        return "GK", 1.0, 1.0, {"GK": 1.0}
    vals = row.loc[list(allowed)].astype(float)
    vals = vals.replace([np.inf, -np.inf], np.nan).fillna(vals.median() if vals.notna().any() else 0.0)
    arr = vals.to_numpy(dtype=float)
    arr = arr - np.nanmax(arr)
    exp = np.exp(arr)
    probs = exp / exp.sum() if exp.sum() else np.ones_like(exp) / len(exp)
    prob_s = pd.Series(probs, index=allowed).sort_values(ascending=False)
    label = str(prob_s.index[0])
    top1 = float(prob_s.iloc[0])
    top2 = float(prob_s.iloc[1]) if len(prob_s) > 1 else 0.0
    # Confidence combines absolute dominance and separation from the second-best taxonomy.
    confidence = 100.0 * (0.65 * top1 + 0.35 * max(top1 - top2, 0.0))
    return label, float(confidence), float(top1 - top2), {k: float(v) for k, v in prob_s.items()}


def build_taxonomy(df: pd.DataFrame) -> Tuple[pd.DataFrame, pd.DataFrame]:
    ids = resolve_id_columns(df)
    dim = build_metric_table(df)
    scores = compute_taxonomy_scores(dim)

    tokens = df[ids["pos"]].map(position_tokens)
    allowed = tokens.map(candidate_taxonomies)

    labels: List[str] = []
    confs: List[float] = []
    margins: List[float] = []
    prob_json: List[str] = []
    for idx, allowed_i in allowed.items():
        label, conf, margin, probs = masked_softmax(scores.loc[idx], allowed_i)
        labels.append(label)
        confs.append(round(conf, 2))
        margins.append(round(margin, 4))
        prob_json.append(json.dumps(probs, ensure_ascii=False))

    out = pd.DataFrame({
        "player": df[ids["player"]].astype(str),
        "season": df[ids["season"]],
        "team": df[ids["team"]].astype(str),
        "pos_": df[ids["pos"]].astype(str),
        "position_taxonomy": labels,
        "position_confidence": confs,
        "position_margin": margins,
        "position_candidate_set": allowed.map(lambda x: ",".join(x)),
        "position_probability_json": prob_json,
    })

    diagnostics = pd.concat([out, scores.add_prefix("score_"), dim], axis=1)
    return out, diagnostics


# ---------------------------------------------------------------------------
# Reports
# ---------------------------------------------------------------------------

def normalize_name(s: object) -> str:
    txt = clean_text(s).lower()
    txt = "".join(ch for ch in unicodedata.normalize("NFKD", txt) if not unicodedata.combining(ch))
    return txt


def build_distribution(out: pd.DataFrame) -> pd.DataFrame:
    dist = (
        out.groupby(["position_taxonomy"], dropna=False)
        .agg(
            n_players=("player", "count"),
            avg_confidence=("position_confidence", "mean"),
            median_confidence=("position_confidence", "median"),
        )
        .reset_index()
        .sort_values("position_taxonomy")
    )
    dist["share_pct"] = (dist["n_players"] / max(len(out), 1) * 100).round(2)
    dist["avg_confidence"] = dist["avg_confidence"].round(2)
    dist["median_confidence"] = dist["median_confidence"].round(2)
    return dist


def build_representatives(diagnostics: pd.DataFrame, top_n: int = 15) -> pd.DataFrame:
    reps = []
    for tax in TAXONOMIES:
        subset = diagnostics[diagnostics["position_taxonomy"] == tax].copy()
        if subset.empty:
            continue
        score_col = f"score_{tax}"
        subset["representative_score"] = (
            pd.to_numeric(subset["position_confidence"], errors="coerce") * 0.65
            + robust_z(subset[score_col]) * 10.0 * 0.35
        )
        reps.append(
            subset.sort_values(["representative_score", "position_confidence"], ascending=False)
            .head(top_n)[["position_taxonomy", "player", "team", "season", "pos_", "position_confidence", "representative_score"]]
        )
    if not reps:
        return pd.DataFrame(columns=["position_taxonomy", "player", "team", "season", "pos_", "position_confidence", "representative_score"])
    return pd.concat(reps, ignore_index=True)


def build_validation(out: pd.DataFrame) -> pd.DataFrame:
    validation_rows = []
    tmp = out.copy()
    tmp["_name_norm"] = tmp["player"].map(normalize_name)

    for query, expected in KNOWN_VALIDATION.items():
        qn = normalize_name(query)
        matched = tmp[tmp["_name_norm"].str.contains(qn, na=False)].copy()
        if matched.empty and " " in qn:
            # fallback for partial names such as Van Dijk / Theo Hernandez
            parts = [p for p in qn.split() if len(p) >= 3]
            mask = pd.Series(True, index=tmp.index)
            for p in parts:
                mask &= tmp["_name_norm"].str.contains(p, na=False)
            matched = tmp[mask].copy()
        if matched.empty:
            validation_rows.append({
                "query_player": query,
                "expected_taxonomy": expected,
                "player": None,
                "team": None,
                "season": None,
                "pos_": None,
                "position_taxonomy": None,
                "position_confidence": None,
                "validation_status": "not_found",
            })
            continue
        matched = matched.sort_values(["season", "position_confidence"], ascending=[False, False]).head(5)
        for _, r in matched.iterrows():
            validation_rows.append({
                "query_player": query,
                "expected_taxonomy": expected,
                "player": r["player"],
                "team": r["team"],
                "season": r["season"],
                "pos_": r["pos_"],
                "position_taxonomy": r["position_taxonomy"],
                "position_confidence": r["position_confidence"],
                "validation_status": "pass" if r["position_taxonomy"] == expected else "review",
            })
    return pd.DataFrame(validation_rows)


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def parse_args() -> argparse.Namespace:
    root = find_project_root()
    parser = argparse.ArgumentParser(description="Build TM.6.4.1 position taxonomy.")
    parser.add_argument(
        "--input",
        default=str(root / "data" / "processed" / "player_role_features_advanced.parquet"),
        help="Input parquet with advanced role features.",
    )
    parser.add_argument(
        "--output",
        default=str(root / "data" / "processed" / "player_position_taxonomy.parquet"),
        help="Output parquet for position taxonomy.",
    )
    parser.add_argument(
        "--reports-dir",
        default=str(root / "reports" / "roles"),
        help="Directory for CSV reports.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    input_path = Path(args.input)
    output_path = Path(args.output)
    reports_dir = Path(args.reports_dir)

    if not input_path.exists():
        raise FileNotFoundError(
            f"Input dataset not found: {input_path}. "
            "Run TM.6.2 first or pass --input with the correct parquet path."
        )

    output_path.parent.mkdir(parents=True, exist_ok=True)
    reports_dir.mkdir(parents=True, exist_ok=True)

    df = pd.read_parquet(input_path)
    taxonomy, diagnostics = build_taxonomy(df)

    taxonomy.to_parquet(output_path, index=False)

    distribution = build_distribution(taxonomy)
    representatives = build_representatives(diagnostics)
    validation = build_validation(taxonomy)

    distribution.to_csv(reports_dir / "position_taxonomy_distribution.csv", index=False)
    representatives.to_csv(reports_dir / "position_taxonomy_representatives.csv", index=False)
    validation.to_csv(reports_dir / "position_taxonomy_validation.csv", index=False)

    print("TM.6.4.1 — Position Taxonomy Resolution completed")
    print(f"Input rows: {len(df):,}")
    print(f"Output: {output_path}")
    print(f"Reports: {reports_dir}")
    print("\nDistribution:")
    print(distribution.to_string(index=False))
    print("\nValidation summary:")
    if not validation.empty:
        print(validation["validation_status"].value_counts(dropna=False).to_string())


if __name__ == "__main__":
    main()
