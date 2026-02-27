# Track-Specific Prediction Approaches

This document explains how the NASCAR Monte Carlo Predictor adapts to different track types.

## Track Type Classification

NASCAR races occur on three main track types, each requiring different prediction strategies:

### 1. Superspeedways
**Examples:** Daytona, Talladega  
**Length:** 2.5+ miles  
**Characteristics:** Pack racing, restrictor plates, drafting-dependent

### 2. Intermediate Tracks
**Examples:** Atlanta, Charlotte, Texas  
**Length:** 1.5-2.0 miles  
**Characteristics:** Tire wear, multiple grooves, strategy-dependent

### 3. Road Courses  
**Examples:** COTA, Sonoma, Watkins Glen  
**Characteristics:** Left AND right turns, braking zones, technical racing

---

## Superspeedway Model (Daytona)

### Key Attributes
- **drafting_iq** (0-10): Pack racing awareness and positioning
- **plate_skill** (0-10): Restrictor plate racing ability
- **chaos_survival** (0-10): Avoiding "Big One" multi-car wrecks
- **late_race_clutch** (0-10): Final lap execution under pressure

### Chaos Modeling
**"Big One" Probability:** 98.2%  
**Expected Lap:** 144 (range: 120-190)  
**Crash Size:** 10-20 cars  
**Attrition Rate:** ~50% DNF

### Winner Calculation
```python
score = (
    drafting_iq * 0.25 +
    plate_skill * 0.25 +
    chaos_survival * 0.20 +
    clutch_factor * 0.30
)

# Apply chaos scenario
if big_one_occurred:
    score *= (chaos_survival / 8.0 + 0.5)
```

### Top Performers
- **Penske drivers** (Blaney, Logano): Elite drafting IQ
- **Plate specialists** (Stenhouse, McDowell): Chaos survivors
- **Clutch performers** (Hamlin): Late-race execution

---

## Intermediate Track Model (Atlanta)

### Key Attributes
- **tire_management** (0-10): Preserving tire life over long runs
- **restart_skill** (0-10): Gaining positions on restarts
- **long_run_speed** (0-10): Speed on older tires
- **short_run_speed** (0-10): Speed on fresh tires

### Chaos Modeling
**Early Carnage (Lap 1-5):** 36% probability  
**Green-White-Checkered:** 82% probability  
**Average Cautions:** 4.9  
**Attrition Rate:** ~51% DNF

### Winner Calculation
```python
score = (
    base_speed * 0.18 +
    tire_management * 0.18 +
    restart_skill * 0.18 +
    clutch_factor * 0.22 +
    recent_form * 0.12 +
    long_run_speed * 0.12
)

# Green-white-checkered boost
if overtime:
    score *= (restart_skill / 8.0 + 0.5)
```

### Model Improvements (v2.0)
- ✅ Reduced attrition from 88% → 51%
- ✅ Recent form multiplier (Daytona winner gets boost)
- ✅ Scenario branching (clean vs chaos start)

### Top Performers
- **Hendrick drivers** (Elliott, Byron, Bowman): Equipment + tire management
- **JGR drivers** (Bell, Hamlin): Consistent speed
- **Restart specialists** (Logano): GWC masters

---

## Road Course Model (COTA)

### Key Attributes
- **road_course_skill** (0-10): Overall road racing ability
- **braking_zones** (0-10): Late braking into corners
- **corner_entry** (0-10): Turn-in precision
- **corner_exit** (0-10): Acceleration out of turns
- **passing_ability** (0-10): Wheel-to-wheel road racing
- **recovery** (0-10): Bouncing back from mistakes

### Chaos Modeling
**Turn 1 Lap 1 Incident:** 34% probability  
**Average Cautions:** 3.6  
**Attrition Rate:** ~10% DNF (road courses are CLEAN)

### Winner Calculation
```python
score = (
    road_course_skill * 0.30 +
    braking_zones * 0.15 +
    corner_exit * 0.15 +
    passing_ability * 0.10 +
    tire_preservation * 0.10 +
    clutch_factor * 0.10 +
    recent_form * 0.10
)

# Specialist boost
if tier == "specialist":
    score *= 1.30
```

### Top Performers
- **Road course specialists** (van Gisbergen, Allmendinger): Elite skill
- **Road course winners** (Bell, Byron, Reddick): Historical success
- **Versatile drivers** (Larson, Chastain): Adapt to any track

---

## Attribute Comparison Table

| Attribute | Daytona | Atlanta | COTA |
|-----------|---------|---------|------|
| **Primary Skill** | Drafting IQ | Tire Management | Road Course Skill |
| **Secondary** | Chaos Survival | Restart Execution | Braking Zones |
| **Chaos Type** | Big One (multi-car) | Early + Overtime | Turn 1 incident |
| **Attrition** | 50% | 51% | 10% |
| **Team Advantage** | Penske | Hendrick | Specialists > Teams |

---

## Why Track Type Matters

**Example: Denny Hamlin**

| Track Type | Prediction Rank | Win % | Why |
|------------|----------------|-------|-----|
| Daytona | #2 | 3.36% | Elite drafting IQ (9.5/10) + clutch |
| Atlanta | #2 | 6.37% | Strong restart skill (9.5/10) |
| COTA | #10 | 5.72% | Road course skill only 7.0/10 |

**Example: Shane van Gisbergen**

| Track Type | Prediction Rank | Win % | Why |
|------------|----------------|-------|-----|
| Daytona | Not Top 15 | <2% | No oval experience |
| Atlanta | Not Top 15 | <2% | No oval experience |
| COTA | #1 | 9.11% | Elite road racer (9.5/10 skill) |

---

## Manufacturer Trends by Track

### Superspeedways (Daytona)
- Balanced: Chevy 35%, Toyota 34%, Ford 32%
- Team strength matters more than manufacturer

### Intermediate (Atlanta)
- Chevy advantage: 44%, Toyota 29%, Ford 27%
- Hendrick equipment dominance

### Road Courses (COTA)
- Chevy dominance: 65%, Toyota 19%, Ford 16%
- Trackhouse (SVG, Chastain) + Hendrick fleet

---

## Model Adaptation Process

1. **Analyze track characteristics**
   - Length, banking, turn count
   - Historical winner patterns
   - Chaos probabilities

2. **Define relevant attributes**
   - What skills matter at this track?
   - Which attributes become irrelevant?

3. **Weight attributes appropriately**
   - Primary skills: 25-30%
   - Secondary skills: 10-20%
   - Clutch/momentum: 10-15%

4. **Calibrate chaos model**
   - Historical incident rates
   - Typical crash sizes
   - Attrition patterns

5. **Validate predictions**
   - Recent winners in top 10?
   - Specialists ranked appropriately?
   - Attrition rate realistic?

---

## Future Track Types

**Short Tracks (Bristol, Martinsville):**
- Attributes: Handling, patience, bump-and-run skill
- Chaos: Constant contact, tire strategy critical

**Intermediate Ovals (Kansas, Las Vegas):**
- Attributes: Aero efficiency, handling balance
- Chaos: Clean racing, strategy-dependent

Each track type requires a custom approach. The model learns and adapts.
