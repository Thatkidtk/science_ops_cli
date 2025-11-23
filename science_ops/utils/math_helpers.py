from __future__ import annotations

from typing import Iterable, Tuple

import numpy as np


def describe(data: Iterable[float]) -> dict:
    arr = np.array(list(data), dtype=float)
    if arr.size == 0:
        raise ValueError("No data provided")

    return {
        "count": int(arr.size),
        "mean": float(arr.mean()),
        "std": float(arr.std(ddof=1)) if arr.size > 1 else 0.0,
        "min": float(arr.min()),
        "max": float(arr.max()),
        "median": float(np.median(arr)),
    }


def linspace(start: float, stop: float, num: int) -> np.ndarray:
    return np.linspace(start, stop, num=num)
