from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]

DATA_DIR = ROOT / "data"
RAW_DATA_DIR = DATA_DIR / "raw"
INTERIM_DATA_DIR = DATA_DIR / "interim"
PROCESSED_DATA_DIR = DATA_DIR / "processed"
EXTERNAL_DATA_DIR = DATA_DIR / "external"

REPORTS_DIR = ROOT / "reports"
FIGURES_DIR = REPORTS_DIR / "figures"
TABLES_DIR = REPORTS_DIR / "tables"
RANKINGS_DIR = REPORTS_DIR / "rankings"
SCOUTING_REPORTS_DIR = REPORTS_DIR / "scouting_reports"
MODEL_DIAGNOSTICS_DIR = REPORTS_DIR / "model_diagnostics"

ARTIFACTS_DIR = ROOT / "artifacts"
MODEL_ARTIFACTS_DIR = ARTIFACTS_DIR / "models"
SCALERS_DIR = ARTIFACTS_DIR / "scalers"
ENCODERS_DIR = ARTIFACTS_DIR / "encoders"
FEATURE_IMPORTANCE_DIR = ARTIFACTS_DIR / "feature_importance"
PREDICTIONS_DIR = ARTIFACTS_DIR / "predictions"

LOGS_DIR = ROOT / "logs"
CONFIG_DIR = ROOT / "config"
NOTEBOOKS_DIR = ROOT / "notebooks"