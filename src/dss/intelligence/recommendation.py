from __future__ import annotations

from .evidence import attach_evidence
from .models import DecisionAction, DecisionContext, DecisionEvidence
from .policies import evaluate_decision_policies, policy_score
from .recommendation_result import (
    DSSRecommendation,
    build_executive_summary,
    recommended_next_step_for_action,
)
from .strategy import BALANCED, StrategyProfile


def classify_decision_action(
    context: DecisionContext,
    strategy_profile: StrategyProfile = BALANCED,
) -> DecisionAction:
    risk = context.risk_score
    confidence = context.confidence_score
    score = policy_score(context, strategy_profile=strategy_profile)

    critical_risk_cutoff = 75 + (strategy_profile.risk_tolerance - 0.50) * 20
    if risk is not None and risk >= critical_risk_cutoff:
        return "AVOID"

    if score >= strategy_profile.buy_threshold and (
        confidence is None or confidence >= strategy_profile.min_confidence_for_buy
    ):
        return "BUY"

    if score >= strategy_profile.compare_threshold:
        return "COMPARE"

    if score >= strategy_profile.monitor_threshold:
        return "MONITOR"

    return "AVOID"


def build_dss_recommendation(
    context: DecisionContext,
    strategy_profile: StrategyProfile = BALANCED,
) -> DSSRecommendation:
    policy_results = evaluate_decision_policies(
        context,
        strategy_profile=strategy_profile,
    )
    policy_evidence: list[DecisionEvidence] = [
        evidence
        for result in policy_results
        for evidence in result.evidence
    ]

    legacy_context = attach_evidence(context)
    all_evidence = tuple(policy_evidence) + legacy_context.evidence

    enriched = DecisionContext(
        **{
            **context.__dict__,
            "evidence": all_evidence,
        }
    )

    action = classify_decision_action(enriched, strategy_profile=strategy_profile)

    positives = tuple(e for e in enriched.evidence if e.polarity == "positive")
    negatives = tuple(e for e in enriched.evidence if e.polarity == "negative")
    neutrals = tuple(e for e in enriched.evidence if e.polarity == "neutral")

    return DSSRecommendation(
        player_name=enriched.player_name,
        action=action,
        strategy_profile=strategy_profile,
        policy_score=policy_score(enriched, strategy_profile=strategy_profile),
        context=enriched,
        policy_results=policy_results,
        evidence=enriched.evidence,
        positive_evidence=positives,
        negative_evidence=negatives,
        neutral_evidence=neutrals,
        recommended_next_step=recommended_next_step_for_action(action),
        executive_summary=build_executive_summary(
            player_name=enriched.player_name,
            action=action,
            strategy_profile=strategy_profile,
            positive_evidence=positives,
            negative_evidence=negatives,
        ),
    )


def generate_dss_recommendation(
    context: DecisionContext,
    strategy_profile: StrategyProfile = BALANCED,
) -> dict:
    """
    Backward-compatible dictionary adapter.

    New code should prefer build_dss_recommendation().
    """
    rec = build_dss_recommendation(context, strategy_profile=strategy_profile)

    return {
        "player_name": rec.player_name,
        "decision_action": rec.action,
        "strategy_profile": rec.strategy_profile,
        "policy_score": rec.policy_score,
        "policy_results": rec.policy_results,
        "positive_evidence": list(rec.positive_evidence),
        "negative_evidence": list(rec.negative_evidence),
        "neutral_evidence": list(rec.neutral_evidence),
        "evidence": rec.evidence,
        "context": rec.context,
        "recommended_next_step": rec.recommended_next_step,
        "executive_summary": rec.executive_summary,
    }
