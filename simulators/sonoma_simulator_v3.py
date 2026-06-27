#!/usr/bin/env python3
"""
Sonoma Raceway Monte Carlo Simulator v3.0
Toyota/Save Mart 350 - June 28, 2026
1.99-mile road course, 12 turns, multi-elevation
110 laps, 218.9 miles
Key: Technical precision, smooth braking, elevation management, road course mastery
"""

import random
import math
from collections import defaultdict

# ═══════════════════════════════════════════════════════════════════════════
# SONOMA ROAD COURSE PARAMETERS
# ═══════════════════════════════════════════════════════════════════════════

# Sonoma is a TRADITIONAL ROAD COURSE - established, familiar, technical
# Characteristics:
# - 1.99-mile oval-turned-road course (historic track)
# - 12 turns (technical, elevation changes)
# - Multi-elevation layout (gains/losses throughout)
# - Heavy braking zones (precision required)
# - Limited passing zones (qualifying/track position matter)
# - Rewards smooth driving, technical precision, patience
# - SVG OWNS this track (won 2025, 6 of 8 recent road wins)
# - Kyle Larson 2x winner here (local guy - Elk Grove)
# - Unlike San Diego (unpredictable street chaos), Sonoma is KNOWN entity

SONOMA_AVERAGE_SPEED = 110  # mph (established road course, faster than street circuits)
SONOMA_LAP_TIME = 64.6      # seconds (~1 min 4.6 sec)
SONOMA_LAPS = 110
SONOMA_BRAKING_EVENTS = 12  # 12 turns = 12 braking zones per lap
SONOMA_CAUTION_PROBABILITY = 0.035  # 3.5% per lap (established track, fewer mistakes)

# Driver data: (base_speed, road_course_specialty, braking_precision, elevation_management, patience, adaptability)
# Road/road course specialists rated VERY HIGH
DRIVERS = {
    "Shane van Gisbergen": (136, 0.98, 0.97, 0.96, 0.98, 0.97),  # SONOMA DEFENDING CHAMP (won 2025, 6 of 8 road wins)
    "Kyle Larson": (138, 0.94, 0.95, 0.94, 0.93, 0.92),  # 2x Sonoma winner (2021, 2024) - LOCAL guy
    "Tyler Reddick": (137, 0.91, 0.92, 0.90, 0.91, 0.90),  # Smooth style, road capable
    "Chase Elliott": (139, 0.89, 0.90, 0.88, 0.89, 0.87),  # Proven road winner, recent form dipped
    "Chris Buescher": (136, 0.88, 0.89, 0.87, 0.88, 0.86),  # Underrated road specialist
    "Michael McDowell": (135, 0.87, 0.88, 0.86, 0.87, 0.85),  # Consistent technician
    "Christopher Bell": (138, 0.86, 0.87, 0.85, 0.86, 0.84),  # Strong on road but not specialist
    "Connor Zilisch": (135, 0.85, 0.84, 0.83, 0.85, 0.83),  # Young, road racing background
    "William Byron": (139, 0.83, 0.84, 0.82, 0.83, 0.81),  # Technical but not road specialist
    "Denny Hamlin": (141, 0.72, 0.73, 0.71, 0.70, 0.69),  # WEAK on road courses (oval guy)
    "Kyle Larson": (138, 0.94, 0.95, 0.94, 0.93, 0.92),  # 2x Sonoma winner
    "Joey Logano": (139, 0.75, 0.76, 0.74, 0.75, 0.73),  # Oval-focused
    "Ryan Blaney": (141, 0.77, 0.78, 0.76, 0.77, 0.75),  # Better on ovals
    "AJ Allmendinger": (135, 0.93, 0.92, 0.91, 0.93, 0.91),  # ROAD LEGEND
    "Ty Gibbs": (138, 0.79, 0.78, 0.77, 0.78, 0.76),  # Developing road skills
    "Austin Cindric": (137, 0.81, 0.80, 0.79, 0.80, 0.78),  # Road capable
}

# ═══════════════════════════════════════════════════════════════════════════
# SIMULATION ENGINE
# ═══════════════════════════════════════════════════════════════════════════

def run_sonoma_race_simulation(num_simulations=10000):
    """
    Run Monte Carlo simulation for Sonoma road course race
    
    Track dynamics:
    - 1.99-mile traditional road course (established, familiar)
    - 12 turns with elevation management
    - Road/road course specialists dominate (NOT unpredictable like San Diego)
    - Technical precision >> raw speed
    - Established track = SVG's wheelhouse (defending champ, 6 of 8 road wins)
    - Kyle Larson local threat (2x Sonoma winner)
    - Fewer cautions than street courses (established track)
    
    DATA POINT: Shane van Gisbergen won Sonoma 2025, dominates road courses
    This is SVG's track type and SVG's actual track. Data is VERY strong.
    """
    
    results = defaultdict(int)
    
    for sim in range(num_simulations):
        # Initialize race state
        tire_wear = {driver: 0 for driver in DRIVERS}
        position = {driver: i for i, driver in enumerate(DRIVERS, 1)}
        laps_led = {driver: 0 for driver in DRIVERS}
        pit_stops = {driver: 0 for driver in DRIVERS}
        mistakes = {driver: 0 for driver in DRIVERS}
        
        current_leader = "Shane van Gisbergen"  # SVG favored
        caution_flags = 0
        lap = 0
        
        # ─────────────────────────────────────────────────────────────────────
        # RACE SIMULATION: 110 laps
        # ─────────────────────────────────────────────────────────────────────
        
        while lap < SONOMA_LAPS:
            lap += 1
            
            # ─────────────────────────────────────────────────────────────────
            # TIRE WEAR & PIT STRATEGY
            # ─────────────────────────────────────────────────────────────────
            
            for driver in DRIVERS:
                base_speed, road_spec, braking, elevation, patience, adapt = DRIVERS[driver]
                tire_wear[driver] += (1.0 / (35 * braking))  # 35-lap tire window on road course
            
            # Pit window every 35 laps
            pit_window_open = (lap % 35 == 0) or (lap > SONOMA_LAPS - 10)
            
            if pit_window_open:
                for driver in DRIVERS:
                    if tire_wear[driver] > 0.90 or lap > SONOMA_LAPS - 10:
                        tire_wear[driver] = 0
                        pit_stops[driver] += 1
            
            # ─────────────────────────────────────────────────────────────────
            # PERFORMANCE VARIANCE (Road course = moderate variance)
            # ─────────────────────────────────────────────────────────────────
            
            performance = {}
            for driver in DRIVERS:
                base_speed, road_spec, braking, elevation, patience, adapt = DRIVERS[driver]
                
                # Road course variance: lower than street courses (established track)
                variance = random.gauss(1.0, 0.018)
                
                # Road/road course specialty bonus (DOMINANT factor)
                road_bonus = 1.0 + (road_spec * 0.05)
                
                # Braking precision bonus (12 turns = 12 braking zones)
                braking_bonus = 1.0 + (braking * 0.03)
                
                # Elevation management bonus (unique to Sonoma's multi-elevation)
                elevation_bonus = 1.0 + (elevation * 0.02)
                
                # Patience bonus (road courses reward smooth, patient drivers)
                patience_bonus = 1.0 + (patience * 0.02)
                
                # Tire wear impact
                tire_impact = 1.0 - (tire_wear[driver] / 1.0) * 0.03
                
                # Adaptability on established track
                adapt_bonus = 1.0 + (adapt * 0.015)
                
                # Mistake penalty (fewer mistakes on established track)
                if random.random() < (1.0 - braking) * 0.07:
                    mistakes[driver] += 1
                mistake_penalty = 1.0 - (mistakes[driver] * 0.015)
                
                performance[driver] = (
                    base_speed * 
                    variance * 
                    road_bonus * 
                    braking_bonus * 
                    elevation_bonus * 
                    patience_bonus * 
                    tire_impact * 
                    adapt_bonus * 
                    mistake_penalty
                )
            
            # ─────────────────────────────────────────────────────────────────
            # POSITION DETERMINATION
            # ─────────────────────────────────────────────────────────────────
            
            sorted_drivers = sorted(performance.items(), key=lambda x: x[1], reverse=True)
            
            for new_pos, (driver, perf) in enumerate(sorted_drivers, 1):
                position[driver] = new_pos
            
            # Leader tracking
            current_leader = sorted_drivers[0][0]
            laps_led[current_leader] += 1
            
            # ─────────────────────────────────────────────────────────────────
            # CAUTION FLAG EVENTS (Lower probability - established track)
            # ─────────────────────────────────────────────────────────────────
            
            if random.random() < SONOMA_CAUTION_PROBABILITY:
                caution_flags += 1
                random.shuffle(list(DRIVERS.keys()))
        
        # ─────────────────────────────────────────────────────────────────────
        # RACE WINNER
        # ─────────────────────────────────────────────────────────────────────
        
        winner = current_leader
        results[winner] += 1
    
    return results

# ═══════════════════════════════════════════════════════════════════════════
# ANALYZE RESULTS
# ═══════════════════════════════════════════════════════════════════════════

def analyze_sonoma_results():
    """Run simulations and display results"""
    
    print("\n" + "="*80)
    print("SONOMA RACEWAY - MONTE CARLO SIMULATION v3.0")
    print("Toyota/Save Mart 350 | June 28, 2026 | 110 laps, 218.9 miles")
    print("="*80)
    print("\nTrack Profile: 1.99-mile TRADITIONAL ROAD COURSE (12 turns, multi-elevation)")
    print("Historic track at Sonoma Raceway in wine country, Northern California")
    print("Key Factors: Road course mastery, technical precision, elevation management, patience")
    print("Caution Factor: Lower (established track, fewer mistakes than street courses)")
    print("\n" + "="*80)
    
    print("\n⏳ Running 10,000 simulations...")
    results = run_sonoma_race_simulation(10000)
    
    # Sort by win count
    sorted_results = sorted(results.items(), key=lambda x: x[1], reverse=True)
    
    print("\n" + "="*80)
    print("TOP 10 PREDICTED FINISHERS:")
    print("="*80)
    
    total_sims = sum(results.values())
    
    for rank, (driver, wins) in enumerate(sorted_results[:10], 1):
        percentage = (wins / total_sims) * 100
        bars = "█" * int(percentage / 2) + "░" * (50 - int(percentage / 2))
        print(f"\n{rank:2d}. {driver:30s} {wins:5d} wins ({percentage:6.2f}%)")
        print(f"    │{bars}│")
    
    # Calculate confidence for top pick
    top_driver = sorted_results[0][0]
    top_percentage = (sorted_results[0][1] / total_sims) * 100
    
    print("\n" + "="*80)
    print("THE MACHINE'S SONOMA PICK:")
    print("="*80)
    print(f"\n🤖 {top_driver.upper()}")
    print(f"   Confidence: {top_percentage:.2f}%")
    print(f"\n   Why: Sonoma is a TRADITIONAL ROAD COURSE. {top_driver} has")
    print(f"   road course mastery, technical precision, elevation management,")
    print(f"   and established track experience. This is {top_driver}'s wheelhouse.")
    print(f"\n   Key Quote: \"{top_percentage:.1f}%. {top_driver}. Road course dominance.\"")
    
    print("\n" + "="*80)
    print("SONOMA RACE CONTEXT:")
    print("="*80)
    print("\n✓ 1.99-mile traditional road course (established, familiar)")
    print("✓ 12 turns with elevation management (multi-elevation changes)")
    print("✓ Historic track (unlike San Diego's brand-new street course)")
    print("✓ 110 laps, 218.9 miles")
    print("✓ Limited passing zones (qualifying/track position critical)")
    print("✓ Heavy braking zones (precision required)")
    print("✓ SVG: Defending 2025 champion, 6 of 8 recent road wins")
    print("✓ Kyle Larson: 2x Sonoma winner (2021, 2024) - LOCAL guy from Elk Grove")
    print("✓ Road course specialists expected to dominate (NOT unpredictable)")
    print("✓ Starts 2026 In-Season Challenge")
    
    print("\n" + "="*80)
    print(f"RACE INFO: Toyota/Save Mart 350")
    print(f"Date: Sunday, June 28, 2026 | Time: 3:30 PM ET")
    print(f"Track: Sonoma Raceway, Sonoma, California (wine country)")
    print(f"Network: TNT Sports")
    print(f"Historic: 2025 winner Shane van Gisbergen returning as defending champ")
    print("="*80 + "\n")
    
    return sorted_results

# ═══════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    results = analyze_sonoma_results()
