import os
from pathlib import Path

# Project paths
BASE_DIR = Path(__file__).resolve().parent.parent
MODEL_DIR = BASE_DIR / "models" / "deberta-v3-base-zeroshot"

# Model configuration
MODEL_NAME = "MoritzLaurer/deberta-v3-base-zeroshot-v2.0"
DEFAULT_THRESHOLD = 0.5

# API configuration
API_TITLE = "Log Anomaly Detection API"
API_VERSION = "1.0.0"
API_DESCRIPTION = """
Log Anomaly Detection API using Zero-Shot Classification.

This API analyzes log messages and classifies them as either 'anomaly' or 'normal'
using a pre-trained DeBERTa model.
"""

# Labels for classification
CLASSIFICATION_LABELS = ["anomaly", "normal"]
