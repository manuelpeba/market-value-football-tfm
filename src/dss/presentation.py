from __future__ import annotations

from typing import Any

import pandas as pd

from src.dss.common import normalize_player_id
from src.dss.registry import PlayerRegistry


DISPLAY_COLUMNS = [
    "player_id_tm",
    "display_player_name",
    "display_club",
    "display_league",
    "display_age",
    "display_market_value_eur",
    "display_position",
    "display_position_group",
    "display_nationality",
    "display_valuation_date",
    "display_performance_season",
    "display_performance_club",
    "display_performance_league",
    "display_minutes_played",
    "display_goals",
    "display_assists",
    "display_performance_market_value_eur",
    "display_opportunity_score",
    "display_confidence_score",
    "display_risk_score",
    "display_opportunity_tier",
    "display_growth_score",
    "display_predicted_market_value_eur",
    "display_market_value_gap_eur",
    "display_market_value_gap_pct",
    "display_roi_pct",
    "display_roi_score",
    "display_upside_eur",
    "display_future_asset_score",
    "display_risk_adjusted_opportunity_score",
    "display_executive_decision_score",
    "display_portfolio_score_conservative",
    "display_portfolio_score_balanced",
    "display_portfolio_score_aggressive",
    "display_portfolio_cost_eur",
]


def _safe(value: Any) -> Any:
    try:
        if pd.isna(value):
            return None
    except Exception:
        pass
    return value


def build_display_row(player_id_tm: Any, registry: PlayerRegistry) -> dict[str, Any] | None:
    player_id = normalize_player_id(player_id_tm)
    if player_id is None:
        return None

    view = registry.get(player_id)
    if view is None or not view.is_resolved:
        return None

    identity = view.identity
    performance = view.performance
    scoring = view.scoring
    portfolio = view.portfolio

    return {
        "player_id_tm": player_id,

        # Identity Authority
        "display_player_name": _safe(identity.player_name) if identity else None,
        "display_club": _safe(identity.club) if identity else None,
        "display_league": _safe(identity.league) if identity else None,
        "display_age": _safe(identity.age) if identity else None,
        "display_market_value_eur": _safe(identity.market_value_eur) if identity else None,
        "display_position": _safe(identity.position) if identity else None,
        "display_position_group": _safe(identity.position_group) if identity else None,
        "display_nationality": _safe(identity.nationality) if identity else None,
        "display_valuation_date": _safe(identity.valuation_date) if identity else None,

        # Performance Authority
        "display_performance_season": _safe(performance.season) if performance else None,
        "display_performance_club": _safe(performance.club) if performance else None,
        "display_performance_league": _safe(performance.league) if performance else None,
        "display_minutes_played": _safe(performance.minutes_played) if performance else None,
        "display_goals": _safe(performance.goals) if performance else None,
        "display_assists": _safe(performance.assists) if performance else None,
        "display_performance_market_value_eur": _safe(performance.market_value_eur) if performance else None,

        # Scoring Authority
        "display_opportunity_score": _safe(scoring.opportunity_score) if scoring else None,
        "display_confidence_score": _safe(scoring.confidence_score) if scoring else None,
        "display_risk_score": _safe(scoring.risk_score) if scoring else None,
        "display_opportunity_tier": _safe(scoring.tier) if scoring else None,
        "display_growth_score": _safe(scoring.growth_score) if scoring else None,

        # Portfolio Authority
        "display_predicted_market_value_eur": _safe(portfolio.predicted_market_value_eur) if portfolio else None,
        "display_market_value_gap_eur": _safe(portfolio.market_value_gap_eur) if portfolio else None,
        "display_market_value_gap_pct": _safe(portfolio.market_value_gap_pct) if portfolio else None,
        "display_roi_pct": _safe(portfolio.roi_pct) if portfolio else None,
        "display_roi_score": _safe(portfolio.roi_score) if portfolio else None,
        "display_upside_eur": _safe(portfolio.upside_eur) if portfolio else None,
        "display_future_asset_score": _safe(portfolio.future_asset_score) if portfolio else None,
        "display_risk_adjusted_opportunity_score": _safe(portfolio.risk_adjusted_opportunity_score) if portfolio else None,
        "display_executive_decision_score": _safe(portfolio.executive_decision_score) if portfolio else None,
        "display_portfolio_score_conservative": _safe(portfolio.portfolio_score_conservative) if portfolio else None,
        "display_portfolio_score_balanced": _safe(portfolio.portfolio_score_balanced) if portfolio else None,
        "display_portfolio_score_aggressive": _safe(portfolio.portfolio_score_aggressive) if portfolio else None,
        "display_portfolio_cost_eur": _safe(portfolio.portfolio_cost_eur) if portfolio else None,
    }


def build_display_dataset(
    base_df: pd.DataFrame,
    registry: PlayerRegistry | None = None,
    player_id_col: str = "player_id_tm",
) -> pd.DataFrame:
    """
    Presentation Engine.

    Receives any base dataframe with player_id_tm and returns a UI-safe DisplayDataset.
    It never mutates or overwrites legacy columns.
    """
    if player_id_col not in base_df.columns:
        raise KeyError(f"Base dataframe must contain {player_id_col}")

    if registry is None:
        registry = PlayerRegistry.build()

    rows: list[dict[str, Any]] = []

    for raw_id in base_df[player_id_col].tolist():
        row = build_display_row(raw_id, registry)
        if row is not None:
            rows.append(row)

    display_df = pd.DataFrame(rows)

    for col in DISPLAY_COLUMNS:
        if col not in display_df.columns:
            display_df[col] = None

    return display_df[DISPLAY_COLUMNS].copy()
