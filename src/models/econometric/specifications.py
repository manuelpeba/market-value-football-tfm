ECONOMETRIC_TARGET = "log_market_value_eur"


BASE_OLS_FEATURES = [
    "age",
    "log_minutes_played",
    "goals_per90",
    "assists_per90",
]


FIXED_EFFECTS = [
    "league",
    "season",
    "position_group",
]


def build_ols_formula() -> str:
    numeric_terms = " + ".join(BASE_OLS_FEATURES)

    fe_terms = " + ".join(
        [f"C({feature})" for feature in FIXED_EFFECTS]
    )

    formula = (
        f"{ECONOMETRIC_TARGET} ~ "
        f"{numeric_terms} + "
        f"{fe_terms}"
    )

    return formula