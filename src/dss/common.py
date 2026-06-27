from __future__ import annotations

from typing import Any

import numpy as np
import pandas as pd


def normalize_player_id(value: Any) -> int | None:
    if value is None:
        return None
    try:
        if pd.isna(value):
            return None
        x = float(value)
        if not np.isfinite(x):
            return None
        return int(x)
    except Exception:
        return None


def normalize_float(value: Any) -> float | None:
    if value is None:
        return None
    try:
        if pd.isna(value):
            return None
        x = float(value)
        if not np.isfinite(x):
            return None
        return x
    except Exception:
        return None
