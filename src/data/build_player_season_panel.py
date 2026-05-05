from pathlib import Path
import pandas as pd
from rapidfuzz import process, fuzz

from src.data.name_normalization import normalize_name

ROOT = Path(__file__).resolve().parents[2]


def load_data():
    fbref = pd.read_parquet(ROOT / "data/processed/fbref_features.parquet")
    tm = pd.read_parquet(ROOT / "data/processed/transfermarkt_features.parquet")

    return fbref, tm


def prepare_data(fbref, tm):
    fbref["player_name_norm"] = fbref["player_name"].apply(normalize_name)
    tm["player_name_norm"] = tm["player_name_norm"]  # ya viene normalizado

    return fbref, tm


def exact_matching(fbref, tm):
    df = fbref.merge(
        tm,
        on=["player_name_norm", "season"],
        how="left",
        suffixes=("_fbref", "_tm")
    )

    df["matching_method"] = "exact"
    df["matching_confidence"] = df["market_value_eur"].notna().astype(float)

    return df


def fuzzy_matching(df, tm):
    unmatched = df[df["market_value_eur"].isna()].copy()

    candidates = tm["player_name_norm"].unique()

    def match(row):
        name = row["player_name_norm"]
        season = row["season"]

        best_match, score, _ = process.extractOne(
            name,
            candidates,
            scorer=fuzz.token_sort_ratio
        )

        if score >= 90:
            tm_match = tm[
                (tm["player_name_norm"] == best_match) &
                (tm["season"] == season)
            ]

            if len(tm_match) > 0:
                return pd.Series([
                    tm_match.iloc[0]["market_value_eur"],
                    "fuzzy",
                    score / 100
                ])

        return pd.Series([None, None, 0])

    unmatched[["market_value_eur", "matching_method", "matching_confidence"]] = \
        unmatched.apply(match, axis=1)

    df.update(unmatched)

    return df


def build_panel():
    fbref, tm = load_data()
    fbref, tm = prepare_data(fbref, tm)

    df = exact_matching(fbref, tm)
    df = fuzzy_matching(df, tm)

    df["matching_status"] = df["market_value_eur"].notna()

    output_path = ROOT / "data/processed/player_season_panel.parquet"
    df.to_parquet(output_path, index=False)

    print("Panel construido")
    print(f"Rows: {len(df):,}")
    print(f"Match rate: {df['matching_status'].mean():.2%}")


if __name__ == "__main__":
    build_panel()