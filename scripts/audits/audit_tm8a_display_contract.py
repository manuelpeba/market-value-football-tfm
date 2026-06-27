from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[2]
APP = ROOT / "app" / "streamlit_app.py"

text = APP.read_text(encoding="utf-8", errors="ignore")

forbidden = [
    "display_dss_confidence_score",
    "display_dss_opportunity_score",
    "display_dss_risk_score",
    "display_dss_roi_3y_pct",
    "display_dss_expected_roi_pct",
    "display_dss_future_asset_score",
    "display_dss_risk_adjusted_opportunity_score",
    "display_dss_executive_decision_score",
    "display_dss_predicted_market_value_eur",
    "display_dss_market_value_gap_eur",
    "display_dss_market_value_gap_pct",
]

violations = []

for token in forbidden:
    if token in text:
        violations.append(token)

display_tokens = sorted(set(re.findall(r"\bdisplay_[a-zA-Z0-9_]+\b", text)))

print("TM.8A DISPLAY CONTRACT AUDIT")
print("=" * 80)
print("display tokens:", len(display_tokens))
print()
for token in display_tokens:
    print(token)

if violations:
    print()
    print("Forbidden legacy display_dss_* tokens found:")
    for token in violations:
        print("-", token)
    raise SystemExit("FAIL: display contract still contains legacy display_dss_* fields")

print()
print("OK — TM.8A Display Contract Normalization closed")
