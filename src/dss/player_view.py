from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from src.dss.common import normalize_player_id
from src.dss.identity import PlayerIdentity
from src.dss.performance import PlayerPerformance
from src.dss.scoring import PlayerScoring
from src.dss.portfolio import PlayerPortfolio


@dataclass(frozen=True)
class PlayerView:
    player_id_tm: int
    identity: PlayerIdentity | None = None
    performance: PlayerPerformance | None = None
    scoring: PlayerScoring | None = None
    portfolio: PlayerPortfolio | None = None

    @property
    def is_resolved(self) -> bool:
        return any([self.identity, self.performance, self.scoring, self.portfolio])

    @property
    def player_name(self) -> str | None:
        if self.identity and self.identity.player_name:
            return self.identity.player_name
        return None

    @property
    def current_club(self) -> str | None:
        return self.identity.club if self.identity else None

    @property
    def current_league(self) -> str | None:
        return self.identity.league if self.identity else None

    @property
    def current_age(self) -> float | None:
        return self.identity.age if self.identity else None

    @property
    def current_market_value_eur(self) -> float | None:
        return self.identity.market_value_eur if self.identity else None

    @property
    def latest_season(self) -> str | None:
        return self.performance.season if self.performance else None

    @property
    def performance_minutes(self) -> float | None:
        return self.performance.minutes_played if self.performance else None

    @property
    def opportunity_score(self) -> float | None:
        return self.scoring.opportunity_score if self.scoring else None

    @property
    def confidence_score(self) -> float | None:
        return self.scoring.confidence_score if self.scoring else None

    @property
    def opportunity_tier(self) -> str | None:
        return self.scoring.tier if self.scoring else None

    @property
    def predicted_market_value_eur(self) -> float | None:
        return self.portfolio.predicted_market_value_eur if self.portfolio else None

    @property
    def market_value_gap_eur(self) -> float | None:
        return self.portfolio.market_value_gap_eur if self.portfolio else None

    @property
    def portfolio_cost_eur(self) -> float | None:
        return self.portfolio.portfolio_cost_eur if self.portfolio else None


def build_player_view(
    player_id_tm: Any,
    *,
    identity_lookup: dict[int, PlayerIdentity] | None = None,
    performance_lookup: dict[int, PlayerPerformance] | None = None,
    scoring_lookup: dict[int, PlayerScoring] | None = None,
    portfolio_lookup: dict[int, PlayerPortfolio] | None = None,
) -> PlayerView | None:
    player_id = normalize_player_id(player_id_tm)
    if player_id is None:
        return None

    return PlayerView(
        player_id_tm=player_id,
        identity=identity_lookup.get(player_id) if identity_lookup else None,
        performance=performance_lookup.get(player_id) if performance_lookup else None,
        scoring=scoring_lookup.get(player_id) if scoring_lookup else None,
        portfolio=portfolio_lookup.get(player_id) if portfolio_lookup else None,
    )
