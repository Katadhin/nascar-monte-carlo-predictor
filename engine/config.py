#!/usr/bin/env python3
"""Configuration loader for tracks and algorithm versions (JSON-based)."""

import json
import os
from typing import Dict, List


class ConfigLoader:
    """Load track and algorithm configurations from JSON files."""
    
    def __init__(self, base_path: str = '.'):
        self.base_path = base_path
        self.tracks_path = os.path.join(base_path, 'engine/data/tracks')
        self.algo_path = os.path.join(base_path, 'engine/data/algorithms')
        self.field_path = os.path.join(base_path, 'engine/data/field')
    
    def load_track_config(self, track_name: str) -> Dict:
        """Load track configuration from JSON."""
        filepath = os.path.join(self.tracks_path, f'{track_name}.json')
        
        if not os.path.exists(filepath):
            raise FileNotFoundError(f"Track config not found: {filepath}")
        
        with open(filepath, 'r') as f:
            return json.load(f)
    
    def load_algorithm_version(self, version: str) -> Dict:
        """Load algorithm version configuration from JSON."""
        filepath = os.path.join(self.algo_path, version, 'parameters.json')
        
        if not os.path.exists(filepath):
            raise FileNotFoundError(f"Algorithm version not found: {filepath}")
        
        with open(filepath, 'r') as f:
            return json.load(f)
    
    def load_field(self, field_name: str = 'default') -> Dict:
        """Load driver field from JSON."""
        filepath = os.path.join(self.field_path, f'{field_name}.json')
        
        if not os.path.exists(filepath):
            raise FileNotFoundError(f"Field not found: {filepath}")
        
        with open(filepath, 'r') as f:
            return json.load(f)
    
    def list_available_tracks(self) -> List[str]:
        """List all available track configurations."""
        if not os.path.exists(self.tracks_path):
            return []
        return sorted([f[:-5] for f in os.listdir(self.tracks_path) if f.endswith('.json')])
    
    def list_available_algorithms(self) -> List[str]:
        """List all available algorithm versions."""
        if not os.path.exists(self.algo_path):
            return []
        versions = []
        for item in os.listdir(self.algo_path):
            if os.path.isdir(os.path.join(self.algo_path, item)):
                versions.append(item)
        return sorted(versions)
