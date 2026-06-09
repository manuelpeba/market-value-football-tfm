from pathlib import Path
from time import perf_counter

import numpy as np
import pandas as pd

from optimize_transfer_portfolio import optimize_portfolio


ROOT = Path(__file__).resolve().parents[2]

OUTPUT_DIR = ROOT / "reports" / "strategy"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

GRID_OUTPUT_FILE = OUTPUT_DIR / "scenario_grid.csv"
GRID_PORTFOLIOS_FILE = OUTPUT_DIR / "scenario_grid_portfolios.csv"


BUDGETS = [
    10_000_000,
    20_000_000,
    30_000_000,
    50_000_000,
    75_000_000,
    100_000_000,
]

SCENARIOS = [
    "conservative",
    "balanced",
    "aggressive",
]

POSITIONS_NEEDED = ["DEF", "MID", "ATT"]

MAX_SIGNINGS_BY_BUDGET = {
    10_000_000: 4,
    20_000_000: 5,
    30_000_000: 5,
    50_000_000: 6,
    75_000_000: 7,
    100_000_000: 8,
}


def summarize_portfolio(
    portfolio: pd.DataFrame,
    budget: int,
    scenario: str,
    elapsed_seconds: float,
) -> dict:
    total_cost = portfolio["portfolio_cost"].sum()
    expected_upside = portfolio["expected_upside"].sum()
    expected_roi = expected_upside / total_cost if total_cost > 0 else np.nan

    return {
        "scenario": scenario,
        "budget": budget,
        "max_signings": MAX_SIGNINGS_BY_BUDGET[budget],
        "players_selected": len(portfolio),
        "total_cost": total_cost,
        "budget_utilization": total_cost / budget,
        "expected_upside": expected_upside,
        "expected_roi": expected_roi,
        "avg_portfolio_score": portfolio["portfolio_value_score"].mean(),
        "avg_optimization_score": portfolio["optimization_score"].mean(),
        "avg_confidence": portfolio["matching_confidence_norm"].mean(),
        "avg_risk_proxy": portfolio["risk_proxy"].mean(),
        "solver_status": portfolio["solver_status"].iloc[0],
        "elapsed_seconds": elapsed_seconds,
        "selected_players": " | ".join(portfolio["player_name_fbref"].tolist()),
        "error": "",
    }


def main() -> None:
    rows = []
    portfolios = []

    for scenario in SCENARIOS:
        for budget in BUDGETS:
            max_signings = MAX_SIGNINGS_BY_BUDGET[budget]

            print(
                f"\nRunning scenario={scenario} "
                f"budget=€{budget:,.0f} "
                f"max_signings={max_signings}"
            )

            start = perf_counter()

            try:
                portfolio = optimize_portfolio(
                    budget=budget,
                    positions_needed=POSITIONS_NEEDED,
                    scenario=scenario,
                    max_signings=max_signings,
                    min_budget_utilization=0.70,
                )

                elapsed = perf_counter() - start

                portfolio = portfolio.copy()
                portfolio["grid_scenario"] = scenario
                portfolio["grid_budget"] = budget
                portfolio["grid_elapsed_seconds"] = elapsed

                rows.append(
                    summarize_portfolio(
                        portfolio=portfolio,
                        budget=budget,
                        scenario=scenario,
                        elapsed_seconds=elapsed,
                    )
                )

                portfolios.append(portfolio)

                print(f"OK | elapsed={elapsed:.2f}s")

            except Exception as exc:
                elapsed = perf_counter() - start

                rows.append(
                    {
                        "scenario": scenario,
                        "budget": budget,
                        "max_signings": max_signings,
                        "players_selected": 0,
                        "total_cost": np.nan,
                        "budget_utilization": np.nan,
                        "expected_upside": np.nan,
                        "expected_roi": np.nan,
                        "avg_portfolio_score": np.nan,
                        "avg_optimization_score": np.nan,
                        "avg_confidence": np.nan,
                        "avg_risk_proxy": np.nan,
                        "solver_status": "FAILED",
                        "elapsed_seconds": elapsed,
                        "selected_players": "",
                        "error": str(exc),
                    }
                )

                print(f"FAILED | elapsed={elapsed:.2f}s | {exc}")

    grid = pd.DataFrame(rows)
    grid.to_csv(GRID_OUTPUT_FILE, index=False)

    if portfolios:
        all_portfolios = pd.concat(portfolios, ignore_index=True)
        all_portfolios.to_csv(GRID_PORTFOLIOS_FILE, index=False)

    print(f"\nSaved: {GRID_OUTPUT_FILE}")
    print(f"Saved: {GRID_PORTFOLIOS_FILE}")

    print("\nSCENARIO GRID")
    print(
        grid[
            [
                "scenario",
                "budget",
                "players_selected",
                "total_cost",
                "budget_utilization",
                "expected_upside",
                "expected_roi",
                "avg_portfolio_score",
                "avg_confidence",
                "avg_risk_proxy",
                "solver_status",
                "elapsed_seconds",
                "error",
            ]
        ].to_string(index=False)
    )

    print("\nVALIDATION SUMMARY")
    print("-" * 50)
    print(f"Runs: {len(grid)}")
    print(f"Successful runs: {(grid['solver_status'] == 'Optimal').sum()}")
    print(f"Failed runs: {(grid['solver_status'] != 'Optimal').sum()}")
    print(f"Max elapsed seconds: {grid['elapsed_seconds'].max():.2f}")
    print(f"Mean elapsed seconds: {grid['elapsed_seconds'].mean():.2f}")


if __name__ == "__main__":
    main()