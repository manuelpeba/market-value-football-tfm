from rapidfuzz import fuzz


def compute_name_similarity(name1: str, name2: str) -> float:
    return fuzz.token_sort_ratio(name1, name2) / 100.0


def compute_matching_score(row) -> float:
    score = 0

    # name similarity
    score += row["name_similarity"] * 0.6

    # same club
    if row["club_tm"] == row["squad"]:
        score += 0.2

    # same age
    if row["age_tm"] == row["age_fbref"]:
        score += 0.2

    return score
