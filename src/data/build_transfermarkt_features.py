from pathlib import Path
import argparse
import numpy as np
import pandas as pd

from src.data.name_normalization import normalize_name


ROOT = Path(__file__).resolve().parents[2]


def resolve_paths(input_path: str | Path) -> tuple[Path, Path]:
    input_path = Path(input_path)

    if not input_path.is_absolute():
        input_path = ROOT / input_path

    if input_path.is_dir():
        valuations_path = input_path / "player_valuations.csv"
        players_path = input_path / "players.csv"
    else:
        valuations_path = input_path
        players_path = input_path.parent / "players.csv"

    if not valuations_path.exists():
        raise FileNotFoundError(f"Missing player_valuations.csv: {valuations_path}")

    if not players_path.exists():
        raise FileNotFoundError(f"Missing players.csv: {players_path}")

    return valuations_path, players_path


def season_from_date(date: pd.Timestamp) -> str:
    year = date.year

    if date.month >= 7:
        return f"{year}-{year + 1}"

    return f"{year - 1}-{year}"


def season_start_year_from_date(date: pd.Timestamp) -> int:
    if date.month >= 7:
        return date.year

    return date.year - 1


def map_position_group(position: object) -> str:
    if pd.isna(position):
        return "UNK"

    position = str(position).lower()

    if "goalkeeper" in position:
        return "GK"
    if "defender" in position:
        return "DEF"
    if "midfield" in position:
        return "MID"
    if "attack" in position or "forward" in position:
        return "ATT"

    return "UNK"


def calculate_age(date_of_birth: pd.Series, valuation_date: pd.Series) -> pd.Series:
    dob = pd.to_datetime(date_of_birth, errors="coerce")
    val_date = pd.to_datetime(valuation_date, errors="coerce")

    age = (val_date - dob).dt.days / 365.25

    return age


def build_transfermarkt_features(input_path: str | Path) -> pd.DataFrame:
    valuations_path, players_path = resolve_paths(input_path)

    valuations = pd.read_csv(valuations_path)
    players = pd.read_csv(players_path)

    valuations = valuations.copy()
    players = players.copy()

    valuations["valuation_date"] = pd.to_datetime(
        valuations["date"],
        errors="coerce",
    )

    valuations = valuations[valuations["valuation_date"].notna()].copy()

    valuations["season"] = valuations["valuation_date"].apply(season_from_date)
    valuations["season_start_year"] = valuations["valuation_date"].apply(
        season_start_year_from_date
    )

    valuations = valuations.rename(
        columns={
            "market_value_in_eur": "market_value_eur",
        }
    )

    player_cols = [
        "player_id",
        "name",
        "date_of_birth",
        "country_of_citizenship",
        "position",
        "sub_position",
        "foot",
        "height_in_cm",
        "current_club_id",
        "current_club_name",
        "current_club_domestic_competition_id",
    ]

    player_cols = [col for col in player_cols if col in players.columns]

    players = players[player_cols].copy()

    players = players.rename(
        columns={
            "name": "player_name",
            "country_of_citizenship": "nationality",
            "position": "position_tm",
            "sub_position": "sub_position_tm",
            "current_club_id": "current_club_id_tm",
            "current_club_name": "current_club_name_tm",
            "current_club_domestic_competition_id": "competition_id_tm",
        }
    )

    df = valuations.merge(
        players,
        on="player_id",
        how="left",
    )

    df = df[df["market_value_eur"].notna()].copy()
    df = df[df["market_value_eur"] > 0].copy()

    df["player_name_norm"] = df["player_name"].apply(normalize_name)

    df["age"] = calculate_age(
        df["date_of_birth"],
        df["valuation_date"],
    )

    df["position_group"] = df["position_tm"].apply(map_position_group)

    df["log_market_value_eur"] = np.log(df["market_value_eur"])

    df = df.sort_values(
        by=[
            "player_id",
            "valuation_date",
        ]
    ).copy()

    df["market_value_prev_eur"] = (
        df.groupby("player_id")["market_value_eur"].shift(1)
    )

    df["market_value_next_eur"] = (
        df.groupby("player_id")["market_value_eur"].shift(-1)
    )

    df["market_value_growth_1y"] = (
        df["market_value_next_eur"] - df["market_value_eur"]
    ) / df["market_value_eur"]

    df["delta_log_market_value_1y"] = (
        np.log(df["market_value_next_eur"]) - df["log_market_value_eur"]
    )

    df["source"] = "transfermarkt_kaggle_player_scores"

    df = df.rename(
        columns={
            "player_id": "player_id_tm",
            "player_name": "player_name_tm",
            "season_start_year": "season_start_year_tm",
            "age": "age_tm",
        }
    )

    keep_cols = [
        "player_id_tm",
        "player_name_tm",
        "player_name_norm",
        "season",
        "season_start_year_tm",
        "valuation_date",
        "market_value_eur",
        "log_market_value_eur",
        "market_value_prev_eur",
        "market_value_next_eur",
        "market_value_growth_1y",
        "delta_log_market_value_1y",
        "age_tm",
        "date_of_birth",
        "nationality",
        "position_tm",
        "sub_position_tm",
        "position_group",
        "foot",
        "height_in_cm",
        "current_club_name_tm",
        "current_club_id_tm",
        "competition_id_tm",
        "source",
    ]

    keep_cols = [col for col in keep_cols if col in df.columns]

    df = df[keep_cols].copy()

    return df


def main():
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--input",
        default="data/raw/transfermarkt/kaggle_player_scores",
    )

    parser.add_argument(
        "--output",
        default="data/processed/transfermarkt_features.parquet",
    )

    args = parser.parse_args()

    df = build_transfermarkt_features(args.input)

    output_path = Path(args.output)

    if not output_path.is_absolute():
        output_path = ROOT / output_path

    output_path.parent.mkdir(parents=True, exist_ok=True)
    df.to_parquet(output_path, index=False)

    print("Transfermarkt feature build completed")
    print(f"Rows: {len(df):,}")
    print(f"Columns: {len(df.columns):,}")
    print(f"Output: {output_path}")

    print("\nSeasons:")
    print(df["season"].value_counts().sort_index().tail(10))

    print("\nPosition groups:")
    print(df["position_group"].value_counts(dropna=False))


if __name__ == "__main__":
    main()