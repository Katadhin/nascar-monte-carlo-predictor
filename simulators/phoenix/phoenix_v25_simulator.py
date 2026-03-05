"""
Phoenix Raceway Monte Carlo Simulator v2.5
Straight Talk Wireless 500 - March 8, 2026

MODEL v2.5: HOT HAND + REGRESSION TO MEAN
"""

import numpy as np
import pandas as pd
from dataclasses import dataclass
from typing import List, Dict
import random

@dataclass
class PhoenixDriver:
    name: str
    car_num: int
    team: str
    flat_track_skill: float
    handling: float
    tire_management: float
    clutch_factor: float
    recent_form: float = 5.0
    consecutive_wins: int = 0
    points_position: int = 99
    running: bool = True

# Driver profiles
PHOENIX_DRIVERS = [
    PhoenixDriver("Tyler Reddick", 45, "23XI", 8.5, 8.5, 8.5, 9.0, 10.0, 3, 1),
    PhoenixDriver("Kyle Larson", 5, "Hendrick", 9.5, 9.5, 9.0, 9.5, 6.0, 0, 5),
    PhoenixDriver("Christopher Bell", 20, "Joe Gibbs", 9.0, 9.0, 9.0, 9.0, 5.0, 0, 8),
    PhoenixDriver("William Byron", 24, "Hendrick", 8.5, 8.5, 8.5, 8.5, 4.5, 0, 10),
    PhoenixDriver("Denny Hamlin", 11, "Joe Gibbs", 8.5, 8.5, 8.5, 9.5, 6.0, 0, 4),
    PhoenixDriver("Chase Elliott", 9, "Hendrick", 8.0, 8.0, 8.5, 8.5, 5.0, 0, 12),
    PhoenixDriver("Ryan Blaney", 12, "Penske", 8.5, 8.5, 8.0, 9.5, 5.5, 0, 7),
]

def calculate_streak_regression(consecutive_wins: int) -> float:
    """Regression to mean for win streaks"""
    if consecutive_wins == 0:
        return 1.0
    elif consecutive_wins == 1:
        return 1.25
    elif consecutive_wins == 2:
        return 1.4
    elif consecutive_wins == 3:
        return 1.15  # Regression kicks in
    elif consecutive_wins >= 4:
        return 0.95
    return 1.0

class PhoenixSimulator:
    def __init__(self, drivers: List[PhoenixDriver]):
        self.drivers = drivers
        
    def determine_winner(self) -> PhoenixDriver:
        """v2.5 formula with regression"""
        scores = []
        for driver in self.drivers:
            score = (
                driver.flat_track_skill * 0.20 +
                driver.handling * 0.15 +
                driver.tire_management * 0.15 +
                driver.clutch_factor * 0.20 +
                driver.recent_form * 0.30
            )
            
            # Streak with regression
            if driver.consecutive_wins > 0:
                streak_boost = calculate_streak_regression(driver.consecutive_wins)
                score *= streak_boost
                
                # Pressure penalty for long streaks
                if driver.consecutive_wins >= 3:
                    pressure = 0.88
                    rarity = 0.88
                    score *= pressure * rarity
            
            # Points leader
            if driver.points_position == 1:
                score *= 1.15
                
            scores.append(score)
        
        total = sum(scores)
        probs = [s/total for s in scores]
        return np.random.choice(self.drivers, p=probs)
    
    def simulate(self) -> str:
        winner = self.determine_winner()
        return winner.name

def run_simulation(n=10000):
    results = []
    for _ in range(n):
        sim = PhoenixSimulator(PHOENIX_DRIVERS)
        results.append(sim.simulate())
    
    df = pd.DataFrame({'winner': results})
    print("\nPHOENIX v2.5 PREDICTIONS:")
    print(df['winner'].value_counts(normalize=True).head(10) * 100)
    return df

if __name__ == "__main__":
    run_simulation()
