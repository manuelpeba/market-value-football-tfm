from src.dss.intelligence import (
    DecisionContext,
    build_executive_decision_narrative,
    classify_decision_action,
    generate_dss_recommendation,
    get_strategy_profile,
    policy_score,
)


def test_strategy_profiles_change_policy_score():
    context = DecisionContext(
        player_name="Strategic Prospect",
        age=22,
        market_value_gap_pct=32,
        opportunity_score=74,
        growth_score=78,
        confidence_score=58,
        risk_score=57,
    )

    balanced = get_strategy_profile("balanced")
    aggressive = get_strategy_profile("aggressive_growth")
    low_risk = get_strategy_profile("low_risk")

    balanced_score = policy_score(context, strategy_profile=balanced)
    aggressive_score = policy_score(context, strategy_profile=aggressive)
    low_risk_score = policy_score(context, strategy_profile=low_risk)

    assert aggressive_score > balanced_score
    assert low_risk_score <= balanced_score


def test_strategy_profiles_can_change_decision_action():
    context = DecisionContext(
        player_name="Growth Target",
        age=22,
        market_value_gap_pct=40,
        opportunity_score=76,
        growth_score=82,
        confidence_score=49,
        risk_score=58,
    )

    aggressive = get_strategy_profile("aggressive_growth")
    low_risk = get_strategy_profile("low_risk")

    aggressive_action = classify_decision_action(context, strategy_profile=aggressive)
    low_risk_action = classify_decision_action(context, strategy_profile=low_risk)

    assert aggressive_action in {"BUY", "COMPARE"}
    assert low_risk_action in {"COMPARE", "MONITOR", "AVOID"}
    assert aggressive_action != "AVOID"


def test_recommendation_and_narrative_include_strategy_profile():
    context = DecisionContext(
        player_name="Value Prospect",
        club="Test FC",
        league="Eredivisie",
        age=23,
        market_value_gap_pct=45,
        opportunity_score=80,
        growth_score=70,
        confidence_score=60,
        risk_score=45,
    )

    profile = get_strategy_profile("value_investing")

    rec = generate_dss_recommendation(context, strategy_profile=profile)
    assert rec["strategy_profile"].name == "value_investing"

    narrative = build_executive_decision_narrative(context, strategy_profile=profile)
    assert "Value Investing" in narrative
    assert "Value Prospect" in narrative
