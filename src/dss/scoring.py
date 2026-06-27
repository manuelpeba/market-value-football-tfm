from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any

import pandas as pd

from src.dss.common import normalize_float, normalize_player_id


ROOT = Path(__file__).resolve().parents[2]
DEFAULT_SCORING_PATH = ROOT / "reports" / "dss" / "global_prospect_universe.csv"


@dataclass(frozen=True)
class PlayerScoring:
    player_id_tm: int
    opportunity_score: float | None = None
    confidence_score: float | None = None
    risk_score: float | None = None
    tier: str | None = None
    opportunity_rank: float | None = None
    growth_score: float | None = None
    growth_rank: float | None = None
    is_scouting_target: bool | None = None


def load_scoring_layer(path: Path | str = DEFAULT_SCORING_PATH) -> pd.DataFrame:
    path = Path(path)
    if not path.exists():
        raise FileNotFoundError(f"Scoring layer not found: {path}")

    df = pd.read_csv(path)

    if "player_id_tm" not in df.columns:
        raise KeyError("Scoring layer must contain player_id_tm")

    df = df.copy()
    df["player_id_tm"] = pd.to_numeric(df["player_id_tm"], errors="coerce").astype("Int64")
    df = df[df["player_id_tm"].notna()].copy()

    return df.reset_index(drop=True)


def _get(row: pd.Series, *candidates: str) -> Any:
    for col in candidates:
        if col in row.index:
            value = row.get(col)
            if pd.notna(value):
                return value
    return None


def _to_bool(value: Any) -> bool | None:
    if value is None:
        return None
    try:
        if pd.isna(value):
            return None
    except Exception:
        pass
    if isinstance(value, bool):
        return value
    text = str(value).strip().lower()
    if text in {"1", "true", "yes", "y"}:
        return True
    if text in {"0", "false", "no", "n"}:
        return False
    return None


def build_scoring_lookup(df: pd.DataFrame | None = None) -> dict[int, PlayerScoring]:
    if df is None:
        df = load_scoring_layer()

    lookup: dict[int, PlayerScoring] = {}

    for _, row in df.iterrows():
        player_id = normalize_player_id(row.get("player_id_tm"))
        if player_id is None:
            continue

        lookup[player_id] = PlayerScoring(
            player_id_tm=player_id,
            opportunity_score=normalize_float(_get(row, "opportunity_score")),
            confidence_score=normalize_float(_get(row, "confidence_score")),
            risk_score=normalize_float(_get(row, "risk_score")),
            tier=_get(row, "opportunity_tier", "tier"),
            opportunity_rank=normalize_float(_get(row, "opportunity_rank")),
            growth_score=normalize_float(_get(row, "growth_score")),
            growth_rank=normalize_float(_get(row, "growth_rank")),
            is_scouting_target=_to_bool(_get(row, "is_scouting_target")),
        )

    return lookup


def get_player_scoring(
    player_id_tm: Any,
    lookup: dict[int, PlayerScoring] | None = None,
) -> PlayerScoring | None:
    player_id = normalize_player_id(player_id_tm)
    if player_id is None:
        return None
    if lookup is None:
        lookup = build_scoring_lookup()
    return lookup.get(player_id)
