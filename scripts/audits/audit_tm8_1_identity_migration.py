from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[2]
APP = ROOT / "app" / "streamlit_app.py"

text = APP.read_text(encoding="utf-8", errors="ignore")
lines = text.splitlines()

legacy_patterns = [
    r'safe_get\(row,\s*"club"',
    r'safe_get\(row,\s*"league"',
    r'safe_get\(row,\s*"position"',
    r'safe_get\(row,\s*"position_group"',
    r'safe_get\(row,\s*"nationality"',
    r'safe_get\(row,\s*"market_value_eur"',
    r'get_numeric_value\(row,\s*"age"',
    r'get_numeric_value\(row,\s*"market_value_eur"',
]

allowed_context = [
    "tm7_value(",
    "display_",
    "fallback",
    "legacy_",
    "DEBUG",
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

print("TM.8.1 IDENTITY MIGRATION AUDIT")
print("=" * 80)

if violations:
    print("Potential legacy identity reads:")
    for line_no, content in violations[:80]:
        print(f"{line_no}: {content}")
    print()
    raise SystemExit(f"FAIL: {len(violations)} potential identity legacy reads remain")

print("OK — TM.8.1 Identity Migration closed")
