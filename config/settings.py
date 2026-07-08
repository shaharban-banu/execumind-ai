"""
Application configuration.

Loads:
- Project paths
- Database settings
- Dataset configuration
- Canonical schema
- Column mappings
- Capability definitions
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

CONFIG_DIR=BASE_DIR/"config"

def load_yaml(filename:str):
    filepath=CONFIG_DIR/filename
    if not filepath.exists():
        raise FileNotFoundError(f"configuration file not found :{filepath}")

    with open(filepath,"r",encoding='utf-8') as file:
        return yaml.safe_load(file)
    
#Load configuration
#----------------------
DATASET_CONFIG=load_yaml("dataset_config.yaml")
CANONICAL_SCHEMA = load_yaml("canonical_schema.yaml")
COLUMN_MAPPING = load_yaml("column_mapping.yaml")
CAPABILITIES = load_yaml("capabilities.yaml")


#Dataset information
#--------------------------
DATASET=DATASET_CONFIG["dataset"]
DATASET_NAME=DATASET["name"]
CONNECTOR=DATASET["connector"]
RAW_DATA_PATH=BASE_DIR/DATASET["raw_path"]

#validation rule
#--------------------------
VALIDATION=DATASET_CONFIG["validation"]
REQUIRED_TABLES=VALIDATION["required_tables"]
OPTIONAL_TABLES=VALIDATION["optional_tables"]

#Table configuration
#-------------------------------
TABLES=DATASET_CONFIG["tables"]

#canonical schema
#--------------------
CANONICAL_TABLES = CANONICAL_SCHEMA["tables"]

#column mapping
#---------------------
COLUMN_MAPPINGS = COLUMN_MAPPING

#capabilities
#-------------
SYSTEM_CAPABILITIES = CAPABILITIES["capabilities"]