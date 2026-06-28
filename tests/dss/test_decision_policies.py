from src.dss.intelligence import (
    DecisionContext,
    classify_decision_action,
    evaluate_decision_policies,
    generate_dss_recommendation,
    policy_score,
)


def test_policy_score_buy_case():
    context = DecisionContext(
        player_name="Elite Prospect",
        market_value_gap_pct=45,
        opportunity_score=86,
        growth_score=80,
        confidence_score=75,
        risk_score=25,
    )

    results = evaluate_decision_policies(context)
    assert len(results) >= 5
    assert policy_score(context) >= 78
    assert classify_decision_action(context) == "BUY"

    rec = generate_dss_recommendation(context)
    assert rec["decision_action"] == "BUY"
    assert rec["policy_score"] >= 78
    assert any(e.code == "strong_market_inefficiency" for e in rec["evidence"])
    assert any(e.code == "elite_opportunity" for e in rec["evidence"])


def test_policy_score_avoid_case_due_to_risk():
    context = DecisionContext(
        player_name="High Risk Prospect",
        market_value_gap_pct=50,
        opportunity_score=88,
        growth_score=82,
        confidence_score=80,
        risk_score=81,
    )

    assert classify_decision_action(context) == "AVOID"

    rec = generate_dss_recommendation(context)
    assert rec["decision_action"] == "AVOID"
    assert any(e.code == "critical_risk_profile" for e in rec["evidence"])


def test_policy_score_monitor_case():
    context = DecisionContext(
        player_name="Unclear Prospect",
        market_value_gap_pct=4,
        opportunity_score=52,
        growth_score=50,
        confidence_score=48,
        risk_score=50,
    )

    assert classify_decision_action(context) == "MONITOR"
