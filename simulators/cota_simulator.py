"""
Circuit of the Americas (COTA) Monte Carlo Simulator
DuraMAX Texas Grand Prix - March 1, 2026

ROAD COURSE RACING - Completely different from ovals
3.41 miles, 20 turns, technical road racing
"""

import numpy as np
import pandas as pd
from dataclasses import dataclass
from typing import List, Dict
import random

@dataclass
class COTADriver:
    """Driver attributes for road course racing"""
    name: str
    car_num: int
    team: str
    manufacturer: str
    tier: str
    
    # Road course-specific attributes (0-10 scale)
    road_course_skill: float  # Overall road racing ability
    braking_zones: float      # Ability to brake late and hard
    corner_entry: float       # Turn-in skill
    corner_exit: float        # Acceleration out of corners
    passing_ability: float    # Wheel-to-wheel road racing
    tire_preservation: float  # Tire management on road course
    fuel_strategy: float      # Fuel saving ability
    recovery: float           # Ability to recover from mistakes
    aggression: float
    clutch_factor: float
    recent_form: float = 5.0
    
    # State
    running: bool = True
    laps_led: int = 0
    incidents: int = 0


# COTA 2026 Driver Profiles - Road Course Specialists
COTA_DRIVERS = [
    # ROAD COURSE ACES
    COTADriver("AJ Allmendinger", 16, "Kaulig", "Chevrolet", "specialist",
           road_course_skill=9.5, braking_zones=9.0, corner_entry=9.5, corner_exit=9.0,
           passing_ability=9.5, tire_preservation=8.5, fuel_strategy=8.5, recovery=9.0,
           aggression=8.0, clutch_factor=9.0, recent_form=5.0),
    
    COTADriver("Shane van Gisbergen", 97, "Trackhouse", "Chevrolet", "specialist",
           road_course_skill=9.5, braking_zones=9.5, corner_entry=9.5, corner_exit=9.5,
           passing_ability=9.0, tire_preservation=9.0, fuel_strategy=8.0, recovery=8.5,
           aggression=8.5, clutch_factor=8.5, recent_form=6.5),  # Supercars legend
    
    # ELITE - Strong road racers
    COTADriver("Tyler Reddick", 45, "23XI", "Toyota", "elite",
           road_course_skill=9.0, braking_zones=8.5, corner_entry=9.0, corner_exit=8.5,
           passing_ability=8.5, tire_preservation=8.5, fuel_strategy=8.0, recovery=8.5,
           aggression=8.0, clutch_factor=8.5, recent_form=9.5),  # Daytona winner + 2023 COTA winner
    
    COTADriver("Christopher Bell", 20, "Joe Gibbs", "Toyota", "elite",
           road_course_skill=9.0, braking_zones=9.0, corner_entry=8.5, corner_exit=8.5,
           passing_ability=8.5, tire_preservation=8.5, fuel_strategy=8.5, recovery=8.0,
           aggression=7.5, clutch_factor=8.5, recent_form=6.0),  # 2025 COTA winner
    
    COTADriver("William Byron", 24, "Hendrick", "Chevrolet", "elite",
           road_course_skill=8.5, braking_zones=8.5, corner_entry=8.5, corner_exit=8.5,
           passing_ability=8.0, tire_preservation=8.5, fuel_strategy=8.0, recovery=8.0,
           aggression=7.0, clutch_factor=8.5, recent_form=4.5),  # 2024 COTA winner
    
    COTADriver("Kyle Larson", 5, "Hendrick", "Chevrolet", "elite",
           road_course_skill=8.5, braking_zones=8.0, corner_entry=8.5, corner_exit=9.0,
           passing_ability=8.5, tire_preservation=8.0, fuel_strategy=7.5, recovery=8.5,
           aggression=8.0, clutch_factor=9.0, recent_form=6.0),
    
    COTADriver("Ross Chastain", 1, "Trackhouse", "Chevrolet", "strong",
           road_course_skill=8.5, braking_zones=8.0, corner_entry=7.5, corner_exit=8.5,
           passing_ability=9.5, tire_preservation=7.0, fuel_strategy=7.0, recovery=7.5,
           aggression=10.0, clutch_factor=8.0, recent_form=5.0),  # 2022 COTA winner, very aggressive
    
    COTADriver("Chase Elliott", 9, "Hendrick", "Chevrolet", "elite",
           road_course_skill=8.0, braking_zones=8.0, corner_entry=8.0, corner_exit=8.0,
           passing_ability=7.5, tire_preservation=8.5, fuel_strategy=8.5, recovery=9.0,
           aggression=6.5, clutch_factor=8.5, recent_form=5.5),
    
    # STRONG ROAD RACERS
    COTADriver("Alex Bowman", 48, "Hendrick", "Chevrolet", "strong",
           road_course_skill=7.5, braking_zones=7.5, corner_entry=7.5, corner_exit=7.5,
           passing_ability=7.0, tire_preservation=8.0, fuel_strategy=7.5, recovery=8.0,
           aggression=6.0, clutch_factor=7.0, recent_form=5.0),  # Top-10 all 4 COTA races
    
    COTADriver("Chris Buescher", 17, "RFK", "Ford", "strong",
           road_course_skill=7.5, braking_zones=7.5, corner_entry=7.5, corner_exit=7.0,
           passing_ability=7.5, tire_preservation=8.0, fuel_strategy=8.5, recovery=7.5,
           aggression=6.5, clutch_factor=7.5, recent_form=5.5),
    
    COTADriver("Kyle Busch", 8, "RCR", "Chevrolet", "strong",
           road_course_skill=8.0, braking_zones=8.0, corner_entry=7.5, corner_exit=8.0,
           passing_ability=8.5, tire_preservation=7.5, fuel_strategy=7.5, recovery=7.5,
           aggression=8.0, clutch_factor=8.0, recent_form=5.0),
    
    COTADriver("Ryan Blaney", 12, "Penske", "Ford", "strong",
           road_course_skill=7.5, braking_zones=7.5, corner_entry=7.5, corner_exit=7.5,
           passing_ability=7.5, tire_preservation=7.5, fuel_strategy=7.5, recovery=7.5,
           aggression=7.5, clutch_factor=9.0, recent_form=6.0),
    
    COTADriver("Joey Logano", 22, "Penske", "Ford", "strong",
           road_course_skill=7.5, braking_zones=7.5, corner_entry=7.0, corner_exit=7.5,
           passing_ability=8.0, tire_preservation=7.0, fuel_strategy=7.5, recovery=7.0,
           aggression=8.5, clutch_factor=9.5, recent_form=4.5),
    
    COTADriver("Denny Hamlin", 11, "Joe Gibbs", "Toyota", "elite",
           road_course_skill=7.0, braking_zones=7.0, corner_entry=7.0, corner_exit=7.0,
           passing_ability=7.5, tire_preservation=8.0, fuel_strategy=8.5, recovery=7.5,
           aggression=8.5, clutch_factor=9.5, recent_form=6.0),  # Not a road course ace
    
    # Mid-pack road racers
    COTADriver("Daniel Suarez", 7, "Spire", "Chevrolet", "mid",
           road_course_skill=7.0, braking_zones=7.0, corner_entry=7.0, corner_exit=7.0,
           passing_ability=7.0, tire_preservation=7.0, fuel_strategy=7.0, recovery=7.0,
           aggression=7.0, clutch_factor=7.5, recent_form=5.0),
    
    COTADriver("Connor Zilisch", 88, "Trackhouse", "Chevrolet", "mid",
           road_course_skill=8.0, braking_zones=8.0, corner_entry=8.5, corner_exit=8.0,
           passing_ability=7.0, tire_preservation=6.5, fuel_strategy=6.0, recovery=6.5,
           aggression=8.5, clutch_factor=7.0, recent_form=5.0),  # Rookie road course ace
]


class COTARaceSimulator:
    """COTA road course simulator - different chaos than ovals"""
    
    def __init__(self, drivers: List[COTADriver]):
        self.drivers = [self._copy_driver(d) for d in drivers]
        self.total_laps = 68  # ~230 miles
        self.current_lap = 0
        self.caution_laps = []
        self.turn_1_carnage = False  # Lap 1 Turn 1 incident common
        self.stage_breaks = [15, 30]  # 2 stages
        
    def _copy_driver(self, driver: COTADriver) -> COTADriver:
        """Create fresh driver instance"""
        return COTADriver(
            name=driver.name, car_num=driver.car_num, team=driver.team,
            manufacturer=driver.manufacturer, tier=driver.tier,
            road_course_skill=driver.road_course_skill, braking_zones=driver.braking_zones,
            corner_entry=driver.corner_entry, corner_exit=driver.corner_exit,
            passing_ability=driver.passing_ability, tire_preservation=driver.tire_preservation,
            fuel_strategy=driver.fuel_strategy, recovery=driver.recovery,
            aggression=driver.aggression, clutch_factor=driver.clutch_factor,
            recent_form=driver.recent_form,
            running=True, laps_led=0, incidents=0
        )
    
    def simulate_turn_1_lap_1(self):
        """Lap 1 Turn 1 chaos - common at COTA"""
        if self.current_lap == 1 and random.random() < 0.35:  # 35% chance
            self.turn_1_carnage = True
            
            # 2-5 cars involved (smaller than oval crashes)
            incident_size = random.randint(2, 5)
            running_drivers = [d for d in self.drivers if d.running]
            
            # Aggressive drivers more likely to be involved
            incident_weights = [d.aggression / 30.0 for d in running_drivers]
            
            victims = random.choices(running_drivers, weights=incident_weights,
                                    k=min(incident_size, len(running_drivers)))
            
            for victim in victims:
                # Road course = damage not always terminal
                if random.random() < 0.6:  # 60% still out
                    victim.running = False
                else:
                    victim.incidents += 1  # Damaged but running
            
            self.caution_laps.append(1)
    
    def simulate_racing_incident(self, lap: int):
        """Road course incidents - contact, off-track, spins"""
        if lap > 5 and random.random() < 0.02:  # 2% per lap
            running_drivers = [d for d in self.drivers if d.running]
            if running_drivers:
                # 1-2 car incidents typical
                incident_size = random.randint(1, 2)
                
                # Weight by aggression - recovery skill
                incident_weights = []
                for d in running_drivers:
                    weight = (d.aggression / 20.0) - (d.recovery / 30.0)
                    incident_weights.append(max(0.01, weight))
                
                victims = random.choices(running_drivers, weights=incident_weights,
                                        k=min(incident_size, len(running_drivers)))
                
                for victim in victims:
                    if random.random() < 0.5:  # 50% terminal
                        victim.running = False
                    else:
                        victim.incidents += 1
                
                self.caution_laps.append(lap)
    
    def determine_winner(self) -> COTADriver:
        """Road course winner determination"""
        running_drivers = [d for d in self.drivers if d.running]
        
        if not running_drivers:
            return random.choice(self.drivers)
        
        win_scores = []
        for driver in running_drivers:
            # Road course skill dominates
            score = (
                driver.road_course_skill * 0.30 +
                driver.braking_zones * 0.15 +
                driver.corner_exit * 0.15 +
                driver.passing_ability * 0.10 +
                driver.tire_preservation * 0.10 +
                driver.clutch_factor * 0.10 +
                driver.recent_form * 0.10
            )
            
            # Penalty for incidents (damage hurts)
            score *= (1.0 - (driver.incidents * 0.15))
            
            # Road course specialists get boost
            if driver.tier == "specialist":
                score *= 1.30
            
            # Elite teams still matter
            if driver.team in ["Hendrick", "Joe Gibbs", "Trackhouse"]:
                score *= 1.10
            
            win_scores.append(max(0.1, score))
        
        total_score = sum(win_scores)
        win_probs = [s / total_score for s in win_scores]
        
        winner = np.random.choice(running_drivers, p=win_probs)
        return winner
    
    def simulate_race(self) -> Dict:
        """Run COTA race simulation"""
        
        for lap in range(1, self.total_laps + 1):
            self.current_lap = lap
            
            # Lap 1 Turn 1 check
            if lap == 1:
                self.simulate_turn_1_lap_1()
            
            # Racing incidents
            if lap > 1:
                self.simulate_racing_incident(lap)
            
            # Stage breaks (no incidents)
            if lap in self.stage_breaks:
                self.caution_laps.append(lap)
        
        winner = self.determine_winner()
        running_at_finish = len([d for d in self.drivers if d.running])
        
        return {
            'winner': winner.name,
            'manufacturer': winner.manufacturer,
            'team': winner.team,
            'tier': winner.tier,
            'turn_1_carnage': self.turn_1_carnage,
            'total_cautions': len(self.caution_laps),
            'running_at_finish': running_at_finish,
            'attrition_rate': (len(self.drivers) - running_at_finish) / len(self.drivers)
        }


def run_cota_monte_carlo(n_simulations: int = 10000) -> pd.DataFrame:
    """Run COTA Monte Carlo simulation"""
    
    print(f"\n{'='*70}")
    print(f"COTA ROAD COURSE SIMULATOR - {n_simulations:,} SIMULATIONS")
    print(f"DuraMAX Texas Grand Prix - March 1, 2026")
    print(f"{'='*70}")
    print("3.41 miles, 20 turns - Road racing chaos\n")
    
    results = []
    milestones = [int(n_simulations * p) for p in [0.25, 0.5, 0.75, 1.0]]
    
    for i in range(n_simulations):
        sim = COTARaceSimulator(COTA_DRIVERS)
        result = sim.simulate_race()
        results.append(result)
        
        if (i + 1) in milestones:
            pct = ((i + 1) / n_simulations) * 100
            print(f"Progress: {i+1:,}/{n_simulations:,} ({pct:.0f}%)")
    
    df = pd.DataFrame(results)
    return df


def analyze_cota_results(df: pd.DataFrame):
    """Analyze COTA results"""
    
    print(f"\n{'='*70}")
    print("COTA PREDICTIONS")
    print(f"{'='*70}\n")
    
    win_counts = df['winner'].value_counts()
    total_sims = len(df)
    
    print("WIN PROBABILITIES (Top 15):")
    print(f"{'Driver':<30} {'Wins':>8} {'Win %':>8}")
    print("-" * 70)
    for driver, wins in win_counts.head(15).items():
        win_pct = (wins / total_sims) * 100
        print(f"{driver:<30} {wins:>8,} {win_pct:>7.2f}%")
    
    # Road course chaos stats
    print(f"\n{'='*70}")
    print("ROAD COURSE CHAOS STATISTICS")
    print(f"{'='*70}")
    
    turn1_rate = df['turn_1_carnage'].sum() / total_sims
    avg_cautions = df['total_cautions'].mean()
    avg_attrition = df['attrition_rate'].mean()
    
    print(f"Turn 1 Lap 1 Incident: {turn1_rate:.1%}")
    print(f"Average Cautions: {avg_cautions:.1f}")
    print(f"Average Attrition Rate: {avg_attrition:.1%} DNF")
    print(f"\nRoad course = Lower attrition than ovals")
    
    # Manufacturer
    print(f"\n{'='*70}")
    print("MANUFACTURER PERFORMANCE")
    print(f"{'='*70}")
    
    mfg_wins = df['manufacturer'].value_counts()
    for mfg, wins in mfg_wins.items():
        print(f"{mfg}: {wins:,} wins ({wins/total_sims:.1%})")
    
    return df


if __name__ == "__main__":
    results_df = run_cota_monte_carlo(n_simulations=10000)
    analyze_cota_results(results_df)
    
    results_df.to_csv('/home/claude/cota_simulation_results.csv', index=False)
    print(f"\n{'='*70}")
    print("COTA results saved to: cota_simulation_results.csv")
    print(f"{'='*70}\n")
