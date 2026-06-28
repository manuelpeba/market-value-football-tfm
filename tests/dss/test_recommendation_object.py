from src.dss.intelligence import (
    DSSRecommendation,
    DecisionContext,
    build_dss_recommendation,
    generate_dss_recommendation,
    get_strategy_profile,
)


def test_recommendation_object_is_domain_entity():
    context = DecisionContext(
        player_name="Recommendation Prospect",
        club="Test FC",
        league="Bundesliga",
        age=21,
        market_value_gap_pct=42,
        opportunity_score=84,
        growth_score=79,
        confidence_score=72,
        risk_score=28,
    )

    rec = build_dss_recommendation(
        context,
        strategy_profile=get_strategy_profile("balanced"),
    )

    assert isinstance(rec, DSSRecommendation)
    assert rec.player_name == "Recommendation Prospect"
    assert rec.action == "BUY"
    assert rec.policy_score >= 78
    assert rec.recommended_next_step
    assert rec.executive_summary
    assert len(rec.positive_evidence) >= 3


def test_recommendation_object_serializes_to_dict():
    context = DecisionContext(
        player_name="Serializable Prospect",
        market_value_gap_pct=30,
        opportunity_score=72,
        growth_score=65,
        confidence_score=60,
        risk_score=45,
    )

    rec = build_dss_recommendation(context)
    payload = rec.to_dict()

    assert payload["player_name"] == "Serializable Prospect"
    assert "strategy_profile" in payload
    assert "policy_results" in payload
    assert "evidence" in payload
    assert isinstance(payload["evidence"], list)


def test_legacy_generate_dss_recommendation_still_returns_dict():
    context = DecisionContext(
        player_name="Legacy Prospect",
        market_value_gap_pct=40,
        opportunity_score=80,
        growth_score=75,
        confidence_score=70,
        risk_score=30,
    )

    rec = generate_dss_recommendation(context)

    assert isinstance(rec, dict)
    assert rec["decision_action"] == "BUY"
    assert rec["recommended_next_step"]
    assert rec["executive_summary"]
