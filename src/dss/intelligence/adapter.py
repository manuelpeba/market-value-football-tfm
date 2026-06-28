from __future__ import annotations

from typing import Any

from .context import build_player_decision_context
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


def _safe_str(value: Any) -> str | None:
    if value is None:
        return None
    text = str(value).strip()
    if not text or text.lower() in {"nan", "none", "null", "n/a", "na"}:
        return None
    return text


def _get_attr(obj: Any, name: str, default: Any = None) -> Any:
    if obj is None:
        return default
    return getattr(obj, name, default)


def _first(*values: Any) -> Any:
    for value in values:
        if value is None:
            continue
        try:
            if value != value:
                continue
        except Exception:
            pass
        if isinstance(value, str) and not value.strip():
            continue
        return value
    return None


def build_decision_context_from_player_view(player_view: Any) -> DecisionContext:
    """
    Convert the certified PlayerView domain object into a DSS DecisionContext.

    This adapter is the only place where the intelligence layer knows how to read
    PlayerView internals. Streamlit should call this adapter instead of manually
    reconstructing DSS fields from dataframe columns.
    """
    if player_view is None:
        return DecisionContext(player_name="Unknown player", source="PlayerViewAdapter")

    base = build_player_decision_context(player_view)

    identity = _get_attr(player_view, "identity")
    scoring = _get_attr(player_view, "scoring")
    portfolio = _get_attr(player_view, "portfolio")
    performance = _get_attr(player_view, "performance")

    return DecisionContext(
        player_name=_safe_str(_first(
            _get_attr(identity, "player_name"),
            _get_attr(identity, "name"),
            base.player_name if base.player_name != "Unknown player" else None,
        )) or "Unknown player",

        club=_safe_str(_first(base.club, _get_attr(identity, "club"))),
        league=_safe_str(_first(base.league, _get_attr(identity, "league"))),
        position=_safe_str(_first(
            base.position,
            _get_attr(identity, "position"),
            _get_attr(identity, "position_group"),
        )),
        age=_safe_float(_first(base.age, _get_attr(identity, "age"))),

        market_value_eur=_safe_float(_first(
            base.market_value_eur,
            _get_attr(identity, "market_value_eur"),
            _get_attr(portfolio, "market_value_eur"),
        )),
        predicted_market_value_eur=_safe_float(_first(
            base.predicted_market_value_eur,
            _get_attr(portfolio, "predicted_market_value_eur"),
        )),
        market_value_gap_eur=_safe_float(_first(
            base.market_value_gap_eur,
            _get_attr(portfolio, "market_value_gap_eur"),
        )),
        market_value_gap_pct=_safe_float(_first(
            base.market_value_gap_pct,
            _get_attr(portfolio, "market_value_gap_pct"),
        )),

        opportunity_score=_safe_float(_first(
            base.opportunity_score,
            _get_attr(scoring, "opportunity_score"),
        )),
        growth_score=_safe_float(_first(
            base.growth_score,
            _get_attr(scoring, "growth_score"),
        )),
        confidence_score=_safe_float(_first(
            base.confidence_score,
            _get_attr(scoring, "confidence_score"),
        )),
        risk_score=_safe_float(_first(
            base.risk_score,
            _get_attr(scoring, "risk_score"),
        )),
        risk_level=_safe_str(_first(
            base.risk_level,
            _get_attr(scoring, "risk_level"),
        )),
        risk_adjusted_opportunity_score=_safe_float(_first(
            base.risk_adjusted_opportunity_score,
            _get_attr(portfolio, "risk_adjusted_opportunity_score"),
        )),
        executive_decision_score=_safe_float(_first(
            base.executive_decision_score,
            _get_attr(portfolio, "executive_decision_score"),
        )),

        source="PlayerViewAdapter",
    )
