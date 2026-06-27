# Michael vs Machine - 2026 NASCAR Prediction Campaign

## Campaign Status
**Current:** Week 18 - Sonoma Preview (June 27, 2026)
**Season Progress:** Mid-season turning point after San Diego chaos

## Standings (Through Week 17)

| Rank | Predictor | Wins | Losses | Percentage | Status |
|------|-----------|------|--------|-----------|--------|
| 🥇 | Jill | 3 | 6 | 33.3% | LEADING ⭐ |
| 2️⃣ | Mikey | 4 | 12 | 25.0% | Steady |
| 3️⃣ | The Machine | 2 | 15 | 11.8% | Bouncing Back |

## The Narrative

### Setup (Weeks 14-15)
Three approaches emerge:
- **Jill:** Momentum reading + warmth (coffee cup iconic)
- **Machine:** Algorithm + analytics (data-driven)
- **Mikey:** Veteran experience + instinct (40 years in racing)

### Rising Action (Week 16)
Hamlin dominates. Jill tries psychological counter-pick. Machine gets it right. Divergence begins.

### Chaos Event (Week 17 - San Diego)
**Everything breaks:**
- Brand new street course at Naval Base Coronado
- Corey Heim (part-timer, 13th career start) wins his FIRST CUP RACE
- Shane van Gisbergen (defending champ, 6 of 8 road wins) gets WRECKED - DNF
- **ALL THREE PREDICTORS WRONG (0-for-3)**

**Lessons Learned:**
- Unpredictability > specialist skills on NEW tracks
- Dominance ≠ Destiny on unpredictable courses
- Hunger + desperation beats experience + credentials

### Redemption (Week 18 - Sonoma)
After chaos, predictors adapt:
- **Machine:** v3.0 → v3.1 algorithm update. Now betting consistency (Larson 2x Sonoma winner) > dominance (SVG defending champ but DNF)
- **Jill:** TBD pick (awaiting)
- **Mikey:** TBD pick (awaiting)

**Central Question:** Can they learn from San Diego? Does consistency beat dominance on established tracks?

## Project Structure

```
├── simulators/
│   ├── sandiego_simulator_v3.py (street course - v3.0 pre-update)
│   ├── sonoma_simulator_v3.py (road course - v3.1 post-update)
│   └── [additional simulators for Nashville, Michigan, Pocono]
│
├── results/
│   └── 2026-race-picks-results.json (full race history + picks)
│
├── campaign/
│   ├── character-records.md (character stats, arcs, signatures)
│   ├── season-narrative.md (full story arc, themes, character development)
│   ├── algorithm-changelog.md (v3.0 → v3.1 evolution, code changes, learnings)
│   └── [weekly-recaps, predictions, posts]
│
└── README.md (this file)
```

## Character Profiles

### 🤖 The Machine
**Role:** Monte Carlo algorithm predictor
**Method:** Data analysis, statistical modeling, track-specific parameters
**Evolution:** v3.0 (dominance-focused) → v3.1 (consistency + context-aware)
**Record:** 2-15 (11.8%) - but algorithm is LEARNING
**Current Pick (Week 18):** Kyle Larson #5 (24.53%)
**Signature:** White MWB shirt, blue glowing eyes, blue circuit patterns, dark background

### ☕ Jillian Camilleri
**Role:** Marketing strategist for Michael Waltrip Brewing Company
**Method:** Momentum reading, narrative psychology, strategic thinking
**Evolution:** Pure heart picks → momentum tracking → psychological analysis
**Record:** 3-6 (33.3%) ⭐ LEADING
**Strength:** Her logic is SOUND even when picks lose. Reads the race narrative.
**Signature:** Coffee cup always in hand, warm/professional, genuine warmth with sharp reads

### 🤠 Michael Waltrip
**Role:** 2x Daytona 500 champion, racing legend
**Method:** Veteran instinct, experience-based reading, championship perspective
**Evolution:** Early wins → struggles with road courses → searching for redemption
**Record:** 4-12 (25%)
**Strength:** Legendary NASCAR knowledge, but road courses proving difficult
**Challenge:** "39 years in racing and I didn't see THAT" (San Diego upset)
**Signature:** Cowboy hat, clipboard, weathered/veteran face, authentic NASCAR presence

## Key Moments

### Week 15 - Michigan (Jill's Rise)
Jill picks Hamlin back-to-back. Gets it right. Momentum reading validates.

### Week 16 - Pocono (Machine's Bounce)
Machine picks Hamlin correctly ("Corners are data"). Algorithm working on known tracks.

### Week 17 - San Diego (THE TURNING POINT)
- Corey Heim wins first Cup race (nobody expected him)
- SVG wrecked Stage 1 (dominance ≠ destiny)
- All three predictors wrong (0-for-3)
- **Inflection point:** Algorithm humbled, veterans questioned, momentum irrelevant

### Week 18 - Sonoma (The Test)
Machine betting consistency (Larson) > dominance (SVG) on established track
v3.1 algorithm learning in real-time
Can they adapt from San Diego chaos?

## Algorithm Evolution

### v3.0 (Baseline)
- Road course specialty bonus: 5% swing
- Dominance weighting: High (6 of 8 wins = strong signal)
- Track familiarity: Not weighted heavily
- **Result:** Works on known ovals, fails on NEW street courses

### San Diego Learning Event
- Chaos exposed algorithm blind spot
- Unpredictability > specialist credentials
- Recent DNF matters more than historic dominance

### v3.1 (Updated)
- **New variable:** Established vs new track distinction
- **Consistency bonus:** +4% on known tracks
- **Dominance penalty:** -50% effectiveness on brand new tracks
- **Local knowledge:** +3% bonus for native region
- **Recent DNF penalty:** 15% performance hit in next race
- **Result:** Sonoma = test of learning (consistency vs dominance)

## Sonoma Hypothesis (v3.1)

**Theory:** Kyle Larson's consistency + local knowledge beats Shane van Gisbergen's dominance + recent DNF

**Supporting Data:**
- Larson: 2x Sonoma winner (2021, 2024), local (Elk Grove), no recent crashes
- SVG: Defending champ (strong), but San Diego DNF (momentum reset)
- Established track = consistency weighted heavily
- Recent DNF = 15% penalty

**Confidence:** 24.53% (moderate, learned humility from San Diego)

## Season Themes

1. **Dominance ≠ Destiny** (SVG had everything, got wrecked)
2. **Consistency > Peak Performance** (on established tracks)
3. **Hunger Beats Experience** (Heim beat SVG at San Diego)
4. **Algorithm Learning in Real-Time** (v3.0 → v3.1 after one race)
5. **Unpredictability Rules** (new tracks trump specialist skills)

## Next Steps

### Week 18 (Sonoma - Tomorrow)
- Await Jill's pick (TBD)
- Await Mikey's pick (TBD)
- Test v3.1 algorithm (Larson vs SVG)
- **Result:** Validates or invalidates San Diego learning

### Weeks 19-36
- In-Season Challenge (knock-out bracket)
- Road course season continues (unpredictability factor)
- Championship implications intensify
- Track campaign + character arc development

## Files & Documentation

- **`2026-race-picks-results.json`** - Full race history with picks, results, records
- **`character-records.md`** - Character stats, signatures, arcs, current standing
- **`season-narrative.md`** - Full story arc, themes, character development, analysis
- **`algorithm-changelog.md`** - v3.0 → v3.1 evolution, code changes, learnings
- **`simulators/`** - Monte Carlo simulator scripts (sandiego_v3.0, sonoma_v3.1)

## Contributing

Weekly updates after each race:
1. Update results in `2026-race-picks-results.json`
2. Update character records in `campaign/character-records.md`
3. Add race recap to `campaign/season-narrative.md`
4. Commit simulator outputs to `simulators/`
5. Document lessons learned in `algorithm-changelog.md`

## Campaign Goals

- Track three predictors' performance over 36-week season
- Document algorithm evolution (v3.0 → v3.1 → ?)
- Capture character arcs (Jill's rise, Machine's learning, Mikey's redemption)
- Analyze NASCAR prediction patterns and unpredictability
- Build narrative-driven sports analytics framework

---

**Campaign Created:** 2026 NASCAR Cup Series, Weeks 14-36
**Last Updated:** June 27, 2026 (Week 18 - Sonoma Preview)
**Status:** Mid-season turning point. Adaptation phase. Redemption arc beginning.
