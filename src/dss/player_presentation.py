from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable

import pandas as pd

from src.dss.player_registry import PlayerRegistry


REQUIRED_PRESENTATION_COLUMNS = {
    "player_id_tm",
    "player_name_fbref",
    "season",
    "season_context_club",
    "season_context_league",
    "season_context_market_value_eur",
    "current_club_snapshot",
    "current_league_snapshot",
    "current_market_value_eur_snapshot",
    "display_club",
    "display_league",
    "display_market_value_eur",
    "context_changed",
    "club_context_changed",
    "league_context_changed",
    "valuation_context",
    "gap_interpretation_status",
}

FORBIDDEN_PRESENTATION_COLUMNS = {
    "club",
    "league",
    "market_value_eur",
    "current_club",
    "current_league",
    "current_market_value_eur",
}


@dataclass(frozen=True)
class PresentationContract:
    required_columns: set[str]
    forbidden_columns: set[str]


DEFAULT_PRESENTATION_CONTRACT = PresentationContract(
    required_columns=REQUIRED_PRESENTATION_COLUMNS,
    forbidden_columns=FORBIDDEN_PRESENTATION_COLUMNS,
)


def validate_display_contract(
    df: pd.DataFrame,
    contract: PresentationContract = DEFAULT_PRESENTATION_CONTRACT,
) -> None:
    """
    Validate that the DSS presentation layer exposes governed context columns
    and does not leak raw ambiguous context columns into UI consumers.
    """
    missing = sorted(contract.required_columns - set(df.columns))
    forbidden = sorted(contract.forbidden_columns & set(df.columns))

    if missing:
        raise ValueError(f"Presentation dataset missing required columns: {missing}")

    if forbidden:
        raise ValueError(f"Presentation dataset contains forbidden raw columns: {forbidden}")


def _first_existing_column(df: pd.DataFrame, candidates: Iterable[str]) -> str | None:
    for col in candidates:
        if col in df.columns:
            return col
    return None


def build_display_dataset(registry: PlayerRegistry) -> pd.DataFrame:
    """
    Build the canonical DSS presentation dataset.

    TM.8.9B.2 intentionally starts from the governed global universe generated
    by TM.8.8. Later TM.8.9 steps will enrich this dataset with contract, role,
    risk and strategy signals while preserving this contract.
    """
    base = registry.global_universe.copy()

    rename_map = {}

    if "club" in base.columns and "season_context_club" not in base.columns:
        rename_map["club"] = "season_context_club"

    if "league" in base.columns and "season_context_league" not in base.columns:
        rename_map["league"] = "season_context_league"

    if "market_value_eur" in base.columns and "season_context_market_value_eur" not in base.columns:
        rename_map["market_value_eur"] = "season_context_market_value_eur"

    if rename_map:
        base = base.rename(columns=rename_map)

    for col in REQUIRED_PRESENTATION_COLUMNS:
        if col not in base.columns:
            base[col] = pd.NA

    # Remove ambiguous raw context columns from presentation consumers.
    base = base.drop(columns=[c for c in FORBIDDEN_PRESENTATION_COLUMNS if c in base.columns], errors="ignore")

    validate_display_contract(base)

    return base
