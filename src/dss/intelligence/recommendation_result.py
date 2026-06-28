from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from .models import DecisionAction, DecisionContext, DecisionEvidence
from .policies import PolicyResult
from .strategy import StrategyProfile


@dataclass(frozen=True)
class DSSRecommendation:
    player_name: str
    action: DecisionAction
    strategy_profile: StrategyProfile
    policy_score: float

    context: DecisionContext
    policy_results: tuple[PolicyResult, ...]
    evidence: tuple[DecisionEvidence, ...]

    positive_evidence: tuple[DecisionEvidence, ...]
    negative_evidence: tuple[DecisionEvidence, ...]
    neutral_evidence: tuple[DecisionEvidence, ...]

    recommended_next_step: str
    executive_summary: str

    def to_dict(self) -> dict[str, Any]:
        return {
            "player_name": self.player_name,
            "action": self.action,
            "strategy_profile": {
                "name": self.strategy_profile.name,
                "label": self.strategy_profile.label,
                "description": self.strategy_profile.description,
            },
            "policy_score": self.policy_score,
            "recommended_next_step": self.recommended_next_step,
            "executive_summary": self.executive_summary,
            "evidence": [
                {
                    "code": e.code,
                    "label": e.label,
                    "polarity": e.polarity,
                    "value": e.value,
                    "explanation": e.explanation,
                }
                for e in self.evidence
            ],
            "policy_results": [
                {
                    "policy_name": p.policy_name,
                    "score_delta": p.score_delta,
                    "evidence_codes": [e.code for e in p.evidence],
                }
                for p in self.policy_results
            ],
        }


def recommended_next_step_for_action(action: DecisionAction) -> str:
    if action == "BUY":
        return "Initiate recruitment validation and prepare transfer feasibility assessment."
    if action == "COMPARE":
        return "Compare against positional alternatives before committing recruitment resources."
    if action == "MONITOR":
        return "Keep the player in the watchlist and wait for stronger confirmation."
    return "Deprioritize unless external scouting evidence contradicts the analytical recommendation."


def build_executive_summary(
    player_name: str,
    action: DecisionAction,
    strategy_profile: StrategyProfile,
    positive_evidence: tuple[DecisionEvidence, ...],
    negative_evidence: tuple[DecisionEvidence, ...],
) -> str:
    if positive_evidence:
        positives = "; ".join(e.label for e in positive_evidence[:3])
    else:
        positives = "no dominant positive signal"

    if negative_evidence:
        negatives = "; ".join(e.label for e in negative_evidence[:3])
    else:
        negatives = "no major negative constraint"

    return (
        f"{player_name} receives a DSS action of {action} under the "
        f"{strategy_profile.label} strategy profile. "
        f"Main supporting signals: {positives}. "
        f"Main constraints: {negatives}."
    )
