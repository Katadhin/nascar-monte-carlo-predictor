# NASCAR Prediction Engine - Development Guide

## Quick Start for Cowork

### Step 1: Clone the Repo to Your Cowork Workspace
```bash
cd ~/Cowork  # or your Cowork workspace folder
git clone https://github.com/Katadhin/nascar-monte-carlo-predictor.git nascar-predictor
cd nascar-predictor
```

### Step 2: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 3: Verify Current Setup
```bash
python simulators/sonoma_simulator_v3.py
# Should output top 10 predictions + confidence levels
```

---

## Project Goals (2026 Season)

### Primary Goal
Build a **modular, reusable prediction engine** that:
- ✅ Runs simulations for any track (not one-off scripts)
- ✅ Tracks character picks vs actual results
- ✅ Updates algorithm based on learnings (v3.0 → v3.1 → ?)
- ✅ Generates weekly predictions + confidence levels
- ✅ Documents algorithm evolution over season

### Current State (Week 18 - Sonoma)
- ❌ Simulators are isolated scripts (hard to reuse, modify)
- ❌ Parameter tweaking requires code edits (not config-driven)
- ❌ Results tracking manual (not automated)
- ❌ Algorithm changes hardcoded (not version-controlled)

### Improved State (Target)
- ✅ One core engine, modular track configs
- ✅ YAML/JSON parameter files (easy tweaks)
- ✅ Automated results tracking & comparison
- ✅ Algorithm versions with changelogs
- ✅ Weekly automation scripts

---

## Development Roadmap

### Phase 1: Refactor Core Engine (Week 1)
**Goal:** One reusable simulator, not individual scripts

**Tasks:**
1. Create `engine/core_simulator.py` (base class)
2. Create `tracks/` directory with individual track configs
3. Refactor simulators into track-specific subclasses
4. Test: Run core engine with Pocono config → should match old output

**Outcome:** One engine, multiple tracks, easy to add new ones

---

### Phase 2: Configuration System (Week 1-2)
**Goal:** Change track parameters without editing code

**Tasks:**
1. Create `config/track_parameters.yaml` template
2. Move all hardcoded values → YAML config
3. Create `config/algorithm_versions.yaml` (v3.0, v3.1, v3.2 params)
4. Build config loader in core engine

**Outcome:** Edit YAML, run engine. No code changes needed.

---

### Phase 3: Results Tracking & Automation (Week 2)
**Goal:** Automated weekly predictions + result logging

**Tasks:**
1. Create `scripts/run_weekly_prediction.py` (automation script)
2. Create `results/predictions/` directory (store weekly outputs)
3. Build `results/results_tracker.py` (compares picks vs actual)
4. Create `scripts/generate_weekly_report.py` (markdown recap)

**Outcome:** One command = prediction + results logging + report generation

---

### Phase 4: Algorithm Versioning (Week 2-3)
**Goal:** Track algorithm evolution systematically

**Tasks:**
1. Create `algorithm/` directory with version subdirs
2. Move v3.0, v3.1 parameters to separate files
3. Build `algorithm/version_manager.py` (track changes)
4. Create `ALGORITHM_CHANGELOG.md` (auto-generated)

**Outcome:** Clear history of what changed, why, when

---

### Phase 5: Dashboard & Analytics (Week 3-4)
**Goal:** Weekly tracking visualization

**Tasks:**
1. Create `analytics/predictor_stats.py` (win %, records, trends)
2. Build `analytics/algorithm_performance.py` (accuracy by track type)
3. Generate weekly JSON outputs for charting
4. Optional: Simple HTML dashboard

**Outcome:** See performance trends, algorithm effectiveness, character arcs

---

## File Structure (Target)

```
nascar-predictor/
├── engine/
│   ├── __init__.py
│   ├── core_simulator.py          # ONE reusable engine
│   ├── track_simulator.py         # Track-specific subclass
│   └── utils.py                   # Helper functions
│
├── tracks/
│   ├── config_template.yaml       # Template for new tracks
│   ├── pocono.yaml                # Pocono parameters
│   ├── sonoma.yaml                # Sonoma parameters
│   ├── michigan.yaml              # etc.
│   └── README.md                  # How to add new tracks
│
├── config/
│   ├── algorithm_versions.yaml    # v3.0, v3.1, v3.2 params
│   ├── track_weights.yaml         # Universal track type weights
│   └── defaults.yaml              # Global defaults
│
├── algorithm/
│   ├── v3_0/                      # v3.0 baseline
│   │   ├── README.md
│   │   └── parameters.yaml
│   ├── v3_1/                      # v3.1 post-San Diego update
│   │   ├── README.md              # What changed + why
│   │   └── parameters.yaml
│   └── version_manager.py         # Track versions
│
├── scripts/
│   ├── run_weekly_prediction.py   # Automation: predict + log
│   ├── generate_weekly_report.py  # Create markdown recap
│   ├── compare_picks.py           # Picks vs actual results
│   └── batch_run_season.py        # Run all races
│
├── results/
│   ├── predictions/               # Weekly prediction outputs
│   │   ├── week_18_sonoma.json
│   │   ├── week_17_sandiego.json
│   │   └── ...
│   ├── results/                   # Race results + tracking
│   │   └── 2026_season_results.json
│   └── reports/                   # Generated markdown recaps
│       ├── week_18_sonoma_report.md
│       └── ...
│
├── analytics/
│   ├── predictor_stats.py         # Character performance
│   ├── algorithm_performance.py   # Algorithm accuracy by track
│   └── trends.py                  # Season trends
│
├── campaign/
│   ├── character_records.md       # (existing)
│   ├── season_narrative.md        # (existing)
│   └── algorithm_changelog.md     # (existing)
│
├── simulators/
│   ├── sandiego_simulator_v3.py   # (legacy, archive)
│   └── sonoma_simulator_v3.py     # (legacy, will refactor)
│
├── DEVELOPMENT_GUIDE.md           # (this file)
├── PROJECT_ARCHITECTURE.md        # System design
├── CODEBASE_IMPROVEMENTS.md       # Specific refactors
├── FILES_MANIFEST.md              # File descriptions
├── README.md                       # (updated)
└── requirements.txt
```

---

## How to Use (Weekly Workflow)

### Sunday After Race
```bash
cd nascar-predictor

# 1. Record actual results
python scripts/compare_picks.py --week 18 --winner "Kyle Larson" --placement 1

# 2. Generate report
python scripts/generate_weekly_report.py --week 18 --track "Sonoma"

# 3. Check trends
python analytics/predictor_stats.py --season 2026

# Done! Report auto-generated at results/reports/week_18_report.md
```

### Next Race Prep (Tuesday)
```bash
# 1. Get next race details
python scripts/get_next_race.py

# 2. Run prediction
python scripts/run_weekly_prediction.py --week 19 --track "next_track"

# 3. Output stored at results/predictions/week_19_*.json
# Share with team, await Jill & Mikey picks
```

---

## Development Best Practices

### 1. Configuration First
- **NEVER** hardcode values in Python
- **ALWAYS** use YAML/JSON configs
- Make parameters tunable without code changes

### 2. Modular Design
- One class = one responsibility
- Core engine independent of track configs
- Easy to add new tracks (just add YAML)

### 3. Version Control
- Tag algorithm versions (v3.0, v3.1, etc.)
- Document why each version changed
- Keep old versions for comparison

### 4. Automated Testing
- Test core engine with old track configs
- Verify outputs match previous simulators
- Build confidence in refactored code

### 5. Documentation
- Every module needs a docstring
- Track parameters explained in YAML comments
- Algorithm changes documented in changelog

---

## Quick Command Reference

```bash
# Setup
git clone <repo> && cd nascar-predictor
pip install -r requirements.txt

# Development
python -m pytest tests/               # Run tests (when built)
python scripts/run_weekly_prediction.py --week 18 --track "sonoma"
python scripts/generate_weekly_report.py --week 18

# Analytics
python analytics/predictor_stats.py --season 2026
python analytics/algorithm_performance.py --version "v3.1"

# Archive (old individual simulators)
python simulators/sonoma_simulator_v3.py  # Legacy - migrate to new engine
```

---

## Success Metrics

By end of Phase 5, you should have:

✅ **One reusable engine** (not 5+ individual scripts)
✅ **Easy parameter tweaking** (YAML configs, no code edits)
✅ **Automated weekly workflow** (one command = full update)
✅ **Algorithm versioning** (clear history of changes)
✅ **Performance tracking** (see trends over season)
✅ **Better codebase** (modular, maintainable, scalable)

---

## Next Steps

1. **Read** `PROJECT_ARCHITECTURE.md` (how to structure the code)
2. **Read** `CODEBASE_IMPROVEMENTS.md` (specific refactors needed)
3. **Read** `FILES_MANIFEST.md` (what each file should do)
4. **Start with Phase 1:** Build core engine + refactor existing simulators
5. **Test:** Verify new engine matches old outputs

---

## Need Help?

- Unclear on refactoring strategy? → Read `PROJECT_ARCHITECTURE.md`
- Not sure what to change? → Read `CODEBASE_IMPROVEMENTS.md`
- Don't know what a file does? → Read `FILES_MANIFEST.md`
- Ready to start coding? → Begin Phase 1 from Roadmap section

---

**Last Updated:** June 27, 2026
**Status:** Ready for Cowork development
**Timeline:** 4 weeks to fully refactored, automated system
