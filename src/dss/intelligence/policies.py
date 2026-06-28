from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol

from .models import DecisionContext, DecisionEvidence
from .strategy import BALANCED, StrategyProfile


@dataclass(frozen=True)
class PolicyResult:
    policy_name: str
    score_delta: float
    evidence: tuple[DecisionEvidence, ...]


class DecisionPolicy(Protocol):
    name: str

    def evaluate(self, context: DecisionContext) -> PolicyResult:
        ...


class MarketInefficiencyPolicy:
    name = "market_inefficiency"

    def evaluate(self, context: DecisionContext) -> PolicyResult:
        gap = context.market_value_gap_pct
        if gap is None:
            return PolicyResult(self.name, 0.0, ())

        if gap >= 35:
            return PolicyResult(
                self.name,
                22.0,
                (DecisionEvidence(
                    code="strong_market_inefficiency",
                    label="Strong market inefficiency",
                    polarity="positive",
                    value=gap,
                    explanation="The estimated market value is substantially above the observed value.",
                ),),
            )

        if gap >= 15:
            return PolicyResult(
                self.name,
                10.0,
                (DecisionEvidence(
                    code="moderate_market_inefficiency",
                    label="Moderate market inefficiency",
                    polarity="positive",
                    value=gap,
                    explanation="The player shows a positive valuation gap.",
                ),),
            )

        if gap <= -10:
            return PolicyResult(
                self.name,
                -18.0,
                (DecisionEvidence(
                    code="negative_market_gap",
                    label="Negative valuation gap",
                    polarity="negative",
                    value=gap,
                    explanation="The player appears overvalued relative to the model estimate.",
                ),),
            )

        return PolicyResult(self.name, 0.0, ())


class OpportunityPolicy:
    name = "opportunity"

    def evaluate(self, context: DecisionContext) -> PolicyResult:
        score = context.opportunity_score
        if score is None:
            return PolicyResult(self.name, 0.0, ())

        if score >= 80:
            return PolicyResult(
                self.name,
                24.0,
                (DecisionEvidence(
                    code="elite_opportunity",
                    label="Elite opportunity signal",
                    polarity="positive",
                    value=score,
                    explanation="Opportunity score is in the strongest actionable band.",
                ),),
            )

        if score >= 65:
            return PolicyResult(
                self.name,
                12.0,
                (DecisionEvidence(
                    code="solid_opportunity",
                    label="Solid opportunity signal",
                    polarity="positive",
                    value=score,
                    explanation="Opportunity score supports continued recruitment attention.",
                ),),
            )

        if score < 45:
            return PolicyResult(
                self.name,
                -20.0,
                (DecisionEvidence(
                    code="weak_opportunity",
                    label="Weak opportunity signal",
                    polarity="negative",
                    value=score,
                    explanation="Opportunity score is below the actionable scouting band.",
                ),),
            )

        return PolicyResult(self.name, 0.0, ())


class RiskPolicy:
    name = "risk"

    def evaluate(self, context: DecisionContext) -> PolicyResult:
        risk = context.risk_score
        if risk is None:
            return PolicyResult(self.name, 0.0, ())

        if risk <= 30:
            return PolicyResult(
                self.name,
                14.0,
                (DecisionEvidence(
                    code="low_risk_profile",
                    label="Low risk profile",
                    polarity="positive",
                    value=risk,
                    explanation="Risk score is low enough to support decision urgency.",
                ),),
            )

        if risk <= 55:
            return PolicyResult(
                self.name,
                4.0,
                (DecisionEvidence(
                    code="acceptable_risk_profile",
                    label="Acceptable risk profile",
                    polarity="neutral",
                    value=risk,
                    explanation="Risk score does not block the recommendation.",
                ),),
            )

        if risk >= 75:
            return PolicyResult(
                self.name,
                -35.0,
                (DecisionEvidence(
                    code="critical_risk_profile",
                    label="Critical risk profile",
                    polarity="negative",
                    value=risk,
                    explanation="Risk score is too high for direct action.",
                ),),
            )

        return PolicyResult(
            self.name,
            -12.0,
            (DecisionEvidence(
                code="elevated_risk_profile",
                label="Elevated risk profile",
                polarity="negative",
                value=risk,
                explanation="Risk score requires additional validation before commitment.",
            ),),
        )


class GrowthPolicy:
    name = "growth"

    def evaluate(self, context: DecisionContext) -> PolicyResult:
        score = context.growth_score
        if score is None:
            return PolicyResult(self.name, 0.0, ())

        if score >= 75:
            return PolicyResult(
                self.name,
                16.0,
                (DecisionEvidence(
                    code="high_growth_upside",
                    label="High growth upside",
                    polarity="positive",
                    value=score,
                    explanation="Growth score supports a revaluation thesis.",
                ),),
            )

        if score < 40:
            return PolicyResult(
                self.name,
                -10.0,
                (DecisionEvidence(
                    code="limited_growth_upside",
                    label="Limited growth upside",
                    polarity="negative",
                    value=score,
                    explanation="Growth score weakens the investment case.",
                ),),
            )

        return PolicyResult(self.name, 0.0, ())


class ConfidencePolicy:
    name = "confidence"

    def evaluate(self, context: DecisionContext) -> PolicyResult:
        score = context.confidence_score
        if score is None:
            return PolicyResult(self.name, 0.0, ())

        if score >= 70:
            return PolicyResult(
                self.name,
                10.0,
                (DecisionEvidence(
                    code="high_confidence_signal",
                    label="High confidence signal",
                    polarity="positive",
                    value=score,
                    explanation="Data quality and model confidence support the recommendation.",
                ),),
            )

        if score < 45:
            return PolicyResult(
                self.name,
                -14.0,
                (DecisionEvidence(
                    code="low_confidence_signal",
                    label="Low confidence signal",
                    polarity="negative",
                    value=score,
                    explanation="Low confidence requires further scouting validation.",
                ),),
            )

        return PolicyResult(self.name, 0.0, ())


DEFAULT_POLICIES = (
    MarketInefficiencyPolicy(),
    OpportunityPolicy(),
    RiskPolicy(),
    GrowthPolicy(),
    ConfidencePolicy(),
)


def evaluate_decision_policies(
    context: DecisionContext,
    policies: tuple[DecisionPolicy, ...] = DEFAULT_POLICIES,
    strategy_profile: StrategyProfile = BALANCED,
) -> tuple[PolicyResult, ...]:
    raw_results = tuple(policy.evaluate(context) for policy in policies)
    adjusted: list[PolicyResult] = []

    for result in raw_results:
        multiplier = 1.0
        if result.policy_name == "market_inefficiency":
            multiplier = strategy_profile.market_gap_weight
        elif result.policy_name == "opportunity":
            multiplier = strategy_profile.opportunity_weight
        elif result.policy_name == "growth":
            multiplier = strategy_profile.growth_weight
        elif result.policy_name == "confidence":
            multiplier = strategy_profile.confidence_weight
        elif result.policy_name == "risk" and result.score_delta < 0:
            multiplier = max(0.25, 1.25 - strategy_profile.risk_tolerance)

        adjusted.append(PolicyResult(
            policy_name=result.policy_name,
            score_delta=result.score_delta * multiplier,
            evidence=result.evidence,
        ))

    return tuple(adjusted)


def policy_score(
    context: DecisionContext,
    strategy_profile: StrategyProfile = BALANCED,
) -> float:
    base = 50.0
    score = base + sum(
        result.score_delta
        for result in evaluate_decision_policies(context, strategy_profile=strategy_profile)
    )

    if strategy_profile.max_preferred_age is not None and context.age is not None:
        if context.age > strategy_profile.max_preferred_age:
            score -= min(12.0, (context.age - strategy_profile.max_preferred_age) * 3.0)

    return max(0.0, min(100.0, score))
