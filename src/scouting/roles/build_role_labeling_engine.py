#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
TM.6.4 — Role Labeling Engine

Transforms unsupervised archetype clusters generated in TM.6.3 into interpretable
football role labels ready for DSS integration.

Inputs
------
- data/processed/player_role_archetypes.parquet
- reports/roles/archetype_feature_centroids.csv
- reports/roles/archetype_representatives.csv   optional, for report enrichment

Outputs
-------
- data/processed/player_role_labels.parquet
- reports/roles/player_role_labels.csv
- reports/roles/role_distribution.csv
- reports/roles/role_representatives.csv
- reports/roles/role_label_mapping.csv

Design principles
-----------------
- Labels are derived from centroid signatures, not imposed before clustering.
- MID labels are fixed from TM.6.3 validation.
- DEF_CB and ATT_CF labels are inferred using dominant z-score features.
- Secondary role is assigned from distance/similarity to non-primary archetype centroids
  within the same role_subgroup.
"""

from __future__ import annotations

import argparse
import json
import math
import re
import unicodedata
from pathlib import Path
from typing import Dict, Iterable, List, Optional, Tuple

import numpy as np
import pandas as pd


# =============================================================================
# Paths
# =============================================================================


def find_project_root() -> Path:
    current = Path(__file__).resolve()
    candidates = [current.parent, *current.parents, Path.cwd(), *Path.cwd().parents]
    for candidate in candidates:
        if (candidate / "data" / "processed").exists() or (candidate / "reports" / "roles").exists():
            return candidate
    return Path.cwd()


ROOT = find_project_root()
PROCESSED_DIR = ROOT / "data" / "processed"
REPORTS_DIR = ROOT / "reports" / "roles"

INPUT_ARCHETYPES = PROCESSED_DIR / "player_role_archetypes.parquet"
INPUT_CENTROIDS = REPORTS_DIR / "archetype_feature_centroids.csv"
INPUT_REPRESENTATIVES = REPORTS_DIR / "archetype_representatives.csv"

OUTPUT_LABELS_PARQUET = PROCESSED_DIR / "player_role_labels.parquet"
OUTPUT_LABELS_CSV = REPORTS_DIR / "player_role_labels.csv"
OUTPUT_DISTRIBUTION = REPORTS_DIR / "role_distribution.csv"
OUTPUT_REPRESENTATIVES = REPORTS_DIR / "role_representatives.csv"
OUTPUT_MAPPING = REPORTS_DIR / "role_label_mapping.csv"
OUTPUT_AUDIT = REPORTS_DIR / "role_labeling_audit.json"


# =============================================================================
# Label dictionaries and descriptions
# =============================================================================

MID_VALIDATED_LABELS = {
    0: "Attacking Progressor",
    1: "Ball Winner",
    2: "Creative Playmaker",
}

ROLE_DESCRIPTIONS = {
    "Attacking Progressor": (
        "Midfielder/attacking midfielder who receives between lines, carries forward "
        "and attacks advanced zones through movement and ball progression."
    ),
    "Ball Winner": (
        "Midfielder with high defensive involvement, recoveries, interceptions and tackles; "
        "prioritises disruption, balance and ball recovery."
    ),
    "Creative Playmaker": (
        "High-creation midfielder who generates key passes, shot-creating actions, goal-creating "
        "actions and passes into dangerous areas."
    ),
    "Ball-Playing Centre-Back": (
        "Centre-back with above-average progression and distribution contribution, involved in build-up."
    ),
    "Defensive Stopper": (
        "Centre-back focused on direct defensive actions: blocks, clearances, duels and protection of the box."
    ),
    "Aerial Defender": (
        "Centre-back with strong aerial-duel profile and defensive box presence."
    ),
    "Aggressive Defender": (
        "Centre-back with proactive defensive behaviour through tackles, interceptions and pressure events."
    ),
    "Box Finisher": (
        "Forward with strong penalty-area presence, close-range finishing and high xG involvement."
    ),
    "Mobile Forward": (
        "Forward who combines finishing with carrying, take-ons and attacking movement across zones."
    ),
    "Creator Forward": (
        "Forward who contributes heavily to chance creation, SCA/GCA and associative attacking play."
    ),
    "Volume Shooter": (
        "Forward with high shot volume and attacking output, not necessarily the most efficient finisher."
    ),
    "Unlabeled Archetype": (
        "Data-derived archetype pending manual tactical validation."
    ),
}

ROLE_EMOJIS = {
    "Attacking Progressor": "🚀",
    "Ball Winner": "🛡️",
    "Creative Playmaker": "🧠",
    "Ball-Playing Centre-Back": "🎯",
    "Defensive Stopper": "🧱",
    "Aerial Defender": "🦅",
    "Aggressive Defender": "⚔️",
    "Box Finisher": "🎯",
    "Mobile Forward": "⚡",
    "Creator Forward": "🧩",
    "Volume Shooter": "🚀",
    "Unlabeled Archetype": "🧬",
}


# =============================================================================
# Utilities
# =============================================================================


def normalize_text(value: object) -> str:
    if pd.isna(value):
        return ""
    txt = str(value).strip().lower()
    txt = unicodedata.normalize("NFKD", txt)
    txt = "".join(ch for ch in txt if not unicodedata.combining(ch))
    txt = re.sub(r"[^a-z0-9]+", " ", txt)
    return re.sub(r"\s+", " ", txt).strip()


def safe_numeric(series: pd.Series) -> pd.Series:
    return pd.to_numeric(series, errors="coerce")


def ensure_dirs() -> None:
    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)


def read_inputs() -> Tuple[pd.DataFrame, pd.DataFrame, Optional[pd.DataFrame]]:
    if not INPUT_ARCHETYPES.exists():
        raise FileNotFoundError(
            f"Missing input: {INPUT_ARCHETYPES}. Run TM.6.3 first: "
            "python src/scouting/roles/build_archetype_discovery.py"
        )
    if not INPUT_CENTROIDS.exists():
        raise FileNotFoundError(
            f"Missing input: {INPUT_CENTROIDS}. Run TM.6.3 first."
        )

    archetypes = pd.read_parquet(INPUT_ARCHETYPES)
    centroids = pd.read_csv(INPUT_CENTROIDS)
    reps = pd.read_csv(INPUT_REPRESENTATIVES) if INPUT_REPRESENTATIVES.exists() else None
    return archetypes, centroids, reps


def detect_id_cols(df: pd.DataFrame) -> Tuple[str, str]:
    subgroup_col = "role_subgroup" if "role_subgroup" in df.columns else None
    archetype_col = "archetype_id" if "archetype_id" in df.columns else None
    if subgroup_col is None or archetype_col is None:
        raise ValueError("Expected columns role_subgroup and archetype_id are required.")
    return subgroup_col, archetype_col


def z_columns(df: pd.DataFrame) -> List[str]:
    return [c for c in df.columns if c.endswith("_z")]


def top_z_features(row: pd.Series, n: int = 8) -> List[Tuple[str, float]]:
    cols = [c for c in row.index if c.endswith("_z")]
    values = []
    for c in cols:
        val = pd.to_numeric(pd.Series([row[c]]), errors="coerce").iloc[0]
        if pd.notna(val):
            values.append((c, float(val)))
    values.sort(key=lambda x: x[1], reverse=True)
    return values[:n]


def top_feature_string(row: pd.Series, n: int = 6) -> str:
    return "; ".join(f"{name}:{val:.2f}" for name, val in top_z_features(row, n=n))


# =============================================================================
# Label inference
# =============================================================================


def infer_def_cb_label(row: pd.Series, used_labels: set[str]) -> str:
    """Infer CB archetype label from centroid z-score signature."""
    # Aggregate families from whichever feature names are present.
    vals = {c: float(pd.to_numeric(pd.Series([row.get(c)]), errors="coerce").iloc[0])
            for c in row.index if c.endswith("_z") and pd.notna(row.get(c))}

    def score(patterns: Iterable[str]) -> float:
        total = 0.0
        count = 0
        for c, v in vals.items():
            lc = c.lower()
            if any(p in lc for p in patterns):
                total += v
                count += 1
        return total / count if count else -999.0

    progression = score(["progressive_pass", "prgp", "prog", "pass_completion", "total_cmp", "passes_final"])
    aerial = score(["aerial", "duel"])
    stopper = score(["block", "clear", "clr", "touches_def_pen", "blocks"])
    aggressive = score(["tackle", "interception", "recover", "tkl", "int_"])

    ranked = sorted(
        [
            ("Ball-Playing Centre-Back", progression),
            ("Aerial Defender", aerial),
            ("Defensive Stopper", stopper),
            ("Aggressive Defender", aggressive),
        ],
        key=lambda x: x[1],
        reverse=True,
    )

    for label, _ in ranked:
        if label not in used_labels:
            return label
    return ranked[0][0]


def infer_att_cf_label(row: pd.Series, used_labels: set[str]) -> str:
    """Infer CF archetype label from centroid z-score signature."""
    vals = {c: float(pd.to_numeric(pd.Series([row.get(c)]), errors="coerce").iloc[0])
            for c in row.index if c.endswith("_z") and pd.notna(row.get(c))}

    def score(patterns: Iterable[str]) -> float:
        total = 0.0
        count = 0
        for c, v in vals.items():
            lc = c.lower()
            if any(p in lc for p in patterns):
                total += v
                count += 1
        return total / count if count else -999.0

    box = score(["touches_box", "touches_att_pen", "xg", "npxg"])
    finishing = score(["finishing", "g_per_shot", "g_per_sot", "sot", "shots"])
    mobile = score(["progressive_carr", "carries", "takeons", "progressive_receipts"])
    creation = score(["sca", "gca", "key_pass", "xag", "assist"])
    volume = score(["shots_p90", "shot", "standard_sh"])

    combined = [
        ("Box Finisher", 0.55 * box + 0.45 * finishing),
        ("Mobile Forward", mobile),
        ("Creator Forward", creation),
        ("Volume Shooter", volume - 0.25 * finishing),
    ]
    ranked = sorted(combined, key=lambda x: x[1], reverse=True)

    for label, _ in ranked:
        if label not in used_labels:
            return label
    return ranked[0][0]


def build_label_mapping(centroids: pd.DataFrame) -> pd.DataFrame:
    subgroup_col, archetype_col = detect_id_cols(centroids)
    rows = []

    for subgroup, part in centroids.groupby(subgroup_col, dropna=False):
        used_labels: set[str] = set()
        part = part.sort_values(archetype_col).copy()

        for _, row in part.iterrows():
            archetype_id = int(row[archetype_col]) if pd.notna(row[archetype_col]) else -1

            if subgroup == "MID" and archetype_id in MID_VALIDATED_LABELS:
                label = MID_VALIDATED_LABELS[archetype_id]
            elif subgroup == "DEF_CB":
                label = infer_def_cb_label(row, used_labels)
            elif subgroup == "ATT_CF":
                label = infer_att_cf_label(row, used_labels)
            else:
                label = f"{subgroup}_{archetype_id}"

            used_labels.add(label)
            rows.append(
                {
                    "role_subgroup": subgroup,
                    "archetype_id": archetype_id,
                    "role_name": label,
                    "role_label": f"{ROLE_EMOJIS.get(label, '🧬')} {label}",
                    "role_description": ROLE_DESCRIPTIONS.get(label, ROLE_DESCRIPTIONS["Unlabeled Archetype"]),
                    "top_centroid_features": top_feature_string(row, n=8),
                    "label_status": "validated" if subgroup == "MID" else "inferred_v1",
                }
            )

    return pd.DataFrame(rows)


# =============================================================================
# Similarity, secondary role and confidence
# =============================================================================


def feature_columns_for_similarity(df: pd.DataFrame) -> List[str]:
    # Prefer standardized features from TM.6.3 if present.
    cols = [c for c in df.columns if c.endswith("_z")]
    if cols:
        return cols

    # Fallback: role/tactical numeric columns excluding identifiers and generated metadata.
    excluded = {
        "archetype_id", "cluster", "cluster_probability", "archetype_similarity",
        "role_confidence", "role_ambiguity", "season", "age", "minutes"
    }
    id_like = {"player", "team", "league", "role_subgroup", "primary_role", "secondary_role"}
    numeric = []
    for c in df.columns:
        if c in excluded or c in id_like:
            continue
        if pd.api.types.is_numeric_dtype(df[c]):
            numeric.append(c)
    return numeric


def centroid_matrix(archetypes: pd.DataFrame, feature_cols: List[str]) -> pd.DataFrame:
    return (
        archetypes
        .groupby(["role_subgroup", "archetype_id"], dropna=False)[feature_cols]
        .mean(numeric_only=True)
        .reset_index()
    )


def compute_role_distances(archetypes: pd.DataFrame, feature_cols: List[str]) -> pd.DataFrame:
    """Compute similarity to all centroids within the same subgroup.

    Similarity is 100 * exp(-distance / median_distance_subgroup), producing a stable
    bounded score that is easier to interpret than raw Euclidean distance.
    """
    out_rows = []
    cent = centroid_matrix(archetypes, feature_cols)

    # Stable row id for rejoining after long-form distance calculation.
    # If caller already provided _row_id, preserve it. Otherwise create it.
    # This avoids duplicate _row_id columns after reset_index(), which can make
    # part["_row_id"] return a DataFrame and break int(row_id).
    base = archetypes.copy().reset_index(drop=True)
    if "_row_id" not in base.columns:
        base["_row_id"] = np.arange(len(base), dtype=int)
    else:
        base["_row_id"] = pd.to_numeric(base["_row_id"], errors="coerce")
        if base["_row_id"].isna().any():
            base["_row_id"] = np.arange(len(base), dtype=int)
        base["_row_id"] = base["_row_id"].astype(int)

    for subgroup, part in base.groupby("role_subgroup", dropna=False):
        cent_part = cent[cent["role_subgroup"] == subgroup].copy()
        if cent_part.empty or part.empty:
            continue

        X = part[feature_cols].apply(pd.to_numeric, errors="coerce").fillna(0.0).to_numpy(dtype=float)
        C = cent_part[feature_cols].apply(pd.to_numeric, errors="coerce").fillna(0.0).to_numpy(dtype=float)

        # Pairwise Euclidean distances.
        # Shape: n_players x n_centroids
        distances = np.sqrt(((X[:, None, :] - C[None, :, :]) ** 2).sum(axis=2))
        positive_dist = distances[np.isfinite(distances)]
        scale = float(np.median(positive_dist)) if positive_dist.size else 1.0
        if not np.isfinite(scale) or scale <= 0:
            scale = 1.0
        sims = 100.0 * np.exp(-distances / scale)

        centroid_ids = cent_part["archetype_id"].to_numpy()
        for i, row_id in enumerate(part["_row_id"].to_numpy()):
            order = np.argsort(-sims[i])
            primary_idx = order[0]
            secondary_idx = order[1] if len(order) > 1 else order[0]
            primary_similarity = float(sims[i, primary_idx])
            secondary_similarity = float(sims[i, secondary_idx])

            out_rows.append(
                {
                    "_row_id": int(row_id),
                    "primary_archetype_id_calc": int(centroid_ids[primary_idx]),
                    "primary_role_similarity": round(primary_similarity, 1),
                    "secondary_archetype_id": int(centroid_ids[secondary_idx]),
                    "secondary_role_similarity": round(secondary_similarity, 1),
                    "role_confidence": round(max(0.0, primary_similarity - secondary_similarity), 1),
                    "role_ambiguity": round(max(0.0, 100.0 - (primary_similarity - secondary_similarity)), 1),
                }
            )

    return pd.DataFrame(out_rows)


def role_fit_bucket(score: float) -> str:
    if pd.isna(score):
        return "Unknown"
    if score >= 90:
        return "Elite Fit"
    if score >= 80:
        return "Strong Fit"
    if score >= 70:
        return "Good Fit"
    if score >= 60:
        return "Hybrid Fit"
    return "Ambiguous Fit"


def add_labels(archetypes: pd.DataFrame, mapping: pd.DataFrame) -> pd.DataFrame:
    df = archetypes.copy().reset_index(drop=True)
    if "archetype_id" not in df.columns or "role_subgroup" not in df.columns:
        raise ValueError("archetypes input must contain role_subgroup and archetype_id")

    feature_cols = feature_columns_for_similarity(df)
    if not feature_cols:
        raise ValueError("No numeric feature columns found for similarity calculation.")

    df = df.reset_index(drop=False).rename(columns={"index": "_row_id"})
    dist = compute_role_distances(df.drop(columns=[]), feature_cols)
    df = df.merge(dist, on="_row_id", how="left")

    # Primary label from discovered archetype assignment, not recalculated nearest centroid.
    primary_map = mapping.rename(
        columns={
            "archetype_id": "archetype_id",
            "role_name": "primary_role",
            "role_label": "primary_role_label",
            "role_description": "primary_role_description",
            "label_status": "primary_label_status",
        }
    )[
        [
            "role_subgroup", "archetype_id", "primary_role", "primary_role_label",
            "primary_role_description", "primary_label_status",
        ]
    ]
    df = df.merge(primary_map, on=["role_subgroup", "archetype_id"], how="left")

    # Secondary role from second-nearest centroid.
    secondary_map = mapping.rename(
        columns={
            "archetype_id": "secondary_archetype_id",
            "role_name": "secondary_role",
            "role_label": "secondary_role_label",
            "role_description": "secondary_role_description",
        }
    )[
        [
            "role_subgroup", "secondary_archetype_id", "secondary_role",
            "secondary_role_label", "secondary_role_description",
        ]
    ]
    df = df.merge(secondary_map, on=["role_subgroup", "secondary_archetype_id"], how="left")

    # If the primary cluster from HDBSCAN/KMeans differs from nearest centroid due to numerical edge cases,
    # keep original archetype_id but record diagnostic.
    df["primary_archetype_match"] = df["archetype_id"].eq(df["primary_archetype_id_calc"])

    df["role_fit_bucket"] = df["primary_role_similarity"].apply(role_fit_bucket)
    df["role_profile_type"] = np.select(
        [
            df["role_confidence"].ge(25),
            df["role_confidence"].between(12, 24.999, inclusive="both"),
            df["role_confidence"].lt(12),
        ],
        ["Specialist", "Balanced", "Hybrid"],
        default="Unknown",
    )

    for col in ["primary_role", "primary_role_label", "primary_role_description", "secondary_role", "secondary_role_label"]:
        if col in df.columns:
            df[col] = df[col].fillna("Unlabeled Archetype")

    # Clean technical helper columns later, but keep diagnostics useful for audit.
    return df


# =============================================================================
# Reports
# =============================================================================


def parse_similar_player_string(value: object) -> Tuple[str, str, str, Optional[float]]:
    """Parse strings like 'Player | Team | Season | 86.1' if present."""
    if pd.isna(value):
        return "", "", "", None
    parts = [p.strip() for p in str(value).split("|")]
    if len(parts) >= 4:
        score = pd.to_numeric(pd.Series([parts[3]]), errors="coerce").iloc[0]
        return parts[0], parts[1], parts[2], float(score) if pd.notna(score) else None
    if len(parts) >= 1:
        return parts[0], "", "", None
    return "", "", "", None


def build_distribution(labels: pd.DataFrame) -> pd.DataFrame:
    return (
        labels
        .groupby(["role_subgroup", "archetype_id", "primary_role", "role_fit_bucket"], dropna=False)
        .size()
        .reset_index(name="n")
        .sort_values(["role_subgroup", "primary_role", "role_fit_bucket"])
    )


def build_representatives(labels: pd.DataFrame, max_per_role: int = 20) -> pd.DataFrame:
    sort_col = "primary_role_similarity" if "primary_role_similarity" in labels.columns else None
    rows = []
    group_cols = ["role_subgroup", "archetype_id", "primary_role"]

    for keys, part in labels.groupby(group_cols, dropna=False):
        role_subgroup, archetype_id, role_name = keys
        part = part.copy()
        if sort_col:
            part = part.sort_values(sort_col, ascending=False)
        else:
            part = part.head(max_per_role)

        for rank, (_, row) in enumerate(part.head(max_per_role).iterrows(), start=1):
            rows.append(
                {
                    "role_subgroup": role_subgroup,
                    "archetype_id": archetype_id,
                    "role_name": role_name,
                    "rank": rank,
                    "player": row.get("player", ""),
                    "team": row.get("team", ""),
                    "league": row.get("league", ""),
                    "season": row.get("season", ""),
                    "minutes": row.get("minutes", row.get("Playing Time_Min", np.nan)),
                    "primary_role_similarity": row.get("primary_role_similarity", np.nan),
                    "role_confidence": row.get("role_confidence", np.nan),
                    "secondary_role": row.get("secondary_role", ""),
                }
            )
    return pd.DataFrame(rows)


def ordered_output_columns(df: pd.DataFrame) -> List[str]:
    preferred = [
        "player", "season", "team", "league", "role_subgroup",
        "archetype_id", "primary_role", "primary_role_label", "primary_role_description",
        "primary_role_similarity", "role_confidence", "role_ambiguity", "role_profile_type",
        "secondary_archetype_id", "secondary_role", "secondary_role_label", "secondary_role_similarity",
        "role_fit_bucket", "primary_label_status", "primary_archetype_match",
        "minutes", "age", "pos_",
    ]
    cols = [c for c in preferred if c in df.columns]
    remaining = [c for c in df.columns if c not in cols and c != "_row_id"]
    return cols + remaining


def write_outputs(labels: pd.DataFrame, mapping: pd.DataFrame) -> None:
    ensure_dirs()

    labels = labels.copy()
    labels = labels[ordered_output_columns(labels)]

    labels.to_parquet(OUTPUT_LABELS_PARQUET, index=False)
    labels.to_csv(OUTPUT_LABELS_CSV, index=False)

    distribution = build_distribution(labels)
    distribution.to_csv(OUTPUT_DISTRIBUTION, index=False)

    representatives = build_representatives(labels, max_per_role=20)
    representatives.to_csv(OUTPUT_REPRESENTATIVES, index=False)

    mapping.to_csv(OUTPUT_MAPPING, index=False)

    audit = {
        "input_archetypes": str(INPUT_ARCHETYPES.relative_to(ROOT)) if INPUT_ARCHETYPES.exists() else str(INPUT_ARCHETYPES),
        "input_centroids": str(INPUT_CENTROIDS.relative_to(ROOT)) if INPUT_CENTROIDS.exists() else str(INPUT_CENTROIDS),
        "output_labels": str(OUTPUT_LABELS_PARQUET.relative_to(ROOT)),
        "n_rows": int(len(labels)),
        "n_roles": int(labels["primary_role"].nunique(dropna=True)),
        "role_subgroups": labels["role_subgroup"].value_counts(dropna=False).to_dict(),
        "role_distribution": labels["primary_role"].value_counts(dropna=False).to_dict(),
        "primary_archetype_match_rate": float(labels["primary_archetype_match"].mean()) if "primary_archetype_match" in labels else None,
    }
    OUTPUT_AUDIT.write_text(json.dumps(audit, indent=2, ensure_ascii=False), encoding="utf-8")


# =============================================================================
# CLI
# =============================================================================


def main() -> None:
    parser = argparse.ArgumentParser(description="TM.6.4 Role Labeling Engine")
    parser.add_argument("--print-samples", action="store_true", help="Print sample distribution and representatives")
    args = parser.parse_args()

    ensure_dirs()
    archetypes, centroids, _ = read_inputs()

    print("=" * 88)
    print("TM.6.4 — Role Labeling Engine")
    print("=" * 88)
    print(f"ROOT: {ROOT}")
    print(f"Input archetypes: {INPUT_ARCHETYPES}")
    print(f"Input centroids:  {INPUT_CENTROIDS}")
    print(f"Rows: {len(archetypes):,}")
    print("Subgroups:")
    print(archetypes["role_subgroup"].value_counts(dropna=False).to_string())

    mapping = build_label_mapping(centroids)
    labels = add_labels(archetypes, mapping)
    write_outputs(labels, mapping)

    print("\nRole mapping:")
    print(mapping[["role_subgroup", "archetype_id", "role_name", "label_status"]].to_string(index=False))

    print("\nRole distribution:")
    print(labels["primary_role"].value_counts(dropna=False).to_string())

    print("\nOutputs:")
    for path in [OUTPUT_LABELS_PARQUET, OUTPUT_LABELS_CSV, OUTPUT_DISTRIBUTION, OUTPUT_REPRESENTATIVES, OUTPUT_MAPPING, OUTPUT_AUDIT]:
        print(f"- {path.relative_to(ROOT)}")

    if args.print_samples:
        reps = build_representatives(labels, max_per_role=5)
        print("\nRepresentative sample:")
        print(reps.head(50).to_string(index=False))


if __name__ == "__main__":
    main()
