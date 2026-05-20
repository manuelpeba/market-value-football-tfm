"""
Especificaciones econométricas del proyecto.

Este módulo centraliza:
- variable objetivo
- features baseline
- features avanzadas
- features de crecimiento
- fixed effects
- columnas excluidas por leakage

La lógica de entrenamiento debe importar estas listas para evitar
hardcoding en los pipelines.
"""

ECONOMETRIC_TARGET = "log_market_value_eur"


# ==========================================================
# BASELINE FEATURES
# ==========================================================

BASE_OLS_FEATURES = [
    "age",
    "log_minutes_played",
    "goals_per90",
    "assists_per90",
]


# ==========================================================
# POSITIONAL NORMALIZATION FEATURES
# ==========================================================

ADVANCED_OLS_FEATURES = [
    "age",
    "log_minutes_played",
    "goals_per90",
    "assists_per90",
    "goals_per90_pos_z",
    "assists_per90_pos_z",
    "goals_position_percentile",
    "assists_position_percentile",
]


# ==========================================================
# GROWTH / TEMPORAL DYNAMICS FEATURES
# ==========================================================
# Versión conservadora:
# no incluye market_value_growth_prev ni delta_log_market_value_prev
# para evitar introducir una dependencia excesiva del target.

GROWTH_OLS_FEATURES = [
    "age",
    "age_squared",
    "career_year",
    "log_minutes_played",
    "goals_per90",
    "assists_per90",
    "breakout_indicator",
    "finishing_index",
    "playmaking_index",
    "experience_index",
]


# ==========================================================
# FIXED EFFECTS
# ==========================================================

FIXED_EFFECTS = [
    "league",
    "season",
    "position_group",
]


# ==========================================================
# LEAKAGE CONTROL
# ==========================================================

LEAKAGE_COLUMNS = [
    "market_value_next_eur",
    "market_value_growth_1y",
    "delta_log_market_value_1y",
    "predicted_log_market_value",
    "predicted_market_value_eur",
    "market_value_gap_eur",
    "market_value_gap_pct",
    "inefficiency_score",
    "inefficiency_score_z",
    "opportunity_score",
    "growth_score",
    "confidence_score",
]


# ==========================================================
# MODEL REGISTRY
# ==========================================================

OLS_MODEL_SPECS = {
    "baseline_ols": {
        "target": ECONOMETRIC_TARGET,
        "features": BASE_OLS_FEATURES,
        "fixed_effects": FIXED_EFFECTS,
        "description": (
            "OLS baseline with core performance features and contextual fixed effects."
        ),
    },
    "advanced_positional_ols": {
        "target": ECONOMETRIC_TARGET,
        "features": ADVANCED_OLS_FEATURES,
        "fixed_effects": FIXED_EFFECTS,
        "description": (
            "OLS with positional and league-normalized performance features."
        ),
    },
    "growth_ols": {
        "target": ECONOMETRIC_TARGET,
        "features": GROWTH_OLS_FEATURES,
        "fixed_effects": FIXED_EFFECTS,
        "description": (
            "OLS with conservative temporal dynamics and player growth features."
        ),
    },
}


# ==========================================================
# ACCESSORS
# ==========================================================

def get_ols_features(model_name: str) -> list[str]:
    """
    Return feature list for a registered OLS specification.
    """

    if model_name not in OLS_MODEL_SPECS:
        available = ", ".join(OLS_MODEL_SPECS.keys())
        raise ValueError(
            f"Unknown OLS model specification: {model_name}. "
            f"Available specs: {available}"
        )

    return OLS_MODEL_SPECS[model_name]["features"]


def get_ols_fixed_effects(model_name: str) -> list[str]:
    """
    Return fixed effects for a registered OLS specification.
    """

    if model_name not in OLS_MODEL_SPECS:
        available = ", ".join(OLS_MODEL_SPECS.keys())
        raise ValueError(
            f"Unknown OLS model specification: {model_name}. "
            f"Available specs: {available}"
        )

    return OLS_MODEL_SPECS[model_name]["fixed_effects"]


def get_ols_target(model_name: str) -> str:
    """
    Return target variable for a registered OLS specification.
    """

    if model_name not in OLS_MODEL_SPECS:
        available = ", ".join(OLS_MODEL_SPECS.keys())
        raise ValueError(
            f"Unknown OLS model specification: {model_name}. "
            f"Available specs: {available}"
        )

    return OLS_MODEL_SPECS[model_name]["target"]


def get_ols_description(model_name: str) -> str:
    """
    Return description for a registered OLS specification.
    """

    if model_name not in OLS_MODEL_SPECS:
        available = ", ".join(OLS_MODEL_SPECS.keys())
        raise ValueError(
            f"Unknown OLS model specification: {model_name}. "
            f"Available specs: {available}"
        )

    return OLS_MODEL_SPECS[model_name]["description"]