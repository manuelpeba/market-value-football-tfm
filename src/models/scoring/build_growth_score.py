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


def safe_zscore(series: pd.Series) -> pd.Series:
    mean = series.mean(skipna=True)
    std = series.std(skipna=True)

    if pd.isna(std) or std == 0:
        return pd.Series(0.0, index=series.index)

    return (series - mean) / std


def winsorize_series(
    series: pd.Series,
    lower_quantile: float,
    upper_quantile: float,
) -> pd.Series:
    lower = series.quantile(lower_quantile)
    upper = series.quantile(upper_quantile)

    return series.clip(lower=lower, upper=upper)


def minmax_0_100(series: pd.Series) -> pd.Series:
    min_value = series.min(skipna=True)
    max_value = series.max(skipna=True)

    if pd.isna(min_value) or pd.isna(max_value) or max_value == min_value:
        return pd.Series(50.0, index=series.index)

    return 100 * (series - min_value) / (max_value - min_value)


def validate_variables(df: pd.DataFrame, variables: list[str]) -> list[str]:
    available = [col for col in variables if col in df.columns]
    missing = [col for col in variables if col not in df.columns]

    if missing:
        print(f"Warning: missing growth variables ignored: {missing}")

    if not available:
        raise KeyError(
            "No growth variables available. "
            f"Requested: {variables}. "
            f"Available columns: {df.columns.tolist()}"
        )

    return available


def build_growth_score(
    df: pd.DataFrame,
    positive_variables: list[str],
    negative_variables: list[str],
    weights: dict[str, float],
    winsorize_lower: float = 0.01,
    winsorize_upper: float = 0.99,
) -> pd.DataFrame:
    df = df.copy()

    all_variables = positive_variables + negative_variables
    available_variables = validate_variables(df, all_variables)

    normalized_components = []

    for variable in available_variables:
        component = pd.to_numeric(df[variable], errors="coerce")

        component = winsorize_series(
            component,
            lower_quantile=winsorize_lower,
            upper_quantile=winsorize_upper,
        )

        component_z = safe_zscore(component)

        if variable in negative_variables:
            component_z = -component_z

        component_name = f"{variable}_growth_component_z"
        df[component_name] = component_z

        weight = weights.get(variable, 1.0 / len(available_variables))

        normalized_components.append(
            (
                component_name,
                weight,
            )
        )

    total_weight = sum(weight for _, weight in normalized_components)

    if total_weight == 0:
        raise ValueError("Growth Score weights sum to zero.")

    df["growth_score_raw"] = 0.0

    for component_name, weight in normalized_components:
        df["growth_score_raw"] += (
            df[component_name].fillna(0.0) * weight / total_weight
        )

    df["growth_score_z"] = safe_zscore(df["growth_score_raw"])
    df["growth_score"] = minmax_0_100(df["growth_score_raw"])

    df["growth_rank"] = (
        df["growth_score"]
        .rank(method="first", ascending=False)
        .astype(int)
    )

    df["high_growth_flag"] = df["growth_score"] >= df["growth_score"].quantile(0.80)

    return df


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Build Growth Score for scouting opportunity ranking."
    )

    parser.add_argument(
        "--config",
        default=str(DEFAULT_CONFIG_PATH),
        help="Path to scoring YAML config.",
    )

    args = parser.parse_args()

    config = load_config(Path(args.config))
    growth_config = config["growth_score"]

    input_path = resolve_path(growth_config["input_path"])
    output_path = resolve_path(growth_config["output_path"])

    if not input_path.exists():
        raise FileNotFoundError(f"Input scoring dataset not found: {input_path}")

    df = pd.read_csv(input_path)

    variables_config = growth_config["variables"]
    normalization_config = growth_config.get("normalization", {})

    scored_df = build_growth_score(
        df=df,
        positive_variables=variables_config.get("positive", []),
        negative_variables=variables_config.get("negative", []),
        weights=growth_config.get("weights", {}),
        winsorize_lower=normalization_config.get("winsorize_lower", 0.01),
        winsorize_upper=normalization_config.get("winsorize_upper", 0.99),
    )

    scored_df = scored_df.sort_values(
        by="growth_score",
        ascending=False,
    )

    output_path.parent.mkdir(parents=True, exist_ok=True)
    scored_df.to_csv(output_path, index=False)

    print("Growth scoring completed")
    print(f"Input: {input_path}")
    print(f"Rows: {len(scored_df):,}")
    print(f"High growth players: {int(scored_df['high_growth_flag'].sum()):,}")
    print(f"Output: {output_path}")


if __name__ == "__main__":
    main()