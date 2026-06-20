from pathlib import Path
import streamlit as st

ASSETS_DIR = Path("app/assets")

CLUB_DIR = ASSETS_DIR / "clubs"
LEAGUE_DIR = ASSETS_DIR / "leagues"
PLACEHOLDER_DIR = ASSETS_DIR / "placeholders"


@st.cache_data
def get_club_logo(club_name: str):

    if not club_name:
        return str(PLACEHOLDER_DIR / "club.png")

    filename = (
        club_name.lower()
        .replace(".", "")
        .replace(" ", "_")
        .replace("-", "_")
    )

    path = CLUB_DIR / f"{filename}.png"

    if path.exists():
        return str(path)

    return str(PLACEHOLDER_DIR / "club.png")


@st.cache_data
def get_league_logo(league_name: str):

    mapping = {
        "Premier League": "premier_league.png",
        "LaLiga": "laliga.png",
        "Bundesliga": "bundesliga.png",
        "Serie A": "serie_a.png",
        "Ligue 1": "ligue_1.png",
        "Eredivisie": "eredivisie.png",
        "Liga Portugal": "liga_portugal.png",
        "Belgian Pro League": "belgian_pro_league.png",
        "Austrian Bundesliga": "austrian_bundesliga.png",
    }

    league_name = str(league_name or "").strip()

    file_name = mapping.get(league_name)

    if not file_name:
        league_name_lower = league_name.lower()
        file_name = next(
            (
                asset_file
                for league_label, asset_file in mapping.items()
                if league_label.lower() in league_name_lower
            ),
            None,
        )

    if not file_name:
        return str(PLACEHOLDER_DIR / "league.png")

    path = LEAGUE_DIR / file_name

    if path.exists():
        return str(path)

    return str(PLACEHOLDER_DIR / "league.png")