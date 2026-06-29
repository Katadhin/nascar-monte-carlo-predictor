#!/usr/bin/env python3
"""Post-race learning loop for The Machine.

Runs after every round. It does two data-driven things and deliberately does
NOT do a third.

DOES:
  1. Updates per-driver FORM (a bounded, decaying multiplier, separate for road
     and oval) from how drivers actually finished versus what the Machine
     predicted. Beat your prediction -> form up; missed it -> form down.
  2. Recalibrates the Machine's CONFIDENCE: it tracks how wrong its
     probabilities were (Brier score) and nudges race variance so the model
     gets humbler after blind-side losses and sharper after clean calls.

DELIBERATELY DOESN'T:
  - Rewrite driver skill ratings or the strategic algorithm weights. Those
    stay human-controlled. The reason is written in this repo's own history:
    after San Diego the Machine hard-coded a one-race "lesson" (penalize the
    recent DNF), and the penalized driver -- SVG -- won the very next race at
    Sonoma. A loop that swings hard on each result repeats that mistake weekly.

The guardrails are the point: small learning rate, decay back toward neutral,
and tight bounds, so no single Sunday can capture the model. Skill is slow;
form is fast but leashed.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Dict, List, Optional, Tuple

try:
    from engine.config import ConfigLoader
    from engine.core_simulator import CoreSimulator
except ModuleNotFoundError:
    import sys
    sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
    from engine.config import ConfigLoader
    from engine.core_simulator import CoreSimulator

# Tunables -- chosen so one race moves form by at most ~6%.
FORM_LEARNING_RATE = 0.4
FORM_DECAY = 0.34            # fraction of current form reverted toward 1.0 / race
FORM_BOUNDS = (0.94, 1.06)
VARIANCE_BOUNDS = (1.5, 8.0)
VARIANCE_STEP = 0.25


# --------------------------------------------------------------------------- #
# Scoring
# --------------------------------------------------------------------------- #
def brier_score(pred_probs: Dict[str, float], winner: str) -> float:
    """Multiclass Brier score: how far the probabilities were from reality.

    pred_probs are fractions (0-1). Lower is better (0 = perfect, called it at
    100%). A confident-but-wrong pick is punished harder than a humble one.
    """
    names = set(pred_probs) | {winner}
    return sum((pred_probs.get(n, 0.0) - (1.0 if n == winner else 0.0)) ** 2
               for n in names)


def predicted_probabilities(
    track: Dict, algo: Dict, field: Dict, seed: int = 42,
    n: int = 5000, variance_override: Optional[float] = None
) -> Dict[str, float]:
    """Run the sim and return {driver: win fraction} for every driver."""
    sim = CoreSimulator(track, algo, field, seed=seed, variance_override=variance_override)
    results = sim.run_simulation(n)
    total = sum(results.values()) or 1
    return {name: results.get(name, 0) / total for name in field}


def _rank(probs: Dict[str, float]) -> Dict[str, int]:
    """Rank drivers 1..N by win probability, highest first."""
    order = sorted(probs, key=lambda d: probs[d], reverse=True)
    return {name: i + 1 for i, name in enumerate(order)}


# --------------------------------------------------------------------------- #
# Form update
# --------------------------------------------------------------------------- #
def _perf(rank: int, field_size: int) -> float:
    """Map a finishing/predicted rank to a 0-1 performance score (1 = win)."""
    if field_size <= 1:
        return 1.0
    return 1.0 - (rank - 1) / (field_size - 1)


def update_form(
    field: Dict, finish_order: List[str], pred_rank: Dict[str, int], form_key: str,
    k: float = FORM_LEARNING_RATE, decay: float = FORM_DECAY,
    bounds: Tuple[float, float] = FORM_BOUNDS,
) -> Dict[str, Dict]:
    """Update each driver's form in place; return per-driver change report.

    finish_order: drivers in finishing order (winner first); may include names
    not in the field (they're ignored). Field drivers with no recorded finish
    decay toward neutral only.
    """
    m = len(field)
    finish_pos = {name: i + 1 for i, name in enumerate(finish_order)}
    report: Dict[str, Dict] = {}

    for d in field:
        old = field[d].get(form_key, 1.0)
        reverted = 1.0 + (old - 1.0) * (1.0 - decay)  # mean-revert toward 1.0

        if d in finish_pos and d in pred_rank:
            actual = _perf(finish_pos[d], m)
            expected = _perf(pred_rank[d], m)
            delta = actual - expected
            new = min(bounds[1], max(bounds[0], reverted + k * delta))
        else:
            delta = None
            new = reverted

        field[d][form_key] = round(new, 4)
        report[d] = {"old": round(old, 4), "new": round(new, 4),
                     "delta_perf": None if delta is None else round(delta, 3)}
    return report


# --------------------------------------------------------------------------- #
# Calibration
# --------------------------------------------------------------------------- #
def update_calibration(state: Dict, brier: float, top_pick_won: bool) -> float:
    """Nudge race variance from outcome; return the new variance_percent.

    Earned a clean call -> tighten (more confidence). Got blind-sided -> widen
    (more humility). Bounded so it drifts, never lurches.
    """
    cal = state.setdefault("calibration", {"variance_percent": 2.0, "rolling_brier": []})
    v = cal.get("variance_percent", 2.0)
    v += -VARIANCE_STEP if top_pick_won else VARIANCE_STEP
    v = min(VARIANCE_BOUNDS[1], max(VARIANCE_BOUNDS[0], v))
    cal["variance_percent"] = round(v, 3)
    cal["rolling_brier"] = (cal.get("rolling_brier", []) + [round(brier, 4)])[-8:]
    return v


# --------------------------------------------------------------------------- #
# Orchestration
# --------------------------------------------------------------------------- #
class LearningLoop:
    def __init__(self, repo_root: Optional[str] = None):
        self.loader = ConfigLoader(repo_root)
        self.field_file = self.loader.field_path / "default.json"
        self.state_file = self.loader.data_root / "season_state.json"

    def _read(self, path: Path) -> Dict:
        with open(path) as f:
            return json.load(f)

    def _write(self, path: Path, data: Dict) -> None:
        with open(path, "w") as f:
            json.dump(data, f, indent=2)

    def load_state(self) -> Dict:
        if self.state_file.is_file():
            return self._read(self.state_file)
        return {
            "season": 2026, "through_week": 0,
            "calibration": {"variance_percent": 2.0, "rolling_brier": []},
            "records": {}, "log": [],
        }

    def learn_from_race(
        self, week: int, track_key: str, finish_order: List[str],
        picks: Optional[Dict[str, str]] = None, n: int = 5000,
        write: bool = True,
    ) -> Dict:
        """Score the round, update form + calibration + records, persist."""
        picks = picks or {}
        track = self.loader.load_track_config(track_key)
        algo = self.loader.load_algorithm_version("v3.2")
        raw_field = self._read(self.field_file)
        field = raw_field["field"]
        state = self.load_state()
        var = state.get("calibration", {}).get("variance_percent")

        winner = finish_order[0]
        probs = predicted_probabilities(track, algo, field, n=n, variance_override=var)
        pred_rank = _rank(probs)
        machine_pick = min(pred_rank, key=pred_rank.get)
        picks.setdefault("Machine", machine_pick)

        brier = brier_score(probs, winner)
        form_key = "road_form" if "road" in str(track.get("track_type", "")).lower() else "oval_form"
        form_report = update_form(field, finish_order, pred_rank, form_key)
        new_var = update_calibration(state, brier, machine_pick == winner)

        # Records: only score a character if we know their pick.
        records = state.setdefault("records", {})
        for who, pick in picks.items():
            rec = records.setdefault(who, {"w": 0, "l": 0})
            if pick == winner:
                rec["w"] += 1
            else:
                rec["l"] += 1

        entry = {
            "week": week, "track": track_key, "winner": winner,
            "machine_pick": machine_pick, "machine_win_prob": round(probs.get(machine_pick, 0) * 100, 2),
            "winner_predicted_prob": round(probs.get(winner, 0) * 100, 2),
            "brier": round(brier, 4), "picks": picks,
        }
        state["log"] = state.get("log", []) + [entry]
        state["through_week"] = max(state.get("through_week", 0), week)

        report = {
            "entry": entry, "form_key": form_key, "new_variance": new_var,
            "form_movers": self._top_movers(form_report),
            "records": records, "form_report": form_report,
        }

        if write:
            self._write(self.field_file, raw_field)
            self._write(self.state_file, state)
            note = self._render_note(report, track)
            note_path = self.loader.data_root.parent.parent / "results" / f"week-{week}-{track_key}-learning.md"
            note_path.parent.mkdir(parents=True, exist_ok=True)
            note_path.write_text(note)
            report["note_path"] = str(note_path)
            report["note"] = note
        return report

    @staticmethod
    def _top_movers(form_report: Dict, k: int = 5) -> Dict[str, List]:
        moved = [(d, r["new"] - r["old"]) for d, r in form_report.items()
                 if abs(r["new"] - r["old"]) > 1e-6]
        moved.sort(key=lambda x: x[1])
        downs = [(d, round(v, 4)) for d, v in moved if v < 0][:k]
        ups = [(d, round(v, 4)) for d, v in reversed(moved) if v > 0][:k]
        return {"up": ups, "down": downs}

    @staticmethod
    def _render_note(report: Dict, track: Dict) -> str:
        e = report["entry"]
        hit = "HIT" if e["machine_pick"] == e["winner"] else "MISS"
        lines = [
            f"# What The Machine Learned - Week {e['week']} ({track.get('track_name', e['track'])})",
            "",
            f"Winner: {e['winner']}. Machine pick: {e['machine_pick']} "
            f"({e['machine_win_prob']}%) -> {hit}.",
            f"The winner was given {e['winner_predicted_prob']}% pre-race. "
            f"Brier {e['brier']} (lower is sharper).",
            "",
            f"Confidence recalibrated: race variance -> {report['new_variance']} "
            f"({'tighter, earned' if hit == 'HIT' else 'wider, humbled'}).",
            "",
            f"Form moves ({report['form_key']}):",
        ]
        for d, v in report["form_movers"]["up"]:
            lines.append(f"  up   {d}: {v:+.3f}  (Machine underrated)")
        for d, v in report["form_movers"]["down"]:
            lines.append(f"  down {d}: {v:+.3f}  (Machine overrated)")
        recs = ", ".join(f"{who} {r['w']}-{r['l']}" for who, r in report["records"].items())
        lines += ["", f"Standings: {recs}"]
        return "\n".join(lines) + "\n"


# --------------------------------------------------------------------------- #
# CLI
# --------------------------------------------------------------------------- #
def main(argv: Optional[List[str]] = None) -> int:
    import argparse

    p = argparse.ArgumentParser(description="Run The Machine's post-race learning loop.")
    p.add_argument("--week", type=int, required=True)
    p.add_argument("--track", default="sonoma")
    p.add_argument("--finish", required=True,
                   help="Finishing order, winner first, comma-separated driver names")
    p.add_argument("--mikey", default=None, help="Mikey's pick (driver name)")
    p.add_argument("--jill", default=None, help="Jill's pick (driver name)")
    p.add_argument("-n", "--num-simulations", type=int, default=5000)
    p.add_argument("--dry-run", action="store_true", help="Preview without writing")
    args = p.parse_args(argv)

    finish = [s.strip() for s in args.finish.split(",") if s.strip()]
    picks = {}
    if args.mikey:
        picks["Mikey"] = args.mikey
    if args.jill:
        picks["Jill"] = args.jill

    loop = LearningLoop()
    report = loop.learn_from_race(args.week, args.track, finish, picks,
                                  n=args.num_simulations, write=not args.dry_run)
    print(report.get("note") or LearningLoop._render_note(report, loop.loader.load_track_config(args.track)))
    if not args.dry_run:
        print(f"(written: {report.get('note_path')}, field + season_state updated)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
