from pathlib import Path
import argparse
import json
import pandas as pd

try:
    import pulp
except ImportError as exc:
    raise ImportError(
        "PuLP is required for Sprint 14.2. Install it with: pip install pulp"
    ) from exc


ROOT = Path(__file__).resolve().parents[2]

INPUT_PATH = ROOT / "reports" / "portfolio" / "portfolio_candidates.csv"
OUTPUT_DIR = ROOT / "reports" / "portfolio"

OUTPUT_CSV = OUTPUT_DIR / "recommended_portfolio.csv"
OUTPUT_JSON = OUTPUT_DIR / "recommended_portfolio_summary.json"


SCORE_COLUMNS = {
    "conservative": "portfolio_score_conservative",
    "balanced": "portfolio_score_balanced",
    "aggressive": "portfolio_score_aggressive",
}


def optimize_transfer_strategy(
    budget_millions: float,
    positions_needed: list[str],
    risk_profile: str = "balanced",
    max_players: int = 5,
) -> tuple[pd.DataFrame, dict]:
    if risk_profile not in SCORE_COLUMNS:
        raise ValueError(f"Invalid risk_profile: {risk_profile}. Use conservative, balanced or aggressive.")

    if not INPUT_PATH.exists():
        raise FileNotFoundError(f"Missing portfolio dataset: {INPUT_PATH}")

    df = pd.read_csv(INPUT_PATH).copy()
    df = df[df["is_optimization_candidate"] == True].copy()

    score_col = SCORE_COLUMNS[risk_profile]
    required = [
        "player_name_fbref",
        "position_group",
        "portfolio_cost_eur",
        "opportunity_score",
        "risk_score",
        "confidence_score",
        "future_asset_score",
        "roi_score",
        "upside_eur",
        score_col,
    ]

    missing = [c for c in required if c not in df.columns]
    if missing:
        raise ValueError(f"Missing required columns: {missing}")

    for col in [
        "portfolio_cost_eur",
        "opportunity_score",
        "risk_score",
        "confidence_score",
        "future_asset_score",
        "roi_score",
        "upside_eur",
        score_col,
    ]:
        df[col] = pd.to_numeric(df[col], errors="coerce")

    df = df.dropna(subset=["portfolio_cost_eur", score_col, "position_group"])
    df = df[df["portfolio_cost_eur"] > 0].reset_index(drop=True)

    budget_eur = budget_millions * 1_000_000

    problem = pulp.LpProblem(
        name=f"transfer_strategy_{risk_profile}",
        sense=pulp.LpMaximize,
    )

    x = {
        i: pulp.LpVariable(name=f"x_{i}", cat="Binary")
        for i in df.index
    }

    problem += pulp.lpSum(df.loc[i, score_col] * x[i] for i in df.index)

    problem += pulp.lpSum(df.loc[i, "portfolio_cost_eur"] * x[i] for i in df.index) <= budget_eur
    problem += pulp.lpSum(x[i] for i in df.index) <= max_players

    for position in positions_needed:
        position = position.upper().strip()
        if position:
            problem += pulp.lpSum(
                x[i] for i in df.index if df.loc[i, "position_group"] == position
            ) >= 1

    solver = pulp.PULP_CBC_CMD(msg=False)
    status = problem.solve(solver)

    selected_idx = [i for i in df.index if pulp.value(x[i]) == 1]

    selected = df.loc[selected_idx].copy()
    selected = selected.sort_values(score_col, ascending=False)

    total_cost = float(selected["portfolio_cost_eur"].sum()) if not selected.empty else 0.0
    expected_upside = float(selected["upside_eur"].sum()) if not selected.empty else 0.0

    summary = {
        "status": pulp.LpStatus[status],
        "risk_profile": risk_profile,
        "score_column": score_col,
        "budget_millions": budget_millions,
        "budget_eur": budget_eur,
        "positions_needed": positions_needed,
        "max_players": max_players,
        "selected_players": int(len(selected)),
        "total_cost_eur": total_cost,
        "budget_used_pct": round(total_cost / budget_eur * 100, 2) if budget_eur else 0,
        "expected_upside_eur": expected_upside,
        "expected_roi_score": round(float(selected["roi_score"].mean()), 2) if not selected.empty else None,
        "average_risk": round(float(selected["risk_score"].mean()), 2) if not selected.empty else None,
        "average_confidence": round(float(selected["confidence_score"].mean()), 2) if not selected.empty else None,
        "average_future_asset_score": round(float(selected["future_asset_score"].mean()), 2) if not selected.empty else None,
        "objective_value": round(float(pulp.value(problem.objective)), 4) if pulp.value(problem.objective) is not None else None,
    }

    return selected, summary


def main() -> None:
    parser = argparse.ArgumentParser(description="Sprint 14.2 - Transfer Strategy Optimization Engine")
    parser.add_argument("--budget", type=float, default=40, help="Budget in millions of euros.")
    parser.add_argument("--positions", type=str, default="DEF,MID", help="Comma-separated position groups: GK,DEF,MID,ATT.")
    parser.add_argument("--risk-profile", type=str, default="balanced", choices=["conservative", "balanced", "aggressive"])
    parser.add_argument("--max-players", type=int, default=5)

    args = parser.parse_args()

    positions = [p.strip().upper() for p in args.positions.split(",") if p.strip()]

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    selected, summary = optimize_transfer_strategy(
        budget_millions=args.budget,
        positions_needed=positions,
        risk_profile=args.risk_profile,
        max_players=args.max_players,
    )

    selected.to_csv(OUTPUT_CSV, index=False)
    OUTPUT_JSON.write_text(json.dumps(summary, indent=2), encoding="utf-8")

    print("Transfer strategy optimization completed.")
    print(json.dumps(summary, indent=2))
    print(f"Saved portfolio to: {OUTPUT_CSV}")
    print(f"Saved summary to: {OUTPUT_JSON}")

    if not selected.empty:
        cols = [
            "player_name_fbref",
            "club",
            "league",
            "position_group",
            "portfolio_cost_eur",
            "opportunity_score",
            "risk_score",
            "confidence_score",
            "future_asset_score",
            SCORE_COLUMNS[args.risk_profile],
        ]
        print(selected[[c for c in cols if c in selected.columns]].to_string(index=False))


if __name__ == "__main__":
    main()
