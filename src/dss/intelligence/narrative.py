from __future__ import annotations

from .models import DecisionContext
from .recommendation import generate_dss_recommendation


def build_executive_decision_narrative(context: DecisionContext) -> str:
    rec = generate_dss_recommendation(context)
    action = rec["decision_action"]
    positives = rec["positive_evidence"]
    negatives = rec["negative_evidence"]

    player = context.player_name
    club = context.club or "current club unavailable"
    league = context.league or "league unavailable"

    intro = f"{player} ({club}, {league}) receives a DSS action of {action}."

    if positives:
        positive_text = " Main supporting signals: " + "; ".join(e.label for e in positives[:3]) + "."
    else:
        positive_text = " No dominant positive signal is strong enough to drive an automatic buy recommendation."

    if negatives:
        negative_text = " Main constraints: " + "; ".join(e.label for e in negatives[:3]) + "."
    else:
        negative_text = " No major negative constraint dominates the current analytical profile."

    if action == "BUY":
        closing = " Recommended next step: initiate recruitment validation and prepare transfer feasibility assessment."
    elif action == "MONITOR":
        closing = " Recommended next step: keep the player in the watchlist and wait for stronger confirmation."
    elif action == "COMPARE":
        closing = " Recommended next step: compare against positional alternatives before committing resources."
    else:
        closing = " Recommended next step: deprioritize unless external scouting evidence contradicts the model."

    return intro + positive_text + negative_text + closing
