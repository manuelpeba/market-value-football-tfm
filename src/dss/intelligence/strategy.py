from __future__ import annotations

from dataclasses import dataclass
from typing import Literal


StrategyName = Literal[
    "balanced",
    "aggressive_growth",
    "low_risk",
    "elite_club",
    "value_investing",
]


@dataclass(frozen=True)
class StrategyProfile:
    name: StrategyName
    label: str
    description: str

    risk_tolerance: float = 0.50
    opportunity_weight: float = 1.00
    market_gap_weight: float = 1.00
    growth_weight: float = 1.00
    confidence_weight: float = 1.00

    max_preferred_age: float | None = None
    min_confidence_for_buy: float = 50.0
    buy_threshold: float = 78.0
    compare_threshold: float = 62.0
    monitor_threshold: float = 45.0


BALANCED = StrategyProfile(
    name="balanced",
    label="Balanced",
    description="Default strategy balancing opportunity, growth, confidence and risk.",
)

AGGRESSIVE_GROWTH = StrategyProfile(
    name="aggressive_growth",
    label="Aggressive Growth",
    description="Prioritizes upside and market inefficiency, accepting higher uncertainty.",
    risk_tolerance=0.75,
    opportunity_weight=1.10,
    market_gap_weight=1.15,
    growth_weight=1.25,
    confidence_weight=0.85,
    max_preferred_age=23,
    min_confidence_for_buy=45,
    buy_threshold=76,
    compare_threshold=60,
)

LOW_RISK = StrategyProfile(
    name="low_risk",
    label="Low Risk",
    description="Prioritizes confidence and controlled downside over maximum upside.",
    risk_tolerance=0.30,
    opportunity_weight=0.90,
    market_gap_weight=0.90,
    growth_weight=0.85,
    confidence_weight=1.25,
    min_confidence_for_buy=65,
    buy_threshold=82,
    compare_threshold=68,
    monitor_threshold=50,
)

ELITE_CLUB = StrategyProfile(
    name="elite_club",
    label="Elite Club",
    description="Raises the bar for direct action; suitable for clubs with high quality thresholds.",
    risk_tolerance=0.40,
    opportunity_weight=1.05,
    market_gap_weight=0.85,
    growth_weight=0.95,
    confidence_weight=1.15,
    max_preferred_age=24,
    min_confidence_for_buy=65,
    buy_threshold=86,
    compare_threshold=72,
    monitor_threshold=52,
)

VALUE_INVESTING = StrategyProfile(
    name="value_investing",
    label="Value Investing",
    description="Prioritizes undervaluation and risk-adjusted opportunity under budget discipline.",
    risk_tolerance=0.55,
    opportunity_weight=1.00,
    market_gap_weight=1.35,
    growth_weight=1.00,
    confidence_weight=1.00,
    max_preferred_age=25,
    min_confidence_for_buy=55,
    buy_threshold=78,
    compare_threshold=61,
)


DEFAULT_STRATEGY_PROFILES = {
    "balanced": BALANCED,
    "aggressive_growth": AGGRESSIVE_GROWTH,
    "low_risk": LOW_RISK,
    "elite_club": ELITE_CLUB,
    "value_investing": VALUE_INVESTING,
}


def get_strategy_profile(name: str | None = None) -> StrategyProfile:
    if not name:
        return BALANCED
    key = str(name).strip().lower().replace(" ", "_").replace("-", "_")
    return DEFAULT_STRATEGY_PROFILES.get(key, BALANCED)
