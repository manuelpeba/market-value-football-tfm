import pandas as pd


def extract_feature_importance(
    model,
    feature_names,
    model_name: str,
) -> pd.DataFrame:

    if not hasattr(model, "feature_importances_"):
        raise ValueError(
            f"{model_name} has no feature_importances_ attribute"
        )

    importance_df = pd.DataFrame({
        "feature": feature_names,
        "importance": model.feature_importances_,
    })

    importance_df["model"] = model_name

    importance_df = importance_df.sort_values(
        by="importance",
        ascending=False,
    ).reset_index(drop=True)

    return importance_df