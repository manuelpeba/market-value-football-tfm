from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from src.dss.common import normalize_player_id
from src.dss.identity import PlayerIdentity, build_identity_lookup, load_identity_layer
from src.dss.performance import PlayerPerformance, build_performance_lookup, load_performance_layer
from src.dss.scoring import PlayerScoring, build_scoring_lookup, load_scoring_layer
from src.dss.portfolio import PlayerPortfolio, build_portfolio_lookup, load_portfolio_layer
from src.dss.player_view import PlayerView, build_player_view


@dataclass
class PlayerRegistry:
    identity_lookup: dict[int, PlayerIdentity] = field(default_factory=dict)
    performance_lookup: dict[int, PlayerPerformance] = field(default_factory=dict)
    scoring_lookup: dict[int, PlayerScoring] = field(default_factory=dict)
    portfolio_lookup: dict[int, PlayerPortfolio] = field(default_factory=dict)

    @classmethod
    def build(cls) -> "PlayerRegistry":
        return cls(
            identity_lookup=build_identity_lookup(load_identity_layer()),
            performance_lookup=build_performance_lookup(load_performance_layer()),
            scoring_lookup=build_scoring_lookup(load_scoring_layer()),
            portfolio_lookup=build_portfolio_lookup(load_portfolio_layer()),
        )

    def get(self, player_id_tm: Any) -> PlayerView | None:
        player_id = normalize_player_id(player_id_tm)
        if player_id is None:
            return None

        return build_player_view(
            player_id,
            identity_lookup=self.identity_lookup,
            performance_lookup=self.performance_lookup,
            scoring_lookup=self.scoring_lookup,
            portfolio_lookup=self.portfolio_lookup,
        )

    def has(self, player_id_tm: Any) -> bool:
        view = self.get(player_id_tm)
        return bool(view and view.is_resolved)

    def coverage(self) -> dict[str, int]:
        all_ids = set()
        all_ids |= set(self.identity_lookup.keys())
        all_ids |= set(self.performance_lookup.keys())
        all_ids |= set(self.scoring_lookup.keys())
        all_ids |= set(self.portfolio_lookup.keys())

        fully_resolved = 0
        dss_resolved = 0

        for player_id in all_ids:
            has_identity = player_id in self.identity_lookup
            has_performance = player_id in self.performance_lookup
            has_scoring = player_id in self.scoring_lookup
            has_portfolio = player_id in self.portfolio_lookup

            if has_identity and has_performance and has_scoring and has_portfolio:
                fully_resolved += 1

            if has_identity and has_scoring:
                dss_resolved += 1

        return {
            "identity_players": len(self.identity_lookup),
            "performance_players": len(self.performance_lookup),
            "scoring_players": len(self.scoring_lookup),
            "portfolio_players": len(self.portfolio_lookup),
            "union_players": len(all_ids),
            "fully_resolved_players": fully_resolved,
            "dss_resolved_players": dss_resolved,
        }
