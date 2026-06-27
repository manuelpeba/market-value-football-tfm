from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

import pandas as pd

from src.dss.registry import PlayerRegistry
from src.dss.scoring import load_scoring_layer
from src.dss.presentation import build_display_dataset

YAN_DIOMANDE_ID = 1390649

registry = PlayerRegistry.build()
base_df = load_scoring_layer()

display_df = build_display_dataset(base_df, registry=registry)
yan = display_df[display_df["player_id_tm"] == YAN_DIOMANDE_ID]

print("TM.7.4 PRESENTATION ENGINE AUDIT")
print("=" * 80)
print("base rows:", len(base_df))
print("display rows:", len(display_df))
print("display columns:", list(display_df.columns))
print()
print("Yan Diomande display row:")
print(yan.T)

assert not display_df.empty
assert len(display_df.columns) <= 40
assert len(yan) == 1

row = yan.iloc[0]

assert row["display_club"] == "RasenBallsport Leipzig"
assert row["display_league"] == "Bundesliga"
assert round(float(row["display_market_value_eur"]), 0) == 75000000
assert int(row["display_minutes_played"]) == 2472
assert round(float(row["display_opportunity_score"]), 2) == 69.95
assert round(float(row["display_confidence_score"]), 2) == 59.51
assert round(float(row["display_predicted_market_value_eur"]), 0) == 13066159
assert round(float(row["display_market_value_gap_eur"]), 0) == 12466159

# Critical anti-leakage checks
assert row["display_market_value_eur"] != row["display_portfolio_cost_eur"]
assert row["display_market_value_eur"] == 75000000
assert row["display_performance_market_value_eur"] == 20000000
assert row["display_portfolio_cost_eur"] == 600000

print()
print("OK — TM.7.4 Presentation Engine closed")
