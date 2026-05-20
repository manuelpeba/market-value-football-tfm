from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parents[3]

INPUT_DIR = ROOT / "artifacts" / "feature_importance"

OUTPUT_TABLE = (
    ROOT
    / "reports"
    / "tables"
    / "explainability"
    / "feature_importance_comparison_top10.csv"
)

OUTPUT_FIGURE = (
    ROOT
    / "reports"
    / "figures"
    / "explainability"
    / "feature_importance_comparison_top10.png"
)


FILES = {
    "Random Forest":
        "random_forest_feature_importance.csv",

    "Tuned Random Forest":
        "tuned_random_forest_feature_importance.csv",

    "Tuned XGBoost":
        "tuned_xgboost_feature_importance.csv",

    "Tuned LightGBM":
        "tuned_lightgbm_feature_importance.csv",

    "Gradient Boosting":
        "gradient_boosting_feature_importance.csv"
}


def load_importance():

    dfs = []

    for model_name, filename in FILES.items():

        path = INPUT_DIR / filename

        if not path.exists():
            print(f"Skipping: {filename}")
            continue

        df = pd.read_csv(path)

        cols = [c.lower() for c in df.columns]

        if "feature" not in cols:
            raise ValueError(
                f"{filename} does not contain feature column"
            )

        importance_col = [
            c for c in df.columns
            if "importance" in c.lower()
        ][0]

        df = df.rename(
            columns={
                df.columns[0]: "feature",
                importance_col: "importance"
            }
        )

        df["model"] = model_name

        dfs.append(df)

    return pd.concat(dfs, ignore_index=True)


def create_summary(df):

    top = (
        df
        .groupby("feature")["importance"]
        .mean()
        .sort_values(ascending=False)
        .head(10)
        .reset_index()
    )

    return top


def plot_top(top):

    plt.figure(figsize=(10,6))

    plt.barh(
        top["feature"],
        top["importance"]
    )

    plt.xlabel("Mean importance")

    plt.ylabel("Feature")

    plt.title(
        "Top 10 Features Across ML Models"
    )

    plt.gca().invert_yaxis()

    OUTPUT_FIGURE.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    plt.tight_layout()

    plt.savefig(
        OUTPUT_FIGURE,
        dpi=300
    )

    plt.close()


def main():

    print("Loading feature importance files...")

    df = load_importance()

    top = create_summary(df)

    OUTPUT_TABLE.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    top.to_csv(
        OUTPUT_TABLE,
        index=False
    )

    plot_top(top)

    print("\nDone")
    print(f"Rows analyzed: {len(df):,}")
    print(f"Output table: {OUTPUT_TABLE}")
    print(f"Output figure: {OUTPUT_FIGURE}")

    print("\nTop features:")
    print(top)


if __name__ == "__main__":
    main()