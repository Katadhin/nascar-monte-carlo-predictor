# Quick Start Guide - Get Rolling in 5 Minutes

## TL;DR - Read This First

You have **4 comprehensive guides** to improve your codebase:

1. **DEVELOPMENT_GUIDE.md** - 4-week roadmap with phases
2. **PROJECT_ARCHITECTURE.md** - System design and layers  
3. **CODEBASE_IMPROVEMENTS.md** - Specific refactoring checklist
4. **FILES_MANIFEST.md** - Every file you need to create

**Start here:** Read this quick start, then pick a guide based on what you need.

---

## The Problem You're Solving

Current codebase:
- ❌ 5+ individual simulator scripts (hard to maintain)
- ❌ Hardcoded parameters (can't easily tweak)
- ❌ No results tracking (manual copy-paste)
- ❌ Algorithm changes scattered (hard to track)

Target state:
- ✅ One reusable engine + YAML configs
- ✅ Change parameters without touching code
- ✅ Automated prediction → results → reporting
- ✅ Clear algorithm version history

**Time estimate:** 4 weeks to fully refactor (13-18 hours)

---

## 5-Minute Setup in Cowork

### Step 1: Clone Repo (2 minutes)
```bash
cd ~/Cowork  # Your Cowork workspace
git clone https://github.com/Katadhin/nascar-monte-carlo-predictor.git nascar-predictor
cd nascar-predictor
```

### Step 2: Install Dependencies (1 minute)
```bash
pip install -r requirements.txt  # (currently minimal)
pip install pyyaml pytest numpy pandas
```

### Step 3: Read Your Guides (2 minutes)
You now have these files in `/home/claude/`:
- `DEVELOPMENT_GUIDE.md` - Weekly phases
- `PROJECT_ARCHITECTURE.md` - System design
- `CODEBASE_IMPROVEMENTS.md` - Refactoring checklist
- `FILES_MANIFEST.md` - What each file does

**Copy them to your repo:**
```bash
cp /home/claude/DEVELOPMENT_GUIDE.md nascar-predictor/
cp /home/claude/PROJECT_ARCHITECTURE.md nascar-predictor/
cp /home/claude/CODEBASE_IMPROVEMENTS.md nascar-predictor/
cp /home/claude/FILES_MANIFEST.md nascar-predictor/
git add *.md && git commit -m "Add development guides"
```

### Done! Ready to Start
Everything is set up. Time to start coding.

---

## Which Guide to Read?

### "I want to see what needs to be built"
→ Read **FILES_MANIFEST.md**
- Every file you need to create
- What it does
- Where it goes

### "I want a roadmap and timeline"
→ Read **DEVELOPMENT_GUIDE.md**
- 4-week phase-by-phase breakdown
- What to do each week
- Success metrics

### "I want to understand the architecture"
→ Read **PROJECT_ARCHITECTURE.md**
- System layers and design
- Data flow diagrams
- Class relationships

### "I want specific things to change"
→ Read **CODEBASE_IMPROVEMENTS.md**
- Specific problems + solutions
- Code examples (bad vs good)
- Dependency updates needed

---

## Phase 1: Start Here (This Week)

**Goal:** Build the core engine (one reusable simulator)

### Task 1.1: Create Core Simulator (2-3 hours)
```bash
touch engine/core_simulator.py
```

**What to do:**
1. Open `sonoma_simulator_v3.py`
2. Copy the algorithm logic (Monte Carlo loop, driver data, performance calculation)
3. Remove hardcoded values (SONOMA_AVERAGE_SPEED, etc.)
4. Create `CoreSimulator` class with `__init__(config, algorithm_params)` and `run_simulation()`
5. Test: Load parameters, run sim, get results

**Reference:** See `FILES_MANIFEST.md` → `engine/core_simulator.py` for interface

### Task 1.2: Create Config Loader (1 hour)
```bash
touch engine/config.py
```

**What to do:**
1. Create `ConfigLoader` class
2. Implement `load_track_config(track_name)` - loads YAML
3. Implement `load_algorithm_version(version)` - loads YAML
4. Test: Load `tracks/sonoma.yaml` (which you'll create)

**Reference:** See `FILES_MANIFEST.md` → `engine/config.py`

### Task 1.3: Create Track Config (30 minutes)
```bash
mkdir -p tracks
touch tracks/sonoma.yaml
```

**What to do:**
1. Copy constants from `sonoma_simulator_v3.py`
2. Create YAML structure with all parameters
3. No Python values—just YAML config

**Example:**
```yaml
track_name: "Sonoma Raceway"
distance_miles: 1.99
avg_speed_mph: 110
# ... etc (see FILES_MANIFEST.md for full list)
```

### Task 1.4: Test & Verify (1 hour)
```bash
python -c "
from engine.config import ConfigLoader
from engine.core_simulator import CoreSimulator

config = ConfigLoader().load_track_config('sonoma')
algo = ConfigLoader().load_algorithm_version('v3.1')
sim = CoreSimulator(config, algo)
results = sim.run_simulation(10000)
print(results)
"
```

**Success criteria:**
- ✅ Core simulator runs without errors
- ✅ Output matches old `sonoma_simulator_v3.py` (within 1%)
- ✅ Parameters loaded from YAML, not hardcoded

---

## Typical Weekly Workflow (After Refactor)

### Before Race (Wednesday)
```bash
# 1. Run prediction
python scripts/run_weekly_prediction.py --week 19 --track "michigan"

# Output: results/predictions/week_19_michigan.json
# Shows Machine's pick + waits for Jill & Mikey picks

# 2. Share predictions with team
cat results/predictions/week_19_michigan.json
```

### After Race (Sunday)
```bash
# 1. Record actual winner
python scripts/compare_picks.py --week 19 --actual-winner "Kyle Larson"

# 2. Generate report
python scripts/generate_weekly_report.py --week 19 --track michigan

# Output: results/reports/week_19_michigan.md
# Shows: predictions vs results, character records updated

# 3. Check standings
python analytics/predictor_stats.py
# Output: Current standings, trends, performance by track type
```

---

## File Structure After Phase 1

```
nascar-predictor/
├── engine/
│   ├── __init__.py
│   ├── core_simulator.py      ✅ NEW
│   ├── config.py               ✅ NEW
│   └── utils.py                (optional, Phase 2)
│
├── tracks/
│   ├── sonoma.yaml             ✅ NEW
│   └── config_template.yaml    (optional, Phase 2)
│
├── config/
│   ├── defaults.yaml           ✅ NEW
│   └── algorithm_versions.yaml (Phase 2)
│
├── algorithm/
│   ├── v3_1/                   (Phase 2)
│   └── version_manager.py      (Phase 2)
│
├── scripts/                    (Phase 3)
├── results/                    (auto-generated)
├── analytics/                  (Phase 5)
├── tests/
│   └── test_core_simulator.py  ✅ NEW
│
├── DEVELOPMENT_GUIDE.md        ✅ NEW
├── PROJECT_ARCHITECTURE.md     ✅ NEW
├── CODEBASE_IMPROVEMENTS.md    ✅ NEW
├── FILES_MANIFEST.md           ✅ NEW
└── README.md                   (update)
```

---

## Key Principles (Remember These)

### 1. Configuration Over Code
- **Parameters in YAML, not Python**
- Change `tracks/sonoma.yaml` → changes behavior
- No code edits needed

### 2. One Engine, Many Tracks
- Core simulator works for ALL tracks
- Track-specific logic comes from YAML
- Add new track = add YAML file (5 minutes)

### 3. Automated Workflows
- One command = prediction
- One command = results recording
- One command = report generation
- No manual copy-paste

### 4. Versioned Algorithms
- v3.0 in `algorithm/v3_0/`
- v3.1 in `algorithm/v3_1/`
- Easy to compare, revert, test

---

## Success Metrics for Phase 1

When Phase 1 is complete, you should:

✅ Have `engine/core_simulator.py` (reusable)
✅ Have `engine/config.py` (YAML loader)
✅ Have `tracks/sonoma.yaml` (parameters)
✅ Have passing test that verifies output
✅ Understand how configuration works
✅ Be ready to refactor other tracks

---

## Common Questions

### "Should I throw away the old simulators?"
No! Keep them in `simulators/` folder as reference/archive. Extract logic into core, then they become obsolete.

### "How do I know my refactored code is correct?"
Write tests! Compare output of new `CoreSimulator` with old `sonoma_simulator_v3.py`. They should match within 1% (randomness).

### "Can I do all 5 phases at once?"
Not recommended. Each phase builds on previous. Do Phase 1, test it, then move to Phase 2.

### "When should I start automation scripts?"
After Phase 2 (algorithm versioning). Phase 3 scripts depend on both core engine + algorithm versions.

---

## Next Steps

1. **Copy guides to repo:**
   ```bash
   cp DEVELOPMENT_GUIDE.md PROJECT_ARCHITECTURE.md CODEBASE_IMPROVEMENTS.md FILES_MANIFEST.md nascar-predictor/
   ```

2. **Read FILES_MANIFEST.md** (30 minutes)
   - Understand what you're building

3. **Start Phase 1, Task 1.1** (2-3 hours)
   - Create `engine/core_simulator.py`

4. **Test & iterate** (1-2 hours)
   - Verify output matches old code

5. **Move to Task 1.2** (1 hour)
   - Create config loader

**By end of this week:** Phase 1 complete ✅

---

## Time Breakdown

| Task | Hours | Status |
|------|-------|--------|
| Phase 1 (Core engine) | 3-4 | Start this week |
| Phase 2 (Configs) | 2-3 | Next week |
| Phase 3 (Scripts) | 3-4 | Week 3 |
| Phase 4 (Testing) | 2-3 | Week 3 (parallel) |
| Phase 5 (Analytics) | 3-4 | Week 4 |
| **TOTAL** | **13-18** | **4 weeks recommended** |

---

## You've Got This! 🚀

- ✅ You have 4 comprehensive guides
- ✅ Clear phase-by-phase roadmap
- ✅ Every file you need to create is documented
- ✅ Sample code and examples provided
- ✅ Success criteria defined

**Start with Phase 1, Task 1.1 today.**

Questions? Reference the appropriate guide:
- "What file?" → FILES_MANIFEST.md
- "What order?" → DEVELOPMENT_GUIDE.md
- "How does it fit together?" → PROJECT_ARCHITECTURE.md
- "What should I change?" → CODEBASE_IMPROVEMENTS.md

---

**Last Updated:** June 27, 2026
**Status:** Ready to begin Phase 1
**Estimated Start:** Today
**Estimated Completion:** 4 weeks
