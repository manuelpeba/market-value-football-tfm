from pathlib import Path
import pandas as pd

ROOT = Path(".")
FILES = {
    "dss": ROOT / "reports/dss/global_prospect_universe.csv",
    "portfolio": ROOT / "reports/strategy/transfer_portfolio_dataset.csv",
    "contract": ROOT / "reports/tm3_contract_intelligence/contract_intelligence_dataset.csv",
    "snapshot": ROOT / "data/processed/current_player_snapshot.csv",
}

TARGETS = [
    "Endrick",
    "Lucas Gourna-Douath",
    "Jesus Rodríguez",
    "Jesús Rodríguez",
    "Yan Diomandé",
    "Yan Diomande",
    "Diego Coppola",
]

def load(path):
    return pd.read_csv(path, low_memory=False) if path.suffix == ".csv" else pd.read_parquet(path)

for name, path in FILES.items():
    if not path.exists():
        print("MISSING", name, path)
        continue

    df = load(path)
    print("\n" + "="*120)
    print(name, path, "rows", len(df), "cols", len(df.columns))

    name_cols = [c for c in df.columns if "player_name" in c.lower() or c.lower() in {"name", "player"}]
    context_cols = [
        c for c in [
            "player_id_tm",
            "player_name_fbref",
            "player_name_tm",
            "club",
            "club_actual",
            "season_context_club",
            "current_club",
            "current_club_name_tm",
            "current_club_snapshot",
            "display_club",
            "league",
            "season_context_league",
            "current_league",
            "current_league_snapshot",
            "display_league",
            "market_value_eur",
            "season_context_market_value_eur",
            "current_market_value_eur",
            "current_market_value_eur_snapshot",
            "predicted_market_value_eur",
            "market_value_gap_eur",
            "market_value_gap_pct",
        ] if c in df.columns
    ]

    for target in TARGETS:
        mask = pd.Series(False, index=df.index)
        for c in name_cols:
            mask |= df[c].astype(str).str.contains(target, case=False, regex=False, na=False)

        hit = df[mask]
        if hit.empty:
            continue

        print(f"\nTARGET {target}: rows={len(hit)}")
        print(hit[context_cols].head(15).to_string(index=False))

    if {"display_club", "display_league", "club", "league"}.issubset(df.columns):
        leaks = df[
            df["display_club"].notna()
            & df["display_league"].notna()
            & df["club"].notna()
            & df["league"].notna()
            & (
                (df["display_club"].astype(str) != df["club"].astype(str))
                | (df["display_league"].astype(str) != df["league"].astype(str))
            )
        ].copy()
        print("\nCONTEXT_MISMATCH_ROWS:", len(leaks))
        cols = [c for c in context_cols if c in leaks.columns]
        print(leaks[cols].head(20).to_string(index=False))
