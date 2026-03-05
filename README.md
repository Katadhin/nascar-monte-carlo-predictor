# NASCAR Monte Carlo Predictor

![Python](https://img.shields.io/badge/python-3.8+-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)
![NumPy](https://img.shields.io/badge/numpy-1.24+-orange.svg)
![Status](https://img.shields.io/badge/campaign-active-brightgreen.svg)

Monte Carlo simulation engine for NASCAR race predictions. Built for "Michael vs. Machine" campaign - AI vs human racing instinct across different track types.

**Read the story:** [Can Racing Instinct Beat Algorithms? We're Testing It Every Week](https://medium.com/@katadhin/can-racing-instinct-beat-algorithms-were-testing-it-every-week-6cfb2217ae73)

---

## Campaign Results (2026 Season)

| Week | Track | Machine Pick | Mikey Pick | Actual Winner | Result |
|------|-------|-------------|-----------|---------------|--------|
| 1 | Daytona 500 | Ryan Blaney | Ryan Blaney | Tyler Reddick | Both ❌ |
| 2 | Atlanta | Chase Elliott | Ross Chastain | Tyler Reddick | Both ❌ |
| 3 | COTA | Shane van Gisbergen | Tyler Reddick | Tyler Reddick | Machine ❌ Mikey ✅ |
| 4 | Phoenix | *See below* | TBD | TBD | Pending |

**Current Record:**
- Machine: 0-3 on winners
- Mikey: 1-3 on winners (called Reddick at COTA)

### Phoenix Dual Model Predictions (Week 4)

For the first time, the Machine generated **two different models** with conflicting predictions:

**Model v2.0 (Hot Hand Formula):**
- **Winner Pick:** Tyler Reddick - 22.58%
- Philosophy: Momentum beats everything. Ride the hot streak.

**Model v2.5 (Regression to Mean):**
- **Winner Pick:** William Byron - 11.82%
- Tyler Reddick: 7.22% (drops to #7)
- Philosophy: Streaks always end. Respect statistical probability.

**The Disagreement:** 15.36% delta on Reddick's win probability.

**The Question:** Does momentum override statistical regression, or do long win streaks inevitably end? Sunday's race validates which approach works.

---

## Model Evolution: v1.0 → v2.0 → v2.5

### v1.0 (Weeks 1-3): Track Specialists
- Track history: 25% of score
- Recent form: only 10%
- No streak adjustments
- **Result: 0-3** (missed Reddick's momentum completely)

### v2.0 (Week 4): Hot Hand Formula
- Recent form: 30% (tripled)
- Hot streak multiplier: 2.0x for 3+ wins
- Points leader boost: 1.20x
- **Phoenix: Reddick 22.58% (#1)**
- Philosophy: Momentum beats everything

### v2.5 (Week 4): Regression to Mean
- Recent form: 30% (same)
- Streak boost: 1.15x (reduced)
- Pressure penalty: 0.88x for long streaks
- Historical rarity: 0.88x (4 straight is rare)
- **Phoenix: Byron 11.82% (#1), Reddick 7.22% (#7)**
- Philosophy: Streaks end, regression matters

**The Experiment:** Publishing both models to see which philosophy works better.

---

## Track Type Adaptation

Different NASCAR tracks require completely different prediction models:

### Superspeedways (Daytona, Talladega)
- Pack racing, drafting critical
- Key attributes: Drafting IQ, Chaos survival, Plate racing skill

### Intermediate Ovals (Atlanta, Las Vegas)
- Tire management crucial
- Key attributes: Long-run speed, Tire wear, Handling

### Road Courses (COTA, Sonoma)
- Technical racing, specialists dominate
- Key attributes: Road racing skill, Braking zones, Corner entry

### Flat Tracks (Phoenix, Richmond)
- Handling and tire management critical
- Key attributes: Flat track skill, Short-run speed, Passing ability

---

## Installation
```bash
git clone https://github.com/Katadhin/nascar-monte-carlo-predictor.git
cd nascar-monte-carlo-predictor
pip install -r requirements.txt
```

---

## License

MIT License - see [LICENSE](LICENSE)

---

**Current Status:** Testing dual Phoenix models (v2.0 vs v2.5). Race day March 8, 2026. 🏁🤖
