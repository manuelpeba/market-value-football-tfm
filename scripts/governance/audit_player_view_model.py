from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

import pandas as pd

from src.dss.identity import build_identity_lookup
from src.dss.performance import build_performance_lookup
from src.dss.player_service import get_player_view

IDENTITY = ROOT / "data" / "processed" / "player_identity_current.parquet"
MODELING = ROOT / "data" / "processed" / "player_season_modeling_v13a.parquet"
OUT = ROOT / "reports" / "data_quality" / "tm7_player_view_model_audit.csv"


def main():
    identity = pd.read_parquet(IDENTITY)
    modeling = pd.read_parquet(MODELING)

    identity_lookup = build_identity_lookup(identity)
    performance_lookup = build_performance_lookup(modeling)

    sample = modeling[
        modeling["player_name_tm"].astype(str).str.contains("Diomande|Diomandé", case=False, na=False)
    ].copy()

    rows = []

    for _, row in sample.iterrows():
        player = get_player_view(row, identity_lookup, performance_lookup)
        rows.append({
            "player_id_tm": player.identity.player_id_tm,
            "name": player.identity.name,
            "identity_club": player.identity.club,
            "identity_league": player.identity.league,
            "identity_age": player.identity.age,
            "identity_market_value_eur": player.identity.market_value_eur,
            "identity_status": player.identity.quality_status,

            "performance_season": player.performance.season if player.performance else None,
            "performance_club": player.performance.club if player.performance else None,
            "performance_league": player.performance.league if player.performance else None,
            "performance_minutes": player.performance.minutes_played if player.performance else None,
            "performance_market_value_eur": player.performance.market_value_eur if player.performance else None,

            "analytics_modeling_club": player.analytics.modeling_club,
            "analytics_modeling_league": player.analytics.modeling_league,
            "analytics_modeling_age": player.analytics.modeling_age,
            "analytics_modeling_market_value_eur": player.analytics.modeling_market_value_eur,
        })

    audit = pd.DataFrame(rows)
    OUT.parent.mkdir(parents=True, exist_ok=True)
    audit.to_csv(OUT, index=False)

    print("=" * 120)
    print("TM.7.2 PLAYER VIEW AUDIT — IDENTITY + PERFORMANCE + DSS ANALYTICS")
    print("=" * 120)
    print(audit.to_string(index=False))
    print("=" * 120)
    print(f"Saved: {OUT}")


if __name__ == "__main__":
    main()
