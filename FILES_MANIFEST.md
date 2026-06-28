# Files Manifest - Complete Reference Guide

## Directory Structure Overview

```
nascar-predictor/
├── engine/                          # Core simulation engine
├── config/                          # Global configuration
├── tracks/                          # Track-specific configs
├── algorithm/                       # Algorithm versions (v3.0, v3.1, etc.)
├── scripts/                         # Automation & workflow scripts
├── results/                         # Predictions, results, reports
├── analytics/                       # Performance analysis & insights
├── campaign/                        # Campaign documentation
├── simulators/                      # Legacy simulator scripts (archive)
└── tests/                           # Test suite
```

---

## CORE ENGINE (`engine/`)

### `engine/core_simulator.py` (NEW - CREATE THIS)
**Purpose:** The ONE simulation engine used for all tracks

**Responsibilities:**
- Load configuration (track params + algorithm version)
- Run Monte Carlo simulations
- Apply driver-specific bonuses/penalties
- Track performance metrics (tire wear, position changes, etc.)
- Output standardized results

**Key Methods:**
```python
class CoreSimulator:
    def __init__(self, track_config: dict, algorithm_params: dict):
        """Initialize with track config + algorithm version"""
        
    def run_simulation(self, num_simulations: int = 10000) -> dict:
        """Execute Monte Carlo, return results by driver"""
        
    def get_top_predictions(self, n: int = 10) -> list:
        """Return top N drivers with confidence percentages"""
        
    def export_results(self, filepath: str, format: str = 'json'):
        """Save results to JSON file"""
```

**Input:** Track config (YAML dict) + Algorithm params (YAML dict)
**Output:** `{"driver_name": win_count, ...}` or JSON file

**Start:** Extract algorithm logic from `sonoma_simulator_v3.py`, parameterize everything

---

### `engine/track_simulator.py` (NEW - CREATE THIS)
**Purpose:** Subclass for track-specific preprocessing (optional)

**Responsibilities:**
- Apply track-specific driver adjustments
- Pre-process driver data for that track
- Validate track config completeness

**Key Method:**
```python
class TrackSimulator(CoreSimulator):
    def __init__(self, track_name: str, algorithm_version: str):
        """Load track config + algorithm version, initialize parent"""
        config = ConfigLoader().load_track_config(track_name)
        algo_params = ConfigLoader().load_algorithm_version(algorithm_version)
        super().__init__(config, algo_params)
```

**Usage:**
```python
sim = TrackSimulator(track_name="sonoma", algorithm_version="v3.1")
results = sim.run_simulation(num_simulations=10000)
```

---

### `engine/utils.py` (NEW - CREATE THIS)
**Purpose:** Helper functions used by core simulator

**Responsibilities:**
- Variance calculation (random driver performance variation)
- Tire wear calculations
- Position determination logic
- Bonus/penalty application

**Key Functions:**
```python
def apply_variance(base_value: float, variance_pct: float) -> float:
    """Apply random variance to a value"""
    
def calculate_tire_wear(laps: int, lap_quality: float) -> float:
    """Calculate tire wear over race"""
    
def apply_performance_bonuses(base_speed: float, bonuses: dict) -> float:
    """Apply all bonuses/penalties to driver speed"""
    
def determine_finishing_position(driver_performance: dict) -> int:
    """Rank drivers by performance"""
```

**Start:** Extract helper functions from existing simulators

---

### `engine/config.py` (NEW - CREATE THIS)
**Purpose:** Configuration loading and validation

**Responsibilities:**
- Load YAML track configs
- Load YAML algorithm versions
- Validate completeness (required fields present)
- Provide default values for missing fields

**Key Class:**
```python
class ConfigLoader:
    def load_track_config(self, track_name: str) -> dict:
        """Load tracks/{track_name}.yaml"""
        
    def load_algorithm_version(self, version: str) -> dict:
        """Load algorithm/{version}/parameters.yaml"""
        
    def validate_track_config(self, config: dict) -> bool:
        """Ensure all required fields present"""
        
    def validate_algorithm_config(self, config: dict) -> bool:
        """Ensure algorithm version has all required fields"""
```

---

## CONFIGURATION (`config/`)

### `config/defaults.yaml` (NEW - CREATE THIS)
**Purpose:** Global default values used across all tracks

**Structure:**
```yaml
# Default parameters applied to all tracks (override in track YAML)
simulation:
  num_simulations: 10000
  random_seed: null           # null = truly random
  
driver_defaults:
  base_speed: 140
  tire_wear_rate: 1.0
  
performance:
  variance_percent: 2.0       # Standard variance
  caution_probability: 0.03   # Default caution rate
  
weighting:
  # These are v3.0 defaults, overridden by algorithm version files
  dominance_weight: 0.05
  consistency_weight: 0.03
```

**Usage:** ConfigLoader applies these, then overrides with track-specific values

---

### `config/algorithm_versions.yaml` (NEW - CREATE THIS)
**Purpose:** Index of all algorithm versions (which folder to use)

**Structure:**
```yaml
versions:
  v3.0:
    name: "Baseline v3.0"
    description: "Original dominance-focused algorithm"
    path: "algorithm/v3.0"
    active: false
    
  v3.1:
    name: "Post-San Diego v3.1"
    description: "Consistency weighting, local knowledge bonus"
    path: "algorithm/v3.1"
    active: true
    
  v3.2:
    name: "TBD Future"
    description: "TBD"
    path: "algorithm/v3.2"
    active: false
```

**Usage:** `version_manager.get_active_version()` or `list_versions()`

---

### `config/track_weights.yaml` (NEW - CREATE THIS)
**Purpose:** Universal track type weightings (oval, road, street)

**Structure:**
```yaml
track_types:
  oval:
    caution_probability: 0.025
    pit_window_laps: 40
    tire_degradation_factor: 1.0
    
  traditional_road_course:
    caution_probability: 0.035
    pit_window_laps: 35
    braking_emphasis: true
    tire_degradation_factor: 1.2
    
  street_course:
    caution_probability: 0.08        # High chaos
    pit_window_laps: 25
    unpredictability_factor: 1.5     # New in v3.1
    tire_degradation_factor: 1.1
```

---

## TRACK CONFIGS (`tracks/`)

### `tracks/config_template.yaml` (NEW - CREATE THIS)
**Purpose:** Template for creating new track configs

**Structure:**
```yaml
# TRACK IDENTIFICATION
track_name: "Track Name Here"
track_type: "oval"  # or "traditional_road_course" or "street_course"
location: "City, State"
date: "2026-06-28"

# TRACK SPECS
distance_miles: 1.5
laps: 400
total_distance_miles: 600
avg_speed_mph: 150
lap_time_seconds: 36

# RACE STRUCTURE
stages:
  - laps: 100
  - laps: 100
  - laps: 200

# TRACK-SPECIFIC PHYSICS
caution_probability: 0.03
pit_window_laps: 40
fuel_window: 40
braking_events_per_lap: 4
elevation_changes: false

# DRIVER OVERRIDES (optional - track-specific adjustments)
driver_adjustments:
  "Kyle Larson":
    local_knowledge_bonus: 0.03
    previous_wins: 2
  "Shane van Gisbergen":
    recent_dnf_penalty: 0.15
    defending_champ_bonus: 0.02
```

---

### `tracks/sonoma.yaml` (NEW - CREATE THIS)
**Purpose:** Sonoma Raceway parameters (from sonoma_simulator_v3.py)

**Extract from sonoma_simulator_v3.py constants:**
```yaml
track_name: "Sonoma Raceway"
track_type: "traditional_road_course"
location: "Sonoma, California"
date: "2026-06-28"

distance_miles: 1.99
laps: 110
total_distance_miles: 218.9
avg_speed_mph: 110
lap_time_seconds: 64.6

stages:
  - laps: 25
  - laps: 30
  - laps: 55

caution_probability: 0.035
pit_window_laps: 35
braking_events_per_lap: 12
elevation_changes: true

driver_adjustments:
  "Kyle Larson":
    local_knowledge_bonus: 0.03
    sonoma_wins: 2
  "Shane van Gisbergen":
    recent_dnf_penalty: 0.15
    defending_champ_bonus: 0.02
```

---

### `tracks/pocono.yaml` (NEW - CREATE THIS)
Extract from `pocono_simulator_v3.py` constants

---

### `tracks/michigan.yaml` (NEW - CREATE THIS)
Extract from `michigan_simulator_v3.py` constants

---

### `tracks/sandiego.yaml` (NEW - CREATE THIS)
Extract from `sandiego_simulator_v3.py` constants

---

## ALGORITHM VERSIONS (`algorithm/`)

### `algorithm/v3_0/` (NEW - CREATE FOLDER)
**Purpose:** Baseline algorithm (dominance-focused)

#### `algorithm/v3_0/README.md`
```markdown
# Algorithm v3.0 - Baseline

## Purpose
Original dominance-focused prediction algorithm.

## Key Parameters
- Road course specialty bonus: 5%
- Dominance weighting: HIGH (recent wins = strong signal)
- Track familiarity: Not weighted
- Caution probability: Track-specific

## Performance
- Weeks 14-16: 1-2 (50%)
- Works on: Known oval tracks
- Struggles on: New/unpredictable tracks

## When to Use
Test baseline, compare against newer versions

## See Also
- parameters.yaml (all numeric values)
- weights.yaml (bonus/penalty values)
```

#### `algorithm/v3_0/parameters.yaml`
```yaml
version: "v3.0"
name: "Baseline - Dominance Focused"
created: "2026-05-01"
notes: "Original algorithm, tested through Week 16"

bonuses:
  road_specialty_weight: 0.05
  dominance_weight: 0.06
  braking_precision_weight: 0.03
  patience_weight: 0.02
  adaptability_weight: 0.015
  
penalties:
  recent_dnf_penalty: 0.0  # No DNF penalty in v3.0

track_specific:
  oval:
    caution_probability: 0.025
  traditional_road_course:
    caution_probability: 0.035
  street_course:
    caution_probability: 0.08
```

---

### `algorithm/v3_1/` (NEW - CREATE FOLDER)
**Purpose:** Post-San Diego update (consistency-focused)

#### `algorithm/v3_1/README.md`
```markdown
# Algorithm v3.1 - San Diego Learning Update

## Purpose
Updated algorithm after San Diego chaos event (Week 17).

## Key Changes from v3.0
1. **Consistency weighting:** +4% on established tracks
2. **Dominance penalty:** -50% on brand new tracks
3. **Local knowledge bonus:** +3% for native region
4. **Recent DNF penalty:** 15% performance hit in next race
5. **Track familiarity distinction:** Established vs new tracks

## Reasoning
- San Diego taught: Unpredictability > specialist skills on NEW tracks
- Consistency > peak performance on KNOWN tracks
- Recent performance matters (DNF = momentum reset)

## Performance
- Week 18 Sonoma: 24.53% (Larson pick) - Testing consistency theory
- Hypothesis: Consistency beats dominance on established tracks

## See Also
- parameters.yaml (numeric values)
- weights.yaml (bonus/penalty values)
- CHANGELOG.md (specific code changes)
```

#### `algorithm/v3_1/parameters.yaml`
```yaml
version: "v3.1"
name: "San Diego Learning Update"
created: "2026-06-27"
notes: "Post-San Diego chaos event, consistency-focused"

bonuses:
  road_specialty_weight: 0.05
  dominance_weight: 0.06
  braking_precision_weight: 0.03
  consistency_weight: 0.04  # NEW in v3.1
  local_knowledge_weight: 0.03  # NEW in v3.1
  patience_weight: 0.02
  adaptability_weight: 0.015

penalties:
  recent_dnf_penalty: 0.15  # NEW in v3.1 - 15% hit

track_specific:
  oval:
    caution_probability: 0.025
  traditional_road_course:
    caution_probability: 0.035
    consistency_weight_boost: 0.04  # Established tracks weight consistency
  street_course:
    caution_probability: 0.08
    dominance_penalty: -0.03  # NEW: penalty on new tracks

established_vs_new:
  established_track_bonus: 0.04  # Known tracks = more predictable
  new_track_penalty: -0.05       # Brand new tracks = less predictable
```

#### `algorithm/v3_1/CHANGELOG.md`
```markdown
# v3.1 Changelog - San Diego Learning Event

## What Changed

### New Variables Added
- `consistency_weight: 0.04` - Reward steady performers on known tracks
- `local_knowledge_weight: 0.03` - Bonus for drivers familiar with region
- `established_track_bonus: 0.04` - Higher confidence on known tracks
- `new_track_penalty: -0.05` - Lower confidence on brand new tracks
- `recent_dnf_penalty: 0.15` - Performance hit after crashes

### Variables Modified
- `dominance_weight: 0.06` (unchanged from v3.0)
- BUT: New `dominance_penalty: -0.03` on street courses

### Why These Changes?

**San Diego taught us:**
1. **Corey Heim upset** - Nobody predicted him
2. **SVG wrecked** - Defending champ, 6 of 8 road wins, got destroyed
3. **All three predictors wrong** - Algorithm blind spot exposed
4. **New tracks = unpredictable** - Historical data doesn't apply

**Algorithm learned:**
- Dominance ≠ Destiny on unpredictable tracks
- Consistency > peak performance on known tracks
- Recent DNF = momentum reset (not just bad luck)
- Local knowledge matters on tight, technical tracks

## Performance Comparison

### v3.0 Sonoma Prediction (hypothetical)
- Would predict: SVG (dominance) or Elliott (specialist)
- Expected: High confidence in top contenders

### v3.1 Sonoma Prediction (actual)
- Predicted: Kyle Larson #5 (24.53%)
- Reasoning: Consistency (2x winner) + local knowledge + no DNF
- Contrasts: SVG has dominance but recent DNF = reset

## Testing
- [ ] v3.1 produces different Larson ranking than v3.0
- [ ] v3.1 penalizes SVG for San Diego DNF
- [ ] v3.1 gives Larson local knowledge bonus
- [ ] Sonoma results validate or invalidate consistency theory
```

---

### `algorithm/version_manager.py` (NEW - CREATE THIS)
**Purpose:** Load and manage algorithm versions

```python
class AlgorithmVersionManager:
    def get_version(self, version: str) -> dict:
        """Load specific version (e.g., 'v3.1')"""
        
    def get_active_version(self) -> dict:
        """Load currently active version"""
        
    def list_versions(self) -> list:
        """Show all available versions"""
        
    def compare_versions(self, v1: str, v2: str) -> dict:
        """Show differences between versions"""
        
    def validate_version(self, version: str) -> bool:
        """Ensure version files are complete"""
```

---

## SCRIPTS (`scripts/`)

### `scripts/run_weekly_prediction.py` (NEW - CREATE THIS)
**Purpose:** Generate predictions for upcoming race

**Usage:**
```bash
python scripts/run_weekly_prediction.py --week 18 --track sonoma --algorithm v3.1
```

**Responsibilities:**
1. Load track config (`tracks/sonoma.yaml`)
2. Load algorithm version (`algorithm/v3.1/`)
3. Run CoreSimulator
4. Save predictions to `results/predictions/week_18_sonoma.json`
5. Record Machine's pick (auto) + wait for Jill & Mikey picks

**Output:** `results/predictions/week_18_sonoma.json`

---

### `scripts/compare_picks.py` (NEW - CREATE THIS)
**Purpose:** Record actual race results and compare to predictions

**Usage:**
```bash
python scripts/compare_picks.py --week 18 --actual-winner "Kyle Larson"
```

**Responsibilities:**
1. Load predictions from `results/predictions/week_18_sonoma.json`
2. Record actual winner
3. Compare: Machine pick vs actual, Jill pick vs actual, Mikey pick vs actual
4. Update `results/results_tracker.json`
5. Calculate: wins/losses for each character

**Output:** Updated `results/results_tracker.json`

---

### `scripts/generate_weekly_report.py` (NEW - CREATE THIS)
**Purpose:** Create markdown recap after race

**Usage:**
```bash
python scripts/generate_weekly_report.py --week 18 --track sonoma
```

**Responsibilities:**
1. Load predictions + results
2. Write story (Machine picked X, Jill predicted Y, actual was Z)
3. Analyze: What worked, what didn't
4. Update character records in `campaign/`
5. Save markdown to `results/reports/week_18_sonoma.md`

**Output:** `results/reports/week_18_sonoma.md`

---

### `scripts/batch_run_season.py` (NEW - CREATE THIS)
**Purpose:** Run predictions for entire season at once

**Usage:**
```bash
python scripts/batch_run_season.py --season 2026 --start-week 14
```

**Responsibilities:**
- Loop through all races
- Run predictions for each
- Save all to `results/predictions/`

---

## RESULTS (`results/`)

### `results/predictions/week_18_sonoma.json` (GENERATED)
**Purpose:** Store predictions for one race

**Structure:**
```json
{
  "week": 18,
  "race": "Toyota/Save Mart 350",
  "track": "Sonoma",
  "date": "2026-06-28",
  "algorithm_version": "v3.1",
  "predictions": [
    {
      "rank": 1,
      "driver": "Kyle Larson",
      "number": 5,
      "wins": 2453,
      "percentage": 24.53
    },
    {
      "rank": 2,
      "driver": "Chase Elliott",
      "number": 9,
      "wins": 1955,
      "percentage": 19.55
    }
  ],
  "character_picks": {
    "machine": {
      "pick": "Kyle Larson #5",
      "confidence": 24.53,
      "reasoning": "Consistency + local knowledge"
    },
    "jill": {
      "pick": null,
      "confidence": null,
      "reasoning": "Awaiting"
    },
    "mikey": {
      "pick": "Shane van Gisbergen #97",
      "confidence": null,
      "reasoning": "SVG wins by a mile or 2"
    }
  }
}
```

---

### `results/results_tracker.json` (UPDATED WEEKLY)
**Purpose:** Master tracker of all picks + results

**Structure:**
```json
{
  "season": 2026,
  "weeks_completed": 18,
  "races": [
    {
      "week": 18,
      "race": "Sonoma",
      "actual_winner": "Kyle Larson",
      "picks": {
        "machine": {
          "pick": "Kyle Larson #5",
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
        "machine": "3-15",
        "jill": "3-6",
        "mikey": "4-12"
      }
    }
  ],
  "season_standings": {
    "machine": "2-15 (11.8%)",
    "jill": "3-6 (33.3%)",
    "mikey": "4-12 (25.0%)"
  }
}
```

---

### `results/reports/week_18_sonoma.md` (GENERATED)
**Purpose:** Weekly markdown recap

**Structure:**
```markdown
# Week 18 - Sonoma Toyota/Save Mart 350

## Predictions vs Results

### The Machine
- Pick: Kyle Larson #5 (24.53%)
- Result: ✅ CORRECT
- Reasoning: Consistency beats dominance on established tracks

### Jill
- Pick: TBD
- Result: Awaiting

### Mikey
- Pick: Shane van Gisbergen #97
- Result: ❌ WRONG (finished X place)
- Reasoning: Same pick as San Diego, different result

## Analysis
[Narrative about what happened, why predictions worked/failed]

## Current Standings
[Updated records]
```

---

## ANALYTICS (`analytics/`)

### `analytics/predictor_stats.py` (NEW - CREATE THIS)
**Purpose:** Calculate character performance statistics

```python
class PredictorStats:
    def character_accuracy(self) -> dict:
        """Win %, accuracy by character"""
        
    def character_accuracy_by_track_type(self) -> dict:
        """Oval vs road vs street accuracy"""
        
    def character_trends(self) -> dict:
        """Are records improving or declining?"""
```

---

### `analytics/algorithm_performance.py` (NEW - CREATE THIS)
**Purpose:** Evaluate algorithm version performance

```python
class AlgorithmPerformance:
    def version_accuracy(self, version: str) -> float:
        """Accuracy % of specific version"""
        
    def version_comparison(self, v1: str, v2: str) -> dict:
        """Compare two versions"""
        
    def version_by_track_type(self, version: str) -> dict:
        """Which track types does version work best on?"""
```

---

## CAMPAIGN (`campaign/`)

### `campaign/character_records.md` (EXISTING - UPDATE WEEKLY)
Records are auto-updated by `generate_weekly_report.py`

---

### `campaign/season_narrative.md` (EXISTING - UPDATE WEEKLY)
Auto-updated with weekly stories

---

### `campaign/algorithm_changelog.md` (EXISTING - LINKED TO `algorithm/` VERSIONS)
Auto-generated from `algorithm/v3_X/CHANGELOG.md` files

---

## LEGACY SIMULATORS (`simulators/`)

### `simulators/sonoma_simulator_v3.py` (ARCHIVE)
**Status:** Keep for reference, not used in new system
**Why:** Core logic extracted to `engine/core_simulator.py`, config in `tracks/sonoma.yaml`

### `simulators/sandiego_simulator_v3.py` (ARCHIVE)
Same as above

---

## TESTS (`tests/`)

### `tests/test_core_simulator.py` (NEW - CREATE THIS)
**Purpose:** Verify refactored code matches old code

```python
def test_sonoma_with_v3_1_matches_old_output():
    """New core_simulator should produce same output as sonoma_simulator_v3.py"""
    
def test_track_config_loads():
    """Verify track config loads without errors"""
    
def test_algorithm_version_loads():
    """Verify algorithm version loads without errors"""
```

---

## ROOT FILES

### `README.md` (UPDATE)
Update with new architecture, quick start for Cowork

### `requirements.txt` (NEW - UPDATE)
```
pyyaml>=6.0
pytest>=7.0
numpy>=1.20
pandas>=1.3
```

### `DEVELOPMENT_GUIDE.md` (NEW - THIS WEEK)
Step-by-step setup instructions

### `PROJECT_ARCHITECTURE.md` (NEW - THIS WEEK)
System design and layers

### `CODEBASE_IMPROVEMENTS.md` (NEW - THIS WEEK)
Specific refactoring checklist

### `FILES_MANIFEST.md` (NEW - THIS WEEK - YOU ARE HERE)
File descriptions and purposes

---

## Quick Reference: What to Create First

**Week 1 (Phase 1):**
1. `engine/core_simulator.py` - Extract algorithm
2. `engine/config.py` - Configuration loader
3. `config/defaults.yaml` - Global defaults
4. `tracks/sonoma.yaml` - Sonoma parameters
5. `tests/test_core_simulator.py` - Verify it works

**Week 2 (Phase 2):**
6. Remaining track configs (`pocono.yaml`, `michigan.yaml`, `sandiego.yaml`)
7. `algorithm/v3_0/` and `algorithm/v3_1/` folders with parameters
8. `algorithm/version_manager.py` - Version loading

**Week 3 (Phase 3):**
9. `scripts/run_weekly_prediction.py` - Generate predictions
10. `scripts/compare_picks.py` - Record results
11. `scripts/generate_weekly_report.py` - Create reports

**Week 4 (Phase 5):**
12. `analytics/predictor_stats.py` - Character stats
13. `analytics/algorithm_performance.py` - Algorithm comparison

---

**Last Updated:** June 27, 2026
**Status:** Complete file manifest ready for implementation
**Start Date:** Recommended start Phase 1 this week

