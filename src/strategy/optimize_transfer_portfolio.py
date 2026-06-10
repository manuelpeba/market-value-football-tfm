from pathlib import Path

import numpy as np
import pandas as pd
import pulp


ROOT = Path(__file__).resolve().parents[2]

INPUT_FILE = ROOT / "reports" / "strategy" / "transfer_portfolio_dataset.csv"
OUTPUT_DIR = ROOT / "reports" / "strategy"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

OUTPUT_FILE = OUTPUT_DIR / "optimized_transfer_portfolio.csv"


PLAYER_LEVEL_ORDER = {
    "Development Prospect": 1,
    "Rotation Profile": 2,
    "First Team Ready": 3,
    "Key Player Profile": 4,
    "Elite Target": 5,
}



SCENARIO_CONFIG = {
    "conservative": {
        "min_confidence": 75,
        "max_avg_risk_proxy": 25,
        "value_weight": 0.75,
        "roi_weight": 0.25,
    },
    "balanced": {
        "min_confidence": 60,
        "max_avg_risk_proxy": 40,
        "value_weight": 0.65,
        "roi_weight": 0.35,
    },
    "aggressive": {
        "min_confidence": 45,
        "max_avg_risk_proxy": 60,
        "value_weight": 0.50,
        "roi_weight": 0.50,
    },
}


def minmax(series: pd.Series) -> pd.Series:
    s = pd.to_numeric(series, errors="coerce")

    if s.dropna().empty:
        return pd.Series(0.0, index=s.index)

    if s.max() == s.min():
        return pd.Series(50.0, index=s.index)

    return 100 * (s - s.min()) / (s.max() - s.min())


def prepare_candidates(
    budget: float,
    positions_needed: list[str],
    scenario: str,
    minimum_player_level: str = "Development Prospect",
) -> pd.DataFrame:
    df = pd.read_csv(INPUT_FILE)

    if "expected_roi" not in df.columns:
        df["expected_roi"] = np.where(
            df["market_value_eur"] > 0,
            df["expected_upside"] / df["market_value_eur"],
            np.nan,
        )

    if "matching_confidence_norm" not in df.columns:
        df["matching_confidence_norm"] = df["matching_confidence"].clip(0, 1) * 100

    if "player_level_tier" not in df.columns:
        df["player_level_tier"] = "Development Prospect"

    if "player_level_rank" not in df.columns:
        df["player_level_rank"] = df["player_level_tier"].map(PLAYER_LEVEL_ORDER)

    numeric_cols = [
        "portfolio_cost",
        "portfolio_value_score",
        "expected_upside",
        "expected_roi",
        "matching_confidence_norm",
        "player_level_rank",
    ]

    for col in numeric_cols:
        df[col] = pd.to_numeric(df[col], errors="coerce")

    candidates = df[df["is_eligible_portfolio"] == True].copy()
    candidates = candidates[candidates["portfolio_cost"] <= budget].copy()

    if positions_needed:
        candidates = candidates[candidates["position_group"].isin(positions_needed)].copy()

    if minimum_player_level not in PLAYER_LEVEL_ORDER:
        raise ValueError(f"Invalid minimum player level: {minimum_player_level}")

    candidates = candidates[
        candidates["player_level_rank"] >= PLAYER_LEVEL_ORDER[minimum_player_level]
    ].copy()

    config = SCENARIO_CONFIG[scenario]

    candidates = candidates[
        candidates["matching_confidence_norm"] >= config["min_confidence"]
    ].copy()

    candidates["risk_proxy"] = 100 - candidates["matching_confidence_norm"]
    candidates["roi_score_norm"] = minmax(candidates["expected_roi"])

    candidates["optimization_score"] = (
        config["value_weight"] * candidates["portfolio_value_score"]
        + config["roi_weight"] * candidates["roi_score_norm"]
    )

    candidates = candidates.dropna(
        subset=[
            "portfolio_cost",
            "portfolio_value_score",
            "optimization_score",
            "expected_upside",
            "expected_roi",
            "risk_proxy",
        ]
    ).copy()

    candidates = candidates.reset_index(drop=True)

    if candidates.empty:
        raise ValueError("No eligible candidates found under current constraints.")

    return candidates


def optimize_portfolio(
    budget: float,
    positions_needed: list[str],
    scenario: str = "balanced",
    max_signings: int = 5,
    min_budget_utilization: float = 0.70,
    minimum_player_level: str = "Development Prospect",
) -> pd.DataFrame:
    if scenario not in SCENARIO_CONFIG:
        raise ValueError(f"Invalid scenario: {scenario}")

    candidates = prepare_candidates(
        budget=budget,
        positions_needed=positions_needed,
        scenario=scenario,
        minimum_player_level=minimum_player_level,
    )

    config = SCENARIO_CONFIG[scenario]

    minimum_budget = budget * min_budget_utilization

    model = pulp.LpProblem(
        name="transfer_portfolio_optimization",
        sense=pulp.LpMaximize,
    )

    x = {
        i: pulp.LpVariable(f"x_{i}", cat="Binary")
        for i in candidates.index
    }

    # Objective function
    model += pulp.lpSum(
        candidates.loc[i, "optimization_score"] * x[i]
        for i in candidates.index
    )

    # Budget constraint
    model += pulp.lpSum(
        candidates.loc[i, "portfolio_cost"] * x[i]
        for i in candidates.index
    ) <= budget

    # Minimum budget utilization constraint 
    model += pulp.lpSum(
        candidates.loc[i, "portfolio_cost"] * x[i]
        for i in candidates.index
    ) >= minimum_budget

    # Max signings constraint
    model += pulp.lpSum(
        x[i] for i in candidates.index
    ) <= max_signings

    # At least one signing if feasible
    model += pulp.lpSum(
        x[i] for i in candidates.index
    ) >= 1

    # Average risk constraint:
    # sum(risk_i * x_i) <= max_avg_risk * sum(x_i)
    model += pulp.lpSum(
        candidates.loc[i, "risk_proxy"] * x[i]
        for i in candidates.index
    ) <= config["max_avg_risk_proxy"] * pulp.lpSum(
        x[i] for i in candidates.index
    )

    # Positional coverage:
    # If positions are requested, try to cover each requested position.
    # This only applies when max_signings allows it.
    unique_positions = list(dict.fromkeys(positions_needed))

    if unique_positions and max_signings >= len(unique_positions):
        for pos in unique_positions:
            available_pos = candidates[candidates["position_group"] == pos]

            if not available_pos.empty:
                model += pulp.lpSum(
                    x[i] for i in available_pos.index
                ) >= 1

    solver = pulp.PULP_CBC_CMD(msg=False)
    model.solve(solver)

    status = pulp.LpStatus[model.status]

    if status != "Optimal":
        raise ValueError(f"No optimal solution found. Solver status: {status}")

    selected_idx = [
        i for i in candidates.index
        if pulp.value(x[i]) == 1
    ]

    portfolio = candidates.loc[selected_idx].copy()

    portfolio["scenario"] = scenario
    portfolio["budget"] = budget
    portfolio["max_signings"] = max_signings
    portfolio["minimum_player_level"] = minimum_player_level
    portfolio["solver_status"] = status

    portfolio["budget_utilization"] = (
        portfolio["portfolio_cost"].sum() / budget
    )

    portfolio = portfolio.sort_values(
        "optimization_score",
        ascending=False,
    )

    portfolio.to_csv(OUTPUT_FILE, index=False)

    return portfolio


def print_summary(portfolio: pd.DataFrame) -> None:
    total_cost = portfolio["portfolio_cost"].sum()
    expected_upside = portfolio["expected_upside"].sum()
    expected_roi = expected_upside / total_cost if total_cost > 0 else np.nan
    budget = portfolio["budget"].iloc[0]

    budget_utilization = (
        portfolio["portfolio_cost"].sum() / budget
        )

    print("\nOPTIMIZED TRANSFER PORTFOLIO")
    print("-" * 45)
    print(f"Scenario: {portfolio['scenario'].iloc[0]}")
    if "minimum_player_level" in portfolio.columns:
        print(f"Minimum player level: {portfolio['minimum_player_level'].iloc[0]}")
    print(f"Players selected: {len(portfolio)}")
    print(f"Total cost: €{total_cost:,.0f}")
    print(f"Expected upside: €{expected_upside:,.0f}")
    print(f"Expected ROI: {expected_roi:.2%}")
    print(f"Average portfolio score: {portfolio['portfolio_value_score'].mean():.2f}")
    print(f"Average optimization score: {portfolio['optimization_score'].mean():.2f}")
    print(f"Average confidence: {portfolio['matching_confidence_norm'].mean():.2f}")
    print(f"Average risk proxy: {portfolio['risk_proxy'].mean():.2f}")
    print(f"Budget utilization: {budget_utilization:.2%}")

    print("\nRECOMMENDED PORTFOLIO")
    print(
        portfolio[
            [
                "player_name_fbref",
                "club",
                "position_group",
                "player_level_tier",
                "market_value_eur",
                "expected_upside",
                "expected_roi",
                "portfolio_value_score",
                "optimization_score",
            ]
        ].to_string(index=False)
    )

    print(f"\nSaved: {OUTPUT_FILE}")


if __name__ == "__main__":
    portfolio = optimize_portfolio(
        budget=30_000_000,
        positions_needed=["DEF", "MID", "ATT"],
        scenario="balanced",
        max_signings=5,
    )

    print_summary(portfolio)