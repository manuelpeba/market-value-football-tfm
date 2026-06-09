from pathlib import Path

import numpy as np
import pandas as pd

from optimize_transfer_portfolio import optimize_portfolio


ROOT = Path(__file__).resolve().parents[2]

OUTPUT_DIR = ROOT / "reports" / "strategy"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

SCENARIO_OUTPUT_FILE = OUTPUT_DIR / "scenario_comparison.csv"
PORTFOLIO_OUTPUT_FILE = OUTPUT_DIR / "scenario_portfolios.csv"


SCENARIOS = [
    {
        "scenario": "conservative",
        "budget": 10_000_000,
        "positions_needed": ["DEF", "MID", "ATT"],
        "max_signings": 4,
        "min_budget_utilization": 0.70,
    },
    {
        "scenario": "balanced",
        "budget": 30_000_000,
        "positions_needed": ["DEF", "MID", "ATT"],
        "max_signings": 5,
        "min_budget_utilization": 0.70,
    },
    {
        "scenario": "aggressive",
        "budget": 50_000_000,
        "positions_needed": ["DEF", "MID", "ATT"],
        "max_signings": 6,
        "min_budget_utilization": 0.70,
    },
]


def summarize_portfolio(portfolio: pd.DataFrame, params: dict) -> dict:
    total_cost = portfolio["portfolio_cost"].sum()
    expected_upside = portfolio["expected_upside"].sum()
    expected_roi = expected_upside / total_cost if total_cost > 0 else np.nan

    return {
        "scenario": params["scenario"],
        "budget": params["budget"],
        "max_signings": params["max_signings"],
        "positions_needed": ",".join(params["positions_needed"]),
        "players_selected": len(portfolio),
        "total_cost": total_cost,
        "budget_utilization": total_cost / params["budget"],
        "expected_upside": expected_upside,
        "expected_roi": expected_roi,
        "avg_portfolio_score": portfolio["portfolio_value_score"].mean(),
        "avg_optimization_score": portfolio["optimization_score"].mean(),
        "avg_confidence": portfolio["matching_confidence_norm"].mean(),
        "avg_risk_proxy": portfolio["risk_proxy"].mean(),
        "selected_players": " | ".join(portfolio["player_name_fbref"].tolist()),
    }


def main() -> None:
    summaries = []
    all_portfolios = []

    for params in SCENARIOS:
        print(
            f"\nRunning scenario={params['scenario']} "
            f"budget=€{params['budget']:,.0f}"
        )

        try:
            portfolio = optimize_portfolio(
                budget=params["budget"],
                positions_needed=params["positions_needed"],
                scenario=params["scenario"],
                max_signings=params["max_signings"],
                min_budget_utilization=params["min_budget_utilization"],
            )

            portfolio["scenario_run"] = params["scenario"]
            portfolio["scenario_budget"] = params["budget"]

            summaries.append(
                summarize_portfolio(
                    portfolio=portfolio,
                    params=params,
                )
            )

            all_portfolios.append(portfolio)

            print("OK")

        except Exception as exc:
            print(f"FAILED: {exc}")

            summaries.append(
                {
                    "scenario": params["scenario"],
                    "budget": params["budget"],
                    "max_signings": params["max_signings"],
                    "positions_needed": ",".join(params["positions_needed"]),
                    "players_selected": 0,
                    "total_cost": np.nan,
                    "budget_utilization": np.nan,
                    "expected_upside": np.nan,
                    "expected_roi": np.nan,
                    "avg_portfolio_score": np.nan,
                    "avg_optimization_score": np.nan,
                    "avg_confidence": np.nan,
                    "avg_risk_proxy": np.nan,
                    "selected_players": "",
                    "error": str(exc),
                }
            )

    scenario_comparison = pd.DataFrame(summaries)
    scenario_comparison.to_csv(SCENARIO_OUTPUT_FILE, index=False)

    if all_portfolios:
        scenario_portfolios = pd.concat(all_portfolios, ignore_index=True)
        scenario_portfolios.to_csv(PORTFOLIO_OUTPUT_FILE, index=False)

    print(f"\nSaved: {SCENARIO_OUTPUT_FILE}")
    print(f"Saved: {PORTFOLIO_OUTPUT_FILE}")

    print("\nSCENARIO COMPARISON")
    print(
        scenario_comparison[
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
            ]
        ].to_string(index=False)
    )


if __name__ == "__main__":
    main()