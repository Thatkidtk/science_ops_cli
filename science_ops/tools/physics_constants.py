from __future__ import annotations

from typing import Dict

# Fundamental constants
C = 2.99792458e8  # m/s
G = 6.67430e-11   # m^3 kg^-1 s^-2

# Common celestial bodies with useful parameters
BODIES: Dict[str, Dict[str, float]] = {
    "earth": {
        "name": "Earth",
        "mass": 5.97219e24,
        "radius": 6.371e6,
        "mu": 3.986004418e14,
        "g": 9.80665,
    },
    "venus": {
        "name": "Venus",
        "mass": 4.8675e24,
        "radius": 6.0518e6,
        "mu": 3.24859e14,
        "g": 8.87,
    },
    "moon": {
        "name": "Moon",
        "mass": 7.342e22,
        "radius": 1.7374e6,
        "mu": 4.9048695e12,
        "g": 1.62,
    },
    "mars": {
        "name": "Mars",
        "mass": 6.4171e23,
        "radius": 3.3895e6,
        "mu": 4.282837e13,
        "g": 3.721,
    },
    "jupiter": {
        "name": "Jupiter",
        "mass": 1.89813e27,
        "radius": 6.9911e7,
        "mu": 1.26686534e17,
        "g": 24.79,
    },
    "saturn": {
        "name": "Saturn",
        "mass": 5.6834e26,
        "radius": 5.8232e7,
        "mu": 3.7931187e16,
        "g": 10.44,
    },
    "sun": {
        "name": "Sun",
        "mass": 1.98847e30,
        "radius": 6.9634e8,
        "mu": 1.32712440018e20,
        "g": 274.0,
    },
}


def get_body(name: str) -> Dict[str, float]:
    key = name.lower()
    if key not in BODIES:
        raise KeyError(f"Unknown body '{name}'")
    return BODIES[key]


def known_bodies() -> str:
    return ", ".join(sorted(BODIES))
