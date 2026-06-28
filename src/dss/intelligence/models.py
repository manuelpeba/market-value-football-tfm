from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Literal


DecisionAction = Literal["BUY", "MONITOR", "COMPARE", "AVOID"]
EvidencePolarity = Literal["positive", "negative", "neutral"]


@dataclass(frozen=True)
class DecisionEvidence:
    code: str
    label: str
    polarity: EvidencePolarity
    value: Any = None
    explanation: str = ""


@dataclass(frozen=True)
class DecisionContext:
    player_name: str
    club: str | None = None
    league: str | None = None
    position: str | None = None
    age: float | None = None

    market_value_eur: float | None = None
    predicted_market_value_eur: float | None = None
    market_value_gap_eur: float | None = None
    market_value_gap_pct: float | None = None

    opportunity_score: float | None = None
    growth_score: float | None = None
    confidence_score: float | None = None
    risk_score: float | None = None
    risk_level: str | None = None
    risk_adjusted_opportunity_score: float | None = None
    executive_decision_score: float | None = None

    evidence: tuple[DecisionEvidence, ...] = field(default_factory=tuple)
    source: str = "PlayerView"
