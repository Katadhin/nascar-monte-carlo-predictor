#!/usr/bin/env python3
"""Configuration loader for tracks, algorithm versions, and driver fields.

Synthesized from both branches: Phase 1.2's API and JSON layout, made robust
with path resolution relative to this file (so it works from any working
directory, not just the repo root) and friendlier errors that list what IS
available when a lookup misses.

Layout under engine/data:
    tracks/<key>.json
    algorithms/<version>/parameters.json
    field/<name>.json   (driver ratings under a top-level "field" key)
"""

from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Dict, List, Optional


class ConfigLoader:
    """Load track, algorithm, and field configs from the data directory."""

    def __init__(self, base_path: Optional[str] = None):
        # Default: the engine/data shipped beside this file. Override with
        # base_path (a repo root) when needed, e.g. in tests.
        if base_path is not None:
            data_root = Path(base_path) / "engine" / "data"
        else:
            data_root = Path(__file__).resolve().parent / "data"
        self.data_root = data_root
        self.tracks_path = data_root / "tracks"
        self.algo_path = data_root / "algorithms"
        self.field_path = data_root / "field"

    # -- loading ------------------------------------------------------------ #
    def load_track_config(self, track_name: str) -> Dict:
        path = self.tracks_path / f"{track_name}.json"
        if not path.is_file():
            raise FileNotFoundError(
                f"No track config '{track_name}'. Available: {self.list_available_tracks()}"
            )
        return self._read(path)

    def load_algorithm_version(self, version: str) -> Dict:
        candidates = [version] if version.startswith("v") else [version, f"v{version}"]
        for cand in candidates:
            path = self.algo_path / cand / "parameters.json"
            if path.is_file():
                return self._read(path)
        raise FileNotFoundError(
            f"No algorithm version '{version}'. Available: {self.list_available_algorithms()}"
        )

    def load_field(self, field_name: str = "default") -> Dict:
        """Return the driver-ratings dict (the contents of the "field" key)."""
        path = self.field_path / f"{field_name}.json"
        if not path.is_file():
            raise FileNotFoundError(f"No field '{field_name}' in {self.field_path}")
        data = self._read(path)
        drivers = data.get("field", data)
        if not drivers:
            raise ValueError(f"Field '{field_name}' has no drivers")
        return drivers

    # -- discovery ---------------------------------------------------------- #
    def list_available_tracks(self) -> List[str]:
        if not self.tracks_path.is_dir():
            return []
        return sorted(p.stem for p in self.tracks_path.glob("*.json"))

    def list_available_algorithms(self) -> List[str]:
        if not self.algo_path.is_dir():
            return []
        return sorted(
            p.name for p in self.algo_path.iterdir()
            if p.is_dir() and (p / "parameters.json").is_file()
        )

    # -- internal ----------------------------------------------------------- #
    @staticmethod
    def _read(path: Path) -> Dict:
        with open(path, "r") as f:
            return json.load(f)
