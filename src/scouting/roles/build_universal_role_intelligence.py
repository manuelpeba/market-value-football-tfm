"""
TM.6 — Universal Role Intelligence v5
Position-aware role discovery with subgroups:
  - DEF_CB and DEF_FB are modelled separately.
  - ATT_CF and ATT_WIDE are modelled separately.
  - MID remains one tactical universe.
  - GK is modelled only when enough goalkeeper-specific features exist.

Key methodological changes vs v4:
  - no global DEF/ATT clustering that mixes fullbacks, centre-backs, wingers and strikers;
  - role labels are derived from cluster centroids after clustering, not imposed through fixed archetype vectors;
  - representative reports use a high-minutes threshold to avoid low-sample archetypes;
  - output includes role_subgroup and position_detail for auditability.

Outputs:
  data/processed/player_role_universal.parquet
  reports/roles/universal_role_distribution.csv
  reports/roles/universal_role_representatives.csv
  reports/roles/universal_role_model_report.csv
  reports/roles/universal_role_centroids.csv

Run:
  python src/scouting/roles/build_universal_role_intelligence.py
"""

from __future__ import annotations

import argparse
import math
import re
import unicodedata
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Optional, Sequence, Tuple

import numpy as np
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.impute import SimpleImputer
from sklearn.metrics import silhouette_score
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.preprocessing import RobustScaler


ROLE_COLUMNS = [
    "primary_role",
    "secondary_role",
    "primary_role_similarity",
    "secondary_role_similarity",
    "role_confidence",
    "role_ambiguity",
    "primary_role_cluster",
    "secondary_role_cluster",
    "role_similar_player_1",
    "role_similar_player_2",
    "role_similar_player_3",
    "role_similar_player_4",
    "role_similar_player_5",
]

ID_CANDIDATES = {
    "player": [
        "player", "player_name", "player_name_display", "player_display_name",
        "player_fbref", "player_name_fbref", "player_tm", "fbref_player", "tm_player",
        "name", "short_name", "long_name", "Player", "Name", "player_",
    ],
    "team": ["team", "club", "squad", "Team", "Club"],
    "league": ["league", "competition", "League", "Comp"],
    "season": ["season", "Season"],
    "position_group": ["position_group", "pos_group", "pos_", "Pos", "pos", "position", "Position"],
    "position_detail": ["position", "Position", "pos_", "Pos", "pos", "position_group"],
    "age": ["age", "age_", "Age"],
    "minutes": ["minutes_played", "Playing Time_Min", "minutes", "Min", "Playing Time_Minutes"],
}

FEATURE_ALIASES: Dict[str, List[str]] = {
    # Common
    "minutes": ["minutes_played", "Playing Time_Min", "minutes", "Min"],
    "availability": ["availability_index", "Availability Index"],
    "defensive_activity": ["defensive_activity_index", "Defensive Activity"],
    "finishing": ["finishing_index_v2", "finishing_index", "Finishing Index"],
    "growth": ["growth_score", "growth_index", "Growth Score"],
    "confidence": ["confidence_score", "Confidence Score"],
    # Attacking
    "goals_p90": ["goals_per90", "Goals_Per90", "Performance_Gls_per90", "Gls_per90"],
    "assists_p90": ["assists_per90", "Assists_Per90", "Performance_Ast_per90", "Ast_per90"],
    "ga_p90": ["g_a_per90", "G+A_per90", "Performance_G+A_per90"],
    "shots_p90": ["shots_per90", "Standard_Sh_per90", "Shooting_Sh_per90", "Sh_per90"],
    "sot_p90": ["shots_on_target_per90", "Shooting_SoT_per90", "SoT_per90"],
    "xg_p90": ["xg_per90", "Expected_xG_per90", "xG_per90"],
    "xa_p90": ["xa_per90", "Expected_xAG_per90", "xA_per90", "xAG_per90"],
    "sca_p90": ["sca_per90", "SCA_SCA90", "SCA90"],
    "gca_p90": ["gca_per90", "GCA_GCA90", "GCA90"],
    # Passing / progression
    "progressive_passes_p90": ["progressive_passes_per90", "Passing_PrgP_per90", "PrgP_per90"],
    "progressive_carries_p90": ["progressive_carries_per90", "Possession_PrgC_per90", "PrgC_per90"],
    "progressive_receptions_p90": ["progressive_passes_received_per90", "Possession_PrgR_per90", "PrgR_per90"],
    "pass_completion": ["passes_completed_pct", "Passing_Cmp%", "pass_completion_pct", "Cmp%"],
    "key_passes_p90": ["key_passes_per90", "Passing_KP_per90", "KP_per90"],
    # Defense
    "tackles_p90": ["tackles_per90", "Tackles_Tkl_per90", "Tkl_per90"],
    "interceptions_p90": ["interceptions_per90", "Int_per90"],
    "blocks_p90": ["blocks_per90", "Blocks_Blocks_per90", "Blocks_per90"],
    "clearances_p90": ["clearances_per90", "Clr_per90"],
    "aerial_win_pct": ["aerial_duels_won_pct", "Aerial Duels_Won%", "Won%"],
    # GK
    "save_pct": ["save_pct", "Performance_Save%", "Save%"],
    "clean_sheets": ["clean_sheets", "Performance_CS", "CS"],
    "psxg_ga": ["psxg_ga", "Expected_PSxG+/-", "PSxG+/-"],
    "cross_stop_pct": ["cross_stop_pct", "Crosses_Stp%", "Stp%"],
    "sweeper_actions_p90": ["sweeper_actions_per90", "Sweeper_#OPA/90", "#OPA/90"],
    "launch_completion_pct": ["launch_completion_pct", "Launched_Cmp%"],
}

SUBGROUP_FEATURES = {
    "DEF_CB": [
        "minutes", "defensive_activity", "tackles_p90", "interceptions_p90", "blocks_p90",
        "clearances_p90", "aerial_win_pct", "progressive_passes_p90", "progressive_carries_p90",
        "pass_completion", "availability", "growth", "confidence",
    ],
    "DEF_FB": [
        "minutes", "defensive_activity", "tackles_p90", "interceptions_p90", "blocks_p90",
        "progressive_passes_p90", "progressive_carries_p90", "assists_p90", "sca_p90",
        "pass_completion", "availability", "growth", "confidence",
    ],
    "MID": [
        "minutes", "defensive_activity", "tackles_p90", "interceptions_p90", "progressive_passes_p90",
        "progressive_carries_p90", "progressive_receptions_p90", "key_passes_p90", "assists_p90",
        "sca_p90", "gca_p90", "pass_completion", "availability", "growth", "confidence",
    ],
    "ATT_CF": [
        "minutes", "goals_p90", "assists_p90", "ga_p90", "shots_p90", "sot_p90", "xg_p90",
        "aerial_win_pct", "finishing", "availability", "growth", "confidence",
    ],
    "ATT_WIDE": [
        "minutes", "goals_p90", "assists_p90", "ga_p90", "shots_p90", "sot_p90", "xa_p90",
        "sca_p90", "gca_p90", "progressive_carries_p90", "progressive_receptions_p90",
        "finishing", "availability", "growth", "confidence",
    ],
    "GK": [
        "minutes", "save_pct", "clean_sheets", "psxg_ga", "cross_stop_pct", "sweeper_actions_p90",
        "launch_completion_pct", "availability", "growth", "confidence",
    ],
}

DEFAULT_K = {"DEF_CB": 4, "DEF_FB": 3, "MID": 4, "ATT_CF": 4, "ATT_WIDE": 4, "GK": 3}
MIN_SUBGROUP_SIZE = {"DEF_CB": 80, "DEF_FB": 60, "MID": 100, "ATT_CF": 60, "ATT_WIDE": 60, "GK": 35}
MIN_REAL_FEATURES = {"DEF_CB": 3, "DEF_FB": 3, "MID": 4, "ATT_CF": 3, "ATT_WIDE": 3, "GK": 3}


@dataclass
class GroupResult:
    role_subgroup: str
    position_group: str
    n_players: int
    n_features: int
    k: int
    silhouette: float | None
    feature_names: List[str]


def normalize_key(value: object) -> str:
    if pd.isna(value):
        return ""
    text = str(value).strip().lower()
    text = unicodedata.normalize("NFKD", text)
    text = "".join(ch for ch in text if not unicodedata.combining(ch))
    text = re.sub(r"[^a-z0-9]+", " ", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text


def find_project_root(start: Path) -> Path:
    candidates = [start.resolve(), *start.resolve().parents]
    for c in candidates:
        if (c / "data").exists() or (c / "reports").exists() or (c / "src").exists():
            return c
    return start.resolve()


def resolve_first_existing(root: Path, candidates: Sequence[str]) -> Path:
    for rel in candidates:
        p = root / rel
        if p.exists():
            return p
    raise FileNotFoundError("No input dataset found. Checked:\n" + "\n".join(str(root / c) for c in candidates))


def read_table(path: Path) -> pd.DataFrame:
    if path.suffix.lower() == ".parquet":
        return pd.read_parquet(path)
    if path.suffix.lower() == ".csv":
        return pd.read_csv(path)
    raise ValueError(f"Unsupported file type: {path}")


def first_existing_col(df: pd.DataFrame, candidates: Sequence[str]) -> Optional[str]:
    for c in candidates:
        if c in df.columns:
            return c
    lower_map = {str(c).lower(): c for c in df.columns}
    for c in candidates:
        if c.lower() in lower_map:
            return lower_map[c.lower()]
    return None


def infer_player_column(df: pd.DataFrame) -> Optional[str]:
    banned = ("id", "url", "href", "slug", "key", "normalized", "norm", "code")
    preferred_tokens = ("player", "footballer", "name", "jugador")
    candidates = []
    for col in df.columns:
        cl = str(col).lower()
        if not any(tok in cl for tok in preferred_tokens):
            continue
        if any(tok in cl for tok in banned):
            continue
        s = df[col]
        if not (pd.api.types.is_string_dtype(s) or s.dtype == object):
            continue
        non_na = s.dropna().astype(str).str.strip()
        if non_na.empty:
            continue
        avg_len = non_na.str.len().mean()
        unique_ratio = non_na.nunique() / max(1, len(non_na))
        candidates.append(("player" in cl, unique_ratio, avg_len, col))
    if not candidates:
        return None
    candidates.sort(key=lambda x: (x[0], x[1], -abs(x[2] - 14)), reverse=True)
    return candidates[0][3]


def infer_position_group(value: object) -> str:
    if pd.isna(value):
        return "UNK"
    raw = str(value).strip()
    s = raw.upper()
    compact = re.sub(r"[^A-Z0-9]+", "", s)
    words = set(re.findall(r"[A-Z]+", s))

    if compact in {"GK", "GOALKEEPER"} or "GK" in words or "GOALKEEPER" in words:
        return "GK"
    if any(code in words for code in ["MF", "MID", "CM", "DM", "AM", "LM", "RM"]):
        return "MID"
    if any(code in words for code in ["DF", "DEF", "CB", "LB", "RB", "WB", "FB"]):
        return "DEF"
    if any(code in words for code in ["FW", "ATT", "ST", "CF", "LW", "RW", "W"]):
        return "ATT"

    if any(token in s for token in ["MIDFIELDER", "MEDIO", "MEDIOCENTRO", "CENTROCAMPISTA", "PIVOT"]):
        return "MID"
    if any(token in s for token in ["DEFENDER", "DEFEN", "CENTRE BACK", "CENTER BACK", "FULLBACK", "FULL BACK", "WING BACK", "LATERAL"]):
        return "DEF"
    if any(token in s for token in ["FORWARD", "STRIKER", "WINGER", "ATTACKER", "DELANTERO", "EXTREMO", "CENTRE FORWARD", "CENTER FORWARD"]):
        return "ATT"
    if any(token in s for token in ["KEEPER", "PORTERO", "GOAL"]):
        return "GK"

    if any(code in compact for code in ["CM", "DM", "AM", "MF"]):
        return "MID"
    if any(code in compact for code in ["CB", "LB", "RB", "WB", "DF"]):
        return "DEF"
    if any(code in compact for code in ["LW", "RW", "ST", "CF", "FW"]):
        return "ATT"
    return s if s in {"DEF", "MID", "ATT", "GK"} else "UNK"


def infer_position_detail(value: object, position_group: str) -> str:
    if pd.isna(value):
        return position_group
    raw = str(value).strip()
    s = raw.upper()
    compact = re.sub(r"[^A-Z0-9]+", "", s)
    words = set(re.findall(r"[A-Z]+", s))

    if position_group == "GK":
        return "GK"

    if position_group == "DEF":
        if any(code in words for code in ["LB", "RB", "WB", "LWB", "RWB", "FB"]) or any(t in s for t in ["FULLBACK", "FULL BACK", "WING BACK", "LATERAL", "LEFT BACK", "RIGHT BACK"]):
            return "FB"
        if any(code in words for code in ["CB", "LCB", "RCB"]) or any(t in s for t in ["CENTRE BACK", "CENTER BACK", "CENTRAL DEFENDER"]):
            return "CB"
        if any(code in compact for code in ["LB", "RB", "WB", "FB"]):
            return "FB"
        if "CB" in compact:
            return "CB"
        return "CB"  # conservative default: most generic DEF observations are centre-backs

    if position_group == "ATT":
        if any(code in words for code in ["LW", "RW", "W", "LM", "RM"]) or any(t in s for t in ["WINGER", "EXTREMO", "WIDE"]):
            return "WIDE"
        if any(code in words for code in ["ST", "CF"]) or any(t in s for t in ["STRIKER", "CENTRE FORWARD", "CENTER FORWARD", "DELANTERO"]):
            return "CF"
        if any(code in compact for code in ["LW", "RW"]):
            return "WIDE"
        if any(code in compact for code in ["ST", "CF"]):
            return "CF"
        return "CF"  # conservative default: generic FW usually behaves as central forward

    if position_group == "MID":
        if any(code in words for code in ["DM", "CDM"]) or "DEFENSIVE MID" in s:
            return "DM"
        if any(code in words for code in ["AM", "CAM"]) or "ATTACKING MID" in s:
            return "AM"
        if any(code in words for code in ["CM", "MF", "MID"]):
            return "CM"
        return "CM"

    return position_group


def assign_role_subgroup(position_group: str, position_detail: str) -> str:
    if position_group == "DEF":
        return "DEF_FB" if position_detail == "FB" else "DEF_CB"
    if position_group == "ATT":
        return "ATT_WIDE" if position_detail == "WIDE" else "ATT_CF"
    if position_group == "MID":
        return "MID"
    if position_group == "GK":
        return "GK"
    return "UNK"


def standardize_ids(df: pd.DataFrame) -> pd.DataFrame:
    out = df.copy()
    canonical = pd.DataFrame(index=out.index)
    source_map = {}
    for target, candidates in ID_CANDIDATES.items():
        col = first_existing_col(out, candidates)
        if target == "player" and col is None:
            col = infer_player_column(out)
        if col is not None:
            canonical[target] = out[col]
            source_map[target] = col
        else:
            canonical[target] = np.nan
            source_map[target] = None

    alias_cols = set()
    for candidates in ID_CANDIDATES.values():
        lower_map = {str(c).lower(): c for c in out.columns}
        for c in candidates:
            if c in out.columns:
                alias_cols.add(c)
            if c.lower() in lower_map:
                alias_cols.add(lower_map[c.lower()])
    out = out.drop(columns=[c for c in alias_cols if c in out.columns], errors="ignore")

    for target in ID_CANDIDATES:
        out[target] = canonical[target]

    out["position_raw"] = out["position_detail"].fillna(out["position_group"])
    out["position_group"] = out["position_group"].apply(infer_position_group)
    out["position_detail"] = [infer_position_detail(v, g) for v, g in zip(out["position_raw"], out["position_group"])]
    out["role_subgroup"] = [assign_role_subgroup(g, d) for g, d in zip(out["position_group"], out["position_detail"])]

    for c in ["player", "team", "league", "season", "position_detail", "role_subgroup"]:
        out[c] = out[c].fillna("").astype(str)
    out["age"] = pd.to_numeric(out["age"], errors="coerce")
    out["minutes"] = pd.to_numeric(out["minutes"], errors="coerce")

    out["player_key"] = out["player"].map(normalize_key)
    out["team_key"] = out["team"].map(normalize_key)
    out["league_key"] = out["league"].map(normalize_key)
    out["season_key"] = out["season"].astype(str).map(normalize_key)

    print("[TM.6] Canonical source columns:")
    for target, source in source_map.items():
        print(f"[TM.6]   {target}: {source}")
    return out


def build_feature_frame(df: pd.DataFrame, role_subgroup: str) -> Tuple[pd.DataFrame, List[str], List[str]]:
    values = {}
    feature_names = []
    source_cols = []
    for canonical in SUBGROUP_FEATURES[role_subgroup]:
        col = first_existing_col(df, [canonical] + FEATURE_ALIASES.get(canonical, []))
        if col is not None:
            values[canonical] = pd.to_numeric(df[col], errors="coerce")
            feature_names.append(canonical)
            source_cols.append(col)

    # Derived defensive activity fallback.
    if role_subgroup in {"DEF_CB", "DEF_FB", "MID"} and "defensive_activity" not in values:
        parts = []
        for name in ["tackles_p90", "interceptions_p90", "blocks_p90"]:
            col = first_existing_col(df, [name] + FEATURE_ALIASES.get(name, []))
            if col is not None:
                parts.append(pd.to_numeric(df[col], errors="coerce"))
        if parts:
            values["defensive_activity"] = pd.concat(parts, axis=1).mean(axis=1)
            feature_names.append("defensive_activity")
            source_cols.append("derived:tackles+interceptions+blocks")

    # Derived G+A fallback.
    if role_subgroup in {"ATT_CF", "ATT_WIDE"} and "ga_p90" not in values:
        g_col = first_existing_col(df, ["goals_p90"] + FEATURE_ALIASES.get("goals_p90", []))
        a_col = first_existing_col(df, ["assists_p90"] + FEATURE_ALIASES.get("assists_p90", []))
        if g_col is not None and a_col is not None:
            values["ga_p90"] = pd.to_numeric(df[g_col], errors="coerce") + pd.to_numeric(df[a_col], errors="coerce")
            feature_names.append("ga_p90")
            source_cols.append("derived:goals+assists")

    if not values:
        raise ValueError(f"No usable features for subgroup {role_subgroup}.")

    X = pd.DataFrame(values, index=df.index)
    valid = []
    valid_sources = []
    for c, src in zip(X.columns, source_cols):
        non_na = X[c].notna().sum()
        nunique = X[c].nunique(dropna=True)
        if non_na >= max(10, int(0.05 * len(X))) and nunique > 1:
            valid.append(c)
            valid_sources.append(src)
    X = X[valid]
    if X.empty:
        raise ValueError(f"All candidate features for {role_subgroup} were empty or constant.")
    return X, list(X.columns), valid_sources


def robust_scale(X: pd.DataFrame) -> np.ndarray:
    imputer = SimpleImputer(strategy="median")
    scaler = RobustScaler()
    return scaler.fit_transform(imputer.fit_transform(X))


def choose_k(role_subgroup: str, n: int, override: Optional[int] = None) -> int:
    base = override if override is not None else DEFAULT_K[role_subgroup]
    if n < MIN_SUBGROUP_SIZE[role_subgroup]:
        return max(2, min(base, int(max(2, math.sqrt(n / 3)))))
    return min(base, max(2, n - 1))


def top_positive_features(centroid: np.ndarray, feature_names: List[str], top_n: int = 5) -> List[str]:
    order = np.argsort(-centroid)
    return [feature_names[i] for i in order[:top_n] if centroid[i] > 0]


def label_from_centroid(role_subgroup: str, centroid: np.ndarray, feature_names: List[str], used: set[str]) -> str:
    top = set(top_positive_features(centroid, feature_names, 6))

    candidates: List[Tuple[str, int]] = []
    def score(label: str, keys: Sequence[str]) -> None:
        candidates.append((label, sum(1 for k in keys if k in top)))

    if role_subgroup == "DEF_CB":
        score("Ball Playing Centre Back", ["progressive_passes_p90", "progressive_carries_p90", "pass_completion"])
        score("Defensive Stopper", ["blocks_p90", "clearances_p90", "aerial_win_pct", "defensive_activity"])
        score("Aggressive Centre Back", ["tackles_p90", "interceptions_p90", "defensive_activity"])
        score("Complete Centre Back", ["minutes", "availability", "confidence", "growth"])
    elif role_subgroup == "DEF_FB":
        score("Attacking Fullback", ["progressive_carries_p90", "assists_p90", "sca_p90"])
        score("Build-Up Fullback", ["progressive_passes_p90", "pass_completion", "progressive_carries_p90"])
        score("Defensive Fullback", ["defensive_activity", "tackles_p90", "interceptions_p90", "blocks_p90"])
        score("Two-Way Fullback", ["minutes", "availability", "growth", "confidence"])
    elif role_subgroup == "MID":
        score("Creative Playmaker", ["key_passes_p90", "assists_p90", "sca_p90", "gca_p90"])
        score("Ball Progressor", ["progressive_passes_p90", "progressive_carries_p90", "progressive_receptions_p90", "pass_completion"])
        score("Defensive Anchor", ["defensive_activity", "tackles_p90", "interceptions_p90", "pass_completion"])
        score("Box-to-Box Engine", ["minutes", "availability", "defensive_activity", "progressive_carries_p90", "growth"])
    elif role_subgroup == "ATT_CF":
        score("Penalty Box Finisher", ["goals_p90", "xg_p90", "sot_p90", "finishing"])
        score("Target Forward", ["aerial_win_pct", "shots_p90", "xg_p90", "minutes"])
        score("Linking Forward", ["assists_p90", "ga_p90", "confidence", "growth"])
        score("Mobile Striker", ["ga_p90", "shots_p90", "availability", "growth"])
    elif role_subgroup == "ATT_WIDE":
        score("Wide Creator", ["assists_p90", "xa_p90", "sca_p90", "gca_p90"])
        score("Inside Forward", ["goals_p90", "shots_p90", "sot_p90", "finishing"])
        score("Direct Runner", ["progressive_carries_p90", "progressive_receptions_p90", "ga_p90"])
        score("Hybrid Winger", ["minutes", "availability", "growth", "confidence"])
    elif role_subgroup == "GK":
        score("Shot Stopper", ["save_pct", "psxg_ga", "clean_sheets"])
        score("Sweeper Keeper", ["sweeper_actions_p90", "launch_completion_pct"])
        score("Build-Up Goalkeeper", ["launch_completion_pct", "availability", "confidence"])

    candidates.sort(key=lambda x: x[1], reverse=True)
    for label, sc in candidates:
        if sc > 0 and label not in used:
            used.add(label)
            return label
    for label, _ in candidates:
        if label not in used:
            used.add(label)
            return label
    label = f"{role_subgroup} Hybrid Role {len(used) + 1}"
    used.add(label)
    return label


def label_clusters(role_subgroup: str, labels: np.ndarray, X_scaled: np.ndarray, feature_names: List[str]) -> Tuple[Dict[int, str], pd.DataFrame]:
    cluster_ids = sorted(np.unique(labels).tolist())
    used: set[str] = set()
    mapping: Dict[int, str] = {}
    centroid_rows = []
    for cid in cluster_ids:
        centroid = X_scaled[labels == cid].mean(axis=0)
        role = label_from_centroid(role_subgroup, centroid, feature_names, used)
        mapping[cid] = role
        top_feats = top_positive_features(centroid, feature_names, 8)
        row = {
            "role_subgroup": role_subgroup,
            "cluster": cid,
            "derived_role": role,
            "cluster_size": int((labels == cid).sum()),
            "top_positive_features": ", ".join(top_feats),
        }
        for f, v in zip(feature_names, centroid):
            row[f"centroid_{f}"] = round(float(v), 4)
        centroid_rows.append(row)
    return mapping, pd.DataFrame(centroid_rows)


def format_similar(row: pd.Series, sim: float) -> str:
    return f"{str(row.get('player','')).strip()} | {str(row.get('team','')).strip()} | {str(row.get('season','')).strip()} | {round(float(sim), 1)}"


def compute_similarity_scores(X_scaled: np.ndarray, centroids: np.ndarray) -> np.ndarray:
    dists = np.linalg.norm(X_scaled[:, None, :] - centroids[None, :, :], axis=2)
    positive = dists[np.isfinite(dists) & (dists > 0)]
    scale = float(np.median(positive)) if len(positive) else 1.0
    if scale <= 0:
        scale = 1.0
    return 100.0 * np.exp(-dists / scale)


def compute_roles_for_subgroup(df_group: pd.DataFrame, role_subgroup: str, k_override: Optional[int] = None) -> Tuple[pd.DataFrame, GroupResult, pd.DataFrame]:
    X_raw, feature_names, source_cols = build_feature_frame(df_group, role_subgroup)
    real_features_ex_minutes = [f for f in feature_names if f != "minutes"]
    if len(real_features_ex_minutes) < MIN_REAL_FEATURES[role_subgroup]:
        raise ValueError(
            f"Only {len(real_features_ex_minutes)} real non-minute features for {role_subgroup}; "
            f"required {MIN_REAL_FEATURES[role_subgroup]}. Features={feature_names}"
        )

    X_scaled = robust_scale(X_raw)
    n = len(df_group)
    k = choose_k(role_subgroup, n, k_override)

    model = KMeans(n_clusters=k, random_state=42, n_init=50, max_iter=500)
    labels = model.fit_predict(X_scaled)

    sil = None
    if len(set(labels)) > 1 and n > len(set(labels)):
        try:
            sil = float(silhouette_score(X_scaled, labels))
        except Exception:
            sil = None

    cluster_role_map, centroid_report = label_clusters(role_subgroup, labels, X_scaled, feature_names)
    centroid_report["position_group"] = df_group["position_group"].iloc[0] if len(df_group) else ""
    centroid_report["features_used"] = ", ".join(feature_names)
    centroid_report["source_columns"] = ", ".join(source_cols)

    centroids = model.cluster_centers_
    sim_scores = compute_similarity_scores(X_scaled, centroids)
    sorted_clusters = np.argsort(-sim_scores, axis=1)

    base_cols = [
        "player", "season", "team", "league", "position_group", "position_detail", "role_subgroup",
        "age", "minutes", "player_key", "team_key", "season_key",
    ]
    out = df_group[base_cols].copy()
    out["primary_role_cluster"] = labels.astype(int)
    out["primary_role"] = [cluster_role_map[int(c)] for c in labels]

    secondary_clusters = []
    secondary_roles = []
    primary_sims = []
    secondary_sims = []
    for i, ranked in enumerate(sorted_clusters):
        p_cluster = int(ranked[0])
        s_cluster = int(ranked[1]) if len(ranked) > 1 else p_cluster
        p_sim = float(sim_scores[i, p_cluster])
        s_sim = float(sim_scores[i, s_cluster]) if s_cluster != p_cluster else 0.0
        secondary_clusters.append(s_cluster)
        secondary_roles.append(cluster_role_map[s_cluster] if s_cluster != p_cluster else "N/A")
        primary_sims.append(round(p_sim, 1))
        secondary_sims.append(round(s_sim, 1))

    out["secondary_role_cluster"] = secondary_clusters
    out["secondary_role"] = secondary_roles
    out["primary_role_similarity"] = primary_sims
    out["secondary_role_similarity"] = secondary_sims
    out["role_confidence"] = (out["primary_role_similarity"] - out["secondary_role_similarity"]).clip(lower=0).round(1)
    out["role_ambiguity"] = (100 - out["role_confidence"]).clip(0, 100).round(1)

    sim_matrix = cosine_similarity(X_scaled)
    similar_cols = {f"role_similar_player_{i}": [] for i in range(1, 6)}
    for i in range(n):
        order = np.argsort(-sim_matrix[i])
        picked = []
        seen_players = {out.iloc[i]["player_key"]}
        for same_role_first in [True, False]:
            for j in order:
                if j == i:
                    continue
                candidate_key = out.iloc[j]["player_key"]
                if candidate_key in seen_players:
                    continue
                if same_role_first and out.iloc[j]["primary_role"] != out.iloc[i]["primary_role"]:
                    continue
                picked.append(format_similar(out.iloc[j], sim_matrix[i, j] * 100))
                seen_players.add(candidate_key)
                if len(picked) == 5:
                    break
            if len(picked) == 5:
                break
        while len(picked) < 5:
            picked.append("")
        for idx in range(1, 6):
            similar_cols[f"role_similar_player_{idx}"].append(picked[idx - 1])
    for col, vals in similar_cols.items():
        out[col] = vals

    result = GroupResult(
        role_subgroup=role_subgroup,
        position_group=str(df_group["position_group"].iloc[0]) if len(df_group) else "",
        n_players=n,
        n_features=len(feature_names),
        k=k,
        silhouette=sil,
        feature_names=feature_names,
    )
    return out, result, centroid_report


def build_reports(universal: pd.DataFrame, group_results: List[GroupResult], centroid_reports: List[pd.DataFrame], reports_dir: Path, representative_min_minutes: float) -> None:
    reports_dir.mkdir(parents=True, exist_ok=True)

    dist = (
        universal.groupby(["position_group", "role_subgroup", "primary_role"], dropna=False)
        .agg(players=("player", "count"), avg_confidence=("role_confidence", "mean"), avg_ambiguity=("role_ambiguity", "mean"), avg_minutes=("minutes", "mean"))
        .reset_index()
        .sort_values(["position_group", "role_subgroup", "players"], ascending=[True, True, False])
    )
    dist.to_csv(reports_dir / "universal_role_distribution.csv", index=False)

    reps = []
    for (group, subgroup, role), sub in universal.groupby(["position_group", "role_subgroup", "primary_role"]):
        candidates = sub[sub["minutes"].fillna(0) >= representative_min_minutes].copy()
        rep_filter = f"minutes>={representative_min_minutes:g}"
        if candidates.empty and representative_min_minutes > 900:
            candidates = sub[sub["minutes"].fillna(0) >= 900].copy()
            rep_filter = "minutes>=900_fallback"
        if candidates.empty:
            candidates = sub.copy()
            rep_filter = "all_fallback"
        top = candidates.sort_values(["primary_role_similarity", "minutes", "role_confidence"], ascending=[False, False, False]).head(10)
        for rank, (_, row) in enumerate(top.iterrows(), start=1):
            reps.append({
                "position_group": group,
                "role_subgroup": subgroup,
                "primary_role": role,
                "rank": rank,
                "player": row.get("player"),
                "team": row.get("team"),
                "league": row.get("league"),
                "season": row.get("season"),
                "primary_role_similarity": row.get("primary_role_similarity"),
                "role_confidence": row.get("role_confidence"),
                "minutes": row.get("minutes"),
                "representative_filter": rep_filter,
            })
    pd.DataFrame(reps).to_csv(reports_dir / "universal_role_representatives.csv", index=False)

    report = pd.DataFrame([
        {
            "position_group": r.position_group,
            "role_subgroup": r.role_subgroup,
            "n_players": r.n_players,
            "n_features": r.n_features,
            "k": r.k,
            "silhouette": r.silhouette,
            "features": ", ".join(r.feature_names),
        }
        for r in group_results
    ])
    report.to_csv(reports_dir / "universal_role_model_report.csv", index=False)

    if centroid_reports:
        pd.concat(centroid_reports, ignore_index=True).to_csv(reports_dir / "universal_role_centroids.csv", index=False)


def main() -> None:
    parser = argparse.ArgumentParser(description="Build position-aware universal role intelligence artifact.")
    parser.add_argument("--root", default=".", help="Project root. Default: current directory.")
    parser.add_argument("--input", default=None, help="Optional explicit input dataset path.")
    parser.add_argument("--min-minutes", type=float, default=900.0, help="Minimum minutes for role modelling universe.")
    parser.add_argument("--representative-min-minutes", type=float, default=1200.0, help="Minimum minutes used for representative report.")
    parser.add_argument("--include-gk", action="store_true", help="Attempt GK modelling only if enough GK-specific features exist.")
    args = parser.parse_args()

    root = find_project_root(Path(args.root))
    input_path = Path(args.input) if args.input else resolve_first_existing(root, [
        "data/processed/player_season_modeling_v13b_productive_candidate.parquet",
        "data/processed/player_season_modeling_v13b_advanced.parquet",
        "data/processed/player_season_modeling_advanced_v13a.parquet",
        "data/processed/player_season_modeling_v13a.parquet",
        "data/processed/player_season_modeling.parquet",
        "reports/rankings/scoring_dataset.csv",
    ])
    if not input_path.is_absolute():
        input_path = root / input_path

    print(f"[TM.6] Project root: {root}")
    print(f"[TM.6] Input dataset: {input_path}")
    raw = read_table(input_path)
    df = standardize_ids(raw)

    print("[TM.6] Position-group distribution after standardization:")
    print(df["position_group"].value_counts(dropna=False).to_string())
    print("[TM.6] Role-subgroup distribution before filters:")
    print(df["role_subgroup"].value_counts(dropna=False).to_string())

    blank_players = int(df["player_key"].eq("").sum())
    print(f"[TM.6] Usable player keys: {len(df) - blank_players:,}/{len(df):,}")

    universe = df[df["position_group"].isin(["DEF", "MID", "ATT", "GK"])].copy()
    universe = universe[universe["player_key"].ne("")]
    if args.min_minutes is not None:
        universe = universe[(universe["minutes"].isna()) | (universe["minutes"] >= args.min_minutes)].copy()
    universe = universe.drop_duplicates(["player_key", "team_key", "season_key", "role_subgroup"], keep="last")

    print("[TM.6] Modelling universe after minutes/filter/dedup:")
    if universe.empty:
        print("[TM.6]   EMPTY")
    else:
        print(universe["role_subgroup"].value_counts(dropna=False).to_string())

    subgroup_order = ["DEF_CB", "DEF_FB", "MID", "ATT_CF", "ATT_WIDE"]
    if args.include_gk:
        subgroup_order.append("GK")
    else:
        print("[TM.6] GK skipped by default. Use --include-gk if GK-specific features are available and validated.")

    outputs = []
    group_results: List[GroupResult] = []
    centroid_reports: List[pd.DataFrame] = []
    for subgroup in subgroup_order:
        gdf = universe[universe["role_subgroup"].eq(subgroup)].copy()
        if len(gdf) < 10:
            print(f"[TM.6] Skipping {subgroup}: only {len(gdf)} rows.")
            continue
        try:
            out, result, centroid_report = compute_roles_for_subgroup(gdf, subgroup)
            outputs.append(out)
            group_results.append(result)
            centroid_reports.append(centroid_report)
            sil = "N/A" if result.silhouette is None else f"{result.silhouette:.3f}"
            print(f"[TM.6] {subgroup}: n={result.n_players}, features={result.n_features}, k={result.k}, silhouette={sil}")
            print(f"[TM.6]   roles: {', '.join(sorted(out['primary_role'].unique()))}")
        except Exception as exc:
            print(f"[TM.6] WARNING: failed for {subgroup}: {exc}")

    if not outputs:
        raise RuntimeError("No role outputs generated. Check input features and position columns.")

    universal = pd.concat(outputs, ignore_index=True)

    final_cols = [
        "player", "season", "team", "league", "position_group", "position_detail", "role_subgroup", "age", "minutes",
        *ROLE_COLUMNS,
    ]
    for c in final_cols:
        if c not in universal.columns:
            universal[c] = np.nan
    universal = universal[final_cols + ["player_key", "team_key", "season_key"]]

    output_dir = root / "data" / "processed"
    output_dir.mkdir(parents=True, exist_ok=True)
    output_path = output_dir / "player_role_universal.parquet"
    universal[final_cols].to_parquet(output_path, index=False)

    reports_dir = root / "reports" / "roles"
    build_reports(universal[final_cols], group_results, centroid_reports, reports_dir, args.representative_min_minutes)

    print(f"[TM.6] Output written: {output_path}")
    print(f"[TM.6] Reports written: {reports_dir}")
    print("[TM.6] Coverage by subgroup:")
    print(universal.groupby(["position_group", "role_subgroup"])["player"].count().to_string())


if __name__ == "__main__":
    main()
