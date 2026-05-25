from pathlib import Path
import argparse
import yaml
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


def select_columns(df: pd.DataFrame, columns: list[str]) -> pd.DataFrame:
    available_columns = [col for col in columns if col in df.columns]
    return df[available_columns].copy()


def apply_base_filters(
    df: pd.DataFrame,
    min_minutes_played: float,
    min_confidence_score: float,
) -> pd.DataFrame:
    df = df.copy()

    if "minutes_played" in df.columns:
        df = df[df["minutes_played"] >= min_minutes_played].copy()

    if "confidence_score" in df.columns:
        df = df[df["confidence_score"] >= min_confidence_score].copy()

    return df


def export_csv(df: pd.DataFrame, output_path: Path) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(output_path, index=False)


def generate_rankings(
    df: pd.DataFrame,
    output_dir: Path,
    selected_columns: list[str],
    top_n_global: int,
    top_n_by_group: int,
    top_n_shortlist: int,
    min_minutes_played: float,
    min_confidence_score: float,
    min_opportunity_score: float,
) -> dict[str, Path]:
    output_paths = {}

    base_df = apply_base_filters(
        df=df,
        min_minutes_played=min_minutes_played,
        min_confidence_score=min_confidence_score,
    )

    # 1. Top undervalued global
    top_undervalued_global = (
        base_df[base_df["is_undervalued"] == True]
        .sort_values("opportunity_score", ascending=False)
        .head(top_n_global)
    )

    output_path = output_dir / "top_undervalued_global.csv"
    export_csv(select_columns(top_undervalued_global, selected_columns), output_path)
    output_paths["top_undervalued_global"] = output_path

    # 2. Top undervalued by league
    top_by_league = (
        base_df[base_df["is_undervalued"] == True]
        .sort_values(["league", "opportunity_score"], ascending=[True, False])
        .groupby("league", group_keys=False)
        .head(top_n_by_group)
    )

    output_path = output_dir / "top_undervalued_by_league.csv"
    export_csv(select_columns(top_by_league, selected_columns), output_path)
    output_paths["top_undervalued_by_league"] = output_path

    # 3. Top undervalued by position
    top_by_position = (
        base_df[base_df["is_undervalued"] == True]
        .sort_values(["position_group", "opportunity_score"], ascending=[True, False])
        .groupby("position_group", group_keys=False)
        .head(top_n_by_group)
    )

    output_path = output_dir / "top_undervalued_by_position.csv"
    export_csv(select_columns(top_by_position, selected_columns), output_path)
    output_paths["top_undervalued_by_position"] = output_path

    # 4. Top high potential
    top_high_potential = (
        base_df.sort_values(
            ["growth_score", "opportunity_score"],
            ascending=[False, False],
        )
        .head(top_n_global)
    )

    output_path = output_dir / "top_high_potential.csv"
    export_csv(select_columns(top_high_potential, selected_columns), output_path)
    output_paths["top_high_potential"] = output_path

    # 5. Top low risk
    top_low_risk = (
        base_df.sort_values(
            ["confidence_score", "opportunity_score"],
            ascending=[False, False],
        )
        .head(top_n_global)
    )

    output_path = output_dir / "top_low_risk.csv"
    export_csv(select_columns(top_low_risk, selected_columns), output_path)
    output_paths["top_low_risk"] = output_path

    # 6. Final scouting shortlist
    scouting_shortlist = (
        base_df[
            (base_df["opportunity_score"] >= min_opportunity_score)
            & (base_df["is_undervalued"] == True)
        ]
        .sort_values(
            ["opportunity_score", "confidence_score", "growth_score"],
            ascending=[False, False, False],
        )
        .head(top_n_shortlist)
    )

    output_path = output_dir / "scouting_shortlist.csv"
    export_csv(select_columns(scouting_shortlist, selected_columns), output_path)
    output_paths["scouting_shortlist"] = output_path

    return output_paths


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Generate final scouting rankings from Opportunity Score."
    )

    parser.add_argument(
        "--config",
        default=str(DEFAULT_CONFIG_PATH),
        help="Path to scoring YAML config.",
    )

    args = parser.parse_args()

    config = load_config(Path(args.config))
    rankings_config = config["rankings"]

    input_path = resolve_path(rankings_config["input_path"])
    output_dir = resolve_path(rankings_config["output_dir"])

    if not input_path.exists():
        raise FileNotFoundError(f"Opportunity scoring dataset not found: {input_path}")

    df = pd.read_csv(input_path)

    required_columns = [
        "opportunity_score",
        "growth_score",
        "confidence_score",
        "is_undervalued",
    ]

    missing = [col for col in required_columns if col not in df.columns]

    if missing:
        raise KeyError(
            f"Missing required columns for ranking generation: {missing}. "
            f"Available columns: {df.columns.tolist()}"
        )

    top_n_config = rankings_config.get("top_n", {})
    filters_config = rankings_config.get("filters", {})

    output_paths = generate_rankings(
        df=df,
        output_dir=output_dir,
        selected_columns=rankings_config.get("columns", []),
        top_n_global=top_n_config.get("global", 50),
        top_n_by_group=top_n_config.get("by_group", 20),
        top_n_shortlist=top_n_config.get("shortlist", 100),
        min_minutes_played=filters_config.get("min_minutes_played", 300),
        min_confidence_score=filters_config.get("min_confidence_score", 50),
        min_opportunity_score=filters_config.get("min_opportunity_score", 60),
    )

    print("Ranking generation completed")
    print(f"Input: {input_path}")
    print(f"Rows: {len(df):,}")

    for name, path in output_paths.items():
        rows = len(pd.read_csv(path))
        print(f"{name}: {rows:,} rows -> {path}")


if __name__ == "__main__":
    main()