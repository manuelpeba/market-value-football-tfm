ECONOMETRIC_TARGET = "log_market_value_eur"


BASE_OLS_FEATURES = [
    "age",
    "log_minutes_played",
    "goals_per90",
    "assists_per90",
]


BASE_FIXED_EFFECTS = [
    "league",
    "position_group",
]


SEASON_FIXED_EFFECT = "season"


def build_ols_formula(
    include_season_fe: bool = True,
) -> str:
    """
    Build OLS formula for econometric market value model.

    Notes
    -----
    - include_season_fe=True is useful for explanatory/in-sample models.
    - include_season_fe=False is required for strict temporal validation
      when predicting an unseen future season.
    """

    numeric_terms = " + ".join(BASE_OLS_FEATURES)

    fixed_effects = BASE_FIXED_EFFECTS.copy()

    if include_season_fe:
        fixed_effects.append(SEASON_FIXED_EFFECT)

    fe_terms = " + ".join(
        [f"C({feature})" for feature in fixed_effects]
    )

    formula = (
        f"{ECONOMETRIC_TARGET} ~ "
        f"{numeric_terms} + "
        f"{fe_terms}"
    )

    return formula