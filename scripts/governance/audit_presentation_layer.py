from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

import pandas as pd

from src.dss.presentation import build_presentation_df

MODELING = ROOT / "data" / "processed" / "player_season_modeling_v13a.parquet"
OUT = ROOT / "reports" / "data_quality" / "tm7_presentation_layer_audit.csv"


def main():
    df = pd.read_parquet(MODELING)

    sample = df[
        df["player_name_tm"].astype(str).str.contains("Yan Diomande|Yan Diomandé", case=False, na=False)
    ].copy()

    presentation = build_presentation_df(sample)

    cols = [
        "player_id_tm",
        "player_name_tm",
        "season",
        "club",
        "league",
        "market_value_eur",
        "minutes_played",
        "display_club",
        "display_league",
        "display_age",
        "display_market_value_eur",
        "display_performance_season",
        "display_performance_club",
        "display_performance_league",
        "display_minutes_played",
        "display_performance_market_value_eur",
        "display_dss_season",
        "display_dss_modeling_club",
        "display_dss_modeling_league",
        "display_dss_modeling_market_value_eur",
        "display_dss_opportunity_score",
        "display_dss_confidence_score",
        "display_dss_risk_score",
        "display_dss_roi_3y_pct",
    ]
    cols = [c for c in cols if c in presentation.columns]

    OUT.parent.mkdir(parents=True, exist_ok=True)
    presentation[cols].to_csv(OUT, index=False)

    print("=" * 140)
    print("TM.7.2 PRESENTATION LAYER AUDIT")
    print("=" * 140)
    print(presentation[cols].to_string(index=False))
    print("=" * 140)
    print(f"Saved: {OUT}")


if __name__ == "__main__":
    main()
