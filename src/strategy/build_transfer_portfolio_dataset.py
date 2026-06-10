from pathlib import Path

import numpy as np
import pandas as pd


ROOT = Path(__file__).resolve().parents[2]

INPUT_FILE = ROOT / "reports" / "rankings" / "scoring_dataset.csv"

OUTPUT_DIR = ROOT / "reports" / "strategy"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

OUTPUT_FILE = OUTPUT_DIR / "transfer_portfolio_dataset.csv"


PLAYER_LEVEL_ORDER = {
    "Development Prospect": 1,
    "Rotation Profile": 2,
    "First Team Ready": 3,
    "Key Player Profile": 4,
    "Elite Target": 5,
}


def classify_player_level(score: object) -> str:
    """Classify candidates into executive recruitment quality tiers.

    This is a post-model decision-support layer. It does not retrain the
    valuation model; it translates the portfolio value score into a minimum
    competitive-quality filter for recruitment planning.
    """
    value = pd.to_numeric(pd.Series([score]), errors="coerce").iloc[0]

    if pd.isna(value):
        return "Unclassified"
    if value >= 94:
        return "Elite Target"
    if value >= 88:
        return "Key Player Profile"
    if value >= 82:
        return "First Team Ready"
    if value >= 75:
        return "Rotation Profile"
    return "Development Prospect"


def player_level_rank(level: object) -> float:
    """Return ordered rank for player-level tiers."""
    return PLAYER_LEVEL_ORDER.get(str(level), np.nan)


def minmax(series: pd.Series) -> pd.Series:
    """Scale numeric series to 0-100. Constant series receive neutral score 50."""
    s = pd.to_numeric(series, errors="coerce")

    if s.dropna().empty:
        return pd.Series(np.nan, index=s.index)

    if s.max() == s.min():
        return pd.Series(50.0, index=s.index)

    return 100 * (s - s.min()) / (s.max() - s.min())


def build_portfolio_dataset() -> pd.DataFrame:
    df = pd.read_csv(INPUT_FILE)

    required_input_cols = [
        "player_name_fbref",
        "club",
        "league",
        "position",
        "position_group",
        "age",
        "market_value_eur",
        "predicted_market_value_eur",
        "market_value_gap_eur",
        "market_value_gap_pct",
        "inefficiency_score_z",
        "matching_confidence",
    ]

    missing_cols = [col for col in required_input_cols if col not in df.columns]
    if missing_cols:
        raise ValueError(f"Missing required input columns: {missing_cols}")

    portfolio = df.copy()

    numeric_cols = [
        "age",
        "market_value_eur",
        "predicted_market_value_eur",
        "market_value_gap_eur",
        "market_value_gap_pct",
        "inefficiency_score_z",
        "matching_confidence",
    ]

    for col in numeric_cols:
        portfolio[col] = pd.to_numeric(portfolio[col], errors="coerce")

    # --------------------------------------------------
    # Expected Upside and ROI
    # --------------------------------------------------

    portfolio["expected_upside"] = (
        portfolio["predicted_market_value_eur"]
        - portfolio["market_value_eur"]
    )

    portfolio["expected_roi"] = np.where(
        portfolio["market_value_eur"] > 0,
        portfolio["expected_upside"] / portfolio["market_value_eur"],
        np.nan,
    )

    # --------------------------------------------------
    # Normalized Components
    # --------------------------------------------------

    portfolio["inefficiency_score_norm"] = minmax(
        portfolio["inefficiency_score_z"]
    )

    portfolio["upside_score_norm"] = minmax(
        portfolio["expected_upside"]
    )

    portfolio["matching_confidence_norm"] = (
        portfolio["matching_confidence"].clip(lower=0, upper=1) * 100
    )

    # --------------------------------------------------
    # Age Potential
    # Peak value creation around 23
    # --------------------------------------------------

    portfolio["age_potential_score"] = (
        100 - abs(portfolio["age"] - 23) * 4
    ).clip(lower=0, upper=100)

    # --------------------------------------------------
    # Portfolio Value Score v1
    # --------------------------------------------------

    portfolio["portfolio_value_score"] = (
        0.50 * portfolio["inefficiency_score_norm"]
        + 0.25 * portfolio["upside_score_norm"]
        + 0.15 * portfolio["matching_confidence_norm"]
        + 0.10 * portfolio["age_potential_score"]
    )

    # --------------------------------------------------
    # Player Level Layer v1
    # --------------------------------------------------

    portfolio["player_level_tier"] = portfolio["portfolio_value_score"].apply(
        classify_player_level
    )
    portfolio["player_level_rank"] = portfolio["player_level_tier"].apply(
        player_level_rank
    )

    # --------------------------------------------------
    # Cost
    # --------------------------------------------------

    portfolio["portfolio_cost"] = portfolio["market_value_eur"]

    # --------------------------------------------------
    # Eligibility
    # --------------------------------------------------

    required_eligibility_cols = [
        "market_value_eur",
        "predicted_market_value_eur",
        "inefficiency_score_z",
        "matching_confidence",
        "position_group",
        "portfolio_value_score",
        "expected_upside",
        "expected_roi",
    ]

    portfolio["is_eligible_portfolio"] = (
        portfolio[required_eligibility_cols]
        .notna()
        .all(axis=1)
    )

    portfolio["is_eligible_portfolio"] &= portfolio["market_value_eur"] > 0

    # --------------------------------------------------
    # Output columns
    # --------------------------------------------------

    final_cols = [
        "player_name_fbref",
        "club",
        "league",
        "position",
        "position_group",
        "age",
        "market_value_eur",
        "predicted_market_value_eur",
        "market_value_gap_eur",
        "market_value_gap_pct",
        "inefficiency_score_z",
        "matching_confidence",
        "expected_upside",
        "expected_roi",
        "inefficiency_score_norm",
        "upside_score_norm",
        "matching_confidence_norm",
        "age_potential_score",
        "portfolio_value_score",
        "player_level_tier",
        "player_level_rank",
        "portfolio_cost",
        "is_eligible_portfolio",
    ]

    portfolio = portfolio[final_cols].sort_values(
        "portfolio_value_score",
        ascending=False,
    )

    portfolio.to_csv(OUTPUT_FILE, index=False)

    eligible_count = int(portfolio["is_eligible_portfolio"].sum())

    print(f"\nSaved: {OUTPUT_FILE}")
    print(f"Rows: {len(portfolio):,}")
    print(f"Eligible rows: {eligible_count:,}")

    return portfolio


if __name__ == "__main__":
    build_portfolio_dataset()