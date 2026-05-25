from pathlib import Path
import argparse
import yaml
import numpy as np
import pandas as pd


ROOT = Path(__file__).resolve().parents[3]
DEFAULT_CONFIG_PATH = ROOT / "config" / "scoring.yaml"


ID_COLUMNS = [
    "player_name",
    "player_name_fbref",
    "player_name_tm",
    "club",
    "league",
    "season",
    "position",
    "position_group",
    "age",
    "minutes_played",
    "matching_confidence",
    "matching_method",
]


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


def validate_required_columns(df: pd.DataFrame, required_columns: list[str]) -> None:
    missing = [col for col in required_columns if col not in df.columns]

    if missing:
        raise KeyError(
            "Missing required columns for inefficiency scoring: "
            f"{missing}. Available columns: {df.columns.tolist()}"
        )


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


def build_inefficiency_score(
    df: pd.DataFrame,
    observed_market_value_col: str,
    observed_log_market_value_col: str,
    predicted_log_market_value_col: str,
    min_predicted_market_value_eur: float = 100_000,
    max_market_value_gap_pct: float = 5.0,
    winsorize_lower: float = 0.01,
    winsorize_upper: float = 0.99,
) -> pd.DataFrame:
    df = df.copy()

    validate_required_columns(
        df,
        [
            observed_market_value_col,
            observed_log_market_value_col,
            predicted_log_market_value_col,
        ],
    )

    df["predicted_market_value_eur"] = np.exp(df[predicted_log_market_value_col])
    df["predicted_market_value_eur"] = df["predicted_market_value_eur"].clip(
        lower=min_predicted_market_value_eur
    )

    df["residual_observed_minus_predicted_log"] = (
        df[observed_log_market_value_col] - df[predicted_log_market_value_col]
    )

    df["inefficiency_score_log"] = (
        df[predicted_log_market_value_col] - df[observed_log_market_value_col]
    )

    df["market_value_gap_eur"] = (
        df["predicted_market_value_eur"] - df[observed_market_value_col]
    )

    df["market_value_gap_pct"] = (
        df["market_value_gap_eur"] / df[observed_market_value_col]
    )

    df["market_value_gap_pct"] = df["market_value_gap_pct"].clip(
        lower=-max_market_value_gap_pct,
        upper=max_market_value_gap_pct,
    )

    df["inefficiency_score_log_winsorized"] = winsorize_series(
        df["inefficiency_score_log"],
        lower_quantile=winsorize_lower,
        upper_quantile=winsorize_upper,
    )

    df["market_value_gap_pct_winsorized"] = winsorize_series(
        df["market_value_gap_pct"],
        lower_quantile=winsorize_lower,
        upper_quantile=winsorize_upper,
    )

    df["inefficiency_score_z"] = safe_zscore(
        df["inefficiency_score_log_winsorized"]
    )

    df["market_value_gap_pct_z"] = safe_zscore(
        df["market_value_gap_pct_winsorized"]
    )

    df["is_undervalued"] = df["inefficiency_score_log"] > 0
    df["is_overvalued"] = df["inefficiency_score_log"] < 0

    df["inefficiency_rank"] = (
        df["inefficiency_score_z"]
        .rank(method="first", ascending=False)
        .astype(int)
    )

    return df


def select_output_columns(df: pd.DataFrame) -> pd.DataFrame:
    return df.copy()


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Build robust Inefficiency Score for scouting rankings."
    )

    parser.add_argument(
        "--config",
        default=str(DEFAULT_CONFIG_PATH),
        help="Path to scoring YAML config.",
    )

    args = parser.parse_args()

    config = load_config(Path(args.config))
    scoring_config = config["scoring"]

    input_path = resolve_path(scoring_config["input_predictions_path"])
    output_path = resolve_path(scoring_config["output_path"])

    columns_config = scoring_config["columns"]
    clipping_config = scoring_config.get("clipping", {})
    normalization_config = scoring_config.get("normalization", {})

    if not input_path.exists():
        raise FileNotFoundError(f"Input predictions file not found: {input_path}")

    df = pd.read_csv(input_path)

    scored_df = build_inefficiency_score(
        df=df,
        observed_market_value_col=columns_config["observed_market_value"],
        observed_log_market_value_col=columns_config["observed_log_market_value"],
        predicted_log_market_value_col=columns_config["predicted_log_market_value"],
        min_predicted_market_value_eur=clipping_config.get(
            "min_predicted_market_value_eur", 100_000
        ),
        max_market_value_gap_pct=clipping_config.get(
            "max_market_value_gap_pct", 5.0
        ),
        winsorize_lower=normalization_config.get("winsorize_lower", 0.01),
        winsorize_upper=normalization_config.get("winsorize_upper", 0.99),
    )

    output_df = select_output_columns(scored_df)
    output_df = output_df.sort_values(
        by="inefficiency_score_z",
        ascending=False,
    )

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_df.to_csv(output_path, index=False)

    print("Inefficiency scoring completed")
    print(f"Input: {input_path}")
    print(f"Rows: {len(output_df):,}")
    print(f"Undervalued players: {int(output_df['is_undervalued'].sum()):,}")
    print(f"Overvalued players: {int(output_df['is_overvalued'].sum()):,}")
    print(f"Output: {output_path}")


if __name__ == "__main__":
    main()