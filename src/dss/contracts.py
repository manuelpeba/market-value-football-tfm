from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class PlayerIdentity:
    player_id_tm: int
    name: str
    club: str | None
    league: str | None
    age: float | None
    market_value_eur: float | None
    position: str | None
    position_group: str | None
    nationality: str | None
    valuation_date: str | None
    source: str | None
    quality_status: str | None


@dataclass(frozen=True)
class PlayerPerformance:
    player_id_tm: int
    season: str | None
    club: str | None
    league: str | None
    age: float | None
    position: str | None
    position_group: str | None
    minutes_played: float | None
    goals: float | None
    assists: float | None
    xg: float | None
    xa: float | None
    market_value_eur: float | None
    valuation_date: str | None


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


@dataclass(frozen=True)
class PlayerAnalytics:
    season: str | None
    modeling_club: str | None
    modeling_league: str | None
    modeling_age: float | None
    modeling_market_value_eur: float | None
    minutes_played: float | None
    opportunity_score: float | None
    risk_score: float | None
    confidence_score: float | None
    role: str | None
    expected_market_value_eur: float | None
    market_value_gap_eur: float | None


@dataclass(frozen=True)
class PlayerView:
    identity: PlayerIdentity
    performance: PlayerPerformance | None
    dss: PlayerDSSMetrics | None
    analytics: PlayerAnalytics
