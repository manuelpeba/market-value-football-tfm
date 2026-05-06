from pathlib import Path
import numpy as np
import pandas as pd
from rapidfuzz import process, fuzz

from src.data.name_normalization import normalize_name

ROOT = Path(__file__).resolve().parents[2]

FBREF_PATH = ROOT / "data/processed/fbref_features.parquet"
TM_PATH = ROOT / "data/processed/transfermarkt_features.parquet"
OUTPUT_PATH = ROOT / "data/processed/player_season_panel.parquet"

MAX_AGE_DIFF = 1.5
FUZZY_THRESHOLD = 92
MIN_CLUB_SCORE = 70


def get_first_existing_column(df: pd.DataFrame, candidates: list[str]) -> str:
    for col in candidates:
        if col in df.columns:
            return col
    raise KeyError(f"None of these columns found: {candidates}")


def prepare_fbref(fbref: pd.DataFrame) -> pd.DataFrame:
    fbref = fbref.copy()

    player_col = get_first_existing_column(
        fbref,
        ["player_name", "player_name_fbref", "Player", "player"],
    )

    if player_col != "player_name_fbref":
        fbref = fbref.rename(columns={player_col: "player_name_fbref"})

    fbref["player_name_norm"] = fbref["player_name_fbref"].apply(normalize_name)

    if "age" in fbref.columns and "age_fbref" not in fbref.columns:
        fbref = fbref.rename(columns={"age": "age_fbref"})

    if "season_start_year" in fbref.columns and "season_start_year_fbref" not in fbref.columns:
        fbref = fbref.rename(columns={"season_start_year": "season_start_year_fbref"})

    if "season" not in fbref.columns:
        raise KeyError("FBref dataset must contain 'season'.")

    return fbref


def prepare_transfermarkt(tm: pd.DataFrame) -> pd.DataFrame:
    tm = tm.copy()

    if "player_name_norm" not in tm.columns:
        tm["player_name_norm"] = tm["player_name"].apply(normalize_name)

    if "age" in tm.columns and "age_tm" not in tm.columns:
        tm = tm.rename(columns={"age": "age_tm"})

    if "season_start_year" in tm.columns and "season_start_year_tm" not in tm.columns:
        tm = tm.rename(columns={"season_start_year": "season_start_year_tm"})

    if "player_id" in tm.columns and "player_id_tm" not in tm.columns:
        tm = tm.rename(columns={"player_id": "player_id_tm"})

    if "player_name" in tm.columns and "player_name_tm" not in tm.columns:
        tm = tm.rename(columns={"player_name": "player_name_tm"})

    required_cols = [
        "player_id_tm",
        "player_name_tm",
        "player_name_norm",
        "season",
        "season_start_year_tm",
        "market_value_eur",
        "log_market_value_eur",
        "age_tm",
        "position_group",
    ]

    missing = [col for col in required_cols if col not in tm.columns]
    if missing:
        raise KeyError(f"Missing required Transfermarkt columns: {missing}")

    tm = tm.dropna(subset=["player_name_norm", "season", "market_value_eur"])
    tm = tm[tm["market_value_eur"] > 0]

    return tm


def candidate_age_filter(candidates: pd.DataFrame, age_fbref) -> pd.DataFrame:
    candidates = candidates.copy()

    if pd.isna(age_fbref):
        candidates["age_diff"] = np.nan
        return candidates

    candidates["age_diff"] = (candidates["age_tm"] - age_fbref).abs()
    return candidates[candidates["age_diff"] <= MAX_AGE_DIFF]


def choose_best_candidate(candidates: pd.DataFrame, club_fbref=None) -> pd.Series | None:
    if candidates.empty:
        return None

    candidates = candidates.copy()

    if "age_diff" not in candidates.columns:
        candidates["age_diff"] = np.nan

    if club_fbref is not None and "current_club_name_tm" in candidates.columns:
        club_norm = normalize_name(club_fbref)

        candidates["club_score"] = candidates["current_club_name_tm"].fillna("").apply(
            lambda x: fuzz.token_sort_ratio(club_norm, normalize_name(x))
        )

        candidates = candidates[candidates["club_score"] >= MIN_CLUB_SCORE]
    else:
        candidates["club_score"] = 0

    if candidates.empty:
        return None

    candidates["age_rank"] = candidates["age_diff"].fillna(999)

    candidates = candidates.sort_values(
        by=["club_score", "age_rank", "market_value_eur"],
        ascending=[False, True, False],
    )

    return candidates.iloc[0]


def empty_match() -> dict:
    return {
        "match_index": None,
        "matching_method": None,
        "matching_confidence": 0.0,
        "age_diff": np.nan,
        "club_score": np.nan,
    }


def match_one_player(row: pd.Series, tm_by_season: dict[str, pd.DataFrame]) -> dict:
    season = row["season"]
    name_norm = row["player_name_norm"]
    age_fbref = row.get("age_fbref", np.nan)
    club_fbref = row.get("club", None)

    season_candidates = tm_by_season.get(season)

    if season_candidates is None or season_candidates.empty:
        return empty_match()

    exact_candidates = season_candidates[
        season_candidates["player_name_norm"] == name_norm
    ].copy()

    exact_candidates = candidate_age_filter(exact_candidates, age_fbref)
    best_exact = choose_best_candidate(exact_candidates, club_fbref)

    if best_exact is not None:
        return {
            "match_index": best_exact.name,
            "matching_method": "exact_age_club_validated",
            "matching_confidence": 1.0,
            "age_diff": best_exact.get("age_diff", np.nan),
            "club_score": best_exact.get("club_score", np.nan),
        }

    names = season_candidates["player_name_norm"].dropna().unique().tolist()

    if not names:
        return empty_match()

    fuzzy = process.extractOne(
        name_norm,
        names,
        scorer=fuzz.token_sort_ratio,
    )

    if fuzzy is None:
        return empty_match()

    best_name, score, _ = fuzzy

    if score < FUZZY_THRESHOLD:
        return empty_match()

    fuzzy_candidates = season_candidates[
        season_candidates["player_name_norm"] == best_name
    ].copy()

    fuzzy_candidates = candidate_age_filter(fuzzy_candidates, age_fbref)
    best_fuzzy = choose_best_candidate(fuzzy_candidates, club_fbref)

    if best_fuzzy is not None:
        return {
            "match_index": best_fuzzy.name,
            "matching_method": "fuzzy_age_club_validated",
            "matching_confidence": score / 100,
            "age_diff": best_fuzzy.get("age_diff", np.nan),
            "club_score": best_fuzzy.get("club_score", np.nan),
        }

    return empty_match()


def build_player_season_panel() -> pd.DataFrame:
    fbref = pd.read_parquet(FBREF_PATH)
    tm = pd.read_parquet(TM_PATH)

    fbref = prepare_fbref(fbref)
    tm = prepare_transfermarkt(tm)

    tm_by_season = {
        season: season_df
        for season, season_df in tm.groupby("season", dropna=False)
    }

    print("Building validated player-season matching...")
    print(f"FBref rows: {len(fbref):,}")
    print(f"Transfermarkt rows: {len(tm):,}")
    print(f"Max age diff: {MAX_AGE_DIFF}")
    print(f"Min club score: {MIN_CLUB_SCORE}")
    print(f"Fuzzy threshold: {FUZZY_THRESHOLD}")

    match_rows = []

    for _, row in fbref.iterrows():
        match_rows.append(match_one_player(row, tm_by_season))

    matches = pd.DataFrame(match_rows, index=fbref.index)

    tm_selected_cols = [
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

    tm_selected_cols = [col for col in tm_selected_cols if col in tm.columns]
    tm_lookup = tm[tm_selected_cols].copy()

    matched_mask = matches["match_index"].notna()
    matched_indices = matches.loc[matched_mask, "match_index"].astype(int)

    matched_tm = tm_lookup.reindex(matched_indices)
    matched_tm.index = matches.loc[matched_mask].index

    cols_to_join = [
        col for col in matched_tm.columns
        if col not in ["season", "player_name_norm"]
        and col not in fbref.columns
    ]

    panel = fbref.copy()
    panel = panel.join(matched_tm[cols_to_join], how="left")

    panel["matching_method"] = matches["matching_method"]
    panel["matching_confidence"] = matches["matching_confidence"]
    panel["age_diff"] = matches["age_diff"]
    panel["club_score"] = matches["club_score"]
    panel["matching_status"] = panel["market_value_eur"].notna()

    dedup_cols = ["player_name_fbref", "season"]

    if "club" in panel.columns:
        dedup_cols.append("club")

    panel = panel.drop_duplicates(subset=dedup_cols)

    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    panel.to_parquet(OUTPUT_PATH, index=False)

    print("\nPanel construido")
    print(f"Rows: {len(panel):,}")
    print(f"Match rate: {panel['matching_status'].mean():.2%}")

    print("\nMatching method:")
    print(panel["matching_method"].value_counts(dropna=False))

    print("\nAge diff summary:")
    print(panel.loc[panel["matching_status"], "age_diff"].describe())

    print("\nClub score summary:")
    print(panel.loc[panel["matching_status"], "club_score"].describe())

    print(f"\nOutput: {OUTPUT_PATH}")

    return panel


if __name__ == "__main__":
    build_player_season_panel()