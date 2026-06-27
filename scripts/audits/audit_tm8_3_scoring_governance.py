from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[2]
APP = ROOT / "app" / "streamlit_app.py"

lines = APP.read_text(encoding="utf-8", errors="ignore").splitlines()

legacy_patterns = [
    r'safe_get\(row,\s*"opportunity_score"',
    r'get_numeric_value\(row,\s*"opportunity_score"',
    r'safe_get\(row,\s*"confidence_score"',
    r'get_numeric_value\(row,\s*"confidence_score"',
    r'safe_get\(row,\s*"risk_score"',
    r'get_numeric_value\(row,\s*"risk_score"',
    r'safe_get\(row,\s*"growth_score"',
    r'get_numeric_value\(row,\s*"growth_score"',
    r'safe_get\(row,\s*"opportunity_tier"',
]

allowed_context = [
    "tm7_value(",
    "display_",
    "fallback",
    "legacy_",
    "DEBUG",
    "debug",
    "ranking_df",
    "tmp[",
    "sort_cols",
    "available_cols",
    "if ",
    "in ",
    "columns",
    "_snapshot_numeric",
    "_tm69_numeric",
]

violations = []

for i, line in enumerate(lines, start=1):
    stripped = line.strip()

    if stripped.startswith("#"):
        continue

    for pattern in legacy_patterns:
        if re.search(pattern, stripped):
            if not any(token in stripped for token in allowed_context):
                violations.append((i, stripped))

print("TM.8.3 SCORING GOVERNANCE AUDIT")
print("=" * 80)

if violations:
    print("Potential legacy scoring reads:")
    for line_no, content in violations[:160]:
        print(f"{line_no}: {content}")
    print()
    raise SystemExit(f"FAIL: {len(violations)} potential scoring legacy reads remain")

print("OK — TM.8.3 Scoring Governance closed")
