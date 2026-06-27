from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[2]
APP = ROOT / "app" / "streamlit_app.py"

lines = APP.read_text(encoding="utf-8", errors="ignore").splitlines()

legacy_patterns = [
    r'safe_get\(row,\s*"minutes_played"',
    r'get_numeric_value\(row,\s*"minutes_played"',
    r'safe_get\(row,\s*"goals"',
    r'get_numeric_value\(row,\s*"goals"',
    r'safe_get\(row,\s*"assists"',
    r'get_numeric_value\(row,\s*"assists"',
    r'safe_get\(row,\s*"season"',
    r'safe_get\(row,\s*"valuation_date"',
]

allowed_context = [
    "tm7_value(",
    "display_",
    "fallback",
    "legacy_",
    "DEBUG",
    "role_",
    "_role",
    "season_col",
    "season_key",
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

print("TM.8.2 PERFORMANCE MIGRATION AUDIT")
print("=" * 80)

if violations:
    print("Potential legacy performance reads:")
    for line_no, content in violations[:120]:
        print(f"{line_no}: {content}")
    print()
    raise SystemExit(f"FAIL: {len(violations)} potential performance legacy reads remain")

print("OK — TM.8.2 Performance Migration closed")
