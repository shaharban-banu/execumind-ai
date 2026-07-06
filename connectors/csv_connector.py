"""csv connector
load all csv files into pandas dataframe
"""
from pathlib import Path
from utils.logger import logger
import pandas as pd
from connectors.base_connector import BaseConnector
from config.settings import RAW_DATA_PATH,TABLES

class CSVConnector(BaseConnector):
    def load_tables(self):
        datasets={}
        logger.info("Loading CSV dataset.....")
        for tablename,table_config in TABLES.items():
            if not table_config.get("enabled",True):
                logger.info("Skipping disabled table: %s",tablename)
                continue
            filename=table_config["file"]
            filepath=Path(RAW_DATA_PATH)/filename
            if not filepath.exists():
                logger.warning("File not found for table %s :%s",tablename,filepath)
                continue
            logger.info("loading %s ....",filename)
            datasets[tablename]=pd.read_csv(filepath)

        logger.info("Loaded %d tables",len(datasets))
        return datasets