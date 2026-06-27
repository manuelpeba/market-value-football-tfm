from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[2]

if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.dss.performance import (
    load_performance_layer,
    build_performance_lookup,
)

perf = load_performance_layer()
lookup = build_performance_lookup(perf)

print("=" * 80)
print("TM.7.2 PERFORMANCE AUTHORITY")
print("=" * 80)

print(f"Rows: {len(perf):,}")
print(f"Players: {len(lookup):,}")

for pid in [1390649, 974982]:
    print()
    print(lookup.get(pid))