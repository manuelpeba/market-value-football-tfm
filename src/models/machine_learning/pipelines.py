import numpy as np
import pandas as pd


TARGET = "log_market_value_eur"


NUMERIC_FEATURES = [
    "age",
    "log_minutes_played",
    "goals_per90",
    "assists_per90",
]


CATEGORICAL_FEATURES = [
    "league",
    "season",
    "position_group",
]


def prepare_ml_dataset(
    df: pd.DataFrame,
):

    df = df.copy()

    # Feature engineering
    df["log_minutes_played"] = np.log1p(
        df["minutes_played"]
    )

    required_cols = (
        NUMERIC_FEATURES
        + CATEGORICAL_FEATURES
        + [TARGET]
    )

    df = df.dropna(
        subset=required_cols
    ).copy()

    X = df[
        NUMERIC_FEATURES
        + CATEGORICAL_FEATURES
    ].copy()

    X = pd.get_dummies(
        X,
        columns=CATEGORICAL_FEATURES,
        drop_first=True,
    )

    y = df[TARGET].copy()

    return X, y, df