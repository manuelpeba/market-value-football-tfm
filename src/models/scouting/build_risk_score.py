from pathlib import Path
import numpy as np
import pandas as pd


ROOT = Path(__file__).resolve().parents[3]

INPUT_PATH = ROOT / "reports" / "rankings" / "scouting_shortlist.csv"
OUTPUT_PATH = ROOT / "reports" / "rankings" / "scouting_shortlist_with_risk.csv"


def calculate_age_risk(age: pd.Series) -> pd.Series:
    age = pd.to_numeric(age, errors="coerce")

    risk = np.select(
        [
            age < 20,
            (age >= 20) & (age <= 23),
            (age > 23) & (age <= 26),
            (age > 26) & (age <= 30),
            age > 30,
        ],
        [35, 15, 20, 45, 80],
        default=50,
    )

    return pd.Series(risk, index=age.index)


def calculate_minutes_risk(minutes: pd.Series) -> pd.Series:
    minutes = pd.to_numeric(minutes, errors="coerce")

    risk = np.select(
        [
            minutes < 300,
            (minutes >= 300) & (minutes < 700),
            (minutes >= 700) & (minutes < 1200),
            (minutes >= 1200) & (minutes < 2000),
            minutes >= 2000,
        ],
        [90, 70, 45, 25, 10],
        default=60,
    )

    return pd.Series(risk, index=minutes.index)


def calculate_confidence_risk(confidence_score: pd.Series) -> pd.Series:
    confidence_score = pd.to_numeric(confidence_score, errors="coerce").fillna(50)
    return 100 - confidence_score.clip(0, 100)


def calculate_gap_extreme_risk(df: pd.DataFrame) -> pd.Series:
    """
    Calculate valuation-gap risk in percentage points.

    Project convention:
    market_value_gap_pct is stored as a ratio, where 0.25 means 25%.
    Business thresholds in this function are expressed in percentage points.
    """
    if {"market_value_gap_eur", "market_value_eur"}.issubset(df.columns):
        gap_eur = pd.to_numeric(
            df["market_value_gap_eur"],
            errors="coerce",
        )
        market_value_eur = pd.to_numeric(
            df["market_value_eur"],
            errors="coerce",
        )

        gap_percentage_points = pd.Series(
            np.where(
                market_value_eur > 0,
                gap_eur / market_value_eur * 100,
                np.nan,
            ),
            index=df.index,
            dtype="float64",
        )

    elif "market_value_gap_pct" in df.columns:
        gap_ratio = pd.to_numeric(
            df["market_value_gap_pct"],
            errors="coerce",
        )
        gap_percentage_points = gap_ratio * 100

    else:
        return pd.Series(50, index=df.index, dtype="float64")

    abs_gap = gap_percentage_points.abs()

    risk = np.select(
        [
            abs_gap < 25,
            (abs_gap >= 25) & (abs_gap < 75),
            (abs_gap >= 75) & (abs_gap < 150),
            abs_gap >= 150,
        ],
        [15, 30, 60, 85],
        default=50,
    )

    return pd.Series(risk, index=df.index, dtype="float64")


def assign_risk_level(risk_score: pd.Series) -> pd.Series:
    return pd.cut(
        risk_score,
        bins=[-0.01, 25, 50, 75, 100],
        labels=["Bajo", "Moderado", "Alto", "Muy alto"],
    ).astype(str)


def build_risk_score(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()

    required_columns = [
        "age",
        "minutes_played",
        "confidence_score",
    ]

    missing_columns = [col for col in required_columns if col not in df.columns]

    if missing_columns:
        raise KeyError(f"Missing required columns: {missing_columns}")

    df["risk_age_component"] = calculate_age_risk(df["age"])
    df["risk_minutes_component"] = calculate_minutes_risk(df["minutes_played"])
    df["risk_confidence_component"] = calculate_confidence_risk(df["confidence_score"])
    df["risk_gap_component"] = calculate_gap_extreme_risk(df)

    df["risk_score_raw"] = (
        0.25 * df["risk_age_component"]
        + 0.30 * df["risk_minutes_component"]
        + 0.30 * df["risk_confidence_component"]
        + 0.15 * df["risk_gap_component"]
    ).clip(0, 100).round(2)

    df["risk_score"] = (
        df["risk_score_raw"]
        .rank(pct=True, method="average")
        .mul(100)
        .round(2)
    )

    df["risk_level"] = assign_risk_level(df["risk_score"])

    if "opportunity_score" in df.columns:
        df["risk_adjusted_opportunity_score"] = (
            pd.to_numeric(df["opportunity_score"], errors="coerce")
            * (1 - df["risk_score"] / 100)
        ).round(2)

    return df


def main() -> None:
    if not INPUT_PATH.exists():
        raise FileNotFoundError(f"Input file not found: {INPUT_PATH}")

    df = pd.read_csv(INPUT_PATH)

    scored_df = build_risk_score(df)

    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    scored_df.to_csv(OUTPUT_PATH, index=False)

    print("Risk Score construido correctamente")
    print(f"Input: {INPUT_PATH}")
    print(f"Output: {OUTPUT_PATH}")
    print(f"Rows: {len(scored_df):,}")

    print("\nDistribución Risk Level:")
    print(scored_df["risk_level"].value_counts().sort_index())

    print("\nRisk Score Raw Summary")
    print(scored_df["risk_score_raw"].describe())

    print("\nRisk Score Relative Summary")
    print(scored_df["risk_score"].describe())


if __name__ == "__main__":
    main()