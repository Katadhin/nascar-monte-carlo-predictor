"""
Atlanta Motor Speedway Monte Carlo Simulator - RECALIBRATED
Autotrader 400 - February 22, 2026

IMPROVEMENTS:
- Reduced attrition (88% → ~60-65%)
- Scenario branching (clean vs chaos start)
- Recent form integration (Daytona winner boost)
- More realistic crash frequencies
"""

import numpy as np
import pandas as pd
from dataclasses import dataclass
from typing import List, Dict
import random
from collections import defaultdict

@dataclass
class AtlantaDriver:
    """Driver attributes tuned for Atlanta's unique characteristics"""
    name: str
    car_num: int
    team: str
    manufacturer: str
    tier: str
    
    # Atlanta-specific attributes (0-10 scale)
    base_speed: float
    tire_management: float
    drafting_iq: float
    restart_skill: float
    aggression: float
    chaos_survival: float
    long_run_speed: float
    short_run_speed: float
    clutch_factor: float
    recent_form: float = 5.0  # NEW: Recent performance boost
    
    # State
    running: bool = True
    laps_led: int = 0
    involved_in_crash: bool = False
    pit_strategy: str = "normal"


# Atlanta 2026 Driver Profiles - RECALIBRATED
ATLANTA_DRIVERS = [
    # ELITE - Hendrick Chevrolet
    AtlantaDriver("Kyle Larson", 5, "Hendrick", "Chevrolet", "elite",
                  base_speed=9.5, tire_management=8.5, drafting_iq=8.0, restart_skill=9.0,
                  aggression=8.0, chaos_survival=6.5, long_run_speed=9.5, short_run_speed=9.0, 
                  clutch_factor=9.0, recent_form=6.0),
    
    AtlantaDriver("Chase Elliott", 9, "Hendrick", "Chevrolet", "elite",
                  base_speed=9.0, tire_management=9.0, drafting_iq=8.5, restart_skill=8.5,
                  aggression=6.5, chaos_survival=7.5, long_run_speed=9.0, short_run_speed=8.5, 
                  clutch_factor=8.5, recent_form=5.5),
    
    AtlantaDriver("William Byron", 24, "Hendrick", "Chevrolet", "elite",
                  base_speed=9.0, tire_management=8.0, drafting_iq=8.0, restart_skill=8.5,
                  aggression=7.0, chaos_survival=7.0, long_run_speed=8.5, short_run_speed=9.0, 
                  clutch_factor=8.5, recent_form=4.5),  # DNF at Daytona
    
    AtlantaDriver("Alex Bowman", 48, "Hendrick", "Chevrolet", "strong",
                  base_speed=8.0, tire_management=7.5, drafting_iq=7.5, restart_skill=7.0,
                  aggression=6.0, chaos_survival=8.0, long_run_speed=7.5, short_run_speed=7.5, 
                  clutch_factor=7.0, recent_form=5.0),
    
    # ELITE - Joe Gibbs Toyota
    AtlantaDriver("Denny Hamlin", 11, "Joe Gibbs", "Toyota", "elite",
                  base_speed=9.0, tire_management=9.0, drafting_iq=9.5, restart_skill=9.5,
                  aggression=8.5, chaos_survival=8.5, long_run_speed=8.5, short_run_speed=9.0, 
                  clutch_factor=9.5, recent_form=6.0),
    
    AtlantaDriver("Christopher Bell", 20, "Joe Gibbs", "Toyota", "elite",
                  base_speed=8.5, tire_management=8.0, drafting_iq=7.5, restart_skill=8.0,
                  aggression=7.5, chaos_survival=7.0, long_run_speed=8.5, short_run_speed=8.0, 
                  clutch_factor=8.0, recent_form=5.0),
    
    AtlantaDriver("Ty Gibbs", 54, "Joe Gibbs", "Toyota", "strong",
                  base_speed=7.5, tire_management=7.0, drafting_iq=6.5, restart_skill=7.0,
                  aggression=7.0, chaos_survival=6.0, long_run_speed=7.0, short_run_speed=7.5, 
                  clutch_factor=6.5, recent_form=5.0),
    
    AtlantaDriver("Chase Briscoe", 19, "Joe Gibbs", "Toyota", "strong",
                  base_speed=7.5, tire_management=7.5, drafting_iq=7.0, restart_skill=7.5,
                  aggression=7.5, chaos_survival=7.0, long_run_speed=7.5, short_run_speed=7.5, 
                  clutch_factor=7.5, recent_form=5.5),
    
    # ELITE - 23XI Toyota
    AtlantaDriver("Tyler Reddick", 45, "23XI", "Toyota", "elite",
                  base_speed=8.5, tire_management=8.5, drafting_iq=8.5, restart_skill=8.5,
                  aggression=8.0, chaos_survival=7.5, long_run_speed=8.5, short_run_speed=8.5, 
                  clutch_factor=8.5, recent_form=9.5),  # DAYTONA WINNER BOOST
    
    AtlantaDriver("Bubba Wallace", 23, "23XI", "Toyota", "strong",
                  base_speed=7.5, tire_management=7.0, drafting_iq=7.5, restart_skill=7.5,
                  aggression=7.0, chaos_survival=7.0, long_run_speed=7.0, short_run_speed=7.5, 
                  clutch_factor=7.0, recent_form=5.5),
    
    # ELITE - Penske Ford
    AtlantaDriver("Ryan Blaney", 12, "Penske", "Ford", "elite",
                  base_speed=8.5, tire_management=8.5, drafting_iq=9.0, restart_skill=9.0,
                  aggression=7.5, chaos_survival=8.5, long_run_speed=8.5, short_run_speed=9.0, 
                  clutch_factor=9.0, recent_form=6.0),
    
    AtlantaDriver("Joey Logano", 22, "Penske", "Ford", "elite",
                  base_speed=8.5, tire_management=8.0, drafting_iq=9.5, restart_skill=9.5,
                  aggression=8.5, chaos_survival=8.0, long_run_speed=8.0, short_run_speed=9.0, 
                  clutch_factor=9.5, recent_form=4.5),  # Daytona crash
    
    AtlantaDriver("Austin Cindric", 2, "Penske", "Ford", "strong",
                  base_speed=7.5, tire_management=7.5, drafting_iq=8.0, restart_skill=8.0,
                  aggression=7.0, chaos_survival=7.5, long_run_speed=7.5, short_run_speed=8.0, 
                  clutch_factor=8.5, recent_form=5.5),
    
    # More key drivers
    AtlantaDriver("Brad Keselowski", 6, "RFK", "Ford", "strong",
                  base_speed=8.0, tire_management=8.5, drafting_iq=8.5, restart_skill=8.0,
                  aggression=7.5, chaos_survival=7.5, long_run_speed=8.0, short_run_speed=8.0, 
                  clutch_factor=8.0, recent_form=6.5),
    
    AtlantaDriver("Chris Buescher", 17, "RFK", "Ford", "strong",
                  base_speed=7.5, tire_management=8.0, drafting_iq=7.5, restart_skill=7.5,
                  aggression=6.5, chaos_survival=7.5, long_run_speed=7.5, short_run_speed=7.0, 
                  clutch_factor=7.5, recent_form=5.5),
    
    AtlantaDriver("Ross Chastain", 1, "Trackhouse", "Chevrolet", "strong",
                  base_speed=8.0, tire_management=6.5, drafting_iq=6.5, restart_skill=7.5,
                  aggression=10.0, chaos_survival=4.0, long_run_speed=7.5, short_run_speed=8.0, 
                  clutch_factor=7.5, recent_form=5.0),
    
    AtlantaDriver("Daniel Suarez", 7, "Spire", "Chevrolet", "strong",
                  base_speed=7.5, tire_management=7.5, drafting_iq=7.5, restart_skill=8.0,
                  aggression=7.0, chaos_survival=7.0, long_run_speed=7.5, short_run_speed=7.5, 
                  clutch_factor=8.5, recent_form=5.0),  # 2024 Atlanta winner
    
    AtlantaDriver("Kyle Busch", 8, "RCR", "Chevrolet", "strong",
                  base_speed=8.0, tire_management=8.5, drafting_iq=7.5, restart_skill=8.5,
                  aggression=8.0, chaos_survival=6.5, long_run_speed=8.0, short_run_speed=8.0, 
                  clutch_factor=8.0, recent_form=5.0),
    
    AtlantaDriver("Ricky Stenhouse Jr.", 47, "HYAK", "Chevrolet", "strong",
                  base_speed=7.0, tire_management=7.0, drafting_iq=8.5, restart_skill=8.0,
                  aggression=9.0, chaos_survival=7.5, long_run_speed=7.0, short_run_speed=7.5, 
                  clutch_factor=8.5, recent_form=7.5),  # Daytona P2!
    
    AtlantaDriver("Michael McDowell", 71, "Spire", "Chevrolet", "mid",
                  base_speed=6.5, tire_management=7.5, drafting_iq=8.5, restart_skill=7.5,
                  aggression=7.5, chaos_survival=8.5, long_run_speed=6.5, short_run_speed=7.0, 
                  clutch_factor=8.0, recent_form=5.0),
]


class AtlantaRaceSimulator:
    """RECALIBRATED Atlanta simulator with scenario tracking"""
    
    def __init__(self, drivers: List[AtlantaDriver]):
        self.drivers = [self._copy_driver(d) for d in drivers]
        self.total_laps = 260
        self.current_lap = 0
        self.caution_laps = []
        self.early_carnage = False
        self.early_carnage_lap = None
        self.green_white_checkered = False
        
    def _copy_driver(self, driver: AtlantaDriver) -> AtlantaDriver:
        """Create fresh driver instance"""
        return AtlantaDriver(
            name=driver.name, car_num=driver.car_num, team=driver.team,
            manufacturer=driver.manufacturer, tier=driver.tier,
            base_speed=driver.base_speed, tire_management=driver.tire_management,
            drafting_iq=driver.drafting_iq, restart_skill=driver.restart_skill,
            aggression=driver.aggression, chaos_survival=driver.chaos_survival,
            long_run_speed=driver.long_run_speed, short_run_speed=driver.short_run_speed,
            clutch_factor=driver.clutch_factor, recent_form=driver.recent_form,
            running=True, laps_led=0, involved_in_crash=False,
            pit_strategy=random.choice(["normal", "normal", "normal", "aggressive"])
        )
    
    def simulate_early_carnage(self, lap: int):
        """RECALIBRATED: Reduced early crash probability and size"""
        if not self.early_carnage and 1 <= lap <= 5:
            base_prob = 0.18 if lap == 2 else 0.06  # Reduced from 0.25/0.10
            
            if random.random() < base_prob:
                self.early_carnage = True
                self.early_carnage_lap = lap
                
                # 6-12 cars involved (reduced from 10-16)
                crash_size = random.randint(6, 12)
                running_drivers = [d for d in self.drivers if d.running]
                
                if len(running_drivers) < crash_size:
                    crash_size = len(running_drivers) - 12  # More survivors
                
                # Weighted by chaos_survival
                survival_weights = [1.0 / (d.chaos_survival + 1) for d in running_drivers]
                for i, driver in enumerate(running_drivers):
                    survival_weights[i] *= (driver.aggression / 10.0 + 0.5)
                
                total_weight = sum(survival_weights)
                survival_probs = [w / total_weight for w in survival_weights]
                
                crash_victims = np.random.choice(
                    running_drivers, size=crash_size, replace=False, p=survival_probs
                )
                
                for victim in crash_victims:
                    victim.running = False
                    victim.involved_in_crash = True
                
                self.caution_laps.append(lap)
                return len(crash_victims)
        
        return 0
    
    def simulate_mid_race_incidents(self, lap: int):
        """RECALIBRATED: Reduced incident frequency"""
        if random.random() < 0.015:  # Reduced from 0.025
            running_drivers = [d for d in self.drivers if d.running]
            if running_drivers:
                # 1-3 car incidents (reduced from 2-4)
                incident_size = random.randint(1, 3)
                incident_weights = [d.aggression / 50.0 for d in running_drivers]
                
                victims = random.choices(running_drivers, weights=incident_weights, 
                                        k=min(incident_size, len(running_drivers)))
                for victim in victims:
                    victim.running = False
                
                self.caution_laps.append(lap)
    
    def check_green_white_checkered(self, lap: int):
        """Late caution forces overtime"""
        if lap >= 255 and random.random() < 0.25:
            self.green_white_checkered = True
            self.total_laps = lap + 2
            self.caution_laps.append(lap)
    
    def determine_winner(self) -> AtlantaDriver:
        """Determine race winner with recent form boost"""
        running_drivers = [d for d in self.drivers if d.running]
        
        if not running_drivers:
            return random.choice(self.drivers)
        
        win_scores = []
        for driver in running_drivers:
            # Base calculation
            score = (
                driver.base_speed * 0.18 +
                driver.tire_management * 0.18 +
                driver.drafting_iq * 0.12 +
                driver.restart_skill * 0.18 +
                driver.clutch_factor * 0.22 +
                driver.recent_form * 0.12  # NEW: Recent form matters
            )
            
            # GWC boost restart skill
            if self.green_white_checkered:
                score *= (driver.restart_skill / 8.0 + 0.5)
                score *= (driver.clutch_factor / 8.0 + 0.5)
            
            # Manufacturer teamwork
            if driver.manufacturer == "Chevrolet":
                score *= 1.10
            elif driver.manufacturer == "Toyota":
                score *= 1.05
            
            # Elite teams
            if driver.team in ["Hendrick", "Joe Gibbs", "Penske"]:
                score *= 1.15
            
            win_scores.append(score)
        
        total_score = sum(win_scores)
        win_probs = [s / total_score for s in win_scores]
        
        winner = np.random.choice(running_drivers, p=win_probs)
        return winner
    
    def simulate_race(self) -> Dict:
        """Run complete race simulation"""
        
        for lap in range(1, self.total_laps + 1):
            self.current_lap = lap
            
            # Early carnage
            crash_count = self.simulate_early_carnage(lap)
            
            # Mid-race incidents
            if lap > 10:
                self.simulate_mid_race_incidents(lap)
            
            # Late caution check
            if not self.green_white_checkered:
                self.check_green_white_checkered(lap)
        
        winner = self.determine_winner()
        running_at_finish = len([d for d in self.drivers if d.running])
        
        return {
            'winner': winner.name,
            'manufacturer': winner.manufacturer,
            'team': winner.team,
            'tier': winner.tier,
            'early_carnage': self.early_carnage,
            'early_carnage_lap': self.early_carnage_lap,
            'total_cautions': len(self.caution_laps),
            'green_white_checkered': self.green_white_checkered,
            'running_at_finish': running_at_finish,
            'attrition_rate': (len(self.drivers) - running_at_finish) / len(self.drivers)
        }


def run_atlanta_monte_carlo(n_simulations: int = 10000) -> pd.DataFrame:
    """Run recalibrated Monte Carlo simulation"""
    
    print(f"\n{'='*70}")
    print(f"ATLANTA MONTE CARLO - RECALIBRATED - {n_simulations:,} SIMULATIONS")
    print(f"Autotrader 400 - February 22, 2026")
    print(f"{'='*70}")
    print("IMPROVEMENTS: Reduced attrition, recent form boost, scenario tracking\n")
    
    results = []
    milestones = [int(n_simulations * p) for p in [0.25, 0.5, 0.75, 1.0]]
    
    for i in range(n_simulations):
        sim = AtlantaRaceSimulator(ATLANTA_DRIVERS)
        result = sim.simulate_race()
        results.append(result)
        
        if (i + 1) in milestones:
            pct = ((i + 1) / n_simulations) * 100
            print(f"Progress: {i+1:,}/{n_simulations:,} ({pct:.0f}%)")
    
    df = pd.DataFrame(results)
    return df


def analyze_atlanta_results(df: pd.DataFrame):
    """Analyze recalibrated results with scenario breakdowns"""
    
    print(f"\n{'='*70}")
    print("RECALIBRATED ATLANTA PREDICTIONS")
    print(f"{'='*70}\n")
    
    win_counts = df['winner'].value_counts()
    total_sims = len(df)
    
    print("WIN PROBABILITIES (Top 15):")
    print(f"{'Driver':<25} {'Wins':>8} {'Win %':>8}")
    print("-" * 70)
    for driver, wins in win_counts.head(15).items():
        win_pct = (wins / total_sims) * 100
        print(f"{driver:<25} {wins:>8,} {win_pct:>7.2f}%")
    
    # Chaos stats
    print(f"\n{'='*70}")
    print("CHAOS STATISTICS (RECALIBRATED)")
    print(f"{'='*70}")
    
    early_carnage_rate = df['early_carnage'].sum() / total_sims
    avg_early_lap = df[df['early_carnage']]['early_carnage_lap'].mean() if df['early_carnage'].sum() > 0 else 0
    gwc_rate = df['green_white_checkered'].sum() / total_sims
    avg_cautions = df['total_cautions'].mean()
    avg_attrition = df['attrition_rate'].mean()
    
    print(f"Early Carnage (Laps 1-5): {early_carnage_rate:.1%}")
    print(f"Average Early Crash Lap: {avg_early_lap:.1f}")
    print(f"Green-White-Checkered Rate: {gwc_rate:.1%}")
    print(f"Average Cautions: {avg_cautions:.1f}")
    print(f"Average Attrition Rate: {avg_attrition:.1%} DNF")
    
    # Scenario breakdown
    print(f"\n{'='*70}")
    print("SCENARIO BREAKDOWN")
    print(f"{'='*70}")
    
    clean_start = df[~df['early_carnage']]
    chaos_start = df[df['early_carnage']]
    
    print(f"\nCLEAN START RACES ({len(clean_start):,} / {total_sims:,}):")
    if len(clean_start) > 0:
        clean_winners = clean_start['winner'].value_counts().head(5)
        for driver, wins in clean_winners.items():
            print(f"  {driver}: {wins/len(clean_start):.1%}")
    
    print(f"\nCHAOS START RACES ({len(chaos_start):,} / {total_sims:,}):")
    if len(chaos_start) > 0:
        chaos_winners = chaos_start['winner'].value_counts().head(5)
        for driver, wins in chaos_winners.items():
            print(f"  {driver}: {wins/len(chaos_start):.1%}")
    
    # Manufacturer
    print(f"\n{'='*70}")
    print("MANUFACTURER PERFORMANCE")
    print(f"{'='*70}")
    
    mfg_wins = df['manufacturer'].value_counts()
    for mfg, wins in mfg_wins.items():
        print(f"{mfg}: {wins:,} wins ({wins/total_sims:.1%})")
    
    return df


if __name__ == "__main__":
    results_df = run_atlanta_monte_carlo(n_simulations=10000)
    analyze_atlanta_results(results_df)
    
    results_df.to_csv('/home/claude/atlanta_recalibrated_results.csv', index=False)
    print(f"\n{'='*70}")
    print("Recalibrated results saved to: atlanta_recalibrated_results.csv")
    print(f"{'='*70}\n")
