import statsmodels.formula.api as smf
from statsmodels.regression.linear_model import RegressionResultsWrapper

from src.models.econometric.specifications import build_ols_formula


def train_ols_model(
    df,
    include_season_fe: bool = True,
) -> RegressionResultsWrapper:
    formula = build_ols_formula(
        include_season_fe=include_season_fe,
    )

    model = smf.ols(
        formula=formula,
        data=df,
    ).fit(
        cov_type="HC3",
    )

    return model