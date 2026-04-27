from pathlib import Path
import pandas as pd


REQUIRED_TRANSFERMARKT_COLUMNS = [
    "player_name",
    "season",
    "age",
    "position",
    "club",
    "league",
    "market_value_eur",
]


def validate_required_columns(df: pd.DataFrame, required_columns: list[str]) -> None:
    missing = [col for col in required_columns if col not in df.columns]

    if missing:
        raise ValueError(f"Missing required columns: {missing}")


def validate_not_empty(df: pd.DataFrame) -> None:
    if df.empty:
        raise ValueError("Dataset is empty.")


def validate_transfermarkt_schema(df: pd.DataFrame) -> None:
    validate_not_empty(df)
    validate_required_columns(df, REQUIRED_TRANSFERMARKT_COLUMNS)


def load_and_validate_transfermarkt(path: str | Path) -> pd.DataFrame:
    path = Path(path)

    if path.suffix == ".csv":
        df = pd.read_csv(path)
    elif path.suffix == ".parquet":
        df = pd.read_parquet(path)
    else:
        raise ValueError(f"Unsupported file format: {path.suffix}")

    validate_transfermarkt_schema(df)

    return df
