from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import pandas as pd

from src.dss.utils import first, safe_float, safe_int, safe_str


ROOT = Path(__file__).resolve().parents[2]
DEFAULT_DSS_PATH = ROOT / "reports" / "strategy" / "transfer_portfolio_dataset.csv"


@dataclass(frozen=True)
class PlayerDSSMetrics:
    player_id_tm: int
    opportunity_score: float | None
    confidence_score: float | None
    risk_score: float | None
    expected_roi: float | None
    predicted_market_value_eur: float | None
    market_value_gap_eur: float | None
    future_asset_score: float | None
    risk_adjusted_opportunity_score: float | None
    source: str | None


def load_dss_metrics_layer(path: str | Path = DEFAULT_DSS_PATH) -> pd.DataFrame:
    path = Path(path)
    if not path.is_absolute():
        path = ROOT / path

    if not path.exists():
        raise FileNotFoundError(f"DSS metrics layer not found: {path}")

    if path.suffix.lower() == ".parquet":
        return pd.read_parquet(path).copy()

    if path.suffix.lower() == ".csv":
        return pd.read_csv(path).copy()

    raise ValueError(f"Unsupported DSS metrics file format: {path}")


def _resolve_player_id_col(df: pd.DataFrame) -> str | None:
    for col in ["player_id_tm", "player_id", "tm_player_id"]:
        if col in df.columns:
            return col
    return None


def _score_row_quality(row: pd.Series) -> float:
    score = 0.0
    for col in [
        "opportunity_score",
        "confidence_score",
        "risk_score",
        "expected_roi",
        "asset_roi_3y_pct",
        "future_asset_score",
        "risk_adjusted_opportunity_score",
        "predicted_market_value_eur",
        "market_value_gap_eur",
    ]:
        if col in row.index and pd.notna(row.get(col)):
            score += 1.0
    return score


def build_player_dss_metrics(row: pd.Series | dict, source: str = "portfolio_candidates") -> PlayerDSSMetrics:
    return PlayerDSSMetrics(
        player_id_tm=safe_int(first(row, ["player_id_tm", "player_id", "tm_player_id"])) or -1,
        opportunity_score=safe_float(first(row, ["opportunity_score"])),
        confidence_score=safe_float(first(row, ["confidence_score"])),
        risk_score=safe_float(first(row, ["risk_score"])),
        expected_roi=safe_float(first(row, ["asset_roi_3y_pct", "expected_roi", "roi_proxy_pct", "expected_roi_3y_pct"])),
        predicted_market_value_eur=safe_float(first(row, ["predicted_market_value_eur", "expected_market_value_eur"])),
        market_value_gap_eur=safe_float(first(row, ["market_value_gap_eur", "value_gap_adjusted_league_eur"])),
        future_asset_score=safe_float(first(row, ["future_asset_score"])),
        risk_adjusted_opportunity_score=safe_float(first(row, ["risk_adjusted_opportunity_score"])),
        source=source,
    )


def build_dss_lookup(df: pd.DataFrame | None = None) -> dict[str, PlayerDSSMetrics]:
    if df is None:
        df = load_dss_metrics_layer()

    if df is None or df.empty:
        return {}

    id_col = _resolve_player_id_col(df)
    if id_col is None:
        raise ValueError("DSS metrics layer must contain player_id_tm/player_id/tm_player_id")

    out = df.copy()
    out["_dss_player_id"] = pd.to_numeric(out[id_col], errors="coerce")
    out = out[out["_dss_player_id"].notna()].copy()

    if out.empty:
        return {}

    out["_dss_quality"] = out.apply(_score_row_quality, axis=1)

    sort_cols = ["_dss_player_id", "_dss_quality"]
    ascending = [True, False]

    if "opportunity_score" in out.columns:
        out["_dss_opportunity_sort"] = pd.to_numeric(out["opportunity_score"], errors="coerce")
        sort_cols.append("_dss_opportunity_sort")
        ascending.append(False)

    if "risk_score" in out.columns:
        out["_dss_risk_sort"] = pd.to_numeric(out["risk_score"], errors="coerce")
        sort_cols.append("_dss_risk_sort")
        ascending.append(True)

    out = out.sort_values(sort_cols, ascending=ascending)
    latest = out.drop_duplicates("_dss_player_id", keep="first").copy()

    lookup: dict[str, PlayerDSSMetrics] = {}

    for _, row in latest.iterrows():
        player_id = safe_int(row.get("_dss_player_id"))
        if player_id is not None:
            lookup[str(player_id)] = build_player_dss_metrics(row)

    return lookup


def get_player_dss_metrics(
    player_id_tm,
    lookup: dict[str, PlayerDSSMetrics] | None = None,
) -> PlayerDSSMetrics | None:
    if lookup is None:
        lookup = build_dss_lookup()

    player_id = safe_int(player_id_tm)
    if player_id is None:
        return None

    return lookup.get(str(player_id))
