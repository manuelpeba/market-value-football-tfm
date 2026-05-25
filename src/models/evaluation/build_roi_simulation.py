from pathlib import Path
import argparse
from duckdb import df
import pandas as pd


ROOT = Path(__file__).resolve().parents[3]

DEFAULT_INPUT_PATH = ROOT / "reports" / "rankings" / "scoring_dataset_opportunity.csv"
DEFAULT_SHORTLIST_PATH = ROOT / "reports" / "rankings" / "scouting_shortlist.csv"
DEFAULT_OUTPUT_DIR = ROOT / "reports" / "business"


REQUIRED_COLUMNS = [
    "player_name_fbref",
    "league",
    "position_group",
    "market_value_eur",
    "predicted_market_value_eur",
    "opportunity_score",
    "confidence_score",
    "growth_score",
    "is_undervalued",
]


GROUP_COLUMNS = [
    "league",
    "position_group",
    "opportunity_tier",
]


def resolve_path(path: str | Path) -> Path:
    path = Path(path)

    if path.is_absolute():
        return path

    return ROOT / path


def validate_columns(df: pd.DataFrame, required_columns: list[str]) -> None:
    missing = [col for col in required_columns if col not in df.columns]

    if missing:
        raise KeyError(
            f"Missing required columns for ROI simulation: {missing}. "
            f"Available columns: {df.columns.tolist()}"
        )


def prepare_roi_dataset(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()

    numeric_columns = [
        "market_value_eur",
        "predicted_market_value_eur",
        "opportunity_score",
        "confidence_score",
        "growth_score",
    ]

    for column in numeric_columns:
        if column in df.columns:
            df[column] = pd.to_numeric(df[column], errors="coerce")

    df = df[df["market_value_eur"].notna()].copy()
    df = df[df["predicted_market_value_eur"].notna()].copy()
    df = df[df["market_value_eur"] > 0].copy()

    df["assumed_buy_price_eur"] = df["market_value_eur"]

    # Conservative realization scenario:
    # only a fraction of the predicted upside is assumed
    # to materialize in the transfer market.

    realization_factor = 0.5

    df["assumed_sell_price_eur"] = (
        df["market_value_eur"]
    +
        (
            df["predicted_market_value_eur"]
            - df["market_value_eur"]
        )
        * realization_factor
    )

    df["expected_profit_eur"] = (
        df["assumed_sell_price_eur"] - df["assumed_buy_price_eur"]
    )

    df["expected_roi_pct"] = (
        df["expected_profit_eur"] / df["assumed_buy_price_eur"]
    ) * 100

    df["positive_roi_flag"] = df["expected_profit_eur"] > 0

    df["risk_adjusted_profit_eur"] = (
        df["expected_profit_eur"] * (df["confidence_score"] / 100)
    )

    df["risk_adjusted_roi_pct"] = (
        df["risk_adjusted_profit_eur"] / df["assumed_buy_price_eur"]
    ) * 100

    return df


def build_roi_simulation(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()

    sort_columns = [
        "opportunity_score",
        "risk_adjusted_profit_eur",
        "confidence_score",
    ]

    available_sort_columns = [col for col in sort_columns if col in df.columns]

    return (
        df.sort_values(
            by=available_sort_columns,
            ascending=[False] * len(available_sort_columns),
        )
        .reset_index(drop=True)
    )


def build_strategy_summary(
    df: pd.DataFrame,
    group_column: str,
) -> pd.DataFrame:
    if group_column not in df.columns:
        return pd.DataFrame()

    summary = (
        df.groupby(group_column)
        .agg(
            players=("player_name_fbref", "count"),
            avg_market_value_eur=("market_value_eur", "mean"),
            avg_predicted_value_eur=("predicted_market_value_eur", "mean"),
            total_expected_profit_eur=("expected_profit_eur", "sum"),
            avg_expected_profit_eur=("expected_profit_eur", "mean"),
            median_expected_profit_eur=("expected_profit_eur", "median"),
            avg_expected_roi_pct=("expected_roi_pct", "mean"),
            median_expected_roi_pct=("expected_roi_pct", "median"),
            positive_roi_rate=("positive_roi_flag", "mean"),
            total_risk_adjusted_profit_eur=("risk_adjusted_profit_eur", "sum"),
            avg_risk_adjusted_roi_pct=("risk_adjusted_roi_pct", "mean"),
            avg_opportunity_score=("opportunity_score", "mean"),
            avg_confidence_score=("confidence_score", "mean"),
            avg_growth_score=("growth_score", "mean"),
        )
        .reset_index()
        .sort_values(
            by="total_risk_adjusted_profit_eur",
            ascending=False,
        )
    )

    return summary


def build_global_summary(df: pd.DataFrame) -> pd.DataFrame:
    summary = {
        "players": len(df),
        "total_market_value_eur": df["market_value_eur"].sum(),
        "total_predicted_value_eur": df["predicted_market_value_eur"].sum(),
        "total_expected_profit_eur": df["expected_profit_eur"].sum(),
        "avg_expected_profit_eur": df["expected_profit_eur"].mean(),
        "median_expected_profit_eur": df["expected_profit_eur"].median(),
        "avg_expected_roi_pct": df["expected_roi_pct"].mean(),
        "median_expected_roi_pct": df["expected_roi_pct"].median(),
        "positive_roi_rate": df["positive_roi_flag"].mean(),
        "total_risk_adjusted_profit_eur": df["risk_adjusted_profit_eur"].sum(),
        "avg_risk_adjusted_roi_pct": df["risk_adjusted_roi_pct"].mean(),
        "avg_opportunity_score": df["opportunity_score"].mean(),
        "avg_confidence_score": df["confidence_score"].mean(),
        "avg_growth_score": df["growth_score"].mean(),
    }

    return pd.DataFrame([summary])


def select_business_columns(df: pd.DataFrame) -> pd.DataFrame:
    preferred_columns = [
        "player_name_fbref",
        "player_name_tm",
        "club",
        "league",
        "season",
        "position_group",
        "age",
        "minutes_played",
        "market_value_eur",
        "predicted_market_value_eur",
        "assumed_buy_price_eur",
        "assumed_sell_price_eur",
        "expected_profit_eur",
        "expected_roi_pct",
        "risk_adjusted_profit_eur",
        "risk_adjusted_roi_pct",
        "positive_roi_flag",
        "inefficiency_score_z",
        "growth_score",
        "confidence_score",
        "opportunity_score",
        "opportunity_tier",
        "matching_confidence",
        "matching_method",
    ]

    available_columns = [col for col in preferred_columns if col in df.columns]

    return df[available_columns].copy()


def export_csv(df: pd.DataFrame, output_path: Path) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(output_path, index=False)


def run_roi_simulation(
    input_path: Path,
    shortlist_path: Path,
    output_dir: Path,
) -> dict[str, Path]:
    if not input_path.exists():
        raise FileNotFoundError(f"Scoring dataset not found: {input_path}")

    df = pd.read_csv(input_path)
    validate_columns(df, REQUIRED_COLUMNS)

    roi_df = prepare_roi_dataset(df)

    # Main ROI simulation over the full scored dataset.
    roi_simulation = build_roi_simulation(roi_df)

    outputs = {}

    output_path = output_dir / "roi_simulation.csv"
    export_csv(select_business_columns(roi_simulation), output_path)
    outputs["roi_simulation"] = output_path

    # Global summary.
    output_path = output_dir / "roi_global_summary.csv"
    export_csv(build_global_summary(roi_df), output_path)
    outputs["roi_global_summary"] = output_path

    # Strategy summaries.
    strategy_frames = []

    for group_column in GROUP_COLUMNS:
        summary = build_strategy_summary(roi_df, group_column)

        if summary.empty:
            continue

        summary.insert(0, "strategy_dimension", group_column)
        summary = summary.rename(columns={group_column: "strategy_segment"})
        strategy_frames.append(summary)

    if strategy_frames:
        transfer_strategy_analysis = pd.concat(
            strategy_frames,
            ignore_index=True,
        )
    else:
        transfer_strategy_analysis = pd.DataFrame()

    output_path = output_dir / "transfer_strategy_analysis.csv"
    export_csv(transfer_strategy_analysis, output_path)
    outputs["transfer_strategy_analysis"] = output_path

    # Shortlist-specific simulation.
    if shortlist_path.exists():
        shortlist_df = pd.read_csv(shortlist_path)

        shortlist_required_columns = [
            col for col in REQUIRED_COLUMNS if col != "is_undervalued"
        ]

        validate_columns(shortlist_df, shortlist_required_columns)

        if "is_undervalued" not in shortlist_df.columns:
            shortlist_df["is_undervalued"] = True

        shortlist_roi_df = prepare_roi_dataset(shortlist_df)

        shortlist_roi = build_roi_simulation(shortlist_roi_df)

        output_path = output_dir / "roi_scouting_shortlist.csv"
        export_csv(select_business_columns(shortlist_roi), output_path)
        outputs["roi_scouting_shortlist"] = output_path

        output_path = output_dir / "roi_scouting_shortlist_summary.csv"
        export_csv(build_global_summary(shortlist_roi_df), output_path)
        outputs["roi_scouting_shortlist_summary"] = output_path

    return outputs


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Build ROI simulation for scouting rankings."
    )

    parser.add_argument(
        "--input",
        default=str(DEFAULT_INPUT_PATH),
        help="Path to scoring_dataset_opportunity.csv.",
    )

    parser.add_argument(
        "--shortlist",
        default=str(DEFAULT_SHORTLIST_PATH),
        help="Path to scouting_shortlist.csv.",
    )

    parser.add_argument(
        "--output-dir",
        default=str(DEFAULT_OUTPUT_DIR),
        help="Directory where business outputs will be saved.",
    )

    args = parser.parse_args()

    input_path = resolve_path(args.input)
    shortlist_path = resolve_path(args.shortlist)
    output_dir = resolve_path(args.output_dir)

    outputs = run_roi_simulation(
        input_path=input_path,
        shortlist_path=shortlist_path,
        output_dir=output_dir,
    )

    print("ROI simulation completed")
    print(f"Input: {input_path}")

    for name, path in outputs.items():
        rows = len(pd.read_csv(path))
        print(f"{name}: {rows:,} rows -> {path}")


if __name__ == "__main__":
    main()