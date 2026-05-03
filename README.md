# 🏁 NASCAR Monte Carlo Predictor
## Michael vs Machine - 2026 Season Battle

[![Python](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![NumPy](https://img.shields.io/badge/numpy-1.24+-orange.svg)](https://numpy.org/)
[![Pandas](https://img.shields.io/badge/pandas-2.0+-red.svg)](https://pandas.pydata.org/)
[![Campaign Status](https://img.shields.io/badge/campaign-active-brightgreen.svg)](https://github.com/Katadhin/nascar-monte-carlo-predictor)

[![Machine Record](https://img.shields.io/badge/🤖%20machine-0--10%20(0%25)-red.svg)](https://github.com/Katadhin/nascar-monte-carlo-predictor)
[![Mikey Record](https://img.shields.io/badge/🏆%20mikey-2.5--8%20(27%25)-yellow.svg)](https://github.com/Katadhin/nascar-monte-carlo-predictor)
[![Jill Record](https://img.shields.io/badge/⭐%20jill-1--2%20(33%25)-green.svg)](https://github.com/Katadhin/nascar-monte-carlo-predictor)

[![Model Version](https://img.shields.io/badge/model-v3.0-purple.svg)](https://github.com/Katadhin/nascar-monte-carlo-predictor)
[![Current Week](https://img.shields.io/badge/week%2011-Texas-orange.svg)](https://github.com/Katadhin/nascar-monte-carlo-predictor)
[![Next Race](https://img.shields.io/badge/next%20race-May%203-blue.svg)](https://github.com/Katadhin/nascar-monte-carlo-predictor)
[![Simulations](https://img.shields.io/badge/simulations-10%2C000%2Frace-blueviolet.svg)](https://github.com/Katadhin/nascar-monte-carlo-predictor)
[![Learning in Public](https://img.shields.io/badge/learning-in%20public-success.svg)](https://github.com/Katadhin/nascar-monte-carlo-predictor)

> 🎲 A Monte Carlo simulation engine predicting NASCAR Cup Series winners, competing head-to-head against 2x Daytona 500 champion Michael Waltrip and MWB Communications Manager Jill.

**Current Status: The Machine is 0-10 (winless) 🤖💀**

📖 **Read the full story:** [Can Racing Instinct Beat Algorithms? We're Testing It Every Week](https://medium.com/@katadhin/can-racing-instinct-beat-algorithms-were-testing-it-every-week-6cfb2217ae73)

---

## 📊 Season Standings (Through Week 10 - Talladega)

| Predictor | Record | Win % | Method | Status |
|-----------|--------|-------|--------|--------|
| ⭐ **Jill** | 1-2 | **33%** 🥇 | Staff meeting vibes | Best record |
| 🏆 **Mikey** | 2.5-8 | 27% | 30+ years experience | 2x Daytona 500 champion |
| 🤖 **Machine** | 0-10 | **0%** 💀 | 10,000 Monte Carlo simulations | Seeking first win |

### 📈 Win Percentage Visualization

```
Jill:    ████████░░ 33% ⭐ LEADING
Mikey:   ███████░░░ 27%
Machine: ░░░░░░░░░░  0% 💀 WINLESS
```

---

## 🏁 Race-by-Race Results

| Week | 🏟️ Track | 🏆 Winner | 🤖 Machine | 🏁 Mikey | ⭐ Jill | Result |
|------|----------|-----------|------------|----------|---------|--------|
| 1 | Daytona 500 | Tyler Reddick | Ryan Blaney ❌ | Ryan Blaney ❌ | - | Both wrong |
| 2 | Atlanta | Tyler Reddick | Chase Elliott ❌ | Ross Chastain ❌ | - | Both wrong |
| 3 | COTA | Tyler Reddick | van Gisbergen ❌ | **Tyler Reddick ✅** | - | Mikey wins! |
| 4 | Phoenix | Ryan Blaney | Reddick/Byron ❌ | Tyler Reddick ❌ | - | Dual model fail |
| 5 | Vegas | Denny Hamlin | Byron (3rd) ❌ | **Hamlin HM ✅** | - | Mikey 0.5 |
| 6 | Darlington | Tyler Reddick | Hamlin (11th) ❌ | **Tyler Reddick ✅** | - | Mikey wins! |
| 7 | Martinsville | Chase Elliott | Hamlin (2nd) ❌ | Byron (5th) ❌ | - | Both had Elliott 5th |
| 8 | Bristol | **Ty Gibbs** | Elliott (spun) ❌ | Hamlin (9th) ❌ | **Ty Gibbs ✅** | **JILL WINS!** 🎉 |
| 9 | Kansas | Tyler Reddick | Larson (2nd) ❌ | Byron (7th) ❌ | Bell (wrecked) ❌ | Reddick again |
| 10 | Talladega | Carson Hocevar | Logano (Big One) ❌ | TBD | Briscoe (Big One) ❌ | Chaos wins |

### 🎯 Win Breakdown

- 🤖 **Machine Wins:** 0 💀
- 🏆 **Mikey Wins:** 2 full + 0.5 HM = 2.5 ✅
- ⭐ **Jill Wins:** 1 ✅

---

## 🔄 Model Evolution Journey

### v1.0 - Weeks 1-3 (FAILED) ❌
```
Confidence: 18%+
Philosophy: Pick favorites with high certainty
Result: 0-3, too overconfident
Lesson: NASCAR is too chaotic for certainty
```

### v2.0 - Week 4 Phoenix (FAILED) ❌
```
Change: Hot-hand formula (2.0x streak multiplier)
Pick: Tyler Reddick (continuing streak)
Result: Ryan Blaney won, streak ended
Lesson: Streaks regress to mean
```

### v2.5 - Weeks 4-5 (FAILED) ❌
```
Change: Pressure penalties, regression to mean
Confidence: Flattened to ~15%
Result: Still 0-2
Lesson: Better philosophy, wrong picks
```

### v3.0 - Weeks 6-Present (0-6, BUT LEARNING) 📚
```
Changes:
✓ Track-type specific data
✓ Flattened certainty (18.6% → 7.27%)
✓ Chaos variance (±10% standard, ±40% Talladega)
✓ Reduced boosts (no runaway favorites)
✓ Specialist recognition
✓ Qualifying integration (10% weight)

Progress:
✓ Had Elliott 5th at Martinsville (he won)
✓ Picked Larson at Kansas (finished 2nd - closest yet)
✓ Talladega: Predicted chaos, got chaos
```

### 📉 Confidence Reduction Over Time

```
Darlington:   ████████████████ 15.75%
Martinsville: ███████████░░░░░ 10.76%
Bristol:      █████████░░░░░░░  9.39%
Kansas:       █████████░░░░░░░  8.74%
Talladega:    ███████░░░░░░░░░  7.27% ← Humility achieved
Texas:        █████████░░░░░░░  8.97%
```

**Translation:** The model is learning to be less certain = more honest.

---

## 🎬 Key Campaign Moments

### 💬 "AI Can Kiss My Butt" - Vegas Week 5
Michael's pre-race quote before picking Blaney (who finished 16th). Hamlin won. Comedy gold. 😂

### 🔄 "The Qualifying Switch" - Darlington Week 6
- **Thursday:** Presumed Hamlin pick
- **Friday:** Watched qualifying, switched to Reddick
- **Machine:** Mocked "recency bias"
- **Result:** Reddick WON ✅, Machine's Hamlin finished 11th ❌
- **Lesson:** Context > Data

### 🎯 "Both Had Elliott 5th" - Martinsville Week 7
Neither Mikey nor Machine picked Elliott #1. Both had him 5th. He won on pit strategy (short-pitted lap 261). Hamlin led 292 laps, lost. **Strategy beats data.**

### 🎉 "Jill Destroys Both Experts" - Bristol Week 8
- **Machine** (10K simulations): Elliott ❌ (spun)
- **Mikey** (30 years): Hamlin ❌ (9th)
- **Jill** (staff meetings): **Ty Gibbs ✅** (first career win)
- Machine had Gibbs #11 (6.50%)
- **Staff meeting vibes > algorithms** 🤯

### 💥 "The Big One" - Talladega Week 10
- **Lap 115:** 26-car crash (Bubba/Chastain contact)
- **Eliminated:** Logano (Machine's pick), Larson, Byron, Reddick, Keselowski, Blaney
- **Winner:** Carson Hocevar (first career win, outside Machine's top 15)
- **Machine predicted:** 70% chance of Big One ✅
- **Model was right to say:** "We have no idea" ✓

---

## 📍 Week 11 Preview: Texas Motor Speedway

### 🤝 THE FIRST AGREEMENT

**For the first time, Mikey and The Machine agree:**

#### 🔥 BOTH PICKED: Tyler Reddick #45

**Why Reddick:**
- 5 wins in 2026 (50% win rate) 🏆🏆🏆🏆🏆
- Won Kansas last week ✅
- Won Texas 2022 ✅
- Points leader with massive lead 📊
- Machine: 8.97% probability

#### ⚡ JILL PICKED: Denny Hamlin #11

**Why Hamlin:**
- 3 Texas wins 🏆🏆🏆
- Machine has him #5 (7.78%) 
- Veteran play 🎯
- Jill picks Machine's underrated drivers (again)

### 🥊 The Matchup

```
THE ALLIANCE          vs          THE REBEL
(Mikey + Machine)                   (Jill)
Tyler Reddick #45                Denny Hamlin #11
8.97% probability                Machine's #5 pick
Hot hand (5 wins)                Veteran (3 Texas wins)
```

**Race:** Würth 400 presented by LIQUI MOLY  
**Date:** Sunday, May 3, 2026  
**Time:** 3:30 PM ET  
**TV:** FS1

---

## 🧠 What We've Learned

### 1️⃣ Uncertainty is Honesty
Going from 18% confidence (v1.0) to 7% (Talladega) isn't failure - it's **realism**. NASCAR is chaotic.

### 2️⃣ Context Beats Data
Michael watching qualifying and switching picks beat 10,000 simulations. **Experience captures what models can't.**

### 3️⃣ Simplicity Sometimes Wins
Jill (1-2) picks drivers she "likes" after staff meetings. No data. **Better record than the algorithm.**

### 4️⃣ Specialists Exist
Larson at Kansas. Hendrick at Texas. The model learned to recognize track dominance, even if picks still failed.

### 5️⃣ Chaos is Real
Talladega proved it: "The Big One" eliminated half the field randomly. Model predicted chaos, got chaos. **Being right about uncertainty is still being right.**

---

## 🛠️ Technical Details

### Model Architecture

```python
# v3.0 Formula
score = (
    track_history * 0.25 +           # Historical track performance
    track_type_speed * 0.20 +        # Track-specific speed
    tire_management * 0.15 +         # Long race tire wear
    long_run_speed * 0.15 +          # Sustained pace
    late_race_execution * 0.10 +     # Final laps matter
    track_specific_skill * 0.10 +    # Specialist recognition
    recent_form * 0.05               # Current momentum
)

# Chaos variance
chaos = random.uniform(0.90, 1.10)  # ±10% standard
# Talladega exception: random.uniform(0.60, 1.40)  # ±40%

score *= chaos
```

### Track Type Adaptation

Different NASCAR tracks require completely different models:

| Track Type | Key Attributes | Example Tracks |
|------------|----------------|----------------|
| 🏁 **Superspeedways** | Drafting, chaos survival, pack racing | Daytona, Talladega |
| 🛣️ **Intermediates** | Tire management, long-run speed | Kansas, Texas, Charlotte |
| 🛤️ **Road Courses** | Braking zones, road racing skill | COTA, Sonoma, Watkins Glen |
| 📐 **Short Tracks** | Patience, brake management, passing | Bristol, Martinsville, Richmond |
| 🏜️ **Flat Tracks** | Handling, tire wear, short-run speed | Phoenix, New Hampshire |

---

## 📁 Repository Structure

```
nascar-monte-carlo-predictor/
│
├── 📊 data/
│   ├── driver_stats.csv          # Historical performance data
│   ├── track_data.csv             # Track characteristics
│   └── season_results.csv         # 2026 race results
│
├── 🎨 campaign-content/
│   ├── social-posts/              # Weekly prediction posts
│   ├── images/                    # Generated graphics
│   └── results/                   # Post-race recaps
│
├── 🐍 simulators/
│   ├── v1.0/
│   │   ├── daytona_simulator_v1.py
│   │   ├── atlanta_simulator_v1.py
│   │   └── cota_simulator_v1.py
│   │
│   ├── v2.0/
│   │   └── phoenix_simulator_v2.py (hot hand)
│   │
│   ├── v2.5/
│   │   ├── phoenix_simulator_v2.5.py (regression)
│   │   ├── vegas_simulator_v2.5.py
│   │   └── darlington_simulator_v2.5.py
│   │
│   └── v3.0/
│       ├── martinsville_simulator_v3.py (short track)
│       ├── bristol_simulator_v3.py (high-banked)
│       ├── kansas_simulator_v3.py (intermediate)
│       ├── talladega_simulator_v3.py (chaos mode)
│       └── texas_simulator_v3.py (intermediate)
│
├── 📖 docs/
│   ├── model_evolution.md         # Version history
│   ├── methodology.md             # How it works
│   └── lessons_learned.md         # Campaign insights
│
├── 📄 README.md                   # You are here
├── 📋 requirements.txt            # Python dependencies
└── 📜 LICENSE                     # MIT License

```

---

## 🚀 Installation & Usage

### Prerequisites

```bash
Python 3.8+
NumPy 1.24+
Pandas 2.0+
```

### Quick Start

```bash
# Clone the repository
git clone https://github.com/Katadhin/nascar-monte-carlo-predictor.git
cd nascar-monte-carlo-predictor

# Install dependencies
pip install -r requirements.txt

# Run latest simulator (Texas example)
cd simulators/v3.0
python texas_simulator_v3.py
```

### Output Example

```
================================================================================
TEXAS MOTOR SPEEDWAY - MONTE CARLO SIMULATOR v3.0
Würth 400 presented by LIQUI MOLY | Sunday, May 3, 2026
================================================================================

THE HENDRICK vs REDDICK SHOWDOWN:
- Hendrick Motorsports: 3 of last 5 Texas wins
- Tyler Reddick: 5 wins in 2026, won Texas 2022

Running 10,000 simulations...

================================================================================
TEXAS MONTE CARLO RESULTS (10,000 SIMULATIONS)
================================================================================

Driver                         Car        Wins    Win %
--------------------------------------------------------------------------------
Tyler Reddick                  #45         897    8.97%
Chase Elliott                  #9          812    8.12%
Kyle Larson                    #5          799    7.99%
...

THE MACHINE'S TEXAS PICK (v3.0):
WINNER: Tyler Reddick
WIN PROBABILITY: 8.97%
================================================================================
```

---

## 🤝 Contributing

We're building in public and learning from our mistakes. PRs welcome, especially if you can help us get to 1-10! 😅

**What would you model differently?**

### Ways to Contribute:
- 🐛 Bug fixes
- 📊 Data improvements
- 🧮 Model enhancements
- 📝 Documentation
- 💡 New feature ideas

---

## 📱 Follow the Campaign

- 🏁 **Michael Waltrip Brands:** [Facebook](https://facebook.com/MichaelWaltripBrands) | [Twitter/X](https://x.com/WaltripBrewing) | [Instagram](https://instagram.com/michaelwaltrip)
- 🏆 **Michael Waltrip:** [Twitter/X](https://x.com/MW55)
- 👤 **John Andrews:** [Twitter/X](https://x.com/Katadhin) | [LinkedIn](https://linkedin.com/in/johnandrewsnc) | [GitHub](https://github.com/Katadhin)
- 📝 **Medium:** [Full Campaign Story](https://medium.com/@katadhin/can-racing-instinct-beat-algorithms-were-testing-it-every-week-6cfb2217ae73)

**Weekly picks, results, and model updates posted every race week!**

---

## 📊 Campaign Stats

```
Total Races:        10
Total Simulations:  100,000 (10K per race)
Models Built:       4 (v1.0, v2.0, v2.5, v3.0)
Code Commits:       30+
Social Posts:       50+
Machine Wins:       0 💀
Lessons Learned:    Priceless
```

---

## 📜 License

MIT License - see [LICENSE](LICENSE) for details

**TL;DR:** Use it, modify it, learn from our mistakes. Just don't claim the Machine is good at predictions. 😂

---

## 🙏 Acknowledgments

- **Michael Waltrip** - 2x Daytona 500 champion, proving experience > algorithms
- **Jill** - MWB Communications Manager, proving staff meetings > algorithms
- **The Machine** - Teaching us humility, one loss at a time
- **NASCAR** - For being beautifully unpredictable
- **Everyone following along** - Building in public works because of you

---

## 💭 The Bottom Line

**The Machine is 0-10.**

But the learning is 10-0.

AI isn't replacing human judgment in complex, chaotic systems like NASCAR. It's revealing where intuition still wins - and teaching us to build better models through humble, public failure.

We're picking Tyler Reddick for Texas (Machine + Mikey agree for the first time).

Will we finally get one right? 🤞

**Find out Sunday, May 3 at 3:30 PM ET on FS1.**

---

<div align="center">

### 🏁 Built with ❤️ and a lot of 0-10 humility

**Star this repo if you enjoy watching an AI learn the hard way** ⭐

[![GitHub stars](https://img.shields.io/github/stars/Katadhin/nascar-monte-carlo-predictor?style=social)](https://github.com/Katadhin/nascar-monte-carlo-predictor)
[![Follow @WaltripBrewing](https://img.shields.io/twitter/follow/WaltripBrewing?style=social)](https://x.com/WaltripBrewing)
[![Follow @MW55](https://img.shields.io/twitter/follow/MW55?style=social)](https://x.com/MW55)
[![Follow @Katadhin](https://img.shields.io/twitter/follow/Katadhin?style=social)](https://x.com/Katadhin)

**Next update:** Post-Texas results (Will it be 1-10 or 0-11? Place your bets!)

</div>

---

*Last updated: May 2, 2026*  
*Next race: Texas Motor Speedway - May 3, 2026*  
*Current streak: The Machine has never won* 💀
