from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

from src.dss.registry import PlayerRegistry

YAN_DIOMANDE_ID = 1390649

registry = PlayerRegistry.build()
view = registry.get(YAN_DIOMANDE_ID)

print("TM.7.3 PLAYER REGISTRY AUDIT")
print("=" * 80)
print("coverage:")
for k, v in registry.coverage().items():
    print(f"{k}: {v}")

print()
print("Yan Diomande:")
print(view)

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
print("OK — TM.7.3 PlayerRegistry closed")
