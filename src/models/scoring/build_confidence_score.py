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


def safe_zscore(series: pd.Series) -> pd.Series:
    mean = series.mean(skipna=True)
    std = series.std(skipna=True)

    if pd.isna(std) or std == 0:
        return pd.Series(0.0, index=series.index)

    return (series - mean) / std


def build_feature_completeness(
    df: pd.DataFrame,
    required_features: list[str],
) -> pd.Series:
    available_features = [col for col in required_features if col in df.columns]

    if not available_features:
        return pd.Series(0.0, index=df.index)

    return df[available_features].notna().mean(axis=1)


def build_temporal_stability(df: pd.DataFrame) -> pd.Series:
    components = []

    if "career_year" in df.columns:
        career_year = pd.to_numeric(df["career_year"], errors="coerce").fillna(0)
        components.append(np.minimum(career_year / 3, 1))

    if "market_value_growth_prev" in df.columns:
        growth = pd.to_numeric(df["market_value_growth_prev"], errors="coerce")
        growth_stability = 1 - np.minimum(growth.abs(), 1)
        components.append(growth_stability.fillna(0.5))

    if not components:
        return pd.Series(0.5, index=df.index)

    return pd.concat(components, axis=1).mean(axis=1)


def build_confidence_score(
    df: pd.DataFrame,
    weights: dict[str, float],
    full_reliability_minutes: float,
    required_features: list[str],
) -> pd.DataFrame:
    df = df.copy()

    if "matching_confidence" in df.columns:
        df["matching_confidence_component"] = (
            pd.to_numeric(df["matching_confidence"], errors="coerce")
            .clip(lower=0, upper=1)
            .fillna(0.5)
        )
    else:
        df["matching_confidence_component"] = 0.5

    if "minutes_played" not in df.columns:
        raise KeyError("minutes_played is required to calculate Confidence Score.")

    df["minutes_reliability_component"] = (
        pd.to_numeric(df["minutes_played"], errors="coerce")
        .fillna(0)
        .clip(lower=0)
        / full_reliability_minutes
    ).clip(lower=0, upper=1)

    df["feature_completeness_component"] = build_feature_completeness(
        df=df,
        required_features=required_features,
    )

    df["temporal_stability_component"] = build_temporal_stability(df).clip(
        lower=0,
        upper=1,
    )

    total_weight = sum(weights.values())

    if total_weight == 0:
        raise ValueError("Confidence Score weights sum to zero.")

    df["confidence_score_raw"] = (
        weights.get("matching_confidence", 0.35)
        * df["matching_confidence_component"]
        + weights.get("minutes_reliability", 0.35)
        * df["minutes_reliability_component"]
        + weights.get("feature_completeness", 0.20)
        * df["feature_completeness_component"]
        + weights.get("temporal_stability", 0.10)
        * df["temporal_stability_component"]
    ) / total_weight

    df["confidence_score"] = 100 * df["confidence_score_raw"]
    df["confidence_score_z"] = safe_zscore(df["confidence_score"])
    df["confidence_rank"] = (
        df["confidence_score"]
        .rank(method="first", ascending=False)
        .astype(int)
    )

    df["low_confidence_flag"] = df["confidence_score"] <= df[
        "confidence_score"
    ].quantile(0.20)

    return df


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Build Confidence Score for scouting rankings."
    )

    parser.add_argument(
        "--config",
        default=str(DEFAULT_CONFIG_PATH),
        help="Path to scoring YAML config.",
    )

    args = parser.parse_args()

    config = load_config(Path(args.config))
    confidence_config = config["confidence_score"]

    input_path = resolve_path(confidence_config["input_path"])
    output_path = resolve_path(confidence_config["output_path"])

    if not input_path.exists():
        raise FileNotFoundError(f"Input growth scoring dataset not found: {input_path}")

    df = pd.read_csv(input_path)

    scored_df = build_confidence_score(
        df=df,
        weights=confidence_config.get("weights", {}),
        full_reliability_minutes=confidence_config.get("minutes", {}).get(
            "full_reliability_minutes", 1800
        ),
        required_features=confidence_config.get("required_features", []),
    )

    scored_df = scored_df.sort_values(
        by="confidence_score",
        ascending=False,
    )

    output_path.parent.mkdir(parents=True, exist_ok=True)
    scored_df.to_csv(output_path, index=False)

    print("Confidence scoring completed")
    print(f"Input: {input_path}")
    print(f"Rows: {len(scored_df):,}")
    print(f"Low confidence players: {int(scored_df['low_confidence_flag'].sum()):,}")
    print(f"Output: {output_path}")


if __name__ == "__main__":
    main()