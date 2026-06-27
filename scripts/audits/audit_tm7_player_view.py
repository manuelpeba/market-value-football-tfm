from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

from src.dss.identity import load_identity_layer, build_identity_lookup
from src.dss.performance import load_performance_layer, build_performance_lookup
from src.dss.scoring import load_scoring_layer, build_scoring_lookup
from src.dss.portfolio import load_portfolio_layer, build_portfolio_lookup
from src.dss.player_view import build_player_view

YAN_DIOMANDE_ID = 1390649

identity_lookup = build_identity_lookup(load_identity_layer())
performance_lookup = build_performance_lookup(load_performance_layer())
scoring_lookup = build_scoring_lookup(load_scoring_layer())
portfolio_lookup = build_portfolio_lookup(load_portfolio_layer())

view = build_player_view(
    YAN_DIOMANDE_ID,
    identity_lookup=identity_lookup,
    performance_lookup=performance_lookup,
    scoring_lookup=scoring_lookup,
    portfolio_lookup=portfolio_lookup,
)

print("TM.7.2 PLAYER VIEW AUDIT")
print("=" * 80)
print(view)
print()
print("player_name:", view.player_name)
print("current_club:", view.current_club)
print("current_league:", view.current_league)
print("current_age:", view.current_age)
print("current_market_value_eur:", view.current_market_value_eur)
print("latest_season:", view.latest_season)
print("performance_minutes:", view.performance_minutes)
print("opportunity_score:", view.opportunity_score)
print("confidence_score:", view.confidence_score)
print("opportunity_tier:", view.opportunity_tier)
print("predicted_market_value_eur:", view.predicted_market_value_eur)
print("market_value_gap_eur:", view.market_value_gap_eur)
print("portfolio_cost_eur:", view.portfolio_cost_eur)

assert view is not None
assert view.identity is not None
assert view.performance is not None
assert view.scoring is not None
assert view.portfolio is not None

assert view.current_club == "RasenBallsport Leipzig"
assert view.current_league == "Bundesliga"
assert round(float(view.current_market_value_eur), 0) == 75000000
assert int(view.performance_minutes) == 2472
assert round(float(view.opportunity_score), 2) == 69.95

print()
print("OK — TM.7.2 PlayerView closed")
