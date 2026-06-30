from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Dict

import pandas as pd


@dataclass(frozen=True)
class PlayerRegistry:
    """
    Single loading contract for DSS player-level sources.

    This object is intentionally a registry, not yet a presentation dataset.
    No UI module should independently load player identity/context sources once
    the TM.8.9 migration is complete.
    """
    snapshot: pd.DataFrame
    global_universe: pd.DataFrame
    contract: pd.DataFrame
    risk: pd.DataFrame
    role: pd.DataFrame
    role_dna: pd.DataFrame
    transfermarkt: pd.DataFrame

    def as_dict(self) -> Dict[str, pd.DataFrame]:
        return {
            "snapshot": self.snapshot,
            "global": self.global_universe,
            "contract": self.contract,
            "risk": self.risk,
            "role": self.role,
            "role_dna": self.role_dna,
            "tm": self.transfermarkt,
        }


def _read_csv(path: Path) -> pd.DataFrame:
    if not path.exists():
        return pd.DataFrame()
    return pd.read_csv(path, low_memory=False)


def _read_parquet(path: Path) -> pd.DataFrame:
    if not path.exists():
        return pd.DataFrame()
    return pd.read_parquet(path)


def load_player_registry(root: Path) -> PlayerRegistry:
    """
    Load all player-level DSS source tables from a single architectural entry point.

    Step 1 of TM.8.9 only centralizes loading.
    It does not yet resolve presentation semantics.
    """
    root = Path(root)

    processed_path = root / "data" / "processed"
    reports_path = root / "reports"

    return PlayerRegistry(
        snapshot=_read_parquet(processed_path / "current_player_snapshot.parquet"),
        global_universe=_read_csv(reports_path / "dss" / "global_prospect_universe.csv"),
        contract=_read_csv(reports_path / "tm3_contract_intelligence" / "contract_intelligence_dataset.csv"),
        risk=_read_csv(reports_path / "rankings" / "scouting_shortlist_with_risk.csv"),
        role=_read_parquet(processed_path / "player_role_features_advanced.parquet"),
        role_dna=_read_csv(reports_path / "roles" / "player_role_dna.csv"),
        transfermarkt=_read_parquet(processed_path / "transfermarkt_features_v13a.parquet"),
    )
