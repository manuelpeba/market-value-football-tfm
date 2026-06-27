from __future__ import annotations

import pandas as pd

from src.dss.analytics import build_player_analytics
from src.dss.contracts import PlayerView
from src.dss.dss_metrics import build_dss_lookup, get_player_dss_metrics
from src.dss.identity import build_identity_lookup, build_player_identity, missing_identity_from_row
from src.dss.performance import build_performance_lookup, get_latest_performance
from src.dss.utils import first, safe_int


def get_player_view(
    row: pd.Series | dict,
    identity_lookup: dict[str, pd.Series] | None = None,
    performance_lookup: dict | None = None,
    dss_lookup: dict | None = None,
) -> PlayerView:
    player_id = safe_int(first(row, ["player_id_tm"]))

    if identity_lookup is None:
        identity_lookup = build_identity_lookup()

    if performance_lookup is None:
        performance_lookup = build_performance_lookup()

    if dss_lookup is None:
        dss_lookup = build_dss_lookup()

    identity_row = identity_lookup.get(str(player_id)) if player_id is not None else None

    identity = (
        build_player_identity(identity_row)
        if identity_row is not None
        else missing_identity_from_row(row)
    )

    performance = get_latest_performance(player_id, performance_lookup) if player_id is not None else None
    dss = get_player_dss_metrics(player_id, dss_lookup) if player_id is not None else None
    analytics = build_player_analytics(row)

    return PlayerView(
        identity=identity,
        performance=performance,
        dss=dss,
        analytics=analytics,
    )


def get_player_views(
    df: pd.DataFrame,
    identity_df: pd.DataFrame | None = None,
    performance_df: pd.DataFrame | None = None,
    dss_df: pd.DataFrame | None = None,
) -> list[PlayerView]:
    identity_lookup = build_identity_lookup(identity_df)
    performance_lookup = build_performance_lookup(performance_df)
    dss_lookup = build_dss_lookup(dss_df)
    return [
        get_player_view(row, identity_lookup, performance_lookup, dss_lookup)
        for _, row in df.iterrows()
    ]
