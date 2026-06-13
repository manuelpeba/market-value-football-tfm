#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
TM.6.3 — Archetype Discovery Engine

Builds empirical football role archetypes from advanced FBref role features.

Input:
    data/processed/player_role_features_advanced.parquet

Outputs:
    data/processed/player_role_archetypes.parquet
    reports/roles/archetype_representatives.csv
    reports/roles/archetype_feature_centroids.csv
    reports/roles/archetype_cluster_summary.csv
    reports/roles/archetype_cluster_selection.csv

Preferred model:
    StandardScaler -> UMAP -> HDBSCAN

Fallback if umap-learn/hdbscan are not installed:
    StandardScaler -> PCA -> KMeans grid search

The script intentionally does NOT assign final tactical labels yet. It produces
cluster ids, representatives and centroids so labels can be validated manually
in TM.6.4.
"""

from __future__ import annotations

import argparse
import math
import warnings
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Iterable, List, Optional, Tuple

import numpy as np
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
from sklearn.impute import SimpleImputer
from sklearn.metrics import calinski_harabasz_score, silhouette_score
from sklearn.metrics import pairwise_distances
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

warnings.filterwarnings("ignore", category=FutureWarning)
warnings.filterwarnings("ignore", category=UserWarning)

RANDOM_STATE = 42

IDENTITY_COLS = [
    "player",
    "season",
    "team",
    "league",
    "pos_",
    "age_",
    "minutes",
    "role_subgroup",
]

# Feature families. The builder is intentionally robust: only columns present in
# the input parquet are used. If a preferred feature is missing, it is skipped.
FEATURES_BY_SUBGROUP: Dict[str, List[str]] = {
    "DEF_CB": [
        "progressive_passes_p90",
        "pass_completion_pct",
        "long_pass_completion_pct",
        "passes_final_third_p90",
        "blocks_p90",
        "clearances_p90",
        "interceptions_p90",
        "tackles_p90",
        "tackles_won_p90",
        "aerials_won_p90",
        "aerials_won_pct",
        "duel_index_role",
        "defending_index_role",
        "errors_p90",
        "recoveries_p90",
    ],
    "MID": [
        "progressive_passes_p90",
        "progressive_carries_p90",
        "progressive_receipts_p90",
        "key_passes_p90",
        "sca_p90",
        "gca_p90",
        "gca_live_p90",
        "passes_final_third_p90",
        "passes_penalty_area_p90",
        "touches_mid_third_p90",
        "touches_att_third_p90",
        "touches_box_p90",
        "takeons_attempted_p90",
        "takeons_success_pct",
        "tackles_p90",
        "interceptions_p90",
        "recoveries_p90",
        "creation_index_role",
        "progression_index_role",
        "defending_index_role",
        "availability_index",
    ],
    "ATT_CF": [
        "xg_p90",
        "npxg_p90",
        "shots_p90",
        "sot_p90",
        "g_per_shot",
        "g_per_sot",
        "shot_distance",
        "touches_box_p90",
        "progressive_receipts_p90",
        "progressive_carries_p90",
        "carries_box_p90",
        "takeons_attempted_p90",
        "takeons_success_pct",
        "key_passes_p90",
        "sca_p90",
        "gca_p90",
        "gca_live_p90",
        "finishing_index_role",
        "creation_index_role",
        "progression_index_role",
    ],
    "ATT_WIDE": [
        "progressive_carries_p90",
        "carries_box_p90",
        "crosses_penalty_area_p90",
        "takeons_attempted_p90",
        "takeons_success_pct",
        "touches_att_third_p90",
        "touches_box_p90",
        "progressive_receipts_p90",
        "key_passes_p90",
        "sca_p90",
        "gca_p90",
        "xg_p90",
        "shots_p90",
        "sot_p90",
        "creation_index_role",
        "progression_index_role",
        "finishing_index_role",
    ],
    "GK": [
        # Kept deliberately conservative. Use only if --include-gk is passed.
        "pass_completion_pct",
        "long_pass_completion_pct",
        "progressive_passes_p90",
        "errors_p90",
        "availability_index",
        "minutes",
    ],
}

DEFAULT_SUBGROUPS = ["DEF_CB", "MID", "ATT_CF"]


@dataclass
class ModelResult:
    method: str
    labels: np.ndarray
    probabilities: np.ndarray
    embedding: np.ndarray
    model: object
    metrics: Dict[str, float]
    n_clusters: int
    n_noise: int


def log(msg: str) -> None:
    print(f"[TM.6.3] {msg}")


def project_root_from_script() -> Path:
    cwd = Path.cwd()
    if (cwd / "data").exists():
        return cwd
    # Allows running from src/scouting/roles
    for parent in Path(__file__).resolve().parents:
        if (parent / "data").exists():
            return parent
    return cwd


def coerce_numeric(df: pd.DataFrame, cols: Iterable[str]) -> pd.DataFrame:
    out = df.copy()
    for c in cols:
        if c in out.columns:
            out[c] = pd.to_numeric(out[c], errors="coerce")
    return out


def existing_features(df: pd.DataFrame, subgroup: str) -> List[str]:
    features = [c for c in FEATURES_BY_SUBGROUP.get(subgroup, []) if c in df.columns]
    # Drop constant or near-empty features.
    valid = []
    for c in features:
        s = pd.to_numeric(df[c], errors="coerce")
        if s.notna().sum() < max(50, int(len(df) * 0.20)):
            continue
        if s.nunique(dropna=True) <= 1:
            continue
        valid.append(c)
    return valid


def make_matrix(df: pd.DataFrame, features: List[str]) -> Tuple[np.ndarray, Pipeline]:
    pipe = Pipeline(
        steps=[
            ("imputer", SimpleImputer(strategy="median")),
            ("scaler", StandardScaler()),
        ]
    )
    X = pipe.fit_transform(df[features])
    return X, pipe


def try_umap_hdbscan(
    X: np.ndarray,
    n_neighbors: int,
    min_dist: float,
    min_cluster_size: int,
    min_samples: int,
) -> Optional[ModelResult]:
    try:
        import umap  # type: ignore
        import hdbscan  # type: ignore
    except Exception:
        return None

    n_components = min(10, max(2, X.shape[1]))
    reducer = umap.UMAP(
        n_components=n_components,
        n_neighbors=min(n_neighbors, max(2, X.shape[0] - 1)),
        min_dist=min_dist,
        metric="euclidean",
        random_state=RANDOM_STATE,
    )
    embedding = reducer.fit_transform(X)

    clusterer = hdbscan.HDBSCAN(
        min_cluster_size=min_cluster_size,
        min_samples=min_samples,
        metric="euclidean",
        prediction_data=True,
    )
    labels = clusterer.fit_predict(embedding)
    probabilities = getattr(clusterer, "probabilities_", np.ones(len(labels)))

    valid = labels >= 0
    n_clusters = len(set(labels[valid]))
    n_noise = int((labels == -1).sum())

    metrics: Dict[str, float] = {
        "noise_rate": float(n_noise / len(labels)) if len(labels) else np.nan,
    }
    if n_clusters >= 2 and valid.sum() > n_clusters:
        metrics["silhouette"] = float(silhouette_score(embedding[valid], labels[valid]))
        metrics["calinski_harabasz"] = float(calinski_harabasz_score(embedding[valid], labels[valid]))
    else:
        metrics["silhouette"] = np.nan
        metrics["calinski_harabasz"] = np.nan

    return ModelResult(
        method="UMAP+HDBSCAN",
        labels=labels,
        probabilities=probabilities,
        embedding=embedding,
        model={"umap": reducer, "hdbscan": clusterer},
        metrics=metrics,
        n_clusters=n_clusters,
        n_noise=n_noise,
    )


def kmeans_fallback(X: np.ndarray, k_min: int, k_max: int) -> Tuple[ModelResult, pd.DataFrame]:
    n = X.shape[0]
    n_components = min(10, max(2, X.shape[1]), max(2, n - 1))
    pca = PCA(n_components=n_components, random_state=RANDOM_STATE)
    embedding = pca.fit_transform(X)

    rows = []
    best_model = None
    best_score = -np.inf
    best_labels = None

    upper = min(k_max, max(k_min, n // 50))
    upper = max(k_min, upper)

    for k in range(k_min, upper + 1):
        if k >= n:
            continue
        model = KMeans(n_clusters=k, random_state=RANDOM_STATE, n_init=30)
        labels = model.fit_predict(embedding)
        sil = silhouette_score(embedding, labels) if len(set(labels)) > 1 else np.nan
        ch = calinski_harabasz_score(embedding, labels) if len(set(labels)) > 1 else np.nan
        rows.append(
            {
                "k": k,
                "silhouette": sil,
                "calinski_harabasz": ch,
                "inertia": model.inertia_,
            }
        )
        score = sil if not pd.isna(sil) else -np.inf
        if score > best_score:
            best_score = score
            best_model = model
            best_labels = labels

    if best_model is None or best_labels is None:
        raise RuntimeError("KMeans fallback failed: no valid cluster model.")

    # Confidence from distance separation: bigger gap between first and second
    # nearest centroid implies more cluster certainty.
    dists = pairwise_distances(embedding, best_model.cluster_centers_)
    sorted_dists = np.sort(dists, axis=1)
    nearest = sorted_dists[:, 0]
    second = sorted_dists[:, 1] if sorted_dists.shape[1] > 1 else sorted_dists[:, 0]
    sep = (second - nearest) / (second + 1e-9)
    probabilities = np.clip(sep, 0, 1)

    metrics = {
        "silhouette": float(best_score),
        "calinski_harabasz": float(calinski_harabasz_score(embedding, best_labels)),
        "noise_rate": 0.0,
        "pca_explained_variance": float(np.sum(pca.explained_variance_ratio_)),
    }

    result = ModelResult(
        method="PCA+KMeans",
        labels=best_labels,
        probabilities=probabilities,
        embedding=embedding,
        model={"pca": pca, "kmeans": best_model},
        metrics=metrics,
        n_clusters=len(set(best_labels)),
        n_noise=0,
    )
    return result, pd.DataFrame(rows)


def choose_params(n: int, subgroup: str) -> Dict[str, int | float]:
    # Conservative defaults by subgroup size. These are starting points; reports
    # let us validate whether clusters are tactically useful.
    min_cluster_size = {
        "DEF_CB": 150,
        "MID": 120,
        "ATT_CF": 100,
        "ATT_WIDE": 80,
        "GK": 60,
    }.get(subgroup, 100)
    min_cluster_size = min(min_cluster_size, max(30, n // 8))
    min_samples = max(10, min(40, min_cluster_size // 3))
    n_neighbors = max(15, min(40, n // 40))
    return {
        "n_neighbors": int(n_neighbors),
        "min_dist": 0.10,
        "min_cluster_size": int(min_cluster_size),
        "min_samples": int(min_samples),
    }


def build_representatives(
    sub: pd.DataFrame,
    features: List[str],
    labels: np.ndarray,
    embedding: np.ndarray,
    max_per_cluster: int,
) -> pd.DataFrame:
    rows = []
    sub = sub.reset_index(drop=True).copy()
    for label in sorted([x for x in set(labels) if x >= 0]):
        idx = np.where(labels == label)[0]
        if len(idx) == 0:
            continue
        center = embedding[idx].mean(axis=0, keepdims=True)
        dist = pairwise_distances(embedding[idx], center).ravel()
        order = np.argsort(dist)[:max_per_cluster]
        max_dist = dist.max() if dist.max() > 0 else 1.0
        for rank, local_pos in enumerate(order, start=1):
            i = idx[local_pos]
            rec = sub.iloc[i]
            sim = 100.0 * (1.0 - (dist[local_pos] / max_dist))
            row = {
                "role_subgroup": rec.get("role_subgroup"),
                "archetype_id": int(label),
                "rank": rank,
                "player": rec.get("player"),
                "team": rec.get("team"),
                "league": rec.get("league"),
                "season": rec.get("season"),
                "pos_": rec.get("pos_"),
                "age_": rec.get("age_"),
                "minutes": rec.get("minutes"),
                "archetype_similarity": round(float(np.clip(sim, 0, 100)), 1),
            }
            for f in features:
                row[f] = rec.get(f)
            rows.append(row)
    return pd.DataFrame(rows)


def build_centroids(
    sub: pd.DataFrame,
    features: List[str],
    labels: np.ndarray,
) -> pd.DataFrame:
    rows = []
    work = sub.reset_index(drop=True).copy()
    work["archetype_id"] = labels
    for label in sorted([x for x in set(labels) if x >= 0]):
        cluster = work[work["archetype_id"] == label]
        if cluster.empty:
            continue
        row = {
            "role_subgroup": cluster["role_subgroup"].iloc[0],
            "archetype_id": int(label),
            "n_players": int(len(cluster)),
        }
        for f in features:
            row[f"{f}_mean"] = float(pd.to_numeric(cluster[f], errors="coerce").mean())
            row[f"{f}_median"] = float(pd.to_numeric(cluster[f], errors="coerce").median())
        # Relative z centroid across subgroup for interpretability.
        for f in features:
            s = pd.to_numeric(work[f], errors="coerce")
            mu = s.mean()
            sd = s.std(ddof=0)
            val = pd.to_numeric(cluster[f], errors="coerce").mean()
            row[f"{f}_z"] = float((val - mu) / sd) if sd and not pd.isna(sd) else 0.0
        rows.append(row)
    return pd.DataFrame(rows)


def enrich_output(
    sub: pd.DataFrame,
    features: List[str],
    result: ModelResult,
) -> pd.DataFrame:
    out = sub.copy().reset_index(drop=True)
    out["archetype_id"] = result.labels
    out["archetype_method"] = result.method
    out["archetype_probability"] = np.round(result.probabilities * 100, 1)

    # Similarity to own cluster centroid in embedding space.
    sim = np.full(len(out), np.nan)
    for label in sorted([x for x in set(result.labels) if x >= 0]):
        idx = np.where(result.labels == label)[0]
        center = result.embedding[idx].mean(axis=0, keepdims=True)
        dist = pairwise_distances(result.embedding[idx], center).ravel()
        max_dist = dist.max() if dist.max() > 0 else 1.0
        sim[idx] = 100.0 * (1.0 - dist / max_dist)
    out["archetype_similarity"] = np.round(np.clip(sim, 0, 100), 1)

    # Keep interpretable feature columns in the output as well.
    keep = [c for c in IDENTITY_COLS if c in out.columns]
    keep += ["archetype_id", "archetype_method", "archetype_probability", "archetype_similarity"]
    keep += [c for c in features if c in out.columns and c not in keep]
    return out[keep]


def main() -> None:
    parser = argparse.ArgumentParser(description="TM.6.3 Archetype Discovery Engine")
    parser.add_argument(
        "--input",
        default="data/processed/player_role_features_advanced.parquet",
        help="Input advanced role feature parquet.",
    )
    parser.add_argument(
        "--output",
        default="data/processed/player_role_archetypes.parquet",
        help="Output archetypes parquet.",
    )
    parser.add_argument(
        "--reports-dir",
        default="reports/roles",
        help="Reports directory.",
    )
    parser.add_argument(
        "--include-gk",
        action="store_true",
        help="Include GK clustering. Disabled by default unless GK-specific features are validated.",
    )
    parser.add_argument("--min-rows", type=int, default=120, help="Minimum subgroup rows.")
    parser.add_argument("--k-min", type=int, default=3, help="KMeans fallback min k.")
    parser.add_argument("--k-max", type=int, default=8, help="KMeans fallback max k.")
    parser.add_argument("--representatives", type=int, default=20, help="Representatives per cluster.")
    args = parser.parse_args()

    root = project_root_from_script()
    input_path = root / args.input
    output_path = root / args.output
    reports_dir = root / args.reports_dir
    reports_dir.mkdir(parents=True, exist_ok=True)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    log(f"Project root: {root}")
    log(f"Input: {input_path}")

    if not input_path.exists():
        raise FileNotFoundError(f"Input file not found: {input_path}")

    df = pd.read_parquet(input_path)
    log(f"Input shape: {df.shape[0]:,} rows x {df.shape[1]:,} cols")

    if "role_subgroup" not in df.columns:
        raise KeyError("Input must contain role_subgroup.")

    subgroups = DEFAULT_SUBGROUPS.copy()
    if args.include_gk:
        subgroups.append("GK")
    if "ATT_WIDE" in df["role_subgroup"].unique():
        subgroups.append("ATT_WIDE")

    all_outputs = []
    all_reps = []
    all_centroids = []
    all_summary = []
    all_selection = []

    for subgroup in subgroups:
        sub = df[df["role_subgroup"].eq(subgroup)].copy()
        log(f"{subgroup}: raw rows={len(sub):,}")
        if len(sub) < args.min_rows:
            log(f"Skipping {subgroup}: only {len(sub):,} rows < {args.min_rows}")
            continue

        features = existing_features(sub, subgroup)
        log(f"{subgroup}: features={len(features)} -> {features}")
        min_features = 5 if subgroup != "GK" else 3
        if len(features) < min_features:
            log(f"Skipping {subgroup}: insufficient real features ({len(features)} < {min_features})")
            continue

        sub = coerce_numeric(sub, features)
        X, _ = make_matrix(sub, features)

        params = choose_params(len(sub), subgroup)
        result = try_umap_hdbscan(
            X,
            n_neighbors=int(params["n_neighbors"]),
            min_dist=float(params["min_dist"]),
            min_cluster_size=int(params["min_cluster_size"]),
            min_samples=int(params["min_samples"]),
        )
        selection_df = pd.DataFrame()
        if result is None or result.n_clusters < 2:
            if result is None:
                log(f"{subgroup}: UMAP/HDBSCAN not available. Falling back to PCA+KMeans.")
            else:
                log(f"{subgroup}: HDBSCAN found <2 clusters. Falling back to PCA+KMeans.")
            result, selection_df = kmeans_fallback(X, args.k_min, args.k_max)
            if not selection_df.empty:
                selection_df.insert(0, "role_subgroup", subgroup)
                all_selection.append(selection_df)
        else:
            log(
                f"{subgroup}: {result.method}, clusters={result.n_clusters}, "
                f"noise={result.n_noise}, silhouette={result.metrics.get('silhouette', np.nan):.3f}"
            )

        out = enrich_output(sub, features, result)
        reps = build_representatives(sub, features, result.labels, result.embedding, args.representatives)
        cents = build_centroids(sub, features, result.labels)

        all_outputs.append(out)
        all_reps.append(reps)
        all_centroids.append(cents)
        all_summary.append(
            {
                "role_subgroup": subgroup,
                "rows": int(len(sub)),
                "features": int(len(features)),
                "feature_list": ", ".join(features),
                "method": result.method,
                "n_clusters": int(result.n_clusters),
                "n_noise": int(result.n_noise),
                "noise_rate": result.metrics.get("noise_rate", np.nan),
                "silhouette": result.metrics.get("silhouette", np.nan),
                "calinski_harabasz": result.metrics.get("calinski_harabasz", np.nan),
                "params": str(params),
            }
        )

    if not all_outputs:
        raise RuntimeError("No archetype outputs generated. Check input features and subgroup definitions.")

    archetypes = pd.concat(all_outputs, ignore_index=True)
    reps_df = pd.concat(all_reps, ignore_index=True) if all_reps else pd.DataFrame()
    cents_df = pd.concat(all_centroids, ignore_index=True) if all_centroids else pd.DataFrame()
    summary_df = pd.DataFrame(all_summary)
    selection_df = pd.concat(all_selection, ignore_index=True) if all_selection else pd.DataFrame()

    archetypes.to_parquet(output_path, index=False)
    reps_path = reports_dir / "archetype_representatives.csv"
    cents_path = reports_dir / "archetype_feature_centroids.csv"
    summary_path = reports_dir / "archetype_cluster_summary.csv"
    selection_path = reports_dir / "archetype_cluster_selection.csv"

    reps_df.to_csv(reps_path, index=False)
    cents_df.to_csv(cents_path, index=False)
    summary_df.to_csv(summary_path, index=False)
    selection_df.to_csv(selection_path, index=False)

    log(f"Output written: {output_path}")
    log(f"Representatives: {reps_path}")
    log(f"Centroids: {cents_path}")
    log(f"Summary: {summary_path}")
    log(f"Cluster selection: {selection_path}")
    log("Cluster summary:")
    print(summary_df.to_string(index=False))


if __name__ == "__main__":
    main()
