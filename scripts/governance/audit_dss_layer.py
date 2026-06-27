from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

from src.dss.dss_metrics import load_dss_metrics_layer, build_dss_lookup

df = load_dss_metrics_layer()
lookup = build_dss_lookup(df)

print("=" * 100)
print("TM.7.3 DSS METRICS AUTHORITY")
print("=" * 100)
print(f"Rows: {len(df):,}")
print(f"Players: {len(lookup):,}")

for pid in [1390649, 974982]:
    print()
    print(pid)
    print(lookup.get(str(pid)))
