from __future__ import annotations

from typing import Any
import pandas as pd


def is_missing(value: Any) -> bool:
    try:
        return pd.isna(value)
    except Exception:
        return value is None


def first(row: pd.Series | dict[str, Any], candidates: list[str], default: Any = None) -> Any:
    for col in candidates:
        try:
            if col in row:
                value = row[col]
                if not is_missing(value) and str(value).strip() != "":
                    return value
        except Exception:
            continue
    return default


def safe_float(value: Any) -> float | None:
    if is_missing(value):
        return None
    try:
        return float(value)
    except Exception:
        return None


def safe_int(value: Any) -> int | None:
    if is_missing(value):
        return None
    try:
        return int(float(value))
    except Exception:
        return None


def safe_str(value: Any) -> str | None:
    if is_missing(value):
        return None
    text = str(value).strip()
    return text if text else None
