from pathlib import Path
import argparse
import yaml
import numpy as np
import pandas as pd


ROOT = Path(__file__).resolve().parents[3]
DEFAULT_CONFIG_PATH = ROOT / "config" / "scoring.yaml"


def load_config(config_path: Path = DEFAULT_CONFIG_PATH) -> dict:
    if not config_path.exists():
        raise FileNotFoundError(f"Config file not found: {config_path}")

    with config_path.open("r", encoding="utf-8") as file:
        return yaml.safe_load(file)


def resolve_path(path: str | Path) -> Path:
    path = Path(path)
    if path.is_absolute():
        return path
    return ROOT / path


def minmax_0_100(series: pd.Series) -> pd.Series:
    min_value = series.min(skipna=True)
    max_value = series.max(skipna=True)

    if pd.isna(min_value) or pd.isna(max_value) or max_value == min_value:
        return pd.Series(50.0, index=series.index)

    return 100 * (series - min_value) / (max_value - min_value)


def validate_required_columns(df: pd.DataFrame, columns: list[str]) -> None:
    missing = [col for col in columns if col not in df.columns]

    if missing:
        raise KeyError(
            f"Missing required columns for Opportunity Score: {missing}. "
            f"Available columns: {df.columns.tolist()}"
        )


def assign_opportunity_tier(
    score: float,
    tiers: dict[str, float],
) -> str:
    if score >= tiers.get("high_priority", 80):
        return "target_scouting"

    if score >= tiers.get("monitoring", 60):
        return "high_priority"

    if score >= tiers.get("interesting", 40):
        return "monitoring"

    if score >= tiers.get("low", 20):
        return "interesting"

    return "low_opportunity"


def build_opportunity_score(
    df: pd.DataFrame,
    weights: dict[str, float],
    tiers: dict[str, float],
) -> pd.DataFrame:
    df = df.copy()

    required_columns = list(weights.keys())
    validate_required_columns(df, required_columns)

    total_weight = sum(weights.values())

    if total_weight == 0:
        raise ValueError("Opportunity Score weights sum to zero.")

    df["opportunity_score_raw"] = 0.0

    for column, weight in weights.items():
        df["opportunity_score_raw"] += (
            pd.to_numeric(df[column], errors="coerce").fillna(0.0)
            * weight
            / total_weight
        )

    df["opportunity_score"] = minmax_0_100(df["opportunity_score_raw"])

    df["opportunity_rank"] = (
        df["opportunity_score"]
        .rank(method="first", ascending=False)
        .astype(int)
    )

    df["opportunity_tier"] = df["opportunity_score"].apply(
        lambda value: assign_opportunity_tier(
            score=float(value),
            tiers=tiers,
        )
    )

    df["is_scouting_target"] = df["opportunity_tier"] == "target_scouting"

    df["is_high_priority_or_target"] = df["opportunity_tier"].isin(
        [
            "high_priority",
            "target_scouting",
        ]
    )

    return df


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Build final Opportunity Score for scouting rankings."
    )

    parser.add_argument(
        "--config",
        default=str(DEFAULT_CONFIG_PATH),
        help="Path to scoring YAML config.",
    )

    args = parser.parse_args()

    config = load_config(Path(args.config))
    opportunity_config = config["opportunity_score"]

    input_path = resolve_path(opportunity_config["input_path"])
    output_path = resolve_path(opportunity_config["output_path"])

    if not input_path.exists():
        raise FileNotFoundError(
            f"Input confidence scoring dataset not found: {input_path}"
        )

    df = pd.read_csv(input_path)

    scored_df = build_opportunity_score(
        df=df,
        weights=opportunity_config["weights"],
        tiers=opportunity_config.get("tiers", {}),
    )

    scored_df = scored_df.sort_values(
        by="opportunity_score",
        ascending=False,
    )

    output_path.parent.mkdir(parents=True, exist_ok=True)
    scored_df.to_csv(output_path, index=False)

    print("Opportunity scoring completed")
    print(f"Input: {input_path}")
    print(f"Rows: {len(scored_df):,}")
    print(f"Scouting targets: {int(scored_df['is_scouting_target'].sum()):,}")
    print(
        "High priority or target players: "
        f"{int(scored_df['is_high_priority_or_target'].sum()):,}"
    )
    print(f"Output: {output_path}")


if __name__ == "__main__":
    main()