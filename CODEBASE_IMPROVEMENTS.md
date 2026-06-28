# Codebase Improvements - Specific Refactoring Tasks

## Problem: Current Codebase Limitations

### 1. Duplicated Simulator Code
**Problem:**
- `sandiego_simulator_v3.py` (street course)
- `sonoma_simulator_v3.py` (road course)
- `pocono_simulator_v3.py` (road oval)
- `michigan_simulator_v3.py` (oval)
- Each has ~250-300 lines of similar code

**Cost:**
- Bug fix? Update 5 files
- Algorithm change? Update 5 files
- New track? Write from scratch (another 250 lines)

**Solution:** One core engine, track-specific configs

---

### 2. Hardcoded Parameters
**Problem:**
Current code:
```python
POCONO_AVERAGE_SPEED = 140
POCONO_LAP_TIME = 51.0
POCONO_LAPS = 160
POCONO_FUEL_WINDOW = 40
POCONO_CAUTION_PROBABILITY = 0.045
```

To change a parameter, you must:
1. Open Python file
2. Edit the constant
3. Save file
4. Re-run script
5. Can't easily compare old vs new

**Solution:** YAML config files

```yaml
# tracks/pocono.yaml
average_speed_mph: 140
lap_time_seconds: 51.0
total_laps: 160
fuel_window: 40
caution_probability: 0.045
```

---

### 3. No Results Tracking
**Problem:**
- Predictions are printed to console
- Copy-paste into JSON manually
- Results recorded in spreadsheet
- No automated comparison

**Solution:** Automated pipeline

```bash
# One command does all:
python scripts/run_weekly_prediction.py --week 18 --track sonoma
# → Saves predictions/week_18_sonoma.json
# → Logs to results tracker
# → Ready for post-race comparison
```

---

### 4. Algorithm Changes Not Documented
**Problem:**
- v3.0 vs v3.1 parameters scattered in code
- San Diego learning event not clearly tracked
- Can't easily compare "what changed" between versions
- Future versions will be even harder to manage

**Solution:** Versioned algorithm folders

```
algorithm/
├── v3_0/
│   ├── parameters.yaml
│   ├── README.md (explains v3.0 logic)
│   └── weights.yaml
└── v3_1/
    ├── parameters.yaml
    ├── README.md (San Diego changes documented)
    ├── weights.yaml
    └── CHANGELOG.md (specific code changes)
```

---

### 5. Manual Testing
**Problem:**
- No automated tests
- Changes might break old tracks
- Can't verify refactored code matches original
- Scary to make improvements

**Solution:** Test suite

```python
# tests/test_core_simulator.py
def test_sonoma_with_v3_1_matches_old_output():
    """Verify refactored core_simulator produces same results as original"""
    # Load old sonoma_simulator_v3.py output
    # Load new core_simulator with v3.1 config
    # Compare results
    # Assert differences < 1%
```

---

### 6. No Performance Analytics
**Problem:**
- Manually calculate: Jill is 3-6, Machine is 2-15, Mikey is 4-12
- No automated trends
- Can't easily answer: "Which algorithm version works best?"
- No "accuracy by track type" analysis

**Solution:** Analytics module

```python
# analytics/predictor_stats.py
stats = PredictorStats()
print(stats.character_accuracy())     # Win % by character
print(stats.algorithm_comparison())   # v3.0 vs v3.1 accuracy
print(stats.track_type_performance()) # Oval vs road vs street
print(stats.trend_analysis())         # Are we improving?
```

---

## Refactoring Checklist

### Phase 1: Core Engine (3-4 hours)

**1.1 Create Base Core Simulator**
- [ ] Create `engine/core_simulator.py`
- [ ] Extract pure algorithm from `sonoma_simulator_v3.py`
- [ ] Remove hardcoded values (leave placeholders)
- [ ] Create `__init__(self, config: dict)` method
- [ ] Create `run_simulation(self, num_simulations)` method
- [ ] Create `export_results()` method

**1.2 Build Configuration System**
- [ ] Create `config/` directory
- [ ] Create `tracks/config_template.yaml`
- [ ] Create `ConfigLoader` class in `engine/config.py`
- [ ] Test: Load YAML, apply to simulator

**1.3 Test & Verify**
- [ ] Run core simulator with Sonoma config
- [ ] Compare output vs original `sonoma_simulator_v3.py`
- [ ] Output should match within 1% (randomness)

**Deliverable:** `engine/core_simulator.py` + `tracks/sonoma.yaml` producing identical results to old code

---

### Phase 2: Configuration Migration (2-3 hours)

**2.1 Create Track Configs**
- [ ] Create `tracks/pocono.yaml` (from pocono_simulator_v3.py constants)
- [ ] Create `tracks/michigan.yaml` (from michigan_simulator_v3.py constants)
- [ ] Create `tracks/sandiego.yaml` (from sandiego_simulator_v3.py constants)
- [ ] Each YAML should have ALL parameters (no hardcoded values)

**2.2 Create Algorithm Version Files**
- [ ] Create `algorithm/v3_0/parameters.yaml` (baseline)
- [ ] Create `algorithm/v3_1/parameters.yaml` (post-San Diego)
- [ ] Document differences in `algorithm/v3_1/CHANGELOG.md`

**2.3 Build AlgorithmVersionManager**
- [ ] Create `algorithm/version_manager.py`
- [ ] Implement `get_version(version_name)` 
- [ ] Implement `compare_versions(v1, v2)`
- [ ] Test: Load v3.0 vs v3.1, see what changed

**Deliverable:** All hardcoded values moved to YAML files, version manager working

---

### Phase 3: Automation Scripts (3-4 hours)

**3.1 Weekly Prediction Script**
- [ ] Create `scripts/run_weekly_prediction.py`
- [ ] Arguments: `--week`, `--track`, `--algorithm-version`
- [ ] Loads config + algorithm version
- [ ] Runs core simulator
- [ ] Saves to `results/predictions/week_XX_TRACK.json`
- [ ] Accepts character picks (Machine auto, Jill TBD, Mikey TBD)

**3.2 Results Comparison Script**
- [ ] Create `scripts/compare_picks.py`
- [ ] Arguments: `--week`, `--actual-winner`
- [ ] Loads predictions JSON
- [ ] Records actual winner
- [ ] Updates `results/results_tracker.json`
- [ ] Calculates: who was right/wrong

**3.3 Report Generation Script**
- [ ] Create `scripts/generate_weekly_report.py`
- [ ] Reads predictions + results
- [ ] Generates markdown recap (like San Diego chaos post)
- [ ] Saves to `results/reports/week_XX_TRACK.md`
- [ ] Auto-updates character records

**Deliverable:** Full automation pipeline working (predict → record → report)

---

### Phase 4: Testing Framework (2-3 hours)

**4.1 Unit Tests**
- [ ] Create `tests/test_core_simulator.py`
- [ ] Test: Core simulator with Sonoma config matches old output (within 1%)
- [ ] Test: Core simulator with Pocono config matches old output
- [ ] Test: Track parameters load correctly from YAML

**4.2 Integration Tests**
- [ ] Test: Full pipeline (prediction → results → report)
- [ ] Test: Config loader applies all parameters correctly
- [ ] Test: Algorithm version manager loads all versions

**4.3 Regression Tests**
- [ ] Archive old simulator outputs (expected results)
- [ ] Run tests against new code
- [ ] Ensure refactored code produces same results

**Deliverable:** Test suite where `pytest tests/` passes

---

### Phase 5: Analytics Module (3-4 hours)

**5.1 Character Performance Analytics**
- [ ] Create `analytics/predictor_stats.py`
- [ ] Implement `character_accuracy()` - Win %, trends
- [ ] Implement `character_performance_by_track_type()` - Oval vs road vs street
- [ ] Generate stats for Jill, Machine, Mikey

**5.2 Algorithm Performance Analytics**
- [ ] Create `analytics/algorithm_performance.py`
- [ ] Implement `algorithm_accuracy_by_version()` - v3.0 vs v3.1
- [ ] Implement `algorithm_accuracy_by_track_type()` - Which version works best where
- [ ] Show: v3.1 improvements over v3.0

**5.3 Weekly Reports**
- [ ] Auto-generate `analytics/weekly_summary.json`
- [ ] Predictions accuracy % that week
- [ ] Character standings
- [ ] Algorithm version performance
- [ ] Trending direction

**Deliverable:** Analytics dashboard showing performance trends

---

## Specific Code Changes

### Change 1: Extract Hardcoded Driver Data
**Current (bad):**
```python
DRIVERS = {
    "Shane van Gisbergen": (136, 0.98, 0.97, 0.96, 0.97),
    "Kyle Larson": (138, 0.94, 0.95, 0.94, 0.93),
    # ... 15 more drivers
}
```

**New (good):**
```yaml
# config/drivers.yaml
drivers:
  "Shane van Gisbergen":
    base_speed: 136
    road_specialty: 0.98
    braking_precision: 0.97
    elevation_management: 0.96
    adaptability: 0.97
```

**Benefit:** Change driver ratings without editing Python

---

### Change 2: Parameterize Algorithm Weights
**Current (bad):**
```python
road_bonus = 1.0 + (road_specialty * 0.05)
braking_bonus = 1.0 + (braking * 0.03)
```

**New (good):**
```yaml
# algorithm/v3_1/weights.yaml
bonuses:
  road_specialty_weight: 0.05
  braking_weight: 0.03
  consistency_weight: 0.04  # New in v3.1
```

**Python:**
```python
road_bonus = 1.0 + (road_specialty * self.config['bonuses']['road_specialty_weight'])
```

**Benefit:** Tune algorithm without rewriting code

---

### Change 3: Modularize Monte Carlo Loop
**Current (bad):**
```python
for sim in range(num_simulations):
    # 100 lines of simulation logic in loop
```

**New (good):**
```python
def run_simulation(self, num_simulations):
    for sim in range(num_simulations):
        result = self._simulate_one_race()
        self.results.append(result)
    return self.results

def _simulate_one_race(self):
    """One race simulation (lap-by-lap)"""
    # Extract to separate method
```

**Benefit:** Easier to test, understand, modify

---

### Change 4: Configuration Loading
**Current (bad):**
```python
# Hard to change tracks
if track == "sonoma":
    LAP_TIME = 64.6
    AVERAGE_SPEED = 110
elif track == "pocono":
    LAP_TIME = 51.0
    AVERAGE_SPEED = 140
```

**New (good):**
```python
class ConfigLoader:
    def load_track_config(self, track_name):
        yaml_file = f'tracks/{track_name}.yaml'
        return yaml.safe_load(open(yaml_file))
    
    def load_algorithm_version(self, version):
        yaml_file = f'algorithm/{version}/parameters.yaml'
        return yaml.safe_load(open(yaml_file))
```

**Benefit:** Add new tracks instantly (no code changes)

---

## Dependency Changes

### Current Requirements
```
# Current requirements.txt
# (probably empty or minimal)
```

### New Requirements
```
# New requirements.txt
pyyaml>=6.0          # For config files
pytest>=7.0          # For testing
numpy>=1.20          # For statistics
pandas>=1.3          # For analytics
matplotlib>=3.3      # Optional: for charts
```

---

## Timeline Estimate

| Phase | Tasks | Hours | Status |
|-------|-------|-------|--------|
| 1 | Core engine + config system | 3-4 | Ready to start |
| 2 | Config migration | 2-3 | After Phase 1 |
| 3 | Automation scripts | 3-4 | After Phase 2 |
| 4 | Testing framework | 2-3 | Parallel with Phase 3 |
| 5 | Analytics module | 3-4 | After Phase 3 |
| **TOTAL** | **Full refactor** | **13-18 hours** | **4 weeks recommended** |

---

## Success Metrics

After refactoring, you should be able to:

✅ Add a new track in 5 minutes (just create YAML file)
✅ Change algorithm weights without touching Python
✅ Run weekly predictions with one command
✅ Auto-generate weekly reports
✅ Compare algorithm versions with one command
✅ Run full test suite with `pytest`
✅ See performance analytics instantly
✅ Track all changes in version history

---

## Quick Start

1. Read `DEVELOPMENT_GUIDE.md` (this week's roadmap)
2. Read `PROJECT_ARCHITECTURE.md` (system design)
3. Start Phase 1: Build core engine
4. Test: Make sure refactored code matches old code
5. Move forward incrementally

Don't try to do all 5 phases at once. Each phase builds on the previous.

---

**Last Updated:** June 27, 2026
**Status:** Ready for implementation
**Recommend Starting:** Phase 1 (Core Engine)
