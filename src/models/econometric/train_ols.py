import statsmodels.formula.api as smf

from src.models.econometric.specifications import (
    build_ols_formula,
)


def train_ols_model(df):
    formula = build_ols_formula()

    model = smf.ols(
        formula=formula,
        data=df,
    ).fit(cov_type="HC3")

    return model