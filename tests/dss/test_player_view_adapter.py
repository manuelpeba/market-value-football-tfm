from types import SimpleNamespace

from src.dss.intelligence import (
    build_decision_context_from_player_view,
    build_dss_recommendation,
)


def test_player_view_adapter_uses_domain_objects():
    player_view = SimpleNamespace(
        identity=SimpleNamespace(
            player_name="Adapter Prospect",
            club="Adapter FC",
            league="Serie A",
            position="W",
            age=22,
            market_value_eur=10_000_000,
        ),
        scoring=SimpleNamespace(
            opportunity_score=84,
            growth_score=78,
            confidence_score=72,
            risk_score=31,
            risk_level="Low",
        ),
        portfolio=SimpleNamespace(
            predicted_market_value_eur=16_000_000,
            market_value_gap_eur=6_000_000,
            market_value_gap_pct=60,
            risk_adjusted_opportunity_score=70,
            executive_decision_score=82,
        ),
    )

    context = build_decision_context_from_player_view(player_view)

    assert context.player_name == "Adapter Prospect"
    assert context.club == "Adapter FC"
    assert context.league == "Serie A"
    assert context.opportunity_score == 84
    assert context.market_value_gap_pct == 60
    assert context.source == "PlayerViewAdapter"

    rec = build_dss_recommendation(context)
    assert rec.action == "BUY"


def test_player_view_adapter_handles_none():
    context = build_decision_context_from_player_view(None)

    assert context.player_name == "Unknown player"
    assert context.source == "PlayerViewAdapter"
