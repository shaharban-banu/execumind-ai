"""
Data Transformer.

Performs data cleaning and standardization after schema mapping.
"""
from utils.logger import logger
from config.settings import CANONICAL_TABLES
import pandas as pd
from typing import Dict

class DataTransformer:
    def __init__(self,datasets:dict):
        self.datasets=datasets

    def transform(self):
        logger.info("Starting transformations..........")
        transformed={}

        for tablename,dataframe in self.datasets.items():
            logger.info("Transforming table %s",tablename)

            dataframe=self._convert_dtypes(tablename,dataframe)
            dataframe=self._clean_text(dataframe)
            dataframe=self._handle_missing_values(tablename,dataframe)
            dataframe=self._remove_duplicates(tablename,dataframe)
            dataframe=self._create_features(tablename,dataframe)

            transformed[tablename]=dataframe
        logger.info("Data transformations completed")
        return transformed

    def _convert_dtypes(self,tablename:str,dataframe:pd.DataFrame):
        schema=CANONICAL_TABLES[tablename]['columns']
        for col,config in schema.items():
            if col not in dataframe.columns:
                continue
            dtype=config["dtype"]
            try:
                if dtype=="datetime":
                    dataframe[col]=pd.to_datetime(dataframe[col],errors='coerce')
                elif dtype=='float':
                    dataframe[col]=pd.to_numeric(dataframe[col],errors='coerce')
                elif dtype=='integer':
                    dataframe[col]=pd.to_numeric(dataframe[col],errors='coerce').astype("Int64")
                elif dtype=="string":
                    dataframe[col]=dataframe[col].astype("string")
            except Exception as e:
                logger.warning("unable to convert %s.%s : %s",tablename,col,e)
        return dataframe
    
    def _clean_text(self,dataframe:pd.DataFrame):
        for col in dataframe.select_dtypes(include="string"):
            dataframe[col]=(dataframe[col].str.strip().str.replace(r"\s+"," ",regex=True))
        return dataframe

    def _handle_missing_values(self,tablename,dataframe:pd.DataFrame):
        schema=CANONICAL_TABLES[tablename]['columns']
        for col,config in schema.items():
            if col not in dataframe.columns:
                continue
            dtype=config['dtype']
            if dtype=="string":
                dataframe[col]=dataframe[col].fillna("")
        return dataframe
    
    def _remove_duplicates(self,tablename,dataframe:pd.DataFrame):
        primary_keys=CANONICAL_TABLES[tablename]['primary_keys']
        dataframe=dataframe.drop_duplicates(subset=primary_keys)
        return dataframe
    
    def _create_features(self,table_name: str,dataframe: pd.DataFrame,) :

        if (table_name == "orders"and "order_date" in dataframe.columns):

            dataframe["order_year"] = (dataframe["order_date"].dt.year)
            dataframe["order_month"] = (dataframe["order_date"].dt.month)

        if (table_name == "orders" and "delivered_date" in dataframe.columns and "order_date" in dataframe.columns):

            dataframe["delivery_days"] = (dataframe["delivered_date"] - dataframe["order_date"]).dt.days

        return dataframe