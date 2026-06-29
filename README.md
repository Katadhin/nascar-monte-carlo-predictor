# 🏁 NASCAR Monte Carlo Predictor
## Michael vs Machine — 2026 Season Battle

[![Python](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![NumPy](https://img.shields.io/badge/numpy-1.24+-orange.svg)](https://numpy.org/)
[![Tests](https://img.shields.io/badge/tests-25%20passing-brightgreen.svg)](tests/)
[![Campaign Status](https://img.shields.io/badge/campaign-active-brightgreen.svg)](https://github.com/Katadhin/nascar-monte-carlo-predictor)

[![Machine Record](https://img.shields.io/badge/🤖%20machine-2--16%20(11%25)-red.svg)](https://github.com/Katadhin/nascar-monte-carlo-predictor)
[![Mikey Record](https://img.shields.io/badge/🏎️%20mikey-5--12%20(29%25)-yellow.svg)](https://github.com/Katadhin/nascar-monte-carlo-predictor)
[![Jill Record](https://img.shields.io/badge/☕%20jill-3--6%20(33%25)-brightgreen.svg)](https://github.com/Katadhin/nascar-monte-carlo-predictor)

[![Model Version](https://img.shields.io/badge/model-v3.2-purple.svg)](campaign/algorithm-changelog.md)
[![Last Race](https://img.shields.io/badge/week%2018-Sonoma-orange.svg)](results/2026-race-picks-results.json)
[![Next Race](https://img.shields.io/badge/next%20race-Chicagoland%20Jul%205-blue.svg)](https://github.com/Katadhin/nascar-monte-carlo-predictor)
[![Simulations](https://img.shields.io/badge/simulations-5%2C000%2Frace-blueviolet.svg)](engine/core_simulator.py)
[![Learning](https://img.shields.io/badge/learning-loop%20+%20audit-success.svg)](engine/learning.py)
[![Learning in Public](https://img.shields.io/badge/built-in%20public-success.svg)](https://github.com/Katadhin/nascar-monte-carlo-predictor)

> 🎲 A Monte Carlo simulation engine predicting NASCAR Cup Series winners, racing head-to-head every week against 2x Daytona 500 champion **Michael Waltrip** and MWB strategist **Jill** — a model that doesn't hide its picks, it shows its mind, and gets a little less wrong each week.

**Current status (through Week 18, Sonoma): The Machine sits 2-16 — and just rebuilt itself overnight.** 🤖🔧

---

## 📊 Season Standings (Through Week 18 — Sonoma)

| Predictor | Record | Win % | Method | Status |
|-----------|--------|-------|--------|--------|
| ☕ **Jill** | 3-6 | **33.3%** 🥇 | Momentum + narrative reads | Best record, on top |
| 🏎️ **Mikey** | 5-12 | 29.4% | 40 years of instinct | Hot — nailed Sonoma |
| 🤖 **Machine** | 2-16 | 11.1% | 5,000 Monte Carlo sims | Rebuilt to v3.2 |

```
Jill:    ██████████ 33% 🥇 LEADING
Mikey:   █████████░ 29% 🔥 CLIMBING
Machine: ███░░░░░░░ 11% 🔧 REBUILT
```

> Jill held the lead from a beach chair — she was on vacation for Sonoma and made no pick, so her record stood pat while the others swung.

---

## 🏁 Recent Results (Weeks 14–18)

Full race-by-race history lives in [`results/2026-race-picks-results.json`](results/2026-race-picks-results.json).

| Week | 🏟️ Track | 🏆 Winner | 🤖 Machine | 🏎️ Mikey | ☕ Jill | Result |
|------|----------|-----------|------------|----------|--------|--------|
| 14 | Nashville | Denny Hamlin | Blaney (8th) ❌ | **Hamlin ✅** | Bell (2nd) ❌ | Mikey calls it |
| 15 | Michigan | Denny Hamlin | Larson (4th) ❌ | Bell (DNF) ❌ | **Hamlin ✅** | Jill debuts 1-0 |
| 16 | Pocono | Denny Hamlin | **Hamlin ✅** | Hocevar ❌ | — | "Corners are data" |
| 17 | San Diego | **Corey Heim** | Elliott ❌ | SVG (DNF) ❌ | SVG (DNF) ❌ | 0-for-3. Chaos. |
| 18 | Sonoma | **Shane van Gisbergen** | Larson (4th) ❌ | **SVG ✅** | 🏖️ vacation | Mikey again |

**Sonoma in one line:** SVG held off Chase Briscoe by 0.357s for the second straight year and swept the weekend — his 8th career road-course win, tying Tony Stewart for second all-time.

---

## 🔧 The Sonoma Rebuild (v3.1 → v3.2)

The most honest result of the season isn't a pick. It's a bug we found *after* the race.

**What happened:** v3.1 confidently picked Kyle Larson at 24.5% for Sonoma. Larson ran 4th. A clean miss. Moving the project into an environment that could actually run, test, and stress the model — not just generate it — surfaced *why* it missed, and it wasn't bad luck.

**Two broken assumptions:**

1. **A near-deterministic finish.** The model effectively decided races on a final-lap coin flip instead of race-long pace.
2. **Compressed skill ratings.** Drivers were packed so tightly that a 3% input nudge swung a driver **77 points**, and confidence ballooned past **70%** in the learning loop. The model *looked* precise. It was brittle. Those two feel identical right up until they don't.

**The fix (v3.2):** a proportional finish (winner drawn by race-long pace) plus widened skill ratings. Favorites dropped from a falsely confident 24% to a realistic **16%**. That same 3% nudge now moves ~5 points instead of 77. **25 tests green** (15 v3.1 parity + 10 v3.2/learning).

**The kicker:** rebuilt v3.2 picks **Shane van Gisbergen at 16.2%** for Sonoma — the driver who actually won. The old model was confidently wrong. The new one is humbly right.

> 📓 Full technical history in [`campaign/algorithm-changelog.md`](campaign/algorithm-changelog.md).

---

## 🧠 How The Machine Learns (Two Layers)

The engine improves on two clocks, and the split is deliberate: **if the fix is a number, the loop owns it. If the fix is a belief, a human signs off.**

### Layer 1 — The Learning Loop (`engine/learning.py`) ✅ live
Runs automatically after every race. Bounded and leashed on purpose.
- Updates per-driver **form** (a decaying, bounded multiplier, separate for road and oval) based on how drivers finished versus what the Machine predicted.
- Recalibrates **confidence** via Brier score — humbler after blind-side losses, sharper after clean calls.
- Writes a plain-English *"what the Machine learned"* note.
- **Deliberately does NOT** rewrite driver skill ratings or algorithm weights. The repo's own history is the reason: after San Diego the model hard-coded a one-race "lesson" (penalize SVG's DNF) — and SVG won the next week. A loop that lurches on every result repeats that mistake weekly.

### Layer 2 — The Race Audit Agent 🛠️ in design
A human-in-the-loop layer that questions the model's *assumptions* — the structural stuff the loop won't touch. After each race it runs a fixed diagnostic battery (calibration, segment accuracy, blind spots, stability, drift), then proposes at most three ranked changes that **a human decides on**. Every suggestion, decision, and downstream result is logged, so the project can actually measure its central question: *can a human and a machine get better together?*

```bash
# Run the weekly learning loop after a race
python -m engine.learning --week 18 --track sonoma \
  --finish "Shane van Gisbergen,Chase Briscoe,Ty Gibbs,Kyle Larson,Christopher Bell" \
  --mikey "Shane van Gisbergen"
```

---

## 🛠️ Technical Details

### Architecture

```
score = Σ (track-relevant skill attributes × track-type weights)
        × form (bounded, learned)
        × chaos variance (calibrated per race)
```

The model picks attributes and weights by **track type** — drafting and chaos survival on superspeedways, tire management and restarts on intermediates, braking zones and road skill on road courses. See [`docs/TRACK_TYPES.md`](docs/TRACK_TYPES.md).

### Repository Structure

```
nascar-monte-carlo-predictor/
│
├── engine/                     # The v3.2 core
│   ├── core_simulator.py       # Monte Carlo race simulation
│   ├── learning.py             # Layer 1: post-race learning loop
│   ├── config.py               # Track / algorithm / field loader
│   └── data/
│       ├── tracks/             # Per-track configs (sonoma.json, …)
│       ├── algorithms/         # v3.1, v3.2 parameter sets
│       ├── field/              # Driver ratings (default.json)
│       └── season_state.json   # Records, calibration, form (live)
│
├── simulators/                 # Standalone per-track scripts (history)
├── campaign/                   # Records, narrative, algorithm changelog
├── results/                    # Race picks JSON + weekly learning notes
├── tests/                      # 25 tests (v3.1 parity + v3.2/learning)
└── docs/                       # Methodology, track types
```

### Quick Start

```bash
git clone https://github.com/Katadhin/nascar-monte-carlo-predictor.git
cd nascar-monte-carlo-predictor
pip install -r requirements.txt

# Run the test suite
python -m pytest -q

# Run the post-race learning loop (see example above)
python -m engine.learning --help
```

---

## 💭 The Bottom Line

The Machine is 2-16. The veteran is beating it. The newcomer is beating both.

That's the point. This was never about an AI replacing human judgment in a chaotic system — it's about watching where instinct still wins, and building a model honest enough to show its work, own its losses, and improve in public. Sonoma proved both halves at once: the human (Mikey) called it, and the machine, when rebuilt honestly, would have too.

**Next up: Chicagoland Speedway, Sunday July 5 — a 1.5-mile intermediate, and v3.2's first real test.**

---

## 📱 Follow the Campaign

- 🏁 **Michael Waltrip Brands:** [Facebook](https://facebook.com/MichaelWaltripBrands) | [Twitter/X](https://x.com/WaltripBrewing) | [Instagram](https://instagram.com/michaelwaltrip)
- 🏆 **Michael Waltrip:** [Twitter/X](https://x.com/MW55)
- 👤 **John Andrews:** [Twitter/X](https://x.com/Katadhin) | [LinkedIn](https://linkedin.com/in/johnandrewsnc) | [GitHub](https://github.com/Katadhin)
- 📝 **Medium:** [Full Campaign Story](https://medium.com/@katadhin/can-racing-instinct-beat-algorithms-were-testing-it-every-week-6cfb2217ae73)

---

## 📜 License

MIT License — see [LICENSE](LICENSE). Use it, modify it, learn from our mistakes. Just don't claim the Machine is good at predictions yet. 😄

<div align="center">

### 🏁 Built in public, one humbling Sunday at a time

**Star the repo if you enjoy watching a model learn the hard way** ⭐

[![GitHub stars](https://img.shields.io/github/stars/Katadhin/nascar-monte-carlo-predictor?style=social)](https://github.com/Katadhin/nascar-monte-carlo-predictor)
[![Follow @WaltripBrewing](https://img.shields.io/twitter/follow/WaltripBrewing?style=social)](https://x.com/WaltripBrewing)
[![Follow @MW55](https://img.shields.io/twitter/follow/MW55?style=social)](https://x.com/MW55)
[![Follow @Katadhin](https://img.shields.io/twitter/follow/Katadhin?style=social)](https://x.com/Katadhin)

</div>

---

*Last updated: June 29, 2026 — Week 18 (Sonoma) complete, v3.2 live.*
*Next race: Chicagoland Speedway — Sunday, July 5, 2026.*
