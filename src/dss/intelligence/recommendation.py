from __future__ import annotations

from .evidence import attach_evidence
from .models import DecisionAction, DecisionContext, DecisionEvidence
from .policies import evaluate_decision_policies, policy_score


def classify_decision_action(context: DecisionContext) -> DecisionAction:
    risk = context.risk_score
    confidence = context.confidence_score
    score = policy_score(context)

    if risk is not None and risk >= 75:
        return "AVOID"

    if score >= 78 and (confidence is None or confidence >= 50):
        return "BUY"

    if score >= 62:
        return "COMPARE"

    if score >= 45:
        return "MONITOR"

    return "AVOID"


def generate_dss_recommendation(context: DecisionContext) -> dict:
    policy_results = evaluate_decision_policies(context)
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

    action = classify_decision_action(enriched)

    positives = [e for e in enriched.evidence if e.polarity == "positive"]
    negatives = [e for e in enriched.evidence if e.polarity == "negative"]
    neutrals = [e for e in enriched.evidence if e.polarity == "neutral"]

    return {
        "player_name": enriched.player_name,
        "decision_action": action,
        "policy_score": policy_score(enriched),
        "policy_results": policy_results,
        "positive_evidence": positives,
        "negative_evidence": negatives,
        "neutral_evidence": neutrals,
        "evidence": enriched.evidence,
        "context": enriched,
    }
