# Algorithm Evolution Changelog - 2026 NASCAR Prediction Campaign

## v3.0 → v3.1 Evolution (San Diego Learning Event)

### v3.0 Baseline (Through Week 16 - Pocono)
**Status:** Established road course parameters, decent oval performance

**Key Parameters:**
- Road course specialty bonus: 5% swing
- Braking precision bonus: 3% swing
- Tire wear calculations: standard
- Caution probability: track-dependent
- Variance: 2-3% per lap

**Performance:**
- Week 14 (Nashville oval): ❌ Elliott pick (Hamlin won)
- Week 15 (Michigan oval): ❌ Larson pick (Hamlin won)
- Week 16 (Pocono oval): ✅ Hamlin pick (Hamlin won 3rd straight)
- **Record:** 1-2 on oval track picks

**Insight:** Algorithm works on familiar oval tracks with established data.

---

### The San Diego Chaos Event (Week 17)
**What Happened:**
- Track: Brand-new street course at Naval Base Coronado
- Algorithm pick: Chase Elliott #9 (technical consistency)
- Expected winner: SVG (defending champ, 6 of 8 road wins)
- **ACTUAL WINNER:** Corey Heim #67 (part-timer, 13th career start, FIRST CUP WIN)

**Why Algorithm Failed:**
1. **Unpredictability:** New street course = no historical data
2. **Dominance ≠ Destiny:** SVG was wrecked Stage 1 (DNF)
3. **Chaos factor:** Elliott didn't place top 5
4. **Overconfidence:** Algorithm weighted specialist skills too heavily
5. **Missing variable:** Hunger + desperation (Heim had nothing to lose)

**Post-Race Analysis:**
- Street course chaos = algorithm blind spot
- Unpredictable tracks require different weighting
- Consistency metrics > dominance metrics on NEW tracks
- Road/street courses need distinction (traditional vs temporary)

---

### v3.1 Update (Week 18 - Sonoma Preparation)

**Code Changes Implemented:**

#### 1. Track Familiarity Weighting
```
ESTABLISHED_TRACK_BONUS = 1.0 + (consistency_metric * 0.04)
NEW_TRACK_PENALTY = 1.0 - (unpredictability_factor * 0.05)
```

**Logic:** 
- Established tracks (Sonoma, Charlotte, Vegas) = consistency > dominance
- New/street courses = historical performance < local knowledge + hunger

#### 2. Dominance Recalibration
```
OLD: dominance_bonus = 1.0 + (recent_wins * 0.06)
NEW: dominance_on_known_tracks = 1.0 + (recent_wins * 0.06)
     dominance_on_new_tracks = 1.0 + (recent_wins * 0.02)
```

**Logic:**
- 6 of 8 road wins = strong signal on KNOWN tracks
- 6 of 8 road wins = weaker signal on BRAND NEW tracks
- Unpredictability changes the equation

#### 3. Local Knowledge Addition
```
local_knowledge_bonus = 1.0 + (native_region * 0.03)
```

**Sonoma Application:**
- Kyle Larson: Elk Grove, CA (local) = +3% bonus
- Shane van Gisbergen: Australia (not local) = no bonus

#### 4. Consistency vs Peak Performance
```
OLD: performance = base_speed * road_specialty * variance
NEW: 
  ON_ESTABLISHED_TRACK: performance = base_speed * consistency * road_specialty * variance
  ON_NEW_TRACK: performance = base_speed * adaptability * hunger * variance
```

**Logic:**
- Established tracks reward steady, consistent performers
- New tracks reward adaptability + drivers with less pressure

#### 5. DNF Momentum Reset
```
RECENT_DNF_PENALTY = 0.85 (15% performance hit in next race)
```

**Application:**
- SVG wrecked San Diego = 15% penalty entering Sonoma
- Even though SVG won at Sonoma 2025, recent DNF impacts confidence

---

### v3.1 Parameters Updated

**Sonoma Specific (Traditional Road Course - Established Track):**

```python
SONOMA_CONSISTENCY_WEIGHT = 0.95  # High (established track)
SONOMA_DOMINANCE_WEIGHT = 0.80   # Medium (proven performance)
SONOMA_LOCAL_KNOWLEDGE = 0.92     # High (Larson local)
SONOMA_RECENT_DNF_FACTOR = 0.85   # SVG penalty
```

**Result:**
- Kyle Larson: 24.53% (consistency + local + no recent DNF)
- Chase Elliott: 19.55% (consistent road specialist)
- Shane van Gisbergen: 12.77% (dominance but SVG DNF penalty + established track weights consistency)

---

## Learning Framework

### What San Diego Taught The Algorithm

1. **New ≠ Predictable**
   - Brand-new tracks can't be modeled from historical data
   - Hunger + desperation > specialist credentials

2. **Dominance Is Conditional**
   - 6 of 8 wins = strong on KNOWN tracks
   - 6 of 8 wins ≠ guarantee on UNKNOWN tracks

3. **Unpredictability Has a Variance**
   - Street courses: 5.5% caution probability
   - Oval courses: 2-3% caution probability
   - New street courses: Unknown variance (treat as +10% chaos)

4. **Recent Performance Context Matters**
   - DNF = momentum reset
   - Even defending champs need rebuilding after crashes

5. **Consistency > Peak Performance (On Known Tracks)**
   - Established tracks reward steady drivers
   - Street courses = chaos (all bets off)

---

## Sonoma Hypothesis (v3.1)

**Theory:** Kyle Larson's consistency + local knowledge beats Shane van Gisbergen's recent DNF momentum reset

**Data Supporting:**
- Larson: 2x Sonoma winner, local (Elk Grove), no recent crashes
- SVG: Defending champ (strong), but DNF at San Diego (momentum hit)

**Code Supporting:**
- Established track = consistency weighted heavily
- Recent DNF = 15% penalty
- Local knowledge = +3% bonus

**Confidence:** 24.53% (moderate, not dominant)

**Risk:** If Sonoma proves unpredictable again (like San Diego), algorithm needs further evolution

---

## Future Evolutions (Pending)

### v3.2: Driver Hunger Index
- First-time winners at track
- Desperation metrics (playoff position)
- Revenge factor (redemption after losses)

### v3.3: Multi-Track Pattern Recognition
- Oval vs road course consistency
- Driver specialization across track types
- Seasonal momentum tracking

### v3.4: Real-Time Adjustment
- Live pit strategy analysis
- Weather impact modeling
- Caution flag frequency updates

---

## Deployment Notes

### For Cowork Tracking
- **Simulator:** `/simulators/sonoma_simulator_v3.py` (v3.1 code embedded)
- **Previous simulators:** San Diego (v3.0 pre-update), Pocono/Michigan/Nashville (archived)
- **Next build:** Include v3.1 parameters in all future simulators

### For Season Analysis
- San Diego = inflection point (algorithm humbled)
- Sonoma = redemption test (algorithm bounces back?)
- Consistency hypothesis being tested live

---

**Last Updated:** June 27, 2026 (Pre-Sonoma)
**Next Update:** June 28, 2026 (Post-Sonoma - validation of v3.1)
