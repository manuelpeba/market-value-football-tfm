from pathlib import Path
import argparse
import json
import pandas as pd

from optimize_transfer_strategy import optimize_transfer_strategy


ROOT = Path(__file__).resolve().parents[2]

OUTPUT_DIR = ROOT / "reports" / "portfolio" / "scenarios"
SUMMARY_PATH = OUTPUT_DIR / "scenario_simulation_summary.csv"
METADATA_PATH = OUTPUT_DIR / "scenario_simulation_metadata.json"

RISK_PROFILES = ["conservative", "balanced", "aggressive"]


def simulate_transfer_scenarios(
    budget_millions: float,
    positions_needed: list[str],
    max_players: int = 5,
) -> tuple[pd.DataFrame, dict]:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    summaries = []
    metadata = {
        "sprint": "Sprint 14.3",
        "component": "Transfer Strategy Engine - Scenario Simulator",
        "budget_millions": budget_millions,
        "positions_needed": positions_needed,
        "max_players": max_players,
        "scenarios": {},
    }

    for risk_profile in RISK_PROFILES:
        selected, summary = optimize_transfer_strategy(
            budget_millions=budget_millions,
            positions_needed=positions_needed,
            risk_profile=risk_profile,
            max_players=max_players,
        )

        portfolio_path = OUTPUT_DIR / f"recommended_portfolio_{risk_profile}.csv"
        summary_path = OUTPUT_DIR / f"recommended_portfolio_{risk_profile}_summary.json"

        selected.to_csv(portfolio_path, index=False)
        summary_path.write_text(json.dumps(summary, indent=2), encoding="utf-8")

        selected_players = (
            "; ".join(selected["player_name_fbref"].astype(str).tolist())
            if not selected.empty
            else ""
        )

        summaries.append({
            "scenario": risk_profile,
            "status": summary.get("status"),
            "selected_players_n": summary.get("selected_players"),
            "selected_players": selected_players,
            "budget_millions": summary.get("budget_millions"),
            "total_cost_eur": summary.get("total_cost_eur"),
            "budget_used_pct": summary.get("budget_used_pct"),
            "expected_upside_eur": summary.get("expected_upside_eur"),
            "expected_roi_score": summary.get("expected_roi_score"),
            "average_risk": summary.get("average_risk"),
            "average_confidence": summary.get("average_confidence"),
            "average_future_asset_score": summary.get("average_future_asset_score"),
            "objective_value": summary.get("objective_value"),
            "portfolio_output": str(portfolio_path.relative_to(ROOT)),
            "summary_output": str(summary_path.relative_to(ROOT)),
        })

        metadata["scenarios"][risk_profile] = {
            "portfolio_output": str(portfolio_path.relative_to(ROOT)),
            "summary_output": str(summary_path.relative_to(ROOT)),
            "status": summary.get("status"),
            "selected_players": summary.get("selected_players"),
            "total_cost_eur": summary.get("total_cost_eur"),
            "budget_used_pct": summary.get("budget_used_pct"),
            "expected_upside_eur": summary.get("expected_upside_eur"),
            "average_risk": summary.get("average_risk"),
            "average_confidence": summary.get("average_confidence"),
        }

    summary_df = pd.DataFrame(summaries)
    summary_df.to_csv(SUMMARY_PATH, index=False)
    METADATA_PATH.write_text(json.dumps(metadata, indent=2), encoding="utf-8")

    return summary_df, metadata


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Sprint 14.3 - Transfer Strategy Scenario Simulator"
    )
    parser.add_argument("--budget", type=float, default=40, help="Budget in millions of euros.")
    parser.add_argument("--positions", type=str, default="DEF,MID", help="Comma-separated position groups: GK,DEF,MID,ATT.")
    parser.add_argument("--max-players", type=int, default=5)

    args = parser.parse_args()

    positions = [p.strip().upper() for p in args.positions.split(",") if p.strip()]

    summary_df, metadata = simulate_transfer_scenarios(
        budget_millions=args.budget,
        positions_needed=positions,
        max_players=args.max_players,
    )

    print("Scenario simulation completed.")
    print(f"Saved summary to: {SUMMARY_PATH}")
    print(f"Saved metadata to: {METADATA_PATH}")
    print()
    print(summary_df[[
        "scenario",
        "status",
        "selected_players_n",
        "total_cost_eur",
        "budget_used_pct",
        "expected_roi_score",
        "expected_upside_eur",
        "average_risk",
        "average_confidence",
        "average_future_asset_score",
    ]].to_string(index=False))


if __name__ == "__main__":
    main()
