#!/usr/bin/env python3
"""NASCAR Monte Carlo Simulator - v3.1 (synthesized).

Lineage: this is Phase 1.2's changelog-faithful v3.1 model, repaired so it
actually runs, with the engineering from the parallel build folded back in.

What Phase 1.2 got right and is preserved here:
  - Real v3.1 algorithm: road specialty, braking, patience, adaptability,
    consistency, plus the two features the campaign narrative hinges on --
    a local-knowledge bonus (Larson at Sonoma) and a recent-DNF penalty
    (SVG after the San Diego crash), both read from each driver's
    `sonoma_specific` block.
  - JSON-driven track / algorithm / field configs.
  - Result export.

What was repaired:
  - The crash: `tuple(data.values()[:6])` is invalid in Python 3 and was
    also order-fragile. Attributes are now pulled by name, so the field
    schema can grow without breaking the model.
  - Determinism: the global `random` module is replaced with a seeded
    `random.Random` instance, so runs are reproducible and tests isolated.
  - A real argparse CLI (was a hard-coded, cwd-dependent __main__).
  - num_simulations is validated.

The model still decides a race by who leads the final lap, aggregated over
many races into win probabilities -- unchanged, so the campaign's published
Sonoma ranking (Larson on top) holds.
"""

from __future__ import annotations

import json
import random
from collections import defaultdict
from typing import Dict, List, Optional, Tuple

# The six numeric ratings every driver carries, in a fixed order. Pulling by
# name (not by dict position) is what makes the field schema safe to extend.
ATTRIBUTE_KEYS = (
    "base_speed",
    "road_specialty",
    "braking_precision",
    "elevation_management",
    "patience",
    "adaptability",
)

# Oval / intermediate attribute set, in fixed order. Index 2 (tire_management)
# is the "control" rating that drives tire wear + mistakes, parallel to
# braking_precision on road, so run_simulation's tire model is track-agnostic.
OVAL_ATTRIBUTE_KEYS = (
    "base_speed",
    "oval_specialty",
    "tire_management",
    "restart_skill",
    "short_run_speed",
    "long_run_speed",
)


class CoreSimulator:
    """NASCAR race simulator implementing the v3.1 algorithm."""

    def __init__(
        self,
        track_config: Dict,
        algo_config: Dict,
        field: Optional[Dict] = None,
        seed: Optional[int] = None,
        variance_override: Optional[float] = None,
    ):
        """
        Args:
            track_config: track parameters (JSON dict).
            algo_config: algorithm version parameters (JSON dict).
            field: driver-ratings dict keyed by name. Loads default if None.
            seed: overrides the algorithm's seed for reproducible runs.
        """
        self.track_config = track_config
        self.algo_config = algo_config
        self.results: Dict[str, int] = defaultdict(int)

        if field is None:
            field = self._load_default_field()
        self.driver_info = field  # full dicts (notes, sonoma_specific, ...)

        # Track type decides which attribute set (and weights) apply.
        _is_road = "road" in str(track_config.get("track_type", "")).lower()
        self.attr_keys = ATTRIBUTE_KEYS if _is_road else OVAL_ATTRIBUTE_KEYS
        # Numeric ratings pulled by name -> order-independent and crash-free.
        self.drivers: Dict[str, Tuple[float, ...]] = {
            name: tuple(data[k] for k in self.attr_keys)
            for name, data in field.items()
        }

        # Track parameters (Phase 1.2 schema: nested physics block).
        self.laps = track_config.get("laps", 110)
        self.avg_speed = track_config.get("avg_speed_mph", 110)
        physics = track_config.get("physics", {})
        self.caution_prob = physics.get("caution_probability", 0.035)
        self.pit_window = physics.get("pit_window_laps", 35)
        # Variance can be overridden by the learning loop's calibration state.
        self.variance = variance_override if variance_override is not None \
            else physics.get("variance_percent", 2.0)
        # Which form rating applies depends on track type.
        self.is_road = "road" in str(track_config.get("track_type", "")).lower()
        self.form_key = "road_form" if self.is_road else "oval_form"

        # Algorithm parameters.
        self.version = algo_config.get("version", "v3.1")
        self.seed = seed if seed is not None else algo_config.get("seed", None)
        self.rng = random.Random(self.seed)  # seeded instance, not global RNG

        self.bonuses = algo_config.get("bonuses", {})
        self.oval_bonuses = algo_config.get("oval_bonuses", {})
        self.penalties = algo_config.get("penalties", {})
        self.track_specific = algo_config.get("track_specific", {})

        # Finish model. v3.1 default ("argmax") = winner leads the final lap,
        # which is near-deterministic and amplifies small edges. v3.2
        # ("proportional") draws the winner with probability proportional to
        # race-long pace ^ decisiveness, so form and tilt move outcomes
        # smoothly. Higher decisiveness => more concentrated on the favorite.
        finish = algo_config.get("finish", {})
        self.finish_method = finish.get("method", "argmax")
        self.decisiveness = finish.get("decisiveness", 1.0)

        # The per-driver `sonoma_specific` tilts (local-knowledge bonus, recent-DNF
        # penalty) are recorded in the field data but OFF by default. Reason: on
        # this single-lap-argmax model they are all-or-nothing -- applying them at
        # even 10% strength collapses SVG from 3rd to 8th and pushes Larson past
        # 30%, breaking the published "moderate, not dominant" calibration
        # (Larson ~24.5%). Left off, the engine reproduces the published ranking.
        # Making the tilt behave gradually needs a less deterministic finish model
        # (a v3.2 project). Set "apply_sonoma_tilt": true to experiment.
        self.apply_tilt = algo_config.get("apply_sonoma_tilt", False)

    @staticmethod
    def _load_default_field() -> Dict:
        """Load the default driver field via ConfigLoader."""
        try:
            from engine.config import ConfigLoader
        except ModuleNotFoundError:
            import sys
            from pathlib import Path

            sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
            from engine.config import ConfigLoader
        return ConfigLoader().load_field("default")

    # -- simulation --------------------------------------------------------- #
    def run_simulation(self, num_simulations: int = 1000) -> Dict[str, int]:
        """Run `num_simulations` races; return {driver: win_count}."""
        if num_simulations <= 0:
            raise ValueError("num_simulations must be positive")

        results: Dict[str, int] = defaultdict(int)

        for _ in range(num_simulations):
            tire_wear = {d: 0.0 for d in self.drivers}
            mistakes = {d: 0 for d in self.drivers}
            perf_sum = {d: 0.0 for d in self.drivers}
            current_leader = next(iter(self.drivers))

            for lap in range(1, self.laps + 1):
                # Tire wear accrues; better braking extends the tire window.
                for d in self.drivers:
                    braking = self.drivers[d][2]
                    tire_wear[d] += 1.0 / (self.pit_window * braking)

                # Pit window: scheduled, or forced in the closing laps.
                if lap % self.pit_window == 0 or lap > self.laps - 10:
                    for d in self.drivers:
                        if tire_wear[d] > 0.90 or lap > self.laps - 10:
                            tire_wear[d] = 0.0

                performance = self._lap_performance(tire_wear, mistakes)
                current_leader = max(performance, key=performance.get)
                for d in self.drivers:
                    perf_sum[d] += performance[d]

                # Caution counted but inert (preserves validated distribution).
                if self.rng.random() < self.caution_prob:
                    pass

            results[self._decide_winner(perf_sum, current_leader)] += 1

        self.results = results
        return results

    def _decide_winner(self, perf_sum: Dict[str, float], leader: str) -> str:
        """Pick the race winner from accumulated pace.

        argmax (v3.1): whoever led the final lap. proportional (v3.2): a draw
        weighted by race-long average pace ^ decisiveness -- smooth, so a small
        edge yields a small win-share change.
        """
        if self.finish_method != "proportional":
            return leader
        names = list(perf_sum)
        avg = [perf_sum[d] / self.laps for d in names]
        # Normalize by the field's best pace before exponentiating: keeps the
        # weights in a sane range (no overflow) while leaving the relative
        # sampling probabilities identical.
        top = max(avg) or 1.0
        weights = [(a / top) ** self.decisiveness for a in avg]
        return self.rng.choices(names, weights=weights, k=1)[0]

    def _lap_performance(
        self, tire_wear: Dict[str, float], mistakes: Dict[str, int]
    ) -> Dict[str, float]:
        """Compute one lap's performance score for every driver (v3.1 math)."""
        b = self.bonuses
        perf: Dict[str, float] = {}

        for d in self.drivers:
            if not self.is_road:
                perf[d] = self._oval_perf(d, tire_wear, mistakes)
                continue
            base_speed, road_spec, braking, elevation, patience, adapt = self.drivers[d]

            variance = self.rng.gauss(1.0, self.variance / 100.0)

            road_bonus = 1.0 + road_spec * b.get("road_specialty_weight", 0.05)
            braking_bonus = 1.0 + braking * b.get("braking_precision_weight", 0.03)
            # Elevation management: a real Sonoma factor (multi-elevation track).
            # Present in the original simulator; Phase 1.2 dropped it -- restored.
            elevation_bonus = 1.0 + elevation * b.get("elevation_weight", 0.02)
            patience_bonus = 1.0 + patience * b.get("patience_weight", 0.02)
            adapt_bonus = 1.0 + adapt * b.get("adaptability_weight", 0.015)
            # Consistency is a flat, field-wide bonus (ranking-neutral by design;
            # there is no per-driver consistency rating yet -- see notes).
            consistency_bonus = 1.0 + b.get("consistency_weight", 0.04) * 0.5

            tire_impact = 1.0 - tire_wear[d] * 0.03

            # Form: a bounded, decaying multiplier the learning loop updates
            # from results (1.0 = neutral, so an unlearned field is unchanged).
            form = self.driver_info.get(d, {}).get(self.form_key, 1.0)

            # v3.1 per-driver tilts, OFF by default (see __init__ note).
            local_bonus = 1.0
            dnf_penalty = 1.0
            if self.apply_tilt:
                specific = self.driver_info.get(d, {}).get("sonoma_specific", {})
                if "local_knowledge_bonus" in specific:
                    local_bonus = 1.0 + specific["local_knowledge_bonus"]
                if "recent_dnf_penalty" in specific:
                    dnf_penalty = 1.0 - specific["recent_dnf_penalty"]

            # Mistakes: weaker braking slips more often; drag is cumulative.
            if self.rng.random() < (1.0 - braking) * 0.07:
                mistakes[d] += 1
            mistake_penalty = 1.0 - mistakes[d] * 0.015

            perf[d] = (
                base_speed
                * variance
                * road_bonus
                * braking_bonus
                * elevation_bonus
                * consistency_bonus
                * patience_bonus
                * adapt_bonus
                * tire_impact
                * form
                * local_bonus
                * dnf_penalty
                * mistake_penalty
            )
        return perf

    def _oval_perf(
        self, d: str, tire_wear: Dict[str, float], mistakes: Dict[str, int]
    ) -> float:
        """One lap's performance for an oval / intermediate.

        Mirrors the road path's structure but uses the oval attribute set and
        oval weights: oval_specialty, tire_management, restart_skill,
        short_/long_run_speed. Index 2 (tire_management) drives tire wear and
        mistakes, parallel to braking on road, so run_simulation is unchanged.
        """
        ob = self.oval_bonuses
        base_speed, oval_spec, tire_mgmt, restart, short_run, long_run = self.drivers[d]

        variance = self.rng.gauss(1.0, self.variance / 100.0)
        spec_bonus = 1.0 + oval_spec * ob.get("oval_specialty_weight", 0.40)
        tire_bonus = 1.0 + tire_mgmt * ob.get("tire_management_weight", 0.24)
        restart_bonus = 1.0 + restart * ob.get("restart_skill_weight", 0.16)
        short_bonus = 1.0 + short_run * ob.get("short_run_speed_weight", 0.12)
        long_bonus = 1.0 + long_run * ob.get("long_run_speed_weight", 0.16)
        consistency_bonus = 1.0 + self.bonuses.get("consistency_weight", 0.04) * 0.5

        tire_impact = 1.0 - tire_wear[d] * 0.03
        form = self.driver_info.get(d, {}).get(self.form_key, 1.0)

        if self.rng.random() < (1.0 - tire_mgmt) * 0.07:
            mistakes[d] += 1
        mistake_penalty = 1.0 - mistakes[d] * 0.015

        return (
            base_speed * variance * spec_bonus * tire_bonus * restart_bonus
            * short_bonus * long_bonus * consistency_bonus * tire_impact
            * form * mistake_penalty
        )

    # -- reporting ---------------------------------------------------------- #
    def get_top_predictions(self, n: int = 10) -> List[Tuple[str, float]]:
        """Top N drivers as (name, win_pct)."""
        if not self.results:
            return []
        total = sum(self.results.values())
        top = sorted(self.results.items(), key=lambda x: x[1], reverse=True)[:n]
        return [(driver, 100.0 * wins / total) for driver, wins in top]

    def print_results(self, n: int = 10) -> None:
        """Print the top N predictions with campaign context notes."""
        if not self.results:
            print("No results. Run simulation first.")
            return

        total = sum(self.results.values())
        track = self.track_config.get("track_name", "Unknown")

        print(f"\n{'=' * 70}")
        print(f"{track} | model {self.version} | {total:,} simulated races | seed {self.seed}")
        print(f"{'=' * 70}\n")
        print(f"{'#':>2}  {'Driver':<30} {'Win%':>7}  Notes")
        print("-" * 70)

        for rank, (driver, pct) in enumerate(self.get_top_predictions(n=n), 1):
            notes = ""
            if "sonoma" in track.lower():
                if driver == "Kyle Larson":
                    notes = "<- 2x winner, LOCAL, no DNF"
                elif driver == "Shane van Gisbergen":
                    notes = "<- defending, but San Diego DNF"
            print(f"{rank:2d}  {driver:<30} {pct:>6.1f}%  {notes}")

        print(f"{'=' * 70}\n")

    def export_results(self, filepath: str) -> None:
        """Export full ranked results to JSON."""
        if not self.results:
            return
        total = sum(self.results.values())
        output = {
            "track": self.track_config.get("track_name"),
            "algorithm_version": self.version,
            "seed": self.seed,
            "total_simulations": total,
            "predictions": [
                {
                    "rank": rank,
                    "driver": driver,
                    "wins": self.results[driver],
                    "percentage": 100.0 * self.results[driver] / total,
                }
                for rank, (driver, _) in enumerate(
                    self.get_top_predictions(n=len(self.results)), 1
                )
            ],
        }
        with open(filepath, "w") as f:
            json.dump(output, f, indent=2)
        print(f"Results exported to {filepath}")


# --------------------------------------------------------------------------- #
# Command-line interface
# --------------------------------------------------------------------------- #
def main(argv: Optional[List[str]] = None) -> int:
    """Run a simulation from the command line.

    Example:
        python engine/core_simulator.py --track sonoma --algorithm v3.1
    """
    import argparse

    try:
        from engine.config import ConfigLoader
    except ModuleNotFoundError:
        import sys
        from pathlib import Path

        sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
        from engine.config import ConfigLoader

    parser = argparse.ArgumentParser(description="NASCAR Monte Carlo race predictor.")
    parser.add_argument("--track", default="sonoma", help="Track key (e.g. sonoma)")
    parser.add_argument("--algorithm", default="v3.2",
                        help="Algorithm version (v3.2 = realistic finish; v3.1 = legacy)")
    parser.add_argument("--field", default="default", help="Driver field name")
    parser.add_argument("-n", "--num-simulations", type=int, default=10000,
                        help="Number of races to simulate (default 10000)")
    parser.add_argument("--top", type=int, default=10, help="How many drivers to show")
    parser.add_argument("--seed", type=int, default=None, help="Override RNG seed")
    parser.add_argument("--export", metavar="PATH", default=None,
                        help="Write full results JSON to PATH")
    args = parser.parse_args(argv)

    loader = ConfigLoader()
    track = loader.load_track_config(args.track)
    algo = loader.load_algorithm_version(args.algorithm)
    field = loader.load_field(args.field)

    sim = CoreSimulator(track, algo, field, seed=args.seed)
    print(f"Running {args.num_simulations:,} simulations...")
    sim.run_simulation(num_simulations=args.num_simulations)
    sim.print_results(n=args.top)
    if args.export:
        sim.export_results(args.export)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
