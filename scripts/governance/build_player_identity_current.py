from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
PROCESSED = ROOT / "data" / "processed"
SNAPSHOT = PROCESSED / "current_player_snapshot.parquet"
OUT = PROCESSED / "player_identity_current.parquet"
AUDIT = ROOT / "reports" / "data_quality" / "tm7_player_identity_current_audit.csv"

def first_existing(df, candidates):
    for c in candidates:
        if c in df.columns:
            return c
    return None

def main():
    if not SNAPSHOT.exists():
        raise FileNotFoundError(f"Missing snapshot: {SNAPSHOT}")

    df = pd.read_parquet(SNAPSHOT).copy()

    date_col = first_existing(df, ["valuation_date", "current_valuation_date"])
    position_col = first_existing(df, ["current_position", "position"])
    position_group_col = first_existing(df, ["current_position_group", "position_group"])

    required = [
        "player_id_tm",
        "player_name_tm",
        "current_club",
        "current_league",
        "current_age",
        "current_market_value_eur",
    ]

    missing = [c for c in required if c not in df.columns]
    if date_col is None:
        missing.append("valuation_date/current_valuation_date")

    if missing:
        raise ValueError(f"Missing required snapshot columns: {missing}")

    identity = pd.DataFrame({
        "player_id_tm": df["player_id_tm"],
        "player_name_display": df["player_name_tm"],
        "current_club": df["current_club"],
        "current_league": df["current_league"],
        "current_age": pd.to_numeric(df["current_age"], errors="coerce"),
        "current_market_value_eur": pd.to_numeric(df["current_market_value_eur"], errors="coerce"),
        "valuation_date": pd.to_datetime(df[date_col], errors="coerce"),
        "current_position": df[position_col] if position_col else pd.NA,
        "current_position_group": df[position_group_col] if position_group_col else pd.NA,
        "nationality": df["nationality"] if "nationality" in df.columns else pd.NA,
        "identity_source": df["snapshot_source"] if "snapshot_source" in df.columns else "current_player_snapshot",
        "identity_snapshot_version": "tm7.0",
    })

    identity["identity_quality_status"] = "OK"

    critical = [
        "player_id_tm",
        "player_name_display",
        "current_club",
        "current_league",
        "current_age",
        "current_market_value_eur",
        "valuation_date",
    ]

    for col in critical:
        bad = identity[col].isna() | (identity[col].astype(str).str.strip() == "")
        identity.loc[bad, "identity_quality_status"] = "INCOMPLETE"

    dupes = identity["player_id_tm"].duplicated(keep=False)
    identity.loc[dupes, "identity_quality_status"] = "DUPLICATE_PLAYER_ID"

    identity = (
        identity.sort_values(["player_id_tm", "valuation_date"], ascending=[True, False])
        .drop_duplicates("player_id_tm", keep="first")
        .reset_index(drop=True)
    )

    OUT.parent.mkdir(parents=True, exist_ok=True)
    AUDIT.parent.mkdir(parents=True, exist_ok=True)

    identity.to_parquet(OUT, index=False)

    audit = pd.DataFrame([{
        "rows": len(identity),
        "unique_players": identity["player_id_tm"].nunique(),
        "missing_club": int(identity["current_club"].isna().sum()),
        "missing_league": int(identity["current_league"].isna().sum()),
        "missing_age": int(identity["current_age"].isna().sum()),
        "missing_market_value": int(identity["current_market_value_eur"].isna().sum()),
        "missing_position": int(identity["current_position"].isna().sum()),
        "status_ok_pct": round(identity["identity_quality_status"].eq("OK").mean() * 100, 2),
        "output": str(OUT.relative_to(ROOT)),
    }])

    audit.to_csv(AUDIT, index=False)

    print("=" * 80)
    print("TM.7.0 PLAYER IDENTITY CURRENT BUILT")
    print("=" * 80)
    print(audit.to_string(index=False))
    print("=" * 80)
    print(f"Saved: {OUT}")
    print(f"Audit: {AUDIT}")

if __name__ == "__main__":
    main()
