"""Tests for the learning loop and the v3.2 realistic-finish model.

These lock the guarantees that took the most work to earn: v3.2 produces a
clear-but-moderate favorite, learning moves the board PROPORTIONATELY (the
v3.1 blow-up must never come back), and the loop only corrects its mistakes.
"""

import copy
import pytest

from engine.config import ConfigLoader
from engine.core_simulator import CoreSimulator
from engine import learning as L


@pytest.fixture
def loader():
    return ConfigLoader()


@pytest.fixture
def sonoma(loader):
    return loader.load_track_config("sonoma")


@pytest.fixture
def v32(loader):
    return loader.load_algorithm_version("v3.2")


@pytest.fixture
def field(loader):
    return loader.load_field("default")


# -- scoring ---------------------------------------------------------------- #
def test_brier_perfect_call_is_zero():
    probs = {"A": 1.0, "B": 0.0}
    assert L.brier_score(probs, "A") == 0.0


def test_brier_punishes_confident_miss():
    confident_wrong = L.brier_score({"A": 0.9, "B": 0.1}, "B")
    humble_wrong = L.brier_score({"A": 0.5, "B": 0.5}, "B")
    assert confident_wrong > humble_wrong


# -- v3.2 model behavior ---------------------------------------------------- #
def test_v32_has_clear_but_moderate_favorite(sonoma, v32, field):
    probs = L.predicted_probabilities(sonoma, v32, field, n=2000)
    top = max(probs.values())
    assert 0.10 <= top <= 0.30  # a real favorite, not a runaway


def test_v32_road_master_is_favorite(sonoma, v32, field):
    probs = L.predicted_probabilities(sonoma, v32, field, n=2000)
    favorite = max(probs, key=probs.get)
    assert favorite == "Shane van Gisbergen"  # widened skill -> road ace leads


def test_v32_oval_specialist_is_buried(sonoma, v32, field):
    probs = L.predicted_probabilities(sonoma, v32, field, n=2000)
    assert probs["Denny Hamlin"] < probs["Shane van Gisbergen"]


def test_v32_no_overflow_high_decisiveness(sonoma, field):
    algo = {"version": "x", "seed": 1, "bonuses": {"road_specialty_weight": 0.4},
            "finish": {"method": "proportional", "decisiveness": 200}}
    # Must not raise OverflowError (weights are normalized before exponentiating).
    CoreSimulator(sonoma, algo, field, seed=1).run_simulation(50)


# -- learning is proportionate (the v3.1 blow-up must not return) ----------- #
def test_form_bump_moves_proportionately(sonoma, v32, field):
    before = L.predicted_probabilities(sonoma, v32, field, n=2000)["Shane van Gisbergen"]
    bumped = copy.deepcopy(field)
    bumped["Shane van Gisbergen"]["road_form"] = 1.06
    after = L.predicted_probabilities(sonoma, v32, bumped, n=2000)["Shane van Gisbergen"]
    swing = (after - before) * 100
    assert 0 < swing < 20  # proportionate; under v3.1 this was +77


def test_form_update_marks_down_the_overrated(sonoma, v32, field):
    """Larson predicted high but finished 4th -> his form should drop."""
    probs = L.predicted_probabilities(sonoma, v32, field, n=2000)
    rank = L._rank(probs)
    finish = ["Shane van Gisbergen", "Ty Gibbs", "Kyle Larson", "Christopher Bell"]
    L.update_form(field, finish, rank, "road_form")
    assert field["Kyle Larson"]["road_form"] < 1.0


def test_form_stays_within_bounds(sonoma, v32, field):
    rank = L._rank(L.predicted_probabilities(sonoma, v32, field, n=1500))
    finish = ["Ty Gibbs", "AJ Allmendinger", "Chris Buescher"]  # big upsets
    L.update_form(field, finish, rank, "road_form")
    for d in field.values():
        assert L.FORM_BOUNDS[0] <= d.get("road_form", 1.0) <= L.FORM_BOUNDS[1]


def test_calibration_humbles_after_miss():
    state = {"calibration": {"variance_percent": 2.0, "rolling_brier": []}}
    v = L.update_calibration(state, brier=0.9, top_pick_won=False)
    assert v > 2.0  # blind-sided -> wider, more humble
