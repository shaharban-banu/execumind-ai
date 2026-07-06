"""
Application configuration.

Loads project paths and dataset configuration from YAML.
"""
from pathlib import Path
import yaml

#project paths
#----------------------

BASE_DIR = Path(__file__).resolve().parent.parent

DATA_DIR = BASE_DIR / "data"

SQLITE_DIR = DATA_DIR / "sqlite"

SQLITE_DIR.mkdir(parents=True, exist_ok=True)

DATABASE_URL = f"sqlite:///{SQLITE_DIR}/execumind.db"

CONNECTORS_DIR = BASE_DIR / "connectors"

#Dataset configuration
#--------------------------

CONFIG_FILE=BASE_DIR/"config"/"dataset_config.yaml"

with open(CONFIG_FILE,"r",encoding='utf-8') as file:
    CONFIG=yaml.safe_load(file)

#Dataset information
#--------------------------
DATASET=CONFIG["dataset"]
DATASET_NAME=DATASET["name"]
CONNECTOR=DATASET["connector"]
RAW_DATA_PATH=BASE_DIR/DATASET["raw_path"]

#validation rule
#--------------------------
VALIDATION=CONFIG["validation"]
REQUIRED_TABLES=VALIDATION["required_tables"]
OPTIONAL_TABLES=VALIDATION["optional_tables"]

#Table configuration
#-------------------------------
TABLES=CONFIG["tables"]