from __future__ import annotations

from .models import DecisionContext, DecisionEvidence


def build_decision_evidence(context: DecisionContext) -> tuple[DecisionEvidence, ...]:
    evidence: list[DecisionEvidence] = []

    if context.market_value_gap_pct is not None:
        if context.market_value_gap_pct >= 25:
            evidence.append(DecisionEvidence(
                code="market_undervaluation",
                label="Market undervaluation",
                polarity="positive",
                value=context.market_value_gap_pct,
                explanation="Estimated value is materially above observed market value.",
            ))
        elif context.market_value_gap_pct <= -10:
            evidence.append(DecisionEvidence(
                code="market_overvaluation",
                label="Market overvaluation risk",
                polarity="negative",
                value=context.market_value_gap_pct,
                explanation="Observed market value appears above the model-implied valuation.",
            ))

    if context.opportunity_score is not None:
        if context.opportunity_score >= 75:
            evidence.append(DecisionEvidence(
                code="high_opportunity",
                label="High opportunity score",
                polarity="positive",
                value=context.opportunity_score,
                explanation="The player ranks strongly within the opportunity framework.",
            ))
        elif context.opportunity_score < 45:
            evidence.append(DecisionEvidence(
                code="low_opportunity",
                label="Limited opportunity signal",
                polarity="negative",
                value=context.opportunity_score,
                explanation="Opportunity score is below the preferred scouting threshold.",
            ))

    if context.growth_score is not None:
        if context.growth_score >= 70:
            evidence.append(DecisionEvidence(
                code="growth_upside",
                label="Growth upside",
                polarity="positive",
                value=context.growth_score,
                explanation="Growth score indicates attractive future value potential.",
            ))
        elif context.growth_score < 40:
            evidence.append(DecisionEvidence(
                code="weak_growth",
                label="Weak growth signal",
                polarity="negative",
                value=context.growth_score,
                explanation="Growth score does not support a strong appreciation thesis.",
            ))

    if context.confidence_score is not None:
        if context.confidence_score >= 70:
            evidence.append(DecisionEvidence(
                code="high_confidence",
                label="High analytical confidence",
                polarity="positive",
                value=context.confidence_score,
                explanation="The recommendation is supported by relatively reliable data signals.",
            ))
        elif context.confidence_score < 45:
            evidence.append(DecisionEvidence(
                code="low_confidence",
                label="Low analytical confidence",
                polarity="negative",
                value=context.confidence_score,
                explanation="The recommendation requires additional validation before action.",
            ))

    if context.risk_score is not None:
        if context.risk_score <= 35:
            evidence.append(DecisionEvidence(
                code="controlled_risk",
                label="Controlled risk profile",
                polarity="positive",
                value=context.risk_score,
                explanation="Risk score remains within an acceptable range.",
            ))
        elif context.risk_score >= 65:
            evidence.append(DecisionEvidence(
                code="high_risk",
                label="High risk profile",
                polarity="negative",
                value=context.risk_score,
                explanation="Risk score is elevated and should constrain decision urgency.",
            ))

    return tuple(evidence)


def attach_evidence(context: DecisionContext) -> DecisionContext:
    return DecisionContext(
        **{
            **context.__dict__,
            "evidence": build_decision_evidence(context),
        }
    )
