import pandas as pd


def get_undervalued_players(
    df: pd.DataFrame,
    top_n: int = 25,
) -> pd.DataFrame:
    """
    Return most undervalued players.
    """

    ranking = (
        df.sort_values(
            by="inefficiency_score",
            ascending=False,
        )
        .head(top_n)
        .copy()
    )

    return ranking


def get_overvalued_players(
    df: pd.DataFrame,
    top_n: int = 25,
) -> pd.DataFrame:
    """
    Return most overvalued players.
    """

    ranking = (
        df.sort_values(
            by="inefficiency_score",
            ascending=True,
        )
        .head(top_n)
        .copy()
    )

    return ranking


def build_scouting_columns(
    df: pd.DataFrame,
) -> pd.DataFrame:
    """
    Select columns useful for scouting outputs.
    """

    preferred_cols = [
        "player_name_fbref",
        "club",
        "league",
        "season",
        "position_group",
        "age",
        "minutes_played",
        "market_value_eur",
        "predicted_market_value_eur",
        "market_value_gap_eur",
        "market_value_gap_pct",
        "inefficiency_score",
        "inefficiency_score_z",
    ]

    keep_cols = [
        col for col in preferred_cols
        if col in df.columns
    ]

    return df[keep_cols].copy()