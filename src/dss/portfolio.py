from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd


ROOT = Path(__file__).resolve().parents[2]

PORTFOLIO_PATH = ROOT / "reports" / "strategy" / "transfer_portfolio_dataset.csv"
DSS_FALLBACK_PATH = ROOT / "reports" / "dss" / "global_prospect_universe.csv"


@dataclass(frozen=True)
class PlayerPortfolio:
    player_id_tm: int | None
    predicted_market_value_eur: float | None = None
    market_value_gap_eur: float | None = None
    market_value_gap_pct: float | None = None
    roi_pct: float | None = None
    roi_score: float | None = None
    upside_eur: float | None = None
    future_asset_score: float | None = None
    risk_adjusted_opportunity_score: float | None = None
    executive_decision_score: float | None = None
    portfolio_score_conservative: float | None = None
    portfolio_score_balanced: float | None = None
    portfolio_score_aggressive: float | None = None
    portfolio_cost_eur: float | None = None


def _first_existing(df: pd.DataFrame, candidates: list[str]) -> str | None:
    return next((c for c in candidates if c in df.columns), None)


def _to_float(value: Any) -> float | None:
    if value is None:
        return None
    try:
        if pd.isna(value):
            return None
        x = float(value)
        if not np.isfinite(x):
            return None
        return x
    except Exception:
        return None


def _to_int(value: Any) -> int | None:
    try:
        if pd.isna(value):
            return None
        return int(float(value))
    except Exception:
        return None


def _coalesce(row: pd.Series, candidates: list[str]) -> float | None:
    for col in candidates:
        if col in row.index:
            value = _to_float(row[col])
            if value is not None:
                return value
    return None


def load_portfolio_layer(
    portfolio_path: Path | str = PORTFOLIO_PATH,
    fallback_path: Path | str = DSS_FALLBACK_PATH,
) -> pd.DataFrame:
    """
    Portfolio Authority.

    Owns only valuation / gap / ROI / future asset / portfolio decision metrics.
    Does not own identity, current snapshot, season performance or DSS opportunity tier.
    """
    portfolio_path = Path(portfolio_path)
    fallback_path = Path(fallback_path)

    if portfolio_path.exists():
        df = pd.read_csv(portfolio_path)
        source = "transfer_portfolio_dataset"
    elif fallback_path.exists():
        df = pd.read_csv(fallback_path)
        source = "global_prospect_universe_fallback"
    else:
        raise FileNotFoundError(
            f"No portfolio source found. Checked: {portfolio_path} and {fallback_path}"
        )

    if df.empty:
        raise ValueError(f"Portfolio source is empty: {portfolio_path if portfolio_path.exists() else fallback_path}")

    if "player_id_tm" not in df.columns:
        raise KeyError("Portfolio source must contain player_id_tm")

    df = df.copy()
    df["player_id_tm"] = pd.to_numeric(df["player_id_tm"], errors="coerce").astype("Int64")
    df = df[df["player_id_tm"].notna()].copy()
    df["portfolio_source"] = source

    canonical = pd.DataFrame()
    canonical["player_id_tm"] = df["player_id_tm"]

    column_map = {
        "predicted_market_value_eur": [
            "predicted_market_value_eur",
            "expected_market_value_eur",
            "predicted_value_eur",
        ],
        "market_value_gap_eur": [
            "market_value_gap_eur",
            "value_gap_eur",
            "gap_eur",
        ],
        "market_value_gap_pct": [
            "market_value_gap_pct",
            "value_gap_pct",
            "gap_pct",
        ],
        "roi_pct": [
            "roi_proxy_pct",
            "expected_roi_pct",
            "asset_roi_3y_pct",
            "roi_pct",
        ],
        "roi_score": [
            "roi_score",
        ],
        "upside_eur": [
            "upside_eur",
            "asset_upside_3y_eur",
            "expected_upside_eur",
        ],
        "future_asset_score": [
            "future_asset_score",
            "asset_score",
        ],
        "risk_adjusted_opportunity_score": [
            "risk_adjusted_opportunity_score",
            "risk_adjusted_score",
        ],
        "executive_decision_score": [
            "executive_decision_score_v2",
            "executive_decision_score",
            "decision_score",
        ],
        "portfolio_score_conservative": [
            "portfolio_score_conservative",
        ],
        "portfolio_score_balanced": [
            "portfolio_score_balanced",
            "portfolio_score",
        ],
        "portfolio_score_aggressive": [
            "portfolio_score_aggressive",
        ],
        "portfolio_cost_eur": [
            "portfolio_cost_eur",
            "portfolio_cost",
            "estimated_transfer_cost_eur",
        ],
    }

    for output_col, candidates in column_map.items():
        source_col = _first_existing(df, candidates)
        canonical[output_col] = pd.to_numeric(df[source_col], errors="coerce") if source_col else np.nan

    score_cols = [
        "executive_decision_score",
        "future_asset_score",
        "risk_adjusted_opportunity_score",
        "portfolio_score_balanced",
    ]
    available_score_cols = [c for c in score_cols if c in canonical.columns]

    if available_score_cols:
        canonical["_portfolio_sort_score"] = canonical[available_score_cols].max(axis=1, skipna=True)
    else:
        canonical["_portfolio_sort_score"] = np.nan

    canonical = (
        canonical.sort_values(["player_id_tm", "_portfolio_sort_score"], ascending=[True, False])
        .drop_duplicates("player_id_tm", keep="first")
        .drop(columns=["_portfolio_sort_score"])
        .reset_index(drop=True)
    )

    return canonical


def build_portfolio_lookup(df: pd.DataFrame | None = None) -> dict[int, PlayerPortfolio]:
    if df is None:
        df = load_portfolio_layer()

    lookup: dict[int, PlayerPortfolio] = {}

    for _, row in df.iterrows():
        player_id = _to_int(row.get("player_id_tm"))
        if player_id is None:
            continue

        lookup[player_id] = PlayerPortfolio(
            player_id_tm=player_id,
            predicted_market_value_eur=_coalesce(row, ["predicted_market_value_eur"]),
            market_value_gap_eur=_coalesce(row, ["market_value_gap_eur"]),
            market_value_gap_pct=_coalesce(row, ["market_value_gap_pct"]),
            roi_pct=_coalesce(row, ["roi_pct"]),
            roi_score=_coalesce(row, ["roi_score"]),
            upside_eur=_coalesce(row, ["upside_eur"]),
            future_asset_score=_coalesce(row, ["future_asset_score"]),
            risk_adjusted_opportunity_score=_coalesce(row, ["risk_adjusted_opportunity_score"]),
            executive_decision_score=_coalesce(row, ["executive_decision_score"]),
            portfolio_score_conservative=_coalesce(row, ["portfolio_score_conservative"]),
            portfolio_score_balanced=_coalesce(row, ["portfolio_score_balanced"]),
            portfolio_score_aggressive=_coalesce(row, ["portfolio_score_aggressive"]),
            portfolio_cost_eur=_coalesce(row, ["portfolio_cost_eur"]),
        )

    return lookup


def get_player_portfolio(player_id_tm: Any, lookup: dict[int, PlayerPortfolio] | None = None) -> PlayerPortfolio | None:
    player_id = _to_int(player_id_tm)
    if player_id is None:
        return None
    if lookup is None:
        lookup = build_portfolio_lookup()
    return lookup.get(player_id)
