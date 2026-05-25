from pathlib import Path
import argparse
import pandas as pd
from typing import Any


ROOT = Path(__file__).resolve().parents[3]

DEFAULT_INPUT_PATH = ROOT / "reports" / "rankings" / "scoring_dataset_opportunity.csv"
DEFAULT_OUTPUT_DIR = ROOT / "reports" / "model_diagnostics"


SCORE_COLUMNS = [
    "inefficiency_score_z",
    "growth_score",
    "growth_score_z",
    "confidence_score",
    "confidence_score_z",
    "opportunity_score",
]

REQUIRED_COLUMNS = [
    "league",
    "position_group",
    "opportunity_score",
    "growth_score",
    "confidence_score",
    "is_undervalued",
]


def validate_columns(df: pd.DataFrame, required_columns: list[str]) -> None:
    missing = [col for col in required_columns if col not in df.columns]

    if missing:
        raise KeyError(
            f"Missing required columns for ranking diagnostics: {missing}. "
            f"Available columns: {df.columns.tolist()}"
        )


def safe_numeric(df: pd.DataFrame, columns: list[str]) -> pd.DataFrame:
    df = df.copy()

    for column in columns:
        if column in df.columns:
            df[column] = pd.to_numeric(df[column], errors="coerce")

    return df


def build_ranking_summary(df: pd.DataFrame) -> pd.DataFrame:
    available_scores = [col for col in SCORE_COLUMNS if col in df.columns]

    summary_rows = []

    for column in available_scores:
        series = pd.to_numeric(df[column], errors="coerce")

        summary_rows.append(
            {
                "metric": column,
                "count": int(series.notna().sum()),
                "missing": int(series.isna().sum()),
                "mean": series.mean(),
                "median": series.median(),
                "std": series.std(),
                "min": series.min(),
                "p10": series.quantile(0.10),
                "p25": series.quantile(0.25),
                "p75": series.quantile(0.75),
                "p90": series.quantile(0.90),
                "max": series.max(),
            }
        )

    return pd.DataFrame(summary_rows)


def build_group_diagnostics(
    df: pd.DataFrame,
    group_column: str,
) -> pd.DataFrame:
    available_scores = [col for col in SCORE_COLUMNS if col in df.columns]

    aggregations: dict[str, Any] = {
    "player_name_fbref": "count",
    "is_undervalued": "mean",
}

    for score in available_scores:
        aggregations[score] = ["mean", "median", "std"]

    grouped = df.groupby(group_column).agg(aggregations)

    grouped.columns = [
        "_".join(col).strip("_")
        if isinstance(col, tuple)
        else str(col)
        for col in grouped.columns
    ]

    grouped = grouped.reset_index()

    grouped = grouped.rename(
        columns={
            "player_name_fbref_count": "players",
            "is_undervalued_mean": "undervalued_rate",
        }
    )

    grouped["sample_share"] = grouped["players"] / len(df)

    return grouped.sort_values("players", ascending=False)


def build_score_correlations(df: pd.DataFrame) -> pd.DataFrame:
    available_scores = [col for col in SCORE_COLUMNS if col in df.columns]

    if len(available_scores) < 2:
        return pd.DataFrame()

    corr = df[available_scores].corr(method="pearson")

    return corr.reset_index().rename(columns={"index": "score"})


def build_opportunity_tier_summary(df: pd.DataFrame) -> pd.DataFrame:
    if "opportunity_tier" not in df.columns:
        return pd.DataFrame()

    tier_summary = (
        df.groupby("opportunity_tier")
        .agg(
            players=("player_name_fbref", "count"),
            avg_opportunity_score=("opportunity_score", "mean"),
            avg_growth_score=("growth_score", "mean"),
            avg_confidence_score=("confidence_score", "mean"),
            undervalued_rate=("is_undervalued", "mean"),
        )
        .reset_index()
        .sort_values("avg_opportunity_score", ascending=False)
    )

    tier_summary["sample_share"] = tier_summary["players"] / len(df)

    return tier_summary


def export_csv(df: pd.DataFrame, output_path: Path) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(output_path, index=False)


def run_diagnostics(
    input_path: Path,
    output_dir: Path,
) -> dict[str, Path]:
    if not input_path.exists():
        raise FileNotFoundError(f"Ranking input not found: {input_path}")

    df = pd.read_csv(input_path)
    validate_columns(df, REQUIRED_COLUMNS)

    df = safe_numeric(df, SCORE_COLUMNS)

    outputs = {}

    ranking_summary = build_ranking_summary(df)
    output_path = output_dir / "ranking_summary.csv"
    export_csv(ranking_summary, output_path)
    outputs["ranking_summary"] = output_path

    ranking_by_league = build_group_diagnostics(df, "league")
    output_path = output_dir / "ranking_by_league.csv"
    export_csv(ranking_by_league, output_path)
    outputs["ranking_by_league"] = output_path

    ranking_by_position = build_group_diagnostics(df, "position_group")
    output_path = output_dir / "ranking_by_position.csv"
    export_csv(ranking_by_position, output_path)
    outputs["ranking_by_position"] = output_path

    ranking_score_correlations = build_score_correlations(df)
    output_path = output_dir / "ranking_score_correlations.csv"
    export_csv(ranking_score_correlations, output_path)
    outputs["ranking_score_correlations"] = output_path

    ranking_tier_summary = build_opportunity_tier_summary(df)
    output_path = output_dir / "ranking_tier_summary.csv"
    export_csv(ranking_tier_summary, output_path)
    outputs["ranking_tier_summary"] = output_path

    return outputs


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Build diagnostics for scouting ranking outputs."
    )

    parser.add_argument(
        "--input",
        default=str(DEFAULT_INPUT_PATH),
        help="Path to scoring_dataset_opportunity.csv.",
    )

    parser.add_argument(
        "--output-dir",
        default=str(DEFAULT_OUTPUT_DIR),
        help="Directory where ranking diagnostics will be saved.",
    )

    args = parser.parse_args()

    input_path = Path(args.input)
    output_dir = Path(args.output_dir)

    if not input_path.is_absolute():
        input_path = ROOT / input_path

    if not output_dir.is_absolute():
        output_dir = ROOT / output_dir

    outputs = run_diagnostics(
        input_path=input_path,
        output_dir=output_dir,
    )

    print("Ranking diagnostics completed")
    print(f"Input: {input_path}")

    for name, path in outputs.items():
        rows = len(pd.read_csv(path))
        print(f"{name}: {rows:,} rows -> {path}")


if __name__ == "__main__":
    main()