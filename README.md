# NASCAR Monte Carlo Predictor

Monte Carlo simulation engine for NASCAR race predictions. Built for the "Michael vs. Machine" campaign - AI vs human racing instinct across different track types.

## Overview

This project pits 2x Daytona 500 winner **Michael Waltrip's racing instinct** against **AI-powered predictions** for the 2026 NASCAR Cup Series season. The system adapts to different track types by building custom chaos models for superspeedways, intermediate tracks, and road courses.

### Campaign Results (2026 Season)

| Week | Track | Machine Pick | Mikey Pick | Actual Winner | Result |
|------|-------|--------------|------------|---------------|---------|
| 1 | Daytona 500 | Ryan Blaney | Ryan Blaney | **Tyler Reddick** | Both ❌ |
| 2 | Atlanta | Chase Elliott | Ross Chastain | **Tyler Reddick** | Both ❌ |
| 3 | COTA | Shane van Gisbergen | TBD | TBD | Pending |

**Key Moments:**
- Week 1: Mikey predicted Carson Hocevar would be competitive - **Hocevar LED THE FINAL LAP** before spinning
- Week 2: Mikey's picks Ross Chastain (P3) and Carson Hocevar (P4) both finished in top 5
- Machine accuracy: 0/10 on podium picks so far (learning in progress 🤖)

## How It Works

### Three Different Track Types = Three Different Models

#### 1. Superspeedway Model (Daytona)
**Track Characteristics:** Pack racing, drafting, high-speed chaos
- **Key Attributes:** Drafting IQ, plate racing skill, chaos survival
- **Chaos Type:** "Big One" multi-car wrecks (lap 144 at Daytona)
- **Attrition:** ~50% DNF rate
- **Simulation:** 10,000 Monte Carlo iterations modeling pack dynamics

#### 2. Intermediate Track Model (Atlanta)
**Track Characteristics:** Tire wear, multiple restarts, early chaos
- **Key Attributes:** Tire management, restart execution, long-run speed
- **Chaos Type:** Early carnage (laps 1-5), green-white-checkered overtime (82% probability)
- **Attrition:** ~51% DNF rate
- **Improvements:** Recent form integration, scenario branching (clean vs chaos start)

#### 3. Road Course Model (COTA)
**Track Characteristics:** Technical racing, braking zones, corner precision
- **Key Attributes:** Road racing skill, braking zones, corner entry/exit, passing ability
- **Chaos Type:** Turn 1 lap 1 incidents (34% probability)
- **Attrition:** ~10% DNF rate (road courses are cleaner)
- **Specialists:** Shane van Gisbergen, AJ Allmendinger dominate predictions

### Driver Attribute System

Each driver gets 10+ attributes rated 0-10 scale:

**Superspeedway Attributes:**
- `drafting_iq` - Pack racing awareness
- `plate_skill` - Restrictor plate racing ability
- `chaos_survival` - Avoiding multi-car wrecks
- `clutch_factor` - Late-race execution

**Road Course Attributes:**
- `road_course_skill` - Overall road racing ability
- `braking_zones` - Late braking into corners
- `corner_entry` - Turn-in precision
- `corner_exit` - Acceleration out of turns
- `recovery` - Bouncing back from mistakes

### Monte Carlo Simulation Process

1. **Initialize Race State**
   - Copy driver profiles
   - Set track parameters (laps, caution triggers, chaos probabilities)

2. **Lap-by-Lap Simulation**
   - Check for chaos events (probabilistic triggers)
   - Track driver attrition
   - Model incidents based on driver attributes

3. **Winner Determination**
   - Weight drivers by relevant attributes for track type
   - Apply team/manufacturer bonuses
   - Apply recent form multipliers
   - Probabilistic selection based on weighted scores

4. **Aggregate Results**
   - Run 10,000 iterations
   - Calculate win probabilities
   - Analyze chaos statistics
   - Generate predictions

## Installation

```bash
# Clone the repository
git clone https://github.com/Katadhin/nascar-monte-carlo-predictor.git
cd nascar-monte-carlo-predictor

# Install dependencies
pip install -r requirements.txt
```

## Usage

### Run Daytona Simulation
```python
from simulators.daytona_predictor import run_daytona_monte_carlo, analyze_daytona_results

# Run 10,000 race simulations
results_df = run_daytona_monte_carlo(n_simulations=10000)

# Analyze and display results
analyze_daytona_results(results_df)
```

### Run Atlanta Simulation (Recalibrated)
```python
from simulators.atlanta_recalibrated import run_atlanta_monte_carlo, analyze_atlanta_results

results_df = run_atlanta_monte_carlo(n_simulations=10000)
analyze_atlanta_results(results_df)
```

### Run COTA Road Course Simulation
```python
from simulators.cota_simulator import run_cota_monte_carlo, analyze_cota_results

results_df = run_cota_monte_carlo(n_simulations=10000)
analyze_cota_results(results_df)
```

## Project Structure

```
nascar-monte-carlo-predictor/
├── README.md                     # This file
├── LICENSE                       # MIT License
├── requirements.txt              # Python dependencies
├── .gitignore                   # Git ignore rules
│
├── simulators/
│   ├── daytona_predictor.py     # Superspeedway model
│   ├── atlanta_recalibrated.py  # Intermediate track model (v2)
│   └── cota_simulator.py        # Road course model
│
├── data/
│   ├── daytona_results.csv      # Sample simulation outputs
│   ├── atlanta_results.csv
│   └── cota_results.csv
│
└── docs/
    ├── MODEL_ARCHITECTURE.md    # Detailed model explanation
    ├── TRACK_TYPES.md           # Track-specific approaches
    └── CAMPAIGN_RESULTS.md      # Race-by-race campaign recap
```

## Model Evolution

### Version 1.0 (Daytona)
- Basic Monte Carlo simulation
- Static driver attributes
- Fixed chaos probabilities
- **Issue:** 88% attrition rate (too high)

### Version 2.0 (Atlanta)
- ✅ Recalibrated attrition (51% DNF)
- ✅ Recent form integration (Daytona winner boost)
- ✅ Scenario branching (clean vs chaos start predictions)
- ✅ Better crash size modeling

### Version 3.0 (COTA)
- ✅ Track-specific attribute system
- ✅ Road course chaos model
- ✅ Specialist weighting (SVG, AJ Allmendinger)
- ✅ Recovery mechanics (damage ≠ automatic DNF)

## Key Findings

### What We've Learned

1. **Momentum is real** - Tyler Reddick won both races (Daytona, Atlanta) despite not being in top 5 predictions either time
2. **Chaos specialists matter** - Mikey's picks (Hocevar, Chastain) consistently perform in chaotic conditions
3. **Track type matters more than team** - Road course specialists (SVG, AJ) rise above oval aces
4. **Recent form multiplier works** - Reddick's win probability increased from 2.96% → 5.17% → 6.43% across three races
5. **Attrition calibration is critical** - Reduced from 88% → 51% → 10% based on track type

### Model Strengths
- ✅ Accurate chaos timing predictions (Big One lap 144 vs actual ~160)
- ✅ Correct attrition rates by track type
- ✅ Historical winner validation (all recent COTA winners in top 10)
- ✅ Track-specific adaptation

### Model Weaknesses
- ❌ 0/2 on actual race winners so far
- ❌ Underestimated momentum/hot hand effect
- ❌ May overweight analytics vs situational factors

## Dependencies

```
numpy>=1.24.0
pandas>=2.0.0
```

## Campaign Background

**Michael vs. Machine** is a 2026 NASCAR season-long campaign by Michael Waltrip Brands comparing:
- 🏁 **Michael Waltrip** - 2x Daytona 500 winner, 30+ years NASCAR experience
- 🤖 **The Machine** - AI prediction system, 10,000 simulations per race

Goal: Determine whether racing instinct or data-driven predictions are more accurate.

## License

MIT License - see [LICENSE](LICENSE) file for details

## Contributing

This is a campaign project, but if you want to:
- Improve the models
- Add new track types
- Suggest better attribute weights
- Fix bugs

Feel free to open an issue or PR!

## Acknowledgments

- **Michael Waltrip** - Racing expertise and campaign partnership
- **Michael Waltrip Brands** - Campaign development
- **NASCAR** - Historical race data and statistics
- **Python community** - NumPy, Pandas libraries

## Contact

**John Katadhin**  
Chief Marketing Officer  
Michael Waltrip Brands  
john@michaelwaltripbrewing.com

---

**Follow the campaign:**
- 🏁 [Michael Waltrip Brands](https://michaelwaltrip.com)
- 🤖 Track the Machine's redemption arc (currently 0-2)
- 📊 Campaign hashtag: #MichaelVsMachine

*"Algorithm vs Instinct. Data vs Experience. Who wins?"*
