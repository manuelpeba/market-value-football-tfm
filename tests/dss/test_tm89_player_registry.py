from pathlib import Path

from src.dss.player_registry import PlayerRegistry, load_player_registry


def test_tm89_player_registry_loads_expected_sources():
    registry = load_player_registry(Path("."))

    assert isinstance(registry, PlayerRegistry)

    tables = registry.as_dict()
    assert set(tables.keys()) == {
        "snapshot",
        "global",
        "contract",
        "risk",
        "role",
        "role_dna",
        "tm",
    }

    for name, df in tables.items():
        assert hasattr(df, "columns"), name


def test_tm89_player_registry_core_sources_are_available():
    registry = load_player_registry(Path("."))

    assert not registry.snapshot.empty
    assert not registry.global_universe.empty
    assert not registry.contract.empty

    assert "player_id_tm" in registry.snapshot.columns
    assert "player_name_fbref" in registry.global_universe.columns
