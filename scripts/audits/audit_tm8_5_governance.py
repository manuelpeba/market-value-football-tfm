from pathlib import Path
import sys
import re

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

from src.dss.presentation import DISPLAY_COLUMNS

APP = ROOT / "app" / "streamlit_app.py"
app_text = APP.read_text(encoding="utf-8", errors="ignore")

required_display_contract = {
    "Identity": [
        "display_club",
        "display_league",
        "display_age",
        "display_market_value_eur",
        "display_position",
        "display_position_group",
        "display_nationality",
    ],
    "Performance": [
        "display_minutes_played",
        "display_goals",
        "display_assists",
        "display_performance_season",
        "display_performance_club",
        "display_performance_league",
        "display_performance_market_value_eur",
    ],
    "Scoring": [
        "display_opportunity_score",
        "display_confidence_score",
        "display_risk_score",
        "display_growth_score",
        "display_opportunity_tier",
    ],
    "Portfolio": [
        "display_predicted_market_value_eur",
        "display_market_value_gap_eur",
        "display_market_value_gap_pct",
        "display_future_asset_score",
        "display_roi_score",
        "display_portfolio_cost_eur",
    ],
}

print("=" * 80)
print("TM.8.5 GOVERNANCE CERTIFICATION")
print("=" * 80)

missing_contract = []

for family, fields in required_display_contract.items():
    print(f"\n{family}")
    print("-" * 40)

    for field in fields:
        in_contract = field in DISPLAY_COLUMNS
        ui_count = len(re.findall(rf"\b{re.escape(field)}\b", app_text))

        if in_contract:
            print(f"✓ {field:<45} contract=YES ui_refs={ui_count}")
        else:
            print(f"✗ {field:<45} contract=NO  ui_refs={ui_count}")
            missing_contract.append(field)

if missing_contract:
    print()
    print("Missing fields in Presentation DISPLAY_COLUMNS:")
    for field in missing_contract:
        print("-", field)
    raise SystemExit("FAIL: Display contract incomplete")

print()
print("OK — Governance certified")
