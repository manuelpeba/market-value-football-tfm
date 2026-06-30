import pandas as pd


DSS_PATH = "reports/dss/global_prospect_universe.csv"


def test_display_context_matches_current_snapshot_when_available():
    df = pd.read_csv(DSS_PATH)

    required = {
        "display_club",
        "display_league",
        "current_club_snapshot",
        "current_league_snapshot",
    }
    missing = required - set(df.columns)
    assert not missing, f"Missing required display contract columns: {sorted(missing)}"

    has_snapshot_club = df["current_club_snapshot"].notna()
    has_snapshot_league = df["current_league_snapshot"].notna()

    club_mismatch = df[
        has_snapshot_club
        & df["display_club"].fillna("").astype(str).ne(df["current_club_snapshot"].fillna("").astype(str))
    ]

    league_mismatch = df[
        has_snapshot_league
        & df["display_league"].fillna("").astype(str).ne(df["current_league_snapshot"].fillna("").astype(str))
    ]

    assert club_mismatch.empty, club_mismatch[
        ["player_name_fbref", "display_club", "current_club_snapshot", "club", "season_context_club"]
    ].head(20).to_string(index=False)

    assert league_mismatch.empty, league_mismatch[
        ["player_name_fbref", "display_league", "current_league_snapshot", "league", "season_context_league"]
    ].head(20).to_string(index=False)


def test_context_change_control_columns_exist():
    df = pd.read_csv(DSS_PATH)

    required = {
        "context_changed",
        "club_context_changed",
        "league_context_changed",
        "valuation_context",
        "gap_interpretation_status",
    }

    missing = required - set(df.columns)
    assert not missing, f"Missing required TM.8.8 context governance columns: {sorted(missing)}"
