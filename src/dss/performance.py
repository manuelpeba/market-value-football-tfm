from __future__ import annotations

from dataclasses import dataclass

import pandas as pd
import streamlit as st


@st.cache_data(show_spinner=False)
def load_performance_layer():
    return pd.read_parquet(
        "data/processed/player_season_modeling_v13a.parquet"
    )


@dataclass
class PlayerPerformance:

    player_id_tm: int

    season: str

    club: str

    league: str

    age: float

    position: str | None

    position_group: str | None

    minutes_played: float | None

    goals: float | None

    assists: float | None

    xg: float | None

    xa: float | None

    market_value_eur: float | None

    valuation_date: str | None


def build_performance_lookup(df):

    df = df.copy()

    if "valuation_date" in df.columns:
        df["valuation_date"] = pd.to_datetime(
            df["valuation_date"],
            errors="coerce",
        )

    df = df.sort_values(
        [
            "player_id_tm",
            "valuation_date",
        ],
        ascending=[
            True,
            False,
        ],
    )

    latest = (
        df
        .drop_duplicates(
            "player_id_tm",
            keep="first",
        )
    )

    lookup = {}

    for _, r in latest.iterrows():

        lookup[int(r.player_id_tm)] = PlayerPerformance(

            player_id_tm=int(r.player_id_tm),

            season=r.get("season"),

            club=r.get("club"),

            league=r.get("league"),

            age=r.get("age"),

            position=r.get("position"),

            position_group=r.get("position_group"),

            minutes_played=r.get("minutes_played"),

            goals=r.get("goals"),

            assists=r.get("assists"),

            xg=r.get("xg"),

            xa=r.get("xa"),

            market_value_eur=r.get("market_value_eur"),

            valuation_date=str(r.get("valuation_date")),
        )

    return lookup


def get_latest_performance(player_id_tm, lookup):

    try:
        return lookup.get(int(player_id_tm))
    except Exception:
        return None