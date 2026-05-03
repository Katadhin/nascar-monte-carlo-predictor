# NASCAR Monte Carlo Predictor
## Michael vs Machine - 2026 Season

A Monte Carlo simulation-based NASCAR Cup Series race prediction system competing against 2x Daytona 500 champion Michael Waltrip and MWB Communications Manager Jill.

**Current Status: The Machine is 0-10 (winless)**

---

## Season Standings (Through Week 10 - Talladega)

| Predictor | Record | Win % | Method |
|-----------|--------|-------|--------|
| **Jill** | 1-2 | 33% | Staff meeting vibes |
| **Mikey** | 2.5-8 | 27% | 30+ years experience |
| **Machine** | 0-10 | 0% | 10,000 Monte Carlo simulations |

---

## Race-by-Race Results

| Week | Race | Winner | Machine Pick | Mikey Pick | Jill Pick | Result |
|------|------|--------|--------------|------------|-----------|--------|
| 1 | Daytona 500 | Tyler Reddick | Ryan Blaney ❌ | Ryan Blaney ❌ | - | Both wrong |
| 2 | Atlanta | Tyler Reddick | Chase Elliott ❌ | Ross Chastain ❌ | - | Both wrong |
| 3 | COTA | Tyler Reddick | Shane van Gisbergen ❌ | Tyler Reddick ✅ | - | Mikey wins |
| 4 | Phoenix | Ryan Blaney | Tyler Reddick/William Byron ❌ | Tyler Reddick ❌ | - | Dual model fail |
| 5 | Vegas | Denny Hamlin | William Byron (3rd) ❌ | Hamlin HM ✅ | - | Mikey 0.5 |
| 6 | Darlington | Tyler Reddick | Denny Hamlin (11th) ❌ | Tyler Reddick ✅ | - | Mikey wins |
| 7 | Martinsville | Chase Elliott | Denny Hamlin (2nd) ❌ | William Byron (5th) ❌ | - | Both had Elliott 5th |
| 8 | Bristol | Ty Gibbs | Chase Elliott (spun) ❌ | Denny Hamlin (9th) ❌ | Ty Gibbs ✅ | Jill wins! |
| 9 | Kansas | Tyler Reddick | Kyle Larson (2nd) ❌ | William Byron (7th) ❌ | Christopher Bell (wrecked) ❌ | Reddick wins again |
| 10 | Talladega | Carson Hocevar | Joey Logano (Big One) ❌ | TBD | Chase Briscoe (Big One) ❌ | Chaos wins |

---

## Model Evolution

### v1.0 - Weeks 1-3 (FAILED)
- **Philosophy:** Pick favorites with high confidence
- **Confidence:** 18%+ for top picks
- **Result:** 0-3, overconfident
- **Lesson:** NASCAR is too chaotic for certainty

### v2.0 - Week 4 Phoenix (FAILED)
- **Change:** Added hot-hand formula (2.0x streak multiplier)
- **Pick:** Tyler Reddick (continuing streak)
- **Result:** Ryan Blaney won, streak ended
- **Lesson:** Streaks regress to mean

### v2.5 - Weeks 4-5 (FAILED)
- **Change:** Pressure penalties, regression to mean
- **Confidence:** Flattened to ~15%
- **Result:** Still 0-2
- **Lesson:** Better philosophy, wrong picks

### v3.0 - Weeks 6-Present (0-6, BUT LEARNING)
- **Changes:**
  - Track-type specific data (short track only for short tracks)
  - Flattened certainty (18.6% → 7.27% at Talladega)
  - Chaos variance always on (±10% standard, ±40% Talladega)
  - Reduced boosts (no runaway favorites)
  - Specialist recognition (Larson at Kansas, Hendrick at Texas)
  - Qualifying integration (10% weight)

**Confidence Reduction:**
- Darlington: 15.75%
- Martinsville: 10.76%
- Bristol: 9.39%
- Kansas: 8.74%
- Talladega: 7.27%
- Texas: 8.97%

**Progress Indicators:**
- ✅ Had Elliott 5th at Martinsville (he won)
- ✅ Picked Larson at Kansas (finished 2nd - closest yet)
- ✅ Talladega: Predicted chaos, got chaos (Hocevar won, outside top 15)

---

## Key Campaign Moments

### "AI Can Kiss My Butt" - Vegas Week 5
Michael's pre-race quote before picking Blaney (who finished 16th). Hamlin won. Comedy gold.

### "Mikey Changes Mind After Qualifying" - Darlington Week 6
- Thursday: Presumed Hamlin pick
- Friday: Watched qualifying, switched to Reddick
- Machine: Mocked "recency bias"
- Result: Reddick WON, Machine's Hamlin finished 11th
- Lesson: Context > data

### "Both Had Elliott 5th" - Martinsville Week 7
Neither Mikey nor Machine picked Elliott #1. Both had him 5th. He won on pit strategy (short-pitted lap 261). Hamlin led 292 laps, lost. Strategy beats data.

### "Jill Destroys Both Experts" - Bristol Week 8
- Machine (10K simulations): Elliott ❌ (spun)
- Mikey (30 years): Hamlin ❌ (9th)
- Jill (staff meetings): Ty Gibbs ✅ (first career win)
- Machine had Gibbs #11 (6.50%)
- Staff meeting vibes > algorithms

### "The Big One" - Talladega Week 10
- Lap 115: 26-car crash (Bubba/Chastain contact)
- Eliminated: Logano (Machine's pick), Larson, Byron, Reddick, Keselowski, Blaney
- Winner: Carson Hocevar (first career win, outside Machine's top 15)
- Machine predicted 70% chance of Big One ✅
- Model was right to say "we have no idea"

---

## Technical Details

**Model:** Monte Carlo simulation (10,000 iterations per race)

**Inputs:**
- Historical track performance
- Recent form/momentum
- Track-type specific data
- Qualifying results (10% weight)
- Team/manufacturer advantages
- Specialist recognition

**v3.0 Formula:**
```python
score = (
    track_history * 0.25 +
    track_type_speed * 0.20 +
    tire_management * 0.15 +
    long_run_speed * 0.15 +
    late_race_execution * 0.10 +
    track_specific_skill * 0.10 +
    recent_form * 0.05
)

# Chaos variance
chaos = random.uniform(0.90, 1.10)  # ±10%
# Talladega exception: ±40%

score *= chaos
```

**Output:** Win probabilities for all drivers

---

## What We've Learned

### 1. Uncertainty is Honesty
Going from 18% confidence (v1.0) to 7% (Talladega) isn't failure - it's realism. NASCAR is chaotic.

### 2. Context Beats Data
Michael watching qualifying and switching picks beat 10,000 simulations. Experience captures what models can't.

### 3. Simplicity Sometimes Wins
Jill (1-2) picks drivers she "likes" after staff meetings. No data. Better record than the algorithm.

### 4. Specialists Exist
Larson at Kansas. Hendrick at Texas. The model learned to recognize track dominance, even if picks still failed.

### 5. Chaos is Real
Talladega proved it: "The Big One" eliminated half the field randomly. Model predicted chaos, got chaos. Being right about uncertainty is still being right.

---

## Week 11 Preview: Texas

**For the first time, Mikey and The Machine agree:**

**BOTH PICKED: Tyler Reddick #45**
- 5 wins in 2026 (50% win rate)
- Won Kansas last week
- Won Texas 2022
- Machine: 8.97% probability

**JILL PICKED: Denny Hamlin #11**
- 3 Texas wins
- Machine has him #5 (7.78%)
- Veteran play

**The Alliance (Mikey + Machine) vs The Rebel (Jill)**

Race: Sunday, May 3 | 3:30 PM ET | FS1

---

## Repository Structure

```
/simulators
  /v1.0
    - daytona_simulator_v1.py
    - atlanta_simulator_v1.py
    - cota_simulator_v1.py
  /v2.0
    - phoenix_simulator_v2.py (hot hand)
  /v2.5
    - phoenix_simulator_v2.5.py (regression)
    - vegas_simulator_v2.5.py
    - darlington_simulator_v2.5.py
  /v3.0
    - martinsville_simulator_v3.py (short track)
    - bristol_simulator_v3.py (high-banked)
    - kansas_simulator_v3.py (intermediate)
    - talladega_simulator_v3.py (chaos mode)
    - texas_simulator_v3.py (intermediate)

/results
  - weekly_results.csv
  - season_standings.csv

README.md
```

---

## Follow Along

- **Social:** Michael Waltrip Brands (Facebook, Twitter, Instagram, LinkedIn)
- **Full transparency:** Every pick, every result, every failure
- **Building in public:** Model iterations visible

---

## The Bottom Line

**The Machine is 0-10.**

But the learning is 10-0.

AI isn't replacing human judgment in complex, chaotic systems. It's revealing where intuition still wins - and teaching us to build better models through humble failure.

---

## License

MIT License - Feel free to use, modify, and learn from our mistakes.

---

## Contributing

PRs welcome. Especially if you can help us get to 1-10.

What would you model differently?

---

*Last updated: May 2, 2026*
*Next race: Texas Motor Speedway - May 3, 2026*
*The Machine: Still seeking first win*
