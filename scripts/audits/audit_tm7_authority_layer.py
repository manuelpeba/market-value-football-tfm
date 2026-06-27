from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

YAN_DIOMANDE_ID = 1390649

from src.dss.identity import build_identity_lookup, load_identity_layer
from src.dss.performance import build_performance_lookup, load_performance_layer
from src.dss.scoring import build_scoring_lookup, load_scoring_layer
from src.dss.portfolio import build_portfolio_lookup, load_portfolio_layer


def audit_layer(name, df, lookup, player_id):
    print()
    print(f"{name}")
    print("-" * 80)
    print("rows:", len(df))
    print("players:", len(lookup))
    print("columns:", list(df.columns))
    print("sample:")
    print(lookup.get(player_id))

    if len(df) == 0:
        raise SystemExit(f"FAIL: {name} dataframe is empty")
    if len(lookup) == 0:
        raise SystemExit(f"FAIL: {name} lookup is empty")
    if player_id not in lookup:
        raise SystemExit(f"FAIL: {name} missing Yan Diomande")


print("TM.7.1 AUTHORITY LAYER MASTER AUDIT")
print("=" * 80)

identity_df = load_identity_layer()
identity_lookup = build_identity_lookup(identity_df)
audit_layer("IDENTITY AUTHORITY", identity_df, identity_lookup, YAN_DIOMANDE_ID)

performance_df = load_performance_layer()
performance_lookup = build_performance_lookup(performance_df)
audit_layer("PERFORMANCE AUTHORITY", performance_df, performance_lookup, YAN_DIOMANDE_ID)

scoring_df = load_scoring_layer()
scoring_lookup = build_scoring_lookup(scoring_df)
audit_layer("SCORING AUTHORITY", scoring_df, scoring_lookup, YAN_DIOMANDE_ID)

portfolio_df = load_portfolio_layer()
portfolio_lookup = build_portfolio_lookup(portfolio_df)
audit_layer("PORTFOLIO AUTHORITY", portfolio_df, portfolio_lookup, YAN_DIOMANDE_ID)

print()
print("=" * 80)
print("OK — TM.7.1 Authority Layer closed")
