from pathlib import Path
import json
import numpy as np
import pandas as pd


ROOT = Path(__file__).resolve().parents[2]

INPUT_PATH = ROOT / "reports" / "rankings" / "scouting_shortlist_with_risk.csv"
OUTPUT_DIR = ROOT / "reports" / "portfolio"

OUTPUT_CSV = OUTPUT_DIR / "portfolio_candidates.csv"
OUTPUT_PARQUET = OUTPUT_DIR / "portfolio_candidates.parquet"
SUMMARY_CSV = OUTPUT_DIR / "portfolio_dataset_summary.csv"
METADATA_JSON = OUTPUT_DIR / "portfolio_dataset_metadata.json"


def minmax_score(series: pd.Series) -> pd.Series:
    s = pd.to_numeric(series, errors="coerce")
    if s.notna().sum() == 0:
        return pd.Series(50.0, index=series.index)
    min_v, max_v = s.min(), s.max()
    if min_v == max_v:
        return pd.Series(50.0, index=series.index)
    return ((s - min_v) / (max_v - min_v) * 100).clip(0, 100)


def build_portfolio_dataset() -> pd.DataFrame:
    if not INPUT_PATH.exists():
        raise FileNotFoundError(f"Input file not found: {INPUT_PATH}")

    df = pd.read_csv(INPUT_PATH).copy()

    required = [
        "player_name_fbref",
        "club",
        "league",
        "season",
        "position_group",
        "age",
        "minutes_played",
        "market_value_eur",
        "market_value_gap_eur",
        "market_value_gap_pct",
        "growth_score",
        "confidence_score",
        "opportunity_score",
        "risk_score",
        "risk_level",
        "risk_adjusted_opportunity_score",
    ]

    missing = [c for c in required if c not in df.columns]
    if missing:
        raise ValueError(f"Missing required columns: {missing}")

    numeric_cols = [
        "age",
        "minutes_played",
        "market_value_eur",
        "market_value_gap_eur",
        "market_value_gap_pct",
        "growth_score",
        "confidence_score",
        "opportunity_score",
        "risk_score",
        "risk_adjusted_opportunity_score",
    ]

    for col in numeric_cols:
        df[col] = pd.to_numeric(df[col], errors="coerce")

    df = df.dropna(subset=[
        "market_value_eur",
        "opportunity_score",
        "risk_score",
        "confidence_score",
        "growth_score",
    ])

    df = df[df["market_value_eur"] > 0].copy()

    df["portfolio_cost_eur"] = df["market_value_eur"]

    # Proxy ROI based on current mispricing gap.
    df["roi_proxy_pct"] = (
        df["market_value_gap_eur"] / df["market_value_eur"] * 100
    ).replace([np.inf, -np.inf], np.nan)

    df["roi_score"] = minmax_score(df["roi_proxy_pct"])

    df["upside_eur"] = df["market_value_gap_eur"].clip(lower=0)
    df["upside_score"] = minmax_score(df["upside_eur"])

    df["future_asset_score"] = (
        0.35 * df["roi_score"]
        + 0.25 * df["upside_score"]
        + 0.20 * df["opportunity_score"]
        + 0.10 * df["confidence_score"]
        + 0.10 * (100 - df["risk_score"])
    ).clip(0, 100)

    df["executive_decision_score"] = (
        0.30 * df["risk_adjusted_opportunity_score"]
        + 0.25 * df["future_asset_score"]
        + 0.20 * df["opportunity_score"]
        + 0.15 * df["confidence_score"]
        - 0.10 * df["risk_score"]
    ).clip(0, 100)

    df["portfolio_score_conservative"] = (
        0.35 * df["confidence_score"]
        + 0.25 * df["executive_decision_score"]
        + 0.20 * df["opportunity_score"]
        - 0.30 * df["risk_score"]
    )

    df["portfolio_score_balanced"] = (
        0.30 * df["opportunity_score"]
        + 0.25 * df["future_asset_score"]
        + 0.20 * df["roi_score"]
        + 0.15 * df["confidence_score"]
        - 0.20 * df["risk_score"]
    )

    df["portfolio_score_aggressive"] = (
        0.35 * df["future_asset_score"]
        + 0.30 * df["growth_score"]
        + 0.25 * df["roi_score"]
        - 0.10 * df["risk_score"]
    )

    df["is_optimization_candidate"] = (
        df["portfolio_cost_eur"].notna()
        & df["position_group"].isin(["GK", "DEF", "MID", "ATT"])
        & df["opportunity_score"].notna()
        & df["risk_score"].notna()
    )

    output_cols = [
        "player_name_fbref",
        "player_name_tm",
        "club",
        "league",
        "season",
        "position_group",
        "age",
        "minutes_played",
        "market_value_eur",
        "portfolio_cost_eur",
        "predicted_market_value_eur",
        "market_value_gap_eur",
        "market_value_gap_pct",
        "roi_proxy_pct",
        "roi_score",
        "upside_eur",
        "upside_score",
        "growth_score",
        "confidence_score",
        "opportunity_score",
        "risk_score",
        "risk_level",
        "risk_adjusted_opportunity_score",
        "future_asset_score",
        "executive_decision_score",
        "portfolio_score_conservative",
        "portfolio_score_balanced",
        "portfolio_score_aggressive",
        "is_optimization_candidate",
    ]

    existing_cols = [c for c in output_cols if c in df.columns]
    return df[existing_cols].sort_values(
        "portfolio_score_balanced", ascending=False
    )


def main() -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    portfolio_df = build_portfolio_dataset()

    portfolio_df.to_csv(OUTPUT_CSV, index=False)
    portfolio_df.to_parquet(OUTPUT_PARQUET, index=False)

    summary = pd.DataFrame({
        "metric": [
            "rows",
            "optimization_candidates",
            "avg_market_value_eur",
            "avg_opportunity_score",
            "avg_risk_score",
            "avg_future_asset_score",
            "avg_balanced_portfolio_score",
        ],
        "value": [
            len(portfolio_df),
            int(portfolio_df["is_optimization_candidate"].sum()),
            portfolio_df["market_value_eur"].mean(),
            portfolio_df["opportunity_score"].mean(),
            portfolio_df["risk_score"].mean(),
            portfolio_df["future_asset_score"].mean(),
            portfolio_df["portfolio_score_balanced"].mean(),
        ],
    })

    summary.to_csv(SUMMARY_CSV, index=False)

    metadata = {
        "sprint": "Sprint 14.1",
        "component": "Transfer Strategy Engine - Portfolio Dataset",
        "input": str(INPUT_PATH.relative_to(ROOT)),
        "outputs": [
            str(OUTPUT_CSV.relative_to(ROOT)),
            str(OUTPUT_PARQUET.relative_to(ROOT)),
            str(SUMMARY_CSV.relative_to(ROOT)),
        ],
        "rows": int(len(portfolio_df)),
        "optimization_candidates": int(portfolio_df["is_optimization_candidate"].sum()),
    }

    METADATA_JSON.write_text(json.dumps(metadata, indent=2), encoding="utf-8")

    print("Portfolio dataset created successfully.")
    print(f"Rows: {len(portfolio_df)}")
    print(f"Optimization candidates: {portfolio_df['is_optimization_candidate'].sum()}")
    print(f"Saved to: {OUTPUT_CSV}")


if __name__ == "__main__":
    main()
