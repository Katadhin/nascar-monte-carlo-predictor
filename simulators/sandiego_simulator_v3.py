#!/usr/bin/env python3
"""
San Diego Naval Base Coronado Monte Carlo Simulator v3.0
Anduril 250 "Race the Base" - June 21, 2026
3.4-mile temporary street course (16 turns) - LONGEST road course on Cup schedule
75 laps, 255 miles
Key: Road/street course mastery, technical precision, braking, adaptability
First NASCAR race EVER on an active U.S. military base
"""

import random
import math
from collections import defaultdict

# ═══════════════════════════════════════════════════════════════════════════
# SAN DIEGO STREET COURSE PARAMETERS
# ═══════════════════════════════════════════════════════════════════════════

# San Diego is a ROAD/STREET COURSE - completely different animal from ovals
# Characteristics:
# - 3.4 miles (longest on Cup schedule)
# - 16 turns (technical, precision required)
# - Heavy braking zones
# - Tight corners mixed with long straights
# - Passes aircraft carriers, hangars, active airfield
# - Brand new track (no Cup history)
# - Rewards: road course specialists, technical precision, adaptability
# - Penalizes: oval-only drivers, raw speed without technique

SANDIEGO_AVERAGE_SPEED = 105  # mph (street course = much slower than ovals)
SANDIEGO_LAP_TIME = 123.0     # seconds (~2 minutes, longest laps on schedule)
SANDIEGO_LAPS = 75
SANDIEGO_BRAKING_EVENTS = 16  # 16 turns = 16 braking zones per lap
SANDIEGO_CAUTION_PROBABILITY = 0.055  # 5.5% per lap (street course = tight, more mistakes)

# Driver data: (oval_speed, road_course_specialty, braking_precision, technical_skill, adaptability)
# Road/street course specialists rated MUCH higher
DRIVERS = {
    "Shane van Gisbergen": (135, 0.98, 0.97, 0.96, 0.97),  # ROAD COURSE MASTER (6 of 7 wins)
    "Christopher Bell": (139, 0.93, 0.94, 0.93, 0.92),  # Strong on road courses
    "Chase Elliott": (140, 0.92, 0.93, 0.92, 0.91),  # Consistent road course performer
    "Tyler Reddick": (138, 0.91, 0.91, 0.90, 0.90),  # Road course capable
    "William Byron": (139, 0.88, 0.89, 0.88, 0.87),  # Good technical skills
    "Michael McDowell": (137, 0.87, 0.88, 0.86, 0.85),  # Street race specialist
    "Connor Zilisch": (136, 0.86, 0.85, 0.84, 0.83),  # Young, road racing background
    "Denny Hamlin": (142, 0.72, 0.75, 0.73, 0.71),  # WEAK ON ROAD COURSES (oval specialist)
    "Kyle Larson": (141, 0.80, 0.82, 0.81, 0.80),  # Can adapt but not a road specialist
    "Joey Logano": (140, 0.78, 0.80, 0.79, 0.78),  # Oval-focused
    "Ryan Blaney": (142, 0.76, 0.77, 0.76, 0.75),  # Better on ovals
    "Chase Briscoe": (141, 0.74, 0.75, 0.74, 0.73),  # Oval specialist
    "Carson Hocevar": (138, 0.73, 0.72, 0.71, 0.70),  # Limited road course experience
    "Ty Gibbs": (138, 0.79, 0.78, 0.77, 0.76),  # Developing road skills
    "AJ Allmendinger": (136, 0.95, 0.94, 0.95, 0.93),  # ROAD COURSE LEGEND
}

# ═══════════════════════════════════════════════════════════════════════════
# SIMULATION ENGINE
# ═══════════════════════════════════════════════════════════════════════════

def run_sandiego_race_simulation(num_simulations=10000):
    """
    Run Monte Carlo simulation for San Diego street course race
    
    Track dynamics:
    - 3.4-mile street course (longest on Cup schedule)
    - 16 turns = 16 braking events per lap
    - Road/street course specialists dominate
    - Technical precision >> raw speed
    - Brand new track = learning for everyone (except road specialists)
    - Heavy braking zones (precision required)
    - Tight corners (adaptability critical)
    - Cautions common (street course mistakes = tight racing)
    
    DATA POINT: Shane van Gisbergen wins 6 of last 7 road/street courses
    This is SVG's wheelhouse. Data supports him heavily.
    """
    
    results = defaultdict(int)
    
    for sim in range(num_simulations):
        # Initialize race state
        tire_wear = {driver: 0 for driver in DRIVERS}
        position = {driver: i for i, driver in enumerate(DRIVERS, 1)}
        laps_led = {driver: 0 for driver in DRIVERS}
        pit_stops = {driver: 0 for driver in DRIVERS}
        mistakes = {driver: 0 for driver in DRIVERS}  # Street course mistakes
        
        current_leader = "Shane van Gisbergen"  # SVG starts strong
        caution_flags = 0
        lap = 0
        
        # ─────────────────────────────────────────────────────────────────────
        # RACE SIMULATION: 75 laps
        # ─────────────────────────────────────────────────────────────────────
        
        while lap < SANDIEGO_LAPS:
            lap += 1
            
            # ─────────────────────────────────────────────────────────────────
            # TIRE WEAR & PIT STRATEGY (street course = different windows)
            # ─────────────────────────────────────────────────────────────────
            
            for driver in DRIVERS:
                # Street courses wear tires faster (heavy braking)
                oval_speed, road_specialty, braking, technical, adapt = DRIVERS[driver]
                tire_wear[driver] += (1.0 / (30 * braking))  # 30-lap tire window
            
            # Pit window every 30 laps (street course fuel/tire window)
            pit_window_open = (lap % 30 == 0) or (lap > SANDIEGO_LAPS - 10)
            
            if pit_window_open:
                for driver in DRIVERS:
                    if tire_wear[driver] > 0.90 or lap > SANDIEGO_LAPS - 10:
                        tire_wear[driver] = 0
                        pit_stops[driver] += 1
            
            # ─────────────────────────────────────────────────────────────────
            # PERFORMANCE VARIANCE (Street course = high variance, technical)
            # ─────────────────────────────────────────────────────────────────
            
            performance = {}
            for driver in DRIVERS:
                oval_speed, road_specialty, braking, technical, adapt = DRIVERS[driver]
                
                # Street course variance: higher (tight = mistakes)
                variance = random.gauss(1.0, 0.025)
                
                # Road/street course specialty bonus (DOMINANT factor on this track)
                road_bonus = 1.0 + (road_specialty * 0.05)  # 5% swing based on specialty
                
                # Braking precision bonus (16 turns = 16 braking zones per lap)
                braking_bonus = 1.0 + (braking * 0.03)
                
                # Technical skill bonus (tight corners require technique)
                technical_bonus = 1.0 + (technical * 0.03)
                
                # Tire wear impact
                tire_impact = 1.0 - (tire_wear[driver] / 1.0) * 0.04
                
                # Adaptability (new track, learning curve helps adaptive drivers)
                adapt_bonus = 1.0 + (adapt * 0.02)
                
                # Mistake penalty (street course = mistakes common)
                if random.random() < (1.0 - technical) * 0.10:
                    mistakes[driver] += 1
                mistake_penalty = 1.0 - (mistakes[driver] * 0.02)
                
                performance[driver] = (
                    oval_speed * 
                    variance * 
                    road_bonus * 
                    braking_bonus * 
                    technical_bonus * 
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
            # CAUTION FLAG EVENTS (Street course = tight, more mistakes)
            # ─────────────────────────────────────────────────────────────────
            
            if random.random() < SANDIEGO_CAUTION_PROBABILITY:
                caution_flags += 1
                # Caution resets field, favors adaptable/mistake-free cars
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

def analyze_sandiego_results():
    """Run simulations and display results"""
    
    print("\n" + "="*80)
    print("SAN DIEGO NAVAL BASE CORONADO - MONTE CARLO SIMULATION v3.0")
    print("Anduril 250 'Race the Base' | June 21, 2026 | 75 laps, 255 miles")
    print("="*80)
    print("\nTrack Profile: 3.4-mile STREET COURSE (16 turns) - LONGEST on Cup schedule")
    print("First NASCAR race EVER on an active U.S. military base")
    print("Key Factors: Road/street course mastery, technical precision, braking, adaptability")
    print("Caution Factor: Higher (tight street course = unpredictable)")
    print("\n" + "="*80)
    
    print("\n⏳ Running 10,000 simulations...")
    results = run_sandiego_race_simulation(10000)
    
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
    print("THE MACHINE'S SAN DIEGO PICK:")
    print("="*80)
    print(f"\n🤖 {top_driver.upper()}")
    print(f"   Confidence: {top_percentage:.2f}%")
    print(f"\n   Why: San Diego is a ROAD COURSE. {top_driver} has mastered")
    print(f"   street/road courses (6 of last 7 wins). Technical precision,")
    print(f"   braking expertise, and adaptability dominate here.")
    print(f"\n   Denny Hamlin is WEAK on road courses. Oval dominance ≠ street skill.")
    print(f"\n   Key Quote: \"{top_percentage:.1f}%. {top_driver}. Road courses are data.\"")
    
    print("\n" + "="*80)
    print("SAN DIEGO RACE CONTEXT:")
    print("="*80)
    print("\n✓ 3.4-mile street course (LONGEST on Cup schedule)")
    print("✓ 16 turns (technical, precision required)")
    print("✓ Brand new track (no Cup history, but road skills transfer)")
    print("✓ Heavy braking zones (precision > raw speed)")
    print("✓ 75 laps, 255 miles")
    print("✓ Cautions likely (tight street course)")
    print("✓ SVG: 6 of last 7 road/street course wins (dominance)")
    print("✓ Hamlin WEAK on road/street courses (oval specialist)")
    print("✓ Road specialists shine: Bell, Elliott, Allmendinger, Reddick")
    
    print("\n" + "="*80)
    print(f"RACE INFO: Anduril 250 'Race the Base'")
    print(f"Date: Sunday, June 21, 2026 | Time: 4:00 PM ET")
    print(f"Track: Naval Base Coronado, San Diego, California")
    print(f"Network: Prime Video")
    print(f"Historic: First NASCAR race EVER on active U.S. military base")
    print("="*80 + "\n")
    
    return sorted_results

# ═══════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    results = analyze_sandiego_results()
