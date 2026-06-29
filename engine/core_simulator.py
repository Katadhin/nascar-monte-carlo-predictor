#!/usr/bin/env python3
"""
NASCAR Monte Carlo Simulator - v3.1 (Real Implementation)

Algorithm v3.1: Post-San Diego learning. Consistency beats dominance on established tracks.
Loads real driver data, real track configs, real algorithm weights from JSON.
"""

import json
import random
import os
from collections import defaultdict
from typing import Dict, List, Tuple, Optional


class CoreSimulator:
    """Real NASCAR simulator with v3.1 algorithm implementation."""
    
    def __init__(self, track_config: Dict, algo_config: Dict, field: Dict = None):
        """
        Initialize simulator with track config, algorithm config, and driver field.
        
        Args:
            track_config: Track parameters (JSON dict)
            algo_config: Algorithm version parameters (JSON dict)
            field: Driver ratings dict. If None, loads default.
        """
        self.track_config = track_config
        self.algo_config = algo_config
        self.results = defaultdict(int)
        
        # Load driver field
        if field is None:
            field = self._load_default_field()
        
        self.drivers = {name: tuple(data.values()[:6]) for name, data in field.items()}
        self.driver_info = field  # Keep full info for notes/adjustments
        
        # Track parameters
        self.laps = track_config.get('laps', 110)
        self.avg_speed = track_config.get('avg_speed_mph', 110)
        self.caution_prob = track_config.get('physics', {}).get('caution_probability', 0.035)
        self.pit_window = track_config.get('physics', {}).get('pit_window_laps', 35)
        self.variance = track_config.get('physics', {}).get('variance_percent', 2.0)
        
        # Algorithm parameters (v3.1)
        self.version = algo_config.get('version', 'v3.1')
        self.seed = algo_config.get('seed', None)
        
        if self.seed:
            random.seed(self.seed)
        
        self.bonuses = algo_config.get('bonuses', {})
        self.penalties = algo_config.get('penalties', {})
        self.track_specific = algo_config.get('track_specific', {})
    
    
    @staticmethod
    def _load_default_field() -> Dict:
        """Load default driver field from JSON."""
        field_path = os.path.join(os.path.dirname(__file__), 'data/field/default.json')
        if os.path.exists(field_path):
            with open(field_path, 'r') as f:
                return json.load(f)['field']
        return {}
    
    
    def run_simulation(self, num_simulations: int = 1000) -> Dict[str, int]:
        """
        Run Monte Carlo simulations.
        
        Args:
            num_simulations: Number of races to simulate
        
        Returns:
            Dict of {driver_name: win_count}
        """
        results = defaultdict(int)
        
        for sim in range(num_simulations):
            # ─────────────────────────────────────────────────────────────────
            # SIMULATE ONE RACE
            # ─────────────────────────────────────────────────────────────────
            
            tire_wear = {driver: 0.0 for driver in self.drivers}
            mistakes = {driver: 0 for driver in self.drivers}
            pit_stops = {driver: 0 for driver in self.drivers}
            
            current_leader = list(self.drivers.keys())[0]
            
            for lap in range(1, self.laps + 1):
                # TIRE WEAR
                for driver in self.drivers:
                    _, _, braking, _, _, _ = self.drivers[driver]
                    tire_degrade = 1.0 / (self.pit_window * braking)
                    tire_wear[driver] += tire_degrade
                
                # PIT STRATEGY
                pit_window_open = (lap % self.pit_window == 0) or (lap > self.laps - 10)
                if pit_window_open:
                    for driver in self.drivers:
                        if tire_wear[driver] > 0.90 or lap > self.laps - 10:
                            tire_wear[driver] = 0.0
                            pit_stops[driver] += 1
                
                # ─────────────────────────────────────────────────────────────────
                # PERFORMANCE CALCULATION (v3.1 REAL MATH)
                # ─────────────────────────────────────────────────────────────────
                
                performance = {}
                
                for driver in self.drivers:
                    base_speed, road_spec, braking, elevation, patience, adapt = self.drivers[driver]
                    
                    # Random variance (different each lap)
                    variance = random.gauss(1.0, self.variance / 100.0)
                    
                    # ─ BONUSES (v3.1) ─
                    
                    # Road specialty bonus (from driver ratings)
                    road_bonus = 1.0 + (road_spec * self.bonuses.get('road_specialty_weight', 0.05))
                    
                    # Braking precision bonus
                    braking_bonus = 1.0 + (braking * self.bonuses.get('braking_precision_weight', 0.03))
                    
                    # Consistency bonus (v3.1 NEW)
                    consistency_bonus = 1.0 + (self.bonuses.get('consistency_weight', 0.04) * 0.5)
                    
                    # Patience bonus (road courses reward smooth)
                    patience_bonus = 1.0 + (patience * self.bonuses.get('patience_weight', 0.02))
                    
                    # Adaptability bonus
                    adapt_bonus = 1.0 + (adapt * self.bonuses.get('adaptability_weight', 0.015))
                    
                    # Tire wear impact
                    tire_impact = 1.0 - (tire_wear[driver] / 1.0) * 0.03
                    
                    # ─ TRACK-SPECIFIC ADJUSTMENTS ─
                    
                    # Local knowledge (v3.1 NEW - Larson at Sonoma)
                    local_bonus = 1.0
                    if driver in self.driver_info:
                        sonoma_adjust = self.driver_info[driver].get('sonoma_specific', {})
                        if 'local_knowledge_bonus' in sonoma_adjust:
                            local_bonus = 1.0 + sonoma_adjust['local_knowledge_bonus']
                    
                    # Recent DNF penalty (v3.1 NEW - SVG at Sonoma after San Diego crash)
                    dnf_penalty = 1.0
                    if driver in self.driver_info:
                        sonoma_adjust = self.driver_info[driver].get('sonoma_specific', {})
                        if 'recent_dnf_penalty' in sonoma_adjust:
                            dnf_penalty = 1.0 - sonoma_adjust['recent_dnf_penalty']
                    
                    # ─ MISTAKES ─
                    if random.random() < (1.0 - braking) * 0.07:
                        mistakes[driver] += 1
                    mistake_penalty = 1.0 - (mistakes[driver] * 0.015)
                    
                    # ─ FINAL PERFORMANCE ─
                    performance[driver] = (
                        base_speed *
                        variance *
                        road_bonus *
                        braking_bonus *
                        consistency_bonus *
                        patience_bonus *
                        adapt_bonus *
                        tire_impact *
                        local_bonus *
                        dnf_penalty *
                        mistake_penalty
                    )
                
                # Rank drivers by performance
                sorted_drivers = sorted(performance.items(), key=lambda x: x[1], reverse=True)
                current_leader = sorted_drivers[0][0]
                
                # Caution flag
                if random.random() < self.caution_prob:
                    pass  # Could implement restart logic
            
            # ─────────────────────────────────────────────────────────────────
            # RACE WINNER
            # ─────────────────────────────────────────────────────────────────
            
            results[current_leader] += 1
        
        self.results = results
        return results
    
    
    def get_top_predictions(self, n: int = 10) -> List[Tuple[str, float]]:
        """Get top N predictions with percentages."""
        if not self.results:
            return []
        
        total = sum(self.results.values())
        top = sorted(self.results.items(), key=lambda x: x[1], reverse=True)[:n]
        return [(driver, (wins / total) * 100) for driver, wins in top]
    
    
    def print_results(self, n: int = 10) -> None:
        """Print top N predictions."""
        if not self.results:
            print("No results. Run simulation first.")
            return
        
        total = sum(self.results.values())
        track = self.track_config.get('track_name', 'Unknown')
        
        print(f"\n{'='*70}")
        print(f"{track} | model {self.version} | {total:,} simulated races | seed {self.seed}")
        print(f"{'='*70}\n")
        print(f"{'#':>2}  {'Driver':<30} {'Win%':>7}  {'Notes'}")
        print("-" * 70)
        
        for rank, (driver, pct) in enumerate(self.get_top_predictions(n=n), 1):
            wins = self.results[driver]
            notes = ""
            
            # Add context notes
            if driver == "Kyle Larson" and "sonoma" in track.lower():
                notes = "← 2x winner, LOCAL, no DNF"
            elif driver == "Shane van Gisbergen" and "sonoma" in track.lower():
                notes = "← defending, but San Diego DNF"
            
            print(f"{rank:2d}  {driver:<30} {pct:>6.1f}%  {notes}")
        
        print(f"{'='*70}\n")
    
    
    def export_results(self, filepath: str) -> None:
        """Export results to JSON."""
        if not self.results:
            return
        
        total = sum(self.results.values())
        output = {
            'track': self.track_config.get('track_name'),
            'algorithm_version': self.version,
            'total_simulations': total,
            'predictions': [
                {
                    'rank': rank,
                    'driver': driver,
                    'wins': self.results[driver],
                    'percentage': (self.results[driver] / total) * 100
                }
                for rank, (driver, _) in enumerate(self.get_top_predictions(n=len(self.results)), 1)
            ]
        }
        
        with open(filepath, 'w') as f:
            json.dump(output, f, indent=2)
        
        print(f"✅ Results exported to {filepath}")


# ═══════════════════════════════════════════════════════════════════════════
# CLI USAGE
# ═══════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    import json
    
    # Load configs from JSON
    with open('engine/data/tracks/sonoma.json') as f:
        track_config = json.load(f)
    
    with open('engine/data/algorithms/v3.1/parameters.json') as f:
        algo_config = json.load(f)
    
    with open('engine/data/field/default.json') as f:
        field = json.load(f)['field']
    
    # Run simulation
    sim = CoreSimulator(track_config, algo_config, field)
    print("Running 1000 simulations...")
    sim.run_simulation(num_simulations=1000)
    sim.print_results(n=10)
    sim.export_results('sonoma_predictions.json')
