from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

from src.dss.portfolio import build_portfolio_lookup, load_portfolio_layer

YAN_DIOMANDE_ID = 1390649

df = load_portfolio_layer()
lookup = build_portfolio_lookup(df)

print("TM.7 PORTFOLIO AUTHORITY AUDIT")
print("=" * 80)
print("rows:", len(df))
print("players:", len(lookup))
print("columns:", list(df.columns))
print()
print("Yan Diomande:")
print(lookup.get(YAN_DIOMANDE_ID))

required_any = [
    "predicted_market_value_eur",
    "market_value_gap_eur",
    "roi_pct",
    "future_asset_score",
    "executive_decision_score",
]

available = [c for c in required_any if c in df.columns and df[c].notna().any()]
print()
print("available portfolio metrics:", available)

if not available:
    raise SystemExit("FAIL: no portfolio metrics available")

if YAN_DIOMANDE_ID not in lookup:
    raise SystemExit("FAIL: Yan Diomande not found in Portfolio Authority")

print()
print("OK")
