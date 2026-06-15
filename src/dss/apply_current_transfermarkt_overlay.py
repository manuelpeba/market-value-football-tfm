from pathlib import Path
import numpy as np
import pandas as pd
import unicodedata
import re


ROOT = Path(__file__).resolve().parents[2]

TM_RAW_DIR = ROOT / "data" / "raw" / "transfermarkt" / "kaggle_player_scores"
VALUATIONS_PATH = TM_RAW_DIR / "player_valuations.csv"
PLAYERS_PATH = TM_RAW_DIR / "players.csv"

TARGET_FILES = [
    ROOT / "reports" / "dss" / "global_prospect_universe.csv",
    ROOT / "reports" / "tm3_contract_intelligence" / "contract_intelligence_dataset.csv",
    ROOT / "reports" / "strategy" / "transfer_portfolio_dataset.csv",
]

COMPETITION_TO_LEAGUE = {
    "GB1": "Premier League",
    "ES1": "LaLiga",
    "L1": "Bundesliga",
    "IT1": "Serie A",
    "FR1": "Ligue 1",
    "NL1": "Eredivisie",
    "PO1": "Liga Portugal",
    "BE1": "Belgian Pro League",
    "A1": "Austrian Bundesliga",
    "GB2": "EFL Championship",
    "ES2": "Spanish Segunda División",
}

ALLOWED_PROJECT_LEAGUES = {
    "Premier League",
    "LaLiga",
    "Bundesliga",
    "Serie A",
    "Ligue 1",
    "Eredivisie",
    "Liga Portugal",
    "Belgian Pro League",
    "Austrian Bundesliga",
    "EFL Championship",
    "Spanish Segunda División",
}


def normalize_key(value: object) -> str:
    if pd.isna(value):
        return ""
    text = str(value).strip().lower()
    text = unicodedata.normalize("NFKD", text)
    text = "".join(ch for ch in text if not unicodedata.combining(ch))
    text = re.sub(r"[^a-z0-9 ]+", " ", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text


def current_age_from_dob(date_of_birth: object, reference_date: str = "2026-06-15") -> float:
    dob = pd.to_datetime(date_of_birth, errors="coerce")
    ref = pd.to_datetime(reference_date)
    if pd.isna(dob):
        return np.nan
    return round((ref - dob).days / 365.25, 2)


def first_existing_column(df: pd.DataFrame, candidates: list[str]) -> str | None:
    for col in candidates:
        if col in df.columns:
            return col
    return None


def build_current_tm_overlay() -> pd.DataFrame:
    if not VALUATIONS_PATH.exists():
        raise FileNotFoundError(f"Missing valuations file: {VALUATIONS_PATH}")

    if not PLAYERS_PATH.exists():
        raise FileNotFoundError(f"Missing players file: {PLAYERS_PATH}")

    valuations = pd.read_csv(VALUATIONS_PATH)
    players = pd.read_csv(PLAYERS_PATH)

    required_valuations = [
        "player_id",
        "date",
        "market_value_in_eur",
        "current_club_name",
        "player_club_domestic_competition_id",
    ]

    required_players = [
        "player_id",
        "name",
        "date_of_birth",
        "current_club_name",
    ]

    missing_val = [c for c in required_valuations if c not in valuations.columns]
    missing_players = [c for c in required_players if c not in players.columns]

    if missing_val:
        raise ValueError(f"Missing required columns in player_valuations.csv: {missing_val}")

    if missing_players:
        raise ValueError(f"Missing required columns in players.csv: {missing_players}")

    valuations = valuations.copy()
    players = players.copy()

    valuations["valuation_date_dt"] = pd.to_datetime(
        valuations["date"],
        errors="coerce",
    )

    valuations["market_value_in_eur"] = pd.to_numeric(
        valuations["market_value_in_eur"],
        errors="coerce",
    )

    valuations = valuations[
        valuations["valuation_date_dt"].notna()
        & valuations["market_value_in_eur"].notna()
        & (valuations["market_value_in_eur"] > 0)
    ].copy()

    latest = (
        valuations.sort_values(
            ["player_id", "valuation_date_dt"],
            ascending=[True, False],
        )
        .drop_duplicates("player_id", keep="first")
        .copy()
    )

    players_keep = [
        c
        for c in [
            "player_id",
            "name",
            "date_of_birth",
            "current_club_name",
            "current_club_id",
            "current_club_domestic_competition_id",
        ]
        if c in players.columns
    ]

    overlay = latest.merge(
        players[players_keep],
        on="player_id",
        how="left",
        suffixes=("_valuation", "_player"),
    )

    overlay["player_name_fbref"] = overlay["name"]
    overlay["name_key"] = overlay["player_name_fbref"].map(normalize_key)

    overlay["tm_current_club"] = overlay["current_club_name_valuation"].fillna(
        overlay.get("current_club_name_player")
    )

    valuation_comp = overlay["player_club_domestic_competition_id"]

    if "current_club_domestic_competition_id" in overlay.columns:
        player_comp = overlay["current_club_domestic_competition_id"]
        comp = valuation_comp.fillna(player_comp)
    else:
        comp = valuation_comp

    overlay["tm_current_league"] = comp.map(COMPETITION_TO_LEAGUE).fillna(comp)

    overlay = overlay[
        overlay["tm_current_league"].isin(ALLOWED_PROJECT_LEAGUES)
    ].copy()

    overlay["tm_current_season"] = overlay["valuation_date_dt"].apply(
        lambda d: f"{d.year}-{d.year + 1}" if d.month >= 7 else f"{d.year - 1}-{d.year}"
    )

    overlay["tm_current_market_value_eur"] = overlay["market_value_in_eur"]
    overlay["tm_current_valuation_date"] = overlay["valuation_date_dt"].dt.strftime("%Y-%m-%d")
    overlay["tm_date_of_birth"] = overlay["date_of_birth"]
    overlay["current_age"] = overlay["date_of_birth"].map(current_age_from_dob)

    overlay = overlay[
        [
            "name_key",
            "player_name_fbref",
            "tm_current_club",
            "tm_current_league",
            "tm_current_season",
            "tm_current_market_value_eur",
            "tm_current_valuation_date",
            "tm_date_of_birth",
            "current_age",
        ]
    ].copy()

    return overlay


def apply_overlay_to_file(path: Path, overlay: pd.DataFrame) -> None:
    if not path.exists():
        print(f"[SKIP] Missing file: {path}")
        return

    df = pd.read_csv(path)

    if df.empty:
        print(f"[SKIP] Empty file: {path}")
        return

    name_col = first_existing_column(
        df,
        ["player_name_fbref", "player_name", "player", "name"],
    )

    if name_col is None:
        print(f"[SKIP] No player name column in: {path}")
        return

    df = df.copy()

    previous_overlay_cols = [
        "tm_current_club",
        "tm_current_league",
        "tm_current_season",
        "tm_current_market_value_eur",
        "tm_current_valuation_date",
        "tm_date_of_birth",
        "current_age",
        "club_matches_current_tm",
        "player_name_fbref_overlay",
        "current_club_name_tm_overlay",
        "tm_overlay_source",
        "tm_overlay_applied",
    ]

    previous_overlay_cols = [c for c in previous_overlay_cols if c in df.columns]

    if previous_overlay_cols:
        df = df.drop(columns=previous_overlay_cols)

    df["name_key"] = df[name_col].map(normalize_key)

    df = df.merge(
        overlay,
        on="name_key",
        how="inner",
        suffixes=("", "_overlay"),
    )

    has_overlay = df["tm_current_market_value_eur"].notna()

    for col in [
        "club",
        "league",
        "season",
        "age",
        "market_value_eur",
        "current_club_name",
        "current_club_name_tm",
    ]:
        if col in df.columns and f"{col}_before_tm_overlay" not in df.columns:
            df[f"{col}_before_tm_overlay"] = df[col]

    text_cols = [
        "club",
        "league",
        "season",
        "current_club_name",
        "current_club_name_tm",
    ]

    numeric_cols = [
        "age",
        "market_value_eur",
    ]

    for col in text_cols:
        if col not in df.columns:
            df[col] = pd.Series(pd.NA, index=df.index, dtype="object")
        else:
            df[col] = df[col].astype("object")

    for col in numeric_cols:
        if col not in df.columns:
            df[col] = np.nan
        else:
            df[col] = pd.to_numeric(df[col], errors="coerce")

    df.loc[has_overlay, "club"] = df.loc[has_overlay, "tm_current_club"]
    df.loc[has_overlay, "league"] = df.loc[has_overlay, "tm_current_league"]
    df.loc[has_overlay, "season"] = df.loc[has_overlay, "tm_current_season"]
    df.loc[has_overlay, "market_value_eur"] = df.loc[
        has_overlay,
        "tm_current_market_value_eur",
    ]

    df.loc[has_overlay & df["current_age"].notna(), "age"] = df.loc[
        has_overlay & df["current_age"].notna(),
        "current_age",
    ]

    if "current_club_name_tm" in df.columns:
        df.loc[has_overlay, "current_club_name_tm"] = df.loc[
            has_overlay,
            "tm_current_club",
        ]

    if "current_club_name" in df.columns:
        df.loc[has_overlay, "current_club_name"] = df.loc[
            has_overlay,
            "tm_current_club",
        ]

    df["tm_current_club"] = df["tm_current_club"].astype("object")
    df["tm_current_league"] = df["tm_current_league"].astype("object")
    df["tm_current_season"] = df["tm_current_season"].astype("object")

    df.loc[~has_overlay, "tm_current_club"] = pd.NA
    df.loc[~has_overlay, "tm_current_league"] = pd.NA
    df.loc[~has_overlay, "tm_current_season"] = pd.NA

    df["tm_current_market_value_eur"] = pd.to_numeric(
        df["tm_current_market_value_eur"],
        errors="coerce",
    )

    df["tm_current_valuation_date"] = pd.to_datetime(
        df["tm_current_valuation_date"],
        errors="coerce",
    ).dt.strftime("%Y-%m-%d")

    df.loc[~has_overlay, "tm_current_valuation_date"] = pd.NA

    pred_col = first_existing_column(
        df,
        [
            "predicted_market_value_eur",
            "predicted_market_value_ml_eur",
            "expected_market_value_eur",
        ],
    )

    if pred_col and "market_value_eur" in df.columns:
        observed = pd.to_numeric(df["market_value_eur"], errors="coerce")
        predicted = pd.to_numeric(df[pred_col], errors="coerce")

        df["market_value_gap_eur"] = predicted - observed
        df["market_value_gap_pct"] = np.where(
            observed > 0,
            df["market_value_gap_eur"] / observed,
            np.nan,
        )

    df["tm_overlay_applied"] = has_overlay
    df["tm_overlay_source"] = np.where(
        has_overlay,
        "kaggle_player_scores_latest_available_valuation",
        "not_matched",
    )

    drop_cols = [
        "player_name_fbref_overlay",
        "current_club_name_tm_overlay",
    ]

    drop_cols = [c for c in drop_cols if c in df.columns]

    if drop_cols:
        df = df.drop(columns=drop_cols)

    if df.columns.duplicated().any():
        df = df.loc[:, ~df.columns.duplicated()]

    df.to_csv(path, index=False, encoding="utf-8-sig")

    matched = int(has_overlay.sum())

    print(f"[OK] {path.relative_to(ROOT)}")
    print(f"     rows={len(df):,} | overlay_matched={matched:,}")

    sample = df[
        df[name_col]
        .astype(str)
        .str.contains("Woltemade|Pau Victor|Pau Víctor", case=False, na=False)
    ]

    if not sample.empty:
        cols = [
            c
            for c in [
                name_col,
                "club",
                "league",
                "season",
                "age",
                "market_value_eur",
                "tm_current_club",
                "tm_current_league",
                "tm_current_market_value_eur",
                "tm_current_valuation_date",
                "club_before_tm_overlay",
                "league_before_tm_overlay",
                "season_before_tm_overlay",
                "age_before_tm_overlay",
                "market_value_eur_before_tm_overlay",
                "tm_overlay_applied",
            ]
            if c in sample.columns
        ]

        print(sample[cols].head(12).to_string(index=False))


def main() -> None:
    overlay = build_current_tm_overlay()

    print("=" * 100)
    print("CURRENT TRANSFERMARKT OVERLAY")
    print("=" * 100)
    print(f"overlay rows: {len(overlay):,}")

    qa = overlay[
        overlay["player_name_fbref"].astype(str).str.contains(
            "Woltemade|Pau Victor|Pau Víctor",
            case=False,
            na=False,
        )
    ]

    if not qa.empty:
        print("\nQA overlay sample:")
        print(
            qa[
                [
                    "player_name_fbref",
                    "tm_current_club",
                    "tm_current_league",
                    "tm_current_season",
                    "current_age",
                    "tm_current_market_value_eur",
                    "tm_current_valuation_date",
                ]
            ].to_string(index=False)
        )

    print("\n" + "=" * 100)
    print("APPLYING OVERLAY TO DSS ARTEFACTS")
    print("=" * 100)

    for path in TARGET_FILES:
        apply_overlay_to_file(path, overlay)


if __name__ == "__main__":
    main()