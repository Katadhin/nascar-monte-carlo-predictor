"""Tests for the synthesized v3.1 engine.

Two jobs: lock the campaign-facing guarantee (The Machine picks Larson at
Sonoma, with Larson > Elliott > SVG), and lock the engineering that Phase 1.2
lacked (it runs, it's deterministic, the v3.1 tilt features actually fire).
"""

import json
from pathlib import Path

import pytest

from engine.config import ConfigLoader
from engine.core_simulator import CoreSimulator


@pytest.fixture
def loader():
    return ConfigLoader()


@pytest.fixture
def sonoma(loader):
    return loader.load_track_config("sonoma")


@pytest.fixture
def v31(loader):
    return loader.load_algorithm_version("v3.1")


@pytest.fixture
def field(loader):
    return loader.load_field("default")


@pytest.fixture
def baseline_field():
    """Frozen pre-learning field for v3.1 parity tests.

    v3.1's near-deterministic finish is highly sensitive to form, so parity must
    be checked against fixed inputs, not the live field the learning loop mutates
    every race. (The live field moving past this snapshot is itself the
    brittleness v3.2 was built to fix.)
    """
    p = Path(__file__).parent / "fixtures" / "baseline_field.json"
    data = json.loads(p.read_text())
    return data.get("field", data)


# -- config loading --------------------------------------------------------- #
def test_lists_sonoma(loader):
    assert "sonoma" in loader.list_available_tracks()


def test_lists_v31(loader):
    assert "v3.1" in loader.list_available_algorithms()


def test_sonoma_schema(sonoma):
    assert sonoma["laps"] == 110
    assert sonoma["track_name"] == "Sonoma Raceway"
    assert sonoma["physics"]["caution_probability"] == 0.035


def test_algorithm_version_accepts_both_forms(loader):
    assert loader.load_algorithm_version("v3.1")["version"] == "v3.1"
    assert loader.load_algorithm_version("3.1")["version"] == "v3.1"


def test_field_is_dict_of_15(field):
    assert isinstance(field, dict)
    assert len(field) == 15
    assert all("base_speed" in d for d in field.values())


def test_missing_track_raises_with_hint(loader):
    with pytest.raises(FileNotFoundError) as exc:
        loader.load_track_config("talladega")
    assert "sonoma" in str(exc.value)


# -- the crash Phase 1.2 shipped must stay fixed ---------------------------- #
def test_constructs_without_crashing(sonoma, v31, field):
    # Phase 1.2 raised TypeError here on `data.values()[:6]`.
    sim = CoreSimulator(sonoma, v31, field, seed=42)
    assert len(sim.drivers) == 15
    # Attributes pulled by name, in the documented order.
    assert sim.drivers["Kyle Larson"][0] == 138  # base_speed


# -- v3.1 features actually fire -------------------------------------------- #
def test_v31_tilt_features_present_in_data(field):
    assert field["Kyle Larson"]["sonoma_specific"]["local_knowledge_bonus"] == 0.03
    assert field["Shane van Gisbergen"]["sonoma_specific"]["recent_dnf_penalty"] == 0.15


# -- parity with the published model ---------------------------------------- #
def test_sonoma_pick_is_larson(sonoma, v31, baseline_field):
    sim = CoreSimulator(sonoma, v31, baseline_field, seed=42)
    sim.run_simulation(5000)
    assert sim.get_top_predictions(1)[0][0] == "Kyle Larson"


def test_sonoma_top_three_order(sonoma, v31, baseline_field):
    sim = CoreSimulator(sonoma, v31, baseline_field, seed=42)
    sim.run_simulation(5000)
    top3 = [name for name, _ in sim.get_top_predictions(3)]
    assert top3 == ["Kyle Larson", "Chase Elliott", "Shane van Gisbergen"]


def test_larson_confidence_in_expected_band(sonoma, v31, baseline_field):
    sim = CoreSimulator(sonoma, v31, baseline_field, seed=42)
    sim.run_simulation(5000)
    pct = sim.get_top_predictions(1)[0][1]
    assert 20.0 <= pct <= 30.0


# -- invariants ------------------------------------------------------------- #
def test_wins_sum_to_total(sonoma, v31, field):
    sim = CoreSimulator(sonoma, v31, field, seed=1)
    results = sim.run_simulation(2000)
    assert sum(results.values()) == 2000


def test_zero_runs_rejected(sonoma, v31, field):
    with pytest.raises(ValueError):
        CoreSimulator(sonoma, v31, field).run_simulation(0)


# -- determinism (impossible in Phase 1.2's global-RNG version) ------------- #
def test_same_seed_identical(sonoma, v31, field):
    a = CoreSimulator(sonoma, v31, field, seed=7).run_simulation(1500)
    b = CoreSimulator(sonoma, v31, field, seed=7).run_simulation(1500)
    assert dict(a) == dict(b)


def test_different_seed_differs(sonoma, v31, field):
    a = CoreSimulator(sonoma, v31, field, seed=7).run_simulation(1500)
    b = CoreSimulator(sonoma, v31, field, seed=8).run_simulation(1500)
    assert dict(a) != dict(b)
