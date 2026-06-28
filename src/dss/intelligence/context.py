from __future__ import annotations

from typing import Any

from .models import DecisionContext


def _safe_float(value: Any) -> float | None:
    try:
        if value is None:
            return None
        x = float(value)
        if x != x:
            return None
        return x
    except Exception:
        return None


def _first_attr(obj: Any, names: list[str], default: Any = None) -> Any:
    for name in names:
        if hasattr(obj, name):
            value = getattr(obj, name)
            if value is not None:
                return value
    return default


def _from_display_contract(player_view: Any, key: str) -> Any:
    display = getattr(player_view, "display", None)
    if isinstance(display, dict):
        return display.get(key)
    if hasattr(player_view, key):
        return getattr(player_view, key)
    return None


def build_player_decision_context(player_view: Any) -> DecisionContext:
    """
    Build the first DSS Intelligence aggregate from the certified PlayerView/display contract.

    This function is intentionally read-only:
    - no dataset access
    - no Authority mutation
    - no Streamlit dependency
    - no Presentation Engine mutation
    """
    name = (
        _from_display_contract(player_view, "display_player_name")
        or _first_attr(player_view, ["player_name", "name"], "Unknown player")
    )

    return DecisionContext(
        player_name=str(name),
        club=_from_display_contract(player_view, "display_club"),
        league=_from_display_contract(player_view, "display_league"),
        position=_from_display_contract(player_view, "display_position"),
        age=_safe_float(_from_display_contract(player_view, "display_age")),

        market_value_eur=_safe_float(_from_display_contract(player_view, "display_market_value_eur")),
        predicted_market_value_eur=_safe_float(_from_display_contract(player_view, "display_predicted_market_value_eur")),
        market_value_gap_eur=_safe_float(_from_display_contract(player_view, "display_market_value_gap_eur")),
        market_value_gap_pct=_safe_float(_from_display_contract(player_view, "display_market_value_gap_pct")),

        opportunity_score=_safe_float(_from_display_contract(player_view, "display_opportunity_score")),
        growth_score=_safe_float(_from_display_contract(player_view, "display_growth_score")),
        confidence_score=_safe_float(_from_display_contract(player_view, "display_confidence_score")),
        risk_score=_safe_float(_from_display_contract(player_view, "display_risk_score")),
        risk_level=_from_display_contract(player_view, "display_risk_level"),
        risk_adjusted_opportunity_score=_safe_float(
            _from_display_contract(player_view, "display_risk_adjusted_opportunity_score")
        ),
        executive_decision_score=_safe_float(_from_display_contract(player_view, "display_executive_decision_score")),
    )
