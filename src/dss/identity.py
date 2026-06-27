from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any

import pandas as pd

from src.dss.common import normalize_float, normalize_player_id


ROOT = Path(__file__).resolve().parents[2]
DEFAULT_IDENTITY_PATH = ROOT / "data" / "processed" / "player_identity_current.parquet"


@dataclass(frozen=True)
class PlayerIdentity:
    player_id_tm: int
    player_name: str | None = None
    club: str | None = None
    league: str | None = None
    age: float | None = None
    market_value_eur: float | None = None
    valuation_date: str | None = None
    position: str | None = None
    position_group: str | None = None
    nationality: str | None = None
    source: str | None = None
    snapshot_version: str | None = None
    quality_status: str | None = None


def load_identity_layer(path: Path | str = DEFAULT_IDENTITY_PATH) -> pd.DataFrame:
    path = Path(path)
    if not path.exists():
        raise FileNotFoundError(f"Identity layer not found: {path}")

    df = pd.read_parquet(path)

    if "player_id_tm" not in df.columns:
        raise KeyError("Identity layer must contain player_id_tm")

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


def build_identity_lookup(df: pd.DataFrame | None = None) -> dict[int, PlayerIdentity]:
    if df is None:
        df = load_identity_layer()

    lookup: dict[int, PlayerIdentity] = {}

    for _, row in df.iterrows():
        player_id = normalize_player_id(row.get("player_id_tm"))
        if player_id is None:
            continue

        lookup[player_id] = PlayerIdentity(
            player_id_tm=player_id,
            player_name=_get(row, "player_name_display", "player_name_tm", "player_name"),
            club=_get(row, "current_club", "club"),
            league=_get(row, "current_league", "league"),
            age=normalize_float(_get(row, "current_age", "age")),
            market_value_eur=normalize_float(_get(row, "current_market_value_eur", "market_value_eur")),
            valuation_date=_get(row, "valuation_date"),
            position=_get(row, "current_position", "position"),
            position_group=_get(row, "current_position_group", "position_group"),
            nationality=_get(row, "nationality"),
            source=_get(row, "identity_source"),
            snapshot_version=_get(row, "identity_snapshot_version"),
            quality_status=_get(row, "identity_quality_status"),
        )

    return lookup


def get_player_identity(
    player_id_tm: Any,
    lookup: dict[int, PlayerIdentity] | None = None,
) -> PlayerIdentity | None:
    player_id = normalize_player_id(player_id_tm)
    if player_id is None:
        return None
    if lookup is None:
        lookup = build_identity_lookup()
    return lookup.get(player_id)


# ---------------------------------------------------------------------
# Legacy compatibility adapter — TM.7 migration
# ---------------------------------------------------------------------
def build_player_identity(row_or_player_id=None, lookup: dict[int, PlayerIdentity] | None = None):
    """
    Backward-compatible adapter for legacy Streamlit code.

    New code should use:
        PlayerRegistry.get(player_id).identity
    """
    if isinstance(row_or_player_id, dict):
        player_id = row_or_player_id.get("player_id_tm")
    else:
        try:
            player_id = row_or_player_id.get("player_id_tm")
        except Exception:
            player_id = row_or_player_id

    return get_player_identity(player_id, lookup=lookup)


def missing_identity_from_row(row) -> bool:
    """
    Backward-compatible adapter for legacy TM.7.0 Streamlit code.

    New code should use PlayerRegistry / PlayerView.
    """
    identity = build_player_identity(row)
    return identity is None
