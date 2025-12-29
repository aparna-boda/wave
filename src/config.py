import os
from pathlib import Path

# Project Root
PROJECT_ROOT = Path(__file__).parent.parent

# Data Paths
DATA_DIR = PROJECT_ROOT / "data"
RAW_DATA_DIR = DATA_DIR / "raw"
LOGS_DIR = DATA_DIR / "logs"

# Ensure directories exist
RAW_DATA_DIR.mkdir(parents=True, exist_ok=True)
LOGS_DIR.mkdir(parents=True, exist_ok=True)

# Sensor Baselines & Thresholds
BASELINE_PH = (7.0, 7.4)
BASELINE_TURBIDITY = (1.0, 2.0)
BASELINE_TDS = (100.0, 300.0)
BASELINE_TEMP = (20.0, 25.0)

# Valid Ranges (Physical Limits)
VALID_RANGE_PH = (0.0, 14.0)
VALID_RANGE_TURBIDITY = (0.0, 1000.0) # Assumed max
VALID_RANGE_TDS = (0.0, 2000.0)       # Assumed max
VALID_RANGE_TEMP = (-10.0, 50.0)

# Model Parameters
ROLLING_WINDOW_SIZE = 24
ANOMALY_CONTAMINATION_RATE_INIT = 0.05
NU_PARAMETER = 0.05
RANDOM_SEED = 42

# File Names
DATASET_FILENAME = RAW_DATA_DIR / "wave_monitoring_data.csv"
DASHBOARD_FILENAME = PROJECT_ROOT / "wave_dashboard.png"
ALERTS_LOG_FILENAME = LOGS_DIR / "alerts_log.json"
LEARNING_METRICS_FILENAME = LOGS_DIR / "learning_metrics.json"
