from pathlib import Path

import pytest

from src.dss.player_presentation import (
    FORBIDDEN_PRESENTATION_COLUMNS,
    REQUIRED_PRESENTATION_COLUMNS,
    build_display_dataset,
    validate_display_contract,
)
from src.dss.player_registry import load_player_registry


def test_tm89_display_dataset_satisfies_contract():
    registry = load_player_registry(Path("."))
    display = build_display_dataset(registry)

    assert not display.empty

    missing = REQUIRED_PRESENTATION_COLUMNS - set(display.columns)
    forbidden = FORBIDDEN_PRESENTATION_COLUMNS & set(display.columns)

    assert missing == set()
    assert forbidden == set()


def test_tm89_display_dataset_preserves_governed_context_columns():
    registry = load_player_registry(Path("."))
    display = build_display_dataset(registry)

    assert "season_context_club" in display.columns
    assert "current_club_snapshot" in display.columns
    assert "display_club" in display.columns
    assert "gap_interpretation_status" in display.columns


def test_tm89_validate_display_contract_rejects_raw_context_columns():
    registry = load_player_registry(Path("."))
    display = build_display_dataset(registry)

    bad = display.copy()
    bad["club"] = bad["display_club"]

    with pytest.raises(ValueError, match="forbidden raw columns"):
        validate_display_contract(bad)
