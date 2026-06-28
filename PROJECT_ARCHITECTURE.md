# NASCAR Prediction Engine - Project Architecture

## System Overview

### Current Problem
- **5+ individual simulator scripts** (each one-off, hard to reuse)
- **Hardcoded parameters** (changes require code edits)
- **Manual results tracking** (not automated)
- **Algorithm changes scattered** (hard to track evolution)

### Solution Architecture
- **One core engine** (pluggable, track-agnostic)
- **Configuration-driven** (YAML files for parameters)
- **Automated pipeline** (prediction → results → reporting)
- **Versioned algorithms** (clear evolution tracking)

---

## Core Engine Architecture

### Layer 1: Core Simulator Engine
**File:** `engine/core_simulator.py`

**Purpose:** The ONLY algorithm implementation (used for all tracks)

**Responsibilities:**
- Run Monte Carlo simulations
- Apply track-agnostic logic (variance, tire wear, pit strategy)
- Track driver performance metrics
- Output standardized results

**Interface:**
```python
class CoreSimulator:
    def __init__(self, config: dict):
        # Load track parameters, driver data, algorithm version
        
    def run_simulation(self, num_simulations: int = 10000):
        # Execute Monte Carlo, return results
        
    def get_top_predictions(self, n: int = 10):
        # Return top N drivers with confidence %
        
    def export_results(self, format: str = 'json'):
        # Save to JSON for tracking/analytics
```

**Key Insight:** This class is **track-agnostic**. All track-specific logic comes from config, not code.

---

### Layer 2: Track Configuration System
**Files:** `config/track_parameters.yaml`, `tracks/*.yaml`

**Purpose:** Define track-specific parameters (no code changes needed)

**Structure:**
```yaml
# tracks/sonoma.yaml
track_name: "Sonoma Raceway"
track_type: "traditional_road_course"
distance_miles: 1.99
laps: 110
avg_speed_mph: 110
lap_time_seconds: 64.6

# Track-specific bonuses/penalties
braking_events_per_lap: 12
elevation_changes: true
caution_probability: 0.035

# Driver base parameters (override defaults)
driver_adjustments:
  "Kyle Larson":
    local_knowledge_bonus: 0.03
    sonoma_wins: 2
  "Shane van Gisbergen":
    recent_dnf_penalty: 0.15
    defending_champ_bonus: 0.02
```

**Key Insight:** Change parameters → change track behavior. Zero code edits needed.

---

### Layer 3: Algorithm Version Management
**Files:** `algorithm/v3_0/`, `algorithm/v3_1/`, `algorithm/version_manager.py`

**Purpose:** Track algorithm evolution, apply versions consistently

**Structure:**
```
algorithm/
├── v3_0/
│   ├── parameters.yaml          # v3.0 baseline parameters
│   ├── README.md                # What v3.0 does
│   └── weights.yaml             # Dominance weighting, etc.
│
├── v3_1/
│   ├── parameters.yaml          # Post-San Diego updates
│   ├── README.md                # San Diego learning changes
│   ├── weights.yaml             # Consistency weighting
│   └── CHANGELOG.md             # Specific code changes
│
└── version_manager.py           # Load correct version
```

**Version Manager Interface:**
```python
class AlgorithmVersionManager:
    def get_version(self, version: str) -> dict:
        # Load v3.0, v3.1, v3.2, etc. parameters
        
    def list_versions(self) -> list:
        # Show all available versions
        
    def compare_versions(self, v1: str, v2: str) -> dict:
        # Show what changed between versions
```

**Key Insight:** Algorithms are treated as **products with versions**, not monolithic code.

---

### Layer 4: Results Pipeline
**Files:** `scripts/run_weekly_prediction.py`, `results/predictions/`, `analytics/`

**Purpose:** Automate prediction → recording → analysis flow

**Pipeline Flow:**
```
1. run_weekly_prediction.py
   ├─ Loads track config (e.g., sonoma.yaml)
   ├─ Loads algorithm version (e.g., v3.1)
   ├─ Runs CoreSimulator
   ├─ Saves output: results/predictions/week_18_sonoma.json
   └─ Records: Jill's pick, Mikey's pick, Machine's pick

2. Post-race: compare_picks.py
   ├─ Loads actual winner
   ├─ Compares vs predictions
   ├─ Updates: results/results_tracker.json
   └─ Records: who was right/wrong

3. generate_weekly_report.py
   ├─ Reads predictions + results
   ├─ Calculates: wins, losses, trends
   ├─ Creates: results/reports/week_18_report.md
   └─ Updates: campaign/ character records
```

**Key Insight:** Entire workflow is **automated and trackable**.

---

## Data Flow Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                      PREDICTION PHASE                       │
└─────────────────────────────────────────────────────────────┘

Track Config (YAML)  ──┐
Algorithm Params (YAML)─┼──> CoreSimulator ──> Predictions (JSON)
Driver Data (dict)    ──┘         (Python)       Top 10 drivers
                                                  + Confidence %

┌─────────────────────────────────────────────────────────────┐
│                       TRACKING PHASE                        │
└─────────────────────────────────────────────────────────────┘

Character Picks ──────┐
                       ├──> Results Tracker ──> Analytics
Actual Winner ─────────┤       (Python)          (Python)
Predictions (JSON) ────┘
                                    ↓
                           Weekly Report (MD)
                           Character Stats
                           Algorithm Performance

```

---

## Module Responsibilities

### `engine/`
- `core_simulator.py` - The ONE algorithm (all tracks use this)
- `track_simulator.py` - Subclass with track-specific preprocessing
- `utils.py` - Helper functions (variance, tire wear calculations, etc.)

**Responsibility:** Pure simulation logic, parameter application, output generation

---

### `config/`
- `algorithm_versions.yaml` - v3.0, v3.1, v3.2 parameter sets
- `track_parameters.yaml` - Template for track configs
- `defaults.yaml` - Global defaults

**Responsibility:** All configurable values live here (never hardcoded)

---

### `tracks/`
- `pocono.yaml`, `sonoma.yaml`, `michigan.yaml`, etc.
- `config_template.yaml` - Example for new tracks

**Responsibility:** Track-specific parameters (distance, lap time, caution probability, etc.)

---

### `algorithm/`
- `v3_0/`, `v3_1/`, `v3_2/` subdirectories
- Each version has `parameters.yaml`, `README.md`, `CHANGELOG.md`
- `version_manager.py` - Load/compare versions

**Responsibility:** Algorithm history, versioning, comparison logic

---

### `scripts/`
- `run_weekly_prediction.py` - Predict next race
- `generate_weekly_report.py` - Create markdown recap
- `compare_picks.py` - Record actual results
- `batch_run_season.py` - Run all races at once

**Responsibility:** Automation, weekly workflows, orchestration

---

### `analytics/`
- `predictor_stats.py` - Character performance (Jill 3-6, etc.)
- `algorithm_performance.py` - Accuracy by track type
- `trends.py` - Season trends over time

**Responsibility:** Analytics, insights, performance tracking

---

### `results/`
- `predictions/` - Weekly JSON outputs (predictions by race)
- `results/` - Master tracker (all picks + results)
- `reports/` - Auto-generated markdown recaps

**Responsibility:** Data storage, results tracking, report generation

---

## Design Principles

### 1. Configuration Over Code
- Parameters in YAML, not Python
- Change behavior by editing files, not code
- Config files are the source of truth

### 2. Single Responsibility
- Core engine = simulation only
- Config system = parameter management
- Scripts = automation/orchestration
- Analytics = insights/tracking

### 3. Pluggability
- New track? Add YAML file (no code changes)
- New algorithm version? Add `algorithm/v3_2/` folder
- New analysis? Add analytics module (doesn't touch core)

### 4. Testability
- Core engine can be tested in isolation
- Config can be tested separately
- Results can be verified against known outputs

### 5. Versioning
- Algorithm versions tracked explicitly
- Track configs versioned with repo
- Results tied to algorithm version + config date

---

## Class Hierarchy

```
CoreSimulator (base class)
├── TrackSimulator (subclass for track-specific preprocessing)
├── AlgorithmVersionManager (version loading/comparison)
├── ConfigLoader (YAML loading)
├── ResultsTracker (pick/result recording)
└── AnalyticsEngine (performance calculation)
```

---

## Data Structures

### Prediction Output (JSON)
```json
{
  "race": "Sonoma",
  "week": 18,
  "date": "2026-06-28",
  "algorithm_version": "v3.1",
  "config_date": "2026-06-27",
  "predictions": [
    {
      "rank": 1,
      "driver": "Kyle Larson",
      "number": 5,
      "wins": 2453,
      "percentage": 24.53
    },
    // ... more drivers
  ]
}
```

### Results Tracker (JSON)
```json
{
  "week": 18,
  "race": "Sonoma",
  "actual_winner": "Kyle Larson",
  "picks": {
    "machine": {
      "pick": "Kyle Larson #5",
      "confidence": 24.53,
      "correct": true
    },
    "jill": {
      "pick": "TBD",
      "correct": null
    },
    "mikey": {
      "pick": "Shane van Gisbergen #97",
      "correct": false
    }
  },
  "records": {
    "machine": "2-16",
    "jill": "3-6",
    "mikey": "4-12"
  }
}
```

---

## Refactoring Strategy

### Step 1: Extract Core Logic
- Take `sonoma_simulator_v3.py`
- Remove hardcoded values → move to config
- Remove track-specific tweaks → move to subclass
- Extract pure algorithm → `core_simulator.py`

### Step 2: Build Configuration System
- Create `tracks/sonoma.yaml` with all parameters
- Create `config/algorithm_versions.yaml` with v3.0 + v3.1
- Build `ConfigLoader` class
- Test: Core engine + Sonoma config = old output

### Step 3: Build Automation Scripts
- `run_weekly_prediction.py` uses core engine + config
- `compare_picks.py` records results
- `generate_weekly_report.py` creates markdown

### Step 4: Algorithm Versioning
- Create `algorithm/v3_0/` (baseline)
- Create `algorithm/v3_1/` (post-San Diego)
- Build version manager
- Test: v3.1 produces different results than v3.0

### Step 5: Analytics & Dashboard
- Build `predictor_stats.py`
- Build `algorithm_performance.py`
- Generate weekly trends
- Optional: HTML dashboard

---

## Success Criteria

By end of refactoring:

✅ **Zero hardcoded values** in Python (all in YAML)
✅ **One core engine** (no duplicate simulators)
✅ **Easy track addition** (just add YAML, no code)
✅ **Automated workflow** (one command = full week)
✅ **Algorithm versioning** (clear history)
✅ **Performance tracking** (automated analytics)
✅ **Maintainability** (modular, testable, documented)

---

**Last Updated:** June 27, 2026
**Status:** Ready for implementation
**Estimated Timeline:** 4 weeks to complete refactor
