from types import SimpleNamespace

from src.dss.intelligence import (
    build_executive_decision_narrative,
    build_player_decision_context,
    classify_decision_action,
    generate_dss_recommendation,
)


def test_buy_recommendation_from_display_contract():
    player_view = SimpleNamespace(
        display={
            "display_player_name": "Test Prospect",
            "display_club": "Test FC",
            "display_league": "LaLiga",
            "display_position": "W",
            "display_age": 21,
            "display_market_value_gap_pct": 42,
            "display_opportunity_score": 82,
            "display_growth_score": 76,
            "display_confidence_score": 71,
            "display_risk_score": 33,
        }
    )

    context = build_player_decision_context(player_view)
    assert context.player_name == "Test Prospect"

    action = classify_decision_action(context)
    assert action == "BUY"

    rec = generate_dss_recommendation(context)
    assert rec["decision_action"] == "BUY"
    assert len(rec["positive_evidence"]) >= 3

    narrative = build_executive_decision_narrative(context)
    assert "BUY" in narrative
    assert "Test Prospect" in narrative


def test_high_risk_avoid():
    player_view = SimpleNamespace(
        display={
            "display_player_name": "Risky Prospect",
            "display_opportunity_score": 80,
            "display_confidence_score": 70,
            "display_risk_score": 82,
        }
    )

    context = build_player_decision_context(player_view)
    assert classify_decision_action(context) == "AVOID"
