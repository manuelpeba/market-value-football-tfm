from pathlib import Path

import pandas as pd

from src.models.scouting.build_risk_score import build_risk_score


SCORING_PATH = Path("reports/rankings/scoring_dataset_opportunity.csv")
PORTFOLIO_PATH = Path("reports/strategy/transfer_portfolio_dataset.csv")
OUTPUT_PATH = Path("reports/dss/global_prospect_universe.csv")


PRODUCTIVE_MODEL = "XGBoost"
PRODUCTIVE_FEATURE_SET = "B_v13B_advanced"


PORTFOLIO_COLUMNS = [
    "player_name_fbref",
    "expected_roi",
    "expected_upside",
    "player_level_tier",
    "player_level_rank",
    "portfolio_value_score",
    "is_eligible_portfolio",
    "portfolio_cost",
    "upside_score_norm",
]


def main() -> None:
    scoring = pd.read_csv(SCORING_PATH)
    portfolio = pd.read_csv(PORTFOLIO_PATH)

    # 1. Keep only the official productive scoring layer
    dss = scoring[
        (scoring["model"] == PRODUCTIVE_MODEL)
        & (scoring["feature_set"] == PRODUCTIVE_FEATURE_SET)
    ].copy()

    # 2. Preserve previous club information when duplicated players exist
    duplicated_players = dss[dss.duplicated("player_name_fbref", keep=False)].copy()

    previous_clubs = (
        duplicated_players
        .groupby("player_name_fbref")["club"]
        .apply(lambda x: " | ".join(sorted(set(x.dropna().astype(str)))))
        .reset_index(name="club_history")
    )

    # 3. Keep one row per player:
    #    priority = highest opportunity_score, then highest predicted value
    dss = (
        dss.sort_values(
            by=["player_name_fbref", "opportunity_score", "predicted_market_value_eur"],
            ascending=[True, False, False],
        )
        .drop_duplicates(subset=["player_name_fbref"], keep="first")
        .copy()
    )

    dss = dss.rename(columns={"club": "club_actual"})

    dss = dss.merge(
        previous_clubs,
        on="player_name_fbref",
        how="left",
    )

    dss["club_anterior"] = dss.apply(
        lambda row: (
            row["club_history"].replace(str(row["club_actual"]), "").replace(" |  | ", " | ").strip(" |")
            if pd.notna(row.get("club_history"))
            else pd.NA
        ),
        axis=1,
    )

    dss = dss.drop(columns=["club_history"])

    # 4. Prepare portfolio layer
    portfolio_cols = [c for c in PORTFOLIO_COLUMNS if c in portfolio.columns]

    portfolio_layer = (
        portfolio[portfolio_cols]
        .sort_values(
            by=[c for c in ["player_name_fbref", "portfolio_value_score"] if c in portfolio.columns],
            ascending=[True, False] if "portfolio_value_score" in portfolio.columns else True,
        )
        .drop_duplicates(subset=["player_name_fbref"], keep="first")
        .copy()
    )

    # 5. Merge portfolio features
    dss = dss.merge(
        portfolio_layer,
        on="player_name_fbref",
        how="left",
        suffixes=("", "_portfolio"),
    )

    # 6. Build the official risk layer over the complete productive universe.
    # Risk percentiles must be estimated after the one-row-per-player universe
    # has been resolved, not copied from a partial historical shortlist.
    dss = build_risk_score(dss)

    required_risk_columns = [
        "risk_age_component",
        "risk_minutes_component",
        "risk_confidence_component",
        "risk_gap_component",
        "risk_score_raw",
        "risk_score",
        "risk_level",
        "risk_adjusted_opportunity_score",
    ]

    missing_risk_columns = [
        column
        for column in required_risk_columns
        if column not in dss.columns
    ]

    if missing_risk_columns:
        raise RuntimeError(
            "Risk layer is incomplete. "
            f"Missing columns: {missing_risk_columns}"
        )

    risk_score = pd.to_numeric(
        dss["risk_score"],
        errors="coerce",
    )

    risk_score_raw = pd.to_numeric(
        dss["risk_score_raw"],
        errors="coerce",
    )

    risk_gap_component = pd.to_numeric(
        dss["risk_gap_component"],
        errors="coerce",
    )

    risk_validation_errors = []

    if risk_score.isna().any():
        risk_validation_errors.append(
            "risk_score contains null values"
        )

    if not risk_score.dropna().between(0, 100).all():
        risk_validation_errors.append(
            "risk_score contains values outside [0, 100]"
        )

    if risk_score.eq(0).all():
        risk_validation_errors.append(
            "risk_score is degenerate: all values are zero"
        )

    if risk_score.nunique(dropna=True) <= 10:
        risk_validation_errors.append(
            "risk_score has insufficient variation"
        )

    if risk_score_raw.nunique(dropna=True) <= 10:
        risk_validation_errors.append(
            "risk_score_raw has insufficient variation"
        )

    if risk_gap_component.nunique(dropna=True) < 4:
        risk_validation_errors.append(
            "risk_gap_component does not cover all expected bands"
        )

    if dss["risk_level"].isna().any():
        risk_validation_errors.append(
            "risk_level contains null values"
        )

    if risk_validation_errors:
        raise RuntimeError(
            "Risk layer validation failed: "
            + "; ".join(risk_validation_errors)
        )

    # 7. Add DSS metadata
    dss["dss_entity"] = "player"
    dss["dss_universe"] = "global_prospect_universe"
    dss["dss_model"] = PRODUCTIVE_MODEL
    dss["dss_feature_set"] = PRODUCTIVE_FEATURE_SET

    # 8. Sort for operational use
    if "opportunity_score" in dss.columns:
        dss = dss.sort_values("opportunity_score", ascending=False)

    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    dss.to_csv(OUTPUT_PATH, index=False)

    print("Saved:", OUTPUT_PATH)
    print("Rows:", len(dss))
    print("Unique players:", dss["player_name_fbref"].nunique())
    print("Columns:", len(dss.columns))

    print("\nAge range:")
    print(dss["age"].min(), "->", dss["age"].max())

    print("\nLeagues:", dss["league"].nunique())

    print("\nTop columns added:")
    for col in [
        "club_actual",
        "club_anterior",
        "expected_roi",
        "expected_upside",
        "player_level_tier",
        "portfolio_value_score",
        "dss_entity",
    ]:
        print(col, "YES" if col in dss.columns else "NO")


if __name__ == "__main__":
    main()
