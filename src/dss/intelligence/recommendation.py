from __future__ import annotations

from .evidence import attach_evidence
from .models import DecisionAction, DecisionContext


def classify_decision_action(context: DecisionContext) -> DecisionAction:
    opportunity = context.opportunity_score
    risk = context.risk_score
    confidence = context.confidence_score
    gap_pct = context.market_value_gap_pct
    executive = context.executive_decision_score

    if opportunity is None:
        return "COMPARE"

    if risk is not None and risk >= 75:
        return "AVOID"

    if opportunity >= 75:
        if risk is not None and risk <= 55 and (confidence is None or confidence >= 50):
            return "BUY"
        return "MONITOR"

    if opportunity >= 60:
        if gap_pct is not None and gap_pct >= 20 and (risk is None or risk <= 60):
            return "COMPARE"
        return "MONITOR"

    if executive is not None and executive >= 70 and (risk is None or risk <= 60):
        return "COMPARE"

    return "AVOID"


def generate_dss_recommendation(context: DecisionContext) -> dict:
    enriched = attach_evidence(context)
    action = classify_decision_action(enriched)

    positives = [e for e in enriched.evidence if e.polarity == "positive"]
    negatives = [e for e in enriched.evidence if e.polarity == "negative"]

    return {
        "player_name": enriched.player_name,
        "decision_action": action,
        "positive_evidence": positives,
        "negative_evidence": negatives,
        "evidence": enriched.evidence,
        "context": enriched,
    }
