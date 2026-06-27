from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[2]

targets = ["app", "src", "scripts"]
patterns = [
    "from src.dss.view_models",
    "import src.dss.view_models",
    "view_models import",
]

violations = []

for target in targets:
    path = ROOT / target
    if not path.exists():
        continue

    for file in path.rglob("*.py"):
        if file.name == "view_models.py":
            continue
        text = file.read_text(encoding="utf-8", errors="ignore")
        for pattern in patterns:
            if pattern in text:
                violations.append((str(file.relative_to(ROOT)), pattern))

print("TM.7.6 LEGACY DECOMMISSION AUDIT")
print("=" * 80)

if violations:
    print("Legacy imports found:")
    for file, pattern in violations:
        print(f"- {file}: {pattern}")
    raise SystemExit("FAIL: legacy view_models imports remain")

print("OK — no active imports of src.dss.view_models")
print("OK — TM.7.6 Legacy Decommission closed")
