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

    if "club" not in fbref.columns:
        raise KeyError("FBref dataset must contain 'club'.")

    return fbref


def prepare_transfermarkt(tm: pd.DataFrame) -> pd.DataFrame:
    tm = tm.copy()

    if "player_name_norm" not in tm.columns:
        tm["player_name_norm"] = tm["player_name_tm"].apply(normalize_name)

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
    tm = tm[tm["market_value_eur"] > 0].copy()

    return tm


def reduce_transfermarkt_search_space(
    fbref: pd.DataFrame,
    tm: pd.DataFrame,
) -> pd.DataFrame:
    tm = tm.copy()

    seasons = set(fbref["season"].dropna().unique())
    tm = tm[tm["season"].isin(seasons)].copy()

    if "age_fbref" in fbref.columns and "age_tm" in tm.columns:
        min_age = pd.to_numeric(fbref["age_fbref"], errors="coerce").min()
        max_age = pd.to_numeric(fbref["age_fbref"], errors="coerce").max()

        if pd.notna(min_age) and pd.notna(max_age):
            tm = tm[
                tm["age_tm"].between(
                    min_age - MAX_AGE_DIFF - 1,
                    max_age + MAX_AGE_DIFF + 1,
                )
            ].copy()

    return tm


def add_blocking_keys(df: pd.DataFrame, name_col: str) -> pd.DataFrame:
    df = df.copy()

    df["name_first_char"] = (
        df[name_col]
        .fillna("")
        .astype(str)
        .str[:1]
    )

    df["name_first_token"] = (
        df[name_col]
        .fillna("")
        .astype(str)
        .str.split()
        .str[0]
        .fillna("")
    )

    return df


def candidate_age_filter(candidates: pd.DataFrame, age_fbref) -> pd.DataFrame:
    candidates = candidates.copy()

    if pd.isna(age_fbref):
        candidates["age_diff"] = np.nan
        return candidates

    candidates["age_diff"] = (candidates["age_tm"] - age_fbref).abs()

    return candidates[candidates["age_diff"] <= MAX_AGE_DIFF]


def choose_best_candidate(
    candidates: pd.DataFrame,
    club_fbref=None,
    require_club_validation: bool = False,
) -> pd.Series | None:
    if candidates.empty:
        return None

    candidates = candidates.copy()

    if "age_diff" not in candidates.columns:
        candidates["age_diff"] = np.nan

    if club_fbref is not None and "current_club_name_tm" in candidates.columns:
        club_norm = normalize_name(club_fbref)

        candidates["club_score"] = (
            candidates["current_club_name_tm"]
            .fillna("")
            .apply(lambda x: fuzz.token_sort_ratio(club_norm, normalize_name(x)))
        )
    else:
        candidates["club_score"] = np.nan

    if require_club_validation:
        candidates = candidates[candidates["club_score"] >= MIN_CLUB_SCORE]

    if candidates.empty:
        return None

    candidates["age_rank"] = candidates["age_diff"].fillna(999)
    candidates["club_score_rank"] = candidates["club_score"].fillna(0)

    candidates = candidates.sort_values(
        by=["age_rank", "club_score_rank", "market_value_eur"],
        ascending=[True, False, False],
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


def build_tm_indexes(tm: pd.DataFrame) -> tuple[dict, dict, dict]:
    tm_by_exact_name = {
        key: group
        for key, group in tm.groupby(["season", "player_name_norm"], dropna=False)
    }

    tm_by_fuzzy_block = {
        key: group
        for key, group in tm.groupby(["season", "name_first_char"], dropna=False)
    }

    names_by_fuzzy_block = {}

    for key, group in tm_by_fuzzy_block.items():
        names_by_fuzzy_block[key] = (
            group["player_name_norm"]
            .dropna()
            .unique()
            .tolist()
        )

    return tm_by_exact_name, tm_by_fuzzy_block, names_by_fuzzy_block


def match_one_player(
    row: pd.Series,
    tm_by_exact_name: dict,
    tm_by_fuzzy_block: dict,
    names_by_fuzzy_block: dict,
) -> dict:
    season = row["season"]
    name_norm = row["player_name_norm"]
    first_char = row["name_first_char"]
    age_fbref = row.get("age_fbref", np.nan)
    club_fbref = row.get("club", None)

    # 1. Exact name + season
    exact_candidates = tm_by_exact_name.get((season, name_norm))

    if exact_candidates is not None and not exact_candidates.empty:
        exact_candidates = candidate_age_filter(exact_candidates, age_fbref)

        best_exact = choose_best_candidate(
            candidates=exact_candidates,
            club_fbref=club_fbref,
            require_club_validation=False,
        )

        if best_exact is not None:
            club_score = best_exact.get("club_score", np.nan)

            method = (
                "exact_age_club_validated"
                if pd.notna(club_score) and club_score >= MIN_CLUB_SCORE
                else "exact_age_validated"
            )

            confidence = 1.0 if method == "exact_age_club_validated" else 0.85

            return {
                "match_index": best_exact.name,
                "matching_method": method,
                "matching_confidence": confidence,
                "age_diff": best_exact.get("age_diff", np.nan),
                "club_score": club_score,
            }

    # 2. Fuzzy name only within season + first character block
    block_key = (season, first_char)
    block_candidates = tm_by_fuzzy_block.get(block_key)

    if block_candidates is None or block_candidates.empty:
        return empty_match()

    names = names_by_fuzzy_block.get(block_key, [])

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

    fuzzy_candidates = block_candidates[
        block_candidates["player_name_norm"] == best_name
    ].copy()

    fuzzy_candidates = candidate_age_filter(fuzzy_candidates, age_fbref)

    best_fuzzy = choose_best_candidate(
        candidates=fuzzy_candidates,
        club_fbref=club_fbref,
        require_club_validation=True,
    )

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

    print("Building validated player-season matching...")
    print(f"FBref rows: {len(fbref):,}")
    print(f"Transfermarkt rows before filtering: {len(tm):,}")
    print(f"Max age diff: {MAX_AGE_DIFF}")
    print(f"Min club score: {MIN_CLUB_SCORE}")
    print(f"Fuzzy threshold: {FUZZY_THRESHOLD}")

    tm = reduce_transfermarkt_search_space(fbref, tm)

    fbref = add_blocking_keys(fbref, "player_name_norm")
    tm = add_blocking_keys(tm, "player_name_norm")

    print(f"Transfermarkt rows after filtering: {len(tm):,}")

    tm_by_exact_name, tm_by_fuzzy_block, names_by_fuzzy_block = build_tm_indexes(tm)

    match_rows = []
    total = len(fbref)

    for i, (_, row) in enumerate(fbref.iterrows(), start=1):
        match_rows.append(
            match_one_player(
                row=row,
                tm_by_exact_name=tm_by_exact_name,
                tm_by_fuzzy_block=tm_by_fuzzy_block,
                names_by_fuzzy_block=names_by_fuzzy_block,
            )
        )

        if i % 1000 == 0:
            print(f"Matched {i:,}/{total:,} rows...")

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

    panel = panel.drop(
        columns=[
            "name_first_char",
            "name_first_token",
        ],
        errors="ignore",
    )

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

    print("\nMatch rate by season:")
    print(
        panel.groupby("season")["matching_status"]
        .agg(["count", "sum", "mean"])
        .sort_index()
    )

    print("\nMatch rate by league:")
    print(
        panel.groupby("league")["matching_status"]
        .agg(["count", "sum", "mean"])
        .sort_values("mean", ascending=False)
    )

    print(f"\nOutput: {OUTPUT_PATH}")

    return panel


if __name__ == "__main__":
    build_player_season_panel()