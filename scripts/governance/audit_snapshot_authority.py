from pathlib import Path
import sys
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
SNAPSHOT = ROOT / "data" / "processed" / "current_player_snapshot.parquet"
IDENTITY = ROOT / "data" / "processed" / "player_identity_current.parquet"
OUT = ROOT / "reports" / "data_quality" / "tm7_snapshot_authority_audit.csv"

MIN_IDENTITY_OK_PCT = 99.0
MAX_MISSING_CLUB = 0
MAX_MISSING_LEAGUE = 0
MAX_MISSING_VALUE = 0

def fail(msg):
    print(f"[FAIL] {msg}")
    sys.exit(1)

def main():
    if not SNAPSHOT.exists():
        fail(f"Missing snapshot: {SNAPSHOT}")
    if not IDENTITY.exists():
        fail(f"Missing identity layer: {IDENTITY}")

    snap = pd.read_parquet(SNAPSHOT)
    identity = pd.read_parquet(IDENTITY)

    checks = {
        "snapshot_rows": len(snap),
        "identity_rows": len(identity),
        "identity_unique_players": identity["player_id_tm"].nunique(),
        "identity_duplicate_ids": int(identity["player_id_tm"].duplicated().sum()),
        "missing_current_club": int(identity["current_club"].isna().sum()),
        "missing_current_league": int(identity["current_league"].isna().sum()),
        "missing_current_age": int(identity["current_age"].isna().sum()),
        "missing_current_market_value": int(identity["current_market_value_eur"].isna().sum()),
        "identity_ok_pct": round(identity["identity_quality_status"].eq("OK").mean() * 100, 2),
    }

    OUT.parent.mkdir(parents=True, exist_ok=True)
    pd.DataFrame([checks]).to_csv(OUT, index=False)

    print("=" * 80)
    print("TM.7.0 SNAPSHOT AUTHORITY AUDIT")
    print("=" * 80)
    print(pd.DataFrame([checks]).to_string(index=False))
    print("=" * 80)

    if checks["identity_rows"] == 0:
        fail("Identity layer is empty")
    if checks["identity_duplicate_ids"] > 0:
        fail("Duplicate player_id_tm found in identity layer")
    if checks["missing_current_club"] > MAX_MISSING_CLUB:
        fail("Missing current_club above threshold")
    if checks["missing_current_league"] > MAX_MISSING_LEAGUE:
        fail("Missing current_league above threshold")
    if checks["missing_current_market_value"] > MAX_MISSING_VALUE:
        fail("Missing current_market_value_eur above threshold")
    if checks["identity_ok_pct"] < MIN_IDENTITY_OK_PCT:
        fail("identity_ok_pct below threshold")

    print("[OK] Snapshot Authority is valid")

if __name__ == "__main__":
    main()
