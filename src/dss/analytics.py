from __future__ import annotations

import pandas as pd

from src.dss.contracts import PlayerAnalytics
from src.dss.utils import first, safe_float, safe_str


def build_player_analytics(row: pd.Series | dict) -> PlayerAnalytics:
    return PlayerAnalytics(
        season=safe_str(first(row, ["season", "current_season"])),
        modeling_club=safe_str(first(row, ["club", "season_context_club", "modeling_club"])),
        modeling_league=safe_str(first(row, ["league", "season_context_league", "modeling_league"])),
        modeling_age=safe_float(first(row, ["age", "age_tm", "modeling_age"])),
        modeling_market_value_eur=safe_float(first(row, ["market_value_eur", "modeling_market_value_eur"])),
        minutes_played=safe_float(first(row, ["minutes_played", "minutes", "playing_time_minutes"])),
        opportunity_score=safe_float(first(row, ["opportunity_score", "risk_adjusted_opportunity_score"])),
        risk_score=safe_float(first(row, ["risk_score"])),
        confidence_score=safe_float(first(row, ["confidence_score", "matching_confidence"])),
        role=safe_str(first(row, ["primary_role", "role_subgroup", "tm69_role_subgroup", "taxonomy_role_context"])),
        expected_market_value_eur=safe_float(first(row, [
            "expected_market_value_eur",
            "predicted_market_value_eur",
            "xgb_predicted_market_value_eur",
        ])),
        market_value_gap_eur=safe_float(first(row, [
            "market_value_gap_eur",
            "valuation_gap_eur",
            "gap_eur",
        ])),
    )
