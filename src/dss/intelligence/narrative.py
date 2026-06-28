from __future__ import annotations

from .models import DecisionContext
from .recommendation import build_dss_recommendation
from .strategy import BALANCED, StrategyProfile


def build_executive_decision_narrative(
    context: DecisionContext,
    strategy_profile: StrategyProfile = BALANCED,
) -> str:
    rec = build_dss_recommendation(context, strategy_profile=strategy_profile)

    player = context.player_name
    club = context.club or "current club unavailable"
    league = context.league or "league unavailable"

    intro = (
        f"{player} ({club}, {league}) receives a DSS action of {rec.action} "
        f"under the {strategy_profile.label} strategy profile."
    )

    if rec.positive_evidence:
        positive_text = (
            " Main supporting signals: "
            + "; ".join(e.label for e in rec.positive_evidence[:3])
            + "."
        )
    else:
        positive_text = " No dominant positive signal is strong enough to drive an automatic buy recommendation."

    if rec.negative_evidence:
        negative_text = (
            " Main constraints: "
            + "; ".join(e.label for e in rec.negative_evidence[:3])
            + "."
        )
    else:
        negative_text = " No major negative constraint dominates the current analytical profile."

    closing = f" Recommended next step: {rec.recommended_next_step}"

    return intro + positive_text + negative_text + closing
