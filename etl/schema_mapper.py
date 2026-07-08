"""
Schema Mapper.

Maps dataset-specific column names to the ExecuMind
canonical schema.
"""
from utils.logger import logger
import pandas as pd
from config.settings import COLUMN_MAPPING,CANONICAL_TABLES
from etl.exceptions import SchemaMappingError

class SchemaMapper:
    def __init__(self,datasets:dict, keep_extra_columns: bool = True,):
        self.datasets=datasets
        self.keep_extra_columns = keep_extra_columns

    def map(self):
        logger.info("Started schema mapping......")
        mapped={}

        for tablename,dataframe in self.datasets.items():
            logger.info("Mapping table : %s",tablename)
            if tablename not in COLUMN_MAPPING:
                raise SchemaMappingError(f"No mapping found for table '{tablename}'")
            
            mapping=COLUMN_MAPPING[tablename]
            dataframe = dataframe.rename(columns=mapping)
            self._validate_required_columns(tablename,dataframe)
            
            if not self.keep_extra_columns:
                dataframe = self._select_canonical_columns(tablename,dataframe,)

            mapped[tablename]=dataframe

        logger.info("Schema mapping completed")
        return mapped
    
    def _validate_required_columns(self,tablename,dataframe:dict):
        schema=CANONICAL_TABLES[tablename]
        required_columns=[]

        for column_name,config in schema['columns'].items():
            if config['required']:
                required_columns.append(column_name)
        missing_columns=[column for column in required_columns if column not in dataframe.columns]
        if missing_columns:
            raise SchemaMappingError(f"""table : {tablename}
                                    missing required canonical columns : {missing_columns}""")
        

    def _select_canonical_columns(self,tablename:str,dataframe:pd.DataFrame):
        canonical_columns=list(CANONICAL_TABLES[tablename]['columns'].keys())
        available_columns=[col for col in canonical_columns if col in dataframe.columns ]
        return dataframe[available_columns]
        
