"""Configuration générale et chemins du projet."""

import os
from pathlib import Path

APP_TITLE = "Gabon GeoAI Lab"
TAGLINE = "Observer · Comprendre · Prédire · Simuler"
PROJECT_STATUS = "Le projet est actuellement en phase de recherche et de conception."

PROJECT_ROOT = Path(__file__).resolve().parent.parent
_data_directory = os.environ.get("GABON_GEOAI_DATA_DIR", "data").strip() or "data"
_data_path = Path(_data_directory).expanduser()
DATA_DIR = (_data_path if _data_path.is_absolute() else PROJECT_ROOT / _data_path).resolve()
RAW_DATA_DIR = DATA_DIR / "raw"
INTERIM_DATA_DIR = DATA_DIR / "interim"
PROCESSED_DATA_DIR = DATA_DIR / "processed"
