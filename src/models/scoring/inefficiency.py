import numpy as np
import pandas as pd


def add_inefficiency_scores(
    df: pd.DataFrame,
    observed_col: str = "market_value_eur",
    predicted_log_col: str = "predicted_log_market_value",
) -> pd.DataFrame:
    """
    Compute inefficiency scores from observed and predicted market values.
    """

    df = df.copy()

    df["predicted_market_value_eur"] = np.exp(
        df[predicted_log_col]
    )

    df["market_value_gap_eur"] = (
        df["predicted_market_value_eur"]
        - df[observed_col]
    )

    df["market_value_gap_pct"] = (
        df["market_value_gap_eur"]
        / df[observed_col]
    )

    df["inefficiency_score"] = (
        df["market_value_gap_pct"]
    )

    df["inefficiency_score_z"] = (
        (
            df["inefficiency_score"]
            - df["inefficiency_score"].mean()
        )
        / df["inefficiency_score"].std()
    )

    return df