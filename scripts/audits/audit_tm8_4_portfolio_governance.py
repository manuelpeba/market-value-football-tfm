from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[2]
APP = ROOT / "app" / "streamlit_app.py"

lines = APP.read_text(encoding="utf-8", errors="ignore").splitlines()

legacy_patterns = [
    r'safe_get\(row,\s*"predicted_market_value_eur"',
    r'get_numeric_value\(row,\s*"predicted_market_value_eur"',
    r'safe_get\(row,\s*"market_value_gap_eur"',
    r'get_numeric_value\(row,\s*"market_value_gap_eur"',
    r'safe_get\(row,\s*"market_value_gap_pct"',
    r'get_numeric_value\(row,\s*"market_value_gap_pct"',
    r'safe_get\(row,\s*"roi_score"',
    r'get_numeric_value\(row,\s*"roi_score"',
    r'safe_get\(row,\s*"future_asset_score"',
    r'get_numeric_value\(row,\s*"future_asset_score"',
    r'safe_get\(row,\s*"portfolio_cost"',
    r'get_numeric_value\(row,\s*"portfolio_cost"',
]

# Contextos que NO deben migrarse (lógica de negocio)
ignore_tokens = [
    "pulp",
    "lpSum",
    "budget",
    "optimizer",
    "optimization",
    "portfolio_cost_share",
    "budget_utilization",
    "selected_cost",
    "constraints",
    "candidate",
    "model +=",
]

violations = []

for i, line in enumerate(lines, start=1):
    stripped = line.strip()

    if stripped.startswith("#"):
        continue

    matched = False
    for pattern in legacy_patterns:
        if re.search(pattern, stripped):
            matched = True
            break

    if not matched:
        continue

    # Already migrated: display_* is the primary read; legacy token is only fallback.
    if "display_" in stripped:
        continue

    if any(token in stripped for token in ignore_tokens):
        continue

    violations.append((i, stripped))

print("TM.8.4 PORTFOLIO GOVERNANCE AUDIT")
print("=" * 80)

if violations:
    print("Visual portfolio legacy reads:")
    for line_no, content in violations:
        print(f"{line_no}: {content}")

    print()
    raise SystemExit(f"FAIL: {len(violations)} visual portfolio reads remain")

print("OK — TM.8.4 Portfolio Governance closed")
