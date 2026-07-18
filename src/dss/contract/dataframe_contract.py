from __future__ import annotations

from collections.abc import Iterable

import numpy as np
import pandas as pd


# =========================================================
# TM.8.10 — DataFrame Contract Layer v1
#
# Structural safety rules:
# - guarantee required columns;
# - resolve only semantically equivalent aliases;
# - preserve unknown analytical values as NaN;
# - never fabricate business metrics with 0, 50 or 100;
# - remain schema- and value-idempotent.
# =========================================================


IDENTITY_FALLBACKS: dict[str, list[str]] = {
    "player_id_tm": [],
    "player_name": [
        "player_name_fbref",
        "player_name_tm",
        "display_player_name",
    ],
    "club": [
        "club_actual",
        "season_context_club",
    ],
    "league": [
        "season_context_league",
    ],
}


SCORING_FALLBACKS: dict[str, list[str]] = {
    "opportunity_score": [
        "display_opportunity_score",
    ],
    "confidence_score": [
        "display_confidence_score",
    ],
    "risk_score": [
        "display_risk_score",
    ],
}


# Legacy names still consumed by parts of the dashboard.
# Only equivalent authorities are allowed here.
COLUMN_FALLBACKS: dict[str, list[str]] = {
    "asset_roi_3y_pct": [
        "display_roi_pct",
        "roi_pct",
    ],
    "future_asset_score": [
        "display_future_asset_score",
    ],
    "projected_market_value_3y_eur": [
        "display_projected_market_value_3y_eur",
    ],
}


REQUIRED_COLUMNS: dict[str, list[str]] = {
    "identity": list(IDENTITY_FALLBACKS),
    "scoring": list(SCORING_FALLBACKS),
    "business": list(COLUMN_FALLBACKS),
}


NUMERIC_CONTRACT_COLUMNS = (
    REQUIRED_COLUMNS["scoring"]
    + REQUIRED_COLUMNS["business"]
)


def _resolve_column(
    df: pd.DataFrame,
    target: str,
    fallbacks: Iterable[str],
    *,
    default: object,
) -> None:
    """
    Guarantee a target column without fabricating analytical information.

    Existing target values remain authoritative. Missing target values may be
    completed only from explicitly declared equivalent aliases.
    """
    if target not in df.columns:
        df[target] = default

    for fallback in fallbacks:
        if fallback not in df.columns:
            continue

        df[target] = df[target].combine_first(
            df[fallback]
        )


def enforce_dataframe_contract(
    df: pd.DataFrame,
) -> pd.DataFrame:
    """
    Return a structurally safe DataFrame.

    The contract guarantees column availability but does not calculate,
    impute or infer business metrics. Unknown analytical values remain NaN.
    """
    contracted = df.copy()

    # -----------------------------
    # 1. Identity structural layer
    # -----------------------------
    for target, fallbacks in IDENTITY_FALLBACKS.items():
        _resolve_column(
            contracted,
            target,
            fallbacks,
            default=pd.NA,
        )

    # -----------------------------
    # 2. Scoring structural layer
    # -----------------------------
    for target, fallbacks in SCORING_FALLBACKS.items():
        _resolve_column(
            contracted,
            target,
            fallbacks,
            default=np.nan,
        )

    # -----------------------------
    # 3. Legacy business aliases
    # -----------------------------
    for target, fallbacks in COLUMN_FALLBACKS.items():
        _resolve_column(
            contracted,
            target,
            fallbacks,
            default=np.nan,
        )

    # -----------------------------
    # 4. Numeric type enforcement
    # -----------------------------
    for column in NUMERIC_CONTRACT_COLUMNS:
        contracted[column] = pd.to_numeric(
            contracted[column],
            errors="coerce",
        )

    return contracted


def safe_sort(
    df: pd.DataFrame,
    col: str,
    ascending: bool = False,
) -> pd.DataFrame:
    """
    Sort without mutating the input DataFrame.

    A missing sort variable is represented as unknown rather than zero.
    """
    result = df.copy()

    if col not in result.columns:
        result[col] = np.nan

    return result.sort_values(
        col,
        ascending=ascending,
        na_position="last",
    )


def safe_mean(
    df: pd.DataFrame,
    col: str,
) -> float:
    """
    Return the numeric mean or NaN when no authority is available.
    """
    if col not in df.columns:
        return float("nan")

    values = pd.to_numeric(
        df[col],
        errors="coerce",
    )

    if not values.notna().any():
        return float("nan")

    return float(values.mean())
